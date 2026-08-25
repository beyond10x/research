"""Resumable batch classification with two interchangeable backends.

backend=cli  -> `claude -p` (subscription auth; no API credits needed) [default]
backend=api  -> Messages API with structured outputs (needs ANTHROPIC_API_KEY credit)

The CLI backend cannot enforce a JSON schema server-side, so the schema is inlined
in the system prompt and the reply is validated here, with one repair retry.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import usage_cost

_lock = threading.Lock()
COST = {"usd": 0.0, "calls": 0, "in": 0, "out": 0, "fail": 0}
FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.S)


def _account(model: str, usage: dict, reported: float | None = None) -> None:
    with _lock:
        COST["usd"] += reported if reported is not None else usage_cost(model, usage)
        COST["calls"] += 1
        COST["in"] += (usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0)
                       + usage.get("cache_creation_input_tokens", 0))
        COST["out"] += usage.get("output_tokens", 0)


def _extract_json(text: str) -> dict:
    text = (text or "").strip()
    m = FENCE.search(text)
    if m:
        text = m.group(1).strip()
    start = min([i for i in (text.find("{"), text.find("[")) if i >= 0], default=-1)
    if start > 0:
        text = text[start:]
    return json.loads(text)


# --------------------------------------------------------------------------- cli
def _call_cli(system: str, user: str, model: str, effort: str, timeout: int) -> dict:
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    cmd = ["claude", "-p", "--model", model, "--output-format", "json",
           "--no-session-persistence", "--strict-mcp-config", "--system-prompt", system]
    proc = subprocess.run(cmd, input=user, capture_output=True, text=True, env=env, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"claude exit {proc.returncode}: {proc.stderr[-300:]}")
    envelope = json.loads(proc.stdout)
    _account(model, envelope.get("usage") or {}, envelope.get("total_cost_usd"))
    if envelope.get("is_error"):
        raise RuntimeError(f"claude error: {str(envelope.get('result'))[:200]}")
    return _extract_json(envelope.get("result", ""))


# --------------------------------------------------------------------------- api
_client = None


def _api_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(max_retries=5)
    return _client


def _call_api(system: str, user: str, schema: dict, model: str, effort: str, max_tokens: int) -> dict:
    resp = _api_client().messages.create(
        model=model, max_tokens=max_tokens,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user}],
        output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
    )
    _account(model, resp.usage.model_dump())
    if resp.stop_reason == "refusal":
        raise RuntimeError("refusal")
    return json.loads(next(b.text for b in resp.content if b.type == "text"))


def call_json(system: str, user: str, schema: dict, model: str, effort: str = "medium",
              backend: str = "cli", max_tokens: int = 8000, timeout: int = 600) -> dict:
    sys_full = system
    if backend == "cli":
        sys_full = (system + "\n\nReturn ONE JSON object matching this JSON Schema exactly. "
                    "No prose, no markdown fence, no commentary.\n" + json.dumps(schema))
    last = None
    for attempt in range(3):
        try:
            if backend == "cli":
                return _call_cli(sys_full, user, model, effort, timeout)
            return _call_api(sys_full, user, schema, model, effort, max_tokens)
        except Exception as exc:  # transient API/CLI/parse failures are all retryable here
            last = exc
            time.sleep(3 * (attempt + 1))
    with _lock:
        COST["fail"] += 1
    return {"_error": f"{type(last).__name__}: {str(last)[:200]}"}


def run_batches(batches, fn, out_path: Path, key_fn, workers: int = 6) -> int:
    """Map fn over batches, appending to out_path. Keys already present are skipped,
    so an interrupted run resumes where it stopped."""
    done = set()
    if out_path.exists():
        for line in out_path.open(errors="replace"):
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "_error" not in rec:
                done.add(rec.get("_batch"))
    todo = [b for b in batches if key_fn(b) not in done]
    print(f"{out_path.name}: {len(done)} batches cached, {len(todo)} to run", flush=True)
    if not todo:
        return 0
    written = 0
    t0 = time.time()
    with out_path.open("a") as fh, ThreadPoolExecutor(max_workers=workers) as pool:
        for i, rows in enumerate(pool.map(fn, todo), 1):
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                written += 1
            fh.flush()
            if i % 5 == 0 or i == len(todo):
                rate = i / max(time.time() - t0, 1e-9)
                print(f"  {i}/{len(todo)} batches  ${COST['usd']:.2f}  "
                      f"{rate * 60:.1f}/min  fails={COST['fail']}", flush=True)
    return written

"""Shared constants and helpers for the session-transcript research pipeline."""
from __future__ import annotations

import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
OUT = REPO / "out"
PROJECTS = Path(os.environ.get("CLAUDE_PROJECTS", Path.home() / ".claude" / "projects"))

# $/MTok (input, output). Source: bundled claude-api skill, model table cached 2026-06-24.
PRICES = {
    "claude-opus-5": (5.0, 25.0),
    "claude-opus-4-8": (5.0, 25.0),
    "claude-opus-4-7": (5.0, 25.0),
    "claude-opus-4-6": (5.0, 25.0),
    "claude-fable-5": (10.0, 50.0),
    "claude-mythos-5": (10.0, 50.0),
    "claude-sonnet-5": (2.0, 10.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
    "claude-haiku-4-5-20251001": (1.0, 5.0),
}
# Fast mode (research preview) reprices Opus 5 / 4.8 at Fable rates.
FAST_PRICES = {"claude-opus-5": (10.0, 50.0), "claude-opus-4-8": (10.0, 50.0)}
CACHE_READ_MULT = 0.1
CACHE_WRITE_5M_MULT = 1.25
CACHE_WRITE_1H_MULT = 2.0


def usage_cost(model: str, usage: dict) -> float:
    """Dollar cost of one assistant response from its usage block."""
    if not usage:
        return 0.0
    speed = usage.get("speed")
    table = FAST_PRICES if speed == "fast" and model in FAST_PRICES else PRICES
    if model not in table:
        return 0.0
    pin, pout = table[model]
    cc = usage.get("cache_creation") or {}
    w1h = cc.get("ephemeral_1h_input_tokens", 0)
    w5m = cc.get("ephemeral_5m_input_tokens", 0)
    if not (w1h or w5m):  # older records only carry the aggregate
        w5m = usage.get("cache_creation_input_tokens", 0)
    tok = (
        usage.get("input_tokens", 0)
        + usage.get("cache_read_input_tokens", 0) * CACHE_READ_MULT
        + w5m * CACHE_WRITE_5M_MULT
        + w1h * CACHE_WRITE_1H_MULT
    )
    return tok / 1e6 * pin + usage.get("output_tokens", 0) / 1e6 * pout


def jl_write(path: Path, rows) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def jl_read(path: Path):
    with Path(path).open(errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def text_of(content) -> str:
    """Flatten a message content field to plain text."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for b in content:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "text":
            parts.append(b.get("text", ""))
        elif b.get("type") == "thinking":
            continue
    return "\n".join(parts)

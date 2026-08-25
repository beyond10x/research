#!/usr/bin/env python3
"""Stage 6 - turn the evidence into a catalogue of candidate runnable workflows.

One call per workflow archetype. The model gets only what the earlier stages measured:
the recipes actually executed, the human turns that occurred inside those sessions, the
mined operation motifs, and the blockers. It returns a spec someone could implement.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict

from common import DATA, OUT, jl_read
from llm import COST, call_json, run_batches

SPEC_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "kebab-case workflow name"},
        "one_line": {"type": "string", "description": "what it does, <=15 words"},
        "trigger": {"type": "string", "description": "the observable event that should start it, not a human typing"},
        "preconditions": {"type": "array", "items": {"type": "string"}},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "op": {"type": "string", "description": "imperative step, tool-level"},
                    "kind": {"type": "string", "enum": ["deterministic", "agent", "gate"]},
                    "fails_if": {"type": "string", "description": "the check that makes this step verifiable, or ''"},
                },
                "required": ["op", "kind", "fails_if"],
                "additionalProperties": False,
            },
        },
        "human_gates": {"type": "array", "items": {"type": "string"},
                        "description": "points where a human must still decide, and what they decide"},
        "autonomy": {"type": "string", "enum": ["full_auto", "auto_with_gates", "assisted"]},
        "removes_turns": {"type": "string", "description": "which observed human turn types this eliminates"},
        "blockers": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "number"},
    },
    "required": ["name", "one_line", "trigger", "preconditions", "steps", "human_gates",
                 "autonomy", "removes_turns", "blockers", "confidence"],
    "additionalProperties": False,
}

SYSTEM = """You design runnable workflows from observed agent-session evidence.

You are given one workflow archetype: the recipes that were actually executed across N real
sessions, the human turns that occurred inside them, the mined operation motifs, and the blockers
another pass identified. Produce ONE workflow spec that could run this archetype with as little
human involvement as the evidence supports.

Rules:
- The trigger must be a machine-observable event (a webhook, a file change, a failing gate, a cron
  tick, a queue item), never "the human asks".
- Every step is deterministic (a script/CLI a human could read), agent (needs a model), or gate
  (a check that can fail the run). Prefer deterministic. An agent step that could be a script is a
  design smell.
- `fails_if` makes a step verifiable. If a step has no failure check, say so with an empty string -
  do not invent one.
- human_gates: only where the evidence shows a human contributed authority, taste, business
  priority or outside-the-machine information. If the evidence shows the human only said
  "yes"/"continue"/"go on", that is NOT a gate - drop it and say so in removes_turns.
- blockers: what is actually missing today. Be specific and concrete.
- Do not invent capabilities. Ground every step in something the transcripts show happening."""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--backend", default="cli", choices=["cli", "api"])
    ap.add_argument("--effort", default="high")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--min-sessions", type=int, default=3)
    args = ap.parse_args()

    mining = json.loads((OUT / "mining.json").read_text())
    slabels = [r for r in jl_read(DATA / "session_labels.jsonl") if "_error" not in r]
    turns = {f"{t['session_id']}#{t['turn_idx']}": t for t in jl_read(DATA / "turns.jsonl")}
    tlabels = [r for r in jl_read(DATA / "turn_labels.jsonl") if "_error" not in r and r.get("id")]
    tl_by_sess = defaultdict(list)
    for r in tlabels:
        tl_by_sess[r["id"].split("#")[0]].append(r)

    by_arch = defaultdict(list)
    for r in slabels:
        by_arch[r["workflow_archetype"]].append(r)
    archs = [(k, v) for k, v in sorted(by_arch.items(), key=lambda kv: -len(kv[1]))
             if len(v) >= args.min_sessions and k != "other"]

    def work(item):
        arch, rows = item
        sample_turns = []
        for r in rows[:12]:
            for tl in tl_by_sess.get(r["session_id"], [])[:6]:
                t = turns.get(tl["id"])
                if t:
                    sample_turns.append({
                        "intent": tl["intent"], "replaceable_by": tl["replaceable_by"],
                        "novel_information": tl["novel_information"],
                        "rule": tl["rule_sketch"], "text": t["text"][:160]})
        payload = {
            "archetype": arch,
            "sessions_observed": len(rows),
            "outcomes": dict(Counter(r["outcome"] for r in rows)),
            "verdicts": dict(Counter(r["automation_verdict"] for r in rows)),
            "recipes_executed": [r["steps"] for r in rows[:14]],
            "human_essential_moments": [m for r in rows for m in r.get("human_essential_moments", [])][:25],
            "blockers_reported": Counter(b.lower().strip() for r in rows
                                         for b in r.get("automation_blockers", [])).most_common(12),
            "human_turns_sample": sample_turns[:45],
            "mined_operation_motifs": [m["motif"] for m in mining.get("op_motifs_per_session", [])[:12]],
        }
        res = call_json(SYSTEM, json.dumps(payload, ensure_ascii=False)[:60000],
                        SPEC_SCHEMA, args.model, args.effort, backend=args.backend)
        return [{"_batch": arch, "archetype": arch, "sessions_observed": len(rows), **res}]

    n = run_batches(archs, work, DATA / "workflow_specs.jsonl",
                    key_fn=lambda item: item[0], workers=args.workers)
    print(f"wrote {n} workflow specs; spend ${COST['usd']:.2f} over {COST['calls']} calls")


if __name__ == "__main__":
    main()

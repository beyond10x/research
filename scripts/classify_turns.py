#!/usr/bin/env python3
"""Stage 2 - label every human turn on the axes in taxonomy.py.

Turns are batched per session so the classifier sees them in order and can tell
"the human is repairing the agent" from "the human is opening new work".
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict

from common import DATA, jl_read
from llm import COST, call_json, run_batches
from taxonomy import INTENT, MOTIVATION, NOVEL_INFO, REPLACEABLE_BY, SENTIMENT, TASK_KIND, TURN_SCHEMA

SYSTEM = f"""You classify HUMAN turns from Claude Code coding-agent transcripts.

The research question is: **which of these human turns could be replaced by a deterministic
script, by a fixed agent policy, or by another AI - and which genuinely needed the human?**
Label honestly against that question; do not flatter the human or the agent.

For every turn you get: what the agent had just said, what the human typed, and what the agent
then did (its tool calls). Judge the turn in that context.

INTENT (pick exactly one, the dominant one):
{chr(10).join(f"- {k}: {v}" for k, v in INTENT.items())}

TASK_KIND: {", ".join(TASK_KIND)}
MOTIVATION: {", ".join(MOTIVATION)}
SENTIMENT: {", ".join(SENTIMENT)} (terse_pressing = clipped/imperative but not angry)

NOVEL_INFORMATION - what did the human contribute that was not already available?
{chr(10).join(f"- {k}: {v}" for k, v in NOVEL_INFO.items())}

REPLACEABLE_BY - the core axis. Be strict:
{chr(10).join(f"- {k}: {v}" for k, v in REPLACEABLE_BY.items())}
A turn that only says "yes/go on/do it/continue" after the agent proposed a plan is almost always
deterministic_rule or ai_policy, not human_only. A turn carrying taste, business priority, external
observation or accountability for an irreversible act is human_only.

rule_sketch: when replaceable_by is deterministic_rule or ai_policy, write the rule as
"<trigger> -> <action>", at most 15 words. Otherwise empty string.

is_rework: true when this turn would not exist if the agent had done the previous step correctly
and completely.

Return one entry per input turn, same ids, same order."""


def render(t: dict, total: int) -> str:
    tools = t.get("tool_detail") or []
    return json.dumps({
        "id": f"{t['session_id']}#{t['turn_idx']}",
        "position": f"{t['turn_idx'] + 1}/{total}",
        "entered_via": t["source"],
        "seconds_agent_waited": t.get("idle_before_s"),
        "interrupted_a_running_agent": t.get("interrupted_agent"),
        "agent_said_just_before": (t.get("prev_assistant_tail") or "")[-700:],
        "HUMAN_TYPED": t["text"][:1500],
        "agent_then_ran": tools[:12],
        "agent_replied": (t.get("assistant_reply_head") or "")[:300],
    }, ensure_ascii=False)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--backend", default="cli", choices=["cli", "api"])
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit-batches", type=int, default=0)
    args = ap.parse_args()

    turns = [t for t in jl_read(DATA / "turns.jsonl") if t["source"] != "sdk"]
    by_session = defaultdict(list)
    for t in turns:
        by_session[t["session_id"]].append(t)

    batches = []
    for sid, ts in by_session.items():
        ts.sort(key=lambda x: x["turn_idx"])
        for i in range(0, len(ts), args.batch):
            batches.append({"sid": sid, "i": i, "turns": ts[i:i + args.batch], "total": len(ts)})
    if args.limit_batches:
        batches = batches[: args.limit_batches]

    def work(b):
        payload = "\n".join(render(t, b["total"]) for t in b["turns"])
        res = call_json(SYSTEM, f"Classify these {len(b['turns'])} turns:\n{payload}",
                        TURN_SCHEMA, args.model, args.effort, backend=args.backend)
        if "_error" in res:
            return [{"_batch": f"{b['sid']}:{b['i']}", "_error": res["_error"]}]
        out = []
        for lbl in res.get("labels", []):
            out.append({"_batch": f"{b['sid']}:{b['i']}", **lbl})
        return out

    n = run_batches(batches, work, DATA / "turn_labels.jsonl",
                    key_fn=lambda x: x["_batch"] if "_batch" in x else f"{x['sid']}:{x['i']}",
                    workers=args.workers)
    print(f"wrote {n} labels; api spend ${COST['usd']:.2f} over {COST['calls']} calls")


if __name__ == "__main__":
    main()

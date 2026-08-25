#!/usr/bin/env python3
"""Stage 3 - one label set per session: what it was for, whether it worked,
which workflow archetype it instantiates, and how automatable that archetype is."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict

from common import DATA, jl_read
from llm import COST, call_json, run_batches
from taxonomy import SESSION_SCHEMA

SYSTEM = """You analyse whole Claude Code coding-agent sessions.

You get a session digest: the metrics, the ordered list of what the human typed, the tools the
agent ran, and the agent's final message. From that, judge:

1. goal - what the session was for.
2. outcome - success / partial / failed / abandoned / open_ended.
   Judge on evidence: did the artifact get produced, did gates pass, did the human stop mid-flight,
   did the last message report completion or a blocker? "abandoned" = the human walked away mid-task.
   "open_ended" = exploration or chat with no completion criterion.
3. workflow_archetype - the reusable shape of the work, from the enum.
4. steps - the recipe that was actually executed, 3-10 imperative tool-level steps. Write them so
   another engineer could turn them into a script: "read the failing test", "patch module X",
   "run the gate", "open a PR". Not prose, not narration.
5. human_essential_moments - list ONLY the turns where a human was genuinely irreplaceable
   (authority for an irreversible act, taste, business priority, information from outside the
   machine). If the human added nothing a policy or script could not have added, return [].
6. automation_verdict:
   - full_auto: this session could run end to end unattended today
   - auto_with_gates: unattended with a small number of approval/verification checkpoints
   - needs_human_judgment: a human must make substantive calls mid-flight
   - not_automatable: the value was the human thinking, not the execution
7. automation_blockers - concrete things standing in the way (missing tests, no gate, ambiguous
   spec, credentials, external system access, ...). Empty if none.
8. rework_share - how much of the session was the human repairing the agent's own output.

Be blunt. Most sessions are more automatable than their participants think, but say so only when
the evidence supports it."""


def digest(s: dict, turns: list[dict]) -> str:
    tools = sorted(s["tools"].items(), key=lambda kv: -kv[1])[:12]
    lines = []
    for t in turns:
        lines.append(f"  [{t['turn_idx']}] ({t['source']}, +{t['tool_count']} tools) "
                     f"{t['text'][:200].replace(chr(10), ' ')}")
    return json.dumps({
        "project": s["project"],
        "title": s["title"],
        "branch": s["git_branch"],
        "headless_no_human": s["headless"],
        "duration_min": round(s["duration_s"] / 60, 1),
        "human_turns": s["human_turns"],
        "agent_messages": s["assistant_msgs"],
        "tool_calls": s["tool_calls"],
        "top_tools": dict(tools),
        "slash_commands": s["slash_commands"][:20],
        "skills_loaded": s["skills_loaded"],
        "subagents_spawned": s["subagents_spawned"],
        "files_edited": s["files_edited_n"],
        "git_commits": s["commits"],
        "user_interruptions": s["interruptions"],
        "context_compactions": s["compactions"],
        "api_errors": s["api_errors"],
        "tool_errors": s["tool_errors"],
        "cost_usd_api_equiv": s["cost_usd"],
    }, ensure_ascii=False) + "\n\nHUMAN TURNS IN ORDER:\n" + ("\n".join(lines) or "  (none - headless run)") \
        + "\n\nAGENT'S FINAL MESSAGE:\n" + (s["last_assistant_tail"] or "")[-1500:]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--backend", default="cli", choices=["cli", "api"])
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    by_session = defaultdict(list)
    for t in jl_read(DATA / "turns.jsonl"):
        by_session[t["session_id"]].append(t)
    sessions = list(jl_read(DATA / "sessions.jsonl"))
    if args.limit:
        sessions = sessions[: args.limit]

    def work(s):
        d = digest(s, sorted(by_session[s["session_id"]], key=lambda x: x["turn_idx"]))
        res = call_json(SYSTEM, "Analyse this session:\n" + d, SESSION_SCHEMA,
                        args.model, args.effort, backend=args.backend)
        row = {"_batch": s["session_id"], "session_id": s["session_id"], "project": s["project"]}
        row.update(res)
        return [row]

    n = run_batches(sessions, work, DATA / "session_labels.jsonl",
                    key_fn=lambda s: s["session_id"], workers=args.workers)
    print(f"wrote {n} session labels; spend ${COST['usd']:.2f} over {COST['calls']} calls")


if __name__ == "__main__":
    main()

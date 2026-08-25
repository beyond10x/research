#!/usr/bin/env python3
"""Stage 5 - render out/REPORT.md from the extracted tables, labels and mined motifs."""
from __future__ import annotations

import json
import statistics as st
from collections import Counter, defaultdict
from datetime import datetime, timezone

from common import DATA, OUT, jl_read


def pct(x: float) -> str:
    return f"{x * 100:.0f}%"


def table(headers, rows) -> str:
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def main() -> None:
    sessions = list(jl_read(DATA / "sessions.jsonl"))
    turns = [t for t in jl_read(DATA / "turns.jsonl") if t["source"] != "sdk"]
    mining = json.loads((OUT / "mining.json").read_text())
    labels = {r["id"]: r for r in jl_read(DATA / "turn_labels.jsonl")
              if "_error" not in r and r.get("id")} if (DATA / "turn_labels.jsonl").exists() else {}
    slabels = {r["session_id"]: r for r in jl_read(DATA / "session_labels.jsonl")
               if "_error" not in r} if (DATA / "session_labels.jsonl").exists() else {}
    by_id = {s["session_id"]: s for s in sessions}

    span = (min(s["start_ts"] for s in sessions if s["start_ts"]),
            max(s["end_ts"] for s in sessions if s["end_ts"]))
    fmt = lambda t: datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d")

    L = []
    A = L.append
    A("# Where does the human actually sit in the loop?")
    A("")
    A(f"*Corpus: {len(sessions)} Claude Code sessions, {fmt(span[0])} to {fmt(span[1])}. "
      f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}.*")
    A("")

    # ---------------------------------------------------------------- corpus
    A("## 1. Corpus")
    A("")
    tot_cost = sum(s["cost_usd"] for s in sessions)
    A(table(["metric", "value"], [
        ("sessions", len(sessions)),
        ("&nbsp;&nbsp;of which headless (`claude -p`, no human)", sum(s["headless"] for s in sessions)),
        ("distinct projects", len({s["project"] for s in sessions})),
        ("human turns", len(turns)),
        ("agent messages", f"{sum(s['assistant_msgs'] for s in sessions):,}"),
        ("tool calls", f"{sum(s['tool_calls'] for s in sessions):,}"),
        ("sub-agents spawned", f"{sum(s['subagents_spawned'] for s in sessions):,}"),
        ("output tokens", f"{sum(s['out_tok'] for s in sessions):,}"),
        ("cache-read tokens", f"{sum(s['cache_read_tok'] for s in sessions):,}"),
        ("API-list-price equivalent", f"${tot_cost:,.0f}"),
        ("wall-clock across sessions (sessions overlap)",
         f"{sum(s['duration_s'] for s in sessions) / 3600:,.0f} h"),
        ("&nbsp;&nbsp;active, gaps over 5 min excluded",
         f"{sum(s['active_s'] for s in sessions) / 3600:,.0f} h"),
        ("tool calls per human turn (median)", mining["turn_shape"]["median_tools_triggered"]),
    ]))
    A("")
    proj = defaultdict(lambda: [0, 0, 0.0, 0])
    for s in sessions:
        p = proj[s["project"].replace("-home-timo-", "").replace("-home-timo", "~")]
        p[0] += 1
        p[1] += s["human_turns"]
        p[2] += s["cost_usd"]
        p[3] += s["tool_calls"]
    A("<details><summary>by project</summary>")
    A("")
    A(table(["project", "sessions", "human turns", "tool calls", "$ equiv"],
            [(k, v[0], v[1], f"{v[3]:,}", f"{v[2]:,.0f}")
             for k, v in sorted(proj.items(), key=lambda kv: -kv[1][2])]))
    A("")
    A("</details>")
    A("")

    # ---------------------------------------------------------- turn anatomy
    ts = mining["turn_shape"]
    A("## 2. What a human turn actually looks like")
    A("")
    A(table(["metric", "value"], [
        ("median length", f"{ts['median_chars']:.0f} chars / {ts['median_words']:.0f} words"),
        ("turns under 10 words", pct(ts["share_under_10_words"])),
        ("median tool calls the turn triggers", ts["median_tools_triggered"]),
        ("turns that trigger no tool at all", pct(ts["share_zero_tool_followup"])),
        ("turns that interrupt a running agent", pct(ts["share_interrupting_agent"])),
        ("entered as slash command", f"{ts['by_source'].get('slash', 0)}"),
        ("entered while agent was busy (queued)", f"{ts['by_source'].get('queued', 0)}"),
    ]))
    A("")
    hl = mining["human_latency"]
    A(f"**Agent idle waiting for a human**: median {hl['median_s']:.0f} s between the agent "
      f"finishing and the human replying, p90 {hl['p90_s']:.0f} s, "
      f"{hl['total_h']:.0f} h in total - {pct(hl['share_of_session_wallclock'])} of all session wall-clock.")
    A("")

    # ------------------------------------------------------------- labels
    if labels:
        lab = mining["labels"]
        A("## 3. Classification of human input")
        A("")
        for field, title in (("intent", "Intent"), ("task_kind", "Task kind"),
                             ("motivation", "Motivation"), ("sentiment", "Sentiment"),
                             ("novel_information", "Information the human contributed")):
            A(f"**{title}**")
            A("")
            A(table(["label", "turns", "share"],
                    [(k, v["n"], pct(v["share"])) for k, v in lab[field].items()]))
            A("")

        A("## 4. Can this turn be replaced?")
        A("")
        A(table(["replaceable by", "turns", "share"],
                [(k, v["n"], pct(v["share"])) for k, v in lab["replaceable_by"].items()]))
        A("")
        A(f"**Rework**: {pct(lab['is_rework']['share'])} of human turns "
          f"({lab['is_rework']['n']} of {len(labels)}) exist only because the agent erred or stopped short.")
        A("")
        A("**Friction source**")
        A("")
        A(table(["source", "turns", "share"],
                [(k, v["n"], pct(v["share"])) for k, v in lab["friction_source"].items()]))
        A("")
        A("**Which intents are the automatable ones** (rows sorted by volume)")
        A("")
        xt = mining["intent_x_replaceable"]
        keys = ["deterministic_rule", "ai_policy", "ai_with_context", "human_only"]
        A(table(["intent", "n", *keys, "% removable"],
                [(k, sum(v.values()), *[v.get(kk, 0) for kk in keys],
                  pct((v.get("deterministic_rule", 0) + v.get("ai_policy", 0)) / max(sum(v.values()), 1)))
                 for k, v in xt.items()]))
        A("")
        A("**Most frequent trigger -> action rules the model extracted**")
        A("")
        A(table(["rule", "times"], [(r, n) for r, n in mining["rule_sketches_top"][:25] if n > 1]))
        A("")

    # ------------------------------------------------------------ sessions
    if slabels:
        sl = mining["session_labels"]
        A("## 5. Session outcomes")
        A("")
        A(table(["outcome", "sessions"], list(sl["outcome"].items())))
        A("")
        A(table(["automation verdict", "sessions"], list(sl["automation_verdict"].items())))
        A("")
        A(table(["human repair share of session", "sessions"], list(sl["rework_share"].items())))
        A("")
        A("## 6. Workflow archetypes")
        A("")
        at = mining["archetype_table"]
        A(table(["archetype", "sessions", "$ equiv", "success", "verdict spread"],
                [(k, v["n"], f"{v['cost_usd']:,.0f}",
                  f"{v['outcomes'].get('success', 0)}/{v['n']}",
                  ", ".join(f"{kk}:{vv}" for kk, vv in sorted(v["verdicts"].items(), key=lambda x: -x[1])))
                 for k, v in at.items()]))
        A("")
        A("**Recipes actually executed** (most common opening verbs per archetype)")
        A("")
        steps_by_arch = defaultdict(Counter)
        for r in slabels.values():
            for i, s_ in enumerate(r.get("steps", [])):
                steps_by_arch[r["workflow_archetype"]][f"{i + 1}. {s_.split()[0].lower()}"] += 1
        for arch, ctr in sorted(steps_by_arch.items(), key=lambda kv: -at.get(kv[0], {}).get("n", 0))[:8]:
            top = ", ".join(f"{k.split('. ')[1]}" for k, _ in ctr.most_common(8))
            A(f"- **{arch}** ({at[arch]['n']} sessions): {top}")
        A("")
        A("**Blockers to unattended execution**")
        A("")
        A(table(["blocker", "sessions"], [(b, n) for b, n in sl["blockers_top"][:20]]))
        A("")

    # --------------------------------------------------------------- motifs
    if "approval_tax" in mining:
        at_ = mining["approval_tax"]
        A("**The approval tax** - turns that carried no information the agent did not already have:")
        A("")
        A(table(["metric", "value"], [
            ("such turns", f"{at_['turns_carrying_no_new_information']} "
                           f"({pct(at_['share_of_labelled_turns'])} of labelled turns)"),
            ("consecutive runs of them", at_["consecutive_runs"]),
            ("longest run", at_["longest_run"]),
        ]))
        A("")
    if "intent_by_phase" in mining:
        A("**Where each intent shows up in a session**")
        A("")
        ph = mining["intent_by_phase"]
        allk = sorted({k for v in ph.values() for k in v}, key=lambda k: -sum(v.get(k, 0) for v in ph.values()))[:8]
        A(table(["phase", *allk], [(p_, *[ph[p_].get(k, 0) for k in allk])
                                   for p_ in ("opening", "middle", "closing") if p_ in ph]))
        A("")
    if "outcome_by_human_turns" in mining:
        A("**Outcome against how much the human intervened**")
        A("")
        ob = mining["outcome_by_human_turns"]
        outs = sorted({k for v in ob.values() for k in v})
        A(table(["human turns", *outs, "n"],
                [(b, *[v.get(o, 0) for o in outs], sum(v.values())) for b, v in ob.items()]))
        A("")

    A("## 7. Mined operation sequences (workflow candidates)")
    A("")
    A("Operation classes are derived from tool calls and shell command heads; runs of the same "
      "op are folded (`edit*`). A motif is kept only if no longer motif has the same count.")
    A("")
    A("**Per human turn** - what one instruction expands into")
    A("")
    A(table(["motif", "occurrences", "sessions"],
            [(m["motif"], m["count"], m["sessions"]) for m in mining["op_motifs_per_turn"][:18]]))
    A("")
    A("**Per session** - the longer arcs")
    A("")
    A(table(["motif", "occurrences", "sessions"],
            [(m["motif"], m["count"], m["sessions"]) for m in mining["op_motifs_per_session"][:18]]))
    A("")
    A("**Shell-level, plumbing removed**")
    A("")
    A(table(["motif", "occurrences", "sessions"],
            [(m["motif"], m["count"], m["sessions"]) for m in mining["shell_motifs"][:15]]))
    A("")
    if "intent_motifs" in mining:
        A("**Interaction loop** - what the human does, in order")
        A("")
        A(table(["motif", "occurrences", "sessions"],
                [(m["motif"], m["count"], m["sessions"]) for m in mining["intent_motifs"][:18]]))
        A("")
    if "trigger_procedures" in mining:
        A("**Trigger -> procedure**: given an intent, what the agent then ran")
        A("")
        A(table(["human intent", "n", "top operation signature", "share"],
                [(r["intent"], r["n"], r["signature"], pct(r["share"]))
                 for r in mining["trigger_procedures"][:20]]))
        A("")

    # ------------------------------------------------------- opportunity math
    if labels:
        lab = mining["labels"]
        rep = lab["replaceable_by"]
        removable = rep.get("deterministic_rule", {"n": 0})["n"] + rep.get("ai_policy", {"n": 0})["n"]
        med = mining["human_latency"]["median_s"] or 0
        A("## 8. The bill for the human in the loop")
        A("")
        A(table(["quantity", "value", "how it is derived"], [
            ("human turns", len(labels), "measured"),
            ("turns a rule or a policy could emit", f"{removable} ({pct(removable / len(labels))})",
             "classifier judgement"),
            ("median agent idle before a human replies", f"{med:.0f} s", "measured"),
            ("idle time behind those turns",
             f"{removable * med / 3600:.0f} h",
             "removable turns x median idle - upper bound, assumes serial waiting"),
            ("total agent idle waiting on a human",
             f"{mining['human_latency']['total_h']:.0f} h "
             f"({pct(mining['human_latency']['share_of_session_wallclock'])} of session wall-clock)",
             "measured"),
        ]))
        A("")
        if slabels:
            costs = {sid: by_id[sid]["cost_usd"] for sid in slabels if sid in by_id}
            byv = defaultdict(lambda: [0, 0.0])
            for sid, r in slabels.items():
                byv[r["automation_verdict"]][0] += 1
                byv[r["automation_verdict"]][1] += costs.get(sid, 0.0)
            tot = sum(v[1] for v in byv.values())
            A("Weighted by what each session cost to run:")
            A("")
            A(table(["verdict", "sessions", "$ equiv", "share of spend"],
                    [(k, v[0], f"{v[1]:,.0f}", pct(v[1] / max(tot, 1)))
                     for k, v in sorted(byv.items(), key=lambda kv: -kv[1][1])]))
            A("")

    # ---------------------------------------------------------- the catalogue
    spec_path = DATA / "workflow_specs.jsonl"
    if spec_path.exists():
        specs = [r for r in jl_read(spec_path) if "_error" not in r]
        A("## 9. Candidate workflows")
        A("")
        A(table(["workflow", "archetype", "sessions", "autonomy", "steps", "gates"],
                [(f"`{r['name']}`", r["archetype"], r["sessions_observed"], r["autonomy"],
                  len(r["steps"]), len(r["human_gates"])) for r in
                 sorted(specs, key=lambda r: -r["sessions_observed"])]))
        A("")
        for r in sorted(specs, key=lambda r: -r["sessions_observed"]):
            A(f"### `{r['name']}` - {r['one_line']}")
            A("")
            A(f"- **evidence**: {r['sessions_observed']} sessions labelled `{r['archetype']}`")
            A(f"- **trigger**: {r['trigger']}")
            A(f"- **autonomy**: {r['autonomy']}")
            A(f"- **removes**: {r['removes_turns']}")
            if r.get("preconditions"):
                A(f"- **preconditions**: {'; '.join(r['preconditions'])}")
            A("")
            A(table(["#", "step", "kind", "fails if"],
                    [(i + 1, s_["op"], s_["kind"], s_["fails_if"] or "-")
                     for i, s_ in enumerate(r["steps"])]))
            A("")
            if r.get("human_gates"):
                A("**Human still decides**: " + "; ".join(r["human_gates"]))
                A("")
            if r.get("blockers"):
                A("**Blocked on**: " + "; ".join(r["blockers"]))
                A("")

    A("## 10. Method and caveats")
    A("")
    A("- Corpus frozen in `data/manifest.json`; the live session running the analysis is excluded.")
    A(f"- {sum(x['unparsable_lines'] for x in sessions)} of "
      f"{sum(x['total_lines'] for x in sessions):,} transcript records failed to parse (truncated "
      "writes) and were skipped.")
    A("- Costs are **API list-price equivalents** computed from `usage` blocks, not billed spend "
      "(these sessions ran on a subscription). One API response is written to the transcript as "
      "several records carrying identical `usage`; each response is billed once, by message id.")
    A("- Cache pricing: read 0.1x input, 5-minute write 1.25x, 1-hour write 2x.")
    A("- Turn and session labels come from an LLM classifier over a closed taxonomy "
      "(`scripts/taxonomy.py`); they are judgements, not measurements. Motifs, counts, latencies "
      "and costs are measurements.")
    A("- `replaceable_by` is the classifier's opinion about a single turn in context. It does not "
      "know what an automated replacement would have cost or broken.")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "REPORT.md").write_text("\n".join(L) + "\n")
    print(f"wrote {OUT / 'REPORT.md'} ({len(L)} lines)")


if __name__ == "__main__":
    main()

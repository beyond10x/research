#!/usr/bin/env python3
"""Stage 4 - mine repeated operation sequences: the candidate workflows.

Three independent miners, all deterministic:
  A. tool motifs      - n-grams over the tool sequence each human turn triggers
  B. shell motifs     - n-grams over normalised shell verbs (git commit, cargo test, ...)
  C. interaction loop - n-grams over human-turn intents (needs stage 2 labels)
Plus the human-in-the-loop cost model: wall-clock the agent spent waiting for a human.

Writes out/mining.json and prints the headline tables.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path

from common import DATA, OUT, jl_read

ENV_PREFIX = re.compile(r"^(?:\w+=\S+\s+)+")

# --- shell command -> operation class -------------------------------------
# This machine's agents are instructed to do file work through Bash, so `cat`/`sed`
# ARE the read/edit operations. Classify them, don't discard them.
SHELL_NOISE = {
    "echo", "cd", "pwd", "true", "false", "printf", "export", "set", "unset", "source", ".",
    "sleep", "date", "which", "type", "command", "eval", "exec", "clear", "alias", "history",
    "wait", "read", "seq", "yes", "trap", "shift", "return", "exit", "for", "do", "done", "if",
    "then", "fi", "else", "elif", "while", "until", "case", "esac", "function", "local",
    "test", "[", "[[", "]]", "time", "watch", "tmux", "less", "more", "open", "code", "man",
}
SHELL_INSPECT = {
    "ls", "cat", "head", "tail", "grep", "rg", "egrep", "fgrep", "find", "fd", "wc", "tree",
    "du", "df", "stat", "diff", "comm", "sort", "uniq", "cut", "awk", "jq", "yq", "column",
    "paste", "join", "nl", "rev", "fold", "tr", "realpath", "basename", "dirname", "file",
    "strings", "xxd", "zcat", "ps", "pgrep", "top", "env", "printenv", "sed", "tee", "xargs",
}
SHELL_FS = {"mkdir", "cp", "mv", "rm", "ln", "chmod", "chown", "touch", "tar", "gzip", "unzip",
            "mktemp", "rsync", "split", "kill", "pkill", "truncate"}
PLUMBING = SHELL_NOISE | SHELL_INSPECT | SHELL_FS  # kept for the raw-verb miner

OP_BY_TOOL = {
    "Read": "inspect", "Glob": "inspect", "Grep": "inspect", "LSP": "inspect",
    "NotebookRead": "inspect",
    "Edit": "edit", "Write": "edit", "NotebookEdit": "edit", "MultiEdit": "edit",
    "Agent": "delegate", "Task": "delegate", "Workflow": "delegate", "SendMessage": "delegate",
    "TaskOutput": "delegate", "TaskStop": "delegate",
    "WebSearch": "web", "WebFetch": "web",
    "TodoWrite": "plan", "ExitPlanMode": "plan", "EnterPlanMode": "plan",
    "Skill": "skill", "ToolSearch": "skill",
    "AskUserQuestion": "ask_human", "ReportFindings": "report",
}
BASH_OP = [
    (re.compile(r"^git (commit|push|tag|merge|rebase|cherry-pick|revert|reset|checkout|switch|branch|worktree|stash|add|rm|mv|init|remote|config|notes|apply|am)\b"), "vcs_write"),
    (re.compile(r"^git\b"), "vcs_read"),
    (re.compile(r"^gh\b"), "forge"),
    (re.compile(r"^(pytest|jest|vitest|cargo test|go test|npm test|task .*test|.*\btest\b.*\.sh)"), "test"),
    (re.compile(r"^(cargo (build|check|clippy|fmt|run)|go (build|vet|run)|npm run|tsc|make)\b"), "build"),
    (re.compile(r"^(ruff|eslint|mypy|black|prettier|shellcheck|clippy)\b"), "lint"),
    (re.compile(r"^task\b"), "taskrunner"),
    (re.compile(r"^(uv|pip|pip3|npm|pnpm|yarn|poetry|cargo add|go get|apt|pacman|brew)\b"), "deps"),
    (re.compile(r"^(docker|docker-compose|kubectl|helm|terraform|systemctl|k9s|minikube|kind)\b"), "infra"),
    (re.compile(r"^(curl|wget|http|httpie|nc|ping|dig|ss|netstat)\b"), "net"),
    (re.compile(r"^(psql|bq|sqlite3|mysql|redis-cli|mongosh)\b"), "query"),
    (re.compile(r"^(claude|ant|flux|codex|fluxplane-plugin|autodev|scratchpad|protocol|connectors)\b"), "agent_cli"),
    (re.compile(r"^(python3?|node|deno|ruby|bash|sh|zsh|perl|\./|/home/)"), "run_script"),
]
HEREDOC = re.compile(r"<<-?\s*'?\"?(\w+)'?\"?.*?^\1\s*$", re.S | re.M)
REDIRECT_WRITE = re.compile(r">>?\s*(?!&)[\w./~$-]+")
TIMEOUT_PREFIX = re.compile(r"^timeout\s+[\d.]+[smhd]?\s+")
WRAPPER_PREFIX = re.compile(r"^(?:sudo|nohup|time|env(?:\s+-\w+)*(?:\s+\w+=\S+)*|command|exec)\s+")


def bash_ops(cmd: str) -> list[str]:
    """Semantic operation classes performed by one shell command line."""
    cmd = HEREDOC.sub(lambda m: f" <<{m.group(1)}-BODY ", cmd)  # heredoc bodies are data, not commands
    out = []
    for part in re.split(r"(?:&&|\|\||;|\n)", ENV_PREFIX.sub("", cmd.strip())):
        part = part.strip().lstrip("(").strip()
        if not part:
            continue
        # a redirection into a path is a write, whatever the producing command was
        writes = bool(REDIRECT_WRITE.search(part)) or "-BODY" in part
        part = TIMEOUT_PREFIX.sub("", part)
        part = WRAPPER_PREFIX.sub("", part)
        toks = part.split()
        if not toks:
            continue
        head = Path(toks[0]).name
        if head == "sed" and ("-i" in toks or any(t.startswith("-i") for t in toks)):
            out.append("edit")
            continue
        matched = None
        for rx, op in BASH_OP:
            if rx.match(part):
                matched = op
                break
        if matched:
            out.append(matched)
        elif head in SHELL_INSPECT:
            out.append("edit" if writes else "inspect")
        elif head in SHELL_FS:
            out.append("fs_mutate")
        elif head in SHELL_NOISE:
            if writes:
                out.append("edit")
        else:
            out.append("other_cmd")
    return out


def op_class(ev: dict) -> str | None:
    tool = ev["tool"]
    if tool.startswith("mcp__slack") or tool.startswith("mcp__"):
        return "comms" if "slack" in tool else "mcp"
    if tool == "Bash":
        ops = bash_ops(ev["arg"])
        return ops[0] if ops else None
    return OP_BY_TOOL.get(tool, "other_tool")
SUBCMD_BINARIES = {"git", "cargo", "task", "npm", "npx", "uv", "gh", "docker", "kubectl",
                   "go", "pnpm", "yarn", "pip", "poetry", "terraform", "systemctl", "flux", "ant"}


def shell_verbs(cmd: str) -> list[str]:
    """Normalise a shell command line into the sequence of binaries it invokes.
    Heredoc bodies are data (usually inline Python), not commands - strip them first."""
    cmd = ENV_PREFIX.sub("", HEREDOC.sub(lambda m: f" <<{m.group(1)}-BODY ", cmd).strip())
    out = []
    # split on ; && || | and newlines, keep it crude but stable
    for part in re.split(r"(?:&&|\|\||;|\||\n)", cmd):
        part = part.strip()
        if not part:
            continue
        toks = [t for t in re.split(r"\s+", part) if t and not t.startswith("-")]
        if not toks:
            continue
        binary = Path(toks[0]).name
        if binary in ("sudo", "time", "env", "nohup", "xargs"):
            toks = toks[1:]
            if not toks:
                continue
            binary = Path(toks[0]).name
        if binary in SUBCMD_BINARIES and len(toks) > 1:
            out.append(f"{binary} {toks[1]}")
        else:
            out.append(binary)
    return out


def collapse(seq: list[str]) -> list[str]:
    """Fold runs of the same op: Bash,Bash,Bash -> Bash*."""
    out = []
    for x in seq:
        if out and out[-1].rstrip("*") == x:
            out[-1] = x + "*"
        else:
            out.append(x)
    return out


def ngrams(seqs: list[tuple[str, list[str]]], nmin: int, nmax: int, min_support: int):
    """Count n-grams and the number of distinct sessions each appears in."""
    counts: Counter = Counter()
    sessions: dict[tuple, set] = defaultdict(set)
    for sid, seq in seqs:
        for n in range(nmin, nmax + 1):
            for i in range(len(seq) - n + 1):
                g = tuple(seq[i:i + n])
                counts[g] += 1
                sessions[g].add(sid)
    return {g: (c, len(sessions[g])) for g, c in counts.items() if c >= min_support}


def closed(grams: dict) -> dict:
    """Drop an n-gram if a longer one containing it has the same count (it adds nothing)."""
    by_len = defaultdict(list)
    for g in grams:
        by_len[len(g)].append(g)
    keep = {}
    for g, (c, s) in grams.items():
        redundant = False
        for longer in by_len[len(g) + 1]:
            if grams[longer][0] == c and (longer[: len(g)] == g or longer[1:] == g):
                redundant = True
                break
        if not redundant:
            keep[g] = (c, s)
    return keep


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-support", type=int, default=8)
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    sessions = {s["session_id"]: s for s in jl_read(DATA / "sessions.jsonl")}
    turns = [t for t in jl_read(DATA / "turns.jsonl") if t["source"] != "sdk"]
    events = list(jl_read(DATA / "tool_events.jsonl"))
    labels = {}
    lp = DATA / "turn_labels.jsonl"
    if lp.exists():
        for r in jl_read(lp):
            if "_error" not in r and r.get("id"):
                labels[r["id"]] = r

    report: dict = {}

    # ---- A. tool motifs, one sequence per human turn ----------------------
    tool_seqs = [(t["session_id"], collapse(t["tool_seq"])) for t in turns if t["tool_seq"]]
    A = closed(ngrams(tool_seqs, 2, 6, args.min_support))
    report["tool_motifs"] = [
        {"motif": " > ".join(g), "count": c, "sessions": s}
        for g, (c, s) in sorted(A.items(), key=lambda kv: (-kv[1][1], -kv[1][0]))[: args.top]
    ]

    # ---- B. shell verb motifs, one sequence per session --------------------
    by_sess_shell = defaultdict(list)
    for e in events:
        if e["tool"] == "Bash":
            by_sess_shell[e["session_id"]].extend(
                v for v in shell_verbs(e["arg"]) if v.split() and v.split()[0] not in PLUMBING)
    shell_seqs = [(sid, collapse(v)) for sid, v in by_sess_shell.items()]
    B = closed(ngrams(shell_seqs, 2, 5, args.min_support))
    report["shell_motifs"] = [
        {"motif": " > ".join(g), "count": c, "sessions": s}
        for g, (c, s) in sorted(B.items(), key=lambda kv: (-kv[1][1], -kv[1][0]))[: args.top]
    ]
    verb_counts = Counter(v for _, seq in by_sess_shell.items() for v in seq)
    report["shell_verbs_top"] = verb_counts.most_common(30)

    # ---- B2. operation-class motifs: the workflow vocabulary ---------------
    ev_by_turn = defaultdict(list)
    ev_by_sess = defaultdict(list)
    for e in events:
        op = op_class(e)
        if not op:
            continue
        ev_by_turn[(e["session_id"], e["turn_idx"])].append(op)
        ev_by_sess[e["session_id"]].append(op)
    turn_op_seqs = [(k[0], collapse(v)) for k, v in ev_by_turn.items() if len(v) > 1]
    OPS = closed(ngrams(turn_op_seqs, 2, 6, args.min_support))
    report["op_motifs_per_turn"] = [
        {"motif": " > ".join(g), "count": c, "sessions": s}
        for g, (c, s) in sorted(OPS.items(), key=lambda kv: (-kv[1][1], -kv[1][0]))[: args.top]
    ]
    sess_op_seqs = [(k, collapse(v)) for k, v in ev_by_sess.items()]
    OPS2 = closed(ngrams(sess_op_seqs, 3, 7, 6))
    report["op_motifs_per_session"] = [
        {"motif": " > ".join(g), "count": c, "sessions": s}
        for g, (c, s) in sorted(OPS2.items(), key=lambda kv: (-kv[1][1], -kv[1][0]))[: args.top]
    ]
    report["op_frequency"] = Counter(op for _, v in ev_by_sess.items() for op in v).most_common()

    # ---- C. interaction-loop motifs over human intents ---------------------
    if labels:
        by_sess_intent = defaultdict(list)
        for t in sorted(turns, key=lambda x: (x["session_id"], x["turn_idx"])):
            lb = labels.get(f"{t['session_id']}#{t['turn_idx']}")
            if lb:
                by_sess_intent[t["session_id"]].append(lb["intent"])
        C = closed(ngrams([(k, v) for k, v in by_sess_intent.items()], 2, 4, 5))
        report["intent_motifs"] = [
            {"motif": " > ".join(g), "count": c, "sessions": s}
            for g, (c, s) in sorted(C.items(), key=lambda kv: (-kv[1][1], -kv[1][0]))[: args.top]
        ]

    # ---- C2. trigger -> procedure: intent to the ops it actually caused -----
    if labels:
        sig_by_intent = defaultdict(Counter)
        for t in turns:
            lb = labels.get(f"{t['session_id']}#{t['turn_idx']}")
            if not lb:
                continue
            ops = collapse(ev_by_turn.get((t["session_id"], t["turn_idx"]), []))
            sig = " > ".join(ops[:3]) if ops else "(no tools)"
            sig_by_intent[lb["intent"]][sig] += 1
        rows = []
        for intent, ctr in sig_by_intent.items():
            n = sum(ctr.values())
            for sig, c in ctr.most_common(2):
                rows.append({"intent": intent, "n": n, "signature": sig,
                             "count": c, "share": round(c / n, 3)})
        report["trigger_procedures"] = sorted(rows, key=lambda r: (-r["n"], -r["count"]))

    # ---- D. human-in-the-loop cost model -----------------------------------
    lat = [t["idle_before_s"] for t in turns
           if t.get("idle_before_s") and 0 < t["idle_before_s"] < 6 * 3600]
    report["human_latency"] = {
        "turns_measured": len(lat),
        "median_s": round(st.median(lat), 1) if lat else None,
        "mean_s": round(st.mean(lat), 1) if lat else None,
        "p90_s": round(sorted(lat)[int(len(lat) * 0.9)], 1) if lat else None,
        "total_h": round(sum(lat) / 3600, 1),
        "share_of_session_wallclock": round(
            sum(lat) / max(sum(s["duration_s"] for s in sessions.values()), 1), 3),
    }

    # ---- E. per-turn shape --------------------------------------------------
    report["turn_shape"] = {
        "turns": len(turns),
        "median_chars": st.median([t["char_len"] for t in turns]),
        "median_words": st.median([t["word_len"] for t in turns]),
        "share_under_10_words": round(sum(t["word_len"] < 10 for t in turns) / len(turns), 3),
        "share_zero_tool_followup": round(sum(t["tool_count"] == 0 for t in turns) / len(turns), 3),
        "median_tools_triggered": st.median([t["tool_count"] for t in turns]),
        "share_interrupting_agent": round(sum(bool(t["interrupted_agent"]) for t in turns) / len(turns), 3),
        "by_source": dict(Counter(t["source"] for t in turns)),
    }

    # ---- F. label rollups ---------------------------------------------------
    if labels:
        def share(field):
            c = Counter(v[field] for v in labels.values())
            n = sum(c.values())
            return {k: {"n": v, "share": round(v / n, 3)} for k, v in c.most_common()}
        report["labels"] = {f: share(f) for f in
                            ("intent", "task_kind", "motivation", "sentiment",
                             "novel_information", "replaceable_by", "friction_source")}
        report["labels"]["is_rework"] = {
            "n": sum(v["is_rework"] for v in labels.values()),
            "share": round(sum(v["is_rework"] for v in labels.values()) / len(labels), 3)}
        rules = Counter(v["rule_sketch"].strip().lower() for v in labels.values() if v["rule_sketch"].strip())
        report["rule_sketches_top"] = rules.most_common(40)
        # cross-tab: which intents are the automatable ones
        xt = defaultdict(Counter)
        for v in labels.values():
            xt[v["intent"]][v["replaceable_by"]] += 1
        report["intent_x_replaceable"] = {k: dict(c) for k, c in
                                          sorted(xt.items(), key=lambda kv: -sum(kv[1].values()))}

    # ---- F2. where in a session each intent shows up -------------------------
    if labels:
        pos = defaultdict(Counter)
        for t in turns:
            lb = labels.get(f"{t['session_id']}#{t['turn_idx']}")
            n = sessions.get(t["session_id"], {}).get("human_turns", 0)
            if not lb or n < 4:
                continue
            third = min(int(t["turn_idx"] / n * 3), 2)
            pos[["opening", "middle", "closing"][third]][lb["intent"]] += 1
        report["intent_by_phase"] = {k: dict(v.most_common(8)) for k, v in pos.items()}

        # the approval tax: runs of turns that carried no new information
        empty = {"approve_proceed", "resume_continue", "request_status", "social"}
        runs, cur_run, tax = [], 0, 0
        for t in sorted(turns, key=lambda x: (x["session_id"], x["turn_idx"])):
            lb = labels.get(f"{t['session_id']}#{t['turn_idx']}")
            if lb and (lb["intent"] in empty or lb["novel_information"] == "none"):
                cur_run += 1
                tax += 1
            else:
                if cur_run:
                    runs.append(cur_run)
                cur_run = 0
        if cur_run:
            runs.append(cur_run)
        report["approval_tax"] = {
            "turns_carrying_no_new_information": tax,
            "share_of_labelled_turns": round(tax / max(len(labels), 1), 3),
            "consecutive_runs": len(runs),
            "longest_run": max(runs) if runs else 0,
            "median_run": st.median(runs) if runs else 0,
        }

    # ---- G. session rollups -------------------------------------------------
    sp = DATA / "session_labels.jsonl"
    if sp.exists():
        slabels = [r for r in jl_read(sp) if "_error" not in r]
        report["session_labels"] = {
            "n": len(slabels),
            "outcome": dict(Counter(r["outcome"] for r in slabels).most_common()),
            "archetype": dict(Counter(r["workflow_archetype"] for r in slabels).most_common()),
            "automation_verdict": dict(Counter(r["automation_verdict"] for r in slabels).most_common()),
            "rework_share": dict(Counter(r["rework_share"] for r in slabels).most_common()),
            "blockers_top": Counter(b.strip().lower() for r in slabels
                                    for b in r.get("automation_blockers", [])).most_common(25),
            "step_verbs_top": Counter(s.split()[0].lower() for r in slabels
                                      for s in r.get("steps", []) if s.split()).most_common(25),
        }
        # archetype x verdict, weighted by cost and by session count
        cost = {s["session_id"]: s["cost_usd"] for s in sessions.values()}
        agg = defaultdict(lambda: {"n": 0, "cost": 0.0, "verdicts": Counter(), "outcomes": Counter()})
        for r in slabels:
            a = agg[r["workflow_archetype"]]
            a["n"] += 1
            a["cost"] += cost.get(r["session_id"], 0.0)
            a["verdicts"][r["automation_verdict"]] += 1
            a["outcomes"][r["outcome"]] += 1
        # does more human involvement produce better outcomes?
        buckets = defaultdict(Counter)
        for r in slabels:
            n = sessions.get(r["session_id"], {}).get("human_turns", 0)
            b = "0 (headless)" if n == 0 else "1-3" if n <= 3 else "4-10" if n <= 10 else "11-30" if n <= 30 else "31+"
            buckets[b][r["outcome"]] += 1
        report["outcome_by_human_turns"] = {k: dict(v) for k, v in sorted(buckets.items())}

        report["archetype_table"] = {
            k: {"n": v["n"], "cost_usd": round(v["cost"], 2),
                "verdicts": dict(v["verdicts"]), "outcomes": dict(v["outcomes"])}
            for k, v in sorted(agg.items(), key=lambda kv: -kv[1]["n"])}

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "mining.json").write_text(json.dumps(report, indent=1))
    print(json.dumps({k: (v if not isinstance(v, list) else v[:5]) for k, v in report.items()
                      if k in ("human_latency", "turn_shape")}, indent=1))
    print(f"\ntop tool motifs ({len(report['tool_motifs'])}):")
    for m in report["tool_motifs"][:12]:
        print(f"  {m['sessions']:>3} sess {m['count']:>5}x  {m['motif']}")
    print("\ntop shell motifs (plumbing removed):")
    for m in report["shell_motifs"][:12]:
        print(f"  {m['sessions']:>3} sess {m['count']:>5}x  {m['motif']}")
    print("\ntop operation motifs per human turn:")
    for m in report["op_motifs_per_turn"][:15]:
        print(f"  {m['sessions']:>3} sess {m['count']:>5}x  {m['motif']}")
    print(f"\nwrote {OUT / 'mining.json'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Stage 1 - deterministic extraction from Claude Code session transcripts.

Emits three tables under data/:
  sessions.jsonl    one row per session, with cost/turn/tool metrics
  turns.jsonl       one row per *human* turn, with the surrounding context
  tool_events.jsonl one row per tool call, attributed to the human turn that caused it

Nothing here calls an LLM; every field is read straight off the transcript.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

from common import DATA, PROJECTS, jl_write, text_of, usage_cost

INTERRUPT_RE = re.compile(r"\[Request interrupted by user")
SLASH_RE = re.compile(r"<command-name>([^<]*)</command-name>")
SKILL_RE = re.compile(r"Base directory for this skill: \S+/([\w.-]+)\s*$", re.M)


def ts(rec) -> float:
    t = rec.get("timestamp")
    if not t:
        return 0.0
    try:
        return datetime.fromisoformat(t.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def pick_sessions(limit: int, since: str | None, exclude: set[str], manifest: Path) -> list[Path]:
    """Choose the N most recently touched top-level sessions.

    The transcript store is live - the session running this script keeps growing,
    and any concurrent session reshuffles the mtime order. The first run freezes
    its selection into data/manifest.json so every later stage sees the same corpus.
    """
    if manifest.exists():
        return [Path(p) for p in json.loads(manifest.read_text())["files"] if Path(p).exists()]
    files = [p for p in PROJECTS.glob("*/*.jsonl") if p.parent.parent == PROJECTS and p.stem not in exclude]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    if since:
        cut = datetime.fromisoformat(since).timestamp()
        files = [p for p in files if p.stat().st_mtime >= cut]
    files = files[:limit]
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({
        "picked_at": datetime.now().isoformat(timespec="seconds"),
        "limit": limit,
        "excluded": sorted(exclude),
        "files": [str(p) for p in files],
    }, indent=1))
    return files


def tool_arg_digest(name: str, inp: dict) -> str:
    """One short string capturing what this tool call actually did."""
    if not isinstance(inp, dict):
        return ""
    if name == "Bash" and isinstance(inp.get("command"), str):
        return inp["command"][:1500]  # keep heredocs intact so the op classifier can parse them
    for key in ("command", "file_path", "path", "pattern", "query", "url", "prompt", "skill", "description"):
        if key in inp and isinstance(inp[key], str):
            return inp[key][:240].replace("\n", " ")
    return json.dumps(inp)[:160]


def parse_session(path: Path) -> tuple[dict, list, list]:
    recs = []
    unparsable = 0
    for line in path.open(errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except json.JSONDecodeError:
            unparsable += 1  # truncated records do occur; count them rather than hide them

    sid = path.stem
    project = path.parent.name
    sess = {
        "session_id": sid,
        "project": project,
        "file": str(path),
        "title": None,
        "cwd": None,
        "git_branch": None,
        "entrypoint": None,
        "versions": set(),
        "models": Counter(),
        "efforts": Counter(),
        "permission_modes": Counter(),
        "tools": Counter(),
        "slash_commands": [],
        "skills_loaded": [],
        "subagents_spawned": 0,
        "compactions": 0,
        "api_errors": 0,
        "tool_errors": 0,
        "interruptions": 0,
        "queued_turns": 0,
        "human_turns": 0,
        "sdk_turns": 0,
        "assistant_msgs": 0,
        "tool_calls": 0,
        "in_tok": 0,
        "out_tok": 0,
        "cache_read_tok": 0,
        "cache_write_tok": 0,
        "thinking_tok": 0,
        "cost_usd": 0.0,
        "files_edited": set(),
        "commits": 0,
        "start_ts": None,
        "end_ts": None,
        "unparsable_lines": unparsable,
        "total_lines": len(recs) + unparsable,
    }

    turns: list[dict] = []
    tool_events: list[dict] = []
    cur = None                 # human turn currently in flight
    last_assistant_text = ""   # what the agent last said (context for the human reply)
    last_assistant_ts = 0.0
    pending_tools: dict[str, dict] = {}
    # One API response is written to the transcript as several records (one per
    # content block), each carrying an identical copy of `usage`. Bill each id once.
    billed_ids: set[str] = set()
    seen_tool_ids: set[str] = set()

    prev_ts = 0.0
    gap_before = None
    active_s = 0.0
    for rec in recs:
        t = rec.get("type")
        rts = ts(rec)
        if rts:
            # "active" = wall-clock excluding gaps longer than 5 min, so an abandoned
            # session left open overnight does not read as 14 hours of work
            if prev_ts and 0 < rts - prev_ts <= 300:
                active_s += rts - prev_ts
            gap_before = rts - prev_ts if prev_ts else None
            prev_ts = rts
            sess["start_ts"] = rts if sess["start_ts"] is None else min(sess["start_ts"], rts)
            sess["end_ts"] = rts if sess["end_ts"] is None else max(sess["end_ts"], rts)
        if rec.get("version"):
            sess["versions"].add(rec["version"])
        for fld, key in (("cwd", "cwd"), ("gitBranch", "git_branch"), ("entrypoint", "entrypoint")):
            if rec.get(fld) and not sess[key]:
                sess[key] = rec[fld]

        if t == "ai-title" and rec.get("aiTitle"):
            sess["title"] = rec["aiTitle"]
        elif t == "permission-mode":
            sess["permission_modes"][rec.get("permissionMode")] += 1
        elif t == "system":
            if rec.get("compactMetadata"):
                sess["compactions"] += 1

        elif t == "assistant":
            msg = rec.get("message", {})
            model = msg.get("model", "?")
            mid = msg.get("id") or rec.get("uuid")
            if mid not in billed_ids:
                billed_ids.add(mid)
                sess["assistant_msgs"] += 1
                sess["models"][model] += 1
                if rec.get("effort"):
                    sess["efforts"][rec["effort"]] += 1
                if rec.get("isApiErrorMessage"):
                    sess["api_errors"] += 1
                u = msg.get("usage") or {}
                sess["in_tok"] += u.get("input_tokens", 0)
                sess["out_tok"] += u.get("output_tokens", 0)
                sess["cache_read_tok"] += u.get("cache_read_input_tokens", 0)
                sess["cache_write_tok"] += u.get("cache_creation_input_tokens", 0)
                sess["thinking_tok"] += (u.get("output_tokens_details") or {}).get("thinking_tokens", 0)
                sess["cost_usd"] += usage_cost(model, u)

            txt = text_of(msg.get("content"))
            if txt.strip():
                last_assistant_text = txt
                last_assistant_ts = rts
                if cur is not None and len(cur["assistant_reply_head"]) < 900:
                    cur["assistant_reply_head"] += ("\n" + txt)[:900]
            for b in msg.get("content", []) or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    if b.get("id") in seen_tool_ids:
                        continue
                    seen_tool_ids.add(b.get("id"))
                    name = b.get("name", "?")
                    sess["tools"][name] += 1
                    sess["tool_calls"] += 1
                    if name in ("Agent", "Task"):
                        sess["subagents_spawned"] += 1
                    inp = b.get("input") or {}
                    digest = tool_arg_digest(name, inp)
                    if name in ("Edit", "Write", "NotebookEdit") and isinstance(inp.get("file_path"), str):
                        sess["files_edited"].add(inp["file_path"])
                    if name == "Bash" and re.search(r"\bgit commit\b", str(inp.get("command", ""))):
                        sess["commits"] += 1
                    ev = {
                        "session_id": sid,
                        "turn_idx": cur["turn_idx"] if cur else -1,
                        "seq": len(tool_events),
                        "ts": rts,
                        "tool": name,
                        "arg": digest,
                        "sub_agent": bool(rec.get("isSidechain")),
                        "is_error": False,
                        "dur_s": None,
                    }
                    tool_events.append(ev)
                    pending_tools[b.get("id", "")] = ev
                    if cur is not None:
                        cur["tool_seq"].append(name)
                        if len(cur["tool_detail"]) < 40:
                            cur["tool_detail"].append(f"{name}: {digest[:120]}")

        elif t == "user":
            msg = rec.get("message", {})
            content = msg.get("content")
            origin = rec.get("origin") if isinstance(rec.get("origin"), dict) else {}
            raw = text_of(content) if not isinstance(content, str) else content

            if rec.get("toolUseResult") is not None:
                tur = rec["toolUseResult"]
                blocks = content if isinstance(content, list) else []
                for b in blocks:
                    if isinstance(b, dict) and b.get("type") == "tool_result":
                        ev = pending_tools.get(b.get("tool_use_id", ""))
                        err = bool(b.get("is_error"))
                        body = b.get("content")
                        body_s = body if isinstance(body, str) else json.dumps(body)[:4000]
                        if INTERRUPT_RE.search(body_s or ""):
                            sess["interruptions"] += 1
                            if cur is not None:
                                cur["interrupted_agent"] = True
                        if isinstance(tur, dict) and tur.get("interrupted"):
                            err = err or False
                        if err:
                            sess["tool_errors"] += 1
                        if ev is not None:
                            ev["is_error"] = err
                            if rts and ev["ts"]:
                                ev["dur_s"] = round(rts - ev["ts"], 3)
                continue

            if rec.get("isMeta"):
                m = SKILL_RE.search(raw or "")
                if m:
                    sess["skills_loaded"].append(m.group(1))
                continue

            if INTERRUPT_RE.search(raw or ""):
                sess["interruptions"] += 1
                if cur is not None:
                    cur["interrupted_agent"] = True

            slash = SLASH_RE.search(raw or "")
            is_human = origin.get("kind") == "human"
            is_sdk = rec.get("promptSource") == "sdk"  # headless `claude -p` - already automated
            if not (is_human or slash or is_sdk):
                continue  # task notifications, peer messages, system injections

            if slash:
                cmd = slash.group(1).strip()
                sess["slash_commands"].append(cmd)
                args = re.search(r"<command-args>(.*?)</command-args>", raw, re.S)
                text = f"/{cmd} {args.group(1).strip() if args else ''}".strip()
                source = "slash"
            else:
                text = raw
                source = rec.get("promptSource") or "typed"
                if is_sdk:
                    source = "sdk"
            if rec.get("promptSource") == "queued":
                sess["queued_turns"] += 1

            if cur is not None:
                cur["tool_count"] = len(cur["tool_seq"])
                turns.append(cur)
            sess["human_turns"] += 1
            if source == "sdk":
                sess["sdk_turns"] += 1
            cur = {
                "session_id": sid,
                "project": project,
                "turn_idx": sess["human_turns"] - 1,
                "ts": rts,
                "source": source,
                "text": text,
                "char_len": len(text),
                "word_len": len(text.split()),
                # idle = gap since the agent's LAST activity of any kind, not its last spoken
                # word; measuring from the spoken word counts tool-running time as human latency
                "idle_before_s": round(gap_before, 2) if gap_before else None,
                "since_agent_spoke_s": round(rts - last_assistant_ts, 2) if last_assistant_ts and rts else None,
                "prev_assistant_tail": last_assistant_text[-900:],
                "assistant_reply_head": "",
                "tool_seq": [],
                "tool_detail": [],
                "tool_count": 0,
                "interrupted_agent": False,
                "attachments": 0,
            }

        elif t == "attachment" and cur is not None:
            cur["attachments"] += 1

    if cur is not None:
        cur["tool_count"] = len(cur["tool_seq"])
        turns.append(cur)

    sess["versions"] = sorted(sess["versions"])
    sess["models"] = dict(sess["models"])
    sess["efforts"] = dict(sess["efforts"])
    sess["permission_modes"] = dict(sess["permission_modes"])
    sess["tools"] = dict(sess["tools"])
    sess["files_edited_n"] = len(sess["files_edited"])
    sess["files_edited"] = sorted(sess["files_edited"])[:60]
    sess["skills_loaded"] = sorted(set(sess["skills_loaded"]))
    sess["duration_s"] = round((sess["end_ts"] or 0) - (sess["start_ts"] or 0), 1)
    sess["active_s"] = round(active_s, 1)
    sess["cost_usd"] = round(sess["cost_usd"], 4)
    sess["human_turns"] -= sess["sdk_turns"]  # human_turns counts typed/queued/slash only
    sess["headless"] = sess["entrypoint"] == "sdk-cli"
    sess["first_prompt"] = turns[0]["text"][:1200] if turns else ""
    sess["last_prompt"] = turns[-1]["text"][:600] if turns else ""
    sess["last_assistant_tail"] = last_assistant_text[-1500:]
    return sess, turns, tool_events


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--since", default=None, help="ISO date; only sessions touched on/after")
    ap.add_argument("--exclude", default=os.environ.get("CLAUDE_CODE_SESSION_ID", ""),
                    help="comma-separated session ids to skip (defaults to the live session)")
    ap.add_argument("--refresh", action="store_true", help="re-pick the corpus, discarding the manifest")
    args = ap.parse_args()

    manifest = DATA / "manifest.json"
    if args.refresh and manifest.exists():
        manifest.unlink()
    exclude = {s for s in args.exclude.split(",") if s}
    files = pick_sessions(args.limit, args.since, exclude, manifest)
    sessions, turns, events = [], [], []
    for p in files:
        s, t, e = parse_session(p)
        sessions.append(s)
        turns.extend(t)
        events.extend(e)

    jl_write(DATA / "sessions.jsonl", sessions)
    jl_write(DATA / "turns.jsonl", turns)
    jl_write(DATA / "tool_events.jsonl", events)
    print(
        f"sessions={len(sessions)} human_turns={len(turns)} tool_calls={len(events)} "
        f"cost=${sum(s['cost_usd'] for s in sessions):,.2f}"
    )


if __name__ == "__main__":
    main()

# research

Empirical study of my own Claude Code session transcripts, aimed at one question:

> **Where in these interactions is the human load-bearing, and where is the human just
> a slow, expensive scheduler that a script or a second agent could replace?**

The pipeline reads `~/.claude/projects/*/*.jsonl`, reconstructs each session as
`human turn -> agent operations -> outcome`, labels the human turns against a closed
taxonomy, mines the repeated operation sequences, and renders a report.

## Run it

```sh
task all                 # extract -> classify turns -> classify sessions -> mine -> report
task extract LIMIT=100   # deterministic stage only, no API calls
task report              # re-render out/REPORT.md from whatever labels exist
```

Output lands in `out/REPORT.md`. Both classification stages are **resumable** - they skip
batches already present in `data/*_labels.jsonl`, so an interrupted run costs nothing to redo.

## Stages

| stage | script | LLM? | writes |
|---|---|---|---|
| 1 extract | `scripts/extract.py` | no | `data/sessions.jsonl`, `data/turns.jsonl`, `data/tool_events.jsonl`, `data/manifest.json` |
| 2 classify turns | `scripts/classify_turns.py` | yes | `data/turn_labels.jsonl` |
| 3 classify sessions | `scripts/classify_sessions.py` | yes | `data/session_labels.jsonl` |
| 4 mine | `scripts/mine_workflows.py` | no | `out/mining.json` |
| 5 report | `scripts/report.py` | no | `out/REPORT.md` |

`scripts/taxonomy.py` holds every label enum and the two JSON schemas. Changing a taxonomy means
`task clean-labels && task classify-turns`.

## Backends

`scripts/llm.py` speaks to either:

- `--backend cli` (default) - shells out to `claude -p --output-format json`, which authenticates
  against the local subscription. Needs no API credit. The JSON schema is inlined into the system
  prompt and validated client-side, because the CLI cannot enforce one server-side.
- `--backend api` - Messages API with `output_config.format` structured outputs. Needs a funded
  `ANTHROPIC_API_KEY`.

## Things that will bite you if you fork this

- **One API response is written to the transcript as several records**, one per content block,
  each carrying an *identical* `usage` object. Summing them naively inflates cost ~1.9x.
  `extract.py` bills per `message.id`.
- **The transcript store is live.** The session running the analysis grows while you read it, and
  any concurrent session reshuffles mtime order. Stage 1 freezes its file list into
  `data/manifest.json`; delete it (or `--refresh`) to re-pick.
- **`origin.kind == "human"` is the only reliable human-turn marker.** `promptSource` also carries
  `system` (task notifications), `sdk` (headless runs) and `queued`. Slash commands arrive as
  `<command-name>` records with no origin at all.
- **This machine's agents do file work through Bash**, per a global instruction. So `cat`/`sed`
  *are* the read/edit operations - dropping shell "plumbing" throws away most of the signal.
  `mine_workflows.py` classifies shell heads into operation classes instead.
- Costs printed anywhere here are **API list-price equivalents**, not billed spend.

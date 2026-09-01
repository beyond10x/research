# AGENTS.md - research

## What this repo is

A one-shot empirical study of Claude Code transcripts, kept because the pipeline is re-runnable.
The research question is fixed: **which human turns in an agent session are load-bearing, and
which are ceremony that a deterministic flow or a second agent could take over?** Every design
choice serves that question - do not generalise the pipeline into a transcript-analytics library.

## Serves

The objectives of the collection this repository moves, by id from `atlas/ROADMAP.md` — the only
cross-repository roadmap, and the page that says what each id means and which evidence closes it:

- **O6 — self-improvement, built into all of it.** Which human turns in an agent session are load-bearing is the map of what the system should take over from the operator next.

A change here that moves none of these is a question for the operator, not a task.
`atlas/scripts/check-map.sh` fails a repository whose `AGENTS.md` names no objective.

## Layout

- `scripts/extract.py` - deterministic parse. No LLM calls, no judgement. If a number appears in
  the report, it was produced here.
- `scripts/taxonomy.py` - the closed label sets and JSON schemas. Single source of truth.
- `scripts/classify_turns.py`, `scripts/classify_sessions.py` - LLM labelling, resumable.
- `scripts/mine_workflows.py` - sequence mining. Deterministic.
- `scripts/report.py` - rendering only. No new analysis.
- `data/` - generated, gitignored. `out/` - generated report.

## Invariants

1. **Measurements and judgements stay separable.** Counts, costs, latencies and motifs come from
   stages 1 and 4. Everything from stages 2-3 is an LLM opinion and must be labelled as such in
   any output. Never blend the two in one table without a column saying which is which.
2. **Stage 1 never calls a model.** It must run offline, and its output must be stable across runs
   given the same manifest.
3. **The corpus is frozen in `data/manifest.json`.** Re-picking silently would make two report
   runs incomparable. Changing the corpus is an explicit `--refresh`.
4. **Billing is per `message.id`.** Transcripts repeat an identical `usage` block on every record
   belonging to one API response.
5. **Costs are API list-price equivalents**, never described as spend.
6. Label changes invalidate labels: `task clean-labels` before re-classifying.

## Conventions

- Task runner is `Taskfile.yml`. No Makefile.
- Python 3.13 in `.venv`, managed with `uv`.
- Stage scripts take `--limit` / `--workers` / `--backend` and are safe to interrupt.

<!-- b10x-docs-operations:start -->
## Public documentation operations

This repository owns the public source and presentation allowlist in `b10x.docs.yaml`; the unified [beyond10x Website](https://beyond10x.github.io/docs/research/) passively collects those declared files from the exact commit in `website/sources.lock.json`. Atlas owns discovery grouping/order; Website and Docs System own rendering, shared components, search, and feeds. Do not add a standalone docs deployer or put App credentials in this public repository. If Atlas catalogs a former Pages workflow, that file remains repository-owned validation: preserve its bespoke checks while keeping exact read-only permissions, an unconditional pull-request trigger, and no deployment primitives. Project Pages at `/research/` is only the generated redirect façade in `.github/workflows/b10x-docs-pages.yml`.

From the complete organization workspace, verify the contract with a clean Atlas checkout at the current remote `main`. Set `B10X_ATLAS_CHECKOUT` to a managed Atlas worktree when the primary checkout is dirty or stale; never infer command availability from the primary alone.

```bash
atlas_checkout="${B10X_ATLAS_CHECKOUT:-atlas}"
atlas_head="$(git -C "$atlas_checkout" rev-parse HEAD)"
atlas_main="$(git -C "$atlas_checkout" ls-remote origin refs/heads/main | awk '{print $1}')"
test -z "$(git -C "$atlas_checkout" status --porcelain)"
test "$atlas_head" = "$atlas_main"
cargo run --manifest-path "$atlas_checkout/Cargo.toml" --locked -q -- \
  --store "$atlas_checkout/catalog/store" docs reconcile --workspace . --check
```

Keep internal plans, stories, ADRs, decisions, worklogs, security material, and research out of the public allowlist unless a repository authority explicitly declares them public.
<!-- b10x-docs-operations:end -->

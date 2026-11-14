# Literature evidence schema

**Version 1. Approved by the operator on 2026-11-14** (version 0 plus proposals P1 to P6).
A change to a field, a section or a closed set below needs the operator's approval. Until then a paper that does
not fit goes under *Schema proposals* at the end of this file, and the paper file keeps the current shape.

## Purpose

Collect evidence for methods that make autonomous agentic coding work, one paper at a time, and keep
one aggregated reading of it. The unit is not the paper. The unit is the **finding**: one practice or
one observed condition, the effect the paper reports for it, and the evidence the paper gives.

## Files

| file | holds | written by |
|---|---|---|
| `SCHEMA.md` | this schema and pending proposals | agent proposes, the operator approves |
| `queries.txt` | the arXiv queries, one per line | agent |
| `arxiv_search.py` | deterministic fetch of the query hits, no model calls | agent |
| `fetch_paper.py` | downloads metadata, PDF and extracted text of queued papers to the scratch directory | agent |
| `READER.md` | the two briefs a reader sub-agent gets | agent |
| `add_leads.py` | adds leads to `QUEUE.md` with title and date from the arXiv API | agent |
| `mark_read.py` | moves a queued line of `QUEUE.md` to its Read section | agent |
| `distil.py` | re-renders `DISTILLATION.md`: counts, order and placement from the paper files, texts from an additions file | agent |
| `check.py` | checks `DISTILLATION.md` against the paper files | agent |
| `QUEUE.md` | every candidate paper and its state: queued, read, skipped with a reason | agent |
| `papers/<arxiv-id>.md` | one file per paper read | agent |
| `DISTILLATION.md` | the aggregate, one section per slug | agent |

The paper's PDF and extracted text are not stored. They are re-downloadable from the `url` field.

## The loop

1. **Search.** `arxiv_search.py queries.txt` writes the hits to the scratch directory.
2. **Queue.** New hits that bear on the purpose go into `QUEUE.md`; a hit that is left out is not listed.
3. **Pick.** Newest first, at most 3 in a row on one topic, so the set stays broad.
4. **Read.** Full text, not the abstract. A paper read only in part says so in `read.coverage`.
   Reader procedure, from 5 Haiku runs on 2026-11-13: 1 run wrote a paper file (9 pages); 4 runs
   on papers of 24 pages (94 KB of text) and 51 pages (165 KB) ran out of context, 2 while
   re-reading the paper and 2 after finishing their notes, while re-reading the notes before writing.
   The notes of those 2 were complete and usable. So:
   - list the paper's sections with `grep -n` and choose the line ranges of the main text and the
     result-bearing appendices;
   - the reader reads each range once, at most 250 lines per call, and appends notes with
     locations and exact quotes to a scratch `notes.md` after each chunk;
   - the paper file is written from the notes, and numbers are checked with `grep` against the
     extracted text;
   - a Haiku reader takes notes only, and a larger model writes the file. `read.by` names every
     model involved.

   On 2026-11-14, 12 Sonnet readers each read one paper (5 to 37 pages, 43 KB to 157 KB of text)
   and wrote its file with the two briefs in `READER.md`: 12 of 12 files passed `check.py`, in 82 to
   190 seconds and 63,000 to 116,000 tokens per reader. Of 1,471 numbers in their evidence lines,
   1,455 occur in the paper texts; the other 16 are marked reader's arithmetic or carry a unit
   suffix (`5.61M`). The caller then changed 4 kinds and 3 slugs. So a Sonnet reader does the whole
   read, and the caller checks kinds, slugs and numbers.

   A second batch of 12 Sonnet readers on 2026-11-14 read papers of 11 to 72 pages (54 KB to
   402 KB of text): 12 of 12 files passed `check.py`, in 79 to 229 seconds and 77,000 to 135,000
   tokens per reader. Of 1,254 numbers in their evidence lines, 1,243 occur in the paper texts.
   The caller changed 3 slugs and no kind.

   A third batch of 13 Sonnet readers on 2026-11-14 read papers of 4 to 56 pages (24 KB to 282 KB
   of text), with at most 1,800 lines read per paper: 13 of 13 files passed `check.py`, in 69 to
   258 seconds and 63,000 to 136,000 tokens per reader. Of 1,497 numbers in their evidence lines,
   1,492 occur in the paper texts: 3 of the other 5 are marked reader's arithmetic, 1 rounds
   `-2.9e-03` to `-0.003`, and 1 was a rounded count ("about 830") that the caller replaced with
   the table's counts. The caller changed 4 slugs, no kind and 1 `read.coverage` line.

   A fourth batch of 12 Sonnet readers on 2026-11-14 read papers of 5 to 52 pages (36 KB to 227 KB
   of text), with at most 1,800 lines read per paper: 12 of 12 files passed `check.py`, in 74 to
   242 seconds and 64,000 to 123,000 tokens per reader. Of 1,212 numbers in their evidence lines,
   1,120 occur in the paper texts as written. Of the other 92, 85 are in one paper that prints
   `.08` for 0.08 (all 85 occur without the leading zero), 3 are printed with a unit suffix
   (`184s`), and 4 are marked reader's arithmetic. The caller changed 3 slugs and no kind.

   A fifth batch of 12 Sonnet readers on 2026-11-14 read papers of 10 to 43 pages (44 KB to 184 KB
   of text), with at most 1,800 lines read per paper: 12 of 12 files passed `check.py`, in 105 to
   254 seconds and 72,000 to 134,000 tokens per reader. Of 1,484 numbers in their evidence lines,
   1,462 occur in the paper texts as written. Of the other 22, 19 are printed in another form
   (`28.00`, `38, 447`, `107.8M`), 2 are marked reader's arithmetic and 1 is a share the reader
   derived from table counts (`73/73` as 100%). The caller changed 1 slug, no kind and 1 `design`
   value (experience-report to rct for 2402.05636, whose participants were divided at random).

   A sixth batch of 12 Sonnet readers on 2026-11-14 read papers of 5 to 52 pages (22 KB to 194 KB
   of text), with at most 1,800 lines read per paper: 12 of 12 files passed `check.py`, in 70 to
   233 seconds and 61,000 to 124,000 tokens per reader. Of 1,116 numbers in their evidence lines,
   1,113 occur in the paper texts as written. Of the other 3, 2 are the parts of a date printed
   in another form (`2026-05-04` for "4 May 2026") and 1 is marked reader's arithmetic. The
   caller changed 4 slugs, no kind and no `design` value.
   A seventh batch of 12 Sonnet readers on 2026-11-14 read papers of 5 to 37 pages (20 KB to
   181 KB of text), with at most 1,800 lines read per paper: 12 of 12 files passed `check.py`,
   in 60 to 276 seconds and 58,000 to 128,000 tokens per reader. All 1,280 numbers in their
   evidence lines occur in the paper texts as written. The caller changed 4 slugs, 1 kind and
   no `design` value. 4 of the 12 papers score no coding task (2605.23904, 2609.20625,
   2610.00372, 2610.29823); the `reader:` and `reading:` lines of their findings say so.
   An eighth batch of 12 Sonnet readers on 2026-11-14 read papers of 6 to 143 pages (41 KB to
   1,245 KB of text), with at most 1,800 lines read per paper: 12 of 12 files passed `check.py`,
   in 104 to 197 seconds and 77,000 to 132,000 tokens per reader. Of 1,400 numbers in their
   evidence lines, 1,392 occur in the paper texts as written and the other 8 are marked reader's
   arithmetic. The caller changed 6 slugs, 1 kind and no `design` value. 2 of the 12 papers score
   no coding task (2608.19013, 2608.22960), 1 codes practitioner documents (2607.07980) and 1
   counts policy texts (2609.07542).
   A ninth batch of 12 Sonnet readers on 2026-11-14 read papers of 4 to 33 pages (33 KB to 195 KB of
   text): 12 of 12 files passed `check.py`, in 84 to 288 seconds and 66,000 to 145,000 tokens per
   reader. Of 1,480 numbers in their evidence lines, 1,476 occur in the paper texts as written and
   the other 4 are marked reader's arithmetic. The caller changed 5 slugs, 2 kinds and no `design`
   value. 2 of the 12 papers score no coding task (2608.12307, 2610.27301), 1 counts policy texts
   (2609.07919) and 1 studies human reviewers of agent PRs (2609.06213).
5. **Write** `papers/<arxiv-id>.md` in the shape below.
6. **Distil.** Add each finding to its slug in `DISTILLATION.md` with `distil.py` (one evidence
   line per finding, a description and a reading per new slug); mark the paper read with
   `mark_read.py`; follow the paper's leads into `QUEUE.md`; run `python3 -I literature/check.py`
   from the repository root.

## Two kinds of field

Invariant 1 of this repository applies: measurements and judgements stay separable.

- **paper** fields are copied from the paper and carry a location (`§4.2`, `Table 5`, `p. 12`).
  A paper field the paper does not give is written `not stated`, never left out and never guessed.
- **reader** fields are an LLM's judgement about the paper. They are `design`, `controlled`,
  `independent`, every finding's kind, grade, `effect:` and `reader:` line, and the sections
  *Reader's notes* and *Discrepancies*. In `DISTILLATION.md` the `reading:` line is a reader field.

A number that appears in a paper file was read from the paper. Arithmetic done by the reader is marked
`(reader's arithmetic)`.

## `papers/<arxiv-id>.md`

Front matter:

```yaml
schema: 1
id: arxiv:2604.09388          # paper
version: v2                   # paper: the version that was read
title: ...                    # paper
authors: [...]                # paper
affiliation: ...              # paper
submitted: 2026-04-10         # paper: v1 date
revised: 2026-04-27           # paper: date of the version read, when not v1
categories: [cs.SE, cs.AI]    # paper
url: https://arxiv.org/abs/2604.09388v2
read:
  by: claude-fable-5-2        # every model that read the paper or wrote this file
  on: 2026-11-13
  coverage: 28 of 28 pages, PDF text
design: experience-report     # reader: closed set below
subjects: ...                 # paper: who or what was studied, with counts
agents: [...]                 # paper: the coding agents and models used
period: 2025-12 to 2026-04    # paper: the dates the data covers
controlled: false             # reader: true when at least one finding is graded E4, nothing else
independent: false            # reader: true when the evaluators are neither the authors nor the
                              #   vendor of the system or product that is evaluated
artifacts: [...]              # paper: code or data the paper links
```

Body, in this order:

- `## Question`: the paper's question in one or two lines. paper.
- `## Findings`: one block per finding, numbered `F1`, `F2`, … and never renumbered.
- `## Limits stated by the authors`: paper.
- `## Reader's notes`: confounds and gaps the authors do not state. reader.
- `## Discrepancies`: places where the paper contradicts itself. reader.
- `## Leads`: cited work worth queueing.

A finding block:

```markdown
### F4 · practice · acceptance-rate-feedback · E2
- practice: what was done, concretely enough to repeat; for an observation, what was observed.
- claim: the effect the paper claims.
- evidence: the numbers or cases given, each with its location.
- effect: helps
- reader: why this grade and this effect; the confound that matters most.
```

The heading is `F<n> · <kind> · <slug> · <grade>`. A finding with no claimed effect is not a finding.

## Closed sets

**Kind** of a finding:

| value | meaning |
|---|---|
| `practice` | something a team or a study chose to do with or around a coding agent, and its effect |
| `observation` | how agent work fares under a condition nobody applied as a treatment: a setting, a subgroup, a property of agent output |

**`effect`**, the direction the paper reports for the practice or observed condition, on the outcome
that finding measures. It records the paper's result at the finding's grade, not the reader's belief:

| value | meaning |
|---|---|
| `helps` | the outcome is better with the practice or condition |
| `hurts` | the outcome is worse, or the cost is higher with no gain |
| `none` | no difference was found |
| `mixed` | better on one outcome or subgroup and worse on another |

**Grade**, the strength of the evidence the paper gives for one finding's claim:

| grade | name | the paper shows |
|---|---|---|
| `E4` | controlled | the practice against a control: randomisation, an ablation, an A/B on equal tasks |
| `E3` | compared | numbers before and after, or between groups, with no control |
| `E2` | described | numbers that describe the practice or its outcome, with nothing to compare against |
| `E1` | anecdote | one or a few concrete cases |
| `E0` | asserted | the claim only |

The grade is about the claim, not the paper. One paper can hold an `E4` finding and an `E0` finding.

**`design`**, the paper's main design:

| value | meaning |
|---|---|
| `rct` | randomised controlled trial with human participants |
| `benchmark-eval` | agents scored on a task benchmark, with or without ablations |
| `repo-mining` | observational study over many repositories or pull requests |
| `user-study` | interviews, surveys or observed sessions without randomisation |
| `case-study` | one or a few projects studied by outside researchers |
| `experience-report` | the authors report on their own project or system |
| `literature-review` | a review of other papers |
| `position` | an argument without new data |

## Open sets

**Slugs** are an open vocabulary: lowercase, hyphenated, named for what is done or observed
(`external-work-ledger`), not for a product (`beads`). `DISTILLATION.md` holds the list in use. A new
slug needs no approval. Merging or renaming one is recorded in its section there.

## `DISTILLATION.md`

- A header with counts: papers read, findings, findings per grade, per kind and per effect.
- `## Practices` and `## Observations`, one section per slug. A slug whose findings are all
  observations is under `## Observations`; every other slug is under `## Practices`.

```markdown
### acceptance-rate-feedback
What is done or observed, in one line.
- reading: what the evidence so far supports, in one line. (reader)
- best grade: E2 · papers: 1 · helps 1 · hurts 0 · none 0 · mixed 0
- E2 · helps · 2604.09388 F4 · the number or case, in one line
```

- Every evidence line names a paper file and a finding number that exist, with the same grade and
  effect as the paper file. Nothing enters the distillation that is not in a paper file.
- `## Contradictions` lists slugs where findings disagree, and says what each side measured.
- `check.py` fails when an evidence line, a count line or the header disagrees with the paper files.

## `QUEUE.md`

A search log, then three sections: `## Read`, `## Skipped`, `## Queued`. One line per candidate,
newest first. `## Queued` is split by topic heading so that picking can stay broad; the topics are an
open set.

```markdown
- [ ] 2604.09388 · 2026-04-10 · Title
- [ ] 2302.06590 · 2023-02 · Title · lead from 2604.09388
- [x] 2604.09388 · 2026-04-10 · Title · read 2026-11-13
- [-] 2604.09388 · 2026-04-10 · Title · skipped: reason
```

## Schema proposals

Open, from the 109 papers read on 2026-11-14. The files keep the version 1 shape until the operator
decides.

- **P7: three more count lines in the header of `DISTILLATION.md`.** `at E4 by effect`,
  `at E4, independent papers`, `at E4, other papers`. Already rendered by `distil.py` and checked
  by `check.py`, because they are counts over existing fields; rejecting P7 removes the 3 lines.
  Why: at 16 papers, 17 of the 19 `helps` findings at E4 come from papers whose authors evaluate
  their own system, and the plain count per effect hides that.
- **P8: an `outcome:` field per finding**, closed set `success`, `cost`, `time`, `quality`,
  `compliance`, `perception`, `reporting`. Why: `effect` is a direction on "the outcome that
  finding measures", and the outcome is only in prose. 2611.13241 F1 is `helps` on tokens and F2 is
  `none` on resolve rate for the same practice; 2507.09089 F2 and 2410.18334 F11 sit in one slug
  with `hurts` and `helps` and agree in substance. The count line per slug adds them up.
- **P9: a fifth `effect` value, `describes`,** for an observation that reports a share or a
  distribution with no direction. Why: the schema says a finding with no claimed effect is not a
  finding, and 3 readers still met them and chose `hurts` or `mixed` (2611.10058 F2 and F8,
  2610.35348 F1 to F6, 2611.13241 F9). Without P9 those findings are either dropped or carry a
  direction the paper does not claim. In the third batch 5 more readers chose `hurts` or `mixed`
  for such findings (2611.04367 F4 and F5, 2608.21311 F1 to F4, 2608.23067 F4 and F7, 2611.00314
  F11 to F13, 2611.02207 F12), and 2 left results out of the findings for want of a direction:
  the prevalence of AI review in 2608.21311 (8.8% of agent PRs) and the change of model ranking
  under task switching in 2611.02017. In the fourth batch 5 readers chose a direction for such
  findings (2607.26375 F4, F5 and F9; 2607.13091 F4 and F10; 2610.36254 F2 and F8; 2609.32459 F2,
  F3 and F15; 2610.06406 F11), and the reader of 2611.02383 left 4 results out: adoption by
  repository popularity, the shares of the 4 file formats, maintenance statistics, and heading
  additions against deletions. In the fifth batch 8 readers chose a direction for such findings
  (2608.08453 F1 and F6; 2608.09290 F9; 2609.39957 F8 and F11; 2609.20812 F1, F2, F6, F9 and F10;
  2606.14249 F2, F10 and F13; 2610.35992 F5 and F13; 2611.07286 F10 and F11; 2610.35971 F6 and
  F8), and 2 left results out: delegation scale and timing in 2610.10263, run-to-run discordance
  in 2610.35992. The reader of the survey 2610.11179 reports that `effect` there is the direction
  respondents state and no measured outcome, which is P8. In the sixth batch 4 readers chose a
  value for such findings (2607.00911 F1, F3, F4, F6 and F7; 2609.01985 F6 and F7; 2610.32578 F1,
  F8, F10 and F12; 2609.37985 F1, F12 and F13), and 2 left results out: the seven-stage
  supervision framework and its coded-quote shares in 2609.24234, the root-cause distribution in
  2609.37985. The reader of 2607.00911 wrote `none` on 5 descriptive findings, so the `none`
  count now holds findings that measured no effect next to findings that measured one of zero.
  In the seventh batch 6 readers chose a value for such findings (2208.09727 F4 and F5;
  2605.23904 F14; 2609.05364 F2; 2609.20625 F7; 2609.26847 F2 and F3; all 11 findings of the
  census 2610.31715, whose reader left pure prevalences out), and 2 left results out: AI
  reviewer use by PR type in 2607.13196, the T2 resolution result in 2610.04779.
  In the eighth batch 3 readers chose a value for such findings (2608.30572 F3 and F4;
  2608.22960 F2, F3, F4, F7 and F10; all 10 findings of the policy census 2609.07542, filed as
  `none`), 1 folded a task distribution into another finding (2607.21832 F4), and 3 left
  results out: the position of the first edit in 2610.29870, the share of revisions that change
  a rule in 2610.04832, the failure-stage distribution in 2609.20804.
  In the ninth batch 8 readers chose a value for such findings (2609.26781 F6; 2609.06213 F1, F2 and
  F6; 2609.35381 F1; 2609.07919 F1 to F8, filed as `none`; 2610.27301 F7, F8 and F15; 2610.38244 F2
  and F13; 2608.25202 F3, F4, F5 and F14; 2609.03028 F2 and F7), and 2 left results out: the share
  of events after the session midpoint, the trigger mix and the semantic-audit split in 2609.03028,
  the residual-error profile and the builder-adaptation result in 2608.12307.
- **P10: topic headings in `DISTILLATION.md`.** At 113 papers, 944 slugs, 866 of them with one
  paper, are a flat list of 6,444 lines ordered by grade (148 slugs and 963 lines at 16
  papers).
  Proposal: group the slug sections under the open topic set
  of `QUEUE.md` (instruction files, skills, harness, tests and verification, review, plans,
  multi-agent, memory and long runs, oversight, self-improvement, trials and field data), with the
  topic stored once per slug in `DISTILLATION.md`.
- **P11: a ninth `design` value, `agent-experiment`,** for a study that runs agents under assigned
  conditions on tasks the authors built for it, with no task benchmark and no human participants.
  Why: 3 papers carry `benchmark-eval` as the closest value and score no benchmark: 2610.11647
  (312 skill pairs, 6,368 runs), 2611.09802 (3 stale lines, 732 runs), 2611.00689 (926 runs of
  agent teams). 2 of their readers reported the misfit, and 3 readers of the third batch did
  (2611.04367, 2610.38214, 2611.02207). In the fifth batch 4 readers did: 2610.09995 (one
  translation task run 14 times, filed as `experience-report`), 2609.20812 and 2610.35992 (filed
  as `benchmark-eval`), and 2610.35971 (replays of recorded runs, filed as `repo-mining`). In the
  sixth batch 4 readers did: 2610.07261, 2610.29869 and 2610.04375 (author-built scenarios, filed
  as `benchmark-eval`) and 2610.32578 (replays in one repository, filed as `experience-report`).
  In the seventh batch 3 readers did: 2609.08371 and 2609.20625 (author-built tasks and
  incidents, filed as `benchmark-eval`) and 2610.04779 (a predictor study on replayed PR pairs,
  filed as `repo-mining` with `controlled: true`).
  In the eighth batch 4 readers did: 2608.22960 (measurement procedures on recorded
  file-localization episodes), 2610.30571 (40 author-built projects) and 2609.20804, all filed
  as `benchmark-eval`, and 2607.07980 (a theory built from practitioner documents, filed as
  `user-study`).
  In the ninth batch 4 readers did: 2610.38244, 2608.12307 and 2610.27301 (filed as
  `benchmark-eval`) and 2609.03028 (an author-built agent experiment inside a `repo-mining` paper).

Decided:

- P1 to P6, approved 2026-11-14 and merged into version 1: findings have a kind (P1), `controlled`
  is derived from the grades (P2), `independent` is defined (P3), `period` is the data window (P4),
  `not stated` is written out (P5), every finding has an `effect` (P6).
- Not adopted: a per-finding `split:` field for what a comparison divides on, suggested by the
  reader of 2609.17598. The `evidence:` line holds it.

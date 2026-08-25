# Where does the human actually sit in the loop?

*Corpus: 100 Claude Code sessions, 2026-08-11 to 2026-08-25. Generated 2026-08-25 13:09.*

## 1. Corpus

| metric | value |
|---|---|
| sessions | 100 |
| &nbsp;&nbsp;of which headless (`claude -p`, no human) | 18 |
| distinct projects | 22 |
| human turns | 1567 |
| agent messages | 33,327 |
| tool calls | 33,293 |
| sub-agents spawned | 714 |
| output tokens | 26,599,080 |
| cache-read tokens | 13,476,686,661 |
| API-list-price equivalent | $10,179 |
| wall-clock across sessions (sessions overlap) | 673 h |
| &nbsp;&nbsp;active, gaps over 5 min excluded | 222 h |
| tool calls per human turn (median) | 9 |

<details><summary>by project</summary>

| project | sessions | human turns | tool calls | $ equiv |
|---|---|---|---|---|
| daemonloom-daemonloom | 24 | 432 | 11,230 | 3,786 |
| babelforce-projects-company-brain | 25 | 561 | 10,686 | 3,027 |
| projects-engineering-protocols | 7 | 226 | 5,438 | 1,756 |
| beyond10x | 4 | 79 | 1,569 | 408 |
| projects-flux-connectors | 1 | 17 | 533 | 287 |
| projects-autodev | 4 | 57 | 879 | 234 |
| daemonloom | 2 | 34 | 620 | 202 |
| projects-flux-roadmap | 3 | 48 | 435 | 160 |
| babelforce-projects-sbf-acd | 1 | 21 | 686 | 135 |
| babelforce-projects-ai-selfhosted-inference | 3 | 44 | 374 | 73 |
| projects-flux-exchange | 1 | 17 | 310 | 63 |
| ~ | 10 | 17 | 341 | 29 |
| beyond10x-metaharness | 1 | 3 | 95 | 8 |
| selfdirect | 2 | 6 | 28 | 6 |
| projects-infra-scout | 1 | 3 | 16 | 1 |
| beyond10x-infra-scout | 2 | 2 | 16 | 1 |
| -cache-claude-tmp-plugin-eval-MFN9tB-project | 1 | 0 | 12 | 0 |
| -cache-claude-tmp-plugin-eval-xnRL8e-project | 1 | 0 | 12 | 0 |
| -cache-claude-tmp-plugin-eval-3Rgmwv-project | 1 | 0 | 13 | 0 |
| -cache-claude-tmp-probe | 3 | 0 | 0 | 0 |
| projects-engineering-protocols--claude-worktrees-proof-run-w4-2 | 2 | 0 | 0 | 0 |
| -cache-claude-tmp-plugin-eval-M7ZtU4-project | 1 | 0 | 0 | 0 |

</details>

## 2. What a human turn actually looks like

| metric | value |
|---|---|
| median length | 64 chars / 11 words |
| turns under 10 words | 44% |
| median tool calls the turn triggers | 9 |
| turns that trigger no tool at all | 14% |
| turns that interrupt a running agent | 1% |
| entered as slash command | 201 |
| entered while agent was busy (queued) | 91 |

**Agent idle waiting for a human**: median 122 s between the agent finishing and the human replying, p90 1244 s, 229 h in total - 34% of all session wall-clock.

## 3. Classification of human input

**Intent**

| label | turns | share |
|---|---|---|
| initiate_task | 324 | 21% |
| approve_proceed | 190 | 12% |
| refine_scope | 145 | 9% |
| meta_process | 136 | 9% |
| ask_question | 130 | 8% |
| correct_error | 123 | 8% |
| supply_info | 121 | 8% |
| housekeeping | 101 | 6% |
| resume_continue | 70 | 4% |
| request_status | 67 | 4% |
| reject_redirect | 56 | 4% |
| request_verification | 54 | 3% |
| delegate_parallel | 39 | 2% |
| interrupt_abort | 9 | 1% |
| social | 2 | 0% |

**Task kind**

| label | turns | share |
|---|---|---|
| planning_design | 219 | 14% |
| release_deploy | 190 | 12% |
| implement | 182 | 12% |
| meta_agent_config | 140 | 9% |
| config_env | 134 | 9% |
| debug | 127 | 8% |
| communication | 107 | 7% |
| other | 106 | 7% |
| research_explore | 71 | 4% |
| review | 70 | 4% |
| test | 60 | 4% |
| ops_incident | 51 | 3% |
| data_analysis | 38 | 2% |
| docs_write | 37 | 2% |
| refactor | 33 | 2% |
| housekeeping | 2 | 0% |

**Motivation**

| label | turns | share |
|---|---|---|
| deliver_artifact | 390 | 25% |
| steer_quality | 253 | 16% |
| unblock_agent | 221 | 14% |
| verify_trust | 183 | 12% |
| save_cost_time | 159 | 10% |
| fix_agent_mistake | 124 | 8% |
| explore_options | 77 | 5% |
| enforce_standard | 72 | 5% |
| personal_preference | 50 | 3% |
| curiosity | 38 | 2% |

**Sentiment**

| label | turns | share |
|---|---|---|
| neutral | 734 | 47% |
| terse_pressing | 687 | 44% |
| frustrated | 83 | 5% |
| positive | 58 | 4% |
| appreciative | 5 | 0% |

**Information the human contributed**

| label | turns | share |
|---|---|---|
| none | 660 | 42% |
| goal | 244 | 16% |
| external_state | 196 | 12% |
| preference | 174 | 11% |
| judgment_call | 164 | 10% |
| domain_knowledge | 129 | 8% |

## 4. Can this turn be replaced?

| replaceable by | turns | share |
|---|---|---|
| human_only | 687 | 44% |
| ai_policy | 363 | 23% |
| deterministic_rule | 306 | 20% |
| ai_with_context | 211 | 14% |

**Rework**: 20% of human turns (313 of 1567) exist only because the agent erred or stopped short.

**Friction source**

| source | turns | share |
|---|---|---|
| none | 1056 | 67% |
| agent_omission | 278 | 18% |
| agent_error | 110 | 7% |
| missing_context | 54 | 3% |
| tool_failure | 49 | 3% |
| ambiguous_spec | 20 | 1% |

**Which intents are the automatable ones** (rows sorted by volume)

| intent | n | deterministic_rule | ai_policy | ai_with_context | human_only | % removable |
|---|---|---|---|---|---|---|
| initiate_task | 324 | 40 | 21 | 47 | 216 | 19% |
| approve_proceed | 190 | 28 | 87 | 7 | 68 | 61% |
| refine_scope | 145 | 0 | 11 | 32 | 102 | 8% |
| meta_process | 136 | 84 | 15 | 0 | 37 | 73% |
| ask_question | 130 | 1 | 45 | 73 | 11 | 35% |
| correct_error | 123 | 6 | 46 | 16 | 55 | 42% |
| supply_info | 121 | 16 | 3 | 9 | 93 | 16% |
| housekeeping | 101 | 59 | 5 | 2 | 35 | 63% |
| resume_continue | 70 | 44 | 23 | 1 | 2 | 96% |
| request_status | 67 | 20 | 45 | 1 | 1 | 97% |
| reject_redirect | 56 | 0 | 8 | 10 | 38 | 14% |
| request_verification | 54 | 6 | 36 | 7 | 5 | 78% |
| delegate_parallel | 39 | 0 | 15 | 6 | 18 | 38% |
| interrupt_abort | 9 | 1 | 3 | 0 | 5 | 44% |
| social | 2 | 1 | 0 | 0 | 1 | 50% |

**Most frequent trigger -> action rules the model extracted**

| rule | times |
|---|---|
| context window near limit -> compact automatically | 6 |
| context window near threshold -> run compaction automatically | 4 |
| new unrelated task starting -> clear session context | 4 |
| new unrelated task starts -> clear conversation context | 3 |
| context window near threshold -> compact automatically | 2 |
| session context stale or task finished -> clear conversation context | 2 |
| new work session starts -> clear context | 2 |
| context near limit -> compact automatically | 2 |
| context stale or new task starting -> clear conversation history | 2 |
| context stale or task finished -> clear conversation history | 2 |
| new unrelated task starts -> clear context | 2 |
| next wave plan presented -> approve implement/test/document/push | 2 |
| new unrelated task starting -> clear conversation context | 2 |

## 5. Session outcomes

| outcome | sessions |
|---|---|
| success | 41 |
| partial | 39 |
| abandoned | 11 |
| failed | 6 |
| open_ended | 3 |

| automation verdict | sessions |
|---|---|
| auto_with_gates | 37 |
| needs_human_judgment | 34 |
| full_auto | 27 |
| not_automatable | 2 |

| human repair share of session | sessions |
|---|---|
| none | 47 |
| low | 25 |
| medium | 23 |
| high | 5 |

## 6. Workflow archetypes

| archetype | sessions | $ equiv | success | verdict spread |
|---|---|---|---|---|
| ops_investigation | 19 | 1,779 | 7/19 | auto_with_gates:10, needs_human_judgment:8, full_auto:1 |
| other | 17 | 1,663 | 2/17 | full_auto:12, needs_human_judgment:3, not_automatable:1, auto_with_gates:1 |
| agent_harness_tuning | 11 | 1,773 | 4/11 | full_auto:6, needs_human_judgment:4, auto_with_gates:1 |
| greenfield_scaffold | 10 | 1,482 | 5/10 | auto_with_gates:7, needs_human_judgment:3 |
| refactor_sweep | 9 | 742 | 4/9 | needs_human_judgment:5, auto_with_gates:4 |
| multi_agent_fanout | 7 | 1,595 | 3/7 | needs_human_judgment:4, auto_with_gates:3 |
| review_and_gate | 7 | 340 | 4/7 | auto_with_gates:3, needs_human_judgment:3, full_auto:1 |
| backlog_grooming | 5 | 23 | 4/5 | full_auto:3, auto_with_gates:1, needs_human_judgment:1 |
| doc_or_report_write | 4 | 27 | 3/4 | auto_with_gates:2, full_auto:1, not_automatable:1 |
| exploratory_chat | 3 | 1 | 1/3 | full_auto:2, auto_with_gates:1 |
| release_cut | 3 | 504 | 1/3 | needs_human_judgment:2, auto_with_gates:1 |
| ticket_to_pr | 2 | 107 | 1/2 | auto_with_gates:2 |
| research_brief | 2 | 8 | 2/2 | auto_with_gates:1, full_auto:1 |
| bug_hunt_fix | 1 | 135 | 0/1 | needs_human_judgment:1 |

**Recipes actually executed** (most common opening verbs per archetype)

- **ops_investigation** (19 sessions): run, load, run, query, send, fan, run, create
- **other** (17 sessions): receive, invoke, reset, attempt, terminate, hit, emit, issue
- **agent_harness_tuning** (11 sessions): send, capture, run, let, load, run, commit, emit
- **greenfield_scaffold** (10 sessions): write, run, add, fetch, run, commit, commit, create
- **refactor_sweep** (9 sessions): inventory, replace, inspect, commit, run, report, fan, create
- **multi_agent_fanout** (7 sessions): read, run, fan, run, run, file, fan, review
- **review_and_gate** (7 sessions): read, check, fetch, post, run, load, load, run
- **backlog_grooming** (5 sessions): load, read, write, write, write, record, run, list

**Blockers to unattended execution**

| blocker | sessions |
|---|---|
| repo-visibility and gh-pages publishing are irreversible acts needing approval | 1 |
| commit/push/release gated by explicit-instruction policy | 1 |
| story lifecycle transitions are project-state claims reserved for the operator | 1 |
| semantic design choice (absent vs three-valued not-exists) had no test or spec to decide it | 1 |
| one api error and 5 tool errors; 2 context compactions indicate unattended runs risk losing thread | 1 |
| ambiguous initial spec (callback vs copy-paste token) needed human framing | 1 |
| no commit/rebase autonomy under repo policy — git writes require explicit approval | 1 |
| secret-scan before public release needs a human accept/reject gate, not just a tool run | 1 |
| release publish job only executes on real tag push, so end-to-end path is unverified | 1 |
| ci runner scheduling latency (macos-13) makes unattended completion time unbounded | 1 |
| review-finding triage had no scored severity gate; the human arbitrated | 1 |
| production tenant config write needs explicit authority; not safely unattended | 1 |
| diagnosis rests on code reading with no runtime verification — agent itself flags this | 1 |
| slack posting that contradicts two colleagues' conclusions requires human sign-off | 1 |
| incident scope arrived as informal slack chatter, not a ticket with a spec | 1 |
| brief generation encoded a wrong release-process model until a human corrected it | 1 |
| interactive oauth/credential entry | 1 |
| no task content in the session to automate | 1 |
| github org rename and github app creation/transfer require owner auth in a web ui | 1 |
| production secret rotation/copy needs credentials and an irreversible-action approval | 1 |

**The approval tax** - turns that carried no information the agent did not already have:

| metric | value |
|---|---|
| such turns | 748 (48% of labelled turns) |
| consecutive runs of them | 355 |
| longest run | 9 |

**Where each intent shows up in a session**

| phase | initiate_task | approve_proceed | refine_scope | ask_question | meta_process | correct_error | supply_info | housekeeping |
|---|---|---|---|---|---|---|---|---|
| opening | 138 | 50 | 48 | 45 | 67 | 25 | 44 | 0 |
| middle | 90 | 69 | 50 | 45 | 31 | 48 | 33 | 38 |
| closing | 81 | 67 | 46 | 40 | 25 | 49 | 43 | 35 |

**Outcome against how much the human intervened**

| human turns | abandoned | failed | open_ended | partial | success | n |
|---|---|---|---|---|---|---|
| 0 (headless) | 0 | 6 | 2 | 0 | 10 | 18 |
| 1-3 | 8 | 0 | 1 | 0 | 17 | 26 |
| 11-30 | 2 | 0 | 0 | 13 | 6 | 21 |
| 31+ | 0 | 0 | 0 | 17 | 2 | 19 |
| 4-10 | 1 | 0 | 0 | 9 | 6 | 16 |

## 7. Mined operation sequences (workflow candidates)

Operation classes are derived from tool calls and shell command heads; runs of the same op are folded (`edit*`). A motif is kept only if no longer motif has the same count.

**Per human turn** - what one instruction expands into

| motif | occurrences | sessions |
|---|---|---|
| inspect > edit | 595 | 64 |
| inspect* > edit | 548 | 61 |
| edit > inspect | 508 | 61 |
| edit > inspect* | 442 | 59 |
| inspect > edit* | 330 | 55 |
| edit > run_script | 505 | 53 |
| edit* > inspect | 261 | 53 |
| inspect* > edit* | 299 | 50 |
| run_script > edit | 389 | 49 |
| inspect > run_script | 586 | 47 |
| edit* > run_script | 198 | 47 |
| run_script > inspect | 491 | 46 |
| other_cmd > inspect | 190 | 46 |
| edit* > inspect* | 157 | 45 |
| inspect > edit > inspect | 137 | 45 |
| edit > inspect > edit | 163 | 44 |
| inspect* > run_script | 384 | 43 |
| run_script > inspect* | 332 | 43 |

**Per session** - the longer arcs

| motif | occurrences | sessions |
|---|---|---|
| inspect > edit > inspect | 141 | 46 |
| edit > inspect > edit | 172 | 45 |
| edit* > inspect > edit | 87 | 44 |
| inspect* > edit > inspect* | 166 | 43 |
| inspect > edit > run_script | 93 | 42 |
| inspect* > edit > inspect | 115 | 40 |
| edit > inspect* > edit | 151 | 37 |
| run_script > edit > run_script | 125 | 35 |
| inspect > edit > inspect* | 111 | 35 |
| edit* > inspect > edit* | 95 | 35 |
| inspect* > edit* > inspect | 87 | 34 |
| edit > run_script > inspect | 75 | 34 |
| edit > run_script > edit | 134 | 33 |
| inspect > edit* > inspect | 100 | 33 |
| edit > inspect > edit* | 80 | 33 |
| edit > inspect* > edit* | 70 | 33 |
| run_script > inspect > run_script | 183 | 32 |
| inspect > run_script > inspect | 168 | 32 |

**Shell-level, plumbing removed**

| motif | occurrences | sessions |
|---|---|---|
| python3 > import | 1626 | 58 |
| git status > git log | 124 | 40 |
| git log > git status | 143 | 39 |
| git add > git commit | 551 | 34 |
| git add > git status | 77 | 34 |
| git status > python3 | 61 | 33 |
| git status > git diff | 65 | 30 |
| python3* > import | 212 | 29 |
| python3 > git add | 143 | 29 |
| git commit > git log | 144 | 28 |
| git status > git add | 70 | 28 |
| git diff > git status | 38 | 28 |
| " > python3 | 135 | 26 |
| python3 > git status | 54 | 26 |
| import > d=json.load(sys.stdin) | 142 | 25 |

**Interaction loop** - what the human does, in order

| motif | occurrences | sessions |
|---|---|---|
| meta_process > initiate_task | 52 | 38 |
| initiate_task > approve_proceed | 49 | 35 |
| initiate_task > refine_scope | 41 | 28 |
| initiate_task > initiate_task | 53 | 24 |
| housekeeping > initiate_task | 30 | 23 |
| refine_scope > initiate_task | 29 | 21 |
| initiate_task > correct_error | 27 | 21 |
| approve_proceed > initiate_task | 32 | 19 |
| ask_question > initiate_task | 23 | 17 |
| correct_error > initiate_task | 20 | 17 |
| approve_proceed > approve_proceed | 25 | 16 |
| initiate_task > supply_info | 19 | 15 |
| approve_proceed > refine_scope | 18 | 15 |
| refine_scope > refine_scope | 19 | 14 |
| initiate_task > meta_process | 18 | 14 |
| approve_proceed > housekeeping | 17 | 14 |
| initiate_task > housekeeping | 21 | 13 |
| supply_info > initiate_task | 19 | 13 |

**Trigger -> procedure**: given an intent, what the agent then ran

| human intent | n | top operation signature | share |
|---|---|---|---|
| initiate_task | 324 | (no tools) | 7% |
| initiate_task | 324 | inspect > edit > inspect* | 3% |
| approve_proceed | 190 | (no tools) | 3% |
| approve_proceed | 190 | inspect* > edit > inspect* | 2% |
| refine_scope | 145 | (no tools) | 6% |
| refine_scope | 145 | edit | 3% |
| meta_process | 136 | (no tools) | 74% |
| meta_process | 136 | ask_human > inspect > agent_cli* | 1% |
| ask_question | 130 | (no tools) | 29% |
| ask_question | 130 | inspect* | 5% |
| correct_error | 123 | (no tools) | 6% |
| correct_error | 123 | inspect > edit > run_script | 3% |
| supply_info | 121 | (no tools) | 3% |
| supply_info | 121 | edit > inspect* > fs_mutate | 2% |
| housekeeping | 101 | vcs_read | 5% |
| housekeeping | 101 | vcs_read > edit > vcs_read | 3% |
| resume_continue | 70 | (no tools) | 7% |
| resume_continue | 70 | inspect > edit > inspect | 3% |
| request_status | 67 | (no tools) | 27% |
| request_status | 67 | edit | 8% |

## 8. The bill for the human in the loop

| quantity | value | how it is derived |
|---|---|---|
| human turns | 1567 | measured |
| turns a rule or a policy could emit | 669 (43%) | classifier judgement |
| median agent idle before a human replies | 122 s | measured |
| idle time behind those turns | 23 h | removable turns x median idle - upper bound, assumes serial waiting |
| total agent idle waiting on a human | 229 h (34% of session wall-clock) | measured |

Weighted by what each session cost to run:

| verdict | sessions | $ equiv | share of spend |
|---|---|---|---|
| needs_human_judgment | 34 | 8,423 | 83% |
| auto_with_gates | 37 | 1,733 | 17% |
| full_auto | 27 | 17 | 0% |
| not_automatable | 2 | 6 | 0% |

## 9. Candidate workflows

| workflow | archetype | sessions | autonomy | steps | gates |
|---|---|---|---|---|---|
| `incident-thread-to-verified-root-cause-and-gated-fix` | ops_investigation | 19 | auto_with_gates | 18 | 7 |
| `harness-eval-gate` | agent_harness_tuning | 11 | auto_with_gates | 12 | 5 |
| `design-doc-to-scaffolded-repo` | greenfield_scaffold | 10 | auto_with_gates | 17 | 5 |
| `org-wide-rename-sweep` | refactor_sweep | 9 | auto_with_gates | 12 | 5 |
| `backlog-wave-fanout-integrate` | multi_agent_fanout | 7 | auto_with_gates | 14 | 5 |
| `mr-review-and-gate-runner` | review_and_gate | 7 | auto_with_gates | 17 | 5 |
| `intake-to-groomed-backlog-artifacts` | backlog_grooming | 5 | auto_with_gates | 14 | 5 |
| `doc-change-to-verified-broadcast` | doc_or_report_write | 4 | auto_with_gates | 15 | 5 |
| `session-resume-briefing` | exploratory_chat | 3 | auto_with_gates | 9 | 1 |
| `release-cut-gated-pipeline` | release_cut | 3 | auto_with_gates | 16 | 5 |

### `incident-thread-to-verified-root-cause-and-gated-fix` - Turns a monitored incident signal into evidenced root cause and gated production fix

- **evidence**: 19 sessions labelled `ops_investigation`
- **trigger**: Channel/gate watcher fires: a new thread in a monitored incident channel (#sre, #dev-team, #<customer>-internal) matching customer/service/symptom patterns, OR a monitored pipeline/readiness gate flips red, OR a scheduled 08:00 re-check cron tick for an open verification
- **autonomy**: auto_with_gates
- **removes**: All routine initiation turns (//knowledge, //refresh, //workday, //brief, //clear and their <user> variants) become the trigger and step 2. All bare continuation turns ('continue', 'again', 'go on') are dropped — they carried no information and are not gates. Routine 'commit and push' after a clean round becomes step 17. Default-matching approvals ('1 yes 2 1y 3 no') are resolved by stated defaults. Restating known prior art ('lookup what I mean') is replaced by the brain-cache grep in step 3. Retained as gates only: irreversible prod writes, outward-facing posts, priority/policy calls and outside-the-machine facts.
- **preconditions**: Slack channel watcher with read access to the monitored channels, emitting channel+ts (not a human-pasted permalink); Local company-brain/knowledge store cloned, with /knowledge, /refresh, /workday, /brief runnable headlessly and their gates (status-lean, verify-token, worklog-order, dirty-buckets) exit-coded; Read access to backend DB, ACD/NATS state, and the service-token endpoint able to mint an ephemeral manager token for the affected account owner; git clone access to config/chart repos (GitLab file API is not sufficient — it truncates at 65kb); kubectl/port-forward access to the affected cluster namespace plus homer for wire-level call records; A registered approver identity reachable for the two blocking gates (prod write, customer-facing post)

| # | step | kind | fails if |
|---|---|---|---|
| 1 | Resolve the trigger event to channel+ts; fetch the thread, all replies, and any linked card/ticket/MR | deterministic | thread or replies cannot be fetched, or the event yields no customer/service/DID/module identifier to key the investigation on |
| 2 | Run /knowledge dirty-buckets then /refresh and /workday to hydrate operator context and flags | deterministic | refresh exits non-zero, or the store is still reported dirty/stale after refresh |
| 3 | Grep the local brain cache for the customer, service and symptom keywords; read customers/<id>/worklog.md, company/teams/needs.md and infrastructure/delivery.md for prior occurrences and open commitments | deterministic | no prior-art query is run for the identified customer/service |
| 4 | Build the incident timeline: release notes, MR merge timestamps, deployed image tags in the affected env, and chart/version pins read via `git show <tag>:values.yaml` from a clone | deterministic | any version/pin is sourced from a GitLab file API read, or a deployed tag cannot be resolved for the affected namespace |
| 5 | Reproduce the reported failure against the named environment/namespace (red pipeline locally, HTTP/CORS probe, DB/ACD row counts bucketed per day) | agent | no reproduction attempt produced a captured runtime artifact (command output, HTTP status, log line, DB row count) |
| 6 | Require a runtime observation before any causal claim proceeds | gate | the candidate root cause is supported only by code reading with no traced instance or before/after series |
| 7 | Fan out subagents over the implicated code path (diff of the suspect MR vs main) to explain each observed test case/symptom, with file:line citations | agent | any claimed mechanism lacks a file:line citation or leaves an observed test case unexplained |
| 8 | Adversarially test rival hypotheses (node roll, chart bump, SDK version, unrelated deploy) against the timeline and traffic in the onset window | agent | a rival hypothesis is dismissed without a timestamped evidence line, or two rival hypotheses remain equally supported |
| 9 | Mint an ephemeral service/manager token for the affected account owner and read current tenant/module config plus DB flag state (read-only) | deterministic | token mint fails, or the API read and DB state disagree on the current value |
| 10 | Emit the fix artefacts without sending: exact mutating request body (method, URL, JSON), effective diff, per-fleet ordered rollout steps, and a red-first test | deterministic | the artefact contains an unresolved placeholder, or the request body's target account/module UUID does not match the one read in the previous step |
| 11 | Write/refresh the contract gate script (e.g. bin/fleet-callerid-readiness.py) that exits 1 while any fleet's version/config contract is unmet | deterministic | the gate script exits 0 against a fleet known to be unpatched |
| 12 | Block on approver sign-off for the production/customer-tenant write, presenting the exact body and blast radius | gate | no approval recorded, or the body sent differs byte-for-byte from the body approved |
| 13 | Execute the approved write, then confirm via API GET, DB version/lastUpdated bump, and homer call records for the affected DID | deterministic | any of the three confirmations does not show the new value, or no call record proves the path on the wire |
| 14 | Draft the incident verdict/status post with app.slack.com thread links, the numbers, and the correction footer if a previously posted number changed | deterministic | the draft contains a workspace-host or /p<ts> Slack link, or restates a number that a later measurement contradicted without a correction footer |
| 15 | Block on approver sign-off for any customer- or stakeholder-facing post, and for any post that contradicts a named colleague's stated conclusion | gate | a post to a customer/stakeholder channel is sent without a recorded approval |
| 16 | Post the approved message to the thread, cross-link into the secondary channel, and comment the root cause under the originating card | deterministic | post returns non-2xx, or the read-back of the thread does not show the message |
| 17 | Persist drift, tickets, follow-ups and worklog into the knowledge store, run the store gates, then commit and push | deterministic | status-lean, verify-token or worklog-order gate exits non-zero, or push is rejected |
| 18 | Schedule the follow-up cron re-check (flag persistence, traffic, gate script) for the next morning window | deterministic | no cron entry exists after the run for an investigation left with owed verification |

**Human still decides**: Authorise the mutating write against a live customer tenant, after seeing the exact request body — irreversible, customer-visible (observed: 'show me the body you will send'; tenant callerId fix); Authorise any customer/stakeholder-facing Slack post, especially a verdict that contradicts colleagues' stated conclusions — reputational call; Set release urgency and rollout timing (ship ASAP vs freeze until Monday; mandate human review before production); Grant policy exceptions the machine cannot infer: direct-to-main commits, whether to involve SRE, which org/visibility/bot identity a repo is pushed under; Decide semantics with no machine-derivable answer: 'update to COMPLETED' instead of delete, finished=created for rows with no true completion time, the 8h/24h stakeholder closure convention; Supply outside-the-machine facts that can invalidate the premise (zero calls on the Nimbus DID since 2026-08-14; the team questions the concept, not the impact; Valentin runs ns=latest); Veto destructive housekeeping the run proposes (deleting a cron, removing the stale upstream repo, deleting merged branches)

**Blocked on**: No monitored Slack channel feed today — incident context arrives as a human paste of a permalink or a verbal report, so the trigger itself does not exist yet; No approval channel: the two blocking gates have no mechanism to present a request body and capture a recorded, byte-comparable approval outside an interactive session; GitLab file API truncates values.yaml at ~65kb and returns it silently — the git-clone fallback must be enforced or version reads are wrong without erroring; Runtime verification is not wired for every symptom class: several sessions reached only code-reading diagnoses (callerIdMode, cleanup-job skip) with no traced instance; Ephemeral service-token minting and writer-credential harvest from the backend pod are ad hoc per session; no least-privilege, audited path exists; Retest of a customer-visible fix depends on a third party (Valentin, Oksana, Mira) outside the machine, so 'verified' cannot be reached unattended; Incident scope arrives as informal chatter, not a ticket with a spec — no machine-readable statement of expected vs actual to gate against; The brief/knowledge generators encoded a wrong release-candidate merge model until a human corrected it; process semantics are not asserted anywhere the run can check; GitHub App installation token / bot identity and target org+visibility must be supplied as parameters; no default is safely inferrable; Tooling defects in the routine path (verify-triage.py fence handling, workday flag schema field) break the hydration step and were fixed mid-session

### `harness-eval-gate` - On harness/spec push, run headless arm evals, assert transcripts, gate release

- **evidence**: 11 sessions labelled `agent_harness_tuning`
- **trigger**: push or merge-to-main touching .workflow/ specs, harness/driver crates, or skill/CLI surface in engineering-protocols|metaharness|harness-tools (plus a nightly cron tick to re-run the same matrix against the stored baseline)
- **autonomy**: auto_with_gates
- **removes**: Drops every resume_continue turn ('keep goig', 'continue with it', 'good, implement the next wave'), the bare approve_proceed acks ('1y 2y 3 yes', '5 + 4'), the meta_process turns (//clear, //compact, skill loading), the request_status turns ('whats the overall topic of this session'), and the request_verification turns ('make available under :3000') — the run serves its own artifacts and reports its own state. Keeps only scope, architecture/safety, release and policy decisions.
- **preconditions**: arms matrix file checked in (raw-text, plugin, metaharness, own-harness) with endpoint + model per arm, instead of arms named turn by turn; credentials for the llm gateway (llm.dev.babelforce.com /v1/messages) available to the runner as env, with a positive balance check; fixture inputs and a scratch work dir under ~/.cache (never /tmp) writable by the runner; baseline transcript-metric file committed (skill-loaded, tool-called, max iterations/tokens, TTFT, cache hits, per-step latency, payload sizes); repo scope allowlist committed as a file (e.g. daemonloop excluded), not held only in the operator's head

| # | step | kind | fails if |
|---|---|---|---|
| 1 | Resolve changed paths from the push event and select the affected arms + eval rows from the arms matrix file | deterministic | changed path matches no arm and no row is selected, or a changed repo is absent from the scope allowlist |
| 2 | Precheck the gateway: one cheap headless SDK probe ('say hi', no tools) per arm endpoint, capture the reply | gate | reply empty, or the run terminates on an API error (auth failure, 'Credit balance is too low') before any tool call — abort the whole run as infra, not as a regression |
| 3 | Scaffold one isolated scratch dir per eval row, copy fixture inputs, spawn the headless agent, capture the full NDJSON transcript to disk | deterministic | a row produces no transcript file, zero events, or a non-zero driver exit |
| 4 | Run the transcript assertion DSL over every captured transcript (skill loaded, expected tool called with agnostic tool name, iteration/token ceilings, TTFT, cache hits, per-step latency, tool-call payload size) | gate | any asserted invariant is violated, or a metric regresses past its baseline threshold |
| 5 | Replay the workflow-file context preload and write-scope enforcement checks against each transcript's tool calls | gate | a run wrote outside its declared scope, or a required workflow-file preload is missing from the transcript |
| 6 | Run the repo gate (gate.py + validators: check-verify.py, claim/coverage/date checks) on the working tree | gate | any blocking validator fails; calendar-staleness findings are emitted as advisory rows and do not fail the run |
| 7 | Classify every failing or missing row: driver defect (caching, tool-name blindness, preload/scope), genuine arm regression, or transient infra | agent | a failing row is left unclassified, or a classification cites no transcript event id as evidence |
| 8 | Re-run rows classified transient exactly once, in fresh scratch dirs | deterministic | a row is still missing or failing after the single retry |
| 9 | Write the results table plus baseline diff to the eval results file and open one follow-up story per confirmed driver defect or regression | deterministic | a confirmed defect has no corresponding story id in the results file |
| 10 | Commit results and stories on a scratch branch through the repo gate hook, never on main | deterministic | the commit targets main, or the commit is attempted with --no-verify |
| 11 | Post the eval digest (per-arm pass counts, regressed metrics, story ids) as bot role to the internal dev channel, one line per fact | deterministic | the post call returns no permalink |
| 12 | Halt before any merge of worktrees, CHANGELOG entry, tag, push to a public org, or docs deploy | gate | the run reaches an irreversible publish act without a recorded human authorisation token |

**Human still decides**: Scope authority: which repos/arms are in play and which are off-limits this cycle (the daemonloop exclusion, the metaharness repo split) — until the allowlist file is the source of truth.; Architecture and safety authority on driver changes: harness-agnostic tool declaration, no-bash-by-default, substrate-as-sandbox — approve or reject diffs touching the safety envelope.; Release authority: merge worktrees into main, cut CHANGELOG + tags, push to the public org, deploy the docs site. Irreversible; agent stops and asks.; Policy call the gate cannot make for itself: does calendar-based verification staleness block or stay advisory (default-if-silent = advisory).; Outside-the-machine inputs: GitHub org/account identity and auth for new orgs, peer-session socket addresses, and taste judgements on docs look-and-feel.

**Blocked on**: No committed arms matrix or eval spec: arms and rows were invented mid-session, so a trigger has nothing deterministic to select against.; No red/green threshold on eval quality — the assertion DSL exists but there is no baseline metric file, so 'regression' is currently a human reading a table.; Gateway credentials and deploy access are session-attached; an unattended run has no injected credential and dies on billing exhaustion ('Credit balance is too low') with no infra-vs-regression classification.; gate.py has no pytest wired in, so the gate produces no test signal at all.; check-verify.py fails on calendar drift rather than actor error — the pass criterion is ambiguous, and 19-20 stale claims flip the gate red for no behavioural reason.; Sessions bypass the gate with --no-verify; without a pre-receive or CI-side re-run the gate is advisory, so step 10's fails_if is not currently enforceable.; Commit authority is withheld from agents by standing repo policy, so even a fully green run cannot land its own results without a human turn.; The repo scope boundary (daemonloop excluded, metaharness split out) exists only in the operator's head — no machine-readable allowlist to fail against.; Cross-session peer messaging still depends on human-supplied UDS socket addresses; the /proc/<pid>/cwd scan is a workaround, not a registry.; The agent's mental model of tool declaration was wrong for many turns and only human correction fixed it — no conformance test asserts harness-agnostic tool names, so the same defect can recur silently.

### `design-doc-to-scaffolded-repo` - Scaffold, gate, review, document and publish a new repo from an intake design spec

- **evidence**: 10 sessions labelled `greenfield_scaffold`
- **trigger**: A new design spec file lands in the watched intake directory (designs/inbox/*.md with required frontmatter), or its content hash changes
- **autonomy**: auto_with_gates
- **removes**: Eliminates the approve_proceed and resume_continue filler ('okay, now run it', 'continue', 'implement', 'wonderful, show me the next wave'), the delegate_parallel prompts ('run independent review agent', 'start an independent reviewer'), the ai_policy asks ('anything we need to sort out?', 'review the current impl again'), and the meta_process turns (//compact, //model, //clear, //agents). Bare 'yes/continue' turns are NOT gates and are dropped. Retains only the five authority/taste gates above.
- **preconditions**: gh CLI authenticated with repo-create scope for the target org; git bot identity configured (committer email = users.noreply.github.com address) and scripts/as-bot.sh present; Repo template + AGENTS.md invariant set available and versioned (Rust workspace template, Docusaurus website template, Actions Pages workflow); Credential/endpoint locations declared in a config file (e.g. ~/.flux, .env paths) rather than discovered per session; Project gate command declared per language (Taskfile target, cargo build/test/clippy/fmt, or docusaurus build); Approval artifact channel exists (a signed approval file/queue the run can read for commit/push/visibility decisions)

| # | step | kind | fails if |
|---|---|---|---|
| 1 | Parse intake spec frontmatter: target org, repo name, visibility, language template, docs_site flag, source URLs, invariants | deterministic | Any required frontmatter field is missing, or visibility is not one of private|public |
| 2 | Fetch every referenced external source (OpenAPI spec, design conversation export) and vendor it with pinned sha256 + fetched_at | deterministic | Fetch returns non-200, or the vendored file is written without a recorded hash and timestamp |
| 3 | Create the scratch worktree and instantiate the repo skeleton from the versioned template with org/project/baseUrl substituted | deterministic | Target directory already exists with tracked content, or template substitution leaves unresolved placeholders |
| 4 | Derive modules/crates, README.md, AGENTS.md and initial source files from the design spec and vendored sources | agent | README.md or AGENTS.md missing, or any design-spec requirement has no corresponding file/entry in the requirements register |
| 5 | Run the declared project gate (build + test + clippy + fmt, or site build) until green | gate | Gate command exits non-zero, or reports broken links / base-url errors |
| 6 | Scaffold ./website (Docusaurus) with organizationName/projectName/baseUrl, sidebar, navbar, and the Pages deploy workflow when docs_site=true | deterministic | Local site build fails, or a sidebar entry points at a nonexistent doc |
| 7 | Write docs pages from repo source material and record implementation percentage in README | agent | Site build fails after doc write, or any docs page is unreachable from the sidebar |
| 8 | Spawn an independent read-only review agent over the full diff against AGENTS.md invariants and the design spec; emit findings as structured JSON with file:line evidence | agent | Reviewer returns findings without file:line evidence, or fails to emit valid findings JSON |
| 9 | Apply review findings in source and docs; record each unverifiable finding with an explicit reason | agent | A blocking-severity finding is neither fixed nor annotated with a recorded justification |
| 10 | Re-run the full project gate plus site build after fixes | gate | Gate command exits non-zero |
| 11 | Generate the CHANGELOG entry, compute the owned-path set, and verify no path outside it is dirty | deterministic | git status --porcelain shows modified/untracked paths outside the owned set (another session's work) |
| 12 | Read the approval artifact for visibility, commit/push and release-cut decisions; halt and post the decision request with defaults if absent | gate | No approval artifact for this run id, or it does not cover the requested acts |
| 13 | Stage only owned paths and commit via scripts/as-bot.sh with a conventional message matching repo history | deterministic | Committer email is not the configured noreply bot address, or staged file list differs from the owned-path set |
| 14 | Create the GitHub repo at the approved visibility, push, and (if approved) tag the release | deterministic | gh repo create or git push exits non-zero, or the created repo visibility differs from the approved value |
| 15 | Watch the Pages Actions run to completion and curl every published page URL | gate | Workflow conclusion != success, or any published URL returns HTTP != 200 |
| 16 | Derive the next-wave roadmap and seed backlog stories into docs/stories, then regenerate the status board | agent | Any generated story file fails frontmatter schema validation, or board regeneration exits non-zero |
| 17 | Post the run report: gate counts, review findings applied, published URLs, open decisions with defaults | deterministic | Report exceeds the 20-line operator cap or omits a failed step |

**Human still decides**: Repo visibility and publish destination (private vs public, gh-pages vs none) — irreversible public exposure, not derivable from the design spec; Authorization to commit, push to main and cut a release — repo policy forbids autonomous commits; Semantic/architecture choices the spec does not decide (e.g. absent vs three-valued condition semantics, ES-for-all-persistence, runtime must not know model ids) — presented as options with concrete examples and a stated default; Any destructive act on pre-existing machine state (deleting build caches, stale worktrees) including the count/scope; Spending real money or shared infrastructure (live inference on a shared gateway, GPU pod provisioning, live SIP call)

**Blocked on**: No machine-readable intake spec exists today — design sources arrive as a ChatGPT share URL or a pasted draft, so the trigger has nothing to parse and step 1 cannot run; ChatGPT share links are not reliably fetchable/vendorable; the design conversation cannot be pinned by hash like an OpenAPI spec can; Commit/push authorization is conveyed only as chat text; there is no approval artifact or signed token a run can read, so step 12 has nothing to check; GitHub Pages settings and Actions workflow permissions are repo-level external configuration the scaffold cannot set, so a first publish still needs a manual repo settings visit; No automated quality gate on documentation content beyond build success and HTTP 200 — factual drift in docs passes silently; Reviewer output is free-text prose; no severity schema or machine-checkable finding format exists, so 'blocking finding unresolved' is not currently enforceable; Design-semantics choices had no test or spec to decide them (observed: absent vs three-valued); there is no ADR-with-options mechanism to record the decision and gate on it; Unattended long runs hit context compaction and model/session limits (2 compactions, 1 API error, 5 tool errors observed across sessions) with no checkpoint/resume, so a run can lose the thread mid-scaffold; The repo skeleton is re-derived by the model each session rather than instantiated from a versioned template; steps 3 and 6 assume templates that do not exist yet; External environment facts (credential file locations, target endpoints, test numbers, trunk hostnames) live only in the operator's head; no registry exists for the preconditions to read

### `org-wide-rename-sweep` - Sweep banned identifiers and broken links org-wide, gate, and open PRs

- **evidence**: 9 sessions labelled `refactor_sweep`
- **trigger**: Push webhook on any org repo's default branch, or nightly cron, where scripts/brand-sweep.sh --check reports a banned-identifier hit or check-markdown.py/check-links.py exits non-zero
- **autonomy**: auto_with_gates
- **removes**: Eliminates the continuation nudges ('continue here', 'just keep going', 'keep going', 'sleeping again?'), the bare approvals ('1+2+3+4 -> YES', 'makes sense, do it', 'implement it', 'okay, make it happen'), the status pings ('whats next, anything for me to decide?'), the dirty-tree questions ('what is changed in connectors?'), and the //clear + //model session-management turns. These carried no information the run needs and are not gates.
- **preconditions**: A bot GitHub App installation (b10x-bot) with read/write on every org repo and a token available to the runner, so no personal token is used; A committed, machine-readable rename registry: old->new identifier map plus banned surface strings (e.g. 'daemonloom', 'codewandler', old org name), owned by atlas/scripts/brand-sweep.sh; scripts/check-markdown.py and each component's check-links.py present and exit 0 on the pre-sweep baseline; Per-workspace gate commands declared in Taskfile.yml (test/clippy/fmt/static.sh/release-process.sh/architecture fence) for substrate, zwirn, connectors; Git worktree creation allowed for merge-base baseline reproduction; Path allowlist declaring which trees the sweep may rewrite, and a denylist for secrets, deploy manifests, and external account config

| # | step | kind | fails if |
|---|---|---|---|
| 1 | Enumerate org repos via the bot app API and fetch/refresh a working copy of each default branch | deterministic | any repo in the org listing cannot be cloned or fetched with the bot token, or the token has no read grant |
| 2 | Run brand-sweep.sh --check, check-markdown.py, and per-component check-links.py across every working copy; emit a per-repo/per-file hit inventory as JSON | deterministic | a scanner exits with a non-finding error (missing rename registry, missing checker script, unreadable path) |
| 3 | Classify each hit as mechanical (exact registry match in an allowlisted path) or residual (prose, identifier whose rename changes semantics, path outside allowlist) | deterministic | a hit matches the denylist (secrets, deploy manifests, ~/.config connector files, CI billing/pipeline config) — those are routed to a human gate, not rewritten |
| 4 | Halt and route to the human gate if the run requires an external-account action: org rename, GitHub App creation/transfer, repo visibility change, bot permission grant, secret copy/rotation, or deletion of extracted source | gate | any planned action is outside the repo and needs owner auth in a web UI or production credentials |
| 5 | Apply mechanical rewrites from the rename registry: package names, string literals, remote URLs, registry and config paths, dependency pins | deterministic | a post-rewrite brand-sweep.sh --check still reports a mechanical hit, or the diff touches a file outside the path allowlist |
| 6 | Repair lockfiles and dependency pins after the rename and rebuild the dependency graph | deterministic | lockfile regeneration is non-empty after a second run, or any workspace fails to resolve dependencies |
| 7 | Have an agent resolve the residual hits: prose in *.md and AGENTS.md, dangling markdown links caused by the moves, references that need rewording rather than substitution | agent | check-markdown.py or any check-links.py still exits non-zero, or the agent edited a file not present in the hit inventory |
| 8 | Run every declared gate per workspace: cargo test sweeps, clippy, fmt, static.sh, release-process.sh, architecture fence suite | gate | any declared gate command exits non-zero |
| 9 | For each failing gate, reproduce it in a scratch worktree at the pre-sweep merge-base and label the failure pre-existing or new | deterministic | a failure does not reproduce at merge-base, i.e. the sweep introduced it |
| 10 | Have a review agent check each repo's diff is pure rename/motion: no public API surface change, no behaviour edit outside the registry map | agent | the reviewer finds a changed public signature, a deleted or added symbol, or an edit with no corresponding registry entry |
| 11 | Push one branch per repo and open a PR carrying the diff, the hit inventory, per-file deltas, skipped files, and pre-existing-failure labels | deterministic | the bot cannot push or open a PR, or a commit is authored with an address other than the configured noreply address |
| 12 | Emit the operator report: gate results table, retained-vs-removed inventory, repos skipped and why, and each open decision with the default that will be taken | deterministic | - |

**Human still decides**: Supply or amend the rename registry: which names are banned at the surface, and what each maps to — a branding/taste call with no mechanical criterion (evidence: umbrella repo naming, 'daemonloom must not appear at the surface'); Authorize external-account actions: org rename, GitHub App creation/ownership transfer, bot write grants, repo visibility — owner-only web UI actions; Authorize destructive scope: deleting extracted source from the origin repo, deleting merged branches/worktrees, retiring scripts (dev.sh, probe-inference.sh); Approve production secret copy/rotation and cluster-side changes (vault, grafana, ingress ownership, registry endpoint) before any namespace teardown; Explicit commit/push authorization, and any instruction to land on main instead of a PR branch — required by standing policy

**Blocked on**: No machine-readable rename registry exists today — the old->new map and the banned surface strings lived only in the human's head; the sweep cannot start without it being committed; GitHub org rename, App creation/transfer, bot permission grants and repo visibility require owner auth in a web browser; no API path the bot can take; Production secret copy/rotation (vault, grafana) needs credentials outside the repo plus an irreversible-action approval; No smoke/e2e gate exists to certify a migrated namespace before the old one is torn down; Cluster, registry and DNS facts (push to cluster IP / k8s DNS, not public DNS) are not encoded anywhere the sweep can read; the human corrected this by hand; No maturity or coupling metric in-repo, so extraction/ranking decisions ('which components are solid enough to extract') have no mechanical basis; Per-repo brand checks were removed in favour of one central script, but link checkers are still per-component with inconsistent names and entry points; Pre-existing-failure discrimination needs a full build at merge-base in a scratch worktree; that baseline is not cached or wired into any gate; GitHub Actions billing state blocked a release run mid-sweep; CI spend is external account state the workflow does not observe before pushing; Long runs stalled twice on model usage/rate limits and needed manual restart; there is no checkpoint/auto-resume for a partially applied org-wide sweep

### `backlog-wave-fanout-integrate` - Fan ready backlog stories to isolated implementors, review, gate, integrate

- **evidence**: 7 sessions labelled `multi_agent_fanout`
- **trigger**: Post-merge/cron tick on the repo detects >=2 stories with status=ready and satisfied deps in docs/stories, and no wave branch currently in flight
- **autonomy**: auto_with_gates
- **removes**: Eliminates the pure continuation and housekeeping turns: 'continue', 'resume, follow goal', 'pick up from the last session', '//clear' plus manual re-injection of the prior wave summary, 'commit all, make sure all clean', 'what happens right now', 'i cannot see any bg activity, keep going', and 'whats next, whats clearly missing' - all of which are board/git-state derivable. Keeps only authority turns (publish, spend, roadmap, external facts, confidentiality).
- **preconditions**: Repo uses the track backlog layout (docs/stories/*.md with status+acceptance frontmatter, generated board, roadmap); A single project gate command exists and exits non-zero on failure (unit + browser/e2e smoke); git worktree support and a scratch branch namespace (impl/<ID>) are available locally; gh org token readable at a fixed path (e.g. ~/.cache/claude-tmp/gh-tok) with repo scope on the target org; A declared per-wave token/spend ceiling and model tier policy exist as config, not conversation; AGENTS.md lists safety invariants and the file/repo boundaries each implementor may touch

| # | step | kind | fails if |
|---|---|---|---|
| 1 | Snapshot state across all managed trees: git status, git log --oneline, git diff origin/main, and record HEADs per repo | deterministic | any managed tree has uncommitted changes not created by this run, or a local branch diverged from origin without a recorded reason |
| 2 | Verify credentials: read the org token from its fixed path and call the org API for repo-creation/push permission | gate | token file missing/expired, or org permission field is null/false |
| 3 | Regenerate the status board and select the set of ready, mutually independent stories for this wave (no shared files, no dep edges between them) | deterministic | selected set is empty, or two selected stories declare overlapping owned paths |
| 4 | Check the wave against the declared spend ceiling: stories x model tier x historical per-story token cost | gate | projected spend exceeds the configured wave ceiling |
| 5 | Dispatch one story-impl agent per selected story into its own git worktree on impl/<ID>; each writes a failing-first test, implements, runs the gate to green, commits on its branch only | agent | an agent returns no commit on its branch, or exits without a structured handoff record |
| 6 | Enforce the write boundary: diff each returned branch and assert every changed path is inside that story's declared ownership and inside this repo | deterministic | a diff touches a shared ledger (CHANGELOG/board/roadmap/lockfile), another story's files, or a path outside the repo root |
| 7 | Run the full project gate against each returned branch rebased on current main | gate | gate exit code is non-zero for that branch |
| 8 | Run two independent adversarial story-review agents per non-trivial diff against the story's Acceptance and the AGENTS.md invariants; each returns a verdict with file:line evidence | agent | a reviewer returns a verdict without evidence anchors, or the two reviewers cannot be run independently |
| 9 | Integrate: merge each branch whose gate is green and whose reviewers both pass into the wave branch; bounce the rest back as reopened stories with the reviewer evidence attached | deterministic | a merge conflicts, or an item with a failing reviewer verdict reaches the wave branch |
| 10 | Merge current main into the wave branch and re-run the full gate on the merged result | gate | post-merge gate exit code is non-zero |
| 11 | Update the shared ledgers (CHANGELOG, board, story statuses) and commit the wave on the wave branch, authored with the configured noreply address | deterministic | working tree is not clean after commit, or commit author email is not the configured noreply address |
| 12 | Scan the wave diff for customer-named or confidential material before anything targeted at a public repo | gate | a known-confidential entity name or credential pattern appears in files destined for a public repo |
| 13 | Emit the run report: per-story table (gate result, reviewer verdicts, merged/bounced), remaining ready queue, and the default next action if nobody answers | deterministic | report omits any dispatched story |
| 14 | Hold for push/publish authorization, then merge the wave into main, push, and cut/tag a release if the wave closes an epic | deterministic | local and remote HEADs disagree across the managed repos after push |

**Human still decides**: Authorize the irreversible publish: push to origin/main and cut/tag/publish a release version (observed repeatedly: 'cut a new version and push to gh', release 0.4.0-ess-wave-4, v0.22.0); Approve raising the model tier or spend ceiling above the configured default for a wave (observed: 'use opus for them', $163 spend with no budget gate); Decide roadmap/priority questions the backlog does not encode: wave ordering, whether a new crate/repo is created, product/brand naming, architectural boundaries (e.g. modules must not touch http/sql directly, target repo layout and repo name); Supply out-of-machine facts the agent cannot read: which environment the fix is deployed to, which namespaces exist in the cluster, that a service token exists, that org auth was granted and where the token lives; Confirm the confidentiality scrub for anything published to a public repo (observed: babelforce-named examples found by the human, not the machine)

**Blocked on**: No machine-readable acceptance criteria per story: wave scope was renegotiated conversationally every session, so nothing can decide 'done' without a human reading the diff; No path/repo guardrail on sub-agent writes - implementors wrote into the wrong repo with nothing stopping them; No unattended health gate for deploy-shaped work: 'pods healthy' and 'e2e green against latest.dev' were judged by a human eye, not an exit code; Org and cluster credentials still require human provisioning and re-auth; the grant itself (members_can_create_repositories) was flipped outside the machine; No spend/budget accounting hook - $163 in one archetype with no ceiling enforced before fan-out; No automatic sub-agent state restore after a session crash or quota cutoff; resuming a half-finished wave was a human instruction each time; Unowned uncommitted changes from other sessions/agents in shared trees block a clean pre-wave snapshot and cannot be safely discarded; Product naming, module inclusion/exclusion and architectural boundary rules are not codified anywhere the machine can read, so they resurface as corrections; No recorded golden samples for external-format drift, so a passing gate does not prove the integration still matches reality

### `mr-review-and-gate-runner` - On MR open/update, gate the diff, verify findings, draft review, await approval

- **evidence**: 7 sessions labelled `review_and_gate`
- **trigger**: GitLab/GitHub merge-request webhook: MR opened, or new commits pushed to an open MR's head (plus a nightly cron sweep for MRs whose webhook was missed)
- **autonomy**: auto_with_gates
- **removes**: Eliminates: task initiation by pasting an MR/Slack URL ('review: <mr url>'); 'post review to MR'; 're-review now'; 'store in docs/reviews with timestamp'; bare 'continue' / 'continue, usage fixed' resume turns; 'reload your CLAUDE.md and respond appropriately'; and the 'but unrelated unit-test failures are normal' turn, which is now the merge-base baseline diff. Bare 'yes' / 'ok, proceed' turns that carried no new information are dropped entirely and are not gates.
- **preconditions**: GitLab integration (flux gitlab plugin) authenticated with a bot identity that may read MR metadata/diffs and post notes — never a personal PAT; Repo declares its gate: fmt/lint/test/schema commands and invariants in AGENTS.md or .agents/, machine-readable; Runner can create a throwaway git worktree at an arbitrary SHA, isolated from any dirty working tree another session owns; docs/reviews/ exists (or is creatable) in the target repo for the durable review artifact; Findings store keyed by (project, MR iid, head SHA, finding fingerprint) so re-runs and retractions are idempotent; Slack bot token for the verdict pointer, with the linked-thread URL recorded on the MR or in the store

| # | step | kind | fails if |
|---|---|---|---|
| 1 | Parse webhook payload; extract project, MR iid, head SHA, target branch, draft flag; exit 0 if draft or if head SHA already reviewed | deterministic | payload lacks project/iid/head SHA, or head SHA cannot be resolved in the remote |
| 2 | Fetch MR metadata and full diff via the GitLab integration into a run directory | deterministic | integration call errors, or returned diff is empty while the API reports changed files |
| 3 | Create a throwaway worktree checked out at the MR head SHA and at the merge-base with the target branch | deterministic | checked-out HEAD != requested SHA, or worktree is not clean (`git status --porcelain` non-empty) |
| 4 | Load repo AGENTS.md/CLAUDE.md, invariant register, and the declared gate command list into the run context | deterministic | no gate definition found — no fmt/lint/test/schema commands declared for this repo |
| 5 | Run the declared gate (fmt, lint/clippy, test suite, schema check) at merge-base and at head; store both exit codes and per-test results | deterministic | any gate command is missing or the run times out before producing a result file |
| 6 | Classify each failing test as pre-existing (fails at merge-base too) or introduced (green at merge-base, red at head) | gate | any test is introduced-red at head, or fmt/schema check regresses relative to merge-base |
| 7 | Run codegate scoring over the changed source and markdown; record score deltas vs merge-base | deterministic | codegate exits non-zero or produces no score for the changed paths |
| 8 | Query CI run history for the target branch and the MR pipeline; attach red-run SHAs and job ids to the run record | deterministic | CI history query returns an error (an empty history is a valid result, not a failure) |
| 9 | Run the code-review skill over the diff in a fresh-context sub-agent that is forbidden from reading prior reviews of this MR | agent | sub-agent returns no structured findings object, or its transcript shows it read docs/reviews/ or prior MR notes |
| 10 | Adversarially verify each finding at head SHA — enumerate callers, null guards, cache keys, scope checks — and attach a concrete failure scenario | agent | a finding survives with no file:line evidence or no failure scenario |
| 11 | Bucket findings: verified-from-code / needs-runtime-or-config-access / cut; drop findings whose fingerprint already exists for a prior head SHA and was not re-triggered | deterministic | any finding lands in no bucket, or a fingerprint collides across two different findings |
| 12 | Write docs/reviews/<timestamp>-mr<iid>-<slug>.md with findings, evidence, gate results, pre-existing-failure list, and a default decision line; leave uncommitted | deterministic | file not written, or it omits the gate exit codes / default decision |
| 13 | Emit the review to the operator in verdict-first format with the artifact path and the pending decisions | deterministic | report exceeds the 20-line operator cap or omits the artifact path |
| 14 | Hold before any external write; post per-finding inline notes plus one summary note to the MR only after approval, deduping by fingerprint | deterministic | a note with the same fingerprint already exists on the MR, or the post is attempted without a recorded approval token |
| 15 | Read back posted notes and reconcile against the intended set; retract (delete) any note not in the intended set | gate | read-back note set differs from the intended set after one reconcile pass |
| 16 | Post a short verdict pointer as bot into the linked Slack thread using the app.slack.com thread route, if a thread URL is recorded | deterministic | no linked thread URL recorded (skip, not fail), or the constructed link is not the /thread/<CH>-<parent ts> form |
| 17 | On approval, approve and merge the MR; on a follow-up push, re-enter at step 1 and diff new findings against the prior head's set | deterministic | merge is attempted while the introduced-red gate is failing or without a recorded approval token |

**Human still decides**: Authorize the first external write per MR: publishing review notes to GitLab and the verdict reply into a named Slack channel — non-idempotent, publicly attributed, and observed to have needed retraction twice; Approve and merge: the irreversible accept decision ('approve + merge if LGTY'), including whether verified findings are blocking or advisory; Rule on findings marked needs-runtime-or-config-access (e.g. whether prod customer tokens carry api:settings) — not derivable from the repo; Declare cross-team ownership when a fix falls outside the repo's mandate (chart/version changes owned by SRE) — org boundary and change authority; Supply outside-the-machine state the repos do not encode: release calendar (which env receives which chart version), a test being stale because a backend endpoint changed, an MR already merged out of band

**Blocked on**: No MR webhook is wired today — work items arrived through an unmonitored Slack thread pasted by the human; the Slack-thread-to-MR link is not recorded anywhere machine-readable; Review scope is implicit ('full review'); no fixed per-repo checklist exists, so two runs over the same diff are not comparable; GitLab notes and Slack posts are non-idempotent and there is no fingerprint store, so a re-run duplicates comments and a wrong comment must be deleted by hand; Gate definitions are not declared machine-readably in most target repos (Groovy/Grails and Rust repos differ); the runner must currently guess the fmt/lint/test/schema commands; Sessions review a dirty shared working tree that other agent sessions mutate concurrently — findings are a race-prone snapshot until worktree isolation is mandatory; Security and config claims (token scopes, ehcache TTL propagation, which env is on which chart version) need runtime/prod-config read access the runner does not have; The release calendar and env→chart-version mapping exist only in humans' heads; the agent guessed wrong repeatedly; Approval authority has no token or ACL representation — 'approve + merge' is a chat sentence, not a signed artifact the runner can verify; ~10 QA items per release are inherently human checks with no automated equivalent; the runner can only surface the coverage gap, not close it; No policy encodes fresh-context enforcement — the sub-agent's not-reading-prior-reviews constraint is currently prompt-level, unverifiable after the fact

### `intake-to-groomed-backlog-artifacts` - Decompose intake items into validated epic/story artifacts, sync board, open review PR

- **evidence**: 5 sessions labelled `backlog_grooming`
- **trigger**: Tracker webhook: issue opened/labelled `needs-grooming`, or a new/changed file under `docs/intake/*.md` on the default branch (poll tick as fallback)
- **autonomy**: auto_with_gates
- **removes**: Removes: `//clear` and other context-management meta turns; bare `yes`/`continue`/`go on` acks before a next step; 'was the story pushed to origin/main - is it there?' verification requests (step 13 reports it unprompted); 'clear all unused worktrees now' housekeeping for the run's own worktree; restating id/frontmatter/relation conventions each session. Kept as gates (not removed): the priority-lens choice, the 'which of the 3 to build' decision, the release-pattern judgment call, and the reject/redirect turn that imposed a constraint the agent had not inferred.
- **preconditions**: Repo carries an artifact store with templates and a lifecycle schema (docs/stories/, docs/designs/, artifact frontmatter: id, kind, status, relations); `protocol artifact validate` (or track equivalent) runs non-interactively and exits nonzero on invalid artifacts; `.grooming.yml` exists in-repo and supplies: priority lens (e.g. `ui/ux`), shortlist size, sync/async thresholds, open-question owners, default-if-silent horizon; Board regeneration command exists and rewrites only the generated region; Push rights to the `groom/*` branch namespace and a forge token that can read the intake issue and open a draft PR; Working tree clean at trigger time; git worktree support available

| # | step | kind | fails if |
|---|---|---|---|
| 1 | Fetch the intake payload (issue title/body/labels, or the intake markdown file) into the run directory as JSON | deterministic | payload fetch exits nonzero, or title/body is empty |
| 2 | Create an isolated worktree on branch `groom/<intake-id>` from origin/main | deterministic | branch already exists, base is not fast-forwardable, or worktree add exits nonzero |
| 3 | Load the planning/protocol schema, artifact templates, existing artifact IDs and `.grooming.yml` into a single context bundle | deterministic | schema, template or `.grooming.yml` missing, or ID allocator returns an ID already present in the store |
| 4 | Agent: decompose the intake item into one epic plus N stories, each with a quantified acceptance statement and a `derived_from` relation to the epic, and each unresolved decision recorded as an open question with an owner from `.grooming.yml` and a default-if-silent | agent | no epic emitted, any story lacks `derived_from` or acceptance, any acceptance threshold is unquantified, or any open question lacks owner and default |
| 5 | Render the agent's structured output into artifact files through the repo templates at the allocated IDs, status `draft`, performing no status transitions | deterministic | writer exits nonzero, a file is not created at its allocated ID, or any written frontmatter status differs from the lifecycle-start status |
| 6 | Gate: run `protocol artifact validate` over the store | gate | exit nonzero, or valid-artifact count != number of artifacts written |
| 7 | Verify every code anchor cited in the new artifacts by argv-safe grep of the referenced path/symbol (no shell glob expansion) | gate | a cited file path does not exist, a cited symbol is not found, or the grep invocation errors |
| 8 | Regenerate the status board from story frontmatter | deterministic | command exits nonzero, or the diff touches bytes outside the generated region |
| 9 | Agent: rank all ready stories under the lens and shortlist size from `.grooming.yml`, emitting size, user-visible effect, per-pick evidence, exclusion rationale and a default-if-silent pick | agent | lens value is absent from the frontmatter taxonomy, shortlist length != configured size, or any ranked row lacks size/effect/evidence |
| 10 | Commit artifact-only paths on `groom/<intake-id>`, push the branch, and open a draft PR referencing the intake item | deterministic | commit touches paths outside docs/stories, docs/designs and the board; push or PR creation returns non-2xx |
| 11 | Post the artifact table, ranked shortlist, open questions with owners, and the default-if-silent to the PR and the review channel | deterministic | post returns non-2xx, or read-back of the thread does not find the posted message |
| 12 | Human gate: product owner answers open questions and confirms which shortlisted story is built next | gate | no response and no default-if-silent recorded before the configured horizon |
| 13 | On PR merge, fetch origin and confirm each artifact path is present at origin/main; report SHA and paths | deterministic | any artifact path is absent from the origin/main tree after the merge event |
| 14 | Remove only this run's worktree and local branch after the push is confirmed; leave every other worktree and branch untouched | deterministic | the run worktree has uncommitted changes, the branch is not present on origin, or the cleanup targets a path outside the run worktree |

**Human still decides**: Answer the open questions the decomposition could not resolve (row-count threshold, notification channel, link expiry, column set) — outside-the-machine product information; Pick which shortlisted story is actually built next — commits engineering capacity; Approve merge of the grooming PR to main, and supply any strategic constraint the agent did not infer (e.g. forge-neutral, in-workflow) as a PR review redirect; Authorise any destructive cleanup beyond this run's own worktree/branch (stale worktrees, leftover impl/wave-* branches); Set or change the priority lens and shortlist size in `.grooming.yml` — done out of band, not during the run

**Blocked on**: Story frontmatter has no enforced taxonomy: `ui/ux` and `open` are informal free strings, so the ranking filter and the lens gate cannot be checked mechanically today; No scoring rubric encodes 'user-visible surface gain vs size' — the ranking step is unscored taste and its output cannot be reproduced or diffed run to run; No intake feed exists: every observed session began from a human sentence; there is no `needs-grooming` label convention, no `docs/intake/` directory and no webhook wired; `protocol artifact validate` checks schema and relations only; nothing verifies that acceptance criteria are quantified/testable or that cited code anchors resolve — the anchor gate must be built; Anchor verification is not yet reliable: 3 tool errors from shell globbing on `.rs` grep patterns left an evidence claim unverified; needs argv-safe invocation before it can fail a run; Standing policy blocks commit/push without explicit human instruction; needs a narrow scoped exception for artifact-only paths on `groom/*` branches, otherwise steps 10–13 stall; No forge-neutral, non-interactive adapter for board sync and PR creation across GitHub and GitLab — the `--target` adapter is a story doc (A-500), not shipped code; Open questions have no owner-routing or default-if-silent timer machinery; today they sit in story bodies and nothing escalates or expires them; Destructive cleanup has no safety predicate encoded (uncommitted changes, live process, unpushed branch), so worktree/branch pruning cannot yet run unattended

### `doc-change-to-verified-broadcast` - On doc push, verify claims against repo, draft posts, gate, publish, brief

- **evidence**: 4 sessions labelled `doc_or_report_write`
- **trigger**: push webhook on a tracked docs repo touching *.md under the doc/knowledge paths (or the scheduled knowledge-refresh cron tick), with a `share:` or `status: ready` marker in the changed file's frontmatter
- **autonomy**: auto_with_gates
- **removes**: Eliminates all meta_process turns (`//clear`, model-switch-then-resubmit-identical-prompt), all housekeeping turns ('commit all, push, /refresh' — recurring verbatim across the round), the bare approve_proceed 'yes'/'good'/'correct' acknowledgements, and the request_verification turns that only asked for mechanical re-checks (repo visibility, link clickability, doc-vs-repo fact drift) — those are now gates. Does NOT remove the audience/tagging turn, the 'its public now' external-state turn, the naming turn, or the cross-repo redirect turn.
- **preconditions**: Doc repo is cloned locally and the push ref is fetchable; `gh` authenticated for the target repo; plain `curl` available for unauthenticated visibility probes; `bin/slack-post.py` present and Slack bot token valid for the target channels; Channel/audience policy file exists mapping doc topic -> channels, tag list, bot|user voice (does not exist today; see blockers); Knowledge store repo checked out with `/refresh` ingest sources reachable (Slack, Jira, worklog)

| # | step | kind | fails if |
|---|---|---|---|
| 1 | Resolve changed doc paths and full diff from the push ref (`git diff --name-only <before>..<after>`) | deterministic | no changed path matches the doc glob, or the ref is not fetchable |
| 2 | Load posting-convention context: babelforce + flux-plugin skill config, slack-post.py channel map, permalink-form rules | deterministic | any referenced skill/config file is missing |
| 3 | Extract mechanical repo facts the doc asserts (crate/module existence, module counts, file/stub sizes, script params) into facts.json via git ls-files + wc + parse | deterministic | extraction script exits non-zero |
| 4 | Probe every external link in the doc: `gh repo view --json visibility` plus unauthenticated `curl -o /dev/null -w %{http_code}` | deterministic | any repo-hosted link returns != 200 unauthenticated, or `gh` reports visibility private |
| 5 | Search Slack history for prior threads discussing this doc's topic and emit candidate crosslink targets with parent ts | deterministic | Slack search API call errors; zero hits is a valid empty result, not a failure |
| 6 | Draft the long-form post for the primary channel plus shorter crosslink/thread replies, each claim annotated with its source (file:line or facts.json key) | agent | any drafted claim carries no source annotation |
| 7 | Verify draft against repo state: every annotated claim re-checked against facts.json and the pushed tree; unverifiable claims collected | gate | any claim in the draft contradicts facts.json or has no matching source in the pushed tree |
| 8 | Lint link forms in every draft: require app.slack.com/client/<TEAM>/<CH>/thread/<CH>-<parent ts with dot>; reject /p<ts> and *.slack.com/archives/* | gate | any link uses a rejected host or route form, or a thread link uses a reply ts instead of the parent ts |
| 9 | Present the draft with resolved audience (channels, tag list, voice) for approval | gate | human rejects, or no response before the configured timeout (run halts, nothing is posted) |
| 10 | Post via `bin/slack-post.py` as the policy-resolved role, one call per target thread/channel | deterministic | any post call returns non-zero or no message ts |
| 11 | Read back each post's delivery report and emit a permalink table plus an explicit manual 'to try' item for mention rendering | deterministic | any posted message ts cannot be read back |
| 12 | Commit all dirty doc/knowledge files with conventional messages and push to origin/main | deterministic | commit or push exits non-zero, or `git config user.email` is not the GitHub noreply address |
| 13 | Run the knowledge `/refresh` ingest and reconcile new signals: route unanswered handovers, log pain points, open tasks for unverifiable claims | agent | ingest exits non-zero, or a reconciled signal is written with no evidence pointer |
| 14 | Flag expired `Verify:` markers, breached SLAs and store-growth thresholds; never execute compaction or archive rewrite | deterministic | the run attempts any destructive archive rewrite |
| 15 | Emit the operator brief: needs-you-today items with per-item evidence, permalink table, and a decisions table each carrying the default taken on silence | deterministic | brief exceeds 20 lines, or any decision row lacks a stated default |

**Human still decides**: Audience and voice: which channels, which people to tag by name, bot vs user persona, which channels to exclude — not derivable from the doc; Final approval before the irreversible public post (post shape, link formatting, and that external publication has actually happened); Naming and doctrine calls inside a design doc (component name, invariants like 'brokers but never proxies') — taste with long-lived cost; Approving any destructive archive compaction — no safe rollback exists; Approve/reject on the pending-task queue — business priority ordering

**Blocked on**: No mechanical check for Slack mention rendering: slack.thread returns only fallback text, never the block payload — the '@emir renders as a real mention' check stays a human eyeball step; Audience policy is unencoded: which channels, who to tag, bot vs user voice, and which channels to exclude were human-supplied every time; no policy file exists to resolve them; Publication timing is external: the doc's repo went public by a human action outside the machine, so the visibility probe can only poll, not schedule the run; Slack posts are irreversible — there is no edit/delete path wired into bin/slack-post.py, so a bad post cannot be rolled back by the workflow; No gate can validate an architecture or design doc's correctness; the doc-vs-repo gate only catches factual drift about repo contents, not whether the design is right; External-system facts (whether release 1.284.0 is tagged, whether a customer claim about Groovy `=~` holds) are not readable by the knowledge store and need an out-of-band call; Destructive archive compaction has no rollback or dry-run mode, so it cannot be moved inside the automated path even with a gate; For the design-doc session the spec existed only in the human's head — no ticket, no acceptance criteria, nothing for a trigger to fire on; Cross-repo alignment targets (connectors/specs catalog schema) still carry working, unfixed values, so an automated consistency check would produce false failures

### `session-resume-briefing` - On session start in a known repo, auto-brief where work stopped

- **evidence**: 3 sessions labelled `exploratory_chat`
- **trigger**: SessionStart hook fires for a repo whose path matches a known worktree (or a new-transcript file appears under the session dir)
- **autonomy**: auto_with_gates
- **removes**: Eliminates the resume_continue turn ('continue last session in this dir') and the follow-up orientation questions — the briefing is produced before the human types. Bare 'yes'/'continue' acknowledgements are not gates and are dropped; only the scope/next-action decision remains.
- **preconditions**: repo is a git working tree; repo checkout readable without credentials; AGENTS.md and/or docs/stories exist or are known-absent; a durable per-repo state file path is agreed (e.g. .claude/last-session.json), even if empty on first run

| # | step | kind | fails if |
|---|---|---|---|
| 1 | resolve repo root and branch: git rev-parse --show-toplevel --abbrev-ref HEAD | deterministic | not a git repo, or rev-parse exits non-zero |
| 2 | collect tree state: git status --porcelain=v2 --branch, git log --oneline -20, git stash list, git diff --stat | deterministic | any git command exits non-zero |
| 3 | collect doc/context state: cat AGENTS.md, list docs/stories/*.md frontmatter, ls -t recently modified files (mtime-sorted, top 20) | deterministic | - |
| 4 | read prior state file (.claude/last-session.json): last goal, last step, open story ID, unfinished gate | deterministic | file exists but is not valid JSON |
| 5 | gate: prior state file exists AND its recorded HEAD is an ancestor of current HEAD (state is not stale) | gate | no state file, or recorded HEAD unknown to this repo — emit 'no resumable session, cold start' and stop |
| 6 | agent: reconcile git evidence + docs + prior state into a briefing — what the last session was doing, what is in flight, the single next action, and one explicit completion criterion | agent | briefing omits next action or completion criterion, or cites a file/commit not present in the collected evidence |
| 7 | gate: every factual claim in the briefing resolves to a collected artifact (commit sha, file path, story ID) | gate | any claim has no matching artifact in the step-2/3/4 output |
| 8 | emit briefing to the session (<=20 lines, verdict first) and write updated .claude/last-session.json with current HEAD, goal, next action | deterministic | state file write fails or output exceeds the line cap |
| 9 | gate: stop before any edit — resume executes nothing until the next-action is confirmed | gate | any Edit/Write/commit is attempted in this run |

**Human still decides**: Approve or redirect the proposed next action and its completion criterion — the evidence shows 'continue' had no completion criterion and scope was set by the human, not derivable from the repo.

**Blocked on**: No durable per-session state file today — nothing records what 'last session' was working on; the workflow must create .claude/last-session.json and be written on session end, which does not exist yet.; No session-end hook writing that state, so the first N runs have nothing to resume from.; No completion criterion is derivable from repo state alone — git and AGENTS.md show what changed, not what 'done' means for the in-flight goal.; Uncommitted work in the tree may belong to another agent/session; there is no ownership marker to distinguish 'my last session' from a concurrent one.; Only 3 sessions observed, 2 of which were trivial harness probes ('hi', list agent types) — the resume recipe is grounded in a single session that was interrupted before scope was established.

### `release-cut-gated-pipeline` - Cuts, verifies and publishes a release from a version-bump event with human release gates

- **evidence**: 3 sessions labelled `release_cut`
- **trigger**: Push webhook on main/release-candidate whose diff touches a version field (Cargo.toml, Chart.yaml, chart values, package version) or creation of a release-candidate tag ref
- **autonomy**: auto_with_gates
- **removes**: Session-priming and status-request turns (//knowledge, //refresh, //brief, 'give me a clear list of decisions'), the housekeeping 'commit and push all docs' turn, and all bare continuation turns ('yes', 'keep going', 'disk is fine, keep going') — those carried no information the pipeline cannot compute, so they are not gates.
- **preconditions**: Repo has a path-ownership manifest (CODEOWNERS or owner map) mapping every tracked path to docs / implementation / foreign-team; Release definition-of-done is declared in-repo (in-repo e2e suite + testing/e2e-tests both green, no allow_failure); Cluster/e2e credentials (latest.dev, ns=latest) resolvable from a secret store, not verbally; Per-customer release matrix (line -> last released tag -> target version) exists as a machine-readable file; Bot credentials for Jira issue creation and Slack posting exist, with audience routing (internal bot vs customer-facing) configured

| # | step | kind | fails if |
|---|---|---|---|
| 1 | Snapshot the tree: git status --porcelain, git stash list, git diff --name-only; classify every changed path against the ownership manifest | deterministic | any changed path has no owner rule, or a foreign-owner path is dirty |
| 2 | Stage only the paths whose owner rule matches this release's scope (explicit git add of listed paths, never -A) | deterministic | staged set differs from the computed allowlist |
| 3 | Materialise HEAD+staged in a scratch worktree and run the build there | gate | scratch-worktree build fails, or a staged doc/config references a crate, chart or path absent from the committed tree |
| 4 | Run the cross-document consistency check: status.md trace rows, VISION.md, AGENTS.md, README and CHANGELOG against git tags, merge-base and the version being cut | gate | any document states a status, version or tag that contradicts git ground truth |
| 5 | Verify release pin integrity: declared version, pinned commit SHA and version description match the published authority; run as a PR-gate job, not inside --self-test | gate | pinned SHA is stale, or version description does not match the version being cut |
| 6 | Poll the upstream registry (crates.io / chart repo) for every dependency version this release requires, with a bounded timeout | deterministic | a required upstream version is not published when the timeout expires |
| 7 | Fetch e2e credentials from the secret store and run both the in-repo e2e suite and testing/e2e-tests, N consecutive runs, no allow_failure | gate | any run is red, or results differ across runs (flake detected) |
| 8 | On a red or flaky e2e result, diagnose the failure and produce a runtime observation (trace of one instance or before/after series), then have an independent reviewer try to refute the diagnosis | agent | diagnosis carries no runtime observation, or the adversarial reviewer refutes it |
| 9 | Generate per-customer-line compare links between the last released tag and the current head, and emit the proposed hotfix/branch matrix with names derived from the release matrix file | deterministic | a customer line in the matrix has no released baseline tag or no reachable compare range |
| 10 | Check every intended write target (branches, tags, MRs, chart repos) against the ownership policy and refuse targets owned by another team | gate | a target path or repo resolves to a foreign owner (e.g. SRE-owned prod helm config) |
| 11 | Write the commit/tag message to a file (heredoc, never -m with backticks) recording what was deliberately excluded and why | deterministic | message file is title-only, or the excluded-paths section does not list every path the classifier withheld |
| 12 | Create branches, tag the release and open MRs against release-candidate for each approved line | deterministic | a tag already exists, a branch name collides, or MR creation returns non-2xx |
| 13 | Open Jira issues for every residual item detected by the gates (flakes, stale pins, disabled deploy jobs) and link them to the release tag | deterministic | an issue is created without a link back to the release tag or the failing gate's job URL |
| 14 | Write briefings/topics/<line>/<date>.md with the compare ranges, gate results and data-retrieval notes | deterministic | - |
| 15 | Draft the release status post: verdict line, table of gates with numbers, Jira refs as full clickable URLs, Slack links in app.slack.com thread form | agent | post contains a prose paragraph, a bare ticket key without URL, or a *.slack.com/archives or /p<ts> link form |
| 16 | Post the drafted status to the internal release channel as bot; hold the customer-facing variant in a queue until approved | deterministic | post API returns non-2xx, or a customer-facing channel is targeted without an approval record |

**Human still decides**: Authorise the irreversible acts: push/merge to shared main and creation of the release tag — the machine prepares, a human releases; Approve the per-customer hotfix matrix: which lines get a hotfix, branch naming, and any line whose version differs from the default (e.g. spiegel's ACD version) — business priority; Approve wording and audience for customer- or stakeholder-facing posts; internal bot posts go without a gate; Ratify any action that contradicts a recorded prior decision (e.g. overriding an X-157-style 'do not move this check' note) before it is executed; Rule on an architecture or storage-model question the gates surface as underspecified (e.g. metadata in DB vs secret path layout) before implementation continues

**Blocked on**: No machine-readable path-ownership manifest exists; splitting docs from a peer's in-flight files in a dirty shared tree was pure judgment in session 1; No cross-document consistency checker is wired into CI — status.md/VISION.md/AGENTS.md drift was caught by a human reading, not a gate; e2e suite has a concurrency race and no reliable green signal; an N-run threshold is a heuristic standing in for a real gate; Cluster credentials for latest.dev (ns=latest) are not discoverable in-repo; they were handed over verbally at turn 15; Cross-team ownership (SRE owns prod helm-config MRs) is unwritten policy — there is no file for step 10 to check against; Upstream dependency publication (flux-connectors on crates.io) is an external, unschedulable system; needs an agreed timeout and fallback behaviour; GitHub Pages is not enabled and the deploy job fails red; enabling it needs repo-admin credentials outside any session; The customer-line matrix (lyse / spiegel / ACD 1.281-1.283) exists only in human memory; nothing machine-readable to drive step 9; Cross-repo decision artifacts (decision 0022, C-534 epic, X-157 note) have no access path from the release repo, so step 4 cannot check against them; No configured bot identity plus audience-routing policy for Jira and Slack, so steps 13 and 16 currently need a human to send

## 10. Method and caveats

- Corpus frozen in `data/manifest.json`; the live session running the analysis is excluded.
- 14 of 209,928 transcript records failed to parse (truncated writes) and were skipped.
- Costs are **API list-price equivalents** computed from `usage` blocks, not billed spend (these sessions ran on a subscription). One API response is written to the transcript as several records carrying identical `usage`; each response is billed once, by message id.
- Cache pricing: read 0.1x input, 5-minute write 1.25x, 1-hour write 2x.
- Turn and session labels come from an LLM classifier over a closed taxonomy (`scripts/taxonomy.py`); they are judgements, not measurements. Motifs, counts, latencies and costs are measurements.
- `replaceable_by` is the classifier's opinion about a single turn in context. It does not know what an automated replacement would have cost or broken.

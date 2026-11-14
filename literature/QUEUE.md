# Queue

State of every candidate paper. Line format and marks are defined in `SCHEMA.md`.

## Search log

- Run 1, 2026-11-13: the 23 queries in `queries.txt`, 40 newest hits per query, 628 unique papers,
  published 2022-01-17 to 2026-11-12.
- 100 of the 628 are queued below. They were selected by title; the abstracts were not read.
- The other 528 were not selected. They are not listed and were not judged as skipped.
- The queries sort newest first, so 323 of the 628 hits are from 2026-10 and 2026-11. Older work is
  under-represented in this run.
- 4 more papers are queued from the leads of papers read, each marked `lead from <id>`. Their titles
  and dates come from the citing paper's reference list, not from arXiv.
- 2026-11-14: 12 papers read, the newest queued paper of each of the 12 topics. 49 of their leads
  are queued with `add_leads.py`, titles and dates from the arXiv API. Leads that only define a
  benchmark were left out.
- 2026-11-14, second batch: 12 more papers read, again the newest queued paper of each of the 12
  topics. 29 of their leads are queued with `add_leads.py`.
- 2026-11-14, third batch: 13 more papers read, the newest queued paper of each of the 12 topics
  and a second controlled trial (2302.06590). 40 of their leads are queued with `add_leads.py`;
  6 more were queued already.
- 2026-11-14, fourth batch: 12 more papers read, the newest queued paper of each of the 12 topics.
  31 of their leads are queued with `add_leads.py`; 6 more were in this file already.
- 2026-11-14, fifth batch: 12 more papers read, the newest queued paper of each of the 12 topics.
  43 of their leads are queued with `add_leads.py`; 11 more were in this file already.
- 2026-11-14, sixth batch: 12 more papers read, the newest queued paper of each of the 12 topics.
  35 of their leads are queued with `add_leads.py`; 10 more were in this file already.
- 2026-11-14, seventh batch: 12 more papers read, the newest queued paper of each of the 12 topics.
  29 of their leads are queued with `add_leads.py`; 20 more were in this file already.
  4 of the 12 score no coding task (2605.23904, 2609.20625, 2610.00372, 2610.29823).
- 2026-11-14, trial search: the topic "controlled trials with developers" had no queued paper
  left. 10 queries were added to `queries.txt` and run with `--max 40`: 49 unique hits, 5 in this
  file already. A reader (claude-fable-5-2) chose 16 of the other 44 from title and abstract: 5
  under controlled trials, 11 under 7 other topics. `add_leads.py` sorted each topic by a wrong
  field until this run; fixed, so the next run reorders the topics newest first.
- 2026-11-14, eighth batch: 12 more papers read, the newest queued paper of each of the 11 topics
  that had one, and a second paper under instruction files (2610.29870). 25 of their leads are
  queued with `add_leads.py`; 20 more were in this file already. 2 of the 12 score no coding
  task (2608.19013, 2608.22960).
- 2026-11-14, ninth batch: 12 more papers read, the newest queued paper of each of the 12 topics. 25
  of their leads are queued with `add_leads.py`; 9 more were in this file already. 2 of the 12 score
  no coding task (2608.12307, 2610.27301).

## Read

- [x] 2611.16289 · 2026-11-12 · Eliciting and Mitigating Specification Satisficing in Coding Agents · read 2026-11-14
- [x] 2611.13709 · 2026-11-10 · Do They Do as They Are Told? Investigating Coding Agents' Adherence to Explicit Instructions in Context Files · read 2026-11-14
- [x] 2611.13241 · 2026-11-09 · FlowPlan: Reducing the Token Cost of Coding Agents with Abstraction-Guided Planning and Verification · read 2026-11-14
- [x] 2611.10058 · 2026-11-06 · From Delegation to Action Approval: An Exploratory Study of Developers' Practices in Collaborating with AI Coding Agents · read 2026-11-14
- [x] 2611.09802 · 2026-11-06 · When Instruction Files Go Stale: Documentation Debt and Hidden Cost in Coding Agents · read 2026-11-14
- [x] 2611.07286 · 2026-11-05 · How Should Agents See Code? Rethinking Code Representations for Agentic Software Engineering · read 2026-11-14
- [x] 2611.07166 · 2026-11-04 · Multi-step SWE: Can Coding Agents Keep Building on Their Own Code Over Long Horizons? · read 2026-11-14
- [x] 2611.06946 · 2026-11-03 · Beyond the Agent Harness: Boundary Criteria for Software-Factory Orchestration - A Single-Operator Case Study · read 2026-11-14
- [x] 2611.05094 · 2026-11-03 · A Gated Spec-Driven Workflow: An Audit-Trail Study of Coding-Agent Work · read 2026-11-14
- [x] 2611.04466 · 2026-11-03 · From Watching to Steering: Enabling Human-Coding Agent Collaboration through Execution Traces · read 2026-11-14
- [x] 2611.04367 · 2026-11-03 · Do Coding Agents Follow AGENTS.md? The Effect of Policy Wording on Instruction Compliance · read 2026-11-14
- [x] 2611.03219 · 2026-11-02 · Can Coding Agents Sustain Continual Evolution without Forgetting? · read 2026-11-14
- [x] 2611.02383 · 2026-11-02 · Toward an Evidence-Based Template for Agent Instruction Files: An Empirical Study of Adoption, Consistency, and Maintenance · read 2026-11-14
- [x] 2611.02017 · 2026-11-01 · Switch-SWE: Do Coding Agents Hold Focus When Switching Between Unfinished Tasks? · read 2026-11-14
- [x] 2611.02207 · 2026-11-01 · Built on Broken Assumptions (BOBA): Why Coding Agents Cannot Be Left Alone · read 2026-11-14
- [x] 2611.01181 · 2026-10-31 · Do Coding Agents Catch Their Own Bugs? (They Don't.) · read 2026-11-14
- [x] 2611.00689 · 2026-10-31 · Getting a Grip: Operating Human-Agent Software Teams Through Governed Messages · read 2026-11-14
- [x] 2611.00314 · 2026-10-30 · Decentralized Multi-Agent Coordination and Communication in Shared Codebases · read 2026-11-14
- [x] 2610.41433 · 2026-10-30 · What Does a Repair Agent Gain from Remembering Its Failure? An Exploratory Study on Real Python Bugs · read 2026-11-14
- [x] 2610.38214 · 2026-10-28 · Skeleton Coding: Program Structure as a Specification for Agents · read 2026-11-14
- [x] 2610.38244 · 2026-10-28 · Precedent or Intent? What Coding Agents Follow When Evolving Existing Code · read 2026-11-14
- [x] 2610.35348 · 2026-10-26 · Toward Evidence-Based Agentic Software Engineering · read 2026-11-14
- [x] 2610.36188 · 2026-10-26 · Skill Dreaming: Evolving Repository Skills through Pull Request Streams · read 2026-11-14
- [x] 2610.35297 · 2026-10-26 · Testing with Coding Agents: A Large-Scale Comparison of Agent-Supported and Human-Authored Pull Requests · read 2026-11-14
- [x] 2610.36254 · 2026-10-26 · Instant Software Factories · read 2026-11-14
- [x] 2610.35971 · 2026-10-26 · Continue or Restart? The Limits of Early Failure Prediction in Coding Agents · read 2026-11-14
- [x] 2610.35992 · 2026-10-26 · Before the First Edit? Measuring When Coding-Agent Guidance Actually Arrives · read 2026-11-14
- [x] 2610.32578 · 2026-10-23 · Lessons Outlive Their Failures: A Case Study of Rules for AI Coding Agents · read 2026-11-14
- [x] 2610.31715 · 2026-10-22 · What Open-Source Projects Tell Their Coding Agents: A Census of AGENTS.md and CLAUDE.md · read 2026-11-14
- [x] 2610.30571 · 2026-10-22 · Stale Instruction Files Override the Code in Coding Agents: A One-Sentence Fix · read 2026-11-14
- [x] 2610.29869 · 2026-10-21 · Compaction Laundering: Provenance Destruction in Context-Compacting Coding Agents · read 2026-11-14
- [x] 2610.29823 · 2026-10-21 · MemoryTax: The Bitter Lesson of Agent Memory · read 2026-11-14
- [x] 2610.29870 · 2026-10-21 · PAUSE: Search-Free Steering of Coding Agents Before Their First Source-Code Edit · read 2026-11-14
- [x] 2610.27524 · 2026-10-20 · MemDev-Bench: Does Memory Help Code Agents?Benchmarking Memory Systems over Real Repository Histories · read 2026-11-14
- [x] 2610.28683 · 2026-10-19 · Who Approved This? Coding Agents, Human Accounts, and Merge-Gate Evidence at a Fintech Startup · read 2026-11-14
- [x] 2610.27381 · 2026-10-19 · Documentation Drift in AI-Generated Pull Requests · read 2026-11-14
- [x] 2610.27301 · 2026-10-19 · Evaluating Context Compaction on the Questions That Come Later · read 2026-11-14
- [x] 2610.23782 · 2026-10-16 · Enforcing Code Reasoning in Agentic Scaffold for More Effective Issue Resolution · read 2026-11-14
- [x] 2610.22791 · 2026-10-16 · Self-Evolving Coding Agents via Harness-Policy Optimization · read 2026-11-14
- [x] 2610.15708 · 2026-10-11 · SpecForge: Recursive Self-Improvement for Coding Agents via Behavioral Specifications · read 2026-11-14
- [x] 2610.13668 · 2026-10-09 · (When) Should a Software Factory be Lights-off? Benchmarking Code Review Agents on Bug Detection · read 2026-11-14
- [x] 2610.14224 · 2026-10-09 · Harness^2: Recursive Agent Harnessing for an Open World · read 2026-11-14
- [x] 2610.11647 · 2026-10-08 · One Skill Too Many: How Co-Installed Skills Conflict in Coding Agents · read 2026-11-14
- [x] 2610.11179 · 2026-10-08 · Who Pays the Review Cost? Triage, Fairness, and Accountability in AI-authored Pull Requests · read 2026-11-14
- [x] 2610.09995 · 2026-10-07 · Designing Collaborative AI-Driven Workflows for Scientific Software Engineering · read 2026-11-14
- [x] 2610.10263 · 2026-10-07 · When Sub-Agents Work in Parallel: The Promises and Pitfalls of Dynamic Concurrency in Long-Horizon Coding Tasks · read 2026-11-14
- [x] 2610.07832 · 2026-10-06 · Harness Engineering for Software Engineering via Modular Executable Dev-Primitives · read 2026-11-14
- [x] 2610.08651 · 2026-10-06 · A Case Study in Assuring AI-Written Software · read 2026-11-14
- [x] 2610.06406 · 2026-10-05 · What Did the Agent Actually Do? Evidence-Grounded Oversight for Long-Horizon Agents · read 2026-11-14
- [x] 2610.07261 · 2026-10-05 · Verifying Coordination in Parallel Coding Agents: NP-Bench and a Scheduling Planner · read 2026-11-14
- [x] 2610.04832 · 2026-10-04 · Agent Skill Evolution: How Revisions Affect Coding Agents · read 2026-11-14
- [x] 2610.04375 · 2026-10-03 · Do Tool Calls Execute as Intended? Measuring and Repairing Intent-Execution Correspondence in LLM Agents · read 2026-11-14
- [x] 2610.04779 · 2026-10-03 · Asymmetric Repository Lineage Modeling and Verifier-Guided Coordination in Concurrent AI Coding Agents · read 2026-11-14
- [x] 2609.40303 · 2026-09-30 · How Much of a Harness Does a Strong Agent Need for Autonomous ML Engineering? · read 2026-11-14
- [x] 2609.39957 · 2026-09-30 · Learning When and How to Intervene: A Hindsight-Distilled Sentinel for Coding Agents · read 2026-11-14
- [x] 2610.00372 · 2026-09-30 · When Harnesses Lose the Signal: Causal Evaluation of Recovery in LLM Agents · read 2026-11-14
- [x] 2609.37985 · 2026-09-29 · Merged, Not Measured: An Empirical Study of Performance Issues Fixed by Coding Agents · read 2026-11-14
- [x] 2609.36323 · 2026-09-28 · Towards an AI Software Factory for Data Systems · read 2026-11-14
- [x] 2609.35381 · 2026-09-28 · MCP Error Messages Written for Developers Hurt the Most Capable Agents Most · read 2026-11-14
- [x] 2609.32459 · 2026-09-26 · Beyond the Model: Demystifying Harness Effects in Software Engineering Agents · read 2026-11-14
- [x] 2609.26847 · 2026-09-22 · Who Finishes the Job? A Study of Follow-Up Fixes and Commit Authorship on AI Coding Agent Pull Requests · read 2026-11-14
- [x] 2609.26781 · 2026-09-22 · Agensh: Scaling Organizational Intelligence to 1,024 Agents · read 2026-11-14
- [x] 2609.24234 · 2026-09-21 · The Work Behind Delegation: A Framework for Supervising AI Coding Agents · read 2026-11-14
- [x] 2609.20812 · 2026-09-17 · Quantifying Overclaiming Propensity in Frontier LLM Agents · read 2026-11-14
- [x] 2609.20625 · 2026-09-17 · Chronicle: Cut-Point Replay for Regression Testing of LLM Agents · read 2026-11-14
- [x] 2609.20804 · 2026-09-17 · An Empirical Study of Harness Design for Coding Agents · read 2026-11-14
- [x] 2609.15877 · 2026-09-14 · Using Agentic AI for contextualized and multifaceted code review at Ericsson · read 2026-11-14
- [x] 2609.17598 · 2026-09-12 · Not All Agents Are Equal: Code Quality and Post-Merge Maintenance Across Five Autonomous Coding Agents in the Wild · read 2026-11-13
- [x] 2609.12742 · 2026-09-11 · Skill Issue: Lessons from Optimizing Repository SKILLs for Coding Agents · read 2026-11-14
- [x] 2609.09671 · 2026-09-09 · Introducing Consort: A Spec-First Agent Framework for Enforced, Test-Driven Development on Live Database Branches · read 2026-11-14
- [x] 2609.08371 · 2026-09-08 · Authority Is Not a String: A Capability-Scoped Harness for Prompt-Injection-Resistant Coding Agents · read 2026-11-14
- [x] 2609.07542 · 2026-09-07 · "We Permit the Use of AI, but [...]": The Landscape of AI Policies in Popular Open Source Projects · read 2026-11-14
- [x] 2609.07919 · 2026-09-07 · You can contribute if you... An Empirical Framework of AI Contribution Policies in OSS · read 2026-11-14
- [x] 2609.06213 · 2026-09-05 · Beyond Lexical Metrics: Sentence-Embedding Detection of Reviewer Habituation in AI Code Review · read 2026-11-14
- [x] 2609.05364 · 2026-09-04 · Design Docs Are All You Need: An AI-native Machine-Learning Performance Tool · read 2026-11-14
- [x] 2609.04167 · 2026-09-03 · SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents · read 2026-11-14
- [x] 2609.01985 · 2026-09-02 · When Agents Implement Systems: A Case Study in Defects, Detection, and Evaluation Rigor · read 2026-11-14
- [x] 2609.03028 · 2026-09-02 · Requirements After the First Edit: Mining Late Requirement Emergence and Rework in Real-World Coding-Agent Sessions · read 2026-11-14
- [x] 2609.00252 · 2026-08-31 · Spec-Driven Development for Agentic Software Engineering: Harnessing Human-Agent Teamwork · read 2026-11-14
- [x] 2608.30572 · 2026-08-31 · Practical Implementation Report on Introducing Spec-Driven Development Using AI Agents in Software Development PBL · read 2026-11-14
- [x] 2608.25202 · 2026-08-25 · Spec-Driven Development as Prescribed and as Practiced · read 2026-11-14
- [x] 2608.23067 · 2026-08-24 · Signal or Noise? A Benchmark Study of Agent Skills in Web Development · read 2026-11-14
- [x] 2608.22960 · 2026-08-24 · What Process Evaluation of Coding Agents Actually Measures: Action, Task, and Step Are Three Different Levels · read 2026-11-14
- [x] 2608.21311 · 2026-08-21 · AI-to-AI Code Reviews of GitHub Pull Requests · read 2026-11-14
- [x] 2608.19013 · 2026-08-19 · Harness Continual Learning: Continual Adaptation Beyond Model Parameters · read 2026-11-14
- [x] 2608.18167 · 2026-08-16 · Adversarial Review: Structured Disagreement for Grounded Agentic Code Review · read 2026-11-14
- [x] 2608.14036 · 2026-08-14 · Demystifying Agent Skills: Why They Work-Until They Don't · read 2026-11-14
- [x] 2608.12307 · 2026-08-12 · AI4AI at Test-Time: Strong-to-Weak Capability Transfer via Harnesses · read 2026-11-14
- [x] 2608.09290 · 2026-08-10 · OpenCodeReview: Determinism over Non-Determinism for Cost-Effective Agent-Based Code Review · read 2026-11-14
- [x] 2608.08453 · 2026-08-09 · What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files · read 2026-11-14
- [x] 2608.08950 · 2026-08-09 · Independent Patch Verification for Coding Agents with a Bidirectional Reconstruct-and-Verify Framework · read 2026-11-14
- [x] 2607.26375 · 2026-07-29 · (Im)Paired Programming: Coding Agents Improve Productivity but Harm Understanding · read 2026-11-14
- [x] 2607.21832 · 2026-07-23 · How Do AI Coding Agents Contribute to Software Development? an Empirical Study of Agentic Pull Requests · read 2026-11-14
- [x] 2607.21656 · 2026-07-22 · Cross-Model LLM Code Review: Should you use Claude to review Codex or vice versa? · read 2026-11-14
- [x] 2607.13196 · 2026-07-14 · From Human-Centric to Agentic Code Review: The Impact of Different Generations of Generative AI Technology on Review Quality · read 2026-11-14
- [x] 2607.13156 · 2026-07-14 · Design-System-Aware Development with AI: Evaluating Productivity and Design Consistency · read 2026-11-14
- [x] 2607.13091 · 2026-07-13 · Self-Improving AI Coding Agents Through Accumulated Behavioral Rules: A Closed-Loop Framework · read 2026-11-14
- [x] 2607.07980 · 2026-07-08 · 3100 Opinions on Code Review in an AI World: Building Causal Theory from Practitioner Discourse · read 2026-11-14
- [x] 2607.00911 · 2026-07-01 · From Registry to Repository: How AI Agent Skills Are Written, Adapted, and Maintained · read 2026-11-14
- [x] 2606.14249 · 2026-06-12 · HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry · read 2026-11-14
- [x] 2606.09498 · 2026-06-08 · Self-Harness: Harnesses That Improve Themselves · read 2026-11-14
- [x] 2605.23904 · 2026-05-22 · SkillOpt: Executive Strategy for Self-Evolving Agent Skills · read 2026-11-14
- [x] 2605.24050 · 2026-05-21 · More Skills, Worse Agents? Skill Shadowing Degrades Performance When Expanding Skill Libraries · read 2026-11-14
- [x] 2604.09388 · 2026-04-10 · The AI Codebase Maturity Model: From Assisted Coding to Fully Autonomous Systems · read 2026-11-13
- [x] 2602.11988 · 2026-02-12 · Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? · read 2026-11-13
- [x] 2507.09089 · 2025-07-12 · Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity · read 2026-11-13
- [x] 2410.18334 · 2024-10-24 · Dear Diary: A randomized controlled trial of Generative AI coding tools in the workplace · read 2026-11-14
- [x] 2410.12944 · 2024-10-16 · How much does AI impact development speed? An enterprise-based randomized controlled trial · read 2026-11-14
- [x] 2406.17910 · 2024-06-25 · Transforming Software Development: Evaluating the Efficiency and Challenges of GitHub Copilot in Real-World Projects · read 2026-11-14
- [x] 2402.05636 · 2024-02-08 · The Impact of AI Tool on Engineering at ANZ Bank An Empirical Study on GitHub Copilot within Corporate Environment · read 2026-11-14
- [x] 2304.10778 · 2023-04-21 · Evaluating the Code Quality of AI-Assisted Code Generation Tools: An Empirical Study on GitHub Copilot, Amazon CodeWhisperer, and ChatGPT · read 2026-11-14
- [x] 2302.06590 · 2023-02 · The Impact of AI on Developer Productivity: Evidence from GitHub Copilot · read 2026-11-14
- [x] 2208.09727 · 2022-08-20 · Lost at C: A User Study on the Security Implications of Large Language Model Code Assistants · read 2026-11-14

## Skipped

None yet.

## Queued

### controlled trials with developers

- [ ] 2607.08885 · 2026-07-09 · Programmers Are Poor and Overconfident Judges of LLM-Generated Assertions · lead from the trial search of 2026-11-14
- [ ] 2605.07320 · 2026-05-08 · Splitting User Stories Into Tasks with AI -- A Foe or an Ally? · lead from the trial search of 2026-11-14
- [ ] 2507.15822 · 2025-07-21 · Do AI models help produce verified bug fixes? · lead from the trial search of 2026-11-14
- [ ] 2507.00788 · 2025-07-01 · Echoes of AI: Investigating the Downstream Effects of AI Assistants on Software Maintainability · lead from the trial search of 2026-11-14

### field data from real repositories

- [ ] 2607.04003 · 2026-07-04 · "AI Slop is DDoSing Open Source": Understanding the Impact of AI-Generated Contributions on Open Source Sustainability · lead from 2610.11179
- [ ] 2607.01904 · 2026-07-02 · AI Writes Faster Than Humans Can Review: A Longitudinal Study of an Enterprise 2x Mandate · lead from the trial search of 2026-11-14
- [ ] 2606.26289 · 2026-06-24 · Augmentation with Dilution? A Large-Scale Empirical Study of Human Contributor Ecosystems After AI Coding Agent Adoption · lead from 2609.03028
- [ ] 2606.21804 · 2026-06-19 · Is Agent Code Less Maintainable Than Human Code? · lead from 2611.01181
- [ ] 2606.07448 · 2026-06-05 · Agentic Very Much! Adoption of Coding Agent in New GitHub Projects · lead from 2609.07542
- [ ] 2605.29442 · 2026-05-28 · How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions · lead from 2609.09671
- [ ] 2605.18461 · 2026-05-18 · One Developer Is All You Need: A Case Study of an AI-Augmented One-Person Squad in a Brownfield Enterprise
- [ ] 2605.08017 · 2026-05-08 · Collaborator or Assistant? How AI Coding Agents Partition Work Across Pull Request Lifecycles · lead from 2610.28683
- [ ] 2605.06464 · 2026-05-07 · To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study · lead from 2610.35297
- [ ] 2604.16754 · 2026-04-17 · AI Slop and the Software Commons · lead from 2610.11179
- [ ] 2604.09805 · 2026-04-10 · Building an Internal Coding Agent at Zup: Lessons and Open Questions
- [ ] 2604.04059 · 2026-04-05 · Humans Integrate, Agents Fix: How Agent-Authored Pull Requests Are Referenced in Practice
- [ ] 2604.00917 · 2026-04-01 · Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time
- [ ] 2604.00436 · 2026-04-01 · Programming by Chat: A Large-Scale Behavioral Analysis of 11,579 Real-World AI-Assisted IDE Sessions · lead from 2609.03028
- [ ] 2603.28592 · 2026-03-30 · Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild · lead from 2609.26847
- [ ] 2603.20847 · 2026-03-21 · Engineering Pitfalls in AI Coding Tools: An Empirical Study of Bugs in Claude Code, Codex, and Gemini CLI · lead from 2609.07919
- [ ] 2602.17084 · 2026-02-19 · How AI Coding Agents Communicate: A Study of Pull Request Description Characteristics and Human Review Responses · lead from 2609.26847
- [ ] 2602.09185 · 2026-02 · AIDev: Studying autonomous coding agents in the wild · lead from 2609.17598
- [ ] 2602.04226 · 2026-02-04 · Why Agentic-PRs Get Rejected: A Comparative Study of Coding Agents · lead from 2607.07980
- [ ] 2602.00164 · 2026-01-29 · Why Are AI Agent Involved Pull Requests (Fix-Related) Remain Unmerged? An Empirical Study · lead from 2609.26847
- [ ] 2601.20109 · 2026-01-27 · Beyond Bug Fixes: An Empirical Investigation of Post-Merge Code Quality Issues in Agent-Generated Pull Requests · lead from 2609.37985
- [ ] 2601.18341 · 2026-01-26 · Agentic Much? Adoption of Coding Agents on GitHub · lead from 2609.07542
- [ ] 2601.16809 · 2026-01-23 · Will It Survive? Deciphering the Fate of AI Agent-Authored Code in Open Source · lead from 2609.26847
- [ ] 2601.15195 · 2026-01-21 · Where Do AI Coding Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub · lead from 2610.35297
- [ ] 2601.02200 · 2026-01-05 · Code for Machines, Not Just Humans: Quantifying AI-Friendliness with Code Health Metrics
- [ ] 2601.00477 · 2026-01-01 · Security in the Age of AI Teammates: An Empirical Study of Agentic Pull Requests on GitHub · lead from 2610.27381
- [ ] 2512.10493 · 2025-12-11 · Decoding Human-LLM Collaboration in Coding: An Empirical Study of Multi-Turn Conversations in the Wild · lead from 2609.03028
- [ ] 2512.05314 · 2025-12-04 · WhatsCode: Large-Scale GenAI Deployment for Developer Efficiency at WhatsApp · lead from 2610.28683
- [ ] 2511.04824 · 2025-11-06 · Agentic Refactoring: An Empirical Study of AI Coding Agents · lead from 2611.13709
- [ ] 2511.04427 · 2025-11-06 · Speed at the Cost of Quality: How Cursor AI Increases Short-Term Velocity and Long-Term Complexity in Open-Source Projects · lead from 2610.35297
- [ ] 2510.15494 · 2025-10-17 · Do AI Models Dream of Faster Code? An Empirical Study on LLM-Proposed Performance Improvements in Real-World Software · lead from 2609.37985
- [ ] 2509.14745 · 2025-09-18 · On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub · lead from 2610.28683
- [ ] 2509.10402 · 2025-09-12 · Developer-LLM Conversations: An Empirical Study of Interactions and Generated Code Quality · lead from 2607.13196
- [ ] 2507.15003 · 2025-07-20 · The Rise of AI Teammates in Software Engineering (SE) 3.0: How Autonomous Coding Agents Are Reshaping Software Engineering · lead from 2611.13709
- [ ] 2506.12347 · 2025-06-14 · Why AI Agents Still Need You: Findings from Developer-Agent Collaborations in the Wild · lead from 2609.09671
- [ ] 2409.08379 · 2024-09-12 · The Impact of Large Language Models on Open-source Innovation: Evidence from GitHub Copilot · lead from 2410.12944
- [ ] 2310.02059 · 2023-10 · Security weaknesses of Copilot-generated code in GitHub projects · lead from 2609.17598
- [ ] 2303.08733 · 2023-03-15 · Practices and Challenges of Using GitHub Copilot: An Empirical Study · lead from 2402.05636

### instruction and context files

- [ ] 2610.21421 · 2026-10-15 · The Role of Agentic Instruction Categories for Code Generation: A Study of Five Python Libraries
- [ ] 2610.16859 · 2026-10-12 · ANCHOR: Assessing Naturalistic Constraint Hierarchies and Ordering in Repository-Grounded Agentic Coding · lead from 2611.05094
- [ ] 2610.06193 · 2026-10-05 · Correct Code, Broken Contributions? SWE-CC: Benchmarking Repository Policy Compliance for Coding Agents
- [ ] 2609.07360 · 2026-09-07 · Scanning the Harness: Configuration Exposures in AI Coding-Agent Supply Chains · lead from 2611.02383
- [ ] 2608.28497 · 2026-08-28 · On the Maintenance and Co-evolution of Agent Plugins: An Empirical Study of Claude Code Plugin Marketplaces · lead from 2611.02383
- [ ] 2608.25241 · 2026-08-26 · A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption · lead from 2610.30571
- [ ] 2608.16630 · 2026-08-17 · The Working Set of a Coding Agent: Coherence Debt in Repository-Scale Tasks · lead from 2611.09802
- [ ] 2608.11727 · 2026-08-12 · Harness-IF: Evaluating Instruction Following Across Instruction Surfaces in Coding Agents · lead from 2610.30571
- [ ] 2608.11095 · 2026-08-11 · Why Does CLAUDE.md Keep Growing? Catastrophic Remembering in Agentic Coding · lead from 2610.32578
- [ ] 2607.27250 · 2026-07-28 · Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories
- [ ] 2607.26819 · 2026-07-29 · A First Look at Coding Agents' Compliance with AI Contribution Rules in Open-Source Communities · lead from 2611.04367
- [ ] 2606.25257 · 2026-06-24 · How Do Developers Maintain and Evolve Their Agents' Instructions? An Empirical Study
- [ ] 2606.20512 · 2026-06-18 · Probe-and-Refine Tuning of Repository Guidance for Coding Agents
- [ ] 2606.15828 · 2026-06-14 · Configuration Smells in AGENTS.md Files: Common Mistakes in Configuring Coding Agents · lead from 2611.02383
- [ ] 2606.12231 · 2026-06-10 · Rule Taxonomy and Evolution in AI IDEs: A Mining and Survey Study · lead from 2610.32578
- [ ] 2606.09090 · 2026-06-08 · Context Rot in AI-Assisted Software Development: Repurposing Documentation Consistency for AI Configuration Artifacts · lead from 2611.09802
- [ ] 2605.10039 · 2026-05-11 · Instruction Adherence in Coding Agent Configuration Files: A Factorial Study of Four File-Structure Variables · lead from 2611.04367
- [ ] 2604.13108 · 2026-04-11 · Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents · lead from the trial search of 2026-11-14
- [ ] 2604.11088 · 2026-04-13 · Guardrails Beat Guidance: A Large-Scale Study of Rules, Skills, and Persistent Configuration for Coding Agents · lead from 2610.32578
- [ ] 2603.00822 · 2026-02-28 · ContextCov: Deriving and Enforcing Executable Constraints from Agent Instruction Files
- [ ] 2602.20478 · 2026-02-24 · Codified Context: Infrastructure for AI Agents in a Complex Codebase · lead from 2610.32578
- [ ] 2602.14690 · 2026-02-16 · Harness Engineering for Agentic AI Coding Tools: An Exploratory Study · lead from 2611.13709
- [ ] 2601.20404 · 2026-01-28 · On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents · lead from 2611.13709
- [ ] 2511.12884 · 2025-11-17 · Agent READMEs: An Empirical Study of Context Files for Agentic Coding
- [ ] 2510.21413 · 2025-10-24 · Context Engineering for AI Agents in Open-Source Software · lead from 2611.13709
- [ ] 2509.14744 · 2025-09-18 · On the Use of Agentic Coding Manifests: An Empirical Study of Claude Code · lead from 2607.00911
- [ ] 2302.00438 · 2023-02-01 · On the Robustness of Code Generation Techniques: An Empirical Study on GitHub Copilot · lead from 2304.10778

### skills

- [ ] 2608.11888 · 2026-08-12 · Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents · lead from 2610.04832
- [ ] 2605.13716 · 2026-05-13 · SkillOps: Managing LLM Agent Skill Libraries as Self-Maintaining Software Ecosystems · lead from 2610.36188
- [ ] 2605.11946 · 2026-05-12 · Counterfactual Trace Auditing of LLM Agent Skills · lead from 2610.04832
- [ ] 2604.04323 · 2026-04-06 · How Well Do Agentic Skills Work in the Wild: Benchmarking LLM Skill Usage in Realistic Settings · lead from 2610.11647
- [ ] 2604.03070 · 2026-04-03 · How Your Credentials Are Leaked by LLM Agent Skills: An Empirical Study · lead from 2607.00911
- [ ] 2603.29919 · 2026-03-31 · SkillReducer: Optimizing LLM Agent Skills for Token Efficiency · lead from 2605.24050
- [ ] 2603.22455 · 2026-03-23 · SkillRouter: Skill Routing for LLM Agents at Scale · lead from 2608.14036
- [ ] 2603.15401 · 2026-03-16 · SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering? · lead from 2610.11647
- [ ] 2603.02766 · 2026-03-03 · EvoSkill: Automated Skill Discovery for Multi-Agent Systems · lead from 2605.23904
- [ ] 2602.20867 · 2026-02-24 · SoK: Agentic Skills -- Beyond Tool Use in LLM Agents · lead from 2605.24050
- [ ] 2602.12670 · 2026-02-13 · SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks · lead from 2610.11647
- [ ] 2602.12430 · 2026-02-12 · Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward · lead from 2605.24050
- [ ] 2602.08004 · 2026-02-08 · Agent Skills: A Data-Driven Analysis of Claude Skills for Extending Large Language Model Functionality · lead from 2607.00911
- [ ] 2601.10338 · 2026-01-15 · Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at Scale · lead from 2607.00911
- [ ] 2505.03275 · 2025-05-06 · RAG-MCP: Mitigating Prompt Bloat in LLM Tool Selection via Retrieval-Augmented Generation · lead from 2605.24050
- [ ] 2305.16291 · 2023-05-25 · Voyager: An Open-Ended Embodied Agent with Large Language Models · lead from 2607.13091

### harness design

- [ ] 2609.01736 · 2026-09-01 · Harness Engineering in LLM Tool Use via Agent-Native Reusable Tool Primitives · lead from 2610.07832
- [ ] 2609.00006 · 2026-07-15 · Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents -- A Source-Code Study of Eleven Systems · lead from 2611.06946
- [ ] 2608.26218 · 2026-08-26 · Same Model, Different Harness: Different Coding-Agent Results · lead from 2610.35348
- [ ] 2608.21884 · 2026-08-22 · Loop Engineering: Building Blocks, Adoption, and Impact · lead from 2610.35348
- [ ] 2608.13547 · 2026-08-13 · QuoteBench: How Matched Scores Can Hide Command-Path Failures · lead from 2610.04375
- [ ] 2608.11386 · 2026-08-11 · The Devil Is in the Interface: Evaluating How Tool Architecture Shapes Coding Agent Behavior · lead from the trial search of 2026-11-14
- [ ] 2608.04804 · 2026-08-05 · Scrouting: Cost-Aware Routing of Coding Agents by Scouting the Repository First · lead from 2610.35971
- [ ] 2608.01964 · 2026-08-03 · LongHorizon-Harness: Advancing Long-Horizon Agents for Real-World Tasks · lead from 2610.00372
- [ ] 2608.01347 · 2026-08-02 · Prompt-Induced Waste in Coding Agents: Reasoning, Effort, Harness Design, and End-to-End Cost · lead from the trial search of 2026-11-14
- [ ] 2607.18859 · 2026-07-21 · PhoenixRepair: Rethinking Repair Strategy Exploration in Software Agents · lead from 2609.04167
- [ ] 2607.15684 · 2026-07-17 · Understanding Agent-Reactive Bugs at the Model-Harness Boundary: An Empirical Study of LLM Agent Issue Reports · lead from 2610.04375
- [ ] 2607.06000 · 2026-07-07 · Context-to-Execution Integrity for LLM Agents · lead from 2610.04375
- [ ] 2607.03691 · 2026-07-04 · Don't Blame the Large Language Model: How Agent Harness Evolution Shapes Coding Agent Quality · lead from 2610.35348
- [ ] 2606.17454 · 2026-06-16 · Dissecting model behavior through agent trajectories · lead from 2610.04375
- [ ] 2606.16988 · 2026-06-15 · Agent trajectories as programs: fingerprinting and programming coding-agent behavior · lead from 2610.35992
- [ ] 2606.10106 · 2026-06-08 · What makes a harness a harness: necessary and sufficient conditions for an agent harness · lead from 2611.06946
- [ ] 2606.08275 · 2026-06-06 · Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures · lead from 2610.04375
- [ ] 2606.00198 · 2026-05-29 · BAGEN: Are LLM Agents Budget-Aware? · lead from 2611.13241
- [ ] 2605.28840 · 2026-04-23 · How Consistent Are LLM Agents? Measuring Behavioral Reproducibility in Multi-Step Tool-Calling Pipelines · lead from 2608.09290
- [ ] 2605.27922 · 2026-05-27 · Harness-Bench: Evaluating Agent Harnesses across Models and Realistic Workflows · lead from 2610.00372
- [ ] 2605.25338 · 2026-05-25 · CausalFlow: Causal Attribution and Counterfactual Repair for LLM Agent Failures · lead from 2610.00372
- [ ] 2605.23950 · 2026-05-07 · Stop Comparing LLM Agents Without Disclosing the Harness · lead from 2610.35348
- [ ] 2605.18747 · 2026-05-18 · Code as Agent Harness · lead from 2609.32459
- [ ] 2605.18332 · 2026-05-18 · Same Signal, Different Semantics: A Cross-Framework Behavioral Analysis of Software Engineering Agents · lead from 2610.10263
- [ ] 2605.13357 · 2026-05-13 · AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents · lead from 2610.35992
- [ ] 2605.05716 · 2026-05-07 · More Is Not Always Better: Cross-Component Interference in LLM Agent Scaffolding · lead from 2609.20804
- [ ] 2605.03117 · 2026-05-04 · ARISE: A Repository-level Graph Representation and Toolset for Agentic Program Repair and Fault Localization · lead from 2611.07286
- [ ] 2604.25850 · 2026-04-28 · Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses · lead from 2610.35348
- [ ] 2604.22750 · 2026-04-24 · How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks · lead from 2610.04832
- [ ] 2604.08224 · 2026-04-09 · Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering · lead from 2609.32459
- [ ] 2604.02547 · 2026-04-02 · Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure · lead from 2611.09802
- [ ] 2603.26499 · 2026-03-27 · AIRA_2: Overcoming Bottlenecks in AI Research Agents · lead from 2609.40303
- [ ] 2603.25723 · 2026-03-26 · Natural-Language Agent Harnesses · lead from 2609.32459
- [ ] 2603.05637 · 2026-03-05 · Real Faults in Model Context Protocol (MCP) Software: a Comprehensive Taxonomy · lead from 2609.35381
- [ ] 2603.01048 · 2026-03-01 · RepoRepair: Leveraging Code Documentation for Repository-Level Automated Program Repair · lead from 2611.07286
- [ ] 2602.14878 · 2026-02-16 · Model Context Protocol (MCP) Tool Descriptions Are Smelly! Towards Improving AI Agent Efficiency with Augmented MCP Tool Descriptions · lead from 2609.35381
- [ ] 2601.22129 · 2026-01-29 · SWE-Replay: Efficient Test-Time Scaling for Software Engineering Agents · lead from 2610.29870
- [ ] 2601.05777 · 2026-01-09 · EET: Experience-Driven Early Termination for Cost-Efficient Software Engineering Agents · lead from 2611.13241
- [ ] 2601.04688 · 2026-01-08 · ToolGate: Contract-Grounded and Verified Tool Execution for LLMs · lead from 2609.08371
- [ ] 2510.11977 · 2025-10-13 · Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation · lead from 2610.35348
- [ ] 2509.23586 · 2025-09-28 · Reducing Cost of LLM Agents with Trajectory Reduction · lead from 2611.13241
- [ ] 2509.09853 · 2025-09-11 · SWE-Effi: Re-Evaluating Software AI Agent System Effectiveness Under Resource Constraints · lead from 2608.09290
- [ ] 2508.02694 · 2025-07-24 · Efficient Agents: Building Effective Agents While Reducing Cost · lead from 2608.09290
- [ ] 2507.02554 · 2025-07-03 · AI Research Agents for Machine Learning: Search, Exploration, and Generalization in MLE-bench · lead from 2609.40303
- [ ] 2501.14723 · 2025-01-24 · CodeMonkeys: Scaling Test-Time Compute for Software Engineering · lead from 2608.08950
- [ ] 2407.21787 · 2024-07-31 · Large Language Monkeys: Scaling Inference Compute with Repeated Sampling · lead from 2610.41433
- [ ] 2407.01489 · 2024-07-01 · Agentless: Demystifying LLM-based Software Engineering Agents · lead from 2609.32459
- [ ] 2405.15793 · 2024-05-06 · SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering · lead from 2607.13091
- [ ] 2403.17134 · 2024-03-25 · RepairAgent: An Autonomous, LLM-Based Agent for Program Repair · lead from 2610.41433

### tests and self-verification

- [ ] 2608.04682 · 2026-08-05 · Active-SWE: Benchmarking Coding Agents for Proactive Bug Fixing without Issue Reports · lead from 2611.01181
- [ ] 2607.28871 · 2026-07-30 · Validation Evidence in LLM Repair Agents: How Much of What Passes Actually Tests the Bug? · lead from 2610.30571
- [ ] 2607.28815 · 2026-07-30 · Preventing Premature Commitment in Coding Agents with an Evidence-Conditioned Execution Layer
- [ ] 2607.18966 · 2026-07-21 · Measuring Reward-Seeking via Contrastive Belief Updates · lead from 2609.20812
- [ ] 2607.18057 · 2026-07-20 · Test Coverage Analysis of Agentic Pull Requests · lead from 2610.35297
- [ ] 2607.14890 · 2026-07-16 · Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control
- [ ] 2607.00990 · 2026-07-01 · SWE-Doctor: Guiding Software Engineering Agents with Runtime Diagnosis from Multi-Faceted Bug Reproduction Tests · lead from 2610.23782
- [ ] 2606.26978 · 2026-06-25 · To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair · lead from 2611.13241
- [ ] 2606.24820 · 2026-06-23 · SHERLOC: Structured Diagnostic Localization for Code Repair Agents · lead from 2610.29870
- [ ] 2606.22936 · 2026-06-22 · When Agents Commit Too Soon: Diagnosing Premature Commitment in LLM Agents · lead from 2611.16289
- [ ] 2606.01522 · 2026-06-01 · Type-Error Ablation and AI Coding Agents · lead from the trial search of 2026-11-14
- [ ] 2606.00920 · 2026-05-30 · How Much Can Repeated Running Buy? A Measured Variance Ceiling for LLM Code Evaluation · lead from 2610.41433
- [ ] 2605.25665 · 2026-05-25 · Meta-Engineering Harnesses for AI-Native Software Production: A Contract-Driven Adversarial Verification Architecture with Early Deployment Report · lead from 2611.06946
- [ ] 2605.12925 · 2026-05-13 · AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation · lead from 2611.09802
- [ ] 2605.06125 · 2026-05-07 · Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution · lead from 2610.35297
- [ ] 2604.05955 · 2026-04-07 · Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution · lead from 2609.04167
- [ ] 2604.01518 · 2026-04-02 · Probe to Generate: Program Variant-Guided Test Augmentation for Repository-Level Repair Benchmarks · lead from 2608.08950
- [ ] 2602.07900 · 2026-02-08 · Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents
- [ ] 2602.06948 · 2026-02-06 · Agentic Uncertainty Reveals Agentic Overconfidence · lead from 2611.16289
- [ ] 2602.05892 · 2026-02-05 · ContextBench: A Benchmark for Context Retrieval in Coding Agents · lead from 2609.20812
- [ ] 2602.00409 · 2026-01-30 · Are Coding Agents Generating Over-Mocked Tests? An Empirical Study · lead from 2609.09671
- [ ] 2601.18827 · 2026-01-25 · Automated structural testing of LLM-based agents: methods, framework, and case studies · lead from 2609.20625
- [ ] 2512.21919 · 2025-12-26 · SWE-RM: Execution-free Feedback For Software Engineering Agents · lead from the trial search of 2026-11-14
- [ ] 2511.14224 · 2025-11-18 · Knowledge Matters: Injecting Project and Testing Knowledge into LLM-based Unit Test Generation · lead from 2609.04167
- [ ] 2510.23761 · 2025-10-27 · TDFlow: Agentic Workflows for Test Driven Development
- [ ] 2510.20270 · 2025-10-23 · ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases
- [ ] 2509.13941 · 2025-09-17 · An Empirical Study on Failures in Automated Issue Solving · lead from 2611.16289
- [ ] 2505.17716 · 2025-05-23 · Get Experience from Practice: LLM Agents with Record & Replay · lead from 2609.20625
- [ ] 2411.13768 · 2024-11-21 · Evaluation-Driven Development and Operations of LLM Agents: A Process Model and Reference Architecture · lead from 2610.08651
- [ ] 2409.09464 · 2024-09-14 · Measuring the Influence of Incorrect Code on Test Generation · lead from 2610.08651
- [ ] 2404.13340 · 2024-04-20 · Large Language Models as Test Case Generators: Performance Evaluation and Enhancement · lead from 2610.15708
- [ ] 2310.01798 · 2023-10-03 · Large Language Models Cannot Self-Correct Reasoning Yet · lead from 2611.16289
- [ ] 2304.05128 · 2023-04-11 · Teaching Large Language Models to Self-Debug · lead from 2607.13091
- [ ] 2207.10397 · 2022-07-21 · CodeT: Code Generation with Generated Tests · lead from 2607.21656

### code review by agents

- [ ] 2607.06065 · 2026-07-07 · SWE-Review: Closing the Loop on Issue Resolution with Agentic Code Review · lead from 2611.01181
- [ ] 2607.03316 · 2026-07-03 · Is Agentic Code Review Helpful? Mining Developers' Feedback to CodeRabbit Reviews in the Wild · lead from 2608.21311
- [ ] 2606.13175 · 2026-06-11 · The End of Code Review: Coding Agents Supersede Human Inspection · lead from 2610.28683
- [ ] 2606.01859 · 2026-06-01 · Improving LLM-Based Go Code Review through Issue-List Generation and Context Augmentation · lead from 2608.09290
- [ ] 2604.24450 · 2026-04-27 · On the Footprints of Reviewer Bots Feedback on Agentic Pull Requests in OSS GitHub Repositories · lead from 2607.07980
- [ ] 2604.03196 · 2026-04-03 · From Industry Claims to Empirical Reality: An Empirical Study of Code Review Agents in Pull Requests
- [ ] 2603.23448 · 2026-03-24 · Code Review Agent Benchmark · lead from 2610.13668
- [ ] 2603.15911 · 2026-03-16 · Human-AI Synergy in Agentic Code Review · lead from 2608.21311
- [ ] 2603.12123 · 2026-03-12 · Cross-Context Review: Improving LLM Output Quality by Separating Production and Review Sessions · lead from 2611.05094
- [ ] 2603.11078 · 2026-03-10 · CR-Bench: Evaluating the Real-World Utility of AI Code Review Agents · lead from 2610.13668
- [ ] 2603.00539 · 2026-02-28 · Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement · lead from 2607.21656
- [ ] 2602.19441 · 2026-02-23 · When AI Teammates Meet Code Review: Collaboration Signals Shaping the Integration of Agent-Authored Pull Requests · lead from 2607.07980
- [ ] 2601.19494 · 2026-01-27 · AACR-Bench: Evaluating Automatic Code Review with Holistic Repository-Level Context · lead from 2608.09290
- [ ] 2601.19287 · 2026-01-27 · Understanding Dominant Themes in Reviewing Agentic AI-authored Code · lead from 2607.07980
- [ ] 2601.13754 · 2026-01-20 · On Autopilot? An Empirical Study of Human-AI Teaming and Review Practices in Open Source · lead from 2607.07980
- [ ] 2508.18771 · 2025-08-26 · Does AI Code Review Lead to Code Changes? A Case Study of GitHub Actions · lead from 2610.28683
- [ ] 2501.18160 · 2025-01-30 · RepoAudit: An Autonomous LLM-Agent for Repository-Level Code Auditing · lead from 2608.09290
- [ ] 2410.21819 · 2024-10-29 · Self-Preference Bias in LLM-as-a-Judge · lead from 2608.21311
- [ ] 2407.00215 · 2024-06-28 · LLM Critics Help Catch LLM Bugs · lead from 2610.08651
- [ ] 2404.18496 · 2024-04-29 · AI-powered Code Review with LLMs: Early Results · lead from 2607.13196

### specifications and plans

- [ ] 2608.21747 · 2026-08-22 · Architecture as Capability Equalizer for Coding Agents · lead from the trial search of 2026-11-14
- [ ] 2608.17177 · 2026-08-17 · Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation
- [ ] 2608.12440 · 2026-08-12 · Specification-first convergence with an AI coding agent: a case study of dismantling a core architectural invariant across 189 files in a 717k-line codebase with no test oracle and no human code review · lead from 2611.05094
- [ ] 2608.04661 · 2026-08-05 · An Exploratory Study of Agent Plans for Agentic AI Coding Tools in Open-Source Software
- [ ] 2607.27167 · 2026-07-29 · SpecFirst: Behavioral Specification Elicitation as a First-Class Step in Agent-Based Program Synthesis from Scratch · lead from 2610.38214
- [ ] 2606.27045 · 2026-06-25 · The Spec Growth Engine: Spec-Anchored, Code-Coupled, Drift-Enforced Architecture for AI-Assisted Software Development · lead from 2608.25202
- [ ] 2606.07681 · 2026-06-04 · Systematic LLM Translation of Legacy Scientific Code to Differentiable Frameworks: Application to a Land Surface Model · lead from 2610.09995
- [ ] 2604.05278 · 2026-04-07 · Spec Kit Agents: Context-Grounded Agentic Workflows · lead from 2611.05094
- [ ] 2603.25697 · 2026-03-26 · The Kitchen Loop: User-Spec-Driven Development for a Self-Evolving Codebase · lead from 2608.25202
- [ ] 2602.02584 · 2026-01-31 · Constitutional Spec-Driven Development: Enforcing Security by Construction in AI-Assisted Code Generation · lead from 2608.25202
- [ ] 2602.00180 · 2026-01-30 · Spec-Driven Development:From Code to Contract in the Age of AI Coding Assistants · lead from 2609.09671
- [ ] 2601.23257 · 2026-01-30 · From Historical Patches to Repair Plans: Outcome-Conditioned Reasoning for Repository-Level Program Repair · lead from 2608.08950
- [ ] 2601.22956 · 2026-01-30 · SWE-Manager: Selecting and Synthesizing Golden Proposals Before Coding · lead from 2610.29870
- [ ] 2509.16198 · 2025-09-19 · RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation · lead from 2610.38214
- [ ] 2509.06216 · 2025-09-07 · Agentic Software Engineering: Foundational Pillars and a Research Roadmap · lead from 2609.00252
- [ ] 2410.24119 · 2024-10-31 · Leveraging Large Language Models for Code Translation and Software Development in Scientific Computing · lead from 2610.09995
- [ ] 2410.06107 · 2024-10-08 · Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap · lead from 2609.00252

### parallel and multi-agent work

- [ ] 2609.25396 · 2026-09-21 · Passes Alone, Fails Together: Benchmarking Semantic Coordination in Parallel LLM-Agent Development
- [ ] 2609.01481 · 2026-09-01 · Harness-of-Harness: Multi-Day Autonomous Software Development with Continual Improvement · lead from 2611.06946
- [ ] 2608.26081 · 2026-08-26 · SwarmWorld: Stigmergic technological evolution in societies of language-model agents · lead from 2610.36254
- [ ] 2608.11965 · 2026-08-12 · Developing LLM-based Multi-Agent Systems in Software Engineering: A Mixed-Method Experience Report
- [ ] 2608.02685 · 2026-08-03 · BulkPR-Bench: Benchmarking Queue-Level Governance of Interacting Pull Requests · lead from 2610.04779
- [ ] 2608.00267 · 2026-07-31 · LoopsBench: From Harness Engineering to Loop Engineering in Coding Agent Evaluation · lead from 2610.10263
- [ ] 2607.28430 · 2026-07-30 · AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration · lead from 2611.00314
- [ ] 2607.04697 · 2026-07-06 · AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates · lead from 2610.04779
- [ ] 2606.25514 · 2026-06-24 · Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution · lead from 2610.23782
- [ ] 2606.19616 · 2026-06-17 · Before the Pull Request: Mining Multi-Agent Coordination
- [ ] 2606.10662 · 2026-06-09 · Decentralized Multi-Agent Systems with Shared Context · lead from 2611.00314
- [ ] 2604.03551 · 2026-04-04 · AgenticFlict: A Large-Scale Dataset of Merge Conflicts in AI Coding Agent Pull Requests on GitHub · lead from 2610.04779
- [ ] 2603.21489 · 2026-03-23 · Effective Strategies for Asynchronous Software Engineering Agents · lead from 2611.00314
- [ ] 2602.03128 · 2026-02-03 · Architectural Design, Not Only Model Intelligence, Governs Multi-Agent LLM Performance · lead from 2609.40303
- [ ] 2601.13295 · 2026-01-19 · CooperBench: Why Coding Agents Cannot be Your Teammates Yet · lead from 2611.00314
- [ ] 2512.08296 · 2025-12-09 · Towards a Science of Scaling Agent Systems · lead from 2610.36254
- [ ] 2511.02687 · 2025-11-04 · The Collaboration Gap: Exploration and Benchmarking of Open-World Agentic Cooperation · lead from 2611.00314
- [ ] 2505.00212 · 2025-04-30 · Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems · lead from 2609.39957
- [ ] 2503.13657 · 2025-03 · Why do multi-agent LLM systems fail? · lead from 2609.17598
- [ ] 2312.13010 · 2023-12-20 · AgentCoder: Multi-Agent-based Code Generation with Iterative Testing and Optimisation · lead from 2607.21656

### memory, state and long-running work

- [ ] 2610.17616 · 2026-10-13 · StateHarness: Maintaining Evolving Project State for Long-Horizon Coding Agents
- [ ] 2610.05572 · 2026-10-04 · Disentangling Task Difficulty from Run-Level Failure in Agent Failure Prediction · lead from 2610.35971
- [ ] 2609.36059 · 2026-09-28 · Mnemon: Raw Records, Fast Judgments, Slow Thoughts · lead from 2610.27301
- [ ] 2609.23570 · 2026-09-20 · VibeMemBench: Evaluating Memory Systems for Coding Agents on Real Repository Coding Tasks · lead from 2610.41433
- [ ] 2609.20045 · 2026-09-17 · Correct Now, Insufficient Later: Auditing Update Sufficiency in Context Compression · lead from 2610.27301
- [ ] 2609.05510 · 2026-08-31 · Memory as Infrastructure: Reliability Engineering for Persistent Agent Memory in Months-Long LLM-Assisted Development
- [ ] 2609.03436 · 2026-09-03 · It's the Problem, Not the Path: Budget and Difficulty Confounds in LLM Reasoning Trajectories · lead from 2610.35971
- [ ] 2608.22752 · 2026-08-24 · The Compaction Cliff in Long-Running AI Agent Memory · lead from 2611.00689
- [ ] 2608.16370 · 2026-08-17 · What Does Context Compression Cost an Agent? Interaction Costs Unrevealed by Task-Completion Metrics · lead from 2610.27301
- [ ] 2608.11242 · 2026-07-31 · Lost in Context Compaction: When LLM Systems Drop Side Constraints · lead from 2610.27301
- [ ] 2608.03222 · 2026-08-04 · Fail-Fast, Restart-Smart: Early Failure Prediction and Restart for SWE Agentic Tasks · lead from 2610.35971
- [ ] 2607.09510 · 2026-07-10 · Failure as a Process: An Anatomy of CLI Coding Agent Trajectories · lead from 2610.35971
- [ ] 2607.06503 · 2026-07-07 · Doomed from the Start: Early Abort of LLM Agent Episodes via a Recall-Controlled Probe Cascade · lead from 2610.35971
- [ ] 2606.30005 · 2026-06-29 · LLM Agents Are Latent Context Managers: Eliciting Self-Managed Context via State Proprioception · lead from 2609.20804
- [ ] 2606.29914 · 2026-06-29 · MemDelta: Controlled Baselines and Hidden Confounds in Agent Memory Evaluation · lead from 2610.29823
- [ ] 2606.24322 · 2026-06-23 · Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees · lead from 2610.29869
- [ ] 2606.23127 · 2026-06-22 · Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation · lead from 2608.14036
- [ ] 2606.22528 · 2026-06-21 · Governance Decay: How Context Compaction Silently Erases Safety Constraints in Long-Horizon LLM Agents · lead from 2610.29869
- [ ] 2606.22417 · 2026-06-21 · Code Isn't Memory: A Structural Codebase Index Inside a Coding Agent · lead from 2610.35348
- [ ] 2606.21732 · 2026-06-19 · Safe to Check, Unsafe to Use: Relinking at the Compression Boundary of LLM Agents · lead from 2610.29869
- [ ] 2606.07682 · 2026-06-05 · SWE-Marathon: Can Agents Autonomously Complete Ultra-Long-Horizon Software Work?
- [ ] 2606.05894 · 2026-06-04 · EMBER: Efficient Memory via Budgeted Evidence Retention for Long-Horizon Agents · lead from 2610.27301
- [ ] 2606.04329 · 2026-06-03 · From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents · lead from 2610.29869
- [ ] 2606.02875 · 2026-06-01 · Handoff Debt: The Rediscovery Cost When Coding Agents Take Over Interrupted Tasks · lead from 2611.02017
- [ ] 2605.29463 · 2026-05-28 · Honest Lying: Understanding Memory Confabulation in Reflexive Agents · lead from 2610.41433
- [ ] 2605.26596 · 2026-05-26 · AGORA: Adapter-Grounded Observation-Action Retention for Inference-Free Prompt Compression in LLM Agents · lead from 2610.27301
- [ ] 2605.14415 · 2026-05-14 · SWE-Chain: Benchmarking Coding Agents on Chained Release-Level Package Upgrades · lead from 2611.07166
- [ ] 2605.06527 · 2026-05-07 · STALE: Can LLM Agents Know When Their Memories Are No Longer Valid? · lead from 2610.32578
- [ ] 2605.04050 · 2026-02-14 · LCM: Lossless Context Management · lead from 2609.20804
- [ ] 2604.11628 · 2026-04-13 · Back to Basics: Let Conversational Agents Remember with Just Retrieval and Generation · lead from 2610.29823
- [ ] 2604.03035 · 2026-04-03 · Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution · lead from 2611.07166
- [ ] 2603.24755 · 2026-03-25 · SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks · lead from 2611.07166
- [ ] 2602.17913 · 2026-02-20 · From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents · lead from 2610.27301
- [ ] 2602.14229 · 2026-02-15 · CORPGEN: Simulating Corporate Environments with Autonomous Digital Employees in Multi-Horizon Task Environments · lead from 2611.02017
- [ ] 2602.08316 · 2026-02-09 · SWE Context Bench: A Benchmark for Context Learning in Coding · lead from 2611.02017
- [ ] 2601.06789 · 2026-01-11 · MemGovern: Enhancing Code Agents through Learning from Governed Human Experiences · lead from 2610.41433
- [ ] 2601.00821 · 2025-12-23 · Fidelity Before Structure: Verbatim Chunks Beat Lossy Artifact Extraction in Long-Conversation LLM Memory · lead from 2610.29823
- [ ] 2512.18746 · 2025-12-21 · MemEvolve: Meta-Evolution of Agent Memory Systems · lead from 2610.29823
- [ ] 2510.00615 · 2025-10-01 · ACON: Optimizing Context Compression for Long-horizon LLM Agents · lead from 2609.20804
- [ ] 2509.25140 · 2025-09-29 · ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory · lead from 2610.14224
- [ ] 2508.21433 · 2025-08-29 · The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management · lead from 2611.02017
- [ ] 2508.06433 · 2025-08-08 · Memp: Exploring Agent Procedural Memory · lead from 2608.14036
- [ ] 2507.00014 · 2025-06-13 · SWE-Bench-CL: Continual Learning for Coding Agents · lead from 2611.03219
- [ ] 2409.07429 · 2024-09-11 · Agent Workflow Memory · lead from 2608.14036

### human oversight and intervention

- [ ] 2608.06701 · 2026-08-07 · Online Monitoring and Corrective Steering of Programming Agents · lead from 2610.23782
- [ ] 2608.03329 · 2026-08-04 · Making AI Visible, Not Vanished: How AI Policies Reshape Developer Experience on GitHub · lead from 2610.11179
- [ ] 2607.21642 · 2026-07-21 · CARE: Pre-Execution Command Verification for Shell-Executing LLM Agents · lead from 2610.04375
- [ ] 2607.10856 · 2026-07-12 · How Do Practitioners Build SE Agents? Insights from a Mixed-Methods Study · lead from 2610.08651
- [ ] 2607.02389 · 2026-07-02 · Steerability via constraints: a substrate for scalable oversight of coding agents · lead from the trial search of 2026-11-14
- [ ] 2606.22721 · 2026-06-21 · Habituation at the Gate: Rising Approval and Declining Scrutiny in Human Review of AI Agent Code · lead from 2607.07980
- [ ] 2605.18583 · 2026-05-18 · Overeager Coding Agents: Measuring Out-of-Scope Actions on Benign Tasks · lead from 2611.05094
- [ ] 2605.16706 · 2026-05-15 · AI Policy, Disclosure, and Human in the Loop: How Are Contribution Guidelines Adapting to GenAI? · lead from 2610.11179
- [ ] 2605.12105 · 2026-05-12 · Autonomy and Agency in Agentic AI: Architectural Tactics for Regulated Contexts · lead from 2610.08651
- [ ] 2605.11495 · 2026-05-12 · Hedwig: Dynamic Autonomy for Coding Agents Under Local Oversight
- [ ] 2605.10913 · 2026-05-11 · Shepherd: Enabling Programmable Meta-Agents via Reversible Agentic Execution Traces · lead from 2610.08651
- [ ] 2605.02273 · 2026-05-04 · These Aren't the Reviews You're Looking For How Humans Review AI-Generated Pull Requests · lead from 2610.28683
- [ ] 2604.20779 · 2026-04-22 · SWE-chat: Coding Agent Interactions From Real Users in the Wild · lead from 2609.39957
- [ ] 2604.10599 · 2026-04-12 · Rethinking Software Engineering for Agentic AI Systems · lead from 2609.24234
- [ ] 2604.10493 · 2026-04-12 · SWE-Shepherd: Advancing PRMs for Reinforcing Code Agents · lead from 2608.08950
- [ ] 2603.26487 · 2026-03-27 · To Ban or not to Ban? How Open Source Projects Govern GenAI Contributions · lead from 2609.07542
- [ ] 2603.26233 · 2026-03-27 · Ask or Assume? Uncertainty-Aware Clarification-Seeking in Coding Agents
- [ ] 2603.22106 · 2026-03-23 · From Technical Debt to Cognitive and Intent Debt: Rethinking Software Health in the Age of AI · lead from 2608.25202
- [ ] 2602.02475 · 2026-02-02 · AgentRx: Diagnosing AI Agent Failures from Execution Trajectories · lead from 2609.39957
- [ ] 2512.14012 · 2025-12-16 · Professional Software Developers Don't Vibe, They Control: AI Agent Use for Coding in 2025 · lead from 2611.13709
- [ ] 2509.22040 · 2025-09-26 · "Your AI, My Shell": Demystifying Prompt Injection Attacks on Agentic AI Coding Editors · lead from 2609.08371
- [ ] 2509.02360 · 2025-09-02 · When Agents go Astray: Course-Correcting SWE Agents with PRMs · lead from 2610.29870
- [ ] 2505.08638 · 2025-05-13 · TRAIL: Trace Reasoning and Agentic Issue Localization · lead from 2609.39957
- [ ] 2504.11703 · 2025-04-16 · Progent: Securing AI Agents with Privilege Control · lead from 2609.08371
- [ ] 2503.12374 · 2025-03-16 · Beyond Final Code: A Process-Oriented Error Analysis of Software Development Agents in Real-World GitHub Scenarios · lead from 2609.39957
- [ ] 2210.14306 · 2022-10-25 · Reading Between the Lines: Modeling User Behavior and Costs in AI-Assisted Programming · lead from 2302.06590
- [ ] 2206.15000 · 2022-06-30 · Grounded Copilot: How Programmers Interact with Code-Generating Models · lead from 2302.06590

### self-improving agents

- [ ] 2608.02276 · 2026-08-03 · Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories · lead from 2610.32578
- [ ] 2607.15524 · 2026-07-17 · Recursive Harness Self-Improvement · lead from 2610.14224
- [ ] 2607.12227 · 2026-07-14 · Rethinking the Evaluation of Harness Evolution for Agents · lead from 2610.32578
- [ ] 2607.08124 · 2026-07-09 · TTHE: Test-Time Harness Evolution · lead from 2610.14224
- [ ] 2606.06324 · 2026-06-04 · From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws · lead from 2611.06946
- [ ] 2606.01770 · 2026-06-01 · Adaptive Auto-Harness: Sustained Self-Improvement for Agentic System Deployment on Open-Ended Task Streams · lead from 2610.14224
- [ ] 2605.25430 · 2026-05-25 · CODESKILL: Learning Self-Evolving Skills for Coding Agents · lead from 2610.36188
- [ ] 2605.22166 · 2026-05-21 · Adapting the Interface, Not the Model: Runtime Harness Adaptation for Deterministic LLM Agents · lead from 2606.14249
- [ ] 2605.09998 · 2026-05-11 · Continual Harness: Online Adaptation for Self-Improving Foundation Agents · lead from 2610.14224
- [ ] 2603.28052 · 2026-03-30 · Meta-Harness: End-to-End Optimization of Model Harnesses · lead from 2611.03219
- [ ] 2603.26664 · 2026-03-27 · Learning to Commit: Generating Organic Pull Requests via Online Repository Memory · lead from 2610.36188
- [ ] 2603.25158 · 2026-03-26 · Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills · lead from 2610.36188
- [ ] 2603.19461 · 2026-03-19 · Hyperagents · lead from 2606.14249
- [ ] 2511.13646 · 2025-11-17 · Live-SWE-agent: Can Software Engineering Agents Self-Evolve on the Fly?
- [ ] 2510.04618 · 2025-10-06 · Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models · lead from 2609.12742
- [ ] 2505.22954 · 2025-05-29 · Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents
- [ ] 2505.22535 · 2025-05-28 · RiverMamba: A State Space Model for Global River Discharge and Flood Forecasting · lead from 2606.14249
- [ ] 2504.15228 · 2025-04-21 · A Self-Improving Coding Agent · lead from 2606.14249

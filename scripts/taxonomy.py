"""Closed-set label taxonomy. Every axis exists to answer one question:
which human turns are load-bearing, and which are ceremony a workflow could do?"""

INTENT = {
    "initiate_task": "opens new work: a goal, feature, bug, question not previously in play",
    "refine_scope": "narrows/expands/constrains work already in play",
    "approve_proceed": "green-lights what the agent proposed; adds no new information",
    "reject_redirect": "rejects the agent's direction and points elsewhere",
    "correct_error": "the agent got something wrong or incomplete; the human fixes it",
    "supply_info": "hands over facts the agent could not obtain itself (creds, external state, screenshots, decisions)",
    "ask_question": "asks about code/state/plan without commissioning work",
    "request_status": "asks what happened / where things stand",
    "request_verification": "asks the agent to prove, test, re-check or show evidence",
    "meta_process": "changes how the agent works: prefs, rules, tools, memory, harness config",
    "interrupt_abort": "stops the agent mid-flight",
    "housekeeping": "commit, push, PR, cleanup, release chores",
    "delegate_parallel": "asks for fan-out, sub-agents, background work",
    "resume_continue": "'go on', 'continue', 'next' - restart of stalled work with no new content",
    "social": "thanks, praise, banter, venting with no operational content",
}

TASK_KIND = [
    "implement", "debug", "refactor", "review", "test", "release_deploy",
    "research_explore", "docs_write", "data_analysis", "config_env",
    "planning_design", "ops_incident", "communication", "meta_agent_config", "other",
]

MOTIVATION = [
    "unblock_agent", "steer_quality", "save_cost_time", "verify_trust",
    "explore_options", "enforce_standard", "deliver_artifact", "curiosity",
    "fix_agent_mistake", "personal_preference",
]

SENTIMENT = ["positive", "neutral", "terse_pressing", "frustrated", "appreciative"]

NOVEL_INFO = {
    "none": "everything in the turn was already derivable from the transcript or the repo",
    "preference": "a taste/style/priority call that is the human's to make",
    "external_state": "facts only the human could see (a UI, a person said X, a device, a dashboard)",
    "goal": "new objective or business intent",
    "judgment_call": "a tradeoff decision between options the agent had already surfaced",
    "domain_knowledge": "non-obvious system/domain knowledge the agent lacked",
}

REPLACEABLE_BY = {
    "deterministic_rule": "a script/hook/CI gate could have emitted this turn verbatim (e.g. 'run the tests', 'commit it', 'fix the lint')",
    "ai_policy": "a fixed agent policy/system-prompt rule could replace it (e.g. always verify before claiming done)",
    "ai_with_context": "another AI with repo+history context could produce this turn, but it needs judgment",
    "human_only": "requires human authority, taste, external observation or accountability",
}

FRICTION = ["agent_error", "agent_omission", "ambiguous_spec", "missing_context", "tool_failure", "none"]

TURN_SCHEMA = {
    "type": "object",
    "properties": {
        "labels": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "intent": {"type": "string", "enum": list(INTENT)},
                    "task_kind": {"type": "string", "enum": TASK_KIND},
                    "motivation": {"type": "string", "enum": MOTIVATION},
                    "sentiment": {"type": "string", "enum": SENTIMENT},
                    "novel_information": {"type": "string", "enum": list(NOVEL_INFO)},
                    "replaceable_by": {"type": "string", "enum": list(REPLACEABLE_BY)},
                    "rule_sketch": {"type": "string", "description": "if deterministic_rule or ai_policy: the trigger->action rule, <=15 words. else ''"},
                    "is_rework": {"type": "boolean", "description": "this turn exists only because the agent erred or stopped short"},
                    "friction_source": {"type": "string", "enum": FRICTION},
                    "confidence": {"type": "number"},
                },
                "required": ["id", "intent", "task_kind", "motivation", "sentiment",
                             "novel_information", "replaceable_by", "rule_sketch",
                             "is_rework", "friction_source", "confidence"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["labels"],
    "additionalProperties": False,
}

SESSION_SCHEMA = {
    "type": "object",
    "properties": {
        "goal": {"type": "string", "description": "what the session was for, <=20 words"},
        "outcome": {"type": "string", "enum": ["success", "partial", "failed", "abandoned", "open_ended"]},
        "outcome_evidence": {"type": "string", "description": "the concrete signal you judged on, <=25 words"},
        "workflow_archetype": {"type": "string", "enum": [
            "ticket_to_pr", "bug_hunt_fix", "refactor_sweep", "greenfield_scaffold",
            "review_and_gate", "release_cut", "research_brief", "ops_investigation",
            "doc_or_report_write", "agent_harness_tuning", "data_pull_analysis",
            "backlog_grooming", "multi_agent_fanout", "exploratory_chat", "other"]},
        "steps": {"type": "array", "items": {"type": "string"},
                  "description": "the ordered recipe actually executed, 3-10 imperative steps, tool-level not prose"},
        "human_essential_moments": {"type": "array", "items": {"type": "string"},
                                    "description": "turns where a human was genuinely required, and why. empty if none"},
        "automation_verdict": {"type": "string", "enum": [
            "full_auto", "auto_with_gates", "needs_human_judgment", "not_automatable"]},
        "automation_blockers": {"type": "array", "items": {"type": "string"}},
        "rework_share": {"type": "string", "enum": ["none", "low", "medium", "high"],
                         "description": "how much of the session was the human repairing agent output"},
        "confidence": {"type": "number"},
    },
    "required": ["goal", "outcome", "outcome_evidence", "workflow_archetype", "steps",
                 "human_essential_moments", "automation_verdict", "automation_blockers",
                 "rework_share", "confidence"],
    "additionalProperties": False,
}

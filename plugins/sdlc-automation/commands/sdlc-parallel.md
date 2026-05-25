---
allowed-tools: Bash, Read
description: "Run SDLC pipeline in parallel DAG mode — each agent gets a fresh context window"
---

# SDLC Pipeline — Parallel DAG Mode

Each agent runs as an isolated subprocess with a **fresh 200K context window**.
Agents within the same phase run concurrently. JSON contracts on disk are the
only communication channel.

!`python3 scripts/orchestrator.py --mode parallel`

---

## How parallel mode works

```
Phase 1 (parallel):   environment_agent ∥ transcript_agent
Phase 2 (sequential): requirement_agent
Phase 3 (parallel):   documentation_agent ∥ planning_agent
Phase 4 (parallel):   jira_agent ∥ architecture_agent
Phase 5 (optional):   security_threat_model_agent
Phase 6 (sequential): code_agent
Phase 7 (parallel):   testing_agent ∥ compliance_checker_agent
Phase 8 (sequential): deployment_agent
Phase 9 (sequential): summary_agent → cost_estimation_agent → feedback_loop_agent
```

Each agent in the same phase runs in its own `claude -p` process — no context
accumulation, no compaction mid-pipeline.

## Claude.ai web fallback

If shell commands are not available, use `/sdlc-start` to run interactively.

---
allowed-tools: Bash, Read
description: "Run SDLC pipeline sequentially — one agent at a time, fresh context per agent"
---

# SDLC Pipeline — Sequential Mode

Each agent runs as an isolated subprocess — fresh context window per agent.
Agents run one at a time (safer for debugging, easier to resume).

!`python3 scripts/orchestrator.py --mode sequential`

---

## Use sequential mode when

- Debugging a specific phase (easier to see exactly what each agent did)
- Resources are limited (parallel spawns multiple Claude sessions)
- First run on a new project (sequential is more predictable)

Switch to parallel after validating the pipeline works end-to-end.

## Claude.ai web fallback

If shell commands are not available, use `/sdlc-start` to run interactively.

---
allowed-tools: Bash, Read
description: "Run SDLC pipeline sequentially — one agent at a time, fresh context per agent"
---

# SDLC Pipeline — Sequential Mode

Each agent runs as an isolated subprocess — fresh context window per agent.
Agents run one at a time (safer for debugging, easier to resume).

> First time? Run `/sdlc-setup` to copy the scripts into this project.

!`python3 -c "import pathlib, subprocess, sys; paths = [pathlib.Path('scripts/orchestrator.py'), *pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/scripts/orchestrator.py')]; orch = next((p for p in paths if p.exists()), None); (subprocess.run(['python3', str(orch), '--mode sequential']) if orch else print('Run /sdlc-setup first to install helpers and scripts.'))"`


---

## Use sequential mode when

- Debugging a specific phase (easier to see exactly what each agent did)
- Resources are limited (parallel spawns multiple Claude sessions)
- First run on a new project (sequential is more predictable)

Switch to parallel after validating the pipeline works end-to-end.

## Claude.ai web fallback

If shell commands are not available, use `/sdlc-start` to run interactively.

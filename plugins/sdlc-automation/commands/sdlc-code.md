---
allowed-tools: Read, Write, Edit, Bash
description: "Code Generation Agent — Generate production-ready code scaffolding for the full tech stack"
---

# Code Generation Agent (Agent 07)

**Role:** Senior Developer
**Output:** `outputs/code/code_output.json`

**Expected inputs:**
- `outputs/architecture/system_design.json`

!`SDLC_HELPERS=$(python3 -c "import pathlib; paths=[pathlib.Path('helpers'), *pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/helpers')]; print(next((str(p) for p in paths if (p/'harness.py').exists()), 'helpers'))" 2>/dev/null); python3 $SDLC_HELPERS/harness.py pre code_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/07_code_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/code/code_output.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/07_code_agent.md` using the Read tool and follow all instructions.

---
allowed-tools: Read, Write, Edit, Bash
description: "Architecture Agent — Design system architecture, API contracts, DB schema, HLD"
---

# Architecture Agent (Agent 06)

**Role:** Solution Architect
**Output:** `outputs/architecture/system_design.json`

**Expected inputs:**
- `outputs/jira/jira_tickets.json`
- `outputs/requirements/requirement_spec.json`

!`python3 helpers/harness.py pre architecture_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/06_architecture_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/architecture/system_design.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/06_architecture_agent.md` using the Read tool and follow all instructions.

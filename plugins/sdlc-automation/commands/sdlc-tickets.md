---
allowed-tools: Read, Write, Edit, Bash
description: "Ticketing Agent — Create Epic → Story → Task hierarchy (Jira / GitHub Issues / file-based)"
---

# Ticketing Agent (Agent 05)

**Role:** Scrum Master
**Output:** `outputs/jira/jira_tickets.json`

**Expected inputs:**
- `outputs/planning/sprint_plan.json`
- `outputs/requirements/requirement_spec.json`

!`python3 helpers/harness.py pre jira_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/05_jira_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/jira/jira_tickets.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/05_jira_agent.md` using the Read tool and follow all instructions.

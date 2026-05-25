---
allowed-tools: Read, Write, Edit, Bash
description: "Environment Setup Agent — Scan tools, set up environment, create environment_report.json"
---

# Environment Setup Agent (Agent 00)

**Role:** System Scanner
**Output:** `outputs/environment_report.json`

Read the agent instructions and execute them:

@agents/00_environment_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/environment_report.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/00_environment_agent.md` using the Read tool and follow all instructions.

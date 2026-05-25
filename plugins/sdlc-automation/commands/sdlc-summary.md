---
allowed-tools: Read, Write, Edit, Bash
description: "Summary Agent — Executive dashboard, full project summary, artifact inventory"
---

# Summary Agent (Agent 10)

**Role:** Delivery Lead
**Output:** `outputs/pipeline_final.json`

**Expected inputs:**
- `outputs/deployment/deployment_output.json`

!`python3 helpers/harness.py pre summary_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/10_summary_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/pipeline_final.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/10_summary_agent.md` using the Read tool and follow all instructions.

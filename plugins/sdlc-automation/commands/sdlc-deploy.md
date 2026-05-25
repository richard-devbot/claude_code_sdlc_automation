---
allowed-tools: Read, Write, Edit, Bash
description: "Deployment Agent — Generate Dockerfiles, CI/CD pipelines, IaC templates, optional live deploy"
---

# Deployment Agent (Agent 09)

**Role:** DevOps Engineer
**Output:** `outputs/deployment/deployment_output.json`

**Expected inputs:**
- `outputs/qa/qa_results.json`
- `outputs/architecture/system_design.json`

!`python3 helpers/harness.py pre deployment_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/09_deployment_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/deployment/deployment_output.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/09_deployment_agent.md` using the Read tool and follow all instructions.

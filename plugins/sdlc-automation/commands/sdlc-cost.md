---
allowed-tools: Read, Write, Edit, Bash
description: "Cost Estimation Agent — Cloud cost forecast (AWS/Azure/GCP) with Excel/PDF output for stakeholders"
---

# Cost Estimation Agent (Agent 14) *(optional)*

**Role:** FinOps Architect
**Output:** `outputs/cost/cost_estimation.json`

**Expected inputs:**
- `outputs/architecture/system_design.json`

!`python3 helpers/harness.py pre cost_estimation_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/14_cost_estimation_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/cost/cost_estimation.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/14_cost_estimation_agent.md` using the Read tool and follow all instructions.

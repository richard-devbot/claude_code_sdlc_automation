---
allowed-tools: Read, Write, Edit, Bash
description: "Feedback Loop Agent — Cross-pipeline consistency review, traceability matrix, remediation plan"
---

# Feedback Loop Agent (Agent 11) *(optional)*

**Role:** QA Auditor
**Output:** `outputs/feedback/consistency_report.json`

**Expected inputs:**
- `outputs/pipeline_final.json`

!`python3 helpers/harness.py pre feedback_loop_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/11_feedback_loop_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/feedback/consistency_report.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/11_feedback_loop_agent.md` using the Read tool and follow all instructions.

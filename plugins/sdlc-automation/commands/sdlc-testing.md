---
allowed-tools: Read, Write, Edit, Bash
description: "Testing Agent — Generate test plan, test cases, API tests, security checklist + auto-fix loop"
---

# Testing Agent (Agent 08)

**Role:** QA Lead
**Output:** `outputs/qa/qa_results.json`

**Expected inputs:**
- `outputs/code/code_output.json`

!`python3 helpers/harness.py pre testing_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/08_testing_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/qa/qa_results.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/08_testing_agent.md` using the Read tool and follow all instructions.

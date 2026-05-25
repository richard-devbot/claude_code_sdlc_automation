---
allowed-tools: Read, Write, Edit, Bash
description: "Requirements Agent — Extract functional + non-functional requirements with traceability IDs"
---

# Requirements Agent (Agent 02)

**Role:** Senior Business Analyst
**Output:** `outputs/requirements/requirement_spec.json`

**Expected inputs:**
- `outputs/transcripts/structured_meeting_output.json`

!`python3 helpers/harness.py pre requirement_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/02_requirement_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/requirements/requirement_spec.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/02_requirement_agent.md` using the Read tool and follow all instructions.

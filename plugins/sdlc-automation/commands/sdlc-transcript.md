---
allowed-tools: Read, Write, Edit, Bash
description: "Transcript Agent — Parse meeting transcript → structured JSON with domain, features, pain points"
---

# Transcript Agent (Agent 01)

**Role:** Business Analyst
**Output:** `outputs/transcripts/structured_meeting_output.json`

**Expected inputs:**
- `inputs/transcript.txt`

!`python3 helpers/harness.py pre transcript_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/01_transcript_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/transcripts/structured_meeting_output.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/01_transcript_agent.md` using the Read tool and follow all instructions.

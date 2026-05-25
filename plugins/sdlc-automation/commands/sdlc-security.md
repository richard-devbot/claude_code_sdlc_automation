---
allowed-tools: Read, Write, Edit, Bash
description: "Security Threat Model Agent — STRIDE threat model + OWASP Top 10 analysis before code is written"
---

# Security Threat Model Agent (Agent 12) *(optional)*

**Role:** Security Engineer
**Output:** `outputs/security/threat_model.json`

**Expected inputs:**
- `outputs/architecture/system_design.json`

!`python3 helpers/harness.py pre security_threat_model_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/12_security_threat_model_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/security/threat_model.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/12_security_threat_model_agent.md` using the Read tool and follow all instructions.

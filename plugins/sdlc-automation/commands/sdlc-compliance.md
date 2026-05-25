---
allowed-tools: Read, Write, Edit, Bash
description: "Compliance Checker Agent — HIPAA / GDPR / PCI-DSS / SOC 2 gap analysis against pipeline artifacts"
---

# Compliance Checker Agent (Agent 13) *(optional)*

**Role:** Compliance Engineer
**Output:** `outputs/compliance/compliance_matrix.json`

**Expected inputs:**
- `outputs/requirements/requirement_spec.json`
- `outputs/architecture/system_design.json`

!`SDLC_HELPERS=$(python3 -c "import pathlib; paths=[pathlib.Path('helpers'), *pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/helpers')]; print(next((str(p) for p in paths if (p/'harness.py').exists()), 'helpers'))" 2>/dev/null); python3 $SDLC_HELPERS/harness.py pre compliance_checker_agent 2>&1 || echo '[harness] input check skipped'`

Read the agent instructions and execute them:

@agents/13_compliance_checker_agent.md

> **Isolated mode:** Write your output JSON contract to `outputs/compliance/compliance_matrix.json` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/13_compliance_checker_agent.md` using the Read tool and follow all instructions.

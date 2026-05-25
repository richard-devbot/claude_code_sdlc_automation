---
allowed-tools: Bash, Read, Write, Edit
description: "Run a single SDLC agent in isolation with a fresh context window"
argument-hint: <agent-name-or-number>
---

# SDLC — Run Single Agent

Runs exactly one agent in isolation as a fresh `claude -p` subprocess.
The agent reads its inputs from disk, does its work, writes its JSON contract,
and exits. The pipeline does not continue automatically.

!`python3 -c "import pathlib,subprocess,sys; paths=[pathlib.Path('scripts/orchestrator.py'), *pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/scripts/orchestrator.py')]; orch=next((p for p in paths if p.exists()),None); subprocess.run(['python3',str(orch),'--mode','single','--agent','$ARGUMENTS']) if orch else print('Run /sdlc-setup first')"`

---

## Examples

```
/sdlc-agent architecture_agent
/sdlc-agent 06_architecture_agent
/sdlc-agent security_threat_model_agent
```

## Use cases

- Re-run a single failed agent without running the whole pipeline
- Test a new agent version in isolation
- Run optional agents (cost estimation, compliance) on demand

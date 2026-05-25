---
allowed-tools: Bash, Read
description: "Show current SDLC pipeline status — which agents completed, which are pending"
---

# SDLC Pipeline — Status

!`python3 -c "import pathlib, subprocess, sys; paths = [pathlib.Path('scripts/orchestrator.py'), *pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/scripts/orchestrator.py')]; orch = next((p for p in paths if p.exists()), None); (subprocess.run(['python3', str(orch), '--status']) if orch else print('Run /sdlc-setup first to install helpers and scripts.'))"`

## Legend

- `[OK]` — Agent completed and output contract is valid
- `[  ]` — Agent has not run yet (or contract is missing/invalid)

## Detailed status

!`python3 -c "import pathlib,subprocess,sys; paths=[pathlib.Path('helpers/pipeline_status.py'), *pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/helpers/pipeline_status.py')]; p=next((x for x in paths if x.exists()),None); subprocess.run(['python3',str(p)]) if p else print('Run /sdlc-setup first')"`

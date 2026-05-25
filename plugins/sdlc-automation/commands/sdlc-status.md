---
allowed-tools: Bash, Read
description: "Show current SDLC pipeline status — which agents completed, which are pending"
---

# SDLC Pipeline — Status

!`python3 scripts/orchestrator.py --status`

---

## Legend

- `[OK]` — Agent completed and output contract is valid
- `[  ]` — Agent has not run yet (or contract is missing/invalid)

## Check status without shell

Read these files to assess pipeline progress:

!`python3 helpers/pipeline_status.py`

Run the analytics report:

!`python3 helpers/pipeline_analytics.py 2>/dev/null || echo "Run pipeline first to generate analytics"`

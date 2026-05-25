---
allowed-tools: Bash
description: "Clean all pipeline outputs for a fresh run"
---

# SDLC — Clean Outputs

Remove all generated pipeline outputs to start fresh.
Your input transcript (`inputs/transcript.txt`) is preserved.

!`bash scripts/clean_outputs.sh`

> **Warning:** This deletes all outputs. Run `/sdlc-status` first to confirm
> you want to discard the current pipeline run.

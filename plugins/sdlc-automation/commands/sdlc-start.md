---
allowed-tools: Read, Write, Edit, Bash
description: "Start the full SDLC pipeline — interactive mode (agents chain autonomously)"
argument-hint: [--express | --replay]
---

# Start SDLC Automation Pipeline

Place your client meeting transcript in `inputs/transcript.txt`, then start:

!`bash scripts/run_pipeline.sh`

---

## Manual start (Claude.ai web or Claude Code interactive)

Read `.claude/agents/00_environment_agent.md` and execute it.
The environment agent will scan available tools and autonomously trigger all
subsequent agents (01 → 14) via JSON contract handoffs.

**Pipeline execution order:**
1. `00` Environment Setup → `01` Transcript → `02` Requirements → `03` Documentation
2. `04` Planning ∥ `03` (parallel)
3. `05` Tickets ∥ `06` Architecture (parallel)
4. `12` Security Threat Model *(optional, shift-left)*
5. `07` Code Generation
6. `08` Testing ∥ `13` Compliance (parallel)
7. `09` Deployment → `10` Summary → `14` Cost *(optional)* → `11` Feedback *(optional)*

**Execution mode options:**
- **Interactive** (default): Claude pauses at tool/platform choices and asks you
- **Express**: `"Run in express mode"` — uses recommended defaults, no pauses
- **Replay**: Provide `user_preferences.json` — all decisions pre-loaded

> Tip: run `/sdlc-status` at any time to check which agents have completed.

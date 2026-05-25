# Isolated Mode — Orchestrator-Managed Execution

When the orchestrator spawns you as a subprocess (`claude -p`), you are running
in **isolated mode**. Each agent gets a fresh context window. JSON contracts on
disk are the only communication channel between agents.

## Rules for Isolated Mode

1. **Do NOT invoke the Task tool** to trigger the next agent.
   The orchestrator (`scripts/orchestrator.py`) manages sequencing based on the
   DAG defined in `sdlc-pipeline.yml`. Calling Task would start a new session
   that the orchestrator cannot track.

2. **Read all inputs from disk.** Your input contracts are already written by
   prior agents. Use the `Read` tool to load them.

3. **Complete all your tasks** as specified in your agent prompt.

4. **Write your output JSON contract** to the correct path.

5. **Stop cleanly** after writing the contract. The orchestrator polls for your
   output file and will proceed to the next phase once it detects it.

## How the Orchestrator Detects Completion

The orchestrator polls for your output file every 15 seconds.
A contract is considered complete when:
- The file exists at the expected path
- It is valid JSON
- `produced_by` matches your agent ID exactly

## Context Window in Isolated Mode

You have a fresh, full context window. You do NOT need to worry about
prior agents' conversation history — everything you need is in the JSON
contracts on disk. Read only what you need.

## Parallel Execution

Some phases run multiple agents concurrently. If you are running in parallel:
- You own specific files in `outputs/` — do NOT write to another agent's paths
- Your sibling agents are running simultaneously in separate processes
- The orchestrator waits for ALL agents in a phase before starting the next

## Signaling Completion (summary + feedback agents only)

The final agent (summary_agent or feedback_loop_agent) should set:
```json
"pipeline_complete": true
```
in its output contract. This signals the orchestrator that the full pipeline
has finished.

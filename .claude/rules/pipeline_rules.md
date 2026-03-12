# Pipeline Rules

## Core Rules

1. **Sequential Execution**: Agents execute in order 01 → 10. No skipping.
2. **JSON Contracts Only**: Agents communicate ONLY through structured JSON files.
3. **No Central Orchestrator**: Each agent triggers the next directly (peer-to-peer).
4. **Domain Agnostic**: Agent prompts are generic. Domain intelligence flows from
   the transcript through JSON contracts.
5. **Autonomous Pipeline**: Once started, the pipeline runs without human intervention.
6. **Idempotent Outputs**: Re-running an agent overwrites its previous output.

## File Conventions

- Agent definitions: `.claude/agents/NN_agent_name.md`
- Contract schemas: `contracts/agent_output.schema.json`
- Input data: `inputs/`
- Generated artifacts: `outputs/<agent_category>/`
- Helper utilities: `helpers/`
- CLI scripts: `scripts/`

## Agent Naming Convention
- File: `NN_descriptive_name_agent.md` (NN = 01-10, zero-padded)
- Identifier in JSON: `descriptive_name_agent` (snake_case)

## Output Directory Structure
```
outputs/
├── transcripts/     ← Agent 01
├── requirements/    ← Agent 02
├── documents/       ← Agent 03
├── planning/        ← Agent 04
├── jira/            ← Agent 05
├── architecture/    ← Agent 06
├── code/            ← Agent 07
├── qa/              ← Agent 08
├── deployment/      ← Agent 09
└── (root)           ← Agent 10 (final summary)
```

## Quality Gates
- Every agent must write valid JSON matching its schema
- Every agent must create all files specified in its prompt
- Every agent (except the last) must trigger the next agent
- The final agent must set `pipeline_complete: true`

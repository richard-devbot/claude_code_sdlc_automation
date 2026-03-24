# Pipeline Rules

## Core Rules

1. **Sequential Execution**: Agents execute in order 01 → 10. No skipping.
2. **JSON Contracts Only**: Agents communicate ONLY through structured JSON files.
3. **No Central Orchestrator**: Each agent triggers the next directly (peer-to-peer).
4. **Domain Agnostic**: Agent prompts are generic. Domain intelligence flows from
   the transcript through JSON contracts.
5. **Interactive Decision Mode**: When an agent encounters a tool dependency or
   implementation choice, it MUST present all feasible options to the user and
   wait for confirmation before proceeding. See Interactive Decision Protocol below.
6. **Idempotent Outputs**: Re-running an agent overwrites its previous output.

## Interactive Decision Protocol

When an agent reaches a step that has multiple implementation approaches (e.g.,
Jira vs file-based tickets, Docker vs manual scripts, real DB vs SQLite):

1. **Detect** all available options (tools installed, credentials present, free alternatives)
2. **Present** a numbered list of ALL feasible options to the user, with:
   - Option name and brief description
   - Prerequisites (what's needed — credentials, tool install, etc.)
   - Pros and cons
   - Whether the tool can be auto-installed right now
   - A recommended option (marked with ★)
3. **Wait** for the user to choose an option number
4. **Execute** the chosen path — which may include:
   - Downloading/installing a tool
   - Asking the user for credentials or configuration
   - Using a web-based tool via browser automation
   - Falling back to file-based approach
5. **Record** the user's choice in the output contract under `user_preferences`
   so downstream agents respect the same decisions

### When to Present Options (Decision Points)
- **Agent 00**: Tool installation choices, integration setup
- **Agent 05**: Ticketing platform choice (Jira / GitHub Issues / Azure DevOps / Linear / File-based)
- **Agent 06**: Tech stack confirmation (backend framework, database, cloud provider)
- **Agent 07**: Code scaffolding tool choices (npm init, git init, DB setup)
- **Agent 09**: Deployment platform choices (Docker, cloud provider, CI/CD platform)

### When NOT to Pause
- If user previously chose an option in an earlier agent → reuse that decision
- If only one option exists → use it without asking
- Pure analysis/generation tasks with no tool dependency → run autonomously

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

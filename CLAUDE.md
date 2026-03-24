# SDLC Automation Platform — Claude Code Agent Pipeline

## Project Purpose
This project automates the entire Software Development Lifecycle (SDLC) using
Claude Code's agent pipeline. Feed in a client meeting transcript (from Teams,
Zoom, or any discovery call) and the pipeline autonomously produces:
requirements, documentation, sprint plans, Jira tickets, architecture,
code scaffolding, test plans, and deployment readiness — for ANY domain.

## CRITICAL: Pipeline Rules
1. Each agent MUST read its input JSON contract from the outputs/ directory
2. Each agent MUST write its output JSON contract to the outputs/ directory
3. Each agent MUST trigger the next agent using the Task tool before completing
4. JSON contracts are the ONLY communication channel between agents
5. Never skip the handoff — always call the next agent
6. Agents are DOMAIN-AGNOSTIC — they handle ANY industry automatically
7. Domain intelligence flows FROM the transcript through JSON contracts
8. **THE PIPELINE NEVER STOPS** — if a tool is missing, use fallback mode
9. Every agent checks `outputs/environment_report.json` for tool availability
10. File-based fallback is ALWAYS available for every external tool dependency
11. **INTERACTIVE DECISIONS** — When an agent has multiple implementation options
    (e.g., Jira vs file-based, Docker vs manual), it MUST present all options to
    the user and wait for confirmation before proceeding
12. User choices are recorded in `user_preferences` in each contract and propagated
    forward — downstream agents reuse prior decisions without re-asking

## Pipeline Execution Modes
- **Interactive Mode** (default): Agents pause at decision points and ask the user
- **Express Mode**: Say "run in express mode" — uses recommended defaults, only pauses if unavailable
- **Replay Mode**: Provide `user_preferences.json` — all decisions pre-loaded, no pauses

## How to Start the Pipeline
Place your meeting transcript in `inputs/transcript.txt`, then prompt:
```
Start the SDLC automation pipeline.
Read .claude/agents/00_environment_agent.md and execute it.
It will scan the system, set up tools, and autonomously trigger all agents.
```

Or skip environment setup and start directly:
```
Start the SDLC automation pipeline.
Read .claude/agents/01_transcript_agent.md and execute it.
The agent will autonomously trigger all subsequent agents.
```

## Agent Execution Order (11 Agents)
```
00_environment_agent (setup) → 01_transcript_agent → 02_requirement_agent
→ 03_documentation_agent → 04_planning_agent → 05_jira_agent
→ 06_architecture_agent → 07_code_agent → 08_testing_agent
→ 09_deployment_agent → 10_summary_agent
```

## Tool Fallback Strategy (Pipeline NEVER Stops)
| Tool Missing | Fallback | Impact |
|-------------|----------|--------|
| Jira/ServiceNow | File-based tickets (JSON + CSV) | Zero — import later |
| Git/GitHub | Generate code as local files | Zero — git init later |
| Docker | Generate Dockerfiles + manual scripts | Zero — run with Docker later |
| PostgreSQL | Default to SQLite | Minimal — swap DB config later |
| Node.js | Generate code files | Zero — install Node to run |
| Slack | Skip notifications | Zero — configure later |

## Directory Structure
```
sdlc-automation/
├── .claude/
│   ├── agents/                   ← 11 agent prompt definitions
│   │   ├── 00_environment_agent.md
│   │   ├── 01_transcript_agent.md
│   │   ├── 02_requirement_agent.md
│   │   ├── 03_documentation_agent.md
│   │   ├── 04_planning_agent.md
│   │   ├── 05_jira_agent.md
│   │   ├── 06_architecture_agent.md
│   │   ├── 07_code_agent.md
│   │   ├── 08_testing_agent.md
│   │   ├── 09_deployment_agent.md
│   │   ├── 10_summary_agent.md
│   │   └── _COMMUNICATION_PROTOCOL.md
│   ├── skills/                   ← SDLC domain knowledge
│   │   ├── sdlc-process/         ← Methodology skills
│   │   ├── pipeline/             ← Pipeline mechanics
│   │   └── domain-adaptation/    ← Multi-domain rules
│   ├── hooks/                    ← Quality gate hooks
│   │   ├── post_agent_contract_validator.py
│   │   └── pre_handoff_checker.py
│   ├── rules/
│   │   └── pipeline_rules.md
│   └── settings.json
├── contracts/                    ← JSON schema definitions
├── helpers/                      ← Python utility modules
├── scripts/                      ← CLI scripts
├── inputs/                       ← Client transcript (pipeline input)
│   └── transcript.txt
├── outputs/                      ← All generated artifacts
│   ├── transcripts/
│   ├── requirements/
│   ├── documents/
│   ├── planning/
│   ├── jira/
│   ├── architecture/
│   ├── code/
│   ├── qa/
│   └── deployment/
├── CLAUDE.md                     ← This file
└── README.md
```

## Input Required
Before starting, ensure `inputs/transcript.txt` exists with the client meeting
transcript or discovery call notes. The pipeline reads this as its starting point.

## Resuming the Pipeline
If the pipeline stops at any agent, resume with:
```
Resume the SDLC pipeline from [agent_name].
Read outputs/[previous_output].json and execute .claude/agents/[NN_agent_name].md
```

## Running Helpers
```bash
python helpers/pipeline_status.py       # Check pipeline progress
python helpers/contract_validator.py    # Validate all output contracts
python helpers/output_reporter.py       # Generate output report
bash scripts/clean_outputs.sh           # Clean outputs for fresh run
```

## Domain-Agnostic Design
All agent prompts are written generically. Domain-specific intelligence flows
FROM the meeting transcript through the JSON contracts. Agents auto-detect
and adapt to whatever domain the client discusses.

## Supported Domains
Healthcare, E-Commerce, Fintech, Education, HR Tech, Logistics, SaaS,
Government, Real Estate, Manufacturing, Legal, Media/Entertainment,
Travel/Hospitality, Agriculture, and more.

## SDLC Phases Mapped to Agents
| Phase | Agent(s) | Role |
|-------|----------|------|
| Pre-Sales & Discovery | 01 Transcript | Business Analyst |
| Requirements Engineering | 02 Requirement | Senior BA |
| Documentation & SOW | 03 Documentation | Technical Writer |
| Sprint Planning | 04 Planning | Project Manager |
| Ticket Creation | 05 Jira | Scrum Master |
| Solution Architecture | 06 Architecture | Solution Architect |
| Code Scaffolding | 07 Code | Senior Developer |
| QA & Testing | 08 Testing | QA Lead |
| Deployment Readiness | 09 Deployment | DevOps Engineer |
| Final Summary | 10 Summary | Delivery Lead |

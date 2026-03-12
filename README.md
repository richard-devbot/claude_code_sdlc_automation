# SDLC Automation Platform — Claude Code

Automates the entire Software Development Lifecycle using Claude Code's agent
pipeline. Feed in a client meeting transcript, get out requirements, documents,
sprint plans, tickets, architecture, code, tests, and deployment configs.

## Quick Start

1. Place your meeting transcript in `inputs/transcript.txt`
2. Open Claude Code in the `sdlc-automation/` directory
3. Prompt:
   ```
   Start the SDLC automation pipeline.
   Read .claude/agents/01_transcript_agent.md and execute it.
   The agent will autonomously trigger all subsequent agents.
   ```

## Pipeline (10 Agents)

| # | Agent | Role | Output |
|---|-------|------|--------|
| 01 | Transcript | Business Analyst | Structured meeting JSON |
| 02 | Requirement | Senior BA | FR/NFR specifications |
| 03 | Documentation | Technical Writer | BRD, FRD, SOW |
| 04 | Planning | Project Manager | Sprint plan |
| 05 | Jira | Scrum Master | Epics, Stories, Tasks |
| 06 | Architecture | Solution Architect | Tech stack, DB, APIs |
| 07 | Code | Senior Developer | Backend + Frontend scaffold |
| 08 | Testing | QA Lead | Test plans, security checklists |
| 09 | Deployment | DevOps Engineer | Docker, CI/CD, production checklist |
| 10 | Summary | Delivery Lead | Final project summary |

## Prerequisites

- Claude Code CLI with valid API key
- Python 3.7+ (for helper utilities)

## Supported Domains

Any industry — auto-detected from transcript:
Healthcare, E-Commerce, Fintech, Education, HR Tech, Logistics, SaaS,
Government, Real Estate, Manufacturing, Legal, Media, Travel, and more.

## Utilities

```bash
python helpers/pipeline_status.py       # Check pipeline progress
python helpers/contract_validator.py    # Validate output contracts
python helpers/output_reporter.py       # Generate output report
bash scripts/clean_outputs.sh           # Reset for fresh run
bash scripts/run_pipeline.sh            # Pre-flight check
```

## Two Execution Modes

### Mode 1: Sequential Pipeline (Default)
Agents run one after another in a chain. Simpler, lower token cost.

### Mode 2: Agent Teams (Parallel)
Uses Claude Code's **Agent Teams** feature. Multiple teammates run in parallel
where possible. Faster but uses more tokens.
See `.claude/agents/AGENT_TEAMS_MODE.md` for setup.

## Installed Skills (All 18 from skills.sh)

- **frontend-design** — Production-grade UI design
- **pdf** — PDF generation and processing
- **docx** — Word document generation
- **xlsx** — Spreadsheet generation
- **pptx** — Presentation generation
- **webapp-testing** — Web application testing with Playwright
- **mcp-builder** — MCP server building
- **skill-creator** — Custom skill creation
- **doc-coauthoring** — Documentation co-authoring
- **internal-comms** — Internal communications
- **web-artifacts-builder** — Web artifact building
- **canvas-design** — Canvas-based visual design
- **brand-guidelines** — Brand guideline creation
- **algorithmic-art** — Generative art creation
- **template-skill** — Skill template for custom skills
- **slack-gif-creator** — Slack GIF creation
- **theme-factory** — Theme/design system creation
- **claude-api** — Claude API integration

## Sample Use Cases (5 Included)

| File | Domain | Client |
|------|--------|--------|
| `inputs/transcript.txt` | SaaS/Agency | TechNova Solutions (default) |
| `inputs/samples/healthcare_transcript.txt` | Healthcare | MedCare Hospital |
| `inputs/samples/ecommerce_transcript.txt` | E-Commerce | UrbanBazaar Marketplace |
| `inputs/samples/fintech_transcript.txt` | Fintech | PayWise Financial |
| `inputs/samples/education_transcript.txt` | Education | BrightPath Academy |
| `inputs/samples/saas_transcript.txt` | SaaS/B2B | CloudMetrics Inc |

## Documentation

| File | What It Covers |
|------|---------------|
| `CLAUDE.md` | Project structure and pipeline rules |
| `USAGE_GUIDE.md` | Complete usage guide with all examples |
| `SDLC_TERMINOLOGY_GUIDE.md` | Full SDLC terminology and how IT companies work |
| `.claude/agents/AGENT_TEAMS_MODE.md` | Agent Teams parallel execution guide |

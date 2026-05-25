# SDLC Automation Platform — AI-Powered Software Development Lifecycle

> Drop a meeting transcript in. Get requirements, documentation, sprint plans, tickets, architecture, code, tests, and deployment configs out. For ANY industry domain.

![Pipeline](https://img.shields.io/badge/Pipeline-15_Agents-blue)
![Skills](https://img.shields.io/badge/Skills-93_Imported-green)
![Specialists](https://img.shields.io/badge/Specialist_Agents-42-orange)
![Hooks](https://img.shields.io/badge/Quality_Hooks-26-red)
![Commands](https://img.shields.io/badge/Commands-44-purple)
![Domains](https://img.shields.io/badge/Domains-13+-teal)
![Version](https://img.shields.io/badge/Version-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Install (1 command)

```bash
claude plugin marketplace add richard-devbot/claude_code_sdlc_automation && \
claude plugin install sdlc-automation@claude_code_sdlc_automation
```

Restart Claude Code. Type `/sdlc` — all 22 pipeline commands appear.

---

## Quick Start (3 steps)

**Step 1 — Add your transcript**

```bash
cp your_meeting_notes.txt inputs/transcript.txt
# No transcript yet? Use a sample:
cp inputs/samples/healthcare_transcript.txt inputs/transcript.txt
```

**Step 2 — Start the pipeline**

```
/sdlc-start
```

Or choose an execution mode:

| Command | Mode | Best for |
|---------|------|---------|
| `/sdlc-start` | Interactive | First run, full control over decisions |
| `/sdlc-parallel` | Parallel DAG | Speed — each agent gets a fresh 200K context window |
| `/sdlc-sequential` | Sequential | Debugging — one agent at a time |

**Step 3 — Review your deliverables**

```
outputs/PROJECT_COMPLETE_SUMMARY.md   ← full project summary
outputs/EXECUTIVE_DASHBOARD.md        ← one-page stakeholder view
```

---

## Overview

The SDLC Automation Platform is an end-to-end software development lifecycle engine built on Claude Code's agent pipeline. It takes a raw client meeting transcript — from a Zoom call, a Teams recording, or handwritten discovery notes — and autonomously produces every deliverable a development team needs: structured requirements, BRD/FRD/SOW documentation, sprint plans, Jira-ready tickets, system architecture, code scaffolding, test plans, deployment configurations, cost estimates, security threat models, and compliance matrices. The entire pipeline is orchestrated through a chain of 15 AI agents that communicate via structured JSON contracts, with a DAG-based execution model that runs independent phases in parallel. It works for any industry domain — healthcare, fintech, e-commerce, education, government, and more — with automatic domain detection and compliance-aware generation.

---

## Architecture

### Pipeline Flow (DAG-Based Parallel Execution)

```
                               +---------------------+
                               |  Meeting Transcript  |
                               +----------+----------+
                                          |
                          +---------------+---------------+
                          |                               |
                   +------v------+                 +------v------+
                   | 00 Environ- |                 | 01 Tran-    |
                   |    ment     |                 |   script    |
                   +------+------+                 +------+------+
                          |                               |
                          +---------------+---------------+
                                          |
                                   +------v------+
                                   | 02 Require- |
                                   |    ment     |
                                   +------+------+
                                          |
                          +---------------+---------------+
                          |                               |
                   +------v------+                 +------v------+
                   | 03 Documen- |                 | 04 Planning |
                   |   tation    |                 |             |
                   +------+------+                 +------+------+
                          |                               |
                          +---------------+---------------+
                                          |
                          +---------------+---------------+
                          |                               |
                   +------v------+                 +------v------+
                   | 05 Jira /   |                 | 06 Architec-|
                   |   Tickets   |                 |    ture     |
                   +------+------+                 +------+------+
                          |                               |
                          |                        +------v------+
                          |                        | 12 Security | (optional)
                          |                        | Threat Model|
                          |                        +------+------+
                          |                               |
                          +---------------+---------------+
                                          |
                                   +------v------+
                                   | 07 Code     |
                                   |  Generation |
                                   +------+------+
                                          |
                          +---------------+---------------+
                          |                               |
                   +------v------+                 +------v------+
                   | 08 Testing  |                 | 13 Compli-  | (optional)
                   |             |                 |  ance Check |
                   +------+------+                 +------+------+
                          |                               |
                          +---------------+---------------+
                                          |
                                   +------v------+
                                   | 09 Deploy-  |
                                   |    ment     |
                                   +------+------+
                                          |
                          +------+--------+--------+------+
                          |               |               |
                   +------v------+ +------v------+ +------v------+
                   | 10 Summary  | | 14 Cost     | | 11 Feedback |
                   |             | | Estimation  | |    Loop     |
                   +-------------+ +-------------+ +-------------+
                                          |
                                   +------v------+
                                   |  Complete   |
                                   | Deliverables|
                                   +-------------+
```

### Parallel Phase Groups

Defined in `sdlc-pipeline.yml`, the DAG determines which agents can run concurrently:

| Phase | Agents Running in Parallel | Depends On |
|-------|---------------------------|------------|
| Phase 1 — Analysis | `00_environment` + `01_transcript` | — |
| Phase 2 — Requirements | `02_requirement` | Phase 1 |
| Phase 3 — Documentation | `03_documentation` + `04_planning` | Phase 2 |
| Phase 4 — Design | `05_jira` + `06_architecture` | Phase 3 |
| Phase 5 — Security | `12_security_threat_model` (optional) | Phase 4 |
| Phase 6 — Implementation | `07_code` | Phase 4 + Phase 5 |
| Phase 7 — Quality | `08_testing` + `13_compliance_checker` (optional) | Phase 6 |
| Phase 8 — Deployment | `09_deployment` | Phase 7 |
| Phase 9 — Delivery | `10_summary` then `14_cost_estimation` then `11_feedback_loop` | Phase 8 |

---

## Agent Inventory

All 15 agents in the pipeline (00-14):

| # | Agent Name | Role | Input | Output | Optional? |
|---|------------|------|-------|--------|-----------|
| 00 | Environment Setup | System Scanner | System scan | `outputs/environment_report.json` | No |
| 01 | Transcript Parser | Business Analyst | `inputs/transcript.txt` | `outputs/transcripts/structured_meeting_output.json` | No |
| 02 | Requirement Spec | Senior BA | Transcript output | `outputs/requirements/requirement_spec.json` | No |
| 03 | Documentation | Technical Writer | Requirement spec | `outputs/documents/documentation_output.json` + BRD/FRD/SOW | No |
| 04 | Sprint Planning | Project Manager | Docs + Requirements | `outputs/planning/sprint_plan.json` | No |
| 05 | Ticket Creation | Scrum Master | Sprint plan + Requirements | `outputs/jira/jira_tickets.json` + CSV + Markdown | No |
| 06 | Architecture | Solution Architect | Tickets + Requirements | `outputs/architecture/system_design.json` + HLD.md | No |
| 07 | Code Generation | Senior Developer | System design + HLD | `outputs/code/` (backend + frontend scaffold) | No |
| 08 | Testing and QA | QA Lead | Code + Tickets + Requirements | `outputs/qa/qa_results.json` | No |
| 09 | Deployment | DevOps Engineer | QA + Architecture + Code | `outputs/deployment/` (Docker, CI/CD, scripts) | No |
| 10 | Project Summary | Delivery Lead | ALL contracts | `outputs/pipeline_final.json` + dashboards | No |
| 11 | Feedback Loop | QA Auditor | ALL contracts | `outputs/feedback/consistency_report.json` | Yes |
| 12 | Security Threat Model | AppSec Engineer | Architecture + Requirements | `outputs/security/threat_model.json` | Yes |
| 13 | Compliance Checker | Compliance Engineer | All artifacts | `outputs/compliance/compliance_matrix.json` | Yes |
| 14 | Cost Estimation | FinOps Engineer | Architecture + Planning | `outputs/cost/cost_estimate.json` | Yes |

---

## Pipeline Communication

### JSON Contract Chain

Every agent communicates through structured JSON contracts written to the `outputs/` directory. In interactive mode each agent reads its predecessor's output, performs its work, writes its own output, and triggers the next agent via the Task tool. In orchestrator mode (`/sdlc-parallel`, `/sdlc-sequential`) the orchestrator manages sequencing externally and each agent runs as an isolated subprocess.

```
Interactive mode:
  Agent A  →  writes outputs/N.json
           →  calls Task tool to invoke Agent B
               Agent B reads outputs/N.json
               Agent B writes outputs/N+1.json
               Agent B calls Task tool to invoke Agent C
               ... continues until final agent

Orchestrator mode (parallel / sequential):
  Orchestrator reads sdlc-pipeline.yml DAG
  → spawns each agent as `claude -p` subprocess (fresh 200K context window)
  → polls for output contract file
  → starts next phase when all phase contracts are valid
```

### Contract v1.0 Standard Fields

Every JSON contract MUST include these fields:

| Field | Type | Description |
|-------|------|-------------|
| `contract_version` | string | Always `"1.0"` |
| `produced_by` | string | Agent identifier (e.g., `"transcript_agent"`) |
| `timestamp` | string | ISO 8601 timestamp |
| `domain` | string | Auto-detected industry domain, propagated from Agent 01 |
| `next_agent` | string | Name of the next agent to invoke (interactive mode) |
| `next_input_file` | string | Path to this contract file |
| `user_preferences` | object | User choices made during interactive decisions |
| `pipeline_complete` | boolean | Set to `true` by the final agent only |

### Decision Propagation Rules

1. When an agent presents options and receives a user choice, it records the decision in `user_preferences`.
2. Downstream agents MUST check `user_preferences` from ALL previous contracts before presenting redundant options.
3. If a user chose "Jira Cloud" in Agent 05, no downstream agent will re-ask about ticketing — it reuses the decision.
4. Preferences accumulate through the chain, building a complete decision record.

```json
"user_preferences": {
  "ticketing_platform": "jira_cloud",
  "ticketing_credentials_provided": true,
  "database_engine": "postgresql",
  "deployment_platform": "docker_compose",
  "ci_cd_platform": "github_actions",
  "cloud_provider": "aws",
  "install_tools_when_missing": true
}
```

---

## Interactive Decision Framework

### Three Execution Modes

| Mode | Behavior | How to Activate |
|------|----------|-----------------|
| **Interactive** (default) | Agents pause at every decision point and present numbered options with pros/cons and a recommended choice. User picks a number. | `/sdlc-start` or start pipeline normally. |
| **Express** | Uses recommended defaults automatically. Only pauses when the recommended option is unavailable. | Say "run in express mode" when starting. |
| **Replay** | All decisions pre-loaded from `sdlc-pipeline.yml` user_preferences. Zero pauses. | Edit `sdlc-pipeline.yml`, set `mode: "replay"`, and provide all preferences. |

### Decision Points by Agent

| Agent | Decision | Options Presented |
|-------|----------|-------------------|
| 00 Environment | Tool installation | Auto-install / Provide credentials / Skip with fallback |
| 01 Transcript | Input source | Local files / Paste / Zoom / Teams / Google Meet / Otter.ai / Audio |
| 03 Documentation | Publishing platform | Local / Confluence / Notion / SharePoint / PDF |
| 05 Ticketing | Platform choice | Jira Cloud / GitHub Issues / Azure DevOps / Linear / File-based |
| 06 Architecture | Tech stack confirmation | Backend framework, database engine, cloud provider |
| 07 Code | Repository setup | Local git / GitHub repo / GitLab / Azure DevOps / Skip |
| 08 Testing | Test execution | Generate only / Run now / Generate + Run / CI workflow |
| 09 Deployment | Containerization | Docker / Podman / Kubernetes / Manual scripts |
| 09 Deployment | CI/CD platform | GitHub Actions / GitLab CI / Jenkins / Azure Pipelines / All |
| 09 Deployment | Cloud provider | AWS / Azure / GCP / Cloud-agnostic / On-premise |

**When NOT to pause:** If only one option exists, if a prior agent already decided, or if the task is pure analysis with no tool dependency.

---

## Orchestrator (Parallel + Sequential Modes)

`scripts/orchestrator.py` manages agent execution externally so each agent runs in an isolated subprocess with a fresh context window. This prevents context accumulation and compaction mid-pipeline.

```bash
python scripts/orchestrator.py --mode parallel     # agents within a phase run concurrently
python scripts/orchestrator.py --mode sequential   # one agent at a time
python scripts/orchestrator.py --status            # show [OK] / [  ] for all 15 agents
python scripts/orchestrator.py --resume-from code_agent   # skip completed phases
python scripts/orchestrator.py --mode single --agent architecture_agent  # run one agent
```

Or via slash commands (after plugin install):

```
/sdlc-parallel      /sdlc-sequential      /sdlc-status      /sdlc-resume <agent>
```

`helpers/harness.py` wraps each agent invocation with lifecycle hooks:
- `pre_agent()` — validates input contracts exist and are valid JSON before spawning
- `post_agent()` — validates output contract + fires completion notification
- `phase_boundary()` — cross-phase consistency check between phases

`helpers/test_retry_loop.py` manages the self-healing test loop (exit 0 = pass, exit 10 = retry Code Agent up to 3×, exit 20 = escalate to user).

---

## Features

### Core Pipeline
- **Multi-Transcript Merger** — Accept multiple meeting transcripts from different sessions; merge chronologically, resolve contradictions (latest wins), and track sources with priority ranking.
- **Real-Time Transcript Integration** — Import transcripts directly from Zoom, Microsoft Teams, Google Meet, or Otter.ai via API; or transcribe raw audio files. Configured via `input.source` in `sdlc-pipeline.yml`.
- **Parallel Agent Execution (DAG)** — Nine-phase dependency graph allows agents in the same phase to run simultaneously. Documentation and Planning run in parallel; Tickets and Architecture run in parallel.
- **Pipeline-as-Code** — The entire pipeline is version-controlled in `sdlc-pipeline.yml`: agent order, parallel groups, user preferences, quality gates, notification webhooks, analytics toggles.
- **Domain-Agnostic Design** — Auto-detects and adapts to 13+ industry domains from the transcript content. No manual domain configuration required. Compliance rules applied per domain automatically.
- **Graceful Degradation** — The pipeline never stops. Missing tools (Jira, Docker, Git, PostgreSQL, Node.js, Slack) trigger file-based fallbacks with zero data loss. Import into real tools later.
- **Interactive Tool Resolution** — When tools are missing, agents present installation options with pros/cons rather than failing silently.

### Quality and Security
- **Feedback Loop Agent** — Post-pipeline consistency checker that cross-references ALL artifacts for gaps, mismatches, uncovered requirements, missing tests, and capacity overflows.
- **Security Threat Modeling (STRIDE/DREAD)** — STRIDE analysis and DREAD scoring applied to the system architecture. Generates threat matrices, trust boundary maps, and mitigation recommendations that downstream agents must implement. Runs before code is written (shift-left).
- **Compliance Auto-Checker (HIPAA, PCI-DSS, GDPR, SOC2)** — Verifies regulatory framework requirements against all pipeline artifacts. Produces a gap analysis matrix and remediation plan for regulated domains.
- **Self-Healing Test Loop** — If generated tests fail, the pipeline retries the Code Agent automatically with a `failed_tests.json` contract listing failures and suggested fixes. Max 3 retries before escalating to the user.
- **Code Quality Scoring** — Self-analysis for anti-patterns, security vulnerabilities, and input validation gaps. Scores 0-100 with auto-regeneration if below the configured threshold.
- **Dependency Vulnerability Scan** — Runs `npm audit` / `pip audit` on generated dependencies; offers auto-fix or alternative package recommendations.

### Integrations
- **Jira/Azure DevOps Bidirectional Sync** — Detects existing project tickets, offers merge/replace/supplement options; duplicate detection via title similarity. Also supports GitHub Issues and Linear.
- **Confluence/Notion Auto-Publish** — Publish generated BRD, FRD, and SOW directly to Confluence, Notion, or SharePoint. Configurable via `documentation_platform` in pipeline config.
- **GitHub/GitLab Repository Auto-Setup** — Initialize repositories, create branches, set up branch protection, PR templates, and CODEOWNERS files automatically.
- **Slack/Teams Notifications** — Webhook-based status updates at each agent completion, pipeline completion, and error events. Falls back to macOS desktop notification if no webhook is configured.
- **Live Deployment** — After generating Docker configs, optionally run `docker compose up -d` and perform a health check. A `live_staging_url` is written to the deployment contract and surfaced in the executive dashboard.
- **Test Runner Integration** — Actually RUN generated tests against scaffolded code; capture pass/fail/coverage metrics in the QA results contract.

### Analytics and Estimation
- **Pipeline Analytics Dashboard** — Token usage tracking, execution time per agent, and pipeline metrics saved to `outputs/analytics/pipeline_metrics.json`.
- **Cost Estimation Agent** — Cloud infrastructure cost projections across AWS, Azure, and GCP with per-environment breakdowns (development, staging, production).

---

## Directory Structure

```
sdlc-automation/
├── .claude-plugin/
│   └── marketplace.json                     # GitHub marketplace registration (enables 1-line install)
│
├── .claude/
│   ├── agents/                              # 15 pipeline agents + docs
│   │   ├── 00_environment_agent.md          # System scanner and tool checker
│   │   ├── 01_transcript_agent.md           # Business analyst - transcript parsing
│   │   ├── 02_requirement_agent.md          # Senior BA - FR/NFR extraction
│   │   ├── 03_documentation_agent.md        # Technical writer - BRD, FRD, SOW
│   │   ├── 04_planning_agent.md             # Project manager - sprint planning
│   │   ├── 05_jira_agent.md                 # Scrum master - ticket creation
│   │   ├── 06_architecture_agent.md         # Solution architect - system design
│   │   ├── 07_code_agent.md                 # Senior developer - code scaffolding
│   │   ├── 08_testing_agent.md              # QA lead - test plans and execution
│   │   ├── 09_deployment_agent.md           # DevOps engineer - infra and CI/CD
│   │   ├── 10_summary_agent.md              # Delivery lead - final summary
│   │   ├── 11_feedback_loop_agent.md        # QA auditor - consistency checking
│   │   ├── 12_security_threat_model_agent.md   # AppSec - STRIDE/DREAD analysis
│   │   ├── 13_compliance_checker_agent.md      # Compliance - regulatory gap analysis
│   │   ├── 14_cost_estimation_agent.md         # FinOps - cloud cost projections
│   │   ├── _COMMUNICATION_PROTOCOL.md       # JSON contract chain specification
│   │   ├── _ISOLATED_MODE.md                # Rules for orchestrator-spawned agents
│   │   ├── AGENT_TEAMS_MODE.md              # Parallel execution guide
│   │   └── specialists/                     # 42 specialist sub-agents
│   │       ├── project-management/   (7)    # scrum-master, project-manager, ...
│   │       ├── documentation/        (7)    # technical-writer, diagram-architect, ...
│   │       ├── architecture/         (9)    # architect, api-architect, database-architect, ...
│   │       ├── testing/              (6)    # e2e-runner, error-detective, ...
│   │       ├── security/             (5)    # compliance-auditor, security-engineer, ...
│   │       ├── devops/               (3)    # build-engineer, cloud-architect, ...
│   │       └── performance/          (5)    # performance-engineer, monitoring-specialist, ...
│   │
│   ├── skills/                              # 93 imported + 21 existing skill packages
│   │   ├── sdlc-process/                    # Core SDLC methodology knowledge
│   │   ├── pipeline/                        # Agent chain, contract protocol, tool registry
│   │   ├── domain-adaptation/               # Multi-domain compliance rules (13+ domains)
│   │   ├── requirements-planning/    (10)   # Sprint planner, Jira, Scrum, JTBD
│   │   ├── documentation-writing/    (10)   # API docs, Mermaid, README, templates
│   │   ├── architecture-design/      (15)   # API design, backend patterns, DB arch
│   │   ├── code-patterns/            (10)   # Django, FastAPI, Express, Angular
│   │   ├── testing-qa/               (10)   # Coverage analysis, API tests, mocks
│   │   ├── security-compliance/       (9)   # OWASP, auth patterns, fuzzing
│   │   ├── devops-deployment/        (13)   # Ansible, ArgoCD, AWS, Azure
│   │   ├── performance-monitoring/   (12)   # Web Vitals, Datadog, APM dashboards
│   │   ├── automation/                (4)   # Bash scripting, bottleneck detection
│   │   └── [18 pre-installed skills]        # pdf, docx, xlsx, pptx, frontend-design, ...
│   │
│   ├── hooks/                               # Quality gate hooks
│   │   ├── post_agent_contract_validator.py # Validates JSON contracts after agents
│   │   ├── pre_handoff_checker.py           # Checks chain integrity before handoffs
│   │   ├── notification_dispatcher.py       # Slack/Teams/desktop agent-completion alerts
│   │   ├── quality-gates/             (9)   # TDD gate, scope guard, test runner
│   │   ├── devops/                    (7)   # Conventional commits, branch naming
│   │   ├── security/                  (6)   # Secret scanner, dangerous cmd blocker
│   │   └── code-quality/             (2)    # Lint-on-save, smart formatting
│   │
│   ├── commands/                     (22)   # Project-scoped slash commands
│   ├── rules/
│   │   └── pipeline_rules.md                # Core pipeline behavior constraints
│   └── settings.json                        # Hooks wiring, agent teams mode, permissions
│
├── plugins/
│   └── sdlc-automation/                     # Installable plugin (GitHub marketplace source)
│       ├── .claude-plugin/plugin.json        # Plugin manifest
│       ├── commands/                         # 22 /sdlc-* slash commands
│       ├── agents/                           # 15 agent definitions with YAML frontmatter
│       ├── helpers/                          # harness, test_retry_loop, pipeline_status
│       ├── scripts/                          # orchestrator, run_pipeline
│       └── sdlc-pipeline.yml
│
├── contracts/                               # JSON schema definitions for contracts
├── inputs/                                  # Pipeline input (transcripts)
│   ├── transcript.txt                       # Default input transcript
│   └── samples/                             # 5 domain-specific sample transcripts
│       ├── healthcare_transcript.txt
│       ├── ecommerce_transcript.txt
│       ├── fintech_transcript.txt
│       ├── education_transcript.txt
│       └── saas_transcript.txt
├── outputs/                                 # All generated artifacts
│   ├── transcripts/                         # Agent 01 output
│   ├── requirements/                        # Agent 02 output
│   ├── documents/                           # Agent 03 output
│   ├── planning/                            # Agent 04 output
│   ├── jira/                                # Agent 05 output
│   ├── architecture/                        # Agent 06 output
│   ├── code/                                # Agent 07 output
│   ├── qa/                                  # Agent 08 output
│   ├── deployment/                          # Agent 09 output
│   ├── security/                            # Agent 12 output (optional)
│   ├── compliance/                          # Agent 13 output (optional)
│   ├── cost/                                # Agent 14 output (optional)
│   ├── feedback/                            # Agent 11 output
│   └── analytics/                           # Pipeline metrics + notification log
├── helpers/                                 # Python utility modules
│   ├── harness.py                           # Agent lifecycle wrapper (pre/post hooks)
│   ├── test_retry_loop.py                   # Self-healing test-fix loop
│   ├── pipeline_status.py                   # Check pipeline progress
│   ├── contract_validator.py                # Validate JSON contract schemas
│   ├── output_reporter.py                   # Generate output summary report
│   └── pipeline_analytics.py               # Pipeline metrics and analytics
├── scripts/                                 # Shell and Python scripts
│   ├── orchestrator.py                      # DAG runner — parallel + sequential modes
│   ├── build_plugin.py                      # Rebuild sdlc-automation.plugin from sources
│   ├── clean_outputs.sh                     # Reset outputs for a fresh run
│   ├── run_pipeline.sh                      # Mode chooser + pre-flight launcher
│   └── validate_all.sh                      # Validate all contracts in one pass
├── sdlc-automation.plugin                   # Built plugin zip (web + desktop install)
├── sdlc-pipeline.yml                        # Pipeline-as-Code configuration
├── CLAUDE.md                                # Project rules for Claude Code
├── USAGE_GUIDE.md                           # Complete usage guide
└── SDLC_TERMINOLOGY_GUIDE.md              # SDLC terminology reference
```

---

## Quick Start (Manual — no plugin)

### Prerequisites

- Claude Code CLI with a valid API key
- Python 3.7+ (for helper utilities)

### Step 1: Place Your Transcript

Copy your meeting transcript (plain text) into `inputs/transcript.txt`. This can be a discovery call, stakeholder interview, project kickoff, or any client meeting.

```bash
cp your_meeting_notes.txt inputs/transcript.txt
```

For multiple transcripts, add all `.txt` files to `inputs/` — Agent 01 merges them automatically with conflict resolution.

### Step 2: Start the Pipeline

Open Claude Code in the `sdlc-automation/` directory and prompt:

```
Start the SDLC automation pipeline.
Read .claude/agents/00_environment_agent.md and execute it.
It will scan the system, present tool options, and trigger all agents.
```

Or skip environment setup and start directly from transcript parsing:

```
Start the SDLC automation pipeline.
Read .claude/agents/01_transcript_agent.md and execute it.
The agent will autonomously trigger all subsequent agents.
```

### Step 3: Answer Interactive Questions

In Interactive mode (default), agents will pause at decision points and present numbered options:
- Agent 05 asks which ticketing platform to use
- Agent 06 confirms the recommended tech stack
- Agent 09 asks about deployment preferences

Pick a number and the pipeline continues. Your choices propagate forward — no repeat questions.

### Step 4: Collect Your Outputs

When the pipeline completes, all deliverables are in `outputs/`:

```bash
python helpers/pipeline_status.py       # Check what completed
python helpers/output_reporter.py       # Generate summary report
```

### Express Mode (Zero Interaction)

```
Start the SDLC automation pipeline in express mode.
Read .claude/agents/00_environment_agent.md and execute it.
Use all recommended defaults without asking.
```

### Replay Mode (Pre-Configured)

Edit `sdlc-pipeline.yml` with your preferences, then:

```
Run the pipeline using sdlc-pipeline.yml configuration.
```

---

## Pipeline-as-Code

The `sdlc-pipeline.yml` file configures the entire pipeline. It is the single source of truth for reproducible, version-controlled pipeline runs.

| Section | What It Configures |
|---------|--------------------|
| `pipeline` | Name, version, description |
| `input` | Transcript paths, multi-transcript merger, source type (local/Zoom/Teams/Meet) |
| `execution` | Mode (interactive/express/replay) and parallel group definitions (DAG) |
| `user_preferences` | Pre-loaded decisions for replay mode (ticketing, DB, cloud, CI/CD) |
| `optional_agents` | Toggle security threat model, compliance checker, cost estimation, feedback loop |
| `notifications` | Slack/Teams webhook URLs and event triggers |
| `analytics` | Token usage tracking, execution time, output file path |
| `quality_gates` | Minimum code quality score, test coverage, vulnerability thresholds |
| `testing_retry_loop` | Max retries, retry contract path, escalation action |
| `live_deployment` | Auto docker-compose deploy, health check timeout, staging URL |

**Example: Enable all optional agents and run in express mode**

```yaml
execution:
  mode: "express"

optional_agents:
  security_threat_model: true
  compliance_checker: true
  cost_estimation: true
  feedback_loop: true
```

**Example: Pre-load preferences for replay mode**

```yaml
execution:
  mode: "replay"

user_preferences:
  ticketing_platform: "jira_cloud"
  database_engine: "postgresql"
  deployment_platform: "kubernetes"
  ci_cd_platform: "github_actions"
  cloud_provider: "aws"
  documentation_platform: "confluence"
  install_tools_when_missing: true
```

---

## Skills and Domain Knowledge

93 skill packages imported from 14 source domains, organized by SDLC phase:

| Phase | Skills Count | Key Skills | Source Domains |
|-------|-------------|------------|----------------|
| Requirements and Planning | 10 | sprint-planner, jira-expert, scrum-master, agile-product-owner, backlog-grooming-assistant | project_management |
| Documentation | 10 | api-documentation, mermaid-diagrams, crafting-effective-readmes, documentation-templates | documentation |
| Architecture and Design | 15 | api-design, backend-patterns, database-architecture, api-contract, api-endpoint-builder | code_quality, backend, api_integration, database |
| Code Patterns | 10 | django-patterns, express-route-generator, angular, fastapi-router-creator, flask-blueprint-creator | backend, frontend, code_quality |
| Testing and QA | 10 | api-test-generator, analyzing-test-coverage, api-mock-generator, api-test-suite-builder | testing_qa |
| Security and Compliance | 9 | api-security-best-practices, auth-implementation-patterns, attack-surface-analyzer | security |
| DevOps and Deployment | 13 | ansible-playbook-creator, aws-serverless, argocd-app-deployer, azure-functions, aws-cost-optimizer | devops_cicd, cloud_infrastructure |
| Performance and Monitoring | 12 | core-web-vitals, datadog-cli, creating-apm-dashboards, cache-performance-optimizer | performance_optimization, monitoring_observability |
| Automation | 4 | bash-scripting, bottleneck-detector, bash-linux | automation_scripting |
| **Total** | **93** | | **14 source domains** |

In addition to these 93 imported skills, the project includes 3 custom-written skill sets (sdlc-process, pipeline, domain-adaptation) and 18 pre-installed utility skills (pdf, docx, xlsx, pptx, frontend-design, webapp-testing, claude-api, canvas-design, brand-guidelines, algorithmic-art, mcp-builder, skill-creator, doc-coauthoring, internal-comms, template-skill, slack-gif-creator, theme-factory, web-artifacts-builder).

---

## Specialist Agents

42 specialist agent definitions organized by function. These serve as reusable sub-agents invoked within the pipeline for targeted tasks.

| Specialization | Count | Key Agents |
|----------------|-------|------------|
| Project Management | 7 | scrum-master, project-manager, product-sprint-prioritizer, atlassian-requirements-to-jira, cs-agile-product-owner, cs-product-manager, cs-project-manager |
| Documentation | 7 | documentation-engineer, technical-writer, diagram-architect, api-documenter, se-technical-writer, documentation-expert, changelog-generator |
| Architecture | 9 | architect, api-architect, database-architect, database-designer, database-administrator, backend-architect, code-architect, api-builder, api-designer |
| Testing | 6 | e2e-runner, error-detective, architect-reviewer, codebase-pattern-finder, cs-quality-regulatory, cs-engineering-lead |
| Security | 5 | compliance-auditor, engineering-security-engineer, compliance-specialist, engineering-code-reviewer, api-security-audit |
| DevOps | 3 | build-engineer, cloud-architect, build-logger |
| Performance | 5 | performance-engineer, monitoring-specialist, performance-profiler, performance-monitor, devops-troubleshooter |
| **Total** | **42** | |

---

## Hooks (Quality Gates)

26 hook files across 4 categories, plus 3 pipeline lifecycle hooks:

### Pipeline Hooks

| Hook | Purpose |
|------|---------|
| `post_agent_contract_validator.py` | Validates JSON contract structure after each agent completes |
| `pre_handoff_checker.py` | Checks chain integrity and required fields before agent handoffs |
| `notification_dispatcher.py` | Posts agent-completion messages to Slack, Teams, or macOS desktop |

### Quality Gates (9 files)

| Hook | Type | Purpose |
|------|------|---------|
| `plan-gate.json` + `plan-gate.sh` | Pre-execution | Validates implementation plan before coding starts |
| `scope-guard.json` + `scope-guard.sh` | Pre-execution | Prevents scope creep during implementation |
| `tdd-gate.json` + `tdd-gate.sh` | Pre-execution | Enforces test-driven development workflow |
| `test-runner.json` | Post-tool | Runs tests after code changes |
| `performance-budget-guard.json` | Post-tool | Enforces performance budgets |
| `performance-monitor.json` | Post-tool | Monitors performance metrics |

### DevOps Hooks (7 files)

| Hook | Type | Purpose |
|------|------|---------|
| `conventional-commits.json` + `.py` | Pre-commit | Enforces conventional commit message format |
| `prevent-direct-push.json` + `.py` | Pre-push | Blocks direct pushes to protected branches |
| `validate-branch-name.json` + `.py` | Pre-commit | Validates branch naming conventions |
| `smart-commit.json` | Pre-commit | Auto-generates smart commit messages |

### Security Hooks (6 files)

| Hook | Type | Purpose |
|------|------|---------|
| `dangerous-command-blocker.json` + `.py` | Pre-tool | Blocks dangerous shell commands |
| `secret-scanner.json` + `.py` | Pre-commit | Scans for leaked secrets and credentials |
| `file-protection.json` | Pre-tool | Protects sensitive files from modification |
| `security-scanner.json` | Post-tool | Runs security scans on code changes |

### Code Quality Hooks (2 files)

| Hook | Type | Purpose |
|------|------|---------|
| `lint-on-save.json` | Post-tool | Auto-lints code after file writes |
| `smart-formatting.json` | Post-tool | Auto-formats code after edits |

---

## Commands

### Pipeline Commands (22 — installed via plugin)

| Command | Purpose |
|---------|---------|
| `/sdlc-start` | Start full pipeline (interactive, agents chain autonomously) |
| `/sdlc-parallel` | Run in parallel DAG mode (fresh context per agent) |
| `/sdlc-sequential` | Run sequentially (one agent at a time) |
| `/sdlc-status` | Show `[OK]` / `[  ]` for all 15 agents |
| `/sdlc-resume <agent>` | Resume pipeline from any agent |
| `/sdlc-agent <agent>` | Run exactly one agent in isolation |
| `/sdlc-clean` | Remove all outputs for a fresh run |
| `/sdlc-env` | Agent 00 — environment setup |
| `/sdlc-transcript` | Agent 01 — transcript analysis |
| `/sdlc-requirements` | Agent 02 — requirements |
| `/sdlc-docs` | Agent 03 — documentation |
| `/sdlc-planning` | Agent 04 — sprint planning |
| `/sdlc-tickets` | Agent 05 — Jira/GitHub tickets |
| `/sdlc-architecture` | Agent 06 — system design |
| `/sdlc-security` | Agent 12 — security threat model *(optional)* |
| `/sdlc-code` | Agent 07 — code generation |
| `/sdlc-testing` | Agent 08 — QA + auto-fix loop |
| `/sdlc-compliance` | Agent 13 — compliance check *(optional)* |
| `/sdlc-deploy` | Agent 09 — deployment |
| `/sdlc-cost` | Agent 14 — cost estimation *(optional)* |
| `/sdlc-summary` | Agent 10 — executive dashboard |
| `/sdlc-feedback` | Agent 11 — consistency review *(optional)* |

### SDLC Workflow Commands (22 — project-scoped)

| Command | Source Domain | Purpose |
|---------|-------------|---------|
| `/create-prd` | project_management | Generate a Product Requirements Document |
| `/create-feature` | project_management | Create a feature specification |
| `/estimate-assistant` | project_management | Effort estimation helper |
| `/architecture-review` | project_management | Architecture review checklist |
| `/create-jtbd` | project_management | Jobs-to-be-Done analysis |
| `/dependency-mapper` | project_management | Map project dependencies |
| `/analyze-coverage` | testing_qa | Test coverage analysis |
| `/code-permutation-tester` | testing_qa | Code permutation testing |
| `/add-mutation-testing` | testing_qa | Set up mutation testing |
| `/add-property-based-testing` | testing_qa | Set up property-based testing |
| `/blue-green-deployment` | devops_cicd | Blue-green deployment strategy |
| `/branch-cleanup` | devops_cicd | Git branch cleanup |
| `/act` | devops_cicd | Run GitHub Actions locally |
| `/add-authentication-system` | security | Auth system implementation |
| `/check-owasp` | security | OWASP compliance check |
| `/audit-report` | security | Security audit report generation |
| `/add-changelog` | documentation | Create changelog entries |
| `/compliance-docs-generate` | documentation | Generate compliance documentation |
| `/context-prime` | documentation | Context priming for agents |
| `/code-review` | code_quality | Code review workflow |
| `/create-pr` | code_quality | Pull request creation |
| `/clean` | code_quality | Code cleanup (lint, format, fix) |

---

## Supported Domains

The pipeline auto-detects the industry domain from the transcript and applies domain-specific compliance rules, terminology, and architecture patterns. No manual configuration required.

| Domain | Compliance Frameworks | Auto-Applied Rules |
|--------|----------------------|-------------------|
| Healthcare | HIPAA, HITECH, HL7/FHIR | MFA, audit logging, 15-min session timeout, encryption at rest, +20% capacity buffer |
| E-Commerce | PCI-DSS, CCPA, GDPR | Secure payment processing, inventory management, +10% buffer |
| Fintech | PCI-DSS, SOX, KYC/AML, SOC 2 | KYC/AML verification, transaction logging, 2FA, cardholder data encryption, +20% buffer |
| Education | FERPA, COPPA, WCAG 2.1 | Student data privacy, accessibility standards, +15% buffer |
| HR Tech | GDPR, EEOC | Employee PII protection, payroll encryption, +10% buffer |
| Logistics | — | Real-time tracking, route optimization, +10% buffer |
| SaaS / B2B | SOC 2, GDPR | Multi-tenancy isolation, billing integration, +10% buffer |
| Government | FedRAMP, FISMA, Section 508 | Data sovereignty, accessibility compliance, +25% buffer |
| Real Estate | RESPA | Property listing management, escrow workflows |
| Manufacturing | ISO 9001 | MES systems, IoT integration, supply chain tracking |
| Legal | GDPR, ABA Standards | Document management, attorney-client confidentiality |
| Media / Entertainment | DMCA, COPPA, GDPR | Content management, DRM, streaming infrastructure |
| Travel / Hospitality | PCI-DSS, GDPR | Booking systems, payment security, loyalty programs |

Additional domains (Agriculture, Nonprofit, Telecom, and more) are handled through the generic compliance detection engine in `domain-adaptation/domain_rules.md`.

---

## Helper Scripts and Utilities

### Python Helpers

```bash
python helpers/pipeline_status.py       # Check pipeline progress - which agents completed
python helpers/contract_validator.py    # Validate all output JSON contracts against schemas
python helpers/output_reporter.py       # Generate a summary report of all pipeline outputs
python helpers/pipeline_analytics.py    # View analytics dashboard (token usage, timing, metrics)
python helpers/harness.py pre <agent>   # Validate inputs before running an agent
python helpers/harness.py post <agent>  # Validate output contract after an agent completes
python helpers/test_retry_loop.py       # Run the self-healing test-fix loop check
```

### Shell Scripts

```bash
bash scripts/clean_outputs.sh           # Reset all outputs for a fresh pipeline run
bash scripts/run_pipeline.sh            # Mode chooser + pre-flight check + launcher
bash scripts/validate_all.sh            # Validate all contracts in a single pass
python scripts/orchestrator.py --status # Show current pipeline status
python scripts/build_plugin.py          # Rebuild sdlc-automation.plugin from project sources
```

### Notifications Setup

Edit `sdlc-pipeline.yml` to enable Slack or Teams alerts after each agent completes:

```yaml
notifications:
  enabled: true
  channels:
    slack:
      webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    teams:
      webhook_url: "https://outlook.office.com/webhook/YOUR/URL"
```

If no webhook is configured, the hook falls back to a macOS desktop notification.

### Tool Fallback Strategy

The pipeline never stops. When a tool is missing, agents fall back gracefully:

| Tool Missing | Fallback | Impact |
|-------------|----------|--------|
| Jira / ServiceNow | File-based tickets (JSON + CSV + Markdown) | Zero — import into Jira later |
| Git / GitHub | Generate code as local files | Zero — git init later |
| Docker | Generate Dockerfiles + manual deployment scripts | Zero — build with Docker later |
| PostgreSQL | Default to SQLite | Minimal — swap DB config later |
| Node.js | Generate code files without running | Zero — install Node to run |
| Slack | Skip notifications | Zero — configure webhooks later |

---

## Sample Transcripts

Five domain-specific sample transcripts are included for testing and demonstration:

| File | Domain | Client | Scenario |
|------|--------|--------|----------|
| `inputs/transcript.txt` | SaaS / Agency | TechNova Solutions | Digital agency platform (default) |
| `inputs/samples/healthcare_transcript.txt` | Healthcare | MedCare Hospital | Patient portal with HIPAA compliance |
| `inputs/samples/ecommerce_transcript.txt` | E-Commerce | UrbanBazaar Marketplace | Multi-vendor marketplace with PCI-DSS |
| `inputs/samples/fintech_transcript.txt` | Fintech | PayWise Financial | Payment platform with KYC/AML |
| `inputs/samples/education_transcript.txt` | Education | BrightPath Academy | LMS platform with FERPA compliance |
| `inputs/samples/saas_transcript.txt` | SaaS / B2B | CloudMetrics Inc | Analytics SaaS with SOC 2 |

To use a sample, copy it to the default input path:

```bash
cp inputs/samples/healthcare_transcript.txt inputs/transcript.txt
```

---

## Resuming the Pipeline

If the pipeline stops at any agent (network error, token limit, manual pause), resume from the exact point of failure. Each agent is idempotent — re-running it overwrites its previous output without side effects.

**Via slash command (after plugin install):**

```
/sdlc-resume code_agent
/sdlc-resume deployment_agent
```

**Via orchestrator:**

```bash
python scripts/orchestrator.py --resume-from code_agent
```

**Manual prompt pattern:**

```
Resume the SDLC pipeline from [agent_name].
Read outputs/[previous_output].json and execute .claude/agents/[NN_agent_name].md
```

**Specific examples:**

```
# Resume from Architecture (Agent 06 reads Jira output)
Resume the SDLC pipeline from architecture.
Read outputs/jira/jira_tickets.json and execute .claude/agents/06_architecture_agent.md

# Resume from Code Generation (Agent 07 reads Architecture output)
Resume the SDLC pipeline from code generation.
Read outputs/architecture/system_design.json and execute .claude/agents/07_code_agent.md

# Resume from Testing (Agent 08 reads Code output)
Resume the SDLC pipeline from testing.
Read outputs/code/code_output.json and execute .claude/agents/08_testing_agent.md

# Run only the Feedback Loop agent after everything else completed
Read .claude/agents/11_feedback_loop_agent.md and execute it.
```

---

## Configuration

### settings.json

Located at `.claude/settings.json`. Controls Claude Code environment settings, hooks, and tool permissions:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "permissions": {
    "allow": [
      "Bash(python:*)", "Bash(python3:*)", "Bash(bash:*)",
      "Bash(cat:*)", "Bash(ls:*)", "Bash(mkdir:*)",
      "Bash(node:*)", "Bash(npm:*)", "Bash(npx:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [{ "matcher": "Bash", "hooks": [{ "type": "command", "command": "python3 .claude/hooks/security/dangerous-command-blocker.py" }] }],
    "PostToolUse": [{ "matcher": "Write|Edit", "hooks": [
      { "type": "command", "command": "python3 .claude/hooks/post_agent_contract_validator.py" },
      { "type": "command", "command": "python3 .claude/hooks/notification_dispatcher.py" }
    ]}],
    "SessionEnd": [{ "hooks": [{ "type": "command", "command": "python3 .claude/hooks/pre_handoff_checker.py" }] }]
  }
}
```

### sdlc-pipeline.yml

The primary pipeline configuration file. Controls execution mode, parallel groups, user preferences, optional agents, notifications, analytics, and quality gates. See the [Pipeline-as-Code](#pipeline-as-code) section for full details.

### Quality Gates

Configured in the `quality_gates` section of `sdlc-pipeline.yml`:

| Gate | Default | Description |
|------|---------|-------------|
| `code_quality_minimum_score` | 70 | Minimum code quality score (0-100). Code agent auto-regenerates if below. |
| `test_coverage_minimum` | 60 | Minimum test coverage percentage for generated test suites. |
| `vulnerability_max_critical` | 0 | Maximum allowed critical vulnerabilities. Pipeline flags if exceeded. |
| `vulnerability_max_high` | 3 | Maximum allowed high-severity vulnerabilities. |

---

## Stats at a Glance

| Component | Count |
|-----------|-------|
| Pipeline agents | 15 (11 core + 4 optional) |
| Specialist agents | 42 |
| Skills (imported) | 93 |
| Skills (pre-installed) | 18 |
| Skills (custom) | 3 |
| Hooks | 26 + 3 pipeline |
| Commands (pipeline /sdlc-*) | 22 |
| Commands (workflow) | 22 |
| Sample transcripts | 6 |
| Supported domains | 13+ |
| Helper scripts | 9 |
| Execution modes | 3 (Interactive, Express, Replay) + Parallel + Sequential orchestrator |
| Output directories | 15 |

---

## Documentation

| File | What It Covers |
|------|---------------|
| [`CLAUDE.md`](CLAUDE.md) | Pipeline rules, agent execution order, fallback strategy, directory structure |
| [`USAGE_GUIDE.md`](USAGE_GUIDE.md) | Complete usage guide with all examples and scenarios |
| [`SDLC_TERMINOLOGY_GUIDE.md`](SDLC_TERMINOLOGY_GUIDE.md) | Full SDLC terminology reference and how IT companies work |
| [`sdlc-pipeline.yml`](sdlc-pipeline.yml) | Pipeline-as-Code configuration (execution, preferences, gates) |
| [`plugins/sdlc-automation/README.md`](plugins/sdlc-automation/README.md) | Plugin install + command reference |
| [`.claude/agents/AGENT_TEAMS_MODE.md`](.claude/agents/AGENT_TEAMS_MODE.md) | Agent Teams parallel execution and DAG guide |
| [`.claude/agents/_COMMUNICATION_PROTOCOL.md`](.claude/agents/_COMMUNICATION_PROTOCOL.md) | JSON contract chain specification (v1.0) |
| [`.claude/agents/_ISOLATED_MODE.md`](.claude/agents/_ISOLATED_MODE.md) | Rules for orchestrator-managed agent execution |
| [`.claude/rules/pipeline_rules.md`](.claude/rules/pipeline_rules.md) | Core pipeline behavior constraints and interactive decision protocol |

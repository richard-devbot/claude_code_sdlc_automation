# SDLC Automation Platform

> Drop a client meeting transcript in. Get requirements, documentation, sprint plans, tickets, architecture, code, tests, security models, and deployment configs out — for any industry.

![Pipeline](https://img.shields.io/badge/Pipeline-15_Agents-blue)
![Commands](https://img.shields.io/badge/Commands-22-purple)
![Domains](https://img.shields.io/badge/Domains-13+-teal)
![Version](https://img.shields.io/badge/Version-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Install in 1 command

```bash
claude plugin marketplace add richard-devbot/claude_code_sdlc_automation && \
claude plugin install sdlc-automation@claude_code_sdlc_automation
```

Restart Claude Code. Type `/sdlc` to see all commands.

---

## Quick Start (3 steps)

**Step 1 — Add your transcript**

Create `inputs/transcript.txt` and paste your client meeting notes, Zoom transcript, or discovery call recording.

> No transcript yet? Use one of the 5 sample transcripts in `inputs/samples/` (healthcare, fintech, e-commerce, education, SaaS).

**Step 2 — Start the pipeline**

```
/sdlc-start
```

Claude will scan your environment, detect tools, and ask a few quick questions (ticketing platform, database, deployment target). Then it runs autonomously.

**Step 3 — Review your deliverables**

When the pipeline completes, open:

```
outputs/PROJECT_COMPLETE_SUMMARY.md   ← full project summary
outputs/EXECUTIVE_DASHBOARD.md        ← one-page stakeholder view
```

Every generated artifact is in the `outputs/` directory, organized by phase.

---

## What you get

| Phase | Agent | What it produces |
|-------|-------|-----------------|
| Analysis | 00 Environment + 01 Transcript | Structured JSON from your meeting notes |
| Requirements | 02 Requirements | Functional + non-functional requirements with IDs |
| Documentation | 03 Documentation | BRD, FRD, Statement of Work (Word/PDF-ready) |
| Planning | 04 Planning | Sprint plan, team composition, milestones |
| Ticketing | 05 Tickets | Jira/GitHub epics → stories → tasks |
| Architecture | 06 Architecture | System design, API contracts, DB schema, HLD |
| Security | 12 Security *(optional)* | STRIDE threat model, OWASP Top 10 mitigations |
| Code | 07 Code | Production-ready scaffolding for your full stack |
| Testing | 08 Testing | Test plan, test cases, API tests + self-healing loop |
| Compliance | 13 Compliance *(optional)* | HIPAA / GDPR / PCI-DSS / SOC 2 gap matrix |
| Deployment | 09 Deployment | Dockerfiles, CI/CD pipeline, IaC templates |
| Cost | 14 Cost *(optional)* | Cloud cost forecast (AWS/Azure/GCP) in Excel |
| Summary | 10 Summary | Executive dashboard, full artifact inventory |
| Feedback | 11 Feedback *(optional)* | Consistency review, traceability matrix, remediation plan |

---

## Commands

### Pipeline control

| Command | What it does |
|---------|-------------|
| `/sdlc-start` | Full pipeline — interactive, agents chain autonomously |
| `/sdlc-parallel` | DAG orchestrator, parallel mode (each agent gets a fresh context window) |
| `/sdlc-sequential` | Orchestrator, sequential mode (one agent at a time — easiest to debug) |
| `/sdlc-status` | Show which agents completed `[OK]` vs pending `[  ]` |
| `/sdlc-resume <agent>` | Resume pipeline from any agent after a failure |
| `/sdlc-agent <agent>` | Run exactly one agent in isolation |
| `/sdlc-clean` | Remove all outputs for a fresh run |

### Individual agent triggers

```
/sdlc-env          /sdlc-transcript    /sdlc-requirements  /sdlc-docs
/sdlc-planning     /sdlc-tickets       /sdlc-architecture  /sdlc-security
/sdlc-code         /sdlc-testing       /sdlc-compliance    /sdlc-deploy
/sdlc-cost         /sdlc-summary       /sdlc-feedback
```

---

## Execution modes

### Interactive (default)
Agents pause at decision points (ticketing platform, database, deployment target) and ask you to choose. Choices are saved and reused — you're never asked the same question twice.

### Parallel DAG (recommended for speed)
```
/sdlc-parallel
```
Each agent runs as its own `claude -p` subprocess with a **fresh 200K context window**. No context accumulation, no mid-pipeline compaction. Phases run in dependency order; agents within a phase run concurrently.

### Sequential (recommended for debugging)
```
/sdlc-sequential
```
One agent at a time. Easier to inspect what each agent produced before the next one runs.

### Resume from any point
```
/sdlc-resume code_agent
/sdlc-resume deployment_agent
```
If a phase fails, fix it and resume. All completed agents are skipped automatically.

---

## Supported domains

Healthcare · Fintech · E-Commerce · Education · HR Tech · Logistics · SaaS ·
Government · Real Estate · Manufacturing · Legal · Media · Travel · Agriculture

Domain intelligence is detected automatically from your transcript and flows through all agents via JSON contracts. No configuration needed.

---

## Notifications (optional)

Get a Slack or Teams message every time an agent completes. Edit `sdlc-pipeline.yml`:

```yaml
notifications:
  enabled: true
  channels:
    slack:
      webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    teams:
      webhook_url: "https://outlook.office.com/webhook/YOUR/URL"
```

If no webhook is configured, falls back to a macOS desktop notification.

---

## Update the plugin

```bash
claude plugin marketplace update claude_code_sdlc_automation
claude plugin update sdlc-automation@claude_code_sdlc_automation
```

---

## Repository structure

```
inputs/                    ← put transcript.txt here
  samples/                 ← 5 domain samples (healthcare, fintech, etc.)
outputs/                   ← all generated artifacts
.claude/
  agents/                  ← 15 pipeline agent definitions
  commands/                ← slash commands available in this project
  hooks/                   ← quality gates, notifications, validators
  settings.json            ← hooks wiring + permissions
plugins/sdlc-automation/   ← installable plugin (GitHub marketplace source)
scripts/
  orchestrator.py          ← DAG runner (parallel + sequential modes)
  build_plugin.py          ← rebuilds sdlc-automation.plugin from sources
helpers/
  harness.py               ← agent lifecycle wrapper (pre/post validation)
  test_retry_loop.py       ← cyclic test-fix loop helper
sdlc-pipeline.yml          ← pipeline config (phases, optional agents, notifications)
```

---

## Pipeline communication

Agents communicate only through JSON contracts written to `outputs/`. No central broker. Each agent reads its upstream contract, does its work, writes its own contract.

```
Agent N  →  writes outputs/N_result.json
Agent N+1  →  reads outputs/N_result.json  →  writes outputs/N+1_result.json
...
Agent 10  →  pipeline_complete: true
```

The orchestrator (`/sdlc-parallel`, `/sdlc-sequential`) manages phase sequencing externally so each agent runs in an isolated subprocess with no accumulated context.

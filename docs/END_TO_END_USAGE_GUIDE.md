# End-to-End Usage Guide — SDLC Automation Pipeline

This document walks through the **complete pipeline execution** from trigger prompt
to final output. It covers every agent, every decision point, every input/output,
and shows sample data at each stage.

---

## Table of Contents

1. [Prerequisites Checklist](#1-prerequisites-checklist)
2. [The Trigger Prompt](#2-the-trigger-prompt)
3. [Step-by-Step Pipeline Walkthrough](#3-step-by-step-pipeline-walkthrough)
4. [Parallel Execution Map](#4-parallel-execution-map)
5. [Complete Input/Output Reference](#5-complete-inputoutput-reference)
6. [Sample Interactive Decision Flow](#6-sample-interactive-decision-flow)
7. [What You Get at the End](#7-what-you-get-at-the-end)
8. [Alternative Prompts](#8-alternative-prompts)

---

## 1. Prerequisites Checklist

Before triggering the pipeline, verify these are in place:

```
✅ Claude Code CLI installed and authenticated
✅ Working directory is sdlc-automation/
✅ inputs/transcript.txt exists (or multiple .txt files in inputs/)
✅ Python 3.7+ available (for helper scripts — optional)
```

### Verify your transcript is in place

```bash
ls inputs/
# Expected: transcript.txt (and optionally more .txt files)
```

The default transcript is a **TechNova Solutions** discovery call (digital agency,
150 employees, project management + client portal + invoicing). You can replace it
with your own meeting notes.

### No other tools required

The pipeline works with **zero external tools**. Everything falls back to file-based
output. But if you want live integrations (Jira, GitHub, Docker), the pipeline will
ask you interactively — you don't need to set anything up in advance.

---

## 2. The Trigger Prompt

Open Claude Code in the `sdlc-automation/` directory and paste this prompt:

### Full Interactive Mode (recommended for first run)

```
Start the SDLC automation pipeline.
Read .claude/agents/00_environment_agent.md and execute it.
It will scan the system, present tool options, and autonomously trigger all
subsequent agents through the chain. At each decision point, present me with
all available options and wait for my choice.
```

### Express Mode (use recommended defaults, no questions)

```
Start the SDLC automation pipeline in express mode.
Read .claude/agents/00_environment_agent.md and execute it.
Use all recommended (★) defaults without asking. Only pause if a recommended
option is unavailable. Run all agents through to completion.
```

### Skip Environment Setup (start from transcript directly)

```
Start the SDLC automation pipeline.
Read .claude/agents/01_transcript_agent.md and execute it.
Input file: inputs/transcript.txt
The agent will autonomously trigger all subsequent agents.
```

---

## 3. Step-by-Step Pipeline Walkthrough

Here is exactly what happens after you trigger the prompt, in order.

---

### Phase 1: Environment + Transcript (parallel capable)

#### Agent 00 — Environment Setup

```
Reads:    System environment (no file input)
Writes:   outputs/environment_report.json
          outputs/SETUP_INSTRUCTIONS.md (if tools need manual install)
Duration: ~30 seconds
```

**What happens:**
1. Scans your system for tools: git, node, npm, python, docker, database CLIs
2. Checks environment variables: JIRA_BASE_URL, GITHUB_TOKEN, SLACK_WEBHOOK_URL, etc.
3. **Presents interactive decisions** for each missing tool:

```
🔧 Docker — not detected on this system

This tool is used by: Agent 09 — Deployment
Impact if missing: Deployment configs generated as files only (can't test build)

Available options:
  1. Install Docker Desktop (~5 min download)
  2. Use Podman (lightweight alternative)
  3. ★ Skip — generate Dockerfiles as text files
  4. I already have it — let me configure the path

Which option would you prefer? (1/2/3/4)
```

```
☁️ JIRA Cloud Integration — not configured

  1. I have Jira credentials — let me provide them
  2. Use GitHub Issues instead (free)
  3. Use Azure DevOps Boards
  4. Use Linear
  5. ★ Skip — generate file-based tickets (JSON + CSV + Markdown)

Which option? (1/2/3/4/5)
```

4. Records ALL your choices in `user_preferences`
5. Writes `outputs/environment_report.json`

**Sample output** (`outputs/environment_report.json`):
```json
{
  "contract_version": "1.1",
  "produced_by": "environment_agent",
  "timestamp": "2026-03-24T10:00:00Z",
  "tools_available": {
    "git": { "available": true, "version": "2.44.0" },
    "node": { "available": true, "version": "20.11.0" },
    "docker": { "available": false, "user_choice": "skip" }
  },
  "user_preferences": {
    "ticketing_platform": "file_based",
    "database_engine": "sqlite",
    "deployment_platform": "docker_compose",
    "ci_cd_platform": "github_actions",
    "interactive_mode": true
  },
  "pipeline_ready": true,
  "next_agent": "transcript_agent"
}
```

**Handoff:** Automatically triggers Agent 01.

---

#### Agent 01 — Transcript Parser

```
Reads:    inputs/transcript.txt (or multiple .txt files)
          outputs/environment_report.json
Writes:   outputs/transcripts/structured_meeting_output.json
Duration: ~1-2 minutes
```

**What happens:**
1. **Presents transcript source options** (if interactive mode):

```
📝 TRANSCRIPT INPUT — Where should I get the meeting transcript?

  1. ★ Local file(s) in inputs/ directory [FOUND: transcript.txt]
  2. Paste transcript text directly
  3. Pull from Zoom Cloud Recordings
  ...

Which option? (1)
```

2. If multiple .txt files found in `inputs/`, merges them chronologically
3. Parses the transcript and extracts:
   - Meeting metadata (date, duration, attendees)
   - Pain points and current challenges
   - Requested features and capabilities
   - Technical context and constraints
   - Compliance/regulatory mentions
   - Budget and timeline expectations
   - Open questions and decisions
4. **Auto-detects domain** (e.g., "SaaS" from TechNova transcript)

**Sample output** (`outputs/transcripts/structured_meeting_output.json`):
```json
{
  "contract_version": "1.1",
  "produced_by": "transcript_agent",
  "timestamp": "2026-03-24T10:02:00Z",
  "domain": "saas",
  "meeting_metadata": {
    "date": "2026-03-05",
    "duration_minutes": 75,
    "client": "TechNova Solutions",
    "industry": "Digital Agency"
  },
  "attendees": [
    { "name": "Marcus Chen", "role": "CEO", "affiliation": "client" },
    { "name": "Sarah Williams", "role": "Head of Operations", "affiliation": "client" },
    { "name": "David Park", "role": "Business Analyst", "affiliation": "team" }
  ],
  "pain_points": [
    "Scattered tools — spreadsheets, emails, shared drives",
    "3 hours every Monday compiling status reports",
    "No visibility into team capacity and workload",
    "Clients email asking for project status — no self-service"
  ],
  "requested_features": [
    { "id": "F-001", "name": "Centralized Project Dashboard", "priority": "critical" },
    { "id": "F-002", "name": "Client Portal with Self-Service", "priority": "critical" },
    { "id": "F-003", "name": "Automated Invoicing & Time Tracking", "priority": "high" },
    { "id": "F-004", "name": "Resource Allocation & Capacity View", "priority": "high" },
    { "id": "F-005", "name": "Document Management System", "priority": "medium" }
  ],
  "compliance_mentions": ["SOC2", "data_privacy"],
  "budget_range": "$150,000 - $200,000",
  "timeline": "6 months MVP",
  "next_agent": "requirement_agent",
  "next_input_file": "outputs/transcripts/structured_meeting_output.json"
}
```

**Handoff:** Automatically triggers Agent 02.

---

### Phase 2: Requirements

#### Agent 02 — Requirement Specification

```
Reads:    outputs/transcripts/structured_meeting_output.json
Writes:   outputs/requirements/requirement_spec.json
Duration: ~2-3 minutes
```

**What happens:**
1. Maps each pain point to features, each feature to formal requirements
2. Classifies as Functional (FR) or Non-Functional (NFR)
3. Prioritizes using MoSCoW method (Must/Should/Could/Won't)
4. Identifies actors (Admin, Client, Team Lead, Developer, etc.)
5. Adds domain-specific requirements (SOC2 → audit logging, access controls, etc.)
6. Performs risk analysis

**Sample output structure:**
```json
{
  "produced_by": "requirement_agent",
  "functional_requirements": [
    {
      "id": "FR-001",
      "title": "Project Dashboard with Real-Time Status",
      "description": "System shall display all active projects with status, timeline, and team allocation",
      "priority": "Must Have",
      "source_feature": "F-001",
      "actors": ["Admin", "Team Lead", "Project Manager"],
      "acceptance_criteria": [
        "Dashboard loads in < 2 seconds",
        "Shows project status, % complete, team members, deadlines",
        "Filterable by client, team, status, date range"
      ]
    }
  ],
  "non_functional_requirements": [
    {
      "id": "NFR-001",
      "category": "Performance",
      "requirement": "Page load time < 2 seconds for 95th percentile"
    },
    {
      "id": "NFR-002",
      "category": "Security",
      "requirement": "SOC2 compliant audit logging on all data access"
    }
  ],
  "modules": ["Project Management", "Client Portal", "Invoicing", "Resource Management", "Documents"],
  "risks": [
    { "risk": "Scope creep from 40+ client needs", "probability": "High", "mitigation": "Strict MVP scope" }
  ],
  "next_agent": "documentation_agent"
}
```

**Handoff:** Automatically triggers Agent 03.

---

### Phase 3: Documentation + Planning (parallel capable)

#### Agent 03 — Documentation Writer

```
Reads:    outputs/requirements/requirement_spec.json
Writes:   outputs/documents/documentation_output.json
          outputs/documents/BRD.md
          outputs/documents/FRD.md
          outputs/documents/SOW.md
Duration: ~3-4 minutes
```

**What happens:**
1. Generates 3 documents:
   - **BRD.md** — Business Requirements Document (executive-facing)
   - **FRD.md** — Functional Requirements Document (developer-facing)
   - **SOW.md** — Statement of Work (client contract)
2. **Presents publishing options:**

```
📚 DOCUMENT PUBLISHING — Where should I publish?

Generated: BRD.md, FRD.md, SOW.md

  1. ★ Keep as local files only
  2. Publish to Confluence
  3. Publish to Notion
  4. Export as PDF documents
  5. Multiple — local + platform

Which option? (1)
```

**Handoff:** Triggers Agent 04.

#### Agent 04 — Sprint Planner (can run parallel with Agent 03)

```
Reads:    outputs/documents/documentation_output.json
          outputs/requirements/requirement_spec.json
Writes:   outputs/planning/sprint_plan.json
Duration: ~2 minutes
```

**What happens:**
1. Creates sprint breakdown: Sprint 0 (setup) through Sprint N
2. Estimates team composition (backend devs, frontend devs, QA, DevOps)
3. Calculates timeline with domain-specific buffer (+10% for SaaS)
4. Identifies parallel work streams

**Sample output structure:**
```json
{
  "produced_by": "planning_agent",
  "total_sprints": 7,
  "sprint_duration_weeks": 2,
  "total_timeline_weeks": 16,
  "team_composition": {
    "backend_developers": 2,
    "frontend_developers": 2,
    "qa_engineer": 1,
    "devops_engineer": 1,
    "project_manager": 1,
    "total_team_size": 7
  },
  "sprints": [
    {
      "sprint_number": 0,
      "name": "Project Setup & Foundation",
      "goals": ["Dev environment", "CI/CD", "Auth system", "Database schema"],
      "story_points": 21
    },
    {
      "sprint_number": 1,
      "name": "Core Project Management",
      "goals": ["Project CRUD", "Dashboard", "Status tracking"],
      "story_points": 34
    }
  ],
  "next_agent": "jira_agent"
}
```

**Handoff:** Triggers Agent 05.

---

### Phase 4: Tickets + Architecture (parallel capable)

#### Agent 05 — Ticket Creation

```
Reads:    outputs/planning/sprint_plan.json
          outputs/requirements/requirement_spec.json
          outputs/environment_report.json
Writes:   outputs/jira/jira_tickets.json
          outputs/jira/jira_tickets_readable.md
          outputs/jira/jira_import.csv
          outputs/jira/ticketing_report.md
Duration: ~3-4 minutes
```

**What happens:**
1. Checks user's ticketing preference from `user_preferences.ticketing_platform`
2. If live platform chosen → checks for existing project, offers bidirectional sync:

```
🔄 EXISTING PROJECT CHECK

I detected an existing Jira project with:
  - 3 existing epics
  - 12 existing stories

How should I handle this?
  1. ★ Merge — Add new tickets alongside existing
  2. Replace — Archive existing and create fresh
  3. Supplement — Only create tickets for uncovered requirements
  4. Skip — Generate files only

Which option? (1/2/3/4)
```

3. Creates ticket hierarchy: Epic → User Story → Task
4. Every FR gets at least one User Story with acceptance criteria
5. Generates importable CSV for any ticketing tool

**Sample ticket:**
```json
{
  "epic_id": "EPIC-001",
  "epic_name": "Project Management Module",
  "user_stories": [
    {
      "story_id": "US-001",
      "title": "As a Project Manager, I want to see all active projects on a dashboard so that I can track status at a glance",
      "acceptance_criteria": [
        "GIVEN I am logged in WHEN I open the dashboard THEN I see all my active projects",
        "GIVEN projects are displayed WHEN I click a project THEN I see detailed status"
      ],
      "story_points": 5,
      "sprint": 1,
      "tasks": [
        { "task_id": "T-001", "title": "Create project listing API endpoint", "assignee_role": "Backend Dev" },
        { "task_id": "T-002", "title": "Build project dashboard UI component", "assignee_role": "Frontend Dev" },
        { "task_id": "T-003", "title": "Write E2E tests for dashboard", "assignee_role": "QA Engineer" }
      ]
    }
  ]
}
```

**Handoff:** Triggers Agent 06.

#### Agent 06 — Architecture (can run parallel with Agent 05)

```
Reads:    outputs/jira/jira_tickets.json
          outputs/requirements/requirement_spec.json
Writes:   outputs/architecture/system_design.json
          outputs/architecture/HLD.md
Duration: ~3-5 minutes
```

**What happens:**
1. **Presents tech stack for confirmation:**

```
🏗️ TECH STACK RECOMMENDATION

Based on SaaS domain, 150 users, SOC2 compliance:

BACKEND:    1. ★ Node.js / Express    2. Python / FastAPI    3. Java / Spring Boot
FRONTEND:   1. ★ React.js             2. Next.js             3. Vue.js
DATABASE:   1. ★ PostgreSQL            2. MySQL               3. MongoDB
AUTH:       1. ★ JWT + refresh tokens  2. OAuth2              3. Session-based

Go with recommended stack (★), or modify?
```

2. Designs database schema (users, projects, clients, invoices, etc.)
3. Defines API contracts (REST endpoints with request/response schemas)
4. Creates security architecture (JWT, RBAC, audit logging)
5. Writes HLD.md (High-Level Design document)

**Handoff:** Triggers Agent 12 (if security threat modeling enabled) or Agent 07.

---

### Phase 5: Security Threat Model (optional)

#### Agent 12 — Security Threat Model

```
Reads:    outputs/architecture/system_design.json
          outputs/requirements/requirement_spec.json
Writes:   outputs/security/threat_model.json
          outputs/security/THREAT_MODEL.md
Duration: ~2-3 minutes
Enabled:  Only if optional_agents.security_threat_model = true in sdlc-pipeline.yml
```

**What happens:**
1. Performs STRIDE analysis on each architecture component
2. Scores each threat with DREAD (1-10 per factor)
3. Generates mitigation recommendations
4. Adds security requirements for Agent 07 (Code) and Agent 08 (Testing)

**Sample threat:**
```json
{
  "component": "Authentication API",
  "stride_category": "Spoofing",
  "threat": "Attacker uses stolen JWT to impersonate user",
  "dread_score": { "damage": 8, "reproducibility": 7, "exploitability": 5, "affected_users": 9, "discoverability": 4, "total": 6.6 },
  "severity": "HIGH",
  "mitigation": "Implement short-lived JWTs (15 min), refresh token rotation, token binding to IP/device"
}
```

**Handoff:** Triggers Agent 07.

---

### Phase 6: Code Generation

#### Agent 07 — Code Generation

```
Reads:    outputs/architecture/system_design.json
          outputs/architecture/HLD.md
          outputs/security/threat_model.json (if exists)
          outputs/environment_report.json
Writes:   outputs/code/code_output.json
          outputs/code/backend/  (full scaffold)
          outputs/code/frontend/ (full scaffold)
          outputs/code/README.md
          outputs/code/.gitignore
Duration: ~5-8 minutes (largest agent)
```

**What happens:**
1. **Presents code setup options:**

```
⚡ CODE SCAFFOLDING — Setup Options

📦 PACKAGE INITIALIZATION
  1. ★ Run npm init + install dependencies (Node.js detected ✓)
  2. Generate package.json only

🗃️ DATABASE: Using SQLite (from your earlier choice)

🔧 GIT REPOSITORY
  1. ★ Initialize local git repo + first commit
  2. Create GitHub repository + push + branch protection
  3. Skip git setup

Which options? (1, 1)
```

2. Generates **actual working code** (not pseudocode):
   - Backend: `app.js`, auth middleware, audit middleware, database config, controllers, services, routes, migrations, `.env.example`, `package.json`
   - Frontend: `App.jsx`, Login page, Dashboard, API service, auth service, useAuth hook, ProtectedRoute component, `package.json`

3. **Runs dependency vulnerability scan:**

```
⚠️ DEPENDENCY VULNERABILITIES FOUND

  0 critical, 1 high, 3 moderate vulnerabilities

  1. ★ Auto-fix — run npm audit fix
  2. Show details
  3. Ignore

Which option? (1)
```

4. **Performs code quality scoring:**
   - Security: 85/100
   - Maintainability: 78/100
   - Performance: 82/100
   - If any score < 70, regenerates affected files

**Handoff:** Triggers Agent 08.

---

### Phase 7: Testing + Compliance (parallel capable)

#### Agent 08 — Testing & QA

```
Reads:    outputs/code/code_output.json
          outputs/jira/jira_tickets.json
          outputs/requirements/requirement_spec.json
Writes:   outputs/qa/qa_results.json
Duration: ~3-4 minutes
```

**What happens:**
1. Creates test plans mapped to requirements
2. Generates test cases (unit, integration, E2E, security)
3. Creates security testing checklist
4. **Presents test execution options:**

```
🧪 TEST EXECUTION — Run generated tests?

  1. ★ Generate test files only (run manually later)
  2. Run tests now against the generated code
  3. Generate AND run — install deps, execute suite
  4. Generate test files + GitHub Actions CI workflow

Which option? (1)
```

5. If option 2/3: installs dependencies, runs tests, captures pass/fail/coverage

**Handoff:** Triggers Agent 13 (if compliance enabled) or Agent 09.

#### Agent 13 — Compliance Checker (optional, parallel with Agent 08)

```
Reads:    ALL output contracts
Writes:   outputs/compliance/compliance_matrix.json
          outputs/compliance/COMPLIANCE_REPORT.md
Duration: ~2 minutes
Enabled:  Auto-enabled for regulated domains (healthcare, fintech)
```

**What happens:**
1. Identifies applicable frameworks from domain (SOC2 for SaaS)
2. Maps each compliance requirement to pipeline artifacts
3. Checks: Is it in requirements? In architecture? In code? In tests?
4. Produces pass/fail matrix

**Sample output:**
```
SOC2 Compliance Matrix — TechNova Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Score: 87% (26/30 requirements met)

✅ PASS  Access control — Role-based auth in architecture + code
✅ PASS  Audit logging — Audit middleware implemented
✅ PASS  Encryption in transit — HTTPS enforced
⚠️ PARTIAL  Encryption at rest — DB encryption not configured
❌ FAIL  Incident response plan — Not documented
```

**Handoff:** Triggers Agent 09.

---

### Phase 8: Deployment

#### Agent 09 — Deployment & CI/CD

```
Reads:    outputs/qa/qa_results.json
          outputs/architecture/system_design.json
          outputs/code/code_output.json
          outputs/environment_report.json
Writes:   outputs/deployment/deployment_output.json
          outputs/deployment/Dockerfile.backend
          outputs/deployment/Dockerfile.frontend
          outputs/deployment/docker-compose.yml
          outputs/deployment/github-actions-ci.yml
          outputs/deployment/env-template.md
          outputs/deployment/production_readiness.md
          outputs/deployment/scripts/run_backend.sh
          outputs/deployment/scripts/run_frontend.sh
          outputs/deployment/scripts/setup_database.sh
Duration: ~3-5 minutes
```

**What happens:**
1. **Presents deployment decisions:**

```
🚀 DEPLOYMENT STRATEGY

🐳 CONTAINERIZATION
  1. ★ Docker + Docker Compose
  2. Kubernetes manifests
  3. No containers — manual scripts only
  → Using: ★ Docker (from your earlier choice)

🔄 CI/CD PIPELINE
  1. ★ GitHub Actions
  2. GitLab CI
  3. All platforms
  → Using: ★ GitHub Actions (from your earlier choice)

☁️ CLOUD PROVIDER
  1. AWS templates
  2. Azure templates
  3. ★ Cloud-agnostic (Docker Compose runs anywhere)

Which cloud option? (3)
```

2. Generates Dockerfiles (multi-stage production builds)
3. Generates docker-compose.yml with all services
4. Generates CI/CD pipeline config
5. Creates manual deployment scripts (no-Docker fallback)
6. Creates production readiness checklist

**Handoff:** Triggers Agent 10.

---

### Phase 9: Summary + Cost + Feedback (sequential)

#### Agent 10 — Project Summary

```
Reads:    ALL output contracts from outputs/
Writes:   outputs/pipeline_final.json
          outputs/PROJECT_COMPLETE_SUMMARY.md (~30KB)
          outputs/EXECUTIVE_DASHBOARD.md
Duration: ~2-3 minutes
```

**What happens:**
1. Reads every contract from every agent
2. Compiles comprehensive project summary
3. Creates executive dashboard (one-page management view)
4. Records overall pipeline status

**Handoff:** Triggers Agent 14 (if cost estimation enabled) or Agent 11.

#### Agent 14 — Cost Estimation (optional)

```
Reads:    outputs/architecture/system_design.json
          outputs/planning/sprint_plan.json
Writes:   outputs/cost/cost_estimation.json
          outputs/cost/COST_BREAKDOWN.md
Duration: ~2 minutes
```

**What happens:**
1. **Asks about expected traffic:**

```
💰 COST ESTIMATION — Help me estimate accurately

Expected monthly active users: ___
Expected API requests per day: ___
Expected data storage (GB): ___
Preferred region: (us-east-1 / eu-west-1 / etc.)
```

2. Estimates costs across AWS, Azure, GCP for dev/staging/prod

**Sample output:**
```
Monthly Cost Estimates — TechNova Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                  AWS        Azure      GCP
Development      $45/mo     $42/mo     $40/mo
Staging          $120/mo    $115/mo    $110/mo
Production       $380/mo    $365/mo    $350/mo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Annual Total     $6,540     $6,264     $6,000
```

**Handoff:** Triggers Agent 11.

#### Agent 11 — Feedback Loop (final agent)

```
Reads:    ALL output contracts
Writes:   outputs/feedback/consistency_report.json
          outputs/feedback/REMEDIATION_PLAN.md
Duration: ~2-3 minutes
```

**What happens:**
1. Cross-references ALL outputs for consistency:
   - Every FR-XXX must have at least one US-XXX
   - Every US-XXX must have test coverage
   - Every API endpoint in architecture must exist in code
   - Sprint capacity must not exceed team velocity
   - Compliance requirements must all be addressed
2. Categorizes issues: CRITICAL / WARNING / INFO
3. Produces remediation plan with action items

**Sample finding:**
```
⚠️ WARNING: FR-012 (Document Version History) has no test coverage
   → Requirement defined in requirement_spec.json
   → User story US-018 exists in jira_tickets.json
   → Code exists in backend/src/controllers/documents.controller.js
   → ❌ No test case found in qa_results.json
   → ACTION: Add test case for document version history API
```

**Sets `pipeline_complete: true`** — Pipeline is done.

---

## 4. Parallel Execution Map

When using Agent Teams mode or DAG execution, agents run in parallel where possible:

```
TIME ──────────────────────────────────────────────────────────►

Phase 1   ┌─ [00 Environment] ─┐
          │                     ├─► Phase 2
          └─ [01 Transcript]  ─┘

Phase 2       [02 Requirement] ──────────────────────► Phase 3

Phase 3   ┌─ [03 Documentation] ─┐
          │                       ├─► Phase 4
          └─ [04 Planning]      ─┘

Phase 4   ┌─ [05 Jira Tickets]  ─┐
          │                       ├─► Phase 5/6
          └─ [06 Architecture]  ─┘

Phase 5       [12 Security] ─────────────────────────► Phase 6
              (optional — skip if disabled)

Phase 6       [07 Code Generation] ──────────────────► Phase 7

Phase 7   ┌─ [08 Testing]           ─┐
          │                           ├─► Phase 8
          └─ [13 Compliance Checker] ─┘
              (optional)

Phase 8       [09 Deployment] ───────────────────────► Phase 9

Phase 9       [10 Summary]
              [14 Cost Estimation]  (optional)
              [11 Feedback Loop]
```

**Speed comparison:**
- Sequential: ~35-45 minutes (one agent at a time)
- Parallel (DAG): ~20-28 minutes (phases run concurrently)

---

## 5. Complete Input/Output Reference

| Agent | Input Files | Output Files |
|-------|------------|-------------|
| 00 Environment | System scan | `outputs/environment_report.json`, `outputs/SETUP_INSTRUCTIONS.md` |
| 01 Transcript | `inputs/transcript.txt` (or multiple .txt) | `outputs/transcripts/structured_meeting_output.json` |
| 02 Requirement | Transcript output | `outputs/requirements/requirement_spec.json` |
| 03 Documentation | Requirement spec | `outputs/documents/documentation_output.json`, `BRD.md`, `FRD.md`, `SOW.md` |
| 04 Planning | Docs + requirements | `outputs/planning/sprint_plan.json` |
| 05 Jira | Sprint plan + requirements + env report | `outputs/jira/jira_tickets.json`, `jira_tickets_readable.md`, `jira_import.csv`, `ticketing_report.md` |
| 06 Architecture | Tickets + requirements | `outputs/architecture/system_design.json`, `HLD.md` |
| 12 Security | Architecture + requirements | `outputs/security/threat_model.json`, `THREAT_MODEL.md` |
| 07 Code | System design + HLD + threat model | `outputs/code/code_output.json`, `backend/`, `frontend/`, `README.md` |
| 08 Testing | Code + tickets + requirements | `outputs/qa/qa_results.json` |
| 13 Compliance | ALL contracts | `outputs/compliance/compliance_matrix.json`, `COMPLIANCE_REPORT.md` |
| 09 Deployment | QA + architecture + code + env report | `outputs/deployment/deployment_output.json`, Dockerfiles, docker-compose.yml, CI/CD, scripts |
| 10 Summary | ALL contracts | `outputs/pipeline_final.json`, `PROJECT_COMPLETE_SUMMARY.md`, `EXECUTIVE_DASHBOARD.md` |
| 14 Cost | Architecture + planning | `outputs/cost/cost_estimation.json`, `COST_BREAKDOWN.md` |
| 11 Feedback | ALL contracts | `outputs/feedback/consistency_report.json`, `REMEDIATION_PLAN.md` |

---

## 6. Sample Interactive Decision Flow

Here is a realistic conversation flow for the TechNova transcript:

```
USER:  Start the SDLC automation pipeline.
       Read .claude/agents/00_environment_agent.md and execute it.

AGENT 00: Scanning system...
          ✓ Git 2.44.0, Node 20.11.0, npm 10.2.3, Python 3.12
          ✗ Docker not found
          ✗ Jira not configured

          🔧 Docker — not detected
            1. Install Docker Desktop
            2. ★ Skip — generate files only
          Which option?

USER:  2

AGENT 00: ☁️ Jira Cloud — not configured
            1. I have Jira credentials
            2. Use GitHub Issues
            3. ★ File-based tickets
          Which option?

USER:  3

AGENT 00: ✅ Environment report saved. Triggering Transcript Agent...

AGENT 01: 📝 Found: inputs/transcript.txt (TechNova Discovery Call)
          Using local file. Parsing transcript...
          ✅ Domain detected: SaaS
          ✅ 5 features, 7 pain points, 6 attendees extracted
          Triggering Requirement Agent...

AGENT 02: (runs autonomously — no decisions needed)
          ✅ 18 FRs, 12 NFRs, 5 modules identified
          Triggering Documentation Agent...

AGENT 03: 📚 Publishing options:
            1. ★ Local files only
            2. Confluence
          Which option?

USER:  1

AGENT 03: ✅ BRD.md, FRD.md, SOW.md generated
          Triggering Planning Agent...

AGENT 04: (runs autonomously)
          ✅ 7 sprints, 16 weeks, team of 7
          Triggering Jira Agent...

AGENT 05: Using file-based tickets (your earlier choice)
          ✅ 5 epics, 23 stories, 68 tasks created
          Triggering Architecture Agent...

AGENT 06: 🏗️ Tech Stack Recommendation:
          ★ Node.js + React + PostgreSQL + JWT
          Go with recommended? (yes/no)

USER:  yes

AGENT 06: ✅ System design + HLD generated
          Triggering Code Agent...

AGENT 07: ⚡ npm init + install deps, SQLite, local git
          Generating backend + frontend code...
          Running npm audit... 0 critical, 1 moderate
          Quality scores: Security 85, Maintainability 78, Performance 82
          ✅ 24 files generated
          Triggering Testing Agent...

AGENT 08: 🧪 Generate test files only? (1)

USER:  1

AGENT 08: ✅ 45 test cases across 8 suites
          Triggering Deployment Agent...

AGENT 09: 🚀 Using Docker + GitHub Actions + cloud-agnostic (your choices)
          ✅ Dockerfiles, docker-compose, CI/CD, scripts generated
          Triggering Summary Agent...

AGENT 10: ✅ PROJECT_COMPLETE_SUMMARY.md (30KB)
          ✅ EXECUTIVE_DASHBOARD.md
          Triggering Feedback Loop Agent...

AGENT 11: Reviewing all outputs for consistency...
          ✅ Consistency Score: 94/100
          ⚠️ 2 warnings, 0 critical issues
          📋 REMEDIATION_PLAN.md generated

          ══════════════════════════════════
          ✅ PIPELINE COMPLETE
          ══════════════════════════════════
          Files generated: 50+
          Time: ~35 minutes
          All outputs in: outputs/
```

---

## 7. What You Get at the End

After the pipeline completes, your `outputs/` directory contains:

```
outputs/
├── environment_report.json              ← System + user preferences
├── transcripts/
│   └── structured_meeting_output.json   ← Parsed transcript (JSON)
├── requirements/
│   └── requirement_spec.json            ← 18 FRs + 12 NFRs
├── documents/
│   ├── documentation_output.json        ← Contract
│   ├── BRD.md                           ← Business Requirements (~15 pages)
│   ├── FRD.md                           ← Functional Requirements (~20 pages)
│   └── SOW.md                           ← Statement of Work (~10 pages)
├── planning/
│   └── sprint_plan.json                 ← 7 sprints, team of 7, 16 weeks
├── jira/
│   ├── jira_tickets.json                ← 5 epics, 23 stories, 68 tasks
│   ├── jira_tickets_readable.md         ← Human-readable ticket list
│   ├── jira_import.csv                  ← Import into any ticketing tool
│   └── ticketing_report.md              ← Ticketing mode + import instructions
├── architecture/
│   ├── system_design.json               ← Tech stack, DB schema, APIs
│   └── HLD.md                           ← High-Level Design document
├── security/                            ← (if threat model enabled)
│   ├── threat_model.json
│   └── THREAT_MODEL.md
├── code/
│   ├── code_output.json                 ← Contract + quality scores
│   ├── README.md                        ← Setup instructions
│   ├── .gitignore
│   ├── backend/
│   │   ├── package.json
│   │   ├── src/app.js
│   │   ├── src/middleware/auth.middleware.js
│   │   ├── src/middleware/audit.middleware.js
│   │   ├── src/config/database.js
│   │   ├── src/controllers/
│   │   ├── src/services/
│   │   ├── src/routes/
│   │   ├── migrations/
│   │   └── .env.example
│   └── frontend/
│       ├── package.json
│       ├── src/App.jsx
│       ├── src/pages/Login.jsx
│       ├── src/pages/Dashboard.jsx
│       ├── src/services/api.service.js
│       ├── src/services/auth.service.js
│       ├── src/hooks/useAuth.js
│       └── src/components/common/ProtectedRoute.jsx
├── qa/
│   └── qa_results.json                  ← 45 test cases, security checklist
├── compliance/                          ← (if compliance checker enabled)
│   ├── compliance_matrix.json
│   └── COMPLIANCE_REPORT.md
├── deployment/
│   ├── deployment_output.json
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── docker-compose.yml
│   ├── github-actions-ci.yml
│   ├── env-template.md
│   ├── production_readiness.md
│   └── scripts/
│       ├── run_backend.sh
│       ├── run_frontend.sh
│       └── setup_database.sh
├── cost/                                ← (if cost estimation enabled)
│   ├── cost_estimation.json
│   └── COST_BREAKDOWN.md
├── feedback/
│   ├── consistency_report.json          ← Cross-cutting consistency review
│   └── REMEDIATION_PLAN.md             ← Action items for gaps
├── analytics/
│   └── pipeline_metrics.json            ← Pipeline run metrics
├── PROJECT_COMPLETE_SUMMARY.md          ← ~30KB comprehensive summary
├── EXECUTIVE_DASHBOARD.md              ← One-page management view
└── pipeline_final.json                  ← Pipeline completion marker
```

**Total: 50+ files covering the entire SDLC from transcript to deployment.**

---

## 8. Alternative Prompts

### Run for a different domain
```
Replace inputs/transcript.txt with your own transcript, then:
Start the SDLC automation pipeline.
Read .claude/agents/00_environment_agent.md and execute it.
```

### Use a sample transcript
```bash
cp inputs/samples/healthcare_transcript.txt inputs/transcript.txt
```
Then trigger the pipeline. It will auto-detect healthcare domain and apply HIPAA compliance.

### Run only specific agents
```
Read .claude/agents/06_architecture_agent.md and execute it.
Input: outputs/jira/jira_tickets.json and outputs/requirements/requirement_spec.json
```

### Run optional agents standalone
```
Run the security threat model agent.
Read .claude/agents/12_security_threat_model_agent.md and execute it.
```

```
Run the cost estimation agent.
Read .claude/agents/14_cost_estimation_agent.md and execute it.
```

### Clean and re-run
```bash
bash scripts/clean_outputs.sh
```
Then trigger the pipeline again.

### Check pipeline analytics after a run
```bash
python helpers/pipeline_analytics.py
```

---

*This guide covers the complete end-to-end flow of the SDLC Automation Pipeline v2.0
with 15 agents, interactive decisions, parallel execution, and 50+ output artifacts.*

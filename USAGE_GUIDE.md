# SDLC Automation — Complete Usage Guide

## What This Is

This is an **end-to-end Software Development Lifecycle (SDLC) automation platform**
powered by Claude Code. It takes a raw client meeting transcript as input and
autonomously produces all project artifacts — from requirements to deployment
configs — using a 10-agent pipeline.

**No manual intervention needed.** You paste a transcript and the pipeline
runs all 10 agents automatically, each handing off to the next.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Quick Start — Run the Pipeline](#2-quick-start)
3. [What the Pipeline Produces](#3-what-the-pipeline-produces)
4. [Sample Use Cases You Can Try](#4-sample-use-cases)
5. [How to Use Each Sample](#5-how-to-use-each-sample)
6. [Running Individual Agents](#6-running-individual-agents)
7. [Resuming a Stopped Pipeline](#7-resuming-a-stopped-pipeline)
8. [Helper Utilities](#8-helper-utilities)
9. [Installed Skills](#9-installed-skills)
10. [Creating Your Own Transcripts](#10-creating-your-own-transcripts)
11. [Agent Teams Mode (Parallel Execution)](#11-agent-teams-mode)
12. [Project Structure Reference](#12-project-structure-reference)
13. [Advanced: Customizing Agents](#13-customizing-agents)
14. [Troubleshooting](#14-troubleshooting)
15. [Use Case Ideas for Demos](#15-use-case-ideas)
16. [SDLC Terminology Reference](#16-sdlc-terminology)

---

## 1. Prerequisites

- **Claude Code CLI** installed with a valid API key
- **Python 3.7+** (for helper utilities — optional but recommended)
- No external Python packages required (standard library only)

### Verify Setup
```bash
claude --version          # Claude Code CLI
python --version          # Python 3.7+
```

---

## 2. Quick Start

### Step 1: Navigate to the project
```bash
cd D:\claude_usecase_tryout\sdlc-automation
```

### Step 2: Verify input file exists
The default transcript is already in place at `inputs/transcript.txt`.
This is a **Digital Agency Project Management Platform** use case.

### Step 3: Run the pre-flight check (optional)
```bash
bash scripts/run_pipeline.sh
```

### Step 4: Start Claude Code and run the pipeline
Open Claude Code in the `sdlc-automation/` directory and paste:

```
Start the SDLC automation pipeline.
Read .claude/agents/01_transcript_agent.md and execute it.
The agent will autonomously trigger all subsequent agents.
```

### Step 5: Watch the pipeline execute
The pipeline will run through all 10 agents:
1. Transcript Agent analyzes the meeting notes
2. Requirement Agent extracts FRs and NFRs
3. Documentation Agent creates BRD, FRD, SOW
4. Planning Agent creates sprint plan
5. Jira Agent creates Epics/Stories/Tasks
6. Architecture Agent designs the system
7. Code Agent generates backend + frontend code
8. Testing Agent creates test plans and cases
9. Deployment Agent creates Docker/CI-CD configs
10. Summary Agent produces the final project summary

### Step 6: Review outputs
All artifacts are in `outputs/`. Start with:
```
outputs/PROJECT_COMPLETE_SUMMARY.md    # Full project summary
outputs/EXECUTIVE_DASHBOARD.md         # One-page management view
```

---

## 3. What the Pipeline Produces

| Agent | Artifacts |
|-------|-----------|
| 01 Transcript | `outputs/transcripts/structured_meeting_output.json` |
| 02 Requirement | `outputs/requirements/requirement_spec.json` |
| 03 Documentation | `outputs/documents/BRD.md`, `FRD.md`, `SOW.md`, `documentation_output.json` |
| 04 Planning | `outputs/planning/sprint_plan.json` |
| 05 Jira | `outputs/jira/jira_tickets.json`, `jira_tickets_readable.md` |
| 06 Architecture | `outputs/architecture/HLD.md`, `system_design.json` |
| 07 Code | `outputs/code/backend/` (full scaffold), `outputs/code/frontend/` (full scaffold) |
| 08 Testing | `outputs/qa/test_plan.md`, `test_cases.md`, `api_test_outlines.md`, `security_checklist.md` |
| 09 Deployment | `outputs/deployment/Dockerfile.*`, `docker-compose.yml`, `github-actions-ci.yml`, `production_readiness.md` |
| 10 Summary | `outputs/PROJECT_COMPLETE_SUMMARY.md`, `EXECUTIVE_DASHBOARD.md`, `pipeline_final.json` |

---

## 4. Sample Use Cases You Can Try

### Default: Digital Agency Platform (Already loaded)
**File**: `inputs/transcript.txt`
**Domain**: SaaS / Professional Services
**Client**: TechNova Solutions — 150-employee digital agency
**They need**: Project management, client portal, time tracking, invoicing, document management
**Complexity**: HIGH

### Sample 1: Healthcare — Hospital Management
**File**: `inputs/samples/healthcare_transcript.txt`
**Domain**: Healthcare
**Client**: MedCare Hospital Network
**They need**: Appointment booking, insurance claim processing, admin dashboard
**Compliance**: HIPAA, MFA mandatory
**Complexity**: HIGH

### Sample 2: E-Commerce — Artisan Marketplace
**File**: `inputs/samples/ecommerce_transcript.txt`
**Domain**: E-Commerce
**Client**: UrbanBazaar Marketplace
**They need**: Multi-vendor marketplace, split payments, seller dashboards, search
**Compliance**: PCI-DSS, GDPR
**Complexity**: HIGH

### Sample 3: Fintech — Lending Platform
**File**: `inputs/samples/fintech_transcript.txt`
**Domain**: Fintech
**Client**: PayWise Financial
**They need**: Automated loan underwriting, KYC/AML, customer portal
**Compliance**: SOC2, PCI-DSS
**Complexity**: VERY_HIGH

### Sample 4: Education — School Management
**File**: `inputs/samples/education_transcript.txt`
**Domain**: Education
**Client**: BrightPath Academy (K-12)
**They need**: Enrollment, attendance, gradebook, parent portal
**Compliance**: FERPA, WCAG 2.1 AA
**Complexity**: MEDIUM

### Sample 5: SaaS — Cloud Cost Analytics
**File**: `inputs/samples/saas_transcript.txt`
**Domain**: SaaS / B2B
**Client**: CloudMetrics Inc.
**They need**: Multi-tenant analytics platform, subscription billing, cloud integrations
**Compliance**: SOC2
**Complexity**: HIGH

---

## 5. How to Use Each Sample

### Option A: Copy the sample to the input file
```bash
# Example: Run the healthcare use case
cp inputs/samples/healthcare_transcript.txt inputs/transcript.txt

# Then start the pipeline in Claude Code:
# "Start the SDLC automation pipeline.
#  Read .claude/agents/01_transcript_agent.md and execute it."
```

### Option B: Clean outputs first for a fresh run
```bash
bash scripts/clean_outputs.sh
cp inputs/samples/ecommerce_transcript.txt inputs/transcript.txt
# Then start the pipeline
```

### Option C: Point the agent to a specific file
```
Read .claude/agents/01_transcript_agent.md and execute it.
But read the input from inputs/samples/fintech_transcript.txt instead of
the default inputs/transcript.txt.
```

---

## 6. Running Individual Agents

You can run any agent independently if its input file exists:

### Run only the Transcript Agent
```
Read .claude/agents/01_transcript_agent.md and execute it.
Stop after writing the output — do NOT trigger the next agent.
```

### Run only the Architecture Agent (if requirements exist)
```
Read .claude/agents/06_architecture_agent.md and execute it.
Input files: outputs/jira/jira_tickets.json and outputs/requirements/requirement_spec.json.
Stop after writing the output.
```

### Run from a specific agent onward
```
Resume the SDLC pipeline from the Planning Agent.
Read outputs/documents/documentation_output.json and execute
.claude/agents/04_planning_agent.md. Let it trigger all subsequent agents.
```

---

## 7. Resuming a Stopped Pipeline

If the pipeline stops at any point (context limit, error, etc.):

### Step 1: Check progress
```bash
python helpers/pipeline_status.py
```

### Step 2: Resume from the last successful agent
The status dashboard tells you which agent to run next. Example:
```
Resume the SDLC pipeline from the Code Agent.
Read outputs/architecture/system_design.json and execute
.claude/agents/07_code_agent.md. Let it trigger all subsequent agents.
```

---

## 8. Helper Utilities

### Pipeline Status Dashboard
```bash
python helpers/pipeline_status.py
```
Shows which agents have completed, which are pending, and the next agent to run.

### Contract Validation
```bash
python helpers/contract_validator.py              # Validate all
python helpers/contract_validator.py testing_agent # Validate one
```
Checks that all output JSON files have the correct structure.

### Output Report
```bash
python helpers/output_reporter.py
```
Shows all files created by the pipeline with sizes.

### Clean Outputs (Fresh Run)
```bash
bash scripts/clean_outputs.sh
```
Removes all generated files so you can start a fresh pipeline run.

### Pre-flight Check
```bash
bash scripts/run_pipeline.sh
```
Verifies all prerequisites are in place before starting.

---

## 9. Installed Skills

These skills from [skills.sh](https://skills.sh) are installed and available:

| Skill | What It Does | When to Use |
|-------|-------------|-------------|
| **frontend-design** | Creates production-grade UI with distinctive design | When the Code Agent generates frontend, or for standalone UI work |
| **pdf** | Read, create, merge, split PDFs | Export BRD/FRD/SOW as PDF |
| **docx** | Create/edit Word documents | Generate formal client documents |
| **xlsx** | Create/edit spreadsheets | Generate sprint plans or ticket exports as Excel |
| **pptx** | Create presentations | Generate project presentations for stakeholders |
| **webapp-testing** | Test web apps with Playwright | Test the generated frontend code |
| **mcp-builder** | Build MCP servers | Create custom tool integrations |
| **skill-creator** | Create new skills | Build domain-specific skills |
| **doc-coauthoring** | Co-author documentation | Iterate on BRD/FRD with refinements |
| **internal-comms** | Write internal communications | Generate status reports, updates |
| **web-artifacts-builder** | Build complex web artifacts | Create interactive dashboards |

### Using Skills After Pipeline

After the pipeline completes, you can use skills for additional work:

```
# Generate a PDF of the BRD
/pdf Create a PDF from outputs/documents/BRD.md

# Generate a PowerPoint presentation of the project summary
/pptx Create a presentation from outputs/PROJECT_COMPLETE_SUMMARY.md

# Export Jira tickets to Excel
/xlsx Create a spreadsheet from outputs/jira/jira_tickets.json

# Generate a Word document for the SOW
/docx Create a formal Word document from outputs/documents/SOW.md

# Test the generated frontend
/webapp-testing Test the frontend at outputs/code/frontend/

# Create a project status report
/internal-comms Write a status report based on outputs/PROJECT_COMPLETE_SUMMARY.md
```

---

## 10. Creating Your Own Transcripts

To run the pipeline with your own client meeting, create a transcript file with
this structure:

```
Meeting Date: [date]
Duration: [minutes] minutes
Location: [Virtual/In-person platform]
Project: Client Discovery Call — [Client Name]

Attendees:
- [Name] ([Role], [Company] — Client)
- [Name] ([Role], Our Team)

---

[Conversational transcript of the meeting]

Open Questions:
- [List of unresolved questions]

Decisions Made:
- [List of agreed decisions]
```

### Tips for Good Transcripts
- Include specific pain points with quotes
- Mention compliance requirements explicitly
- Include timeline and budget if discussed
- List technology preferences or existing systems
- Capture user counts and scale expectations
- Include Phase 1 vs Phase 2 scope decisions

Save your transcript to `inputs/transcript.txt` and run the pipeline.

---

## 11. Agent Teams Mode (Parallel Execution)

Claude Code has an experimental **Agent Teams** feature that lets you run
multiple agents as separate teammates in parallel. Instead of a sequential
chain, a Team Lead coordinates multiple teammates.

### Enable Agent Teams
Already configured in `.claude/settings.json`:
```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

### Start the Pipeline with Agent Teams
```
I need to run the SDLC automation pipeline using Agent Teams.

Create an agent team with 4 teammates:
1. "Business Analyst" — runs agents 01, 02, 03 sequentially
2. "Project Planner" — waits for BA, then runs agents 04, 05
3. "Tech Lead" — waits for Planner, then runs agents 06, 07
4. "QA & DevOps" — waits for Tech Lead, then runs agents 08, 09, 10

The input file is inputs/transcript.txt.
Each agent reads its .claude/agents/NN_*.md file for instructions.
Agents communicate through JSON files in the outputs/ directory.
```

### Agent Teams vs Sequential Pipeline
| Aspect | Sequential | Agent Teams |
|--------|-----------|-------------|
| Speed | Slower | Faster (parallel) |
| Token Usage | Lower | Higher |
| Coordination | Automatic JSON chain | Team Lead manages |
| Best For | Full runs | Speed + debate |

For full Agent Teams documentation, see `.claude/agents/AGENT_TEAMS_MODE.md`.

---

## 12. Project Structure Reference

```
sdlc-automation/
├── .claude/
│   ├── agents/                   ← 10 agent definitions + protocol
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
│   ├── skills/
│   │   ├── sdlc-process/         ← 5 methodology skills
│   │   ├── pipeline/             ← 2 pipeline mechanics skills
│   │   └── domain-adaptation/    ← Domain-specific rules
│   ├── hooks/                    ← 2 quality gate hooks
│   ├── rules/pipeline_rules.md
│   └── settings.json
├── helpers/                      ← 3 Python utilities
├── scripts/                      ← 3 bash scripts
├── inputs/
│   ├── transcript.txt            ← Main input (active use case)
│   └── samples/                  ← 5 sample transcripts
├── outputs/                      ← All generated artifacts (10 dirs)
├── CLAUDE.md                     ← Master instruction file
├── README.md                     ← Quick start guide
├── USAGE_GUIDE.md                ← This file
└── requirements.txt
```

---

## 13. Customizing Agents

### Modify an Agent's Behavior
Edit any `.claude/agents/NN_*.md` file to change:
- What the agent extracts or produces
- The JSON output structure
- Domain-specific rules
- Quality checks

### Add a New Agent
1. Create `.claude/agents/NN_new_agent.md`
2. Update the handoff in the previous agent
3. Update the communication protocol
4. Add the agent to `helpers/pipeline_status.py` and `helpers/contract_validator.py`

### Add Domain Rules
Edit `.claude/skills/domain-adaptation/domain_rules.md` to add new domains
or modify existing domain-specific requirements.

---

## 14. Troubleshooting

### Pipeline stops mid-execution
- Check progress: `python helpers/pipeline_status.py`
- Resume from the last completed agent (see Section 7)

### "Agent not found" error
- Ensure you're in the `sdlc-automation/` directory
- Check `.claude/agents/` has all 10 agent files

### Output validation fails
- Run: `python helpers/contract_validator.py`
- Check which agent produced invalid output
- Re-run that specific agent

### Pipeline produces healthcare-specific output
- The pipeline is domain-agnostic — it auto-detects from the transcript
- Ensure your transcript clearly describes the domain context

---

## 15. Use Case Ideas for Demos

Here are additional use case ideas you can create transcripts for:

| # | Domain | Use Case | Key Features |
|---|--------|----------|-------------|
| 1 | **HR Tech** | Employee Management Platform | Onboarding, leave mgmt, payroll, org chart, performance reviews |
| 2 | **Logistics** | Fleet Management System | Real-time tracking, route optimization, driver scheduling, maintenance |
| 3 | **Real Estate** | Property Management Portal | Listings, tenant portal, lease mgmt, maintenance requests, payments |
| 4 | **Government** | Citizen Services Portal | Permit applications, document requests, payment processing, case tracking |
| 5 | **Legal** | Case Management System | Client intake, case tracking, document management, billing, court dates |
| 6 | **Manufacturing** | Quality Control Platform | Inspection tracking, defect reporting, compliance, supply chain |
| 7 | **Travel** | Booking Platform | Hotel/flight search, bookings, reviews, loyalty program, payments |
| 8 | **Media** | Content Management System | Article publishing, media library, editorial workflow, analytics |
| 9 | **Agriculture** | Farm Management Platform | Crop tracking, IoT sensors, weather integration, market prices |
| 10 | **Nonprofit** | Donor Management CRM | Donor tracking, campaign management, event planning, reporting |
| 11 | **Restaurant** | Restaurant Management Suite | Online ordering, table reservations, kitchen display, inventory |
| 12 | **Fitness** | Gym Management Platform | Membership, class booking, trainer scheduling, payment, progress tracking |
| 13 | **Insurance** | Claims Processing System | Policy management, claims intake, adjudication, payments, fraud detection |
| 14 | **Construction** | Project Management Platform | Bidding, scheduling, resource allocation, inspection, compliance |
| 15 | **Telecom** | Customer Portal | Plan management, billing, support tickets, usage analytics |

### How to Create a New Use Case
1. Write a meeting transcript following the format in Section 10
2. Save to `inputs/samples/your_domain_transcript.txt`
3. Copy to `inputs/transcript.txt`
4. Clean outputs: `bash scripts/clean_outputs.sh`
5. Run the pipeline

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| **Run pipeline** | `Start the SDLC automation pipeline. Read .claude/agents/01_transcript_agent.md and execute it.` |
| **Check status** | `python helpers/pipeline_status.py` |
| **Validate outputs** | `python helpers/contract_validator.py` |
| **View output report** | `python helpers/output_reporter.py` |
| **Clean for fresh run** | `bash scripts/clean_outputs.sh` |
| **Switch use case** | `cp inputs/samples/<domain>_transcript.txt inputs/transcript.txt` |
| **Resume pipeline** | `Resume from [agent_name]. Read outputs/[file].json and execute .claude/agents/[NN_agent].md` |
| **Run single agent** | `Read .claude/agents/[NN_agent].md and execute it. Stop after writing output.` |
| **Agent Teams mode** | See Section 11 or `.claude/agents/AGENT_TEAMS_MODE.md` |

---

## 16. SDLC Terminology Reference

For a complete guide to all SDLC terminology (what is BRD, FRD, SOW, Sprint,
Epic, Story, CI/CD, environments, etc.) and how IT companies really work,
see **`SDLC_TERMINOLOGY_GUIDE.md`** in this project root.

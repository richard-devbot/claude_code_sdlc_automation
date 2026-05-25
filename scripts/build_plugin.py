#!/usr/bin/env python3
"""
Build the SDLC Automation Plugin.

Reads the existing claude-sdlc-pipeline.plugin as the base, injects all
new SDLC pipeline commands (agent triggers + orchestrator controls), updates
the manifest, and writes sdlc-automation.plugin.

Usage:
    python scripts/build_plugin.py
    python scripts/build_plugin.py --output my-custom-name.plugin
"""

import argparse
import json
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXISTING_PLUGIN = PROJECT_ROOT / "claude-sdlc-pipeline.plugin"
DEFAULT_OUTPUT = PROJECT_ROOT / "sdlc-automation.plugin"

# ── Plugin manifest ────────────────────────────────────────────────────────────

PLUGIN_JSON = {
    "name": "sdlc-automation",
    "version": "3.0.0",
    "description": (
        "End-to-end SDLC automation pipeline. "
        "Turn a single client meeting transcript into requirements, sprint plans, "
        "architecture, code scaffolding, test plans, security threat models, "
        "compliance checks, cost estimates, and deployment configs — for any industry. "
        "Works in Claude.ai web and Claude Desktop."
    ),
    "author": {
        "name": "Richardson Gunde",
        "email": "rgunde@evoketechnologies.com",
    },
    "homepage": "https://github.com/Evoke-Technologies/claude-sdlc-pipeline",
    "license": "MIT",
    "keywords": [
        "sdlc", "automation", "agents", "pipeline", "requirements",
        "architecture", "jira", "devops", "security", "cowork", "claude-code",
    ],
}

# ── Agent metadata ─────────────────────────────────────────────────────────────

AGENTS = [
    {
        "id":       "environment_agent",
        "num":      "00",
        "file":     "00_environment_agent.md",
        "cmd":      "sdlc-env",
        "label":    "Environment Setup Agent",
        "role":     "System Scanner",
        "desc":     "Scan tools, set up environment, create environment_report.json",
        "output":   "outputs/environment_report.json",
        "inputs":   [],
        "optional": False,
    },
    {
        "id":       "transcript_agent",
        "num":      "01",
        "file":     "01_transcript_agent.md",
        "cmd":      "sdlc-transcript",
        "label":    "Transcript Agent",
        "role":     "Business Analyst",
        "desc":     "Parse meeting transcript → structured JSON with domain, features, pain points",
        "output":   "outputs/transcripts/structured_meeting_output.json",
        "inputs":   ["inputs/transcript.txt"],
        "optional": False,
    },
    {
        "id":       "requirement_agent",
        "num":      "02",
        "file":     "02_requirement_agent.md",
        "cmd":      "sdlc-requirements",
        "label":    "Requirements Agent",
        "role":     "Senior Business Analyst",
        "desc":     "Extract functional + non-functional requirements with traceability IDs",
        "output":   "outputs/requirements/requirement_spec.json",
        "inputs":   ["outputs/transcripts/structured_meeting_output.json"],
        "optional": False,
    },
    {
        "id":       "documentation_agent",
        "num":      "03",
        "file":     "03_documentation_agent.md",
        "cmd":      "sdlc-docs",
        "label":    "Documentation Agent",
        "role":     "Technical Writer",
        "desc":     "Generate BRD, FRD, SOW documents from requirements",
        "output":   "outputs/documents/documentation_output.json",
        "inputs":   ["outputs/requirements/requirement_spec.json"],
        "optional": False,
    },
    {
        "id":       "planning_agent",
        "num":      "04",
        "file":     "04_planning_agent.md",
        "cmd":      "sdlc-planning",
        "label":    "Planning Agent",
        "role":     "Project Manager",
        "desc":     "Create sprint plan, timeline, team composition, milestones",
        "output":   "outputs/planning/sprint_plan.json",
        "inputs":   ["outputs/requirements/requirement_spec.json"],
        "optional": False,
    },
    {
        "id":       "jira_agent",
        "num":      "05",
        "file":     "05_jira_agent.md",
        "cmd":      "sdlc-tickets",
        "label":    "Ticketing Agent",
        "role":     "Scrum Master",
        "desc":     "Create Epic → Story → Task hierarchy (Jira / GitHub Issues / file-based)",
        "output":   "outputs/jira/jira_tickets.json",
        "inputs":   ["outputs/planning/sprint_plan.json", "outputs/requirements/requirement_spec.json"],
        "optional": False,
    },
    {
        "id":       "architecture_agent",
        "num":      "06",
        "file":     "06_architecture_agent.md",
        "cmd":      "sdlc-architecture",
        "label":    "Architecture Agent",
        "role":     "Solution Architect",
        "desc":     "Design system architecture, API contracts, DB schema, HLD",
        "output":   "outputs/architecture/system_design.json",
        "inputs":   ["outputs/jira/jira_tickets.json", "outputs/requirements/requirement_spec.json"],
        "optional": False,
    },
    {
        "id":       "security_threat_model_agent",
        "num":      "12",
        "file":     "12_security_threat_model_agent.md",
        "cmd":      "sdlc-security",
        "label":    "Security Threat Model Agent",
        "role":     "Security Engineer",
        "desc":     "STRIDE threat model + OWASP Top 10 analysis before code is written",
        "output":   "outputs/security/threat_model.json",
        "inputs":   ["outputs/architecture/system_design.json"],
        "optional": True,
    },
    {
        "id":       "code_agent",
        "num":      "07",
        "file":     "07_code_agent.md",
        "cmd":      "sdlc-code",
        "label":    "Code Generation Agent",
        "role":     "Senior Developer",
        "desc":     "Generate production-ready code scaffolding for the full tech stack",
        "output":   "outputs/code/code_output.json",
        "inputs":   ["outputs/architecture/system_design.json"],
        "optional": False,
    },
    {
        "id":       "testing_agent",
        "num":      "08",
        "file":     "08_testing_agent.md",
        "cmd":      "sdlc-testing",
        "label":    "Testing Agent",
        "role":     "QA Lead",
        "desc":     "Generate test plan, test cases, API tests, security checklist + auto-fix loop",
        "output":   "outputs/qa/qa_results.json",
        "inputs":   ["outputs/code/code_output.json"],
        "optional": False,
    },
    {
        "id":       "compliance_checker_agent",
        "num":      "13",
        "file":     "13_compliance_checker_agent.md",
        "cmd":      "sdlc-compliance",
        "label":    "Compliance Checker Agent",
        "role":     "Compliance Engineer",
        "desc":     "HIPAA / GDPR / PCI-DSS / SOC 2 gap analysis against pipeline artifacts",
        "output":   "outputs/compliance/compliance_matrix.json",
        "inputs":   ["outputs/requirements/requirement_spec.json", "outputs/architecture/system_design.json"],
        "optional": True,
    },
    {
        "id":       "deployment_agent",
        "num":      "09",
        "file":     "09_deployment_agent.md",
        "cmd":      "sdlc-deploy",
        "label":    "Deployment Agent",
        "role":     "DevOps Engineer",
        "desc":     "Generate Dockerfiles, CI/CD pipelines, IaC templates, optional live deploy",
        "output":   "outputs/deployment/deployment_output.json",
        "inputs":   ["outputs/qa/qa_results.json", "outputs/architecture/system_design.json"],
        "optional": False,
    },
    {
        "id":       "cost_estimation_agent",
        "num":      "14",
        "file":     "14_cost_estimation_agent.md",
        "cmd":      "sdlc-cost",
        "label":    "Cost Estimation Agent",
        "role":     "FinOps Architect",
        "desc":     "Cloud cost forecast (AWS/Azure/GCP) with Excel/PDF output for stakeholders",
        "output":   "outputs/cost/cost_estimation.json",
        "inputs":   ["outputs/architecture/system_design.json"],
        "optional": True,
    },
    {
        "id":       "summary_agent",
        "num":      "10",
        "file":     "10_summary_agent.md",
        "cmd":      "sdlc-summary",
        "label":    "Summary Agent",
        "role":     "Delivery Lead",
        "desc":     "Executive dashboard, full project summary, artifact inventory",
        "output":   "outputs/pipeline_final.json",
        "inputs":   ["outputs/deployment/deployment_output.json"],
        "optional": False,
    },
    {
        "id":       "feedback_loop_agent",
        "num":      "11",
        "file":     "11_feedback_loop_agent.md",
        "cmd":      "sdlc-feedback",
        "label":    "Feedback Loop Agent",
        "role":     "QA Auditor",
        "desc":     "Cross-pipeline consistency review, traceability matrix, remediation plan",
        "output":   "outputs/feedback/consistency_report.json",
        "inputs":   ["outputs/pipeline_final.json"],
        "optional": True,
    },
]

# ── Shared shell snippet — finds scripts/helpers in project OR plugin install ──

# Injected into every command that calls scripts/ or helpers/.
# Priority: local project copy → plugin marketplace install → plugin cache.
_PATH_RESOLVER = """\
!`python3 -c "
import pathlib, sys, os

def find_sdlc_root():
    # 1. Local project copy (preferred — user ran /sdlc-setup)
    local = pathlib.Path('scripts/orchestrator.py')
    if local.exists():
        return pathlib.Path('.').resolve()
    # 2. Search all known plugin install locations
    for base in [
        pathlib.Path.home() / '.claude/plugins/marketplaces',
        pathlib.Path.home() / '.claude/plugins/data',
        pathlib.Path.home() / '.claude/plugins/cache',
    ]:
        for p in base.rglob('sdlc-automation/scripts/orchestrator.py'):
            return p.parent.parent
    return None

root = find_sdlc_root()
if root:
    os.environ['SDLC_ROOT'] = str(root)
    print(f'SDLC_ROOT={root}')
else:
    print('SDLC_ROOT=NOT_FOUND — run /sdlc-setup first')
" 2>/dev/null`
"""

# ── Command generators ─────────────────────────────────────────────────────────

def _agent_command(agent: dict) -> str:
    """Generate the command markdown for a single agent trigger."""
    inputs_section = ""
    if agent["inputs"]:
        items = "\n".join(f"- `{i}`" for i in agent["inputs"])
        inputs_section = f"\n**Expected inputs:**\n{items}\n"

    optional_tag = " *(optional)*" if agent["optional"] else ""
    # Use path-resolver so harness.py is found whether local or in plugin dir
    harness_check = (
        f"!`SDLC_HELPERS=$(python3 -c \""
        f"import pathlib; paths=[pathlib.Path('helpers'), *pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/helpers')]; "
        f"print(next((str(p) for p in paths if (p/'harness.py').exists()), 'helpers'))\""
        f" 2>/dev/null); python3 $SDLC_HELPERS/harness.py pre {agent['id']} 2>&1 || echo '[harness] input check skipped'`\n\n"
        if agent["inputs"] else ""
    )

    return f"""---
allowed-tools: Read, Write, Edit, Bash
description: "{agent['label']} — {agent['desc']}"
---

# {agent['label']} (Agent {agent['num']}){optional_tag}

**Role:** {agent['role']}
**Output:** `{agent["output"]}`
{inputs_section}
{harness_check}Read the agent instructions and execute them:

@agents/{agent["file"]}

> **Isolated mode:** Write your output JSON contract to `{agent["output"]}` and stop.
> Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
>
> **Web Claude fallback:** If `@` file references are not supported, read the file
> `.claude/agents/{agent["file"]}` using the Read tool and follow all instructions.
"""


def _setup_command() -> str:
    return """\
---
allowed-tools: Bash, Read, Write
description: "Bootstrap SDLC pipeline in this project — copies helpers, scripts, config from plugin install"
---

# SDLC Setup — Bootstrap This Project

Copies `helpers/`, `scripts/`, and `sdlc-pipeline.yml` from the plugin install directory
into your current project, then creates the `inputs/` and `outputs/` directory structure.

**Run this once after installing the plugin in a new project.**

!`python3 - <<'SETUP_EOF'
import pathlib, shutil, sys, os

cwd = pathlib.Path.cwd()

def find_plugin_root():
    for base in [
        pathlib.Path.home() / ".claude/plugins/marketplaces",
        pathlib.Path.home() / ".claude/plugins/data",
        pathlib.Path.home() / ".claude/plugins/cache",
    ]:
        for p in base.rglob("sdlc-automation/scripts/orchestrator.py"):
            return p.parent.parent
    return None

plugin_root = find_plugin_root()
if not plugin_root:
    print("ERROR: sdlc-automation plugin not found. Install with:")
    print("  claude plugin marketplace add richard-devbot/claude_code_sdlc_automation")
    print("  claude plugin install sdlc-automation@claude_code_sdlc_automation")
    sys.exit(1)

print(f"Plugin found: {plugin_root}")
copied = []

# Copy helpers/
src_helpers = plugin_root / "helpers"
dst_helpers = cwd / "helpers"
if src_helpers.exists():
    dst_helpers.mkdir(exist_ok=True)
    for f in src_helpers.glob("*.py"):
        shutil.copy2(f, dst_helpers / f.name)
        copied.append(f"helpers/{f.name}")

# Copy scripts/
src_scripts = plugin_root / "scripts"
dst_scripts = cwd / "scripts"
if src_scripts.exists():
    dst_scripts.mkdir(exist_ok=True)
    for f in src_scripts.iterdir():
        shutil.copy2(f, dst_scripts / f.name)
        copied.append(f"scripts/{f.name}")

# Copy sdlc-pipeline.yml (only if not already present)
src_yml = plugin_root / "sdlc-pipeline.yml"
dst_yml = cwd / "sdlc-pipeline.yml"
if src_yml.exists() and not dst_yml.exists():
    shutil.copy2(src_yml, dst_yml)
    copied.append("sdlc-pipeline.yml")

# Create inputs/ and outputs/ directory structure
(cwd / "inputs").mkdir(exist_ok=True)
(cwd / "inputs" / "samples").mkdir(exist_ok=True)
for d in ["transcripts","requirements","documents","planning","jira","architecture",
          "code","qa","deployment","security","compliance","cost","feedback","analytics"]:
    out_dir = cwd / "outputs" / d
    out_dir.mkdir(parents=True, exist_ok=True)
    keep = out_dir / ".gitkeep"
    if not keep.exists():
        keep.touch()

# Create transcript placeholder if missing
transcript = cwd / "inputs" / "transcript.txt"
if not transcript.exists():
    transcript.write_text("# Paste your client meeting transcript here\\n")
    copied.append("inputs/transcript.txt (placeholder)")

print(f"\\nSetup complete! Copied {len(copied)} files:")
for f in copied:
    print(f"  + {f}")
print("\\nNext step: add your transcript to inputs/transcript.txt")
print("Then run: /sdlc-start")
SETUP_EOF`
"""


def _update_command() -> str:
    return """\
---
allowed-tools: Bash
description: "Update the SDLC plugin to the latest version from GitHub main branch"
---

# SDLC Update — Pull Latest from GitHub

Updates the plugin (commands + agents) from the `main` branch of the GitHub repo,
then refreshes the helpers and scripts in your current project.

**Step 1 — Refresh marketplace cache from GitHub:**
!`claude plugin marketplace update claude_code_sdlc_automation 2>&1`

**Step 2 — Reinstall the plugin at the latest version:**
!`claude plugin update sdlc-automation@claude_code_sdlc_automation 2>&1`

**Step 3 — Refresh helpers and scripts in this project:**
!`python3 - <<'UPDATE_EOF'
import pathlib, shutil, sys

cwd = pathlib.Path.cwd()

def find_plugin_root():
    for base in [
        pathlib.Path.home() / ".claude/plugins/marketplaces",
        pathlib.Path.home() / ".claude/plugins/data",
        pathlib.Path.home() / ".claude/plugins/cache",
    ]:
        for p in base.rglob("sdlc-automation/scripts/orchestrator.py"):
            return p.parent.parent
    return None

plugin_root = find_plugin_root()
if not plugin_root:
    print("Plugin not found in install locations. Run /sdlc-setup first.")
    sys.exit(1)

updated = []
for src_dir, dst_dir in [
    (plugin_root / "helpers", cwd / "helpers"),
    (plugin_root / "scripts", cwd / "scripts"),
]:
    if src_dir.exists() and dst_dir.exists():
        for f in src_dir.iterdir():
            shutil.copy2(f, dst_dir / f.name)
            updated.append(f"{dst_dir.name}/{f.name}")

# Update sdlc-pipeline.yml only if the user has the default (no local edits)
dst_yml = cwd / "sdlc-pipeline.yml"
src_yml = plugin_root / "sdlc-pipeline.yml"
if dst_yml.exists() and src_yml.exists():
    if dst_yml.read_bytes() != src_yml.read_bytes():
        backup = cwd / "sdlc-pipeline.yml.bak"
        shutil.copy2(dst_yml, backup)
        print(f"Your sdlc-pipeline.yml has local edits — backed up to sdlc-pipeline.yml.bak")
        print("Review the backup and merge any custom settings into the updated file.")
    shutil.copy2(src_yml, dst_yml)
    updated.append("sdlc-pipeline.yml")

print(f"Updated {len(updated)} files:")
for f in updated:
    print(f"  ~ {f}")
print("\\nRestart Claude Code to apply the updated commands and agents.")
UPDATE_EOF`

---

> **Note:** Restart Claude Code after updating for new commands and agents to take effect.
>
> To see what changed: visit https://github.com/richard-devbot/claude_code_sdlc_automation/commits/main
"""


def _pipeline_start_command() -> str:
    return """\
---
allowed-tools: Read, Write, Edit, Bash
description: "Start the full SDLC pipeline — interactive mode (agents chain autonomously)"
argument-hint: [--express | --replay]
---

# Start SDLC Automation Pipeline

First time in this project? Run `/sdlc-setup` to copy helpers and scripts.

Place your client meeting transcript in `inputs/transcript.txt`, then start:

!`bash scripts/run_pipeline.sh 2>/dev/null || python3 -c "
import pathlib, sys
for base in [pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/scripts/run_pipeline.sh')]:
    for p in base:
        import subprocess; subprocess.run(['bash', str(p)]); sys.exit()
print('Run /sdlc-setup first, then retry /sdlc-start')
"`

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
"""


def _orch_cmd(flag: str) -> str:
    """Return a shell snippet that runs orchestrator.py with the given flag,
    finding it in the local project or the plugin install dir."""
    return (
        f'!`python3 -c "'
        f"import pathlib, subprocess, sys; "
        f"paths = [pathlib.Path('scripts/orchestrator.py'), "
        f"*pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/scripts/orchestrator.py')]; "
        f"orch = next((p for p in paths if p.exists()), None); "
        f"(subprocess.run(['python3', str(orch), '{flag}']) if orch else "
        f"print('Run /sdlc-setup first to install helpers and scripts.'))"
        f'"`'
    )


def _parallel_command() -> str:
    return f"""\
---
allowed-tools: Bash, Read
description: "Run SDLC pipeline in parallel DAG mode — each agent gets a fresh context window"
---

# SDLC Pipeline — Parallel DAG Mode

Each agent runs as an isolated subprocess with a **fresh 200K context window**.
Agents within the same phase run concurrently. JSON contracts on disk are the
only communication channel.

> First time? Run `/sdlc-setup` to copy the scripts into this project.

{_orch_cmd('--mode parallel')}


---

## How parallel mode works

```
Phase 1 (parallel):   environment_agent ∥ transcript_agent
Phase 2 (sequential): requirement_agent
Phase 3 (parallel):   documentation_agent ∥ planning_agent
Phase 4 (parallel):   jira_agent ∥ architecture_agent
Phase 5 (optional):   security_threat_model_agent
Phase 6 (sequential): code_agent
Phase 7 (parallel):   testing_agent ∥ compliance_checker_agent
Phase 8 (sequential): deployment_agent
Phase 9 (sequential): summary_agent → cost_estimation_agent → feedback_loop_agent
```

Each agent in the same phase runs in its own `claude -p` process — no context
accumulation, no compaction mid-pipeline.

## Claude.ai web fallback

If shell commands are not available, use `/sdlc-start` to run interactively.
"""


def _sequential_command() -> str:
    return f"""\
---
allowed-tools: Bash, Read
description: "Run SDLC pipeline sequentially — one agent at a time, fresh context per agent"
---

# SDLC Pipeline — Sequential Mode

Each agent runs as an isolated subprocess — fresh context window per agent.
Agents run one at a time (safer for debugging, easier to resume).

> First time? Run `/sdlc-setup` to copy the scripts into this project.

{_orch_cmd('--mode sequential')}


---

## Use sequential mode when

- Debugging a specific phase (easier to see exactly what each agent did)
- Resources are limited (parallel spawns multiple Claude sessions)
- First run on a new project (sequential is more predictable)

Switch to parallel after validating the pipeline works end-to-end.

## Claude.ai web fallback

If shell commands are not available, use `/sdlc-start` to run interactively.
"""


def _status_command() -> str:
    return f"""\
---
allowed-tools: Bash, Read
description: "Show current SDLC pipeline status — which agents completed, which are pending"
---

# SDLC Pipeline — Status

{_orch_cmd('--status')}

## Legend

- `[OK]` — Agent completed and output contract is valid
- `[  ]` — Agent has not run yet (or contract is missing/invalid)

## Detailed status

!`python3 -c "import pathlib,subprocess,sys; paths=[pathlib.Path('helpers/pipeline_status.py'), *pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/helpers/pipeline_status.py')]; p=next((x for x in paths if x.exists()),None); subprocess.run(['python3',str(p)]) if p else print('Run /sdlc-setup first')"`
"""


def _resume_command() -> str:
    return f"""\
---
allowed-tools: Bash, Read
description: "Resume SDLC pipeline from a specific agent"
argument-hint: <agent-name-or-number>
---

# SDLC Pipeline — Resume

Resume the pipeline starting from the specified agent.
All agents before it are assumed to have completed (their JSON contracts exist).

!`python3 -c "import pathlib,subprocess,sys; paths=[pathlib.Path('scripts/orchestrator.py'), *pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/scripts/orchestrator.py')]; orch=next((p for p in paths if p.exists()),None); subprocess.run(['python3',str(orch),'--resume-from','$ARGUMENTS']) if orch else print('Run /sdlc-setup first')"`

---

## Examples

```
/sdlc-resume code_agent
/sdlc-resume 07_code_agent
/sdlc-resume deployment_agent
```

## Manual resume (web fallback)

If shell commands are not available, read the agent file directly:

"Resume the SDLC pipeline from [agent].
Read outputs/[previous_output].json and execute .claude/agents/[NN_agent].md"

## Agent reference

| # | Agent ID | Resume from |
|---|----------|-------------|
| 00 | environment_agent | `/sdlc-resume environment_agent` |
| 01 | transcript_agent | `/sdlc-resume transcript_agent` |
| 02 | requirement_agent | `/sdlc-resume requirement_agent` |
| 03 | documentation_agent | `/sdlc-resume documentation_agent` |
| 04 | planning_agent | `/sdlc-resume planning_agent` |
| 05 | jira_agent | `/sdlc-resume jira_agent` |
| 06 | architecture_agent | `/sdlc-resume architecture_agent` |
| 12 | security_threat_model_agent | `/sdlc-resume security_threat_model_agent` |
| 07 | code_agent | `/sdlc-resume code_agent` |
| 08 | testing_agent | `/sdlc-resume testing_agent` |
| 13 | compliance_checker_agent | `/sdlc-resume compliance_checker_agent` |
| 09 | deployment_agent | `/sdlc-resume deployment_agent` |
| 14 | cost_estimation_agent | `/sdlc-resume cost_estimation_agent` |
| 10 | summary_agent | `/sdlc-resume summary_agent` |
| 11 | feedback_loop_agent | `/sdlc-resume feedback_loop_agent` |
"""


def _single_agent_command() -> str:
    return f"""\
---
allowed-tools: Bash, Read, Write, Edit
description: "Run a single SDLC agent in isolation with a fresh context window"
argument-hint: <agent-name-or-number>
---

# SDLC — Run Single Agent

Runs exactly one agent in isolation as a fresh `claude -p` subprocess.
The agent reads its inputs from disk, does its work, writes its JSON contract,
and exits. The pipeline does not continue automatically.

!`python3 -c "import pathlib,subprocess,sys; paths=[pathlib.Path('scripts/orchestrator.py'), *pathlib.Path.home().glob('.claude/plugins/**/sdlc-automation/scripts/orchestrator.py')]; orch=next((p for p in paths if p.exists()),None); subprocess.run(['python3',str(orch),'--mode','single','--agent','$ARGUMENTS']) if orch else print('Run /sdlc-setup first')"`

---

## Examples

```
/sdlc-agent architecture_agent
/sdlc-agent 06_architecture_agent
/sdlc-agent security_threat_model_agent
```

## Use cases

- Re-run a single failed agent without running the whole pipeline
- Test a new agent version in isolation
- Run optional agents (cost estimation, compliance) on demand
"""


def _clean_outputs_command() -> str:
    return """\
---
allowed-tools: Bash
description: "Clean all pipeline outputs for a fresh run"
---

# SDLC — Clean Outputs

Remove all generated pipeline outputs to start fresh.
Your input transcript (`inputs/transcript.txt`) is preserved.

!`bash scripts/clean_outputs.sh`

> **Warning:** This deletes all outputs. Run `/sdlc-status` first to confirm
> you want to discard the current pipeline run.
"""


# ── README ────────────────────────────────────────────────────────────────────

def _readme() -> str:
    return """\
# sdlc-automation — Claude Code Plugin v3.0

End-to-end SDLC automation pipeline. Drop in a single client meeting transcript
and 15 cooperating agents produce:

- Requirements (BRD, FRD, SOW)
- Sprint plan + Jira/GitHub tickets
- System architecture + API contracts
- Production-ready code scaffolding
- Test plans + auto-fix loop
- Security threat model (STRIDE/OWASP)
- Compliance matrix (HIPAA, GDPR, PCI-DSS, SOC 2)
- Deployment configs (Docker, CI/CD, IaC)
- Cloud cost forecast
- Executive dashboard

Works in **Claude.ai web** and **Claude Desktop / Claude Code**.

---

## Quick Start

1. Place your meeting transcript in `inputs/transcript.txt`
2. In Claude Code, type `/sdlc-start` — or run `bash scripts/run_pipeline.sh`
3. Choose a mode: **parallel** (fast), **sequential** (safe), or **interactive** (steered)

---

## Commands

### Pipeline Control
| Command | Description |
|---------|-------------|
| `/sdlc-start` | Start full pipeline (interactive, agents chain autonomously) |
| `/sdlc-parallel` | Run in parallel DAG mode (fastest, fresh context per agent) |
| `/sdlc-sequential` | Run sequentially (one agent at a time, easiest to debug) |
| `/sdlc-status` | Show which agents completed vs pending |
| `/sdlc-resume <agent>` | Resume pipeline from a specific agent |
| `/sdlc-agent <agent>` | Run exactly one agent in isolation |
| `/sdlc-clean` | Remove all outputs for a fresh run |

### Individual Agent Commands
| Command | Agent | Role |
|---------|-------|------|
| `/sdlc-env` | 00 Environment | System scan + tool detection |
| `/sdlc-transcript` | 01 Transcript | Parse meeting → structured JSON |
| `/sdlc-requirements` | 02 Requirements | FRs + NFRs with traceability |
| `/sdlc-docs` | 03 Documentation | BRD, FRD, SOW |
| `/sdlc-planning` | 04 Planning | Sprint plan + timeline |
| `/sdlc-tickets` | 05 Ticketing | Jira/GitHub epics + stories |
| `/sdlc-architecture` | 06 Architecture | System design + API contracts |
| `/sdlc-security` | 12 Security *(opt)* | STRIDE + OWASP threat model |
| `/sdlc-code` | 07 Code | Production scaffolding |
| `/sdlc-testing` | 08 Testing | Test plan + auto-fix loop |
| `/sdlc-compliance` | 13 Compliance *(opt)* | HIPAA/GDPR/PCI gap analysis |
| `/sdlc-deploy` | 09 Deployment | Docker + CI/CD + IaC |
| `/sdlc-cost` | 14 Cost *(opt)* | Cloud cost forecast |
| `/sdlc-summary` | 10 Summary | Executive dashboard |
| `/sdlc-feedback` | 11 Feedback *(opt)* | Consistency review + remediation |

---

## Context Window Strategy

```
Sequential session (old):  all 15 agents → one context → compaction at Agent 07
Orchestrator mode (new):   each agent → fresh 200K context → zero accumulation
```

Run `/sdlc-parallel` or `/sdlc-sequential` to use the orchestrator.
Run `/sdlc-start` for manual interactive mode.

---

## Supported Domains

Healthcare, Fintech, E-Commerce, Education, HR Tech, Logistics, SaaS,
Government, Real Estate, Manufacturing, Legal, Media, Travel, Agriculture.

Domain intelligence flows automatically from the transcript through JSON contracts.
"""


# ── Builder ────────────────────────────────────────────────────────────────────

def _inject_frontmatter(agent: dict, content: bytes) -> bytes:
    """
    Prepend YAML frontmatter to an agent file if it doesn't already have one.
    Claude Code needs ---frontmatter--- to register agents properly.
    """
    text = content.decode("utf-8", errors="replace")
    if text.startswith("---"):
        return content  # already has frontmatter
    frontmatter = (
        f"---\n"
        f"name: {agent['id']}\n"
        f"description: \"{agent['desc']}\"\n"
        f"---\n\n"
    )
    return (frontmatter + text).encode("utf-8")


def build_plugin(output_path: Path) -> None:
    print(f"Building plugin → {output_path}")

    # Collect assets from base plugin — skip legacy commands (they have YAML errors
    # from double-compression in the original zip) and files we regenerate.
    existing_assets: dict[str, bytes] = {}
    SKIP_LEGACY_COMMANDS = True  # legacy commands from base plugin have corrupt frontmatter
    if EXISTING_PLUGIN.exists():
        print(f"  Reading base plugin: {EXISTING_PLUGIN.name}")
        with zipfile.ZipFile(EXISTING_PLUGIN, "r") as base:
            for name in base.namelist():
                if name.endswith("/"):
                    continue
                # Always skip: manifest, readme, legacy commands (corrupt YAML)
                if name.startswith(".claude-plugin/") or name == "README.md":
                    continue
                if SKIP_LEGACY_COMMANDS and name.startswith("commands/"):
                    continue  # we only ship our own /sdlc-* commands
                # Skip specialist agents — they're referenced by main agents but
                # the documentation-expert.md has corrupt YAML that blocks install
                if name.startswith("agents/specialists/"):
                    continue
                existing_assets[name] = base.read(name)
        print(f"  Carried over {len(existing_assets)} existing files (commands excluded)")
    else:
        print("  No base plugin found — building from scratch")
        for agent in AGENTS:
            src = PROJECT_ROOT / ".claude" / "agents" / agent["file"]
            if src.exists():
                existing_assets[f"agents/{agent['file']}"] = src.read_bytes()

    # New SDLC commands
    new_commands: dict[str, str] = {
        "commands/sdlc-setup.md":      _setup_command(),
        "commands/sdlc-update.md":     _update_command(),      # ← NEW: update to latest
        "commands/sdlc-start.md":      _pipeline_start_command(),
        "commands/sdlc-parallel.md":   _parallel_command(),
        "commands/sdlc-sequential.md": _sequential_command(),
        "commands/sdlc-status.md":     _status_command(),
        "commands/sdlc-resume.md":     _resume_command(),
        "commands/sdlc-agent.md":      _single_agent_command(),
        "commands/sdlc-clean.md":      _clean_outputs_command(),
    }
    for agent in AGENTS:
        new_commands[f"commands/{agent['cmd']}.md"] = _agent_command(agent)

    # Helpers / scripts to bundle
    extra_files: dict[str, Path] = {
        "helpers/harness.py":              PROJECT_ROOT / "helpers" / "harness.py",
        "helpers/test_retry_loop.py":      PROJECT_ROOT / "helpers" / "test_retry_loop.py",
        "helpers/pipeline_status.py":      PROJECT_ROOT / "helpers" / "pipeline_status.py",
        "helpers/pipeline_analytics.py":   PROJECT_ROOT / "helpers" / "pipeline_analytics.py",
        "scripts/orchestrator.py":         PROJECT_ROOT / "scripts" / "orchestrator.py",
        "scripts/run_pipeline.sh":         PROJECT_ROOT / "scripts" / "run_pipeline.sh",
        "sdlc-pipeline.yml":               PROJECT_ROOT / "sdlc-pipeline.yml",
        "agents/_ISOLATED_MODE.md":        PROJECT_ROOT / ".claude" / "agents" / "_ISOLATED_MODE.md",
        "agents/_COMMUNICATION_PROTOCOL.md": PROJECT_ROOT / ".claude" / "agents" / "_COMMUNICATION_PROTOCOL.md",
    }

    # Inject frontmatter into agent files that don't already have it
    agent_lookup = {a["file"]: a for a in AGENTS}
    for name in list(existing_assets.keys()):
        if name.startswith("agents/") and name.endswith(".md"):
            filename = name.split("/")[-1]
            if filename in agent_lookup:
                existing_assets[name] = _inject_frontmatter(
                    agent_lookup[filename], existing_assets[name]
                )

    # Merge into one dict so there are zero duplicate entries in the zip.
    # Priority (highest wins): manifest/readme > extra_files > new_commands > existing_assets
    merged: dict[str, bytes] = {}

    # 1. Base assets from existing plugin (lowest priority)
    for name, data in existing_assets.items():
        merged[name] = data

    # 2. New SDLC commands (overwrite any same-named existing command)
    for name, content in new_commands.items():
        merged[name] = content.encode("utf-8")

    # 3. Fresh project files (always overwrite stale base-plugin copies)
    #    Also inject frontmatter into agent files coming from extra_files
    for dest, src in extra_files.items():
        if src.exists():
            data = src.read_bytes()
            filename = dest.split("/")[-1]
            if dest.startswith("agents/") and filename in agent_lookup:
                data = _inject_frontmatter(agent_lookup[filename], data)
            merged[dest] = data

    # 4. Manifest and README always win (highest priority)
    merged[".claude-plugin/plugin.json"] = json.dumps(PLUGIN_JSON, indent=2).encode("utf-8")
    merged["README.md"] = _readme().encode("utf-8")

    # Write the final zip (one pass, no duplicates)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(merged.keys()):
            zf.writestr(name, merged[name])
            if name.startswith("commands/sdlc") or name in (".claude-plugin/plugin.json", "README.md"):
                print(f"  + {name}")

    # Summary
    with zipfile.ZipFile(output_path, "r") as check:
        files = check.namelist()
    cmds = [f for f in files if f.startswith("commands/") and f.endswith(".md")]
    agents = [f for f in files if f.startswith("agents/") and f.endswith(".md") and "/specialists/" not in f]
    size_kb = output_path.stat().st_size // 1024

    print(f"\n{'='*55}")
    print(f"  Plugin built: {output_path.name}")
    print(f"  Total files:  {len(files)}")
    print(f"  Commands:     {len(cmds)}")
    print(f"  Agents:       {len(agents)}")
    print(f"  Size:         {size_kb} KB")
    print(f"{'='*55}")
    print()
    print("Install in Claude Code:  drag the file into the Claude Code window")
    print("Install in Claude Desktop: Settings → Extensions → Install Plugin")
    print("Install in Claude.ai web: Settings → Extensions → Upload Plugin")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build SDLC Automation Plugin")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT),
                        help="Output plugin file path")
    args = parser.parse_args()
    build_plugin(Path(args.output))

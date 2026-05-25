#!/usr/bin/env python3
"""
SDLC Pipeline Orchestrator — runs agents as isolated subprocesses.

Each agent gets its own `claude -p` call = fresh context window = no accumulation.
JSON contracts on disk are the ONLY communication channel.

Execution modes:
  parallel    — phases run in DAG order; agents WITHIN a phase run concurrently
  sequential  — every agent runs one at a time regardless of phase
  single      — run exactly one agent in isolation

Usage:
  python scripts/orchestrator.py                        # parallel mode (default)
  python scripts/orchestrator.py --mode sequential
  python scripts/orchestrator.py --mode parallel
  python scripts/orchestrator.py --mode single --agent 06_architecture_agent
  python scripts/orchestrator.py --status
  python scripts/orchestrator.py --resume-from 07_code_agent
"""

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR   = PROJECT_ROOT / ".claude" / "agents"
OUTPUTS_DIR  = PROJECT_ROOT / "outputs"
PIPELINE_YML = PROJECT_ROOT / "sdlc-pipeline.yml"
CLAUDE_BIN   = "claude"

# Canonical DAG: phases in execution order
# Each phase: name, agents list, parallel flag, optional flag
PIPELINE_DAG = [
    {"phase": "phase_1_analysis",      "agents": ["environment_agent", "transcript_agent"],          "parallel": True,  "optional": False},
    {"phase": "phase_2_requirements",  "agents": ["requirement_agent"],                               "parallel": False, "optional": False},
    {"phase": "phase_3_documentation", "agents": ["documentation_agent", "planning_agent"],           "parallel": True,  "optional": False},
    {"phase": "phase_4_design",        "agents": ["jira_agent", "architecture_agent"],                "parallel": True,  "optional": False},
    {"phase": "phase_5_security",      "agents": ["security_threat_model_agent"],                     "parallel": False, "optional": True,  "key": "security_threat_model"},
    {"phase": "phase_6_implementation","agents": ["code_agent"],                                      "parallel": False, "optional": False},
    {"phase": "phase_7_quality",       "agents": ["testing_agent", "compliance_checker_agent"],       "parallel": True,  "optional": False, "optional_agents": ["compliance_checker_agent"], "key_map": {"compliance_checker_agent": "compliance_checker"}},
    {"phase": "phase_8_deployment",    "agents": ["deployment_agent"],                                "parallel": False, "optional": False},
    {"phase": "phase_9_delivery",      "agents": ["summary_agent", "cost_estimation_agent", "feedback_loop_agent"], "parallel": False, "optional": False, "optional_agents": ["cost_estimation_agent"], "key_map": {"cost_estimation_agent": "cost_estimation"}},
]

# Agent ID → expected output contract path
AGENT_OUTPUTS: dict[str, str] = {
    "environment_agent":            "outputs/environment_report.json",
    "transcript_agent":             "outputs/transcripts/structured_meeting_output.json",
    "requirement_agent":            "outputs/requirements/requirement_spec.json",
    "documentation_agent":          "outputs/documents/documentation_output.json",
    "planning_agent":               "outputs/planning/sprint_plan.json",
    "jira_agent":                   "outputs/jira/jira_tickets.json",
    "architecture_agent":           "outputs/architecture/system_design.json",
    "security_threat_model_agent":  "outputs/security/threat_model.json",
    "code_agent":                   "outputs/code/code_output.json",
    "testing_agent":                "outputs/qa/qa_results.json",
    "compliance_checker_agent":     "outputs/compliance/compliance_matrix.json",
    "deployment_agent":             "outputs/deployment/deployment_output.json",
    "cost_estimation_agent":        "outputs/cost/cost_estimation.json",
    "summary_agent":                "outputs/pipeline_final.json",
    "feedback_loop_agent":          "outputs/feedback/consistency_report.json",
}

# Agent file name prefix map (NN_name_agent.md)
AGENT_FILES: dict[str, str] = {
    "environment_agent":            "00_environment_agent.md",
    "transcript_agent":             "01_transcript_agent.md",
    "requirement_agent":            "02_requirement_agent.md",
    "documentation_agent":          "03_documentation_agent.md",
    "planning_agent":               "04_planning_agent.md",
    "jira_agent":                   "05_jira_agent.md",
    "architecture_agent":           "06_architecture_agent.md",
    "security_threat_model_agent":  "12_security_threat_model_agent.md",
    "code_agent":                   "07_code_agent.md",
    "testing_agent":                "08_testing_agent.md",
    "compliance_checker_agent":     "13_compliance_checker_agent.md",
    "deployment_agent":             "09_deployment_agent.md",
    "cost_estimation_agent":        "14_cost_estimation_agent.md",
    "summary_agent":                "10_summary_agent.md",
    "feedback_loop_agent":          "11_feedback_loop_agent.md",
}

POLL_INTERVAL_SECONDS = 15
MAX_WAIT_SECONDS      = 1800  # 30 minutes per agent max


# ── YAML parser (no pyyaml dependency) ────────────────────────────────────────

def _parse_optional_toggles() -> dict[str, bool]:
    """Read optional_agents block from sdlc-pipeline.yml.

    Uses the RAW (un-stripped) line to detect block boundaries so that
    indented keys inside optional_agents: are not mistaken for top-level keys.
    """
    defaults = {
        "security_threat_model": True,
        "compliance_checker": True,
        "cost_estimation": True,
        "feedback_loop": True,
    }
    if not PIPELINE_YML.exists():
        return defaults
    in_block = False
    result = dict(defaults)
    for raw_line in PIPELINE_YML.read_text().splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("optional_agents:"):
            in_block = True
            continue
        if in_block:
            # Exit block on any non-indented, non-comment line (use raw_line)
            if raw_line and not raw_line[0].isspace():
                break
            if ":" in stripped:
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.split("#")[0].strip()
                if key in result:
                    result[key] = val.lower() == "true"
    return result


# ── Agent contract completion detection ───────────────────────────────────────

def _contract_complete(agent_id: str) -> bool:
    """Returns True if the agent has written a valid output contract."""
    path_str = AGENT_OUTPUTS.get(agent_id)
    if not path_str:
        return False
    path = PROJECT_ROOT / path_str
    if not path.exists():
        return False
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("produced_by") == agent_id
    except Exception:
        return False


def _wait_for_contract(agent_id: str, timeout: int = MAX_WAIT_SECONDS) -> bool:
    """Poll until the agent writes its output contract or timeout."""
    elapsed = 0
    while elapsed < timeout:
        if _contract_complete(agent_id):
            return True
        time.sleep(POLL_INTERVAL_SECONDS)
        elapsed += POLL_INTERVAL_SECONDS
        mins = elapsed // 60
        secs = elapsed % 60
        print(f"  [wait] {agent_id} — {mins}m{secs:02d}s elapsed ...", flush=True)
    return False


# ── Isolated agent invocation ─────────────────────────────────────────────────

ISOLATED_DIRECTIVE = """

---
## ORCHESTRATOR DIRECTIVE — ISOLATED MODE

You are running as an isolated subprocess managed by orchestrator.py.

RULES FOR ISOLATED MODE:
1. Do NOT invoke the Task tool to trigger the next agent — the orchestrator handles sequencing.
2. Read your input contracts directly from disk (they are already written by prior agents).
3. Complete ALL your tasks as described above.
4. Write your output JSON contract to the correct path.
5. After writing the JSON contract, you are done. Stop cleanly.

The orchestrator will detect your output file and proceed to the next phase.
"""


def _build_prompt(agent_id: str) -> str:
    agent_file = AGENTS_DIR / AGENT_FILES[agent_id]
    if not agent_file.exists():
        raise FileNotFoundError(f"Agent file not found: {agent_file}")
    agent_instructions = agent_file.read_text(encoding="utf-8")
    return f"Read and execute the following agent instructions:\n\n{agent_instructions}{ISOLATED_DIRECTIVE}"


def run_agent_isolated(agent_id: str) -> dict:
    """
    Runs a single agent as an isolated `claude -p` subprocess.
    Returns a result dict with ok, duration, errors.
    """
    start = time.monotonic()
    ts    = datetime.now(timezone.utc).isoformat()

    print(f"\n[{ts[:19]}] STARTING  {agent_id}", flush=True)

    # Pre-flight: validate inputs via harness
    try:
        harness_result = subprocess.run(
            ["python3", str(PROJECT_ROOT / "helpers" / "harness.py"), "pre", agent_id],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if harness_result.returncode != 0:
            print(f"[HARNESS]  pre_agent {agent_id} FAILED — skipping agent")
            print(harness_result.stdout)
            return {"agent": agent_id, "ok": False, "error": "pre_agent failed", "duration": 0}
    except Exception as e:
        print(f"[HARNESS]  pre_agent check error: {e} — continuing anyway")

    # Build prompt and invoke claude -p
    try:
        prompt = _build_prompt(agent_id)
    except FileNotFoundError as e:
        return {"agent": agent_id, "ok": False, "error": str(e), "duration": 0}

    proc = subprocess.Popen(
        [CLAUDE_BIN, "-p", prompt],
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Stream output so the user sees progress
    if proc.stdout:
        for line in proc.stdout:
            print(f"  [{agent_id}] {line}", end="", flush=True)

    proc.wait()

    # If claude exited but contract not yet written, poll briefly
    if not _contract_complete(agent_id):
        print(f"  [wait] {agent_id} — claude exited, polling for contract ...", flush=True)
        completed = _wait_for_contract(agent_id, timeout=120)
    else:
        completed = True

    duration = time.monotonic() - start

    if completed:
        # Post-flight: validate output contract
        subprocess.run(
            ["python3", str(PROJECT_ROOT / "helpers" / "harness.py"), "post", agent_id],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        print(f"[{datetime.now(timezone.utc).isoformat()[:19]}] COMPLETED {agent_id} ({duration:.0f}s)", flush=True)
        return {"agent": agent_id, "ok": True, "duration": duration}
    else:
        print(f"[{datetime.now(timezone.utc).isoformat()[:19]}] TIMEOUT   {agent_id} after {duration:.0f}s", flush=True)
        return {"agent": agent_id, "ok": False, "error": "timeout", "duration": duration}


# ── Phase execution ────────────────────────────────────────────────────────────

def run_phase_parallel(phase_name: str, agents: list[str]) -> dict[str, dict]:
    """Run all agents in a phase concurrently."""
    print(f"\n{'='*60}")
    print(f"  PHASE: {phase_name}  [PARALLEL — {len(agents)} agents]")
    print(f"{'='*60}", flush=True)
    results: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=len(agents)) as pool:
        futures = {pool.submit(run_agent_isolated, agent): agent for agent in agents}
        for future in as_completed(futures):
            agent = futures[future]
            try:
                results[agent] = future.result()
            except Exception as e:
                results[agent] = {"agent": agent, "ok": False, "error": str(e), "duration": 0}
    return results


def run_phase_sequential(phase_name: str, agents: list[str]) -> dict[str, dict]:
    """Run all agents in a phase one at a time."""
    print(f"\n{'='*60}")
    print(f"  PHASE: {phase_name}  [SEQUENTIAL — {len(agents)} agents]")
    print(f"{'='*60}", flush=True)
    results: dict[str, dict] = {}
    for agent in agents:
        results[agent] = run_agent_isolated(agent)
        if not results[agent]["ok"]:
            print(f"  [!] {agent} failed — stopping phase {phase_name}", flush=True)
            break
    return results


# ── Optional agent filtering ───────────────────────────────────────────────────

def _filter_agents(phase: dict, toggles: dict[str, bool]) -> list[str]:
    """Remove disabled optional agents from a phase's agent list."""
    agents = list(phase["agents"])
    optional_in_phase = phase.get("optional_agents", [])
    key_map = phase.get("key_map", {})
    phase_key = phase.get("key")

    # Whole phase optional (e.g., security phase)
    if phase.get("optional") and phase_key:
        if not toggles.get(phase_key, True):
            return []

    # Individual optional agents within a phase
    filtered = []
    for agent in agents:
        if agent in optional_in_phase:
            toggle_key = key_map.get(agent, agent.replace("_agent", ""))
            if not toggles.get(toggle_key, True):
                print(f"  [skip] {agent} — disabled in sdlc-pipeline.yml", flush=True)
                continue
        filtered.append(agent)
    return filtered


# ── Status display ─────────────────────────────────────────────────────────────

def show_status() -> None:
    print("\n" + "="*65)
    print("  SDLC ORCHESTRATOR — Agent Status")
    print("="*65)
    for phase in PIPELINE_DAG:
        print(f"\n  Phase: {phase['phase']}")
        for agent in phase["agents"]:
            done  = _contract_complete(agent)
            icon  = "[OK]" if done else "[  ]"
            path  = AGENT_OUTPUTS.get(agent, "unknown")
            print(f"    {icon} {agent:<40s}  {path}")
    print("\n" + "="*65)


# ── Resume support ─────────────────────────────────────────────────────────────

def _find_resume_phase(resume_agent: str) -> int:
    """Return the phase index to start from for the given agent."""
    agent_id = resume_agent.replace(".md", "").lstrip("0123456789_")
    for i, phase in enumerate(PIPELINE_DAG):
        if any(agent_id in a for a in phase["agents"]) or resume_agent in phase["agents"]:
            return i
    # Try matching by file name prefix (e.g. "07_code_agent" → "code_agent")
    for i, phase in enumerate(PIPELINE_DAG):
        for a in phase["agents"]:
            if a in resume_agent or resume_agent in a:
                return i
    raise ValueError(f"Cannot find phase for agent: {resume_agent}")


# ── Main orchestrator ──────────────────────────────────────────────────────────

def run_pipeline(mode: str = "parallel", start_phase_idx: int = 0) -> None:
    toggles = _parse_optional_toggles()
    print(f"\nOrchestrator started — mode={mode}, optional_agents={toggles}")
    print(f"Start phase index: {start_phase_idx}")

    all_results: list[dict] = []
    pipeline_ok = True

    for i, phase in enumerate(PIPELINE_DAG):
        if i < start_phase_idx:
            print(f"  [skip] Phase {i} ({phase['phase']}) — resuming from phase {start_phase_idx}")
            continue

        agents = _filter_agents(phase, toggles)
        if not agents:
            print(f"  [skip] Phase {i} ({phase['phase']}) — all agents disabled")
            continue

        # Already completed? Skip if all contracts are present
        if all(_contract_complete(a) for a in agents):
            print(f"  [done] Phase {i} ({phase['phase']}) — contracts already present, skipping")
            continue

        use_parallel = phase.get("parallel", False) and mode == "parallel" and len(agents) > 1

        if use_parallel:
            results = run_phase_parallel(phase["phase"], agents)
        else:
            results = run_phase_sequential(phase["phase"], agents)

        all_results.extend(results.values())
        failed = [r for r in results.values() if not r["ok"]]

        if failed:
            pipeline_ok = False
            print(f"\n[!!] Phase {phase['phase']} had failures: {[r['agent'] for r in failed]}")
            print("     Pipeline paused. Fix issues and resume with:")
            print(f"     python scripts/orchestrator.py --resume-from {failed[0]['agent']}")
            break

    _print_summary(all_results, pipeline_ok)


def run_single_agent(agent_id: str) -> None:
    """Run exactly one agent in isolation."""
    # Normalize: accept file name OR agent_id
    if agent_id.endswith(".md"):
        agent_id = agent_id[:-3]
    if agent_id not in AGENT_OUTPUTS:
        # Try stripping numeric prefix
        for key in AGENT_OUTPUTS:
            if key in agent_id or agent_id in key:
                agent_id = key
                break
    print(f"\nRunning single agent: {agent_id}")
    result = run_agent_isolated(agent_id)
    if result["ok"]:
        print(f"\nAgent completed successfully in {result['duration']:.0f}s")
    else:
        print(f"\nAgent failed: {result.get('error', 'unknown')}")
        sys.exit(1)


def _print_summary(results: list[dict], pipeline_ok: bool) -> None:
    total    = len(results)
    passed   = sum(1 for r in results if r.get("ok"))
    failed   = total - passed
    duration = sum(r.get("duration", 0) for r in results)

    print(f"\n{'='*60}")
    print(f"  PIPELINE {'COMPLETE' if pipeline_ok else 'INCOMPLETE'}")
    print(f"  Agents run: {total}  |  Passed: {passed}  |  Failed: {failed}")
    print(f"  Total time: {duration/60:.1f} minutes")
    if pipeline_ok:
        print(f"  Summary: outputs/PROJECT_COMPLETE_SUMMARY.md")
        print(f"  Dashboard: outputs/EXECUTIVE_DASHBOARD.md")
    print(f"{'='*60}\n")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="SDLC Pipeline Orchestrator")
    parser.add_argument("--mode", choices=["parallel", "sequential"], default="parallel",
                        help="Execution mode (default: parallel)")
    parser.add_argument("--agent", help="Agent ID or file name for single-agent mode")
    parser.add_argument("--resume-from", dest="resume_from",
                        help="Agent name to resume pipeline from")
    parser.add_argument("--status", action="store_true",
                        help="Show current pipeline status and exit")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.agent:
        run_single_agent(args.agent)
        return

    start_phase = 0
    if args.resume_from:
        try:
            start_phase = _find_resume_phase(args.resume_from)
            print(f"Resuming from phase index {start_phase} (agent: {args.resume_from})")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    run_pipeline(mode=args.mode, start_phase_idx=start_phase)


if __name__ == "__main__":
    main()

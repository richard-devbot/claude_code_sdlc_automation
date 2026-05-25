#!/usr/bin/env python3
"""
Agent Lifecycle Harness — wraps every agent invocation with pre/post hooks.

Used by orchestrator.py. Can also be called standalone:
    python helpers/harness.py pre  <agent_id>
    python helpers/harness.py post <agent_id>
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RUN_LOG      = PROJECT_ROOT / "outputs" / "analytics" / "run_log.jsonl"
NOTIFIER     = PROJECT_ROOT / ".claude" / "hooks" / "notification_dispatcher.py"

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

# Minimum required input contracts per agent
AGENT_INPUTS: dict[str, list[str]] = {
    "requirement_agent":            ["outputs/transcripts/structured_meeting_output.json"],
    "documentation_agent":          ["outputs/requirements/requirement_spec.json"],
    "planning_agent":               ["outputs/requirements/requirement_spec.json"],
    "jira_agent":                   ["outputs/planning/sprint_plan.json"],
    "architecture_agent":           ["outputs/jira/jira_tickets.json", "outputs/requirements/requirement_spec.json"],
    "security_threat_model_agent":  ["outputs/architecture/system_design.json"],
    "code_agent":                   ["outputs/architecture/system_design.json"],
    "testing_agent":                ["outputs/code/code_output.json"],
    "compliance_checker_agent":     ["outputs/requirements/requirement_spec.json"],
    "deployment_agent":             ["outputs/qa/qa_results.json", "outputs/architecture/system_design.json"],
    "summary_agent":                ["outputs/deployment/deployment_output.json"],
    "feedback_loop_agent":          ["outputs/pipeline_final.json"],
    "cost_estimation_agent":        ["outputs/architecture/system_design.json"],
}


def _log(event: str, agent_id: str, data: dict) -> None:
    RUN_LOG.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "agent": agent_id,
        **data,
    }
    with open(RUN_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def pre_agent(agent_id: str) -> tuple[bool, list[str]]:
    """
    Validates inputs exist before the agent runs.
    Returns (ok, list_of_errors).
    """
    errors: list[str] = []
    required_inputs = AGENT_INPUTS.get(agent_id, [])
    for path_str in required_inputs:
        path = PROJECT_ROOT / path_str
        if not path.exists():
            errors.append(f"Missing input: {path_str}")
        else:
            try:
                with open(path, encoding="utf-8") as f:
                    json.load(f)
            except json.JSONDecodeError:
                errors.append(f"Malformed JSON: {path_str}")

    ok = len(errors) == 0
    _log("pre_agent", agent_id, {"inputs_checked": len(required_inputs), "errors": errors, "ok": ok})
    if errors:
        print(f"[HARNESS] pre_agent {agent_id} FAILED:")
        for e in errors:
            print(f"          {e}")
    else:
        print(f"[HARNESS] pre_agent {agent_id} OK — inputs validated")
    return ok, errors


def post_agent(agent_id: str) -> tuple[bool, list[str]]:
    """
    Validates the output contract after the agent runs.
    Returns (ok, list_of_errors).
    """
    errors: list[str] = []
    output_path_str = AGENT_OUTPUTS.get(agent_id)
    if not output_path_str:
        errors.append(f"Unknown agent: {agent_id}")
        _log("post_agent", agent_id, {"errors": errors, "ok": False})
        return False, errors

    output_path = PROJECT_ROOT / output_path_str
    if not output_path.exists():
        errors.append(f"Output contract not written: {output_path_str}")
        _log("post_agent", agent_id, {"errors": errors, "ok": False})
        print(f"[HARNESS] post_agent {agent_id} FAILED: output contract missing")
        return False, errors

    try:
        with open(output_path, encoding="utf-8") as f:
            contract = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Output contract malformed: {e}")
        _log("post_agent", agent_id, {"errors": errors, "ok": False})
        return False, errors

    for field in ("contract_version", "produced_by", "timestamp"):
        if field not in contract:
            errors.append(f"Contract missing field: {field}")

    if contract.get("produced_by") != agent_id:
        errors.append(
            f"produced_by mismatch: expected {agent_id!r}, got {contract.get('produced_by')!r}"
        )

    ok = len(errors) == 0
    _log("post_agent", agent_id, {
        "output": output_path_str,
        "errors": errors,
        "ok": ok,
        "contract_version": contract.get("contract_version"),
        "pipeline_complete": contract.get("pipeline_complete", False),
    })

    if ok:
        print(f"[HARNESS] post_agent {agent_id} OK — contract valid")
        _notify(agent_id, contract)
    else:
        print(f"[HARNESS] post_agent {agent_id} FAILED:")
        for e in errors:
            print(f"          {e}")

    return ok, errors


def _notify(agent_id: str, contract: dict) -> None:
    """Fire the notification dispatcher (non-blocking, never fails the pipeline)."""
    if NOTIFIER.exists():
        try:
            subprocess.run(
                ["python3", str(NOTIFIER)],
                cwd=str(PROJECT_ROOT),
                timeout=10,
                capture_output=True,
            )
        except Exception:
            pass  # Notifications are non-blocking


def phase_boundary(completed_phase: str, phase_agents: list[str]) -> dict:
    """
    Runs between phases. Validates all agents in the completed phase wrote valid contracts.
    Returns a summary dict.
    """
    results = {}
    all_ok = True
    for agent_id in phase_agents:
        ok, errors = post_agent(agent_id)
        results[agent_id] = {"ok": ok, "errors": errors}
        if not ok:
            all_ok = False

    summary = {
        "phase": completed_phase,
        "agents": phase_agents,
        "all_passed": all_ok,
        "results": results,
    }
    _log("phase_boundary", completed_phase, summary)
    status = "PASSED" if all_ok else "FAILED"
    print(f"[HARNESS] Phase boundary [{completed_phase}]: {status}")
    return summary


# CLI entry point for standalone use
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python helpers/harness.py pre|post <agent_id>")
        sys.exit(1)
    mode, agent = sys.argv[1], sys.argv[2]
    if mode == "pre":
        ok, _ = pre_agent(agent)
    elif mode == "post":
        ok, _ = post_agent(agent)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)
    sys.exit(0 if ok else 2)

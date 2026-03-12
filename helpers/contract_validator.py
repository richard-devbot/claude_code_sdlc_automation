#!/usr/bin/env python3
"""
Validates all pipeline output JSON contracts against expected structure.
Usage: python helpers/contract_validator.py [agent_id]
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

AGENTS = {
    "environment_agent": {
        "output": "outputs/environment_report.json",
        "required": ["contract_version", "produced_by", "timestamp",
                      "tools_available", "pipeline_ready", "next_agent"],
    },
    "transcript_agent": {
        "output": "outputs/transcripts/structured_meeting_output.json",
        "required": ["contract_version", "produced_by", "timestamp", "meeting_metadata",
                      "domain", "discussed_features", "next_agent"],
    },
    "requirement_agent": {
        "output": "outputs/requirements/requirement_spec.json",
        "required": ["contract_version", "produced_by", "timestamp", "project",
                      "functional_requirements", "non_functional_requirements", "next_agent"],
    },
    "documentation_agent": {
        "output": "outputs/documents/documentation_output.json",
        "required": ["contract_version", "produced_by", "timestamp",
                      "documents_created", "next_agent"],
    },
    "planning_agent": {
        "output": "outputs/planning/sprint_plan.json",
        "required": ["contract_version", "produced_by", "timestamp",
                      "project_timeline", "sprints", "next_agent"],
    },
    "jira_agent": {
        "output": "outputs/jira/jira_tickets.json",
        "required": ["contract_version", "produced_by", "timestamp",
                      "summary", "epics", "next_agent"],
    },
    "architecture_agent": {
        "output": "outputs/architecture/system_design.json",
        "required": ["contract_version", "produced_by", "timestamp",
                      "tech_stack", "services", "next_agent"],
    },
    "code_agent": {
        "output": "outputs/code/code_output.json",
        "required": ["contract_version", "produced_by", "timestamp",
                      "files_created", "next_agent"],
    },
    "testing_agent": {
        "output": "outputs/qa/qa_results.json",
        "required": ["contract_version", "produced_by", "timestamp",
                      "artifacts_created", "next_agent"],
    },
    "deployment_agent": {
        "output": "outputs/deployment/deployment_output.json",
        "required": ["contract_version", "produced_by", "timestamp",
                      "artifacts_created", "next_agent"],
    },
    "summary_agent": {
        "output": "outputs/pipeline_final.json",
        "required": ["contract_version", "produced_by", "timestamp",
                      "pipeline_complete", "pipeline_status"],
    },
}


def validate_agent(agent_id, config):
    """Validate a single agent's output."""
    filepath = PROJECT_ROOT / config["output"]

    if not filepath.exists():
        return "SKIP", f"Output file not found (agent not yet executed)"

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return "FAIL", f"Invalid JSON: {e}"

    errors = []
    for field in config["required"]:
        if field not in data:
            errors.append(f"Missing: {field}")

    if data.get("produced_by") != agent_id:
        errors.append(f"produced_by mismatch: got '{data.get('produced_by')}'")

    if errors:
        return "FAIL", "; ".join(errors)
    return "PASS", "All validations passed"


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None

    if target and target not in AGENTS:
        print(f"Unknown agent: {target}")
        print(f"Valid agents: {', '.join(AGENTS.keys())}")
        sys.exit(1)

    agents_to_check = {target: AGENTS[target]} if target else AGENTS
    passed = failed = skipped = 0

    print("=" * 60)
    print("  SDLC Pipeline Contract Validation")
    print("=" * 60)

    for agent_id, config in agents_to_check.items():
        status, message = validate_agent(agent_id, config)
        icon = {"PASS": "+", "FAIL": "X", "SKIP": "-"}[status]
        print(f"  [{icon}] {agent_id}: {message}")

        if status == "PASS":
            passed += 1
        elif status == "FAIL":
            failed += 1
        else:
            skipped += 1

    print("=" * 60)
    print(f"  Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 60)

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()

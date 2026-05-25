#!/usr/bin/env python3
"""
Shows current pipeline progress dashboard.
Usage: python helpers/pipeline_status.py
"""

import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PIPELINE = [
    {"order": 0, "name": "Environment Agent", "id": "environment_agent",
     "output": "outputs/environment_report.json", "role": "Setup & Tools"},
    {"order": 1, "name": "Transcript Agent", "id": "transcript_agent",
     "output": "outputs/transcripts/structured_meeting_output.json", "role": "Business Analyst"},
    {"order": 2, "name": "Requirement Agent", "id": "requirement_agent",
     "output": "outputs/requirements/requirement_spec.json", "role": "Senior BA"},
    {"order": 3, "name": "Documentation Agent", "id": "documentation_agent",
     "output": "outputs/documents/documentation_output.json", "role": "Technical Writer"},
    {"order": 4, "name": "Planning Agent", "id": "planning_agent",
     "output": "outputs/planning/sprint_plan.json", "role": "Project Manager"},
    {"order": 5, "name": "Jira Agent", "id": "jira_agent",
     "output": "outputs/jira/jira_tickets.json", "role": "Scrum Master"},
    {"order": 6, "name": "Architecture Agent", "id": "architecture_agent",
     "output": "outputs/architecture/system_design.json", "role": "Solution Architect"},
    {"order": 7, "name": "Code Agent", "id": "code_agent",
     "output": "outputs/code/code_output.json", "role": "Senior Developer"},
    {"order": 8, "name": "Testing Agent", "id": "testing_agent",
     "output": "outputs/qa/qa_results.json", "role": "QA Lead"},
    {"order": 9, "name": "Deployment Agent", "id": "deployment_agent",
     "output": "outputs/deployment/deployment_output.json", "role": "DevOps Engineer"},
    {"order": 10, "name": "Summary Agent", "id": "summary_agent",
     "output": "outputs/pipeline_final.json", "role": "Delivery Lead"},
]


def check_agent(agent):
    """Check if an agent has completed."""
    filepath = PROJECT_ROOT / agent["output"]
    if not filepath.exists():
        return "PENDING", None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("produced_by") == agent["id"]:
            return "COMPLETED", data.get("timestamp", "unknown")
        return "INVALID", None
    except Exception:
        return "ERROR", None


def main():
    print("\n" + "=" * 65)
    print("  SDLC AUTOMATION PIPELINE — STATUS DASHBOARD")
    print("=" * 65)

    # Check input
    input_file = PROJECT_ROOT / "inputs" / "transcript.txt"
    input_status = "READY" if input_file.exists() else "MISSING"
    print(f"\n  Input: inputs/transcript.txt [{input_status}]")
    print("-" * 65)

    completed = 0
    next_agent = None

    for agent in PIPELINE:
        status, timestamp = check_agent(agent)
        if status == "COMPLETED":
            completed += 1
            icon = "[OK]"
            ts = f" ({timestamp})" if timestamp else ""
        elif status == "PENDING":
            icon = "[  ]"
            ts = ""
            if next_agent is None:
                next_agent = agent
        else:
            icon = "[!!]"
            ts = f" ({status})"

        print(f"  {icon} {agent['order']:02d}. {agent['name']:<25s} | {agent['role']:<20s}{ts}")

    progress = (completed / len(PIPELINE)) * 100
    print("-" * 65)
    print(f"  Progress: {completed}/{len(PIPELINE)} agents ({progress:.0f}%)")

    if next_agent:
        print(f"\n  Next: Run agent {next_agent['order']:02d} ({next_agent['name']})")
        print(f"  Prompt: Read .claude/agents/{next_agent['order']:02d}_{'_'.join(next_agent['name'].lower().split())}.md and execute it.")
    elif completed == len(PIPELINE):
        print(f"\n  PIPELINE COMPLETE! Review: outputs/PROJECT_COMPLETE_SUMMARY.md")

    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()

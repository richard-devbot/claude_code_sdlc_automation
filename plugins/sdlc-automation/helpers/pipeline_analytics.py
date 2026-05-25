#!/usr/bin/env python3
"""Pipeline Analytics — Track metrics across SDLC pipeline runs."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

OUTPUTS_DIR = Path("outputs")
ANALYTICS_DIR = OUTPUTS_DIR / "analytics"
METRICS_FILE = ANALYTICS_DIR / "pipeline_metrics.json"


def collect_metrics():
    """Collect metrics from all pipeline output contracts."""
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

    metrics = {
        "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.now().isoformat(),
        "agents": {},
        "summary": {
            "total_agents_completed": 0,
            "total_files_generated": 0,
            "total_requirements": 0,
            "total_stories": 0,
            "total_tasks": 0,
            "total_test_cases": 0,
            "domain_detected": "unknown",
            "execution_mode": "unknown",
            "tools_used": [],
            "fallbacks_used": []
        }
    }

    # Map of agent output files
    agent_outputs = {
        "environment_agent": "environment_report.json",
        "transcript_agent": "transcripts/structured_meeting_output.json",
        "requirement_agent": "requirements/requirement_spec.json",
        "documentation_agent": "documents/documentation_output.json",
        "planning_agent": "planning/sprint_plan.json",
        "jira_agent": "jira/jira_tickets.json",
        "architecture_agent": "architecture/system_design.json",
        "code_agent": "code/code_output.json",
        "testing_agent": "qa/qa_results.json",
        "deployment_agent": "deployment/deployment_output.json",
        "summary_agent": "pipeline_final.json",
        "feedback_loop_agent": "feedback/consistency_report.json",
        "security_threat_model_agent": "security/threat_model.json",
        "compliance_checker_agent": "compliance/compliance_matrix.json",
        "cost_estimation_agent": "cost/cost_estimation.json"
    }

    for agent_name, output_path in agent_outputs.items():
        full_path = OUTPUTS_DIR / output_path
        if full_path.exists():
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    contract = json.load(f)
                metrics["agents"][agent_name] = {
                    "completed": True,
                    "timestamp": contract.get("timestamp", "unknown"),
                    "file_size_bytes": full_path.stat().st_size
                }
                metrics["summary"]["total_agents_completed"] += 1

                # Extract specific metrics
                if agent_name == "transcript_agent":
                    metrics["summary"]["domain_detected"] = contract.get("domain", "unknown")
                elif agent_name == "requirement_agent":
                    frs = contract.get("functional_requirements", [])
                    metrics["summary"]["total_requirements"] = len(frs)
                elif agent_name == "jira_agent":
                    summary = contract.get("summary", {})
                    metrics["summary"]["total_stories"] = summary.get("total_stories", 0)
                    metrics["summary"]["total_tasks"] = summary.get("total_tasks", 0)
                elif agent_name == "environment_agent":
                    prefs = contract.get("user_preferences", {})
                    metrics["summary"]["execution_mode"] = prefs.get("ticketing_platform", "unknown")

            except (json.JSONDecodeError, KeyError) as e:
                metrics["agents"][agent_name] = {
                    "completed": True,
                    "error": f"Parse error: {e}"
                }
        else:
            metrics["agents"][agent_name] = {"completed": False}

    # Count total files generated
    total_files = sum(1 for _ in OUTPUTS_DIR.rglob("*") if _.is_file())
    metrics["summary"]["total_files_generated"] = total_files

    # Save metrics
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return metrics


def print_dashboard(metrics):
    """Print a human-readable analytics dashboard."""
    s = metrics["summary"]
    print("=" * 60)
    print("  SDLC PIPELINE ANALYTICS DASHBOARD")
    print("=" * 60)
    print(f"  Run ID:     {metrics['run_id']}")
    print(f"  Timestamp:  {metrics['timestamp']}")
    print(f"  Domain:     {s['domain_detected']}")
    print("-" * 60)
    print(f"  Agents Completed:    {s['total_agents_completed']} / {len(metrics['agents'])}")
    print(f"  Files Generated:     {s['total_files_generated']}")
    print(f"  Requirements:        {s['total_requirements']}")
    print(f"  User Stories:        {s['total_stories']}")
    print(f"  Tasks:               {s['total_tasks']}")
    print("-" * 60)
    print("  AGENT STATUS:")
    for name, info in metrics["agents"].items():
        status = "✓" if info.get("completed") else "✗"
        ts = info.get("timestamp", "")[:19] if info.get("completed") else "not run"
        print(f"    {status} {name:40s} {ts}")
    print("=" * 60)


if __name__ == "__main__":
    m = collect_metrics()
    print_dashboard(m)
    print(f"\nMetrics saved to: {METRICS_FILE}")

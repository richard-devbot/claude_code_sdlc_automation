#!/usr/bin/env python3
"""
PostToolUse hook: Dispatches agent-completion notifications to Slack, Teams,
or macOS desktop when a pipeline JSON contract is written.

Exit 0 always — notifications are non-blocking and never stop the pipeline.
"""

import json
import subprocess
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PIPELINE_YML = PROJECT_ROOT / "sdlc-pipeline.yml"
NOTIFICATIONS_LOG = PROJECT_ROOT / "outputs" / "analytics" / "notifications.log"

AGENT_LABELS = {
    "environment_agent":    ("00", "Environment Setup",    "System scanned, tools detected"),
    "transcript_agent":     ("01", "Transcript Analysis",  "Meeting analyzed, domain detected"),
    "requirement_agent":    ("02", "Requirements",         "Functional + non-functional requirements captured"),
    "documentation_agent":  ("03", "Documentation",        "BRD, FRD, SOW generated"),
    "planning_agent":       ("04", "Sprint Planning",      "Sprint plan and timeline created"),
    "jira_agent":           ("05", "Ticketing",            "Epics, stories, and tasks created"),
    "architecture_agent":   ("06", "Architecture",         "System design and API contracts defined"),
    "security_threat_model_agent": ("12", "Security Threat Model", "STRIDE analysis + OWASP mitigations complete"),
    "code_agent":           ("07", "Code Generation",      "Production scaffolding generated"),
    "testing_agent":        ("08", "QA & Testing",         "Test plan, test cases, security checklist created"),
    "compliance_checker_agent": ("13", "Compliance Check", "Regulatory gap analysis complete"),
    "deployment_agent":     ("09", "Deployment",           "Dockerfiles, CI/CD, IaC templates ready"),
    "cost_estimation_agent":("14", "Cost Estimation",      "Cloud cost forecast generated"),
    "summary_agent":        ("10", "Summary",              "Executive dashboard and full summary ready"),
    "feedback_loop_agent":  ("11", "Feedback Loop",        "Consistency review complete"),
}


def load_notification_config():
    """Parse notification config from sdlc-pipeline.yml.

    Uses an indentation-aware state machine so nested keys like
    notifications.channels.slack.webhook_url are correctly extracted.
    """
    config = {"enabled": False, "slack_webhook": "", "teams_webhook": "", "fallback": "desktop"}
    if not PIPELINE_YML.exists():
        return config
    try:
        in_notifications = False
        current_channel: str | None = None  # "slack" or "teams"

        for raw_line in PIPELINE_YML.read_text().splitlines():
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            # Enter notifications block
            if stripped.startswith("notifications:"):
                in_notifications = True
                current_channel = None
                continue

            # Exit notifications block on any non-indented line
            if in_notifications and not raw_line[0].isspace():
                break

            if not in_notifications:
                continue

            # Depth-1 keys: enabled, fallback, channels, events
            if stripped.startswith("enabled:"):
                config["enabled"] = "true" in stripped.lower()
            elif stripped.startswith("fallback:"):
                config["fallback"] = stripped.split(":", 1)[1].split("#")[0].strip().strip('"\'').strip()
            # Depth-2: channel names
            elif stripped.startswith("slack:"):
                current_channel = "slack"
            elif stripped.startswith("teams:"):
                current_channel = "teams"
            # Depth-3: webhook_url under the active channel
            elif stripped.startswith("webhook_url:"):
                raw_val = stripped.split(":", 1)[1].strip()
                # Strip inline comment, then surrounding quotes
                val = raw_val.split("#")[0].strip().strip('"\'').strip()
                if val:
                    if current_channel == "slack" and not config["slack_webhook"]:
                        config["slack_webhook"] = val
                    elif current_channel == "teams" and not config["teams_webhook"]:
                        config["teams_webhook"] = val
            # Reset channel tracker on any other depth-2 key
            elif ":" in stripped and current_channel and raw_line[:6].strip() == "":
                # Still 4-space indent → within same channel block, do nothing
                pass
            elif ":" in stripped:
                current_channel = None

        return config
    except Exception:
        return {"enabled": False}


def find_latest_contract():
    """Find the most recently written output JSON contract."""
    outputs_dir = PROJECT_ROOT / "outputs"
    latest_file = None
    latest_time = 0
    for json_file in outputs_dir.rglob("*.json"):
        try:
            mtime = json_file.stat().st_mtime
            if mtime > latest_time:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "produced_by" in data and "timestamp" in data:
                    latest_time = mtime
                    latest_file = (json_file, data)
        except Exception:
            continue
    return latest_file


def build_message(agent_id, contract_data):
    """Build a human-readable notification message."""
    num, label, summary = AGENT_LABELS.get(agent_id, ("?", agent_id, "Agent completed"))
    ts = contract_data.get("timestamp", datetime.utcnow().isoformat())
    next_agent = contract_data.get("next_agent", "")
    is_final = contract_data.get("pipeline_complete", False)

    if is_final:
        status_line = "PIPELINE COMPLETE — all agents finished"
        next_line = "Review: outputs/PROJECT_COMPLETE_SUMMARY.md"
    elif next_agent:
        next_label = AGENT_LABELS.get(next_agent, ("?", next_agent, ""))[1]
        next_line = f"Next: {next_label}"
        status_line = f"Agent {num} done — {summary}"
    else:
        status_line = f"Agent {num} done — {summary}"
        next_line = ""

    return {
        "short": f"[SDLC] {label}: {summary}",
        "full": f"*[SDLC Pipeline]* Agent {num} — *{label}*\n{summary}\n{next_line}".strip(),
        "status_line": status_line,
        "is_final": is_final,
    }


def post_to_slack(webhook_url, message):
    """POST a message to a Slack Incoming Webhook."""
    if not webhook_url or webhook_url.startswith("#"):
        return False
    payload = json.dumps({"text": message["full"]}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False


def post_to_teams(webhook_url, message):
    """POST a message to a MS Teams Incoming Webhook."""
    if not webhook_url or webhook_url.startswith("#"):
        return False
    payload = json.dumps({
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": message["short"],
        "title": "SDLC Pipeline Update",
        "text": message["full"].replace("*", "**"),
    }).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status in (200, 202)
    except Exception:
        return False


def notify_desktop(message):
    """macOS osascript notification fallback."""
    try:
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{message["short"]}" with title "SDLC Pipeline"'],
            timeout=5, capture_output=True,
        )
        return True
    except Exception:
        return False


def log_notification(agent_id, message, dispatched_to):
    """Append notification record to the analytics log."""
    NOTIFICATIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent": agent_id,
        "message": message["short"],
        "dispatched_to": dispatched_to,
    }
    with open(NOTIFICATIONS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def main():
    config = load_notification_config()
    if not config.get("enabled"):
        return

    result = find_latest_contract()
    if not result:
        return

    contract_path, contract_data = result
    agent_id = contract_data.get("produced_by", "unknown_agent")
    message = build_message(agent_id, contract_data)

    dispatched_to = []

    if config.get("slack_webhook"):
        if post_to_slack(config["slack_webhook"], message):
            dispatched_to.append("slack")

    if config.get("teams_webhook"):
        if post_to_teams(config["teams_webhook"], message):
            dispatched_to.append("teams")

    if not dispatched_to and config.get("fallback") == "desktop":
        if notify_desktop(message):
            dispatched_to.append("desktop")

    log_notification(agent_id, message, dispatched_to)


if __name__ == "__main__":
    main()
    exit(0)

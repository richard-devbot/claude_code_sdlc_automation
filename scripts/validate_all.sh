#!/bin/bash
# Validates all pipeline output contracts.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

PYTHON=$(command -v python3 || command -v python)

if [ -z "$PYTHON" ]; then
    echo "Python not found. Install Python 3.7+ to run validation."
    exit 1
fi

echo "Running contract validation..."
echo ""

if [ -n "$1" ]; then
    $PYTHON "$PROJECT_DIR/helpers/contract_validator.py" "$1"
else
    $PYTHON "$PROJECT_DIR/helpers/contract_validator.py"
fi

echo ""
echo "To validate a single agent: bash scripts/validate_all.sh <agent_id>"
echo "Valid agents: transcript_agent, requirement_agent, documentation_agent,"
echo "  planning_agent, jira_agent, architecture_agent, code_agent,"
echo "  testing_agent, deployment_agent, summary_agent"

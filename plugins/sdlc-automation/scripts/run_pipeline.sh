#!/bin/bash
# Pre-flight check before starting the SDLC automation pipeline.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================"
echo "  SDLC Automation Pipeline — Pre-flight Check"
echo "============================================"

ERRORS=0

# Check input file
if [ -f "$PROJECT_DIR/inputs/transcript.txt" ]; then
    LINES=$(wc -l < "$PROJECT_DIR/inputs/transcript.txt")
    echo "[OK] Input file found: inputs/transcript.txt ($LINES lines)"
else
    echo "[!!] MISSING: inputs/transcript.txt"
    echo "     Place your client meeting transcript in this file."
    ERRORS=$((ERRORS + 1))
fi

# Check agent definitions
AGENT_COUNT=$(ls "$PROJECT_DIR/.claude/agents/"*.md 2>/dev/null | wc -l)
echo "[OK] Agent definitions found: $AGENT_COUNT"

# Check output directories
for dir in transcripts requirements documents planning jira architecture code qa deployment; do
    mkdir -p "$PROJECT_DIR/outputs/$dir"
done
for dir in feedback security compliance cost analytics; do
    mkdir -p "$PROJECT_DIR/outputs/$dir"
done
echo "[OK] Output directories ready (core + optional + analytics)"

echo "============================================"

if [ $ERRORS -gt 0 ]; then
    echo "Fix the above issues before starting."
    exit 1
fi

echo ""
echo "Choose execution mode:"
echo "  1) parallel    — phases run in DAG order; agents within a phase run concurrently"
echo "  2) sequential  — every agent runs one at a time (safer, easier to debug)"
echo "  3) interactive — open Claude Code and paste the prompt yourself (manual)"
echo "  4) status      — show current pipeline progress and exit"
echo ""
read -r -p "Mode [1/2/3/4, default=1]: " MODE_CHOICE

case "$MODE_CHOICE" in
    2) python3 "$PROJECT_DIR/scripts/orchestrator.py" --mode sequential ;;
    3)
        echo ""
        echo "Paste this prompt into Claude Code:"
        echo ""
        echo "  Start the SDLC automation pipeline."
        echo "  Read .claude/agents/00_environment_agent.md and execute it."
        echo "  The agent will autonomously trigger all subsequent agents."
        echo ""
        ;;
    4) python3 "$PROJECT_DIR/scripts/orchestrator.py" --status ;;
    *) python3 "$PROJECT_DIR/scripts/orchestrator.py" --mode parallel ;;
esac

echo "============================================"

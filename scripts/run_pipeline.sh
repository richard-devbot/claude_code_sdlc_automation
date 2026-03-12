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
echo "[OK] Output directories ready"

echo "============================================"

if [ $ERRORS -gt 0 ]; then
    echo "Fix the above issues before starting."
    exit 1
fi

echo ""
echo "To start the pipeline, open Claude Code and paste:"
echo ""
echo "  Start the SDLC automation pipeline."
echo "  Read .claude/agents/01_transcript_agent.md and execute it."
echo "  The agent will autonomously trigger all subsequent agents."
echo ""
echo "============================================"

#!/bin/bash
# Cleans all output directories for a fresh pipeline run.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TOTAL=0

echo "Cleaning output directories..."

for dir in transcripts requirements documents planning jira architecture code qa deployment; do
    DIR_PATH="$PROJECT_DIR/outputs/$dir"
    if [ -d "$DIR_PATH" ]; then
        COUNT=$(find "$DIR_PATH" -type f 2>/dev/null | wc -l)
        TOTAL=$((TOTAL + COUNT))
        rm -rf "$DIR_PATH"/*
        echo "  Cleaned: outputs/$dir/ ($COUNT files)"
    fi
done

# Clean root-level outputs
for f in PROJECT_COMPLETE_SUMMARY.md EXECUTIVE_DASHBOARD.md pipeline_final.json; do
    if [ -f "$PROJECT_DIR/outputs/$f" ]; then
        rm "$PROJECT_DIR/outputs/$f"
        TOTAL=$((TOTAL + 1))
        echo "  Cleaned: outputs/$f"
    fi
done

# Also clean environment report and setup instructions
for f in environment_report.json SETUP_INSTRUCTIONS.md; do
    if [ -f "$PROJECT_DIR/outputs/$f" ]; then
        rm "$PROJECT_DIR/outputs/$f"
        TOTAL=$((TOTAL + 1))
        echo "  Cleaned: outputs/$f"
    fi
done

# Re-create directory structure so agents never hit mkdir errors
for dir in transcripts requirements documents planning jira architecture code/backend code/frontend qa deployment/scripts; do
    mkdir -p "$PROJECT_DIR/outputs/$dir"
done

echo ""
echo "Total files removed: $TOTAL"
echo "Output directories are ready for a fresh pipeline run."

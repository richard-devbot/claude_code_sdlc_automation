#!/usr/bin/env python3
"""
Generates a summary report of all pipeline outputs.
Usage: python helpers/output_reporter.py
"""

import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIRS = {
    "transcripts": "Agent 01: Structured meeting data",
    "requirements": "Agent 02: Requirement specifications",
    "documents": "Agent 03: BRD, FRD, SOW documents",
    "planning": "Agent 04: Sprint plans",
    "jira": "Agent 05: Jira tickets",
    "architecture": "Agent 06: System design & HLD",
    "code": "Agent 07: Code scaffolding",
    "qa": "Agent 08: Test plans & cases",
    "deployment": "Agent 09: Deployment configs",
}


def get_size_str(size_bytes):
    """Convert bytes to human-readable size."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def scan_directory(dir_path):
    """Count files and total size in a directory."""
    total_files = 0
    total_size = 0
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            filepath = os.path.join(root, f)
            total_files += 1
            total_size += os.path.getsize(filepath)
    return total_files, total_size


def main():
    print("\n" + "=" * 65)
    print("  SDLC PIPELINE OUTPUT REPORT")
    print("=" * 65)

    grand_files = 0
    grand_size = 0

    for dir_name, description in OUTPUT_DIRS.items():
        dir_path = PROJECT_ROOT / "outputs" / dir_name
        if not dir_path.exists():
            print(f"\n  {dir_name}/  [{description}]")
            print(f"    (empty)")
            continue

        files, size = scan_directory(dir_path)
        grand_files += files
        grand_size += size

        print(f"\n  {dir_name}/  [{description}]")
        print(f"    Files: {files} | Size: {get_size_str(size)}")

        # List files
        for root, dirs, filenames in os.walk(dir_path):
            for f in sorted(filenames):
                fpath = os.path.join(root, f)
                fsize = os.path.getsize(fpath)
                relpath = os.path.relpath(fpath, PROJECT_ROOT)
                print(f"      {relpath} ({get_size_str(fsize)})")

    # Check root-level outputs
    for root_file in ["PROJECT_COMPLETE_SUMMARY.md", "EXECUTIVE_DASHBOARD.md", "pipeline_final.json"]:
        fpath = PROJECT_ROOT / "outputs" / root_file
        if fpath.exists():
            fsize = os.path.getsize(fpath)
            grand_files += 1
            grand_size += fsize
            print(f"\n  outputs/{root_file} ({get_size_str(fsize)})")

    print("\n" + "=" * 65)
    print(f"  TOTAL: {grand_files} files | {get_size_str(grand_size)}")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()

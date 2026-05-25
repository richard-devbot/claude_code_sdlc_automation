#!/usr/bin/env python3
"""
Cyclic auto-fix loop: Testing Agent → Code Agent.

Usage (called by the Testing Agent after test execution):
    python helpers/test_retry_loop.py

Logic:
  - Reads outputs/qa/qa_results.json for test failures
  - Reads outputs/qa/retry_state.json for current retry count
  - If failures exist AND retry_count < max_retries:
      → Writes outputs/qa/failed_tests.json (Code Agent reads this)
      → Increments retry_state.json
      → Exits with code 10 (signal: retry — invoke Code Agent)
  - If failures exist AND retry_count >= max_retries:
      → Exits with code 20 (signal: escalate — show user the failures)
  - If no failures:
      → Cleans up retry state
      → Exits with code 0 (signal: pass — proceed to Deployment Agent)

Exit codes:
  0  = All tests passed — continue to Deployment Agent
  10 = Tests failed, retry budget remaining — re-invoke Code Agent
  20 = Tests failed, max retries exhausted — escalate to user
"""

import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QA_DIR = PROJECT_ROOT / "outputs" / "qa"
QA_RESULTS = QA_DIR / "qa_results.json"
RETRY_STATE = QA_DIR / "retry_state.json"
FAILED_TESTS = QA_DIR / "failed_tests.json"
PIPELINE_YML = PROJECT_ROOT / "sdlc-pipeline.yml"

DEFAULT_MAX_RETRIES = 3


def load_max_retries():
    """Read max_retries from sdlc-pipeline.yml without a YAML library."""
    if not PIPELINE_YML.exists():
        return DEFAULT_MAX_RETRIES
    try:
        for line in PIPELINE_YML.read_text().splitlines():
            stripped = line.strip()
            if stripped.startswith("max_retries:"):
                val = stripped.split(":")[-1].strip()
                return int(val)
    except Exception:
        pass
    return DEFAULT_MAX_RETRIES


def load_retry_state():
    """Load current retry count and history."""
    if not RETRY_STATE.exists():
        return {"retry_count": 0, "history": []}
    try:
        with open(RETRY_STATE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"retry_count": 0, "history": []}


def save_retry_state(state):
    QA_DIR.mkdir(parents=True, exist_ok=True)
    with open(RETRY_STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def load_qa_results():
    if not QA_RESULTS.exists():
        print(f"ERROR: {QA_RESULTS} not found. Run Testing Agent first.")
        sys.exit(1)
    try:
        with open(QA_RESULTS, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: qa_results.json is malformed: {e}")
        sys.exit(1)


def extract_failures(qa_data):
    """Pull test failures from qa_results.json test_execution block."""
    execution = qa_data.get("test_execution", {})
    if not execution.get("ran", False):
        return []
    failures = execution.get("failures", [])
    backend = execution.get("backend", {})
    frontend = execution.get("frontend", {})
    if backend.get("failed", 0) == 0 and frontend.get("failed", 0) == 0:
        return []
    return failures


def write_failed_tests_contract(failures, retry_count, max_retries, qa_data):
    """Write the contract that the Code Agent will read for auto-fix."""
    contract = {
        "contract_version": "1.0",
        "produced_by": "test_retry_loop",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "retry_count": retry_count,
        "max_retries": max_retries,
        "retries_remaining": max_retries - retry_count,
        "instruction": (
            "The following tests failed. Read each failure's 'error' and "
            "'suggested_fix'. Update the relevant files in outputs/code/ to "
            "fix each failure. Then signal the Testing Agent to re-run."
        ),
        "failures": failures,
        "test_summary": qa_data.get("test_summary", {}),
        "source_qa_results": str(QA_RESULTS),
        "next_agent": "testing_agent",
        "next_input_file": str(FAILED_TESTS),
    }
    QA_DIR.mkdir(parents=True, exist_ok=True)
    with open(FAILED_TESTS, "w", encoding="utf-8") as f:
        json.dump(contract, f, indent=2)
    print(f"Wrote failed_tests.json with {len(failures)} failure(s).")


def clear_retry_state():
    """Remove retry artifacts after a clean pass."""
    for f in [RETRY_STATE, FAILED_TESTS]:
        if f.exists():
            f.unlink()


def main():
    max_retries = load_max_retries()
    qa_data = load_qa_results()
    failures = extract_failures(qa_data)

    if not failures:
        print("All tests passed. Clearing retry state.")
        clear_retry_state()
        sys.exit(0)

    state = load_retry_state()
    retry_count = state["retry_count"]

    print(f"\nTest failures detected: {len(failures)} failure(s).")
    print(f"Retry attempt: {retry_count + 1} of {max_retries}")

    if retry_count >= max_retries:
        print(
            f"\nMax retries ({max_retries}) exhausted. Escalating to user.\n"
            f"Review: {FAILED_TESTS}\n"
            "Options:\n"
            "  1. Fix the code manually and re-run Testing Agent\n"
            "  2. Accept current state and continue to Deployment Agent\n"
            "  3. Abort pipeline"
        )
        write_failed_tests_contract(failures, retry_count, max_retries, qa_data)
        sys.exit(20)

    state["retry_count"] = retry_count + 1
    state["history"].append({
        "attempt": retry_count + 1,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "failure_count": len(failures),
    })
    save_retry_state(state)
    write_failed_tests_contract(failures, retry_count + 1, max_retries, qa_data)

    print(
        f"\nRetry {retry_count + 1}/{max_retries}: failed_tests.json written.\n"
        "Invoke Code Agent to fix failures, then re-run Testing Agent."
    )
    sys.exit(10)


if __name__ == "__main__":
    main()

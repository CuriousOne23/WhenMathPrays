#!/usr/bin/env python3
# ============================================================
# ie_rulechecker.py — Rulechecker for IE Primitive (20.109)
# Path‑A Intake Envelope — Deterministic Replay Verification (v3.3)
# ============================================================

import sys
import yaml
from pathlib import Path

# Import the v3.3 IE primitive implementation
from thought_simulator.requirements_20.system_playground.primitives.ie.ie import run_ie

TESTBENCH_PATH = Path(__file__).parent / "ie_testbench.yaml"


def load_testbench(path: Path):
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("tests", [])


# ------------------------------------------------------------
# Comparison helpers
# ------------------------------------------------------------
def compare_dict(expected, actual, prefix=""):
    diffs = []
    for key, exp_val in expected.items():
        act_val = actual.get(key)
        if exp_val != act_val:
            diffs.append(f"{prefix}{key} mismatch: expected={exp_val!r}, actual={act_val!r}")
    return diffs


def compare_list(expected, actual, prefix=""):
    diffs = []
    if expected != actual:
        diffs.append(f"{prefix}list mismatch: expected={expected!r}, actual={actual!r}")
    return diffs


# ------------------------------------------------------------
# Compare full IE envelope (v3.3)
# ------------------------------------------------------------
def compare_envelope(expected, actual):
    diffs = []

    # intake.normalized_text
    diffs.extend(compare_dict(
        {"normalized_text": expected["intake"].get("normalized_text")},
        actual["intake"],
        prefix="intake."
    ))

    # intake.ie_tokens
    diffs.extend(compare_list(
        expected["intake"].get("ie_tokens", []),
        actual["intake"].get("ie_tokens", []),
        prefix="intake.ie_tokens: "
    ))

    # intake.token_flags
    diffs.extend(compare_list(
        expected["intake"].get("token_flags", []),
        actual["intake"].get("token_flags", []),
        prefix="intake.token_flags: "
    ))

    # structure.tags
    diffs.extend(compare_list(
        expected.get("structure", {}).get("tags", []),
        actual.get("structure", {}).get("tags", []),
        prefix="structure.tags: "
    ))

    # structure.spans
    diffs.extend(compare_list(
        expected.get("structure", {}).get("spans", []),
        actual.get("structure", {}).get("spans", []),
        prefix="structure.spans: "
    ))

    # structure.markup
    diffs.extend(compare_list(
        expected.get("structure", {}).get("markup", []),
        actual.get("structure", {}).get("markup", []),
        prefix="structure.markup: "
    ))

    # metadata.repair_annotations
    diffs.extend(compare_list(
        expected["metadata"].get("repair_annotations", []),
        actual["metadata"].get("repair_annotations", []),
        prefix="metadata.repair_annotations: "
    ))

    # metadata.replay
    diffs.extend(compare_dict(
        expected["metadata"].get("replay", {}),
        actual["metadata"].get("replay", {}),
        prefix="metadata.replay."
    ))

    # metadata.ruleset_id
    diffs.extend(compare_dict(
        {"ruleset_id": expected["metadata"].get("ruleset_id")},
        actual["metadata"],
        prefix="metadata."
    ))

    # error
    diffs.extend(compare_dict(
        {"error": expected.get("error")},
        actual,
        prefix=""
    ))

    return diffs


# ------------------------------------------------------------
# Run a single test
# ------------------------------------------------------------
def run_single_test(test):
    iiinb_output = test.get("iiinb_output", {})
    expected = test.get("expected", {})

    actual = run_ie(iiinb_output)
    diffs = compare_envelope(expected, actual)

    status = "PASS" if not diffs else "FAIL"
    return status, diffs


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    tests = load_testbench(TESTBENCH_PATH)

    passed = 0
    failed = 0

    print("IE Rulechecker — Deterministic Replay Verification (v3.3)")
    print("==========================================================")

    for test in tests:
        test_id = test.get("id", "<unnamed>")
        description = test.get("description", "")
        status, diffs = run_single_test(test)

        print(f"\nTest: {test_id}")
        print(f"Desc: {description}")
        print(f"Result: {status}")

        if status == "PASS":
            passed += 1
        else:
            failed += 1
            for d in diffs:
                print(f"  - {d}")

    print("\nSummary")
    print("-------")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()

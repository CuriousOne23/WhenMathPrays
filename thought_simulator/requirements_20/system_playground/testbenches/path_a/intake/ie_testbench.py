#!/usr/bin/env python3
# ============================================================
# IE Testbench — Deterministic Replay Verification (v3.3)
# Path‑A Intake Envelope — 20.109 IE Primitive
# ============================================================

import yaml
from pathlib import Path
from thought_simulator.requirements_20.system_playground.primitives.ie.ie import run_ie

ROOT = Path(__file__).parent
TESTBENCH = ROOT / "ie_testbench.yaml"
TESTS_TO_RUN = ROOT / "ie_tests_to_run.yaml"


# ------------------------------------------------------------
# Utility: load YAML
# ------------------------------------------------------------
def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------
# Comparison helpers
# ------------------------------------------------------------
def compare_dict(expected, actual, prefix=""):
    diffs = []
    for key, exp_val in expected.items():
        act_val = actual.get(key)
        if exp_val != act_val:
            diffs.append(
                f"{prefix}{key} mismatch: expected={exp_val!r}, actual={act_val!r}"
            )
    return diffs


def compare_list(expected, actual, prefix=""):
    diffs = []
    if expected != actual:
        diffs.append(
            f"{prefix}list mismatch: expected={expected!r}, actual={actual!r}"
        )
    return diffs


# ------------------------------------------------------------
# Compare full IE envelope (v3.3)
# ------------------------------------------------------------
def compare_envelope(expected, actual):
    diffs = []

    # intake.normalized_text
    diffs.extend(
        compare_dict(
            {"normalized_text": expected["intake"].get("normalized_text")},
            actual["intake"],
            prefix="intake."
        )
    )

    # intake.ie_tokens
    diffs.extend(
        compare_list(
            expected["intake"].get("ie_tokens", []),
            actual["intake"].get("ie_tokens", []),
            prefix="intake.ie_tokens: "
        )
    )

    # intake.token_flags
    diffs.extend(
        compare_list(
            expected["intake"].get("token_flags", []),
            actual["intake"].get("token_flags", []),
            prefix="intake.token_flags: "
        )
    )

    # structure.tags
    diffs.extend(
        compare_list(
            expected.get("structure", {}).get("tags", []),
            actual.get("structure", {}).get("tags", []),
            prefix="structure.tags: "
        )
    )

    # structure.spans
    diffs.extend(
        compare_list(
            expected.get("structure", {}).get("spans", []),
            actual.get("structure", {}).get("spans", []),
            prefix="structure.spans: "
        )
    )

    # structure.markup
    diffs.extend(
        compare_list(
            expected.get("structure", {}).get("markup", []),
            actual.get("structure", {}).get("markup", []),
            prefix="structure.markup: "
        )
    )

    # metadata.repair_annotations
    diffs.extend(
        compare_list(
            expected["metadata"].get("repair_annotations", []),
            actual["metadata"].get("repair_annotations", []),
            prefix="metadata.repair_annotations: "
        )
    )

    # metadata.replay
    diffs.extend(
        compare_dict(
            expected["metadata"].get("replay", {}),
            actual["metadata"].get("replay", {}),
            prefix="metadata.replay."
        )
    )

    # metadata.ruleset_id
    diffs.extend(
        compare_dict(
            {"ruleset_id": expected["metadata"].get("ruleset_id")},
            actual["metadata"],
            prefix="metadata."
        )
    )

    # error
    diffs.extend(
        compare_dict(
            {"error": expected.get("error")},
            actual,
            prefix=""
        )
    )

    return diffs


# ------------------------------------------------------------
# Run a single test
# ------------------------------------------------------------
def run_single_test(test):
    test_id = test["id"]
    description = test.get("description", "")
    iiinb_output = test.get("iiinb_output", {})
    expected = test.get("expected", {})

    actual = run_ie(iiinb_output)

    diffs = compare_envelope(expected, actual)
    status = "PASS" if not diffs else "FAIL"

    return status, diffs


# ------------------------------------------------------------
# Main testbench runner
# ------------------------------------------------------------
def main():
    testbench = load_yaml(TESTBENCH)
    tests_to_run = load_yaml(TESTS_TO_RUN).get("tests_to_run", [])

    enabled_ids = {t["id"] for t in tests_to_run if t.get("enabled", False)}

    print("IE Testbench — Deterministic Replay Verification (v3.3)")
    print("========================================================")

    passed = 0
    failed = 0
    skipped = 0

    for test in testbench.get("tests", []):
        test_id = test["id"]
        description = test.get("description", "")

        if test_id not in enabled_ids:
            print(f"\nTest: {test_id}")
            print(f"Desc: {description}")
            print("Result: SKIPPED")
            skipped += 1
            continue

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
    total = passed + failed + skipped
    print(f"Total:   {total}")
    print(f"Passed:  {passed}")
    print(f"Failed:  {failed}")
    print(f"Skipped: {skipped}")


# ------------------------------------------------------------
# Integration hooks for run.py
# ------------------------------------------------------------
_testbench_config = {
    "mode": "testbench",
    "use_inb": False,
    "use_iiinb": True,
    "use_ie": True,
    "tests_to_run": "see ie_tests_to_run.yaml",
}

def set_testbench_config(config: dict):
    global _testbench_config
    _testbench_config = config

def run_testbench():
    print("IE Testbench Configuration:", _testbench_config)
    main()

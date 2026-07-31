#!/usr/bin/env python3
# ============================================================
# ie_rulechecker.py — Rulechecker for IE Primitive (20.109)
# Path‑A Intake Envelope — Deterministic Replay Verification
# ============================================================

import sys
import yaml
from pathlib import Path

# Import the IE primitive implementation
from thought_simulator.requirements_20.system_playground.primitives.ie.ie import IE


TESTBENCH_PATH = Path(__file__).parent / "ie_testbench.yaml"


def load_testbench(path: Path):
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("tests", [])


def normalize_none(value):
    return None if value is None else value


def compare_intake(expected, actual):
    diffs = []

    exp_intake = expected.get("intake", {})
    act_intake = actual.get("intake", {})

    # normalized_text
    if "normalized_text" in exp_intake:
        if exp_intake["normalized_text"] != act_intake.get("normalized_text"):
            diffs.append(
                f"intake.normalized_text mismatch: expected={exp_intake['normalized_text']!r}, "
                f"actual={act_intake.get('normalized_text')!r}"
            )

    # tokens
    if "tokens" in exp_intake:
        if exp_intake["tokens"] != act_intake.get("tokens"):
            diffs.append(
                f"intake.tokens mismatch: expected={exp_intake['tokens']!r}, "
                f"actual={act_intake.get('tokens')!r}"
            )

    # token_flags
    if "token_flags" in exp_intake:
        if exp_intake["token_flags"] != act_intake.get("token_flags"):
            diffs.append(
                f"intake.token_flags mismatch: expected={exp_intake['token_flags']!r}, "
                f"actual={act_intake.get('token_flags')!r}"
            )

    return diffs


def compare_structure(expected, actual):
    diffs = []

    exp_struct = expected.get("structure", {})
    act_struct = actual.get("structure", {})

    # tags
    if "tags" in exp_struct:
        if exp_struct["tags"] != act_struct.get("tags"):
            diffs.append(
                f"structure.tags mismatch: expected={exp_struct['tags']!r}, "
                f"actual={act_struct.get('tags')!r}"
            )

    return diffs


def compare_metadata(expected, actual):
    diffs = []

    exp_meta = expected.get("metadata", {})
    act_meta = actual.get("metadata", {})

    # repair_annotations
    if "repair_annotations" in exp_meta:
        if exp_meta["repair_annotations"] != act_meta.get("repair_annotations"):
            diffs.append(
                "metadata.repair_annotations mismatch:\n"
                f"  expected={exp_meta['repair_annotations']!r}\n"
                f"  actual={act_meta.get('repair_annotations')!r}"
            )

    # replay
    if "replay" in exp_meta:
        if exp_meta["replay"] != act_meta.get("replay"):
            diffs.append(
                "metadata.replay mismatch:\n"
                f"  expected={exp_meta['replay']!r}\n"
                f"  actual={act_meta.get('replay')!r}"
            )

    # ruleset_id
    if "ruleset_id" in exp_meta:
        if exp_meta["ruleset_id"] != act_meta.get("ruleset_id"):
            diffs.append(
                f"metadata.ruleset_id mismatch: expected={exp_meta['ruleset_id']!r}, "
                f"actual={act_meta.get('ruleset_id')!r}"
            )

    return diffs


def compare_error(expected, actual):
    diffs = []

    exp_err = normalize_none(expected.get("error"))
    act_err = normalize_none(actual.get("error"))

    if exp_err != act_err:
        diffs.append(
            f"error mismatch: expected={exp_err!r}, actual={act_err!r}"
        )

    return diffs


def run_single_test(test):
    test_id = test.get("id", "<unnamed>")
    iiinb_output = test.get("iiinb_output", {})
    expected = test.get("expected", {})

    # Build a minimal IIInB output object for IE
    class IIInBOutput:
        def __init__(self, src):
            self.normalized = src.get("normalized", None)
            self.tokens = src.get("tokens", [])
            self.repair_operations = src.get("repair_operations", [])
            self.anomaly_flags = src.get("anomaly_flags", [])
            self.structure = src.get("structure", {})

    src = IIInBOutput(iiinb_output)

    # Run IE
    ie = IE(src)
    ie.inspect()

    # Build actual envelope in the same shape as expected
    actual = {
        "intake": {
            "normalized_text": getattr(ie, "intake", {}).get("normalized_text"),
            "tokens": getattr(ie, "intake", {}).get("tokens"),
            "token_flags": getattr(ie, "intake", {}).get("token_flags"),
        },
        "structure": {
            "tags": getattr(ie, "structure", {}).get("tags"),
        },
        "metadata": {
            "repair_annotations": getattr(ie, "metadata", {}).get("repair_annotations"),
            "replay": getattr(ie, "metadata", {}).get("replay"),
            "ruleset_id": getattr(ie, "metadata", {}).get("ruleset_id"),
        },
        "error": ie.error,
    }

    diffs = []
    diffs.extend(compare_intake(expected, actual))
    diffs.extend(compare_structure(expected, actual))
    diffs.extend(compare_metadata(expected, actual))
    diffs.extend(compare_error(expected, actual))

    status = "PASS" if not diffs else "FAIL"
    return status, diffs


def main():
    tests = load_testbench(TESTBENCH_PATH)

    passed = 0
    failed = 0

    print("IE Rulechecker — Deterministic Replay Verification")
    print("==================================================")

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


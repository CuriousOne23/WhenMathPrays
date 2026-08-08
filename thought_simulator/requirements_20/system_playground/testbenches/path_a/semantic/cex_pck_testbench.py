"""
cex_pck_testbench.py

Deterministic testbench for the CEx-Pck primitive.
This module loads:
  - cex_pck_input.yaml
  - cex_pck_rules.yaml
  - cex_pck_tests_to_run.yaml

It executes:
  - CEx-Pck (via cex_pck.py)
  - Rulechecker (cex_pck_rulechecker.py)

It compares:
  - TP output against expected fields in cex_pck_testbench.yaml

This file is invoked by testbenches/run.py.
"""

import os
import json
import yaml
import subprocess
from typing import Any, Dict


ROOT = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(ROOT, "cex_pck_input.yaml")
RULES_PATH = os.path.join(ROOT, "cex_pck_rules.yaml")
TESTS_PATH = os.path.join(ROOT, "cex_pck_tests_to_run.yaml")
EXPECTED_PATH = os.path.join(ROOT, "cex_pck_testbench.yaml")
RULECHECKER_PATH = os.path.join(ROOT, "cex_pck_rulechecker.py")

# Path to the primitive implementation
CEX_PCK_IMPL = os.path.join(
    ROOT,
    "../../../primitives/cex_pck/cex_pck.py"
)


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_cex_pck(tp_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes the CEx-Pck primitive by importing cex_pck.py.
    Returns the updated TP dictionary.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("cex_pck", CEX_PCK_IMPL)
    cex_pck_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cex_pck_module)

    CExPck = cex_pck_module.CExPck
    pck = CExPck(tp_input)
    pck.inspect()

    return pck.tp


def run_rulechecker(tp_before: Dict[str, Any], tp_after: Dict[str, Any]) -> bool:
    """
    Runs cex_pck_rulechecker.py as a subprocess.
    Returns True if rulecheck passes.
    """

    # Write TP before/after
    before_path = os.path.join(ROOT, "_tp_before.json")
    after_path = os.path.join(ROOT, "_tp_after.json")

    with open(before_path, "w", encoding="utf-8") as f:
        json.dump(tp_before, f, indent=2)

    with open(after_path, "w", encoding="utf-8") as f:
        json.dump(tp_after, f, indent=2)

    # NEW: Load YAML rules here in the testbench
    rules = load_yaml(RULES_PATH)

    # Convert rules to JSON for the rulechecker
    rules_json_path = os.path.join(ROOT, "_rules_tmp.json")
    with open(rules_json_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2)

    import sys

    cmd = [
        sys.executable,   # use same interpreter
        RULECHECKER_PATH,
        rules_json_path,  # pass JSON rules instead of YAML
        before_path,
        after_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Print BOTH stdout and stderr so rulecheck failures are visible
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode == 0


def compare_expected(tp_after: Dict[str, Any], expected: Dict[str, Any]) -> bool:
    """
    Compares TP output against expected fields in cex_pck_testbench.yaml.
    Only checks fields explicitly listed in expected.
    """
    def get_nested(d: Dict[str, Any], path: str):
        cur = d
        for part in path.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                return None
        return cur

    ok = True
    for field_path, expected_value in expected.items():
        actual = get_nested(tp_after, field_path)
        if actual != expected_value:
            print(f"[Mismatch] {field_path}: expected={expected_value!r}, got={actual!r}")
            ok = False

    return ok


def run_testbench():
    tests = load_yaml(TESTS_PATH)["tests_to_run"]
    expected = load_yaml(EXPECTED_PATH)["expected"]

    for test in tests:
        if not test.get("active", False):
            continue

        print(f"\n=== Running Test: {test['id']} ===")
        print(f"Description: {test['description']}")

        tp_input = load_yaml(INPUT_PATH)
        tp_before = json.loads(json.dumps(tp_input))  # deep copy

        # Run CEx-Pck
        tp_after = run_cex_pck(tp_input)

        # Rulecheck
        print("\n--- Rulecheck ---")
        rulecheck_passed = run_rulechecker(tp_before, tp_after)

        # Expected comparison
        print("\n--- Expected Output Comparison ---")
        expected_passed = compare_expected(tp_after, expected)

        # Summary
        print("\n=== Test Summary ===")
        print(f"Test ID: {test['id']}")
        print(f"Description: {test['description']}")

        print("\nResults:")
        print(f"  Rulecheck: {'PASSED' if rulecheck_passed else 'FAILED'}")
        print(f"  Expected Output Comparison: {'PASSED' if expected_passed else 'FAILED'}")

        if rulecheck_passed and expected_passed:
            print("\nOverall: SUCCESS - TP is valid and correct.\n")
        else:
            print("\nOverall: FAILURE - see details above.\n")
            return False

    return True


if __name__ == "__main__":
    success = run_testbench()
    if success:
        print("All active CEx-Pck tests PASSED.")
    else:
        print("One or more CEx-Pck tests FAILED.")

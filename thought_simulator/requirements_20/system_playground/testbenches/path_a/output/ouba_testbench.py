"""
OuBA Testbench (Version 0.1)
  - mode == "testbench" -> ouba_testbench.yaml (deterministic structural comparison)
  - mode == "general"   -> ouba_input.yaml + ouba_rules.yaml
Aligned with progressive_lineup_testing.md, 20.40.060.xxx, and ouba_py_struc_pgm.md.
"""

from __future__ import annotations

import copy
import json
import os
import sys

import yaml

TB_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from thought_simulator.requirements_20.system_playground.primitives.ouba.ouba import (  # noqa: E402
    OUBA,
    get_primitive_name,
)
from thought_simulator.requirements_20.system_playground.testbenches.path_a.output.ouba_rulechecker import (  # noqa: E402
    OUBARuleChecker,
)

assert get_primitive_name() == "ouba", (
    f"Primitive name mismatch: expected ouba, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _subset_compare(actual, expected, path=""):
    """Compare expected as a recursive subset of actual; exact at provided leaves."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False, f"{path or '<root>'}: expected dict, got {type(actual).__name__}"
        for key, exp_val in expected.items():
            if key not in actual:
                return False, f"{path + '.' if path else ''}{key}: missing key"
            ok, msg = _subset_compare(
                actual[key],
                exp_val,
                f"{path + '.' if path else ''}{key}",
            )
            if not ok:
                return False, msg
        return True, None

    if isinstance(expected, list):
        if actual != expected:
            return False, f"{path}: expected {expected!r}, got {actual!r}"
        return True, None

    if actual != expected:
        return False, f"{path}: expected {expected!r}, got {actual!r}"
    return True, None


def _compare_ouba(tp_input, tp_output, expected):
    tpsns = tp_output.get("TPSnS") if isinstance(tp_output.get("TPSnS"), dict) else {}

    if expected.get("expect_ouba_complete", True):
        if tp_output.get("ouba_complete") is not True:
            return False, "ouba_complete expected True"

    if "tpsns" in expected:
        ok, msg = _subset_compare(tpsns, expected["tpsns"], "TPSnS")
        if not ok:
            return False, msg

    if expected.get("ctp_equals_tpsns"):
        if tp_output.get("CTP") != tp_output.get("TPSnS"):
            return False, "CTP does not match TPSnS"

    if expected.get("check_replay"):
        replay = OUBA(copy.deepcopy(tp_input)).process(mode="testbench")
        if replay.get("TPSnS") != tp_output.get("TPSnS"):
            return False, "deterministic replay mismatch"

    if expected.get("check_write_boundary"):
        if "TR" in tp_input and tp_input.get("TR") != tp_output.get("TR"):
            return False, "TR was modified"
        in_proc = tp_input.get("process") if isinstance(tp_input.get("process"), dict) else {}
        out_proc = tp_output.get("process") if isinstance(tp_output.get("process"), dict) else {}
        if "routing_filter" in in_proc:
            if in_proc.get("routing_filter") != out_proc.get("routing_filter"):
                return False, "process.routing_filter was modified"
        in_meta = tp_input.get("metadata") if isinstance(tp_input.get("metadata"), dict) else {}
        out_meta = tp_output.get("metadata") if isinstance(tp_output.get("metadata"), dict) else {}
        for key in ("geometric_state", "geometric_history", "residue"):
            if key in in_meta and in_meta.get(key) != out_meta.get(key):
                return False, f"metadata.{key} was modified"

    return True, None


def run_single_test(test_entry):
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)

    print("\n------------------------------------------------------------")
    print(f"Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    use_ouba = (TESTBENCH_CONFIG or {}).get("use_ouba", True)

    rules_file = os.path.join(BASE_DIR, "ouba_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "ouba_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in ouba_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: ouba_testbench.yaml (testbench mode)")
    print("- Expected Output Source: ouba_testbench.yaml (expected block)")

    if not use_ouba:
        print("- use_ouba=False -> passthrough path; expected comparison skipped")
        tp_output = copy.deepcopy(tp_input)
        return {
            "id": test_id,
            "enabled": True,
            "passed": True,
            "errors": [],
            "passthrough": True,
        }

    ouba = OUBA(copy.deepcopy(tp_input))
    tp_output = ouba.process(mode="testbench")

    structural_match, diff_msg = _compare_ouba(tp_input, tp_output, expected)

    checker = OUBARuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- OuBA Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")

    if rule_errors:
        print("- Rule Violations (diagnostic):")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    tpsns = tp_output.get("TPSnS") if isinstance(tp_output.get("TPSnS"), dict) else {}
    print("\nCommit Summary:")
    print(f"- tpsns_id: {tpsns.get('tpsns_id')}")
    print(f"- commit_timestamp: {tpsns.get('commit_timestamp')}")
    print(f"- routing_epoch_id: {tpsns.get('routing_epoch_id')}")
    print(f"- commit_hash: {tpsns.get('commit_hash')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: ouba_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: ouba_input.yaml (general mode)")
    print("- Checked By: ouba_rules.yaml (rule-driven validation)")

    use_ouba = (TESTBENCH_CONFIG or {}).get("use_ouba", True)

    rules_file = os.path.join(BASE_DIR, "ouba_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "ouba_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    if use_ouba:
        tp_output = OUBA(copy.deepcopy(tp_input)).process(mode="general")
    else:
        print("- use_ouba=False -> passthrough path")
        tp_output = copy.deepcopy(tp_input)

    rule_errors = []
    if use_ouba:
        checker = OUBARuleChecker(tp_input, tp_output, rules)
        rule_errors = checker.run()

    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_ouba_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    tpsns = tp_output.get("TPSnS") if isinstance(tp_output.get("TPSnS"), dict) else {}
    print("\n----- OuBA Commit -----")
    print(json.dumps(tpsns, indent=2, sort_keys=True))

    return {
        "id": "general_ouba_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" OuBA Testbench Runner - Starting Execution")
    print("============================================================")

    mode = (TESTBENCH_CONFIG or {}).get("mode", "testbench")
    print(f"- Mode: {mode}")

    results = []
    total = passed = failed = 0

    if mode == "general":
        result = run_general_mode()
        results.append(result)
        total = 1
        if result["passed"]:
            passed = 1
        else:
            failed = 1
    else:
        tests_to_run_file = os.path.join(BASE_DIR, "ouba_tests_to_run.yaml")
        tests_to_run = load_yaml(tests_to_run_file)
        tests = tests_to_run.get("tests", [])

        for test in tests:
            result = run_single_test(test)
            if not test.get("enabled", False):
                continue
            total += 1
            if result["passed"]:
                passed += 1
            else:
                failed += 1
            results.append(result)

    print("\n============================================================")
    print(" OuBA Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" OuBA Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench", "use_ouba": True})
    run_testbench()

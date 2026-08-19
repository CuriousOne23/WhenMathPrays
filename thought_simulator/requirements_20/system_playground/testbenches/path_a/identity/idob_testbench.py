"""
IdOB Testbench (Version 0.1)
  • mode == "testbench" → idob_testbench.yaml structural foundation match
  • mode == "general"   → idob_input.yaml + idob_rules.yaml
Aligned with progressive_lineup_testing.md v4.2,
20.40.050_idob_prim.md v3.0, idob_py_struc_pgm.md v0.1.
"""

from __future__ import annotations

import copy
import json
import os
import sys

import yaml

# Mandatory import-path initialization (progressive_lineup 3.7)
TB_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from thought_simulator.requirements_20.system_playground.testbenches.path_a.identity.idob_rulechecker import (  # noqa: E402
    IdOBRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.idob.idob import (  # noqa: E402
    IdOB,
    get_primitive_name,
)

assert get_primitive_name() == "idob", (
    f"Primitive name mismatch: expected idob, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _identity(tp):
    return ((tp or {}).get("metadata") or {}).get("identity") or {}


def _compare_idob(actual_tp, expected):
    """Structural foundation comparison for IdOB envelope + flags."""
    act_id = _identity(actual_tp)
    exp_id = (expected or {}).get("identity") or {}

    for key in ("geometry", "continuity", "pressure"):
        if key in exp_id:
            if act_id.get(key) != exp_id.get(key):
                return False, f"identity.{key} expected {exp_id.get(key)!r}, got {act_id.get(key)!r}"

    if "residuals" in exp_id:
        act_r = act_id.get("residuals") or {}
        exp_r = exp_id.get("residuals") or {}
        for rk in ("magnitude", "pattern"):
            if rk in exp_r and act_r.get(rk) != exp_r.get(rk):
                return False, f"identity.residuals.{rk} expected {exp_r.get(rk)!r}, got {act_r.get(rk)!r}"

    if "freeze" in exp_id:
        act_f = (act_id.get("freeze") or {}).get("state")
        exp_f = (exp_id.get("freeze") or {}).get("state")
        if act_f != exp_f:
            return False, f"identity.freeze.state expected {exp_f!r}, got {act_f!r}"

    if "basin_surface" in exp_id:
        act_b = (act_id.get("basin_surface") or {}).get("region")
        exp_b = (exp_id.get("basin_surface") or {}).get("region")
        if act_b != exp_b:
            return False, f"identity.basin_surface.region expected {exp_b!r}, got {act_b!r}"

    if "idob_complete" in expected:
        if actual_tp.get("idob_complete") != expected["idob_complete"]:
            return False, f"idob_complete expected {expected['idob_complete']}, got {actual_tp.get('idob_complete')}"

    if "path_b_eligible" in expected:
        if actual_tp.get("path_b_eligible") != expected["path_b_eligible"]:
            return False, f"path_b_eligible expected {expected['path_b_eligible']}, got {actual_tp.get('path_b_eligible')}"

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

    rules_file = os.path.join(BASE_DIR, "idob_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "idob_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in idob_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: idob_testbench.yaml (testbench mode)")
    print("- Expected Output Source: idob_testbench.yaml (expected block)")

    idob = IdOB(copy.deepcopy(tp_input))
    tp_output = idob.process(mode="testbench")

    structural_match, diff_msg = _compare_idob(tp_output, expected)

    checker = IdOBRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- IdOB Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        print("ACTUAL identity envelope:")
        print(json.dumps(_identity(tp_output), indent=2, sort_keys=True))
        print(f"idob_complete: {tp_output.get('idob_complete')}")
        print(f"path_b_eligible: {tp_output.get('path_b_eligible')}")

    if rule_errors:
        print("- Rule Violations (diagnostic):")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    act = _identity(tp_output)
    print("\nIdentity Summary:")
    print(f"- geometry: {act.get('geometry')}")
    print(f"- continuity: {act.get('continuity')}")
    print(f"- pressure: {act.get('pressure')}")
    print(f"- residuals: {act.get('residuals')}")
    print(f"- freeze: {(act.get('freeze') or {}).get('state')}")
    print(f"- basin_surface: {(act.get('basin_surface') or {}).get('region')}")
    print(f"- idob_complete: {tp_output.get('idob_complete')}")
    print(f"- path_b_eligible: {tp_output.get('path_b_eligible')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: idob_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: idob_input.yaml (general mode)")
    print("- Checked By: idob_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "idob_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "idob_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    idob = IdOB(copy.deepcopy(tp_input))
    tp_output = idob.process(mode="general")

    checker = IdOBRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_idob_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    print("\n----- IdOB identity envelope -----")
    print(json.dumps(_identity(tp_output), indent=2, sort_keys=True))
    print(f"idob_complete: {tp_output.get('idob_complete')}")
    print(f"path_b_eligible: {tp_output.get('path_b_eligible')}")

    return {
        "id": "general_idob_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" IdOB Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "idob_tests_to_run.yaml")
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
    print(" IdOB Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" IdOB Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

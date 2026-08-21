"""
CIL Testbench (Version 0.1 — identity-selection slice)
  • mode == "testbench" → cil_testbench.yaml structural match
  • mode == "general"   → cil_input.yaml + cil_rules.yaml
Aligned with progressive_lineup_testing.md v4.2,
20.33, cil_requirements.md, cil_py_struc_pgm.md, cil_testbench_schema.md.
"""

from __future__ import annotations

import copy
import os
import sys

import yaml

# Mandatory import-path initialization
TB_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cil_rulechecker import (  # noqa: E402
    CILRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.cil.cil import (  # noqa: E402
    get_primitive_name,
    process as cil_process,
)

assert get_primitive_name() == "cil", (
    f"Primitive name mismatch: expected cil, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _get_path(d: dict, path: list):
    cur = d
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def _compare_identity_selection(actual: dict, expected: dict) -> list:
    """Strict comparison of identity_selection block fields."""
    diffs = []
    if not isinstance(actual, dict):
        return [f"identity_selection missing or not a dict: {actual!r}"]
    if not isinstance(expected, dict):
        return ["expected identity_selection is not a dict"]

    for key in ("primary_identity", "secondary_identity", "ordering_score"):
        if key not in expected:
            continue
        exp = expected[key]
        act = actual.get(key)
        if key == "ordering_score":
            try:
                if float(act) != float(exp):
                    diffs.append(f"{key}: expected {exp}, got {act}")
            except (TypeError, ValueError):
                if act != exp:
                    diffs.append(f"{key}: expected {exp}, got {act}")
        else:
            if act != exp:
                diffs.append(f"{key}: expected {exp}, got {act}")

    exp_om = expected.get("ordering_metrics") or {}
    act_om = actual.get("ordering_metrics") or {}
    for key, exp in exp_om.items():
        act = act_om.get(key)
        if key in ("density",):
            try:
                if float(act) != float(exp):
                    diffs.append(f"ordering_metrics.{key}: expected {exp}, got {act}")
            except (TypeError, ValueError):
                if act != exp:
                    diffs.append(f"ordering_metrics.{key}: expected {exp}, got {act}")
        else:
            if act != exp:
                diffs.append(f"ordering_metrics.{key}: expected {exp}, got {act}")

    return diffs


def run_single_test(test_entry):
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)

    print("\n------------------------------------------------------------")
    print(f"Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    rules_file = os.path.join(BASE_DIR, "cil_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "cil_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in cil_testbench.yaml")

    tp_input = copy.deepcopy(tb_test["input"])
    expected = tb_test.get("expected") or {}

    print("- Input Source: cil_testbench.yaml (testbench mode)")
    print("- Expected Output Source: cil_testbench.yaml (expected block)")

    tp_before = copy.deepcopy(tp_input)
    tp_output = cil_process(copy.deepcopy(tp_input), mode="testbench")

    diffs = []

    # Compare identity_selection under canonical path
    exp_sel = _get_path(expected, ["cil", "intake_packet", "identity_selection"])
    act_sel = _get_path(tp_output, ["cil", "intake_packet", "identity_selection"])
    if exp_sel is not None:
        diffs.extend(_compare_identity_selection(act_sel or {}, exp_sel))

    # Compare cob snapshot intact when expected
    exp_snap = _get_path(expected, ["identity", "cob_state_snapshot"])
    if exp_snap is not None:
        act_snap = _get_path(tp_output, ["identity", "cob_state_snapshot"])
        if act_snap != exp_snap:
            diffs.append("identity.cob_state_snapshot diverged from expected")

    # semantic_core must remain if present in expected
    if "semantic_core" in expected:
        if tp_output.get("semantic_core") != expected.get("semantic_core"):
            diffs.append("semantic_core mutated or missing")

    # Packet must exist at canonical path
    packet = _get_path(tp_output, ["cil", "intake_packet"])
    if not isinstance(packet, dict):
        diffs.append("TP.cil.intake_packet missing")

    # routing_path should include cil
    rp = tp_output.get("routing_path") or []
    if "cil" not in rp:
        diffs.append("routing_path missing 'cil'")

    checker = CILRuleChecker(tp_before, tp_output, rules)
    rule_errors = checker.run()

    passed = len(diffs) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if passed else 'FAIL'}")
    if diffs:
        print("- Diffs:")
        for m in diffs:
            print(f"  * {m}")
    if rule_errors:
        print("- Rule Violations (diagnostic):")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    print("\nContext Summary:")
    sel = act_sel or {}
    print(f"- primary_identity: {sel.get('primary_identity')}")
    print(f"- secondary_identity: {sel.get('secondary_identity')}")
    print(f"- ordering_score: {sel.get('ordering_score')}")
    om = sel.get("ordering_metrics") or {}
    print(f"- ordering_metrics.recency: {om.get('recency')}")
    print(f"- ordering_metrics.frequency: {om.get('frequency')}")
    print(f"- ordering_metrics.density: {om.get('density')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: cil_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: cil_input.yaml (general mode)")
    print("- Checked By: cil_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "cil_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "cil_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    tp_before = copy.deepcopy(tp_input)
    tp_output = cil_process(copy.deepcopy(tp_input), mode="general")

    checker = CILRuleChecker(tp_before, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_cil_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    sel = _get_path(tp_output, ["cil", "intake_packet", "identity_selection"]) or {}
    print("\nContext Summary:")
    print(f"- primary_identity: {sel.get('primary_identity')}")
    print(f"- secondary_identity: {sel.get('secondary_identity')}")
    print(f"- ordering_score: {sel.get('ordering_score')}")
    print(f"- routing_path: {tp_output.get('routing_path')}")

    return {
        "id": "general_cil_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" CIL Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "cil_tests_to_run.yaml")
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
    print(" CIL Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" CIL Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

"""
MCB Testbench (Version 0.1)
  • mode == "testbench" → mcb_testbench.yaml structural foundation match
  • mode == "general"   → mcb_input.yaml + mcb_rules.yaml
Aligned with progressive_lineup_testing.md v4.2,
20.40.055_mcb_prim.md v2.0, mcb_py_struc_pgm.md v0.1.
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

from thought_simulator.requirements_20.system_playground.testbenches.path_a.identity.mcb_rulechecker import (  # noqa: E402
    MCBRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.mcb.mcb import (  # noqa: E402
    MCB,
    get_primitive_name,
)

assert get_primitive_name() == "mcb", (
    f"Primitive name mismatch: expected mcb, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _next_context(tp):
    return (tp or {}).get("next_context") or {}


def _compare_mcb(actual_tp, expected):
    """Structural foundation comparison for MCB next_context + flags + delta."""
    act_nc = _next_context(actual_tp)
    exp_nc = (expected or {}).get("next_context") or {}

    for key in (
        "topic",
        "stance",
        "intent",
        "continuity",
        "direction",
        "coherence",
        "shift_required",
        "importance",
    ):
        if key in exp_nc:
            if act_nc.get(key) != exp_nc.get(key):
                return False, (
                    f"next_context.{key} expected {exp_nc.get(key)!r}, "
                    f"got {act_nc.get(key)!r}"
                )

    if "mcb_complete" in expected:
        if actual_tp.get("mcb_complete") != expected["mcb_complete"]:
            return False, (
                f"mcb_complete expected {expected['mcb_complete']}, "
                f"got {actual_tp.get('mcb_complete')}"
            )

    if "mcb_context_coherence" in expected:
        act_coh = ((actual_tp.get("semantic") or {}).get("mcb_context_coherence"))
        if act_coh != expected["mcb_context_coherence"]:
            return False, (
                f"mcb_context_coherence expected {expected['mcb_context_coherence']}, "
                f"got {act_coh}"
            )

    if "mcb_context_shift_required" in expected:
        act_shift = ((actual_tp.get("semantic") or {}).get("mcb_context_shift_required"))
        if act_shift != expected["mcb_context_shift_required"]:
            return False, (
                f"mcb_context_shift_required expected {expected['mcb_context_shift_required']}, "
                f"got {act_shift}"
            )

    # Optional delta magnitude band (exact float is brittle; allow expected scalar)
    if "mcb_delta_h" in expected:
        act_delta = (actual_tp.get("semantic") or {}).get("mcb_delta_h")
        exp_delta = expected["mcb_delta_h"]
        if isinstance(exp_delta, (int, float)) and isinstance(act_delta, (int, float)):
            if abs(float(act_delta) - float(exp_delta)) > 0.05:
                return False, (
                    f"mcb_delta_h expected ~{exp_delta}, got {act_delta}"
                )

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

    rules_file = os.path.join(BASE_DIR, "mcb_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "mcb_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in mcb_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: mcb_testbench.yaml (testbench mode)")
    print("- Expected Output Source: mcb_testbench.yaml (expected block)")

    mcb = MCB(copy.deepcopy(tp_input))
    tp_output = mcb.process(mode="testbench")

    structural_match, diff_msg = _compare_mcb(tp_output, expected)

    checker = MCBRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- MCB Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        print("ACTUAL next_context:")
        print(json.dumps(_next_context(tp_output), indent=2, sort_keys=True))
        print(f"mcb_complete: {tp_output.get('mcb_complete')}")
        print(f"mcb_delta_h: {(tp_output.get('semantic') or {}).get('mcb_delta_h')}")

    if rule_errors:
        print("- Rule Violations (diagnostic):")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    nc = _next_context(tp_output)
    print("\nContext Summary:")
    print(f"- topic: {nc.get('topic')}")
    print(f"- stance: {nc.get('stance')}")
    print(f"- intent: {nc.get('intent')}")
    print(f"- continuity: {nc.get('continuity')}")
    print(f"- direction: {nc.get('direction')}")
    print(f"- coherence: {nc.get('coherence')}")
    print(f"- shift_required: {nc.get('shift_required')}")
    print(f"- importance: {nc.get('importance')}")
    print(f"- mcb_complete: {tp_output.get('mcb_complete')}")
    print(f"- mcb_delta_h: {(tp_output.get('semantic') or {}).get('mcb_delta_h')}")
    print(f"- outcome: {(tp_output.get('_mcb_diagnostics') or {}).get('outcome')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: mcb_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: mcb_input.yaml (general mode)")
    print("- Checked By: mcb_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "mcb_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "mcb_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    mcb = MCB(copy.deepcopy(tp_input))
    tp_output = mcb.process(mode="general")

    checker = MCBRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_mcb_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    print("\n----- MCB next_context -----")
    print(json.dumps(_next_context(tp_output), indent=2, sort_keys=True))
    print(f"mcb_complete: {tp_output.get('mcb_complete')}")
    print(f"mcb_delta_h: {(tp_output.get('semantic') or {}).get('mcb_delta_h')}")

    return {
        "id": "general_mcb_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" MCB Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "mcb_tests_to_run.yaml")
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
    print(" MCB Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" MCB Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

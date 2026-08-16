"""
CE Testbench (Version 2.0)
  • mode == "testbench" → ce_testbench.yaml structural match (PASS/FAIL by exact equality on CE envelope)
  • mode == "general"   → ce_input.yaml + ce_rules.yaml (PASS/FAIL by rule compliance)
Aligned with progressive_lineup_testing.md v4.0 and ce_py_struc_pgm.md v2.0.
"""

from __future__ import annotations

import copy
import json
import os
import sys

import yaml

# ============================================================
# Mandatory import-path initialization (progressive_lineup 3.7)
# ============================================================
TB_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.ce_rulechecker import (  # noqa: E402
    CERuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.ce.ce import (  # noqa: E402
    CE,
    get_primitive_name,
)

assert get_primitive_name() == "ce", (
    f"Primitive name mismatch: expected ce, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def deep_compare(a, b):
    return json.dumps(a, sort_keys=True, default=str) == json.dumps(
        b, sort_keys=True, default=str
    )


def _ctx_summary(tp):
    ctx = (tp or {}).get("metadata", {}).get("context", {}) or {}
    return {
        "topic": ctx.get("topic"),
        "stance": ctx.get("stance"),
        "intent": ctx.get("intent"),
        "continuity": ctx.get("continuity"),
        "direction": ctx.get("direction"),
        "coherence": ctx.get("coherence"),
        "importance": ctx.get("importance"),
    }


def _extract_expected_context(tb_test):
    """Support both expected_output and expected keys."""
    expected_root = tb_test.get("expected_output") or tb_test.get("expected") or {}
    meta = expected_root.get("metadata") or {}
    return meta.get("context") or expected_root.get("context") or {}


def _extract_expected_candidate_set(tb_test):
    expected_root = tb_test.get("expected_output") or tb_test.get("expected") or {}
    ce = expected_root.get("ce") or {}
    return ce.get("candidate_set")


def run_single_test(test_entry):
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)

    print("\n------------------------------------------------------------")
    print(f"Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    rules_file = os.path.join(BASE_DIR, "ce_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "ce_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in ce_testbench.yaml")

    tp_input = tb_test["input"]
    expected_ctx = _extract_expected_context(tb_test)
    expected_cs = _extract_expected_candidate_set(tb_test)

    print("- Input Source: ce_testbench.yaml (testbench mode)")
    print("- Expected Output Source: ce_testbench.yaml (expected block)")

    ce = CE(copy.deepcopy(tp_input))
    tp_output = ce.inspect()

    actual_ctx = (tp_output.get("metadata") or {}).get("context") or {}
    structural_match = deep_compare(actual_ctx, expected_ctx)

    candidate_match = True
    actual_cs = ((tp_output.get("ce") or {}).get("candidate_set"))
    if expected_cs is not None:
        candidate_match = deep_compare(actual_cs, expected_cs)

    # Rulechecker is diagnostic only in testbench mode (progressive_lineup 3.1)
    checker = CERuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()

    passed = structural_match and candidate_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")
    if expected_cs is not None:
        print(f"- Candidate-Set Match: {'PASS' if candidate_match else 'FAIL'}")

    if not structural_match:
        print("\n----- Structural Diff (actual vs expected CE context) -----")
        print("ACTUAL:")
        print(json.dumps(actual_ctx, indent=2, sort_keys=True, default=str))
        print("\nEXPECTED:")
        print(json.dumps(expected_ctx, indent=2, sort_keys=True, default=str))

    if expected_cs is not None and not candidate_match:
        print("\n----- Candidate-Set Diff -----")
        print("ACTUAL:")
        print(json.dumps(actual_cs, indent=2, sort_keys=True, default=str))
        print("\nEXPECTED:")
        print(json.dumps(expected_cs, indent=2, sort_keys=True, default=str))

    if rule_errors:
        print("- Rule Violations (diagnostic):")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    summary = _ctx_summary(tp_output)
    print("\nContext Summary:")
    for k, v in summary.items():
        print(f"- {k}: {v}")

    cs = (tp_output.get("ce") or {}).get("candidate_set") or []
    print(f"- candidate_set_count: {len(cs)}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: ce_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: ce_input.yaml (general mode)")
    print("- Checked By: ce_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "ce_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "ce_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    ce = CE(copy.deepcopy(tp_input))
    tp_output = ce.inspect()

    checker = CERuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_ce_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    ctx = (tp_output.get("metadata") or {}).get("context") or {}
    print("\n----- CE context output -----")
    print(json.dumps(ctx, indent=2, sort_keys=True, default=str))

    cs = (tp_output.get("ce") or {}).get("candidate_set") or []
    print("\n----- CE candidate_set -----")
    print(json.dumps(cs, indent=2, sort_keys=True, default=str))

    summary = _ctx_summary(tp_output)
    print("\nContext Summary:")
    for k, v in summary.items():
        print(f"- {k}: {v}")

    return {
        "id": "general_ce_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" CE Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "ce_tests_to_run.yaml")
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
    print(" CE Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" CE Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

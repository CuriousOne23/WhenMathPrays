"""
SOB Testbench (Version 1.1)
Correct behavior:
    • mode == "testbench" → load sob_testbench.yaml (input + expected)
    • mode == "general"   → load sob_input.yaml + rulecheck only
    • PASS/FAIL by exact equality (testbench) or rule compliance (general)
    • On structural FAIL, dump actual vs expected for diagnosis
"""

import os
import sys
import yaml
import json
import copy

# Mandatory import-path initialization (progressive_lineup_testing.md §3.7)
TB_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.sob_rulechecker import SOBRuleChecker
from thought_simulator.requirements_20.system_playground.primitives.sob.sob import SOB, get_primitive_name

# Naming consistency check
assert get_primitive_name() == "sob", (
    f"Primitive name mismatch: expected sob, got {get_primitive_name()}"
)

# ============================================================
# Global config injected by run.py
# ============================================================
TESTBENCH_CONFIG = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def deep_compare(a, b):
    return json.dumps(a, sort_keys=True, default=str) == json.dumps(b, sort_keys=True, default=str)


def _normalize_for_compare(obj):
    """Recursively drop implementation-defined hash fields marked 'present'."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k.endswith("_hash") and v == "present":
                continue
            out[k] = _normalize_for_compare(v)
        return out
    if isinstance(obj, list):
        return [_normalize_for_compare(x) for x in obj]
    return obj


def _ctx_summary(tp):
    ctx = (tp or {}).get("metadata", {}).get("context", {}).get("context_fields", {})
    if not ctx:
        ctx = (tp or {}).get("metadata", {}).get("context", {})
    return {
        "topic": ctx.get("topic"),
        "stance": ctx.get("stance"),
        "intent": ctx.get("intent"),
        "continuity": ctx.get("continuity"),
        "direction": ctx.get("direction"),
        "coherence": ctx.get("coherence"),
        "importance": ctx.get("importance"),
    }


def run_single_test(test_entry, mode="testbench"):
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)

    print("\n------------------------------------------------------------")
    print(f"Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    rules_file = os.path.join(BASE_DIR, "sob_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    rule_errors = []
    tp_output = {}

    if mode == "testbench":
        testbench_file = os.path.join(BASE_DIR, "sob_testbench.yaml")
        tb = load_yaml(testbench_file)
        tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
        if tb_test is None:
            raise KeyError(f"Test ID {test_id} not found in sob_testbench.yaml")

        tp_input = tb_test["input"]
        expected = tb_test.get("expected") or tb_test.get("expected_output") or {}

        print(f"- Input Source: sob_testbench.yaml (testbench mode)")
        print(f"- Expected Output Source: sob_testbench.yaml (expected block)")

        sob = SOB(copy.deepcopy(tp_input))
        tp_output = sob.process()

        actual_struct = _normalize_for_compare(tp_output.get("structural") or {})
        expected_struct = _normalize_for_compare(expected.get("structural") or {})

        structural_match = deep_compare(actual_struct, expected_struct)

        # Upstream read-only check when expected supplies context
        if "metadata" in expected and "context" in expected["metadata"]:
            ctx_in = (tp_input.get("metadata") or {}).get("context", {}).get("context_fields")
            ctx_out = (tp_output.get("metadata") or {}).get("context", {}).get("context_fields")
            if ctx_in is not None and ctx_out is not None and ctx_in != ctx_out:
                structural_match = False

        checker = SOBRuleChecker(tp_input, tp_output, rules)
        rule_errors = checker.run()

        # Testbench mode: PASS/FAIL by structural equality only
        passed = structural_match

        print("\n----- Test Result -----")
        print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
        print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

        if not structural_match:
            print("\n----- Structural Diff (actual vs expected) -----")
            print("ACTUAL structural:")
            print(json.dumps(actual_struct, indent=2, sort_keys=True, default=str))
            print("\nEXPECTED structural:")
            print(json.dumps(expected_struct, indent=2, sort_keys=True, default=str))
            # Also show audit for diagnosis
            audit = (tp_output.get("metadata") or {}).get("sob_audit_record")
            if audit:
                print("\nACTUAL sob_audit_record:")
                print(json.dumps(audit, indent=2, sort_keys=True, default=str))

        if rule_errors:
            print("- Rule Violations (diagnostic):")
            for rid, msg in rule_errors:
                print(f"  * [{rid}] {msg}")
        else:
            print("- Rule Violations: None")

    else:  # general mode
        input_file = os.path.join(BASE_DIR, "sob_input.yaml")
        tp_input = load_yaml(input_file)
        for k in ("mode", "primitive", "version", "notes"):
            tp_input.pop(k, None)

        print(f"- Input Source: sob_input.yaml (general mode)")
        print(f"- Checked By: sob_rules.yaml (rule-driven validation)")

        sob = SOB(copy.deepcopy(tp_input))
        tp_output = sob.process()

        checker = SOBRuleChecker(tp_input, tp_output, rules)
        rule_errors = checker.run()
        passed = len(rule_errors) == 0

        print("\n----- Test Result -----")
        print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
        if rule_errors:
            print("- Rule Violations:")
            for rid, msg in rule_errors:
                print(f"  * [{rid}] {msg}")
        else:
            print("- Rule Violations: None")

    summary = _ctx_summary(tp_output)
    print("\nContext Summary:")
    for k, v in summary.items():
        print(f"- {k}: {v}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" SOB Testbench Runner - Starting Execution")
    print("============================================================")

    mode = (TESTBENCH_CONFIG or {}).get("mode", "testbench")
    print(f"- Mode: {mode}")

    tests_to_run_file = os.path.join(BASE_DIR, "sob_tests_to_run.yaml")
    tests_to_run = load_yaml(tests_to_run_file)
    tests = tests_to_run.get("tests", [])

    results = []
    total = passed = failed = 0

    for test in tests:
        result = run_single_test(test, mode=mode)
        if not test.get("enabled", False):
            continue
        total += 1
        if result["passed"]:
            passed += 1
        else:
            failed += 1
        results.append(result)

    print("\n============================================================")
    print(" SOB Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" SOB Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

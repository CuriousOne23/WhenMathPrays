"""
WrdNm Testbench (Version 1.0)
Correct behavior:
    • mode == "testbench" → load wrdnm_testbench.yaml (input + expected) per tests_to_run
    • mode == "general"   → load wrdnm_input.yaml once + rulecheck only
    • PASS/FAIL by exact equality on TP.wrdnm numeric fields (testbench)
      or rule compliance (general)
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

from thought_simulator.requirements_20.system_playground.testbenches.path_a.encoder.wrdnm_rulechecker import (
    WrdNmRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.wrdnm.wrdnm import (
    WrdNm,
    get_primitive_name,
)

assert get_primitive_name() == "wrdnm", (
    f"Primitive name mismatch: expected wrdnm, got {get_primitive_name()}"
)

TESTBENCH_CONFIG = {}
BASE_DIR = os.path.dirname(__file__)

# Fields compared in testbench mode (ignore provenance/timestamp noise)
COMPARE_KEYS = [
    "surface_id", "lemma_id", "expression_id",
    "temporal_id", "causal_id", "continuity_id", "entity_id", "thread_hash",
    "adjacency", "ordering_id", "structural_importance",
    "constraint_family_id", "constraint_importance", "missing_slot",
    "modality", "affect", "underspec", "semantic_adjacent_importance",
    "routing_id", "transform_id",
    "identity_id", "next_context_id",
]


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _strip_record(rec):
    """Keep only comparable numeric keys."""
    if not isinstance(rec, dict):
        return {}
    out = {}
    for k in COMPARE_KEYS:
        if k in rec:
            out[k] = rec[k]
    # preserve extra stable keys used in append-only prior record
    for k in ("note",):
        if k in rec:
            out[k] = rec[k]
    return out


def _compare_wrdnm_lists(actual_list, expected_list):
    if not isinstance(actual_list, list) or not isinstance(expected_list, list):
        return False, "wrdnm is not a list on actual or expected"
    if len(actual_list) != len(expected_list):
        return False, f"wrdnm length mismatch: actual={len(actual_list)} expected={len(expected_list)}"
    for i, (a, e) in enumerate(zip(actual_list, expected_list)):
        sa = _strip_record(a)
        se = _strip_record(e)
        # numeric tolerance for float ids
        for k in se:
            if k not in sa:
                return False, f"record[{i}] missing key {k}"
            av, ev = sa[k], se[k]
            if isinstance(ev, float) or isinstance(av, float):
                if abs(float(av) - float(ev)) > 1e-6:
                    return False, f"record[{i}].{k}: actual={av!r} expected={ev!r}"
            else:
                if av != ev:
                    return False, f"record[{i}].{k}: actual={av!r} expected={ev!r}"
    return True, None


def _ctx_summary(tp):
    ctx = (tp or {}).get("metadata", {}).get("context", {}).get("context_fields", {})
    if not ctx:
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


def run_single_test(test_entry):
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)

    print("\n------------------------------------------------------------")
    print(f"Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    rules_file = os.path.join(BASE_DIR, "wrdnm_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "wrdnm_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in wrdnm_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: wrdnm_testbench.yaml (testbench mode)")
    print("- Expected Output Source: wrdnm_testbench.yaml (expected block)")

    wrdnm = WrdNm(copy.deepcopy(tp_input))
    tp_output = wrdnm.process()

    actual_list = tp_output.get("wrdnm") or []
    expected_list = expected.get("wrdnm") or []
    structural_match, diff_msg = _compare_wrdnm_lists(actual_list, expected_list)

    checker = WrdNmRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- WrdNm Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        print("ACTUAL wrdnm:")
        print(json.dumps([_strip_record(r) for r in actual_list], indent=2, sort_keys=True))
        print("EXPECTED wrdnm:")
        print(json.dumps([_strip_record(r) for r in expected_list], indent=2, sort_keys=True))

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

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: wrdnm_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: wrdnm_input.yaml (general mode)")
    print("- Checked By: wrdnm_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "wrdnm_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "wrdnm_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    wrdnm = WrdNm(copy.deepcopy(tp_input))
    tp_output = wrdnm.process()

    checker = WrdNmRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_wrdnm_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    wrdnm_list = tp_output.get("wrdnm") or []
    print("\n----- WrdNm output -----")
    print(json.dumps([_strip_record(r) for r in wrdnm_list], indent=2, sort_keys=True))
    audit = (tp_output.get("metadata") or {}).get("wrdnm_audit_record")
    if audit:
        print("\n----- wrdnm_audit_record -----")
        # drop volatile timestamp for readability
        audit_view = {k: v for k, v in audit.items() if k != "timestamp"}
        print(json.dumps(audit_view, indent=2, sort_keys=True, default=str))

    summary = _ctx_summary(tp_output)
    print("\nContext Summary:")
    for k, v in summary.items():
        print(f"- {k}: {v}")

    return {
        "id": "general_wrdnm_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" WRDNM Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "wrdnm_tests_to_run.yaml")
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
    print(" WRDNM Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" WRDNM Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

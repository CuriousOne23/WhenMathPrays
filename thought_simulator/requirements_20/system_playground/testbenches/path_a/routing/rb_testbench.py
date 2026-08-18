"""
RB Testbench (Version 1.1)
  • mode == "testbench" → rb_testbench.yaml structural match
  • mode == "general"   → rb_input.yaml + rb_rules.yaml
Aligned with progressive_lineup_testing.md v4.2, 20.50 v3.0, rb_py_struc_pgm.md.
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

from thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.rb_rulechecker import (  # noqa: E402
    RBRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.rb.rb import (  # noqa: E402
    RB,
    get_primitive_name,
)

assert get_primitive_name() == "rb", (
    f"Primitive name mismatch: expected rb, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _ctx_summary(tp):
    ctx = ((tp or {}).get("metadata") or {}).get("context") or {}
    return {
        "topic": ctx.get("topic"),
        "stance": ctx.get("stance"),
        "intent": ctx.get("intent"),
        "continuity": ctx.get("continuity"),
        "direction": ctx.get("direction"),
        "coherence": ctx.get("coherence"),
        "importance": ctx.get("importance"),
    }


def _rf(tp):
    process = (tp or {}).get("process") or {}
    if not isinstance(process, dict):
        return {}
    rf = process.get("routing_filter") or {}
    return rf if isinstance(rf, dict) else {}


def _compare_rb(actual_tp, expected, tp_input, replay_rf=None):
    rf = _rf(actual_tp)

    if "selected_ob_ids" in expected:
        got = rf.get("selected_ob_ids") or []
        exp = expected["selected_ob_ids"] or []
        if list(got) != list(exp):
            return False, f"selected_ob_ids: expected {exp!r}, got {got!r}"

    if "max_len" in expected:
        got = rf.get("selected_ob_ids") or []
        if len(got) > int(expected["max_len"]):
            return False, f"selected_ob_ids length {len(got)} exceeds max_len {expected['max_len']}"

    rationales = rf.get("transition_rationale") or []
    if "tr_gate_rationale_contains" in expected:
        tok = expected["tr_gate_rationale_contains"]
        if tok not in rationales:
            return False, f"missing rationale token {tok!r} in {rationales!r}"

    if "rationale_contains" in expected:
        tok = expected["rationale_contains"]
        if tok not in rationales:
            return False, f"missing rationale token {tok!r} in {rationales!r}"

    for key in ("adjacency_class", "displacement_scale", "regime_hint",
                "merge_eligibility", "split_directive"):
        if key in expected:
            if rf.get(key) != expected[key]:
                return False, f"{key}: expected {expected[key]!r}, got {rf.get(key)!r}"

    if "regime_hint_in" in expected:
        allowed = expected["regime_hint_in"] or []
        if rf.get("regime_hint") not in allowed:
            return False, f"regime_hint {rf.get('regime_hint')!r} not in {allowed!r}"

    if expected.get("check_tr_unchanged"):
        if tp_input.get("TR") != actual_tp.get("TR"):
            return False, "TR was modified by RB"
        if tp_input.get("tr_needs_update") != actual_tp.get("tr_needs_update"):
            return False, "tr_needs_update was modified by RB"

    if expected.get("check_write_boundary"):
        if tp_input.get("semantic") != actual_tp.get("semantic"):
            return False, "semantic was modified by RB"
        in_meta = tp_input.get("metadata") or {}
        out_meta = actual_tp.get("metadata") or {}
        if isinstance(in_meta, dict) and isinstance(out_meta, dict):
            if "residue" in in_meta and in_meta.get("residue") != out_meta.get("residue"):
                return False, "metadata.residue was modified by RB"
            if "geometric_state" in in_meta and in_meta.get("geometric_state") != out_meta.get("geometric_state"):
                return False, "metadata.geometric_state was modified by RB"

    if expected.get("check_idob_view_unchanged"):
        in_sem = tp_input.get("semantic") or {}
        out_sem = actual_tp.get("semantic") or {}
        if in_sem != out_sem:
            return False, "IdOB/semantic view was modified by RB"

    if expected.get("check_replay"):
        if replay_rf is None:
            return False, "replay comparison missing second routing_filter"
        if replay_rf != rf:
            return False, "replay routing_filter mismatch"

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

    rules_file = os.path.join(BASE_DIR, "rb_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "rb_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in rb_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: rb_testbench.yaml (testbench mode)")
    print("- Expected Output Source: rb_testbench.yaml (expected block)")

    rb = RB(copy.deepcopy(tp_input))
    tp_output = rb.process()

    replay_rf = None
    if expected.get("check_replay"):
        replay_rf = _rf(RB(copy.deepcopy(tp_input)).process())

    structural_match, diff_msg = _compare_rb(tp_output, expected, tp_input, replay_rf=replay_rf)

    checker = RBRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- RB Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        print("ACTUAL routing_filter:")
        print(json.dumps(_rf(tp_output), indent=2, sort_keys=True))

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
    rf = _rf(tp_output)
    print(f"- adjacency_class: {rf.get('adjacency_class')}")
    print(f"- displacement_scale: {rf.get('displacement_scale')}")
    print(f"- regime_hint: {rf.get('regime_hint')}")
    print(f"- selected_ob_ids: {rf.get('selected_ob_ids')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: rb_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: rb_input.yaml (general mode)")
    print("- Checked By: rb_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "rb_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "rb_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    rb = RB(copy.deepcopy(tp_input))
    tp_output = rb.process()

    checker = RBRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_rb_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    print("\n----- routing_filter -----")
    print(json.dumps(_rf(tp_output), indent=2, sort_keys=True))

    summary = _ctx_summary(tp_output)
    print("\nContext Summary:")
    for k, v in summary.items():
        print(f"- {k}: {v}")

    return {
        "id": "general_rb_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" RB Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "rb_tests_to_run.yaml")
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
    print(" RB Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" RB Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

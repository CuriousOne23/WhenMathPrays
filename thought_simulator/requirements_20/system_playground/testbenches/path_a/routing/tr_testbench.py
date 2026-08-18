"""
TR Testbench (Version 1.0)
  • mode == "testbench" → tr_testbench.yaml structural match
  • mode == "general"   → tr_input.yaml + tr_rules.yaml
Aligned with progressive_lineup_testing.md v4.2,
20.37 v3.0, tr_py_struc_pgm.md.
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

from thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.tr_rulechecker import (  # noqa: E402
    TRRuleChecker,
    ROUTING_FIELDS_KEYS,
)
from thought_simulator.requirements_20.system_playground.primitives.tr.tr import (  # noqa: E402
    TR,
    get_primitive_name,
)

assert get_primitive_name() == "tr", (
    f"Primitive name mismatch: expected tr, got {get_primitive_name()}"
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


def _tr_block(tp):
    return (tp or {}).get("TR") or {}


def _routing_fields(tp):
    return _tr_block(tp).get("routing_fields") or {}


def _compare_tr(actual_tp, expected, tp_input):
    """Structural foundation comparison for TR."""

    if "tr_needs_update" in expected:
        if actual_tp.get("tr_needs_update") != expected["tr_needs_update"]:
            return False, (
                f"tr_needs_update expected {expected['tr_needs_update']!r}, "
                f"got {actual_tp.get('tr_needs_update')!r}"
            )

    if expected.get("TR_present"):
        if not isinstance(actual_tp.get("TR"), dict):
            return False, "TR_present expected but TP.TR missing"

    if expected.get("TR_unchanged"):
        if tp_input.get("TR") != actual_tp.get("TR"):
            return False, "TR was modified on no-op path"

    exp_tr = expected.get("TR") or {}
    act_tr = _tr_block(actual_tp)

    for k, v in exp_tr.items():
        if k == "routing_fields":
            continue
        if act_tr.get(k) != v:
            return False, f"TR.{k}: expected {v!r}, got {act_tr.get(k)!r}"

    exp_rf = exp_tr.get("routing_fields") or {}
    act_rf = act_tr.get("routing_fields") or {}
    for k, v in exp_rf.items():
        if act_rf.get(k) != v:
            return False, f"TR.routing_fields.{k}: expected {v!r}, got {act_rf.get(k)!r}"

    if expected.get("check_routing_fields_complete"):
        if not isinstance(act_rf, dict):
            return False, "routing_fields must be a dict"
        for k in ROUTING_FIELDS_KEYS:
            if k not in act_rf:
                return False, f"routing_fields missing key {k}"

    if "lineage_additions_max_len" in expected:
        la = act_tr.get("lineage_additions") or []
        if not isinstance(la, list):
            return False, "lineage_additions must be a list"
        if len(la) > int(expected["lineage_additions_max_len"]):
            return False, (
                f"lineage_additions length {len(la)} exceeds "
                f"{expected['lineage_additions_max_len']}"
            )

    if expected.get("check_write_boundary") or expected.get("check_idob_view_unchanged"):
        if tp_input.get("semantic") != actual_tp.get("semantic"):
            return False, "semantic was modified by TR"

    if expected.get("check_dcb_unchanged"):
        in_meta = tp_input.get("metadata") if isinstance(tp_input.get("metadata"), dict) else {}
        out_meta = actual_tp.get("metadata") if isinstance(actual_tp.get("metadata"), dict) else {}
        for key in ("geometric_state", "geometric_history"):
            if key in in_meta and in_meta.get(key) != out_meta.get(key):
                return False, f"metadata.{key} was modified by TR"

    if expected.get("check_rb_filter_unchanged"):
        in_proc = tp_input.get("process") if isinstance(tp_input.get("process"), dict) else {}
        out_proc = actual_tp.get("process") if isinstance(actual_tp.get("process"), dict) else {}
        if "routing_filter" in in_proc:
            if in_proc.get("routing_filter") != out_proc.get("routing_filter"):
                return False, "process.routing_filter was modified by TR"

    if expected.get("check_write_boundary"):
        in_meta = tp_input.get("metadata") if isinstance(tp_input.get("metadata"), dict) else {}
        out_meta = actual_tp.get("metadata") if isinstance(actual_tp.get("metadata"), dict) else {}
        if "residue" in in_meta and in_meta.get("residue") != out_meta.get("residue"):
            return False, "metadata.residue was modified by TR"

    if expected.get("check_replay"):
        # Second independent run must match first TR block
        second = TR(copy.deepcopy(tp_input)).process()
        if second.get("TR") != actual_tp.get("TR"):
            return False, "replay produced different TR block"
        if second.get("tr_needs_update") != actual_tp.get("tr_needs_update"):
            return False, "replay produced different tr_needs_update"

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

    rules_file = os.path.join(BASE_DIR, "tr_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "tr_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in tr_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: tr_testbench.yaml (testbench mode)")
    print("- Expected Output Source: tr_testbench.yaml (expected block)")

    tr = TR(copy.deepcopy(tp_input))
    tp_output = tr.process()

    structural_match, diff_msg = _compare_tr(tp_output, expected, tp_input)

    checker = TRRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- TR Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        print("ACTUAL TR fields:")
        print(
            json.dumps(
                {
                    "tr_needs_update": tp_output.get("tr_needs_update"),
                    "TR": _tr_block(tp_output),
                },
                indent=2,
                sort_keys=True,
            )
        )

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
    act = _tr_block(tp_output)
    print(f"- TR.stance: {act.get('stance')}")
    print(f"- TR.intent: {act.get('intent')}")
    print(f"- TR.tension: {act.get('tension')}")
    print(f"- TR.epistemic_delta_h: {act.get('epistemic_delta_h')}")
    print(f"- TR.lineage_additions_len: {len(act.get('lineage_additions') or [])}")
    rf = act.get("routing_fields") or {}
    print(f"- routing_severity: {rf.get('routing_severity')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: tr_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: tr_input.yaml (general mode)")
    print("- Checked By: tr_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "tr_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "tr_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    tr = TR(copy.deepcopy(tp_input))
    tp_output = tr.process()

    checker = TRRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_tr_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    print("\n----- TR fields -----")
    print(
        json.dumps(
            {
                "tr_needs_update": tp_output.get("tr_needs_update"),
                "TR": _tr_block(tp_output),
            },
            indent=2,
            sort_keys=True,
        )
    )

    summary = _ctx_summary(tp_output)
    print("\nContext Summary:")
    for k, v in summary.items():
        print(f"- {k}: {v}")

    return {
        "id": "general_tr_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" TR Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "tr_tests_to_run.yaml")
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
    print(" TR Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" TR Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

"""
DCB Testbench (Version 1.0)
  • mode == "testbench" → dcb_testbench.yaml structural match
  • mode == "general"   → dcb_input.yaml + dcb_rules.yaml
Aligned with progressive_lineup_testing.md v4.1,
20.106 v5.3, dcb_py_struc_pgm.md.
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

from thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.dcb_rulechecker import (  # noqa: E402
    DCBRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.dcb.dcb import (  # noqa: E402
    DCB,
    get_primitive_name,
)

assert get_primitive_name() == "dcb", (
    f"Primitive name mismatch: expected dcb, got {get_primitive_name()}"
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


def _meta(tp):
    return (tp or {}).get("metadata") or {}


def _state(tp):
    return _meta(tp).get("geometric_state") or {}


def _last_event(tp):
    events = _meta(tp).get("dcb_events") or []
    if isinstance(events, list) and events:
        return events[-1]
    return {}


def _compare_dcb(actual_tp, expected, tp_input):
    """Structural foundation comparison."""
    state = _state(actual_tp)
    exp_state = expected.get("geometric_state") or {}

    for k, v in exp_state.items():
        if state.get(k) != v:
            return False, f"geometric_state.{k}: expected {v!r}, got {state.get(k)!r}"

    if "history_len" in expected:
        hist = _meta(actual_tp).get("geometric_history") or []
        if len(hist) != expected["history_len"]:
            return False, f"history_len expected {expected['history_len']}, got {len(hist)}"

    if "event_type" in expected:
        ev = _last_event(actual_tp)
        if ev.get("event_type") != expected["event_type"]:
            return False, f"event_type expected {expected['event_type']!r}, got {ev.get('event_type')!r}"
        if expected["event_type"] == "cycle_start" and ev.get("prev_position") is not None:
            return False, "cycle_start prev_position must be null"

    if "provenance_dcb_last_update" in expected:
        prov = _meta(actual_tp).get("provenance") or {}
        if prov.get("dcb_last_update") != expected["provenance_dcb_last_update"]:
            return False, (
                f"dcb_last_update expected {expected['provenance_dcb_last_update']!r}, "
                f"got {prov.get('dcb_last_update')!r}"
            )

    if expected.get("check_write_boundary"):
        if tp_input.get("semantic") != actual_tp.get("semantic"):
            return False, "semantic was modified by DCB"
        in_res = (_meta(tp_input).get("residue"))
        out_res = (_meta(actual_tp).get("residue"))
        if in_res is not None and in_res != out_res:
            return False, "metadata.residue was modified by DCB"
        for key in ("ssg_status", "ssg_reason_code"):
            if key in tp_input and tp_input.get(key) != actual_tp.get(key):
                return False, f"{key} was modified by DCB"

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

    rules_file = os.path.join(BASE_DIR, "dcb_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "dcb_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in dcb_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: dcb_testbench.yaml (testbench mode)")
    print("- Expected Output Source: dcb_testbench.yaml (expected block)")

    dcb = DCB(copy.deepcopy(tp_input))
    tp_output = dcb.process()

    structural_match, diff_msg = _compare_dcb(tp_output, expected, tp_input)

    checker = DCBRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- DCB Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        print("ACTUAL DCB fields:")
        print(
            json.dumps(
                {
                    "geometric_state": _state(tp_output),
                    "history_len": len(_meta(tp_output).get("geometric_history") or []),
                    "last_event": _last_event(tp_output),
                    "provenance": _meta(tp_output).get("provenance"),
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
    st = _state(tp_output)
    print(f"- position: {st.get('position')}")
    print(f"- direction: {st.get('direction')}")
    print(f"- curvature: {st.get('curvature')}")
    print(f"- step_index: {st.get('step_index')}")
    print(f"- lane_id: {st.get('lane_id')}")
    print(f"- event_type: {_last_event(tp_output).get('event_type')}")
    print(f"- history_len: {len(_meta(tp_output).get('geometric_history') or [])}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: dcb_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: dcb_input.yaml (general mode)")
    print("- Checked By: dcb_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "dcb_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "dcb_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    dcb = DCB(copy.deepcopy(tp_input))
    tp_output = dcb.process()

    checker = DCBRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_dcb_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    print("\n----- DCB fields -----")
    print(
        json.dumps(
            {
                "geometric_state": _state(tp_output),
                "history_len": len(_meta(tp_output).get("geometric_history") or []),
                "last_event": _last_event(tp_output),
                "provenance": _meta(tp_output).get("provenance"),
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
        "id": "general_dcb_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" DCB Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "dcb_tests_to_run.yaml")
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
    print(" DCB Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" DCB Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

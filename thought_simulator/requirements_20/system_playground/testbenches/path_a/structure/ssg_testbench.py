"""
SSG Testbench (Version 1.0)
  • mode == "testbench" → ssg_testbench.yaml structural match
  • mode == "general"   → ssg_input.yaml + ssg_rules.yaml
Aligned with progressive_lineup_testing.md v4.0,
20.47_ssg_prim.md v3.0, ssg_py_struc_pgm.md (structural-only).
"""

from __future__ import annotations

import copy
import json
import math
import os
import sys

import yaml

# Mandatory import-path initialization (progressive_lineup 3.7)
TB_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from thought_simulator.requirements_20.system_playground.testbenches.path_a.structure.ssg_rulechecker import (  # noqa: E402
    SSGRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.ssg.ssg import (  # noqa: E402
    SSG,
    D,
    get_primitive_name,
)

assert get_primitive_name() == "ssg", (
    f"Primitive name mismatch: expected ssg, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _nearly_equal(a, b, tol=1e-6):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) <= tol
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        return all(_nearly_equal(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a.keys()) != set(b.keys()):
            return False
        return all(_nearly_equal(a[k], b[k], tol) for k in a)
    return a == b


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


def _l2_norm(sig):
    if not isinstance(sig, list) or not sig:
        return 0.0
    return math.sqrt(sum(float(v) * float(v) for v in sig))


def _compare_ssg(actual_tp, expected):
    for key in ("ssg_status", "ssg_reason_code", "ssg_layer_bitmap"):
        if key in expected:
            if actual_tp.get(key) != expected.get(key):
                return False, f"{key} actual={actual_tp.get(key)!r} expected={expected.get(key)!r}"

    if "ssg_signature" in expected:
        exp_sig = expected["ssg_signature"]
        act_sig = actual_tp.get("ssg_signature")
        if exp_sig is None:
            if act_sig is not None:
                return False, "ssg_signature should be absent"
        else:
            if not isinstance(act_sig, list):
                return False, "ssg_signature missing or not a list"
            if len(act_sig) != len(exp_sig):
                return False, f"ssg_signature length actual={len(act_sig)} expected={len(exp_sig)}"
            if all(abs(float(v)) < 1e-12 for v in exp_sig):
                if not all(abs(float(v)) < 1e-12 for v in act_sig):
                    return False, "expected zero signature"
            else:
                if abs(_l2_norm(act_sig) - 1.0) > 1e-5:
                    return False, f"signature L2 norm {_l2_norm(act_sig)} != 1"
    else:
        if expected.get("ssg_status") != "MISSING_INPUT":
            act_sig = actual_tp.get("ssg_signature")
            if not isinstance(act_sig, list) or len(act_sig) != D:
                return False, f"ssg_signature must be list of length {D}"
            norm = _l2_norm(act_sig)
            is_zero = all(abs(float(v)) < 1e-12 for v in act_sig)
            if not (is_zero or abs(norm - 1.0) < 1e-5):
                return False, f"signature L2 norm {norm} invalid"

    if expected.get("ssg_status") == "MISSING_INPUT":
        if "ssg_signature" in actual_tp and actual_tp["ssg_signature"] is not None:
            return False, "MISSING_INPUT must not write ssg_signature"

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

    rules_file = os.path.join(BASE_DIR, "ssg_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "ssg_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in ssg_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: ssg_testbench.yaml (testbench mode)")
    print("- Expected Output Source: ssg_testbench.yaml (expected block)")

    ssg = SSG(copy.deepcopy(tp_input))
    tp_output = ssg.process()

    structural_match, diff_msg = _compare_ssg(tp_output, expected)

    checker = SSGRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- SSG Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        print("ACTUAL SSG fields:")
        print(
            json.dumps(
                {
                    "ssg_status": tp_output.get("ssg_status"),
                    "ssg_reason_code": tp_output.get("ssg_reason_code"),
                    "ssg_layer_bitmap": tp_output.get("ssg_layer_bitmap"),
                    "ssg_signature_len": len(tp_output.get("ssg_signature") or []),
                    "ssg_signature_l2": _l2_norm(tp_output.get("ssg_signature") or []),
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
    print(f"- ssg_status: {tp_output.get('ssg_status')}")
    print(f"- ssg_reason_code: {tp_output.get('ssg_reason_code')}")
    print(f"- ssg_layer_bitmap: {tp_output.get('ssg_layer_bitmap')}")
    sig = tp_output.get("ssg_signature")
    print(f"- ssg_signature_len: {len(sig) if isinstance(sig, list) else None}")
    print(f"- ssg_signature_l2: {_l2_norm(sig) if isinstance(sig, list) else None}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: ssg_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: ssg_input.yaml (general mode)")
    print("- Checked By: ssg_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "ssg_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "ssg_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    ssg = SSG(copy.deepcopy(tp_input))
    tp_output = ssg.process()

    checker = SSGRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_ssg_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    print("\n----- SSG fields -----")
    print(
        json.dumps(
            {
                "ssg_status": tp_output.get("ssg_status"),
                "ssg_reason_code": tp_output.get("ssg_reason_code"),
                "ssg_layer_bitmap": tp_output.get("ssg_layer_bitmap"),
                "ssg_signature_len": len(tp_output.get("ssg_signature") or []),
                "ssg_signature_l2": _l2_norm(tp_output.get("ssg_signature") or []),
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
        "id": "general_ssg_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" SSG Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "ssg_tests_to_run.yaml")
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
    print(" SSG Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" SSG Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

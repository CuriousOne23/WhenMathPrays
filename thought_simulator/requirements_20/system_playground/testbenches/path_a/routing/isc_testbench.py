"""
ISc Testbench (Version 1.0)
  • mode == "testbench" → isc_testbench.yaml structural match
  • mode == "general"   → isc_input.yaml + isc_rules.yaml
Aligned with progressive_lineup_testing.md v4.0 and isc_py_struc_pgm.md v2.0.
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

from thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.isc_rulechecker import (  # noqa: E402
    IScRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.isc.isc import (  # noqa: E402
    ISc,
    get_primitive_name,
)

assert get_primitive_name() == "isc", (
    f"Primitive name mismatch: expected isc, got {get_primitive_name()}"
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


def _nearly_equal(a, b, tol=1e-9):
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


def _strip_record(rec):
    """Comparable subset of isc_output record (ignore nested rationale_record noise)."""
    if not isinstance(rec, dict):
        return {}
    keys = [
        "distribution",
        "entropy",
        "delta_h_percent",
        "confidence",
        "cop_triggered",
        "score_set",
        "score_conflict",
        "score_reason_code",
        "provenance",
    ]
    return {k: rec[k] for k in keys if k in rec}


def _strip_scoring_meta(meta):
    if not isinstance(meta, dict):
        return {}
    keys = [
        "score_set",
        "score_conflict",
        "score_reason_code",
        "cop_triggered",
        "entropy",
        "delta_h_percent",
    ]
    return {k: meta[k] for k in keys if k in meta}


def _compare_isc(actual_tp, expected):
    actual_hist = actual_tp.get("isc_output") or []
    expected_hist = expected.get("isc_output") or []
    if len(actual_hist) != len(expected_hist):
        return False, f"isc_output length actual={len(actual_hist)} expected={len(expected_hist)}"
    for i, (a, e) in enumerate(zip(actual_hist, expected_hist)):
        sa, se = _strip_record(a), _strip_record(e)
        if not _nearly_equal(sa, se):
            return False, f"isc_output[{i}] mismatch"

    if "isc" in expected:
        if not _nearly_equal(actual_tp.get("isc"), expected.get("isc")):
            return False, "isc mirror mismatch"

    exp_meta = (expected.get("metadata") or {}).get("scoring_metadata")
    if exp_meta is not None:
        act_meta = (actual_tp.get("metadata") or {}).get("scoring_metadata") or {}
        if not _nearly_equal(_strip_scoring_meta(act_meta), _strip_scoring_meta(exp_meta)):
            return False, "scoring_metadata mismatch"

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

    rules_file = os.path.join(BASE_DIR, "isc_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "isc_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in isc_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: isc_testbench.yaml (testbench mode)")
    print("- Expected Output Source: isc_testbench.yaml (expected block)")

    isc = ISc(copy.deepcopy(tp_input))
    tp_output = isc.process()

    structural_match, diff_msg = _compare_isc(tp_output, expected)

    checker = IScRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- ISc Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        actual_hist = tp_output.get("isc_output") or []
        print("ACTUAL isc_output (stripped):")
        print(json.dumps([_strip_record(r) for r in actual_hist], indent=2, sort_keys=True))
        print("EXPECTED isc_output (stripped):")
        print(json.dumps([_strip_record(r) for r in (expected.get("isc_output") or [])], indent=2, sort_keys=True))

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
    cs = ((tp_input.get("ce") or {}).get("candidate_set")) or []
    print(f"- candidate_set_count: {len(cs)}")
    rec = (tp_output.get("isc_output") or [None])[-1] or {}
    dist = rec.get("distribution") or []
    if dist:
        top = max(dist, key=lambda d: d.get("normalized_score", 0.0))
        print(f"- top_candidate_id: {top.get('candidate_id')}")
        print(f"- top_normalized_score: {top.get('normalized_score')}")
    print(f"- cop_triggered: {rec.get('cop_triggered')}")
    print(f"- score_reason_code: {rec.get('score_reason_code')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: isc_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: isc_input.yaml (general mode)")
    print("- Checked By: isc_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "isc_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "isc_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    isc = ISc(copy.deepcopy(tp_input))
    tp_output = isc.process()

    checker = IScRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_isc_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    hist = tp_output.get("isc_output") or []
    print("\n----- ISc isc_output -----")
    print(json.dumps([_strip_record(r) for r in hist], indent=2, sort_keys=True))

    summary = _ctx_summary(tp_output)
    print("\nContext Summary:")
    for k, v in summary.items():
        print(f"- {k}: {v}")

    return {
        "id": "general_isc_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" ISC Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "isc_tests_to_run.yaml")
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
    print(" ISC Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" ISC Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

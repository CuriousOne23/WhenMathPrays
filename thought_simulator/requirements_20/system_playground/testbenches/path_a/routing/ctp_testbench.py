"""
CTP Testbench (Version 1.0)
  • mode == "testbench" → ctp_testbench.yaml structural match
  • mode == "general"   → ctp_input.yaml + ctp_rules.yaml
Aligned with progressive_lineup_testing.md v4.2,
20.145 v3.0, ctp_py_struc_pgm.md.
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

from thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.ctp_rulechecker import (  # noqa: E402
    CTPRuleChecker,
    HISTORY_TOP_KEYS,
    INVARIANT_KEYS,
)
from thought_simulator.requirements_20.system_playground.primitives.ctp.ctp import (  # noqa: E402
    CTP,
    get_primitive_name,
)

assert get_primitive_name() == "ctp", (
    f"Primitive name mismatch: expected ctp, got {get_primitive_name()}"
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
    if not isinstance(ctx, dict):
        ctx = {}
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
    return (tp or {}).get("metadata") if isinstance((tp or {}).get("metadata"), dict) else {}


def _hist(tp):
    h = _meta(tp).get("cognitive_history")
    return h if isinstance(h, list) else []


def _last_entry(tp):
    h = _hist(tp)
    return h[-1] if h else {}


def _deep_equal(a, b):
    return a == b


def _compare_ctp(actual_tp, expected, tp_input):
    hist = _hist(actual_tp)
    last = _last_entry(actual_tp)

    if "history_len" in expected:
        if len(hist) != int(expected["history_len"]):
            return False, f"history_len expected {expected['history_len']}, got {len(hist)}"

    exp_last = expected.get("last_entry") or {}
    for k, v in exp_last.items():
        if k == "invariants":
            act_inv = last.get("invariants") or {}
            if not isinstance(act_inv, dict):
                return False, "last_entry.invariants must be a dict"
            for ik, iv in (v or {}).items():
                if act_inv.get(ik) != iv:
                    return False, (
                        f"last_entry.invariants.{ik}: expected {iv!r}, got {act_inv.get(ik)!r}"
                    )
        elif k == "idob_geometry":
            act_g = last.get("idob_geometry") or {}
            if not isinstance(act_g, dict):
                return False, "last_entry.idob_geometry must be a dict"
            for gk, gv in (v or {}).items():
                if act_g.get(gk) != gv:
                    return False, (
                        f"last_entry.idob_geometry.{gk}: expected {gv!r}, got {act_g.get(gk)!r}"
                    )
        else:
            if last.get(k) != v:
                return False, f"last_entry.{k}: expected {v!r}, got {last.get(k)!r}"

    if expected.get("check_history_schema_complete"):
        if not isinstance(last, dict):
            return False, "last history entry missing"
        for k in HISTORY_TOP_KEYS:
            if k not in last:
                return False, f"history schema missing key {k}"
        inv = last.get("invariants")
        if not isinstance(inv, dict):
            return False, "invariants must be a dict"
        for k in INVARIANT_KEYS:
            if k not in inv:
                return False, f"invariants missing key {k}"
        geom = last.get("idob_geometry")
        if not isinstance(geom, dict) or "neighborhood" not in geom or "k_id" not in geom:
            return False, "idob_geometry incomplete"

    if "provenance_ctp_last_update" in expected:
        prov = _meta(actual_tp).get("provenance") or {}
        exp_ts = expected["provenance_ctp_last_update"]
        try:
            if float(prov.get("ctp_last_update")) != float(exp_ts):
                return False, (
                    f"ctp_last_update expected {exp_ts!r}, got {prov.get('ctp_last_update')!r}"
                )
        except (TypeError, ValueError):
            return False, f"ctp_last_update expected {exp_ts!r}, got {prov.get('ctp_last_update')!r}"

    if expected.get("prior_entry_unchanged"):
        in_hist = _hist(tp_input)
        out_hist = hist
        if len(out_hist) < len(in_hist):
            return False, "history shrank"
        for i, prev in enumerate(in_hist):
            if out_hist[i] != prev:
                return False, f"prior history entry {i} changed"

    if expected.get("check_tr_unchanged"):
        if tp_input.get("TR") != actual_tp.get("TR"):
            return False, "TR was modified by CTP"
        if "tr_needs_update" in tp_input and tp_input.get("tr_needs_update") != actual_tp.get(
            "tr_needs_update"
        ):
            return False, "tr_needs_update was modified by CTP"

    if expected.get("check_idob_unchanged") or expected.get("check_write_boundary"):
        if tp_input.get("semantic") != actual_tp.get("semantic"):
            return False, "semantic was modified by CTP"

    if expected.get("check_rb_filter_unchanged") or expected.get("check_write_boundary"):
        in_proc = tp_input.get("process") if isinstance(tp_input.get("process"), dict) else {}
        out_proc = actual_tp.get("process") if isinstance(actual_tp.get("process"), dict) else {}
        if "routing_filter" in in_proc:
            if in_proc.get("routing_filter") != out_proc.get("routing_filter"):
                return False, "process.routing_filter was modified by CTP"

    if expected.get("check_dcb_unchanged") or expected.get("check_write_boundary"):
        in_meta = _meta(tp_input)
        out_meta = _meta(actual_tp)
        for key in ("geometric_state", "geometric_history"):
            if key in in_meta and in_meta.get(key) != out_meta.get(key):
                return False, f"metadata.{key} was modified by CTP"

    if expected.get("check_write_boundary"):
        in_meta = _meta(tp_input)
        out_meta = _meta(actual_tp)
        for key in ("residue", "context"):
            if key in in_meta and in_meta.get(key) != out_meta.get(key):
                return False, f"metadata.{key} was modified by CTP"

    if expected.get("check_replay"):
        second = CTP(copy.deepcopy(tp_input)).process()
        if _last_entry(second) != last:
            return False, "replay produced different last history entry"
        if len(_hist(second)) != len(hist):
            return False, "replay produced different history length"

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

    rules_file = os.path.join(BASE_DIR, "ctp_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "ctp_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in ctp_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: ctp_testbench.yaml (testbench mode)")
    print("- Expected Output Source: ctp_testbench.yaml (expected block)")

    ctp = CTP(copy.deepcopy(tp_input))
    tp_output = ctp.process()

    structural_match, diff_msg = _compare_ctp(tp_output, expected, tp_input)

    checker = CTPRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- CTP Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        print("ACTUAL CTP fields:")
        print(
            json.dumps(
                {
                    "history_len": len(_hist(tp_output)),
                    "last_entry": _last_entry(tp_output),
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
    last = _last_entry(tp_output)
    print(f"- history_len: {len(_hist(tp_output))}")
    print(f"- last cycle_id: {last.get('cycle_id')}")
    print(f"- last timestamp: {last.get('timestamp')}")
    print(f"- rb_regime_hint: {last.get('rb_regime_hint')}")
    print(f"- idob_stability: {last.get('idob_stability')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: ctp_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: ctp_input.yaml (general mode)")
    print("- Checked By: ctp_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "ctp_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "ctp_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    ctp = CTP(copy.deepcopy(tp_input))
    tp_output = ctp.process()

    checker = CTPRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_ctp_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    print("\n----- CTP fields -----")
    print(
        json.dumps(
            {
                "history_len": len(_hist(tp_output)),
                "last_entry": _last_entry(tp_output),
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
        "id": "general_ctp_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" CTP Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "ctp_tests_to_run.yaml")
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
    print(" CTP Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" CTP Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

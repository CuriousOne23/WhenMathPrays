"""
CST-Core Testbench (Version 0.1)
  • mode == "testbench" → cst_core_testbench.yaml structural / behavioral match
  • mode == "general"   → cst_core_input.yaml + cst_core_rules.yaml
Aligned with progressive_lineup_testing.md v4.2,
cst_core_py_struc_pgm.md, patha_field_names.md (TP.cst.core lock).
"""

from __future__ import annotations

import copy
import os
import sys

import yaml

# Mandatory import-path initialization
TB_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cst_core_rulechecker import (  # noqa: E402
    CSTCoreRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.cst_core.cst_core import (  # noqa: E402
    CST,
    get_primitive_name,
    process as cst_core_process,
)

assert get_primitive_name() == "cst_core", (
    f"Primitive name mismatch: expected cst_core, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _get_path(d: dict, path: list):
    cur = d
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def _core(tp: dict) -> dict:
    return ((tp or {}).get("cst") or {}).get("core") or {}


def run_single_test(test_entry):
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)

    print("\n------------------------------------------------------------")
    print(f"Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    rules_file = os.path.join(BASE_DIR, "cst_core_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "cst_core_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in cst_core_testbench.yaml")

    tp_input = copy.deepcopy(tb_test["input"])
    expected = tb_test.get("expected") or {}

    print("- Input Source: cst_core_testbench.yaml (testbench mode)")
    print("- Expected Output Source: cst_core_testbench.yaml (expected block)")

    diffs = []

    # ------------------------------------------------------------------
    # Special: multi-turn history window
    # ------------------------------------------------------------------
    if test_id == "cst_core_history_window_cap":
        cst = CST()
        tp = copy.deepcopy(tp_input)
        multi = int(tp.pop("multi_turn", 15))
        final = None
        for t in range(1, multi + 1):
            tp["turn_index"] = t
            # Carry history on TP for continuity across turns
            final = cst.process(copy.deepcopy(tp), mode="testbench")
            # Feed history back
            prior = _core(final)
            tp.setdefault("cst", {})["core"] = {
                "status": prior.get("status") or {},
                "history": prior.get("history") or {"window_len": 10, "turns": []},
                "metrics": prior.get("metrics") or {},
            }
        hist = (_core(final).get("history") or {})
        turns = hist.get("turns") or []
        if len(turns) > expected.get("history_len_le", 10):
            diffs.append(f"history turns {len(turns)} > {expected.get('history_len_le', 10)}")
        if turns and turns[-1].get("turn_index") != expected.get("last_turn_index", multi):
            diffs.append(
                f"last turn_index expected {expected.get('last_turn_index')}, got {turns[-1].get('turn_index')}"
            )
        tp_output = final
        tp_before = copy.deepcopy(tp_input)

    # ------------------------------------------------------------------
    # Special: deterministic replay
    # ------------------------------------------------------------------
    elif test_id == "cst_core_deterministic_replay":
        tp_before = copy.deepcopy(tp_input)
        out1 = cst_core_process(copy.deepcopy(tp_input), mode="testbench")
        out2 = cst_core_process(copy.deepcopy(tp_input), mode="testbench")
        s1 = _core(out1).get("signals")
        s2 = _core(out2).get("signals")
        m1 = _core(out1).get("metrics")
        m2 = _core(out2).get("metrics")
        if s1 != s2:
            diffs.append("signals diverge between independent process calls")
        if m1 != m2:
            diffs.append("metrics diverge between independent process calls")
        tp_output = out1

    # ------------------------------------------------------------------
    # Default process path
    # ------------------------------------------------------------------
    else:
        tp_before = copy.deepcopy(tp_input)
        # Strip test-only keys
        for k in ("multi_turn",):
            tp_input.pop(k, None)
        tp_output = cst_core_process(copy.deepcopy(tp_input), mode="testbench")

        core = _core(tp_output)

        # Envelope presence
        if not core:
            diffs.append("TP.cst.core missing")

        exp_core = _get_path(expected, ["cst", "core"]) or {}

        # status checks
        exp_status = exp_core.get("status") or {}
        act_status = core.get("status") or {}
        for k, v in exp_status.items():
            if act_status.get(k) != v:
                diffs.append(f"status.{k}: expected {v}, got {act_status.get(k)}")

        # audit
        exp_audit = exp_core.get("audit") or {}
        act_audit = core.get("audit") or {}
        for k, v in exp_audit.items():
            if act_audit.get(k) != v:
                diffs.append(f"audit.{k}: expected {v}, got {act_audit.get(k)}")

        # signals presence + specific expectations
        exp_signals = exp_core.get("signals") or {}
        act_signals = core.get("signals") or {}
        for key in exp_signals.keys():
            if key not in act_signals:
                diffs.append(f"signals.{key} missing")

        for key, exp_val in exp_signals.items():
            if not isinstance(exp_val, dict):
                continue
            act_val = act_signals.get(key) or {}
            for sk, sv in exp_val.items():
                if sk == "not_in_collapsed":
                    collapsed = (act_signals.get("collapse") or {}).get("collapsed_objects") or []
                    for pid in sv:
                        if pid in collapsed:
                            diffs.append(f"parent {pid} incorrectly in collapsed_objects")
                elif sk in act_val:
                    if act_val.get(sk) != sv:
                        diffs.append(f"signals.{key}.{sk}: expected {sv}, got {act_val.get(sk)}")
                elif sk in ("frozen_objects", "thawed_objects", "restored_objects",
                            "affected_objects", "collapsed_objects", "increased", "decreased"):
                    if act_val.get(sk) != sv:
                        diffs.append(f"signals.{key}.{sk}: expected {sv}, got {act_val.get(sk)}")

        # cob snapshot unchanged
        if expected.get("cob_snapshot_unchanged"):
            before = ((tp_before.get("identity") or {}).get("cob_state_snapshot"))
            after = ((tp_output.get("identity") or {}).get("cob_state_snapshot"))
            if before != after:
                diffs.append("cob_state_snapshot mutated")

        # routing path
        rp = tp_output.get("routing_path") or []
        if "cst_core" not in rp:
            diffs.append("routing_path missing 'cst_core'")

    checker = CSTCoreRuleChecker(tp_before, tp_output, rules)
    rule_errors = checker.run()

    passed = len(diffs) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if passed else 'FAIL'}")
    if diffs:
        print("- Diffs:")
        for m in diffs:
            print(f"  * {m}")
    if rule_errors:
        print("- Rule Violations (diagnostic):")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    core = _core(tp_output)
    signals = core.get("signals") or {}
    print("\nCST-Core Summary:")
    print(f"- turn_index: {(core.get('status') or {}).get('turn_index')}")
    print(f"- layer_count: {(core.get('status') or {}).get('layer_count')}")
    print(f"- freeze: {(signals.get('freeze') or {}).get('frozen_objects')}")
    print(f"- thaw: {(signals.get('thaw') or {}).get('thawed_objects')}")
    print(f"- drift.affected: {(signals.get('drift') or {}).get('affected_objects')}")
    print(f"- collapse.collapsed: {(signals.get('collapse') or {}).get('collapsed_objects')}")
    print(f"- history.turns: {len((core.get('history') or {}).get('turns') or [])}")
    print(f"- routing_path: {tp_output.get('routing_path')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: cst_core_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: cst_core_input.yaml (general mode)")
    print("- Checked By: cst_core_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "cst_core_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "cst_core_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    tp_before = copy.deepcopy(tp_input)
    tp_output = cst_core_process(copy.deepcopy(tp_input), mode="general")

    checker = CSTCoreRuleChecker(tp_before, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_cst_core_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    core = _core(tp_output)
    signals = core.get("signals") or {}
    print("\nCST-Core Summary:")
    print(f"- freeze: {(signals.get('freeze') or {}).get('frozen_objects')}")
    print(f"- drift.affected: {(signals.get('drift') or {}).get('affected_objects')}")
    print(f"- routing_path: {tp_output.get('routing_path')}")

    return {
        "id": "general_cst_core_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" CST-Core Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "cst_core_tests_to_run.yaml")
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
    print(" CST-Core Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" CST-Core Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

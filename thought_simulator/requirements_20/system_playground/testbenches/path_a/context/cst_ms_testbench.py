"""
CST-MS Testbench (Version 0.1)
  • mode == "testbench" → cst_ms_testbench.yaml structural / behavioral match
  • mode == "general"   → cst_ms_input.yaml + cst_ms_rules.yaml
Aligned with progressive_lineup_testing.md,
cst_ms_py_struc_pgm.md, patha_field_names.md (TP.cst.ms lock).
"""

from __future__ import annotations

import copy
import os
import sys

import yaml

TB_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cst_ms_rulechecker import (  # noqa: E402
    CSTMSRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.cst_ms.cst_ms import (  # noqa: E402
    CST_MS,
    get_primitive_name,
    process as cst_ms_process,
)

assert get_primitive_name() == "cst_ms", (
    f"Primitive name mismatch: expected cst_ms, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)

REQUIRED_COMMAND_KEYS = (
    "freeze",
    "thaw",
    "collapse_recovery",
    "create_identity_layer",
    "split",
    "merge",
)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _ms(tp: dict) -> dict:
    return ((tp or {}).get("cst") or {}).get("ms") or {}


def _normalize_mode(raw) -> str:
    mode = str(raw or "testbench").strip().lower()
    if mode not in ("testbench", "general"):
        print(f"WARNING: unrecognized mode '{raw}' — defaulting to testbench")
        return "testbench"
    return mode


def run_single_test(test_entry):
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)

    print("\n------------------------------------------------------------")
    print(f"[MODE=testbench] Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    rules_file = os.path.join(BASE_DIR, "cst_ms_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "cst_ms_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in cst_ms_testbench.yaml")

    tp_input = copy.deepcopy(tb_test["input"])
    expected = tb_test.get("expected") or {}

    print("- Active MODE: testbench")
    print("- Input Source: cst_ms_testbench.yaml")
    print("- Expected Source: cst_ms_testbench.yaml (expected block)")
    print("- Rulechecker: diagnostic only (PASS/FAIL driven by expected block)")

    diffs = []

    if test_id == "cst_ms_window_cap":
        ms = CST_MS()
        tp = copy.deepcopy(tp_input)
        multi = int(tp.pop("multi_turn", 15))
        final = None
        for t in range(1, multi + 1):
            tp["turn_index"] = t
            core = ((tp.get("cst") or {}).get("core") or {})
            status = core.setdefault("status", {})
            status["turn_index"] = t
            final = ms.process(copy.deepcopy(tp), mode="testbench")
            prior = _ms(final)
            tp.setdefault("cst", {})["ms"] = {
                "stability_window": prior.get("stability_window") or [],
                "command_log": prior.get("command_log") or [],
            }
        window = (_ms(final).get("stability_window") or [])
        if len(window) > expected.get("window_len_le", 10):
            diffs.append(f"window length {len(window)} > {expected.get('window_len_le', 10)}")
        if window and window[-1].get("turn_index") != expected.get("last_turn_index", multi):
            diffs.append(
                f"last turn_index expected {expected.get('last_turn_index')}, got {window[-1].get('turn_index')}"
            )
        tp_output = final
        tp_before = copy.deepcopy(tp_input)

    elif test_id == "cst_ms_deterministic_replay":
        tp_before = copy.deepcopy(tp_input)
        out1 = cst_ms_process(copy.deepcopy(tp_input), mode="testbench")
        out2 = cst_ms_process(copy.deepcopy(tp_input), mode="testbench")
        m1 = _ms(out1)
        m2 = _ms(out2)
        for key in (
            "normalized_metrics",
            "weighted_metrics",
            "stability",
            "instability",
            "collapse_risk",
            "freeze_risk",
            "thaw_readiness",
            "commands",
            "metadata",
        ):
            if m1.get(key) != m2.get(key):
                diffs.append(f"{key} diverges between independent process calls")
        tp_output = out1

    else:
        tp_before = copy.deepcopy(tp_input)
        for k in ("multi_turn",):
            tp_input.pop(k, None)
        tp_output = cst_ms_process(copy.deepcopy(tp_input), mode="testbench")
        ms = _ms(tp_output)

        if not ms:
            diffs.append("TP.cst.ms missing")

        if expected.get("instability_is_complement"):
            st = ((ms.get("stability") or {}).get("aggregate") or {}).get("value")
            inst = ((ms.get("instability") or {}).get("aggregate") or {}).get("value")
            try:
                if abs(float(inst) - (1.0 - float(st))) > 1e-9:
                    diffs.append(f"instability {inst} != 1 - stability {st}")
                if not (0.0 <= float(st) <= 1.0 and 0.0 <= float(inst) <= 1.0):
                    diffs.append("stability/instability out of [0,1]")
            except (TypeError, ValueError):
                diffs.append("stability/instability not numeric")

        if "freeze_contains" in expected:
            layers = ((ms.get("commands") or {}).get("freeze") or {}).get("layers") or []
            for lid in expected["freeze_contains"]:
                if lid not in layers:
                    diffs.append(f"freeze.layers missing {lid}")

        if expected.get("command_log_has"):
            types = [e.get("command_type") for e in (ms.get("command_log") or [])]
            if expected["command_log_has"] not in types:
                diffs.append(f"command_log missing type {expected['command_log_has']}")

        if expected.get("command_keys"):
            commands = ms.get("commands") or {}
            for k in expected["command_keys"]:
                if k not in commands:
                    diffs.append(f"commands missing key {k}")

        if "instability_lt" in expected:
            inst = ((ms.get("instability") or {}).get("aggregate") or {}).get("value")
            try:
                if not (float(inst) < float(expected["instability_lt"])):
                    diffs.append(f"instability {inst} not < {expected['instability_lt']}")
            except (TypeError, ValueError):
                diffs.append("instability not comparable")

        if "new_context_required" in expected:
            act = ((ms.get("metadata") or {}).get("new_context_required"))
            if act is not expected["new_context_required"]:
                diffs.append(
                    f"new_context_required expected {expected['new_context_required']}, got {act}"
                )

        if expected.get("cob_snapshot_unchanged"):
            before = ((tp_before.get("identity") or {}).get("cob_state_snapshot"))
            after = ((tp_output.get("identity") or {}).get("cob_state_snapshot"))
            if before != after:
                diffs.append("cob_state_snapshot mutated")

        if expected.get("core_unchanged"):
            before = ((tp_before.get("cst") or {}).get("core"))
            after = ((tp_output.get("cst") or {}).get("core"))
            if before != after:
                diffs.append("TP.cst.core mutated")

        exp_audit = ((expected.get("cst") or {}).get("ms") or {}).get("audit") or {}
        act_audit = ms.get("audit") or {}
        for k, v in exp_audit.items():
            if act_audit.get(k) != v:
                diffs.append(f"audit.{k}: expected {v}, got {act_audit.get(k)}")

        exp_hist = ((expected.get("cst") or {}).get("ms") or {}).get("history") or {}
        act_hist = ms.get("history") or {}
        for k, v in exp_hist.items():
            if act_hist.get(k) != v:
                diffs.append(f"history.{k}: expected {v}, got {act_hist.get(k)}")

        commands = ms.get("commands") or {}
        for k in REQUIRED_COMMAND_KEYS:
            if k not in commands:
                diffs.append(f"commands missing required key {k}")

        rp = tp_output.get("routing_path") or []
        if "cst_ms" not in rp:
            diffs.append("routing_path missing 'cst_ms'")

    checker = CSTMSRuleChecker(tp_before, tp_output, rules)
    rule_errors = checker.run()

    passed = len(diffs) == 0

    print("\n----- Test Result -----")
    print(f"- MODE: testbench")
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

    ms = _ms(tp_output)
    print("\nCST-MS Summary:")
    print(f"- turn_index: {(ms.get('status') or {}).get('turn_index')}")
    print(f"- stability: {((ms.get('stability') or {}).get('aggregate') or {}).get('value')}")
    print(f"- freeze layers: {((ms.get('commands') or {}).get('freeze') or {}).get('layers')}")
    print(f"- new_context_required: {((ms.get('metadata') or {}).get('new_context_required'))}")
    print(f"- window len: {len(ms.get('stability_window') or [])}")
    print(f"- routing_path: {tp_output.get('routing_path')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n============================================================")
    print("  ACTIVE MODE: general")
    print("  Input:        cst_ms_input.yaml")
    print("  Validation:   cst_ms_rules.yaml (rulechecker is authoritative)")
    print("  Expected YAML: NOT used in general mode")
    print("============================================================")

    rules_file = os.path.join(BASE_DIR, "cst_ms_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "cst_ms_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    tp_before = copy.deepcopy(tp_input)
    tp_output = cst_ms_process(copy.deepcopy(tp_input), mode="general")

    checker = CSTMSRuleChecker(tp_before, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print("- MODE: general")
    print(f"- {'PASS' if passed else 'FAIL'}: general_cst_ms_input")
    print(f"- Rule-driven validation: {'PASS' if passed else 'FAIL'}")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    ms = _ms(tp_output)
    print("\nCST-MS Summary (general mode):")
    print(f"- turn_index: {(ms.get('status') or {}).get('turn_index')}")
    print(f"- stability: {((ms.get('stability') or {}).get('aggregate') or {}).get('value')}")
    print(f"- instability: {((ms.get('instability') or {}).get('aggregate') or {}).get('value')}")
    print(f"- freeze layers: {((ms.get('commands') or {}).get('freeze') or {}).get('layers')}")
    print(f"- new_context_required: {((ms.get('metadata') or {}).get('new_context_required'))}")
    print(f"- window len: {len(ms.get('stability_window') or [])}")
    print(f"- command_log entries: {len(ms.get('command_log') or [])}")
    print(f"- routing_path: {tp_output.get('routing_path')}")
    print(f"- provisional_metrics: {((ms.get('audit') or {}).get('provisional_metrics'))}")

    return {
        "id": "general_cst_ms_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" CST-MS Testbench Runner - Starting Execution")
    print("============================================================")

    raw_mode = (TESTBENCH_CONFIG or {}).get("mode", "testbench")
    mode = _normalize_mode(raw_mode)

    print(f"- Config received from run.py: {TESTBENCH_CONFIG}")
    print(f"- MODE (raw):  {raw_mode!r}")
    print(f"- MODE (active): {mode}")
    if mode == "testbench":
        print("- Path: cst_ms_tests_to_run.yaml → cst_ms_testbench.yaml expected blocks")
    else:
        print("- Path: cst_ms_input.yaml → cst_ms_rules.yaml rulechecker")

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
        print("\n[MODE=testbench] Loading enabled tests from cst_ms_tests_to_run.yaml")
        tests_to_run_file = os.path.join(BASE_DIR, "cst_ms_tests_to_run.yaml")
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
    print(" CST-MS Testbench Summary")
    print("============================================================")
    print(f"- MODE: {mode}")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(f" CST-MS Testbench Runner - Complete (MODE={mode})")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

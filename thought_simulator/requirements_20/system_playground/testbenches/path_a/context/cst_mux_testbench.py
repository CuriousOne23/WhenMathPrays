"""
CST-Mux Testbench (Version 0.1)
  • mode == "testbench" → cst_mux_testbench.yaml structural / behavioral match
  • mode == "general"   → cst_mux_input.yaml + cst_mux_rules.yaml
Aligned with progressive_lineup_testing.md,
cst_mux_py_struc_pgm.md, patha_field_names.md (TP.cst.mux lock).
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

from thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cst_mux_rulechecker import (  # noqa: E402
    CSTMUXRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.cst_mux.cst_mux import (  # noqa: E402
    get_primitive_name,
    process as cst_mux_process,
)

assert get_primitive_name() == "cst_mux", (
    f"Primitive name mismatch: expected cst_mux, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _mux(tp: dict) -> dict:
    return ((tp or {}).get("cst") or {}).get("mux") or {}


def _usp(tp: dict) -> dict:
    return _mux(tp).get("unified_stability_packet") or {}


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

    rules_file = os.path.join(BASE_DIR, "cst_mux_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "cst_mux_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in cst_mux_testbench.yaml")

    tp_input = copy.deepcopy(tb_test["input"])
    expected = tb_test.get("expected") or {}

    print("- Active MODE: testbench")
    print("- Input Source: cst_mux_testbench.yaml")
    print("- Expected Source: cst_mux_testbench.yaml (expected block)")
    print("- Rulechecker: diagnostic only (PASS/FAIL driven by expected block)")

    diffs = []
    tp_before = copy.deepcopy(tp_input)

    if test_id == "cst_mux_deterministic_replay":
        out1 = cst_mux_process(copy.deepcopy(tp_input), mode="testbench")
        out2 = cst_mux_process(copy.deepcopy(tp_input), mode="testbench")
        u1 = _usp(out1)
        u2 = _usp(out2)
        for key in ("turn_index", "layer_index", "core", "ms", "flags", "new_context_required"):
            if u1.get(key) != u2.get(key):
                diffs.append(f"USP.{key} diverges between independent process calls")
        tp_output = out1
    else:
        tp_output = cst_mux_process(copy.deepcopy(tp_input), mode="testbench")
        mux = _mux(tp_output)
        usp = _usp(tp_output)

        if expected.get("envelope_present") and not mux:
            diffs.append("TP.cst.mux missing")

        if expected.get("usp_present") and not usp:
            diffs.append("unified_stability_packet missing")

        if expected.get("routing_has_cst_mux"):
            rp = tp_output.get("routing_path") or []
            if "cst_mux" not in rp:
                diffs.append("routing_path missing 'cst_mux'")

        if "layer_index" in expected:
            act = mux.get("layer_index") or {}
            for lid, idx in expected["layer_index"].items():
                if act.get(lid) != idx:
                    diffs.append(f"layer_index[{lid}] expected {idx}, got {act.get(lid)}")

        if "core_freeze_contains" in expected:
            frozen = (((usp.get("core") or {}).get("signals") or {}).get("freeze") or {}).get(
                "frozen_objects"
            ) or []
            for lid in expected["core_freeze_contains"]:
                if lid not in frozen:
                    diffs.append(f"USP.core freeze missing {lid}")

        if "flag_freeze_L1" in expected:
            flags = usp.get("flags") or {}
            freeze = flags.get("freeze") or {}
            act = freeze.get("L1") if isinstance(freeze, dict) else flags.get("frozen")
            if bool(act) != bool(expected["flag_freeze_L1"]):
                diffs.append(f"flag freeze L1 expected {expected['flag_freeze_L1']}, got {act}")

        if "ms_stability_aggregate" in expected:
            act = (((usp.get("ms") or {}).get("stability") or {}).get("aggregate") or {}).get(
                "value"
            )
            try:
                if abs(float(act) - float(expected["ms_stability_aggregate"])) > 1e-9:
                    diffs.append(
                        f"ms stability aggregate expected {expected['ms_stability_aggregate']}, got {act}"
                    )
            except (TypeError, ValueError):
                diffs.append("ms stability aggregate not numeric")

        if "ms_ambiguity_count" in expected:
            act = (((usp.get("ms") or {}).get("ambiguity_summary") or {}).get("count"))
            if act != expected["ms_ambiguity_count"]:
                diffs.append(
                    f"ms ambiguity count expected {expected['ms_ambiguity_count']}, got {act}"
                )

        if "new_context_required" in expected:
            act = usp.get("new_context_required")
            if bool(act) != bool(expected["new_context_required"]):
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

        if expected.get("ms_unchanged"):
            before = ((tp_before.get("cst") or {}).get("ms"))
            after = ((tp_output.get("cst") or {}).get("ms"))
            if before != after:
                diffs.append("TP.cst.ms mutated")

        if "ms_instability_lt" in expected:
            act = (((usp.get("ms") or {}).get("instability") or {}).get("aggregate") or {}).get(
                "value"
            )
            try:
                if not (float(act) < float(expected["ms_instability_lt"])):
                    diffs.append(f"ms instability {act} not < {expected['ms_instability_lt']}")
            except (TypeError, ValueError):
                diffs.append("ms instability not comparable")

        if expected.get("no_invented_instability"):
            # Mux must not invent a higher instability than MS provided
            ms_in = (((tp_before.get("cst") or {}).get("ms") or {}).get("instability") or {}).get(
                "aggregate"
            ) or {}
            ms_out = (((usp.get("ms") or {}).get("instability") or {}).get("aggregate") or {})
            try:
                if abs(float(ms_out.get("value")) - float(ms_in.get("value"))) > 1e-9:
                    diffs.append("Mux altered MS instability (invented instability)")
            except (TypeError, ValueError):
                diffs.append("instability comparison failed")

    checker = CSTMUXRuleChecker(tp_before, tp_output, rules)
    rule_errors = checker.run()

    passed = len(diffs) == 0

    print("\n----- Test Result -----")
    print("- MODE: testbench")
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

    mux = _mux(tp_output)
    usp = _usp(tp_output)
    print("\nCST-Mux Summary:")
    print(f"- turn_index: {(mux.get('status') or {}).get('turn_index')}")
    print(f"- layer_count: {(mux.get('status') or {}).get('layer_count')}")
    print(f"- layer_index: {mux.get('layer_index')}")
    print(f"- new_context_required: {usp.get('new_context_required')}")
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
    print("  Input:        cst_mux_input.yaml")
    print("  Validation:   cst_mux_rules.yaml (rulechecker is authoritative)")
    print("  Expected YAML: NOT used in general mode")
    print("============================================================")

    rules_file = os.path.join(BASE_DIR, "cst_mux_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "cst_mux_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    tp_before = copy.deepcopy(tp_input)
    tp_output = cst_mux_process(copy.deepcopy(tp_input), mode="general")

    checker = CSTMUXRuleChecker(tp_before, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print("- MODE: general")
    print(f"- {'PASS' if passed else 'FAIL'}: general_cst_mux_input")
    print(f"- Rule-driven validation: {'PASS' if passed else 'FAIL'}")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    mux = _mux(tp_output)
    usp = _usp(tp_output)
    print("\nCST-Mux Summary (general mode):")
    print(f"- turn_index: {(mux.get('status') or {}).get('turn_index')}")
    print(f"- layer_index: {mux.get('layer_index')}")
    print(f"- new_context_required: {usp.get('new_context_required')}")
    print(f"- routing_path: {tp_output.get('routing_path')}")
    print(f"- provisional_flags: {((mux.get('audit') or {}).get('provisional_flags'))}")

    return {
        "id": "general_cst_mux_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" CST-Mux Testbench Runner - Starting Execution")
    print("============================================================")

    raw_mode = (TESTBENCH_CONFIG or {}).get("mode", "testbench")
    mode = _normalize_mode(raw_mode)

    print(f"- Config received from run.py: {TESTBENCH_CONFIG}")
    print(f"- MODE (raw):  {raw_mode!r}")
    print(f"- MODE (active): {mode}")
    if mode == "testbench":
        print("- Path: cst_mux_tests_to_run.yaml → cst_mux_testbench.yaml expected blocks")
    else:
        print("- Path: cst_mux_input.yaml → cst_mux_rules.yaml rulechecker")

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
        print("\n[MODE=testbench] Loading enabled tests from cst_mux_tests_to_run.yaml")
        tests_to_run_file = os.path.join(BASE_DIR, "cst_mux_tests_to_run.yaml")
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
    print(" CST-Mux Testbench Summary")
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
    print(f" CST-Mux Testbench Runner - Complete (MODE={mode})")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

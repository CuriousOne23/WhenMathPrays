"""
IdOB Testbench — structure-to-meaning via primitives/idob/idob.py.
Every enabled test prints utterance + input + output packet.
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
REPO_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from thought_simulator.requirements_20.system_playground.testbenches.path_a.identity.idob_rulechecker import (  # noqa: E402
    IdOBRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.idob.idob import (  # noqa: E402
    IdOB,
    get_primitive_name,
)

assert get_primitive_name() == "idob"

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _pkt(tp):
    return (tp or {}).get("idob") or {}


def _compare_idob(actual_tp, expected):
    pkt = _pkt(actual_tp)
    for key in (
        "resolution_status",
        "selected_group_id",
        "ready_for_ouba",
        "path_b_eligible",
        "idob_complete",
        "residue_code",
        "first_meaning_cycle",
        "structural_key",
    ):
        if key in (expected or {}):
            exp = expected.get(key)
            act = pkt.get(key)
            if exp is None and act not in (None,):
                return False, f"idob.{key} expected null, got {act!r}"
            if exp is not None and act != exp:
                return False, f"idob.{key} expected {exp!r}, got {act!r}"
    if expected.get("meaning_semantics", "_omit") is None:
        if pkt.get("meaning_semantics") is not None:
            return False, "meaning_semantics expected null"
    if expected.get("routing_filter_unchanged"):
        before = ((actual_tp.get("_trace_input") or {}).get("process") or {}).get("routing_filter")
        after = (actual_tp.get("process") or {}).get("routing_filter")
        if before is not None and before != after:
            return False, "routing_filter changed"
    return True, None


def _print_trace(test_id, utterance, tp_input, tp_output):
    pkt = _pkt(tp_output)
    print("\n----- UTTERANCE (carrier) -----")
    print(utterance if utterance is not None else "(none — card-only)")
    print("\n----- INPUT -----")
    show = {k: tp_input.get(k) for k in ("utterance", "card_id", "cie_id", "packs_loaded")}
    show["process.routing_filter"] = (tp_input.get("process") or {}).get("routing_filter")
    print(json.dumps(show, indent=2, default=str))
    print("\n----- OUTPUT packet (tp.idob) -----")
    keys = [
        "utterance",
        "card_id",
        "assignment_status",
        "structural_key",
        "residue_code",
        "identity_residual",
        "candidate_group_ids",
        "final_rank_order",
        "selected_group_id",
        "cie_id",
        "first_meaning_cycle",
        "meaning_delta_h",
        "meaning_cie_delta",
        "resolution_status",
        "ready_for_ouba",
        "path_b_eligible",
        "idob_complete",
        "routing_filter_mutated",
        "expand_target",
    ]
    slim = {k: pkt.get(k) for k in keys}
    slim["meaning_semantics"] = pkt.get("meaning_semantics")
    slim["meaning_semantics_prime"] = pkt.get("meaning_semantics_prime")
    print(json.dumps(slim, indent=2, default=str))
    print(f"root idob_complete: {tp_output.get('idob_complete')}")
    print(f"root path_b_eligible: {tp_output.get('path_b_eligible')}")


def run_single_test(test_entry):
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)

    print("\n------------------------------------------------------------")
    print(f"Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    rules = load_yaml(os.path.join(BASE_DIR, "idob_rules.yaml")).get("rules", [])
    tb = load_yaml(os.path.join(BASE_DIR, "idob_testbench.yaml"))
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in idob_testbench.yaml")

    utterance = tb_test.get("utterance") or (tb_test.get("input") or {}).get("utterance")
    tp_input = copy.deepcopy(tb_test.get("input") or {})
    expected = tb_test.get("expected") or {}

    print(f"- Utterance: {utterance!r}")
    print("- Input Source: idob_testbench.yaml")
    print("- Kernel: primitives/idob/idob.py")

    idob = IdOB(copy.deepcopy(tp_input))
    tp_output = idob.process(
        mode="testbench",
        card_id=tp_input.get("card_id"),
        utterance=tp_input.get("utterance"),
        packs_loaded=tp_input.get("packs_loaded"),
        cie_id=tp_input.get("cie_id", "neutral"),
    )
    tp_output["_trace_input"] = tp_input

    structural_match, diff_msg = _compare_idob(tp_output, expected)
    checker = IdOBRuleChecker(tp_input, tp_output, rules, utterance=utterance)
    rule_errors = checker.run()
    passed = structural_match and not rule_errors

    _print_trace(test_id, utterance, tp_input, tp_output)

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    if not structural_match and diff_msg:
        print(f"- Diff: {diff_msg}")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    return {"id": test_id, "enabled": True, "passed": passed, "errors": rule_errors, "utterance": utterance}


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: idob_input.yaml")
    print("------------------------------------------------------------")
    rules = load_yaml(os.path.join(BASE_DIR, "idob_rules.yaml")).get("rules", [])
    tp_input = load_yaml(os.path.join(BASE_DIR, "idob_input.yaml")) or {}
    utterance = tp_input.get("utterance")
    print(f"- Utterance: {utterance!r}")

    idob = IdOB(copy.deepcopy(tp_input))
    tp_output = idob.process(
        mode="general",
        card_id=tp_input.get("card_id"),
        utterance=tp_input.get("utterance"),
        packs_loaded=tp_input.get("packs_loaded"),
        cie_id=tp_input.get("cie_id", "physical_stance"),
    )
    checker = IdOBRuleChecker(tp_input, tp_output, rules, utterance=utterance)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0
    _print_trace("general_idob_input", utterance, tp_input, tp_output)
    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_idob_input")
    if rule_errors:
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    return {"id": "general_idob_input", "enabled": True, "passed": passed, "errors": rule_errors, "utterance": utterance}


def run_testbench():
    print("\n============================================================")
    print(" IdOB Testbench Runner (primitives/idob)")
    print("============================================================")
    mode = (TESTBENCH_CONFIG or {}).get("mode", "testbench")
    print(f"- Mode: {mode}")
    results = []
    total = passed = failed = 0
    if mode == "general":
        result = run_general_mode()
        results.append(result)
        total = 1
        passed = 1 if result["passed"] else 0
        failed = 1 - passed
    else:
        tests = load_yaml(os.path.join(BASE_DIR, "idob_tests_to_run.yaml")).get("tests", [])
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
    print(" IdOB Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}  utterance={r.get('utterance')!r}")
    print("\n============================================================")
    print(" IdOB Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

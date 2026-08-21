"""
COB Testbench (Version 0.1)
  • mode == "testbench" → cob_testbench.yaml structural / behavioral match
  • mode == "general"   → cob_input.yaml + cob_rules.yaml
Aligned with progressive_lineup_testing.md v4.2,
20.32, cob_requirements.md, cob_py_struc_pgm.md v0.1.
"""

from __future__ import annotations

import copy
import json
import os
import sys

import yaml

# Mandatory import-path initialization
TB_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cob_rulechecker import (  # noqa: E402
    COBRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.cob.cob import (  # noqa: E402
    COB,
    IdentityObject,
    get_primitive_name,
    process as cob_process,
)

assert get_primitive_name() == "cob", (
    f"Primitive name mismatch: expected cob, got {get_primitive_name()}"
)

TESTBENCH_CONFIG: dict = {}
BASE_DIR = os.path.dirname(__file__)


def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _make_obj(spec: dict) -> IdentityObject:
    return IdentityObject(
        id=spec["id"],
        referent_map=spec.get("referent_map", {}),
        anchors=spec.get("anchors", []),
        lineage=spec.get("lineage", {}),
        ambiguity=spec.get("ambiguity", {}),
        stability_metrics=spec.get("stability_metrics", {}),
        ordering_metrics=spec.get("ordering_metrics", {}),
    )


def _seed_cob(cob: COB, seed_objects: list):
    for spec in seed_objects or []:
        cob.add_identity_object(_make_obj(spec))


def _snapshot(tp: dict) -> dict:
    return ((tp or {}).get("identity") or {}).get("cob_state_snapshot") or {}


def run_single_test(test_entry):
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)

    print("\n------------------------------------------------------------")
    print(f"Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    rules_file = os.path.join(BASE_DIR, "cob_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "cob_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in cob_testbench.yaml")

    inp = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: cob_testbench.yaml (testbench mode)")
    print("- Expected Output Source: cob_testbench.yaml (expected block)")

    cob = COB()
    _seed_cob(cob, inp.get("seed_objects"))

    # Special handling for eviction (seed many objects)
    if test_id == "cob_bounded_store_and_eviction":
        for i in range(25):
            cob.add_identity_object(
                IdentityObject(
                    id=f"obj{i}",
                    referent_map={},
                    ordering_metrics={
                        "recency": i % 5,
                        "frequency": i % 3,
                        "density": i % 4,
                    },
                )
            )

    # Special handling for multi-turn ordering metrics
    if test_id == "cob_conversation_ordering_metrics":
        turns = inp.get("turns", 12)
        for t in range(turns):
            cob.run({}, {}, t)
        snap = cob._build_snapshot()
        passed = snap.get("conversation_access_count") == expected.get("conversation_access_count", turns)
        print(f"\n----- Test Result -----")
        print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
        print(f"- conversation_access_count: {snap.get('conversation_access_count')}")
        return {"id": test_id, "enabled": True, "passed": passed, "errors": []}

    # Special handling for deterministic replay
    if test_id == "cob_deterministic_replay":
        cob1 = COB()
        cob2 = COB()
        for spec in inp.get("seed_objects") or []:
            cob1.add_identity_object(_make_obj(spec))
            cob2.add_identity_object(_make_obj(copy.deepcopy(spec)))
        signals = inp.get("signals") or {}
        turn = inp.get("turn_index", 0)
        cob1.run(signals, {}, turn)
        cob2.run(signals, {}, turn)
        s1 = cob1._build_snapshot()
        s2 = cob2._build_snapshot()
        # Compare object stability summaries
        passed = s1.get("stability_summary") == s2.get("stability_summary")
        print(f"\n----- Test Result -----")
        print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
        return {"id": test_id, "enabled": True, "passed": passed, "errors": []}

    # Default path: run once via process surface
    tp_input = {
        "turn_index": inp.get("turn_index", 0),
        "signals": inp.get("signals") or {},
        "next_context": (inp.get("signals") or {}).get("next_context") or inp.get("next_context") or {},
        "identity": {},
        "lineage_log": [],
        "routing_path": [],
    }
    # Inject seeded state into a process call by using the cob instance directly
    state = cob.run(
        inp.get("signals") or {},
        {},
        inp.get("turn_index", 0),
    )
    snap = state.cob_state_snapshot

    # Evaluate expected
    passed = True
    diff_msgs = []

    if "object_count_le" in expected:
        count = snap.get("object_count", len(snap.get("objects") or []))
        if count > expected["object_count_le"]:
            passed = False
            diff_msgs.append(f"object_count {count} > {expected['object_count_le']}")

    if "objects" in expected:
        by_id = {o["id"]: o for o in snap.get("objects") or []}
        for oid, exp_obj in expected["objects"].items():
            act = by_id.get(oid)
            if act is None:
                passed = False
                diff_msgs.append(f"missing object {oid}")
                continue
            for mk, mv in (exp_obj.get("stability_metrics") or {}).items():
                if act.get("stability_metrics", {}).get(mk) != mv:
                    passed = False
                    diff_msgs.append(
                        f"{oid}.stability_metrics.{mk} expected {mv}, got {act.get('stability_metrics', {}).get(mk)}"
                    )

    if expected.get("has_merged_child"):
        ids = [o["id"] for o in snap.get("objects") or []]
        if not any("_merged" in i for i in ids):
            passed = False
            diff_msgs.append("no merged child found")

    if expected.get("lineage_event_type"):
        events = [e.get("event_type") for e in state.lineage_log]
        if expected["lineage_event_type"] not in events:
            passed = False
            diff_msgs.append(f"lineage event {expected['lineage_event_type']} not found")

    if expected.get("compressed"):
        # After compression, exact duplicates should be gone
        for o in snap.get("objects") or []:
            rm = o.get("referent_map")
            if isinstance(rm, list) and len(rm) != len(set(rm)):
                passed = False
                diff_msgs.append("exact duplicates remain after compression")

    if expected.get("has_new_context_object"):
        ids = [o["id"] for o in snap.get("objects") or []]
        if not any(i.startswith("ctx_") for i in ids):
            passed = False
            diff_msgs.append("new context object not created")

    if "old1_drift_unchanged" in expected:
        by_id = {o["id"]: o for o in snap.get("objects") or []}
        old = by_id.get("old1")
        if old is None:
            passed = False
            diff_msgs.append("old1 missing")
        else:
            drift = old.get("stability_metrics", {}).get("drift")
            if drift != expected["old1_drift_unchanged"]:
                passed = False
                diff_msgs.append(f"old1 drift expected {expected['old1_drift_unchanged']}, got {drift}")

    # Also run rulechecker on a process-style TP
    tp_out = {
        "identity": {"cob_state_snapshot": snap},
        "lineage_log": list(state.lineage_log),
        "routing_path": ["cob"],
    }
    checker = COBRuleChecker({}, tp_out, rules)
    rule_errors = checker.run()

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    if diff_msgs:
        print("- Diffs:")
        for m in diff_msgs:
            print(f"  * {m}")
    if rule_errors:
        print("- Rule Violations (diagnostic):")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    print(f"- object_count: {snap.get('object_count')}")
    print(f"- objects: {[o.get('id') for o in snap.get('objects') or []]}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: cob_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: cob_input.yaml (general mode)")
    print("- Checked By: cob_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "cob_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "cob_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    tp_output = cob_process(copy.deepcopy(tp_input), mode="general")

    checker = COBRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_cob_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    snap = _snapshot(tp_output)
    print("\n----- COB snapshot summary -----")
    print(f"object_count: {snap.get('object_count')}")
    print(f"routing_path: {tp_output.get('routing_path')}")

    return {
        "id": "general_cob_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" COB Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "cob_tests_to_run.yaml")
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
    print(" COB Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" COB Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

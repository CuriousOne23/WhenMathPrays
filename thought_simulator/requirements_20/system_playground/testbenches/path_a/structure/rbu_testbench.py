"""
RBU Testbench (Version 1.0)
  • mode == "testbench" → rbu_testbench.yaml structural match
  • mode == "general"   → rbu_input.yaml + rbu_rules.yaml
Aligned with progressive_lineup_testing.md v4.1,
20.51_rbu_prim.md v4.0, rbu_py_struc_pgm.md.
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

from thought_simulator.requirements_20.system_playground.testbenches.path_a.structure.rbu_rulechecker import (  # noqa: E402
    RBURuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.rbu.rbu import (  # noqa: E402
    RBU,
    get_primitive_name,
)

assert get_primitive_name() == "rbu", (
    f"Primitive name mismatch: expected rbu, got {get_primitive_name()}"
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


def _sem(tp):
    return (tp or {}).get("semantic") or {}


def _meta(tp):
    return (tp or {}).get("metadata") or {}


def _compare_rbu(actual_tp, expected):
    """Structural foundation comparison (shape + provenance + key fields)."""
    sem = _sem(actual_tp)
    meta = _meta(actual_tp)
    prov = meta.get("provenance") or {}

    if expected.get("meaning_fields_present"):
        for key in ("identity", "stance", "register", "tone", "tags"):
            if key not in sem:
                return False, f"semantic.{key} missing"
        if "lineage_markers" not in meta:
            return False, "metadata.lineage_markers missing"

    if expected.get("empty_commit"):
        # Empty commit: fields present but identity/tags empty
        if sem.get("identity") not in ({}, None):
            # allow empty dict
            if sem.get("identity"):
                return False, f"expected empty identity, got {sem.get('identity')}"
        if sem.get("tags") not in ([], None):
            return False, f"expected empty tags, got {sem.get('tags')}"

    if expected.get("provenance_origin") == "RBU":
        if prov.get("origin") != "RBU" or prov.get("last_update") != "RBU":
            return False, f"provenance origin/last_update not RBU: {prov}"

    if "identity_persona" in expected:
        persona = (sem.get("identity") or {}).get("persona")
        if persona != expected["identity_persona"]:
            return False, f"identity.persona expected {expected['identity_persona']!r}, got {persona!r}"

    if expected.get("tags_nonempty"):
        if not sem.get("tags"):
            return False, "expected non-empty semantic.tags"

    if "identity_cycle" in expected:
        cycle = (meta.get("lineage_markers") or {}).get("identity_cycle")
        if cycle != expected["identity_cycle"]:
            return False, f"lineage_markers.identity_cycle expected {expected['identity_cycle']}, got {cycle}"

    if "register_formality" in expected:
        formality = (sem.get("register") or {}).get("formality")
        if formality != expected["register_formality"]:
            return False, f"register.formality expected {expected['register_formality']!r}, got {formality!r}"

    if "tone_affect" in expected:
        affect = (sem.get("tone") or {}).get("affect")
        if affect != expected["tone_affect"]:
            return False, f"tone.affect expected {expected['tone_affect']!r}, got {affect!r}"

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

    rules_file = os.path.join(BASE_DIR, "rbu_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "rbu_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in rbu_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: rbu_testbench.yaml (testbench mode)")
    print("- Expected Output Source: rbu_testbench.yaml (expected block)")

    rbu = RBU(copy.deepcopy(tp_input))
    tp_output = rbu.process()

    structural_match, diff_msg = _compare_rbu(tp_output, expected)

    checker = RBURuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- RBU Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        sem = _sem(tp_output)
        prov = _meta(tp_output).get("provenance") or {}
        print("ACTUAL RBU fields:")
        print(
            json.dumps(
                {
                    "identity": sem.get("identity"),
                    "stance": sem.get("stance"),
                    "register": sem.get("register"),
                    "tone": sem.get("tone"),
                    "tags": sem.get("tags"),
                    "lineage_markers": _meta(tp_output).get("lineage_markers"),
                    "provenance": prov,
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
    sem = _sem(tp_output)
    print(f"- identity.persona: {(sem.get('identity') or {}).get('persona')}")
    print(f"- tags: {sem.get('tags')}")
    print(f"- lineage_cycle: {(_meta(tp_output).get('lineage_markers') or {}).get('identity_cycle')}")
    prov = _meta(tp_output).get("provenance") or {}
    print(f"- provenance_origin: {prov.get('origin')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: rbu_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: rbu_input.yaml (general mode)")
    print("- Checked By: rbu_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "rbu_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "rbu_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    rbu = RBU(copy.deepcopy(tp_input))
    tp_output = rbu.process()

    checker = RBURuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_rbu_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    sem = _sem(tp_output)
    prov = _meta(tp_output).get("provenance") or {}
    print("\n----- RBU fields -----")
    print(
        json.dumps(
            {
                "identity": sem.get("identity"),
                "stance": sem.get("stance"),
                "register": sem.get("register"),
                "tone": sem.get("tone"),
                "tags": sem.get("tags"),
                "lineage_markers": _meta(tp_output).get("lineage_markers"),
                "provenance": prov,
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
        "id": "general_rbu_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" RBU Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "rbu_tests_to_run.yaml")
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
    print(" RBU Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" RBU Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

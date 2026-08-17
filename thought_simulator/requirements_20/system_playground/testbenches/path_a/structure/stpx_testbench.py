"""
STPX Testbench (Version 1.0)
  • mode == "testbench" → stpx_testbench.yaml structural match
  • mode == "general"   → stpx_input.yaml + stpx_rules.yaml
Aligned with progressive_lineup_testing.md v4.1,
20.49_stpx_prim.md v4.0, stpx_py_struc_pgm.md.
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

from thought_simulator.requirements_20.system_playground.testbenches.path_a.structure.stpx_rulechecker import (  # noqa: E402
    STPXRuleChecker,
)
from thought_simulator.requirements_20.system_playground.primitives.stpx.stpx import (  # noqa: E402
    STPX,
    get_primitive_name,
)

assert get_primitive_name() == "stpx", (
    f"Primitive name mismatch: expected stpx, got {get_primitive_name()}"
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


def _slm(tp):
    return ((tp or {}).get("metadata") or {}).get("semantic_layer_metadata") or {}


def _compare_stpx(actual_tp, expected):
    """Structural foundation comparison (shape + provenance, not full cue content)."""
    cues = _slm(actual_tp).get("stpx_cues")
    prov = _slm(actual_tp).get("semantic_layer_provenance") or {}

    if not isinstance(cues, dict):
        return False, "stpx_cues missing or not a dict"

    families = expected.get("stpx_cues_families") or ["lexical", "structural", "constraint", "repair"]
    for fam in families:
        if fam not in cues or not isinstance(cues[fam], list):
            return False, f"stpx_cues.{fam} missing or not a list"

    if expected.get("empty_families"):
        for fam in families:
            if cues.get(fam):
                return False, f"expected empty family {fam}, got {cues.get(fam)}"

    if expected.get("lexical_nonempty") and not cues.get("lexical"):
        return False, "expected non-empty lexical family"

    if expected.get("constraint_nonempty") and not cues.get("constraint"):
        return False, "expected non-empty constraint family"

    if expected.get("repair_nonempty") and not cues.get("repair"):
        return False, "expected non-empty repair family"

    if expected.get("provenance_origin") == "STPX":
        if prov.get("origin") != "STPX" or prov.get("last_update") != "STPX":
            return False, f"provenance origin/last_update not STPX: {prov}"

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

    rules_file = os.path.join(BASE_DIR, "stpx_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    testbench_file = os.path.join(BASE_DIR, "stpx_testbench.yaml")
    tb = load_yaml(testbench_file)
    tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
    if tb_test is None:
        raise KeyError(f"Test ID {test_id} not found in stpx_testbench.yaml")

    tp_input = tb_test["input"]
    expected = tb_test.get("expected") or {}

    print("- Input Source: stpx_testbench.yaml (testbench mode)")
    print("- Expected Output Source: stpx_testbench.yaml (expected block)")

    stpx = STPX(copy.deepcopy(tp_input))
    tp_output = stpx.process()

    structural_match, diff_msg = _compare_stpx(tp_output, expected)

    checker = STPXRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = structural_match

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if not structural_match:
        print("\n----- STPX Diff -----")
        if diff_msg:
            print(f"  {diff_msg}")
        cues = _slm(tp_output).get("stpx_cues") or {}
        prov = _slm(tp_output).get("semantic_layer_provenance") or {}
        print("ACTUAL STPX fields:")
        print(
            json.dumps(
                {
                    "families": {k: len(v) if isinstance(v, list) else None for k, v in cues.items()},
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
    cues = _slm(tp_output).get("stpx_cues") or {}
    print(f"- lexical_count: {len(cues.get('lexical') or [])}")
    print(f"- structural_count: {len(cues.get('structural') or [])}")
    print(f"- constraint_count: {len(cues.get('constraint') or [])}")
    print(f"- repair_count: {len(cues.get('repair') or [])}")
    prov = _slm(tp_output).get("semantic_layer_provenance") or {}
    print(f"- provenance_origin: {prov.get('origin')}")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_general_mode():
    print("\n------------------------------------------------------------")
    print("Running General Mode: stpx_input.yaml")
    print("------------------------------------------------------------")
    print("- Input Source: stpx_input.yaml (general mode)")
    print("- Checked By: stpx_rules.yaml (rule-driven validation)")

    rules_file = os.path.join(BASE_DIR, "stpx_rules.yaml")
    rules = load_yaml(rules_file).get("rules", [])

    input_file = os.path.join(BASE_DIR, "stpx_input.yaml")
    tp_input = load_yaml(input_file) or {}
    for k in ("mode", "primitive", "version", "notes"):
        tp_input.pop(k, None)

    stpx = STPX(copy.deepcopy(tp_input))
    tp_output = stpx.process()

    checker = STPXRuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()
    passed = len(rule_errors) == 0

    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: general_stpx_input")
    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    cues = _slm(tp_output).get("stpx_cues") or {}
    prov = _slm(tp_output).get("semantic_layer_provenance") or {}
    print("\n----- STPX fields -----")
    print(
        json.dumps(
            {
                "families": {k: len(v) if isinstance(v, list) else None for k, v in cues.items()},
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
        "id": "general_stpx_input",
        "enabled": True,
        "passed": passed,
        "errors": rule_errors,
    }


def run_testbench():
    print("\n============================================================")
    print(" STPX Testbench Runner - Starting Execution")
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
        tests_to_run_file = os.path.join(BASE_DIR, "stpx_tests_to_run.yaml")
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
    print(" STPX Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" STPX Testbench Runner - Complete")
    print("============================================================")


if __name__ == "__main__":
    set_testbench_config({"mode": "testbench"})
    run_testbench()

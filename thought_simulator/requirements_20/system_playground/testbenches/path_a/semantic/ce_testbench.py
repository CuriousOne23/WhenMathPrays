"""
CE Testbench (Version 1.0)
This module is imported by run.py.

It provides:
    • set_testbench_config(config)
    • run_testbench()

And internally runs the CE testbench runner.
"""

import os
import yaml
import json
import copy

from thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.ce_rulechecker import CERuleChecker
from thought_simulator.requirements_20.system_playground.primitives.ce.ce import CE


# ============================================================
# Global config injected by run.py
# ============================================================
TESTBENCH_CONFIG = {}


def set_testbench_config(config):
    """
    Called by run.py before running the testbench.
    Stores configuration for this testbench module.
    """
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config


# ============================================================
# Utility helpers
# ============================================================

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def deep_compare(a, b):
    """Deep structural comparison of two TP dictionaries."""
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


# ============================================================
# CE Test Runner
# ============================================================

def run_single_test(test_entry):
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)
    input_file = test_entry["input"]
    expected_file = test_entry["expected_output"]
    rules_file = test_entry["rules"]
    rulechecker_file = test_entry["rulechecker"]

    print("\n------------------------------------------------------------")
    print(f"Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    # Load input TP
    tp_input = load_yaml(input_file)

    # Load expected output TP
    tp_expected = load_yaml(expected_file)

    # Load rules
    rules = load_yaml(rules_file)["rules"]

    # Print general info
    print(f"- Primitive: CE")
    print(f"- Mode: testbench")
    print(f"- Input File: {input_file}")
    print(f"- Expected Output File: {expected_file}")
    print(f"- Rules File: {rules_file}")
    print(f"- Rulechecker: {rulechecker_file}")

    # Run CE
    ce = CE(copy.deepcopy(tp_input))
    ce.inspect()
    tp_output = ce.tp

    # Compare output with expected
    structural_match = deep_compare(tp_output, tp_expected)

    # Run rulechecker
    checker = CERuleChecker(tp_input, tp_output, rules)
    rule_errors = checker.run()

    # Determine pass/fail
    passed = structural_match and len(rule_errors) == 0

    # Print results
    print("\n----- Test Result -----")
    print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
    print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")

    if rule_errors:
        print("- Rule Violations:")
        for rid, msg in rule_errors:
            print(f"  * [{rid}] {msg}")
    else:
        print("- Rule Violations: None")

    return {
        "id": test_id,
        "enabled": True,
        "passed": passed,
        "errors": rule_errors
    }


# ============================================================
# run_testbench() — REQUIRED BY run.py
# ============================================================

def run_testbench():
    """
    Called by run.py to execute the CE testbench.
    """
    print("\n============================================================")
    print(" CE Testbench Runner — Starting Execution")
    print("============================================================")

    tests_to_run = load_yaml("ce_tests_to_run.yaml")
    tests = tests_to_run["tests"]

    results = []
    total = 0
    passed = 0
    failed = 0

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
    print(" CE Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")

    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" CE Testbench Runner — Complete")
    print("============================================================")

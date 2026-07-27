"""
IE Testbench — Path‑A Intake Envelope
Development-mode testbench runner for the IE primitive.

This module:
    • Loads ie_testbench.yaml
    • Applies configuration injected by run.py
    • Calls the IE primitive (run_ie)
    • Compares actual vs expected
    • Prints pass/fail results
"""

import os
import yaml

# Import the IE primitive
from thought_simulator.requirements_20.system_playground.primitives.ie.ie import run_ie

# ---------------------------------------------------------------------------
# Global testbench configuration (injected by run.py)
# ---------------------------------------------------------------------------

TESTBENCH_CONFIG = {
    "mode": "standalone",
    "use_inb": False,
    "use_iiinb": False,
    "use_ie": True,
    "tests_to_run": {}
}

def set_testbench_config(config: dict):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config


# ---------------------------------------------------------------------------
# Load YAML test definitions
# ---------------------------------------------------------------------------

def _load_yaml_tests():
    """
    Loads ie_testbench.yaml from the same directory.
    """
    here = os.path.dirname(__file__)
    yaml_path = os.path.join(here, "ie_testbench.yaml")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("tests", [])


# ---------------------------------------------------------------------------
# Comparison helpers
# ---------------------------------------------------------------------------

def _compare(expected: dict, actual: dict) -> bool:
    """
    Compare expected vs actual IE output.
    Only keys present in expected are compared.
    """
    for key, exp_val in expected.items():
        act_val = actual.get(key)

        if act_val != exp_val:
            print(f"    ❌ MISMATCH in '{key}':")
            print(f"       expected: {exp_val}")
            print(f"       actual:   {act_val}")
            return False

    return True


# ---------------------------------------------------------------------------
# Main testbench runner
# ---------------------------------------------------------------------------

def run_testbench():
    """
    Executes all IE tests selected in TESTBENCH_CONFIG.
    """
    print("IE Testbench — Starting\n")

    tests = _load_yaml_tests()
    selected = TESTBENCH_CONFIG.get("tests_to_run", {})

    total = 0
    passed = 0

    for test in tests:
        test_id = test.get("id")

        # Skip tests not selected
        if selected.get(test_id) != "Yes":
            continue

        total += 1
        print(f"------------------------------------------------------------")
        print(f"Running Test: {test_id}")
        print(f"Description: {test.get('description')}")
        print(f"------------------------------------------------------------")

        iiinb_output = test.get("iiinb_output", {})
        expected = test.get("expected", {})

        # Call IE primitive
        actual = run_ie(iiinb_output)

        # Compare
        if _compare(expected, actual):
            print(f"    ✅ PASS: {test_id}\n")
            passed += 1
        else:
            print(f"    ❌ FAIL: {test_id}\n")

    print("============================================================")
    print(f"IE Testbench Complete — {passed}/{total} tests passed")
    print("============================================================\n")

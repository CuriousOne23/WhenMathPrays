"""
InB Intake Testbench — Path A
Runs: InB only
Designed to be executed by run.py
"""

import os
import yaml

# ---------------------------------------------------------------------------
# Import REAL InB primitive
# ---------------------------------------------------------------------------

from thought_simulator.requirements_20.system_playground.primitives.inb.inb import InB

# ---------------------------------------------------------------------------
# Load testbench YAML
# ---------------------------------------------------------------------------

def load_testbench():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "inb_testbench.yaml"
    )
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Load rule-family toggles (inb_tests_to_run.yaml)
# ---------------------------------------------------------------------------

def load_tests_to_run():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "inb_tests_to_run.yaml"
    )
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("tests_to_run", {})

# ---------------------------------------------------------------------------
# Map rule families → rule IDs
# ---------------------------------------------------------------------------

RULE_FAMILY_MAP = {
    "whitespace": [
        "whitespace.excess",
        "whitespace.leading",
        "whitespace.trailing"
    ],
    "punctuation": [
        "punctuation.excess",
        "punctuation.illegal"
    ],
    "unicode": [
        "unicode.invalid",
        "unicode.non_ascii"
    ],
    "structural": [
        "structural.malformed",
        "structural.illegal"
    ],
    "output": [
        "output.defects_list_shape"
    ],
    "deterministic": [
        "deterministic.replay",
        "deterministic.no_external_state"
    ]
}

# ---------------------------------------------------------------------------
# Configuration injection (required by run.py)
# ---------------------------------------------------------------------------

CONFIG = {}

def set_testbench_config(config_dict):
    global CONFIG
    CONFIG = config_dict

# ---------------------------------------------------------------------------
# Filter tests based on rule-family toggles
# ---------------------------------------------------------------------------

def filter_tests_by_rule_families(all_tests):

    toggles = load_tests_to_run()

    # Build a set of enabled rule IDs
    enabled_rule_ids = set()
    for family, enabled in toggles.items():
        if enabled:
            enabled_rule_ids.update(RULE_FAMILY_MAP.get(family, []))

    filtered = []
    for test in all_tests:
        expected_defects = test.get("expected_defects", [])

        # If test has no expected defects → always include
        if not expected_defects:
            filtered.append(test)
            continue

        # If any expected defect belongs to an enabled rule family → include
        if any(defect in enabled_rule_ids for defect in expected_defects):
            filtered.append(test)

    return filtered

# ---------------------------------------------------------------------------
# Development-mode runner (no unittest)
# ---------------------------------------------------------------------------

def run_testbench():

    testbench = load_testbench()
    all_tests = testbench.get("tests", [])

    # Apply rule-family filtering
    tests = filter_tests_by_rule_families(all_tests)

    print(f"\nLoaded {len(tests)} InB intake test cases (after rule-family filtering).\n")

    for test in tests:

        name = test.get("id", "unnamed")
        print(f"Running: {name} ...", end=" ")

        # Extract TP dictionary from YAML
        tp = test.get("tp", {})

        # Handle long-input generator (optional)
        if test.get("generate_long_input", False):
            length = test.get("long_length", 5000)
            tp["raw_input"] = "A" * length

        raw_input = tp.get("raw_input", "")

        # Execute REAL InB primitive (returns a TP dictionary)
        result_tp = InB(tp)

        # Expected values
        expected_defects = test.get("expected_defects", [])
        expected_failure = test.get("expected_failure", False)

        # Actual defects from InB output
        actual_defects = result_tp.get("defects", [])

        # Checks
        defects_ok = (actual_defects == expected_defects)
        passed = defects_ok

        # ------------------------------------------------------------------
        # PASS/FAIL messaging
        # ------------------------------------------------------------------

        if passed:
            if expected_failure:
                print(f"EXPECTED FAILURE — {name}")
                print(f"PASS: InB correctly detected defects {actual_defects} in input \"{raw_input}\".\n")
            else:
                if expected_defects:
                    print(f"PASS — {name}")
                    print(f"Detected expected defects {expected_defects} in input \"{raw_input}\".\n")
                else:
                    print(f"PASS — {name}")
                    print(f"No defects detected, as expected, for input \"{raw_input}\".\n")
        else:
            if expected_failure:
                print(f"UNEXPECTED PASS — {name}")
                print(f"FAIL: Expected defects {expected_defects}, but InB returned {actual_defects}.\n")
            else:
                print(f"FAIL — {name}")
                print(f"Expected defects {expected_defects}, but InB returned {actual_defects}.")
                print(f"InB failed to detect required defect(s) in input \"{raw_input}\".\n")

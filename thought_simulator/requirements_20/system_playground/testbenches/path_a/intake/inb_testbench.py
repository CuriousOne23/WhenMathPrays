"""
InB Intake Testbench — Path A
Supports two modes:
    • general    → uses inb_input.yaml + inb_rulechecker.py
    • testbench  → uses inb_testbench.yaml + inb_tests_to_run.yaml
Designed to be executed by run.py
"""

import os
import yaml

# ---------------------------------------------------------------------------
# Import REAL InB primitive
# ---------------------------------------------------------------------------

from thought_simulator.requirements_20.system_playground.primitives.inb.inb import InB

# ---------------------------------------------------------------------------
# Import InB rulechecker (for general mode)
# ---------------------------------------------------------------------------

from thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_rulechecker import InB_RuleChecker

# ---------------------------------------------------------------------------
# Load general-mode input YAML
# ---------------------------------------------------------------------------

def load_general_input():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "inb_input.yaml"
    )
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Load testbench YAML (regression mode)
# ---------------------------------------------------------------------------

def load_testbench():
    yaml_path = os.path.join(
        os.path.dirname(__file__),
        "inb_testbench.yaml"
    )
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Load rule-family toggles (regression mode)
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
# Filter tests based on rule-family toggles (regression mode)
# ---------------------------------------------------------------------------

def filter_tests_by_rule_families(all_tests):

    toggles = load_tests_to_run()

    enabled_rule_ids = set()
    for family, enabled in toggles.items():
        if enabled:
            enabled_rule_ids.update(RULE_FAMILY_MAP.get(family, []))

    filtered = []
    for test in all_tests:
        expected_defects = test.get("expected_defects", [])

        # No expected defects → always include
        if not expected_defects:
            filtered.append(test)
            continue

        # Include if any expected defect belongs to an enabled rule family
        if any(defect in enabled_rule_ids for defect in expected_defects):
            filtered.append(test)

    return filtered

# ---------------------------------------------------------------------------
# GENERAL MODE
# ---------------------------------------------------------------------------

def run_general_mode():

    print("\n============================================================")
    print("InB General Mode — Using inb_input.yaml + inb_rulechecker.py")
    print("============================================================\n")

    data = load_general_input()
    tp = data.get("tp", {})
    raw_input = tp.get("raw_input", "")

    print(f"Raw input: \"{raw_input}\"\n")

    # Run primitive
    result_tp = InB(tp)
    primitive_defects = result_tp.get("defects", [])

    print(f"Primitive defects: {primitive_defects}")

    # Run rulechecker
    rc = InB_RuleChecker()
    rulechecker_defects = rc.check(result_tp)

    print(f"Rulechecker defects: {rulechecker_defects}\n")

# ---------------------------------------------------------------------------
# REGRESSION TESTBENCH MODE
# ---------------------------------------------------------------------------

def run_regression_mode():

    testbench = load_testbench()
    all_tests = testbench.get("tests", [])

    tests = filter_tests_by_rule_families(all_tests)

    print(f"\nLoaded {len(tests)} InB intake test cases (after rule-family filtering).\n")

    for test in tests:

        name = test.get("id", "unnamed")
        print(f"Running: {name} ...", end=" ")

        tp = test.get("tp", {})

        # Optional long-input generator
        if test.get("generate_long_input", False):
            length = test.get("long_length", 5000)
            tp["raw_input"] = "A" * length

        raw_input = tp.get("raw_input", "")

        # Execute primitive
        result_tp = InB(tp)
        actual_defects = result_tp.get("defects", [])

        expected_defects = test.get("expected_defects", [])
        expected_failure = test.get("expected_failure", False)

        defects_ok = (actual_defects == expected_defects)
        passed = defects_ok

        # PASS/FAIL messaging
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

# ---------------------------------------------------------------------------
# MAIN ENTRYPOINT
# ---------------------------------------------------------------------------

def run_testbench():

    mode = CONFIG.get("mode", "testbench")

    if mode == "general":
        run_general_mode()
    else:
        run_regression_mode()

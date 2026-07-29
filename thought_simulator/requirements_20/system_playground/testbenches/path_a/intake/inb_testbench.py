"""
InB Intake Testbench — Path A
Supports two modes:
    • general    → primitive + rulechecker
    • testbench  → primitive only (regression)
Designed to be executed by run.py
"""

import os
import yaml

# ---------------------------------------------------------------------------
# Import REAL InB primitive (pure minimal primitive)
# ---------------------------------------------------------------------------

from thought_simulator.requirements_20.system_playground.primitives.inb.inb import InB

# ---------------------------------------------------------------------------
# Import rulechecker (used ONLY in general mode)
# ---------------------------------------------------------------------------

from thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_rulechecker import validate_inb

# ---------------------------------------------------------------------------
# Configuration injection (required by run.py)
# ---------------------------------------------------------------------------

CONFIG = {}

def set_testbench_config(config_dict):
    global CONFIG
    CONFIG = config_dict
    CONFIG.setdefault("mode", "testbench")   # default
    CONFIG.setdefault("use_rulechecker", False)

# ---------------------------------------------------------------------------
# YAML loaders
# ---------------------------------------------------------------------------

def load_general_input():
    path = os.path.join(os.path.dirname(__file__), "inb_input.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_testbench():
    path = os.path.join(os.path.dirname(__file__), "inb_testbench.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_tests_to_run():
    path = os.path.join(os.path.dirname(__file__), "inb_tests_to_run.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("tests_to_run", {})

# ---------------------------------------------------------------------------
# Rule-family → rule IDs
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
# Filter tests based on rule-family toggles
# ---------------------------------------------------------------------------

def filter_tests_by_rule_families(all_tests):

    toggles = load_tests_to_run()
    enabled_rule_ids = set()

    for family, enabled in toggles.items():
        if enabled:
            enabled_rule_ids.update(RULE_FAMILY_MAP.get(family, []))

    filtered = []
    for test in all_tests:
        expected = test.get("expected_defects", [])

        # No expected defects → always include
        if not expected:
            filtered.append(test)
            continue

        # Include if any expected defect belongs to an enabled rule family
        if any(d in enabled_rule_ids for d in expected):
            filtered.append(test)

    return filtered

# ---------------------------------------------------------------------------
# GENERAL MODE — primitive + rulechecker
# ---------------------------------------------------------------------------

def run_general_mode():

    print("\n============================================================")
    print("InB General Mode — Primitive + Rulechecker")
    print("============================================================\n")

    CONFIG["use_rulechecker"] = True

    data = load_general_input()
    inputs = data.get("inputs", [])

    if not inputs:
        print("No inputs found in inb_input.yaml\n")
        return

    passes = 0
    fails = 0
    no_tests = 0

    for entry in inputs:

        input_id = entry.get("id", "unnamed")
        raw = entry.get("raw_input", "")

        print(f"\n--- Input: {input_id} ---")
        print(f"Raw input: \"{raw}\"\n")

        # Wrap playground entry into a TP dict for primitive
        tp = {
            "raw_input": raw,
            "tokens": entry.get("tokens", []),
            "metadata": entry.get("metadata", {})
        }

        # Run pure primitive
        primitive_output = InB(tp)
        primitive_defects = primitive_output.get("defects", [])

        # Run rulechecker externally
        rulechecker_defects = validate_inb(primitive_output)

        print(f"Primitive defects: {primitive_defects}")
        print(f"Rulechecker defects: {rulechecker_defects}")

        # Classification logic
        if not rulechecker_defects:
            print("Result: No test in inb_input.yaml.")
            no_tests += 1
            continue

        # If rulechecker has defects, evaluate pass/fail
        # PASS = primitive defects are a subset of rulechecker defects
        if all(d in rulechecker_defects for d in primitive_defects):
            print("Result: PASS")
            passes += 1
        else:
            print("Result: FAIL")
            fails += 1

    # ------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------
    total = len(inputs)
    print("\n==================== GENERAL MODE SUMMARY ====================")
    print(f"Total inputs:        {total}")
    print(f"PASS:                {passes}")
    print(f"FAIL:                {fails}")
    print(f"No test available:   {no_tests}")
    print("==============================================================\n")

# ---------------------------------------------------------------------------
# REGRESSION MODE — primitive only
# ---------------------------------------------------------------------------

def run_regression_mode():

    CONFIG["use_rulechecker"] = False

    tb = load_testbench()
    all_tests = tb.get("tests", [])
    tests = filter_tests_by_rule_families(all_tests)

    print(f"\nLoaded {len(tests)} InB intake test cases.\n")

    passes = 0
    fails = 0

    for test in tests:

        name = test.get("id", "unnamed")
        tp = test.get("tp", {})
        raw = tp.get("raw_input", "")

        print(f"Running: {name} ...", end=" ")

        # Run pure primitive
        result = InB(tp)
        actual = result.get("defects", [])
        expected = test.get("expected_defects", [])

        if actual == expected:
            passes += 1
            print(f"PASS — {name}")
        else:
            fails += 1
            print(f"FAIL — {name}")
            print(f"Expected: {expected}")
            print(f"Actual:   {actual}\n")

    # ------------------------------------------------------------
    # PASS/FAIL SUMMARY
    # ------------------------------------------------------------
    print("\n==================== SUMMARY ====================")
    print(f"Total tests: {len(tests)}")
    print(f"Passes:      {passes}")
    print(f"Failures:    {fails}")
    print("=================================================\n")

# ---------------------------------------------------------------------------
# MAIN ENTRYPOINT
# ---------------------------------------------------------------------------

def run_testbench():

    mode = CONFIG.get("mode", "testbench")

    if mode == "general":
        run_general_mode()
    else:
        run_regression_mode()

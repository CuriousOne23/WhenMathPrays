# ============================================================
# InB Intake Testbench — Path A
# ============================================================

import os
import yaml

from thought_simulator.requirements_20.system_playground.primitives.inb.inb import InB
from thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_rulechecker import validate_inb

CONFIG = {}

def set_testbench_config(config_dict):
    global CONFIG
    CONFIG = config_dict
    # Default: regression mode does NOT use rulechecker
    CONFIG.setdefault("use_rulechecker", False)

def load_general_input():
    path = os.path.join(os.path.dirname(__file__), "inb_input.yaml")
    return yaml.safe_load(open(path, "r", encoding="utf-8"))

def load_testbench():
    path = os.path.join(os.path.dirname(__file__), "inb_testbench.yaml")
    return yaml.safe_load(open(path, "r", encoding="utf-8"))

def load_tests_to_run():
    path = os.path.join(os.path.dirname(__file__), "inb_tests_to_run.yaml")
    return yaml.safe_load(open(path, "r", encoding="utf-8")).get("tests_to_run", {})

RULE_FAMILY_MAP = {
    "whitespace": ["whitespace.excess", "whitespace.leading", "whitespace.trailing"],
    "punctuation": ["punctuation.excess", "punctuation.illegal"],
    "unicode": ["unicode.invalid", "unicode.non_ascii"],
    "structural": ["structural.malformed", "structural.illegal"],
    "output": ["output.defects_list_shape"],
    "deterministic": ["deterministic.replay", "deterministic.no_external_state"]
}

def filter_tests_by_rule_families(all_tests):
    toggles = load_tests_to_run()
    enabled_ids = set()

    for family, enabled in toggles.items():
        if enabled:
            enabled_ids.update(RULE_FAMILY_MAP.get(family, []))

    filtered = []
    for test in all_tests:
        exp = test.get("expected_defects", [])
        if not exp or any(d in enabled_ids for d in exp):
            filtered.append(test)

    return filtered

# ------------------------------------------------------------
# GENERAL MODE (rulechecker enabled)
# ------------------------------------------------------------

def run_general_mode():
    CONFIG["use_rulechecker"] = True

    print("\n============================================================")
    print("InB General Mode — Primitive + Rulechecker")
    print("============================================================\n")

    data = load_general_input()
    tp = data.get("tp", {})
    raw = tp.get("raw_input", "")

    print(f"Raw input: \"{raw}\"\n")

    result = InB(tp, use_rulechecker=True)
    print(f"Primitive defects: {result.get('primitive_defects')}")
    print(f"Rulechecker defects: {result.get('rulechecker_defects')}\n")

# ------------------------------------------------------------
# REGRESSION MODE (primitive only)
# ------------------------------------------------------------

def run_regression_mode():
    CONFIG["use_rulechecker"] = False

    tb = load_testbench()
    tests = filter_tests_by_rule_families(tb.get("tests", []))

    print(f"\nLoaded {len(tests)} InB intake test cases.\n")

    passes = 0
    fails = 0

    for test in tests:
        name = test.get("id", "unnamed")
        print(f"Running: {name} ...", end=" ")

        tp = test.get("tp", {})
        raw = tp.get("raw_input", "")

        result = InB(tp, use_rulechecker=False)
        actual = result.get("defects", [])
        expected = test.get("expected_defects", [])

        if actual == expected:
            passes += 1
            print(f"PASS — {name}")
        else:
            fails += 1
            print(f"FAIL — {name}")
            print(f"Expected: {expected}")
            print(f"Actual:   {actual}")

    print("\n==================== SUMMARY ====================")
    print(f"Total tests: {len(tests)}")
    print(f"Passes:      {passes}")
    print(f"Failures:    {fails}")
    print("=================================================\n")

def run_testbench():
    mode = CONFIG.get("mode", "testbench")
    if mode == "general":
        run_general_mode()
    else:
        run_regression_mode()

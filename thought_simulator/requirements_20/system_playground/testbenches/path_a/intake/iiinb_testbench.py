"""
IIInB Intake Inspection Testbench — Path A
Supports two modes:
    • general    → primitive + rulechecker (developer harness)
    • testbench  → primitive only (regression, rule-family filtered)
Designed to be executed by run.py
"""

import os
import yaml

# ---------------------------------------------------------------------------
# Primitive imports
# ---------------------------------------------------------------------------

from thought_simulator.requirements_20.system_playground.primitives.iiinb.iiinb import IIInB
from thought_simulator.requirements_20.system_playground.primitives.inb.inb import InB as RealInB
from thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.iiinb_rulechecker import validate_iiinb

# ---------------------------------------------------------------------------
# Configuration injection (required by run.py)
# ---------------------------------------------------------------------------

CONFIG = {}

def set_testbench_config(config_dict):
    global CONFIG
    CONFIG = dict(config_dict)
    CONFIG.setdefault("mode", "testbench")   # "general" or "testbench"
    CONFIG.setdefault("use_inb", False)
    CONFIG.setdefault("use_iiinb", True)
    CONFIG.setdefault("use_ie", False)

# ---------------------------------------------------------------------------
# YAML loaders
# ---------------------------------------------------------------------------

def load_general_input():
    path = os.path.join(os.path.dirname(__file__), "iiinb_input.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_testbench():
    path = os.path.join(os.path.dirname(__file__), "iiinb_testbench.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_tests_to_run():
    path = os.path.join(os.path.dirname(__file__), "iiinb_tests_to_run.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("tests_to_run", {})

# ---------------------------------------------------------------------------
# Rule-family → rule IDs (anomaly flags)
# ---------------------------------------------------------------------------

RULE_FAMILY_MAP = {
    "spacing": [
        "spacing.multiple_spaces",
        "spacing.missing_space_after_punctuation",
        "spacing.leading",
        "spacing.trailing",
    ],
    "punctuation": [
        "punctuation.repeated",
        "punctuation.cluster",
        "punctuation.basic_normalization",
    ],
    "control_chars": [
        "control.tab",
        "control.newline",
        "control.mixed",
    ],
    "normalization": [
        "normalize.whitespace",
        "normalize.punctuation",
        "normalize.case",
    ],
    "deterministic": [
        "deterministic.replay",
        "deterministic.no_external_state",
    ],
}

# ---------------------------------------------------------------------------
# Helper: run IIInB and normalize output into a TP dict
# ---------------------------------------------------------------------------

def run_iiinb(tp):
    """
    tp: dict with at least raw_input, tokens, metadata, structure, normalized
    Handles both dict-style and object-style IIInB outputs.
    """
    iiinb_obj = IIInB(tp)
    result = iiinb_obj.inspect()

    # Dict-style output per spec
    if isinstance(result, dict):
        tp.setdefault("metadata", {})
        tp["metadata"]["iiinb_status"] = result.get("iiinb_status")
        tp["repairs"] = result.get("repair_operations", [])
        tp["anomalies"] = result.get("anomaly_flags", [])
        tp["normalized"] = result.get("normalized", tp.get("raw_input", ""))
        tp["tokens"] = result.get("tokens", tp.get("tokens", []))
        tp["structure"] = result.get("structure", tp.get("structure", {}))
        return tp

    # Object-style output: use attributes populated by IIInB
    tp_obj = iiinb_obj

    # Normalize attribute names to TP fields
    tp_dict = {
        "raw_input": getattr(tp_obj, "raw_input", tp.get("raw_input", "")),
        "metadata": getattr(tp_obj, "metadata", tp.get("metadata", {})),
        "repairs": getattr(tp_obj, "repairs", []),
        "anomalies": getattr(tp_obj, "anomalies", []),
        "normalized": getattr(tp_obj, "normalized", tp.get("raw_input", "")),
        "tokens": getattr(tp_obj, "tokens", tp.get("tokens", [])),
        "structure": getattr(tp_obj, "structure", tp.get("structure", {})),
    }

    # Fallbacks for alternate attribute names
    if hasattr(tp_obj, "repair_operations") and not tp_dict["repairs"]:
        tp_dict["repairs"] = tp_obj.repair_operations
    if hasattr(tp_obj, "anomaly_flags") and not tp_dict["anomalies"]:
        tp_dict["anomalies"] = tp_obj.anomaly_flags
    if "iiinb_status" in getattr(tp_obj, "metadata", {}):
        tp_dict["metadata"]["iiinb_status"] = tp_obj.metadata["iiinb_status"]

    return tp_dict

# ---------------------------------------------------------------------------
# Filter tests based on rule-family toggles (testbench mode)
# ---------------------------------------------------------------------------

def filter_tests_by_rule_families(all_tests):
    toggles = load_tests_to_run()
    enabled_rule_ids = set()

    for family, enabled in toggles.items():
        if enabled:
            enabled_rule_ids.update(RULE_FAMILY_MAP.get(family, []))

    filtered = []
    for test in all_tests:
        expected = test.get("expected", {})
        expected_anomalies = expected.get("anomaly_flags", [])

        # No expected anomalies → always include
        if not expected_anomalies:
            filtered.append(test)
            continue

        # Include if any expected anomaly belongs to an enabled rule family
        if any(d in enabled_rule_ids for d in expected_anomalies):
            filtered.append(test)

    return filtered

# ---------------------------------------------------------------------------
# GENERAL MODE — primitive + rulechecker
# ---------------------------------------------------------------------------

def run_general_mode():
    print("\n============================================================")
    print("IIInB General Mode — Primitive + Rulechecker")
    print("============================================================\n")

    data = load_general_input()
    inputs = data.get("inputs", [])

    if not inputs:
        print("No inputs found in iiinb_input.yaml\n")
        return

    passes = 0
    fails = 0
    no_tests = 0

    for entry in inputs:
        input_id = entry.get("id", "unnamed")
        raw = entry.get("raw_input", "")

        print(f"\n--- Input: {input_id} ---")
        print(f"Raw input: \"{raw}\"\n")

        # Wrap playground entry into a TP dict
        tp = {
            "raw_input": raw,
            "tokens": entry.get("tokens", []),
            "metadata": entry.get("metadata", {}),
            "structure": entry.get("structure", {}),
            "normalized": raw,
        }

        # Optional upstream InB
        if CONFIG.get("use_inb", False):
            tp = RealInB(tp)

        # Run IIInB primitive
        tp = run_iiinb(tp)

        primitive_anomalies = tp.get("anomalies", [])
        rulechecker_anomalies = validate_iiinb(tp)

        print(f"Primitive anomalies: {primitive_anomalies}")
        print(f"Rulechecker anomalies: {rulechecker_anomalies}")

        if not rulechecker_anomalies:
            print("Result: No rulechecker test available for this input.")
            no_tests += 1
            continue

        # PASS = primitive anomalies are a subset of rulechecker anomalies
        if all(d in rulechecker_anomalies for d in primitive_anomalies):
            print("Result: PASS")
            passes += 1
        else:
            print("Result: FAIL")
            fails += 1

    total = len(inputs)
    print("\n==================== GENERAL MODE SUMMARY ====================")
    print(f"Total inputs:        {total}")
    print(f"PASS:                {passes}")
    print(f"FAIL:                {fails}")
    print(f"No rulechecker test: {no_tests}")
    print("==============================================================\n")

# ---------------------------------------------------------------------------
# REGRESSION MODE — primitive only (rule-family filtered)
# ---------------------------------------------------------------------------

def run_regression_mode():
    tb = load_testbench()
    all_tests = tb.get("tests", [])
    tests = filter_tests_by_rule_families(all_tests)

    print(f"\nLoaded {len(tests)} IIInB intake test cases (after rule-family filtering).\n")

    passes = 0
    fails = 0

    for test in tests:
        name = test.get("id", "unnamed")
        expected = test.get("expected", {})

        # Stimulus: either generated long input or YAML-defined input
        if test.get("generate_long_input", False):
            length = test.get("long_length", 5000)
            raw_input = "A" * length
        else:
            raw_input = test.get("input", "")

        tp = {
            "raw_input": raw_input,
            "tokens": test.get("tokens", []),
            "metadata": test.get("metadata", {}),
            "structure": test.get("structure", {}),
            "normalized": raw_input,
        }

        print(f"Running: {name} ...", end=" ")

        # Optional upstream InB
        if CONFIG.get("use_inb", False):
            tp = RealInB(tp)

        # Run IIInB primitive
        tp = run_iiinb(tp)

        # Expected fields
        expected_inb_status = expected.get("inb_status", None)
        expected_iiinb_status = expected.get("iiinb_status", "inspected")
        expected_repairs = expected.get("repair_operations", [])
        expected_anomalies = expected.get("anomaly_flags", [])
        expected_normalized = expected.get("normalized", raw_input)
        expected_tokens = expected.get("tokens", None)
        expected_structure = expected.get("structure", None)

        # Actual fields
        actual_inb_status = tp.get("metadata", {}).get("inb_status")
        actual_iiinb_status = tp.get("metadata", {}).get("iiinb_status")
        actual_repairs = tp.get("repairs", [])
        actual_anomalies = tp.get("anomalies", [])
        actual_normalized = tp.get("normalized", raw_input)
        actual_tokens = tp.get("tokens", [])
        actual_structure = tp.get("structure", {})

        results = []

        def check(label, actual, expected):
            if expected is None:
                return True
            if actual == expected:
                results.append(
                    f"  ✔ {label} AGREES — expected {expected!r}, got {actual!r}"
                )
                return True
            else:
                results.append(
                    f"  ✘ {label} DISAGREES — expected {expected!r}, got {actual!r}"
                )
                return False

        inb_ok = True
        if expected_inb_status is not None:
            inb_ok = check("InB status", actual_inb_status, expected_inb_status)

        iiinb_ok = check("IIInB status", actual_iiinb_status, expected_iiinb_status)
        repairs_ok = check("Repairs", actual_repairs, expected_repairs)
        anomalies_ok = check("Anomalies", actual_anomalies, expected_anomalies)
        normalized_ok = check("Normalized", actual_normalized, expected_normalized)

        tokens_ok = True
        if expected_tokens is not None:
            tokens_ok = check("Tokens", actual_tokens, expected_tokens)

        structure_ok = True
        if expected_structure is not None:
            structure_ok = check("Structure", actual_structure, expected_structure)

        passed = (
            inb_ok and iiinb_ok and repairs_ok and anomalies_ok and
            normalized_ok and tokens_ok and structure_ok
        )

        if passed:
            passes += 1
            print("PASS")
        else:
            fails += 1
            print("FAIL")
            for line in results:
                print(line)
        print("")  # blank line between tests

    print("\n==================== TESTBENCH SUMMARY ====================")
    print(f"Total tests: {len(tests)}")
    print(f"Passes:      {passes}")
    print(f"Failures:    {fails}")
    print("===========================================================\n")

# ---------------------------------------------------------------------------
# MAIN ENTRYPOINT
# ---------------------------------------------------------------------------

def run_testbench():
    mode = CONFIG.get("mode", "testbench")

    if mode == "general":
        run_general_mode()
    else:
        run_regression_mode()

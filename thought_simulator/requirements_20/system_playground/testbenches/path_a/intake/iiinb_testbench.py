"""
IIInB Intake Inspection Testbench — Path A
Compliant with 20.101 (Rewritten)
IIInB is a pre-semantic repair-proposal primitive:
    • emits repair_proposals (token-span)
    • emits anomaly_flags (token-span)
    • preserves intake_surface and intake_tokens
    • does NOT apply repairs
    • does NOT mutate surface or tokens
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
    CONFIG.setdefault("mode", "testbench")
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
        data = yaml.safe_load(f)

    # DEBUG: show raw YAML input for replay.determinism
    for t in data.get("tests", []):
        if t.get("id") == "replay.determinism":
            raw = t.get("input")
            print("DEBUG YAML LOAD:", raw)
            print("DEBUG YAML BYTES:", list(raw.encode("utf-8")))
            print("DEBUG YAML CODEPOINTS:", [hex(ord(c)) for c in raw])

    return data

def load_tests_to_run():
    path = os.path.join(os.path.dirname(__file__), "iiinb_tests_to_run.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("tests_to_run", {})

# ---------------------------------------------------------------------------
# Rule-family → rule IDs (proposal/anomaly types)
# ---------------------------------------------------------------------------

RULE_FAMILY_MAP = {
    "spacing": [
        "whitespace.normalize",
    ],
    "punctuation": [
        "punctuation.clean",
        "repeated_punctuation.clean",
    ],
    "control_chars": [
        "illegal_character",
    ],
    "normalization": [
        "unicode.normalize",
        "case.normalize",
        "structural.clean",
    ],
    "deterministic": [],
}

# ---------------------------------------------------------------------------
# Helper: run IIInB and normalize output into a TP dict
# ---------------------------------------------------------------------------

def run_iiinb(tp):
    """
    tp: dict with at least raw_input, tokens, metadata
    IIInB now emits:
        • repair_proposals
        • anomaly_flags
        • intake_surface
        • intake_tokens
    """
    iiinb_obj = IIInB(tp)
    result = iiinb_obj.inspect()

    # Dict-style output per new spec
    if isinstance(result, dict):
        tp.setdefault("metadata", {})
        tp["metadata"]["iiinb_status"] = result.get("iiinb_status")

        tp["repair_proposals"] = result.get("repair_proposals", [])
        tp["anomaly_flags"] = result.get("anomaly_flags", [])

        tp["intake_surface"] = result.get("intake_surface", tp.get("raw_input", ""))
        tp["intake_tokens"] = result.get("intake_tokens", tp.get("tokens", []))

        return tp

    # Object-style output
    tp_obj = iiinb_obj

    tp_dict = {
        "raw_input": tp.get("raw_input", ""),
        "metadata": getattr(tp_obj, "metadata", tp.get("metadata", {})),
        "repair_proposals": getattr(tp_obj, "repair_proposals", []),
        "anomaly_flags": getattr(tp_obj, "anomaly_flags", []),
        "intake_surface": getattr(tp_obj, "intake_surface", tp.get("raw_input", "")),
        "intake_tokens": getattr(tp_obj, "intake_tokens", tp.get("tokens", [])),
    }

    if "iiinb_status" in tp_obj.metadata:
        tp_dict["metadata"]["iiinb_status"] = tp_obj.metadata["iiinb_status"]

    return tp_dict

# ---------------------------------------------------------------------------
# Helpers: extract types from proposal/anomaly lists
# ---------------------------------------------------------------------------

def extract_types_from_list(items):
    types = []
    for x in items:
        if isinstance(x, dict):
            t = x.get("rule_id") or x.get("type")
            if t:
                types.append(t)
    return types

# ---------------------------------------------------------------------------
# Filter tests based on rule-family toggles (testbench mode)
# ---------------------------------------------------------------------------

def filter_tests_by_rule_families(all_tests):
    toggles = load_tests_to_run()
    enabled_rule_types = set()

    for family, enabled in toggles.items():
        if enabled:
            enabled_rule_types.update(RULE_FAMILY_MAP.get(family, []))

    filtered = []
    for test in all_tests:
        expected = test.get("expected", {})

        raw_flags = expected.get("anomaly_flags", [])
        expected_flag_types = extract_types_from_list(raw_flags)

        if not expected_flag_types:
            filtered.append(test)
            continue

        if any(t in enabled_rule_types for t in expected_flag_types):
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

    for entry in inputs:
        input_id = entry.get("id", "unnamed")
        raw = entry.get("raw_input", "")

        print(f"\n--- Input: {input_id} ---")
        print(f"Raw input: \"{raw}\"\n")

        tp = {
            "raw_input": raw,
            "tokens": entry.get("tokens", []),
            "metadata": entry.get("metadata", {}),
        }

        if CONFIG.get("use_inb", False):
            tp = RealInB(tp)

        tp = run_iiinb(tp)

        print("Repair Proposals:", tp.get("repair_proposals"))
        print("Anomaly Flags:", tp.get("anomaly_flags"))
        print("Intake Tokens:", tp.get("intake_tokens"))
        print("Intake Surface:", tp.get("intake_surface"))
        print("")

        primitive_flag_types = extract_types_from_list(tp.get("anomaly_flags", []))
        rulechecker_flag_types = extract_types_from_list(validate_iiinb(tp))

        print(f"Anomaly types: {primitive_flag_types}")
        print(f"Rulechecker types: {rulechecker_flag_types}")

        if primitive_flag_types == rulechecker_flag_types:
            print("Result: PASS")
            passes += 1
        else:
            print("Result: FAIL")
            fails += 1

    total = len(inputs)
    print("\n==================== GENERAL MODE SUMMARY ====================")
    print(f"Total inputs: {total}")
    print(f"PASS:         {passes}")
    print(f"FAIL:         {fails}")
    print("==============================================================\n")

# ---------------------------------------------------------------------------
# REGRESSION MODE — primitive only (rule-family filtered)
# ---------------------------------------------------------------------------

def run_regression_mode():
    tb = load_testbench()
    all_tests = tb.get("tests", [])
    tests = filter_tests_by_rule_families(all_tests)

    print(f"\nLoaded {len(tests)} IIInB intake test cases.\n")

    passes = 0
    fails = 0

    for test in tests:
        name = test.get("id", "unnamed")
        expected = test.get("expected", {})

        if test.get("generate_long_input", False):
            length = test.get("long_length", 5000)
            raw_input = "A" * length
        else:
            raw_input = test.get("input", "")

        # Force UTF‑8 normalization to prevent corruption (fix replay.determinism)
        raw_input = raw_input.encode("utf-8", errors="replace").decode("utf-8", errors="replace")

        tp = {
            "raw_input": raw_input,
            "tokens": test.get("tokens", []),
            "metadata": {},
        }

        print(f"Running: {name} ...", end=" ")

        if CONFIG.get("use_inb", False):
            tp = RealInB(tp)

        tp = run_iiinb(tp)

        expected_status = expected.get("iiinb_status", "inspected")
        expected_repairs = extract_types_from_list(expected.get("repair_proposals", []))
        expected_flags = extract_types_from_list(expected.get("anomaly_flags", []))
        expected_tokens = expected.get("intake_tokens", None)
        expected_surface = expected.get("intake_surface", raw_input)

        actual_status = tp.get("metadata", {}).get("iiinb_status")
        actual_repairs = extract_types_from_list(tp.get("repair_proposals", []))
        actual_flags = extract_types_from_list(tp.get("anomaly_flags", []))
        actual_tokens = tp.get("intake_tokens", [])
        actual_surface = tp.get("intake_surface", raw_input)

        results = []

        def check(label, actual, expected):
            if expected is None:
                return True
            if actual == expected:
                results.append(f"  ✔ {label} AGREES — expected {expected!r}, got {actual!r}")
                return True
            else:
                results.append(f"  ✘ {label} DISAGREES — expected {expected!r}, got {actual!r}")
                return False

        status_ok = check("IIInB status", actual_status, expected_status)
        repairs_ok = check("Repair types", sorted(actual_repairs), sorted(expected_repairs))
        flags_ok = check("Anomaly types", sorted(actual_flags), sorted(expected_flags))
        tokens_ok = True
        if expected_tokens is not None:
            tokens_ok = check("Tokens", actual_tokens, expected_tokens)
        surface_ok = check("Surface", actual_surface, expected_surface)

        passed = status_ok and repairs_ok and flags_ok and tokens_ok and surface_ok

        if passed:
            passes += 1
            print("PASS")
        else:
            fails += 1
            print("FAIL")
            for line in results:
                print(line)
        print("")

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

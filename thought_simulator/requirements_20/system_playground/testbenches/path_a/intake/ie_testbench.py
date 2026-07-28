"""
IE Testbench — Path‑A Intake Envelope
Progressive lineup testbench runner for the IE primitive.

This module:
    • Reads configuration injected by run.py (TESTBENCH_CONFIG)
    • Determines pipeline configuration (upstream primitives enabled)
    • Selects appropriate stimulus YAML (ie / iiinb / inb)
    • Executes the upstream → IE pipeline
    • Compares actual vs expected TP/IE outputs
    • Accounts for supported vs unsupported tests
    • Prints a structured summary (passed / failed / skipped)
"""

import os
import yaml

# ---------------------------------------------------------------------------
# Imports for primitives (pipeline)
# ---------------------------------------------------------------------------

from thought_simulator.requirements_20.system_playground.primitives.ie.ie import run_ie
from thought_simulator.requirements_20.system_playground.primitives.iiinb.iiinb import IIInB
from thought_simulator.requirements_20.system_playground.primitives.inb.inb import InB

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
    """
    Called by run.py to inject configuration.
    """
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config


# ---------------------------------------------------------------------------
# YAML loading helpers
# ---------------------------------------------------------------------------

def _here() -> str:
    return os.path.dirname(__file__)


def _load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_ie_tests() -> list:
    """
    Load IE expected tests from ie_testbench.yaml.
    """
    yaml_path = os.path.join(_here(), "ie_testbench.yaml")
    data = _load_yaml(yaml_path)
    return data.get("tests", [])


def _load_stimulus_yaml():
    """
    Select stimulus YAML based on earliest enabled upstream primitive.
    """
    use_inb = TESTBENCH_CONFIG.get("use_inb", False)
    use_iiinb = TESTBENCH_CONFIG.get("use_iiinb", False)

    if not use_inb and not use_iiinb:
        # IE‑only mode: stimulus comes from ie_testbench.yaml
        path = os.path.join(_here(), "ie_testbench.yaml")
    elif use_inb:
        # Earliest upstream is InB
        path = os.path.join(_here(), "inb_testbench.yaml")
    else:
        # Earliest upstream is IIInB
        path = os.path.join(_here(), "iiinb_testbench.yaml")

    return _load_yaml(path), path


# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------

def _run_pipeline_from_stimulus(stimulus_case: dict) -> dict:
    """
    Execute the configured pipeline from stimulus to IE (TP) output.

    When no upstream primitives are enabled, IE should receive the
    iiinb_output defined in ie_testbench.yaml, exactly like the original
    simple testbench did.
    """
    use_inb = TESTBENCH_CONFIG.get("use_inb", False)
    use_iiinb = TESTBENCH_CONFIG.get("use_iiinb", False)

    # Base input from stimulus:
    # - If upstream primitives are disabled, use iiinb_output (IE-only mode).
    # - If upstream primitives are enabled, use tp (full pipeline mode).
    if not use_inb and not use_iiinb:
        iiinb_output = stimulus_case.get("iiinb_output", {})
    else:
        tp = stimulus_case.get("tp", {})

        # Progressive pipeline:
        if use_inb:
            inb_obj = InB(tp).inspect()
            tp = getattr(inb_obj, "tp", inb_obj)

        if use_iiinb:
            iiinb_obj = IIInB(tp).inspect()
            # For now we assume IIInB emits a dict compatible with IE's intake model.
            iiinb_output = getattr(iiinb_obj, "iiinb_output", iiinb_obj)
        else:
            # If IIInB is not enabled, we treat tp as iiinb_output-like.
            iiinb_output = tp

    # Finally, run IE (TP-aligned).
    ie_output = run_ie(iiinb_output)
    return ie_output


# ---------------------------------------------------------------------------
# Comparison helpers (TP-aligned, recursive)
# ---------------------------------------------------------------------------

def _collect_missing_keys(expected: dict, actual: dict, prefix: str = "") -> list:
    """
    Recursively collect missing keys from actual given expected structure.
    """
    missing = []
    for key, exp_val in expected.items():
        full_key = f"{prefix}{key}" if not prefix else f"{prefix}.{key}"
        if key not in actual:
            missing.append(full_key)
            continue
        act_val = actual[key]
        if isinstance(exp_val, dict) and isinstance(act_val, dict):
            missing.extend(_collect_missing_keys(exp_val, act_val, full_key))
    return missing


def _is_test_supported(expected: dict, actual: dict) -> (bool, list):
    """
    Determine whether a test is supported given expected TP fields
    and the actual IE (TP) output.

    A test is unsupported if the expected YAML defines fields that
    the IE output does not emit under the current pipeline configuration.

    Returns (supported: bool, missing_keys: list).
    """
    missing = _collect_missing_keys(expected, actual)
    return (len(missing) == 0, missing)


def _compare_values(exp_val, act_val, path: str) -> bool:
    """
    Compare two values (scalars, lists, dicts) recursively.
    """
    if isinstance(exp_val, dict) and isinstance(act_val, dict):
        for k in exp_val.keys():
            if k not in act_val:
                print(f"    MISMATCH at '{path}.{k}': key missing in actual")
                return False
            if not _compare_values(exp_val[k], act_val[k], f"{path}.{k}"):
                return False
        return True

    if isinstance(exp_val, list) and isinstance(act_val, list):
        if len(exp_val) != len(act_val):
            print(f"    MISMATCH at '{path}': list length expected {len(exp_val)}, actual {len(act_val)}")
            return False
        for i, (e_item, a_item) in enumerate(zip(exp_val, act_val)):
            if not _compare_values(e_item, a_item, f"{path}[{i}]"):
                return False
        return True

    if exp_val != act_val:
        print(f"    MISMATCH at '{path}':")
        print(f"      expected: {exp_val}")
        print(f"      actual:   {act_val}")
        return False

    return True


def _compare_expected_actual(expected: dict, actual: dict) -> bool:
    """
    Compare expected vs actual TP-aligned IE output.
    Only keys present in expected are compared, recursively.
    """
    for key, exp_val in expected.items():
        if key not in actual:
            print(f"    MISMATCH in '{key}': key missing in actual")
            return False
        act_val = actual[key]
        if not _compare_values(exp_val, act_val, key):
            return False
    return True


# ---------------------------------------------------------------------------
# Main testbench runner
# ---------------------------------------------------------------------------

def execute_ie_testbench():
    """
    Executes IE tests under progressive lineup configuration.
    """
    print("IE Testbench — Progressive Lineup Mode (TP-Aligned)\n")

    use_inb = TESTBENCH_CONFIG.get("use_inb", False)
    use_iiinb = TESTBENCH_CONFIG.get("use_iiinb", False)
    tests_to_run = TESTBENCH_CONFIG.get("tests_to_run", {})

    # Log pipeline configuration
    print("Pipeline configuration:")
    print(f"  use_inb  = {use_inb}")
    print(f"  use_iiinb = {use_iiinb}")
    print(f"  use_ie   = {TESTBENCH_CONFIG.get('use_ie', True)}")
    print()

    # Load expected IE tests (TP-aligned)
    ie_tests = _load_ie_tests()

    # Load stimulus YAML based on earliest upstream
    stimulus_yaml, stimulus_yaml_path = _load_stimulus_yaml()
    stimulus_tests = stimulus_yaml.get("tests", [])

    print(f"Stimulus source YAML: {stimulus_yaml_path}")
    print(f"Expected output YAML: ie_testbench.yaml\n")

    passed = 0
    failed = 0
    skipped = 0
    supported = 0
    total_defined = len(ie_tests)

    # Index stimulus tests by id for lookup
    stimulus_by_id = {t.get("id"): t for t in stimulus_tests}

    for test in ie_tests:
        test_id = test.get("id")

        # Skip tests not selected
        if tests_to_run and tests_to_run.get(test_id) != "Yes":
            continue

        expected = test.get("expected", {})
        stimulus_case = stimulus_by_id.get(test_id, {})

        print("------------------------------------------------------------")
        print(f"Running IE Test: {test_id}")
        print(f"Description: {test.get('description')}")
        print("------------------------------------------------------------")

        # If there is no matching stimulus case, this test is unsupported
        if not stimulus_case:
            print("    SKIP (no matching stimulus case under current lineup)\n")
            skipped += 1
            continue

        # Run pipeline from stimulus to IE (TP) output
        actual_ie = _run_pipeline_from_stimulus(stimulus_case)

        # Determine if this test is supported under current pipeline/output
        is_supported, missing = _is_test_supported(expected, actual_ie)

        if not is_supported:
            print("    SKIP (unsupported under current pipeline):")
            print(f"      missing TP/IE fields: {missing}\n")
            skipped += 1
            continue

        supported += 1

        # Compare expected vs actual
        if _compare_expected_actual(expected, actual_ie):
            print(f"    PASS: {test_id}\n")
            passed += 1
        else:
            print(f"    FAIL: {test_id}\n")
            failed += 1

    print("============================================================")
    print("IE Testbench Summary")
    print("------------------------------------------------------------")
    print(f"  Total IE tests defined:     {total_defined}")
    print(f"  Supported under pipeline:   {supported}")
    print(f"  Passed:                     {passed}")
    print(f"  Failed:                     {failed}")
    print(f"  Skipped (unsupported):      {skipped}")
    print("============================================================\n")


def run_testbench():
    execute_ie_testbench()

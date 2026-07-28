"""
IE Testbench — Path‑A Intake Envelope
Progressive lineup testbench runner for the IE primitive.

This module:
    • Reads configuration injected by run.py (TESTBENCH_CONFIG)
    • Determines pipeline configuration (upstream primitives enabled)
    • Selects appropriate stimulus YAML (ie / iiinb / inb)
    • Executes the upstream → IE pipeline
    • Compares actual vs expected IE outputs
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


def _load_stimulus_yaml() -> dict:
    """
    Select stimulus YAML based on earliest enabled upstream primitive.

    Rules:
        - If no upstream enabled → use ie_testbench.yaml as stimulus.
        - If earliest upstream is IIInB → use iiinb_testbench.yaml.
        - If earliest upstream is InB → use inb_testbench.yaml.
    """
    use_inb = TESTBENCH_CONFIG.get("use_inb", False)
    use_iiinb = TESTBENCH_CONFIG.get("use_iiinb", False)

    # No upstream: IE-only stimulus
    if not use_inb and not use_iiinb:
        path = os.path.join(_here(), "ie_testbench.yaml")
    # Earliest upstream: InB
    elif use_inb:
        path = os.path.join(_here(), "inb_testbench.yaml")
    # Earliest upstream: IIInB
    else:
        path = os.path.join(_here(), "iiinb_testbench.yaml")

    return _load_yaml(path)


# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------

def _run_pipeline_from_stimulus(stimulus_case: dict) -> dict:
    """
    Execute the configured pipeline from stimulus to IE output.

    stimulus_case: one test case from the stimulus YAML.
    Returns: IE output dict.
    """
    use_inb = TESTBENCH_CONFIG.get("use_inb", False)
    use_iiinb = TESTBENCH_CONFIG.get("use_iiinb", False)

    # Base TP from stimulus
    tp = stimulus_case.get("tp", {})

    # Progressive pipeline:
    # If InB enabled, run InB first.
    if use_inb:
        tp = run_inb(tp)

    # If IIInB enabled, run IIInB next.
    if use_iiinb:
        tp = run_iiinb(tp)

    # Finally, run IE.
    ie_output = run_ie(tp)
    return ie_output


# ---------------------------------------------------------------------------
# Comparison helpers
# ---------------------------------------------------------------------------

def _is_test_supported(expected: dict, required_keys: list) -> (bool, list):
    """
    Determine whether a test is supported given expected IE fields.

    Returns (supported: bool, missing_keys: list).
    """
    missing = [k for k in required_keys if k not in expected]
    return (len(missing) == 0, missing)


def _compare_expected_actual(expected: dict, actual: dict) -> bool:
    """
    Compare expected vs actual IE output.
    Only keys present in expected are compared.
    """
    for key, exp_val in expected.items():
        act_val = actual.get(key)

        if act_val != exp_val:
            print(f"    MISMATCH in '{key}':")
            print(f"      expected: {exp_val}")
            print(f"      actual:   {act_val}")
            return False

    return True


# ---------------------------------------------------------------------------
# Main testbench runner
# ---------------------------------------------------------------------------

def execute_ie_testbench():
    """
    Executes IE tests under progressive lineup configuration.
    """
    print("IE Testbench — Progressive Lineup Mode\n")

    use_inb = TESTBENCH_CONFIG.get("use_inb", False)
    use_iiinb = TESTBENCH_CONFIG.get("use_iiinb", False)
    tests_to_run = TESTBENCH_CONFIG.get("tests_to_run", {})

    # Log pipeline configuration
    print("Pipeline configuration:")
    print(f"  use_inb  = {use_inb}")
    print(f"  use_iiinb = {use_iiinb}")
    print(f"  use_ie   = {TESTBENCH_CONFIG.get('use_ie', True)}")
    print()

    # Load expected IE tests
    ie_tests = _load_ie_tests()

    # Load stimulus YAML based on earliest upstream
    stimulus_yaml = _load_stimulus_yaml()
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

    # Define required keys for IE tests (can be refined per test type)
    required_keys = [
        "normalized_text",
        "tokens",
        "repairs",
        "anomalies",
        "tags",
        "replay",
        "error",
    ]

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

        # Determine if this test is supported under current stimulus
        is_supported, missing = _is_test_supported(expected, required_keys)
        if not is_supported:
            skipped += 1
            print(f"    SKIP: {test_id}")
            print(f"    Reason: expected IE fields not fully defined for this test.")
            print(f"    Missing fields: {missing}\n")
            continue

        supported += 1

        # Run pipeline from stimulus to IE
        actual_ie = _run_pipeline_from_stimulus(stimulus_case)

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
    print(f"  Supported under stimulus:   {supported}")
    print(f"  Passed:                     {passed}")
    print(f"  Failed:                     {failed}")
    print(f"  Skipped (unsupported):      {skipped}")
    print("============================================================\n")

def run_testbench():
    execute_ie_testbench()

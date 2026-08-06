"""
CEx‑CCR Testbench (Mode A - Deterministic Testing)
--------------------------------------------------

This testbench:
    • Loads cex_ccr_testbench.yaml (testbench mode) OR cex_ccr_input.yaml (general mode)
    • Loads static cil_input.yaml (10‑conversation CIL substrate)
    • Injects TP.cex.ie + TP.semantic.importance into the CCR primitive
    • Calls CEx‑CCR.inspect()
    • Compares TP.cex.ccr output against expected values (testbench mode)
    • Prints PASS/FAIL for each scenario

This file follows the same structure as InB, IIInB, IE, and CEx‑IE testbenches.
"""

import os
import yaml
import copy

# Import the CCR primitive
from thought_simulator.requirements_20.system_playground.primitives.cex_ccr.cex_ccr import CExCCR

# Import rulechecker (optional but recommended)
from thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.cex_ccr_rulechecker import (
    validate_cex_ccr_envelope
)

# ============================================================
# GLOBAL CONFIG (injected by run.py)
# ============================================================

TESTBENCH_CONFIG = {
    "mode": "testbench",          # "testbench" or "general"
    "tests_to_run": None,         # YAML file controls selection
    "use_cex_ccr": True,
    "cil_source": "cil_input.yaml"
}

def set_testbench_config(config):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(__file__)

CIL_PATH = os.path.join(BASE_DIR, "cil_input.yaml")
TESTBENCH_PATH = os.path.join(BASE_DIR, "cex_ccr_testbench.yaml")
GENERAL_INPUT_PATH = os.path.join(BASE_DIR, "cex_ccr_input.yaml")
TESTS_TO_RUN_PATH = os.path.join(BASE_DIR, "cex_ccr_tests_to_run.yaml")


# ============================================================
# LOAD YAML HELPERS
# ============================================================

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ============================================================
# MAIN TESTBENCH RUNNER
# ============================================================

def run_testbench():

    print("CEx-CCR Testbench Runner Starting...\n")

    # --------------------------------------------------------
    # Load static CIL substrate (always)
    # --------------------------------------------------------
    cil_data = load_yaml(CIL_PATH)
    cil_substrate = cil_data.get("TP", {}).get("cil", {})

    # --------------------------------------------------------
    # Load testbench or general input
    # --------------------------------------------------------
    if TESTBENCH_CONFIG["mode"] == "testbench":
        tb_data = load_yaml(TESTBENCH_PATH)
        scenarios = {k: v for k, v in tb_data.items() if k.startswith("scenario_")}
        print("Mode: TESTBENCH - using cex_ccr_testbench.yaml\n")
    else:
        tb_data = load_yaml(GENERAL_INPUT_PATH)
        scenarios = {k: v for k, v in tb_data.items() if k.startswith("scenario_")}
        print("Mode: GENERAL - using cex_ccr_input.yaml\n")

    # --------------------------------------------------------
    # Load tests_to_run list
    # --------------------------------------------------------
    tests_to_run_data = load_yaml(TESTS_TO_RUN_PATH)
    tests_to_run = tests_to_run_data.get("tests_to_run", [])

    if tests_to_run == "all":
        selected_scenarios = scenarios
    else:
        selected_scenarios = {k: scenarios[k] for k in tests_to_run if k in scenarios}

    # --------------------------------------------------------
    # Execute each scenario
    # --------------------------------------------------------
    for scenario_name, scenario in selected_scenarios.items():

        print(f"------------------------------------------------------------")
        print(f"Running {scenario_name}: {scenario.get('description', '')}")
        print(f"------------------------------------------------------------")

        # Build TP input
        TP = {
            "cex": {
                "ie": copy.deepcopy(scenario["TP"]["cex"]["ie"])
            },
            "semantic": {
                "importance": copy.deepcopy(scenario["TP"].get("semantic", {}).get("importance", {}))
            },
            "cil": copy.deepcopy(cil_substrate)
        }

        # Run CCR primitive
        ccr = CExCCR(TP)
        TP_out = ccr.inspect()

        # Validate envelope shape
        validate_cex_ccr_envelope(TP_out["cex"]["ccr"])

        # Compare against expected (testbench mode only)
        if TESTBENCH_CONFIG["mode"] == "testbench":
            expected = scenario["expected"]["cex"]["ccr"]
            actual = TP_out["cex"]["ccr"]

            if actual == expected:
                print(f"PASS - {scenario_name}")
                print("PASS - Test passed successfully.")
                print("PASS - Expected CCR envelope:")
                print(expected)
                print("PASS - Actual CCR envelope:")
                print(actual)
            else:
                print(f"FAIL - {scenario_name}")
                print("FAIL - Test failed.")
                print("Expected:")
                print(expected)
                print("Actual:")
                print(actual)

        else:
            # General mode: just print output
            print("Output TP.cex.ccr:")
            print(TP_out["cex"]["ccr"])

        print("\n")

    print("CEx-CCR Testbench Runner Complete.\n")


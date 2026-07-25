"""
Thought Simulator — Testbench Runner
------------------------------------

Usage:
    To run specific testbenches:

        1. In ACTIVE_TEST_MODULES below, comment/uncomment the testbench tuples
           you want to run. Each testbench is a single tuple containing both
           the module path and its configuration.

           ⭐ To disable a testbench, place ONE '#' at the start of the tuple.
           ⭐ You do NOT need to comment out every line.

        2. Each tuple includes "expect_failure":
               expect_failure = False  → test expects everything to be OK
               expect_failure = True   → test expects a failure

           Both are valid and important test modes.

        3. Do NOT modify the runner code at the bottom.

        4. Run from repo root:
               python thought_simulator/requirements_20/system_playground/testbenches/run.py > results.log

           Or from inside testbenches:
               python run.py > results.log

    This script adds the repo root to PYTHONPATH so imports always resolve.
"""

import sys
import os
import unittest

# ============================================================
# === FIX: Add repo root to Python path =======================
# ============================================================

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, repo_root)

# ============================================================
# === SELECT WHICH TESTBENCHES TO RUN (ONLY EDIT HERE) ========
# ============================================================

ACTIVE_TEST_MODULES = [

    # --------------------------------------------------------
    # Path A — Intake Testbenches (InB → IIInB → IE)
    # --------------------------------------------------------

    # --- InB Intake Testbench ---
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_testbench",
    #     {
    #         "mode": "standalone",
    #         "use_inb": True,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "expect_failure": False     # or True
    #     }
    # ),

    # --- IIInB Intake Inspection Testbench ---
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.iiinb_testbench",
    #     {
    #         "mode": "standalone",
    #         "use_inb": False,
    #         "use_iiinb": True,
    #         "use_ie": False,
    #         "expect_failure": False     # or True
    #     }
    # ),

    # --- IE Intake Envelope Testbench ---
    (
        "thought_simulator.requirements_20.system_playground/testbenches/path_a/intake/ie_testbench",
        {
            "mode": "standalone",      # or "progressive"
            "use_inb": False,          # True for progressive
            "use_iiinb": False,        # True for progressive
            "use_ie": True,
            "expect_failure": False    # True = test expects failure
        }
    ),

    # --------------------------------------------------------
    # Path A — CEx Testbenches
    # --------------------------------------------------------

    # --- CEx Intake Testbench ---
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.test_cex_intake",
    #     {
    #         "mode": "standalone",
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "expect_failure": False
    #     }
    # ),

    # --- CEx Boundary Testbench ---
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.boundary.test_cex_boundary",
    #     {
    #         "mode": "standalone",
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "expect_failure": True     # Example: boundary tests often expect failure
    #     }
    # ),

    # --------------------------------------------------------
    # Add more tests here later:
    # --------------------------------------------------------
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.output.test_cex_output",
    #     {
    #         "mode": "standalone",
    #         "expect_failure": False
    #     }
    # ),
]

# ============================================================
# === RUNNER (DO NOT EDIT BELOW THIS LINE) ====================
# ============================================================

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for module_path, config in ACTIVE_TEST_MODULES:
        module = __import__(module_path, fromlist=[''])

        # Pass configuration into the testbench if supported
        if hasattr(module, "set_testbench_config"):
            module.set_testbench_config(config)

        suite.addTests(loader.loadTestsFromModule(module))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

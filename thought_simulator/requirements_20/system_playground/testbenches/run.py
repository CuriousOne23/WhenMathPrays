"""
Thought Simulator — Testbench Runner
------------------------------------

Process Overview:
    • User selects which testbenches to run by commenting/uncommenting
      entries in ACTIVE_TEST_MODULES.

    • Each testbench tuple contains:
          - module path
          - configuration dict

    • Configuration supports:
          mode: "standalone" or "progressive"
          use_inb: True/False
          use_iiinb: True/False
          use_ie: True/False
          expect_failure: True/False

      These flags determine how far upstream the pipeline runs.

    • Primitive correctness is enforced inside each testbench.
      Expectation correctness is logged (stdout → redirected to file).

    • Run from repo root:
          python thought_simulator/requirements_20/system_playground/testbenches/run.py > results.log

      Or from inside testbenches:
          python run.py > results.log
"""

import sys
import os
import unittest

# ============================================================
# === Add repo root to Python path ============================
# ============================================================

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, repo_root)

# ============================================================
# === SELECT TESTBENCHES TO RUN (USER EDITS THIS SECTION) =====
# ============================================================

ACTIVE_TEST_MODULES = [

    # --------------------------------------------------------
    # Path A — Intake Testbenches (InB → IIInB → IE)
    # --------------------------------------------------------

    # Example: InB only (standalone)
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_testbench",
    #     {
    #         "mode": "standalone",
    #         "use_inb": True,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "expect_failure": False
    #     }
    # ),

    # Example: IIInB only (standalone)
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.iiinb_testbench",
    #     {
    #         "mode": "standalone",
    #         "use_inb": False,
    #         "use_iiinb": True,
    #         "use_ie": False,
    #         "expect_failure": False
    #     }
    # ),

    # IE Intake Envelope Testbench (3‑test mode)
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
        {
            "mode": "standalone",      # or "progressive"
            "use_inb": False,          # True → include InB upstream
            "use_iiinb": False,        # True → include IIInB upstream
            "use_ie": True,            # IE always runs for IE testbench
            "expect_failure": False    # User sets expectation
        }
    ),

    # --------------------------------------------------------
    # Path A — CEx Testbenches (examples)
    # --------------------------------------------------------

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

    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.boundary.test_cex_boundary",
    #     {
    #         "mode": "standalone",
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "expect_failure": True
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

        # Inject configuration into testbench
        if hasattr(module, "set_testbench_config"):
            module.set_testbench_config(config)

        suite.addTests(loader.loadTestsFromModule(module))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

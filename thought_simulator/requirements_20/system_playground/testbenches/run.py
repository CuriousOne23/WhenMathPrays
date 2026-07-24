"""
Thought Simulator — Testbench Runner
------------------------------------

Usage:
    To run specific testbenches:

        1. In the HEADER below, comment/uncomment the test modules you want to run.
           All test selections are grouped together in one place.

        2. Do NOT modify the runner code at the bottom.

        3. Run from repo root:
               python thought_simulator/requirements_20/system_playground/testbenches/run.py > cex.log

           Or from inside testbenches:
               python run.py *> cex.log

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

    # --- CEx Intake Testbench ---
    "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.test_cex_intake",

    # --- CEx Boundary Testbench ---
    # "thought_simulator.requirements_20.system_playground.testbenches.path_a.boundary.test_cex_boundary",

    # Add more tests here later:
    # "thought_simulator.requirements_20.system_playground.testbenches.path_a.output.test_cex_output",
    # "thought_simulator.requirements_20.system_playground.testbenches.path_b.context.test_context_engine",
]

# ============================================================
# === RUNNER (DO NOT EDIT BELOW THIS LINE) ====================
# ============================================================

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for module_path in ACTIVE_TEST_MODULES:
        module = __import__(module_path, fromlist=[''])
        suite.addTests(loader.loadTestsFromModule(module))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

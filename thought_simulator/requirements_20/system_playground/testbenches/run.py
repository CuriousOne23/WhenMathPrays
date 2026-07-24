"""
Thought Simulator — Testbench Runner
------------------------------------

Usage:
    To run ONLY the CEx intake + boundary tests:

        1. Uncomment the TWO CEx test lines below.
        2. Comment out any other test imports.
        3. From the repo root, run:

               python thought_simulator/requirements_20/system_playground/testbenches/run.py > cex.log

        Or if you are already inside testbenches:
               python run.py > cex.log

    This will produce a full log of the CEx testbench run in cex.log.

    IMPORTANT:
        - Running from repo root OR from testbenches both work,
          because this script adds the repo root to PYTHONPATH.
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
# === SELECT WHICH TESTBENCHES TO RUN ========================
# ============================================================

# --- CEx Intake Testbench ---
from thought_simulator.requirements_20.system_playground.testbenches.path_a.intake import test_cex_intake

# --- CEx Boundary Testbench ---
# from thought_simulator.requirements_20.system_playground.testbenches.path_a.boundary import test_cex_boundary

# ============================================================
# === RUNNER ==================================================
# ============================================================

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromModule(test_cex_intake))
    suite.addTests(loader.loadTestsFromModule(test_cex_boundary))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

import sys
import os

# Add repo root to Python path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, repo_root)

"""
Thought Simulator — Testbench Runner
------------------------------------

Usage:
    To run ONLY the CEx intake + boundary tests:

        1. Uncomment the TWO CEx test lines below.
        2. Comment out any other test imports.
        3. From the repo root, run:

              IMPORTANT:
                  - You may run this script either from the repo root OR from inside the testbenches directory.
                    In both cases, Python will correctly resolve the `thought_simulator` package.

               python thought_simulator/requirements_20/system_playground/testbenches/run.py > cex.log

               If you are in testbenches:
               python run.py > cexlog

    This will produce a full log of the CEx testbench run in cex.log.

    The runner uses Python's unittest loader so you always know exactly
    which testbench modules are being executed.

    IMPORTANT:
        - Always run from the repo root so Python can see `thought_simulator` as a package.
        - This runner is intentionally simple: edit the imports below to select
          which testbenches you want to execute.
"""

import unittest

# ============================================================
# === SELECT WHICH TESTBENCHES TO RUN ========================
# ============================================================

# --- CEx Intake Testbench (UNCOMMENT TO RUN) ---
from thought_simulator.requirements_20.system_playground.testbenches.path_a.intake import test_cex_intake

# --- CEx Boundary Testbench (UNCOMMENT TO RUN) ---
# from thought_simulator.requirements_20.system_playground.testbenches.path_a.boundary import test_cex_boundary

# ============================================================
# === ADD OTHER TESTBENCHES BELOW (COMMENT OUT AS NEEDED) ====
# ============================================================

# Example:
# from thought_simulator.requirements_20.system_playground.testbenches.path_a.output import test_cex_output
# from thought_simulator.requirements_20.system_playground.testbenches.path_b.context import test_context_engine
# etc.


# ============================================================
# === RUNNER ==================================================
# ============================================================

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add selected test modules
    suite.addTests(loader.loadTestsFromModule(test_cex_intake))
    suite.addTests(loader.loadTestsFromModule(test_cex_boundary))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

"""
Thought Simulator — Testbench Runner
------------------------------------

Process:
    • User selects testbenches by commenting/uncommenting entries
      in ACTIVE_TEST_MODULES.

    • Each testbench receives:
          - mode: "standalone" or "progressive"
          - upstream toggles: use_inb, use_iiinb, use_ie
          - expect_failure: { test_id: True/False }

      This allows per‑test expectation control without modifying YAML.

    • Primitive correctness is enforced inside each testbench.
      Expectation correctness is logged (stdout → redirected to file).

    • Run from repo root:
          python thought_simulator/.../testbenches/run.py > results.log
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
    # IE Intake Envelope Testbench (3‑test mode)
    # --------------------------------------------------------
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
        {
            "mode": "standalone",      # or "progressive"
            "use_inb": False,          # True → include InB upstream
            "use_iiinb": False,        # True → include IIInB upstream
            "use_ie": True,            # IE always runs for IE testbench

            # Per‑test expectations (user controls these)
            "expect_failure": {
                "clean.simple": False,
                "normalize.whitespace": True,
                "normalize.punctuation": False
            }
        }
    ),

    # --------------------------------------------------------
    # Add more testbenches here later
    # --------------------------------------------------------
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

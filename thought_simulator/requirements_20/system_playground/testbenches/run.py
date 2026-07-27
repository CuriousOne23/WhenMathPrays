"""
Thought Simulator — Development Testbench Runner
------------------------------------------------

This runner:
    • Loads selected testbench modules
    • Injects configuration (mode, upstream toggles)
    • Calls each testbench's run_testbench() function directly
    • Does NOT use unittest (development mode)
"""

import sys
import os
import importlib

# ============================================================
# Add repo root to Python path
# ============================================================

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, repo_root)

# ============================================================
# SELECT TESTBENCHES TO RUN (USER EDITS THIS SECTION)
# ============================================================

ACTIVE_TEST_MODULES = [

    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
        {
            # Pipeline mode: "standalone" or "progressive"
            "mode": "standalone",

            # Upstream toggles: User inputs True or False
            "use_inb": False,
            "use_iiinb": False,
            "use_ie": True
        }
    ),

    # Add more testbenches here later
]

# ============================================================
# RUNNER (NO unittest)
# ============================================================

if __name__ == "__main__":

    for module_path, config in ACTIVE_TEST_MODULES:

        print("\n============================================================")
        print("Running Testbench Module:")
        print("  {}".format(module_path))
        print("============================================================\n")

        module = importlib.import_module(module_path)

        # Inject configuration
        if hasattr(module, "set_testbench_config"):
            module.set_testbench_config(config)

        # Call development-mode runner
        if hasattr(module, "run_testbench"):
            module.run_testbench()
        else:
            print("ERROR: Module {} does not define run_testbench()".format(module_path))

"""
Thought Simulator — Development Testbench Runner
------------------------------------------------

This runner:
    • Loads selected testbench modules
    • Injects configuration (upstream toggles, tests_to_run)
    • Calls each testbench's run_testbench() function directly
    • Does NOT use unittest (development mode)
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
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

    # **************************** InB Test bench ****************************************************
    # Highest upstream True = InB (primitive under test)
    # Pipeline: InB only, input from InB YAML
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_testbench",
    #     {
    #         "mode": "general",   # or "general" or "testbench"
    #         "use_inb": True,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "tests_to_run": "see inb_tests_to_run.yaml"
    #     }
    # ),
    # **************************** IIInB Test bench ****************************************************
    # Highest upstream True = IIInB (primitive under test)
    # Pipeline: IIInB only, input from IIInB YAML
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.iiinb_testbench",
        {
            "mode": "testbench",   # or "general"
            "use_inb": False,      # Upstream InB ignored
            "use_iiinb": True,     # Primitive under test
            "use_ie": False,       # Downstream IE ignored
    
            # Test selection is now controlled by iiinb_tests_to_run.yaml
            "tests_to_run": "see iiinb_tests_to_run.yaml"
        }
    ),
    # **************************** IE Test bench ******************************************************
    # Highest upstream True = IE (primitive under test)
    # Pipeline: IE only, input from IE YAML
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
    #     {
    #         "use_inb": False,
    #         "use_iiinb": True,
    #         "use_ie": True,
    #         "tests_to_run": {
    #             "ie_repair_only_whitespace": "Yes",
    #             "ie_multiple_repairs": "Yes",
    #             "ie_anomaly_only": "Yes",
    #             "ie_mixed_repairs_anomaly": "Yes",
    #             "ie_structural_tags": "Yes",
    #             "ie_token_preservation": "Yes",
    #             "ie_replay_determinism": "Yes",
    #             "ie_complex_mixed": "Yes"
    #         }
    #     }
    # )
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

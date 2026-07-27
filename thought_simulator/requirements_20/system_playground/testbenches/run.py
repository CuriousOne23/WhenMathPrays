"""
Thought Simulator — Development Testbench Runner
------------------------------------------------

This runner:
    • Loads selected testbench modules
    • Injects configuration (mode, upstream toggles, tests_to_run, user_expects_failure)
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
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_testbench",
    #     {
    #         "mode": "standalone",
    #         "use_inb": True,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "tests_to_run": {
    #             "inb_baseline_no_error": "Yes",
    #             "inb_whitespace_anomaly": "Yes",
    #             "inb_multiple_surface_anomalies": "Yes",
    #             "inb_illegal_character_only": "Yes",
    #             "inb_mixed_whitespace_illegal": "Yes",
    #             "inb_structural_tags_present": "Yes",
    #             "inb_tokenizable_input": "Yes",
    #             "inb_unicode_normalization_opportunity": "Yes",
    #             "inb_complex_mixed_case": "Yes"
    #         }
    #     }
    # ),
    
    # **************************** IIInB Test bench ****************************************************
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.iiinb_testbench",
        {
            # Pipeline mode: "standalone" or "progressive"
            "mode": "standalone",

            # Upstream toggles: User inputs True or False
            "use_inb": False,
            "use_iiinb": True,
            "use_ie": False,

            "tests_to_run": {
                "clean.simple": "Yes",
                "unicode.noise": "Yes",
                "structural.break": "Yes",
                "empty.input": "Yes",
                "long.input": "Yes",
                "repeating.letters": "Yes",
                "shorthand.plz": "Yes",
                "misspelling.transposition": "Yes",
                "misspelling.missing": "Yes",
                "multi.repairs.surface": "Yes",
                "multi.anomalies.illegal": "Yes",
                "mixed.repairs.anomalies": "Yes",
                "structural.surface.mixed": "Yes",
                "token.preservation": "Yes",
                "replay.determinism": "Yes"
            }
        }
    ),

    # **************************** IE Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
    #     {
    #         "mode": "standalone",
    #         "use_inb": False,
    #         "use_iiinb": False,
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

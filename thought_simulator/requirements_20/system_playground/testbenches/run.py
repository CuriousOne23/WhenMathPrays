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
import io
sys.stdout.reconfigure(encoding='utf-8')
import os
import importlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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
    #         "mode": "general",
    #         "use_inb": True,
    #         "tests_to_run": "see inb_tests_to_run.yaml"
    #     }
    # ),
    # **************************** IIInB / IE / CEx / CE / TPU / SOB / ... (commented) **************
    # **************************** STPX / RBU ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.structure.rbu_testbench",
    #     {"mode": "testbench", "use_rbu": True, "tests_to_run": "see rbu_tests_to_run.yaml"}
    # ),
    # **************************** DCB Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.dcb_testbench",
    #     {
    #         "mode": "testbench",
    #         "use_dcb": True,
    #         "tests_to_run": "see dcb_tests_to_run.yaml",
    #     }
    # ),
    # **************************** RB Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.rb_testbench",
    #     {
    #         "mode": "testbench",
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": False,
    #         "use_cex_pck": False,
    #         "use_ce": False,
    #         "use_tpu": False,
    #         "use_sob": False,
    #         "use_srob": False,
    #         "use_cnob": False,
    #         "use_smob": False,
    #         "use_wrdnm": False,
    #         "use_isc": False,
    #         "use_ssg": False,
    #         "use_stpx": False,
    #         "use_rbu": False,
    #         "use_dcb": False,
    #         "use_rb": True,
    #         "tests_to_run": "see rb_tests_to_run.yaml",
    #     }
    # ),
    # **************************** TR Test bench ******************************************************
    # Highest upstream True = TR (primitive under test)
    # Pipeline position: Path-A meaning-layer routing-vector constructor (before CTP / RTU / RB)
    # Input from:
    #   • tr_testbench.yaml (mode = "testbench")
    #   • tr_input.yaml (mode = "general")
    # Location: path_a/routing/
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.tr_testbench",
        {
            "mode": "testbench",     # "general" or "testbench"
            "use_inb": False,
            "use_iiinb": False,
            "use_ie": False,
            "use_cex_ie": False,
            "use_cex_ccr": False,
            "use_cex_pck": False,
            "use_ce": False,
            "use_tpu": False,
            "use_sob": False,
            "use_srob": False,
            "use_cnob": False,
            "use_smob": False,
            "use_wrdnm": False,
            "use_isc": False,
            "use_ssg": False,
            "use_stpx": False,
            "use_rbu": False,
            "use_dcb": False,
            "use_rb": False,
            "use_tr": True,          # Primitive under test
            "tests_to_run": "see tr_tests_to_run.yaml",
        }
    ),
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

        if hasattr(module, "set_testbench_config"):
            module.set_testbench_config(config)

        if hasattr(module, "run_testbench"):
            module.run_testbench()
        else:
            print("ERROR: Module {} does not define run_testbench()".format(module_path))

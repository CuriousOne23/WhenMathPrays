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
    # Highest upstream True = InB (primitive under test)
    # Pipeline: InB only, input from InB YAML
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.inb_testbench",
    #     {
    #         "mode": "general",   # "general" or "testbench"
    #         "use_inb": True,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "tests_to_run": "see inb_tests_to_run.yaml"
    #     }
    # ),
    # **************************** IIInB Test bench ****************************************************
    # Highest upstream True = IIInB (primitive under test)
    # Pipeline: IIInB only, input from IIInB YAML
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.iiinb_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_inb": False,      # Upstream InB ignored
    #         "use_iiinb": True,     # Primitive under test
    #         "use_ie": False,       # Downstream IE ignored
    
    #         # Test selection is now controlled by iiinb_tests_to_run.yaml
    #         "tests_to_run": "see iiinb_tests_to_run.yaml"
    #     }
    # ),
    # **************************** IE Test bench ******************************************************
    # Highest upstream True = IE (primitive under test)
    # Pipeline: IE only, input from IE YAML
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
    #     {
    #         "mode": "testbench",   # "general" or "testbench"
    #         "use_inb": False,      # Upstream InB ignored
    #         "use_iiinb": False,    # If True then Synthetic IIInB input from ie_input.yaml
    #         "use_ie": True,        # Primitive under test

    #         # Test selection is now controlled by ie_tests_to_run.yaml
    #         "tests_to_run": "see ie_tests_to_run.yaml"
    #     }
    # ),
    # **************************** CEx-IE Test bench ******************************************************
    # Highest upstream True = CEx-IE (primitive under test)
    # Pipeline: CEx-IE only, input from CEx-IE YAML
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.cex_ie_testbench",
    #     {
    #         "mode": "testbench",   # "general" or "testbench"
    #         "use_inb": False,    # Upstream primitives ignored
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": True,  # Primitive under test

    #         # Test selection is controlled by cex_ie_input.yaml
    #         "tests_to_run": "see cex_ie_tests_to_run.yaml"
    #     }
    # ),
    # **************************** CEx-CCR Test bench ******************************************************
    # Highest upstream True = CEx-CCR (primitive under test)
    # Pipeline: CEx-CCR only, input from:
    #   • cex_ccr_testbench.yaml (scenarios)
    #   • cil_input.yaml (static 10-conversation CIL substrate)
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.cex_ccr_testbench",
    #     {
    #         "mode": "testbench",     # general or testbench, chooses cex_ccr_input.yam. or cex_ccr_testbench.yaml
    #         "use_inb": False,        # Upstream primitives ignored
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": True,     # Primitive under test

    #         # Test selection controlled by cex_ccr_tests_to_run.yaml
    #         "tests_to_run": "see cex_ccr_tests_to_run.yaml",

    #         # CCR always uses static cil_input.yaml
    #         "cil_source": "cil_input.yaml"
    #     }
    # ),
    # **************************** CEx‑Pck Test bench ******************************************************
    # Highest upstream True = CEx‑Pck (primitive under test)
    # Pipeline: CEx‑Pck only, input from:
    #   • cex_pck_testbench.yaml (scenarios)
    #   • cil_input.yaml (static 10‑conversation CIL substrate)
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.cex_pck_testbench",
    #     {
    #         "mode": "testbench",     # general or testbench, chooses cex_pck_input.yaml or cex_pck_testbench.yaml
    #         "use_inb": False,        # Upstream primitives ignored
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": False,    # CCR is NOT under test here
    #         "use_cex_pck": True,     # Primitive under test

    #         # Test selection controlled by cex_pck_tests_to_run.yaml
    #         "tests_to_run": "see cex_pck_tests_to_run.yaml",

    #         # Pck always uses static cil_input.yaml
    #         "cil_source": "cil_input.yaml"
    #     }
    # ),
    # **************************** CE Test bench ******************************************************
    # Highest upstream True = CE (primitive under test)
    # Pipeline: CE only, input from:
    #   • ce_testbench.yaml (mode = "testbench")
    #   • ce_input.yaml (mode = "general")
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.ce_testbench",
    #     {
    #         "mode": "testbench",     # general or testbench
    #         "use_inb": False,        # Upstream primitives ignored
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": False,    
    #         "use_cex_pck": False,     
    #         "use_ce": True,     # Primitive under test

    #         # Test selection controlled by cex_pck_tests_to_run.yaml
    #         "tests_to_run": "see ce_tests_to_run.yaml",
    #     }
    # ),
    # **************************** TPU Test bench ******************************************************
    # Highest upstream True = TPU (primitive under test)
    # Pipeline: TPU only (or progressive from CE if desired), input from:
    #   • tpu_testbench.yaml (mode = "testbench")
    #   • tpu_input.yaml (mode = "general")
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.transform.tpu_testbench",
    #     {
    #         "mode": "general",     # "general" or "testbench"
    #         "use_inb": False,        # Upstream primitives ignored
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": False,
    #         "use_cex_pck": False,
    #         "use_ce": False,         # Set to True if you want progressive CE → TPU
    #         "use_tpu": True,         # Primitive under test

    #         # Test selection controlled by tpu_tests_to_run.yaml
    #         "tests_to_run": "see tpu_tests_to_run.yaml",
    #     }
    # ),
    # **************************** SOB Test bench ******************************************************
    # Highest upstream True = SOB (primitive under test)
    # Pipeline: SOB only (or progressive from TPU if desired), input from:
    #   • sob_testbench.yaml (mode = "testbench")
    #   • sob_input.yaml (mode = "general")
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.sob_testbench",
        {
            "mode": "testbench",     # "general" or "testbench"
            "use_inb": False,        # Upstream primitives ignored
            "use_iiinb": False,
            "use_ie": False,
            "use_cex_ie": False,
            "use_cex_ccr": False,
            "use_cex_pck": False,
            "use_ce": False,
            "use_tpu": False,        # Set to True if you want progressive TPU → SOB
            "use_sob": True,         # Primitive under test

            # Test selection controlled by sob_tests_to_run.yaml
            "tests_to_run": "see sob_tests_to_run.yaml",
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

        # Inject configuration
        if hasattr(module, "set_testbench_config"):
            module.set_testbench_config(config)

        # Call development-mode runner
        if hasattr(module, "run_testbench"):
            module.run_testbench()
        else:
            print("ERROR: Module {} does not define run_testbench()".format(module_path))

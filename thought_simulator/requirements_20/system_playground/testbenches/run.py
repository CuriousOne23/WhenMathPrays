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
    #         "mode": "general",     # "general" or "testbench"
    #         "use_inb": True,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "tests_to_run": "see inb_tests_to_run.yaml"
    #     }
    # ),
    # **************************** IIInB Test bench ****************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.iiinb_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_inb": False,
    #         "use_iiinb": True,
    #         "use_ie": False,
    #         "tests_to_run": "see iiinb_tests_to_run.yaml"
    #     }
    # ),
    # **************************** IE Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.intake.ie_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": True,
    #         "tests_to_run": "see ie_tests_to_run.yaml"
    #     }
    # ),
    # **************************** CEx-IE Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.cex_ie_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": True,
    #         "tests_to_run": "see cex_ie_tests_to_run.yaml"
    #     }
    # ),
    # **************************** CEx-CCR Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.cex_ccr_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": True,
    #         "tests_to_run": "see cex_ccr_tests_to_run.yaml",
    #         "cil_source": "cil_input.yaml"
    #     }
    # ),
    # **************************** CEx‑Pck Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.cex_pck_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": False,
    #         "use_cex_pck": True,
    #         "tests_to_run": "see cex_pck_tests_to_run.yaml",
    #         "cil_source": "cil_input.yaml"
    #     }
    # ),
    # **************************** CE Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.ce_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": False,
    #         "use_cex_pck": False,
    #         "use_ce": True,
    #         "tests_to_run": "see ce_tests_to_run.yaml",
    #     }
    # ),
    # **************************** TPU Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.transform.tpu_testbench",
    #     {
    #         "mode": "general",     # "general" or "testbench"
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": False,
    #         "use_cex_pck": False,
    #         "use_ce": False,
    #         "use_tpu": True,
    #         "tests_to_run": "see tpu_tests_to_run.yaml",
    #     }
    # ),
    # **************************** SOB Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.sob_testbench",
    #     {
    #         "mode": "general",     # "general" or "testbench"
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": False,
    #         "use_cex_pck": False,
    #         "use_ce": False,
    #         "use_tpu": False,
    #         "use_sob": True,
    #         "tests_to_run": "see sob_tests_to_run.yaml",
    #     }
    # ),
    # **************************** SROB Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.srob_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_inb": False,
    #         "use_iiinb": False,
    #         "use_ie": False,
    #         "use_cex_ie": False,
    #         "use_cex_ccr": False,
    #         "use_cex_pck": False,
    #         "use_ce": False,
    #         "use_tpu": False,
    #         "use_sob": False,
    #         "use_srob": True,
    #         "tests_to_run": "see srob_tests_to_run.yaml",
    #     }
    # ),
    # **************************** CnOB Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.cnob_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
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
    #         "use_cnob": True,
    #         "tests_to_run": "see cnob_tests_to_run.yaml",
    #     }
    # ),
    # **************************** SmOB Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.smob_testbench",
    #     {
    #         "mode": "general",     # "general" or "testbench"
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
    #         "use_smob": True,
    #         "tests_to_run": "see smob_tests_to_run.yaml",
    #     }
    # ),
    # **************************** WrdNm Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.encoder.wrdnm_testbench",
    #     {
    #         "mode": "testbench",
    #         "use_wrdnm": True,
    #         "tests_to_run": "see wrdnm_tests_to_run.yaml",
    #     }
    # ),
    # **************************** ISc Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.isc_testbench",
    #     {
    #         "mode": "testbench",
    #         "use_isc": True,
    #         "tests_to_run": "see isc_tests_to_run.yaml",
    #     }
    # ),
    # **************************** SSG Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.structure.ssg_testbench",
    #     {
    #         "mode": "testbench",
    #         "use_ssg": True,
    #         "tests_to_run": "see ssg_tests_to_run.yaml",
    #     }
    # ),
    # **************************** STPX Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.structure.stpx_testbench",
    #     {
    #         "mode": "testbench",
    #         "use_stpx": True,
    #         "tests_to_run": "see stpx_tests_to_run.yaml",
    #     }
    # ),
    # **************************** RBU Test bench ******************************************************
    # Highest upstream True = RBU (primitive under test)
    # Pipeline position: after IdOB (meaning-side commit)
    # Location: path_a/structure/
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.structure.rbu_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
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
    #         "use_rbu": True,         # Primitive under test
    #         "tests_to_run": "see rbu_tests_to_run.yaml",
    #     }
    # ),
    # **************************** DCB Test bench ******************************************************
    # Highest upstream True = DCB (primitive under test)
    # Pipeline position: after RBU (execution-flow geometric_state / history / events)
    # Input from:
    #   • dcb_testbench.yaml (mode = "testbench")
    #   • dcb_input.yaml (mode = "general")
    # Location: path_a/routing/
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.dcb_testbench",
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
            "use_dcb": True,         # Primitive under test
            "tests_to_run": "see dcb_tests_to_run.yaml",
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

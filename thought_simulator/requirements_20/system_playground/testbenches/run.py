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
    # Highest upstream True = WrdNm (primitive under test)
    # Pipeline: WrdNm only (structured TP fields → numeric vector), input from:
    #   • wrdnm_testbench.yaml (mode = "testbench")
    #   • wrdnm_input.yaml (mode = "general")
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.encoder.wrdnm_testbench",
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
    #         "use_wrdnm": True,       # Primitive under test
    #         "tests_to_run": "see wrdnm_tests_to_run.yaml",
    #     }
    # ),
    # **************************** ISc Test bench ******************************************************
    # Highest upstream True = ISc (primitive under test)
    # Pipeline position: after WrdNm (CE candidate_set + optional wrdnm vectors → scores)
    # Input from:
    #   • isc_testbench.yaml (mode = "testbench")
    #   • isc_input.yaml (mode = "general")
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.isc_testbench",
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
    #         "use_wrdnm": False,      # Set True later for progressive WrdNm → ISc
    #         "use_isc": True,         # Primitive under test
    #         "tests_to_run": "see isc_tests_to_run.yaml",
    #     }
    # ),
    # **************************** SSG Test bench ******************************************************
    # Highest upstream True = SSG (primitive under test)
    # Pipeline position: after SmOB (structural graph → fixed-length structural signature)
    # Input from:
    #   • ssg_testbench.yaml (mode = "testbench")
    #   • ssg_input.yaml (mode = "general")
    # Location: path_a/structure/
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.structure.ssg_testbench",
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
    #         "use_ssg": True,         # Primitive under test
    #         "tests_to_run": "see ssg_tests_to_run.yaml",
    #     }
    # ),
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
    #         "use_rb": True,
    #         "tests_to_run": "see rb_tests_to_run.yaml",
    #     }
    # ),
    # **************************** TR Test bench ******************************************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.tr_testbench",
    #     {
    #         "mode": "testbench",
    #         "use_tr": True,
    #         "tests_to_run": "see tr_tests_to_run.yaml",
    #     }
    # ),
    # **************************** CTP Test bench (previously active) *********************************
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.routing.ctp_testbench",
    #     {
    #         "mode": "testbench",
    #         "use_ctp": True,
    #         "tests_to_run": "see ctp_tests_to_run.yaml",
    #     }
    # ),
    # **************************** IdOB Test bench (previously active) ********************************
    # Category: path_a/identity/
    # Dual-mode: testbench (idob_testbench.yaml) | general (idob_input.yaml + rules)
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.identity.idob_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_idob": True,        # Primitive under test
    #         "tests_to_run": "see idob_tests_to_run.yaml",
    #     }
    # ),
    # **************************** MCB Test bench (previously active) *********************************
    # Category: path_a/identity/
    # Dual-mode: testbench (mcb_testbench.yaml) | general (mcb_input.yaml + rules)
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.identity.mcb_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_mcb": True,         # Primitive under test
    #         "tests_to_run": "see mcb_tests_to_run.yaml",
    #     }
    # ),
    # **************************** OuBA Test bench (previously active) ********************************
    # Category: path_a/output/
    # Dual-mode: testbench (ouba_testbench.yaml) | general (ouba_input.yaml + rules)
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.output.ouba_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_ouba": True,         # Primitive under test
    #         "tests_to_run": "see ouba_tests_to_run.yaml",
    #     }
    # ),

    # **************************** COB Test bench (previously active) *********************************
    # Category: path_a/context/
    # Dual-mode: testbench (cob_testbench.yaml) | general (cob_input.yaml + rules)
    # Normative: 20.32, cob_requirements.md, cob_py_struc_pgm.md, patha_field_names.md
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cob_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_cob": True,          # Primitive under test
    #         "tests_to_run": "see cob_tests_to_run.yaml",
    #     }
    # ),

    # **************************** CIL Test bench (previously active) *********************************
    # Category: path_a/context/
    # Dual-mode: testbench (cil_testbench.yaml) | general (cil_input.yaml + rules)
    # Slice: identity_selection (cil_testbench_schema.md v0.1)
    # Normative: 20.33, cil_requirements.md, cil_py_struc_pgm.md, patha_field_names.md
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cil_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_cil": True,          # Primitive under test
    #         "tests_to_run": "see cil_tests_to_run.yaml",
    #     }
    # ),

    # **************************** CST-Core Test bench (previously active) *****************************
    # Category: path_a/context/
    # Dual-mode: testbench (cst_core_testbench.yaml) | general (cst_core_input.yaml + rules)
    # Normative: 20.32.010.010, cst_core_py_struc_pgm.md, patha_field_names.md (TP.cst.core)
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cst_core_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_cst_core": True,     # Primitive under test
    #         "tests_to_run": "see cst_core_tests_to_run.yaml",
    #     }
    # ),

    # **************************** CST-MS Test bench (ACTIVE) ******************************************
    # Category: path_a/context/
    # Dual-mode: testbench (cst_ms_testbench.yaml) | general (cst_ms_input.yaml + rules)
    # Normative: 20.32.010.020, cst_ms_py_struc_pgm.md, patha_field_names.md (TP.cst.ms)
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cst_ms_testbench",
        {
            "mode": "testbench",     # "general" or "testbench"
            "use_cst_ms": True,       # Primitive under test
            "tests_to_run": "see cst_ms_tests_to_run.yaml",
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

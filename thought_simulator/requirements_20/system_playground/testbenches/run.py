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

    # **************************** COB Test bench (ACTIVE) ********************************************
    # Category: path_a/context/
    # Dual-mode: testbench (cob_testbench.yaml) | general (cob_input.yaml + rules)
    # Normative: 20.32, cob_requirements.md, cob_py_struc_pgm.md, patha_field_names.md
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cob_testbench",
        {
            "mode": "testbench",     # "general" or "testbench"
            "use_cob": True,          # Primitive under test
            "tests_to_run": "see cob_tests_to_run.yaml",
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

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

    # **************************** InB / IIInB / IE / CEx / CE / ... (commented) **************
    # **************************** IdOB / MCB / OuBA (commented) ******************************

    # **************************** COB Test bench (commented) *********************************
    # Category: path_a/context/
    # Dual-mode: testbench (cob_testbench.yaml) | general (cob_input.yaml + rules)
    # Normative: 20.32, cob_requirements.md, cob_py_struc_pgm.md, patha_field_names.md
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cob_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_cob": True,
    #         "tests_to_run": "see cob_tests_to_run.yaml",
    #     }
    # ),

    # **************************** CIL Test bench (commented) *********************************
    # Category: path_a/context/
    # Dual-mode: testbench (cil_testbench.yaml) | general (cil_input.yaml + rules)
    # Slice: identity_selection (cil_testbench_schema.md v0.1)
    # Normative: 20.33, cil_requirements.md, cil_py_struc_pgm.md, patha_field_names.md
    # (
    #     "thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cil_testbench",
    #     {
    #         "mode": "testbench",     # "general" or "testbench"
    #         "use_cil": True,
    #         "tests_to_run": "see cil_tests_to_run.yaml",
    #     }
    # ),

    # **************************** CST-Core Test bench (ACTIVE) *******************************
    # Category: path_a/context/
    # Dual-mode: testbench (cst_core_testbench.yaml) | general (cst_core_input.yaml + rules)
    # Normative: 20.32.010.010, cst_core_py_struc_pgm.md, patha_field_names.md (TP.cst.core)
    (
        "thought_simulator.requirements_20.system_playground.testbenches.path_a.context.cst_core_testbench",
        {
            "mode": "testbench",     # "general" or "testbench"
            "use_cst_core": True,
            "tests_to_run": "see cst_core_tests_to_run.yaml",
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

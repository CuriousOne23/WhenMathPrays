"""
CEx-Pck Testbench (Deterministic)
---------------------------------
This module loads:
  - cex_pck_input.yaml   (general mode)
  - cex_pck_testbench.yaml (testbench mode)
  - cex_pck_rules.yaml
  - cex_pck_tests_to_run.yaml

It executes:
  - CEx-Pck (via cex_pck.py)
  - Rulechecker (cex_pck_rulechecker.py)

It compares:
  - TP output against expected fields in cex_pck_testbench.yaml (testbench mode)
  - TP output against expected fields in cex_pck_testbench.yaml (general mode)

This file is invoked by testbenches/run.py.
"""

import os
import json
import yaml
import subprocess
from typing import Any, Dict

# ============================================================
# Configuration injected by run.py
# ============================================================

TESTBENCH_CONFIG = {
    "mode": "general"   # default
}

def set_testbench_config(config: Dict[str, Any]):
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config


# ============================================================
# Paths
# ============================================================

ROOT = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(ROOT, "cex_pck_input.yaml")
RULES_PATH = os.path.join(ROOT, "cex_pck_rules.yaml")
TESTS_PATH = os.path.join(ROOT, "cex_pck_tests_to_run.yaml")
TESTBENCH_PATH = os.path.join(ROOT, "cex_pck_testbench.yaml")
RULECHECKER_PATH = os.path.join(ROOT, "cex_pck_rulechecker.py")

# Primitive implementation
CEX_PCK_IMPL = os.path.join(
    ROOT,
    "../../../primitives/cex_pck/cex_pck.py"
)


# ============================================================
# YAML Loader
# ============================================================

def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ============================================================
# Run CEx-Pck
# ============================================================

def run_cex_pck(tp_input: Dict[str, Any]) -> Dict[str, Any]:
    import importlib.util

    spec = importlib.util.spec_from_file_location("cex_pck", CEX_PCK_IMPL)
    cex_pck_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cex_pck_module)

    CExPck = cex_pck_module.CExPck
    pck = CExPck(tp_input)
    pck.inspect()

    return pck.tp


# ============================================================
# Rulechecker
# ============================================================

def run_rulechecker(tp_before: Dict[str, Any], tp_after: Dict[str, Any]) -> bool:
    before_path = os.path.join(ROOT, "_tp_before.json")
    after_path = os.path.join(ROOT, "_tp_after.json")

    with open(before_path, "w", encoding="utf-8") as f:
        json.dump(tp_before, f, indent=2)

    with open(after_path, "w", encoding="utf-8") as f:
        json.dump(tp_after, f, indent=2)

    rules = load_yaml(RULES_PATH)
    rules_json_path = os.path.join(ROOT, "_rules_tmp.json")

    with open(rules_json_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2)

    import sys
    cmd = [
        sys.executable,
        RULECHECKER_PATH,
        rules_json_path,
        before_path,
        after_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode == 0


# ============================================================
# Expected Output Comparison
# ============================================================

def compare_expected(tp_after: Dict[str, Any], expected: Dict[str, Any]) -> bool:
    def get_nested(d: Dict[str, Any], path: str):
        cur = d
        for part in path.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                return None
        return cur

    ok = True
    for field_path, expected_value in expected.items():
        actual = get_nested(tp_after, field_path)
        if actual != expected_value:
            print(f"[Mismatch] {field_path}: expected={expected_value!r}, got={actual!r}")
            ok = False

    return ok


# ============================================================
# Main Testbench Runner
# ============================================================

def run_testbench():

    # Load tests_to_run
    tests = load_yaml(TESTS_PATH)["tests_to_run"]

    # Determine mode
    mode = TESTBENCH_CONFIG.get("mode", "general")

    # Load expected always from testbench YAML
    tb_yaml = load_yaml(TESTBENCH_PATH)
    tb_expected = tb_yaml["expected"]

    for test in tests:
        if not test.get("active", False):
            continue

        print(f"\n=== Running Test: {test['id']} ===")
        print(f"Description: {test['description']}")

        # ------------------------------------------------------------
        # Select input source based on mode
        # ------------------------------------------------------------
        if mode == "testbench":
            tp_input = tb_yaml["input"]
            expected = tb_expected
            input_source_name = "cex_pck_testbench.yaml"
        else:
            tp_input = load_yaml(INPUT_PATH)
            expected = tb_expected
            input_source_name = "cex_pck_input.yaml"

        tp_before = json.loads(json.dumps(tp_input))  # deep copy

        # ------------------------------------------------------------
        # Run primitive
        # ------------------------------------------------------------
        tp_after = run_cex_pck(tp_input)

        # ------------------------------------------------------------
        # Rulecheck
        # ------------------------------------------------------------
        print("\n--- Rulecheck ---")
        rulecheck_passed = run_rulechecker(tp_before, tp_after)

        # ------------------------------------------------------------
        # Expected comparison
        # ------------------------------------------------------------
        print("\n--- Expected Output Comparison ---")
        expected_passed = compare_expected(tp_after, expected)

        # ------------------------------------------------------------
        # Summary
        # ------------------------------------------------------------
        print("\n=== Test Summary ===")
        print(f"Test ID: {test['id']}")
        print(f"Description: {test['description']}")

        print("\nRuleChecker:")
        print(f"  Input: {input_source_name}")
        print("  Output Check: by cex_pck_rules.yaml and cex_pck_rulechecker.py")
        print(f"  Result: {'PASSED' if rulecheck_passed else 'FAILED'}")

        print("\nComparison:")
        print(f"  Input: {input_source_name}")
        print("  Output Check: agrees with cex_pck_testbench.yaml Expected Output")
        print(f"  Result: {'PASSED' if expected_passed else 'FAILED'}")

        if rulecheck_passed and expected_passed:
            print("\nOverall: SUCCESS - TP is valid and correct.\n")
        else:
            print("\nOverall: FAILURE - see details above.\n")
            return False

    return True


# ============================================================
# Entrypoint
# ============================================================

if __name__ == "__main__":
    success = run_testbench()
    if success:
        print("All active CEx-Pck tests PASSED.")
    else:
        print("One or more CEx-Pck tests FAILED.")

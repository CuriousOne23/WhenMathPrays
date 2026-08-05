"""
cex_ie_testbench.py
Testbench harness for the CEx-IE primitive.

Supports:
- Mode A (testbench): strict deterministic equality
- Mode B (general): rule-driven validation

Inputs:
- cex_ie_testbench.yaml  (mode A)
- cex_ie_input.yaml       (mode B)
- cex_ie_rules.yaml       (mode B)
- cex_ie_rulechecker.py   (mode B)

This file is invoked by run.py.
"""

import yaml
import copy
from pathlib import Path

# Import the primitive and rulechecker
from thought_simulator.requirements_20.system_playground.primitives.cex_ie.cex_ie import CExIE
from thought_simulator.requirements_20.system_playground.testbenches.path_a.semantic.cex_ie_rulechecker import (
    run_cex_ie_rulecheck
)

BASE_DIR = Path(__file__).parent

# ------------------------------------------------------------
# Utility: load YAML
# ------------------------------------------------------------
def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ------------------------------------------------------------
# Utility: load tests-to-run YAML and filter test list
# ------------------------------------------------------------
def filter_tests_by_selector(all_tests: list, selector_path: str) -> list:
    """
    all_tests: list of test cases from cex_ie_input.yaml or cex_ie_testbench.yaml
    selector_path: path to cex_ie_tests_to_run.yaml
    Returns: filtered list of tests based on enabled flags
    """
    selector = load_yaml(selector_path)
    enabled_map = {}

    for entry in selector.get("tests_to_run", []):
        tid = entry.get("id")
        enabled = entry.get("enabled", False)
        enabled_map[tid] = enabled

    filtered = []
    for case in all_tests:
        cid = case.get("id")
        if enabled_map.get(cid, False):
            filtered.append(case)

    return filtered

# ------------------------------------------------------------
# Mode A — strict deterministic testbench
# ------------------------------------------------------------
def run_mode_testbench(testbench_path: str) -> dict:
    tb = load_yaml(testbench_path)
    tests = filter_tests_by_selector(
        tb.get("tests", []),
        str(Path(testbench_path).parent / "cex_ie_tests_to_run.yaml")
    )

    results = {"pass": True, "cases": []}

    print("\n=== CEx-IE Testbench (Deterministic Mode) ===")

    for case in tests:
        cid = case.get("id")
        tp_input = case.get("input")
        expected = case.get("expected")

        primitive = CExIE(tp_input["TP"])
        tp_output = {"TP": copy.deepcopy(tp_input["TP"])}
        tp_output["TP"]["cex"] = {}
        tp_output["TP"]["cex"]["ie"] = primitive.inspect()["cex"]["ie"]

        actual = tp_output["TP"]["cex"]["ie"]
        exp = expected["TP"]["cex"]["ie"]

        case_pass = (actual == exp)

        if case_pass:
            print(f"[PASS] {cid} — output matched expected structure")
        else:
            print(f"[FAIL] {cid}")
            print(f"  reason: output did not match expected")
            print(f"  actual:   {actual}")
            print(f"  expected: {exp}")

            results["pass"] = False

        results["cases"].append({
            "id": cid,
            "pass": case_pass,
            "actual": actual,
            "expected": exp
        })

    print("\n=== Summary ===")
    total = len(results["cases"])
    passed = sum(1 for c in results["cases"] if c["pass"])
    print(f"  total: {total}")
    print(f"  passed: {passed}")
    print(f"  failed: {total - passed}")
    print(f"  overall: {'PASS' if results['pass'] else 'FAIL'}\n")

    return results

# ------------------------------------------------------------
# Mode B — general rule-driven validation
# ------------------------------------------------------------
def run_mode_general(input_path: str, rules_path: str) -> dict:
    inp = load_yaml(input_path)
    
    tests = filter_tests_by_selector(
        inp.get("tests", []),
        str(Path(input_path).parent / "cex_ie_tests_to_run.yaml")
    )

    results = {"pass": True, "cases": []}

    print("\n=== CEx-IE Testbench (Rule-Driven Mode) ===")

    for case in tests:
        cid = case.get("id")
        tp_input = case.get("TP")

        primitive = CExIE(tp_input)
        tp_output = {"TP": copy.deepcopy(tp_input)}
        tp_output["TP"]["cex"] = {}
        tp_output["TP"]["cex"]["ie"] = primitive.inspect()["cex"]["ie"]

        rc_result = run_cex_ie_rulecheck(rules_path, {"TP": tp_input}, tp_output)

        if rc_result["pass"]:
            print(f"[PASS] {cid} — rulechecker accepted output")
        else:
            print(f"[FAIL] {cid}")
            print("  reason: rulechecker rejected output")
            for err in rc_result["errors"]:
                print(f"   - {err}")

            results["pass"] = False

        results["cases"].append({
            "id": cid,
            "pass": rc_result["pass"],
            "errors": rc_result["errors"],
            "output": tp_output["TP"]["cex"]["ie"]
        })

    print("\n=== Summary ===")
    total = len(results["cases"])
    passed = sum(1 for c in results["cases"] if c["pass"])
    print(f"  total: {total}")
    print(f"  passed: {passed}")
    print(f"  failed: {total - passed}")
    print(f"  overall: {'PASS' if results['pass'] else 'FAIL'}\n")

    return results

# ------------------------------------------------------------
# Entry point used by run.py
# ------------------------------------------------------------
def run_cex_ie_testbench(mode: str,
                         testbench_path: str,
                         input_path: str,
                         rules_path: str) -> dict:
    """
    mode: "testbench" or "general"
    testbench_path: path to cex_ie_testbench.yaml
    input_path: path to cex_ie_input.yaml
    rules_path: path to cex_ie_rules.yaml
    """

    if mode == "testbench":
        return run_mode_testbench(testbench_path)

    elif mode == "general":
        return run_mode_general(input_path, rules_path)

    else:
        return {
            "pass": False,
            "error": f"Unknown mode: {mode}"
        }

# ------------------------------------------------------------
# Standard entry point expected by run.py
# ------------------------------------------------------------
def run_testbench():
    mode = "testbench"

    testbench_path = BASE_DIR / "cex_ie_testbench.yaml"
    input_path     = BASE_DIR / "cex_ie_input.yaml"
    rules_path     = BASE_DIR / "cex_ie_rules.yaml"

    return run_cex_ie_testbench(mode,
                                str(testbench_path),
                                str(input_path),
                                str(rules_path))

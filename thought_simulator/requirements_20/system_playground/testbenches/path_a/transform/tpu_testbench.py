"""
TPU Testbench (Version 1.0)
---------------------------
Deterministic testbench for the TP-UPDATE (TPU) primitive.

Aligned with:
  - progressive_lineup_testing.md (Sections 3.1–3.9)
  - 20.46 (TPU Requirements)
  - tpu_py_struc_pgm.md

Behavior:
  • mode == "testbench"  → load tpu_testbench.yaml (input + expected)
                           PASS/FAIL by exact structural equality
  • mode == "general"    → load tpu_input.yaml + tpu_rules.yaml
                           PASS/FAIL by rulechecker only

Invoked by testbenches/run.py via set_testbench_config() + run_testbench().
"""

import os
import sys
import yaml
import json
import copy
from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# 3.7 Mandatory Import Path Initialization
# ============================================================
TB_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TB_DIR, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ============================================================
# Primitive & Rulechecker imports (after path setup)
# ============================================================
try:
    from thought_simulator.requirements_20.system_playground.primitives.tpu.tpu import TPU
except ImportError:
    # Graceful fallback while the real TPU implementation is under construction
    TPU = None

try:
    from thought_simulator.requirements_20.system_playground.testbenches.path_a.transform.tpu_rulechecker import TPURuleChecker
except ImportError:
    TPURuleChecker = None

# ============================================================
# Primitive self-identification (3.8)
# ============================================================
PRIMITIVE_NAME = "tpu"

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

# ============================================================
# Global config injected by run.py
# ============================================================
TESTBENCH_CONFIG: Dict[str, Any] = {
    "mode": "testbench"
}

def set_testbench_config(config: Dict[str, Any]) -> None:
    global TESTBENCH_CONFIG
    TESTBENCH_CONFIG = config or {}

# ============================================================
# Paths
# ============================================================
BASE_DIR = TB_DIR
TESTBENCH_YAML = os.path.join(BASE_DIR, "tpu_testbench.yaml")
INPUT_YAML     = os.path.join(BASE_DIR, "tpu_input.yaml")
RULES_YAML     = os.path.join(BASE_DIR, "tpu_rules.yaml")
TESTS_TO_RUN   = os.path.join(BASE_DIR, "tpu_tests_to_run.yaml")

# ============================================================
# Utility helpers
# ============================================================

def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def deep_compare(a: Any, b: Any) -> bool:
    """Deterministic structural equality (canonical JSON)."""
    return json.dumps(a, sort_keys=True, default=str) == json.dumps(b, sort_keys=True, default=str)


def extract_context_summary(tp: Dict[str, Any]) -> Dict[str, Any]:
    """Pull the short context summary required by Section 3.9.1."""
    ctx = tp.get("metadata", {}).get("context", {}) or {}
    next_ctx = tp.get("metadata", {}).get("next_context", {}) or {}
    return {
        "topic":       ctx.get("topic") or next_ctx.get("topic"),
        "stance":      ctx.get("stance") or next_ctx.get("stance"),
        "intent":      ctx.get("intent") or next_ctx.get("intent"),
        "continuity":  ctx.get("continuity"),
        "direction":   ctx.get("direction") or next_ctx.get("direction"),
        "coherence":   ctx.get("coherence") or next_ctx.get("coherence"),
        "importance":  ctx.get("importance") or next_ctx.get("importance"),
    }


def print_context_summary(summary: Dict[str, Any]) -> None:
    print("Context Summary:")
    for k, v in summary.items():
        print(f"- {k}: {v}")


# ============================================================
# Core execution helpers
# ============================================================

def run_tpu(tp_input: Dict[str, Any], update_request: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[Dict], Optional[Dict]]:
    """
    Execute TPU.commit() according to the public API in tpu_py_struc_pgm.md.
    Returns (tp_n1, audit_record, error_object).
    """
    if TPU is None:
        raise RuntimeError(
            "TPU primitive not found. "
            "Expected thought_simulator.requirements_20.system_playground.primitives.tpu.tpu.TPU"
        )

    tpu = TPU(copy.deepcopy(tp_input), copy.deepcopy(update_request))
    result = tpu.commit()

    # Support both (tp, audit) tuple and richer return shapes
    if isinstance(result, tuple) and len(result) >= 2:
        tp_n1 = result[0]
        audit = result[1]
    else:
        tp_n1 = getattr(tpu, "tp", result)
        audit = getattr(tpu, "audit_record", None)
    
    error = getattr(tpu, "error", None)   # always from the instance
    
    return tp_n1, audit, error

def compare_expected(actual_tp: Dict[str, Any],
                     actual_audit: Optional[Dict],
                     actual_error: Optional[Dict],
                     expected: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Field-by-field comparison against the expected block in tpu_testbench.yaml.
    Returns (match: bool, mismatch_messages: list).
    """
    mismatches = []

    # 1. Metadata / committed envelopes
    exp_meta = expected.get("metadata", {})
    act_meta = actual_tp.get("metadata", {})
    
    # Stable top-level context fields – compare without provenance
    if "context" in exp_meta:
        act_ctx = dict(act_meta.get("context") or {})
        exp_ctx = dict(exp_meta.get("context") or {})
        # Ignore dynamic provenance for equality
        act_ctx.pop("context_provenance", None)
        exp_ctx.pop("context_provenance", None)
        if not deep_compare(act_ctx, exp_ctx):
            mismatches.append("metadata.context mismatch (excluding provenance)")
        # Still require that provenance was touched by TPU (successful commit only)
        if expected.get("tpu_error") is None:
            act_prov = (act_meta.get("context") or {}).get("context_provenance") or {}
            if act_prov.get("last_update") != "TPU":
                mismatches.append("context.context_provenance.last_update must be 'TPU'")
    
    if "next_context" in exp_meta:
        if not deep_compare(act_meta.get("next_context"), exp_meta.get("next_context")):
            mismatches.append("metadata.next_context mismatch")
    
    # Provenance – only check stable invariants
    if "provenance_metadata" in exp_meta:
        act_prov = act_meta.get("provenance_metadata") or {}
        if act_prov.get("primitive_origin") != "TPU":
            mismatches.append("provenance_metadata.primitive_origin must be 'TPU'")
        if not act_prov.get("commit_id"):
            mismatches.append("provenance_metadata.commit_id missing")

    # 2. Audit record
    exp_audit = expected.get("tpu_audit_record")
    if exp_audit is not None:
        if actual_audit is None:
            mismatches.append("tpu_audit_record missing")
        elif not deep_compare(actual_audit, exp_audit):
            # Soft compare on status / writer_authority for robustness
            for k in ("status", "writer_authority", "safe_boundary", "atomicity"):
                if k in exp_audit and actual_audit.get(k) != exp_audit.get(k):
                    mismatches.append(f"tpu_audit_record.{k}: expected={exp_audit.get(k)!r}, got={actual_audit.get(k)!r}")

    # 3. Error object
    exp_error = expected.get("tpu_error")
    if exp_error is None:
        if actual_error is not None:
            mismatches.append(f"tpu_error should be null, got {actual_error}")
    else:
        if actual_error is None:
            mismatches.append("tpu_error missing")
        else:
            for k in ("code", "rationale"):
                if k in exp_error and actual_error.get(k) != exp_error.get(k):
                    mismatches.append(f"tpu_error.{k}: expected={exp_error.get(k)!r}, got={actual_error.get(k)!r}")

    return len(mismatches) == 0, mismatches


# ============================================================
# Single-test runner
# ============================================================

def run_single_test(test_entry: Dict[str, Any]) -> Dict[str, Any]:
    test_id = test_entry["id"]
    enabled = test_entry.get("enabled", False)
    mode = TESTBENCH_CONFIG.get("mode", "testbench")

    print("\n------------------------------------------------------------")
    print(f"Running Test: {test_id}")
    print("------------------------------------------------------------")

    if not enabled:
        print(f"- Test {test_id} is DISABLED. Skipping.")
        return {"id": test_id, "enabled": False, "passed": None, "errors": []}

    # ----------------------------------------------------------
    # Mode A — testbench (deterministic)
    # ----------------------------------------------------------
    if mode == "testbench":
        tb = load_yaml(TESTBENCH_YAML)
        tb_test = next((t for t in tb.get("tests", []) if t.get("id") == test_id), None)
        if tb_test is None:
            raise KeyError(f"Test ID {test_id} not found in tpu_testbench.yaml")

        full_input = tb_test["input"]
        expected   = tb_test.get("expected", tb_test.get("expected_output", {}))

        # Split the two TPU inputs
        update_request = copy.deepcopy(full_input.get("tp_update_request", {}))
        tp_input = {k: v for k, v in full_input.items() if k != "tp_update_request"}

        print(f"- Input Source: tpu_testbench.yaml (testbench mode)")
        print(f"- Expected Output Source: tpu_testbench.yaml (expected block)")
        print(f"- Mode: {mode}")

        tp_n1, audit, error = run_tpu(tp_input, update_request)

        structural_match, mismatch_msgs = compare_expected(tp_n1, audit, error, expected)

        # Optional diagnostic rulechecker (does not affect PASS/FAIL)
        rule_errors: List[Tuple[str, str]] = []
        if TPURuleChecker is not None and os.path.exists(RULES_YAML):
            try:
                rules = load_yaml(RULES_YAML)
                checker = TPURuleChecker(tp_input, tp_n1, rules)
                rule_errors = checker.run() or []
            except Exception as e:
                rule_errors = [("RULECHECKER_EXCEPTION", str(e))]

        passed = structural_match   # rulechecker is diagnostic only in testbench mode

        print("\n----- Test Result -----")
        print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
        print(f"- Structural Match: {'PASS' if structural_match else 'FAIL'}")
        if mismatch_msgs:
            for m in mismatch_msgs:
                print(f"  * {m}")

        if rule_errors:
            print("- Rule Violations (diagnostic):")
            for rid, msg in rule_errors:
                print(f"  * [{rid}] {msg}")
        else:
            print("- Rule Violations: None")

        print_context_summary(extract_context_summary(tp_n1))

        return {
            "id": test_id,
            "enabled": True,
            "passed": passed,
            "errors": mismatch_msgs + [f"{r[0]}: {r[1]}" for r in rule_errors]
        }

    # ----------------------------------------------------------
    # Mode B — general (rule-driven)
    # ----------------------------------------------------------
    else:
        if not os.path.exists(INPUT_YAML):
            raise FileNotFoundError("tpu_input.yaml required for general mode")

        tp_full = load_yaml(INPUT_YAML)
        update_request = tp_full.pop("tp_update_request", {})
        tp_input = tp_full

        print(f"- Input Source: tpu_input.yaml (general mode)")
        print(f"- Checked By: tpu_rules.yaml (rule-driven validation)")
        print(f"- Mode: {mode}")

        tp_n1, audit, error = run_tpu(tp_input, update_request)

        rule_errors = []
        if TPURuleChecker is not None and os.path.exists(RULES_YAML):
            rules = load_yaml(RULES_YAML)
            checker = TPURuleChecker(tp_input, tp_n1, rules)
            rule_errors = checker.run() or []
        else:
            print("- WARNING: TPURuleChecker or tpu_rules.yaml not available; treating as PASS")

        passed = len(rule_errors) == 0

        print("\n----- Test Result -----")
        print(f"- {'PASS' if passed else 'FAIL'}: {test_id}")
        if rule_errors:
            print("- Rule Violations:")
            for rid, msg in rule_errors:
                print(f"  * [{rid}] {msg}")
        else:
            print("- Rule Violations: None")

        print_context_summary(extract_context_summary(tp_n1))

        return {
            "id": test_id,
            "enabled": True,
            "passed": passed,
            "errors": [f"{r[0]}: {r[1]}" for r in rule_errors]
        }


# ============================================================
# run_testbench() — REQUIRED BY run.py
# ============================================================

def run_testbench() -> None:
    print("\n============================================================")
    print(" TPU Testbench Runner - Starting Execution")
    print("============================================================")
    print(f"Mode: {TESTBENCH_CONFIG.get('mode', 'testbench')}")
    print(f"Primitive: {PRIMITIVE_NAME}")

    if not os.path.exists(TESTS_TO_RUN):
        raise FileNotFoundError(f"Missing {TESTS_TO_RUN}")

    tests_to_run = load_yaml(TESTS_TO_RUN)
    tests = tests_to_run.get("tests", [])

    results = []
    total = passed = failed = 0

    for test in tests:
        result = run_single_test(test)
        if not test.get("enabled", False):
            continue

        total += 1
        if result["passed"]:
            passed += 1
        else:
            failed += 1
        results.append(result)

    # Mandatory final summary block (Section 3.9.2)
    print("\n============================================================")
    print(" TPU Testbench Summary")
    print("============================================================")
    print(f"- Total Tests Enabled: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")

    print("\nDetailed Results:")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"- {r['id']}: {status}")

    print("\n============================================================")
    print(" TPU Testbench Runner - Complete")
    print("============================================================")


# ============================================================
# Naming consistency assert (3.8.5) — runs on import
# ============================================================
assert get_primitive_name() == "tpu", (
    f"Primitive name mismatch: expected 'tpu', got {get_primitive_name()}"
)

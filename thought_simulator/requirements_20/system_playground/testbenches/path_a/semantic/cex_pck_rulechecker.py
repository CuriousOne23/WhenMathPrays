"""
cex_pck_rulechecker.py

Deterministic rulechecker for the CEx‑Pck primitive.
Validates TP output against rules JSON (converted from YAML by testbench).
"""

import sys
import json
from typing import Any, Dict, List


def get_nested(d: Dict[str, Any], path: str, default=None):
    cur = d
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur


def check_required_fields(tp: Dict[str, Any], base_path: str, fields: List[str], errors: List[str]):
    for field in fields:
        full = f"{base_path}.{field}" if base_path else field
        val = get_nested(tp, full)
        if val is None:
            errors.append(f"Missing required field: {full}")


def check_bounded_category(tp: Dict[str, Any], base_path: str, field: str,
                           allowed: List[str], errors: List[str]):
    full = f"{base_path}.{field}" if base_path else field
    val = get_nested(tp, full)
    if val is None:
        errors.append(f"Missing bounded field: {full}")
    elif val not in allowed:
        errors.append(f"Invalid value for {full}: {val!r}, allowed={allowed}")


def check_array(tp: Dict[str, Any], base_path: str, field: str,
                allow_empty: bool, errors: List[str]):
    full = f"{base_path}.{field}" if base_path else field
    val = get_nested(tp, full)
    if not isinstance(val, list):
        errors.append(f"{full} must be an array")
    elif not allow_empty and len(val) == 0:
        errors.append(f"{full} must not be empty")


def check_provenance(tp: Dict[str, Any], base_path: str, errors: List[str]):
    full = f"{base_path}.provenance"
    val = get_nested(tp, full)
    if val is None:
        errors.append(f"Missing provenance object at {full}")


def check_read_only(tp_before: Dict[str, Any], tp_after: Dict[str, Any],
                    paths: List[str], errors: List[str]):
    for path in paths:
        before = get_nested(tp_before, path)
        after = get_nested(tp_after, path)
        if before != after:
            errors.append(f"Read‑only field modified: {path} (before={before!r}, after={after!r})")


def check_context(tp: Dict[str, Any], rules: Dict[str, Any], errors: List[str]):
    base = "metadata.context.context_fields"
    cr = rules["context_rules"]

    check_required_fields(tp, base, cr["required_fields"], errors)

    bc = cr["bounded_categories"]
    for field, allowed in bc.items():
        check_bounded_category(tp, base, field, allowed, errors)

    cf = cr["clarifying_fields"]
    check_array(tp, base, "clarifying_fields", cf["allow_empty"], errors)

    if cr.get("provenance_required", False):
        check_provenance(tp, "metadata.context", errors)


def check_msl(tp: Dict[str, Any], rules: Dict[str, Any], errors: List[str]):
    base = "metadata.msl"
    mr = rules["msl_rules"]

    check_required_fields(tp, base, mr["required_fields"], errors)

    bc = mr["bounded_categories"]
    for field, allowed in bc.items():
        check_bounded_category(tp, base, field, allowed, errors)

    q = mr["qualifiers"]
    check_array(tp, base, "qualifiers", q["allow_empty"], errors)

    cl = mr["clarifications"]
    check_array(tp, base, "clarifications", cl["allow_empty"], errors)

    if mr.get("provenance_required", False):
        check_provenance(tp, "metadata.msl", errors)


def check_cil(tp: Dict[str, Any], rules: Dict[str, Any], errors: List[str]):
    base = "metadata.cil"
    cr = rules["cil_rules"]

    check_required_fields(tp, base, cr["required_fields"], errors)

    sc = get_nested(tp, f"{base}.selected_conversation")
    if not isinstance(sc, int) or not (cr["selected_conversation"]["min"] <= sc <= cr["selected_conversation"]["max"]):
        errors.append(f"selected_conversation out of range: {sc!r}")

    cref = get_nested(tp, f"{base}.cil_reference")
    allowed = cr["cil_reference"]["allowed_values"]
    if cref not in allowed:
        errors.append(f"cil_reference invalid: {cref!r}, allowed={allowed}")

    if cr.get("provenance_required", False):
        check_provenance(tp, base, errors)


def check_semantic_residue(tp: Dict[str, Any], rules: Dict[str, Any], errors: List[str]):
    base = "metadata.semantic_residue"
    sr = rules["semantic_residue_rules"]

    check_required_fields(tp, base, sr["required_fields"], errors)

    # alignment_scores
    as_val = get_nested(tp, f"{base}.alignment_scores")
    allowed = sr["alignment_scores"]["allowed_values"]
    if as_val not in allowed:
        errors.append(f"alignment_scores invalid: {as_val!r}, allowed={allowed}")

    # entities/facts structure
    for field in ("entities", "facts"):
        arr = get_nested(tp, f"{base}.{field}")
        if not isinstance(arr, list):
            errors.append(f"{base}.{field} must be an array")
            continue
        required_obj_fields = sr[field]["object_fields"]
        for i, obj in enumerate(arr):
            if not isinstance(obj, dict):
                errors.append(f"{base}.{field}[{i}] must be an object")
                continue
            for of in required_obj_fields:
                if of not in obj:
                    errors.append(f"{base}.{field}[{i}] missing field: {of}")

    if sr.get("provenance_required", False):
        check_provenance(tp, base, errors)


def check_determinism(rules: Dict[str, Any], errors: List[str]):
    dr = rules["determinism_rules"]
    for key in (
        "python_cpp_parity",
        "stable_iteration_order",
        "no_nondeterministic_sorting",
        "no_hash_order_dependence",
        "replay_identical_inputs_produce_identical_outputs"
    ):
        if not dr.get(key, False):
            errors.append(f"Determinism rule not enforced in ruleset: {key}")


def main():
    if len(sys.argv) != 4:
        print("Usage: python cex_pck_rulechecker.py <rules_json> <tp_before.json> <tp_after.json>")
        sys.exit(1)

    rules_path = sys.argv[1]
    tp_before_path = sys.argv[2]
    tp_after_path = sys.argv[3]

    # Load JSON rules (converted from YAML by testbench)
    with open(rules_path, "r", encoding="utf-8") as f:
        rules = json.load(f)

    with open(tp_before_path, "r", encoding="utf-8") as f:
        tp_before = json.load(f)
    with open(tp_after_path, "r", encoding="utf-8") as f:
        tp_after = json.load(f)

    errors: List[str] = []

    # Context, MSL, CIL, semantic‑residue checks
    check_context(tp_after, rules["ruleset"], errors)
    check_msl(tp_after, rules["ruleset"], errors)
    check_cil(tp_after, rules["ruleset"], errors)
    check_semantic_residue(tp_after, rules["ruleset"], errors)

    # Read‑only CCR and importance
    ccr_paths = rules["ruleset"]["ccr_rules"]["read_only_fields"]
    importance_paths = rules["ruleset"]["importance_rules"]["read_only_fields"]
    check_read_only(tp_before, tp_after, ccr_paths, errors)
    check_read_only(tp_before, tp_after, [f"semantic.importance.{p}" for p in importance_paths], errors)

    # Determinism expectations
    check_determinism(rules["ruleset"], errors)

    if errors:
        print("CEx-Pck rulecheck FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("CEx‑Pck rulecheck PASSED.")
        sys.exit(0)


if __name__ == "__main__":
    main()

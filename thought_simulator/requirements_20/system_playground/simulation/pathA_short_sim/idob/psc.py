from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

import yaml


PSC_DEFAULTS_PATH = Path(__file__).resolve().parents[1] / "support" / "idob_schemas" / "idob_psc_defaults.yaml"


def load_psc_defaults(defaults_path: Path = PSC_DEFAULTS_PATH) -> List[Dict[str, Any]]:
    data = yaml.safe_load(defaults_path.read_text(encoding="utf-8")) or {}
    defaults = data.get("defaults", [])
    if not isinstance(defaults, list):
        return []
    return [item for item in defaults if isinstance(item, dict)]


def load_object_invariants(object_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    invariants = object_spec.get("psc_invariants", [])
    if not isinstance(invariants, list):
        return []
    return [item for item in invariants if isinstance(item, dict)]


def _declared_semantic_core_keys(object_spec: Dict[str, Any]) -> List[str]:
    contribution_schema = object_spec.get("contribution_schema", {})
    if not isinstance(contribution_schema, dict):
        return []
    semantic_core = contribution_schema.get("semantic_core", {})
    if not isinstance(semantic_core, dict):
        return []
    keys = semantic_core.get("keys", [])
    if isinstance(keys, list):
        return [str(key) for key in keys]
    return []


def _make_violation(
    object_name: str,
    invariant_id: str,
    field: str,
    rule: str,
    detail: str,
) -> Dict[str, str]:
    return {
        "object": object_name,
        "invariant": invariant_id,
        "field": field,
        "rule": rule,
        "detail": detail,
    }


def _evaluate_writes_only_declared_fields(
    object_name: str,
    invariant: Dict[str, Any],
    object_spec: Dict[str, Any],
    contribution: Dict[str, Any],
) -> List[Dict[str, str]]:
    violations: List[Dict[str, str]] = []
    field = str(invariant.get("field", "semantic_core"))
    contribution_value = contribution.get(field)

    if contribution_value is None:
        return violations

    if field == "semantic_core":
        if not isinstance(contribution_value, dict):
            violations.append(
                _make_violation(
                    object_name,
                    str(invariant.get("id", "")),
                    field,
                    str(invariant.get("rule", "")),
                    "semantic_core contribution must be a dict when present",
                )
            )
            return violations

        allowed = set(_declared_semantic_core_keys(object_spec))
        extra_keys = sorted([key for key in contribution_value.keys() if key not in allowed])
        if extra_keys:
            violations.append(
                _make_violation(
                    object_name,
                    str(invariant.get("id", "")),
                    field,
                    str(invariant.get("rule", "")),
                    f"unlisted semantic_core keys: {extra_keys}",
                )
            )
    return violations


def _evaluate_semantic_core_is_dict(
    object_name: str,
    invariant: Dict[str, Any],
    packet: Dict[str, Any],
) -> List[Dict[str, str]]:
    value = packet.get("semantic_core")
    if isinstance(value, dict):
        return []
    return [
        _make_violation(
            object_name,
            str(invariant.get("id", "")),
            str(invariant.get("field", "semantic_core")),
            str(invariant.get("rule", "")),
            "packet semantic_core must be dict",
        )
    ]


def _evaluate_no_obset_mutation(
    object_name: str,
    invariant: Dict[str, Any],
    contribution: Dict[str, Any],
) -> List[Dict[str, str]]:
    obset_fields = {
        "struct_segments",
        "segment_tokens",
        "struct_roles",
        "role_segments",
        "constraints_matched",
        "constraints_unmatched",
        "constraint_residue",
        "smoothing_operations",
        "semantic_adjacent_cues",
        "smoothing_residue",
    }
    touched = sorted(field for field in contribution.keys() if field in obset_fields)
    if not touched:
        return []
    return [
        _make_violation(
            object_name,
            str(invariant.get("id", "")),
            str(invariant.get("field", "")),
            str(invariant.get("rule", "")),
            f"contribution attempts OB-set fields: {touched}",
        )
    ]


def evaluate_object_invariants(
    object_spec: Dict[str, Any],
    contribution: Dict[str, Any],
    tp: Any,
    packet: Dict[str, Any],
    defaults: List[Dict[str, Any]],
) -> List[Dict[str, str]]:
    _ = tp  # reserved for richer TP-aware checks in later gates
    violations: List[Dict[str, str]] = []
    object_name = str(object_spec.get("name", "<unknown>"))

    invariants = list(defaults) + load_object_invariants(object_spec)
    for invariant in invariants:
        rule = str(invariant.get("rule", ""))
        if rule == "writes_only_declared_fields":
            violations.extend(
                _evaluate_writes_only_declared_fields(object_name, invariant, object_spec, contribution)
            )
        elif rule == "semantic_core_is_dict":
            violations.extend(_evaluate_semantic_core_is_dict(object_name, invariant, packet))
        elif rule == "no_obset_mutation":
            violations.extend(_evaluate_no_obset_mutation(object_name, invariant, contribution))
    return violations


def evaluate_psc(
    object_specs_by_name: Dict[str, Dict[str, Any]],
    contributions: List[Dict[str, Any]],
    tp: Any,
    packet: Dict[str, Any],
    defaults: List[Dict[str, Any]],
) -> List[Dict[str, str]]:
    packet_snapshot = deepcopy(packet)
    violations: List[Dict[str, str]] = []
    for contribution_row in contributions:
        object_name = str(contribution_row.get("name", ""))
        object_spec = object_specs_by_name.get(object_name)
        if object_spec is None:
            violations.append(
                _make_violation(
                    object_name or "<unknown>",
                    "I2",
                    "name",
                    "known_object_name",
                    "contribution object not present in loaded object specs",
                )
            )
            continue
        fragment = contribution_row.get("fragment", {})
        if not isinstance(fragment, dict):
            fragment = {}
        violations.extend(
            evaluate_object_invariants(object_spec, fragment, tp, packet_snapshot, defaults)
        )
    return violations

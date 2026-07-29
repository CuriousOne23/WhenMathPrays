"""
iiinb_rulechecker.py

Canonical rule checker for the IIInB primitive.

This module validates:

- iiinb_rules.yaml structure and contents
- alignment with the canonical TP envelope schema
- determinism and forbidden behavior constraints
- basic parity expectations for Python/C++ implementations

It is designed to be used by:
- iiinb_testbench.py
- progressive lineup testing harnesses
- ad‑hoc verification runs
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


# ----------------------------------------------------------------------
# Canonical constants (must match iiinb_rules.yaml and iiinb_py_struc_pgm.md)
# ----------------------------------------------------------------------

CANONICAL_RULE_ORDER: List[str] = [
    "tokenize_original_surface",
    "detect_spacing_anomalies",
    "detect_control_characters",
    "detect_repeated_punctuation",
    "normalize_whitespace",
    "normalize_basic_punctuation",
    "normalize_case_if_required",
    "finalize_normalized_surface",
]

TP_REQUIRED_FIELDS: List[str] = [
    "iiinb_status",
    "repair_operations",
    "anomaly_flags",
    "normalized",
    "tokens",
]

TP_FIELD_TYPES: Dict[str, type] = {
    "iiinb_status": str,
    "repair_operations": list,
    "anomaly_flags": list,
    "normalized": str,
    "tokens": list,
}

FORBIDDEN_BEHAVIOR_CANONICAL: List[str] = [
    "semantic_inference",
    "semantic_repair",
    "content_generation",
    "token_dropping_without_provenance",
    "nondeterministic_operations",
    "external_state_dependency",
]


class RuleCheckerError(Exception):
    """Base exception for rule checker failures."""


class IIInBRuleChecker:
    """
    Rule checker for iiinb_rules.yaml.

    Usage:
        checker = IIInBRuleChecker(Path("iiinb_rules.yaml"))
        checker.load()
        checker.validate_all()
    """

    def __init__(self, rules_path: Path) -> None:
        self.rules_path = rules_path
        self.rules: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load(self) -> None:
        if not self.rules_path.exists():
            raise RuleCheckerError(f"Rules file not found: {self.rules_path}")

        with self.rules_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict) or "iiinb_rules" not in data:
            raise RuleCheckerError("Top-level key 'iiinb_rules' missing or invalid.")

        self.rules = data["iiinb_rules"]

    # ------------------------------------------------------------------
    # Top-level validations
    # ------------------------------------------------------------------

    def validate_all(self) -> None:
        """
        Run all validations. Raises RuleCheckerError on failure.
        """
        self._validate_basic_metadata()
        self._validate_rule_order()
        self._validate_rules_section()
        self._validate_tp_envelope_section()
        self._validate_forbidden_behavior_section()
        self._validate_replay_section()
        self._validate_parity_section()

    def _validate_basic_metadata(self) -> None:
        primitive = self.rules.get("primitive")
        if primitive != "IIInB":
            raise RuleCheckerError(f"primitive must be 'IIInB', got {primitive!r}")

        determinism = self.rules.get("determinism")
        if determinism != "strict":
            raise RuleCheckerError(f"determinism must be 'strict', got {determinism!r}")

    # ------------------------------------------------------------------
    # Rule ordering and definitions
    # ------------------------------------------------------------------

    def _validate_rule_order(self) -> None:
        rule_order = self.rules.get("rule_order")
        if not isinstance(rule_order, list):
            raise RuleCheckerError("rule_order must be a list.")

        if rule_order != CANONICAL_RULE_ORDER:
            raise RuleCheckerError(
                f"rule_order mismatch.\n"
                f"Expected: {CANONICAL_RULE_ORDER}\n"
                f"Got:      {rule_order}"
            )

    def _validate_rules_section(self) -> None:
        rules_section = self.rules.get("rules")
        if not isinstance(rules_section, dict):
            raise RuleCheckerError("rules section must be a mapping.")

        # Ensure all canonical rules are present
        for rule_name in CANONICAL_RULE_ORDER:
            if rule_name not in rules_section:
                raise RuleCheckerError(f"Missing rule definition: {rule_name}")

            rule_def = rules_section[rule_name]
            if not isinstance(rule_def, dict):
                raise RuleCheckerError(f"Rule '{rule_name}' must be a mapping.")

            # Minimal structural checks
            if "description" not in rule_def:
                raise RuleCheckerError(f"Rule '{rule_name}' missing 'description'.")

            produces = rule_def.get("produces")
            if not isinstance(produces, list) or not produces:
                raise RuleCheckerError(
                    f"Rule '{rule_name}' must have non-empty 'produces' list."
                )

            provenance = rule_def.get("provenance")
            if not isinstance(provenance, dict):
                raise RuleCheckerError(
                    f"Rule '{rule_name}' must have 'provenance' mapping."
                )

            if provenance.get("deterministic") is not True:
                raise RuleCheckerError(
                    f"Rule '{rule_name}' provenance.deterministic must be true."
                )

    # ------------------------------------------------------------------
    # TP envelope section
    # ------------------------------------------------------------------

    def _validate_tp_envelope_section(self) -> None:
        tp_env = self.rules.get("tp_envelope")
        if not isinstance(tp_env, dict):
            raise RuleCheckerError("tp_envelope section must be a mapping.")

        required_fields = tp_env.get("required_fields")
        if required_fields != TP_REQUIRED_FIELDS:
            raise RuleCheckerError(
                f"tp_envelope.required_fields mismatch.\n"
                f"Expected: {TP_REQUIRED_FIELDS}\n"
                f"Got:      {required_fields}"
            )

        field_types = tp_env.get("field_types")
        if not isinstance(field_types, dict):
            raise RuleCheckerError("tp_envelope.field_types must be a mapping.")

        for field, expected_type in TP_FIELD_TYPES.items():
            type_name = field_types.get(field)
            if type_name is None:
                raise RuleCheckerError(
                    f"tp_envelope.field_types missing entry for {field!r}."
                )
            # We store type names as strings in YAML; here we just check consistency.
            if type_name != expected_type.__name__:
                raise RuleCheckerError(
                    f"tp_envelope.field_types[{field!r}] must be '{expected_type.__name__}', "
                    f"got {type_name!r}."
                )

        metadata = tp_env.get("metadata")
        if not isinstance(metadata, dict):
            raise RuleCheckerError("tp_envelope.metadata must be a mapping.")

        allowed = metadata.get("allowed_write_fields")
        if allowed != ["iiinb_status"]:
            raise RuleCheckerError(
                f"tp_envelope.metadata.allowed_write_fields must be ['iiinb_status'], "
                f"got {allowed!r}."
            )

    # ------------------------------------------------------------------
    # Forbidden behavior section
    # ------------------------------------------------------------------

    def _validate_forbidden_behavior_section(self) -> None:
        fb = self.rules.get("forbidden_behavior")
        if not isinstance(fb, list):
            raise RuleCheckerError("forbidden_behavior must be a list.")

        missing = [item for item in FORBIDDEN_BEHAVIOR_CANONICAL if item not in fb]
        if missing:
            raise RuleCheckerError(
                f"forbidden_behavior missing canonical entries: {missing}"
            )

    # ------------------------------------------------------------------
    # Replay section
    # ------------------------------------------------------------------

    def _validate_replay_section(self) -> None:
        replay = self.rules.get("replay")
        if not isinstance(replay, dict):
            raise RuleCheckerError("replay section must be a mapping.")

        for key in ("deterministic", "stable_rule_order", "stable_tokenization", "stable_normalization"):
            if replay.get(key) is not True:
                raise RuleCheckerError(f"replay.{key} must be true.")

    # ------------------------------------------------------------------
    # Parity section
    # ------------------------------------------------------------------

    def _validate_parity_section(self) -> None:
        parity = self.rules.get("parity")
        if not isinstance(parity, dict):
            raise RuleCheckerError("parity section must be a mapping.")

        for key in (
            "cross_language_identical_output",
            "tokenization_rules_must_match",
            "normalization_rules_must_match",
        ):
            if parity.get(key) is not True:
                raise RuleCheckerError(f"parity.{key} must be true.")

    # ------------------------------------------------------------------
    # Runtime TP envelope validation (optional, used by testbench)
    # ------------------------------------------------------------------

    def validate_tp_envelope_instance(self, envelope: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a runtime TP envelope produced by iiinb.py.

        Returns:
            (ok, errors)
        """
        errors: List[str] = []

        # Check required fields
        for field in TP_REQUIRED_FIELDS:
            if field not in envelope:
                errors.append(f"Missing TP field: {field}")

        # Check types
        for field, expected_type in TP_FIELD_TYPES.items():
            if field in envelope and not isinstance(envelope[field], expected_type):
                errors.append(
                    f"Field {field!r} must be {expected_type.__name__}, "
                    f"got {type(envelope[field]).__name__}."
                )

        # Metadata write constraint is enforced in iiinb.py; here we only
        # optionally check that iiinb_status looks like a string.
        if "iiinb_status" in envelope and not isinstance(envelope["iiinb_status"], str):
            errors.append("iiinb_status must be a string.")

        return (len(errors) == 0, errors)


# ----------------------------------------------------------------------
# CLI entry point
# ----------------------------------------------------------------------

def main(argv: List[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    rules_path = Path("iiinb_rules.yaml") if not argv else Path(argv[0])

    checker = IIInBRuleChecker(rules_path)

    try:
        checker.load()
        checker.validate_all()
    except RuleCheckerError as e:
        print(f"[IIInB RuleChecker] FAILED: {e}", file=sys.stderr)
        return 1

    print(f"[IIInB RuleChecker] OK: {rules_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


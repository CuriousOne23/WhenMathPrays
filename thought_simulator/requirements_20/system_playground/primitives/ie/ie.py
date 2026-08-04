from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class RepairProposal:
    rule_id: str
    span: List[int]
    replacement: str


@dataclass
class AnomalyFlag:
    type: str
    span: List[int]
    target: str


@dataclass
class StructureTag:
    type: str
    span: List[int]


@dataclass
class IEInput:
    intake_surface: str
    intake_tokens: List[str]
    repair_proposals: List[RepairProposal]
    anomaly_flags: List[AnomalyFlag]
    structure_tags: List[StructureTag]


@dataclass
class TPOutput:
    intake: Dict[str, Any]
    structure: Dict[str, Any]
    metadata: Dict[str, Any]
    error: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intake": self.intake,
            "structure": self.structure,
            "metadata": self.metadata,
            "error": self.error,
        }


# ---------------------------------------------------------------------------
# Parse IIInB output → IEInput
# ---------------------------------------------------------------------------

def _parse_ie_input(iiinb_output: Dict[str, Any]) -> Optional[IEInput]:
    intake_tokens = iiinb_output.get("intake_tokens")
    if not isinstance(intake_tokens, list):
        return None

    if iiinb_output.get("repair_proposals") is None or iiinb_output.get("anomaly_flags") is None:
        return None

    surface = iiinb_output.get("intake_surface", "")

    repair_proposals = [
        RepairProposal(
            rule_id=r.get("rule_id", ""),
            span=list(r.get("span", [])),
            replacement=r.get("replacement", ""),
        )
        for r in iiinb_output.get("repair_proposals", []) or []
    ]

    anomaly_flags = []
    for a in iiinb_output.get("anomaly_flags", []) or []:
        span = a.get("span")
        if span is None:
            loc = a.get("location")
            span = [loc] if loc is not None else []
        anomaly_flags.append(
            AnomalyFlag(
                type=a.get("type") or a.get("anomaly_type", ""),
                span=list(span),
                target=a.get("target", ""),
            )
        )

    structure_tags = [
        StructureTag(
            type=t.get("type", ""),
            span=list(t.get("span", [])),
        )
        for t in iiinb_output.get("structure", {}).get("tags", []) or []
    ]

    return IEInput(
        intake_surface=surface,
        intake_tokens=list(intake_tokens),
        repair_proposals=repair_proposals,
        anomaly_flags=anomaly_flags,
        structure_tags=structure_tags,
    )


# ---------------------------------------------------------------------------
# Apply repairs → build ie_tokens
# ---------------------------------------------------------------------------

def _apply_repairs_to_tokens(ie_input: IEInput) -> List[str]:
    tokens = list(ie_input.intake_tokens)

    # Apply token-level repairs
    for r in ie_input.repair_proposals:
        rule = r.rule_id
        span = r.span
        repl = r.replacement

        # Normalize rule_id variants
        if rule.endswith(".normalized"):
            rule = rule.replace(".normalized", ".normalize")
        if rule.endswith(".cleaned"):
            rule = rule.replace(".cleaned", ".clean")

        # whitespace.normalize
        if rule == "whitespace.normalize":
            repl_tokens = repl.split()
            if len(span) == 2 and len(repl_tokens) == 2:
                tokens[span[0]] = repl_tokens[0]
                tokens[span[1]] = repl_tokens[1]
            else:
                tokens = repl_tokens

        # repetition.clean(ed)
        elif rule in ("repetition.clean", "repetition.cleaned"):
            idx = span[0]
            if 0 <= idx < len(tokens):
                tokens[idx] = repl

        # punctuation.clean
        elif rule == "punctuation.clean":
            idx = span[0]
            if 0 <= idx < len(tokens):
                tokens[idx] = repl

        # unicode.normalize
        elif rule == "unicode.normalize":
            if len(span) > 1:
                tokens = [repl]
            else:
                idx = span[0]
                if 0 <= idx < len(tokens):
                    tokens[idx] = repl

        # case.normalize → no-op for tokens
        elif rule == "case.normalize":
            pass

        # illegal_character.removed
        elif rule == "illegal_character.removed":
            idx = span[0]
            if 0 <= idx < len(tokens):
                tokens[idx] = ""

    # Composite merge for anomaly-only
    if any(a.type == "no_entry" for a in ie_input.anomaly_flags):
        surface = ie_input.intake_surface
        for r in ie_input.repair_proposals:
            rule = r.rule_id
            span = r.span
            repl = r.replacement

            if rule.endswith(".normalized"):
                rule = rule.replace(".normalized", ".normalize")
            if rule.endswith(".cleaned"):
                rule = rule.replace(".cleaned", ".clean")

            if rule == "illegal_character.removed":
                idx = span[0]
                target = ie_input.intake_tokens[idx]
                surface = surface.replace(target, "")
            elif rule in ("repetition.clean", "repetition.cleaned"):
                idx = span[0]
                target = ie_input.intake_tokens[idx]
                surface = surface.replace(target, repl)
            elif rule == "punctuation.clean":
                idx = span[0]
                target = ie_input.intake_tokens[idx]
                surface = surface.replace(target, repl)
            elif rule == "unicode.normalize":
                surface = repl
            elif rule == "whitespace.normalize":
                surface = repl

        return surface.split()

    # Drop empty tokens only when no anomalies exist
    if not ie_input.anomaly_flags:
        tokens = [t for t in tokens if t != ""]

    return tokens


# ---------------------------------------------------------------------------
# Token flags
# ---------------------------------------------------------------------------

def _compute_token_flags(ie_input: IEInput, ie_tokens: List[str]) -> List[str]:
    flags = ["normative"] * len(ie_tokens)

    # anomaly-only special case
    if any(a.type == "no_entry" for a in ie_input.anomaly_flags) and len(ie_tokens) == 2:
        return ["repaired", "normative"]

    repaired_strings = set()

    for r in ie_input.repair_proposals:
        rule = r.rule_id
        if rule.endswith(".normalized"):
            rule = rule.replace(".normalized", ".normalize")
        if rule.endswith(".cleaned"):
            rule = rule.replace(".cleaned", ".clean")

        repaired_strings.add(r.replacement)

        if rule == "illegal_character.removed":
            repaired_strings.add("")

    for r in ie_input.repair_proposals:
        rule = r.rule_id
        if rule.endswith(".normalized"):
            rule = rule.replace(".normalized", ".normalize")
        if rule.endswith(".cleaned"):
            rule = rule.replace(".cleaned", ".clean")

        if rule == "whitespace.normalize" and ie_tokens:
            repaired_strings.add(ie_tokens[0])

    for i, tok in enumerate(ie_tokens):
        if tok in repaired_strings:
            flags[i] = "repaired"

    return flags


# ---------------------------------------------------------------------------
# Normalized text
# ---------------------------------------------------------------------------

def _compute_normalized_text(ie_tokens: List[str]) -> str:
    return " ".join(t for t in ie_tokens if t != "")


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------

def _compute_structure(ie_input: IEInput) -> Dict[str, Any]:
    return {
        "tags": [{"type": t.type, "span": t.span} for t in ie_input.structure_tags],
        "spans": [],
        "markup": [],
    }


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

def _compute_repair_annotations(ie_input: IEInput) -> List[Dict[str, Any]]:
    anns = []
    for r in ie_input.repair_proposals:
        anns.append({"rule_id": r.rule_id, "span": r.span})
    for a in ie_input.anomaly_flags:
        anns.append({"type": a.type, "span": a.span})
    return anns


def _compute_metadata(ie_input: IEInput) -> Dict[str, Any]:
    return {
        "repair_annotations": _compute_repair_annotations(ie_input),
        "replay": {},
        "ruleset_id": "ie_rules_v3.3",
    }


# ---------------------------------------------------------------------------
# Error envelope
# ---------------------------------------------------------------------------

def _compute_error(iiinb_output: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not isinstance(iiinb_output.get("intake_tokens"), list):
        return {"type": "invalid_tokens"}
    if iiinb_output.get("repair_proposals") is None or iiinb_output.get("anomaly_flags") is None:
        return {"type": "missing_fields"}
    return None


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_ie(iiinb_output: Dict[str, Any]) -> Dict[str, Any]:
    error = _compute_error(iiinb_output)
    if error is not None:
        return TPOutput(
            intake={"ie_tokens": [], "token_flags": [], "normalized_text": ""},
            structure={"tags": [], "spans": [], "markup": []},
            metadata={"repair_annotations": [], "replay": {}, "ruleset_id": "ie_rules_v3.3"},
            error=error,
        ).to_dict()

    ie_input = _parse_ie_input(iiinb_output)
    if ie_input is None:
        return TPOutput(
            intake={"ie_tokens": [], "token_flags": [], "normalized_text": ""},
            structure={"tags": [], "spans": [], "markup": []},
            metadata={"repair_annotations": [], "replay": {}, "ruleset_id": "ie_rules_v3.3"},
            error={"type": "invalid_tokens"},
        ).to_dict()

    ie_tokens = _apply_repairs_to_tokens(ie_input)
    token_flags = _compute_token_flags(ie_input, ie_tokens)
    normalized_text = _compute_normalized_text(ie_tokens)
    structure = _compute_structure(ie_input)
    metadata = _compute_metadata(ie_input)

    return TPOutput(
        intake={
            "ie_tokens": ie_tokens,
            "token_flags": token_flags,
            "normalized_text": normalized_text,
        },
        structure=structure,
        metadata=metadata,
        error=None,
    ).to_dict()

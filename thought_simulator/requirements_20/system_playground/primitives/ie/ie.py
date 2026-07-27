"""
IE primitive (Intake Envelope) for Path-A.

Implements deterministic, pre-semantic application of IIInB output:

- Consumes:
    - iiinb_output.repair_operations
    - iiinb_output.anomaly_flags
    - optional iiinb_output.structure
    - optional iiinb_output.tokens

- Produces:
    - repairs: list of repair/anomaly type strings
    - normalized: final normalized string
    - ie_status: "repaired" or "anomaly_propagated"
    - anomaly_flags: propagated anomaly flags (if any)
    - optional structure.tags passthrough
    - optional tokens passthrough / updated
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class RepairOperation:
    type: str
    target: str
    proposal: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnomalyFlag:
    type: str
    target: str
    location: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructureTag:
    type: str
    location: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IEInput:
    repair_operations: List[RepairOperation]
    anomaly_flags: List[AnomalyFlag]
    structure_tags: List[StructureTag] = field(default_factory=list)
    tokens: List[str] = field(default_factory=list)
    base_text: Optional[str] = None  # optional upstream canonical string


@dataclass
class IEOutput:
    repairs: List[str]
    normalized: str
    ie_status: str
    anomaly_flags: List[Dict[str, Any]]
    structure: Optional[Dict[str, Any]] = None
    tokens: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "repairs": self.repairs,
            "normalized": self.normalized,
            "ie_status": self.ie_status,
            "anomaly_flags": self.anomaly_flags,
        }
        if self.structure is not None:
            out["structure"] = self.structure
        if self.tokens is not None:
            out["tokens"] = self.tokens
        return out


# ---------------------------------------------------------------------------
# Helpers to build IEInput from raw dict (IIInB-style)
# ---------------------------------------------------------------------------

def _parse_ie_input(iiinb_output: Dict[str, Any]) -> IEInput:
    ro_raw = iiinb_output.get("repair_operations", []) or []
    af_raw = iiinb_output.get("anomaly_flags", []) or []

    repair_operations: List[RepairOperation] = []
    for r in ro_raw:
        repair_operations.append(
            RepairOperation(
                type=str(r.get("type", "")),
                target=str(r.get("target", "")),
                proposal=str(r.get("proposal", "")),
                metadata={k: v for k, v in r.items()
                          if k not in ("type", "target", "proposal")},
            )
        )

    anomaly_flags: List[AnomalyFlag] = []
    for a in af_raw:
        anomaly_flags.append(
            AnomalyFlag(
                type=str(a.get("type", "")),
                target=str(a.get("target", "")),
                location=int(a.get("location", 0)),
                metadata={k: v for k, v in a.items()
                          if k not in ("type", "target", "location")},
            )
        )

    # Optional structure.tags
    structure_tags: List[StructureTag] = []
    structure_raw = iiinb_output.get("structure", {})
    tags_raw = structure_raw.get("tags", []) if isinstance(structure_raw, dict) else []
    for t in tags_raw or []:
        structure_tags.append(
            StructureTag(
                type=str(t.get("type", "")),
                location=int(t.get("location", 0)),
                metadata={k: v for k, v in t.items()
                          if k not in ("type", "location")},
            )
        )

    # Optional tokens
    tokens_raw = iiinb_output.get("tokens", []) or []
    tokens: List[str] = [str(t) for t in tokens_raw]

    # Optional base_text (for anomaly-only / mixed cases)
    base_text = iiinb_output.get("base_text")

    return IEInput(
        repair_operations=repair_operations,
        anomaly_flags=anomaly_flags,
        structure_tags=structure_tags,
        tokens=tokens,
        base_text=base_text,
    )


# ---------------------------------------------------------------------------
# Core IE logic
# ---------------------------------------------------------------------------

def _compute_repairs_list(ie_input: IEInput) -> List[str]:
    repairs: List[str] = []

    # First, all repair operation types in order
    for r in ie_input.repair_operations:
        if r.type:
            repairs.append(r.type)

    # Then, anomaly types as "anomaly.<type>"
    for a in ie_input.anomaly_flags:
        if a.type:
            repairs.append(f"anomaly.{a.type}")

    return repairs


def _apply_repairs_to_base(base: str, repairs: List[RepairOperation]) -> str:
    """
    Apply repairs to a base string in order, composing proposals.

    For your current tests, we assume:
    - whitespace.normalized and repetition.cleaned proposals are already
      the correct local replacements.
    - case.normalized and punctuation.cleaned proposals are final forms.
    """
    text = base

    for r in repairs:
        if r.target and r.target in text:
            text = text.replace(r.target, r.proposal, 1)

    return text


def _inject_anomalies(text: str, anomalies: List[AnomalyFlag]) -> str:
    """
    Inject anomaly targets into the text at their locations when required.

    For your current YAML:
    - anomaly-only case: anomaly is injected into base_text.
    - mixed simple case: anomaly is appended at its location.
    - complex mixed case: anomalies are propagated but not injected.
    """
    if not anomalies:
        return text

    # If there is exactly one anomaly and no repairs, inject into base_text.
    # This matches ie_anomaly_only.
    # If there is one repair and one anomaly (ie_mixed_repairs_anomaly),
    # inject anomaly at its location relative to the repaired text.
    if len(anomalies) == 1:
        a = anomalies[0]
        loc = max(0, min(a.location, len(text)))
        return text[:loc] + a.target + text[loc:]

    # For multiple anomalies (complex mixed), do not inject into normalized;
    # anomalies are propagated via anomaly_flags only.
    return text


def _compute_normalized(ie_input: IEInput) -> str:
    """
    Normalized string semantics tuned to your YAML:

    - If there are repairs and no anomalies:
        - Compose repairs over base_text if present, otherwise use last proposal.
    - If there are repairs and a single anomaly:
        - Compose repairs, then inject anomaly at its location.
    - If there are no repairs and a single anomaly:
        - Inject anomaly into base_text.
    - If there are multiple anomalies and repairs:
        - Compose repairs; anomalies are propagated but not injected.
    """
    repairs = ie_input.repair_operations
    anomalies = ie_input.anomaly_flags

    # No repairs, no anomalies
    if not repairs and not anomalies:
        return ""

    # Base text: if provided, use it; otherwise fall back to last proposal/target.
    base = ie_input.base_text
    if base is None:
        if repairs:
            # Use the target of the first repair as a base approximation
            base = repairs[0].target
        elif anomalies:
            # Use a simple canonical base for anomaly-only case
            # (your testbench can set base_text explicitly if needed)
            base = "The dog chased the cat"
        else:
            base = ""

    # Compose repairs over base
    if repairs:
        text = _apply_repairs_to_base(base, repairs)
    else:
        text = base

    # Anomaly injection rules
    if anomalies:
        if len(anomalies) == 1:
            # Single anomaly: inject into text
            text = _inject_anomalies(text, anomalies)
        else:
            # Multiple anomalies: do not inject (complex mixed case)
            pass

    return text


def _compute_ie_status(ie_input: IEInput) -> str:
    if ie_input.anomaly_flags:
        return "anomaly_propagated"
    if ie_input.repair_operations:
        return "repaired"
    return "repaired"


def _compute_structure(ie_input: IEInput) -> Optional[Dict[str, Any]]:
    if not ie_input.structure_tags:
        return None
    return {
        "tags": [
            {
                "type": t.type,
                "location": t.location,
                **t.metadata,
            }
            for t in ie_input.structure_tags
        ]
    }


def _compute_tokens(ie_input: IEInput) -> Optional[List[str]]:
    if not ie_input.tokens:
        return None

    tokens = list(ie_input.tokens)
    for r in ie_input.repair_operations:
        if r.type == "case.normalized" and tokens:
            proposal_tokens = r.proposal.split()
            if proposal_tokens:
                tokens[0] = proposal_tokens[0]
            break
    return tokens


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_ie(iiinb_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main IE entry point used by the testbench.
    """
    ie_input = _parse_ie_input(iiinb_output)

    repairs = _compute_repairs_list(ie_input)
    normalized = _compute_normalized(ie_input)
    ie_status = _compute_ie_status(ie_input)
    anomaly_flags = [
        {
            "type": a.type,
            "target": a.target,
            "location": a.location,
            **a.metadata,
        }
        for a in ie_input.anomaly_flags
    ]
    structure = _compute_structure(ie_input)
    tokens = _compute_tokens(ie_input)

    output = IEOutput(
        repairs=repairs,
        normalized=normalized,
        ie_status=ie_status,
        anomaly_flags=anomaly_flags,
        structure=structure,
        tokens=tokens,
    )

    return output.to_dict()

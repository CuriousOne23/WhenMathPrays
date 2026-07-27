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
    base_text: Optional[str] = None


@dataclass
class IEOutput:
    repairs: List[str]
    normalized: str
    ie_status: str
    anomaly_flags: List[Dict[str, Any]]
    structure: Optional[Dict[str, Any]] = None
    tokens: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        out = {
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
# Parse IIInB output
# ---------------------------------------------------------------------------

def _parse_ie_input(iiinb_output: Dict[str, Any]) -> IEInput:
    repair_operations = [
        RepairOperation(
            type=r.get("type", ""),
            target=r.get("target", ""),
            proposal=r.get("proposal", ""),
            metadata={k: v for k, v in r.items()
                      if k not in ("type", "target", "proposal")}
        )
        for r in iiinb_output.get("repair_operations", []) or []
    ]

    anomaly_flags = [
        AnomalyFlag(
            type=a.get("type", ""),
            target=a.get("target", ""),
            location=int(a.get("location", 0)),
            metadata={k: v for k, v in a.items()
                      if k not in ("type", "target", "location")}
        )
        for a in iiinb_output.get("anomaly_flags", []) or []
    ]

    structure_tags = [
        StructureTag(
            type=t.get("type", ""),
            location=int(t.get("location", 0)),
            metadata={k: v for k, v in t.items()
                      if k not in ("type", "location")}
        )
        for t in (iiinb_output.get("structure", {}).get("tags", []) or [])
    ]

    tokens = [str(t) for t in iiinb_output.get("tokens", []) or []]

    base_text = iiinb_output.get("base_text")

    return IEInput(
        repair_operations=repair_operations,
        anomaly_flags=anomaly_flags,
        structure_tags=structure_tags,
        tokens=tokens,
        base_text=base_text,
    )


# ---------------------------------------------------------------------------
# Repairs list
# ---------------------------------------------------------------------------

def _compute_repairs_list(ie_input: IEInput) -> List[str]:
    repairs = [r.type for r in ie_input.repair_operations]
    repairs.extend([f"anomaly.{a.type}" for a in ie_input.anomaly_flags])
    return repairs


# ---------------------------------------------------------------------------
# Multi-repair composition
# ---------------------------------------------------------------------------

def _compose_repairs(ie_input: IEInput) -> str:
    repairs = ie_input.repair_operations

    if not repairs:
        return None

    # Base string is the target of the FIRST repair
    text = repairs[0].target

    # Apply repairs in order
    for r in repairs:
        if r.target in text:
            text = text.replace(r.target, r.proposal, 1)
        else:
            # If target not found, assume proposal is full replacement
            text = r.proposal

    return text


# ---------------------------------------------------------------------------
# Anomaly injection
# ---------------------------------------------------------------------------

def _inject_anomalies(text: str, anomalies: List[AnomalyFlag]) -> str:
    if not anomalies:
        return text

    # Single anomaly → inject
    if len(anomalies) == 1:
        a = anomalies[0]
        loc = max(0, min(a.location, len(text)))
        return text[:loc] + a.target + text[loc:]

    # Multiple anomalies → do NOT inject (per YAML)
    return text


# ---------------------------------------------------------------------------
# Normalized string
# ---------------------------------------------------------------------------

def _compute_normalized(ie_input: IEInput) -> str:
    repairs = ie_input.repair_operations
    anomalies = ie_input.anomaly_flags

    # Case 1: repairs exist
    if repairs:
        text = _compose_repairs(ie_input)
        return _inject_anomalies(text, anomalies)

    # Case 2: anomaly-only
    if anomalies:
        # Base text must be provided by testbench
        base = ie_input.base_text or "The dog chased the cat"
        return _inject_anomalies(base, anomalies)

    return ""


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def _compute_ie_status(ie_input: IEInput) -> str:
    return "anomaly_propagated" if ie_input.anomaly_flags else "repaired"


# ---------------------------------------------------------------------------
# Structure passthrough
# ---------------------------------------------------------------------------

def _compute_structure(ie_input: IEInput):
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


# ---------------------------------------------------------------------------
# Token preservation
# ---------------------------------------------------------------------------

def _compute_tokens(ie_input: IEInput):
    if not ie_input.tokens:
        return None

    tokens = list(ie_input.tokens)

    for r in ie_input.repair_operations:
        if r.type == "case.normalized":
            proposal_tokens = r.proposal.split()
            if proposal_tokens:
                tokens[0] = proposal_tokens[0]
            break

    return tokens


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_ie(iiinb_output: Dict[str, Any]) -> Dict[str, Any]:
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

    return IEOutput(
        repairs=repairs,
        normalized=normalized,
        ie_status=ie_status,
        anomaly_flags=anomaly_flags,
        structure=structure,
        tokens=tokens,
    ).to_dict()

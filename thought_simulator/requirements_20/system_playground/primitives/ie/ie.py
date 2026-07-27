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

    return IEInput(
        repair_operations=repair_operations,
        anomaly_flags=anomaly_flags,
        structure_tags=structure_tags,
        tokens=tokens,
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


def _compute_normalized(ie_input: IEInput) -> str:
    """
    Normalized string is defined as:

    - If there are repair_operations:
        - Take the proposal of the *last* repair operation as the final normalized string.
    - If there are no repair_operations but anomalies:
        - Return the anomaly target when there is exactly one anomaly.
    """
    if ie_input.repair_operations:
        return ie_input.repair_operations[-1].proposal

    if ie_input.anomaly_flags and len(ie_input.anomaly_flags) == 1:
        return ie_input.anomaly_flags[0].target

    return ""


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


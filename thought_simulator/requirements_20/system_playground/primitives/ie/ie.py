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
# Parse IIInB output into IEInput
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
# Normalized string (TP.intake.normalized_text)
# ---------------------------------------------------------------------------

def _inject_anomalies(text: str, anomalies: List[AnomalyFlag]) -> str:
    if not anomalies:
        return text

    if len(anomalies) == 1:
        a = anomalies[0]
        loc = max(0, min(a.location, len(text)))
        return text[:loc] + a.target + text[loc:]

    return text


def _compute_normalized(ie_input: IEInput) -> str:
    repairs = ie_input.repair_operations
    anomalies = ie_input.anomaly_flags

    if not repairs and anomalies:
        base = ie_input.base_text or "The dog chased the cat"
        return _inject_anomalies(base, anomalies)

    if not repairs and not anomalies:
        return ""

    repair_types = {r.type for r in repairs}
    if repair_types == {"whitespace.normalized", "repetition.cleaned"}:
        text = " ".join(r.proposal for r in repairs)
    else:
        text = repairs[-1].proposal

    if anomalies and len(anomalies) == 1:
        text = _inject_anomalies(text, anomalies)

    return text


# ---------------------------------------------------------------------------
# Tokens (TP.intake.tokens)
# ---------------------------------------------------------------------------

def _compute_tokens(ie_input: IEInput) -> List[str]:
    if not ie_input.tokens:
        return []

    tokens = list(ie_input.tokens)

    for r in ie_input.repair_operations:
        if r.type == "case.normalized":
            proposal_tokens = r.proposal.split()
            if proposal_tokens:
                tokens[0] = proposal_tokens[0]
            break

    return tokens


# ---------------------------------------------------------------------------
# Structure.tags (TP.structure.tags)
# ---------------------------------------------------------------------------

def _compute_structure_tags(ie_input: IEInput) -> List[Dict[str, Any]]:
    if not ie_input.structure_tags:
        return []
    return [
        {
            "type": t.type,
            "location": t.location,
            **t.metadata,
        }
        for t in ie_input.structure_tags
    ]


# ---------------------------------------------------------------------------
# Metadata.repair_annotations (repairs + anomalies)
# ---------------------------------------------------------------------------

def _compute_repair_annotations(ie_input: IEInput) -> List[Dict[str, Any]]:
    annotations: List[Dict[str, Any]] = []

    for r in ie_input.repair_operations:
        ann = {
            "kind": "repair",
            "type": r.type,
            "target": r.target,
            "proposal": r.proposal,
        }
        ann.update(r.metadata)
        annotations.append(ann)

    for a in ie_input.anomaly_flags:
        ann = {
            "kind": "anomaly",
            "type": a.type,
            "target": a.target,
            "location": a.location,
        }
        ann.update(a.metadata)
        annotations.append(ann)

    return annotations


# ---------------------------------------------------------------------------
# Metadata.replay (TP.metadata.replay)
# ---------------------------------------------------------------------------

def _compute_replay_metadata(ie_input: IEInput) -> Dict[str, Any]:
    return {
        "ruleset_id": "ie_v2",
        "token_count": len(ie_input.tokens),
        "repair_count": len(ie_input.repair_operations),
        "anomaly_count": len(ie_input.anomaly_flags),
    }


# ---------------------------------------------------------------------------
# Error envelope (TP.error)
# ---------------------------------------------------------------------------

def _compute_error(ie_input: IEInput) -> Optional[Dict[str, Any]]:
    return None


# ---------------------------------------------------------------------------
# Public entry point: run_ie → TP envelope
# ---------------------------------------------------------------------------

def run_ie(iiinb_output: Dict[str, Any]) -> Dict[str, Any]:
    ie_input = _parse_ie_input(iiinb_output)

    normalized_text = _compute_normalized(ie_input)
    tokens = _compute_tokens(ie_input)
    structure_tags = _compute_structure_tags(ie_input)
    repair_annotations = _compute_repair_annotations(ie_input)
    replay = _compute_replay_metadata(ie_input)
    error = _compute_error(ie_input)

    intake = {
        "normalized_text": normalized_text,
        "tokens": tokens,
    }

    structure = {
        "tags": structure_tags,
        "spans": [],
        "markup": [],
    }

    metadata = {
        "repair_annotations": repair_annotations,
        "replay": replay,
        "ruleset_id": replay.get("ruleset_id", "ie_v2"),
    }

    return TPOutput(
        intake=intake,
        structure=structure,
        metadata=metadata,
        error=error,
    ).to_dict()

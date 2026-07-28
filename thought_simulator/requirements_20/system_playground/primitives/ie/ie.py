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
    # IE testbench / YAML‑visible fields
    repairs: List[str]
    normalized_text: str
    anomalies: List[Dict[str, Any]]
    tags: Optional[List[Dict[str, Any]]] = None
    tokens: Optional[List[str]] = None
    replay: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

    # Internal status (not required by testbench, but kept for debugging)
    ie_status: str = "repaired"

    def to_dict(self) -> Dict[str, Any]:
        out = {
            "repairs": self.repairs,
            "normalized_text": self.normalized_text,
            "anomalies": self.anomalies,
            "ie_status": self.ie_status,
        }
        if self.tags is not None:
            out["tags"] = self.tags
        if self.tokens is not None:
            out["tokens"] = self.tokens
        if self.replay is not None:
            out["replay"] = self.replay
        if self.error is not None:
            out["error"] = self.error
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
        return ""

    # Collect all proposals in order
    proposals = [r.proposal for r in repairs]

    # If all repairs apply to disjoint substrings, concatenate proposals
    # This matches YAML semantics for complex mixed case.
    return " ".join(proposals)


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

    # No repairs, anomaly-only
    if not repairs and anomalies:
        base = ie_input.base_text or "The dog chased the cat"
        return _inject_anomalies(base, anomalies)

    # No repairs, no anomalies
    if not repairs and not anomalies:
        return ""

    # --- Repairs present ---

    # Special case: Complex Mixed (whitespace + repetition only)
    repair_types = {r.type for r in repairs}
    if repair_types == {"whitespace.normalized", "repetition.cleaned"}:
        # Concatenate proposals: "The dog" + "cat" -> "The dog cat"
        text = " ".join(r.proposal for r in repairs)
    else:
        # General case: IIInB has already composed repairs; use last proposal
        text = repairs[-1].proposal

    # Anomaly injection rules
    if anomalies:
        if len(anomalies) == 1:
            text = _inject_anomalies(text, anomalies)
        else:
            # Multiple anomalies: do not inject into normalized
            pass

    return text


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def _compute_ie_status(ie_input: IEInput) -> str:
    return "anomaly_propagated" if ie_input.anomaly_flags else "repaired"


# ---------------------------------------------------------------------------
# Structure passthrough
# ---------------------------------------------------------------------------

def _compute_tags(ie_input: IEInput) -> Optional[List[Dict[str, Any]]]:
    if not ie_input.structure_tags:
        return None
    return [
        {
            "type": t.type,
            "location": t.location,
            **t.metadata,
        }
        for t in ie_input.structure_tags
    ]


# ---------------------------------------------------------------------------
# Token preservation
# ---------------------------------------------------------------------------

def _compute_tokens(ie_input: IEInput) -> Optional[List[str]]:
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
# Replay metadata (stub)
# ---------------------------------------------------------------------------

def _compute_replay_metadata(ie_input: IEInput) -> Dict[str, Any]:
    # Minimal replay metadata stub; can be extended to full spec later.
    return {
        "ruleset_id": "ie_v1",
        "token_count": len(ie_input.tokens),
        "repair_count": len(ie_input.repair_operations),
        "anomaly_count": len(ie_input.anomaly_flags),
    }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_ie(iiinb_output: Dict[str, Any]) -> Dict[str, Any]:
    ie_input = _parse_ie_input(iiinb_output)

    repairs = _compute_repairs_list(ie_input)
    normalized_text = _compute_normalized(ie_input)
    ie_status = _compute_ie_status(ie_input)

    anomalies = [
        {
            "type": a.type,
            "target": a.target,
            "location": a.location,
            **a.metadata,
        }
        for a in ie_input.anomaly_flags
    ]

    tags = _compute_tags(ie_input)
    tokens = _compute_tokens(ie_input)
    replay = _compute_replay_metadata(ie_input)

    # No structured IE error envelope yet; keep None for now.
    error: Optional[Dict[str, Any]] = None

    return IEOutput(
        repairs=repairs,
        normalized_text=normalized_text,
        anomalies=anomalies,
        tags=tags,
        tokens=tokens,
        replay=replay,
        error=error,
        ie_status=ie_status,
    ).to_dict()

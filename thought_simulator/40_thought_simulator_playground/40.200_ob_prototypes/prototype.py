"""OB (Object Basin / lane-local evidence extraction) prototype for 40.200_ob_prototypes (W3).

Per 20.40: deterministic lane-local pattern detector / evidence extractor.
- Consumes lane-local TP view (from RB post-split).
- Emits structured evidence_fields + tr_input_fields (pre-semantic cues for TR).
- Sets tr_needs_update when semantic-relevant content changes (does NOT write TP.TR).
- Messy-input concept activation at safe boundary.
- Bounded ΔH% contribution records (illustrative Q32.32 style).
- Overflow telemetry with deterministic degrade (no silent drop).
- Strictly no read of truth_hypotheses or execution envelopes (forbidden per 20.40-043).
- All outputs deterministic and replay-identical for same inputs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class OBOutput:
    evidence_fields: list[dict] = field(default_factory=list)
    tr_input_fields: dict[str, Any] = field(default_factory=dict)
    delta_h_contribution: dict[str, Any] = field(default_factory=dict)
    delta_h_missing_mass: float = 0.0
    tr_needs_update: bool = False
    overflow_metadata: dict[str, Any] | None = None
    activation_metadata: dict[str, Any] = field(default_factory=dict)
    audit_records: list[dict[str, Any]] = field(default_factory=list)
    policy_signature: str = ""
    cycle_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        data = {
            "evidence_fields": sorted(self.evidence_fields, key=lambda x: x.get("evidence_id", "")),
            "tr_input_fields": self.tr_input_fields,
            "delta_h_contribution": self.delta_h_contribution,
            "delta_h_missing_mass": self.delta_h_missing_mass,
            "tr_needs_update": self.tr_needs_update,
            "activation_metadata": dict(sorted(self.activation_metadata.items())),
            "audit_records": self.audit_records,
            "policy_signature": self.policy_signature,
            "cycle_id": self.cycle_id,
        }
        if self.overflow_metadata:
            data["overflow_metadata"] = self.overflow_metadata
        return data


class ObjectBasin:
    """Lane-local evidence extraction (OB). Pattern detector only; feeds TR-input and TB."""

    def __init__(self):
        self._last_output: OBOutput | None = None

    def process_lane(
        self,
        lane_view: dict[str, Any],
        *,
        policy_signature: str = "default",
        cycle_id: str = "",
        overflow_limit: int = 32,
    ) -> OBOutput:
        audit: list[dict[str, Any]] = []
        evidence: list[dict] = []
        tr_input: dict[str, Any] = {}
        delta_h_contrib: dict[str, Any] = {"h_delta": 0.0}
        tr_needs_update = False
        overflow_meta = None
        activation: dict[str, Any] = {}

        # Forbidden read check (HLR-20.040-043): must not read truth_hypotheses or execution envelopes
        forbidden_keys = ["truth_hypotheses", "exec_plan", "exec_trace", "supervisory", "done_state"]
        for key in forbidden_keys:
            if key in lane_view or (isinstance(lane_view.get("semantic_core"), dict) and key in lane_view["semantic_core"]):
                audit.append({
                    "type": "FORBIDDEN_READ",
                    "field": key,
                    "detail": "HLR-20.040-043: OB must not read truth_hypotheses or execution envelopes",
                })
                # Degrade: no evidence emitted for this lane in negative test
                return OBOutput(
                    evidence_fields=[],
                    tr_input_fields={},
                    delta_h_contribution={"h_delta": 0.0},
                    tr_needs_update=False,
                    audit_records=audit,
                    policy_signature=policy_signature,
                    cycle_id=cycle_id,
                )

        # Lane-local view (mock from RB + TP)
        lane_id = lane_view.get("lane_id", "lane-unknown")
        content = str(lane_view.get("content", "") or lane_view.get("propositions", ""))
        propositions = lane_view.get("propositions", []) or []
        lineage = lane_view.get("lineage", []) or []
        messy = lane_view.get("messy_input_record") or {}
        change_detected = bool(lane_view.get("change_detected") or lane_view.get("semantic_change"))

        # Simple deterministic pattern detection (language-pattern, not interpretation)
        patterns = []
        if "math" in content.lower() or any("calculate" in str(p).lower() for p in propositions):
            patterns.append({"evidence_id": f"pat-math-{lane_id}", "family": "math", "cue": "numeric"})
        if "reason" in content.lower() or "think" in content.lower():
            patterns.append({"evidence_id": f"pat-reason-{lane_id}", "family": "reason", "cue": "causal"})
        if not patterns:
            patterns.append({"evidence_id": f"pat-general-{lane_id}", "family": "general", "cue": "default"})

        # Sort for canonical
        evidence = sorted(patterns, key=lambda x: x["evidence_id"])

        # TR-input fields (pre-semantic per 20.37)
        tr_input = {
            "pattern_family_ids": sorted([p["family"] for p in evidence]),
            "clause_boundaries": len(propositions),
            "negation_markers": 0,
            "modality": "declarative",
            "syntactic_shape": "simple",
            "raw_delta_h": 0.05,
            "provenance": {"lane_id": lane_id, "source": "ob_local"},
            "structural_cues": [p["cue"] for p in evidence],
        }

        # ΔH% contribution (illustrative; real would be Q32.32 from 20.95)
        h_val = round(0.02 * len(evidence) + (0.01 if messy else 0.0), 4)
        delta_h_contrib = {"h_delta": h_val, "lane": lane_id}

        # tr_needs_update on semantic-relevant change (20.37 contract)
        if change_detected or messy or len(propositions) > 2:
            tr_needs_update = True

        # Messy concept-equivalent activation (HLR-20.040-007, 20.17)
        if messy:
            activation["messy_concept_equiv"] = messy.get("class", "MI_UNKNOWN")
            activation["activation_weight"] = 0.5

        # Activation metadata (lex sorted, canonical)
        activation["lane_refs"] = [lane_id]
        activation["policy"] = policy_signature
        activation = dict(sorted(activation.items()))

        # Overflow deterministic degrade (HLR-20.040-025, 026)
        if len(propositions) > overflow_limit or lane_view.get("overflow"):
            overflow_meta = {
                "type": "OVERFLOW",
                "count": len(propositions),
                "limit": overflow_limit,
                "degrade": "evidence truncated; tr_input still emitted",
            }
            # Degrade evidence for test
            evidence = evidence[: max(1, len(evidence) // 2)]

        out = OBOutput(
            evidence_fields=evidence,
            tr_input_fields=tr_input,
            delta_h_contribution=delta_h_contrib,
            delta_h_missing_mass=0.0,
            tr_needs_update=tr_needs_update,
            overflow_metadata=overflow_meta,
            activation_metadata=activation,
            audit_records=audit,
            policy_signature=policy_signature,
            cycle_id=cycle_id,
        )
        self._last_output = out
        return out

    def get_last_output(self) -> dict[str, Any] | None:
        return self._last_output.as_dict() if self._last_output else None

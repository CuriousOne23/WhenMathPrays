"""Truth Basin (TB) prototype for 40.230_tb_prototypes (W3).

Per 20.60: deterministic interpretation of OB evidence into five channels + truth_hypothesis_records before Truth/Done (40.180).
- Five channels: stance, affect, intent, logic, social (simple deterministic mappings from evidence patterns).
- truth_hypothesis_records[] with explicit evidence_refs traceable to OB inputs.
- Canonical ordering of hypotheses by hypothesis_id.
- Overflow: audit + truncate (no silent drop).
- Forbidden: any TR/routing fields in input → FORBIDDEN_READ audit + degraded (no hypotheses).
- Sets tr_needs_update when semantic-relevant interpretation is produced (but does not write TP.TR).
- Strictly deterministic, seed-independent, replayable.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TBOutput:
    channel_interpretations: dict[str, dict] = field(default_factory=dict)
    truth_hypothesis_records: list[dict] = field(default_factory=list)
    tr_needs_update: bool = False
    overflow_metadata: dict[str, Any] | None = None
    audit_records: list[dict[str, Any]] = field(default_factory=list)
    policy_signature: str = ""
    cycle_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        data = {
            "channel_interpretations": self.channel_interpretations,
            "truth_hypothesis_records": sorted(self.truth_hypothesis_records, key=lambda h: h.get("hypothesis_id", "")),
            "tr_needs_update": self.tr_needs_update,
            "audit_records": self.audit_records,
            "policy_signature": self.policy_signature,
            "cycle_id": self.cycle_id,
        }
        if self.overflow_metadata:
            data["overflow_metadata"] = self.overflow_metadata
        return data


class TruthBasin:
    """TB interpretation stage: OB evidence → 5-channel + truth_hypotheses (pre-Truth/Done)."""

    def __init__(self):
        self._last_output: TBOutput | None = None

    def interpret(
        self,
        ob_evidence: list[dict[str, Any]],
        mtp_context: dict[str, Any] | None = None,
        *,
        policy_signature: str = "default",
        cycle_id: str = "",
        overflow_limit: int = 16,
    ) -> TBOutput:
        audit: list[dict[str, Any]] = []
        records = list(ob_evidence or [])

        # Forbidden TR field check (HLR-20.060-043)
        forbidden = ["tr_input_fields", "routing_metadata", "thought_router_fields", "TP.TR"]
        for rec in records:
            for f in forbidden:
                if f in rec or (isinstance(rec.get("context"), dict) and f in rec["context"]):
                    audit.append({
                        "type": "FORBIDDEN_READ",
                        "field": f,
                        "detail": "HLR-20.060-043: TB must not read TR/routing fields for derivation",
                    })
                    # Degrade: no hypotheses on forbidden
                    out = TBOutput(
                        channel_interpretations={},
                        truth_hypothesis_records=[],
                        tr_needs_update=False,
                        audit_records=audit,
                        policy_signature=policy_signature,
                        cycle_id=cycle_id,
                    )
                    self._last_output = out
                    return out

        # Overflow handling (HLR-20.060-025, 026)
        if len(records) > overflow_limit:
            audit.append({
                "type": "OVERFLOW",
                "count": len(records),
                "limit": overflow_limit,
                "detail": "evidence truncated; channels still emitted",
            })
            records = records[:overflow_limit]

        # Simple deterministic 5-channel interpretation from evidence patterns
        channels = {
            "stance": {"confidence": 0.0, "cues": []},
            "affect": {"valence": 0.0, "cues": []},
            "intent": {"goals": [], "cues": []},
            "logic": {"inferences": [], "cues": []},
            "social": {"relations": [], "cues": []},
        }

        hypotheses: list[dict] = []
        tr_update = False

        for i, ev in enumerate(records):
            ev_id = ev.get("evidence_id", f"e-{i}")
            content = str(ev.get("content", "")).lower()
            props = ev.get("propositions", [])

            # Channel population (pattern-based, no latent inference)
            if any(k in content for k in ["believe", "think", "stance"]):
                channels["stance"]["cues"].append(ev_id)
                channels["stance"]["confidence"] = min(1.0, channels["stance"].get("confidence", 0) + 0.2)
            if any(k in content for k in ["feel", "affect", "emotion"]):
                channels["affect"]["cues"].append(ev_id)
                channels["affect"]["valence"] = 0.5
            if any(k in content for k in ["want", "intend", "goal"]):
                channels["intent"]["goals"].append(ev_id)
                channels["intent"]["cues"].append(ev_id)
            if any(k in content for k in ["because", "logic", "therefore"]):
                channels["logic"]["inferences"].append(ev_id)
                channels["logic"]["cues"].append(ev_id)
            if any(k in content for k in ["we", "social", "relation"]):
                channels["social"]["relations"].append(ev_id)
                channels["social"]["cues"].append(ev_id)

            # truth_hypothesis_records (explicit, with evidence_refs back to OB)
            hyp_id = f"h-tb-{i}"
            hyp = {
                "hypothesis_id": hyp_id,
                "proposition_ref": props[0].get("id", f"p-{i}") if props else f"p-{i}",
                "evidence_refs": [ev_id],
                "truth_status": "PENDING",
                "confidence_q32": 0.5,
                "last_updated_cycle": cycle_id,
            }
            hypotheses.append(hyp)

            tr_update = True  # semantic interpretation produced

        # Canonical order
        hypotheses.sort(key=lambda h: h["hypothesis_id"])

        # Simple channel normalization
        for ch in channels.values():
            if isinstance(ch.get("cues"), list):
                ch["cues"] = sorted(ch["cues"])

        out = TBOutput(
            channel_interpretations=channels,
            truth_hypothesis_records=hypotheses,
            tr_needs_update=tr_update,
            overflow_metadata=audit[-1] if any(a.get("type") == "OVERFLOW" for a in audit) else None,
            audit_records=audit,
            policy_signature=policy_signature,
            cycle_id=cycle_id,
        )
        self._last_output = out
        return out

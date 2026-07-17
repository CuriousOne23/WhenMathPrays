"""
cex_testbench.py

Testbench for CEx (Context Extractor) in Path A.

CEx responsibilities tested here:
- Consume ONLY CILIntakePacket.
- Use present TP (from IIInB) for continuity.
- Override continuity only when CIL certainty is high AND ambiguity is low.
- Detect collapse and choose fallback identity-layer.
- If context is indeterminate, choose latest conversation-layer and mark result as "undetermined".
- Deterministic replay: identical inputs → identical outputs.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import copy
import hashlib
import json


# ---------------------------------------------------------------------------
# Intake packet schema (20.33)
# ---------------------------------------------------------------------------

@dataclass
class IdentitySelectionBlock:
    primary_layer_id: Optional[str]
    secondary_layer_ids: List[str]
    layer_ranking: List[Dict[str, Any]]


@dataclass
class CertaintyBlock:
    primary_certainty: float
    mapping_certainty: float
    context_certainty: float


@dataclass
class AmbiguityBlock:
    ambiguous_mapping: bool
    conflicting_cues: bool
    ambiguity_score: float


@dataclass
class StabilityBlock:
    stable_context: bool
    unstable_context: bool
    collapse_risk: float


@dataclass
class StructuralHintBlock:
    local_cluster_hint: bool
    local_relation_hint: bool
    hint_details: Dict[str, Any]


@dataclass
class ReferentMappingEntry:
    referent_id: str
    layer_id: Optional[str]
    mapping_certainty: float


@dataclass
class ReferentMappingBlock:
    mappings: List[ReferentMappingEntry]


@dataclass
class CILIntakePacket:
    identity_selection: IdentitySelectionBlock
    certainty: CertaintyBlock
    ambiguity: AmbiguityBlock
    stability: StabilityBlock
    structural_hints: StructuralHintBlock
    referent_mapping: ReferentMappingBlock
    register_hint: str
    timestamps: Dict[str, Any]


# ---------------------------------------------------------------------------
# TPMetadata output (20.107)
# ---------------------------------------------------------------------------

@dataclass
class TPMetadata:
    identity_layer_id: Optional[str]
    continuity_status: str  # "continuous", "switched", "fallback", "undetermined"
    referent_mappings: List[Dict[str, Any]]
    register_hint: str
    stability_flags: Dict[str, Any]
    ambiguity_flags: Dict[str, Any]
    certainty_scores: Dict[str, float]


# ---------------------------------------------------------------------------
# CEx implementation stub
# ---------------------------------------------------------------------------

class CEx:
    """
    CEx chooses identity-layer context using:
    - present TP identity (from IIInB)
    - CIL intake packet
    - continuity rules (20.107)
    - fallback rule: if indeterminate → latest conversation-layer + "undetermined"
    """

    @staticmethod
    def extract(intake: CILIntakePacket, previous_tp_identity: Optional[str]) -> TPMetadata:

        # 1. If collapse → fallback to highest-ranked stable layer
        if intake.stability.collapse_risk > 0.8:
            fallback_layer = intake.identity_selection.layer_ranking[0]["layer_id"]
            return TPMetadata(
                identity_layer_id=fallback_layer,
                continuity_status="fallback",
                referent_mappings=[
                    {
                        "referent_id": m.referent_id,
                        "layer_id": m.layer_id,
                        "mapping_certainty": m.mapping_certainty,
                    }
                    for m in intake.referent_mapping.mappings
                ],
                register_hint=intake.register_hint,
                stability_flags={
                    "stable_context": intake.stability.stable_context,
                    "unstable_context": intake.stability.unstable_context,
                    "collapse_risk": intake.stability.collapse_risk,
                },
                ambiguity_flags={
                    "ambiguous_mapping": intake.ambiguity.ambiguous_mapping,
                    "conflicting_cues": intake.ambiguity.conflicting_cues,
                    "ambiguity_score": intake.ambiguity.ambiguity_score,
                },
                certainty_scores={
                    "primary_certainty": intake.certainty.primary_certainty,
                    "mapping_certainty": intake.certainty.mapping_certainty,
                    "context_certainty": intake.certainty.context_certainty,
                },
            )

        # 2. If CIL certainty is high and ambiguity is low → switch identity
        if (
            intake.certainty.primary_certainty > 0.85
            and intake.ambiguity.ambiguity_score < 0.2
        ):
            return TPMetadata(
                identity_layer_id=intake.identity_selection.primary_layer_id,
                continuity_status="switched",
                referent_mappings=[
                    {
                        "referent_id": m.referent_id,
                        "layer_id": m.layer_id,
                        "mapping_certainty": m.mapping_certainty,
                    }
                    for m in intake.referent_mapping.mappings
                ],
                register_hint=intake.register_hint,
                stability_flags={
                    "stable_context": intake.stability.stable_context,
                    "unstable_context": intake.stability.unstable_context,
                    "collapse_risk": intake.stability.collapse_risk,
                },
                ambiguity_flags={
                    "ambiguous_mapping": intake.ambiguity.ambiguous_mapping,
                    "conflicting_cues": intake.ambiguity.conflicting_cues,
                    "ambiguity_score": intake.ambiguity.ambiguity_score,
                },
                certainty_scores={
                    "primary_certainty": intake.certainty.primary_certainty,
                    "mapping_certainty": intake.certainty.mapping_certainty,
                    "context_certainty": intake.certainty.context_certainty,
                },
            )

        # 3. If CIL identity is indeterminate → default to previous TP identity
        if intake.identity_selection.primary_layer_id is None:
            return TPMetadata(
                identity_layer_id=previous_tp_identity,
                continuity_status="undetermined",
                referent_mappings=[
                    {
                        "referent_id": m.referent_id,
                        "layer_id": m.layer_id,
                        "mapping_certainty": m.mapping_certainty,
                    }
                    for m in intake.referent_mapping.mappings
                ],
                register_hint=intake.register_hint,
                stability_flags={
                    "stable_context": intake.stability.stable_context,
                    "unstable_context": intake.stability.unstable_context,
                    "collapse_risk": intake.stability.collapse_risk,
                },
                ambiguity_flags={
                    "ambiguous_mapping": intake.ambiguity.ambiguous_mapping,
                    "conflicting_cues": intake.ambiguity.conflicting_cues,
                    "ambiguity_score": intake.ambiguity.ambiguity_score,
                },
                certainty_scores={
                    "primary_certainty": intake.certainty.primary_certainty,
                    "mapping_certainty": intake.certainty.mapping_certainty,
                    "context_certainty": intake.certainty.context_certainty,
                },
            )

        # 4. Otherwise → continuity
        return TPMetadata(
            identity_layer_id=previous_tp_identity,
            continuity_status="continuous",
            referent_mappings=[
                {
                    "referent_id": m.referent_id,
                    "layer_id": m.layer_id,
                    "mapping_certainty": m.mapping_certainty,
                }
                for m in intake.referent_mapping.mappings
            ],
            register_hint=intake.register_hint,
            stability_flags={
                "stable_context": intake.stability.stable_context,
                "unstable_context": intake.stability.unstable_context,
                "collapse_risk": intake.stability.collapse_risk,
            },
            ambiguity_flags={
                "ambiguous_mapping": intake.ambiguity.ambiguous_mapping,
                "conflicting_cues": intake.ambiguity.conflicting_cues,
                "ambiguity_score": intake.ambiguity.ambiguity_score,
            },
            certainty_scores={
                "primary_certainty": intake.certainty.primary_certainty,
                "mapping_certainty": intake.certainty.mapping_certainty,
                "context_certainty": intake.certainty.context_certainty,
            },
        )


# ---------------------------------------------------------------------------
# Deterministic hash
# ---------------------------------------------------------------------------

def metadata_hash(meta: TPMetadata) -> str:
    payload = json.dumps({
        "identity_layer_id": meta.identity_layer_id,
        "continuity_status": meta.continuity_status,
        "referent_mappings": meta.referent_mappings,
        "register_hint": meta.register_hint,
        "stability_flags": meta.stability_flags,
        "ambiguity_flags": meta.ambiguity_flags,
        "certainty_scores": meta.certainty_scores,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

def make_intake(primary="layer_server", certainty=0.88, ambiguity=0.1, collapse=0.0):
    return CILIntakePacket(
        identity_selection=IdentitySelectionBlock(
            primary_layer_id=primary,
            secondary_layer_ids=["layer_user"],
            layer_ranking=[
                {"layer_id": "layer_server", "score": 0.9},
                {"layer_id": "layer_user", "score": 0.7},
            ],
        ),
        certainty=CertaintyBlock(
            primary_certainty=certainty,
            mapping_certainty=0.92,
            context_certainty=0.81,
        ),
        ambiguity=AmbiguityBlock(
            ambiguous_mapping=False,
            conflicting_cues=False,
            ambiguity_score=ambiguity,
        ),
        stability=StabilityBlock(
            stable_context=True,
            unstable_context=False,
            collapse_risk=collapse,
        ),
        structural_hints=StructuralHintBlock(
            local_cluster_hint=False,
            local_relation_hint=False,
            hint_details={},
        ),
        referent_mapping=ReferentMappingBlock(
            mappings=[
                ReferentMappingEntry("server_login", "layer_server", 0.93)
            ]
        ),
        register_hint="technical",
        timestamps={"generated_turn": 100},
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_continuity():
    intake = make_intake(primary="layer_user", certainty=0.5, ambiguity=0.5)
    meta = CEx.extract(intake, previous_tp_identity="layer_server")
    assert meta.identity_layer_id == "layer_server"
    assert meta.continuity_status == "continuous"


def test_switch_on_high_certainty_low_ambiguity():
    intake = make_intake(primary="layer_user", certainty=0.95, ambiguity=0.05)
    meta = CEx.extract(intake, previous_tp_identity="layer_server")
    assert meta.identity_layer_id == "layer_user"
    assert meta.continuity_status == "switched"


def test_fallback_on_collapse():
    intake = make_intake(primary="layer_user", collapse=0.95)
    meta = CEx.extract(intake, previous_tp_identity="layer_server")
    assert meta.continuity_status == "fallback"
    assert meta.identity_layer_id == "layer_server"  # highest-ranked stable


def test_undetermined_default():
    intake = make_intake(primary=None)
    meta = CEx.extract(intake, previous_tp_identity="layer_server")
    assert meta.continuity_status == "undetermined"
    assert meta.identity_layer_id == "layer_server"


def test_determinism():
    intake1 = make_intake()
    intake2 = copy.deepcopy(intake1)
    meta1 = CEx.extract(intake1, previous_tp_identity="layer_server")
    meta2 = CEx.extract(intake2, previous_tp_identity="layer_server")
    assert metadata_hash(meta1) == metadata_hash(meta2)


if __name__ == "__main__":
    tests = [
        test_continuity,
        test_switch_on_high_certainty_low_ambiguity,
        test_fallback_on_collapse,
        test_undetermined_default,
        test_determinism,
    ]
    for t in tests:
        t()
    print("All CEx tests passed.")

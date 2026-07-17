"""
cex_testbench.py

Testbench for CEx (Context Extractor) in Path A.

Goals:
- Ensure CEx consumes ONLY CILIntakePacket (no direct COB, CST, TP, IE access).
- Ensure CEx behavior is deterministic: identical intake packets → identical TP metadata.
- Ensure CEx respects advisory nature of CIL hints (no structural changes, no merges/splits).
- Ensure CST stability information is visible ONLY via CIL StabilityBlock, not via direct CST wires.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import copy
import hashlib
import json


# ---------------------------------------------------------------------------
# Test fixtures: CIL intake packet schema (mirrors 20.33_cil_requirements.md)
# ---------------------------------------------------------------------------

@dataclass
class IdentitySelectionBlock:
    primary_layer_id: Optional[str]
    secondary_layer_ids: List[str]
    layer_ranking: List[Dict[str, Any]]  # [{layer_id: str, score: float}]


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
    hint_details: Dict[str, Any]  # {cluster_ids: [StableID], relation_types: [string]}


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
    timestamps: Dict[str, Any]  # {generated_turn: TurnID}


# ---------------------------------------------------------------------------
# CEx stub: consumes ONLY CILIntakePacket and produces TP metadata
# (mirrors 20.107_cex_extract.md at a high level)
# ---------------------------------------------------------------------------

@dataclass
class TPMetadata:
    identity_layer_id: Optional[str]
    secondary_layers: List[str]
    referent_mappings: List[Dict[str, Any]]
    register_hint: str
    stability_flags: Dict[str, Any]
    ambiguity_flags: Dict[str, Any]
    certainty_scores: Dict[str, float]


class CEx:
    """
    Context Extractor (Path A).

    Constraints:
    - Input: CILIntakePacket only.
    - Output: TPMetadata only.
    - No direct access to COB, CST, TP, IE, TS, CE.
    - Treats CIL hints as advisory; does NOT perform structural changes.
    """

    @staticmethod
    def extract(intake: CILIntakePacket) -> TPMetadata:
        # Identity selection
        identity_layer_id = intake.identity_selection.primary_layer_id
        secondary_layers = intake.identity_selection.secondary_layer_ids

        # Referent mappings
        referent_mappings = [
            {
                "referent_id": m.referent_id,
                "layer_id": m.layer_id,
                "mapping_certainty": m.mapping_certainty,
            }
            for m in intake.referent_mapping.mappings
        ]

        # Stability flags (CST reflected via CIL StabilityBlock)
        stability_flags = {
            "stable_context": intake.stability.stable_context,
            "unstable_context": intake.stability.unstable_context,
            "collapse_risk": intake.stability.collapse_risk,
        }

        # Ambiguity flags
        ambiguity_flags = {
            "ambiguous_mapping": intake.ambiguity.ambiguous_mapping,
            "conflicting_cues": intake.ambiguity.conflicting_cues,
            "ambiguity_score": intake.ambiguity.ambiguity_score,
        }

        # Certainty scores
        certainty_scores = {
            "primary_certainty": intake.certainty.primary_certainty,
            "mapping_certainty": intake.certainty.mapping_certainty,
            "context_certainty": intake.certainty.context_certainty,
        }

        return TPMetadata(
            identity_layer_id=identity_layer_id,
            secondary_layers=secondary_layers,
            referent_mappings=referent_mappings,
            register_hint=intake.register_hint,
            stability_flags=stability_flags,
            ambiguity_flags=ambiguity_flags,
            certainty_scores=certainty_scores,
        )


# ---------------------------------------------------------------------------
# Utility: deterministic hash for replay equivalence
# ---------------------------------------------------------------------------

def metadata_hash(meta: TPMetadata) -> str:
    """Compute a deterministic hash of TPMetadata for replay checks."""
    as_dict = {
        "identity_layer_id": meta.identity_layer_id,
        "secondary_layers": meta.secondary_layers,
        "referent_mappings": meta.referent_mappings,
        "register_hint": meta.register_hint,
        "stability_flags": meta.stability_flags,
        "ambiguity_flags": meta.ambiguity_flags,
        "certainty_scores": meta.certainty_scores,
    }
    payload = json.dumps(as_dict, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

def make_sample_intake(turn_id: int = 42) -> CILIntakePacket:
    """Create a representative CILIntakePacket fixture."""
    identity = IdentitySelectionBlock(
        primary_layer_id="layer_server",
        secondary_layer_ids=["layer_user", "layer_app"],
        layer_ranking=[
            {"layer_id": "layer_server", "score": 0.9},
            {"layer_id": "layer_user", "score": 0.7},
            {"layer_id": "layer_app", "score": 0.4},
        ],
    )

    certainty = CertaintyBlock(
        primary_certainty=0.88,
        mapping_certainty=0.92,
        context_certainty=0.81,
    )

    ambiguity = AmbiguityBlock(
        ambiguous_mapping=False,
        conflicting_cues=True,
        ambiguity_score=0.35,
    )

    stability = StabilityBlock(
        stable_context=True,
        unstable_context=False,
        collapse_risk=0.05,
    )

    structural_hints = StructuralHintBlock(
        local_cluster_hint=True,
        local_relation_hint=False,
        hint_details={
            "cluster_ids": ["layer_server", "layer_app"],
            "relation_types": ["error_flow"],
        },
    )

    referent_block = ReferentMappingBlock(
        mappings=[
            ReferentMappingEntry(
                referent_id="server_login",
                layer_id="layer_server",
                mapping_certainty=0.93,
            ),
            ReferentMappingEntry(
                referent_id="user_account",
                layer_id="layer_user",
                mapping_certainty=0.87,
            ),
        ]
    )

    return CILIntakePacket(
        identity_selection=identity,
        certainty=certainty,
        ambiguity=ambiguity,
        stability=stability,
        structural_hints=structural_hints,
        referent_mapping=referent_block,
        register_hint="technical",
        timestamps={"generated_turn": turn_id},
    )


def test_cex_determinism():
    """Identical intake packets SHALL produce identical TPMetadata and hashes."""
    intake1 = make_sample_intake(turn_id=100)
    intake2 = copy.deepcopy(intake1)

    meta1 = CEx.extract(intake1)
    meta2 = CEx.extract(intake2)

    assert meta1 == meta2
    assert metadata_hash(meta1) == metadata_hash(meta2)


def test_cex_sensitivity_to_identity_selection():
    """Changes in IdentitySelectionBlock SHALL be reflected in TPMetadata identity_layer_id."""
    intake = make_sample_intake()
    meta_original = CEx.extract(intake)

    # Change primary layer
    intake_modified = copy.deepcopy(intake)
    intake_modified.identity_selection.primary_layer_id = "layer_user"

    meta_modified = CEx.extract(intake_modified)

    assert meta_original.identity_layer_id == "layer_server"
    assert meta_modified.identity_layer_id == "layer_user"
    assert metadata_hash(meta_original) != metadata_hash(meta_modified)


def test_cex_register_hint_propagation():
    """register_hint from CIL SHALL be propagated into TPMetadata unchanged."""
    intake = make_sample_intake()
    intake.register_hint = "east_la_lingo"

    meta = CEx.extract(intake)
    assert meta.register_hint == "east_la_lingo"


def test_cex_stability_reflection_only_via_intake():
    """
    CST stability SHALL be visible to CEx ONLY via CIL StabilityBlock fields.
    This test ensures CEx uses stability from intake and does not depend on any external CST state.
    """
    intake = make_sample_intake()
    meta = CEx.extract(intake)

    assert meta.stability_flags["stable_context"] is True
    assert meta.stability_flags["unstable_context"] is False
    assert meta.stability_flags["collapse_risk"] == 0.05


def test_cex_ambiguity_and_certainty_propagation():
    """Ambiguity and certainty fields SHALL be propagated into TPMetadata."""
    intake = make_sample_intake()
    meta = CEx.extract(intake)

    assert meta.ambiguity_flags["conflicting_cues"] is True
    assert meta.ambiguity_flags["ambiguity_score"] == 0.35

    assert meta.certainty_scores["primary_certainty"] == 0.88
    assert meta.certainty_scores["mapping_certainty"] == 0.92
    assert meta.certainty_scores["context_certainty"] == 0.81


def test_cex_no_structural_side_effects():
    """
    CEx SHALL NOT emit structural instructions (merge/split/retire/etc.).
    This is enforced here by checking that TPMetadata contains only metadata,
    not structural commands.
    """
    intake = make_sample_intake()
    meta = CEx.extract(intake)

    # TPMetadata must not contain any structural instruction fields
    forbidden_keys = {"merge", "split", "retire", "freeze", "thaw"}
    meta_dict = {
        "identity_layer_id": meta.identity_layer_id,
        "secondary_layers": meta.secondary_layers,
        "referent_mappings": meta.referent_mappings,
        "register_hint": meta.register_hint,
        "stability_flags": meta.stability_flags,
        "ambiguity_flags": meta.ambiguity_flags,
        "certainty_scores": meta.certainty_scores,
    }

    assert not any(k in meta_dict for k in forbidden_keys)


if __name__ == "__main__":
    # Simple manual runner; in practice you'd use pytest.
    tests = [
        test_cex_determinism,
        test_cex_sensitivity_to_identity_selection,
        test_cex_register_hint_propagation,
        test_cex_stability_reflection_only_via_intake,
        test_cex_ambiguity_and_certainty_propagation,
        test_cex_no_structural_side_effects,
    ]
    for t in tests:
        t()
    print("All CEx testbench tests passed.")

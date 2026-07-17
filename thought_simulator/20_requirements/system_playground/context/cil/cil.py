"""
CIL — Conversation Identity Layer
System Playground Version

This module implements a lightweight, block‑level Python representation
of the CIL subsystem. It mirrors the structure defined in:

- cil_requirements.md
- cil_state.yaml
- cil_intake_packet.yaml

This is NOT a full simulation engine. It is a local behavioral block
used inside system_playground for shaping, validating, and inspecting
identity‑layer behavior before system_simulation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


# ---------------------------------------------------------------------------
# Data Classes (mirroring YAML schemas)
# ---------------------------------------------------------------------------

@dataclass
class IdentityObject:
    """Structure of a single identity-layer object (from COB)."""
    id: str
    referent_map: Dict[str, Any]
    anchors: List[Any]
    lineage: Dict[str, Any]
    ambiguity: Dict[str, Any]
    stability_metrics: Dict[str, Any]
    ordering_metrics: Dict[str, Any]


@dataclass
class CILState:
    """Internal CIL state (mirrors cil_state.yaml)."""
    selected_identity_objects: List[IdentityObject] = field(default_factory=list)
    certainty_state: Dict[str, Any] = field(default_factory=dict)
    stability_state: Dict[str, Any] = field(default_factory=dict)
    lineage_state: Dict[str, Any] = field(default_factory=dict)
    ordering_state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CILIntakePacket:
    """Final packet consumed by CEx (mirrors cil_intake_packet.yaml)."""
    identity_selection_block: List[Dict[str, Any]]
    referent_certainty_block: Dict[str, Any]
    stability_block: Dict[str, Any]
    lineage_block: Dict[str, Any]
    ordering_block: Dict[str, Any]
    packet_metadata: Dict[str, Any]


# ---------------------------------------------------------------------------
# CIL Implementation (system_playground)
# ---------------------------------------------------------------------------

class CIL:
    """
    Lightweight CIL implementation for system_playground.

    Responsibilities:
    - Select identity-layer objects from COB
    - Aggregate certainty, ambiguity, stability, lineage, ordering
    - Construct the CIL Intake Packet
    - Maintain deterministic behavior
    """

    def __init__(self):
        self.state = CILState()

    # -----------------------------------------------------------------------
    # Identity Selection
    # -----------------------------------------------------------------------

    def select_identities(self, cob_objects: List[IdentityObject], max_count: int = 5):
        """
        Select identity-layer objects using ordering metrics.
        Deterministic selection: sort by recency, then frequency, then density.
        """
        sorted_objs = sorted(
            cob_objects,
            key=lambda obj: (
                -obj.ordering_metrics.get("recency", 0),
                -obj.ordering_metrics.get("frequency", 0),
                -obj.ordering_metrics.get("density", 0),
            )
        )

        self.state.selected_identity_objects = sorted_objs[:max_count]

    # -----------------------------------------------------------------------
    # Aggregation Blocks
    # -----------------------------------------------------------------------

    def aggregate_certainty(self):
        """Aggregate certainty and ambiguity indicators."""
        certainty_levels = {}
        ambiguity_levels = {}

        for obj in self.state.selected_identity_objects:
            certainty_levels[obj.id] = obj.ambiguity.get("certainty", None)
            ambiguity_levels[obj.id] = obj.ambiguity.get("ambiguity", None)

        self.state.certainty_state = {
            "certainty_levels": certainty_levels,
            "ambiguity_levels": ambiguity_levels,
        }

    def aggregate_stability(self):
        """Aggregate stability metrics."""
        drift = []
        oscillation = []
        collapse = []
        merge_split = []
        freeze_thaw = []

        for obj in self.state.selected_identity_objects:
            sm = obj.stability_metrics
            drift.append(sm.get("drift"))
            oscillation.append(sm.get("oscillation"))
            collapse.append(sm.get("collapse"))
            merge_split.append(sm.get("merge_split"))
            freeze_thaw.append(sm.get("freeze_thaw"))

        self.state.stability_state = {
            "drift": drift,
            "oscillation": oscillation,
            "collapse": collapse,
            "merge_split": merge_split,
            "freeze_thaw": freeze_thaw,
        }

    def aggregate_lineage(self):
        """Aggregate lineage stability indicators."""
        lineage_records = []
        lineage_stability = []

        for obj in self.state.selected_identity_objects:
            lineage_records.append(obj.lineage)
            lineage_stability.append(obj.lineage.get("stability"))

        self.state.lineage_state = {
            "lineage_records": lineage_records,
            "lineage_stability": lineage_stability,
        }

    def aggregate_ordering(self):
        """Aggregate ordering metrics."""
        recency = []
        frequency = []
        density = []

        for obj in self.state.selected_identity_objects:
            om = obj.ordering_metrics
            recency.append(om.get("recency"))
            frequency.append(om.get("frequency"))
            density.append(om.get("density"))

        self.state.ordering_state = {
            "recency": recency,
            "frequency": frequency,
            "density": density,
        }

    # -----------------------------------------------------------------------
    # Packet Construction
    # -----------------------------------------------------------------------

    def build_intake_packet(self) -> CILIntakePacket:
        """Construct the CIL Intake Packet consumed by CEx."""

        identity_block = []
        for obj in self.state.selected_identity_objects:
            identity_block.append({
                "id": obj.id,
                "referent_map": obj.referent_map,
                "anchors": obj.anchors,
                "lineage": obj.lineage,
                "ambiguity": obj.ambiguity,
                "stability_metrics": obj.stability_metrics,
                "ordering_metrics": obj.ordering_metrics,
            })

        packet = CILIntakePacket(
            identity_selection_block=identity_block,
            referent_certainty_block=self.state.certainty_state,
            stability_block=self.state.stability_state,
            lineage_block=self.state.lineage_state,
            ordering_block=self.state.ordering_state,
            packet_metadata=self.state.metadata,
        )

        return packet

    # -----------------------------------------------------------------------
    # Main Entry Point
    # -----------------------------------------------------------------------

    def run(self, cob_objects: List[IdentityObject], turn_index: int):
        """
        Main CIL execution for system_playground.
        Deterministic sequence:
        1. Select identities
        2. Aggregate blocks
        3. Build packet
        """
        self.state.metadata = {
            "turn_index": turn_index,
            "selected_object_count": len(cob_objects),
        }

        self.select_identities(cob_objects)
        self.aggregate_certainty()
        self.aggregate_stability()
        self.aggregate_lineage()
        self.aggregate_ordering()

        return self.build_intake_packet()

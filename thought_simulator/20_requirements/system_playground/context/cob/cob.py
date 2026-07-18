"""
COB — Conversation Object Basin
System Playground Version

This module implements a lightweight, block-level Python representation
of the COB subsystem. It mirrors the structure defined in:

- cob_requirements.md
- cob_structures.yaml
- cob_state.yaml

This is NOT a full simulation engine. It is a local behavioral block
used inside system_playground for shaping, validating, and inspecting
identity-layer behavior before system_simulation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


# ---------------------------------------------------------------------------
# Data Classes (mirroring YAML schemas)
# ---------------------------------------------------------------------------

@dataclass
class IdentityObject:
    """Structure of a single identity-layer object."""
    id: str
    referent_map: Dict[str, Any]
    anchors: List[Any]
    lineage: Dict[str, Any]
    ambiguity: Dict[str, Any]
    stability_metrics: Dict[str, Any]
    ordering_metrics: Dict[str, Any]


@dataclass
class COBState:
    """Internal COB basin state (mirrors cob_state.yaml)."""
    objects: List[IdentityObject] = field(default_factory=list)
    object_count: int = 0

    # NEW conversation-level ordering metrics
    conversation_access_count: int = 0
    conversation_access_order: List[int] = field(default_factory=list)
    conversation_frequency_last_10: Dict[str, int] = field(default_factory=dict)

    # existing summaries
    ordering_summary: Dict[str, Any] = field(default_factory=dict)
    stability_summary: List[Dict[str, Any]] = field(default_factory=list)
    ambiguity_summary: List[Dict[str, Any]] = field(default_factory=list)
    lineage_summary: List[Dict[str, Any]] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# COB Implementation (system_playground)
# ---------------------------------------------------------------------------

class COB:
    """
    Lightweight COB implementation for system_playground.

    Responsibilities:
    - Maintain up to 20 identity-layer objects
    - Integrate CST signals (drift, oscillation, collapse, merge, split, freeze, thaw)
    - Update identity objects deterministically
    - Apply ordering metrics
    - Evict lowest-priority objects when >20 exist
    """

    MAX_OBJECTS = 20

    def __init__(self):
        self.state = COBState()

    # -----------------------------------------------------------------------
    # Identity Object Lifecycle
    # -----------------------------------------------------------------------

    def add_identity_object(self, obj: IdentityObject):
        """Add a new identity-layer object to the basin."""
        self.state.objects.append(obj)
        self.state.object_count = len(self.state.objects)
        self._evict_if_needed()

    def update_identity_object(self, obj_id: str, updates: Dict[str, Any]):
        """Update an existing identity-layer object deterministically."""
        for obj in self.state.objects:
            if obj.id == obj_id:
                for key, value in updates.items():
                    setattr(obj, key, value)
                break

    # -----------------------------------------------------------------------
    # CST Signal Integration
    # -----------------------------------------------------------------------

    def apply_cst_signals(self, signals: Dict[str, Any]):
        """
        Apply CST signals to identity-layer objects.
        This is a simplified system_playground version.
        """

        # Freeze/thaw
        frozen_ids = signals.get("freeze", {}).get("frozen_objects", [])
        thawed_ids = signals.get("thaw", {}).get("thawed_objects", [])

        # Drift, oscillation, collapse, merge, split
        drift = signals.get("drift", {})
        oscillation = signals.get("oscillation", {})
        collapse = signals.get("collapse", {})
        merge = signals.get("merge", {})
        split = signals.get("split", {})

        # Certainty/ambiguity adjustments
        certainty_adj = signals.get("certainty_adjustment", {})
        ambiguity_adj = signals.get("ambiguity_adjustment", {})

        # Apply freeze/thaw
        for obj in self.state.objects:
            if obj.id in frozen_ids:
                obj.stability_metrics["frozen"] = True
            if obj.id in thawed_ids:
                obj.stability_metrics["frozen"] = False

        # Apply drift
        for obj in self.state.objects:
            if obj.id in drift.get("affected_objects", []):
                # Skip updates if frozen
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["drift"] = drift.get("magnitude")

        # Apply oscillation
        for obj in self.state.objects:
            if obj.id in oscillation.get("affected_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["oscillation"] = oscillation.get("frequency")

        # Apply collapse
        for obj in self.state.objects:
            if obj.id in collapse.get("collapsed_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["collapse"] = True

        # Apply certainty adjustments
        for obj in self.state.objects:
            if obj.stability_metrics.get("frozen"):
                continue
            if obj.id in certainty_adj.get("increased_certainty", []):
                obj.ambiguity["certainty"] = "high"
            if obj.id in certainty_adj.get("decreased_certainty", []):
                obj.ambiguity["certainty"] = "low"

        # Apply ambiguity adjustments
        for obj in self.state.objects:
            if obj.stability_metrics.get("frozen"):
                continue
            if obj.id in ambiguity_adj.get("increased_ambiguity", []):
                obj.ambiguity["ambiguity"] = "high"
            if obj.id in ambiguity_adj.get("decreased_ambiguity", []):
                obj.ambiguity["ambiguity"] = "low"

        # Merge and split are placeholders in system_playground
        # Full behavior will be implemented in system_simulation

    # -----------------------------------------------------------------------
    # Eviction Logic
    # -----------------------------------------------------------------------

    def _evict_if_needed(self):
        """Evict lowest-priority identity objects when >20 exist."""
        if len(self.state.objects) <= self.MAX_OBJECTS:
            return

        # Sort by ordering metrics: lowest recency, lowest frequency, lowest density
        sorted_objs = sorted(
            self.state.objects,
            key=lambda obj: (
                obj.ordering_metrics.get("recency", 0),
                obj.ordering_metrics.get("frequency", 0),
                obj.ordering_metrics.get("density", 0),
            )
        )

        # Evict the lowest-priority object
        evicted = sorted_objs[0]
        self.state.objects.remove(evicted)
        self.state.object_count = len(self.state.objects)

    # -----------------------------------------------------------------------
    # Summary Aggregation
    # -----------------------------------------------------------------------

    def aggregate_summaries(self):
        """Aggregate ordering, ambiguity, stability, and lineage summaries."""

        recency = []
        frequency = []
        density = []

        ambiguity_levels = []
        stability_levels = []
        lineage_levels = []

        for obj in self.state.objects:
            om = obj.ordering_metrics
            recency.append(om.get("recency"))
            frequency.append(om.get("frequency"))
            density.append(om.get("density"))

            ambiguity_levels.append(obj.ambiguity)
            stability_levels.append(obj.stability_metrics)
            lineage_levels.append(obj.lineage)

        self.state.ordering_summary = {
            "recency_distribution": recency,
            "frequency_distribution": frequency,
            "density_distribution": density,
        }

        self.state.ambiguity_summary = ambiguity_levels
        self.state.stability_summary = stability_levels
        self.state.lineage_summary = lineage_levels

    # -----------------------------------------------------------------------
    # Main Entry Point
    # -----------------------------------------------------------------------

    def run(self, signals: Dict[str, Any], turn_index: int):
        """
        Main COB execution for system_playground.
        Deterministic sequence:
        1. Apply CST signals
        2. Evict if needed
        3. Aggregate summaries
        """

        # Track total access count
        self.state.conversation_access_count += 1
        
        # Track chronological access order
        self.state.conversation_access_order.append(turn_index)
        
        # Compute sliding-window frequency (last 10 accesses)
        window = self.state.conversation_access_order[-10:]
        self.state.conversation_frequency_last_10 = {
            str(idx): window.count(idx) for idx in window
        }      
                
        self.state.metadata = {
            "turn_index": turn_index,
            "object_count": len(self.state.objects),
        }

        self.apply_cst_signals(signals)
        self._evict_if_needed()
        self.aggregate_summaries()

        return self.state

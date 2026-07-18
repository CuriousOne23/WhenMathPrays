"""
COB — Conversation Object Basin
System Playground Version

Lightweight block-level COB implementation for system_playground.
Mirrors:
- cob_requirements.md
- cob_structures.yaml
- cob_state.yaml
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

    # summaries
    ordering_summary: Dict[str, Any] = field(default_factory=dict)
    stability_summary: List[Dict[str, Any]] = field(default_factory=list)
    ambiguity_summary: List[Dict[str, Any]] = field(default_factory=list)
    lineage_summary: List[Dict[str, Any]] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# COB Implementation (system_playground)
# ---------------------------------------------------------------------------

class COB:
    MAX_OBJECTS = 20

    def __init__(self):
        self.state = COBState()

    # -----------------------------------------------------------------------
    # Identity Object Lifecycle
    # -----------------------------------------------------------------------

    def add_identity_object(self, obj: IdentityObject):
        self.state.objects.append(obj)
        self.state.object_count = len(self.state.objects)
        self._evict_if_needed()

    def update_identity_object(self, obj_id: str, updates: Dict[str, Any]):
        for obj in self.state.objects:
            if obj.id == obj_id:
                for key, value in updates.items():
                    setattr(obj, key, value)
                break

    # -----------------------------------------------------------------------
    # CST Signal Integration
    # -----------------------------------------------------------------------

    def apply_cst_signals(self, signals: Dict[str, Any]):
        """Apply CST signals deterministically."""

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

        # -------------------------
        # Freeze / Thaw
        # -------------------------
        for obj in self.state.objects:
            if obj.id in frozen_ids:
                obj.stability_metrics["frozen"] = True
            if obj.id in thawed_ids:
                obj.stability_metrics["frozen"] = False

        # -------------------------
        # Drift
        # -------------------------
        for obj in self.state.objects:
            if obj.id in drift.get("affected_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["drift"] = drift.get("magnitude")

        # -------------------------
        # Oscillation
        # -------------------------
        for obj in self.state.objects:
            if obj.id in oscillation.get("affected_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["oscillation"] = oscillation.get("frequency")

        # -------------------------
        # Collapse
        # -------------------------
        for obj in self.state.objects:
            if obj.id in collapse.get("collapsed_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["collapse"] = True

        # -------------------------
        # Certainty / Ambiguity
        # -------------------------
        for obj in self.state.objects:
            if obj.stability_metrics.get("frozen"):
                continue
            if obj.id in certainty_adj.get("increased_certainty", []):
                obj.ambiguity["certainty"] = "high"
            if obj.id in certainty_adj.get("decreased_certainty", []):
                obj.ambiguity["certainty"] = "low"

        for obj in self.state.objects:
            if obj.stability_metrics.get("frozen"):
                continue
            if obj.id in ambiguity_adj.get("increased_ambiguity", []):
                obj.ambiguity["ambiguity"] = "high"
            if obj.id in ambiguity_adj.get("decreased_ambiguity", []):
                obj.ambiguity["ambiguity"] = "low"

        # -------------------------------------------------------------------
        # Merge and Split (system_playground implementation)
        # -------------------------------------------------------------------

        # MERGE: {"merge": {"pairs": [(idA, idB), ...]}}
        if merge:
            for (idA, idB) in merge.get("pairs", []):
                objA = next((o for o in self.state.objects if o.id == idA), None)
                objB = next((o for o in self.state.objects if o.id == idB), None)
                if not objA or not objB:
                    continue

                # Deterministic referent-map union
                merged_referents = {}
                for key in set(objA.referent_map.keys()).union(objB.referent_map.keys()):
                    valsA = objA.referent_map.get(key, [])
                    valsB = objB.referent_map.get(key, [])
                    merged_referents[key] = sorted(set(valsA + valsB))

                # Deterministic anchor merge
                merged_anchors = [(a + b) / 2 for a, b in zip(objA.anchors, objB.anchors)]

                # Deterministic lineage merge
                merged_lineage = {
                    "parent": None,
                    "history": objA.lineage.get("history", []) +
                               objB.lineage.get("history", []) +
                               [f"merge({idA},{idB})"]
                }

                # Deterministic ordering merge
                merged_ordering = {
                    "recency": max(objA.ordering_metrics["recency"], objB.ordering_metrics["recency"]),
                    "frequency": max(objA.ordering_metrics["frequency"], objB.ordering_metrics["frequency"]),
                    "density": max(objA.ordering_metrics["density"], objB.ordering_metrics["density"]),
                }

                merged_obj = IdentityObject(
                    id=f"{idA}_{idB}_merged",
                    referent_map=merged_referents,
                    anchors=merged_anchors,
                    lineage=merged_lineage,
                    ambiguity={"certainty": "medium", "ambiguity": "medium"},
                    stability_metrics={"drift": 0.0, "oscillation": 0.0, "collapse": False, "frozen": False},
                    ordering_metrics=merged_ordering,
                )

                self.state.objects.remove(objA)
                self.state.objects.remove(objB)
                self.state.objects.append(merged_obj)

        # SPLIT: {"split": {"objects": [idX, ...]}}
        if split:
            for idX in split.get("objects", []):
                objX = next((o for o in self.state.objects if o.id == idX), None)
                if not objX:
                    continue

                keys = sorted(objX.referent_map.keys())
                half = len(keys) // 2
                keys1 = keys[:half]
                keys2 = keys[half:]

                referents1 = {k: objX.referent_map[k] for k in keys1}
                referents2 = {k: objX.referent_map[k] for k in keys2}

                anchors1 = [a * 0.95 for a in objX.anchors]
                anchors2 = [a * 1.05 for a in objX.anchors]

                lineage1 = {
                    "parent": objX.id,
                    "history": objX.lineage.get("history", []) + [f"split({idX})_1"]
                }
                lineage2 = {
                    "parent": objX.id,
                    "history": objX.lineage.get("history", []) + [f"split({idX})_2"]
                }

                ordering1 = objX.ordering_metrics.copy()
                ordering2 = objX.ordering_metrics.copy()

                objX1 = IdentityObject(
                    id=f"{idX}_1",
                    referent_map=referents1,
                    anchors=anchors1,
                    lineage=lineage1,
                    ambiguity=objX.ambiguity.copy(),
                    stability_metrics={"drift": 0.0, "oscillation": 0.0, "collapse": False, "frozen": False},
                    ordering_metrics=ordering1,
                )

                objX2 = IdentityObject(
                    id=f"{idX}_2",
                    referent_map=referents2,
                    anchors=anchors2,
                    lineage=lineage2,
                    ambiguity=objX.ambiguity.copy(),
                    stability_metrics={"drift": 0.0, "oscillation": 0.0, "collapse": False, "frozen": False},
                    ordering_metrics=ordering2,
                )

                self.state.objects.remove(objX)
                self.state.objects.append(objX1)
                self.state.objects.append(objX2)

    # -----------------------------------------------------------------------
    # Eviction Logic
    # -----------------------------------------------------------------------

    def _evict_if_needed(self):
        if len(self.state.objects) <= self.MAX_OBJECTS:
            return

        sorted_objs = sorted(
            self.state.objects,
            key=lambda obj: (
                obj.ordering_metrics.get("recency", 0),
                obj.ordering_metrics.get("frequency", 0),
                obj.ordering_metrics.get("density", 0),
            )
        )

        evicted = sorted_objs[0]
        self.state.objects.remove(evicted)
        self.state.object_count = len(self.state.objects)

    # -----------------------------------------------------------------------
    # Summary Aggregation
    # -----------------------------------------------------------------------

    def aggregate_summaries(self):
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
        """Deterministic COB execution sequence."""

        # Conversation-level metrics
        self.state.conversation_access_count += 1
        self.state.conversation_access_order.append(turn_index)

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

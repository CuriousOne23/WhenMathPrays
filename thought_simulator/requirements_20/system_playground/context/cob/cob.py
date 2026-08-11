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

    # conversation-level ordering metrics
    conversation_access_count: int = 0
    conversation_access_order: List[int] = field(default_factory=list)
    conversation_frequency_last_10: Dict[str, int] = field(default_factory=dict)

    # summaries
    ordering_summary: Dict[str, Any] = field(default_factory=dict)
    stability_summary: List[Dict[str, Any]] = field(default_factory=list)
    ambiguity_summary: List[Dict[str, Any]] = field(default_factory=list)
    lineage_summary: List[Dict[str, Any]] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    # TP-facing fields (for CST via TP)
    lineage_log: List[Dict[str, Any]] = field(default_factory=list)
    cob_state_snapshot: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# COB Implementation (system_playground)
# ---------------------------------------------------------------------------

class COB:
    MAX_OBJECTS = 20

    def __init__(self):
        self.state = COBState()
        # deterministic sequence for lineage_log entries
        self._lineage_seq = 0

    def _next_lineage_seq(self) -> int:
        self._lineage_seq += 1
        return self._lineage_seq

    # -----------------------------------------------------------------------
    # Structural Compression Helpers (HLR-COB-024)
    # -----------------------------------------------------------------------

    @staticmethod
    def _tokenize_surface_form(value: str) -> List[str]:
        """
        Structural tokenization: split on whitespace.
        No semantic interpretation, purely structural.
        """
        if not isinstance(value, str):
            return []
        return value.split()

    @classmethod
    def _compress_surface_forms(cls, forms: List[str]) -> List[str]:
        """
        Structural compression over a list of surface forms:
        - remove exact duplicates
        - remove forms whose token sets are strict subsets of other forms
        """
        if not isinstance(forms, list):
            return forms

        # remove exact duplicates (preserve order deterministically)
        seen = set()
        unique = []
        for f in forms:
            if f not in seen:
                seen.add(f)
                unique.append(f)

        # remove subset forms
        keep = []
        token_sets = [set(cls._tokenize_surface_form(f)) for f in unique]

        for i, f_i in enumerate(unique):
            tokens_i = token_sets[i]
            drop = False
            for j, f_j in enumerate(unique):
                if i == j:
                    continue
                tokens_j = token_sets[j]
                # strict subset: tokens_i ⊂ tokens_j
                if tokens_i and tokens_i.issubset(tokens_j) and tokens_i != tokens_j:
                    drop = True
                    break
            if not drop:
                keep.append(f_i)

        return keep

    @classmethod
    def _compress_referent_map(cls, referent_map: Any) -> Any:
        """
        Structural compression applied to referent_map.

        Rules:
        - If referent_map is a list of strings, compress that list.
        - If referent_map is a dict with 'surface_forms', compress that list.
        - If referent_map is a dict with 'parents', recurse into each parent map.
        - Otherwise, leave referent_map unchanged (non-semantic, structural-only).
        """
        # list-of-strings case
        if isinstance(referent_map, list):
            return cls._compress_surface_forms(referent_map)

        # dict cases
        if isinstance(referent_map, dict):
            # compress surface_forms if present
            if "surface_forms" in referent_map and isinstance(referent_map["surface_forms"], list):
                referent_map["surface_forms"] = cls._compress_surface_forms(
                    referent_map["surface_forms"]
                )

            # recurse into parents sub-structure if present
            if "parents" in referent_map and isinstance(referent_map["parents"], dict):
                for pid, pmap in referent_map["parents"].items():
                    referent_map["parents"][pid] = cls._compress_referent_map(pmap)

        return referent_map

    def _compress_all_referent_maps(self):
        """
        Apply structural compression to all identity-layer referent maps
        after updates, merges, and splits (HLR-COB-024, HLR-COB-025).
        Compression is global and structural-only.
        """
        for obj in self.state.objects:
            obj.referent_map = self._compress_referent_map(obj.referent_map)

    # -----------------------------------------------------------------------
    # Identity Object Lifecycle
    # -----------------------------------------------------------------------

    def add_identity_object(self, obj: IdentityObject):
        self.state.objects.append(obj)
        self.state.object_count = len(self.state.objects)
        # compression is applied globally in run(), not on add
        self._evict_if_needed()

    def update_identity_object(self, obj_id: str, updates: Dict[str, Any]):
        """
        Deterministic identity-object update.
        Structural compression is applied if referent_map changes.
        """
        for obj in self.state.objects:
            if obj.id == obj_id:
                for key, value in updates.items():
                    setattr(obj, key, value)
                obj.referent_map = self._compress_referent_map(obj.referent_map)
                break

    # -----------------------------------------------------------------------
    # CST Signal Integration
    # -----------------------------------------------------------------------

    def apply_cst_signals(self, signals: Dict[str, Any]):
        """Apply CST signals deterministically."""

        apply_only = signals.get("apply_to_only", None)

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
            if apply_only and obj.id != apply_only:
                continue
            if obj.id in frozen_ids:
                obj.stability_metrics["frozen"] = True
            if obj.id in thawed_ids:
                obj.stability_metrics["frozen"] = False

        # -------------------------
        # Drift
        # -------------------------
        for obj in self.state.objects:
            if apply_only and obj.id != apply_only:
                continue
            if obj.id in drift.get("affected_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["drift"] = drift.get("magnitude")

        # -------------------------
        # Oscillation
        # -------------------------
        for obj in self.state.objects:
            if apply_only and obj.id != apply_only:
                continue
            if obj.id in oscillation.get("affected_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["oscillation"] = oscillation.get("frequency")

        # -------------------------
        # Collapse
        # -------------------------
        for obj in self.state.objects:
            if apply_only and obj.id != apply_only:
                continue
            if obj.id in collapse.get("collapsed_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["collapse"] = True

        # -------------------------
        # Certainty / Ambiguity
        # -------------------------
        for obj in self.state.objects:
            if apply_only and obj.id != apply_only:
                continue
            if obj.stability_metrics.get("frozen"):
                continue
            if obj.id in certainty_adj.get("increased_certainty", []):
                obj.ambiguity["certainty"] = "high"
            if obj.id in certainty_adj.get("decreased_certainty", []):
                obj.ambiguity["certainty"] = "low"

        for obj in self.state.objects:
            if apply_only and obj.id != apply_only:
                continue
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

                # capture before-state for lineage_log
                before_referent = {
                    idA: objA.referent_map,
                    idB: objB.referent_map,
                }
                before_ordering = {
                    idA: objA.ordering_metrics,
                    idB: objB.ordering_metrics,
                }

                # structural merge: preserve both parents' semantics without reinterpretation
                merged_referents = {
                    "parents": {
                        idA: objA.referent_map,
                        idB: objB.referent_map,
                    }
                }

                merged_anchors = [
                    (idA, objA.anchors),
                    (idB, objB.anchors),
                ]

                merged_lineage = {
                    "parents": [idA, idB],
                    "stability": {
                        idA: objA.lineage.get("stability"),
                        idB: objB.lineage.get("stability"),
                    },
                }

                merged_ambiguity = {
                    "parents": {
                        idA: objA.ambiguity,
                        idB: objB.ambiguity,
                    }
                }

                merged_stability = {
                    "parents": {
                        idA: objA.stability_metrics,
                        idB: objB.stability_metrics,
                    }
                }

                merged_ordering = {
                    "recency": max(
                        objA.ordering_metrics.get("recency", 0),
                        objB.ordering_metrics.get("recency", 0),
                    ),
                    "frequency": max(
                        objA.ordering_metrics.get("frequency", 0),
                        objB.ordering_metrics.get("frequency", 0),
                    ),
                    "density": max(
                        objA.ordering_metrics.get("density", 0),
                        objB.ordering_metrics.get("density", 0),
                    ),
                }

                merged_obj = IdentityObject(
                    id=f"{idA}_{idB}_merged",
                    referent_map=merged_referents,
                    anchors=merged_anchors,
                    lineage=merged_lineage,
                    ambiguity=merged_ambiguity,
                    stability_metrics=merged_stability,
                    ordering_metrics=merged_ordering,
                )

                # append MERGE event to lineage_log (TP.lineage_log[])
                self.state.lineage_log.append({
                    "event_type": "MERGE",
                    "parent_ref": [idA, idB],
                    "child_refs": [merged_obj.id],
                    "referent_map_before": before_referent,
                    "referent_map_after": {merged_obj.id: merged_referents},
                    "ordering_before": before_ordering,
                    "ordering_after": {merged_obj.id: merged_ordering},
                    "lineage_seq": self._next_lineage_seq(),
                })

                self.state.objects.remove(objA)
                self.state.objects.remove(objB)
                self.state.objects.append(merged_obj)

        # SPLIT: {"split": {"objects": [idX, ...]}}
        if split:
            for idX in split.get("objects", []):
                objX = next((o for o in self.state.objects if o.id == idX), None)
                if not objX:
                    continue

                # capture before-state for lineage_log
                before_referent = {idX: objX.referent_map}
                before_ordering = {idX: objX.ordering_metrics}

                # TS-correct split: copy all semantics to both children
                child1_lineage = {
                    "parent": objX.id,
                    "stability": objX.lineage.get("stability"),
                }
                child2_lineage = {
                    "parent": objX.id,
                    "stability": objX.lineage.get("stability"),
                }

                child1 = IdentityObject(
                    id=f"{idX}_1",
                    referent_map=objX.referent_map,
                    anchors=list(objX.anchors),
                    lineage=child1_lineage,
                    ambiguity=dict(objX.ambiguity),
                    stability_metrics=dict(objX.stability_metrics),
                    ordering_metrics=dict(objX.ordering_metrics),
                )

                child2 = IdentityObject(
                    id=f"{idX}_2",
                    referent_map=objX.referent_map,
                    anchors=list(objX.anchors),
                    lineage=child2_lineage,
                    ambiguity=dict(objX.ambiguity),
                    stability_metrics=dict(objX.stability_metrics),
                    ordering_metrics=dict(objX.ordering_metrics),
                )

                # append SPLIT event to lineage_log (TP.lineage_log[])
                self.state.lineage_log.append({
                    "event_type": "SPLIT",
                    "parent_ref": [idX],
                    "child_refs": [child1.id, child2.id],
                    "referent_map_before": before_referent,
                    "referent_map_after": {
                        child1.id: child1.referent_map,
                        child2.id: child2.referent_map,
                    },
                    "ordering_before": before_ordering,
                    "ordering_after": {
                        child1.id: child1.ordering_metrics,
                        child2.id: child2.ordering_metrics,
                    },
                    "lineage_seq": self._next_lineage_seq(),
                })

                self.state.objects.remove(objX)
                self.state.objects.append(child1)
                self.state.objects.append(child2)

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

    def run(self, core_signals: Dict[str, Any], ms_signals: Dict[str, Any], turn_index: int):
        """Deterministic COB execution sequence."""

        # Merge signals
        signals = {**core_signals, **ms_signals}
    
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

        # -------------------------------------------------------------------
        # NEW_CONTEXT_REQUIRED — create a new identity object immediately
        # -------------------------------------------------------------------
        if signals.get("metadata", {}).get("new_context_required", False):
            new_id = f"ctx_{turn_index}"

            new_obj = IdentityObject(
                id=new_id,
                referent_map=signals.get("next_context", {}).get("referent_map", {}),
                anchors=signals.get("next_context", {}).get("anchors", []),
                lineage={"created_at": turn_index},
                ambiguity={"certainty": "unknown", "ambiguity": "unknown"},
                stability_metrics={"frozen": False},
                ordering_metrics={"recency": turn_index, "frequency": 1, "density": 1},
            )

            # Add new identity object immediately
            self.add_identity_object(new_obj)

            # COB must NOT evolve previous objects when a new context is required
            # So we skip CST signal application for existing objects
            # and only evolve the new object using CST signals
            signals["apply_to_only"] = new_id

        # CST signals (including merge/split)
        self.apply_cst_signals(signals)

        # Structural compression after updates, merges, and splits
        self._compress_all_referent_maps()

        # Eviction and summaries
        self._evict_if_needed()
        self.aggregate_summaries()

        # TP.cob_state_snapshot: stabilized identity-layer snapshot
        self.state.cob_state_snapshot = {
            "objects": [
                {
                    "id": obj.id,
                    "referent_map": obj.referent_map,
                    "anchors": obj.anchors,
                    "lineage": obj.lineage,
                    "ambiguity": obj.ambiguity,
                    "stability_metrics": obj.stability_metrics,
                    "ordering_metrics": obj.ordering_metrics,
                }
                for obj in self.state.objects
            ],
            "ordering_summary": self.state.ordering_summary,
            "stability_summary": self.state.stability_summary,
            "ambiguity_summary": self.state.ambiguity_summary,
            "lineage_summary": self.state.lineage_summary,
            "metadata": self.state.metadata,
        }

        return self.state

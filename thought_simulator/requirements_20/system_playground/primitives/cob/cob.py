"""
COB — Conversation Object Basin
System Playground Version

Aligned with:
- 20.32_cob_requirements.md
- system_playground/primitives/cob/cob_requirements.md
- cob_py_struc_pgm.md
- patha_field_names.md
- progressive_lineup_testing.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import copy


PRIMITIVE_NAME = "cob"


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class IdentityObject:
    """Structure of a single identity-layer object (IdentityLayer schema subset)."""
    id: str
    referent_map: Any
    anchors: List[Any] = field(default_factory=list)
    lineage: Dict[str, Any] = field(default_factory=dict)
    ambiguity: Dict[str, Any] = field(default_factory=dict)
    stability_metrics: Dict[str, Any] = field(default_factory=dict)
    ordering_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class COBState:
    """Internal COB basin state."""
    objects: List[IdentityObject] = field(default_factory=list)
    object_count: int = 0

    conversation_access_count: int = 0
    conversation_access_order: List[int] = field(default_factory=list)
    conversation_frequency_last_10: Dict[str, int] = field(default_factory=dict)

    ordering_summary: Dict[str, Any] = field(default_factory=dict)
    stability_summary: List[Dict[str, Any]] = field(default_factory=list)
    ambiguity_summary: List[Dict[str, Any]] = field(default_factory=list)
    lineage_summary: List[Dict[str, Any]] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)
    lineage_log: List[Dict[str, Any]] = field(default_factory=list)
    cob_state_snapshot: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# COB Implementation
# ---------------------------------------------------------------------------

class COB:
    MAX_OBJECTS = 20

    def __init__(self, initial_state: Optional[COBState] = None):
        self.state = initial_state if initial_state is not None else COBState()
        self._lineage_seq = 0

    def _next_lineage_seq(self) -> int:
        self._lineage_seq += 1
        return self._lineage_seq

    # -----------------------------------------------------------------------
    # Structural Compression (HLR-COB-024 / 025)
    # -----------------------------------------------------------------------

    @staticmethod
    def _tokenize_surface_form(value: str) -> List[str]:
        if not isinstance(value, str):
            return []
        return value.split()

    @classmethod
    def _compress_surface_forms(cls, forms: List[str]) -> List[str]:
        if not isinstance(forms, list):
            return forms
        seen = set()
        unique = []
        for f in forms:
            if f not in seen:
                seen.add(f)
                unique.append(f)
        keep = []
        token_sets = [set(cls._tokenize_surface_form(f)) for f in unique]
        for i, f_i in enumerate(unique):
            tokens_i = token_sets[i]
            drop = False
            for j, f_j in enumerate(unique):
                if i == j:
                    continue
                tokens_j = token_sets[j]
                if tokens_i and tokens_i.issubset(tokens_j) and tokens_i != tokens_j:
                    drop = True
                    break
            if not drop:
                keep.append(f_i)
        return keep

    @classmethod
    def _compress_referent_map(cls, referent_map: Any) -> Any:
        if isinstance(referent_map, list):
            return cls._compress_surface_forms(referent_map)
        if isinstance(referent_map, dict):
            if "surface_forms" in referent_map and isinstance(referent_map["surface_forms"], list):
                referent_map = dict(referent_map)
                referent_map["surface_forms"] = cls._compress_surface_forms(
                    referent_map["surface_forms"]
                )
            if "parents" in referent_map and isinstance(referent_map["parents"], dict):
                referent_map = dict(referent_map)
                parents = {}
                for pid, pmap in referent_map["parents"].items():
                    parents[pid] = cls._compress_referent_map(pmap)
                referent_map["parents"] = parents
        return referent_map

    def _compress_all_referent_maps(self):
        for obj in self.state.objects:
            obj.referent_map = self._compress_referent_map(obj.referent_map)

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
                obj.referent_map = self._compress_referent_map(obj.referent_map)
                break

    # -----------------------------------------------------------------------
    # CST Signal Integration
    # -----------------------------------------------------------------------

    def apply_cst_signals(self, signals: Dict[str, Any]):
        apply_only = signals.get("apply_to_only", None)

        frozen_ids = signals.get("freeze", {}).get("frozen_objects", [])
        thawed_ids = signals.get("thaw", {}).get("thawed_objects", [])
        drift = signals.get("drift", {})
        oscillation = signals.get("oscillation", {})
        collapse = signals.get("collapse", {})
        merge = signals.get("merge", {})
        split = signals.get("split", {})
        certainty_adj = signals.get("certainty_adjustment", {})
        ambiguity_adj = signals.get("ambiguity_adjustment", {})

        for obj in self.state.objects:
            if apply_only and obj.id != apply_only:
                continue
            if obj.id in frozen_ids:
                obj.stability_metrics["frozen"] = True
            if obj.id in thawed_ids:
                obj.stability_metrics["frozen"] = False

        for obj in self.state.objects:
            if apply_only and obj.id != apply_only:
                continue
            if obj.id in drift.get("affected_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["drift"] = drift.get("magnitude")

        for obj in self.state.objects:
            if apply_only and obj.id != apply_only:
                continue
            if obj.id in oscillation.get("affected_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["oscillation"] = oscillation.get("frequency")

        for obj in self.state.objects:
            if apply_only and obj.id != apply_only:
                continue
            if obj.id in collapse.get("collapsed_objects", []):
                if obj.stability_metrics.get("frozen"):
                    continue
                obj.stability_metrics["collapse"] = True

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

        # MERGE (structural only)
        if merge:
            for (idA, idB) in merge.get("pairs", []):
                objA = next((o for o in self.state.objects if o.id == idA), None)
                objB = next((o for o in self.state.objects if o.id == idB), None)
                if not objA or not objB:
                    continue

                before_referent = {idA: objA.referent_map, idB: objB.referent_map}
                before_ordering = {idA: objA.ordering_metrics, idB: objB.ordering_metrics}

                merged_referents = {"parents": {idA: objA.referent_map, idB: objB.referent_map}}
                merged_anchors = [(idA, objA.anchors), (idB, objB.anchors)]
                merged_lineage = {
                    "parents": [idA, idB],
                    "stability": {
                        idA: objA.lineage.get("stability"),
                        idB: objB.lineage.get("stability"),
                    },
                }
                merged_ambiguity = {"parents": {idA: objA.ambiguity, idB: objB.ambiguity}}
                merged_stability = {
                    "parents": {idA: objA.stability_metrics, idB: objB.stability_metrics}
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

                self.state.lineage_log.append({
                    "event_type": "MERGE",
                    "parent_ref": [idA, idB],
                    "child_refs": [merged_obj.id],
                    "referent_map_before": before_referent,
                    "referent_map_after": {merged_obj.id: merged_referents},
                    "ordering_before": before_ordering,
                    "ordering_after": {merged_obj.id: merged_ordering},
                    "lineage_seq": self._next_lineage_seq(),
                    "module_id": "cob",
                })

                self.state.objects.remove(objA)
                self.state.objects.remove(objB)
                self.state.objects.append(merged_obj)

        # SPLIT (structural only — full copy)
        if split:
            for idX in split.get("objects", []):
                objX = next((o for o in self.state.objects if o.id == idX), None)
                if not objX:
                    continue

                before_referent = {idX: objX.referent_map}
                before_ordering = {idX: objX.ordering_metrics}

                child1 = IdentityObject(
                    id=f"{idX}_1",
                    referent_map=copy.deepcopy(objX.referent_map),
                    anchors=list(objX.anchors),
                    lineage={"parent": objX.id, "stability": objX.lineage.get("stability")},
                    ambiguity=dict(objX.ambiguity),
                    stability_metrics=dict(objX.stability_metrics),
                    ordering_metrics=dict(objX.ordering_metrics),
                )
                child2 = IdentityObject(
                    id=f"{idX}_2",
                    referent_map=copy.deepcopy(objX.referent_map),
                    anchors=list(objX.anchors),
                    lineage={"parent": objX.id, "stability": objX.lineage.get("stability")},
                    ambiguity=dict(objX.ambiguity),
                    stability_metrics=dict(objX.stability_metrics),
                    ordering_metrics=dict(objX.ordering_metrics),
                )

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
                    "module_id": "cob",
                })

                self.state.objects.remove(objX)
                self.state.objects.append(child1)
                self.state.objects.append(child2)

    # -----------------------------------------------------------------------
    # Eviction
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
            ),
        )
        evicted = sorted_objs[0]
        self.state.objects.remove(evicted)
        self.state.object_count = len(self.state.objects)

    # -----------------------------------------------------------------------
    # Summaries
    # -----------------------------------------------------------------------

    def aggregate_summaries(self):
        recency, frequency, density = [], [], []
        ambiguity_levels, stability_levels, lineage_levels = [], [], []
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
    # Snapshot builder
    # -----------------------------------------------------------------------

    def _build_snapshot(self) -> Dict[str, Any]:
        return {
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
            "conversation_access_count": self.state.conversation_access_count,
            "conversation_access_order": list(self.state.conversation_access_order),
            "conversation_frequency_last_10": dict(self.state.conversation_frequency_last_10),
            "object_count": self.state.object_count,
        }

    # -----------------------------------------------------------------------
    # Core run (legacy signal-driven path)
    # -----------------------------------------------------------------------

    def run(self, core_signals: Dict[str, Any], ms_signals: Dict[str, Any], turn_index: int):
        signals = {**core_signals, **ms_signals}

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
            self.add_identity_object(new_obj)
            signals["apply_to_only"] = new_id

        self.apply_cst_signals(signals)
        self._compress_all_referent_maps()
        self._evict_if_needed()
        self.aggregate_summaries()
        self.state.cob_state_snapshot = self._build_snapshot()
        return self.state

    # -----------------------------------------------------------------------
    # Structural-program surface: process(tp, mode=...)
    # -----------------------------------------------------------------------

    def process(self, tp: Dict[str, Any], mode: str = "general", **kwargs) -> Dict[str, Any]:
        """
        Main entry required by cob_py_struc_pgm.md and progressive dual-mode contract.
        Reads CST signals and next_context from the TP envelope, updates internal state,
        and writes cob_state_snapshot + lineage_log contributions back into the TP.
        """
        tp = copy.deepcopy(tp) if tp is not None else {}
        turn_index = (
            tp.get("turn_index")
            or tp.get("metadata", {}).get("turn_index")
            or kwargs.get("turn_index")
            or 0
        )

        # Prefer signals carried under TP metadata / cst envelopes when present.
        core_signals = (
            tp.get("cst", {}).get("core", {})
            or tp.get("metadata", {}).get("cst_core", {})
            or tp.get("core_signals", {})
            or {}
        )
        ms_signals = (
            tp.get("cst", {}).get("ms", {})
            or tp.get("metadata", {}).get("cst_ms", {})
            or tp.get("ms_signals", {})
            or {}
        )

        # Allow direct signal injection for testbench convenience
        if "signals" in tp:
            core_signals = {**core_signals, **tp.get("signals", {})}

        # next_context support
        next_ctx = (
            tp.get("next_context")
            or tp.get("metadata", {}).get("next_context")
            or tp.get("metadata", {}).get("next_context_metadata")
            or {}
        )
        if next_ctx and "next_context" not in core_signals:
            core_signals = dict(core_signals)
            core_signals["next_context"] = next_ctx

        self.run(core_signals, ms_signals, turn_index)

        # Write owned fields back into TP
        identity = tp.setdefault("identity", {})
        identity["cob_state_snapshot"] = self.state.cob_state_snapshot

        # Append lineage events
        lineage_log = tp.setdefault("lineage_log", [])
        if not isinstance(lineage_log, list):
            lineage_log = []
            tp["lineage_log"] = lineage_log
        lineage_log.extend(self.state.lineage_log)

        # Routing / provenance markers
        routing_path = tp.setdefault("routing_path", [])
        if isinstance(routing_path, list) and "cob" not in routing_path:
            routing_path.append("cob")

        return tp


def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """Module-level entry matching progressive / structural-program contract."""
    cob = COB()
    return cob.process(tp, mode=mode, **kwargs)

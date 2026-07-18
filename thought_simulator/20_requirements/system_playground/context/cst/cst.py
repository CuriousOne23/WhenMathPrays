"""
CST — Conversation Stability Tracker
System Playground Version

This module implements a lightweight, block-level Python representation
of the CST subsystem. It mirrors the structure defined in:

- cst_requirements.md
- cst_signals.yaml
- cst_state.yaml

This is NOT a full simulation engine. It is a local behavioral block
used inside system_playground for shaping, validating, and inspecting
stability behavior before system_simulation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


# ---------------------------------------------------------------------------
# Data Classes (mirroring YAML schemas)
# ---------------------------------------------------------------------------

@dataclass
class CSTState:
    """Internal CST state (mirrors cst_state.yaml)."""
    drift_state: Dict[str, Any] = field(default_factory=dict)
    oscillation_state: Dict[str, Any] = field(default_factory=dict)
    collapse_state: Dict[str, Any] = field(default_factory=dict)
    merge_state: Dict[str, Any] = field(default_factory=dict)
    split_state: Dict[str, Any] = field(default_factory=dict)
    freeze_state: Dict[str, Any] = field(default_factory=dict)
    thaw_state: Dict[str, Any] = field(default_factory=dict)
    certainty_state: Dict[str, Any] = field(default_factory=dict)
    ambiguity_state: Dict[str, Any] = field(default_factory=dict)
    lineage_stability_state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # NEW — structural continuity + 10‑turn stability window
    structural_events: List[Dict[str, Any]] = field(default_factory=list)
    post_structure_stability_window: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CSTSignals:
    """Signals produced by CST (mirrors cst_signals.yaml)."""
    drift: Dict[str, Any]
    oscillation: Dict[str, Any]
    collapse: Dict[str, Any]
    merge: Dict[str, Any]
    split: Dict[str, Any]
    freeze: Dict[str, Any]
    thaw: Dict[str, Any]
    certainty_adjustment: Dict[str, Any]
    ambiguity_adjustment: Dict[str, Any]
    lineage_stability: Dict[str, Any]
    metadata: Dict[str, Any]


# ---------------------------------------------------------------------------
# CST Implementation (system_playground)
# ---------------------------------------------------------------------------

class CST:
    """
    Lightweight CST implementation for system_playground.

    Responsibilities:
    - Detect drift, oscillation, collapse, merge, split
    - Issue freeze/thaw signals
    - Adjust certainty and ambiguity
    - Evaluate lineage stability
    - Produce deterministic stability signals
    """

    def __init__(self):
        self.state = CSTState()

    # -----------------------------------------------------------------------
    # Drift Detection
    # -----------------------------------------------------------------------

    def detect_drift(self, identity_objects: List[Dict[str, Any]]):
        """
        Drift occurs when referent or anchor positions diverge across turns.
        This is a simplified system_playground version.
        """
        affected = []
        magnitudes = []

        for obj in identity_objects:
            drift_val = obj.stability_metrics.get("drift")
            if drift_val:
                affected.append(obj.id)
                magnitudes.append(drift_val)

        self.state.drift_state = {
            "affected_objects": affected,
            "magnitude": max(magnitudes) if magnitudes else 0,
        }

    # -----------------------------------------------------------------------
    # Oscillation Detection
    # -----------------------------------------------------------------------

    def detect_oscillation(self, identity_objects: List[Dict[str, Any]]):
        """
        Oscillation occurs when identity-layer objects alternate between incompatible states.
        """
        affected = []
        frequencies = []

        for obj in identity_objects:
            osc_val = obj.stability_metrics.get("oscillation")
            if osc_val:
                affected.append(obj.id)
                frequencies.append(osc_val)

        self.state.oscillation_state = {
            "affected_objects": affected,
            "frequency": max(frequencies) if frequencies else 0,
            "amplitude": len(affected),
        }

    # -----------------------------------------------------------------------
    # Collapse Detection
    # -----------------------------------------------------------------------

    def detect_collapse(self, identity_objects: List[Dict[str, Any]]):
        collapsed = [
            obj.id
            for obj in identity_objects
            if obj.stability_metrics.get("collapse")
        ]

        self.state.collapse_state = {
            "collapsed_objects": collapsed,
            "severity": len(collapsed),
        }

    # -----------------------------------------------------------------------
    # Merge Detection
    # -----------------------------------------------------------------------

    def detect_merge(self, identity_objects: List[Dict[str, Any]]):
        """
        Merge detection placeholder for system_playground.
        Full merge logic will be implemented in system_simulation.
        """
        self.state.merge_state = {
            "merge_pairs": [],
            "confidence": 0,
        }

    # -----------------------------------------------------------------------
    # Split Detection
    # -----------------------------------------------------------------------

    def detect_split(self, identity_objects: List[Dict[str, Any]]):
        """
        Split detection placeholder for system_playground.
        Full split logic will be implemented in system_simulation.
        """
        self.state.split_state = {
            "split_objects": [],
            "confidence": 0,
        }

    # -----------------------------------------------------------------------
    # Freeze / Thaw
    # -----------------------------------------------------------------------

    def detect_freeze_thaw(self, identity_objects: List[Dict[str, Any]]):
        frozen = []
        thawed = []

        for obj in identity_objects:
            sm = obj.stability_metrics
            if sm.get("frozen") is True:
                frozen.append(obj.id)
            if sm.get("frozen") is False:
                thawed.append(obj.id)

        self.state.freeze_state = {
            "frozen_objects": frozen,
            "reason": "stability_condition",
        }

        self.state.thaw_state = {
            "thawed_objects": thawed,
            "reason": "stability_condition",
        }

    # -----------------------------------------------------------------------
    # Certainty / Ambiguity Adjustments
    # -----------------------------------------------------------------------

    def detect_certainty_ambiguity(self, identity_objects: List[Dict[str, Any]]):
        increased_certainty = []
        decreased_certainty = []

        increased_ambiguity = []
        decreased_ambiguity = []

        for obj in identity_objects:
            amb = obj.ambiguity
            if amb.get("certainty") == "high":
                increased_certainty.append(obj.id)
            if amb.get("certainty") == "low":
                decreased_certainty.append(obj.id)

            if amb.get("ambiguity") == "high":
                increased_ambiguity.append(obj.id)
            if amb.get("ambiguity") == "low":
                decreased_ambiguity.append(obj.id)

        self.state.certainty_state = {
            "increased_certainty": increased_certainty,
            "decreased_certainty": decreased_certainty,
        }

        self.state.ambiguity_state = {
            "increased_ambiguity": increased_ambiguity,
            "decreased_ambiguity": decreased_ambiguity,
        }

    # -----------------------------------------------------------------------
    # Lineage Stability
    # -----------------------------------------------------------------------

    def detect_lineage_stability(self, identity_objects: List[Dict[str, Any]]):
        stable = []
        unstable = []

        for obj in identity_objects:
            lineage = obj.lineage
            if lineage.get("stability") == "stable":
                stable.append(obj.id)
            if lineage.get("stability") == "unstable":
                unstable.append(obj.id)

        self.state.lineage_stability_state = {
            "stable_lineage": stable,
            "unstable_lineage": unstable,
        }

    # -----------------------------------------------------------------------
    # Structural Continuity Interpretation (MERGE / SPLIT)
    # -----------------------------------------------------------------------

    def interpret_structural_events(self, tp_lineage_log: List[Dict[str, Any]]):
        """
        Reads TP.lineage_log[] and records MERGE/SPLIT structural events.
        CST uses this to suppress false instability and update its topology.
        """

        structural_events = []

        for evt in tp_lineage_log:
            etype = evt.get("event_type")
            if etype in ("MERGE", "SPLIT"):
                structural_events.append(evt)

        # Store structural events in CST state
        self.state.structural_events = structural_events

    # -----------------------------------------------------------------------
    # Structural Compensation (MERGE / SPLIT)
    # -----------------------------------------------------------------------

    def compensate_for_structure(self, identity_objects: List[Dict[str, Any]]):
        """
        Prevents CST from misinterpreting MERGE/SPLIT as instability.
        Updates CST's internal topology to match COB.
        """

        # If no MERGE/SPLIT events, nothing to compensate
        if not self.state.structural_events:
            return identity_objects

        compensated_objects = identity_objects.copy()

        for evt in self.state.structural_events:
            etype = evt.get("event_type")

            if etype == "MERGE":
                parent_ids = evt.get("parent_ref", [])
                child_ids = evt.get("child_refs", [])

                # Remove parents from instability consideration
                compensated_objects = [
                    obj for obj in compensated_objects if obj.id not in parent_ids
                ]

                # Children are legitimate new layers; no instability should be triggered

            elif etype == "SPLIT":
                parent_id = evt.get("parent_ref", [None])[0]
                child_ids = evt.get("child_refs", [])

                # Remove parent from instability consideration
                compensated_objects = [
                    obj for obj in compensated_objects if obj.id != parent_id
                ]

                # Children are legitimate new layers; no instability should be triggered

        return compensated_objects

    # -----------------------------------------------------------------------
    # Post-Structure Stability Tracking (10 TS cycles)
    # -----------------------------------------------------------------------

    def track_post_structure_stability(self, signals: Dict[str, Any]):
        """
        Tracks stability for 10 turns after MERGE/SPLIT.
        Ensures no delayed instability appears due to structural changes.
        """

        window = self.state.post_structure_stability_window

        # Append current turn's signals
        window.append(signals)

        # Keep only the last 10 turns
        if len(window) > 10:
            window.pop(0)

        self.state.post_structure_stability_window = window
    
    # -----------------------------------------------------------------------
    # Main Entry Point
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Main Entry Point
    # -----------------------------------------------------------------------

    def run(
        self,
        identity_objects: List[Dict[str, Any]],
        tp_lineage_log: List[Dict[str, Any]],
        tp_snapshot: Dict[str, Any],
        turn_index: int
    ) -> CSTSignals:
        """
        Main CST execution for system_playground.
        Deterministic sequence:
        1. Interpret structural continuity markers (MERGE/SPLIT)
        2. Compensate identity objects for structural transitions
        3. Detect drift
        4. Detect oscillation
        5. Detect collapse
        6. Detect merge/split (placeholder)
        7. Detect freeze/thaw
        8. Detect certainty/ambiguity adjustments
        9. Detect lineage stability
        10. Track 10-turn post-structure stability
        """

        # Metadata
        self.state.metadata = {
            "turn_index": turn_index,
            "object_count": len(identity_objects),
        }

        # 1. Interpret MERGE/SPLIT structural continuity markers
        self.interpret_structural_events(tp_lineage_log)

        # 2. Compensate identity objects for MERGE/SPLIT
        compensated_objects = self.compensate_for_structure(identity_objects)

        # 3–9. Run all existing detection methods on compensated objects
        self.detect_drift(compensated_objects)
        self.detect_oscillation(compensated_objects)
        self.detect_collapse(compensated_objects)
        self.detect_merge(compensated_objects)
        self.detect_split(compensated_objects)
        self.detect_freeze_thaw(compensated_objects)
        self.detect_certainty_ambiguity(compensated_objects)
        self.detect_lineage_stability(compensated_objects)

        # Package signals
        signals = CSTSignals(
            drift=self.state.drift_state,
            oscillation=self.state.oscillation_state,
            collapse=self.state.collapse_state,
            merge=self.state.merge_state,
            split=self.state.split_state,
            freeze=self.state.freeze_state,
            thaw=self.state.thaw_state,
            certainty_adjustment=self.state.certainty_state,
            ambiguity_adjustment=self.state.ambiguity_state,
            lineage_stability=self.state.lineage_stability_state,
            metadata=self.state.metadata,
        )

        # 10. Track 10-turn post-structure stability
        self.track_post_structure_stability(signals)

        return signals

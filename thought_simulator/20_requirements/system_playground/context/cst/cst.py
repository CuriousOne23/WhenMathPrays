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
            drift_val = obj.get("stability_metrics", {}).get("drift")
            if drift_val:
                affected.append(obj["id"])
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
            osc_val = obj.get("stability_metrics", {}).get("oscillation")
            if osc_val:
                affected.append(obj["id"])
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
            obj["id"]
            for obj in identity_objects
            if obj.get("stability_metrics", {}).get("collapse")
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
            sm = obj.get("stability_metrics", {})
            if sm.get("frozen") is True:
                frozen.append(obj["id"])
            if sm.get("frozen") is False:
                thawed.append(obj["id"])

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
            amb = obj.get("ambiguity", {})
            if amb.get("certainty") == "high":
                increased_certainty.append(obj["id"])
            if amb.get("certainty") == "low":
                decreased_certainty.append(obj["id"])

            if amb.get("ambiguity") == "high":
                increased_ambiguity.append(obj["id"])
            if amb.get("ambiguity") == "low":
                decreased_ambiguity.append(obj["id"])

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
            lineage = obj.get("lineage", {})
            if lineage.get("stability") == "stable":
                stable.append(obj["id"])
            if lineage.get("stability") == "unstable":
                unstable.append(obj["id"])

        self.state.lineage_stability_state = {
            "stable_lineage": stable,
            "unstable_lineage": unstable,
        }

    # -----------------------------------------------------------------------
    # Main Entry Point
    # -----------------------------------------------------------------------

    def run(self, identity_objects: List[Dict[str, Any]], turn_index: int) -> CSTSignals:
        """
        Main CST execution for system_playground.
        Deterministic sequence:
        1. Detect drift
        2. Detect oscillation
        3. Detect collapse
        4. Detect merge/split (placeholder)
        5. Detect freeze/thaw
        6. Detect certainty/ambiguity adjustments
        7. Detect lineage stability
        """

        self.state.metadata = {
            "turn_index": turn_index,
            "object_count": len(identity_objects),
        }

        self.detect_drift(identity_objects)
        self.detect_oscillation(identity_objects)
        self.detect_collapse(identity_objects)
        self.detect_merge(identity_objects)
        self.detect_split(identity_objects)
        self.detect_freeze_thaw(identity_objects)
        self.detect_certainty_ambiguity(identity_objects)
        self.detect_lineage_stability(identity_objects)

        return CSTSignals(
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

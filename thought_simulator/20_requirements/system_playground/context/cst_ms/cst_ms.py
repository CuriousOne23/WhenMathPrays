"""
CST‑MS — Metric Synthesis Module
System Playground Version (Testbench-Compatible)

This module is fully compatible with:
- context_testbench.py
- cst-ms.md (architecture)
- cst-ms_requirements.md (testbench requirements)
- cst-core.py (upstream CST-Core signals)

CST‑MS performs deterministic synthesis of CST-Core metrics:
- normalization
- weighting
- stability synthesis
- instability synthesis
- collapse/freeze/thaw risk
- ambiguity/drift/oscillation summaries
- merge/split neutrality
- 10-turn stability window
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class MSState:
    """Internal CST‑MS state."""
    normalized_metrics: Dict[str, Any] = field(default_factory=dict)
    weighted_metrics: Dict[str, Any] = field(default_factory=dict)
    stability: Dict[str, Any] = field(default_factory=dict)
    instability: Dict[str, Any] = field(default_factory=dict)
    collapse_risk: Dict[str, Any] = field(default_factory=dict)
    freeze_risk: Dict[str, Any] = field(default_factory=dict)
    thaw_readiness: Dict[str, Any] = field(default_factory=dict)
    ambiguity_summary: Dict[str, Any] = field(default_factory=dict)
    drift_summary: Dict[str, Any] = field(default_factory=dict)
    oscillation_summary: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Merge/split structural neutrality
    structural_events: List[Dict[str, Any]] = field(default_factory=list)

    # 10-turn stability window
    stability_window: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class MSSignals:
    """Signals produced by CST‑MS."""
    normalized_metrics: Dict[str, Any]
    weighted_metrics: Dict[str, Any]
    stability: Dict[str, Any]
    instability: Dict[str, Any]
    collapse_risk: Dict[str, Any]
    freeze_risk: Dict[str, Any]
    thaw_readiness: Dict[str, Any]
    ambiguity_summary: Dict[str, Any]
    drift_summary: Dict[str, Any]
    oscillation_summary: Dict[str, Any]
    metadata: Dict[str, Any]


# ---------------------------------------------------------------------------
# CST‑MS Implementation
# ---------------------------------------------------------------------------

class CST_MS:
    """
    Deterministic CST‑MS implementation for system_playground.

    Responsibilities:
    - Normalize CST-Core metrics
    - Apply deterministic layer-specific weights
    - Synthesize stability and instability
    - Compute collapse/freeze/thaw risk
    - Produce ambiguity/drift/oscillation summaries
    - Maintain merge/split neutrality
    - Track 10-turn stability window
    """

    def __init__(self):
        self.state = MSState()

        # Deterministic synthesis weights (placeholder values)
        self.weights = {
            "drift": 0.25,
            "oscillation": 0.25,
            "ambiguity": 0.25,
            "collapse": 0.25,
            "continuity": 0.25,
        }

        # Deterministic maxima for normalization (placeholder values)
        self.maxima = {
            "drift": 1.0,
            "oscillation": 1.0,
            "ambiguity": 1.0,
            "collapse": 1.0,
            "continuity": 1.0,
        }

    # -----------------------------------------------------------------------
    # Structural Neutrality (MERGE / SPLIT)
    # -----------------------------------------------------------------------

    def interpret_structural_events(self, cst_signals: Dict[str, Any]):
        """
        CST‑MS receives merge/split signals from CST-Core.
        These events must NOT produce instability by themselves.
        """

        merge = cst_signals.get("merge", {})
        split = cst_signals.get("split", {})

        events = []
        if merge.get("merge_pairs"):
            events.append({"event_type": "MERGE", "data": merge})
        if split.get("split_objects"):
            events.append({"event_type": "SPLIT", "data": split})

        self.state.structural_events = events

    def neutralize_structure(self, cst_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove structural transitions from instability consideration.
        """

        if not self.state.structural_events:
            return cst_signals

        # Deep copy
        signals = {k: v.copy() if isinstance(v, dict) else v for k, v in cst_signals.items()}

        # Remove merge/split from instability synthesis
        signals["merge"] = {"merge_pairs": [], "confidence": 0}
        signals["split"] = {"split_objects": [], "confidence": 0}

        return signals

    # -----------------------------------------------------------------------
    # Normalization
    # -----------------------------------------------------------------------

    def normalize(self, signals: Dict[str, Any]):
        nm = {}

        nm["drift"] = min(signals["drift"]["magnitude"] / self.maxima["drift"], 1.0)
        nm["oscillation"] = min(signals["oscillation"]["frequency"] / self.maxima["oscillation"], 1.0)
        nm["ambiguity"] = min(
            len(signals["ambiguity_adjustment"]["increased_ambiguity"]) / self.maxima["ambiguity"],
            1.0,
        )
        nm["collapse"] = min(signals["collapse"]["severity"] / self.maxima["collapse"], 1.0)

        # continuity = inverse collapse
        nm["continuity"] = 1.0 - nm["collapse"]

        self.state.normalized_metrics = nm

    # -----------------------------------------------------------------------
    # Weighting
    # -----------------------------------------------------------------------

    def weight(self):
        wm = {}

        for key, val in self.state.normalized_metrics.items():
            wm[key] = val * self.weights.get(key, 1.0)

        self.state.weighted_metrics = wm

    # -----------------------------------------------------------------------
    # Stability / Instability Synthesis
    # -----------------------------------------------------------------------

    def synthesize_stability(self):
        wm = self.state.weighted_metrics

        stability = sum(wm.values())
        stability = max(min(stability, 1.0), 0.0)

        instability = 1.0 - stability

        self.state.stability = {"value": stability}
        self.state.instability = {"value": instability}

    # -----------------------------------------------------------------------
    # Risk Computation
    # -----------------------------------------------------------------------

    def compute_risks(self):
        wm = self.state.weighted_metrics

        collapse_risk = wm["collapse"]
        freeze_risk = wm["ambiguity"] + wm["collapse"]
        thaw_readiness = wm["continuity"]

        self.state.collapse_risk = {"value": min(collapse_risk, 1.0)}
        self.state.freeze_risk = {"value": min(freeze_risk, 1.0)}
        self.state.thaw_readiness = {"value": min(thaw_readiness, 1.0)}

    # -----------------------------------------------------------------------
    # Summaries
    # -----------------------------------------------------------------------

    def compute_summaries(self, signals: Dict[str, Any]):
        self.state.ambiguity_summary = {
            "count": len(signals["ambiguity_adjustment"]["increased_ambiguity"])
        }

        self.state.drift_summary = {
            "magnitude": signals["drift"]["magnitude"]
        }

        self.state.oscillation_summary = {
            "frequency": signals["oscillation"]["frequency"],
            "amplitude": signals["oscillation"]["amplitude"],
        }

    # -----------------------------------------------------------------------
    # Stability Window (10 turns)
    # -----------------------------------------------------------------------

    def track_window(self):
        entry = {
            "stability": self.state.stability,
            "instability": self.state.instability,
            "collapse_risk": self.state.collapse_risk,
            "freeze_risk": self.state.freeze_risk,
            "thaw_readiness": self.state.thaw_readiness,
        }

        window = self.state.stability_window
        window.append(entry)

        if len(window) > 10:
            window.pop(0)

        self.state.stability_window = window
        
    def detect_new_context(self):
        nm = self.state.normalized_metrics
        st = self.state.stability
        inst = self.state.instability
        collapse = self.state.collapse_risk
        freeze = self.state.freeze_risk
        ambiguity = self.state.ambiguity_summary
    
        # 1. Continuity break
        continuity_break = nm["continuity"] < 0.40
    
        # 2. Multi-turn instability trend
        window = self.state.stability_window
        if window:
            avg_instability = sum(entry["instability"]["value"] for entry in window) / len(window)
        else:
            avg_instability = 0.0
        instability_trend = avg_instability > 0.60
    
        # 3. Collapse risk spike
        collapse_spike = collapse["value"] > 0.50
    
        # 4. Ambiguity drift spike
        ambiguity_spike = ambiguity["count"] > 3  # deterministic threshold
    
        # 5. Freeze risk spike
        freeze_spike = freeze["value"] > 0.50
    
        # 6. Merge/split fragmentation
        structural_event = len(self.state.structural_events) > 0
        fragmentation = structural_event and nm["continuity"] < 0.75
    
        new_context_required = (
            continuity_break
            or instability_trend
            or collapse_spike
            or ambiguity_spike
            or freeze_spike
            or fragmentation
        )
    
        self.state.metadata["new_context_required"] = new_context_required

    # -----------------------------------------------------------------------
    # Main Entry Point
    # -----------------------------------------------------------------------

    def run(self, cst_signals: Dict[str, Any], turn_index: int) -> MSSignals:
        """
        Deterministic CST‑MS execution.
        """
    
        # Metadata
        self.state.metadata = {
            "turn_index": turn_index,
        }
    
        # DEBUG 1 — Raw CST-Core signals
        # print("\n[CST-MS DEBUG] Raw CST-Core signals:")
        # print(cst_signals)
    
        # 1. Interpret structural events
        self.interpret_structural_events(cst_signals)
    
        # 2. Neutralize merge/split
        signals = self.neutralize_structure(cst_signals)
    
        # DEBUG 2 — After merge/split neutralization
        # print("\n[CST-MS DEBUG] Signals after structural neutralization:")
        # print(signals)
    
        # 3. Normalize
        self.normalize(signals)
    
        # DEBUG 3 — Normalized metrics
        # print("\n[CST-MS DEBUG] Normalized metrics:")
        # print(self.state.normalized_metrics)
    
        # 4. Weight
        self.weight()
    
        # 5. Stability synthesis
        self.synthesize_stability()
    
        # 6. Risk computation
        self.compute_risks()
    
        # 7. Summaries
        self.compute_summaries(signals)
    
        # 8. Track 10-turn window
        self.track_window()
    
        # 9. Detect new context requirement
        self.detect_new_context()
    
        # DEBUG 4 — Final new_context_required decision
        # print("\n[CST-MS DEBUG] new_context_required =", 
              self.state.metadata.get("new_context_required"))
    
        # Package signals
        return MSSignals(
            normalized_metrics=self.state.normalized_metrics,
            weighted_metrics=self.state.weighted_metrics,
            stability=self.state.stability,
            instability=self.state.instability,
            collapse_risk=self.state.collapse_risk,
            freeze_risk=self.state.freeze_risk,
            thaw_readiness=self.state.thaw_readiness,
            ambiguity_summary=self.state.ambiguity_summary,
            drift_summary=self.state.drift_summary,
            oscillation_summary=self.state.oscillation_summary,
            metadata=self.state.metadata,
        )


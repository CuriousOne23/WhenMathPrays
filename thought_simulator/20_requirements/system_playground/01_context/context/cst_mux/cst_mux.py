"""
CST‑Mux — Stability Signal Multiplexing Module
System Playground Version (Testbench-Compatible)

This module is designed to be compatible with:
- cst-mux.md (architecture paper)
- cst-mux_requirements.md (testbench requirements)
- cst-core.py and cst-ms.py (upstream CST modules)
- future cst-mux_testbench.py

CST‑Mux takes synthesized CST‑MS signals and constructs a Unified Stability
Packet (USP) suitable for consumption by COB and CIL in system_playground.
It is deterministic and replay‑safe.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class MuxState:
    """Internal CST‑Mux state."""
    usp: Dict[str, Any] = field(default_factory=dict)
    activation_flags: Dict[str, Any] = field(default_factory=dict)
    freeze_flags: Dict[str, Any] = field(default_factory=dict)
    thaw_flags: Dict[str, Any] = field(default_factory=dict)
    continuity_flags: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Structural neutrality (MERGE/SPLIT) — placeholder for future use
    structural_events: List[Dict[str, Any]] = field(default_factory=list)

    # 10-turn USP window
    usp_window: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class USP:
    """Unified Stability Packet produced by CST‑Mux."""
    activation_flags: Dict[str, Any]
    freeze_flags: Dict[str, Any]
    thaw_flags: Dict[str, Any]
    continuity_flags: Dict[str, Any]
    stability: Dict[str, Any]
    instability: Dict[str, Any]
    collapse_risk: Dict[str, Any]
    freeze_risk: Dict[str, Any]
    thaw_readiness: Dict[str, Any]
    ambiguity_summary: Dict[str, Any]
    drift_summary: Dict[str, Any]
    oscillation_summary: Dict[str, Any]
    metadata: Dict[str, Any]
    new_context_required: bool = False

# ---------------------------------------------------------------------------
# CST‑Mux Implementation
# ---------------------------------------------------------------------------

class CST_MUX:
    """
    Deterministic CST‑Mux implementation for system_playground.

    Responsibilities:
    - Interpret synthesized CST‑MS signals
    - Compute activation, freeze, thaw, continuity flags
    - Construct Unified Stability Packet (USP)
    - Maintain a 10-turn USP window
    - Preserve merge/split neutrality (no instability by itself)
    """

    def __init__(self):
        self.state = MuxState()

        # Deterministic thresholds (placeholder values)
        self.thresholds = {
            "activation": 0.2,
            "freeze": 0.7,
            "thaw": 0.5,
            "continuity": 0.5,
        }

    # -----------------------------------------------------------------------
    # Flag Computation
    # -----------------------------------------------------------------------

    def compute_activation_flags(self, ms_signals: Dict[str, Any]):
        stability_val = ms_signals["stability"]["value"]
        activated = stability_val >= self.thresholds["activation"]

        self.state.activation_flags = {
            "activated": activated,
            "stability_value": stability_val,
        }

    def compute_freeze_flags(self, ms_signals: Dict[str, Any]):
        freeze_val = ms_signals["freeze_risk"]["value"]
        frozen = freeze_val >= self.thresholds["freeze"]

        self.state.freeze_flags = {
            "frozen": frozen,
            "freeze_risk": freeze_val,
        }

    def compute_thaw_flags(self, ms_signals: Dict[str, Any]):
        thaw_val = ms_signals["thaw_readiness"]["value"]
        thawed = thaw_val >= self.thresholds["thaw"]

        self.state.thaw_flags = {
            "thawed": thawed,
            "thaw_readiness": thaw_val,
        }

    def compute_continuity_flags(self, ms_signals: Dict[str, Any]):
        stability_val = ms_signals["stability"]["value"]
        continuity = stability_val >= self.thresholds["continuity"]

        self.state.continuity_flags = {
            "continuous": continuity,
            "stability_value": stability_val,
        }

    # -----------------------------------------------------------------------
    # USP Construction
    # -----------------------------------------------------------------------

    def construct_usp(self, ms_signals: Dict[str, Any]):
        self.state.usp = {
            "activation_flags": self.state.activation_flags,
            "freeze_flags": self.state.freeze_flags,
            "thaw_flags": self.state.thaw_flags,
            "continuity_flags": self.state.continuity_flags,
             # NEW: propagate new_context_required
            "new_context_required": self.state.metadata.get("new_context_required", False),
            "stability": ms_signals["stability"],
            "instability": ms_signals["instability"],
            "collapse_risk": ms_signals["collapse_risk"],
            "freeze_risk": ms_signals["freeze_risk"],
            "thaw_readiness": ms_signals["thaw_readiness"],
            "ambiguity_summary": ms_signals["ambiguity_summary"],
            "drift_summary": ms_signals["drift_summary"],
            "oscillation_summary": ms_signals["oscillation_summary"],
        }

    # -----------------------------------------------------------------------
    # USP Window (10 turns)
    # -----------------------------------------------------------------------

    def track_usp_window(self):
        window = self.state.usp_window
        window.append(self.state.usp)

        if len(window) > 10:
            window.pop(0)

        self.state.usp_window = window

    # -----------------------------------------------------------------------
    # Main Entry Point
    # -----------------------------------------------------------------------

    def run(self, ms_signals: Dict[str, Any], turn_index: int) -> USP:
        """
        Deterministic CST‑Mux execution.

        ms_signals: MSSignals.__dict__ from cst-ms.py
        """

        # Metadata
        self.state.metadata = {
            "turn_index": turn_index,
        }

        # -------------------------------------------------------------------
        # NEW_CONTEXT_REQUIRED — accept and propagate CST‑MS control signal
        # -------------------------------------------------------------------
        new_ctx = ms_signals.get("metadata", {}).get("new_context_required", False)
        self.state.metadata["new_context_required"] = new_ctx
        
        # 1. Compute flags
        self.compute_activation_flags(ms_signals)
        self.compute_freeze_flags(ms_signals)
        self.compute_thaw_flags(ms_signals)
        self.compute_continuity_flags(ms_signals)

        # 2. Construct USP
        self.construct_usp(ms_signals)

        # 3. Track 10-turn USP window
        self.track_usp_window()

        # 4. Package USP
        return USP(
            activation_flags=self.state.activation_flags,
            freeze_flags=self.state.freeze_flags,
            thaw_flags=self.state.thaw_flags,
            continuity_flags=self.state.continuity_flags,
            stability=ms_signals["stability"],
            instability=ms_signals["instability"],
            collapse_risk=ms_signals["collapse_risk"],
            freeze_risk=ms_signals["freeze_risk"],
            thaw_readiness=ms_signals["thaw_readiness"],
            ambiguity_summary=ms_signals["ambiguity_summary"],
            drift_summary=ms_signals["drift_summary"],
            oscillation_summary=ms_signals["oscillation_summary"],
            metadata=self.state.metadata,
            new_context_required=self.state.metadata.get("new_context_required", False)  # ⭐ ADD THIS
        )

# 40.36_gb_prototypes/prototype.py
"""
Governing Basin (GB) Prototype - Phase B (Expanded)
Non-mutating supervisory subsystem only.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class SupervisoryDecision:
    action: str                    # "Continue", "Dampen", "Slow", "Stop", etc.
    reason_code: str
    confidence: float
    affected_components: List[str]
    timestamp: int


class GoverningBasinPrototype:
    """
    Governing Basin (GB) - Supervisory Layer Only
    MUST NOT mutate TP/MTP semantic state directly.
    """

    def __init__(self):
        self.supervisory_history: List[SupervisoryDecision] = []
        self.intervention_count: int = 0
        self.recent_actions: List[str] = []   # For oscillation detection

    def evaluate_supervisory_state(self, 
                                   global_state_snapshot: Dict[str, Any],
                                   cycle_number: int) -> SupervisoryDecision:
        """
        Main supervisory evaluation.
        Takes a read-only snapshot and returns a supervisory decision.
        """
        delta_h_trend = global_state_snapshot.get("delta_h_trend", 0.0)
        ib_count = global_state_snapshot.get("active_ib_count", 0)
        oscillation_flag = global_state_snapshot.get("oscillation_flag", False)
        contradiction_level = global_state_snapshot.get("contradiction_level", 0.0)

        # Track recent actions for oscillation detection
        self.recent_actions.append("evaluate")
        if len(self.recent_actions) > 10:
            self.recent_actions.pop(0)

        # Decision Logic
        if oscillation_flag:
            decision = SupervisoryDecision(
                action="Dampen",
                reason_code="OSCILLATION_DETECTED",
                confidence=0.88,
                affected_components=["trace_depth", "ib_population"],
                timestamp=cycle_number
            )
        elif delta_h_trend > 0.85:
            decision = SupervisoryDecision(
                action="Dampen",
                reason_code="HIGH_DELTA_H_DRIFT",
                confidence=0.82,
                affected_components=["trace_depth"],
                timestamp=cycle_number
            )
        elif ib_count > 28:
            decision = SupervisoryDecision(
                action="Slow",
                reason_code="HIGH_IB_POPULATION",
                confidence=0.78,
                affected_components=["ib_creation"],
                timestamp=cycle_number
            )
        elif contradiction_level > 0.75:
            decision = SupervisoryDecision(
                action="Dampen",
                reason_code="HIGH_CONTRADICTION_LEVEL",
                confidence=0.75,
                affected_components=["semantic_stability"],
                timestamp=cycle_number
            )
        else:
            decision = SupervisoryDecision(
                action="Continue",
                reason_code="NORMAL_OPERATION",
                confidence=0.92,
                affected_components=[],
                timestamp=cycle_number
            )

        # Record intervention frequency
        if decision.action != "Continue":
            self.intervention_count += 1

        self.supervisory_history.append(decision)
        return decision

    def get_supervisory_log(self) -> List[SupervisoryDecision]:
        """Return immutable copy of history for auditability."""
        return list(self.supervisory_history)

    def get_intervention_frequency(self) -> float:
        """Return intervention rate over logged history."""
        if not self.supervisory_history:
            return 0.0
        return self.intervention_count / len(self.supervisory_history)


# =============================================================================
if __name__ == "__main__":
    gb = GoverningBasinPrototype()
    print("✅ Governing Basin (GB) Prototype initialized successfully.")
    print("   - Supports drift, oscillation, population, and contradiction detection")
    print("   - Maintains deterministic supervisory logging")
    print("   - Respects non-mutation rule")
# 40.36_gb_prototypes/harness.py
"""
Test Harness for GB Prototype (Phase B)
Focus: Explore key scenarios from 20-series
"""

from prototype import GlobalBrainPrototype

def create_test_snapshot(scenario: str) -> dict:
    """Create synthetic global state snapshots for testing."""
    snapshots = {
        "stable": {
            "delta_h_trend": 0.35,
            "active_ib_count": 8,
            "oscillation_flag": False,
            "contradiction_level": 0.1
        },
        "high_drift": {
            "delta_h_trend": 0.92,
            "active_ib_count": 12,
            "oscillation_flag": True,
            "contradiction_level": 0.6
        },
        "high_population": {
            "delta_h_trend": 0.55,
            "active_ib_count": 32,
            "oscillation_flag": False,
            "contradiction_level": 0.4
        },
        "messy_input": {
            "delta_h_trend": 0.78,
            "active_ib_count": 15,
            "oscillation_flag": True,
            "contradiction_level": 0.85
        }
    }
    return snapshots.get(scenario, snapshots["stable"])


def run_gb_harness():
    gb = GlobalBrainPrototype()
    scenarios = ["stable", "high_drift", "high_population", "messy_input"]

    print("=== GB Prototype Test Harness ===\n")

    for scenario in scenarios:
        snapshot = create_test_snapshot(scenario)
        print(f"Scenario: {scenario.upper()}")
        print(f"  Snapshot: {snapshot}")

        decision = gb.evaluate_supervisory_state(snapshot, cycle_number=42)
        
        print(f"  → GB Decision: {decision.action} "
              f"({decision.reason_code}, conf={decision.confidence:.2f})")
        print("-" * 50)

    print(f"\nTotal supervisory decisions logged: {len(gb.get_supervisory_log())}")


if __name__ == "__main__":
    run_gb_harness()
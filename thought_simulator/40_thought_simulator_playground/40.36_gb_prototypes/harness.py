# 40.36_gb_prototypes/harness.py
"""
Test Harness for GB Prototype (Phase B - Expanded)
Tests core supervisory scenarios from 20-series guidance.
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
            "oscillation_flag": False,
            "contradiction_level": 0.4
        },
        "oscillation": {
            "delta_h_trend": 0.65,
            "active_ib_count": 15,
            "oscillation_flag": True,
            "contradiction_level": 0.5
        },
        "high_population": {
            "delta_h_trend": 0.55,
            "active_ib_count": 35,
            "oscillation_flag": False,
            "contradiction_level": 0.3
        },
        "messy_input": {
            "delta_h_trend": 0.78,
            "active_ib_count": 18,
            "oscillation_flag": False,
            "contradiction_level": 0.88
        }
    }
    return snapshots.get(scenario, snapshots["stable"])


def run_gb_harness():
    """Run expanded test scenarios for the GB prototype."""
    gb = GlobalBrainPrototype()
    scenarios = ["stable", "high_drift", "oscillation", "high_population", "messy_input"]

    print("=== GB Prototype Test Harness (Expanded) ===\n")

    for scenario in scenarios:
        snapshot = create_test_snapshot(scenario)
        print(f"Scenario: {scenario.upper():15} | "
              f"ΔH={snapshot['delta_h_trend']:.2f} | "
              f"IB={snapshot['active_ib_count']} | "
              f"Osc={snapshot['oscillation_flag']} | "
              f"Contr={snapshot['contradiction_level']:.2f}")

        decision = gb.evaluate_supervisory_state(snapshot, cycle_number=100 + len(gb.get_supervisory_log()))

        print(f"  → GB Decision: {decision.action:8} "
              f"({decision.reason_code}, conf={decision.confidence:.2f})")
        print("-" * 70)

    # Final statistics
    freq = gb.get_intervention_frequency()
    total_decisions = len(gb.get_supervisory_log())

    print(f"\n=== Harness Summary ===")
    print(f"Total decisions made   : {total_decisions}")
    print(f"Intervention frequency : {freq:.1%}")
    print(f"Supervisory log size   : {total_decisions}")
    print("✅ Harness execution completed.")


if __name__ == "__main__":
    run_gb_harness()
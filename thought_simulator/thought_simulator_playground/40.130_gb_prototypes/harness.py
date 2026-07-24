# 40.130_gb_prototypes/harness.py
"""
Test Harness for Governing Basin (GB) Prototype - 3-Tier Iteration
"""

from prototype import GoverningBasin


def create_test_snapshot(scenario: str) -> dict:
    """Create synthetic global state snapshots for testing."""
    snapshots = {
        "stable": {
            "delta_h_trend": 0.35,
            "active_ib_count": 8,
            "oscillation_flag": False,
            "contradiction_level": 0.10
        },
        "high_drift": {
            "delta_h_trend": 0.92,
            "active_ib_count": 12,
            "oscillation_flag": False,
            "contradiction_level": 0.40
        },
        "oscillation": {
            "delta_h_trend": 0.65,
            "active_ib_count": 15,
            "oscillation_flag": True,
            "contradiction_level": 0.50
        },
        "high_population": {
            "delta_h_trend": 0.55,
            "active_ib_count": 35,
            "oscillation_flag": False,
            "contradiction_level": 0.30
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
    """Run test scenarios against the 3-tier Governing Basin."""
    gb = GoverningBasin()
    scenarios = ["stable", "high_drift", "oscillation", "high_population", "messy_input"]

    print("=== Governing Basin (3-Tier) Test Harness ===\n")

    for scenario in scenarios:
        snapshot = create_test_snapshot(scenario)
        print(f"Scenario: {scenario.upper():15} | "
              f"ΔH={snapshot['delta_h_trend']:.2f} | "
              f"IB={snapshot['active_ib_count']} | "
              f"Osc={snapshot['oscillation_flag']} | "
              f"Contr={snapshot['contradiction_level']:.2f}")

        decision = gb.evaluate(snapshot, cycle=100 + len(gb.integrator.history))

        print(f"  → GB Decision: {decision.action:8} "
              f"({decision.reason_code}, conf={decision.confidence:.2f})")
        print("-" * 70)

    total_decisions = len(gb.integrator.history)
    freq = gb.integrator.intervention_count / total_decisions if total_decisions > 0 else 0.0

    print(f"\n=== Harness Summary ===")
    print(f"Total decisions made   : {total_decisions}")
    print(f"Intervention frequency : {freq:.1%}")
    print("✅ 3-Tier Governing Basin harness execution completed.")


if __name__ == "__main__":
    run_gb_harness()
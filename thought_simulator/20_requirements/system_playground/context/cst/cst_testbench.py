"""
CST Testbench — System Playground Version

This testbench performs block-level validation of the CST subsystem.
It tests:
- drift detection
- oscillation detection
- collapse detection
- freeze/thaw detection
- certainty/ambiguity adjustments
- lineage stability detection

This is NOT a full system simulation. It is a shaping testbench used
inside system_playground before system_simulation.
"""

from cst import CST


def make_identity_object(
    id: str,
    drift=None,
    oscillation=None,
    collapse=False,
    certainty=None,
    ambiguity=None,
    lineage_stability=None,
    frozen=None,
):
    """Helper to create identity-layer objects as dictionaries for CST."""

    return {
        "id": id,
        "referent_map": {"r1": "value"},
        "anchors": ["a1", "a2"],
        "lineage": {"stability": lineage_stability},
        "ambiguity": {"certainty": certainty, "ambiguity": ambiguity},
        "stability_metrics": {
            "drift": drift,
            "oscillation": oscillation,
            "collapse": collapse,
            "frozen": frozen,
        },
    }


def run_drift_test():
    print("\n=== CST Testbench: Drift Detection ===")

    objs = [
        make_identity_object("A", drift=0.1),
        make_identity_object("B", drift=0.3),
        make_identity_object("C", drift=None),
    ]

    cst = CST()
    signals = cst.run(objs, turn_index=1)

    print("\n--- Drift State ---")
    print(signals.drift)


def run_oscillation_test():
    print("\n=== CST Testbench: Oscillation Detection ===")

    objs = [
        make_identity_object("A", oscillation=0.2),
        make_identity_object("B", oscillation=0.5),
        make_identity_object("C", oscillation=None),
    ]

    cst = CST()
    signals = cst.run(objs, turn_index=2)

    print("\n--- Oscillation State ---")
    print(signals.oscillation)


def run_collapse_test():
    print("\n=== CST Testbench: Collapse Detection ===")

    objs = [
        make_identity_object("A", collapse=True),
        make_identity_object("B", collapse=False),
        make_identity_object("C", collapse=True),
    ]

    cst = CST()
    signals = cst.run(objs, turn_index=3)

    print("\n--- Collapse State ---")
    print(signals.collapse)


def run_freeze_thaw_test():
    print("\n=== CST Testbench: Freeze/Thaw Detection ===")

    objs = [
        make_identity_object("A", frozen=True),
        make_identity_object("B", frozen=False),
        make_identity_object("C", frozen=None),
    ]

    cst = CST()
    signals = cst.run(objs, turn_index=4)

    print("\n--- Freeze State ---")
    print(signals.freeze)

    print("\n--- Thaw State ---")
    print(signals.thaw)


def run_certainty_ambiguity_test():
    print("\n=== CST Testbench: Certainty/Ambiguity Detection ===")

    objs = [
        make_identity_object("A", certainty="high", ambiguity="low"),
        make_identity_object("B", certainty="low", ambiguity="high"),
        make_identity_object("C", certainty=None, ambiguity=None),
    ]

    cst = CST()
    signals = cst.run(objs, turn_index=5)

    print("\n--- Certainty Adjustment ---")
    print(signals.certainty_adjustment)

    print("\n--- Ambiguity Adjustment ---")
    print(signals.ambiguity_adjustment)


def run_lineage_stability_test():
    print("\n=== CST Testbench: Lineage Stability Detection ===")

    objs = [
        make_identity_object("A", lineage_stability="stable"),
        make_identity_object("B", lineage_stability="unstable"),
        make_identity_object("C", lineage_stability="stable"),
    ]

    cst = CST()
    signals = cst.run(objs, turn_index=6)

    print("\n--- Lineage Stability ---")
    print(signals.lineage_stability)


if __name__ == "__main__":
    run_drift_test()
    run_oscillation_test()
    run_collapse_test()
    run_freeze_thaw_test()
    run_certainty_ambiguity_test()
    run_lineage_stability_test()

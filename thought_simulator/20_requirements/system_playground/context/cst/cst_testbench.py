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
- merge/split structural compensation
- 10-turn post-structure stability behavior

This is NOT a full system simulation. It is a shaping testbench used
inside system_playground before system_simulation.
"""

from cst import CST


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


def empty_tp_fields():
    """TP lineage/snapshot placeholders for tests that do not involve merge/split."""
    return [], {"objects": [], "metadata": {}}


# ---------------------------------------------------------------------------
# Drift Test
# ---------------------------------------------------------------------------

def run_drift_test():
    print("\n=== CST Testbench: Drift Detection ===")

    objs = [
        make_identity_object("A", drift=0.1),
        make_identity_object("B", drift=0.3),
        make_identity_object("C", drift=None),
    ]

    tp_lineage, tp_snapshot = empty_tp_fields()

    cst = CST()
    signals = cst.run(objs, tp_lineage, tp_snapshot, turn_index=1)

    print("\n--- Drift State ---")
    print(signals.drift)


# ---------------------------------------------------------------------------
# Oscillation Test
# ---------------------------------------------------------------------------

def run_oscillation_test():
    print("\n=== CST Testbench: Oscillation Detection ===")

    objs = [
        make_identity_object("A", oscillation=0.2),
        make_identity_object("B", oscillation=0.5),
        make_identity_object("C", oscillation=None),
    ]

    tp_lineage, tp_snapshot = empty_tp_fields()

    cst = CST()
    signals = cst.run(objs, tp_lineage, tp_snapshot, turn_index=2)

    print("\n--- Oscillation State ---")
    print(signals.oscillation)


# ---------------------------------------------------------------------------
# Collapse Test
# ---------------------------------------------------------------------------

def run_collapse_test():
    print("\n=== CST Testbench: Collapse Detection ===")

    objs = [
        make_identity_object("A", collapse=True),
        make_identity_object("B", collapse=False),
        make_identity_object("C", collapse=True),
    ]

    tp_lineage, tp_snapshot = empty_tp_fields()

    cst = CST()
    signals = cst.run(objs, tp_lineage, tp_snapshot, turn_index=3)

    print("\n--- Collapse State ---")
    print(signals.collapse)


# ---------------------------------------------------------------------------
# Freeze / Thaw Test
# ---------------------------------------------------------------------------

def run_freeze_thaw_test():
    print("\n=== CST Testbench: Freeze/Thaw Detection ===")

    objs = [
        make_identity_object("A", frozen=True),
        make_identity_object("B", frozen=False),
        make_identity_object("C", frozen=None),
    ]

    tp_lineage, tp_snapshot = empty_tp_fields()

    cst = CST()
    signals = cst.run(objs, tp_lineage, tp_snapshot, turn_index=4)

    print("\n--- Freeze State ---")
    print(signals.freeze)

    print("\n--- Thaw State ---")
    print(signals.thaw)


# ---------------------------------------------------------------------------
# Certainty / Ambiguity Test
# ---------------------------------------------------------------------------

def run_certainty_ambiguity_test():
    print("\n=== CST Testbench: Certainty/Ambiguity Detection ===")

    objs = [
        make_identity_object("A", certainty="high", ambiguity="low"),
        make_identity_object("B", certainty="low", ambiguity="high"),
        make_identity_object("C", certainty=None, ambiguity=None),
    ]

    tp_lineage, tp_snapshot = empty_tp_fields()

    cst = CST()
    signals = cst.run(objs, tp_lineage, tp_snapshot, turn_index=5)

    print("\n--- Certainty Adjustment ---")
    print(signals.certainty_adjustment)

    print("\n--- Ambiguity Adjustment ---")
    print(signals.ambiguity_adjustment)


# ---------------------------------------------------------------------------
# Lineage Stability Test
# ---------------------------------------------------------------------------

def run_lineage_stability_test():
    print("\n=== CST Testbench: Lineage Stability Detection ===")

    objs = [
        make_identity_object("A", lineage_stability="stable"),
        make_identity_object("B", lineage_stability="unstable"),
        make_identity_object("C", lineage_stability="stable"),
    ]

    tp_lineage, tp_snapshot = empty_tp_fields()

    cst = CST()
    signals = cst.run(objs, tp_lineage, tp_snapshot, turn_index=6)

    print("\n--- Lineage Stability ---")
    print(signals.lineage_stability)


# ---------------------------------------------------------------------------
# Merge Compensation Test
# ---------------------------------------------------------------------------

def run_merge_compensation_test():
    print("\n=== CST Testbench: MERGE Structural Compensation ===")

    # Parent objects would normally disappear after merge
    objs = [
        make_identity_object("objA", drift=0.5),  # would falsely look unstable
        make_identity_object("objB", oscillation=0.7),  # would falsely look unstable
        make_identity_object("objA_objB_merged", drift=None, oscillation=None),
    ]

    tp_lineage = [
        {
            "event_type": "MERGE",
            "parent_ref": ["objA", "objB"],
            "child_refs": ["objA_objB_merged"],
        }
    ]

    tp_snapshot = {"objects": ["objA_objB_merged"], "metadata": {}}

    cst = CST()
    signals = cst.run(objs, tp_lineage, tp_snapshot, turn_index=7)

    print("\n--- Drift State (should be empty or minimal) ---")
    print(signals.drift)

    print("\n--- Oscillation State (should be empty or minimal) ---")
    print(signals.oscillation)

    print("\n--- Collapse State (should be empty) ---")
    print(signals.collapse)


# ---------------------------------------------------------------------------
# Split Compensation Test
# ---------------------------------------------------------------------------

def run_split_compensation_test():
    print("\n=== CST Testbench: SPLIT Structural Compensation ===")

    objs = [
        make_identity_object("objX", drift=0.4),  # parent would falsely look unstable
        make_identity_object("objX_1", drift=None),
        make_identity_object("objX_2", oscillation=None),
    ]

    tp_lineage = [
        {
            "event_type": "SPLIT",
            "parent_ref": ["objX"],
            "child_refs": ["objX_1", "objX_2"],
        }
    ]

    tp_snapshot = {"objects": ["objX_1", "objX_2"], "metadata": {}}

    cst = CST()
    signals = cst.run(objs, tp_lineage, tp_snapshot, turn_index=8)

    print("\n--- Drift State (should be empty or minimal) ---")
    print(signals.drift)

    print("\n--- Oscillation State (should be empty or minimal) ---")
    print(signals.oscillation)

    print("\n--- Collapse State (should be empty) ---")
    print(signals.collapse)


# ---------------------------------------------------------------------------
# 10-Turn Post-Structure Stability Test
# ---------------------------------------------------------------------------

def run_post_structure_stability_test():
    print("\n=== CST Testbench: 10-Turn Post-Structure Stability Window ===")

    # After merge, no instability should appear for 10 turns
    tp_lineage = [
        {
            "event_type": "MERGE",
            "parent_ref": ["objA", "objB"],
            "child_refs": ["objA_objB_merged"],
        }
    ]

    tp_snapshot = {"objects": ["objA_objB_merged"], "metadata": {}}

    cst = CST()

    for turn in range(1, 12):  # 11 turns to test window behavior
        objs = [
            make_identity_object("objA_objB_merged", drift=None, oscillation=None)
        ]

        signals = cst.run(objs, tp_lineage, tp_snapshot, turn_index=turn)

        print(f"\n--- Turn {turn} Stability Window ---")
        print(cst.state.post_structure_stability_window)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_drift_test()
    run_oscillation_test()
    run_collapse_test()
    run_freeze_thaw_test()
    run_certainty_ambiguity_test()
    run_lineage_stability_test()
    run_merge_compensation_test()
    run_split_compensation_test()
    run_post_structure_stability_test()

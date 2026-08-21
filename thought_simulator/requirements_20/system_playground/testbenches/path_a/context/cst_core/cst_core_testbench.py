"""
CST-Core Testbench — System Playground Version

This testbench validates the CST-Core implementation against:
- cst-core_requirements.md
- cst-core.md
- context_testbench.py

It focuses on:
- snapshot-level stability behavior (drift, oscillation, collapse)
- freeze/thaw behavior
- certainty/ambiguity adjustments
- lineage stability
- MERGE/SPLIT structural compensation
- 10-turn post-structure stability window
- determinism and replay consistency
"""

from cst_core.cst_core import CST
from cil.cil import IdentityObject


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_identity_object(
    id: str,
    drift=None,
    oscillation=None,
    collapse=False,
    frozen=None,
    certainty=None,
    ambiguity=None,
    lineage_stability=None,
):
    """
    Helper to create IdentityObject instances for CST-Core testing.
    Mirrors the OuBA-like objects used in context_testbench.py.
    """

    return IdentityObject(
        id=id,
        referent_map={"r1": "value"},
        anchors=["a1", "a2"],
        lineage={"stability": lineage_stability},
        ambiguity={"certainty": certainty, "ambiguity": ambiguity},
        stability_metrics={
            "drift": drift,
            "oscillation": oscillation,
            "collapse": collapse,
            "frozen": frozen,
        },
        ordering_metrics={
            "recency": 0,
            "frequency": 0,
            "density": 0,
        },
    )


def make_tp_placeholders():
    """
    Create TP-like placeholder structures for CST-Core testing.
    """

    tp_lineage_log = []
    tp_snapshot = {"turn_index": None, "objects": []}
    return tp_lineage_log, tp_snapshot


# ---------------------------------------------------------------------------
# Basic Functionality Tests
# ---------------------------------------------------------------------------

def test_basic_drift_oscillation_collapse():
    """
    Test basic drift, oscillation, and collapse detection.
    Covers:
    - HLR-CST-CORE-001..009, 015..018
    """

    cst = CST()
    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj1 = make_identity_object("obj1", drift=0.1, oscillation=0.0, collapse=False)
    obj2 = make_identity_object("obj2", drift=0.3, oscillation=0.2, collapse=False)
    obj3 = make_identity_object("obj3", drift=None, oscillation=None, collapse=True)

    signals = cst.run(
        identity_objects=[obj1, obj2, obj3],
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=1,
    )

    # Drift: affected objects and magnitude
    assert "obj1" in signals.drift["affected_objects"]
    assert "obj2" in signals.drift["affected_objects"]
    assert signals.drift["magnitude"] == 0.3

    # Oscillation: affected objects, frequency, amplitude
    assert "obj2" in signals.oscillation["affected_objects"]
    assert signals.oscillation["frequency"] == 0.2
    assert signals.oscillation["amplitude"] == len(
        signals.oscillation["affected_objects"]
    )

    # Collapse: collapsed objects and severity
    assert "obj3" in signals.collapse["collapsed_objects"]
    assert signals.collapse["severity"] == 1


# ---------------------------------------------------------------------------
# Freeze / Thaw Tests
# ---------------------------------------------------------------------------

def test_freeze_thaw_behavior():
    """
    Test freeze/thaw detection based on stability_metrics['frozen'].
    Covers:
    - HLR-CST-CORE-019..023, 024..027
    """

    cst = CST()
    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj_frozen = make_identity_object("F", frozen=True)
    obj_thawed = make_identity_object("T", frozen=False)

    signals = cst.run(
        identity_objects=[obj_frozen, obj_thawed],
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=2,
    )

    assert "F" in signals.freeze["frozen_objects"]
    assert "T" in signals.thaw["thawed_objects"]
    assert signals.freeze["reason"] == "stability_condition"
    assert signals.thaw["reason"] == "stability_condition"


# ---------------------------------------------------------------------------
# Certainty / Ambiguity Tests
# ---------------------------------------------------------------------------

def test_certainty_ambiguity_adjustments():
    """
    Test certainty/ambiguity adjustments.
    Covers:
    - HLR-CST-CORE-012..014
    """

    cst = CST()
    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj_high_cert = make_identity_object("HC", certainty="high", ambiguity="low")
    obj_low_cert = make_identity_object("LC", certainty="low", ambiguity="high")

    signals = cst.run(
        identity_objects=[obj_high_cert, obj_low_cert],
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=3,
    )

    assert "HC" in signals.certainty_adjustment["increased_certainty"]
    assert "LC" in signals.certainty_adjustment["decreased_certainty"]
    assert "LC" in signals.ambiguity_adjustment["increased_ambiguity"]
    assert "HC" in signals.ambiguity_adjustment["decreased_ambiguity"]


# ---------------------------------------------------------------------------
# Lineage Stability Tests
# ---------------------------------------------------------------------------

def test_lineage_stability():
    """
    Test lineage stability detection.
    Covers:
    - HLR-CST-CORE-028..031
    """

    cst = CST()
    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj_stable = make_identity_object("S", lineage_stability="stable")
    obj_unstable = make_identity_object("U", lineage_stability="unstable")

    signals = cst.run(
        identity_objects=[obj_stable, obj_unstable],
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=4,
    )

    assert "S" in signals.lineage_stability["stable_lineage"]
    assert "U" in signals.lineage_stability["unstable_lineage"]


# ---------------------------------------------------------------------------
# MERGE / SPLIT Structural Compensation Tests
# ---------------------------------------------------------------------------

def test_merge_split_compensation_no_false_instability():
    """
    Test that MERGE/SPLIT structural events do not produce false instability.
    Covers:
    - HLR-CST-CORE-019..023 (structural neutrality)
    - Merge/split compensation behavior
    """

    cst = CST()

    # MERGE: parents P1, P2 → child C
    tp_lineage_log = [
        {
            "event_type": "MERGE",
            "parent_ref": ["P1", "P2"],
            "child_refs": ["C"],
        }
    ]
    tp_snapshot = {"turn_index": 0, "objects": []}

    P1 = make_identity_object("P1", drift=0.9, collapse=True)
    P2 = make_identity_object("P2", drift=0.8, collapse=True)
    C = make_identity_object("C", drift=None, collapse=False)

    signals = cst.run(
        identity_objects=[P1, P2, C],
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=5,
    )

    # Parents should be compensated out of instability consideration
    assert "P1" not in signals.collapse["collapsed_objects"]
    assert "P2" not in signals.collapse["collapsed_objects"]

    # Child C is legitimate new layer; no collapse expected
    assert "C" not in signals.collapse["collapsed_objects"]


def test_split_compensation_no_false_instability():
    """
    Test that SPLIT structural events do not produce false instability.
    Covers:
    - HLR-CST-CORE-019..023 (structural neutrality)
    """

    cst = CST()

    # SPLIT: parent P → children C1, C2
    tp_lineage_log = [
        {
            "event_type": "SPLIT",
            "parent_ref": ["P"],
            "child_refs": ["C1", "C2"],
        }
    ]
    tp_snapshot = {"turn_index": 0, "objects": []}

    P = make_identity_object("P", drift=0.7, collapse=True)
    C1 = make_identity_object("C1", drift=None, collapse=False)
    C2 = make_identity_object("C2", drift=None, collapse=False)

    signals = cst.run(
        identity_objects=[P, C1, C2],
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=6,
    )

    # Parent should be compensated out of instability consideration
    assert "P" not in signals.collapse["collapsed_objects"]

    # Children are legitimate new layers; no collapse expected
    assert "C1" not in signals.collapse["collapsed_objects"]
    assert "C2" not in signals.collapse["collapsed_objects"]


# ---------------------------------------------------------------------------
# Post-Structure Stability Window Tests (10 turns)
# ---------------------------------------------------------------------------

def test_post_structure_stability_window_length():
    """
    Test that CST tracks a 10-turn post-structure stability window.
    Covers:
    - HLR-CST-CORE-032..036 (determinism, replay, window behavior)
    """

    cst = CST()
    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj = make_identity_object("X", drift=0.1)

    # Run CST for 15 turns; window should cap at 10
    for turn in range(1, 16):
        signals = cst.run(
            identity_objects=[obj],
            tp_lineage_log=tp_lineage_log,
            tp_snapshot=tp_snapshot,
            turn_index=turn,
        )
        assert signals.metadata["turn_index"] == turn

    assert len(cst.state.post_structure_stability_window) == 10
    # Last entry should correspond to turn 15
    last_signals = cst.state.post_structure_stability_window[-1]
    assert last_signals.metadata["turn_index"] == 15


# ---------------------------------------------------------------------------
# Determinism / Replay Tests
# ---------------------------------------------------------------------------

def test_determinism_replay_consistency():
    """
    Test that CST produces identical outputs under replay for identical inputs.
    Covers:
    - HLR-CST-CORE-032..036
    """

    cst1 = CST()
    cst2 = CST()

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    objs = [
        make_identity_object("A", drift=0.2, oscillation=0.1, collapse=False),
        make_identity_object("B", drift=0.3, oscillation=0.0, collapse=True),
    ]

    signals1 = cst1.run(
        identity_objects=objs,
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=10,
    )

    signals2 = cst2.run(
        identity_objects=objs,
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=10,
    )

    assert signals1.drift == signals2.drift
    assert signals1.oscillation == signals2.oscillation
    assert signals1.collapse == signals2.collapse
    assert signals1.freeze == signals2.freeze
    assert signals1.thaw == signals2.thaw
    assert signals1.certainty_adjustment == signals2.certainty_adjustment
    assert signals1.ambiguity_adjustment == signals2.ambiguity_adjustment
    assert signals1.lineage_stability == signals2.lineage_stability
    assert signals1.metadata == signals2.metadata


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n=== CST-Core Testbench: Running All Tests ===")

    test_basic_drift_oscillation_collapse()
    print("[PASS] Basic drift/oscillation/collapse test passed")

    test_freeze_thaw_behavior()
    print("[PASS] Freeze/thaw behavior test passed")

    test_certainty_ambiguity_adjustments()
    print("[PASS] Certainty/ambiguity adjustments test passed")

    test_lineage_stability()
    print("[PASS] Lineage stability test passed")

    test_merge_split_compensation_no_false_instability()
    print("[PASS] MERGE structural compensation test passed")

    test_split_compensation_no_false_instability()
    print("[PASS] SPLIT structural compensation test passed")

    test_post_structure_stability_window_length()
    print("[PASS] Post-structure stability window length test passed")

    test_determinism_replay_consistency()
    print("[PASS] Determinism/replay consistency test passed")

    print("\n=== CST-Core Testbench: All Tests Completed ===")

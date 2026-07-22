"""
CST-MS Testbench — System Playground Version

Validates CST-MS against:
- cst-ms.md (architecture)
- cst-ms_requirements.md (HLR-CST-MS-nnn)
- context_testbench.py (integration)

Tests cover:
- normalization
- weighting
- stability synthesis
- instability synthesis
- collapse/freeze/thaw risk
- ambiguity/drift/oscillation summaries
- merge/split neutrality
- merge/split detection
- 10-turn stability window
- determinism & replay
"""

from cst_ms import CST_MS
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
    certainty=None,
    ambiguity=None,
):
    """OuBA-like identity object for CST-Core → CST-MS testing."""
    return IdentityObject(
        id=id,
        referent_map={"r": "v"},
        anchors=["a1"],
        lineage={"stability": "stable"},
        ambiguity={"certainty": certainty, "ambiguity": ambiguity},
        stability_metrics={
            "drift": drift,
            "oscillation": oscillation,
            "collapse": collapse,
        },
        ordering_metrics={"recency": 0, "frequency": 0, "density": 0},
    )


def make_tp_placeholders():
    return [], {"turn_index": None, "objects": []}


# ---------------------------------------------------------------------------
# 1. Normalization Tests
# ---------------------------------------------------------------------------

def test_normalization_basic():
    """
    Tests:
    - HLR-CST-MS-005 (normalize)
    - HLR-CST-MS-006 (deterministic maxima)
    - HLR-CST-MS-007 (replay-safe)
    """

    cst = CST()
    ms = CST_MS()

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj = make_identity_object("A", drift=0.5, oscillation=0.2, collapse=False)
    signals = cst.run([obj], tp_lineage_log, tp_snapshot, turn_index=1).__dict__

    ms_signals = ms.run(signals, turn_index=1)

    assert ms_signals.normalized_metrics["drift"] == 0.5
    assert ms_signals.normalized_metrics["oscillation"] == 0.2
    assert ms_signals.normalized_metrics["collapse"] == 0.0
    assert ms_signals.normalized_metrics["continuity"] == 1.0


# ---------------------------------------------------------------------------
# 2. Weighting Tests
# ---------------------------------------------------------------------------

def test_weighting_basic():
    """
    Tests:
    - HLR-CST-MS-008 (apply weights)
    - HLR-CST-MS-009 (monotonic, deterministic)
    - HLR-CST-MS-010 (pure function)
    """

    cst = CST()
    ms = CST_MS()

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj = make_identity_object("A", drift=1.0, oscillation=1.0)
    signals = cst.run([obj], tp_lineage_log, tp_snapshot, turn_index=2).__dict__

    ms_signals = ms.run(signals, turn_index=2)

    wm = ms_signals.weighted_metrics

    assert wm["drift"] == 0.25
    assert wm["oscillation"] == 0.25
    assert wm["ambiguity"] == 0.0
    assert wm["collapse"] == 0.0


# ---------------------------------------------------------------------------
# 3. Stability / Instability Tests
# ---------------------------------------------------------------------------

def test_stability_instability_synthesis():
    """
    Tests:
    - HLR-CST-MS-011..015
    """

    cst = CST()
    ms = CST_MS()

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj = make_identity_object("A", drift=1.0, oscillation=1.0, collapse=False)
    signals = cst.run([obj], tp_lineage_log, tp_snapshot, turn_index=3).__dict__

    ms_signals = ms.run(signals, turn_index=3)

    stability = ms_signals.stability["value"]
    instability = ms_signals.instability["value"]

    assert 0.0 <= stability <= 1.0
    assert instability == 1.0 - stability


# ---------------------------------------------------------------------------
# 4. Risk Tests
# ---------------------------------------------------------------------------

def test_risk_computation():
    """
    Tests:
    - HLR-CST-MS-016..021
    """

    cst = CST()
    ms = CST_MS()

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj = make_identity_object("A", drift=0.5, oscillation=0.5, collapse=True)
    signals = cst.run([obj], tp_lineage_log, tp_snapshot, turn_index=4).__dict__

    ms_signals = ms.run(signals, turn_index=4)

    assert ms_signals.collapse_risk["value"] > 0.0
    assert ms_signals.freeze_risk["value"] >= ms_signals.collapse_risk["value"]
    assert ms_signals.thaw_readiness["value"] <= 1.0


# ---------------------------------------------------------------------------
# 5. Summary Tests
# ---------------------------------------------------------------------------

def test_summary_computation():
    """
    Tests:
    - HLR-CST-MS-022..024
    """

    cst = CST()
    ms = CST_MS()

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj1 = make_identity_object("A", drift=0.2, oscillation=0.1, certainty="low", ambiguity="high")
    obj2 = make_identity_object("B", drift=0.3, oscillation=0.2, certainty="high", ambiguity="low")

    signals = cst.run([obj1, obj2], tp_lineage_log, tp_snapshot, turn_index=5).__dict__
    ms_signals = ms.run(signals, turn_index=5)

    assert ms_signals.ambiguity_summary["count"] == 1
    assert ms_signals.drift_summary["magnitude"] == signals["drift"]["magnitude"]
    assert ms_signals.oscillation_summary["frequency"] == signals["oscillation"]["frequency"]


# ---------------------------------------------------------------------------
# 6. Merge/Split Neutrality Tests
# ---------------------------------------------------------------------------

def test_merge_split_neutrality():
    """
    Tests:
    - HLR-CST-MS-029..037
    """

    cst = CST()
    ms = CST_MS()

    # Fake merge event from CST-Core
    signals = {
        "drift": {"magnitude": 0.9},
        "oscillation": {"frequency": 0.4, "amplitude": 1},
        "collapse": {"severity": 1},
        "merge": {"merge_pairs": ["A", "B"], "confidence": 1},
        "split": {"split_objects": [], "confidence": 0},
        "freeze": {"frozen_objects": [], "reason": "none"},
        "thaw": {"thawed_objects": [], "reason": "none"},
        "certainty_adjustment": {"increased_certainty": [], "decreased_certainty": []},
        "ambiguity_adjustment": {"increased_ambiguity": [], "decreased_ambiguity": []},
        "lineage_stability": {"stable_lineage": [], "unstable_lineage": []},
        "metadata": {"turn_index": 6},
    }

    ms_signals = ms.run(signals, turn_index=6)

    # Merge must NOT produce instability by itself
    assert ms_signals.instability["value"] < 1.0
    assert ms_signals.collapse_risk["value"] <= 1.0


# ---------------------------------------------------------------------------
# 7. Stability Window Tests
# ---------------------------------------------------------------------------

def test_stability_window_length():
    """
    Tests:
    - HLR-CST-MS-025..028 (determinism, replay, window)
    """

    cst = CST()
    ms = CST_MS()

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj = make_identity_object("A", drift=0.1)

    for turn in range(1, 15):
        signals = cst.run([obj], tp_lineage_log, tp_snapshot, turn).__dict__
        ms.run(signals, turn)

    assert len(ms.state.stability_window) == 10
    assert ms.state.stability_window[-1]["stability"]["value"] >= 0.0


# ---------------------------------------------------------------------------
# 8. Determinism / Replay Tests
# ---------------------------------------------------------------------------

def test_determinism_replay():
    """
    Tests:
    - HLR-CST-MS-025..028
    """

    cst = CST()
    ms1 = CST_MS()
    ms2 = CST_MS()

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    objs = [
        make_identity_object("A", drift=0.2, oscillation=0.1),
        make_identity_object("B", drift=0.3, oscillation=0.0, collapse=True),
    ]

    signals = cst.run(objs, tp_lineage_log, tp_snapshot, turn_index=10).__dict__

    out1 = ms1.run(signals, turn_index=10)
    out2 = ms2.run(signals, turn_index=10)

    assert out1.normalized_metrics == out2.normalized_metrics
    assert out1.weighted_metrics == out2.weighted_metrics
    assert out1.stability == out2.stability
    assert out1.instability == out2.instability
    assert out1.collapse_risk == out2.collapse_risk
    assert out1.freeze_risk == out2.freeze_risk
    assert out1.thaw_readiness == out2.thaw_readiness
    assert out1.ambiguity_summary == out2.ambiguity_summary
    assert out1.drift_summary == out2.drift_summary
    assert out1.oscillation_summary == out2.oscillation_summary
    assert out1.metadata == out2.metadata


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n=== CST-MS Testbench: Running All Tests ===")

    test_normalization_basic()
    print("[PASS] Normalization test passed")

    test_weighting_basic()
    print("[PASS] Weighting test passed")

    test_stability_instability_synthesis()
    print("[PASS] Stability/instability synthesis test passed")

    test_risk_computation()
    print("[PASS] Risk computation test passed")

    test_summary_computation()
    print("[PASS] Summary computation test passed")

    test_merge_split_neutrality()
    print("[PASS] Merge/split neutrality test passed")

    test_stability_window_length()
    print("[PASS] Stability window test passed")

    test_determinism_replay()
    print("[PASS] Determinism/replay test passed")

    print("\n=== CST-MS Testbench: All Tests Completed ===")

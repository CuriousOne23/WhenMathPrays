"""
CST-Mux Testbench — System Playground Version

Validates CST-Mux against:
- cst-mux.md (architecture)
- cst-mux_requirements.md (HLR-CST-MUX-nnn)
- cst-ms.py (upstream synthesis module)

Tests cover:
- activation flags
- freeze flags
- thaw flags
- continuity flags
- USP construction
- merge/split neutrality
- 10-turn USP window
- determinism & replay
"""

from cst_mux import CST_MUX
from cst_ms.cst_ms import CST_MS
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
    """OuBA-like identity object for CST-Core → CST-MS → CST-Mux testing."""
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


def run_pipeline(objs, turn_index):
    """
    Runs CST → CST-MS → CST-Mux pipeline for test convenience.
    """
    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    cst = CST()
    ms = CST_MS()
    mux = CST_MUX()

    cst_signals = cst.run(objs, tp_lineage_log, tp_snapshot, turn_index).__dict__
    ms_signals = ms.run(cst_signals, turn_index).__dict__
    usp = mux.run(ms_signals, turn_index)

    return usp, mux


# ---------------------------------------------------------------------------
# 1. Activation Flag Tests
# ---------------------------------------------------------------------------

def test_activation_flags():
    """
    Tests:
    - HLR-CST-MUX-001..005
    """

    obj = make_identity_object("A", drift=1.0)
    usp, mux = run_pipeline([obj], turn_index=1)

    assert "activated" in usp.activation_flags
    assert usp.activation_flags["activated"] in (True, False)
    assert usp.activation_flags["stability_value"] == usp.stability["value"]


# ---------------------------------------------------------------------------
# 2. Freeze Flag Tests
# ---------------------------------------------------------------------------

def test_freeze_flags():
    """
    Tests:
    - HLR-CST-MUX-006..010
    """

    obj = make_identity_object("A", collapse=True)
    usp, mux = run_pipeline([obj], turn_index=2)

    assert "frozen" in usp.freeze_flags
    assert usp.freeze_flags["freeze_risk"] == usp.freeze_risk["value"]


# ---------------------------------------------------------------------------
# 3. Thaw Flag Tests
# ---------------------------------------------------------------------------

def test_thaw_flags():
    """
    Tests:
    - HLR-CST-MUX-011..013
    """

    obj = make_identity_object("A", drift=0.0, oscillation=0.0, collapse=False)
    usp, mux = run_pipeline([obj], turn_index=3)

    assert "thawed" in usp.thaw_flags
    assert usp.thaw_flags["thaw_readiness"] == usp.thaw_readiness["value"]


# ---------------------------------------------------------------------------
# 4. Continuity Flag Tests
# ---------------------------------------------------------------------------

def test_continuity_flags():
    """
    Tests:
    - HLR-CST-MUX-014..015
    """

    obj = make_identity_object("A", drift=0.1)
    usp, mux = run_pipeline([obj], turn_index=4)

    assert "continuous" in usp.continuity_flags
    assert usp.continuity_flags["stability_value"] == usp.stability["value"]


# ---------------------------------------------------------------------------
# 5. USP Construction Tests
# ---------------------------------------------------------------------------

def test_usp_construction():
    """
    Tests:
    - HLR-CST-MUX-016..018
    """

    obj = make_identity_object("A", drift=0.3, oscillation=0.2)
    usp, mux = run_pipeline([obj], turn_index=5)

    assert usp.stability["value"] >= 0.0
    assert usp.instability["value"] == 1.0 - usp.stability["value"]
    assert usp.drift_summary["magnitude"] >= 0.0
    assert usp.oscillation_summary["frequency"] >= 0.0

    # ---------------------------------------------------------------------------
    # NEW_CONTEXT_REQUIRED Tests (HLR‑CST‑MUX‑003A, 017A, 032A)
    # ---------------------------------------------------------------------------
    
    def test_new_context_required_flag():
        """
        Tests:
        - CST‑Mux accepts new_context_required from CST‑MS
        - CST‑Mux propagates new_context_required into USP
        - Replay determinism
        """
    
        # Create object that triggers continuity break → CST‑MS sets new_context_required=True
        obj = make_identity_object("A", collapse=True)
    
        # Run pipeline
        usp, mux = run_pipeline([obj], turn_index=50)
    
        print("\n--- NEW_CONTEXT_REQUIRED Flag ---")
        print("USP new_context_required:", usp.get("new_context_required"))
    
        # 1. USP must contain new_context_required=True
        assert usp.get("new_context_required") is True
    
        # 2. Replay determinism
        usp2, mux2 = run_pipeline([obj], turn_index=50)
        assert usp2.get("new_context_required") is True

# ---------------------------------------------------------------------------
# 6. Merge/Split Neutrality Tests
# ---------------------------------------------------------------------------

def test_merge_split_neutrality():
    """
    Tests:
    - HLR-CST-MUX-019..022
    """

    # Fake merge event from CST-Core
    cst_signals = {
        "drift": {"magnitude": 0.5},
        "oscillation": {"frequency": 0.2, "amplitude": 1},
        "collapse": {"severity": 0},
        "merge": {"merge_pairs": ["A", "B"], "confidence": 1},
        "split": {"split_objects": [], "confidence": 0},
        "freeze": {"frozen_objects": [], "reason": "none"},
        "thaw": {"thawed_objects": [], "reason": "none"},
        "certainty_adjustment": {"increased_certainty": [], "decreased_certainty": []},
        "ambiguity_adjustment": {"increased_ambiguity": [], "decreased_ambiguity": []},
        "lineage_stability": {"stable_lineage": [], "unstable_lineage": []},
        "metadata": {"turn_index": 6},
    }

    ms = CST_MS()
    mux = CST_MUX()

    ms_signals = ms.run(cst_signals, turn_index=6).__dict__
    usp = mux.run(ms_signals, turn_index=6)

    # Merge must NOT produce instability by itself
    assert usp.instability["value"] < 1.0
    assert usp.freeze_risk["value"] <= 1.0


# ---------------------------------------------------------------------------
# 7. USP Window Tests
# ---------------------------------------------------------------------------

def test_usp_window_length():
    """
    Tests:
    - HLR-CST-MUX-023..029
    """

    cst = CST()
    ms = CST_MS()
    mux = CST_MUX()

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    obj = make_identity_object("A", drift=0.1)

    for turn in range(1, 15):
        cst_signals = cst.run([obj], tp_lineage_log, tp_snapshot, turn).__dict__
        ms_signals = ms.run(cst_signals, turn).__dict__
        mux.run(ms_signals, turn)

    assert len(mux.state.usp_window) == 10
    assert mux.state.usp_window[-1]["stability"]["value"] >= 0.0


# ---------------------------------------------------------------------------
# 8. Determinism / Replay Tests
# ---------------------------------------------------------------------------

def test_determinism_replay():
    """
    Tests:
    - HLR-CST-MUX-030..033
    """

    cst = CST()
    ms1 = CST_MS()
    ms2 = CST_MS()
    mux1 = CST_MUX()
    mux2 = CST_MUX()

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    objs = [
        make_identity_object("A", drift=0.2, oscillation=0.1),
        make_identity_object("B", drift=0.3, oscillation=0.0, collapse=True),
    ]

    cst_signals = cst.run(objs, tp_lineage_log, tp_snapshot, turn_index=10).__dict__

    ms_out1 = ms1.run(cst_signals, turn_index=10).__dict__
    ms_out2 = ms2.run(cst_signals, turn_index=10).__dict__

    usp1 = mux1.run(ms_out1, turn_index=10)
    usp2 = mux2.run(ms_out2, turn_index=10)

    assert usp1.activation_flags == usp2.activation_flags
    assert usp1.freeze_flags == usp2.freeze_flags
    assert usp1.thaw_flags == usp2.thaw_flags
    assert usp1.continuity_flags == usp2.continuity_flags
    assert usp1.stability == usp2.stability
    assert usp1.instability == usp2.instability
    assert usp1.collapse_risk == usp2.collapse_risk
    assert usp1.freeze_risk == usp2.freeze_risk
    assert usp1.thaw_readiness == usp2.thaw_readiness
    assert usp1.ambiguity_summary == usp2.ambiguity_summary
    assert usp1.drift_summary == usp2.drift_summary
    assert usp1.oscillation_summary == usp2.oscillation_summary
    assert usp1.metadata == usp2.metadata


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n=== CST-Mux Testbench: Running All Tests ===")

    test_activation_flags()
    print("[PASS] Activation flag test passed")

    test_freeze_flags()
    print("[PASS] Freeze flag test passed")

    test_thaw_flags()
    print("[PASS] Thaw flag test passed")

    test_continuity_flags()
    print("[PASS] Continuity flag test passed")

    test_usp_construction()
    print("[PASS] USP construction test passed")

    test_new_context_required_flag()
    print("[PASS] NEW_CONTEXT_REQUIRED flag test passed")

    test_merge_split_neutrality()
    print("[PASS] Merge/split neutrality test passed")

    test_usp_window_length()
    print("[PASS] USP window test passed")

    test_determinism_replay()
    print("[PASS] Determinism/replay test passed")

    print("\n=== CST-Mux Testbench: All Tests Completed ===")

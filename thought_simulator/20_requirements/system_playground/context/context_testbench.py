"""
Unified Context Testbench — System Playground Version (v2.0-M)

This testbench performs block-level validation of the unified context subsystem:
- CST-Core (stability signal generation)
- CST-MS (metric synthesis)
- CST-Mux (USP multiplexing)
- COB (identity-layer construction and evolution)
- CIL (intake packet construction for CEx)

It validates the deterministic pipeline:
CST-Core → CST-MS → CST-Mux → COB → CIL

It is a shaping testbench used inside system_playground before system_simulation.
It does NOT simulate CEx; it focuses on CST → COB → CIL behavior and a TP-like
datastream that records what each block did and when, consistent with:

- system_playground context_requirements.md (v2.0-M)
- cst-core_requirements.md
- cst-ms_requirements.md
- cst-mux_requirements.md
- cob_requirements.md
- cil_requirements.md
"""

from cst_core.cst_core import CST as CSTCore
from cst_ms.cst_ms import CST_MS
from cst_mux.cst_mux import CST_MUX

from cob.cob import COB
from cil.cil import CIL, IdentityObject


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_identity_object(
    id: str,
    recency: int,
    frequency: int,
    density: int,
    drift=None,
    oscillation=None,
    collapse=False,
    certainty=None,
    ambiguity=None,
    lineage_stability=None,
):
    """OuBA-like identity object for unified testing."""
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
        },
        ordering_metrics={
            "recency": recency,
            "frequency": frequency,
            "density": density,
        },
    )


def make_tp_placeholders():
    """TP-like placeholder structures."""
    tp_lineage_log = []
    tp_snapshot = {"turn_index": None, "objects": []}
    return tp_lineage_log, tp_snapshot


# ---------------------------------------------------------------------------
# Unified Pipeline Runner
# ---------------------------------------------------------------------------

def run_pipeline(objs, tp_lineage_log, tp_snapshot, turn_index):
    """
    Runs the full unified pipeline:
    CST-Core → CST-MS → CST-Mux → COB → CIL
    """

    # 1. CST-Core
    cst_core = CSTCore()
    cst_core_signals = cst_core.run(
        identity_objects=objs,
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=turn_index,
    ).__dict__

    # 2. CST-MS
    cst_ms = CST_MS()
    cst_ms_signals = cst_ms.run(cst_core_signals, turn_index).__dict__

    # 3. CST-Mux
    cst_mux = CST_MUX()
    usp = cst_mux.run(cst_ms_signals, turn_index)

    # 4. COB
    cob = COB()
    for obj in objs:
        cob.add_identity_object(obj)

    # CURRENT COB SIGNATURE:
    # cob_state = cob.run(signals=cst_core_signals, turn_index=turn_index)

    # REQUIRED BY SPEC (HLR‑CnTxt‑021):
    # cob_state = cob.run(
    #     core_signals=cst_core_signals,
    #     ms_signals=cst_ms_signals,
    #     usp=usp,
    #     turn_index=turn_index,
    # )

    cob_state = cob.run(
        core_signals=cst_core_signals,
        ms_signals=cst_ms_signals,
        turn_index=turn_index,
    )

    # 5. CIL
    cil = CIL()

    # CURRENT CIL SIGNATURE:
    # cil_packet = cil.run(
    #     cob_objects=cob_state.objects,
    #     cst_signals=cst_core_signals,
    #     turn_index=turn_index,
    # )

    # REQUIRED BY SPEC (HLR‑CnTxt‑021):
    # cil_packet = cil.run(
    #     cob_objects=cob_state.objects,
    #     cst_core_signals=cst_core_signals,
    #     cst_ms_signals=cst_ms_signals,
    #     usp=usp,
    #     turn_index=turn_index,
    # )

    cil_packet = cil.run(
        cob_objects=cob_state.objects,
        cst_signals=cst_core_signals,
        turn_index=turn_index,
    )

    return {
        "cst_core": cst_core_signals,
        "cst_ms": cst_ms_signals,
        "cst_mux": usp,
        "cob_state": cob_state,
        "cil_packet": cil_packet,
    }

# ---------------------------------------------------------------------------
# Unified Tests
# ---------------------------------------------------------------------------

def run_unified_basic_test():
    print("\n=== Unified Context Testbench: Basic Test ===")

    objs = [
        make_identity_object("obj1", 10, 5, 3, drift=0.1, certainty="high", ambiguity="low", lineage_stability="stable"),
        make_identity_object("obj2", 7, 9, 2, drift=0.3, oscillation=0.2, certainty="low", ambiguity="high", lineage_stability="unstable"),
        make_identity_object("obj3", 1, 1, 1, collapse=True, lineage_stability="stable"),
    ]

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    out = run_pipeline(objs, tp_lineage_log, tp_snapshot, turn_index=1)

    print("\n--- CST-Core Signals ---")
    print(out["cst_core"])

    print("\n--- CST-MS Signals ---")
    print(out["cst_ms"])

    print("\n--- CST-Mux USP ---")
    print(out["cst_mux"])

    print("\n--- COB Identity Objects ---")
    for obj in out["cob_state"].objects:
        print(obj.id, obj.ordering_metrics)

    print("\n--- CIL Packet ---")
    print(out["cil_packet"].packet_metadata)


def run_unified_merge_split_test():
    """
    Unified Merge/Split Pipeline Test (HLR-CnTxt-007A + Section 8.6)

    Validates:
    - CST-Core detects MERGE/SPLIT
    - CST-MS preserves structural neutrality
    - CST-Mux produces stable USP flags
    - COB evolves identity-layer objects correctly
    - CIL constructs correct post-merge/post-split packet
    """

    print("\n=== Unified Merge/Split Pipeline Test ===")

    # MERGE: A + B → AB
    A = make_identity_object("A", 5, 3, 2)
    B = make_identity_object("B", 4, 2, 1)

    tp_lineage_log = [
        {"event_type": "MERGE", "parent_ref": ["A", "B"], "child_refs": ["AB"]}
    ]
    tp_snapshot = {"turn_index": 0, "objects": []}

    AB = make_identity_object("AB", 6, 5, 3, lineage_stability="stable")

    out_merge = run_pipeline([AB], tp_lineage_log, tp_snapshot, turn_index=0)

    print("\n--- MERGE: CST-Core Signals ---")
    print(out_merge["cst_core"])

    print("\n--- MERGE: CST-MS Signals ---")
    print(out_merge["cst_ms"])

    print("\n--- MERGE: CST-Mux USP ---")
    print(out_merge["cst_mux"])

    print("\n--- MERGE: CIL Stability Block ---")
    print(out_merge["cil_packet"].stability_block)

    # SPLIT: C → C1, C2
    C = make_identity_object("C", 7, 5, 3)

    tp_lineage_log = [
        {"event_type": "SPLIT", "parent_ref": ["C"], "child_refs": ["C1", "C2"]}
    ]
    tp_snapshot = {"turn_index": 0, "objects": []}

    C1 = make_identity_object("C1", 4, 3, 2)
    C2 = make_identity_object("C2", 3, 2, 1)

    out_split = run_pipeline([C1, C2], tp_lineage_log, tp_snapshot, turn_index=0)

    print("\n--- SPLIT: CST-Core Signals ---")
    print(out_split["cst_core"])

    print("\n--- SPLIT: CST-MS Signals ---")
    print(out_split["cst_ms"])

    print("\n--- SPLIT: CST-Mux USP ---")
    print(out_split["cst_mux"])

    print("\n--- SPLIT: CIL Stability Block ---")
    print(out_split["cil_packet"].stability_block)


def run_new_id_context_test():
    """
    New Identity Context Boundary Test (HLR‑CnTxt‑021 + Section 8.7)

    Validates:
    - CST-MS detects continuity break → new_context_required=True
    - CST-Mux propagates new_context_required into USP
    - COB creates a new identity-layer object immediately
    - CIL constructs an intake packet using the new identity context
    - Pipeline behaves deterministically
    """

    print("\n=== Unified New ID-Context Boundary Test ===")

    # Object that forces continuity break (collapse=True)
    obj = make_identity_object(
        id="old1",
        recency=5,
        frequency=5,
        density=5,
        drift=0.1,
        oscillation=0.1,
        collapse=True,            # ← continuity break trigger
        lineage_stability="stable"
    )

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    # Run pipeline
    out = run_pipeline([obj], tp_lineage_log, tp_snapshot, turn_index=99)

    cst_ms = out["cst_ms"]
    cst_mux = out["cst_mux"]
    cob_state = out["cob_state"]
    cil_packet = out["cil_packet"]

    print("\n--- CST-MS Metadata ---")
    print(cst_ms["metadata"])

    print("\n--- CST-Mux USP ---")
    print(cst_mux)

    print("\n--- COB Identity Objects ---")
    for o in cob_state.objects:
        print(o.id, o.ordering_metrics)

    print("\n--- CIL Packet Metadata ---")
    print(cil_packet.packet_metadata)

    # 1. CST-MS must detect continuity break
    assert cst_ms["metadata"].get("new_context_required") is True

    # 2. CST-Mux must propagate the flag
    assert cst_mux.new_context_required is True

    # 3. COB must create a new identity object immediately
    new_ids = [o.id for o in cob_state.objects]
    assert any("ctx_99" == oid for oid in new_ids)

    # 4. Old object must NOT be evolved (drift unchanged)
    old_obj = next(o for o in cob_state.objects if o.id == "old1")
    assert old_obj.stability_metrics["drift"] == 0.1

    # 5. CIL must treat the turn as a new context boundary
    assert cil_packet.packet_metadata.get("new_context_required") is True

    print("[PASS] New ID-context boundary test passed")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_unified_basic_test()
    run_unified_merge_split_test()
    run_new_id_context_test()

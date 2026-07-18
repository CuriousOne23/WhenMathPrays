"""
Unified Context Testbench — System Playground Version

This testbench performs block-level validation of the unified context subsystem:
- CST (stability analysis)
- COB (identity-layer construction and evolution)
- CIL (intake packet construction for CEx)

It is a shaping testbench used inside system_playground before system_simulation.
It does NOT simulate CEx; it focuses on CST → COB → CIL behavior and a TP-like
datastream that records what each block did and when.
"""

from cst.cst import CST
from cob.cob import COB
from cil.cil import CIL, IdentityObject


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_ouba_identity_object(
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
    """
    Helper to create OuBA-like IdentityObject instances for unified testing.

    These objects approximate the identity-layer structures that OuBA would
    provide to the context subsystem in system_playground.
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
            "merge_split": None,
            "freeze_thaw": None,
        },
        ordering_metrics={
            "recency": recency,
            "frequency": frequency,
            "density": density,
        },
    )


def make_tp_placeholders():
    """
    Create TP-like placeholder structures for system_playground.

    In system_simulation, these would be real TP records. Here they are
    simple dictionaries used to track what CST, COB, and CIL did.
    """

    tp_lineage_log = []
    tp_snapshot = {"turn_index": None, "objects": []}
    return tp_lineage_log, tp_snapshot


# ---------------------------------------------------------------------------
# Unified Tests
# ---------------------------------------------------------------------------

def run_unified_basic_test():
    """
    Run a basic unified context test with three identity objects.

    Sequence:
    1. CST processes OuBA-like identity objects and TP lineage/snapshot.
    2. COB evolves identity-layer objects using CST signals.
    3. CIL constructs the intake packet using COB objects and CST signals.
    4. TP-like datastream is assembled to show historical continuity.
    """

    print("\n=== Unified Context Testbench: Basic Test ===")

    # OuBA-like identity objects
    obj1 = make_ouba_identity_object(
        id="obj1",
        recency=10,
        frequency=5,
        density=3,
        drift=0.1,
        oscillation=0.0,
        collapse=False,
        certainty="high",
        ambiguity="low",
        lineage_stability="stable",
    )

    obj2 = make_ouba_identity_object(
        id="obj2",
        recency=7,
        frequency=9,
        density=2,
        drift=0.3,
        oscillation=0.2,
        collapse=False,
        certainty="low",
        ambiguity="high",
        lineage_stability="unstable",
    )

    obj3 = make_ouba_identity_object(
        id="obj3",
        recency=1,
        frequency=1,
        density=1,
        drift=None,
        oscillation=None,
        collapse=True,
        certainty=None,
        ambiguity=None,
        lineage_stability="stable",
    )

    ouba_objects = [obj1, obj2, obj3]
    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    # -----------------------------------------------------------------------
    # 1. CST Execution
    # -----------------------------------------------------------------------

    cst = CST()
    cst_signals = cst.run(
        identity_objects=ouba_objects,
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=1,
    )

    print("\n--- CST Signals ---")
    print(cst_signals)

    # -----------------------------------------------------------------------
    # 2. COB Execution
    # -----------------------------------------------------------------------

    cob = COB()
    # Add raw identity objects to COB
    for obj in ouba_objects:
        cob.add_identity_object(obj)
    
    # Run COB with CST signals
    cob_state = cob.run(
        signals=cst_signals,
        turn_index=1,
    )

    print("\n--- COB Identity Objects ---")
    for obj in cob_state:
        print(
            obj.id,
            {
                "recency": obj.ordering_metrics.get("recency"),
                "frequency": obj.ordering_metrics.get("frequency"),
                "density": obj.ordering_metrics.get("density"),
            },
        )

    # -----------------------------------------------------------------------
    # 3. CIL Execution
    # -----------------------------------------------------------------------

    cil = CIL()
    cil_packet = cil.run(
        cob_state=cob_state,
        cst_signals=cst_signals,
        turn_index=1,
    )

    print("\n--- CIL Identity Selection Block ---")
    for entry in cil_packet.identity_selection_block:
        print(entry["id"], entry["ordering_metrics"])

    print("\n--- CIL Certainty Block ---")
    print(cil_packet.referent_certainty_block)

    print("\n--- CIL Stability Block ---")
    print(cil_packet.stability_block)

    print("\n--- CIL Lineage Block ---")
    print(cil_packet.lineage_block)

    print("\n--- CIL Ordering Block ---")
    print(cil_packet.ordering_block)

    print("\n--- CIL CST Block ---")
    print(cil_packet.cst_block)

    print("\n--- CIL Packet Metadata ---")
    print(cil_packet.packet_metadata)

    # -----------------------------------------------------------------------
    # 4. TP-like Datastream Assembly
    # -----------------------------------------------------------------------

    tp_datastream = {
        "cst_signals": cst_signals,
        "cob_state": cob_state,
        "cil_packet": cil_packet,
        "metadata": {
            "turn_index": 1,
            "input_object_count": len(ouba_objects),
        },
    }

    print("\n--- TP Datastream (Unified View) ---")
    print(tp_datastream)


def run_unified_selection_stability_test():
    """
    Test unified behavior focusing on selection ordering and stability propagation.

    This test checks:
    - CST stability signals for a varied set of objects.
    - COB evolution under those signals.
    - CIL selection ordering and stability aggregation.
    """

    print("\n=== Unified Context Testbench: Selection + Stability Test ===")

    objs = [
        make_ouba_identity_object("A", recency=1, frequency=1, density=1, drift=0.1),
        make_ouba_identity_object("B", recency=5, frequency=1, density=1, oscillation=0.2),
        make_ouba_identity_object("C", recency=5, frequency=3, density=1, collapse=False),
        make_ouba_identity_object("D", recency=5, frequency=3, density=4, collapse=True),
        make_ouba_identity_object("E", recency=2, frequency=9, density=9, drift=0.4),
    ]

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    cst = CST()
    cst_signals = cst.run(
        identity_objects=objs,
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=2,
    )

    cob = COB()
    cob_state = cob.run(
        raw_objects=objs,
        cst_signals=cst_signals,
        turn_index=2,
    )

    cil = CIL()
    cil_packet = cil.run(
        cob_state=cob_state,
        cst_signals=cst_signals,
        turn_index=2,
    )

    print("\n--- Selection Order (CIL Identity Selection Block) ---")
    for entry in cil_packet.identity_selection_block:
        print(entry["id"], entry["ordering_metrics"])

    print("\n--- CIL Stability Block ---")
    print(cil_packet.stability_block)


def run_unified_tp_focus_test():
    """
    Test unified behavior with emphasis on TP-like datastream structure.

    This test is less about numeric values and more about:
    - presence of CST, COB, and CIL contributions
    - ordering of entries
    - metadata consistency
    """

    print("\n=== Unified Context Testbench: TP Focus Test ===")

    objs = [
        make_ouba_identity_object("T1", recency=3, frequency=2, density=1),
        make_ouba_identity_object("T2", recency=6, frequency=4, density=2),
    ]

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    cst = CST()
    cst_signals = cst.run(
        identity_objects=objs,
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=3,
    )

    cob = COB()
    cob_state = cob.run(
        raw_objects=objs,
        cst_signals=cst_signals,
        turn_index=3,
    )

    cil = CIL()
    cil_packet = cil.run(
        cob_state=cob_state,
        cst_signals=cst_signals,
        turn_index=3,
    )

    tp_datastream = {
        "cst_signals": cst_signals,
        "cob_state": cob_state,
        "cil_packet": cil_packet,
        "metadata": {
            "turn_index": 3,
            "input_object_count": len(objs),
        },
    }

    print("\n--- TP Datastream (Structure Check) ---")
    print(tp_datastream)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_unified_basic_test()
    run_unified_selection_stability_test()
    run_unified_tp_focus_test()


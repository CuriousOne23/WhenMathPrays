```python
"""
Unified Context Testbench — System Playground Version

This testbench performs block-level validation of the unified context subsystem:
- CST (stability analysis)
- COB (identity-layer construction and evolution)
- CIL (intake packet construction for CEx)

It is a shaping testbench used inside system_playground before system_simulation.
It does NOT simulate CEx; it focuses on CST → COB → CIL behavior and a TP-like
datastream that records what each block did and when, consistent with:

- system_playground context_requirements.md
- cst_requirements.md
- cob_requirements.md
- cil_requirements.md
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
    provide to the context subsystem in system_playground. They carry:

    - referent_map
    - anchors
    - lineage stability hints
    - certainty/ambiguity indicators
    - stability metrics (drift, oscillation, collapse, merge/split, freeze/thaw)
    - ordering metrics (recency, frequency, density)
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
    simple dictionaries used to track what CST, COB, and CIL did:

    - tp_lineage_log: structural continuity markers
    - tp_snapshot: stabilized identity-layer snapshot
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

    This test gives a baseline view of:
    - stability signals from CST
    - bounded identity store and ordering in COB
    - identity selection, certainty, stability, lineage, and ordering blocks in CIL
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
    for obj in ouba_objects:
        cob.add_identity_object(obj)

    cob_state = cob.run(
        signals=cst_signals.__dict__,
        turn_index=1,
    )

    print("\n--- COB Identity Objects ---")
    for obj in cob_state.objects:
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
        cob_objects=cob_state.objects,
        cst_signals=cst_signals.__dict__,
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
        "cst_signals": cst_signals.__dict__,
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
    - CST stability signals for a varied set of objects
    - COB evolution under those signals
    - CIL selection ordering and stability aggregation

    It is useful for visually confirming that:
    - ordering metrics drive identity selection deterministically
    - stability metrics from CST are preserved and aggregated in CIL
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
    for obj in objs:
        cob.add_identity_object(obj)

    cob_state = cob.run(
        signals=cst_signals.__dict__,
        turn_index=2,
    )

    cil = CIL()
    cil_packet = cil.run(
        cob_objects=cob_state.objects,
        cst_signals=cst_signals.__dict__,
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

    It helps confirm that a TP-like record can capture:
    - what CST did
    - what COB did
    - what CIL produced
    - when each action occurred
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
    for obj in objs:
        cob.add_identity_object(obj)

    cob_state = cob.run(
        signals=cst_signals.__dict__,
        turn_index=3,
    )

    cil = CIL()
    cil_packet = cil.run(
        cob_objects=cob_state.objects,
        cst_signals=cst_signals.__dict__,
        turn_index=3,
    )

    tp_datastream = {
        "cst_signals": cst_signals.__dict__,
        "cob_state": cob_state,
        "cil_packet": cil_packet,
        "metadata": {
            "turn_index": 3,
            "input_object_count": len(objs),
        },
    }

    print("\n--- TP Datastream (Structure Check) ---")
    print(tp_datastream)


def run_unified_merge_split_instability_test():
    """
    Unified Context Testbench: Merge/Split Structural Stability Test (OuBA-driven)

    This test validates:
    1. CST's interpretation of merge/split events from OuBA identity objects.
    2. CST's ability to avoid false instability during structural transitions.
    3. CST's pass-through of real instability on unrelated objects.
    4. COB and CIL propagation of structural vs. real instability.

    It does not enforce a specific suppression window; instead it inspects how
    CST, COB, and CIL behave across multiple cycles around merge/split events.
    """

    print("\n=== Unified Context Testbench: Merge/Split Structural Stability Test ===")

    # -----------------------------------------------------------------------
    # MERGE SCENARIO: A + B → AB
    # -----------------------------------------------------------------------

    print("\n--- MERGE SCENARIO (A + B -> AB) ---")

    # OuBA identity objects BEFORE merge (conceptual)
    A = make_ouba_identity_object("A", recency=5, frequency=3, density=2)
    B = make_ouba_identity_object("B", recency=4, frequency=2, density=1)

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    # Cycle 0: OuBA performs merge → OuBA now outputs AB instead of A and B
    AB = make_ouba_identity_object(
        "AB",
        recency=6,
        frequency=5,
        density=3,
        lineage_stability="stable",
    )

    cst = CST()
    cst_signals = cst.run(
        identity_objects=[AB],
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=0,
    )

    cob = COB()
    cob.add_identity_object(AB)
    cob_state = cob.run(signals=cst_signals.__dict__, turn_index=0)

    cil = CIL()
    cil_packet = cil.run(
        cob_objects=cob_state.objects,
        cst_signals=cst_signals.__dict__,
        turn_index=0,
    )

    print("\nCycle 0 — Merge Event Observed")
    print("CIL Stability Block:", cil_packet.stability_block)

    # -----------------------------------------------------------------------
    # Cycles 1–5: Observe structural behavior and real instability on X
    # -----------------------------------------------------------------------

    print("\n--- Merge Scenario: Structural vs Real Instability Observation ---")

    for cycle in range(1, 6):

        # Structural changes on AB (simulated)
        AB.stability_metrics["drift"] = 0.9
        AB.stability_metrics["collapse"] = True

        # Real instability on unrelated object X
        X = make_ouba_identity_object(
            "X",
            recency=2,
            frequency=1,
            density=1,
            oscillation=0.4,
        )

        ouba_objects = [AB, X]

        cst_signals = cst.run(
            identity_objects=ouba_objects,
            tp_lineage_log=tp_lineage_log,
            tp_snapshot=tp_snapshot,
            turn_index=cycle,
        )

        cob_state = cob.run(signals=cst_signals.__dict__, turn_index=cycle)
        cil_packet = cil.run(
            cob_objects=cob_state.objects,
            cst_signals=cst_signals.__dict__,
            turn_index=cycle,
        )

        print(f"\nCycle {cycle} — Merge Scenario")
        print("CIL Stability Block:", cil_packet.stability_block)

    # -----------------------------------------------------------------------
    # SPLIT SCENARIO: C → C1, C2
    # -----------------------------------------------------------------------

    print("\n--- SPLIT SCENARIO (C -> C1, C2) ---")

    C = make_ouba_identity_object("C", recency=7, frequency=5, density=3)

    tp_lineage_log, tp_snapshot = make_tp_placeholders()

    # Cycle 0: OuBA performs split → outputs C1 and C2
    C1 = make_ouba_identity_object("C1", recency=4, frequency=3, density=2)
    C2 = make_ouba_identity_object("C2", recency=3, frequency=2, density=1)

    cst_signals = cst.run(
        identity_objects=[C1, C2],
        tp_lineage_log=tp_lineage_log,
        tp_snapshot=tp_snapshot,
        turn_index=0,
    )

    cob = COB()
    cob.add_identity_object(C1)
    cob.add_identity_object(C2)

    cob_state = cob.run(signals=cst_signals.__dict__, turn_index=0)

    cil = CIL()
    cil_packet = cil.run(
        cob_objects=cob_state.objects,
        cst_signals=cst_signals.__dict__,
        turn_index=0,
    )

    print("\nCycle 0 — Split Event Observed")
    print("CIL Stability Block:", cil_packet.stability_block)

    print("\n--- Split Scenario: Structural vs Real Instability Observation ---")

    for cycle in range(1, 6):

        # Structural changes on C1/C2 (simulated)
        C1.stability_metrics["collapse"] = True
        C2.stability_metrics["drift"] = 0.8

        # Real instability on unrelated Y
        Y = make_ouba_identity_object(
            "Y",
            recency=1,
            frequency=1,
            density=1,
            oscillation=0.3,
        )

        ouba_objects = [C1, C2, Y]

        cst_signals = cst.run(
            identity_objects=ouba_objects,
            tp_lineage_log=tp_lineage_log,
            tp_snapshot=tp_snapshot,
            turn_index=cycle,
        )

        cob_state = cob.run(signals=cst_signals.__dict__, turn_index=cycle)
        cil_packet = cil.run(
            cob_objects=cob_state.objects,
            cst_signals=cst_signals.__dict__,
            turn_index=cycle,
        )

        print(f"\nCycle {cycle} — Split Scenario")
        print("CIL Stability Block:", cil_packet.stability_block)

    print("\n=== End of Merge/Split Structural Stability Test ===")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_unified_basic_test()
    run_unified_selection_stability_test()
    run_unified_tp_focus_test()
    run_unified_merge_split_instability_test()
```

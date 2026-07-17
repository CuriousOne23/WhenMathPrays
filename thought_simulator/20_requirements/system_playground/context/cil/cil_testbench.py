"""
CIL Testbench — System Playground Version

This testbench performs block-level validation of the CIL subsystem.
It tests:
- identity selection
- certainty aggregation
- stability aggregation
- lineage aggregation
- ordering aggregation
- intake packet construction

This is NOT a full system simulation. It is a shaping testbench used
inside system_playground before system_simulation.
"""

from cil import CIL, IdentityObject


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
    """Helper to create IdentityObject instances for testing."""

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


def run_basic_test():
    """Run a basic CIL test with three identity objects."""

    print("\n=== CIL Testbench: Basic Test ===")

    obj1 = make_identity_object(
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

    obj2 = make_identity_object(
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

    obj3 = make_identity_object(
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

    cob_objects = [obj1, obj2, obj3]

    cil = CIL()
    packet = cil.run(cob_objects, turn_index=1)

    print("\n--- Identity Selection Block ---")
    for entry in packet.identity_selection_block:
        print(entry["id"], entry["ordering_metrics"])

    print("\n--- Certainty Block ---")
    print(packet.referent_certainty_block)

    print("\n--- Stability Block ---")
    print(packet.stability_block)

    print("\n--- Lineage Block ---")
    print(packet.lineage_block)

    print("\n--- Ordering Block ---")
    print(packet.ordering_block)

    print("\n--- Packet Metadata ---")
    print(packet.packet_metadata)


def run_selection_priority_test():
    """Test deterministic selection ordering based on recency/frequency/density."""

    print("\n=== CIL Testbench: Selection Priority Test ===")

    objs = [
        make_identity_object("A", recency=1, frequency=1, density=1),
        make_identity_object("B", recency=5, frequency=1, density=1),
        make_identity_object("C", recency=5, frequency=3, density=1),
        make_identity_object("D", recency=5, frequency=3, density=4),
        make_identity_object("E", recency=2, frequency=9, density=9),
    ]

    cil = CIL()
    packet = cil.run(objs, turn_index=2)

    print("\n--- Selection Order (Top 5) ---")
    for entry in packet.identity_selection_block:
        print(entry["id"], entry["ordering_metrics"])


def run_stability_aggregation_test():
    """Test aggregation of drift, oscillation, collapse, merge/split, freeze/thaw."""

    print("\n=== CIL Testbench: Stability Aggregation Test ===")

    objs = [
        make_identity_object("X", recency=9, frequency=1, density=1, drift=0.5),
        make_identity_object("Y", recency=8, frequency=2, density=1, oscillation=0.3),
        make_identity_object("Z", recency=7, frequency=3, density=1, collapse=True),
    ]

    cil = CIL()
    packet = cil.run(objs, turn_index=3)

    print("\n--- Stability Block ---")
    print(packet.stability_block)


def run_lineage_aggregation_test():
    """Test aggregation of lineage stability indicators."""

    print("\n=== CIL Testbench: Lineage Aggregation Test ===")

    objs = [
        make_identity_object("L1", recency=5, frequency=2, density=1, lineage_stability="stable"),
        make_identity_object("L2", recency=4, frequency=3, density=2, lineage_stability="unstable"),
        make_identity_object("L3", recency=3, frequency=1, density=1, lineage_stability="stable"),
    ]

    cil = CIL()
    packet = cil.run(objs, turn_index=4)

    print("\n--- Lineage Block ---")
    print(packet.lineage_block)


def run_ordering_aggregation_test():
    """Test aggregation of recency, frequency, and density metrics."""

    print("\n=== CIL Testbench: Ordering Aggregation Test ===")

    objs = [
        make_identity_object("O1", recency=10, frequency=1, density=5),
        make_identity_object("O2", recency=7, frequency=4, density=2),
        make_identity_object("O3", recency=3, frequency=9, density=1),
    ]

    cil = CIL()
    packet = cil.run(objs, turn_index=5)

    print("\n--- Ordering Block ---")
    print(packet.ordering_block)


if __name__ == "__main__":
    run_basic_test()
    run_selection_priority_test()
    run_stability_aggregation_test()
    run_lineage_aggregation_test()
    run_ordering_aggregation_test()

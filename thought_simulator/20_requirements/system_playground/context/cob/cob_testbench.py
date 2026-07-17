"""
COB Testbench — System Playground Version

This testbench performs block-level validation of the COB subsystem.
It tests:
- identity object creation
- adding objects to the basin
- CST signal application (drift, oscillation, collapse, freeze/thaw, certainty/ambiguity)
- eviction logic (max 20 objects)
- summary aggregation

This is NOT a full system simulation. It is a shaping testbench used
inside system_playground before system_simulation.
"""

from cob import COB, IdentityObject


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
    frozen=None,
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
            "freeze_thaw": frozen,
            "frozen": frozen,
        },
        ordering_metrics={
            "recency": recency,
            "frequency": frequency,
            "density": density,
        },
    )


def run_basic_addition_test():
    """Test adding identity objects to COB."""

    print("\n=== COB Testbench: Basic Addition Test ===")

    cob = COB()

    obj1 = make_identity_object("obj1", 10, 5, 3)
    obj2 = make_identity_object("obj2", 7, 9, 2)
    obj3 = make_identity_object("obj3", 1, 1, 1)

    cob.add_identity_object(obj1)
    cob.add_identity_object(obj2)
    cob.add_identity_object(obj3)

    print("\n--- Basin Objects ---")
    for obj in cob.state.objects:
        print(obj.id, obj.ordering_metrics)

    print("\n--- Object Count ---")
    print(cob.state.object_count)


def run_cst_signal_test():
    """Test applying CST signals to COB."""

    print("\n=== COB Testbench: CST Signal Application Test ===")

    cob = COB()

    obj1 = make_identity_object("obj1", 10, 5, 3, drift=0.2)
    obj2 = make_identity_object("obj2", 7, 9, 2, oscillation=0.4)
    obj3 = make_identity_object("obj3", 1, 1, 1, collapse=True)

    cob.add_identity_object(obj1)
    cob.add_identity_object(obj2)
    cob.add_identity_object(obj3)

    signals = {
        "drift": {"affected_objects": ["obj1"], "magnitude": 0.2},
        "oscillation": {"affected_objects": ["obj2"], "frequency": 0.4},
        "collapse": {"collapsed_objects": ["obj3"], "severity": 1},
        "freeze": {"frozen_objects": ["obj2"], "reason": "test"},
        "thaw": {"thawed_objects": ["obj1"], "reason": "test"},
        "certainty_adjustment": {
            "increased_certainty": ["obj1"],
            "decreased_certainty": ["obj3"],
        },
        "ambiguity_adjustment": {
            "increased_ambiguity": ["obj2"],
            "decreased_ambiguity": ["obj3"],
        },
    }

    cob.run(signals, turn_index=1)

    print("\n--- Stability Summary ---")
    print(cob.state.stability_summary)

    print("\n--- Ambiguity Summary ---")
    print(cob.state.ambiguity_summary)

    print("\n--- Freeze/Thaw States ---")
    for obj in cob.state.objects:
        print(obj.id, obj.stability_metrics.get("frozen"))


def run_eviction_test():
    """Test eviction logic when more than 20 objects are added."""

    print("\n=== COB Testbench: Eviction Test ===")

    cob = COB()

    # Add 25 objects with varying ordering metrics
    for i in range(25):
        obj = make_identity_object(
            id=f"obj{i}",
            recency=i % 5,
            frequency=i % 3,
            density=i % 4,
        )
        cob.add_identity_object(obj)

    print("\n--- Final Basin Object Count (should be 20) ---")
    print(cob.state.object_count)

    print("\n--- Remaining Objects ---")
    for obj in cob.state.objects:
        print(obj.id, obj.ordering_metrics)


def run_summary_test():
    """Test summary aggregation."""

    print("\n=== COB Testbench: Summary Aggregation Test ===")

    cob = COB()

    obj1 = make_identity_object("obj1", 10, 5, 3, drift=0.1)
    obj2 = make_identity_object("obj2", 7, 9, 2, oscillation=0.3)
    obj3 = make_identity_object("obj3", 1, 1, 1, collapse=True)

    cob.add_identity_object(obj1)
    cob.add_identity_object(obj2)
    cob.add_identity_object(obj3)

    cob.aggregate_summaries()

    print("\n--- Ordering Summary ---")
    print(cob.state.ordering_summary)

    print("\n--- Stability Summary ---")
    print(cob.state.stability_summary)

    print("\n--- Lineage Summary ---")
    print(cob.state.lineage_summary)


if __name__ == "__main__":
    run_basic_addition_test()
    run_cst_signal_test()
    run_eviction_test()
    run_summary_test()

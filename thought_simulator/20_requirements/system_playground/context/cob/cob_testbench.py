"""
COB Testbench — System Playground Version

This testbench performs block-level validation of the COB subsystem.
It tests:
- identity object creation
- adding objects to the basin
- CST signal application (drift, oscillation, collapse, freeze/thaw, certainty/ambiguity, lineage stability)
- eviction logic (max 20 objects)
- ordering summary aggregation
- ambiguity summary aggregation
- stability summary aggregation
- lineage summary aggregation
- freeze/thaw compliance
- deterministic update behavior
- conversation-level ordering metrics
- structural referent-map compression
- merge/split structural propagation and post-compression

This is NOT a full system simulation. It is a shaping testbench used
inside system_playground before system_simulation.
"""

from cob.cob import COB, IdentityObject


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


# ---------------------------------------------------------------------------
# Basic Addition Test
# ---------------------------------------------------------------------------

def run_basic_addition_test():
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


# ---------------------------------------------------------------------------
# CST Signal Integration Test
# ---------------------------------------------------------------------------

def run_cst_signal_test():
    print("\n=== COB Testbench: CST Signal Application Test ===")

    cob = COB()

    obj1 = make_identity_object("obj1", 10, 5, 3, drift=0.2, lineage_stability="stable")
    obj2 = make_identity_object("obj2", 7, 9, 2, oscillation=0.4, lineage_stability="unstable")
    obj3 = make_identity_object("obj3", 1, 1, 1, collapse=True, lineage_stability="stable")

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
        "lineage_stability": {
            "stable_lineage": ["obj1", "obj3"],
            "unstable_lineage": ["obj2"],
        },
    }

    cob.run(signals, {}, 1)

    print("\n--- Stability Summary ---")
    print(cob.state.stability_summary)

    print("\n--- Ambiguity Summary ---")
    print(cob.state.ambiguity_summary)

    print("\n--- Lineage Summary ---")
    print(cob.state.lineage_summary)

    print("\n--- Freeze/Thaw States ---")
    for obj in cob.state.objects:
        print(obj.id, obj.stability_metrics.get("frozen"))

# ---------------------------------------------------------------------------
# NEW_CONTEXT_REQUIRED Test (HLR‑COB‑010A)
# ---------------------------------------------------------------------------

def run_new_context_required_test():
    print("\n=== COB Testbench: NEW_CONTEXT_REQUIRED Test ===")

    cob = COB()

    # Add an existing object to verify it is NOT evolved when new context is required
    existing = make_identity_object("old1", 5, 5, 5, drift=0.1)
    cob.add_identity_object(existing)

    # Signals from CST‑MS indicating a new context must be created
    signals = {
        "new_context_required": True,
        "next_context": {
            "referent_map": {"surface_forms": ["new topic", "fresh start"]},
            "anchors": ["anchor_new"],
        },
        # Drift/oscillation should NOT apply to old1 when new context is required
        "drift": {"affected_objects": ["old1"], "magnitude": 0.9},
    }

    cob_state = cob.run(signals, {}, 99)

    print("\n--- COB Objects After NEW_CONTEXT_REQUIRED ---")
    for obj in cob_state.objects:
        print(obj.id, obj.referent_map, obj.ordering_metrics)

    print("\n--- Verifications ---")
    # 1. New object must exist
    new_ids = [obj.id for obj in cob_state.objects]
    print("New object created:", any("ctx_99" == oid for oid in new_ids))

    # 2. Old object must NOT be updated by drift
    old_obj = next(o for o in cob_state.objects if o.id == "old1")
    print("Old object drift unchanged (should be 0.1):", old_obj.stability_metrics["drift"])

    # 3. New object must have correct referent map
    new_obj = next(o for o in cob_state.objects if o.id == "ctx_99")
    print("New object referent_map:", new_obj.referent_map)

# ---------------------------------------------------------------------------
# Freeze/Thaw Compliance Test
# ---------------------------------------------------------------------------

def run_freeze_thaw_compliance_test():
    print("\n=== COB Testbench: Freeze/Thaw Compliance Test ===")

    cob = COB()

    frozen_obj = make_identity_object("F", 5, 5, 5, drift=0.1, frozen=True)
    thawed_obj = make_identity_object("T", 5, 5, 5, drift=0.1, frozen=False)

    cob.add_identity_object(frozen_obj)
    cob.add_identity_object(thawed_obj)

    signals = {
        "drift": {"affected_objects": ["F", "T"], "magnitude": 0.9},
        "freeze": {"frozen_objects": ["F"], "reason": "test"},
        "thaw": {"thawed_objects": ["T"], "reason": "test"},
    }

    cob.run(signals, {}, 2)

    print("\n--- Frozen Object Drift (should remain 0.1) ---")
    print(cob.state.objects[0].stability_metrics["drift"])

    print("\n--- Thawed Object Drift (should update to 0.9) ---")
    print(cob.state.objects[1].stability_metrics["drift"])


# ---------------------------------------------------------------------------
# Eviction Test
# ---------------------------------------------------------------------------

def run_eviction_test():
    print("\n=== COB Testbench: Eviction Test ===")

    cob = COB()

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


# ---------------------------------------------------------------------------
# Summary Aggregation Test
# ---------------------------------------------------------------------------

def run_summary_test():
    print("\n=== COB Testbench: Summary Aggregation Test ===")

    cob = COB()

    obj1 = make_identity_object("obj1", 10, 5, 3, drift=0.1, lineage_stability="stable")
    obj2 = make_identity_object("obj2", 7, 9, 2, oscillation=0.3, lineage_stability="unstable")
    obj3 = make_identity_object("obj3", 1, 1, 1, collapse=True, lineage_stability="stable")

    cob.add_identity_object(obj1)
    cob.add_identity_object(obj2)
    cob.add_identity_object(obj3)

    cob.aggregate_summaries()

    print("\n--- Ordering Summary ---")
    print(cob.state.ordering_summary)

    print("\n--- Stability Summary ---")
    print(cob.state.stability_summary)

    print("\n--- Ambiguity Summary ---")
    print(cob.state.ambiguity_summary)

    print("\n--- Lineage Summary ---")
    print(cob.state.lineage_summary)


# ---------------------------------------------------------------------------
# Deterministic Behavior Test
# ---------------------------------------------------------------------------

def run_deterministic_behavior_test():
    print("\n=== COB Testbench: Deterministic Behavior Test ===")

    cob1 = COB()
    cob2 = COB()

    objs = [
        make_identity_object("A", 5, 5, 5, drift=0.1),
        make_identity_object("B", 4, 4, 4, oscillation=0.2),
    ]

    for o in objs:
        cob1.add_identity_object(o)
        cob2.add_identity_object(
            make_identity_object(
                o.id,
                o.ordering_metrics["recency"],
                o.ordering_metrics["frequency"],
                o.ordering_metrics["density"],
                drift=o.stability_metrics["drift"],
                oscillation=o.stability_metrics["oscillation"],
                collapse=o.stability_metrics["collapse"],
                certainty=o.ambiguity["certainty"],
                ambiguity=o.ambiguity["ambiguity"],
                lineage_stability=o.lineage["stability"],
                frozen=o.stability_metrics["frozen"],
            )
        )

    signals = {
        "drift": {"affected_objects": ["A"], "magnitude": 0.9},
        "oscillation": {"affected_objects": ["B"], "frequency": 0.7},
    }

    cob1.run(signals, {}, 3)
    cob2.run(signals, {}, 3)

    print("\n--- Deterministic Stability Comparison ---")
    print(cob1.state.stability_summary == cob2.state.stability_summary)


# ---------------------------------------------------------------------------
# Conversation-Level Ordering Metrics Test
# ---------------------------------------------------------------------------

def run_conversation_ordering_metrics_test():
    print("\n=== COB Testbench: Conversation-Level Ordering Metrics Test ===")

    cob = COB()

    # Simulate 12 conversation turns
    for turn in range(12):
        cob.run({}, {}, turn)

    print("\n--- Conversation Access Count (should be 12) ---")
    print(cob.state.conversation_access_count)

    print("\n--- Conversation Access Order (should be [0..11]) ---")
    print(cob.state.conversation_access_order)

    print("\n--- Sliding-Window Frequency (last 10 accesses) ---")
    print(cob.state.conversation_frequency_last_10)


# ---------------------------------------------------------------------------
# Referent-Map Structural Compression Test (HLR-COB-024)
# ---------------------------------------------------------------------------

def run_referent_map_compression_test():
    print("\n=== COB Testbench: Referent-Map Structural Compression Test ===")

    cob = COB()

    # Identity object with redundant and subset surface forms
    obj = make_identity_object("C", 5, 5, 5)
    obj.referent_map = [
        "dog",
        "australian shepherd dog",
        "dog",
        "shepherd dog",
    ]

    cob.add_identity_object(obj)

    cob_state = cob.run({}, {}, 0)

    print("\n--- Compressed Referent Map ---")
    for o in cob_state.objects:
        print(o.id, o.referent_map)


# ---------------------------------------------------------------------------
# Merge/Split Structural Propagation + Post-Compression Test (HLR-COB-025)
# ---------------------------------------------------------------------------

def run_merge_split_compression_test():
    print("\n=== COB Testbench: Merge/Split Structural Propagation + Post-Compression Test ===")

    cob = COB()

    # Parents with overlapping referent maps
    A = make_identity_object("A", 5, 3, 2)
    B = make_identity_object("B", 4, 2, 1)

    A.referent_map = ["dog", "australian shepherd dog"]
    B.referent_map = ["dog", "border collie dog"]

    cob.add_identity_object(A)
    cob.add_identity_object(B)

    # MERGE signals
    merge_signals = {
        "merge": {"pairs": [("A", "B")]},
    }

    cob_state = cob.run(merge_signals, {}, 1)

    print("\n--- After MERGE ---")
    for obj in cob_state.objects:
        print(obj.id, obj.referent_map)

    # Find merged child id
    merged_id = "A_B_merged"

    # SPLIT signals on merged child
    split_signals = {
        "split": {"objects": [merged_id]},
    }

    cob_state = cob.run(split_signals, {}, 2)

    print("\n--- After SPLIT ---")
    for obj in cob_state.objects:
        print(obj.id, obj.referent_map)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_basic_addition_test()
    run_cst_signal_test()
    run_freeze_thaw_compliance_test()
    run_eviction_test()
    run_summary_test()
    run_deterministic_behavior_test()
    run_conversation_ordering_metrics_test()
    run_referent_map_compression_test()
    run_merge_split_compression_test()
    run_new_context_required_test()

"""
COB Merge/Split Testbench
System Playground — Context Subsystem
Validates TS‑correct structural merge/split behavior:
- MERGE: child contains BOTH parents’ semantics (no blending)
- SPLIT: BOTH children receive ALL semantics (no partitioning)
"""

from context.cob.cob import COB
from context.cil.cil import IdentityObject


# ------------------------------------------------------------
# Helper: Construct identity objects
# ------------------------------------------------------------

def make_identity_object(obj_id, referents, anchors=None, lineage=None, ordering=None):
    return IdentityObject(
        id=obj_id,
        referent_map=referents,
        anchors=anchors or [0.0, 0.0],
        lineage=lineage or {"parent": None},
        ambiguity={"certainty": 1.0, "ambiguity": 0.0},
        stability_metrics={"drift": 0.0, "oscillation": 0.0, "collapse": False, "frozen": False},
        ordering_metrics=ordering or {"recency": 0, "frequency": 0, "density": 0},
    )


# ------------------------------------------------------------
# MERGE TEST
# ------------------------------------------------------------

def run_merge_test():
    print("\n=== MERGE TEST ===")

    cob = COB()

    objA = make_identity_object(
        "objA",
        referents={"user": ["he", "him"], "topic": ["math"]},
        anchors=[0.2, 0.3],
        ordering={"recency": 10, "frequency": 5, "density": 2},
    )

    objB = make_identity_object(
        "objB",
        referents={"user": ["he"], "topic": ["math", "algebra"]},
        anchors=[0.25, 0.35],
        ordering={"recency": 9, "frequency": 4, "density": 2},
    )

    cob.add_identity_object(objA)
    cob.add_identity_object(objB)

    signals = {"merge": {"pairs": [("objA", "objB")]}}

    print("Objects BEFORE merge:")
    for obj in cob.state.objects:
        print(f"- {obj.id}: referents={obj.referent_map}")

    cob.run(signals, turn_index=1)

    print("\nObjects AFTER merge:")
    for obj in cob.state.objects:
        print(f"- {obj.id}: referents={obj.referent_map}, anchors={obj.anchors}, lineage={obj.lineage}")

    # --- Validate MERGE semantics ---
    merged_obj = cob.state.objects[0]

    # 1. Child must contain BOTH parents’ referent maps structurally
    assert "parents" in merged_obj.referent_map, "Merged referent_map must contain both parents"
    assert "objA" in merged_obj.referent_map["parents"], "Merged referent_map missing objA"
    assert "objB" in merged_obj.referent_map["parents"], "Merged referent_map missing objB"

    # 2. Anchors must contain BOTH parents’ anchors
    assert isinstance(merged_obj.anchors, list), "Merged anchors must be a list"
    assert len(merged_obj.anchors) == 2, "Merged anchors must contain both parents"
    assert merged_obj.anchors[0][0] == "objA", "Merged anchors missing objA"
    assert merged_obj.anchors[1][0] == "objB", "Merged anchors missing objB"

    # 3. TP lineage_log correctness
    assert len(cob.state.lineage_log) == 1, "Expected exactly one MERGE event"
    evt = cob.state.lineage_log[0]
    assert evt["event_type"] == "MERGE"
    assert evt["parent_ref"] == ["objA", "objB"]
    assert len(evt["child_refs"]) == 1

    print("\nMERGE test passed.")


# ------------------------------------------------------------
# SPLIT TEST
# ------------------------------------------------------------

def run_split_test():
    print("\n=== SPLIT TEST ===")

    cob = COB()

    objX = make_identity_object(
        "objX",
        referents={"user": ["he", "she"], "topic": ["math", "cooking"]},
        anchors=[0.5, 0.1],
        ordering={"recency": 7, "frequency": 3, "density": 1},
    )

    cob.add_identity_object(objX)

    signals = {"split": {"objects": ["objX"]}}

    print("Objects BEFORE split:")
    for obj in cob.state.objects:
        print(f"- {obj.id}: referents={obj.referent_map}")

    cob.run(signals, turn_index=2)

    print("\nObjects AFTER split:")
    for obj in cob.state.objects:
        print(f"- {obj.id}: referents={obj.referent_map}, anchors={obj.anchors}, lineage={obj.lineage}")

    # --- Validate SPLIT semantics ---
    assert len(cob.state.objects) == 2, "Split must produce exactly two children"

    child1, child2 = cob.state.objects

    # 1. Both children must receive ALL semantics (full copy)
    assert child1.referent_map == child2.referent_map == objX.referent_map, \
        "Both children must receive full referent_map copy"

    assert child1.anchors == child2.anchors == objX.anchors, \
        "Both children must receive full anchors copy"

    assert child1.ambiguity == child2.ambiguity == objX.ambiguity, \
        "Both children must receive full ambiguity copy"

    assert child1.stability_metrics == child2.stability_metrics == objX.stability_metrics, \
        "Both children must receive full stability_metrics copy"

    assert child1.ordering_metrics == child2.ordering_metrics == objX.ordering_metrics, \
        "Both children must receive full ordering_metrics copy"

    # 2. TP lineage_log correctness
    assert len(cob.state.lineage_log) == 1, "Expected exactly one SPLIT event"
    evt = cob.state.lineage_log[0]
    assert evt["event_type"] == "SPLIT"
    assert evt["parent_ref"] == ["objX"]
    assert len(evt["child_refs"]) == 2

    print("\nSPLIT test passed.")


# ------------------------------------------------------------
# Deterministic Replay Test
# ------------------------------------------------------------

def run_merge_split_replay_test():
    print("\n=== MERGE/SPLIT REPLAY TEST ===")

    # First run
    cob1 = COB()
    obj1A = make_identity_object("objA", {"topic": ["math"]})
    obj1B = make_identity_object("objB", {"topic": ["math", "algebra"]})
    cob1.add_identity_object(obj1A)
    cob1.add_identity_object(obj1B)
    cob1.run({"merge": {"pairs": [("objA", "objB")]}}, turn_index=1)

    snapshot1 = [(obj.id, obj.referent_map) for obj in cob1.state.objects]
    lineage_log1 = cob1.state.lineage_log
    cob_snapshot1 = cob1.state.cob_state_snapshot

    # Second run
    cob2 = COB()
    obj2A = make_identity_object("objA", {"topic": ["math"]})
    obj2B = make_identity_object("objB", {"topic": ["math", "algebra"]})
    cob2.add_identity_object(obj2A)
    cob2.add_identity_object(obj2B)
    cob2.run({"merge": {"pairs": [("objA", "objB")]}}, turn_index=1)

    snapshot2 = [(obj.id, obj.referent_map) for obj in cob2.state.objects]
    lineage_log2 = cob2.state.lineage_log
    cob_snapshot2 = cob2.state.cob_state_snapshot

    print("Replay deterministic (objects):", snapshot1 == snapshot2)
    print("Replay deterministic (TP.lineage_log):", lineage_log1 == lineage_log2)
    print("Replay deterministic (TP.cob_state_snapshot):", cob_snapshot1 == cob_snapshot2)

    assert snapshot1 == snapshot2, "Object-level replay must be deterministic"
    assert lineage_log1 == lineage_log2, "TP.lineage_log replay must be deterministic"
    assert cob_snapshot1 == cob_snapshot2, "TP.cob_state_snapshot replay must be deterministic"

    print("\nReplay test passed.")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

if __name__ == "__main__":
    run_merge_test()
    run_split_test()
    run_merge_split_replay_test()

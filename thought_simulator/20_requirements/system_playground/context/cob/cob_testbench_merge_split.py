"""
COB Merge/Split Testbench
System Playground — Context Subsystem
Validates merge/split structural operations at the COB level.
"""

from context.cob.cob import COB
from context.cil.cil import IdentityObject

# ------------------------------------------------------------
# Helper: Construct identity objects with referents + anchors
# ------------------------------------------------------------

def make_identity_object(obj_id, referents, anchors=None, lineage=None, ordering=None):
    return IdentityObject(
        id=obj_id,
        referent_map=referents,
        anchors=anchors or [0.0, 0.0],  # temporal, discourse
        lineage=lineage or {"parent": None, "history": []},
        ambiguity={"certainty": 1.0, "ambiguity": 0.0},
        stability_metrics={"drift": 0.0, "oscillation": 0.0, "collapse": False, "frozen": False},
        ordering_metrics=ordering or {"recency": 0, "frequency": 0, "density": 0},
    )


# ------------------------------------------------------------
# Merge Test
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

    # Correct CST merge signal format for cob.py
    signals = {"merge": {"pairs": [("objA", "objB")]}}

    print("Objects before merge:")
    for obj in cob.state.objects:
        print(f"- {obj.id}: referents={obj.referent_map}")

    cob.run(signals, turn_index=1)

    print("Objects after merge:")
    for obj in cob.state.objects:
        print(f"- {obj.id}: referents={obj.referent_map}, lineage={obj.lineage}, ordering={obj.ordering_metrics}")

    # --- TP-facing checks for MERGE ---
    print("TP.lineage_log after merge:")
    for evt in cob.state.lineage_log:
        print(f"- event_type={evt['event_type']}, parent_ref={evt['parent_ref']}, child_refs={evt['child_refs']}")

    print("TP.cob_state_snapshot after merge:")
    print(f"keys={list(cob.state.cob_state_snapshot.keys())}")

    # basic assertions to validate TP fields for CST
    assert len(cob.state.lineage_log) == 1, "Expected exactly one MERGE event in TP.lineage_log"
    merge_evt = cob.state.lineage_log[0]
    assert merge_evt["event_type"] == "MERGE", "Expected MERGE event_type"
    assert merge_evt["parent_ref"] == ["objA", "objB"], "MERGE parent_ref mismatch"
    assert len(merge_evt["child_refs"]) == 1, "MERGE should produce exactly one child_ref"

    assert "objects" in cob.state.cob_state_snapshot, "cob_state_snapshot must contain 'objects'"
    assert "metadata" in cob.state.cob_state_snapshot, "cob_state_snapshot must contain 'metadata'"

# ------------------------------------------------------------
# Split Test
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

    # Correct CST split signal format for cob.py
    signals = {"split": {"objects": ["objX"]}}

    print("Objects before split:")
    for obj in cob.state.objects:
        print(f"- {obj.id}: referents={obj.referent_map}")
    
    cob.run(signals, turn_index=2)

    print("Objects after split:")
    for obj in cob.state.objects:
        print(f"- {obj.id}: referents={obj.referent_map}, lineage={obj.lineage}, ordering={obj.ordering_metrics}")

    # --- TP-facing checks for SPLIT ---
    print("TP.lineage_log after split:")
    for evt in cob.state.lineage_log:
        print(f"- event_type={evt['event_type']}, parent_ref={evt['parent_ref']}, child_refs={evt['child_refs']}")

    print("TP.cob_state_snapshot after split:")
    print(f"keys={list(cob.state.cob_state_snapshot.keys())}")

    # basic assertions to validate TP fields for CST
    assert len(cob.state.lineage_log) == 1, "Expected exactly one SPLIT event in TP.lineage_log"
    split_evt = cob.state.lineage_log[0]
    assert split_evt["event_type"] == "SPLIT", "Expected SPLIT event_type"
    assert split_evt["parent_ref"] == ["objX"], "SPLIT parent_ref mismatch"
    assert len(split_evt["child_refs"]) == 2, "SPLIT should produce exactly two child_refs"

    assert "objects" in cob.state.cob_state_snapshot, "cob_state_snapshot must contain 'objects'"
    assert "metadata" in cob.state.cob_state_snapshot, "cob_state_snapshot must contain 'metadata'"

# ------------------------------------------------------------
# Deterministic Replay Test
# ------------------------------------------------------------

def run_merge_split_replay_test():
    print("\n=== MERGE/SPLIT REPLAY TEST ===")

    cob1 = COB()
    obj1A = make_identity_object("objA", {"topic": ["math"]})
    obj1B = make_identity_object("objB", {"topic": ["math", "algebra"]})
    cob1.add_identity_object(obj1A)
    cob1.add_identity_object(obj1B)
    cob1.run({"merge": {"pairs": [("objA", "objB")]}}, turn_index=1)

    snapshot1 = [(obj.id, obj.referent_map) for obj in cob1.state.objects]
    lineage_log1 = cob1.state.lineage_log
    cob_snapshot1 = cob1.state.cob_state_snapshot

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

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

if __name__ == "__main__":
    run_merge_test()
    run_split_test()
    run_merge_split_replay_test()

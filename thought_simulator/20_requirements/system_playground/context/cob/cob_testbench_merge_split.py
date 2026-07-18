"""
COB Merge/Split Testbench
System Playground — Context Subsystem
Validates merge/split structural operations at the COB level.
"""

from cob import COB
from cob import IdentityObject

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

    cob.run(signals, turn_index=1)

    print("Objects after merge:")
    for obj in cob.state.objects:
        print(f"- {obj.id}: referents={obj.referent_map}, lineage={obj.lineage}, ordering={obj.ordering_metrics}")


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

    cob.run(signals, turn_index=2)

    print("Objects after split:")
    for obj in cob.state.objects:
        print(f"- {obj.id}: referents={obj.referent_map}, lineage={obj.lineage}, ordering={obj.ordering_metrics}")


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

    cob2 = COB()
    obj2A = make_identity_object("objA", {"topic": ["math"]})
    obj2B = make_identity_object("objB", {"topic": ["math", "algebra"]})
    cob2.add_identity_object(obj2A)
    cob2.add_identity_object(obj2B)
    cob2.run({"merge": {"pairs": [("objA", "objB")]}}, turn_index=1)

    snapshot2 = [(obj.id, obj.referent_map) for obj in cob2.state.objects]

    print("Replay deterministic:", snapshot1 == snapshot2)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

if __name__ == "__main__":
    run_merge_test()
    run_split_test()
    run_merge_split_replay_test()

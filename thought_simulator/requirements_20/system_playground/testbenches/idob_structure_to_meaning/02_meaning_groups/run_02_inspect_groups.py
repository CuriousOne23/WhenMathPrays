"""Slide 02 — Meaning groups carry the six-float prototype."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from lib.schema_load import load_yaml
from lib.vector6 import fmt, from_mapping

def run(group_id=None):
    data = load_yaml(Path(__file__).parent / "meaning_groups.slide.yaml")
    groups = data.get("meaning_groups") or []
    print("=" * 64)
    print("LESSON 02 — MEANING GROUPS")
    print("Six fields = one vector, not six dictionaries.")
    print("Values here are hand-set prototypes for this revision.")
    print("=" * 64)
    shown = 0
    for group in groups:
        if group_id is not None and int(group.get("group_id")) != int(group_id):
            continue
        shown += 1
        vec = from_mapping(group.get("group_dimensions"))
        print(f"\ngroup_id:    {group.get('group_id')}")
        print(f"group_name:  {group.get('group_name')}")
        print(f"primitive:   {group.get('primitive')}")
        print(f"six-vector:  {fmt(vec)}")
        print("structure IDs printed: NO  (boundary holds)")
    if shown == 0:
        print(f"\nNo group matched group_id={group_id!r}.")
    print("\nEnd lesson 02.\n")

def main():
    run()

if __name__ == "__main__":
    main()

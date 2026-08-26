"""Slide 03 — Structure bounds meaning by listing legal groups."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from lib.schema_load import load_yaml

def run(card_id="S_rock_burst"):
    data = load_yaml(Path(__file__).parent / "struct_to_meaning_map.slide.yaml")
    rows = data.get("struct_to_meaning_map") or []
    print("=" * 64)
    print("LESSON 03 — MAP LOOKUP")
    print("Structure -> candidate_group_ids only.")
    print("No ranking. No six-float modulation.")
    print("=" * 64)
    print(f"\nLooking up card_id={card_id!r}")
    found = next((row for row in rows if row.get("card_id") == card_id), None)
    candidates = list((found or {}).get("meaning_group_candidates") or [])
    print(f"candidate_group_ids: {candidates}")
    if not candidates:
        print("Feel this: structure can refuse meaning. That is not 'cognition failed'.")
    elif len(candidates) == 1:
        print("Feel this: thin map — structure looks like a dictator.")
    else:
        print("Feel this: several legal groups — ranking will choose among them later.")
    print("\nEnd lesson 03.\n")
    return candidates

def main():
    run()

if __name__ == "__main__":
    main()

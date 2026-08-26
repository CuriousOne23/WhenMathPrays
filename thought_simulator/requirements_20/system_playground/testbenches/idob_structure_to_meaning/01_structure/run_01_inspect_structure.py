"""Slide 01 — Structure is meaning-blind geometry."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from lib.hash_toy import toy_structural_key
from lib.schema_load import load_yaml


def run(card_id=None):
    data = load_yaml(Path(__file__).parent / "structure_card.examples.yaml")
    cards = data.get("cards") or []
    print("=" * 64)
    print("LESSON 01 — STRUCTURE")
    print("Structure is six IDs + optional residue/features.")
    print("The key is a fingerprint of the IDs only. No meaning scores here.")
    print("=" * 64)
    shown = 0
    for card in cards:
        if card_id and card.get("card_id") != card_id:
            continue
        shown += 1
        key = toy_structural_key(card)
        print(f"\ncard_id:              {card.get('card_id')}")
        print(f"note:                 {card.get('note')}")
        print(f"semantic_field_id:    {card.get('semantic_field_id')}")
        print(f"semantic_role_id:     {card.get('semantic_role_id')}")
        print(f"semantic_object_id:   {card.get('semantic_object_id')}")
        print(f"gradient_id:          {card.get('gradient_id')}")
        print(f"universe_id:          {card.get('universe_id')}")
        print(f"subfield_id:          {card.get('subfield_id')}")
        print(f"residue_code:         {card.get('residue_code')}")
        print(f"feature_tags:         {card.get('feature_tags')}")
        print(f"structural_key:       {key}")
        print("meaning floats printed: NO  (boundary holds)")
    if shown == 0:
        print(f"\nNo card matched card_id={card_id!r}.")
    print("\nEnd lesson 01.\n")


def main():
    run()


if __name__ == "__main__":
    main()

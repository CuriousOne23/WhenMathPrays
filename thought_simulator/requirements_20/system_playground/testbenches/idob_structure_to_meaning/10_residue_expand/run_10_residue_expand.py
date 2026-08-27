"""Slide 10 — print leftover and which file to expand. No meaning floats."""
from pathlib import Path
import sys
from importlib.util import spec_from_file_location, module_from_spec

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_spec = spec_from_file_location("expand", Path(__file__).parent / "expand.py")
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _print(res):
    print(f"\ncard_id:              {res.get('card_id')}")
    print(f"structural_key:       {res.get('structural_key')}")
    print(f"residue_code:         {res.get('residue_code')}")
    print(f"map_empty:            {res.get('map_empty')}")
    print(f"after_status:         {res.get('after_status')}")
    print(f"digested:             {res.get('digested')}")
    print(f"expand_target:        {res.get('expand_target')}")
    print(f"next_key:             {res.get('next_key')}")
    print(f"note:                 {res.get('note')}")
    print("meaning floats printed: NO  (boundary holds)")
    print("next six-tuple invented: NO")


def run(card_id=None):
    print("=" * 64)
    print("LESSON 10 — RESIDUE EXPAND")
    print("Leftover after one hop -> which file a human expands.")
    print("Does not run RB. Does not invent a structural_key.")
    print("=" * 64)
    cards, mmap, table = _mod.load_inputs()
    shown = 0
    for card in cards:
        if card_id and card.get("card_id") != card_id:
            continue
        shown += 1
        cands = mmap.get(card.get("card_id"), [])
        _print(_mod.expand_card(card, cands, table))
    if shown == 0:
        print(f"\nNo card matched card_id={card_id!r}.")
    print("\nEnd lesson 10.\n")


def main():
    run()


if __name__ == "__main__":
    main()

"""Slide 09 — print assignment, miss, packs. No meaning floats."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from importlib.util import spec_from_file_location, module_from_spec

_spec = spec_from_file_location("assign", Path(__file__).parent / "assign.py")
_assign_mod = module_from_spec(_spec)
_spec.loader.exec_module(_assign_mod)
assign = _assign_mod.assign

DEFAULT_LINES = [
    ("The rock burst open.", ["base_en"]),
    ("The project deadline is Friday.", ["base_en"]),
    ("I feel sleepy.", ["base_en"]),
    ("zzzzq no cue", ["base_en"]),
    ("The ore melted.", ["base_en"]),
    ("The ore melted.", ["base_en", "pack_geology"]),
    ("The rock burst open.", ["base_en", "pack_conflict"]),
]


def _print_result(res):
    print(f"\nutterance:            {res.get('utterance')}")
    print(f"packs_loaded:         {res.get('packs_loaded')}")
    print(f"assignment_status:    {res.get('assignment_status')}")
    print(f"semantic_field_id:    {res.get('semantic_field_id')}")
    print(f"semantic_role_id:     {res.get('semantic_role_id')}")
    print(f"semantic_object_id:   {res.get('semantic_object_id')}")
    print(f"gradient_id:          {res.get('gradient_id')}")
    print(f"universe_id:          {res.get('universe_id')}")
    print(f"subfield_id:          {res.get('subfield_id')}")
    print(f"residue_code:         {res.get('residue_code')}")
    print(f"feature_tags:         {res.get('feature_tags')}")
    print(f"collisions:           {res.get('collisions')}")
    print(f"structural_key:       {res.get('structural_key')}")
    print("meaning floats printed: NO  (boundary holds)")


def run(utterance=None, packs_loaded=None):
    print("=" * 64)
    print("LESSON 09 — STRUCTURE ASSIGNMENT")
    print("Utterance + loaded packs -> six IDs or miss. Hasher is dumb.")
    print("Packs on disk but not listed do not fire.")
    print("=" * 64)
    if utterance is not None:
        res = assign(utterance, packs_loaded=packs_loaded or ["base_en"])
        _print_result(res)
    else:
        for line, packs in DEFAULT_LINES:
            _print_result(assign(line, packs_loaded=packs))
    print("\nEnd lesson 09.\n")


def main():
    run()


if __name__ == "__main__":
    main()

"""Slide 05 — Identity moves M. Structure does not change."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
from lib.schema_load import load_yaml
from lib.vector6 import delta_l2, fmt, from_mapping
from modulate import modulate

def _group_vector(group_id):
    data = load_yaml(ROOT / "02_meaning_groups" / "meaning_groups.slide.yaml")
    for group in data.get("meaning_groups") or []:
        if int(group.get("group_id")) == int(group_id):
            return from_mapping(group.get("group_dimensions")), group
    return None, None

def run(group_id=1001, cie_id=None, clip_to_unit=True):
    envelopes = load_yaml(Path(__file__).parent / "cie.examples.yaml").get("envelopes") or []
    M, group = _group_vector(group_id)
    print("=" * 64)
    print("LESSON 05 — CIE MODULATION")
    print("Formula: M' = M + alpha * I")
    print("CIE is local utterance identity. It must not rewrite structural_key.")
    print("=" * 64)
    if M is None:
        print(f"Unknown group_id={group_id}")
        return
    print(f"\nFixed group {group.get('group_id')} {group.get('group_name')}")
    print(f"M  (unmoved): {fmt(M)}")
    shown = 0
    for env in envelopes:
        if cie_id and env.get("cie_id") != cie_id:
            continue
        shown += 1
        alpha = float(env.get("identity_importance", 0))
        I = from_mapping(env.get("identity_vector"))
        Mp = modulate(M, alpha, I, clip=clip_to_unit)
        print(f"\ncie_id:     {env.get('cie_id')}")
        print(f"tags:       {env.get('identity_tags')}")
        print(f"alpha:      {alpha}")
        print(f"I:          {fmt(I)}")
        print(f"M':         {fmt(Mp)}")
        print(f"|M'-M|:     {delta_l2(Mp, M):.4f}")
        print("structural_key changed: NO")
    if shown == 0:
        print(f"\nNo envelope matched cie_id={cie_id!r}.")
    print("\nEnd lesson 05.\n")

def main():
    run()

if __name__ == "__main__":
    main()

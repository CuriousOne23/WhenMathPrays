"""Slide 04 — Rank only among map candidates."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from lib.schema_load import load_yaml

def _lookup_candidates(card_id):
    data = load_yaml(ROOT / "03_map_lookup" / "struct_to_meaning_map.slide.yaml")
    for row in data.get("struct_to_meaning_map") or []:
        if row.get("card_id") == card_id:
            return list(row.get("meaning_group_candidates") or [])
    return []

def run(card_id="S_rock_burst"):
    weights = load_yaml(Path(__file__).parent / "ranking_weights.slide.yaml")
    w = weights.get("ranking_weights") or {}
    toy = {int(k): v for k, v in (weights.get("group_toy_scores") or {}).items()}
    candidates = _lookup_candidates(card_id)
    print("=" * 64)
    print("LESSON 04 — RANKING")
    print("Score = cue_w*cue + invariant_w*invariant + identity_w*identity")
    print("Candidates come from the map. Ranking must not invent groups.")
    print("=" * 64)
    print(f"\ncard_id:     {card_id}")
    print(f"candidates:  {candidates}")
    print(f"weights:     {w}")
    scored = []
    for gid in candidates:
        parts = toy.get(int(gid), {"cue": 0.0, "invariant": 0.0, "identity": 0.0})
        score = (
            float(w.get("cue_weight", 0)) * float(parts.get("cue", 0))
            + float(w.get("invariant_weight", 0)) * float(parts.get("invariant", 0))
            + float(w.get("identity_weight", 0)) * float(parts.get("identity", 0))
        )
        scored.append((score, int(gid), parts))
        print(f"  group {gid}: parts={parts} score={score:.3f}")
    scored.sort(key=lambda item: item[0], reverse=True)
    order = [gid for _score, gid, _parts in scored]
    print(f"\nfinal_rank_order: {order}")
    print("\nEnd lesson 04.\n")
    return order

def main():
    run()

if __name__ == "__main__":
    main()

"""Slide 04 / Stop 4 — Rank only among map candidates.

Weighted sum of three helpers, each clipped to [0, 1]:
    score = cue_w * cue + invariant_w * invariant + identity_w * identity

Helpers this revision read group_toy_scores in ranking_weights.slide.yaml.
They do not route to IdOB and do not invent groups the map forbade.

run() returns final_rank_order (list) so Slide 07 can keep using it.
rank() returns the full record.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from lib.schema_load import load_yaml

WEIGHTS_PATH = Path(__file__).parent / "ranking_weights.slide.yaml"
MAP_PATH = ROOT / "03_map_lookup" / "struct_to_meaning_map.slide.yaml"


def _clip01(value) -> float:
    return max(0.0, min(1.0, float(value)))


def load_weights():
    data = load_yaml(WEIGHTS_PATH)
    weights = data.get("ranking_weights") or {}
    toy = {int(k): v for k, v in (data.get("group_toy_scores") or {}).items()}
    return weights, toy


def lookup_candidates(card_id: str) -> list:
    data = load_yaml(MAP_PATH)
    for row in data.get("struct_to_meaning_map") or []:
        if row.get("card_id") == card_id:
            return list(row.get("meaning_group_candidates") or [])
    return []


def cue_score(group_id: int, toy: dict) -> float:
    """How well this prototype matches the talk-shape cues. Toy table this revision."""
    return _clip01((toy.get(int(group_id)) or {}).get("cue", 0.0))


def invariant_score(group_id: int, toy: dict) -> float:
    """How stable the prototype stays under small talk-shape change. Toy table this revision."""
    return _clip01((toy.get(int(group_id)) or {}).get("invariant", 0.0))


def identity_alignment_score(group_id: int, toy: dict) -> float:
    """How well the prototype sits with the current identity/stance envelope. Toy table this revision."""
    return _clip01((toy.get(int(group_id)) or {}).get("identity", 0.0))


def score_group(group_id: int, weights: dict, toy: dict) -> dict:
    cue = cue_score(group_id, toy)
    invariant = invariant_score(group_id, toy)
    identity = identity_alignment_score(group_id, toy)
    total = (
        float(weights.get("cue_weight", 0.0)) * cue
        + float(weights.get("invariant_weight", 0.0)) * invariant
        + float(weights.get("identity_weight", 0.0)) * identity
    )
    return {
        "group_id": int(group_id),
        "cue": cue,
        "invariant": invariant,
        "identity": identity,
        "score": total,
    }


def rank(card_id: str = "S_rock_burst") -> dict:
    weights, toy = load_weights()
    candidates = lookup_candidates(card_id)
    scored = [score_group(gid, weights, toy) for gid in candidates]
    scored.sort(key=lambda row: (-row["score"], row["group_id"]))
    order = [row["group_id"] for row in scored]
    return {
        "card_id": card_id,
        "candidate_group_ids": [int(g) for g in candidates],
        "weights": {
            "cue_weight": float(weights.get("cue_weight", 0.0)),
            "invariant_weight": float(weights.get("invariant_weight", 0.0)),
            "identity_weight": float(weights.get("identity_weight", 0.0)),
        },
        "scored": scored,
        "final_rank_order": order,
        "selected_group_id": order[0] if order else None,
    }


def run(card_id="S_rock_burst"):
    record = rank(card_id=card_id)
    print("=" * 64)
    print("LESSON 04 / STOP 4 — RANKING")
    print("score = cue_w*cue + invariant_w*invariant + identity_w*identity")
    print("Helpers clipped to [0, 1]. Candidates come from the map only.")
    print("=" * 64)
    print(f"\ncard_id:              {record['card_id']}")
    print(f"candidate_group_ids:  {record['candidate_group_ids']}")
    print(f"weights:              {record['weights']}")
    if not record["candidate_group_ids"]:
        print("Empty map: no winner. Ranking must stay empty.")
    for row in record["scored"]:
        print(
            f"  group {row['group_id']}: "
            f"cue={row['cue']:.3f} invariant={row['invariant']:.3f} "
            f"identity={row['identity']:.3f} score={row['score']:.3f}"
        )
    print(f"\nfinal_rank_order:  {record['final_rank_order']}")
    print(f"selected_group_id: {record['selected_group_id']}")
    print("\nEnd lesson 04.\n")
    return record["final_rank_order"]


def main():
    run()


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from place import place

DEFAULT_SUGGEST_LOG = Path(__file__).parent / "logs" / "suggest.jsonl"

ALLOWED_ABOUT = {
    "material_event_anchor",
    "timed_obligation_anchor",
    "person_load_anchor",
}
ALLOWED_FAMILY = {
    "event_talk",
    "state_talk",
    "task_talk",
    "claim_talk",
    "ask_talk",
    "update_talk",
}

_RULES: list[tuple[str, str | None, str | None, str]] = [
    ("deadline", "timed_obligation_anchor", "state_talk", "keyword deadline"),
    ("friday", "timed_obligation_anchor", "state_talk", "keyword friday"),
    ("burst", "material_event_anchor", "event_talk", "keyword burst"),
    ("broke", "material_event_anchor", "event_talk", "keyword broke"),
    ("can't", "person_load_anchor", None, "keyword can't"),
    ("cannot", "person_load_anchor", None, "keyword cannot"),
]


def _from_rules(utterance: str) -> tuple[str | None, str | None, str]:
    low = utterance.lower()
    about = None
    family = None
    reasons: list[str] = []
    if "?" in utterance or low.startswith(("why ", "what ", "how ", "who ")):
        family = "ask_talk"
        reasons.append("question shape")
    for needle, a, f, why in _RULES:
        if needle in low:
            if a and about is None:
                about = a
            if f and family is None:
                family = f
            reasons.append(why)
    if about is not None and about not in ALLOWED_ABOUT:
        about = None
    if family is not None and family not in ALLOWED_FAMILY:
        family = None
    return about, family, "; ".join(reasons) if reasons else "no Seed rule fired"


def suggest(utterance: str, source: str = "suggest", log_path: Path | None = None) -> dict:
    """Propose about/family from Seed lists only. Appends JSONL. Never writes live cards."""
    placement, holes = place(utterance=utterance, source=source)
    is_gold = str(placement.get("placement_id", "")).startswith("P_") and not str(
        placement.get("placement_id")
    ).startswith("P_unseen_")

    if is_gold:
        suggested_about = placement.get("about_id")
        suggested_family = placement.get("family_id")
        rationale = "echo gold placement; not a new suggestion"
        needs_review = placement.get("card_id") is None
    else:
        suggested_about, suggested_family, rationale = _from_rules(utterance)
        needs_review = True

    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "utterance": utterance,
        "source": source,
        "place_card_id": placement.get("card_id"),
        "place_hole_ids": list(placement.get("hole_ids") or []),
        "suggested_about_id": suggested_about,
        "suggested_family_id": suggested_family,
        "card_id": None,
        "needs_review": needs_review,
        "rationale": rationale,
        "kind": "gold" if is_gold else "unseen",
        "n_place_holes": len(holes),
    }

    target = DEFAULT_SUGGEST_LOG if log_path is None else log_path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")
    return row

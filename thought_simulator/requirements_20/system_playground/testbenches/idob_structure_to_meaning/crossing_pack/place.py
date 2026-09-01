from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

SEED_DIR = Path(__file__).parent / "seed"
PLACEMENTS_PATH = SEED_DIR / "placements.yaml"
HOLE_LEDGER_PATH = SEED_DIR / "hole_ledger.yaml"
ABOUT_PATH = SEED_DIR / "about_index.yaml"
FAMILY_PATH = SEED_DIR / "talk_families.yaml"


def _read_yaml(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or []


def _safe_slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug or "empty"


def _seed_maps() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], set[str], set[str]]:
    placements = _read_yaml(PLACEMENTS_PATH)
    holes = _read_yaml(HOLE_LEDGER_PATH)
    about = _read_yaml(ABOUT_PATH)
    families = _read_yaml(FAMILY_PATH)

    placements_by_utt = {str(row.get("utterance")): row for row in placements}
    holes_by_id = {str(row.get("hole_id")): row for row in holes}
    about_ids = {str(row.get("about_id")) for row in about if row.get("about_id") is not None}
    family_ids = {str(row.get("family_id")) for row in families if row.get("family_id") is not None}
    return placements_by_utt, holes_by_id, about_ids, family_ids


def place(utterance: str, source: str = "test") -> tuple[dict, list[dict]]:
    """Return (placement_record, hole_rows). Do not write files by default."""
    placements_by_utt, holes_by_id, _about_ids, _family_ids = _seed_maps()

    if utterance in placements_by_utt:
        row = dict(placements_by_utt[utterance])
        row["source"] = source
        hole_rows: list[dict[str, Any]] = []
        for hole_id in row.get("hole_ids") or []:
            if hole_id in holes_by_id:
                hole_rows.append(dict(holes_by_id[hole_id]))
        return row, hole_rows

    unseen_hole_id = "H_unseen_{0}".format(_safe_slug(utterance))
    placement = {
        "placement_id": "P_unseen_{0}".format(_safe_slug(utterance)),
        "utterance": utterance,
        "about_id": None,
        "family_id": None,
        "pattern_id": None,
        "card_id": None,
        "hole_ids": [unseen_hole_id],
        "source": source,
    }
    hole_rows = [
        {
            "hole_id": unseen_hole_id,
            "found_in": "utterance",
            "utterance": utterance,
            "family_id": None,
            "about_id": None,
            "card_id": None,
            "note": "Unseen utterance. Seed place() does not invent about/family/card.",
            "status": "open",
        }
    ]
    return placement, hole_rows

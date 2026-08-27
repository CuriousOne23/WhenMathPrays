"""Classify leftover after one hop. Do not invent keys or meaning floats."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from lib.hash_toy import toy_structural_key
from lib.schema_load import load_yaml

TABLE = Path(__file__).parent / "residue_next.examples.yaml"
CARDS = ROOT / "01_structure" / "structure_card.examples.yaml"
MAP = ROOT / "03_map_lookup" / "struct_to_meaning_map.slide.yaml"
KNOWN_CODES = {"static_object_vs_dynamic_action"}


def _map_index(data):
    rows = data.get("struct_to_meaning_map") or data.get("rows") or []
    out = {}
    for row in rows:
        cid = row.get("card_id")
        cands = row.get("meaning_group_candidates") or []
        if cid is not None:
            out[cid] = list(cands)
    return out


def classify(card, candidates):
    code = card.get("residue_code")
    if card.get("assignment_status") == "unassigned":
        return "unassigned", code
    if code and code not in KNOWN_CODES:
        return "unknown_residue", code
    if not list(candidates or []):
        return "empty_map", code
    if code:
        return "leftover_after_map", code
    return "digested_stop", code


def _lookup_row(table_rows, residue_code, after_status):
    for row in table_rows:
        if row.get("after_status") == after_status and row.get("residue_code") == residue_code:
            return row
    for row in table_rows:
        if row.get("after_status") == after_status and row.get("residue_code") in (None, "null"):
            return row
    for row in table_rows:
        if row.get("after_status") == "unknown_residue":
            return row
    return {
        "digested": False,
        "expand_target": "10_residue_expand/residue_next.examples.yaml",
        "next_key": None,
        "note": "No table row; add one.",
    }


def expand_card(card, candidates, table_rows):
    after_status, code = classify(card, candidates)
    row = _lookup_row(table_rows, code, after_status)
    return {
        "card_id": card.get("card_id"),
        "structural_key": toy_structural_key(card),
        "residue_code": code,
        "map_empty": not bool(candidates),
        "after_status": after_status,
        "digested": bool(row.get("digested")),
        "expand_target": row.get("expand_target"),
        "next_key": row.get("next_key"),
        "note": row.get("note"),
    }


def load_inputs():
    cards = (load_yaml(CARDS) or {}).get("cards") or []
    raw_map = load_yaml(MAP) or {}
    return cards, _map_index(raw_map), (load_yaml(TABLE) or {}).get("rows") or []

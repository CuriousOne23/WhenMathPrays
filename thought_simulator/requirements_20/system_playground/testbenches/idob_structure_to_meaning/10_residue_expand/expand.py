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


def _map_index(data):
    out = {}
    rows = data.get("rows") or data.get("map") or data.get("entries") or []
    if isinstance(data, dict) and not rows:
        # common slide shape: list under various keys
        for key in ("cards", "lookups", "items"):
            if key in data:
                rows = data[key]
                break
    if isinstance(data, list):
        rows = data
    for row in rows:
        cid = row.get("card_id") or row.get("id")
        cands = row.get("meaning_group_candidates")
        if cands is None:
            cands = row.get("candidate_group_ids") or row.get("groups") or []
        if cid is not None:
            out[cid] = list(cands or [])
    return out


def classify(card, candidates):
    code = card.get("residue_code")
    cands = list(candidates or [])
    if card.get("assignment_status") == "unassigned":
        return "unassigned", code
    if code and code not in (
        "static_object_vs_dynamic_action",
        None,
    ):
        # unknown unless listed as that exact teaching code
        known = {"static_object_vs_dynamic_action"}
        if code not in known:
            return "unknown_residue", code
    if not cands:
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
    key = toy_structural_key(card)
    return {
        "card_id": card.get("card_id"),
        "structural_key": key,
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

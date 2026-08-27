"""IdOB one-hop orchestrator. See idob_core.md.
Does not parse English except via Slide 09. Does not invent keys or groups.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from lib.hash_toy import toy_structural_key
from lib.schema_load import load_yaml
from lib.vector6 import NAMES, delta_l2, from_mapping, zeros

sys.path.insert(0, str(ROOT / "05_cie"))
from modulate import modulate  # noqa: E402

DEFAULT_EPS = 0.05
SLOTS = [
    "semantic_field_id",
    "semantic_role_id",
    "semantic_object_id",
    "gradient_id",
    "universe_id",
    "subfield_id",
]


def _empty_packet():
    return {
        "card_id": None,
        "utterance": None,
        "packs_loaded": [],
        "assignment_status": None,
        "semantic_field_id": None,
        "semantic_role_id": None,
        "semantic_object_id": None,
        "gradient_id": None,
        "universe_id": None,
        "subfield_id": None,
        "structural_key": None,
        "residue_code": None,
        "feature_tags": [],
        "candidate_group_ids": [],
        "final_rank_order": [],
        "selected_group_id": None,
        "cie_id": None,
        "meaning_semantics": None,
        "meaning_semantics_prime": None,
        "meaning_delta_h": None,
        "identity_delta": None,
        "refinement_cycles": 0,
        "resolution_status": None,
        "ready_for_ouba": False,
        "expand_target": None,
        "next_key": None,
    }


def _cards():
    return (load_yaml(ROOT / "01_structure" / "structure_card.examples.yaml") or {}).get("cards") or []


def _card_by_id(card_id):
    for row in _cards():
        if row.get("card_id") == card_id:
            return dict(row)
    return None


def _map_candidates(card_id):
    data = load_yaml(ROOT / "03_map_lookup" / "struct_to_meaning_map.slide.yaml") or {}
    for row in data.get("struct_to_meaning_map") or []:
        if row.get("card_id") == card_id:
            return list(row.get("meaning_group_candidates") or [])
    return []


def _groups():
    data = load_yaml(ROOT / "02_meaning_groups" / "meaning_groups.slide.yaml") or {}
    out = {}
    for row in data.get("meaning_groups") or []:
        out[int(row["group_id"])] = row
    return out


def _rank(candidates):
    weights = load_yaml(ROOT / "04_ranking" / "ranking_weights.slide.yaml") or {}
    w = weights.get("ranking_weights") or {}
    toy = {int(k): v for k, v in (weights.get("group_toy_scores") or {}).items()}
    scored = []
    for gid in candidates:
        gid = int(gid)
        parts = toy.get(gid, {"cue": 0.0, "invariant": 0.0, "identity": 0.0})
        score = (
            float(w.get("cue_weight", 0)) * float(parts.get("cue", 0))
            + float(w.get("invariant_weight", 0)) * float(parts.get("invariant", 0))
            + float(w.get("identity_weight", 0)) * float(parts.get("identity", 0))
        )
        scored.append((score, gid))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [gid for _s, gid in scored]


def _envelope(cie_id):
    data = load_yaml(ROOT / "05_cie" / "cie.examples.yaml") or {}
    rows = data.get("envelopes") or []
    if cie_id is None:
        cie_id = "neutral"
    for row in rows:
        if row.get("cie_id") == cie_id:
            return row
    return {
        "cie_id": cie_id,
        "identity_importance": 0.0,
        "identity_vector": zeros(),
    }


def _fill_card_fields(pkt, card):
    pkt["card_id"] = card.get("card_id")
    for s in SLOTS:
        pkt[s] = card.get(s)
    pkt["residue_code"] = card.get("residue_code")
    pkt["feature_tags"] = list(card.get("feature_tags") or [])
    if all(card.get(s) is not None for s in SLOTS):
        pkt["structural_key"] = toy_structural_key(card)


def _expand_hint(pkt, card):
    try:
        from importlib.util import spec_from_file_location, module_from_spec

        path = ROOT / "10_residue_expand" / "expand.py"
        spec = spec_from_file_location("expand10", path)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        _cards, mmap, table = mod.load_inputs()
        cands = mmap.get(card.get("card_id"), pkt.get("candidate_group_ids") or [])
        hint = mod.expand_card(card, cands, table)
        pkt["expand_target"] = hint.get("expand_target")
        pkt["next_key"] = hint.get("next_key")
    except Exception:
        pkt["expand_target"] = None
        pkt["next_key"] = None


def run_hop(
    card_id=None,
    utterance=None,
    packs_loaded=None,
    cie_id="physical_stance",
    clip_to_unit=True,
    epsilon=DEFAULT_EPS,
):
    pkt = _empty_packet()
    pkt["utterance"] = utterance
    pkt["packs_loaded"] = list(packs_loaded or [])
    pkt["cie_id"] = cie_id

    card = None
    if card_id:
        card = _card_by_id(card_id)
        if card is None:
            pkt["resolution_status"] = "unassigned"
            pkt["assignment_status"] = "unassigned"
            return pkt
        pkt["assignment_status"] = "card_given"
        _fill_card_fields(pkt, card)
    elif utterance is not None:
        sys.path.insert(0, str(ROOT / "09_structure_assignment"))
        from assign import assign

        packs = list(packs_loaded or ["base_en"])
        pkt["packs_loaded"] = packs
        assigned = assign(utterance, packs)
        pkt["assignment_status"] = assigned.get("assignment_status")
        pkt["residue_code"] = assigned.get("residue_code")
        pkt["feature_tags"] = list(assigned.get("feature_tags") or [])
        pkt["structural_key"] = assigned.get("structural_key")
        for s in SLOTS:
            pkt[s] = assigned.get(s)
        status = assigned.get("assignment_status")
        if status != "assigned":
            pkt["resolution_status"] = status
            return pkt
        card = {"card_id": None, **{s: assigned.get(s) for s in SLOTS}}
        card["residue_code"] = assigned.get("residue_code")
        card["feature_tags"] = assigned.get("feature_tags") or []
        # map is keyed by card_id in this revision; utterance-only hops have no map row
        pkt["candidate_group_ids"] = []
        pkt["resolution_status"] = "empty_map"
        pkt["refinement_cycles"] = 0
        return pkt
    else:
        pkt["resolution_status"] = "unassigned"
        pkt["assignment_status"] = "unassigned"
        return pkt

    if pkt["structural_key"] is None:
        pkt["resolution_status"] = pkt.get("assignment_status") or "unassigned"
        return pkt

    candidates = _map_candidates(pkt["card_id"])
    pkt["candidate_group_ids"] = list(candidates)
    if not candidates:
        pkt["resolution_status"] = "empty_map"
        _expand_hint(pkt, card)
        return pkt

    order = _rank(candidates)
    # wall: drop anything not in the map (should be a no-op)
    allowed = {int(x) for x in candidates}
    order = [g for g in order if g in allowed]
    pkt["final_rank_order"] = order
    if not order:
        pkt["resolution_status"] = "empty_map"
        _expand_hint(pkt, card)
        return pkt

    selected = order[0]
    pkt["selected_group_id"] = selected
    groups = _groups()
    proto = groups.get(int(selected))
    if proto is None:
        pkt["resolution_status"] = "empty_map"
        return pkt

    M = from_mapping(proto.get("group_dimensions"))
    env = _envelope(cie_id)
    alpha = float(env.get("identity_importance") or 0.0)
    I = from_mapping(env.get("identity_vector"))
    Mp = modulate(M, alpha, I, clip=clip_to_unit)
    pkt["meaning_semantics"] = dict(M)
    pkt["meaning_semantics_prime"] = dict(Mp)
    pkt["meaning_delta_h"] = delta_l2(Mp, M)
    shove = {n: alpha * float(I.get(n, 0.0)) for n in NAMES}
    pkt["identity_delta"] = delta_l2(shove, zeros())
    pkt["refinement_cycles"] = 1
    pkt["ready_for_ouba"] = True
    if pkt["meaning_delta_h"] < float(epsilon):
        pkt["resolution_status"] = "meaning_stable"
    else:
        pkt["resolution_status"] = "one_pass_complete"
    _expand_hint(pkt, card)
    return pkt

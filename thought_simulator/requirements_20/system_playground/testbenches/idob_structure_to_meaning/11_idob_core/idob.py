"""IdOB one-hop orchestrator. See idob_core.md.
Does not parse English except via Slide 09. Does not invent keys or groups.
Does not write routing_filter. Crossing is run_hop; process(tp) is an adapter.
"""
from __future__ import annotations

import copy
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
        "first_meaning_cycle": True,
        "meaning_semantics_before": None,
        "meaning_semantics": None,
        "meaning_semantics_prime": None,
        "meaning_delta_h": None,
        "meaning_cie_delta": None,
        "identity_delta": None,
        "identity_residual": {"magnitude": "none", "pattern": "none"},
        "hold_geometry": None,
        "refinement_cycles": 0,
        "resolution_status": None,
        "ready_for_ouba": False,
        "idob_complete": False,
        "path_b_eligible": False,
        "routing_filter_mutated": False,
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


def _set_identity_residual(pkt):
    status = pkt.get("resolution_status")
    code = pkt.get("residue_code")
    born = pkt.get("selected_group_id") is not None
    if status in ("unassigned", "partial"):
        pkt["identity_residual"] = {"magnitude": "small", "pattern": "unassigned"}
    elif status == "empty_map" or (not born and status == "empty_map"):
        pkt["identity_residual"] = {"magnitude": "medium", "pattern": "empty_map"}
    elif born and code:
        pkt["identity_residual"] = {"magnitude": "medium", "pattern": "leftover"}
    elif born:
        pkt["identity_residual"] = {"magnitude": "small", "pattern": "collapsed"}
    else:
        pkt["identity_residual"] = {"magnitude": "none", "pattern": "none"}


def _set_flags(pkt):
    born = pkt.get("selected_group_id") is not None
    pkt["ready_for_ouba"] = bool(born)
    pkt["path_b_eligible"] = bool(born and not pkt.get("residue_code"))
    pkt["idob_complete"] = bool(
        pkt["path_b_eligible"] and pkt.get("resolution_status") == "meaning_stable"
    )
    pkt["routing_filter_mutated"] = False
    if born and not pkt.get("hold_geometry"):
        pkt["hold_geometry"] = "formation"
    _set_identity_residual(pkt)


def run_hop(
    card_id=None,
    utterance=None,
    packs_loaded=None,
    cie_id="physical_stance",
    clip_to_unit=True,
    epsilon=DEFAULT_EPS,
    prior_M=None,
):
    pkt = _empty_packet()
    pkt["utterance"] = utterance
    pkt["packs_loaded"] = list(packs_loaded or [])
    pkt["cie_id"] = cie_id
    pkt["first_meaning_cycle"] = prior_M is None

    card = None
    if card_id:
        card = _card_by_id(card_id)
        if card is None:
            pkt["resolution_status"] = "unassigned"
            pkt["assignment_status"] = "unassigned"
            _set_flags(pkt)
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
            _set_flags(pkt)
            return pkt
        card = {"card_id": None, **{s: assigned.get(s) for s in SLOTS}}
        card["residue_code"] = assigned.get("residue_code")
        card["feature_tags"] = assigned.get("feature_tags") or []
        pkt["candidate_group_ids"] = []
        pkt["resolution_status"] = "empty_map"
        pkt["refinement_cycles"] = 0
        _set_flags(pkt)
        return pkt
    else:
        pkt["resolution_status"] = "unassigned"
        pkt["assignment_status"] = "unassigned"
        _set_flags(pkt)
        return pkt

    if pkt["structural_key"] is None:
        pkt["resolution_status"] = pkt.get("assignment_status") or "unassigned"
        _set_flags(pkt)
        return pkt

    candidates = _map_candidates(pkt["card_id"])
    pkt["candidate_group_ids"] = list(candidates)
    if not candidates:
        pkt["resolution_status"] = "empty_map"
        _expand_hint(pkt, card)
        _set_flags(pkt)
        return pkt

    order = _rank(candidates)
    allowed = {int(x) for x in candidates}
    order = [g for g in order if g in allowed]
    pkt["final_rank_order"] = order
    if not order:
        pkt["resolution_status"] = "empty_map"
        _expand_hint(pkt, card)
        _set_flags(pkt)
        return pkt

    selected = order[0]
    pkt["selected_group_id"] = selected
    groups = _groups()
    proto = groups.get(int(selected))
    if proto is None:
        pkt["resolution_status"] = "empty_map"
        _set_flags(pkt)
        return pkt

    M = from_mapping(proto.get("group_dimensions"))
    env = _envelope(cie_id)
    alpha = float(env.get("identity_importance") or 0.0)
    I = from_mapping(env.get("identity_vector"))
    Mp = modulate(M, alpha, I, clip=clip_to_unit)
    before = from_mapping(prior_M) if prior_M is not None else zeros()
    pkt["meaning_semantics_before"] = dict(before)
    pkt["meaning_semantics"] = dict(M)
    pkt["meaning_semantics_prime"] = dict(Mp)
    pkt["meaning_delta_h"] = delta_l2(Mp, before)
    pkt["meaning_cie_delta"] = delta_l2(Mp, M)
    shove = {n: alpha * float(I.get(n, 0.0)) for n in NAMES}
    pkt["identity_delta"] = delta_l2(shove, zeros())
    pkt["refinement_cycles"] = 1
    pkt["hold_geometry"] = "formation"
    if pkt["meaning_delta_h"] < float(epsilon):
        pkt["resolution_status"] = "meaning_stable"
    else:
        pkt["resolution_status"] = "one_pass_complete"
    _expand_hint(pkt, card)
    _set_flags(pkt)
    return pkt


def _routing_filter(tp):
    if not isinstance(tp, dict):
        return None
    proc = tp.get("process")
    if not isinstance(proc, dict):
        return None
    return proc.get("routing_filter")


def process(tp=None, mode="general", **kwargs):
    """Path A-shaped adapter. Crossing stays in run_hop. Must not write routing."""
    before = copy.deepcopy(tp) if isinstance(tp, dict) else {}
    rf_before = _routing_filter(before)
    card_id = kwargs.get("card_id") or (tp or {}).get("card_id")
    if not card_id and isinstance((tp or {}).get("idob"), dict):
        card_id = tp["idob"].get("card_id")
    utterance = kwargs.get("utterance") or (tp or {}).get("utterance")
    packs = kwargs.get("packs_loaded")
    cie_id = kwargs.get("cie_id", "physical_stance")
    clip = kwargs.get("clip_to_unit", True)
    epsilon = kwargs.get("epsilon", DEFAULT_EPS)
    prior_M = kwargs.get("prior_M")
    pkt = run_hop(
        card_id=card_id,
        utterance=utterance,
        packs_loaded=packs,
        cie_id=cie_id,
        clip_to_unit=clip,
        epsilon=epsilon,
        prior_M=prior_M,
    )
    out = before if before else {}
    out.setdefault("idob", {}).update(pkt)
    out.setdefault("semantic", {})["meaning_delta_h"] = pkt.get("meaning_delta_h")
    if rf_before is not None:
        out.setdefault("process", {})["routing_filter"] = copy.deepcopy(rf_before)
    mutated = _routing_filter(out) != rf_before and rf_before is not None
    if mutated:
        out.setdefault("_idob_diagnostics", {})["routing_filter_mutated"] = True
        out.setdefault("process", {})["routing_filter"] = copy.deepcopy(rf_before)
        pkt["routing_filter_mutated"] = True
        out["idob"]["routing_filter_mutated"] = True
    else:
        pkt["routing_filter_mutated"] = False
        out.setdefault("idob", {})["routing_filter_mutated"] = False
    return out

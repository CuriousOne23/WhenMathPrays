"""IdOB structure-to-meaning hop (Path A production copy).

Loads YAML only from this directory. Does not import 11_idob_core.
Architecturally the same hop as the learning-bench kernel: six IDs -> map ->
rank -> M -> CIE -> delta_h -> flags. Separate file.

Field catalog authority (20.116): requirements_20/20.116_field_catalog.md
and 20.116.010 / .020 / .030. 20.116 wins names/paths/owners;
this module wins hop behavior.
"""
from __future__ import annotations

import copy
import math
import re
from pathlib import Path
from typing import Any, Optional

import yaml

PRIMITIVE_NAME = "idob"
HERE = Path(__file__).resolve().parent
DEFAULT_EPS = 0.05
SLOTS = [
    "semantic_field_id",
    "semantic_role_id",
    "semantic_object_id",
    "gradient_id",
    "universe_id",
    "subfield_id",
]
NAMES = [
    "physicality",
    "sociality",
    "temporality",
    "intentionality",
    "materiality",
    "spatiality",
]
DICT_FILES = {
    "semantic_field_id": "semantic_field_definitions.yaml",
    "semantic_role_id": "semantic_roles_dictionary.yaml",
    "semantic_object_id": "semantic_objects.yaml",
    "gradient_id": "semantic_gradients.yaml",
    "universe_id": "semantic_universe_dictionary.yaml",
    "subfield_id": "semantic_subfields.yaml",
}


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


def _load_yaml(name: str):
    path = HERE / name
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _dict_ids(slot: str):
    data = _load_yaml(DICT_FILES[slot])
    for key in ("entries",):
        if key in data:
            return {int(row["id"]) for row in data[key]}
    # first mapping value that looks like a table
    for v in data.values():
        if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]:
            return {int(row["id"]) for row in v}
    return set()


def toy_structural_key(card: dict) -> str:
    parts = [str(int(card[s])) for s in SLOTS]
    return "SK|" + "|".join(parts)


def zeros():
    return {n: 0.0 for n in NAMES}


def from_mapping(src):
    if not src:
        return zeros()
    if isinstance(src, dict):
        return {n: float(src.get(n, 0.0) or 0.0) for n in NAMES}
    return zeros()


def clip_unit(vec):
    return {n: max(0.0, min(1.0, float(vec[n]))) for n in NAMES}


def add_scaled(M, I, alpha, clip=True):
    out = {n: float(M[n]) + float(alpha) * float(I[n]) for n in NAMES}
    return clip_unit(out) if clip else out


def delta_l2(a, b):
    a, b = from_mapping(a), from_mapping(b)
    return math.sqrt(sum((a[n] - b[n]) ** 2 for n in NAMES))


def modulate(M, alpha, I, clip=True):
    return add_scaled(from_mapping(M), from_mapping(I), float(alpha), clip=clip)


def _normalize(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _phrase_in(norm_utt: str, phrase: str) -> bool:
    p = _normalize(phrase)
    if not p:
        return False
    return f" {p} " in f" {norm_utt} " or norm_utt == p


def _pack_path(pack_id: str) -> Path:
    candidates = [
        HERE / f"pack_{pack_id}.yaml",
        HERE / f"{pack_id}.yaml",
        HERE / pack_id,
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"pack not under primitives/idob: {pack_id}")


def assign(utterance: str, packs_loaded=None) -> dict:
    packs_loaded = list(packs_loaded or ["base_en"])
    norm = _normalize(utterance)
    packs = []
    for pid in packs_loaded:
        data = _load_yaml(_pack_path(pid).name)
        data["pack_id"] = data.get("pack_id") or pid
        data["precedence"] = int(data.get("precedence") or 0)
        packs.append(data)
    packs.sort(key=lambda p: p["precedence"], reverse=True)

    filled = {s: None for s in SLOTS}
    residue = None
    tags = []
    best_tmpl = None
    best_len = -1
    best_prec = -1
    for pack in packs:
        for tmpl in pack.get("templates") or []:
            for phrase in tmpl.get("phrases") or []:
                if not _phrase_in(norm, phrase):
                    continue
                n = len(_normalize(phrase))
                prec = pack["precedence"]
                if n > best_len or (n == best_len and prec > best_prec):
                    best_tmpl, best_len, best_prec = tmpl, n, prec
    if best_tmpl:
        for s in SLOTS:
            if best_tmpl.get(s) is not None:
                filled[s] = best_tmpl[s]
        residue = best_tmpl.get("residue_code")
        tags = list(best_tmpl.get("feature_tags") or [])

    for s in SLOTS:
        if filled[s] is not None:
            continue
        candidates = []
        for pack in packs:
            for cue in (pack.get("slot_cues") or {}).get(s) or []:
                phrase = cue.get("phrase")
                if _phrase_in(norm, phrase):
                    candidates.append((len(_normalize(phrase)), pack["precedence"], cue.get("id")))
        if not candidates:
            continue
        candidates.sort(key=lambda t: (t[0], t[1]), reverse=True)
        filled[s] = candidates[0][2]

    # Touch structure dictionaries so they are live inventories.
    for s in SLOTS:
        if filled[s] is None:
            continue
        allowed = _dict_ids(s)
        if allowed and int(filled[s]) not in allowed:
            residue = residue or "unknown_structure_id"

    present = sum(1 for s in SLOTS if filled[s] is not None)
    status = "assigned" if present == 6 else ("unassigned" if present == 0 else "partial")
    out = {
        "utterance": utterance,
        "packs_loaded": packs_loaded,
        "assignment_status": status,
        "residue_code": residue,
        "feature_tags": tags,
        "structural_key": toy_structural_key(filled) if present == 6 else None,
    }
    out.update(filled)
    return out


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
    return (_load_yaml("structure_card.examples.yaml") or {}).get("cards") or []


def _card_by_id(card_id):
    for row in _cards():
        if row.get("card_id") == card_id:
            return dict(row)
    return None


def _map_candidates(card_id=None, structural_key=None):
    data = _load_yaml("struct_to_meaning_map.yaml") or {}
    rows = data.get("struct_to_meaning_map") or []
    for row in rows:
        if card_id and row.get("card_id") == card_id:
            return list(row.get("meaning_group_candidates") or [])
    if structural_key:
        for row in rows:
            if row.get("structural_key") == structural_key:
                return list(row.get("meaning_group_candidates") or [])
    return []


def _groups():
    data = _load_yaml("meaning_groups.yaml") or {}
    return {int(row["group_id"]): row for row in data.get("meaning_groups") or []}


def _rank(candidates):
    weights = _load_yaml("ranking_weights.yaml") or {}
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
    rows = (_load_yaml("cie.examples.yaml") or {}).get("envelopes") or []
    cie_id = cie_id or "neutral"
    for row in rows:
        if row.get("cie_id") == cie_id:
            return row
    return {"cie_id": cie_id, "identity_importance": 0.0, "identity_vector": zeros()}


def _fill_card_fields(pkt, card):
    pkt["card_id"] = card.get("card_id")
    for s in SLOTS:
        pkt[s] = card.get(s)
    pkt["residue_code"] = card.get("residue_code")
    pkt["feature_tags"] = list(card.get("feature_tags") or [])
    if all(card.get(s) is not None for s in SLOTS):
        pkt["structural_key"] = toy_structural_key(card)


def _expand_hint(pkt):
    table = (_load_yaml("residue_next.examples.yaml") or {}).get("rows") or []
    code = pkt.get("residue_code")
    status = pkt.get("resolution_status")
    born = pkt.get("selected_group_id") is not None
    if born and code:
        want = "leftover_after_map"
    elif status == "empty_map":
        want = "empty_map"
    elif status in ("unassigned", "partial"):
        want = "unassigned"
    elif born and not code:
        want = "digested_stop"
    else:
        want = None
    for row in table:
        if row.get("after_status") == want and (row.get("residue_code") == code or want != "leftover_after_map"):
            if want == "leftover_after_map" and row.get("residue_code") != code:
                continue
            pkt["expand_target"] = row.get("expand_target")
            pkt["next_key"] = row.get("next_key")
            return
    pkt["expand_target"] = None
    pkt["next_key"] = None


def _set_identity_residual(pkt):
    status = pkt.get("resolution_status")
    code = pkt.get("residue_code")
    born = pkt.get("selected_group_id") is not None
    if status in ("unassigned", "partial"):
        pkt["identity_residual"] = {"magnitude": "small", "pattern": "unassigned"}
    elif status == "empty_map":
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
    # packet contract file is loaded so it is not an unused YAML
    _load_yaml("idob_s2m_packet.yaml")


def _birth(pkt, card, cie_id, clip_to_unit, epsilon, prior_M):
    candidates = _map_candidates(pkt.get("card_id"), pkt.get("structural_key"))
    pkt["candidate_group_ids"] = list(candidates)
    if not candidates:
        pkt["resolution_status"] = "empty_map"
        _expand_hint(pkt)
        _set_flags(pkt)
        return pkt
    order = [g for g in _rank(candidates) if int(g) in {int(x) for x in candidates}]
    pkt["final_rank_order"] = order
    if not order:
        pkt["resolution_status"] = "empty_map"
        _expand_hint(pkt)
        _set_flags(pkt)
        return pkt
    selected = order[0]
    pkt["selected_group_id"] = selected
    proto = _groups().get(int(selected))
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
    pkt["resolution_status"] = (
        "meaning_stable" if pkt["meaning_delta_h"] < float(epsilon) else "one_pass_complete"
    )
    _expand_hint(pkt)
    _set_flags(pkt)
    return pkt


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

    if card_id:
        card = _card_by_id(card_id)
        if card is None:
            pkt["resolution_status"] = "unassigned"
            pkt["assignment_status"] = "unassigned"
            _set_flags(pkt)
            return pkt
        pkt["assignment_status"] = "card_given"
        _fill_card_fields(pkt, card)
        return _birth(pkt, card, cie_id, clip_to_unit, epsilon, prior_M)

    if utterance is not None:
        packs = list(packs_loaded or ["base_en"])
        pkt["packs_loaded"] = packs
        assigned = assign(utterance, packs)
        pkt["assignment_status"] = assigned.get("assignment_status")
        pkt["residue_code"] = assigned.get("residue_code")
        pkt["feature_tags"] = list(assigned.get("feature_tags") or [])
        pkt["structural_key"] = assigned.get("structural_key")
        for s in SLOTS:
            pkt[s] = assigned.get(s)
        if assigned.get("assignment_status") != "assigned":
            pkt["resolution_status"] = assigned.get("assignment_status")
            _expand_hint(pkt)
            _set_flags(pkt)
            return pkt
        card = {"card_id": None, **{s: assigned.get(s) for s in SLOTS}}
        card["residue_code"] = assigned.get("residue_code")
        return _birth(pkt, card, cie_id, clip_to_unit, epsilon, prior_M)

    pkt["resolution_status"] = "unassigned"
    pkt["assignment_status"] = "unassigned"
    _set_flags(pkt)
    return pkt


def _routing_filter(tp):
    if not isinstance(tp, dict):
        return None
    proc = tp.get("process")
    if not isinstance(proc, dict):
        return None
    return proc.get("routing_filter")


def process(tp: Optional[dict] = None, mode: str = "general", **kwargs) -> dict:
    before = copy.deepcopy(tp) if isinstance(tp, dict) else {}
    rf_before = _routing_filter(before)
    card_id = kwargs.get("card_id") or before.get("card_id")
    if not card_id and isinstance(before.get("idob"), dict):
        card_id = before["idob"].get("card_id")
    utterance = kwargs.get("utterance") or before.get("utterance")
    if utterance is None and isinstance(before.get("idob"), dict):
        utterance = before["idob"].get("utterance")
    pkt = run_hop(
        card_id=card_id,
        utterance=utterance,
        packs_loaded=kwargs.get("packs_loaded"),
        cie_id=kwargs.get("cie_id", "physical_stance"),
        clip_to_unit=kwargs.get("clip_to_unit", True),
        epsilon=kwargs.get("epsilon", DEFAULT_EPS),
        prior_M=kwargs.get("prior_M"),
    )
    out = before if before else {}
    out.setdefault("idob", {}).update(pkt)
    out.setdefault("semantic", {})["meaning_delta_h"] = pkt.get("meaning_delta_h")
    out["idob_complete"] = bool(pkt.get("idob_complete"))
    out["path_b_eligible"] = bool(pkt.get("path_b_eligible"))
    out["ready_for_ouba"] = bool(pkt.get("ready_for_ouba"))
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


class IdOB:
    def __init__(self, tp: Optional[dict] = None):
        self.tp = copy.deepcopy(tp) if tp is not None else {}

    def process(self, mode: str = "general", **kwargs) -> dict:
        self.tp = process(self.tp, mode=mode, **kwargs)
        return self.tp

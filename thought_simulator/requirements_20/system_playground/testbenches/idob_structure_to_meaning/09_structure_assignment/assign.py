"""Utterance + loaded packs -> structure card or unassigned. Meaning-blind."""
from __future__ import annotations

import re
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from lib.hash_toy import toy_structural_key
from lib.schema_load import load_yaml

SLOTS = [
    "semantic_field_id",
    "semantic_role_id",
    "semantic_object_id",
    "gradient_id",
    "universe_id",
    "subfield_id",
]

PACK_DIR = Path(__file__).resolve().parent / "packs"


def normalize(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _load_pack(pack_id: str) -> dict:
    path = PACK_DIR / f"{pack_id}.yaml"
    if not path.exists():
        # allow pack_geology.yaml named as pack_id pack_geology
        alt = PACK_DIR / f"{pack_id}"
        if alt.exists():
            path = alt
        else:
            raise FileNotFoundError(f"pack not on disk: {pack_id} ({path})")
    data = load_yaml(path) or {}
    data["pack_id"] = data.get("pack_id") or pack_id
    data["precedence"] = int(data.get("precedence") or 0)
    return data


def _phrase_in(norm_utt: str, phrase: str) -> bool:
    p = normalize(phrase)
    if not p:
        return False
    return f" {p} " in f" {norm_utt} " or norm_utt == p


def assign(utterance: str, packs_loaded=None) -> dict:
    packs_loaded = list(packs_loaded or ["base_en"])
    norm = normalize(utterance)
    packs = [_load_pack(pid) for pid in packs_loaded]
    packs.sort(key=lambda p: p["precedence"], reverse=True)

    filled = {s: None for s in SLOTS}
    residue = None
    tags = []
    collisions = []
    source = {s: None for s in SLOTS}

    # templates: longest phrase among loaded packs
    best_tmpl = None
    best_len = -1
    best_prec = -1
    for pack in packs:
        for tmpl in pack.get("templates") or []:
            for phrase in tmpl.get("phrases") or []:
                if not _phrase_in(norm, phrase):
                    continue
                n = len(normalize(phrase))
                prec = pack["precedence"]
                if n > best_len or (n == best_len and prec > best_prec):
                    best_tmpl = tmpl
                    best_len = n
                    best_prec = prec
    if best_tmpl:
        for s in SLOTS:
            if best_tmpl.get(s) is not None:
                filled[s] = best_tmpl[s]
                source[s] = "template"
        residue = best_tmpl.get("residue_code")
        tags = list(best_tmpl.get("feature_tags") or [])

    # slot cues for empty slots
    for s in SLOTS:
        if filled[s] is not None:
            continue
        candidates = []
        for pack in packs:
            for cue in (pack.get("slot_cues") or {}).get(s) or []:
                phrase = cue.get("phrase")
                if _phrase_in(norm, phrase):
                    candidates.append((len(normalize(phrase)), pack["precedence"], pack["pack_id"], cue.get("id"), phrase))
        if not candidates:
            continue
        candidates.sort(key=lambda t: (t[0], t[1]), reverse=True)
        top = candidates[0]
        tied = [c for c in candidates if c[0] == top[0] and c[3] != top[3]]
        if tied:
            collisions.append(
                {"slot": s, "phrase": top[4], "ids": sorted({top[3], *(c[3] for c in tied)})}
            )
        filled[s] = top[3]
        source[s] = "slot_cue"

    present = sum(1 for s in SLOTS if filled[s] is not None)
    if present == 6:
        status = "assigned"
    elif present == 0:
        status = "unassigned"
    else:
        status = "partial"

    out = {
        "utterance": utterance,
        "packs_loaded": packs_loaded,
        "assignment_status": status,
        "collisions": collisions,
        "residue_code": residue,
        "feature_tags": tags,
    }
    for s in SLOTS:
        out[s] = filled[s]
    if present == 6:
        out["structural_key"] = toy_structural_key(filled)
    else:
        out["structural_key"] = None
    return out

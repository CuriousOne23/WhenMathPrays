"""
SmOB — Semantic-Adjacent OB (Version 1.0)
Path-A post-CnOB cue extraction + pre-semantic compression.

Job 1: extract semantic-adjacent cues from CnOB TP residue
Job 2: TR-input vector + presemantic_residue_hash

Aligned with:
  - 20.40.040 v2.0
  - smob_py_struc_pgm.md v1.0
  - smob_cnob_comm_architect.md v1.0 (R4 surface+residue contract)
"""

import os
import copy
import yaml
import hashlib
from datetime import datetime, timezone

PRIMITIVE_NAME = "smob"


def get_primitive_name():
    return PRIMITIVE_NAME


class SmOB:
    def __init__(self, tp_input):
        self.tp = copy.deepcopy(tp_input) if tp_input else {}
        self.rules = {}
        self._dir = os.path.dirname(__file__)
        self._cue_decisions = []
        self._importance_decisions = []
        self._compress_decisions = []
        self._load_status = "ok"

    def process(self):
        self._load_support_yamls()
        cnob_map = self._read_cnob_map()
        cnob_residue = self._read_cnob_residue()
        srob_map = self._read_srob_map()

        cues = self._extract_cues(cnob_map, cnob_residue, srob_map)
        cues = self._normalize_discourse(cues, cnob_map, srob_map)
        cues = self._apply_importance(cues, cnob_map, cnob_residue)

        tr = self._form_tr_vector(cues)
        cue_map = self._build_cue_map(cues)
        residue = self._build_residue(cue_map, cues, tr)
        audit = self._build_audit_record(cue_map, residue)

        self.tp.setdefault("structural", {})
        self.tp["structural"]["smob_cue_map"] = cue_map
        self.tp["structural"]["smob_residue"] = residue
        self.tp.setdefault("metadata", {})
        self.tp["metadata"]["smob_audit_record"] = audit
        return self.tp

    # ----------------------------------------------------------
    # Load / read
    # ----------------------------------------------------------

    def _load_support_yamls(self):
        names = [
            "smob_cue_rules.yaml",
            "smob_discourse_rules.yaml",
            "smob_importance_rules.yaml",
            "smob_compress_rules.yaml",
        ]
        for name in names:
            path = os.path.join(self._dir, name)
            key = name.replace(".yaml", "").replace("smob_", "")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self.rules[key] = yaml.safe_load(f) or {}
            else:
                self.rules[key] = {}
                self._load_status = "partial"

    def _read_cnob_map(self):
        return (self.tp.get("structural") or {}).get("cnob_constraint_map") or {}

    def _read_cnob_residue(self):
        return (self.tp.get("structural") or {}).get("cnob_residue") or {}

    def _read_srob_map(self):
        return (self.tp.get("structural") or {}).get("srob_structural_map") or {}

    # ----------------------------------------------------------
    # CnOB surface helpers
    # ----------------------------------------------------------

    def _conflicts(self, cnob_map, cnob_residue):
        a = list(cnob_map.get("conflict_indicators") or [])
        if not a:
            a = list(cnob_residue.get("conflict_indicators") or [])
        return a

    def _missing(self, cnob_map, cnob_residue):
        a = list(cnob_map.get("missing_slot_signals") or [])
        if not a:
            a = list(cnob_residue.get("missing_slot_signals") or [])
        return a

    def _underspec(self, cnob_map, cnob_residue):
        a = list(cnob_map.get("underspecification_markers") or [])
        if not a:
            a = list(cnob_residue.get("underspecification_markers") or [])
        return a

    def _importance(self, cnob_map, cnob_residue):
        a = list(cnob_map.get("constraint_importance") or [])
        if not a:
            a = list(cnob_residue.get("constraint_importance") or [])
        return a

    def _c7_or_routing(self, cnob_map):
        fam = (cnob_map.get("constraint_families") or {}).get("C7") or []
        routing = cnob_map.get("routing_constraints") or []
        return bool(fam) or bool(routing)

    def _modalities(self, srob_map):
        mods = []
        seen = set()
        for seg in srob_map.get("segments") or []:
            if not isinstance(seg, dict):
                continue
            m = seg.get("modality")
            if m and m not in seen:
                seen.add(m)
                mods.append(str(m))
        return mods

    def _cue_entry(self, family, cue_id, rule_id, source="cnob", segment_ids=None, note=""):
        e = {
            "family": family,
            "cue_id": cue_id,
            "rule_id": rule_id,
            "segment_ids": list(segment_ids or []),
            "source": source,
            "note": note or "",
        }
        self._cue_decisions.append(f"{family}:{cue_id}:{rule_id}")
        return e

    # ----------------------------------------------------------
    # Job 1 — cues
    # ----------------------------------------------------------

    def _extract_cues(self, cnob_map, cnob_residue, srob_map):
        cues = {
            "semantic_adjacent_cues": [],
            "modality_cues": [],
            "affect_markers": [],
            "conflict_adjacent_signals": [],
            "underspecification_adjacent_signals": [],
            "constraint_importance_adjacent_signals": [],
            "discourse_adjacent_cues": [],
            "routing_semantic_cues": [],
            "delta_h_semantic_adjacent": [],
        }

        def add_sa(cue_id, rule_id, source="cnob"):
            cues["semantic_adjacent_cues"].append(
                self._cue_entry("semantic_adjacent", cue_id, rule_id, source=source)
            )

        if self._conflicts(cnob_map, cnob_residue):
            e = self._cue_entry(
                "conflict_adjacent", "conflict_adjacent", "cue_conflict_present"
            )
            cues["conflict_adjacent_signals"].append(e)
            add_sa("conflict_adjacent", "cue_conflict_present")

        if self._missing(cnob_map, cnob_residue):
            segs = []
            for m in self._missing(cnob_map, cnob_residue):
                if isinstance(m, dict):
                    segs.extend(m.get("segment_ids") or [])
            e = self._cue_entry(
                "underspecification_adjacent",
                "gap_adjacent",
                "cue_missing_slot",
                segment_ids=segs,
            )
            cues["underspecification_adjacent_signals"].append(e)
            add_sa("gap_adjacent", "cue_missing_slot")

        if self._underspec(cnob_map, cnob_residue):
            segs = []
            for u in self._underspec(cnob_map, cnob_residue):
                if isinstance(u, dict):
                    segs.extend(u.get("segment_ids") or [])
            e = self._cue_entry(
                "underspecification_adjacent",
                "underspec_adjacent",
                "cue_underspec",
                segment_ids=segs,
            )
            cues["underspecification_adjacent_signals"].append(e)
            add_sa("underspec_adjacent", "cue_underspec")

        if self._c7_or_routing(cnob_map):
            e = self._cue_entry("routing_semantic", "routing_cue", "cue_routing")
            cues["routing_semantic_cues"].append(e)
            add_sa("routing_cue", "cue_routing")

        for mod in self._modalities(srob_map):
            e = self._cue_entry(
                "modality", mod, "cue_modality_from_srob", source="srob"
            )
            cues["modality_cues"].append(e)

        return cues

    def _normalize_discourse(self, cues, cnob_map, srob_map):
        disc_rules = self.rules.get("discourse_rules") or {}
        canon = disc_rules.get("canonicalize") or {}

        def norm_flag(f):
            s = str(f).lower()
            return canon.get(s, canon.get(str(f), str(f)))

        seen = set()
        flags = []

        for item in cnob_map.get("discourse_constraints") or []:
            if isinstance(item, dict):
                for fl in item.get("flags") or []:
                    flags.append((norm_flag(fl), "cnob"))
                if item.get("rule_id") and not item.get("flags"):
                    flags.append((norm_flag(item.get("rule_id")), "cnob"))
            else:
                flags.append((norm_flag(item), "cnob"))

        for fl in srob_map.get("discourse_flags") or []:
            flags.append((norm_flag(fl), "srob"))

        for fid, source in flags:
            if not fid or fid in seen:
                continue
            seen.add(fid)
            e = self._cue_entry(
                "discourse_adjacent",
                fid,
                "disc_from_cnob" if source == "cnob" else "disc_from_srob",
                source=source,
            )
            cues["discourse_adjacent_cues"].append(e)
            cues["semantic_adjacent_cues"].append(
                self._cue_entry(
                    "semantic_adjacent", fid, e["rule_id"], source=source
                )
            )
        return cues

    def _apply_importance(self, cues, cnob_map, cnob_residue):
        imp_rules = self.rules.get("importance_rules") or {}
        label_map = imp_rules.get("label_map") or {
            "gap_high": "sa_gap_high",
            "conflict_high": "sa_conflict_high",
            "constraint_anchor": "sa_anchor",
            "order_sensitive": "sa_order_sensitive",
        }
        allow_unknown = bool(imp_rules.get("allow_passthrough_unknown", False))

        for item in self._importance(cnob_map, cnob_residue):
            if not isinstance(item, dict):
                continue
            labels = item.get("labels") or []
            segs = item.get("segment_ids") or []
            for lab in labels:
                lab_s = str(lab)
                mapped = label_map.get(lab_s)
                if mapped is None:
                    if allow_unknown:
                        mapped = f"sa_{lab_s}"
                    else:
                        continue
                e = self._cue_entry(
                    "constraint_importance_adjacent",
                    mapped,
                    "imp_map_labels",
                    segment_ids=segs,
                )
                cues["constraint_importance_adjacent_signals"].append(e)
                cues["semantic_adjacent_cues"].append(
                    self._cue_entry(
                        "semantic_adjacent", mapped, "imp_map_labels"
                    )
                )
                self._importance_decisions.append(mapped)
        return cues

    # ----------------------------------------------------------
    # Job 2 — TR + hash
    # ----------------------------------------------------------

    def _form_tr_vector(self, cues):
        def first_id(family_key):
            for e in cues.get(family_key) or []:
                if isinstance(e, dict) and e.get("cue_id"):
                    return str(e["cue_id"])
            return ""

        slots = [
            {"slot": "modality", "value": first_id("modality_cues")},
            {
                "slot": "conflict",
                "value": "conflict_adjacent"
                if cues.get("conflict_adjacent_signals")
                else "",
            },
            {
                "slot": "underspec",
                "value": "underspec_adjacent"
                if cues.get("underspecification_adjacent_signals")
                else "",
            },
            {
                "slot": "importance",
                "value": first_id("constraint_importance_adjacent_signals"),
            },
            {
                "slot": "routing",
                "value": "routing_cue" if cues.get("routing_semantic_cues") else "",
            },
            {
                "slot": "discourse",
                "value": first_id("discourse_adjacent_cues"),
            },
        ]
        for s in slots:
            self._compress_decisions.append(f"{s['slot']}={s['value'] or '∅'}")
        return slots

    def _build_cue_map(self, cues):
        return {
            "semantic_adjacent_cues": list(cues.get("semantic_adjacent_cues") or []),
            "modality_cues": list(cues.get("modality_cues") or []),
            "affect_markers": list(cues.get("affect_markers") or []),
            "conflict_adjacent_signals": list(
                cues.get("conflict_adjacent_signals") or []
            ),
            "underspecification_adjacent_signals": list(
                cues.get("underspecification_adjacent_signals") or []
            ),
            "constraint_importance_adjacent_signals": list(
                cues.get("constraint_importance_adjacent_signals") or []
            ),
            "discourse_adjacent_cues": list(
                cues.get("discourse_adjacent_cues") or []
            ),
            "routing_semantic_cues": list(cues.get("routing_semantic_cues") or []),
            "delta_h_semantic_adjacent": list(
                cues.get("delta_h_semantic_adjacent") or []
            ),
        }

    def _build_residue(self, cue_map, cues, tr):
        summary = []
        for name, key in [
            ("semantic_adjacent", "semantic_adjacent_cues"),
            ("modality", "modality_cues"),
            ("conflict_adjacent", "conflict_adjacent_signals"),
            ("underspecification_adjacent", "underspecification_adjacent_signals"),
            ("constraint_importance_adjacent", "constraint_importance_adjacent_signals"),
            ("discourse_adjacent", "discourse_adjacent_cues"),
            ("routing_semantic", "routing_semantic_cues"),
        ]:
            if cue_map.get(key):
                summary.append(name)

        residue_body = {
            "semantic_adjacent_cues": list(cue_map.get("semantic_adjacent_cues") or []),
            "conflict_adjacent_signals": list(
                cue_map.get("conflict_adjacent_signals") or []
            ),
            "underspecification_adjacent_signals": list(
                cue_map.get("underspecification_adjacent_signals") or []
            ),
            "constraint_importance_adjacent_signals": list(
                cue_map.get("constraint_importance_adjacent_signals") or []
            ),
            "tr_input_cues": list(tr),
            "cue_family_summary": summary,
            "disagreement_flags": [],
            "override_flags": [],
        }
        residue_body["presemantic_residue_hash"] = self._hash(
            {"cue_map": cue_map, "signals": residue_body, "tr": tr}
        )
        return residue_body

    def _hash(self, obj):
        raw = yaml.dump(obj, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def _build_audit_record(self, cue_map, residue):
        return {
            "support_yaml_load_status": self._load_status,
            "cue_decisions": self._cue_decisions[:64],
            "importance_decisions": self._importance_decisions[:32],
            "compress_decisions": self._compress_decisions[:16],
            "provenance_lineage": {
                "origin": "SmOB",
                "last_update": "SmOB",
            },
            "smob_cue_map_hash": self._hash(cue_map),
            "presemantic_residue_hash": residue.get("presemantic_residue_hash"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

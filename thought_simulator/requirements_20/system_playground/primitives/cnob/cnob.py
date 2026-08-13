"""
CnOB — Constraint OB (Version 1.0)
Path-A post-SROB constraint residue primitive.

Responsibilities:
  1. Load CnOB support YAMLs only (not srob_*.yaml / sob_*.yaml)
  2. Read SROB map/residue from TP (surface contract)
  3. Encode C1–C7, missing-slot, underspec, conflict, importance
  4. Write full cnob_constraint_map + cnob_residue + audit

Aligned with:
  - 20.40.030 v2.0
  - cnob_py_struc_pgm.md v1.1
  - cnob_srob_comm_architect.md v1.1 (Q9 surface contract)
"""

import os
import copy
import yaml
import hashlib
from datetime import datetime, timezone

PRIMITIVE_NAME = "cnob"


def get_primitive_name():
    return PRIMITIVE_NAME


class CnOB:
    def __init__(self, tp_input):
        self.tp = copy.deepcopy(tp_input) if tp_input else {}
        self.rules = {}
        self._dir = os.path.dirname(__file__)
        self._family_decisions = []
        self._gap_decisions = []
        self._conflict_decisions = []
        self._importance_decisions = []
        self._load_status = "ok"

    def process(self):
        self._load_support_yamls()
        srob_map = self._read_srob_map()
        srob_residue = self._read_srob_residue()

        families = self._encode_families(srob_map, srob_residue)
        missing, under = self._apply_gap_rules(srob_map, srob_residue)
        conflicts = self._apply_conflict_rules(srob_map, srob_residue)
        importance = self._apply_importance(srob_map, missing, under, conflicts)

        cnob_map = self._build_constraint_map(
            families, missing, under, conflicts, importance, srob_map
        )
        residue = self._build_residue(cnob_map, missing, under, conflicts, importance)
        audit = self._build_audit_record(cnob_map, residue)

        self.tp.setdefault("structural", {})
        self.tp["structural"]["cnob_constraint_map"] = cnob_map
        self.tp["structural"]["cnob_residue"] = residue
        self.tp.setdefault("metadata", {})
        self.tp["metadata"]["cnob_audit_record"] = audit
        return self.tp

    # ----------------------------------------------------------
    # Load / read
    # ----------------------------------------------------------

    def _load_support_yamls(self):
        names = [
            "cnob_constraint_rules.yaml",
            "cnob_missing_slot_rules.yaml",
            "cnob_conflict_rules.yaml",
            "cnob_importance_rules.yaml",
        ]
        for name in names:
            path = os.path.join(self._dir, name)
            key = name.replace(".yaml", "").replace("cnob_", "")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self.rules[key] = yaml.safe_load(f) or {}
            else:
                self.rules[key] = {}
                self._load_status = "partial"

    def _read_srob_map(self):
        structural = self.tp.get("structural") or {}
        smap = structural.get("srob_structural_map")
        if smap:
            return smap
        # isolation fallback only
        return structural.get("sob_structural_map") or {}

    def _read_srob_residue(self):
        structural = self.tp.get("structural") or {}
        res = structural.get("srob_residue")
        if res is not None:
            return res
        return structural.get("sob_residue") or {}

    # ----------------------------------------------------------
    # Surface helpers
    # ----------------------------------------------------------

    def _segments(self, smap):
        return list(smap.get("segments") or [])

    def _tag_ids(self, arr):
        ids = []
        for item in arr or []:
            if isinstance(item, dict):
                v = item.get("normalized") or item.get("verb")
                if v is None and item:
                    v = next(iter(item.values()))
                if v is not None:
                    ids.append(str(v))
            else:
                ids.append(str(item))
        return ids

    def _operators(self, smap):
        return self._tag_ids(smap.get("operators"))

    def _lexical_constraints(self, smap):
        return self._tag_ids(smap.get("lexical_constraints"))

    def _constraint_name_match(self, constraints, name):
        name = str(name).lower()
        for c in constraints:
            s = str(c).lower()
            if s == name or s.startswith(name + ".") or ("." + name) in s:
                return True
            # suffix after last dot
            if "." in s and s.split(".")[-1] == name:
                return True
            if s.split(".")[0] == name:
                return True
        return False

    def _modalities(self, smap):
        mods = []
        for seg in self._segments(smap):
            if isinstance(seg, dict) and seg.get("modality"):
                mods.append(str(seg["modality"]))
        return mods

    def _discourse_flags(self, smap):
        return list(smap.get("discourse_flags") or [])

    def _importance_labels_on_segments(self, smap):
        """Map label -> list of segment ids."""
        out = {}
        for seg in self._segments(smap):
            if not isinstance(seg, dict):
                continue
            sid = seg.get("id")
            labels = seg.get("structural_importance") or []
            if isinstance(labels, str):
                labels = [labels]
            for lab in labels:
                out.setdefault(str(lab), []).append(sid)
        return out

    # ----------------------------------------------------------
    # C1–C7
    # ----------------------------------------------------------

    def _encode_families(self, smap, srob_residue):
        families = {f"C{i}": [] for i in range(1, 8)}
        segments = self._segments(smap)
        nseg = len(segments)
        ops = self._operators(smap)
        constraints = self._lexical_constraints(smap)
        discourse = self._discourse_flags(smap)

        list_items = [
            s for s in segments if isinstance(s, dict) and s.get("type") == "list_item"
        ]
        list_with_parent = [
            s for s in list_items if s.get("parent_id") is not None
        ]
        any_id = any(isinstance(s, dict) and s.get("id") for s in segments)

        rule_book = (self.rules.get("constraint_rules") or {}).get("rules") or []

        def emit(family, rule_id, segment_ids=None, payload=None):
            entry = {
                "family": family,
                "rule_id": rule_id,
            }
            if segment_ids is not None:
                entry["segment_ids"] = list(segment_ids)
            if payload is not None:
                entry["payload"] = payload
            families[family].append(entry)
            self._family_decisions.append(f"{family}:{rule_id}")

        # Evaluate built-in v1 behaviors (mirror YAML)
        checks = {
            "c1_segment_exists": nseg >= 1,
            "c1_operator_present": len(ops) > 0,
            "c2_list_parent_child": len(list_with_parent) > 0,
            "c2_discourse_present": len(discourse) > 0,
            "c3_multi_segment_order": nseg >= 2,
            "c4_list_boundary": len(list_items) > 0,
            "c5_segment_id_lineage": any_id,
            "c6_multi_segment_change_surface": nseg >= 2,
            "c7_constraint_hint_present": len(constraints) > 0,
        }

        bind = {
            "c2_list_parent_child": [s.get("id") for s in list_with_parent],
            "c4_list_boundary": [s.get("id") for s in list_items],
        }

        payload_reason = {
            "c1_segment_exists": "segment_exists",
            "c1_operator_present": "operator_present",
            "c2_list_parent_child": "list_parent_child",
            "c2_discourse_present": "discourse_present",
            "c3_multi_segment_order": "multi_segment_order",
            "c4_list_boundary": "list_boundary",
            "c5_segment_id_lineage": "segment_id_lineage",
            "c6_multi_segment_change_surface": "multi_segment_surface",
            "c7_constraint_hint_present": "constraint_hint_present",
        }

        family_of = {
            "c1_segment_exists": "C1",
            "c1_operator_present": "C1",
            "c2_list_parent_child": "C2",
            "c2_discourse_present": "C2",
            "c3_multi_segment_order": "C3",
            "c4_list_boundary": "C4",
            "c5_segment_id_lineage": "C5",
            "c6_multi_segment_change_surface": "C6",
            "c7_constraint_hint_present": "C7",
        }

        for rid, ok in checks.items():
            if not ok:
                continue
            emit(
                family_of[rid],
                rid,
                segment_ids=bind.get(rid),
                payload={"reason": payload_reason[rid]},
            )

        # Prefer YAML rule ids if present (already mirrored)
        _ = rule_book
        return families

    # ----------------------------------------------------------
    # Gaps
    # ----------------------------------------------------------

    def _apply_gap_rules(self, smap, srob_residue):
        missing = []
        under = []
        ops = self._operators(smap)
        constraints = self._lexical_constraints(smap)
        miss_i = 1
        under_i = 1

        for seg in self._segments(smap):
            if not isinstance(seg, dict):
                continue
            text = seg.get("text")
            if text is None or str(text).strip() == "":
                sid = f"miss_{miss_i:03d}"
                miss_i += 1
                entry = {
                    "id": sid,
                    "kind": "missing_slot",
                    "rule_id": "miss_empty_text",
                    "segment_ids": [seg.get("id")],
                    "participants": [],
                    "note": "empty_text",
                }
                missing.append(entry)
                self._gap_decisions.append(f"missing_slot:{sid}")

        mods = self._modalities(smap)
        if "interrogative" in mods and len(ops) == 0:
            segs = [
                s.get("id")
                for s in self._segments(smap)
                if isinstance(s, dict) and s.get("modality") == "interrogative"
            ]
            sid = f"under_{under_i:03d}"
            under_i += 1
            under.append({
                "id": sid,
                "kind": "underspecification",
                "rule_id": "under_question_no_operator",
                "segment_ids": segs,
                "participants": [],
                "note": "question_without_operator",
            })
            self._gap_decisions.append(f"underspecification:{sid}")

        if len(constraints) > 0 and len(ops) == 0:
            # Avoid double-counting if already under_question; still emit distinct rule
            sid = f"under_{under_i:03d}"
            under_i += 1
            under.append({
                "id": sid,
                "kind": "underspecification",
                "rule_id": "under_constraint_no_operator",
                "segment_ids": [],
                "participants": [],
                "note": "constraint_without_operator",
            })
            self._gap_decisions.append(f"underspecification:{sid}")

        return missing, under

    # ----------------------------------------------------------
    # Conflicts
    # ----------------------------------------------------------

    def _apply_conflict_rules(self, smap, srob_residue):
        conflicts = []
        conf_i = 1
        constraints = self._lexical_constraints(smap)
        mods = set(self._modalities(smap))

        if self._constraint_name_match(constraints, "precision") and self._constraint_name_match(
            constraints, "conciseness"
        ):
            sid = f"conf_{conf_i:03d}"
            conf_i += 1
            conflicts.append({
                "id": sid,
                "kind": "conflict",
                "rule_id": "conf_precision_vs_conciseness",
                "segment_ids": [],
                "participants": ["precision", "conciseness"],
                "note": "precision_vs_conciseness",
            })
            self._conflict_decisions.append(sid)

        if "imperative" in mods and "interrogative" in mods:
            sid = f"conf_{conf_i:03d}"
            conf_i += 1
            conflicts.append({
                "id": sid,
                "kind": "conflict",
                "rule_id": "conf_imperative_vs_interrogative",
                "segment_ids": [],
                "participants": ["imperative", "interrogative"],
                "note": "imperative_vs_interrogative",
            })
            self._conflict_decisions.append(sid)

        return conflicts

    # ----------------------------------------------------------
    # Importance
    # ----------------------------------------------------------

    def _apply_importance(self, smap, missing, under, conflicts):
        items = []
        label_map = self._importance_labels_on_segments(smap)

        if "anchor_like" in label_map:
            items.append({
                "labels": ["constraint_anchor"],
                "segment_ids": list(label_map["anchor_like"]),
                "source": "structural",
            })
            self._importance_decisions.append("constraint_anchor")

        if "list_lead" in label_map:
            items.append({
                "labels": ["order_sensitive"],
                "segment_ids": list(label_map["list_lead"]),
                "source": "structural",
            })
            self._importance_decisions.append("order_sensitive")

        if missing:
            items.append({
                "labels": ["gap_high"],
                "segment_ids": [],
                "source": "gap",
            })
            self._importance_decisions.append("gap_high")

        if conflicts:
            items.append({
                "labels": ["conflict_high"],
                "segment_ids": [],
                "source": "conflict",
            })
            self._importance_decisions.append("conflict_high")

        return items

    # ----------------------------------------------------------
    # Build outputs
    # ----------------------------------------------------------

    def _build_constraint_map(self, families, missing, under, conflicts, importance, smap):
        discourse_constraints = []
        if self._discourse_flags(smap):
            discourse_constraints.append({
                "rule_id": "c2_discourse_present",
                "flags": list(self._discourse_flags(smap)),
            })

        return {
            "constraint_families": {
                "C1": families.get("C1", []),
                "C2": families.get("C2", []),
                "C3": families.get("C3", []),
                "C4": families.get("C4", []),
                "C5": families.get("C5", []),
                "C6": families.get("C6", []),
                "C7": families.get("C7", []),
            },
            "missing_slot_signals": list(missing),
            "underspecification_markers": list(under),
            "conflict_indicators": list(conflicts),
            "constraint_importance": list(importance),
            "discourse_constraints": discourse_constraints,
            "lineage_constraints": [],
            "routing_constraints": [],
            "policy_constraints": [],
        }

    def _build_residue(self, cnob_map, missing, under, conflicts, importance):
        fam = cnob_map.get("constraint_families") or {}
        summary = [k for k in ("C1", "C2", "C3", "C4", "C5", "C6", "C7") if fam.get(k)]

        residue_body = {
            "missing_slot_signals": list(missing),
            "underspecification_markers": list(under),
            "conflict_indicators": list(conflicts),
            "constraint_importance": list(importance),
            "constraint_family_summary": summary,
            "disagreement_flags": [],
            "override_flags": [],
        }
        residue_body["constraint_residue_hash"] = self._hash(
            {"map": cnob_map, "signals": residue_body}
        )
        return residue_body

    def _hash(self, obj):
        raw = yaml.dump(obj, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def _build_audit_record(self, cnob_map, residue):
        return {
            "support_yaml_load_status": self._load_status,
            "family_encoding_decisions": self._family_decisions[:64],
            "gap_decisions": self._gap_decisions[:32],
            "conflict_decisions": self._conflict_decisions[:32],
            "importance_decisions": self._importance_decisions[:32],
            "provenance_lineage": {
                "origin": "CnOB",
                "last_update": "CnOB",
            },
            "cnob_constraint_map_hash": self._hash(cnob_map),
            "constraint_residue_hash": residue.get("constraint_residue_hash"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

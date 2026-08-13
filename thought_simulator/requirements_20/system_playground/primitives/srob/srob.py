"""
SROB — Structural Refinement OB (Version 1.0)
Path-A post-SOB structural refinement primitive.

Responsibilities:
  1. Load SROB support YAMLs (not sob_*.yaml)
  2. Validate vocab coupling
  3. Read SOB map/residue from TP
  4. Normalize structure (lists/tables/blocks/boundaries); preserve segment ids (P1)
  5. Sharpen tags per multi_refinement_policy (P3) / unmapped_coarse (P4)
  6. Canonicalize discourse flags
  7. Apply structural-importance rules (multi-label OK — P5)
  8. Write full srob_structural_map + srob_residue + audit (P2)

Aligned with:
  - 20.40.020 v2.0
  - srob_software_architecture.md
  - srob_py_struc_pgm.md v1.1
  - srob_sob_comm_architect.md
"""

import os
import re
import copy
import yaml
import hashlib
from datetime import datetime, timezone

PRIMITIVE_NAME = "srob"


def get_primitive_name():
    return PRIMITIVE_NAME


class SROB:
    def __init__(self, tp_input):
        self.tp = copy.deepcopy(tp_input) if tp_input else {}
        self.rules = {}
        self._dir = os.path.dirname(__file__)
        self._sharpen_decisions = []
        self._normalize_decisions = []
        self._importance_decisions = []
        self._discourse_decisions = []
        self._vocab_status = "ok"

    # ----------------------------------------------------------
    # Public API
    # ----------------------------------------------------------

    def process(self):
        self._load_support_yamls()
        self._validate_vocab_coupling()

        sob_map = self._read_sob_map()
        sob_residue = self._read_sob_residue()

        units = self._normalize_structure(sob_map)
        units = self._resolve_boundaries(units)

        sharpened = self._sharpen_tags(sob_map, sob_residue)
        discourse = self._canonicalize_discourse(sob_residue)
        units = self._apply_importance(units, sob_residue)

        srob_map = self._build_structural_map(units, sharpened, discourse, sob_map)
        residue = self._build_residue(sharpened, discourse, sob_residue)
        audit = self._build_audit_record(srob_map, residue)

        self.tp.setdefault("structural", {})
        self.tp["structural"]["srob_structural_map"] = srob_map
        self.tp["structural"]["srob_residue"] = residue
        self.tp.setdefault("metadata", {})
        self.tp["metadata"]["srob_audit_record"] = audit

        return self.tp

    # ----------------------------------------------------------
    # Load + validate
    # ----------------------------------------------------------

    def _load_support_yamls(self):
        names = [
            "srob_normalize_rules.yaml",
            "srob_sharpen_maps.yaml",
            "srob_importance_rules.yaml",
        ]
        for name in names:
            path = os.path.join(self._dir, name)
            key = name.replace(".yaml", "").replace("srob_", "")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self.rules[key] = yaml.safe_load(f) or {}
            else:
                self.rules[key] = {}
                self._vocab_status = "partial"

    def _validate_vocab_coupling(self):
        """Illegal parent keys are a desync; empty maps are allowed."""
        sm = self.rules.get("sharpen_maps", {}) or {}
        # Soft validation: ensure fine ids nest under parent when present
        for family in ("operators", "domains", "tones", "constraints"):
            block = sm.get(family) or {}
            if not isinstance(block, dict):
                continue
            for parent, body in block.items():
                if parent in ("refinements",):
                    continue
                refs = (body or {}).get("refinements") if isinstance(body, dict) else []
                for r in refs or []:
                    rid = r.get("id") if isinstance(r, dict) else str(r)
                    if rid and not str(rid).startswith(str(parent) + "."):
                        self._vocab_status = "SROB_MAP_DESYNC"
                        return

    def _read_sob_map(self):
        return (self.tp.get("structural") or {}).get("sob_structural_map") or {}

    def _read_sob_residue(self):
        return (self.tp.get("structural") or {}).get("sob_residue") or {}

    # ----------------------------------------------------------
    # Structure normalization (P1: preserve ids)
    # ----------------------------------------------------------

    def _normalize_structure(self, sob_map):
        segments = copy.deepcopy(sob_map.get("segments") or [])
        units = []
        for seg in segments:
            u = {
                "id": seg.get("id"),
                "text": seg.get("text", ""),
                "type": seg.get("type", "sentence"),
                "modality": seg.get("modality", "declarative"),
            }
            # List geometry from text cues (SOB already typed list_item)
            if u["type"] == "list_item":
                text = u["text"] or ""
                # leading spaces on original-ish text for nested detection
                lead = len(text) - len(text.lstrip(" "))
                # also detect "  - " style
                if re.match(r"^\s{2,}", text):
                    u["depth"] = 2
                else:
                    u["depth"] = 1
                u["ordered"] = bool(re.match(r"^\s*\d+[.)]\s+", text))
                u["parent_id"] = None
                u["index_in_parent"] = 0
            units.append(u)
            self._normalize_decisions.append(f"keep:{u.get('id')}:{u.get('type')}")
        return units

    def _resolve_boundaries(self, units):
        """Assign parent_id / index_in_parent for list items."""
        # Track last depth-1 list item as potential parent of depth-2
        last_d1_id = None
        index_at_depth = {1: 0, 2: 0}
        for u in units:
            if u.get("type") != "list_item":
                continue
            depth = u.get("depth", 1)
            if depth <= 1:
                u["depth"] = 1
                u["parent_id"] = None
                u["index_in_parent"] = index_at_depth[1]
                index_at_depth[1] += 1
                index_at_depth[2] = 0
                last_d1_id = u.get("id")
            else:
                u["parent_id"] = last_d1_id
                u["index_in_parent"] = index_at_depth[2]
                index_at_depth[2] += 1
                self._normalize_decisions.append(
                    f"nest:{u.get('id')}→{last_d1_id}"
                )
        return units

    # ----------------------------------------------------------
    # Sharpen tags (P3 / P4)
    # ----------------------------------------------------------

    def _collect_coarse(self, sob_map, sob_residue, family_key, residue_key):
        """Collect ordered unique coarse ids from map arrays and residue tags."""
        ids = []
        seen = set()

        def add(x):
            if not x:
                return
            s = str(x)
            if s not in seen:
                seen.add(s)
                ids.append(s)

        arr = sob_map.get(family_key) or []
        for item in arr:
            if isinstance(item, dict):
                if "normalized" in item:
                    add(item["normalized"])
                elif "verb" in item:
                    add(item["verb"])
                else:
                    for v in item.values():
                        add(v)
                        break
            else:
                add(item)

        for tag in sob_residue.get("lexical_tags") or []:
            if isinstance(tag, dict) and residue_key in tag:
                add(tag[residue_key])

        return ids

    def _refine_one(self, family, coarse):
        """Apply P3/P4 for one coarse tag. Returns (primary_id, refined_bool, unmapped)."""
        sm = self.rules.get("sharpen_maps", {}) or {}
        block = (sm.get(family) or {}) if isinstance(sm.get(family), dict) else {}
        policy = (sm.get("vocab_coupling") or {}).get(
            "multi_refinement_policy", "pass_through_unless_single_child"
        )

        if coarse not in block:
            self._sharpen_decisions.append(f"unmapped:{family}:{coarse}")
            return coarse, False, True

        body = block.get(coarse) or {}
        refs = body.get("refinements") if isinstance(body, dict) else []
        ref_ids = []
        for r in refs or []:
            if isinstance(r, dict):
                rid = r.get("id")
                if rid:
                    ref_ids.append(str(rid))
            else:
                ref_ids.append(str(r))

        if not ref_ids:
            self._sharpen_decisions.append(f"pass_empty:{family}:{coarse}")
            return coarse, False, False

        if len(ref_ids) == 1:
            fine = ref_ids[0]
            self._sharpen_decisions.append(f"single:{family}:{coarse}→{fine}")
            return fine, True, False

        # multi-child, no when in v1 → pass-through (P3)
        self._sharpen_decisions.append(
            f"pass_multi:{family}:{coarse}:available={ref_ids}"
        )
        return coarse, False, False

    def _sharpen_tags(self, sob_map, sob_residue):
        result = {
            "operators": [],
            "lexical_domains": [],
            "lexical_tones": [],
            "lexical_constraints": [],
            "refined_tags": [],
            "pass_through_tags": [],
            "unmapped_coarse": [],
            "available_refinements": [],
        }

        families = [
            ("operators", "operators", "operator"),
            ("domains", "lexical_domains", "domain"),
            ("tones", "lexical_tones", "tone"),
            ("constraints", "lexical_constraints", "constraint"),
        ]

        for family, map_key, tag_key in families:
            coarses = self._collect_coarse(sob_map, sob_residue, map_key, tag_key)
            for coarse in coarses:
                primary, refined, unmapped = self._refine_one(family, coarse)
                out_key = {
                    "operators": "operators",
                    "domains": "lexical_domains",
                    "tones": "lexical_tones",
                    "constraints": "lexical_constraints",
                }[family]
                result[out_key].append(primary)
                if unmapped:
                    result["unmapped_coarse"].append({tag_key: coarse})
                    result["pass_through_tags"].append({tag_key: coarse})
                elif refined:
                    result["refined_tags"].append({tag_key: primary})
                else:
                    result["pass_through_tags"].append({tag_key: coarse})

        return result

    # ----------------------------------------------------------
    # Discourse
    # ----------------------------------------------------------

    def _canonicalize_discourse(self, sob_residue):
        norm = self.rules.get("normalize_rules", {}) or {}
        canon_map = (norm.get("discourse") or {}).get("canonicalize") or {}
        # invert aliases → canonical
        alias_to_canon = {}
        for canon, aliases in canon_map.items():
            for a in aliases or []:
                alias_to_canon[str(a).lower()] = canon
            alias_to_canon[str(canon).lower()] = canon

        flags = []
        seen = set()
        for item in sob_residue.get("structural_adjacent") or []:
            if not isinstance(item, dict):
                continue
            for k, v in item.items():
                if k in ("modality", "list_structure"):
                    continue
                if v is True or v is None or v == "":
                    key = k
                else:
                    key = k
                canon = alias_to_canon.get(str(key).lower(), key)
                if canon not in seen:
                    seen.add(canon)
                    flags.append(canon)
                    if canon != key:
                        self._discourse_decisions.append(f"{key}→{canon}")
        return flags

    # ----------------------------------------------------------
    # Importance (P5)
    # ----------------------------------------------------------

    def _apply_importance(self, units, sob_residue):
        imp = self.rules.get("importance_rules", {}) or {}
        rules = imp.get("rules") or []
        first_sentence_seen = False

        for u in units:
            labels = []
            stype = u.get("type")
            depth = u.get("depth")
            idx = u.get("index_in_parent")

            for rule in rules:
                rid = rule.get("id", "")
                cond = rule.get("if") or {}
                label = rule.get("label")
                if not label or label == "from_sob_coarse":
                    continue

                ok = True
                if "segment_type" in cond and cond["segment_type"] != stype:
                    ok = False
                if "segment_type_in" in cond and stype not in (cond["segment_type_in"] or []):
                    ok = False
                if "depth" in cond and depth != cond["depth"]:
                    ok = False
                if "index_in_parent" in cond and idx != cond["index_in_parent"]:
                    ok = False
                if cond.get("position") == "first":
                    if stype != "sentence" or first_sentence_seen:
                        # only first sentence unit overall
                        if stype == "sentence" and not first_sentence_seen:
                            pass
                        else:
                            ok = False
                    # handled below with tracking

                if cond.get("position") == "first" and stype == "sentence":
                    if first_sentence_seen:
                        ok = False

                if ok:
                    if label not in labels:
                        labels.append(label)
                        self._importance_decisions.append(f"{u.get('id')}:{label}")

            if stype == "sentence":
                first_sentence_seen = True

            if labels:
                u["structural_importance"] = labels

        return units

    # ----------------------------------------------------------
    # Build outputs
    # ----------------------------------------------------------

    def _build_structural_map(self, units, sharpened, discourse, sob_map):
        segments_out = []
        for u in units:
            seg = {
                "id": u.get("id"),
                "text": u.get("text", ""),
                "type": u.get("type", "sentence"),
                "modality": u.get("modality", "declarative"),
            }
            if u.get("type") == "list_item":
                seg["depth"] = u.get("depth", 1)
                seg["parent_id"] = u.get("parent_id")
                seg["index_in_parent"] = u.get("index_in_parent", 0)
                seg["ordered"] = bool(u.get("ordered", False))
            if u.get("structural_importance"):
                seg["structural_importance"] = u["structural_importance"]
            segments_out.append(seg)

        out = {
            "segments": segments_out,
            "operators": list(sharpened.get("operators") or []),
            "lexical_domains": list(sharpened.get("lexical_domains") or []),
            "lexical_tones": list(sharpened.get("lexical_tones") or []),
            "lexical_constraints": list(sharpened.get("lexical_constraints") or []),
            "discourse_flags": list(discourse or []),
        }

        if any(s.get("type") == "list_item" for s in segments_out):
            ordered = any(s.get("ordered") for s in segments_out if s.get("type") == "list_item")
            out["list_structure"] = {"ordered": ordered}

        return out

    def _build_residue(self, sharpened, discourse, sob_residue):
        structural_adjacent = []
        seen = set()
        for item in sob_residue.get("structural_adjacent") or []:
            if not isinstance(item, dict):
                continue
            # keep modality / list_structure; drop raw discourse keys (now on map)
            cleaned = {}
            for k, v in item.items():
                if k in ("modality", "list_structure"):
                    cleaned[k] = v
            if cleaned:
                key = tuple(sorted(cleaned.items()))
                if key not in seen:
                    seen.add(key)
                    structural_adjacent.append(cleaned)

        return {
            "refined_tags": list(sharpened.get("refined_tags") or []),
            "pass_through_tags": list(sharpened.get("pass_through_tags") or []),
            "structural_adjacent": structural_adjacent,
            "unmapped_coarse": list(sharpened.get("unmapped_coarse") or []),
            "disagreement_flags": [],
            "override_flags": [],
        }

    def _build_audit_record(self, srob_map, residue):
        def _hash(obj):
            raw = yaml.dump(obj, sort_keys=True)
            return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

        return {
            "support_yaml_load_status": "ok" if self._vocab_status != "partial" else "partial",
            "vocab_validation_status": self._vocab_status,
            "normalization_decisions": self._normalize_decisions[:32],
            "sharpen_decisions": self._sharpen_decisions[:32],
            "importance_decisions": self._importance_decisions[:32],
            "discourse_decisions": self._discourse_decisions[:32],
            "provenance_lineage": {
                "origin": "SROB",
                "last_update": "SROB",
            },
            "srob_structural_map_hash": _hash(srob_map),
            "srob_residue_hash": _hash(residue),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

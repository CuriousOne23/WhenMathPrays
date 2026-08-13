"""
SOB — Structural OB Layer (Version 1.0)
Path-A first structural classification primitive.

Responsibilities (exactly six):
  1. Load dictionaries
  2. Segment TP text
  3. Classify structural modality
  4. Extract structural-adjacent hints (operator / domain / tone / constraint)
  5. Form residue fragments
  6. Return structured TP + residue + audit

Aligned with:
  - 20.40.010_sob_prim.md
  - sob_software_architecture.md
  - sob_py_struc_pgm.md
  - progressive_lineup_testing.md v4.0
"""

import os
import re
import yaml
import hashlib
import copy
from datetime import datetime, timezone

PRIMITIVE_NAME = "sob"

def get_primitive_name():
    return PRIMITIVE_NAME


class SOB:
    def __init__(self, tp_input):
        self.tp = copy.deepcopy(tp_input) if tp_input else {}
        self.dicts = {}
        self._dict_dir = os.path.dirname(__file__)

    # ----------------------------------------------------------
    # Public API
    # ----------------------------------------------------------

    def process(self):
        self._load_dictionaries()
        text = self._get_text()
        segments = self._segment(text)
        normalized_segments = self._apply_morphology(segments)
        tagged = self._lexical_tag(normalized_segments)
        structural_map = self._build_structural_map(tagged)
        residue = self._build_residue(tagged)
        audit = self._build_audit_record(structural_map, residue)

        # Write only SOB-owned fields
        if "structural" not in self.tp:
            self.tp["structural"] = {}
        self.tp["structural"]["sob_structural_map"] = structural_map
        self.tp["structural"]["sob_residue"] = residue

        if "metadata" not in self.tp:
            self.tp["metadata"] = {}
        self.tp["metadata"]["sob_audit_record"] = audit

        return self.tp

    # ----------------------------------------------------------
    # Dictionary loading
    # ----------------------------------------------------------

    def _load_dictionaries(self):
        names = [
            "sob_dictionary.yaml",
            "sob_operators.yaml",
            "sob_markers.yaml",
            "sob_punctuation.yaml",
            "sob_domains.yaml",
            "sob_tones.yaml",
            "sob_constraints.yaml",
            "sob_morphology.yaml",
        ]
        for name in names:
            path = os.path.join(self._dict_dir, name)
            key = name.replace(".yaml", "").replace("sob_", "")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self.dicts[key] = yaml.safe_load(f) or {}
            else:
                self.dicts[key] = {}

    # ----------------------------------------------------------
    # Text extraction
    # ----------------------------------------------------------

    def _get_text(self):
        intake = self.tp.get("intake", {})
        if isinstance(intake, dict):
            return intake.get("text", "") or ""
        return str(intake) if intake else ""

    # ----------------------------------------------------------
    # Segmentation (order-preserving)
    # ----------------------------------------------------------

    def _segment(self, text):
        if not text.strip():
            return []

        lines = text.splitlines()
        segments = []
        seg_id = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Simple list-item detection
            if re.match(r"^[-*+]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
                segments.append({
                    "id": f"seg_{seg_id}",
                    "text": stripped,
                    "type": "list_item",
                    "raw": line,
                })
                seg_id += 1
                continue

            # Sentence-level split on . ! ?
            parts = re.split(r"(?<=[.!?])\s+", stripped)
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                segments.append({
                    "id": f"seg_{seg_id}",
                    "text": part,
                    "type": "sentence",
                    "raw": part,
                })
                seg_id += 1

        return segments

    # ----------------------------------------------------------
    # Morphology normalization
    # ----------------------------------------------------------

    def _apply_morphology(self, segments):
        morph = self.dicts.get("morphology", {})
        explicit = morph.get("explicit_map", {}) or {}
        suffix_rules = morph.get("suffix_rules", []) or []

        for seg in segments:
            tokens = re.findall(r"\b[\w'-]+\b", seg["text"].lower())
            normalized = []
            flags = []
            for tok in tokens:
                if tok in explicit:
                    base = explicit[tok]
                    flags.append(f"{tok}→{base}")
                    normalized.append(base)
                    continue
                base = tok
                for rule in suffix_rules:
                    suf = rule.get("suffix", "")
                    rep = rule.get("replacement", "")
                    if suf and base.endswith(suf) and len(base) > len(suf) + 1:
                        base = base[:-len(suf)] + rep
                        flags.append(f"{tok}→{base}")
                        break
                normalized.append(base)
            seg["tokens"] = tokens
            seg["normalized_tokens"] = normalized
            seg["morphology_flags"] = flags

        return segments

    # ----------------------------------------------------------
    # Lexical tagging + modality
    # ----------------------------------------------------------

    def _lexical_tag(self, segments):
        operators_dict = self.dicts.get("operators", {})
        domains_dict = self.dicts.get("domains", {})
        tones_dict = self.dicts.get("tones", {})
        constraints_dict = self.dicts.get("constraints", {})
        markers_dict = self.dicts.get("markers", {})

        # Flatten operator forms
        op_forms = {}
        for core in (operators_dict.get("operators") or {}).values():
            if isinstance(core, list):
                for form in core:
                    op_forms[form.lower()] = form.lower()
        for form in (operators_dict.get("additional") or []):
            op_forms[form.lower()] = form.lower()

        # Domain / tone / constraint marker sets
        domain_markers = {}
        for dom, forms in (domains_dict.get("domains") or {}).items():
            for f in (forms or []):
                domain_markers[str(f).lower()] = dom

        tone_markers = {}
        for tone, forms in (tones_dict.get("tones") or {}).items():
            for f in (forms or []):
                tone_markers[str(f).lower()] = tone

        constraint_markers = {}
        for c, forms in (constraints_dict.get("constraints") or {}).items():
            for f in (forms or []):
                constraint_markers[str(f).lower()] = c

        wh = set(m.lower() for m in (markers_dict.get("wh_markers") or []))
        cond = set(m.lower() for m in (markers_dict.get("conditional_markers") or []))

        for seg in segments:
            text_l = seg["text"].lower()
            toks = seg.get("normalized_tokens") or seg.get("tokens") or []

            # Modality
            modality = "declarative"
            if text_l.rstrip().endswith("?") or any(t in wh for t in toks[:3]):
                modality = "interrogative"
            elif any(t in cond for t in toks[:4]):
                modality = "conditional"
            elif text_l.startswith(("please ", "let's ", "let us ")) or \
                 (toks and toks[0] in op_forms and not text_l.rstrip().endswith("?")):
                modality = "imperative"
            seg["modality"] = modality

            # Operators
            ops = []
            for tok in toks:
                if tok in op_forms:
                    ops.append({
                        "verb": tok,
                        "normalized": op_forms[tok],
                        "source": "morphology" if tok in (seg.get("morphology_flags") or []) else "lexical"
                    })
            seg["operators"] = ops

            # Domains / tones / constraints (first match wins for simplicity)
            domains = []
            tones = []
            constraints = []
            for tok in toks:
                if tok in domain_markers and domain_markers[tok] not in domains:
                    domains.append(domain_markers[tok])
                if tok in tone_markers and tone_markers[tok] not in tones:
                    tones.append(tone_markers[tok])
                if tok in constraint_markers and constraint_markers[tok] not in constraints:
                    constraints.append(constraint_markers[tok])
            # Also scan multi-word / phrase markers lightly
            for phrase, dom in domain_markers.items():
                if " " in phrase and phrase in text_l and dom not in domains:
                    domains.append(dom)
            for phrase, tone in tone_markers.items():
                if " " in phrase and phrase in text_l and tone not in tones:
                    tones.append(tone)

            seg["lexical_domains"] = domains
            seg["lexical_tones"] = tones if tones else ["neutral"]
            seg["lexical_constraints"] = constraints

        return segments

    # ----------------------------------------------------------
    # Structural map & residue
    # ----------------------------------------------------------

    def _build_structural_map(self, tagged):
        segments_out = []
        all_ops = []
        all_domains = []
        all_tones = []
        all_constraints = []
        all_morph = []

        for seg in tagged:
            segments_out.append({
                "id": seg["id"],
                "text": seg["text"],
                "type": seg["type"],
                "modality": seg.get("modality", "declarative"),
            })
            all_ops.extend(seg.get("operators", []))
            for d in seg.get("lexical_domains", []):
                if d not in all_domains:
                    all_domains.append(d)
            for t in seg.get("lexical_tones", []):
                if t not in all_tones:
                    all_tones.append(t)
            for c in seg.get("lexical_constraints", []):
                if c not in all_constraints:
                    all_constraints.append(c)
            all_morph.extend(seg.get("morphology_flags", []))

        return {
            "segments": segments_out,
            "operators": all_ops,
            "lexical_domains": all_domains,
            "lexical_tones": all_tones,
            "lexical_constraints": all_constraints,
            "morphology_flags": all_morph,
        }

    def _build_residue(self, tagged):
        lexical_tags = []
        structural_adjacent = []
        seen_modalities = set()

        for seg in tagged:
            mod = seg.get("modality")
            if mod and mod not in seen_modalities:
                structural_adjacent.append({"modality": mod})
                seen_modalities.add(mod)
            for op in seg.get("operators", []):
                lexical_tags.append({"operator": op["normalized"]})
            for d in seg.get("lexical_domains", []):
                lexical_tags.append({"domain": d})
            for t in seg.get("lexical_tones", []):
                if t != "neutral":
                    lexical_tags.append({"tone": t})
            for c in seg.get("lexical_constraints", []):
                lexical_tags.append({"constraint": c})

        # Detect list structure
        if any(s.get("type") == "list_item" for s in tagged):
            structural_adjacent.append({"list_structure": "unordered"})

        return {
            "lexical_tags": lexical_tags,
            "structural_adjacent": structural_adjacent,
            "override_flags": [],
            "disagreement_flags": [],
        }

    def _build_audit_record(self, structural_map, residue):
        def _hash(obj):
            raw = yaml.dump(obj, sort_keys=True)
            return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

        return {
            "dictionary_load_status": "ok",
            "segmentation_decisions": [
                "multi_segment" if len(structural_map.get("segments", [])) > 1 else "single_sentence"
            ] + (["list_detected"] if any(
                s.get("type") == "list_item" for s in structural_map.get("segments", [])
            ) else []),
            "morphology_decisions": structural_map.get("morphology_flags", []),
            "lexical_tagging_decisions": [
                f"operator:{op['normalized']}" for op in structural_map.get("operators", [])
            ] + [
                f"domain:{d}" for d in structural_map.get("lexical_domains", [])
            ] + [
                f"tone:{t}" for t in structural_map.get("lexical_tones", []) if t != "neutral"
            ] + [
                f"constraint:{c}" for c in structural_map.get("lexical_constraints", [])
            ],
            "override_decisions": [],
            "disagreement_flags": [],
            "provenance_lineage": {
                "origin": "SOB",
                "last_update": "SOB",
            },
            "sob_structural_map_hash": _hash(structural_map),
            "sob_residue_hash": _hash(residue),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

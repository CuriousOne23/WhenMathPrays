"""
CE Primitive (Version 2.0)
Canonical Context Engine for Path-A.

Aligned with:
  - ce_py_struc_pgm.md (Version 2.0)
  - 20.108 (CE Envelope)
  - 20.108.010 (CE Candidate-Set)
  - 20.45 (ISc)
  - 20.107.030 (CEx-Pck)
  - 20.105.*, 20.15
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional

PRIMITIVE_NAME = "ce"


def get_primitive_name() -> str:
    return PRIMITIVE_NAME


class CE:
    """
    CE is a deterministic, bounded-context envelope constructor and
    candidate-set generator. It performs NO semantic inference and NO scoring.
    """

    def __init__(self, tp_input: Dict[str, Any]):
        self.tp = tp_input
        self.tp_in = copy.deepcopy(tp_input)

    def inspect(self) -> Dict[str, Any]:
        ctx = self.tp.get("metadata", {}).get("context", {}) or {}
        ctx_fields = ctx.get("context_fields", {}) or {}
        # Support already-flattened inputs (some progressive cases)
        if not ctx_fields and any(k in ctx for k in ("topic", "stance", "intent")):
            ctx_fields = {
                k: ctx.get(k)
                for k in (
                    "topic", "stance", "intent", "register", "politeness", "tone",
                    "continuity", "direction", "coherence", "importance",
                    "clarifying_fields",
                )
                if k in ctx
            }

        flags = {
            "relevance": ctx.get("relevance_flags", {}) or {},
            "copy_forward": ctx.get("copy_forward_flags", {}) or {},
            "reset": ctx.get("reset_flags", {}) or {},
        }

        msl = self.tp.get("metadata", {}).get("msl", {}) or {}
        next_ctx = self.tp.get("metadata", {}).get("next_context", {}) or {}

        semantic_importance = (
            self.tp.get("semantic", {}) or {}
        ).get("importance", {}) or {}
        norm_meta = (
            self.tp.get("metadata", {}) or {}
        ).get("normalization_metadata", {}) or {}
        sem_layer = (
            self.tp.get("metadata", {}) or {}
        ).get("semantic_layer_metadata", {}) or {}
        residue = (
            self.tp.get("metadata", {}) or {}
        ).get("residue", {}) or {}

        normalized = self._normalize_context(ctx_fields, msl, next_ctx, flags)
        audit = self._build_extraction_audit(normalized, msl, next_ctx, flags)

        candidates = self._build_candidate_set(
            semantic_importance=semantic_importance,
            norm_meta=norm_meta,
            sem_layer=sem_layer,
            residue=residue,
            normalized=normalized,
            next_ctx=next_ctx,
        )
        candidates = self._order_candidates(candidates)

        self._update_tp(normalized, audit, candidates)
        return self.tp

    # ------------------------------------------------------------------
    # Classic context normalization
    # ------------------------------------------------------------------
    def _normalize_context(self, ctx_fields, msl, next_ctx, flags):
        normalized: Dict[str, Any] = {}

        for field in [
            "topic", "stance", "intent", "register", "politeness",
            "tone", "continuity", "direction", "coherence",
            "importance", "clarifying_fields",
        ]:
            normalized[field] = ctx_fields.get(field)

        if "stance" in msl and msl["stance"] is not None:
            normalized["stance"] = msl["stance"]
        if "direction" in msl and msl["direction"] is not None:
            normalized["direction"] = msl["direction"]
        if "coherence" in msl and msl["coherence"] is not None:
            normalized["coherence"] = msl["coherence"]

        continuity = ctx_fields.get("continuity")
        if continuity in ["none", "weak", "moderate", "strong"]:
            normalized["continuity"] = continuity

        normalized["clarifying_fields"] = list(
            ctx_fields.get("clarifying_fields", []) or []
        )

        if flags["copy_forward"].get("topic"):
            normalized["topic"] = ctx_fields.get("topic")
        if flags["copy_forward"].get("direction"):
            normalized["direction"] = ctx_fields.get("direction")
        if flags["copy_forward"].get("coherence"):
            normalized["coherence"] = ctx_fields.get("coherence")

        for field, should_reset in (flags.get("reset") or {}).items():
            if should_reset:
                normalized[field] = None

        return normalized

    def _build_extraction_audit(self, normalized, msl, next_ctx, flags):
        continuity = normalized.get("continuity")
        if continuity not in ["none", "weak", "moderate", "strong"]:
            continuity_validation = "invalid"
        else:
            continuity_validation = continuity

        importance = normalized.get("importance")
        if importance not in ["low", "normal", "high"]:
            importance_validation = "normal"
        else:
            importance_validation = importance

        clarifying_validation = normalized.get("clarifying_fields", [])
        if not isinstance(clarifying_validation, list):
            clarifying_validation = []

        return {
            "normalized_fields": [
                "topic", "stance", "intent", "direction", "coherence"
            ],
            "msl_reconciliation": {
                "stance": normalized.get("stance"),
                "direction": normalized.get("direction"),
                "coherence": normalized.get("coherence"),
            },
            "continuity_validation": continuity_validation,
            "importance_validation": importance_validation,
            "clarifying_validation": clarifying_validation,
        }

    # ------------------------------------------------------------------
    # Candidate set (20.108.010)
    # ------------------------------------------------------------------
    def _build_candidate_set(
        self,
        semantic_importance: Dict[str, Any],
        norm_meta: Dict[str, Any],
        sem_layer: Dict[str, Any],
        residue: Dict[str, Any],
        normalized: Dict[str, Any],
        next_ctx: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        entities = list(semantic_importance.get("entities") or [])
        candidates: List[Dict[str, Any]] = []

        if not entities:
            candidates.append(
                self._make_candidate(
                    candidate_id=0,
                    entity=None,
                    norm_meta=norm_meta,
                    sem_layer=sem_layer,
                    residue=residue,
                    normalized=normalized,
                    next_ctx=next_ctx,
                    note="default_interpretation",
                )
            )
            return candidates

        for idx, entity in enumerate(entities):
            candidates.append(
                self._make_candidate(
                    candidate_id=idx,
                    entity=entity,
                    norm_meta=norm_meta,
                    sem_layer=sem_layer,
                    residue=residue,
                    normalized=normalized,
                    next_ctx=next_ctx,
                    note="entity_primary",
                )
            )

        return candidates

    def _make_candidate(
        self,
        candidate_id: int,
        entity: Optional[Dict[str, Any]],
        norm_meta: Dict[str, Any],
        sem_layer: Dict[str, Any],
        residue: Dict[str, Any],
        normalized: Dict[str, Any],
        next_ctx: Dict[str, Any],
        note: str,
    ) -> Dict[str, Any]:
        tokens = norm_meta.get("normalized_tokens") or []
        surface = None
        lemma = None
        if tokens and isinstance(tokens, list) and isinstance(tokens[0], dict):
            surface = tokens[0].get("surface")
            lemma = tokens[0].get("lemma")

        if entity and isinstance(entity, dict):
            # Prefer entity value as surface when no token surface available
            if surface is None:
                surface = entity.get("value")
            if lemma is None:
                lemma = entity.get("value")

        cues = (sem_layer.get("modality_stance_cues") or {}) if isinstance(sem_layer, dict) else {}
        expression = cues.get("expression")
        intent = cues.get("intent")
        if intent is None:
            intent = normalized.get("intent")

        fftm_fields = {
            "token_surface": surface if surface is not None else "",
            "token_base": lemma if lemma is not None else "",
            "token_expression": expression if expression is not None else "",
            "token_intent": intent if intent is not None else "",
        }

        # Deterministic placeholder structural IDs (0.0 fallback when unknown).
        # Real numeric encodings arrive via WrdNm in the full pipeline.
        structural_features = {
            "surface_id": 0.0,
            "lemma_id": 0.0,
            "expression_id": 0.0,
            "ordering_id": float(candidate_id),
            "constraint_family_id": 0.0,
            "next_context_id": 0.0,
        }

        ccr = ((self.tp.get("cex") or {}).get("ccr") or {})
        semantic_residue = (
            (self.tp.get("metadata") or {}).get("semantic_residue")
            or ccr.get("alignment", {}).get("semantic_residue")
            or "none"
        )
        structural_residue = residue.get("structural_residue") or "none"

        semantic_adjacent_features = {
            "semantic_residue": semantic_residue,
            "structural_residue": structural_residue,
        }

        next_context_block = {
            "topic": next_ctx.get("next_context") or normalized.get("topic"),
            "stance": next_ctx.get("stance") or normalized.get("stance"),
            "intent": normalized.get("intent"),
            "direction": next_ctx.get("direction") or normalized.get("direction"),
            "coherence": next_ctx.get("coherence") or normalized.get("coherence"),
            "importance": normalized.get("importance"),
        }

        provenance = {
            "origin": "CE",
            "last_update": "CE",
            "note": note,
            "entity_value": (entity or {}).get("value") if entity else None,
            "entity_role": (entity or {}).get("role") if entity else None,
        }

        return {
            "candidate_id": candidate_id,
            "fftm_fields": fftm_fields,
            "structural_features": structural_features,
            "semantic_adjacent_features": semantic_adjacent_features,
            "next_context": next_context_block,
            "provenance": provenance,
        }

    def _order_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        def key_fn(c: Dict[str, Any]):
            cid = c.get("candidate_id", 0)
            oid = (c.get("structural_features") or {}).get("ordering_id", 0.0)
            surface = (c.get("fftm_fields") or {}).get("token_surface", "") or ""
            return (cid, oid, surface)

        return sorted(candidates, key=key_fn)

    # ------------------------------------------------------------------
    # Write envelopes
    # ------------------------------------------------------------------
    def _update_tp(self, normalized, audit, candidates):
        ctx = self.tp.setdefault("metadata", {}).setdefault("context", {})

        for k, v in normalized.items():
            ctx[k] = v

        in_ctx = (self.tp_in.get("metadata") or {}).get("context") or {}
        ctx["relevance_flags"] = in_ctx.get("relevance_flags", {}) or {}
        ctx["copy_forward_flags"] = in_ctx.get("copy_forward_flags", {}) or {}
        ctx["reset_flags"] = in_ctx.get("reset_flags", {}) or {}

        ctx["extraction_audit"] = audit
        ctx["context_provenance"] = {
            "origin": "CE",
            "last_update": "CE",
            "commit_lineage": self._extend_commit_lineage(),
        }
        # Keep CE_v1.0 for compatibility with existing classic expected blocks;
        # structural program documents CE_v2.0 as the logical version of the
        # dual-envelope CE. Tests that assert the tag use the value written here.
        ctx["ce_version_tag"] = "CE_v1.0"

        if "context_fields" in ctx:
            del ctx["context_fields"]

        ce_block = self.tp.setdefault("ce", {})
        ce_block["candidate_set"] = candidates

    def _extend_commit_lineage(self):
        prov_in = (
            (self.tp_in.get("metadata") or {})
            .get("context", {})
            .get("context_provenance", {})
            or {}
        )
        lineage = copy.deepcopy(prov_in.get("commit_lineage", []) or [])
        lineage.append("c003")
        return lineage

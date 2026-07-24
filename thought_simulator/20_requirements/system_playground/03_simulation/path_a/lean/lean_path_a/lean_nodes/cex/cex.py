"""
CEx — Context Extractor (lean node)

This module implements a lightweight, deterministic CEx primitive for the
system_playground Path A lean pipeline.

It consumes a CILIntakePacket (as defined in the CIL system_playground module)
and produces a CE envelope compatible with TP.metadata.context_metadata and
the cex_reference.yaml boundary specification.

CEx responsibilities (lean version):
- Consume CILIntakePacket as the sole admissible input.
- Select an identity-layer context deterministically.
- Extract and normalize clarifying fields (placeholder in lean version).
- Reflect structural hints, referent mappings, register_hint.
- Reflect next-turn context fields (if provided).
- Populate context_provenance, continuity_status, and extraction_audit.
- Produce a bounded, replayable CE envelope as a plain dict.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# CE Data Structures (lean, schema-aligned with cex_reference.yaml)
# ---------------------------------------------------------------------------

@dataclass
class IdentityLayerContext:
    primary_layer_id: Optional[str]
    ordering_metrics: Dict[str, Any]
    continuity_status: str


@dataclass
class ClarifyingFieldEntry:
    name: str
    subfields: List[Dict[str, Any]] = field(default_factory=list)
    importance: Optional[float] = None
    provenance: Optional[Dict[str, Any]] = None


@dataclass
class ContextFields:
    identity_layer_context: IdentityLayerContext
    clarifying_fields: List[ClarifyingFieldEntry]
    structural_hints: Dict[str, Any]
    referent_mapping: Dict[str, Any]
    register_hint: Optional[str]
    next_context_fields: Dict[str, Any]


@dataclass
class ContextProvenance:
    source: str
    turn_index: int
    packet_metadata: Dict[str, Any]
    lineage_stability: List[Any]


@dataclass
class ExtractionAuditEntry:
    kind: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CEEnvelope:
    relevance_flags: Dict[str, bool]
    copy_forward_flags: Dict[str, bool]
    reset_flags: Dict[str, bool]
    context_fields: ContextFields
    context_provenance: ContextProvenance
    extraction_audit: List[ExtractionAuditEntry]
    continuity_status: str


# ---------------------------------------------------------------------------
# CEx Implementation (lean)
# ---------------------------------------------------------------------------

class CEx:
    """
    Lean CEx implementation.

    Input:  CILIntakePacket-like dict or object with attributes:
            - identity_selection_block
            - referent_certainty_block
            - stability_block
            - lineage_block
            - ordering_block
            - cst_block
            - packet_metadata

    Output: CEEnvelope as a plain dict suitable for TP.metadata.context_metadata.
    """

    def __init__(self):
        # No internal state; CEx is purely functional in lean mode.
        pass

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def run(self, cil_packet: Any, next_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main CEx execution for lean Path A.

        - cil_packet: CILIntakePacket or dict with the expected fields.
        - next_context: optional dict of next-turn context fields
                        (topic, stance, intent, register, politeness,
                         epistemic_shading, continuity, direction, coherence,
                         shift_required, importance).

        Returns:
            CEEnvelope serialized as a dict.
        """
        # Normalize input to dict-like access
        pkt = self._as_dict(cil_packet)

        identity_ctx, continuity_status = self._select_identity(pkt)
        clarifying_fields, clarifying_audit = self._extract_clarifying_fields(pkt)
        structural_hints = self._extract_structural_hints(pkt)
        referent_mapping = self._extract_referent_mapping(pkt)
        register_hint = self._extract_register_hint(pkt)
        next_ctx_fields = next_context or {}

        context_fields = ContextFields(
            identity_layer_context=identity_ctx,
            clarifying_fields=clarifying_fields,
            structural_hints=structural_hints,
            referent_mapping=referent_mapping,
            register_hint=register_hint,
            next_context_fields=next_ctx_fields,
        )

        provenance = self._build_provenance(pkt)
        audit_entries = clarifying_audit

        ce = CEEnvelope(
            relevance_flags=self._default_relevance_flags(context_fields),
            copy_forward_flags=self._default_copy_forward_flags(context_fields),
            reset_flags=self._default_reset_flags(pkt),
            context_fields=context_fields,
            context_provenance=provenance,
            extraction_audit=audit_entries,
            continuity_status=continuity_status,
        )

        # Return as plain dict for TP.metadata.context_metadata
        return self._serialize_ce(ce)

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _as_dict(self, cil_packet: Any) -> Dict[str, Any]:
        """Support both dataclass-like objects and plain dicts."""
        if isinstance(cil_packet, dict):
            return cil_packet
        return {
            "identity_selection_block": getattr(cil_packet, "identity_selection_block", []),
            "referent_certainty_block": getattr(cil_packet, "referent_certainty_block", {}),
            "stability_block": getattr(cil_packet, "stability_block", {}),
            "lineage_block": getattr(cil_packet, "lineage_block", {}),
            "ordering_block": getattr(cil_packet, "ordering_block", {}),
            "cst_block": getattr(cil_packet, "cst_block", {}),
            "packet_metadata": getattr(cil_packet, "packet_metadata", {}),
        }

    def _select_identity(self, pkt: Dict[str, Any]) -> (IdentityLayerContext, str):
        """
        Deterministic identity-layer selection.

        Lean rule: choose the first identity in identity_selection_block.
        Continuity_status:
          - "reset_required" if packet_metadata.new_context_required is True
          - "stable" otherwise
        """
        identities = pkt.get("identity_selection_block", [])
        primary = identities[0] if identities else {}

        primary_id = primary.get("id")
        ordering_metrics = primary.get("ordering_metrics", {})

        new_context_required = bool(
            pkt.get("packet_metadata", {}).get("new_context_required", False)
        )
        continuity_status = "reset_required" if new_context_required else "stable"

        identity_ctx = IdentityLayerContext(
            primary_layer_id=primary_id,
            ordering_metrics=ordering_metrics,
            continuity_status=continuity_status,
        )
        return identity_ctx, continuity_status

    def _extract_clarifying_fields(
        self, pkt: Dict[str, Any]
    ) -> (List[ClarifyingFieldEntry], List[ExtractionAuditEntry]):
        """
        Lean clarifying-field extraction.

        For now, this is a placeholder: no actual clarifying_fields are present
        in the CILIntakePacket used by system_playground. We return an empty list
        and no audit entries, but keep the structure ready for future expansion.
        """
        clarifying_fields: List[ClarifyingFieldEntry] = []
        audit: List[ExtractionAuditEntry] = []

        # If future CILIntakePacket adds clarifying_fields, enforce bounded limits here.

        return clarifying_fields, audit

    def _extract_structural_hints(self, pkt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structural hints from ordering_block and stability_block.

        Lean version: expose ordering metrics and a summary of stability.
        """
        ordering = pkt.get("ordering_block", {})
        stability = pkt.get("stability_block", {})

        return {
            "ordering": ordering,
            "stability_summary": {
                "has_drift": bool(stability.get("drift")),
                "has_collapse": bool(stability.get("collapse")),
            },
        }

    def _extract_referent_mapping(self, pkt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Referent mapping from the selected identity object.

        Lean rule: use referent_map from the first identity in identity_selection_block.
        """
        identities = pkt.get("identity_selection_block", [])
        primary = identities[0] if identities else {}
        return primary.get("referent_map", {})

    def _extract_register_hint(self, pkt: Dict[str, Any]) -> Optional[str]:
        """
        Register hint.

        Lean version: if CIL or CST metadata exposes a register_hint, reflect it.
        Otherwise, return None.
        """
        meta = pkt.get("packet_metadata", {})
        cst_meta = pkt.get("cst_block", {}).get("metadata", {})
        return meta.get("register_hint") or cst_meta.get("register_hint")

    def _build_provenance(self, pkt: Dict[str, Any]) -> ContextProvenance:
        """
        Build context_provenance from packet_metadata and lineage_block.
        """
        meta = pkt.get("packet_metadata", {})
        lineage = pkt.get("lineage_block", {})
        turn_index = int(meta.get("turn_index", 0))

        return ContextProvenance(
            source="CIL",
            turn_index=turn_index,
            packet_metadata=meta,
            lineage_stability=lineage.get("lineage_stability", []),
        )

    def _default_relevance_flags(self, context_fields: ContextFields) -> Dict[str, bool]:
        """
        Simple relevance flags: mark all major components as relevant.
        """
        return {
            "identity_layer_context": True,
            "clarifying_fields": bool(context_fields.clarifying_fields),
            "structural_hints": True,
            "referent_mapping": bool(context_fields.referent_mapping),
            "register_hint": context_fields.register_hint is not None,
            "next_context_fields": bool(context_fields.next_context_fields),
        }

    def _default_copy_forward_flags(self, context_fields: ContextFields) -> Dict[str, bool]:
        """
        Simple copy-forward discipline: identity and clarifying fields may be
        copied forward; next-turn context is per-turn only.
        """
        return {
            "identity_layer_context": True,
            "clarifying_fields": True,
            "structural_hints": True,
            "referent_mapping": True,
            "register_hint": True,
            "next_context_fields": False,
        }

    def _default_reset_flags(self, pkt: Dict[str, Any]) -> Dict[str, bool]:
        """
        Reset flags based on new_context_required.
        """
        new_context_required = bool(
            pkt.get("packet_metadata", {}).get("new_context_required", False)
        )
        return {
            "identity_layer_context": new_context_required,
            "clarifying_fields": new_context_required,
            "structural_hints": new_context_required,
            "referent_mapping": new_context_required,
            "register_hint": new_context_required,
            "next_context_fields": new_context_required,
        }

    def _serialize_ce(self, ce: CEEnvelope) -> Dict[str, Any]:
        """
        Convert CEEnvelope dataclass into a plain dict for TP.metadata.context_metadata.
        """
        return {
            "relevance_flags": ce.relevance_flags,
            "copy_forward_flags": ce.copy_forward_flags,
            "reset_flags": ce.reset_flags,
            "context_fields": {
                "identity_layer_context": {
                    "primary_layer_id": ce.context_fields.identity_layer_context.primary_layer_id,
                    "ordering_metrics": ce.context_fields.identity_layer_context.ordering_metrics,
                    "continuity_status": ce.context_fields.identity_layer_context.continuity_status,
                },
                "clarifying_fields": [
                    {
                        "name": cf.name,
                        "subfields": cf.subfields,
                        "importance": cf.importance,
                        "provenance": cf.provenance,
                    }
                    for cf in ce.context_fields.clarifying_fields
                ],
                "structural_hints": ce.context_fields.structural_hints,
                "referent_mapping": ce.context_fields.referent_mapping,
                "register_hint": ce.context_fields.register_hint,
                "next_context_fields": ce.context_fields.next_context_fields,
            },
            "context_provenance": {
                "source": ce.context_provenance.source,
                "turn_index": ce.context_provenance.turn_index,
                "packet_metadata": ce.context_provenance.packet_metadata,
                "lineage_stability": ce.context_provenance.lineage_stability,
            },
            "extraction_audit": [
                {
                    "kind": entry.kind,
                    "message": entry.message,
                    "details": entry.details,
                }
                for entry in ce.extraction_audit
            ],
            "continuity_status": ce.continuity_status,
        }


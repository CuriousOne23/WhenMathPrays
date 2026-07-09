# path_a_boundary_reference.md

**Document ID:** 20.XXX_path_a_boundary_reference  
**Version:** 0.1  
**Date:** 2026-07-09  
**Status:** Draft — Reference Paper (Path A)  
**Purpose:** Define the Path A boundary conditions, envelope geometry, surface normalization, token/tag structure, correction_context geometry, field allowances, forbidden fields, expansion rules, and testing requirements for the covered primitives.

---

## 1. Purpose & Scope

This document establishes the canonical boundary and envelope specifications for the Path A primitives InB, IIInB, IE, CEx, CE, TPU, and IMR. It defines the required input states, postcondition invariants, transition guards, residue propagation rules, and error envelopes that ensure deterministic, replay-safe behavior.

---

## 2. Boundary Domain Overview

The boundary domain encompasses upstream intake, normalization, context extraction, commitment, and mismatch resolution stages. All operations maintain bounded size, deterministic canonicalization, provenance tracking, and strict separation of structural concerns.

---

## 3. Canonical Envelope Geometry

The canonical envelope maintains a fixed shape across primitives. It consists of transport metadata, payload, repairs metadata, structural tags, and provenance fields. Envelope evolution follows deterministic functions.

$$
\text{Envelope}_{n+1} = f_{\text{det}}(\text{Envelope}_n, \text{Input}, \text{Profile})
$$

---

## 4. Surface Normalization Rules

Surface normalization applies deterministic canonicalization of encoding, punctuation, and shorthand expansions. Repairs attach metadata without semantic inference.

**HLR-PA-BND-001:** Surface normalization preserves original order and meaning.  
**HLR-PA-BND-002:** Surface normalization attaches repair metadata to the envelope.

---

## 5. Token & Tag Structure

Tokens carry surface form, lexical tags, and structural hints. Tags are bounded and deterministic. No semantic tags appear in upstream envelopes.

**HLR-PA-BND-003:** Token structure includes surface form, lexical attributes, and structural tags.  
**HLR-PA-BND-004:** Tag sets remain pre-semantic and bounded.

---

## 6. Correction_Context Geometry

Correction_context carries explicit target_field_ids, mismatch type, and bounded depth/cooldown metadata. It enables deterministic re-interpretation within allowed basins.

**HLR-PA-BND-005:** Correction_context geometry is bounded and carries explicit target identifiers.  
**HLR-PA-BND-006:** Correction_context preserves replay equivalence when artifacts are stripped.

---

## 7. Field Allowance Table

| Primitive | Allowed Fields |
|-----------|----------------|
| InB | transport_metadata, raw_payload, provenance |
| IIInB | normalized_surface, repairs_metadata, provenance |
| IE | tokens, lexical_tags, structural_tags, envelope_metadata, provenance |
| CEx | context_hypotheses, expansion_metadata, provenance |
| CE | selected_context, confidence_scores, provenance |
| TPU | committed_tp_snapshot, authority_metadata, provenance |
| IMR | correction_context, mismatch_type, target_field_ids, provenance |

---

## 8. Forbidden Field Table

| Primitive | Forbidden Fields |
|-----------|------------------|
| InB | semantic_tags, meaning_fields |
| IIInB | semantic_inference, reordered_payload |
| IE | semantic_tags, meaning_fields |
| CEx | semantic_inference, meaning_fields |
| CE | semantic_inference, meaning_fields |
| TPU | semantic_inference, meaning_fields |
| IMR | structural_geometry_modification_outside_allowed_scope, meaning_fields_outside_correction_context |

---

## 9. Expansion Rules

Expansion produces finite candidate sets. All expansions attach metadata and remain deterministic.

**HLR-PA-BND-007:** Expansion rules produce finite, allowlisted candidate sets.  
**HLR-PA-BND-008:** Expansion attaches provenance and repair metadata.

---

## 10. Testing Requirements

Testing includes replay fixtures, boundary cases, malformed inputs, clean/corrected paths, and envelope invariant assertions.

**HLR-PA-BND-009:** All boundary tests verify determinism and replay equivalence.  
**HLR-PA-BND-010:** Envelope shape and field allowance tests are mandatory at each primitive handoff.

---

## 11. Canonical Starter Reference File

```markdown
# Canonical Path A Envelope Starter
envelope_version: "1.0"
transport_metadata: {...}
raw_payload: "..."
provenance: {timestamp, source_id, ...}
repairs_metadata: []
structural_tags: []
```

---

## 12. HLR Traceability Matrix

| HLR ID | Section | Description |
|--------|---------|-------------|
| HLR-PA-BND-001 | 4 | Surface normalization preserves order and meaning |
| HLR-PA-BND-002 | 4 | Surface normalization attaches repair metadata |
| HLR-PA-BND-003 | 5 | Token structure includes surface form and tags |
| HLR-PA-BND-004 | 5 | Tag sets remain pre-semantic and bounded |
| HLR-PA-BND-005 | 6 | Correction_context is bounded with explicit targets |
| HLR-PA-BND-006 | 6 | Correction_context preserves replay equivalence |
| HLR-PA-BND-007 | 9 | Expansion produces finite candidate sets |
| HLR-PA-BND-008 | 9 | Expansion attaches provenance metadata |
| HLR-PA-BND-009 | 10 | Boundary tests verify determinism and replay |
| HLR-PA-BND-010 | 10 | Envelope shape tests are mandatory |

**End of path_a_boundary_reference.md**
```

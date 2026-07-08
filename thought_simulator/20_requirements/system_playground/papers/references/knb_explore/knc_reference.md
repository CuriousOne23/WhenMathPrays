# knc_reference.md

**Title:** KnC — Coarse Grounding Tier Reference  
**Document ID:** Future-HLR  
**Version:** 0.3 (Pre-work — Exploratory)  
**Date:** 2026-07-07  
**Status:** Draft — Playground Reference  
**Purpose:** Define the Coarse grounding tier (KnC) within the KnB pipeline.

---

## 1. Tier Definition

KnC is the **high-entropy, safe fallback** grounding tier.

It produces broad, lexical, and categorical anchors that are stable across manifold basins but do not commit to fine identity or relational geometry.

**KnC is not**: contextual disambiguation, fine identity resolution, relational refinement, or conflict resolution.

**Design Rationale**: KnC exists to provide stable, low-commitment anchors that prevent over-resolution and ensure grounding robustness in early turns or ambiguous contexts.

---

## 2. Inputs

KnC reads:
- LI meaning commitments (proposition fragments, semantic tags)
- CoHI continuity_fields (referential history, conversation objects)
- SSR context from previous turn
- Basic manifold hints (identity and relational basin signals)

**KnC does not read** deep manifold geometry (shapes, relational curvature).

---

## 3. Outputs (Tier-Specific Fields)

KnC writes its own distinct coarse fields. Each field is a structured object.

### 3.1 Field Schemas

**identity_coarse[]**:
```markdown
[
  {
    "text": "a dataset",
    "category": "data_object",
    "entropy": 0.78,
    "provenance": "LI/SSR",
    "kn_dt_ref": ["kndt:category_784"],
    "confidence": "coarse"
  }
]
```

**relation_coarse[]**:
```markdown
[
  {
    "text": "related_to",
    "category": "generic_relation",
    "entropy": 0.81,
    "provenance": "LI/SSR",
    "kn_dt_ref": ["kndt:relation_generic"],
    "confidence": "coarse"
  }
]
```

Similar structured objects for:
- `domain_anchor_coarse[]`
- `qualifier_coarse[]`
- `truth_validation_coarse[]`

Supporting fields: `H_Kn_coarse`, `Kn_level = "KnC"`, `escalation_flag`, `conflict_flag`

---

## 4. Resolution Rules

KnC performs **minimal resolution**:
- Lexical and categorical matching only
- Preserves ambiguity when context is weak
- Escalates to KnM when entropy drops or strong context is present

**Explicit prohibitions**:
- No pronoun resolution
- No relational disambiguation
- No domain-specific anchoring
- No temporal or spatial resolution
- No identity merging
- No conflict resolution

---

## 5. Entropy Thresholds

KnC operates in the **high entropy band** (example: $H \geq 0.65$).

### 5.1 Entropy Components
KnC uses:
- Lexical entropy
- Minimal contextual entropy
- Basic evidential entropy

**Escalation Rule**: Escalation occurs when $H < H_{\text{KnC_threshold}}$ OR contextual_evidence ≥ contextual_threshold.

---

## 6. Examples

**Example 1 — Ambiguous Noun Phrase**  
Input: vague reference to "the dataset"  
KnC output: `identity_coarse`: "a dataset" (broad categorical anchor)

**Example 2 — Ambiguous Relation**  
Input: unclear relation "linked to"  
KnC output: `relation_coarse`: "related_to" (preserves ambiguity)

**Example 3 — Escalation**  
Input: strong context + low entropy  
KnC detects condition → sets `escalation_flag` for KnM

---

## 7. Failure Modes

- Insufficient grounding → escalate to KnM or flag for clarification
- High residual ambiguity → preserve and flag
- KnC must not attempt to repair contradictions; it only flags them.

---

## 8. Invariants

- Determinism and replay safety
- Non-mutation of SSR
- SSR and manifold compatibility
- Feeds cleanly into LI mapping library
- Monotonicity with higher tiers: KnC fields remain frozen and visible to KnM/KnF; higher tiers add refinement fields but do not delete or overwrite coarse fields.

---

**Downstream Use**: LI uses KnC fields as fallback anchors when KnM/KnF do not produce sufficient refinement.

---

*End of knc_reference.md (Revised Draft)*

---

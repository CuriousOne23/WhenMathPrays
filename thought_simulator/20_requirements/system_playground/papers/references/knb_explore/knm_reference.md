# knm_reference.md

**Title:** KnM — Medium Grounding Tier Reference  
**Document ID:** Future-HLR  
**Version:** 0.2 (Pre-work — Exploratory)  
**Date:** 2026-07-07  
**Status:** Draft — Playground Reference  
**Purpose:** Define the Medium grounding tier (KnM) within the KnB pipeline.

---

## 1. Tier Definition

KnM is the **medium-entropy, context-aware** grounding tier.

It refines coarse anchors when context, continuity, or evidential signals justify deeper grounding, but it still avoids fine identity resolution or deep manifold commitments.

**KnM is not**: fine-grained disambiguation, deep relational geometry resolution, or conflict repair.

**Design Rationale**: KnM is the tier most frequently activated during normal grounding conditions. It balances precision and safety by incorporating contextual signals without over-committing.

---

## 2. Inputs

KnM reads:
- LI meaning commitments (proposition fragments, semantic tags)
- CoHI continuity_fields (referential history, conversation objects)
- SSR context from previous turn
- Manifold hints (including shallow relational geometry, basin proximity, and identity curvature signals)

**KnM may read** basin proximity signals but does not commit to basin identity.

---

## 3. Outputs (Tier-Specific Fields)

KnM writes its own distinct medium fields. Each field is a structured object.

### 3.1 Field Schemas

**identity_medium[]**:
```markdown
[
  {
    "text": "the 2025 Q2 sales dataset",
    "context": "revenue_analysis",
    "entropy": 0.52,
    "provenance": "LI/SSR",
    "kn_dt_ref": ["kndt:dataset_7842"],
    "confidence": "medium"
  }
]
```

**relation_medium[]**:
```markdown
[
  {
    "text": "correlates_with",
    "category": "contextual_relation",
    "entropy": 0.49,
    "provenance": "LI/SSR",
    "kn_dt_ref": ["kndt:relation_contextual"],
    "confidence": "medium"
  }
]
```

Similar structured objects for:
- `domain_anchor_medium[]`
- `qualifier_medium[]`
- `truth_validation_medium[]`

Supporting fields: `H_Kn_medium`, `Kn_level = "KnM"`, `escalation_flag`, `conflict_flag`

---

## 4. Resolution Rules

KnM performs **contextual resolution**:
- Contextual identity and relational refinement
- Domain-specific anchoring when supported by evidence
- Moderate ambiguity reduction

**Explicit prohibitions**:
- No identity splitting
- No merging of ambiguous referents
- No domain-specific inference without evidential support
- No temporal ordering beyond coarse sequence
- No spatial anchoring beyond categorical region
- No conflict repair

---

## 5. Entropy Thresholds

KnM operates in the **medium entropy band** (example: $0.35 \leq H < 0.65$).

### 5.1 Entropy Components (KnM)
KnM uses:
- lexical entropy
- contextual entropy
- evidential entropy
- relational entropy
- conflict entropy (lightweight)

**Escalation Rule**: Escalation to KnF occurs when $H < H_{\text{KnM_threshold}}$ OR strong contextual/relational evidence is present.

---

## 6. Examples

**Example 1 — Identity Refinement**  
Input: "the dataset" (from KnC) + context  
KnM output: `identity_medium`: "the 2025 Q2 sales dataset"

**Example 2 — Relation Refinement**  
Input: "linked to" (from KnC)  
KnM output: `relation_medium`: "correlates with marketing spend"

**Example 3 — Domain Anchor Refinement**  
Input: “the report” + context “financial audit”  
KnM output: `domain_anchor_medium`: “finance/audit”

**Example 4 — Escalation**  
Input: very low entropy + fine context  
KnM sets `escalation_flag` for KnF

---

## 7. Failure Modes

- Insufficient context → preserve KnC anchors and escalate to KnF if needed
- High residual ambiguity → preserve and flag
- KnM must not attempt to resolve cross-turn contradictions; it only flags them.

---

## 8. Invariants

- Determinism and replay safety
- Non-mutation of SSR
- SSR and manifold compatibility
- Monotonicity: KnM refines KnC but never contradicts or overwrites coarse fields. KnM fields remain frozen and visible to KnF; KnF adds refinement fields but does not delete or overwrite KnM fields.
- Feeds cleanly into LI mapping library

**Downstream Use**: KnM is LI’s primary grounding source; LI falls back to KnC only when KnM fields are insufficient.

---

*End of knm_reference.md (Revised Draft)*

---
Just say the word.

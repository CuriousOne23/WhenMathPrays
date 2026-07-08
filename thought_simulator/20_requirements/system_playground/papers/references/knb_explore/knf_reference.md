# knf_reference.md

**Title:** KnF — Fine Grounding Tier Reference  
**Document ID:** Future-HLR  
**Version:** 0.2 (Pre-work — Exploratory)  
**Date:** 2026-07-07  
**Status:** Draft — Playground Reference  
**Purpose:** Define the Fine grounding tier (KnF) within the KnB pipeline.

---

## 1. Tier Definition

KnF is the **low-entropy, high-precision** grounding tier.

It performs fine identity resolution, deep contextual alignment, and relational geometry refinement when evidence is strong and entropy is low.

**KnF is not**: manifold re-projection, speculative inference, or conflict repair.

**Design Rationale**: KnF is activated only in cases where context, continuity, and evidential signals converge strongly. It provides the highest precision only when justified by strong evidence, ensuring the system remains safe and deterministic even at fine granularity.

---

## 2. Inputs

KnF reads:
- LI meaning commitments (proposition fragments, semantic tags)
- CoHI continuity_fields (referential history, conversation objects)
- SSR context from previous turn
- Manifold hints including deeper relational geometry, basin identity, curvature signals, and shape-level cues

**KnF may read** deeper manifold geometry but must not re-project or mutate it. KnF may read shape-level cues but must not reinterpret or re-project manifold geometry.

---

## 3. Outputs (Tier-Specific Fields)

KnF writes its own distinct fine fields. Each field is a structured object.

### 3.1 Field Schemas

**identity_fine[]**:
```markdown
[
  {
    "text": "the 2025 Q2 sales dataset v3",
    "context": "revenue_analysis",
    "entropy": 0.28,
    "provenance": "LI/SSR",
    "kn_dt_ref": ["kndt:dataset_7842_v3"],
    "confidence": "fine"
  }
]
```

**relation_fine[]**:
```markdown
[
  {
    "text": "statistically correlates with",
    "category": "quantitative_relation",
    "entropy": 0.31,
    "provenance": "LI/SSR",
    "kn_dt_ref": ["kndt:relation_statistical"],
    "confidence": "fine"
  }
]
```

**domain_anchor_fine[]**:
```markdown
[
  {
    "text": "Q2 financial audit compliance",
    "category": "domain_specific",
    "entropy": 0.29,
    "provenance": "LI/SSR",
    "kn_dt_ref": ["kndt:domain_finance_audit"],
    "confidence": "fine"
  }
]
```

Similar structured objects for:
- `qualifier_fine[]`
- `truth_validation_fine[]`

Supporting fields: `H_Kn_fine`, `Kn_level = "KnF"`, `conflict_flag`

---

## 4. Resolution Rules

KnF performs **fine resolution**:
- Fine identity resolution
- Relational geometry refinement
- Domain-specific anchoring
- Qualifier sharpening
- Conflict surfacing (without repair)

**Explicit prohibitions**:
- No manifold re-projection
- No over-commitment without strong evidence
- No cross-turn contradiction repair
- No speculative inference
- No identity splitting or merging without clear continuity support
- No temporal precision beyond what SSR provides
- No spatial precision beyond categorical region unless explicitly supported

---

## 5. Entropy Thresholds

KnF operates in the **low entropy band** (example: $H < 0.35$).

**Components**: lexical, contextual, evidential, relational, conflict, geometric.

**Activation Rule**: KnF activates only when entropy is below threshold **AND** evidential support is strong. Geometric entropy is read-only and derived from manifold curvature signals.

---

## 6. Examples

**Example 1 — Fine Identity Resolution**  
Input: "the dataset" (from KnM) + strong context  
KnF output: `identity_fine`: "the 2025 Q2 sales dataset v3"

**Example 2 — Fine Relation Refinement**  
Input: "correlates with" (from KnM)  
KnF output: `relation_fine`: "statistically correlates with at p<0.01"

**Example 3 — Domain Anchor Refinement**  
Input: “finance report”  
KnF output: `domain_anchor_fine`: “Q2 financial audit compliance”

**Example 4 — Qualifier Sharpening**  
Input: "high risk"  
KnF output: `qualifier_fine`: "high regulatory compliance risk"

**Example 5 — Conflict Surfacing**  
Input: conflicting evidence  
KnF surfaces conflict flag without attempting repair

---

## 7. Failure Modes

- Insufficient evidence → preserve KnM fields
- Ambiguity → do not over-resolve
- Conflicts → surface but do not repair

---

## 8. Invariants

- Determinism and replay safety
- Non-mutation of SSR
- SSR and manifold compatibility (read-only)
- Monotonicity: KnF refines KnM but never contradicts or overwrites KnM fields. KnF fields remain frozen and visible to higher layers.
- Feeds cleanly into LI mapping library

**Downstream Use**: KnF provides LI’s highest-precision anchors when entropy is low and evidence is strong. KnF fields remain immutable after SSR freeze and are consumed directly by LI.

---

*End of knf_reference.md (Revised Draft)*

---

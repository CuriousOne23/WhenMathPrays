# li_mapping_library_prework.md

**Title:** LI Mapping Library — Pre-work Reference  
**Document ID:** Future-HLR  
**Version:** 0.2 (Pre-work — Exploratory)  
**Date:** 2026-07-07  
**Status:** Draft — Playground Reference  
**Purpose:** Define how LI assembles grounded anchors from KnC/KnM/KnF into coherent realization plans for RG/RSG.

---

## 1. Purpose & Architectural Role

LI (Local Inference) is the lightweight, deterministic mapping layer between the frozen SSR and the expression primitives (RG/RSG/OuBB).

LI is the first layer after SSR freeze that performs assembly rather than grounding.

LI does not perform grounding, manifold projection, or SSR mutation. It works strictly on already-projected, frozen SSR content and produces realization plans for surface-form generation.

**LI is manifold-informed** (via SSR projections) but **not manifold-based**.

---

## 2. Inputs

LI reads:
- Frozen SSR (meaning commitments, continuity_fields)
- KnC / KnM / KnF grounding fields
- CoHI continuity_fields
- TPTB/TPSF constraints (truth/safety phrasing rules)
- Discourse and continuity context

**LI does not read** manifold geometry directly. LI may read continuity_fields but must not reinterpret grounding decisions.

---

## 3. Outputs (Mapping-Level Fields)

LI produces structured realization plans.

**Example schemas**:

**li_identity_map[]**:
```markdown
[
  {
    "selected_tier": "medium",
    "anchor_text": "the 2025 Q2 sales dataset",
    "provenance": "KnM/SSR",
    "continuity_decision": "preserve"
  }
]
```

**li_relation_map[]**:
```markdown
[
  {
    "selected_tier": "fine",
    "anchor_text": "statistically correlates with",
    "provenance": "KnF/SSR",
    "continuity_decision": "preserve"
  }
]
```

**li_domain_map[]**:
```markdown
[
  {
    "selected_tier": "medium",
    "anchor_text": "finance/audit",
    "provenance": "KnM/SSR",
    "continuity_decision": "strengthen"
  }
]
```

**li_qualifier_map[]**:
```markdown
[
  {
    "selected_tier": "fine",
    "anchor_text": "high regulatory compliance risk",
    "provenance": "KnF/SSR",
    "continuity_decision": "sharpen"
  }
]
```

**li_ordering_plan[]**:
```markdown
[
  {
    "ordering": ["identity", "relation", "domain", "qualifier"],
    "continuity_rationale": "maintain referential flow"
  }
]
```

**li_realization_plan[]**:
```markdown
[
  {
    "assembled_text": "...",
    "template_used": "declarative_mapping",
    "safety_adjustments": ["TPSF_soften"],
    "continuity_decisions": ["preserve_identity", "strengthen_relation"],
    "provenance": ["SSR", "KnB", "LI"]
  }
]
```

---

## 4. Mapping Rules

LI selects grounding level using:

$$
\text{grounding_level} = f(\text{entropy}, \text{task_needs}, \text{continuity})
$$

**Decision Flow**:
- If KnF entropy < threshold AND evidence strong → use fine anchors
- Else if KnM entropy in medium band → use medium anchors
- Else → fallback to KnC anchors

LI then:
- Assembles identity + relation + domain anchors
- Applies continuity-aware ordering rules
- Applies qualifier sharpening or softening
- Applies TPTB/TPSF phrasing constraints
- Selects templates for common discourse acts

---

## 5. Template Library (Pre-Work)

Lightweight, deterministic templates include:
- Declarative mapping
- Relational mapping
- Causal mapping
- Comparative mapping
- Continuity-preserving mapping
- Safety-aware phrasing templates

Templates must be deterministic and must not introduce new meaning not present in SSR or KnB.

---

## 6. Examples

**Example 1 — KnM → LI Mapping**  
Input (SSR + KnM):
- identity_medium: “the 2025 Q2 sales dataset”
- relation_medium: “correlates with marketing spend”
- qualifier_coarse: “high risk”
- continuity_fields: “analysis context”

LI Output: 
- assembled_text: “The 2025 Q2 sales dataset correlates with marketing spend, indicating high risk.”
- template_used: “declarative_mapping”
- continuity_decisions: “preserve identity, strengthen relation”
- safety_adjustments: none

**Example 2 — KnF Activation**  
Input: low entropy + strong evidence  
LI selects fine anchors and applies precision templates

**Example 3 — Safety Constraint**  
Input: TPSF qualification requirement  
LI applies safety-aware phrasing to the selected anchors

---

## 7. Failure Modes

- Insufficient grounding → fallback to KnC
- Conflicting anchors → surface conflict, do not repair
- Ambiguous continuity → preserve ambiguity
- Unsafe phrasing → apply TPSF constraints
- LI must not attempt grounding; fallback to KnC/KnM/KnF only.

---

## 8. Invariants

- Determinism and replay safety
- SSR freeze compatibility
- Manifold compatibility (read-only)
- Monotonicity: LI never overwrites KnB fields
- LI produces realization plans consumed directly by RG/RSG
- No component after SSR freeze may re-project or re-resolve manifold geometry
- LI must not introduce new semantic content not present in SSR or KnB

---

*End of li_mapping_library_prework.md (Revised Draft)*

---

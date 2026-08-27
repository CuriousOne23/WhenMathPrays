# IdOB vocabulary (this bench revision)

One-line definitions for Slide 00. Official names preferred.

**Official long definitions and glossary** live in:

- Theory: [../papers/idob_s2m_theory.md](../papers/idob_s2m_theory.md)
- Constructs + Appendix A glossary: [../papers/idob_s2m_constructs.md](../papers/idob_s2m_constructs.md)

This file stays the short table plus the Slide 00 Q&A. If a line here fights the constructs paper, the constructs paper wins until a revision is declared.

**Type note:** official `meaning_semantics` is the six-float vector M, not a literal string such as "Henry". Appendix A uses some literals as teaching examples of what the talk is about. Treat those as notes, not as the packet type.

---

## Structure (meaning-blind)

| Name | Job |
|------|-----|
| `semantic_field_id` | Which semantic field the geometry sits in |
| `semantic_role_id` | Role in that field |
| `semantic_object_id` | Object slot in the geometry |
| `gradient_id` | Dynamic / gradient class of the geometry |
| `universe_id` | Which universe the geometry is drawn from |
| `subfield_id` | Subfield inside the field |
| `structural_hash` / `structural_key` | Fingerprint of the six IDs only |
| `residue_hash` / `residue_code` | Constraint-tension fingerprint; still not meaning |
| `routing_signature` | `struct_hash` + feature hashes for routing / ranking signals |
| `identity_metadata` | Tags/vector adjacent to structure; not baked into the hash |

## Meaning groups and six fields

| Name | Job |
|------|-----|
| `group_id` | Stable id of a meaning group |
| `group_name` | Human label (e.g. ACTION.physical.motion) |
| `primitive` | ENTITY / ACTION / EVENT / STATE / QUALITY / ... |
| `group_dimensions` | Prototype six-vector for the group |
| `physicality` | How much the meaning is physical object/action |
| `sociality` | Social / interpersonal weight |
| `temporality` | Time / event / change weight |
| `intentionality` | Agency / purpose weight |
| `materiality` | Matter / transformation weight |
| `spatiality` | Place / path / geometry weight |
| `meaning_semantics` | IdOB current six-vector M (not a literal name string) |

## Identity and search

| Name | Job |
|------|-----|
| `identity_envelope` / CIE | Local pressure on the speaker-object stand-in (this utterance) |
| `identity_importance` / `alpha` | How hard CIE pushes M |
| `identity_tags` | Coarse stance tags (e.g. physical, scientific) |
| `identity_vector` | Numeric identity pressure used in M' = M + alpha I |
| `identity_delta` | Change in identity vector across cycles |
| `meaning_delta_h` | ||M_i - M_{i-1}|| (machine motion, not a person's change) |
| `idob_search_budget_min` / `max` | Cycle bounds (4-6 in the papers) |
| `resolution_status` | Why the run froze |
| `ready_for_ouba` | Handoff flag; this bench stops here |

## Stop reasons (must match the actual halt)

- `stable` — meaning delta below epsilon
- `identity_stable` — identity delta below epsilon first
- `budget_exhausted` — max cycles hit
- `time_exhausted` — supervisor forced stop

A packet that says `stable` when the halt was budget is an instrument error.

---

# Appendix A — Clarifying Questions for Slide 00_contract

Foundational Q&A from the 00_contract walk. Official `meaning_semantics` is the six-vector M. Literals in examples are teaching notes.

## Q1 — Three major categories of an IdOB packet?

1. Structure (meaning-blind): six IDs, structural_hash, residue_hash, routing_signature, identity_metadata.
2. Meaning groups and six fields: group_id, group_name, primitive, group_dimensions, six axes, meaning_semantics (vector M).
3. Identity and search: CIE, alpha, tags, identity_vector, deltas, budget, resolution_status, ready_for_ouba.

Example utterance for teaching: "Henry fixed the Craftsman table in New York." Structure might be ACTION.repair shaped; meaning uses PERSON/OBJECT/LOCATION prototypes; identity may tag repair/task.

## Q2 — What are the six meaning fields?

physicality, sociality, temporality, intentionality, materiality, spatiality.

## Q3 — Where do literal names like Henry / New York go?

Not in official meaning_semantics (that field is M). Not in the structural key. Not in CIE tags. In this bench they are notes (utterance text, card note, teaching tables). A future revision may add an explicit lexical field.

## Q4 — Do names appear in Structure?

No. Structure is meaning-blind. Role = agent, not "Henry".

## Q5 — Do names appear in Identity?

No. Tags such as repair, not "Henry".

## Q6 — Does Path A fill all three categories?

Full Path A aims to. This learning bench often starts from a hand structure card and only prints what the current slide allows.

## Q7 — Are Meaning-table columns about the same object?

Each row is one meaning group. Six-axis columns describe that group's stand-in vector.

## Q8 — Do Structure and Identity have 2D tables?

Structure: 1 row. Identity: 1 row. Meaning: multiple group rows possible; slide-07 packet still carries one selected M.

## Q9 — What is universe_id?

Universe of discourse for the structure. No meaning scores. Example: everyday_tasks.

## Teaching tables

Structure (1 row): field / role / object / gradient / universe / subfield / hashes.

Meaning (multi-row teaching view): group columns plus a note column for literals. That note column is not packet meaning_semantics.

Identity (1 row): envelope / alpha / tags / vector / deltas / resolution_status / ready_for_ouba.

Appendix A complete.

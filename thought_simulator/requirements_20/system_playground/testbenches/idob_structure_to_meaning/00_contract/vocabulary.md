# IdOB vocabulary (this bench revision)

One-line definitions. Official names preferred.

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
| `meaning_semantics` | IdOB current six-vector M |

## Identity and search

| Name | Job |
|------|-----|
| `identity_envelope` / CIE | Local conversational identity of this utterance |
| `identity_importance` / `alpha` | How hard CIE pushes M |
| `identity_tags` | Coarse stance tags (e.g. physical, scientific) |
| `identity_vector` | Numeric identity pressure used in M' = M + alpha I |
| `identity_delta` | Change in identity vector across cycles |
| `meaning_delta_h` | ||M_i - M_{i-1}|| |
| `idob_search_budget_min` / `max` | Cycle bounds (4-6 in the papers) |
| `resolution_status` | Why the run froze |
| `ready_for_ouba` | Handoff flag; this bench stops here |

## Stop reasons (must match the actual halt)

- `stable` — meaning delta below epsilon
- `identity_stable` — identity delta below epsilon first
- `budget_exhausted` — max cycles hit
- `time_exhausted` — supervisor forced stop

A packet that says `stable` when the halt was budget is an instrument error.

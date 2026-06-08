# Requirements Delta — 40.392

## Status
Phase B complete — 8/8 PASS (2026-06-08)

## Anchor
- 20.39 §3.1–3.2 (HLR-021–025)

## HLR → struct / scenario mapping (20.039)

| HLR | Struct / topic | Primary scenario(s) |
|-----|----------------|---------------------|
| 021 | `ConversationLayerState` envelope partition | `positive_conversation_layer_envelope_clean` |
| 022 | `UspSnapshot` round-trip + content digest | `positive_usp_snapshot_roundtrip`, `positive_iiinb_digest_compat` |
| 023 | `InputRepairTag` intake-bound shape | covered by struct export (Phase B structural) |
| 024 | Canonical ordering + audit exports | `positive_input_repair_tag_ordering`, `positive_audit_struct_exports`, `positive_golden_fixture_match` |
| 025 | Envelope separation guard | `negative_forbidden_semantic_core_field` |
| 019 | Schema version reject | `negative_unknown_schema_version` |

## Implemented
| HLR family | Evidence |
|------------|----------|
| 022 | `positive_usp_snapshot_roundtrip`, digest compat with 40.101 |
| 024 | tag ordering, golden fixture, audit struct exports |
| 021, 025 | envelope separation guard |
| 019 | unknown schema reject |
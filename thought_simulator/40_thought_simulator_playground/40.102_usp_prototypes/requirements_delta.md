# Requirements Delta — 40.102 USP

## Status
Phase B complete — 8/8 PASS (2026-06-08); GATE-B row 201

## Anchor
- 20.102 (HLR-001–024 exploratory coverage via harness)

## HLR → scenario mapping (20.102)

| HLR family | Topic | Primary scenario(s) |
|------------|-------|---------------------|
| 006–008 | Read model (IIInB) | `positive_iiinb_readonly_load`, `positive_empty_profile_snapshot` |
| 009–012 | Versioning + transitions | `positive_single_rule_commit`, `positive_supersede_chain`, `positive_replay_identical_ref` |
| 013–015 | Rule lifecycle | `positive_supersede_chain`, `positive_revoke_rule` |
| 014 | GB veto | `negative_gb_veto_no_active` |
| 016 | Active rule cap | `negative_cap_overflow` |
| 018–019 | Replay + serialization | `positive_replay_identical_ref` (digest via 40.392) |
| 020–022 | Audit / reason codes | reason-code asserts on negative paths |
| 024 | Fixture testability | full 8-scenario matrix |

## Implemented
`USPStore.apply_commit` (create / supersede / revoke), `export_snapshot` (ACTIVE-only), monotonic `usp_version_id`, content-addressed `usp_version_ref`, GB veto path, cap overflow reject. Struct shapes and digest imported from [40.392](../40.392_core_data_structs_prototypes/prototype.py).
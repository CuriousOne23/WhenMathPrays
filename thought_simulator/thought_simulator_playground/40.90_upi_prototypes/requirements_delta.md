# Requirements Delta — 40.90 UPI

## Status
Phase B complete — 8/8 PASS (2026-06-08); GATE-B row 202

## Anchor
- 20.103 (HLR-001–022 via harness mapping)

## HLR → scenario mapping (20.103)

| HLR family | Topic | Primary scenario(s) |
|------------|-------|---------------------|
| 001–004 | Authority / placement | structural (orchestration-only; no A/B mutation) |
| 005–008 | Clarification → commit | `positive_single_commit`, `positive_fifo_two_events`, `negative_incomplete_event` |
| 009–011 | GB governance | `positive_gb_approve`, `positive_gb_veto` |
| 012–014 | Determinism / replay | `positive_fifo_two_events`, `positive_replay_identical_ref` |
| 015–016 | Bounds | `negative_usp_cap_overflow`, `negative_pending_commit_cap` |
| 017–019 | Cross-program separation | structural negatives in harness setup |
| 022 | Append-only audit | audit asserts on all commit paths |

## GB integration
- Harness stub: `gb_decision` → `gb_reason_code` on `UpiCommitRecord`
- Live path: [40.130](../40.130_gb_prototypes/prototype.py) `evaluate_upi_commit` → `harness_w2.py` (4/4 PASS)

## Implemented
FIFO `clarification_event` orchestration → GB gate → `USPStore.apply_commit`. `gb_reason_code` propagated on approve (`GB_TEST_OK` / `GB_APPROVED`) and veto (`GB_VETO` / evaluator code) in `UpiCommitRecord.gb_reason_code` and `reason_codes`.
# 40.101 Requirements Delta

## Evidence-backed deltas

- HLR-20.101-001/002: `profile_enabled=false` skips stage; no USP load — `profile_disabled_skip`
- HLR-20.101-003: `InB → IIInB → RB` stage order — `positive_inb_iiinb_rb_order`
- HLR-20.101-011/015: Rule apply on intake-bound tags only; envelope guard PASS — `positive_usp_rule_apply`
- HLR-20.101-012/017: Escalation without guess — `negative_escalate_no_guess`
- HLR-20.101-019: Apply cap at 16 — `negative_apply_cap`
- HLR-20.101-021: Deterministic replay — `positive_deterministic_replay`

## Open gaps (Phase 2+)

- Full CIL FIFO wire (40.33 redo)
- TCU reporting fidelity (20.150)
- `FAIL_ENVELOPE` replay verdict fixtures (40.510-207)
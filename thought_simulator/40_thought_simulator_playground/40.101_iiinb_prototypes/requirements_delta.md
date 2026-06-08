# Requirements Delta

## Scaffold Status
- scaffold_status: implemented (initial Phase B pass, 2026-06-08)
- Phase A: **complete and promotion-ready** (2026-06-08)
- Phase B: initial execution complete (6/6 PASS); formal approval pending (40.510-101, GATE-A)

## Anchors
- 20-anchor: thought_simulator/20_requirements/20.101_iiinb_requirements.md (full 28 HLRs in software_description.md)
- 10.10-anchors: 10.10.10, 10.10.20, 10.10.50 (intake-bound writes, read-only USP, envelope isolation)
- upstream: 40.100_inb_prototypes (InB handoff `inb_to_iiinb_v1`)

## Exploratory Note
The complete set of HLR-20.101-001 through HLR-20.101-028 is made visible in `software_description.md` for playground exploration. 20.xx remains authoritative; 30.xx is the coverage audit layer. 40.101 is non-canonical.

## Part A Documentation (Phase A deliverables)
- `software_description.md`: purpose, boundaries, full HLR visibility, flows alignment, intake/outbound handoff contracts, draft sections (envelope guard, profile gate, USP consumption, escalation, caps, digest, reason codes, test matrix)
- `verification_capsule.md`: Phase A checklist + initial evidence baseline
- `prototype.py` / `harness.py`: exploratory skeleton (pre-dated Phase A doc; 6/6 initial pass retained as baseline)

## Part B Evidence (Initial pass — 2026-06-08)
- Harness run: 2026-06-08
- Artifact: `artifacts/iiinb_verification_run_2026-06-08.json`
- Status: PASS (6/6 scenarios)
- Evidence types: behavioral, structural, negative, replay

### Implemented / demonstrated
| HLR | Implementation | Scenario |
|-----|----------------|----------|
| 001 | `repair_pass` skip when `profile_enabled=false` | `profile_disabled_skip` |
| 002 | No USP load on profile-disabled path | `profile_disabled_skip` |
| 003 | `run_intake_path` stage ordering | `positive_inb_iiinb_rb_order` |
| 005–008 | Read-only `UspSnapshot`; no mutation | `positive_usp_rule_apply` |
| 009 | Bounded pattern→expansion only | `positive_usp_rule_apply`, `negative_escalate_no_guess` |
| 011 | `repair_outcome=APPLIED` + `rule_id` on intake tags | `positive_usp_rule_apply` |
| 012 | `repair_outcome=ESCALATED` when no rule | `negative_escalate_no_guess` |
| 014 | Writes confined to `tp_intake_fields` | all repair scenarios |
| 015 | `envelope_guard` semantic_core/tp_tr unchanged | all repair scenarios |
| 017 | Escalation refs emitted; no guess | `negative_escalate_no_guess` |
| 019 | `MAX_RULE_APPLICATIONS=16` cap | `negative_apply_cap` |
| 021 | `_canonical_digest` replay contract | `positive_deterministic_replay` |
| 022 | `REASON_CODES` registry in prototype | profile skip, escalate paths |

### Open / partial
| HLR | Gap | Notes |
|-----|-----|-------|
| 004 | Not in RB→OB chain | Structural assertion planned |
| 006 | `usp_version_ref` on record | Partial — set on apply path; dedicated scenario todo |
| 007 | Multi-rule precedence | Overlap edge cases todo |
| 010 | Segmentation policy | Playground whitespace split only |
| 013 | MI_VAGUE/MI_INCOMP non-resolution | Deferred — no IIInB auto-resolve |
| 016 | Conversation-scoped audit storage | In-memory playground record only |
| 018 | Non-blocking Pipeline A | Policy documented; CIL wire deferred Wave 2 |
| 020 | TCU budget vs 20.150 | Playground `tcu_cost` stub only |
| 023 | IMR same-cycle isolation | Not modeled in playground |
| 024 | Pipeline B envelope non-access | Guard positive only; `FAIL_ENVELOPE` todo (40.510-207) |
| 025–028 | Parent invariants, fixtures, audit export, MB diagnostics | Deferred to Phase B expansion / 30-series |

## Phase 1 delta (40.510-101)
- Created IIInB module: `profile_enabled` gate, read-only USP apply, intake-bound TP writes, `run_intake_path` ordering
- Initial harness 6/6 PASS; Phase A software description complete 2026-06-08

## Flows Alignment Statement

- **Forward Flow (20-series)**: [20.101](../../20_requirements/20.101_iiinb_requirements.md) drives all documented obligations; [20.100](../../20_requirements/20.100_inb_requirements.md) / [40.100](../40.100_inb_prototypes/software_description.md) inform upstream handoff.
- **Backward Flow (40-series evidence)**: 6/6 PASS initial artifact proves core repair-path skeleton; open HLRs named above.
- **Iterative Design Flow (50-series influence)**: None yet; Wave 2 conversation layer deferred per [40.510](../40.510_refactor.md).

**Agreement Statement**: Provisionally aligned for Phase A closure. Phase B formal approval requires expanded test matrix and GATE-A reviewer sign-off on 40.510-101.

## Open gaps (Phase 2+)
- Full CIL FIFO wire (40.33 redo)
- TCU reporting fidelity (20.150)
- `FAIL_ENVELOPE` replay verdict fixtures (40.510-207)
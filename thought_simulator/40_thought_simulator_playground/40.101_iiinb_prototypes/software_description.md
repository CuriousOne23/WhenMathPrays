# 40.101_iiinb_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP review, 2026-06-08)
- Phase B (prototype + harness + evidence): **approved** (19/19 PASS; CP review, 2026-06-08; 40.510-101)

## Phase B Deliverables (Executed)
- Harness executed 19 scenarios; artifact: `artifacts/iiinb_verification_run_2026-06-08.json`
- Evidence types (per 40.20): behavioral, structural (intake path ordering, basin-chain exclusion), negative (escalate, caps, rejected handoff, USP load failure), replay, golden diff (diagnostic export)
- Core invariants demonstrated: `profile_enabled` gate, read-only USP apply/immutability, escalate-without-guess, `InB → IIInB → RB` ordering, apply/segment caps, envelope guard (semantic_core, TP.TR, Pipeline B), deterministic replay/segmentation, multi-rule precedence, USP version pinning, TCU reporting, audit record per pass, diagnostic export ordering, non-blocking escalation handoff
- HLR coverage (exploratory, with harness evidence): 001–012, 014–022, 024, 026–028
- Remaining HLR exploration: 013 (MI_VAGUE/MI_INCOMP non-resolution), 023 (IMR same-cycle isolation), 025 (parent invariant cross-check), `FAIL_ENVELOPE` negatives (40.510-207)
- Note: The full HLR list from 20.101_iiinb_requirements.md is included below for exploratory visibility. 20.xx remains the sole source of truth; 30.xx remains the authoritative coverage audit layer. 40.101 is a playground and not authoritative.

## Scaffold Metadata
- scaffold_status: implemented (Phase B complete, 19/19 PASS)
- intended_20_anchor: thought_simulator/20_requirements/20.101_iiinb_requirements.md (primary)
- intended_10_10_anchors:
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md (deterministic cycle; IIInB as optional pre–Pipeline A repair slice)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.20_interprocess_communication_and_channels.md (immutable snapshots; read-only USP consumption)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md (intake-bound TP writes only; no `semantic_core` mutation)
- applicability: exploratory module for IIInB as profile-gated `input_semantic_repair` after InB surface normalization. Focus on read-only USP apply, bounded repair/escalation, intake-bound TP writes, and clean handoff to RB.
- disposition_target: promote
- program_wave: **W1** (Track H intake) per [40.510_refactor.md](../40.510_refactor.md) §4.2

## Purpose

This scaffold reserves the module slot for exploratory implementation of the Input Inference/Repair Basin (IIInB) as the optional **`input_semantic_repair`** stage on the Track H intake path.

It corresponds to the profile-gated repair slice defined in 20.101_iiinb_requirements.md, positioned **after** [20.100](20.100_inb_requirements.md) InB and **before** RB routing.

IIInB executes only when `profile_enabled = true`; otherwise it skips with zero semantic effect.

**Intake ordering (HQ-001):** `InB → IIInB → RB`

IIInB is responsible for:
- Executing `input_semantic_repair` only when `profile_enabled = true` for the active execution signature
- Skipping with zero semantic effect when `profile_enabled = false` (no USP load)
- Loading USP via read-only snapshot pinned by `usp_version_ref`
- Deterministic whitespace segmentation and bounded pattern→expansion repair under USP rules
- Emitting `input_repair_tags[]`, `input_segments[]`, `iiinb_escalation_refs[]` on intake-bound TP fields only
- Escalating unknown shorthand-eligible segments to CIL (no guessing, no UPI/IMR direct call)
- Enforcing segment (32) and apply (16) caps with deterministic truncate-with-audit
- Producing `iiinb_repair_record` per repair pass for replay pinning
- Preserving envelope isolation: no writes to `semantic_core`, `TP.TR`, MTP, or Pipeline B envelopes
- Remaining deterministic and replayable under identical InB output + USP snapshot + profile state

IIInB **does not**:
- Perform surface canonicalization (owned by InB)
- Write or mutate USP state (owned by UPI)
- Write `semantic_core`, `TP.TR`, or meaning-commitment fields
- Auto-resolve `MI_VAGUE` / `MI_INCOMP` (owned by IB/messy-input pathways)
- Block Pipeline A waiting for clarification
- Execute inside the RB→OB→TR→TB basin chain

## Scope
- exploratory module for requirements-driven IIInB prototyping on Track H intake
- initial prototype + harness implemented (`prototype.py`, `harness.py`); evidence in `verification_capsule.md` and `requirements_delta.md`
- continues to explore all behaviors and invariants defined in the 20.101 HLRs below, plus supporting 10-series contracts and boundaries
- cross-turn UPI/GB/CIL wiring deferred to Wave 2 (40.102, 40.103, 40.33 redos)

All exploration **SHALL** remain strictly deterministic, bounded, audit-rich, and replayable. The full HLR list is reproduced here for exploratory visibility in the playground.

## Flows Alignment Statement

- **Forward Flow (10/20-series)**: Driven by [20.101](../../20_requirements/20.101_iiinb_requirements.md) (activation, USP consumption, repair semantics, TP write authority, escalation, bounds, determinism), [20.102](../../20_requirements/20.102_usp_requirements.md) (read-only USP snapshot), [20.105](../../20_requirements/20.105_tp_requirements.md) §3.4 (intake-bound TP fields), [20.38](../../20_requirements/20.38_ts_implementation_guidelines.md) §6 (intake path), and upstream [20.100](../../20_requirements/20.100_inb_requirements.md) InB handoff ([40.100](../40.100_inb_prototypes/software_description.md)). Ordering: `InB → IIInB → RB`.

- **Backward Flow (40-series evidence)**: Phase B complete (2026-06-08): 19/19 harness PASS — full test matrix executed. Artifact: `artifacts/iiinb_verification_run_2026-06-08.json`. Capsule: `verification_capsule.md`; delta: `requirements_delta.md`.

- **Iterative Design Flow (50-series influence)**: None yet; USP/UPI/CIL cross-turn paths deferred to Wave 2 per [40.510](../40.510_refactor.md).

**Agreement Statement**: Aligned — Phase B approved (CP, 2026-06-08). Evidence (19/19 PASS) supports forward intent for profile-gated `input_semantic_repair` on Track H intake. Residual gaps (HLR-013, 023, 025, 024b) are named in `requirements_delta.md` and Risks & Unknowns.

## Phase A Deliverables (this document)
- High-level description of IIInB as `input_semantic_repair` stage for exploratory prototyping
- Mapping of 10/20-series intent to skeleton responsibilities
- Full reproduction of the 20.101 HLR set for exploratory visibility (see "HLR Reference (Exploratory Visibility)")
- Intake handoff contract (consumes 40.100), outbound handoff to RB, `iiinb_repair_record` skeleton
- Draft sections: envelope write guard, profile gate, USP consumption, escalation policy, bounds/caps, state digest, reason codes, minimal internal state, test matrix
- Prototype thresholds (`MAX_SEGMENTS=32`, `MAX_RULE_APPLICATIONS=16`) are playground fixtures; governed by 20-series for authoritative values

## Intake Handoff Contract (from InB)
IIInB consumes accepted InB output per [40.100](../40.100_inb_prototypes/software_description.md) handoff contract (HLR-20.101-003, 20.100-020):

```
inb_handoff = {
  "contract_version": "inb_to_iiinb_v1",
  "next_stage": "input_semantic_repair",
  "downstream_after_repair": "routing",
  "ordering": ["inb_surface_norm", "input_semantic_repair", "routing"],
}
```

Required accepted InB fields for repair pass:
- `canonical_content` (str) — surface-normalized text from InB
- `provenance.outcome` — must be `"accepted"`; rejected InB → skip/error path
- Optional: `state_digest`, `metadata.intake_order` — replay/audit metadata

Rejected InB intake SHALL NOT proceed to USP apply (playground: `INB_HANDOFF_REJECTED`).

## Outbound Handoff (to RB)
After repair pass (or profile-disabled skip), IIInB hands off to routing/RB:

```
iiinb_result = {
  "skipped": bool,
  "stage": "input_semantic_repair" | null,
  "handoff_next_stage": "routing",
  "usp_loaded": bool,
  "tp_intake_fields": {
    "input_segments": [...],
    "input_repair_tags": [...],
    "iiinb_escalation_refs": [...],
  },
  "iiinb_repair_record": {...} | null,
  "envelope_guard": {
    "semantic_core_unchanged": true,
    "tp_tr_unchanged": true,
  },
}
```

Intake path recorder (`run_intake_path`) emits stage sequence: `inb_surface_norm` → [`input_semantic_repair`] → `routing`.

## iiinb_repair_record (Draft Skeleton)
Per 20.101 wire schema (playground fixture):

```
iiinb_repair_record = {
  "iiinb_event_id": str,
  "cycle_id": str,
  "input_packet_id": str,
  "usp_version_ref": str,
  "profile_enabled": true,
  "segment_count": int,
  "applied_rule_count": int,
  "repair_outcomes": ["APPLIED" | "ESCALATED" | "TRUNCATED", ...],
  "rule_ids": [str, ...],
  "escalation_refs": [str, ...],
  "cap_status": "OK" | "SEGMENT_CAP" | "APPLY_CAP",
  "tcu_cost": int,
  "reason_codes": [str, ...],
  "rationale_codes": [],
}
```

## Envelope Write Guard (Draft)
HLR-20.101-015, 024. IIInB **may write** only intake-bound TP fields. **Must not write:**

- `semantic_core` (frozen meaning envelope)
- `TP.TR` / `tp_tr` (truth-related TP partition)
- MTP semantics, OB evidence, truth fields
- Pipeline B envelopes (`exec_plan`, `exec_trace`)

Harness verifies `envelope_guard.semantic_core_unchanged` and `tp_tr_unchanged` after every repair pass (positive guard only; HLR-024b `FAIL_ENVELOPE` negatives — see Risks & Unknowns).

## profile_enabled Gate (Draft)
HLR-20.101-001, 002.

- `profile_enabled = false` → `skipped: true`, `usp_loaded: false`, no `iiinb_repair_record`, zero semantic effect; stage sequence jumps `inb_surface_norm` → `routing`
- `profile_enabled = true` → load USP snapshot (if provided), run repair pass, emit record

## USP Consumption (Draft)
HLR-20.101-005–008, 007.

- Read-only `UspSnapshot` pinned by content-addressed `usp_version_ref` (`compute_usp_version_ref`)
- Apply only `ACTIVE` rules; deterministic precedence: higher `precedence`, then `version`, then `rule_id`
- Pattern match against segmented `segment_text` (exact match in playground)
- `usp_snapshot = null` when profile enabled → `USP_LOAD_FAILED` (no guess)
- No USP mutation

## Escalation Policy (Draft)
HLR-20.101-012, 017, 018.

- No matching rule for shorthand-eligible segment → `repair_outcome: ESCALATED`
- Emit `iiinb_escalation_ref` with `escalation_reason_code` (e.g. `NO_MATCHING_RULE`)
- Queue for CIL handoff (wire deferred to Wave 2); playground records refs only
- Pipeline A does not block waiting for clarification
- No UPI or IMR direct invocation

## Bounds and Caps (Draft)
HLR-20.101-019, 020.

- **MAX_SEGMENTS:** 32 per turn (playground default)
- **MAX_RULE_APPLICATIONS:** 16 per turn (playground default)
- Overflow → deterministic truncate-with-audit; `cap_status`: `SEGMENT_CAP` or `APPLY_CAP`
- `tcu_cost` reported per pass (playground: `len(segments) + applied_count`); full 20.150 budget alignment deferred

## State Digest (Definition)
Deterministic replay fingerprint (HLR-20.101-021):

- **Digest input:** `{record, tp_intake_fields}` — `iiinb_repair_record` plus intake-bound TP field snapshot
- **Algorithm:** SHA-256 over canonical JSON (`sort_keys=True`, compact separators), UTF-8 encoded
- **Replay contract:** identical InB output + `usp_version_ref` + `profile_enabled` + `cycle_id` → identical `state_digest`

## Reason Codes (Draft)
HLR-20.101-022. Playground registry (`REASON_CODES` in `prototype.py`):

| Code | Meaning |
|------|---------|
| `PROFILE_DISABLED` | `profile_enabled=false` skip |
| `USP_LOAD_FAILED` | Profile on but no USP snapshot |
| `SEGMENT_CAP` | Segment span limit exceeded |
| `APPLY_CAP` | Rule application limit exceeded |
| `NO_MATCHING_RULE` | Escalation — no USP coverage |

## Minimal Internal State
**May hold (per repair pass):**
- Ephemeral `IIInB` instance state (`_event_counter` for deterministic `iiinb_event_id` when `deterministic_mode=true`)
- Working segmentation and rule-match state during `repair_pass()` only

**Must not hold:**
- USP mutable store (read-only snapshot per pass)
- `semantic_core`, MTP, OB, RB, CIL internal state
- Cross-pass repair caches that affect determinism

**Persistence and reset:** each harness scenario uses a fresh `IIInB()` unless testing replay with identical inputs.

## Test Matrix
| Category | Scenario (harness) | HLR anchors | Status |
|----------|-------------------|-------------|--------|
| Profile disabled skip | `profile_disabled_skip` | 001, 002 | PASS |
| InB→IIInB→RB order | `positive_inb_iiinb_rb_order` | 003 | PASS |
| Rejected InB handoff | `negative_rejected_inb_handoff` | 003 | PASS |
| Not in RB→OB chain | `positive_not_in_rb_ob_chain` | HLR-20.101-004 | PASS |
| USP rule apply | `positive_usp_rule_apply` | 005, 008, 011, 014, 015 | PASS |
| USP version ref pinned | `positive_usp_version_ref_pinned` | 006 | PASS |
| Multi-rule precedence | `positive_multi_rule_precedence` | 007 | PASS |
| USP snapshot immutable | `positive_usp_snapshot_immutable` | 008 | PASS |
| Escalate no guess | `negative_escalate_no_guess` | 009, 012 | PASS |
| Segmentation deterministic | `positive_segmentation_deterministic` | 010 | PASS |
| CIL escalation non-blocking | `positive_cil_escalation_nonblocking` | 017, 018 | PASS |
| Apply cap | `negative_apply_cap` | 019 | PASS |
| Segment cap | `negative_segment_cap` | 010, 019 | PASS |
| TCU cost reported | `positive_tcu_cost_reported` | 020 | PASS |
| Deterministic replay | `positive_deterministic_replay` | 021 | PASS |
| USP load failure | `negative_usp_load_failure` | 005, 022 | PASS |
| Pipeline B envelope guard | `positive_pipeline_b_envelope_unchanged` | 024 | PASS |
| Audit record per pass | `positive_audit_record_per_pass` | 016 | PASS |
| Diagnostic export ordering | `positive_diagnostic_export_ordering` | 027, 028 | PASS |
| FAIL_ENVELOPE negatives (024b) | *(deferred)* | 015, 024b | todo (40.510-207) |
| MI_VAGUE/MI_INCOMP non-resolve | *(deferred)* | 013 | todo (30-series) |
| IMR same-cycle isolation | *(deferred)* | 023 | todo (30-series) |
| Parent invariant cross-check | *(deferred)* | 025 | todo (30-series) |

## HLR Reference (Exploratory Visibility)
Phase-A evidence for these HLRs is provided in the Test Matrix; Phase B harness evidence (19/19 PASS) is summarized in `verification_capsule.md`. This list is retained as a reference. Source: 20.101_iiinb_requirements.md.

1. HLR-20.101-001: IIInB SHALL execute as stage wire `input_semantic_repair` only when `profile_enabled = true` for the active execution signature.
2. HLR-20.101-002: When `profile_enabled = false`, TS SHALL skip `input_semantic_repair` with zero semantic effect and SHALL NOT load USP.
3. HLR-20.101-003: IIInB SHALL run only after InB handoff and before RB on the intake path: `InB → IIInB → RB`.
4. HLR-20.101-004: IIInB SHALL NOT execute as a stage inside the RB→OB→TR→TB basin chain.
5. HLR-20.101-005: IIInB SHALL load USP via read-only snapshot pinned by `usp_version_ref` per 20.102 HLR-20.102-006.
6. HLR-20.101-006: IIInB SHALL record `usp_version_ref` on every `iiinb_repair_record` for replay pinning.
7. HLR-20.101-007: IIInB SHALL apply only `ACTIVE` USP rules using deterministic precedence per 20.102 HLR-20.102-012.
8. HLR-20.101-008: IIInB SHALL NOT mutate USP state.
9. HLR-20.101-009: IIInB SHALL perform bounded pattern→expansion repair only — no latent inference, no multi-stable meaning selection without USP rule coverage.
10. HLR-20.101-010: IIInB SHALL segment intake text into bounded spans (`input_segments[]`) before rule matching; segmentation SHALL be deterministic under versioned profile rules.
11. HLR-20.101-011: On rule match, IIInB SHALL emit `repair_outcome = APPLIED` with `rule_id`, `segment_ref`, and `resolved_segment_ref` on intake-bound TP fields.
12. HLR-20.101-012: On no matching rule for a shorthand-eligible segment, IIInB SHALL emit `repair_outcome = ESCALATED` and SHALL queue CIL escalation — not guess meaning.
13. HLR-20.101-013: IIInB SHALL NOT auto-resolve `MI_VAGUE` or `MI_INCOMP` semantics; messy-input tags from 20.17 remain authoritative for those pathways.
14. HLR-20.101-014: IIInB writes SHALL be confined to intake-bound TP fields: `input_repair_tags[]`, `input_segments[]`, `iiinb_escalation_refs[]`.
15. HLR-20.101-015: IIInB SHALL NOT write MTP, `semantic_core`, `TP.TR`, OB evidence, or truth fields.
16. HLR-20.101-016: IIInB SHALL append one `iiinb_repair_record` per repair pass to conversation-scoped audit storage (not `exec_trace`).
17. HLR-20.101-017: IIInB escalation SHALL emit `iiinb_escalation_ref` linked to `segment_ref` and SHALL hand off to CIL deterministic escalation interface — not to UPI or IMR directly.
18. HLR-20.101-018: IIInB SHALL NOT block Pipeline A waiting for clarification; escalated segments proceed with explicit unknown markers per policy.
19. HLR-20.101-019: IIInB SHALL enforce a maximum of 32 segment spans per turn and 16 rule applications per turn; overflow SHALL use deterministic truncate-with-audit policy.
20. HLR-20.101-020: IIInB SHALL report TCU usage per repair pass and SHALL remain within IIInB budget ranges defined in 20.150.
21. HLR-20.101-021: IIInB behavior SHALL be deterministic and replayable: identical InB output, `usp_version_ref`, and profile state SHALL yield identical repair tags and escalation refs.
22. HLR-20.101-022: IIInB SHALL use fixed reason codes for truncate, USP load failure, cap exceeded, and unsupported-profile outcomes.
23. HLR-20.101-023: IMR SHALL NOT invoke IIInB, UPI, or clarification in the same cycle.
24. HLR-20.101-024: IIInB SHALL NOT read or write Pipeline B envelopes (`exec_plan`, `exec_trace`).
25. HLR-20.101-025: IIInB requirements SHALL satisfy and SHALL NOT weaken parent invariants in 20.10 and 20.30 or reopen 20.100 InB non-goals.
26. HLR-20.101-026: IIInB SHALL remain fully testable via fixtures: profile off (skip), empty USP (escalate only), rule apply, multi-rule precedence, cap truncate.
27. HLR-20.101-027: IIInB audit exports SHALL use canonical field ordering per 20.95.
28. HLR-20.101-028: IIInB diagnostic records SHALL be consumable by MB without mutating repair state.

## Non-Goals (Scaffold and Phase B)
This module **SHALL NOT**:
- Own surface canonicalization (InB / 40.100)
- Write or commit USP rules (UPI / 40.103)
- Wire CIL FIFO or clarification resolution (deferred Wave 2)
- Mutate `semantic_core`, `TP.TR`, or MTP meaning fields
- Perform post-output IMR correction
- Implement full TCU budget enforcement (20.150) in playground fixtures
- Bypass GB supervisory gates for global behavior

## Risks & Unknowns to Investigate
- **`FAIL_ENVELOPE` negative fixtures (deferred):** Replay-verdict tests for forbidden writes to `semantic_core`, `TP.TR`, MTP, and Pipeline B envelopes (`exec_plan`, `exec_trace`) are deferred to [40.510-207](../40.510_refactor.md) (Wave 2 extension of this module). Phase B v0.1 covers positive `envelope_guard` checks only; Test Matrix row `FAIL_ENVELOPE guard` tracks closure.
- Full CIL escalation wire shape and FIFO ordering at IIInB boundary
- Multi-rule precedence edge cases under overlapping patterns
- TCU reporting fidelity vs 20.150 Stage 3 row
- Integration with live InB handoff object from 40.100 (beyond harness fixtures)
- Conversation-scoped audit storage vs in-memory playground records (HLR-016)
- Cross-turn USP version pinning when UPI commits new rules (Wave 2)

## Required Next Step
GATE-A closed 2026-06-08 (40.510-101). Next: W1 30-series normalize + 50 insight per [40.510](../40.510_refactor.md) §4.2.2. Deferred: HLR-024b `FAIL_ENVELOPE` negatives (40.510-207), integrated strip replay with 40.207, 30-series promotion for HLR-013/023/025 residuals.

## Traceability
- 20.101_iiinb_requirements.md (complete source of the 28 HLRs reproduced above)
- 20.100_inb_requirements.md (upstream InB; handoff)
- 20.102_usp_requirements.md (read-only USP snapshot)
- 20.105_tp_requirements.md (intake-bound TP fields §3.4)
- 20.38_ts_implementation_guidelines.md §6 (intake path)
- 20.33_cil_requirements.md (escalation target — Wave 2)
- 20.150_tcu_budgeting_requirements.md (TCU budget)
- 20.95_ts_numeric_policy.md (canonical ordering)
- 40.100_inb_prototypes (upstream handoff evidence)
- 40.20_master_program_guide.md (workflow guidance — not treated as requirements)
- 40.510_refactor.md (W1 row 40.510-101)
- 40.101_iiinb_prototypes/prototype.py (implemented skeleton)
- 40.101_iiinb_prototypes/harness.py (19-scenario harness)
- 40.101_iiinb_prototypes/verification_capsule.md
- 40.101_iiinb_prototypes/requirements_delta.md
- 40.101_iiinb_prototypes/artifacts/iiinb_verification_run_2026-06-08.json

**Note on authority**: The full HLR list from 20.101 is included in this 40.xx playground document solely for exploratory clarity. 20.xx documents remain the authoritative source of truth. 30.xx provides the coverage audit. This document makes no claim to canonical status.

---

## W2 Phase A Extension (40.510-207)

**Approval State:** Phase A extension **draft — pending review** (W1 Phase B 19/19 PASS remains baseline).

**Program row:** [40.510-207](../40.510_refactor.md) — envelope write-guard **negative** tests and `FAIL_ENVELOPE` replay verdicts (HLR-20.101-024b).

### Purpose (W2 delta)

Extend IIInB harness with falsifiable **negative** scenarios proving no writes to forbidden fields under violation attempts:

- `semantic_core`
- `TP.TR`
- `exec_plan` / `exec_trace`

Positive guard (024a) is W1-closed (`positive_pipeline_b_envelope_unchanged`). W2 adds negative paths producing `FAIL_ENVELOPE` replay verdicts per [20.38](../../20_requirements/20.38_ts_implementation_guidelines.md) §8, exercised in [40.207](../40.207_replay_prototypes/software_description.md) strip/regen compose.

### What Phase B Must Explore (W2)

| Scenario | HLR anchor | Expected |
|----------|------------|----------|
| `negative_forbidden_semantic_core_write` | 024b, 20.38 §8 | Detect + `FAIL_ENVELOPE` |
| `negative_forbidden_tp_tr_write` | 024b | Detect + `FAIL_ENVELOPE` |
| `negative_forbidden_exec_plan_write` | 024b | Detect + `FAIL_ENVELOPE` |
| `positive_envelope_guard_regression` | 024a | W1 positive scenarios still PASS |
| `positive_live_usp_from_40.102` | 005–008 | Read-only snapshot from USP module |

### Dependencies
- [40.102_usp_prototypes](../40.102_usp_prototypes/software_description.md) (live USP snapshot path)
- [40.392_core_data_structs_prototypes](../40.392_core_data_structs_prototypes/software_description.md) (shared struct alignment)

### Flows Alignment (W2 extension)
- **Forward Flow:** 20.101-024b, 20.38 §8, [50.101](../../50_thought_simulator_design/50.101_iiinb_design_spec.md) 024a/024b split
- **Backward Flow:** W1 30.101 / 30.207 positive evidence — extend only
- **Iterative Design Flow:** 50.101 documents 024b in 30.207 scope

**Agreement Statement:** Provisionally aligned — W2 extension must not weaken 024a; negative scenarios are additive harness rows in the same module.
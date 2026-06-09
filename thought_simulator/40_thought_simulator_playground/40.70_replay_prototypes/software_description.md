# 40.70_replay_prototypes / software_description.md

## Approval State
- Phase A (software_description): **approved** (CP review, 2026-06-08)
- Phase B (prototype + harness + evidence): **approved** (18/18 PASS; CP review, 2026-06-08; 40.510-102)

## Phase B Deliverables (Executed)
- Harness executed 18 scenarios; artifact: `artifacts/replay_class7_verification_run_2026-06-08.json`
- Evidence types (per 40.160): behavioral, structural (intake path, fixture IDs, B envelope guards), negative (regen input / forbidden lane_id), replay, golden diff (strip + diagnostic export digests)
- Core invariants demonstrated: C7-A..E (live + simulated), E1 strip scope and `semantic_core` retention, Class 7 suite determinism, intake path ordering, Class 1 strip demo, regen input validation + fixture-root merge, `b_regeneration_equivalent` scaffold, B envelope `lane_id`/`tp_id` guard, replay diagnostic export ordering
- HLR coverage (exploratory, with harness evidence): 20.36-017, 018, 021, 053, 058–062; 20.207-001, 004, 007, 017, 019, 020, 028, 029
- Remaining exploration: Classes 2–6 full runners, live E2 regeneration execution, live UPI/GB/CIL for C7-D/E, YAML golden import — see Test Matrix
- Note: The full HLR list from 20.207_execution_replay_specification.md is included below for exploratory visibility. 20.xx remains the sole source of truth; 30.xx remains the authoritative coverage audit layer. 40.70 is a playground and not authoritative.

## Scaffold Metadata
- scaffold_status: implemented (Phase B complete, 18/18 PASS)
- intended_20_anchor: thought_simulator/20_requirements/20.36_canonical_end_to_end_trace.md §9 (primary — REPLAY_CLASS_7)
- intended_20_secondary: thought_simulator/20_requirements/20.207_execution_replay_specification.md (E1/E2/E3 replay modes; Class 1 `b_regeneration_equivalent`)
- intended_10_10_anchors:
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md (deterministic cycle; replay under frozen meaning)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.20_interprocess_communication_and_channels.md (immutable snapshots; strip/regen as snapshot transforms)
  - thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md (envelope write authority; B artifacts not meaning authority)
- upstream_playground_modules: 40.50_inb_prototypes, 40.60_iiinb_prototypes (live intake path for C7 runners)
- applicability: exploratory **replay harness** for Track H Class 7 (W1 GATE-A) and E1 strip-replay demo; orchestration host for Classes 1–7 deferred to W5 (40.90, 40.80)
- disposition_target: promote
- program_wave: **W1** (Track H intake / GATE-A) + **W5** feeder (strip-replay glue per 40.510-505–506)

## Purpose

This scaffold reserves the module slot for exploratory implementation of a **unified replay harness** starting with **REPLAY_CLASS_7** (Track H input correction) per [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §9.

It provides runnable golden-minimum fixtures **C7-A..E** that exercise the intake path through [40.50](../40.50_inb_prototypes/software_description.md) InB and [40.60](../40.60_iiinb_prototypes/software_description.md) IIInB, asserting replay equivalence, envelope isolation, and cross-turn USP visibility policies from [20.101](../../20_requirements/20.101_iiinb_requirements.md).

The harness also demonstrates **E1 strip replay** (remove `exec_plan` + `exec_trace`; retain `semantic_core`) per [20.207](../../20_requirements/20.207_execution_replay_specification.md) HLR-20.207-001 and 20.207-019 — full dual-pipeline Classes 1–6 and E2 regeneration are **out of W1 scope** and deferred to Phase 5 / W5.

**W1 ordering context:** Class 7 verifies Track H replay **before** full conversation-layer wiring; C7-D/E use **simulated** UPI/GB commit outcomes at playground depth.

**GATE-A W1 scope:** [40.510](../40.510_refactor.md) row 40.510-102 requires **REPLAY_CLASS_7 only** for Wave 1 closure — not Classes 1–6. Per [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) HLR-20.036-063, Class 7 is required for Track H sign-off; Classes 1–5 remain dual-pipeline PoC scope (HLR-20.036-016) and are deferred to W5.

The replay harness is responsible for:
- Loading and executing C7-A..E fixture runners with falsifiable assertions per 20.36 §9
- Composing InB → IIInB intake paths via upstream 40.50/40.60 prototypes
- Emitting `replay_class`, `fixture_id`, `sub_id`, per-assertion pass/fail, and artifact JSON per 40.160 evidence standards
- Providing `strip_b_envelopes()` for E1 strip scope `[exec_plan, exec_trace]`
- Computing canonical JSON digests (20.95 ordering) for replay diff baselines
- Preserving deterministic replay: identical inputs → identical assertion outcomes and digests

The replay harness **does not**:
- Own InB or IIInB repair semantics (40.50, 40.60)
- Execute full Pipeline B regeneration (E2) in W1 — owned normatively by 20.207; implementation deferred
- Run Classes 1–6 in W1 — deferred to 40.90 / 40.80 (W5)
- Wire live UPI/GB/CIL FIFO in C7-D/E — simulated snapshots only until Wave 2
- Use B artifacts as meaning authority (forbidden per 20.207-008 family)

## Scope
- exploratory module for requirements-driven **Class 7** replay prototyping on Track H intake (GATE-A)
- initial prototype + harness implemented (`prototype.py`, `harness.py`); evidence in `verification_capsule.md` and `requirements_delta.md`
- continues to explore 20.36 Class 7 HLRs and the 20.207 replay equivalence model below
- Classes 1–6, E2 `b_regeneration_equivalent`, and YAML golden import deferred to W5 per [40.510](../40.510_refactor.md)

All exploration **SHALL** remain deterministic, falsifiable, and artifact-backed. The full 20.207 HLR list is reproduced for exploratory visibility; Class 7 mapping is in the Test Matrix.

## Flows Alignment Statement

- **Forward Flow (10/20-series)**: Driven by [20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §9 (REPLAY_CLASS_7 golden minimums, C7-A..E assertions, strip_scope), [20.207](../../20_requirements/20.207_execution_replay_specification.md) (E1/E2/E3 equivalence classes, regeneration inputs, verdict taxonomy), [20.101](../../20_requirements/20.101_iiinb_requirements.md) (Track H repair replay pinning), [20.100](../../20_requirements/20.100_inb_requirements.md) (InB surface norm), and [20.38](../../20_requirements/20.38_ts_implementation_guidelines.md) §6 (intake path). Upstream playground: 40.50, 40.60.

- **Backward Flow (40-series evidence)**: Phase B complete (2026-06-08): 18/18 harness PASS. Artifact: `artifacts/replay_class7_verification_run_2026-06-08.json`. Capsule: `verification_capsule.md`; delta: `requirements_delta.md`.

- **Iterative Design Flow (50-series influence)**: None yet; full orchestration and E2 regen deferred to W5 per 40.510.

**Agreement Statement**: Aligned — Phase B approved (CP review, 2026-06-08; 18/18 PASS). GATE-A replay scope closed for REPLAY_CLASS_7 + E1 strip + regen scaffold. Residual gaps (Classes 2–6, live E2, live C7-D/E wire, YAML import) named in `requirements_delta.md`.

## Phase A Deliverables (this document)
- High-level description of 40.70 as Class 7 replay harness (W1) with W5 feeder role
- Mapping of 20.36 §9 + 20.207 intent to skeleton responsibilities
- Full reproduction of the 20.207 HLR set for exploratory visibility (see "HLR Reference (Exploratory Visibility)")
- Class 7 fixture contract skeletons (C7-A..E), strip-replay contract, digest definition, verdict taxonomy draft, test matrix
- Cross-links to upstream 40.50/40.60 intake evidence

## Class 7 Fixture Contract (Draft Skeleton)

Per 20.36 §9 golden minimums. Playground runners map 1:1 to sub-IDs:

| Sub-ID | `fixture_id` | Runner | Mode | Primary assertion |
|--------|--------------|--------|------|-------------------|
| C7-A | `REPLAY_C7_PROFILE_DISABLED` | `run_c7_a` | live (40.50/40.60) | Zero Track H stages; no USP load |
| C7-B | `REPLAY_C7_USP_RULE_APPLY` | `run_c7_b` | live | `repair_outcome = APPLIED`; replay equivalent |
| C7-C | `REPLAY_C7_ESCALATE_NO_GUESS` | `run_c7_c` | live | Escalation refs; no guess |
| C7-D | `REPLAY_C7_CLARIFY_COMMIT_CROSS_TURN` | `run_c7_d` | **simulated UPI/GB** | Cross-turn `usp_version_ref` visibility |
| C7-E | `REPLAY_C7_GB_VETO_COMMIT` | `run_c7_e` | **simulated UPI/GB/CIL** | Veto — no ACTIVE rule; snapshot unchanged |

Common fixture fields:

```
class_7_fixture = {
  "replay_class": "REPLAY_CLASS_7",
  "fixture_id": str,
  "sub_id": "C7-A" | "C7-B" | "C7-C" | "C7-D" | "C7-E",
  "profile_enabled": bool,
  "strip_scope": ["exec_plan", "exec_trace"],
  "assertions": { ... },   # falsifiable booleans
  "pass": bool,
}
```

## Strip Replay Contract (E1 — Draft)

Per 20.207-001, 20.207-019 and 20.36 Class 1 strip tests:

```
strip_scope = ["exec_plan", "exec_trace"]

stripped_trace = strip_b_envelopes(full_trace)
# semantic_core, input_repair_tags, intake-bound fields retained
# B envelopes removed for A-only replay diff
```

E1 strip assumes intake-bound fields and `semantic_core` are unchanged by Track H repair — enforced upstream by [40.60](../40.60_iiinb_prototypes/software_description.md) envelope guard (`envelope_guard.semantic_core_unchanged`, `tp_tr_unchanged`; see C7-B/C assertions).

**Playground W1 scope:** `strip_replay_invariant` harness scenario verifies removal only. Full `semantic_core_replay_equivalent` across A-only replay deferred to Classes 1–5 (W5).

## Regeneration Input Skeleton (E2 — Draft, deferred)

Per 20.207 §2.1 — not executed in W1; documented for Phase 5 / Class 1 `b_regeneration_equivalent`:

```
regeneration_input = {
  "commit_id": str,
  "semantic_snapshot_ref": str,
  "routing_epoch_id": str,
  "seed_scope_ref": str,
  "cycle_id": str,              # MAY merge from fixture root
  "policy_signature": str,
  "execution_signature": str,
  "published_routing_tables": {},
}
```

## Canonical Digest (Definition)

Deterministic replay fingerprint for stripped traces and Class 7 outcomes:

- **Algorithm:** SHA-256 over canonical JSON (`sort_keys=True`, compact separators), UTF-8 encoded — per 20.95 / 20.36-018
- **Function:** `canonical_json_digest(payload)` in `prototype.py`
- **Replay contract:** identical fixture inputs → identical digests and assertion maps

## Replay Verdict Taxonomy (Draft)

Extends 20.36 / 20.207 §8 for harness reporting:

| Verdict | Meaning | W1 usage |
|---------|---------|----------|
| `PASS` | All assertions in sub-scenario satisfied | C7-A..E, strip demo |
| `FAIL_ASSERTION` | One or more Class 7 assertions false | harness exit 1 |
| `FAIL_REGEN_DIFF` | E2 equivalence failure | deferred (20.207-013) |
| `FAIL_REGEN_INPUT` | Incomplete `regeneration_input` | `negative_regen_input_incomplete` |
| `FAIL_REGEN_FORBIDDEN_READ` | TP / `lane_id` in regen path | `negative_regen_forbidden_lane_tp` |
| `SCAFFOLD_DEFERRED` | E2 scaffold passed; execution W5 | `scaffold_b_regeneration_equivalent` |

## Minimal Internal State

**May hold (per run):**
- Dynamically loaded 40.50 / 40.60 prototype modules (importlib)
- Ephemeral InB/IIInB instances per sub-scenario

**Must not hold:**
- Cross-run mutable replay caches that affect determinism
- Live UPI/GB/CIL mutable stores (simulated dicts only in C7-D/E)

**Persistence:** each harness invocation writes a fresh artifact JSON; no in-repo mutation of golden fixtures.

## Test Matrix
| Category | Scenario (harness) | Mode | HLR anchors | Status |
|----------|-------------------|------|-------------|--------|
| Profile disabled (C7-A) | `replay_c7_a_profile_disabled` | live | 20.36-059 | PASS |
| USP rule apply (C7-B) | `replay_c7_b_usp_rule_apply` | live | 20.36-058, 060 | PASS |
| Escalate no guess (C7-C) | `replay_c7_c_escalate_no_guess` | live | 20.36-058, 060 | PASS |
| Cross-turn USP (C7-D) | `replay_c7_d_cross_turn_usp` | simulated UPI/GB | 20.36-061 | PASS |
| GB veto (C7-E) | `replay_c7_e_gb_veto` | simulated UPI/GB/CIL | 20.36-062 | PASS |
| E1 strip invariant | `positive_strip_replay_invariant` | — | 20.207-001, 019 | PASS |
| Strip semantic_core retained | `positive_strip_semantic_core_retained` | — | 20.207-001, 20.36-060 | PASS |
| Strip digest deterministic | `positive_strip_digest_deterministic` | — | 20.36-018 | PASS |
| Class 7 suite deterministic | `positive_class7_suite_deterministic` | — | 20.36-058 | PASS |
| C7-B intake path order | `positive_c7_b_intake_path_order` | live | 20.36-058, 20.101-003 | PASS |
| Class 1 strip demo | `positive_class1_strip_semantic_core_stable` | — | 20.36-021, 20.207-001 | PASS |
| Regen input incomplete | `negative_regen_input_incomplete` | — | 20.207-004, 028 | PASS |
| Regen forbidden lane/tp | `negative_regen_forbidden_lane_tp` | — | 20.207-007, 029, 20.36-053 | PASS |
| E2 regen scaffold | `scaffold_b_regeneration_equivalent` | scaffold | 20.207-017, 020 | PASS |
| Regen fixture-root merge | `positive_regen_merge_from_fixture_root` | — | 20.207-004 | PASS |
| B envelope no lane/tp | `positive_b_envelope_no_lane_tp` | — | 20.36-053, 20.207-007 | PASS |
| Class 7 fixture IDs | `positive_class7_fixture_ids` | — | 20.36-017 | PASS |
| Replay diagnostic export | `positive_replay_diagnostic_export` | — | 20.36-018 | PASS |
| Class 2–5 full runners | *(deferred)* | — | 20.36 Classes 2–5 | todo (W5) |
| Live E2 regeneration | *(deferred)* | — | 20.207-002..016 | todo (W5) |
| REGEN_STALE_EPOCH negative | *(deferred)* | — | 20.207-030 | todo (W5) |
| Live UPI/GB C7-D/E wire | *(deferred)* | simulated | 20.36-061, 062 | todo (W2) |
| YAML golden import | *(deferred)* | — | 20.36-017, 018 | todo (W5) |

## HLR Reference (Exploratory Visibility) — 20.207

Phase-A evidence for Class 7 is in the Test Matrix; full 20.207 HLRs are retained for E2/W5 planning. Source: 20.207_execution_replay_specification.md.

### Equivalence classes (§1)
1. HLR-20.207-001: E1 strip replay SHALL NOT require Pipeline B execution and SHALL NOT use regenerated B artifacts as meaning authority.
2. HLR-20.207-002: E2 regeneration replay SHALL execute Pipeline B only against a frozen `semantic_snapshot_ref` identified by `commit_id`.
3. HLR-20.207-003: E3 replay SHALL treat post-correction `semantic_core` changes as Pipeline A writes; E2 for cycle N SHALL use pre-correction snapshot unless fixture tests post-correction B passes.

### Regeneration inputs (§2)
4. HLR-20.207-004: E2 regeneration SHALL reject inputs missing any required field (after fixture-root merge) with `REGEN_INPUT_INCOMPLETE`.
5. HLR-20.207-005: E2 regeneration SHALL reject `semantic_snapshot_ref` not resolving to `commit_id` with `REGEN_COMMIT_MISMATCH`.
6. HLR-20.207-006: E2 regeneration SHALL reject stale `routing_epoch_id` with `REGEN_STALE_EPOCH`.
7. HLR-20.207-007: E2 regeneration SHALL NOT read TP instances, `tp_id`, or `lane_id`.
8. HLR-20.207-008: Regeneration SHALL perform B stage replay in 20.36-005 order (or equivalent deterministic replanning).

### Regeneration outputs (§3)
9. HLR-20.207-009: E2 regeneration SHALL produce regenerated `exec_plan`, `exec_trace`, and `xp_record` bound to same `commit_id` and `cycle_id`.
10. HLR-20.207-010: Regenerated `xp_id` MAY differ; equivalence on envelope content, not surrogate IDs.
11. HLR-20.207-011: Regenerated envelopes SHALL NOT be written into `semantic_core` or MTP meaning fields.
12. HLR-20.207-012: PoC harnesses SHALL implement at minimum byte-identical `exec_plan` compare; `exec_trace` MAY use content-hash equivalence.
13. HLR-20.207-013: Regeneration equivalence failure SHALL emit `replay_verdict = FAIL_REGEN_DIFF` with deterministic diff artifact.

### Regeneration procedure (§4)
14. HLR-20.207-014: Regeneration SHALL NOT skip IMR evaluation when baseline includes IMR unless `imr_eval_excluded = true`.
15. HLR-20.207-015: Type A IMR retry passes SHALL regenerate with matching `xp_pass_seq` and equivalent per-pass `exec_plan`.
16. HLR-20.207-016: Type B `CorrectionTrigger` in `exec_trace` SHALL regenerate identically; E2 SHALL NOT apply Type B corrections to `semantic_core`.

### 20.36 relationship (§5)
17. HLR-20.207-017: PoC acceptance SHALL require E1 strip pass on 20.36 Classes 1–5; E2 pass required on at least one Class 1 fixture via `b_regeneration_equivalent`.
18. HLR-20.207-018: Dedicated `REPLAY_CLASS_6` full regeneration suite MAY be added; not mandatory for initial PoC if 017 satisfied via Class 1.
19. HLR-20.207-019: E1 strip scope SHALL remain `[exec_plan, exec_trace]` (and `xp_record` per 20.205); regen scope includes all B envelopes but excludes `semantic_core` body comparison except identity check.
20. HLR-20.207-020: `b_regeneration_equivalent` SHALL execute: capture baseline → strip → regenerate from `regeneration_input` → compare per §3.1.

### Seed and epoch (§6)
21. HLR-20.207-021: Identical `seed_scope_ref` and `routing_epoch_id` with identical `regeneration_input` SHALL produce equivalent regenerated B envelopes.
22. HLR-20.207-022: Different `seed_scope_ref` with identical frozen snapshot SHALL produce different `exec_trace` expression selections where seed-bound AND identical stripped `semantic_core`.
23. HLR-20.207-023: Different `routing_epoch_id` MAY produce different `exec_plan` triples; regen SHALL document epoch table version in diff artifacts.

### IMR and supervisory (§7)
24. HLR-20.207-024: Regenerated `imr_record` entries SHALL preserve `trigger_type`, signal codes, `correction_trigger_id` presence, and cap status semantics.
25. HLR-20.207-025: Regeneration of cycles with Type B triggers SHALL NOT execute subsequent A correction as part of E2.
26. HLR-20.207-026: Regenerated supervisory trigger queue entries SHALL be equivalent in effect class and target fields.

### Verdict taxonomy (§8)
27. HLR-20.207-027: Harnesses implementing E2 SHALL emit fixed verdicts (`PASS`, `FAIL_REGEN_DIFF`, `FAIL_REGEN_INPUT`, `FAIL_REGEN_EPOCH`, `FAIL_REGEN_FORBIDDEN_READ`) for CI export.

### Negative fixtures (§9)
28. HLR-20.207-028: `REGEN_NO_COMMIT` → `FAIL_REGEN_INPUT`.
29. HLR-20.207-029: `REGEN_TP_READ` → `FAIL_REGEN_FORBIDDEN_READ`.
30. HLR-20.207-030: `REGEN_STALE_EPOCH` → `FAIL_REGEN_EPOCH`.

*(HLR-031 through 034 are not present in 20.207 v0.3 frontmatter — 30 HLRs numbered 001–030 in body; frontmatter lists 001–034 for forward compatibility; playground tracks 001–030.)*

## Class 7 HLR Reference (20.36 §9)

58. HLR-20.036-058: Class 7 SHALL verify Track H replay equivalence for identical `(InB output, usp_version_ref, profile_enabled, policy_signature)`.
59. HLR-20.036-059: Class 7 SHALL assert `profile_enabled = false` produces zero Track H stage records and no USP load side effects.
60. HLR-20.036-060: Class 7 SHALL assert IIInB repair tags do not alter `semantic_core` or `TP.TR` vs profile-disabled baseline.
61. HLR-20.036-061: Class 7 multi-turn fixtures SHALL pin `usp_version_ref` and demonstrate cross-turn USP visibility (commit N visible on N+1).
62. HLR-20.036-062: Class 7 SHALL assert GB veto produces no ACTIVE `usp_rule` and identical IIInB behavior vs pre-commit snapshot.
63. HLR-20.036-063: Class 7 is optional for dual-pipeline PoC; required for Track H sign-off per 20.510.
64. HLR-20.036-064: Class 7 `strip_scope` removes conversation-layer audit only when testing A equivalence; intake-bound TP fields remain in diff scope.

## Non-Goals (Scaffold and Initial Phase B)
This module **SHALL NOT** (in W1):
- Replace 40.90 unified experiment runner (W5)
- Execute E2 Pipeline B regeneration without frozen `semantic_snapshot_ref`
- Import normative YAML golden files from 20.36 in W1 (inline runners only)
- Wire live UPI/GB/CIL for C7-D/E (simulated until Wave 2)
- Use regenerated or stripped B artifacts as meaning authority

## Risks & Unknowns to Investigate
- **C7-D/E simulation fidelity:** Cross-turn and veto paths use snapshot simulation, not live 40.90/40.130 prototypes — Wave 2 integration required for production-grade replay
- **Classes 1–6 gap:** GATE-A requires Class 7 only; dual-pipeline PoC still needs Classes 1–5 per 20.36-016 (W5)
- **E2 `b_regeneration_equivalent`:** No regen runner in W1; Class 1 sub-assertion deferred to 40.90 / 40.55 cluster
- **YAML fixture import:** Golden files in 20.36 not yet loaded by harness — manual parity with inline runners
- **Strip + A-only equivalence:** `strip_replay_invariant` proves removal only; full byte-identical `semantic_core` diff deferred

## Required Next Step
GATE-A closed 2026-06-08 (40.510-102). Next: W1 30-series normalize + 50 insight per [40.510](../40.510_refactor.md) §4.2.2. W5: Classes 1–6 runners, live E2 `b_regeneration_equivalent`, YAML golden import. W2: wire live UPI/GB for C7-D/E when 40.90/40.130 exist.

## Traceability
- 20.36_canonical_end_to_end_trace.md §9 (REPLAY_CLASS_7)
- 20.207_execution_replay_specification.md (E1/E2/E3)
- 20.101_iiinb_requirements.md, 20.100_inb_requirements.md (Track H)
- 20.206_pipeline_a_b_synchronization_contract.md (equivalence classes)
- 20.95_ts_numeric_policy.md (canonical serialization)
- 40.50_inb_prototypes, 40.60_iiinb_prototypes (upstream intake evidence)
- 40.05_master_program_guide.md (workflow — not requirements)
- 40.510_refactor.md (W1 row 40.510-102; W5 rows 505–506)
- 40.70_replay_prototypes/prototype.py, harness.py
- 40.70_replay_prototypes/artifacts/replay_class7_verification_run_2026-06-08.json

**Note on authority**: The HLR lists above are for exploratory clarity in the playground. 20.xx remains authoritative. 30.xx provides coverage audit. This document makes no claim to canonical status.
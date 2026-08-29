---
status: verification
source_of_truth: this
contains:
  - LLR: [LLR-30.000-001]
---

# 30_verification

This folder is the authoritative verification tier for Thought Simulator modules.

The detailed process, naming conventions, required artifacts (verification capsules, requirements deltas, JSON run artifacts), three-flow requirements, and promotion standards are defined in `30.00_verification_user_guide.md`.

**Authoritative module inventory:** [`30.01_verification_inventory_index.md`](30.01_verification_inventory_index.md).

## Purpose

- store promoted verification capsules
- store deterministic evidence artifacts
- separate verification evidence from exploratory playground work

For user-facing forward/backward flow runbooks and prompt templates, see `../USER_GUIDE.md`.

## Promotion Policy

Promotion into this folder is intentional and manual.

Each promoted module should include:

- a verification capsule
- deterministic replay evidence
- JSON artifacts
- negative-path coverage evidence
- reviewer sign-off metadata

## Controlled Backward Canonical Intake (20 -> 10 -> 30)

Verification updates may be initiated by canonical-anchor changes in `../thought_simulator_req/`.

10-layer disambiguation for this guide:

- `../thought_simulator_req/` = canonical requirement trigger source.
- `00_program_governance/` = architecture/program reference context.

When this guide states "10-layer update" or "update 10", it means `../thought_simulator_req/` unless explicitly qualified.

When those canonical anchors were updated from `../requirements_20/`, intake into this tier must still treat the 10-layer anchor as the normative source and `../requirements_20/` as rationale lineage only.

No-auto-propagation from 20-layer edits:

- changes in `../requirements_20/` alone must not trigger automatic verification updates
- the AI Agent may provide impact analysis and prompt suggestions only
- verification edits begin only after explicit user direction for forward or backward flow

Allowed automatic maintenance (30/40/50 scope, after explicit flow start):

- update `30.30_verification_glossary.md` when terminology in 30/40/50 docs is renamed, added, or deprecated
- update `glossary_term_registry.json` in the same change set as glossary term changes
- repair README and markdown references/paths affected by file rename or section-name changes

Required backward-intake controls:

- explicit flow direction confirmation (`backward`) before edits
- changed canonical anchor list from `../thought_simulator_req/`
- impacted verification capsules and requirement deltas identified before execution
- synchronized terminology check against `30.30_verification_glossary.md`
- lineage note recorded when initiating anchors were promoted from `../requirements_20/`
- automatic backward-flow execution log creation/update under `../thought_simulator_req/docs/`
- automatic post-update integrity check run with result recorded in the backward-flow execution log

Minimum verification-layer integrity check:

- missing or stale requirement references in impacted capsule/delta documents
- terminology mismatch against `30.30_verification_glossary.md`
- missing module-level backward-flow governance section when module docs are in scope

Backward-flow completion dependency for design equivalence:

- downstream design layer must complete full synchronization across all files in `../thought_simulator_design/`
- backward-flow execution log must contain final assertion `Forward-Equivalence State: YES`

If direction is ambiguous (forward vs backward), no verification edits may proceed until explicit human confirmation is recorded.

Minimum confirmation record:

- selected direction (`forward` or `backward`)
- initiating source document(s)
- impacted verification target set

Without confirmation, execution is limited to planning/clarification output only.

## Module inventory

See [`30.01_verification_inventory_index.md`](30.01_verification_inventory_index.md) for the authoritative list of promoted verification modules, governance docs, and promotion status. W1 Track H wave coverage: [`W1_track_h_wave_coverage_note.md`](W1_track_h_wave_coverage_note.md).

CI runs non-blocking warning checks: `validate_30_inventory_index.py` (`30.01` ↔ on-disk `30.*` dirs) and `validate_30_10_50_pairing.py` (`promoted`/`approved` rows ↔ `10.50.{band}_*.md`; one-way only). See [30.00](30.00_verification_user_guide.md) § CI enforcement.

## Directory index (coverage-aligned)

- [30.30_verification_glossary.md](30.30_verification_glossary.md)
- [glossary_term_registry.json](glossary_term_registry.json)
- [30.100_cob_prototypes](30.100_cob_prototypes/)
- [30.110_cil_prototypes](30.110_cil_prototypes/)
- [30.120_cop_prototypes](30.120_cop_prototypes/)
- [30.130_gb_prototypes](30.130_gb_prototypes/)
- [30.140_core_data_structs_prototypes](30.140_core_data_structs_prototypes/)
- [30.150_tp_lifecycle](30.150_tp_lifecycle/)
- [30.160_basin_prototypes](30.160_basin_prototypes/)
- [30.170_ib_prototypes](30.170_ib_prototypes/)
- [30.180_tr_prototypes](30.180_tr_prototypes/)
- [30.190_dcb_stability_prototypes](30.190_dcb_stability_prototypes/)
- [30.200_mb_prototypes](30.200_mb_prototypes/)
- [30.20_verification_of_semantic_specification.md](30.20_verification_of_semantic_specification.md)
- [30.210_scheduler_prototypes](30.210_scheduler_prototypes/)
- [30.220_regulator_prototypes](30.220_regulator_prototypes/)
- [30.230_tick_cycle_skeleton](30.230_tick_cycle_skeleton/)
- [30.240_snapshot_prototypes](30.240_snapshot_prototypes/)
- [30.250_event_log_prototypes](30.250_event_log_prototypes/)
- [30.260_experiment_runner](30.260_experiment_runner/)
- [30.270_math_prototypes](30.270_math_prototypes/)
- [30.30_verification_of_reference_algorithms.md](30.30_verification_of_reference_algorithms.md)
- [30.40_evidence_trace_exemplars_non_normative.md](30.40_evidence_trace_exemplars_non_normative.md)
- [30.50_inb_prototypes](30.50_inb_prototypes/)
- [30.60_iiinb_prototypes](30.60_iiinb_prototypes/)
- [30.70_replay_prototypes](30.70_replay_prototypes/)
- [30.80_usp_prototypes](30.80_usp_prototypes/)
- [30.90_upi_prototypes](30.90_upi_prototypes/)
- [30.tb](30.tb/)
- [W2_conversation_layer_wave_coverage_note.md](W2_conversation_layer_wave_coverage_note.md)

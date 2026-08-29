# Thought Simulator Playground

## Purpose

The playground is a structured exploration space for rapidly testing ideas before promoting them into formal requirements, architecture, and implementation.

It is intentionally separate from production-facing paths so we can iterate quickly, preserve evidence, and make promotion decisions with confidence.

## Governance (process + program)

| Document | Role |
|----------|------|
| [40.05_master_program_guide.md](40.05_master_program_guide.md) | **Process** — how to build modules (capsules, evidence, flows) — Approved v0.12 |
| [40.510_refactor.md](40.510_refactor.md) | **Program** — what to build/redo, phase order, §5 tracking table — Active v0.5 |

Module scheduling and status: **[40.510 §5](40.510_refactor.md)**. Legacy `40.xx` numbering collisions: **[40.510 §3](40.510_refactor.md)** — renumbering prohibited unless a GATE row authorizes it.

## Verification Capsule (Core Process)

Each module maintains a Verification Capsule: a compact, auditable package of design intent, test evidence, failures, and requirement traceability.

Required capsule files per module:

- software_description.md
- prototype.py
- harness.py
- verification_capsule.md
- requirements_delta.md
- artifacts/

Shared playground vocabulary:

- [../verification/30.30_verification_glossary.md](../verification/30.30_verification_glossary.md)

## Workflow

1. Define scope in software_description.md.
2. Draft and evolve prototype.py.
3. Run harness.py for repeatable verification.
4. Record run evidence in verification_capsule.md (command, result, exit code, artifacts, notes).
5. Record failures and invalidated assumptions in verification_capsule.md and requirements_delta.md.
6. Update verification_capsule.md with current status, evidence, and IO fields exercised.
7. Update requirements_delta.md with requirement/design links and change log entries.
8. Decide whether the module is ready to move from exploration to final design.

## Promotion Path: Exploration -> Final Design

A module is promoted when invariants are stable, verification is repeatable, evidence is sufficient, and requirement impacts are explicit.

Promotion sequence:

1. Consolidate validated findings.
2. Update requirement and design documents.
3. Add implementation-grade tests.
4. Integrate into final architecture and codebase.

## Revision Control and Design Release Coupling

Playground artifacts are revision-controlled project assets.

When a design specification in `thought_simulator_design/` cites playground files (for example, `software_description.md`, `verification_capsule.md`, `requirements_delta.md`, or artifact outputs), those cited files become part of the released design evidence for that design version.

Coupling rules:

- requirement intent is authored primarily in `requirements_20/`
- realization-ready requirement anchors are formalized in `thought_simulator_req/` based on selected flow direction
- design documents in `thought_simulator_design/` remain subsystem architectural contracts
- cited playground evidence in `thought_simulator_playground/` remains the auditable verification trail tied to the released design version

Direction control:

- forward flow (typical): 20 -> 40 -> 10
- backward flow (when selected): 20 -> 10 -> 40
- no propagation occurs without explicit user direction.

If cited playground evidence changes materially after promotion:

- update the affected design document version
- update traceability/evidence references
- record the change in the appropriate delta/capsule files

## Module Format Coherence and Exception Policy

To keep the playground coherent and scalable, all numbered module folders under `thought_simulator_playground/` should follow a common verification-capsule structure and naming pattern.

Coherence baseline for module folders:

- `software_description.md`
- `prototype.py`
- `harness.py`
- `verification_capsule.md`
- `requirements_delta.md`
- `artifacts/`

Why this coherence is required:

- consistent onboarding for contributors and external adopters
- consistent verification evidence and traceability across modules
- predictable promotion path from exploration to design release artifacts
- reduced process drift between subsystem teams and module owners

Exception policy for `40.330_math_prototypes/`:

- math prototypes may use a lighter documentation burden while still keeping the same file/folder names where practical
- early mathematical exploration may not immediately impact canonical requirements or design contracts
- when there is no requirement/design impact yet, `requirements_delta.md` may remain concise but should still record that status explicitly

Why the exception exists:

- math research often starts as hypothesis exploration before subsystem contract implications are known
- forcing full design-level delta detail too early increases noise and slows research iteration
- preserving naming compatibility still allows smooth promotion when math findings mature into design-relevant evidence

## Directory Map

*Authoritative inventory and phase assignment: [40.510 §5](40.510_refactor.md). Below is an onboarding index.*

### Program & process docs

- [40.05_master_program_guide.md](40.05_master_program_guide.md) — process owner (how)
- [40.510_refactor.md](40.510_refactor.md) — refactor program inventory (what/when)

### Track H / intake (Pipeline A entry)

- [40.50_inb_prototypes/](40.50_inb_prototypes/) — InB surface normalization (`done` Phase 1)
- [40.60_iiinb_prototypes/](40.60_iiinb_prototypes/) — IIInB `input_semantic_repair` (`done` Phase 1)
- [40.70_replay_prototypes/](40.70_replay_prototypes/) — REPLAY_CLASS_7 C7-A..E harness (`done` Phase 1)

### Conversation layer (B3)

- [40.110_cob_prototypes/](40.110_cob_prototypes/) — COB object promotion
- [40.120_cil_prototypes/](40.120_cil_prototypes/) — CIL clarification FIFO
- [40.340_cop_prototypes/](40.340_cop_prototypes/) — COP async coprocessor

### Meaning carriers & Pipeline A basins (Wave 3 — W3)

- [40.160_tp_lifecycle/](40.160_tp_lifecycle/) — ThoughtPoint lifecycle (W3 redo: intake-bound fields)
- [40.150_mtp_prototypes/](40.150_mtp_prototypes/) — MTP lifecycle; `commit_id` / `mtp_update` *(new W3)*
- [40.170_split_merge_prototypes/](40.170_split_merge_prototypes/) — split/merge; `lineage_delta`; ΔH% *(new W3)*
- [40.180_truth_done_prototypes/](40.180_truth_done_prototypes/) — Truth/Done terminal gate *(new W3)*
- [40.190_rb_prototypes/](40.190_rb_prototypes/) — RB routing; post–IIInB fan-out *(new W3; not 40.50 regulator)*
- [40.200_ob_prototypes/](40.200_ob_prototypes/) — OB lane-local evidence *(new W3; not 40.270 scheduler)*
- [40.210_dcb_prototypes/](40.210_dcb_prototypes/) — DCB geometric meta-basin *(new W3)*
- [40.230_tb_prototypes/](40.230_tb_prototypes/) — TB interpretation *(new W3; not 40.60 tick skeleton)*
- [40.260_basin_prototypes/](40.260_basin_prototypes/) — generic basin (W3 full redo → normative A basins)
- [40.250_ib_prototypes/](40.250_ib_prototypes/) — inquiry basin (W3 extension: escalation routing)
- [40.240_tr_router_prototypes/](40.240_tr_router_prototypes/) — Thought Router (W3 extension: DCB/TR gating)
- [40.220_dcb_stability_prototypes/](40.220_dcb_stability_prototypes/) — DCB stability qualitative (W3 implement)

### Governance & diagnostics (B6)

- [40.130_gb_prototypes/](40.130_gb_prototypes/) — Governing Basin supervisory

### Pipeline B & expression (B4)

- [40.140_oub_prototypes/](40.140_oub_prototypes/) — OuB output realization (scaffold)

### Orchestration, replay glue & cross-cutting (B5/B7)

- [40.270_scheduler_prototypes/](40.270_scheduler_prototypes/) — scheduler (*folder*; 20.40 OB uses `40.200_*` when created)
- [40.320_regulator_prototypes/](40.320_regulator_prototypes/) — regulator / ΔH% (*folder*; 20.50 RB uses `40.190_*` when created)
- [40.280_tick_cycle_skeleton/](40.280_tick_cycle_skeleton/) — tick-cycle skeleton (*folder*; 20.60 TB uses `40.230_*` when created)
- [40.290_snapshot_prototypes/](40.290_snapshot_prototypes/) — snapshot patterns
- [40.300_event_log_prototypes/](40.300_event_log_prototypes/) — event log / replay
- [40.310_experiment_runner/](40.310_experiment_runner/) — experiment orchestration
- [40.330_math_prototypes/](40.330_math_prototypes/) — math / entropy experiments (lighter doc burden per exception policy above)

### Shared

- [shared/](shared/) — shared helpers for prototype work

### External vocabulary

- [../verification/30.30_verification_glossary.md](../verification/30.30_verification_glossary.md) — verification terms
- [../requirements_20/20.190_glossary.md](../requirements_20/20.190_glossary.md) — primitive intent catalog

## Directory index (coverage-aligned)

- [40.100_core_data_structs_prototypes](40.100_core_data_structs_prototypes/)
- [40.80_usp_prototypes](40.80_usp_prototypes/)
- [40.90_upi_prototypes](40.90_upi_prototypes/)
- [archive](archive/)
- [Grok_comment.md](Grok_comment.md)

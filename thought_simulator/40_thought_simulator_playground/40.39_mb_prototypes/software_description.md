# 40.39_mb_prototypes / software_description.md

## Approval State
**Phase A passed (explicit).** Phase B implementation executed under forward flow (20.70 → 40.39).

**2026-06-05 Phase B execution:** Harness with 8 scenarios exercising the canonical MB input→output contract, drift observation, what-if flagging, visibility modes, overflow canonical schema, reproducibility, and lifecycle observability. All scenarios PASS (see artifact). Artifact written to `artifacts/mb_verification_run_2026-06-05.json`. Full three-flow statements recorded in delta + capsule.

Scaffold status removed; this document now records completed Phase A + Phase B per 40.20.

## Scaffold Metadata
- scaffold_status: planned
- intended_20_anchor: thought_simulator/20_requirements/20.70_mb_requirements.md
- intended_10_10_anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.10_system_architecture.md
- applicability: planned exploratory module for Monitoring Basin (MB) non-intrusive diagnostics, drift observation, and stability reporting
- disposition_target: promote

## Purpose
This scaffold reserves the module slot for future exploratory implementation of the Monitoring Basin (MB) prototype in the 40-layer.

It corresponds directly to `20.70_mb_requirements.md` (36 HLRs defining deterministic Monitoring Basin behavior for non-intrusive diagnostics, drift observation, stability reporting, and bounded what-if supervision).

MB provides structured observability and advisory monitoring outputs **without mutating TS core meaning-construction state** (TP, MTP, OB, RB, TB).

## Scope
- placeholder module for requirements-driven exploration of the full HLR-20.070-* set
- no executable behavior, no algorithms, and no numeric policy asserted yet
- exploration focus: deterministic telemetry I/O objects, drift observation over state deltas, visibility-controlled sampling, overflow/degradation telemetry (per 20.30 canonical schema), explicitly flagged + policy-gated what-if probes, reproducibility, lineage/provenance, bounded history, TCU-aware diagnostics, and strict non-intrusion

## Flows Alignment Statement

- **Forward Flow (20-series)**: Driven by the complete 20.70 MB Requirements (HLR-20.070-001 to HLR-20.070-036) plus supporting invariants from 20.30_ts_functional_model.md (overflow schema §8.3, determinism, non-intrusion, lifecycle logging) and 20.10 architectural principles.

- **Backward Flow (40-series evidence)**: No evidence collected yet; this is the initial scaffold. Related prior 40-series observability work (e.g. event log, snapshot prototypes) may provide reusable patterns for telemetry but has not been integrated into an MB prototype.

- **Iterative Design Flow (50-series influence)**: Placeholder. No dedicated 50.39 yet. 50.05_software_spec_construction_guide.md lists MB as component .39. Any future 50.80 logging/observability or 50.05 updates may drive targeted iterations back into this module.

**Agreement Statement**: Scaffold stage only. The three flows are provisionally aligned on MB as a strictly non-intrusive, deterministic, advisory-only observability layer. Full alignment (including explicit three-flow statements in all three core docs) will be recorded after Phase A approval of this software_description and after Phase B execution produces traceable evidence.

## Phase A Deliverables (this document)
- High-level description of MB diagnostic, drift, stability, and what-if supervision behavior
- Mapping of 20.70 intent and key HLR categories to prototype responsibilities
- Identification of unknowns and open questions
- Clear definition of what Phase B must explore
- No implementation, data structures, or thresholds

## What Phase B Must Explore
Phase B **SHALL** explore and produce concrete (deterministic) evidence for at least:

- Construction of the canonical MB input object (basin telemetry, lane identifiers, lineage/provenance, MTP snapshot fields, stability metadata)
- Emission of the canonical MB output object (diagnostics summaries, drift indicators, advisory recommendations, what-if flags, execution diagnostics, telemetry)
- Deterministic drift observation over semantically relevant state deltas across cycles
- Visibility modes (low/medium/high/full) and their effect on sampling density + deterministic user notifications for cost impact
- Overflow and degradation telemetry using the exact 20.30 §8.3 canonical fields (overflow_flag, overflow_type, overflow_source_basin, overflow_cycle, truncated_fields, ΔH%_normalization_applied, tcu_overrun_amount, etc.)
- Explicit flagging, policy-gating, and logging of any what-if / probe / split actions (HLR-20.070-007/008/026)
- Reproducibility: identical effective input + MTP context + seed-bounded state always yields identical MB outputs
- Bounded drift-history depth with explicit retention/eviction
- Non-intrusion invariant: zero direct mutation of core cognitive state
- Test hooks and explicit interfaces sufficient for unit/integration/property-based verification (HLR-20.070-012/013)
- Lifecycle transition logging (entry/running/exit)

## Non-Goals (Scaffold and Initial Phase B)
This module **SHALL NOT**:
- Mutate TP, MTP, OB, RB, or TB core meaning-construction state (HLR-20.070-003)
- Perform semantic interpretation or evidence extraction that belongs to OB/TB
- Issue authoritative supervisory actions (GB territory)
- Define final numeric TCU budgets, visibility policies, or retention windows (those belong in 20.95 / appropriate 50-series)
- Use probabilistic inference, hallucinated reconstruction, or nondeterministic effects

## Risks & Unknowns to Investigate (aligned with 20.10 §1.14)
- Telemetry volume and TCU consumption under high-visibility modes or long drift histories
- Interaction between MB visibility controls and overall pipeline determinism / replay
- Safety of what-if probes (guaranteeing they stay advisory and explicitly flagged)
- Clean separation of MB diagnostics from GB supervision and IB population monitoring
- Memory growth and eviction policy correctness for drift history under continuous operation

## Phase B Deliverables (Executed - 2026-06-05)
- `prototype.py`: `MonitoringBasin` class implementing deterministic `evaluate(MBInput) -> MBOutput`; **now fully implements 10.50.39 Canonical Schemas** (schema_version, full overflow always, etc.) after final alignment.
- `harness.py`: 8 scenarios covering all items listed under "What Phase B Must Explore".
- `artifacts/mb_verification_run_2026-06-05.json`: full structured report with per-scenario status, output summaries, and three-flow note.
- `requirements_delta.md` and `verification_capsule.md` refreshed with evidence, HLR mapping, and explicit three-flow statements.

All outputs are read-only / non-mutating and 100% deterministic.

## Required Next Step (post Phase B)
Populate / promote evidence to matching 30.39 (if desired) and feed findings into 50.05 / future 50.39 or 50.80. 10.50.39 has been updated (v0.2) with canonical schemas + HLR-011..017 per design review.

Continue to respect non-intrusion (HLR-20.070-003) and determinism invariants in any follow-on work.

## Traceability
- thought_simulator/20_requirements/20.70_mb_requirements.md (primary source — all 36 HLR-20.070-*)
- thought_simulator/20_requirements/20.30_ts_functional_model.md (overflow schema, pipeline placement)
- ../40.20_master_program_guide.md (standard structure + three-flow requirement)
- 50.05_software_spec_construction_guide.md (MB listed as component .39)
- 30_verification/30.39_mb_prototypes/ (promoted per 30.00)
- 20.10_ts_architectural_principles.md (non-intrusion, supervision boundaries)

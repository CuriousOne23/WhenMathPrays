# Requirements Delta

## Flows Alignment Statement (per 40.20)

- **Forward Flow (10/20-series)**: Driven by the detailed architecture in 10.10.40_scheduler_and_regulator_architecture.md (regulator role, ΔH% / fan-out / cost / overflow / memory / cycle time enforcement, interrupt generation, separation) and the listed 20-series sources in the 40.50 software_description.md (TCU budgeting, safety constraints, functional model fan-out/overflow, OB/IB bounds and TCU, parameter table enforcement, traceability).
- **Backward Flow (40-series evidence)**: No evidence collected yet; this is the initial scaffold. Preliminary prototype/harness exist but full Phase B evidence collection awaits Phase A approval.
- **Iterative Design Flow (50-series influence)**: Downstream 10.50.50_regulator_requirements.md (HLR-20.450-001..003 + TCU) and 50.50_regulator_design_support.md exist as anchors. This scaffold (and future Phase B) can explore and provide evidence to refine or validate those.

**Agreement Statement**: Scaffold stage only. The three flows are provisionally aligned on the regulator as the non-cognitive, deterministic safety/resource enforcement layer. Full alignment will be recorded after Phase A approval and Phase B execution.

## Proposed Requirement Changes

- Add regulator-specific requirement anchors for deterministic decision replay and policy-mode behavior.
- Add explicit negative-path requirements for invalid policy mode and invalid numeric pressure input.

## Rationale

- Executed harness evidence now confirms deterministic replay and expected policy differentiation.
- Promotion still requires canonical requirement IDs tied to this evidence.
- Phase A software_description now provides the detailed mapping and "What Phase B Must Explore" per 40.20.

## Impacted Documents

- `software_description.md` (now full Phase A per 40.20)
- `verification_capsule.md`
- future canonical requirement anchor under `10_thought_simulator_req/`

## Open Validation Needed

- Confirm minimum regulator decision schema for canonical audit/replay requirements.
- Define tie-break requirements when multiple regulator actions compete.

## Phase B Evidence Snapshot

- Harness result: PASS
- Artifact: `artifacts/regulator_verification_run_2026-05-28.json`
- Scenario outcomes:
	- `positive_deterministic_replay` PASS
	- `positive_policy_comparison` PASS
	- `negative_invalid_policy_mode` PASS
	- `negative_negative_pressure` PASS


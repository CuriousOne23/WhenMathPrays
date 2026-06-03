---
status: verification
source_of_truth: this
contains:
  - HLR: [HLR-20.080-001, HLR-20.080-002, HLR-20.080-003, HLR-20.080-004, HLR-20.080-005, HLR-20.080-006, HLR-20.080-007, HLR-20.080-008, HLR-20.080-009, HLR-20.080-010, HLR-20.080-011, HLR-20.080-012, HLR-20.080-013, HLR-20.080-014, HLR-20.080-015, HLR-20.080-016, HLR-20.080-017, HLR-20.080-018, HLR-20.080-019, HLR-20.080-020, HLR-20.080-021, HLR-20.080-022, HLR-20.080-023, HLR-20.080-024, HLR-20.080-025, HLR-20.080-026, HLR-20.080-027, HLR-20.080-028, HLR-20.080-029, HLR-20.080-030, HLR-20.080-031, HLR-20.080-032, HLR-20.080-033, HLR-20.080-034, HLR-20.080-035, HLR-20.080-036, HLR-20.080-037, HLR-20.080-038]
  - LLR: [LLR-40.36-001]
proves: [HLR-20.080-001, HLR-20.080-002, HLR-20.080-003, HLR-20.080-004, HLR-20.080-005, HLR-20.080-006, HLR-20.080-007, HLR-20.080-008, HLR-20.080-009, HLR-20.080-010, HLR-20.080-011, HLR-20.080-012, HLR-20.080-013, HLR-20.080-014, HLR-20.080-015, HLR-20.080-016, HLR-20.080-017, HLR-20.080-018, HLR-20.080-019, HLR-20.080-020, HLR-20.080-021, HLR-20.080-022, HLR-20.080-023, HLR-20.080-024, HLR-20.080-025, HLR-20.080-026, HLR-20.080-027, HLR-20.080-028, HLR-20.080-029, HLR-20.080-030, HLR-20.080-031, HLR-20.080-032, HLR-20.080-033, HLR-20.080-034, HLR-20.080-035, HLR-20.080-036, HLR-20.080-037, HLR-20.080-038]
derived-from: [LLR-40.36-001]
---

# Requirements Delta

## Purpose

Record GB-specific requirement changes, implementer feedback, and harness evidence for `40.36_gb_prototypes`.

## Evidence-Backed Requirement Deltas

- **HLR-20.080-023 / HLR-20.080-024**  
  **TCU fallback deterministically overrides event-type supervisory actions.**  
  - Evidence: `tcu_fallback_safemode`, `ob_decomposition_reshape`, `cop_proposal_gating`  
  - Traceability: `tcu_usage`, `tcu_fallback`, `supervisory_action="SafeMode"`  
  - Artifact: `artifacts/gb_verification_run_2026-06-03.json`

(Additional evidence entries will be added as more scenarios are executed.)

## Rationale

- GB fallback behavior is now confirmed to take precedence over event-type supervisory actions.
- This matches 20.80.023–024 and 20.30 §8.3–8.4 deterministic overflow semantics.
- Prototype behavior is stable and deterministic across runs.

## Impacted Documents

- `20_requirements/20.80_gb_requirements.md`
- `20_requirements/20.30_ts_functional_model.md`
- `40_thought_simulator_playground/40.36_gb_prototypes/software_description.md`
- `40_thought_simulator_playground/40.36_gb_prototypes/verification_capsule.md`
- `30_verification/30.36_gb_prototypes/30.36_gb_prototypes_verification_capsule.md` (promotion target)

## Open Validation Needed

- Confirm final IB population stability criteria and merge/split thresholds.
- Confirm SafeMode and fallback semantics for TCU overrun.
- Confirm external supervisory command taxonomy and policy-gating rules.

## Promotion Note

This delta will be promoted from approved 40.36 work into canonical 30-layer GB verification governance after evidence is stable.

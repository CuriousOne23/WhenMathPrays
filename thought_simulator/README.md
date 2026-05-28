# Thought Simulator Document Map

This folder hosts the canonical document tiers for the Thought Simulator.

## Structure

Core document tiers:

- [10_program_governance/](10_program_governance/) - project intent, architecture framing, and philosophical governance
- [10_thought_simulator_req/](10_thought_simulator_req/) - canonical HLR layer and promotion governance artifacts (ADR and protocol templates)
- [20_requirements/](20_requirements/) - exploratory requirements playground (reasoning and concept evolution)
- [30_verification/](30_verification/) - verification capsules and deterministic evidence artifacts
- [40_thought_simulator_playground/](40_thought_simulator_playground/) - exploratory prototypes and experiments
- [50_thought_simulator_design/](50_thought_simulator_design/) - formal design specifications

## Tier Clarification

Two `10_*` directories are intentional and do not require correction:

- [10_program_governance/](10_program_governance/) governs program-level architecture context and policy.
- [10_thought_simulator_req/](10_thought_simulator_req/) is the canonical requirement governance root for promotion protocol and ADR governance artifacts.

This split preserves epistemic asymmetry: exploratory layers influence canonical artifacts through human review, while formal traceability remains canonical-to-canonical.

## Operating Principle: Attached Exploration, Protected Canon

This repository intentionally supports both expert play and formal rigor.

- Attached exploration: `20_requirements/` and `40_thought_simulator_playground/` are where teams test ideas quickly, iterate, and discover better approaches.
- Protected canon: `10_thought_simulator_req/`, `30_verification/`, and `50_thought_simulator_design/` are where approved, traceable, and review-stable artifacts live.
- Controlled transfer: exploratory insights can be promoted into canonical layers only through explicit governance and verification steps.

This model is deliberate because high-quality innovation needs space to experiment, while production-relevant decisions need stable process controls.

## First-Time Contributor Reading Order

If you are new to this repository, use this order:

1. [README.md](README.md) (this file)
2. [CONTRIBUTING_CHANGE_WORKFLOW.md](CONTRIBUTING_CHANGE_WORKFLOW.md)
3. [10_thought_simulator_req/docs/promotion_protocol.md](10_thought_simulator_req/docs/promotion_protocol.md)
4. [50_thought_simulator_design/50.05_software_spec_construction_guide.md](50_thought_simulator_design/50.05_software_spec_construction_guide.md)
5. [30_verification/README.md](30_verification/README.md)
6. [30_verification/30.30_verification_glossary.md](30_verification/30.30_verification_glossary.md)

Then review canonical requirement anchors:

7. [10_thought_simulator_req/10.20_tp_requirements.md](10_thought_simulator_req/10.20_tp_requirements.md)
8. [10_thought_simulator_req/10.30_basin_requirements.md](10_thought_simulator_req/10.30_basin_requirements.md)
9. [10_thought_simulator_req/10.40_scheduler_requirements.md](10_thought_simulator_req/10.40_scheduler_requirements.md)

Then review canonical verification evidence snapshots:

10. [30_verification/30.20_tp_lifecycle/30.20_tp_lifecycle_verification_capsule.md](30_verification/30.20_tp_lifecycle/30.20_tp_lifecycle_verification_capsule.md)
11. [30_verification/30.30_basin_prototypes/30.30_basin_prototypes_verification_capsule.md](30_verification/30.30_basin_prototypes/30.30_basin_prototypes_verification_capsule.md)
12. [30_verification/30.40_scheduler_prototypes/30.40_scheduler_prototypes_verification_capsule.md](30_verification/30.40_scheduler_prototypes/30.40_scheduler_prototypes_verification_capsule.md)

## Process Flow (Current)

The process flow is intentionally two-speed:

- exploratory ideation and implementation in [20_requirements/](20_requirements/) and [40_thought_simulator_playground/](40_thought_simulator_playground/)
- canonical governance, verification, and design in [10_thought_simulator_req/](10_thought_simulator_req/), [30_verification/](30_verification/), and [50_thought_simulator_design/](50_thought_simulator_design/)

Operational flow for new `40.*` modules:

1. Phase A: author/review module `software_description.md` only (human approval required).
2. Phase B: generate module prototype/harness/verification capsule/requirements delta and artifact evidence.
3. Promotion prep: anchor requirement IDs in [10_thought_simulator_req/](10_thought_simulator_req/) and mirror canonical evidence in [30_verification/](30_verification/).
4. Design integration: consume canonical requirement + verification sources through [50.05_software_spec_construction_guide.md](50_thought_simulator_design/50.05_software_spec_construction_guide.md).

Process control sources:

- governance and promotion gates: [10_thought_simulator_req/docs/promotion_protocol.md](10_thought_simulator_req/docs/promotion_protocol.md)
- construction workflow rules: [50_thought_simulator_design/50.05_software_spec_construction_guide.md](50_thought_simulator_design/50.05_software_spec_construction_guide.md)
- shared verification vocabulary: [30_verification/30.30_verification_glossary.md](30_verification/30.30_verification_glossary.md)

## Core Reading Path

1. [00.10_vision_and_objectives.md](10_program_governance/00_foundations/00.10_vision_and_objectives.md)
2. [00.20_core_philosophy_and_principles.md](10_program_governance/00_foundations/00.20_core_philosophy_and_principles.md)
3. [00.30_core_conceptual_requirements.md](10_program_governance/00_foundations/00.30_core_conceptual_requirements.md)
4. [10.10_system_architecture.md](10_program_governance/10_architecture/10.10_system_architecture.md)
5. [10.20_manifold_specification.md](10_program_governance/10_architecture/10.20_manifold_specification.md)
6. [10.30_basins.md](10_program_governance/10_architecture/10.30_basins.md)
7. [10.40_TS_state_machine.md](10_program_governance/10_architecture/10.40_TS_state_machine.md)
8. [10.50_TS_data_model.md](10_program_governance/10_architecture/10.50_TS_data_model.md)
9. [10.60_data_structures.md](10_program_governance/10_architecture/10.60_data_structures.md)

## Directional Notes

- Documents 04-07 define the TS-centric architecture and execution model.
- Document 05 treats the manifold as an interpretive model of relational thought, not an ontological claim about reality.
- The prior geometric-era requirement files (old 07.5-14) were removed to reduce conceptual overlap and keep scope aligned with the current architecture.

## Traceability

Use [20.160_traceability_matrix.md](20_requirements/20.160_traceability_matrix.md) as exploratory mapping context, while keeping formal trace edges in canonical layers only.

Canonical trace purity rule:

- canonical-to-canonical only: [10_thought_simulator_req/](10_thought_simulator_req/) -> [50_thought_simulator_design/](50_thought_simulator_design/) -> [30_verification/](30_verification/)
- no formal trace edges from [20_requirements/](20_requirements/) or [40_thought_simulator_playground/](40_thought_simulator_playground/)

## Requirements (20_requirements)

10. [20.10_interaction_model.md](20_requirements/20.10_interaction_model.md)
11. [20.20_error_and_stability_requirements.md](20_requirements/20.20_error_and_stability_requirements.md)
12. [20.40_performance_requirements.md](20_requirements/20.40_performance_requirements.md)
13. [20.50_observability_requirements.md](20_requirements/20.50_observability_requirements.md)
14. [20.60_testing_and_validation.md](20_requirements/20.60_testing_and_validation.md)
15. [20.70_non_functional_requirements.md](20_requirements/20.70_non_functional_requirements.md)
16. [20.80_security_and_safety_requirements.md](20_requirements/20.80_security_and_safety_requirements.md)
17. [20.90_interfaces_and_io.md](20_requirements/20.90_interfaces_and_io.md)
18. [20.100_visualization_exploration.md](20_requirements/20.100_visualization_exploration.md)
19. [20.110_experiment_requirements.md](20_requirements/20.110_experiment_requirements.md)
20. [20.120_stability_requirements.md](20_requirements/20.120_stability_requirements.md)
21. [20.130_risks_assumptions.md](20_requirements/20.130_risks_assumptions.md)
22. [20.140_program_flow.md](20_requirements/20.140_program_flow.md)
23. [20.150_glossary.md](20_requirements/20.150_glossary.md)
24. [20.160_traceability_matrix.md](20_requirements/20.160_traceability_matrix.md)

## Design Documents

Implementation design specifications are maintained under [50_thought_simulator_design/](50_thought_simulator_design/).

- [50.05_software_spec_construction_guide.md](50_thought_simulator_design/50.05_software_spec_construction_guide.md) - generic methodology for constructing subsystem software specifications.

## Root Directory Index

Top-level `thought_simulator/` direct children:

- [10_program_governance/](10_program_governance/)
- [10_thought_simulator_req/](10_thought_simulator_req/)
- [20_requirements/](20_requirements/)
- [30_verification/](30_verification/)
- [40_thought_simulator_playground/](40_thought_simulator_playground/)
- [50_thought_simulator_design/](50_thought_simulator_design/)
- [config/](config/)
- [core/](core/)
- [docs/](docs/)
- [dynamics/](dynamics/)
- [experiments/](experiments/)
- [io/](io/)
- [scripts/](scripts/)
- [utils/](utils/)
- [main.py](main.py)
- [CONTRIBUTING_CHANGE_WORKFLOW.md](CONTRIBUTING_CHANGE_WORKFLOW.md)
- [REFACTOR_2026-05-28_PHASE1.md](REFACTOR_2026-05-28_PHASE1.md)
- [REFACTOR_2026-05-28_PHASE2.md](REFACTOR_2026-05-28_PHASE2.md)
- [REFACTOR_2026-05-28_PHASE3.md](REFACTOR_2026-05-28_PHASE3.md)
- [REFACTOR_2026-05-28_PHASE4.md](REFACTOR_2026-05-28_PHASE4.md)
- [REFACTOR_2026-05-28_PHASE5.md](REFACTOR_2026-05-28_PHASE5.md)
- [REFACTOR_2026-05-28_PHASE6.md](REFACTOR_2026-05-28_PHASE6.md)
- [REFACTOR_2026-05-28_PHASE7.md](REFACTOR_2026-05-28_PHASE7.md)
- [REFACTOR_2026-05-28_PHASE8.md](REFACTOR_2026-05-28_PHASE8.md)
- [REFACTOR_2026-05-28_PHASE9.md](REFACTOR_2026-05-28_PHASE9.md)
- [REFACTOR_2026-05-28_PHASE10.md](REFACTOR_2026-05-28_PHASE10.md)
- [REFACTOR_2026-05-28_PHASE11.md](REFACTOR_2026-05-28_PHASE11.md)
- [REFACTOR_2026-05-28_PHASE12.md](REFACTOR_2026-05-28_PHASE12.md)
- [RENAMING_MIGRATION_REPORT.md](RENAMING_MIGRATION_REPORT.md)
- [_broken_links.csv](_broken_links.csv)

---

**Last Updated**: May 28, 2026  
**Version**: 0.5 (Canonical/Exploratory Boundary Clarified)








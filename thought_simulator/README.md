# Thought Simulator Document Map

This folder hosts the canonical document tiers for the Thought Simulator.

## Structure

Core document tiers:

- [00_program_governance/](00_program_governance/) - project intent, architecture framing, and philosophical governance
- [10_thought_simulator_req/](10_thought_simulator_req/) - formalized requirement anchor layer used for coding and architecture realization
- [20_requirements/](20_requirements/) - primary User/Copilot collaborative requirement layer and traceability source
- [30_verification/](30_verification/) - verification capsules and deterministic evidence artifacts
- [40_thought_simulator_playground/](40_thought_simulator_playground/) - exploratory prototypes and experiments
- [50_thought_simulator_design/](50_thought_simulator_design/) - formal design specifications
- [60_review/](60_review/) - grouped review bundles, decision artifacts, and review manifests
- [70_measurement/](70_measurement/) - metrics, instrumentation, and evaluation methodology
- [80_safety/](80_safety/) - safety constraints, failure containment, and protective controls
- [90_validation_certification/](90_validation_certification/) - validation, certification, conformance, and formal sign-off

## Ownership and Workflow

The repository is human-owned in intent and approval, AI-drafted in breadth, and human-reviewed before authoritative adoption.

In practice:

- humans, led by the repository owner, control the normative direction and final acceptance of the 20-series
- AI agents draft most supporting content, expansion, normalization, and scaffolding
- a small set of core documents remain human-written because they define canonical methodology and release decisions
- AI-generated material becomes authoritative only after human review and approval

## Tier Clarification

- [00_program_governance/](00_program_governance/) governs program-level architecture context and policy.
- [20_requirements/](20_requirements/) is the primary requirement authoring layer where User and Copilot collaborate.
- [10_thought_simulator_req/](10_thought_simulator_req/) is the formalization layer for realization-ready requirement anchors.

Direction control is user-selected per [USER_GUIDE.md](USER_GUIDE.md):

- forward flow (typical): 20 -> 40 -> 10
- backward flow (when selected): 20 -> 10 -> 40

This split preserves epistemic asymmetry: exploratory layers influence canonical artifacts through human review, while formal traceability remains canonical-to-canonical.

## Operating Principle: Attached Exploration, Protected Canon

This repository intentionally supports both expert play and formal rigor.

- Collaborative requirements: `20_requirements/` is where User and Copilot iteratively author and refine requirement intent.
- Evidence development: `40_thought_simulator_playground/` is where prototype behavior and verification evidence are produced.
- Formal realization: `10_thought_simulator_req/` captures realization-ready anchors for coding and architecture.
- Controlled transfer: flow direction is explicit (`forward` or `backward`) and must be user-selected before propagation.

This model is deliberate because high-quality innovation needs space to experiment, while production-relevant decisions need stable process controls.

## First-Time Contributor Reading Order

If you are new to this repository, use this order:

1. [README.md](README.md) (this file)
2. [CONTRIBUTING_CHANGE_WORKFLOW.md](CONTRIBUTING_CHANGE_WORKFLOW.md)
3. [10_thought_simulator_req/docs/promotion_protocol.md](10_thought_simulator_req/docs/promotion_protocol.md)
4. [50_thought_simulator_design/50.05_software_spec_construction_guide.md](50_thought_simulator_design/50.05_software_spec_construction_guide.md)
5. [30_verification/README.md](30_verification/README.md)
6. [30_verification/30.01_verification_inventory_index.md](30_verification/30.01_verification_inventory_index.md)
7. [30_verification/30.30_verification_glossary.md](30_verification/30.30_verification_glossary.md)

Then review canonical requirement anchors:

8. [10_thought_simulator_req/10.20_tp_requirements.md](10_thought_simulator_req/10.20_tp_requirements.md)
9. [10_thought_simulator_req/10.30_basin_requirements.md](10_thought_simulator_req/10.30_basin_requirements.md)
10. [10_thought_simulator_req/10.40_scheduler_requirements.md](10_thought_simulator_req/10.40_scheduler_requirements.md)

Then review canonical verification evidence snapshots:

11. [30_verification/30.20_tp_lifecycle/30.20_tp_lifecycle_verification_capsule.md](30_verification/30.20_tp_lifecycle/30.20_tp_lifecycle_verification_capsule.md)
12. [30_verification/30.30_basin_prototypes/30.30_basin_prototypes_verification_capsule.md](30_verification/30.30_basin_prototypes/30.30_basin_prototypes_verification_capsule.md)
13. [30_verification/30.40_scheduler_prototypes/30.40_scheduler_prototypes_verification_capsule.md](30_verification/30.40_scheduler_prototypes/30.40_scheduler_prototypes_verification_capsule.md)

## Process Flow (Current)

The process flow is direction-controlled and intentionally two-speed:

- requirements collaboration and intent shaping in [20_requirements/](20_requirements/)
- evidence/prototype development in [40_thought_simulator_playground/](40_thought_simulator_playground/)
- formal realization anchors and downstream canonical synchronization in [10_thought_simulator_req/](10_thought_simulator_req/), [30_verification/](30_verification/), and [50_thought_simulator_design/](50_thought_simulator_design/)

Direction examples:

1. Forward (typical): 20 -> 40 -> 10 -> 30/50
2. Backward (when selected): 20 -> 10 -> 40 -> 30/50

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

1. [00.00.10_vision_and_objectives.md](00_program_governance/00_foundations/00.00.10_vision_and_objectives.md)
2. [00.00.20_core_philosophy_and_principles.md](00_program_governance/00_foundations/00.00.20_core_philosophy_and_principles.md)
3. [00.00.30_core_conceptual_requirements.md](00_program_governance/00_foundations/00.00.30_core_conceptual_requirements.md)
4. [00.10.10_system_architecture.md](00_program_governance/10_architecture/00.10.10_system_architecture.md)
5. [00.10.20_manifold_specification.md](00_program_governance/10_architecture/00.10.20_manifold_specification.md)
6. [00.10.30_basins.md](00_program_governance/10_architecture/00.10.30_basins.md)
7. [00.10.40_TS_state_machine.md](00_program_governance/10_architecture/00.10.40_TS_state_machine.md)
8. [00.10.50_TS_data_model.md](00_program_governance/10_architecture/00.10.50_TS_data_model.md)
9. [00.10.60_data_structures.md](00_program_governance/10_architecture/00.10.60_data_structures.md)

## Directional Notes

- Documents 04-07 define the TS-centric architecture and execution model.
- Document 05 treats the manifold as an interpretive model of relational thought, not an ontological claim about reality.
- The prior geometric-era requirement files (old 07.5-14) were removed to reduce conceptual overlap and keep scope aligned with the current architecture.

## Traceability

Use [20.200_traceability_matrix.md](20_requirements/20.200_traceability_matrix.md) as the active 20-series traceability matrix.

Canonical trace purity rule:

- canonical-to-canonical only after direction-confirmed formalization in [10_thought_simulator_req/](10_thought_simulator_req/): [10_thought_simulator_req/](10_thought_simulator_req/) -> [50_thought_simulator_design/](50_thought_simulator_design/) -> [30_verification/](30_verification/)
- no formal trace edges from [20_requirements/](20_requirements/) or [40_thought_simulator_playground/](40_thought_simulator_playground/)

## Historical Requirements (Archive)

10. [20.10_interaction_model.md](20_requirements/archive/20.10_interaction_model.md)
11. [20.20_error_and_stability_requirements.md](20_requirements/archive/20.20_error_and_stability_requirements.md)
12. [20.40_performance_requirements.md](20_requirements/archive/20.40_performance_requirements.md)
13. [20.50_observability_requirements.md](20_requirements/archive/20.50_observability_requirements.md)
14. [20.60_testing_and_validation.md](20_requirements/archive/20.60_testing_and_validation.md)
15. [20.70_non_functional_requirements.md](20_requirements/archive/20.70_non_functional_requirements.md)
16. [20.80_security_and_safety_requirements.md](20_requirements/archive/20.80_security_and_safety_requirements.md)
17. [20.90_interfaces_and_io.md](20_requirements/archive/20.90_interfaces_and_io.md)
18. [20.100_visualization_exploration.md](20_requirements/archive/20.100_visualization_exploration.md)
19. [20.110_experiment_requirements.md](20_requirements/archive/20.110_experiment_requirements.md)
20. [20.120_stability_requirements.md](20_requirements/archive/20.120_stability_requirements.md)
21. [20.130_risks_assumptions.md](20_requirements/archive/20.130_risks_assumptions.md)
22. [20.140_program_flow.md](20_requirements/archive/20.140_program_flow.md)
23. [20.150_glossary.md](20_requirements/archive/20.150_glossary.md)
24. [20.160_traceability_matrix.md](20_requirements/archive/20.160_traceability_matrix.md)

## Design Documents

Implementation design specifications are maintained under [50_thought_simulator_design/](50_thought_simulator_design/).

- [50.05_software_spec_construction_guide.md](50_thought_simulator_design/50.05_software_spec_construction_guide.md) - generic methodology for constructing subsystem software specifications.
- [thought_sim_arch_overview.md](thought_sim_arch_overview.md) - high-level overview of the Thought Simulator project, its goals, architecture, and comparison to today's AI systems.

## Root Directory Index

Top-level `thought_simulator/` direct children:

- [00_program_governance/](00_program_governance/)
- [10_thought_simulator_req/](10_thought_simulator_req/)
- [20_requirements/](20_requirements/)
- [30_verification/](30_verification/)
- [40_thought_simulator_playground/](40_thought_simulator_playground/)
- [50_thought_simulator_design/](50_thought_simulator_design/)
- [60_review/](60_review/)
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
- [USER_GUIDE.md](USER_GUIDE.md)
- [REFACTOR_2026-05-28_PHASE1.md](archive/refactors/REFACTOR_2026-05-28_PHASE1.md)
- [REFACTOR_2026-05-28_PHASE2.md](archive/refactors/REFACTOR_2026-05-28_PHASE2.md)
- [REFACTOR_2026-05-28_PHASE3.md](archive/refactors/REFACTOR_2026-05-28_PHASE3.md)
- [REFACTOR_2026-05-28_PHASE4.md](archive/refactors/REFACTOR_2026-05-28_PHASE4.md)
- [REFACTOR_2026-05-28_PHASE5.md](archive/refactors/REFACTOR_2026-05-28_PHASE5.md)
- [REFACTOR_2026-05-28_PHASE6.md](archive/refactors/REFACTOR_2026-05-28_PHASE6.md)
- [REFACTOR_2026-05-28_PHASE7.md](archive/refactors/REFACTOR_2026-05-28_PHASE7.md)
- [REFACTOR_2026-05-28_PHASE8.md](archive/refactors/REFACTOR_2026-05-28_PHASE8.md)
- [REFACTOR_2026-05-28_PHASE9.md](archive/refactors/REFACTOR_2026-05-28_PHASE9.md)
- [REFACTOR_2026-05-28_PHASE10.md](archive/refactors/REFACTOR_2026-05-28_PHASE10.md)
- [REFACTOR_2026-05-28_PHASE11.md](archive/refactors/REFACTOR_2026-05-28_PHASE11.md)
- [REFACTOR_2026-05-28_PHASE12.md](archive/refactors/REFACTOR_2026-05-28_PHASE12.md)
- [RENAMING_MIGRATION_REPORT.md](RENAMING_MIGRATION_REPORT.md)
- [_broken_links.csv](_broken_links.csv)

---

**Last Updated**: June 2, 2026  
**Version**: 0.6 (Direction-Controlled 20/40/10 Flow Clarified)











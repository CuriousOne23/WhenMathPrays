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

---

**Last Updated**: May 28, 2026  
**Version**: 0.5 (Canonical/Exploratory Boundary Clarified)








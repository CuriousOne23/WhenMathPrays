# Thought Manifold Requirements

This directory is the formal requirements source for the Thought Manifold Simulator.

## Directory Layout

- [00_foundations/](00_foundations/) - conceptual grounding and project intent
- [10_architecture/](10_architecture/) - TS-centric architecture and data model
- [20_requirements/](20_requirements/) - behavioral and quality requirements
- [30_philosophical/](30_philosophical/) - philosophical companion texts

## Reading Order

### Foundations
1. [01_vision_and_objectives.md](00_foundations/01_vision_and_objectives.md)
2. [02_core_philosophy_and_principles.md](00_foundations/02_core_philosophy_and_principles.md)
3. [03_core_conceptual_requirements.md](00_foundations/03_core_conceptual_requirements.md)

### Architecture (TS-centric)
4. [04_system_architecture.md](10_architecture/04_system_architecture.md)
5. [05_manifold_specification.md](10_architecture/05_manifold_specification.md)
6. [06_basins.md](10_architecture/06_basins.md)
7. [07_TS_state_machine.md](10_architecture/07_TS_state_machine.md)
8. [08_TS_data_model.md](10_architecture/08_TS_data_model.md)
9. [09_data_structures.md](10_architecture/09_data_structures.md)

### Requirements
10. [10_interaction_model.md](20_requirements/10_interaction_model.md)
11. [11_error_and_stability_requirements.md](20_requirements/11_error_and_stability_requirements.md)
12. [12_performance_requirements.md](20_requirements/12_performance_requirements.md)
13. [13_observability_requirements.md](20_requirements/13_observability_requirements.md)
14. [14_testing_and_validation.md](20_requirements/14_testing_and_validation.md)
15. [15_non_functional_requirements.md](20_requirements/15_non_functional_requirements.md)
16. [16_interfaces_and_io.md](20_requirements/16_interfaces_and_io.md)
17. [17_visualization_exploration.md](20_requirements/17_visualization_exploration.md)
18. [18_experiment_requirements.md](20_requirements/18_experiment_requirements.md)
19. [19_stability_requirements.md](20_requirements/19_stability_requirements.md)
20. [20_risks_assumptions.md](20_requirements/20_risks_assumptions.md)
21. [21_program_flow.md](20_requirements/21_program_flow.md)
22. [22_glossary.md](20_requirements/22_glossary.md)
23. [23_traceability_matrix.md](20_requirements/23_traceability_matrix.md)

### Philosophical
24. [24_verb_mind.md](30_philosophical/24_verb_mind.md)
25. [25_humility_as_relation.md](30_philosophical/25_humility_as_relation.md)
26. [26_beauty_and_rigor.md](30_philosophical/26_beauty_and_rigor.md)

## Notes on Scope Changes

- Geometric-era requirement files were removed: old 07.5, 08, 09, 10, 11.5, 11, 12, 13, and 14.
- Documents 04-07 now carry the architectural center of gravity for a TS-centric implementation.
- Document 05 defines the manifold as an interpretive relational framework used for inquiry and modeling.

## Traceability

Use [23_traceability_matrix.md](20_requirements/23_traceability_matrix.md) for cross-document linkage between conceptual, architectural, and implementation-facing requirements.

---

**Last Updated**: May 25, 2026
**Version**: 0.4 (Restructured)

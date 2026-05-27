# 24 Traceability Matrix

## Purpose

This matrix provides **end-to-end traceability** from foundational concepts through architecture and requirements to implementation concerns. It serves as the living map that keeps the TS project coherent as it evolves.

## Scope Notes

- Follows the current directory layout: `00_foundations`, `10_architecture`, `20_requirements`, `30_philosophical`.
- Geometric-era documents were pruned during restructuring.
- All links are relative to the `20_requirements/` directory.

## High-Level Traceability

| Area                        | Primary Document                                      | Key Linked Documents                                      | Status      |
|-----------------------------|-------------------------------------------------------|-----------------------------------------------------------|-------------|
| Vision & Objectives         | [01_vision_and_objectives.md](../00_foundations/01_vision_and_objectives.md) | 02, 03, 04, 19, 23 | Complete |
| Core Philosophy             | [02_core_philosophy_and_principles.md](../00_foundations/02_core_philosophy_and_principles.md) | 03, 05, 06, 20, 23 | Complete |
| Conceptual Requirements     | [03_core_conceptual_requirements.md](../00_foundations/03_core_conceptual_requirements.md) | 04–09, 11–23 | Complete |
| System Architecture         | [04_system_architecture.md](../10_architecture/04_system_architecture.md) | 05, 06, 07, 09, 12, 22 | Complete |
| Manifold Specification      | [05_manifold_specification.md](../10_architecture/05_manifold_specification.md) | 03, 04, 06, 18, 23 | Complete |
| Basins                      | [06_basins.md](../10_architecture/06_basins.md)       | 03, 05, 07, 19, 20, 22, 23 | Complete |
| TS State Machine            | [07_TS_state_machine.md](../10_architecture/07_TS_state_machine.md) | 04, 06, 08, 11, 13, 20, 22 | Complete |
| TS Data Model               | [08_TS_data_model.md](../10_architecture/08_TS_data_model.md) | 07, 09, 13, 17, 23 | Complete |
| Data Structures             | [09_data_structures.md](../10_architecture/09_data_structures.md) | 04, 07, 08, 12, 16 | Complete |
| Interaction Model           | [10_interaction_model.md](10_interaction_model.md)    | 04, 07, 16, 17, 22 | Complete |
| Error & Stability           | [11_error_and_stability_requirements.md](11_error_and_stability_requirements.md) | 06, 07, 13, 20, 21, 22 | Complete |
| Performance                 | [12_performance_requirements.md](12_performance_requirements.md) | 09, 15, 16, 20, 22 | Complete |
| Observability               | [13_observability_requirements.md](13_observability_requirements.md) | 04, 07, 11, 16, 17, 18, 22, 23 | Complete |
| Testing & Validation        | [14_testing_and_validation.md](14_testing_and_validation.md) | 11–13, 15–18, 20–23 | Complete |
| Non-Functional              | [15_non_functional_requirements.md](15_non_functional_requirements.md) | 04, 09, 12, 13, 14, 16 | Complete |
| Security & Safety           | [16_security_and_safety_requirements.md](16_security_and_safety_requirements.md) | 12, 13, 14, 20, 21, 22 | Complete |
| Interfaces & I/O            | [17_interfaces_and_io.md](17_interfaces_and_io.md)    | 08, 10, 13, 18, 19 | Complete |
| Visualization & Exploration | [18_visualization_exploration.md](18_visualization_exploration.md) | 05, 13, 15, 17, 23 | Complete |
| Experiment Management       | [19_experiment_requirements.md](19_experiment_requirements.md) | 06, 12, 13, 14, 17, 18, 22 | Complete |
| Stability                   | [20_stability_requirements.md](20_stability_requirements.md) | 11, 12, 14, 16, 20, 21, 22 | Complete |
| TP Requirements             | [10.30_tp_requirements.md](10.30_tp_requirements.md) | 03, 07, 08, 14, 24 | Complete |
| Risks & Assumptions         | [21_risks_assumptions.md](21_risks_assumptions.md) | 11–16, 19–23 | Complete |
| Program Flow                | [22_program_flow.md](22_program_flow.md)              | 04, 07, 11, 13, 16, 20, 22 | Complete |
| Glossary                    | [23_glossary.md](23_glossary.md)                      | 01–23 | Complete |

## Key Concept Traceability Examples

**Minimal Thought Atom**  
→ 01_vision → 03_conceptual → 06_basins → 07_state_machine → 22_program_flow

**Interpretive Manifold**  
→ 03_conceptual → 05_manifold → 18_visualization → 23_glossary

**Unified Entropy**  
→ 03_conceptual → 11_stability → 20_stability → 23_glossary

**Deterministic Parallel Execution**  
→ 12_performance → 15_non_functional → 20_stability → 22_program_flow

**ThoughtPoint Lifecycle and Provenance**
→ 03_conceptual → 07_state_machine → 08_data_model → 14_testing → 20.30_tp_requirements

## Maintenance Rules

- Update this matrix whenever a document is renamed, renumbered, or significantly revised.
- All links must remain relative to the `20_requirements/` folder.
- New requirements or major sections must be added with upstream (foundations/architecture) and downstream (testing/observability/risks) links.

## HLR/LLR Naming Normalization Policy

To keep requirement attachment consistent across modules, use the following naming policy.

### High-Level Requirements (HLR)

- Format: `HLR-<DOMAIN>-<DOCNUM>`
- DOMAIN values:
	- `ARCH` for architecture documents (`10_architecture`)
	- `REQ` for requirements documents (`20_requirements`)
	- `FND` for foundations documents (`00_foundations`) when needed
- DOCNUM is the two-digit document prefix without leading directory context.

Examples:

- `HLR-ARCH-07` for `10_architecture/07_TS_state_machine.md`
- `HLR-ARCH-08` for `10_architecture/08_TS_data_model.md`
- `HLR-REQ-14` for `20_requirements/14_testing_and_validation.md`

### Low-Level Requirements (LLR)

- Prefer canonical IDs defined by the source requirement document.
- Format when explicit IDs exist: `LLR-<SOURCE-ID>`
	- Example: `LLR-T-DET-01`, `LLR-T-OBS-01`
- If a source section lacks explicit low-level IDs:
	- Use provisional section-anchored IDs: `LLR-SEC-<DOCNUM>-<SECTION>`
	- Example: `LLR-SEC-07-8`
	- Mark provisional status in module traceability docs and promote to canonical IDs when available.

### Run Record and Ledger Usage Rules

- Every test row must include at least one HLR and one LLR reference.
- Multiple IDs must be comma-separated.
- If mapping is unknown, use `HLR-?` / `LLR-?` and record remediation in module insights and updated requirements.

---

**Last Updated**: May 26, 2026  
**Version**: 0.7 (Added HLR/LLR naming normalization policy)

---

# Renaming Migration Report

Generated: 2026-05-27

## Scope
- Base path: thought_simulator/
- Objective: archive the executed lossless renaming and reference updates.

## Top-Level Directory Mappings
| Old | New |
|---|---|
| 10_config/ | config/ |
| 20_core/ | core/ |
| 30_docs/ | docs/ |
| 40_dynamics/ | dynamics/ |
| 50_experiments/ | experiments/ |
| 60_io/ | io/ |
| 100_utils/ | utils/ |
| 90_thought_simulator_req/ | 10_thought_simulator_req/ |
| 70_thought_simulator_design/ | 20_thought_simulator_design/ |
| 80_thought_simulator_playground/ | 30_thought_simulator_playground/ |

## Immediate Markdown File Mappings

### Non-Conceptual
| Old Path | New Path |
|---|---|
| thought_simulator/40_dynamics/40.10_parameter_tuning_and_calibration.md | thought_simulator/dynamics/parameter_tuning_and_calibration.md |
| thought_simulator/40_dynamics/40.20_numerical_stability.md | thought_simulator/dynamics/numerical_stability.md |

### Requirements Top Level
| Old Path | New Path |
|---|---|
| thought_simulator/90_thought_simulator_req/90.10_README.md | thought_simulator/10_thought_simulator_req/10.10_README.md |

### Design Top Level
| Old Path | New Path |
|---|---|
| thought_simulator/70_thought_simulator_design/70.10_system_architecture.md | thought_simulator/20_thought_simulator_design/20.10_system_architecture.md |
| thought_simulator/70_thought_simulator_design/70.20_geometry_engine_design.md | thought_simulator/20_thought_simulator_design/20.20_geometry_engine_design.md |
| thought_simulator/70_thought_simulator_design/70.30_dynamics_engine_design.md | thought_simulator/20_thought_simulator_design/20.30_dynamics_engine_design.md |
| thought_simulator/70_thought_simulator_design/70.40_interaction_layer_design.md | thought_simulator/20_thought_simulator_design/20.40_interaction_layer_design.md |
| thought_simulator/70_thought_simulator_design/70.50_data_structures.md | thought_simulator/20_thought_simulator_design/20.50_data_structures.md |
| thought_simulator/70_thought_simulator_design/70.60_error_handling_design.md | thought_simulator/20_thought_simulator_design/20.60_error_handling_design.md |
| thought_simulator/70_thought_simulator_design/70.70_logging_and_observability_design.md | thought_simulator/20_thought_simulator_design/20.70_logging_and_observability_design.md |
| thought_simulator/70_thought_simulator_design/70.80_testing_strategy.md | thought_simulator/20_thought_simulator_design/20.80_testing_strategy.md |
| thought_simulator/70_thought_simulator_design/70.90_api_contract.md | thought_simulator/20_thought_simulator_design/20.90_api_contract.md |
| thought_simulator/70_thought_simulator_design/70.100_core_contract.md | thought_simulator/20_thought_simulator_design/20.100_core_contract.md |
| thought_simulator/70_thought_simulator_design/70.110_ui_contract.md | thought_simulator/20_thought_simulator_design/20.110_ui_contract.md |

### Playground Top Level
| Old Path | New Path |
|---|---|
| thought_simulator/80_thought_simulator_playground/80.10_README.md | thought_simulator/30_thought_simulator_playground/30.10_README.md |
| thought_simulator/80_thought_simulator_playground/80.20_master_program_guide.md | thought_simulator/30_thought_simulator_playground/30.20_master_program_guide.md |
| thought_simulator/80_thought_simulator_playground/80.30_verification_glossary.md | thought_simulator/30_thought_simulator_playground/30.30_verification_glossary.md |

## Additive New File(s)
| Path | Reason |
|---|---|
| thought_simulator/10_thought_simulator_req/20_requirements/10.30_tp_requirements.md | Additive TP requirements consolidation document |
| thought_simulator/RENAMING_MIGRATION_REPORT.md | Migration and audit report |
| thought_simulator/_broken_links.csv | Final link-audit output artifact |

## Content Update Scope
- Updated only path prefixes, filename prefixes, first-heading numeric prefixes for renamed top-level conceptual markdown files, and file references required by the rename.
- Nested markdown files in conceptual subdirectories were not renamed.
- Python files were not renamed or modified.

## Verification Note

Final markdown link audit under thought_simulator/ excluding this report produced no remaining broken internal links.

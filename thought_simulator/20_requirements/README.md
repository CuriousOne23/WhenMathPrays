---
status: requirements
source_of_truth: this
contains:
  - HLR: [HLR-20.000-001]
---

# 20 Requirements

## Purpose
Primary User/Copilot collaborative requirement layer for TS behavior, determinism, safety, and traceability.

This directory is the main authoring workspace for requirement intent, with downstream formalization and realization controlled by user-selected flow direction.

## Bootstrap Reload Set

These four documents are sufficient to bootstrap TS reasoning in a new conversation:

- [20.10_ts_architectural_principles.md](20.10_ts_architectural_principles.md) — architectural essence, dual-pipeline rationale
- [20.12_ts_invariants.md](20.12_ts_invariants.md) — canonical invariants (authoritative)
- [20.20_ts_primitives.md](20.20_ts_primitives.md) — meaning-layer and realization-layer primitives
- [20.30_ts_functional_model.md](20.30_ts_functional_model.md) — Pipeline A/B functional partition and basin pipeline

## Authoritative Requirement Files
- [20.10_ts_architectural_principles.md](20.10_ts_architectural_principles.md)
- [20.12_ts_invariants.md](20.12_ts_invariants.md)
- [20.20_ts_primitives.md](20.20_ts_primitives.md)
- [20.30_ts_functional_model.md](20.30_ts_functional_model.md)
- [20.31_semantic_specification.md](20.31_semantic_specification.md)
- [20.35_reference_algorithms.md](20.35_reference_algorithms.md)
- [20.36_canonical_end_to_end_trace.md](20.36_canonical_end_to_end_trace.md)
- [20.37_thought_router_tr_specification.md](20.37_thought_router_tr_specification.md)
- [20.32_cob_requirements.md](20.32_cob_requirements.md)
- [20.33_cil_requirements.md](20.33_cil_requirements.md)
- [20.34_cop_requirements.md](20.34_cop_requirements.md)
- [20.40_ob_requirements.md](20.40_ob_requirements.md)
- [20.50_rb_requirements.md](20.50_rb_requirements.md)
- [20.60_tb_requirements.md](20.60_tb_requirements.md)
- [20.70_mb_requirements.md](20.70_mb_requirements.md)
- [20.80_gb_requirements.md](20.80_gb_requirements.md)
- [20.90_ib_requirements.md](20.90_ib_requirements.md)
- [20.90_ts_parameter_table.md](20.90_ts_parameter_table.md)
- [20.95_ts_numeric_policy.md](20.95_ts_numeric_policy.md)
- [20.100_inb_requirements.md](20.100_inb_requirements.md)
- [20.105_tp_requirements.md](20.105_tp_requirements.md)
- [20.106_dcb_requirements.md](20.106_dcb_requirements.md)
- [20.110_oub_requirements.md](20.110_oub_requirements.md)
- [20.115_mtp_requirements.md](20.115_mtp_requirements.md)
- [20.120_mtp_schema_requirements.md](20.120_mtp_schema_requirements.md)
- [20.130_splitting_and_merging_requirements.md](20.130_splitting_and_merging_requirements.md)
- [20.140_truth_evaluation_requirements.md](20.140_truth_evaluation_requirements.md)
- [20.150_tcu_budgeting_requirements.md](20.150_tcu_budgeting_requirements.md)
- [20.160_randomness_requirements.md](20.160_randomness_requirements.md)
- [20.165_dcb_stability_requirements.md](20.165_dcb_stability_requirements.md)
- [20.170_safety_requirements.md](20.170_safety_requirements.md)
- [20.180_conversational_relevance_requirements.md](20.180_conversational_relevance_requirements.md)
- [20.190_glossary.md](20.190_glossary.md)
- [20.200_traceability_matrix.md](20.200_traceability_matrix.md)

## Non-Authoritative Supporting Artifacts
- [archive/](archive/)
- [glossary_term_registry.json](glossary_term_registry.json)
- [docs/](docs/)

## Rules
- The files listed in Authoritative Requirement Files are the only authoritative 20-series requirement docs.
- Legacy 20-series files are archived intact under archive/.
- Downstream edits to 30/40/50 are impact-analysis only until explicit user approval.

## Direction-Controlled Flow
- forward flow (typical): 20 -> 40 -> 10
- backward flow (when selected): 20 -> 10 -> 40
- direction MUST be explicitly user-selected before propagation.
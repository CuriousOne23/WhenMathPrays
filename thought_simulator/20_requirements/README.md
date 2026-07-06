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

## Start here — architecture map

**New to the 20-series?** Read [20.01_architecture_map.md](20.01_architecture_map.md) first — runtime-pipeline concept blocks (B0–B8), mermaid diagrams, and suggested read paths. Flat file list remains below; normative HLRs stay in individual modules.

## Bootstrap Reload Set

These four documents are sufficient to bootstrap TS reasoning in a new conversation:

- [20.10_ts_architectural_principles.md](20.10_ts_architectural_principles.md) — architectural essence, dual-pipeline rationale
- [20.12_ts_invariants.md](20.12_ts_invariants.md) — canonical invariants (authoritative)
- [20.20_ts_primitives.md](20.20_ts_primitives.md) — meaning-layer and realization-layer primitives
- [20.30_ts_functional_model.md](20.30_ts_functional_model.md) — Pipeline A/B functional partition and basin pipeline

## Authoritative Requirement Files
- [20.01_architecture_map.md](20.01_architecture_map.md)
- [20.10_ts_architectural_principles.md](20.10_ts_architectural_principles.md)
- [20.12_ts_invariants.md](20.12_ts_invariants.md)
- [20.17_messy_input_handling.md](20.17_messy_input_handling.md)
- [20.20_ts_prim_proc_ref_gov.md](20.20_ts_primprim_proc_ref_gov.md)
- [20.30_ts_functional_model.md](20.30_ts_functional_model.md)
- [20.30.005_rtu_prim.md](20.30.005_rtu_prim.md)
- [20.30.010_ts_ops.md](20.30.010_ts_ops.md)  
- [20.30.020_cycle_alloc.md](20.30.020_cycle_alloc.md)
- [20.30.030_tcu_budgeting.md](20.30.030_tcu_budgeting.md)
- [20.30.040_mcs_rules.md](20.30.040_mcs_rules.md)
- [20.30.050_merge_formal.md](20.30.050_merge_formal.md)
- [20.30.060_truth_completion.md](20.30.060_truth_completion.md)
- [20.30.070_rbu_mtp_sem.md](20.30.070_rbu_mtp_sem.md)
- [20.30.080_rg_resp_gen_sem.md](20.30.080_rg_resp_gen_sem.md)
- [20.30.085_rsg_prim.md](20.30.085_rsg_prim.md)
- [20.30.090_rsg_mapping_rules.md](20.30.090_rsg_mapping_rules.md)
- [20.31_patha_semantic_spec.md](20.31_patha_semantic_spec.md)
- [20.32_cob_requirements.md](20.32_cob_requirements.md)
- [20.33_cil_requirements.md](20.33_cil_requirements.md)
- [20.34_cop_requirements.md](20.34_cop_requirements.md)
- [20.35_reference_algorithms.md](20.35_reference_algorithms.md)
- [20.36_canonical_end_to_end_trace.md](20.36_canonical_end_to_end_trace.md)
- [20.37_thought_router_tr_specification.md](20.37_thought_router_tr_specification.md)
- [20.40_ob_requirements.md](20.40_ob_requirements.md)
- [20.40.010_sob_prim.md](20.40.010_sob_prim.md)
- [20.40.020_srob_prim.md](20.40.010_srob_prim.md)
- [20.40.030_cnob_prim.md](20.40.030_cnob_prim.md)
- [20.40.040_smob_prim.md](20.40.040_smob_prim.md)
- [20.40.050_idob_prim.md](20.40.050_idob_prim.md)
- [20.40.060_ouba_prim.md](20.40.060_ouba_prim.md)
- [20.40.060.010_ouba_input_data_spec.md](20.40.060.010_ouba_input_data_spec.md)
- [20.40.060.700_ouba_field_ref.md](20.40.060.700_ouba_field_ref.md)
- [20.41_opbeh_requirements.md](20.41_opbeh_requirements.md)
- [20.42_obg_requirements.md](20.42_obg_requirements.md)
- [20.43_xlater_requirements.md](20.43_xlater_requirements.md)
- [20.44_ts_isc_scoring.md](20.44_ts_isc_scoring.md)
- [20.44_ts_isc_scoring.md](20.44_ts_isc_scoring.md)
- [20.45_imr_requirements.md](20.45_imr_requirements.md)
- [20.46_tpu_req.md](20.46_tpu_req.md)  
- [20.47_ssg_prim.md](20.47_ssg_prim.md)
- [20.48.010_knc_prim.md](20.41.010_knc_prim.md)
- [20.48.020_knm_prim.md](20.41.020_knm_prim.md)
- [20.48.030_knf_prim.md](20.41.030_knf_prim.md)
- [20.50_rb_requirements.md](20.50_rb_requirements.md)
- [20.51_rbu_prim.md](20.51_rbu_prim.md)
- [20.52_ssr_data_packet.md](20.52_ssr_data_packet.md)
- [20.53_rrw_prim.md](20.53_rrw_prim.md)
- [20.60_tb_requirements.md](20.60_tb_requirements.md)
- [20.64_tptb_prim.md](20.64_tptb_prim.md)
- [20.66_tpsf_prim.md](20.66_tpsf_prim.md)
- [20.70_mb_requirements.md](20.70_mb_requirements.md)
- [20.80_gb_requirements.md](20.80_gb_requirements.md)
- [20.90_ib_requirements.md](20.90_ib_requirements.md)
- [20.92_ts_parameter_table.md](20.90_ts_parameter_table.md)
- [20.95_ts_numeric_policy.md](20.95_ts_numeric_policy.md)
- [20.100_inb_requirements.md](20.100_inb_requirements.md)
- [20.101_iiinb_requirements.md](20.101_iiinb_requirements.md)
- [20.102_usp_requirements.md](20.102_usp_requirements.md)
- [20.103_upi_requirements.md](20.103_upi_requirements.md)
- [20.105_tp_requirements.md](20.105_tp_requirements.md)
- [20.106_dcb_requirements.md](20.106_dcb_requirements.md)
- [20.107_cex_extract.md](20.107_cex_extract.md)
- [20.108_ce_envelope.md](20.108_ce_envelope.md)
- [20.110_oubb_requirements.md](20.110_oubb_requirements.md)
- [20.110.010_oubb_stack.md](20.110.010_oubb_stack.md)
- [20.111_mli.md](20.111_mli.md)
- [20.112_li_prim.md](20.112_li_prim.md)
- [20.113_cohi_prim.md](20.113_cohi_prim.md)
- [20.115_mtp_requirements.md](20.115_mtp_requirements.md)
- [20.120_mtp_schema_requirements.md](20.120_mtp_schema_requirements.md)
- [20.140_truth_done_requirements.md](20.140_truth_done_requirements.md)
- [20.145_ctp_prm.md](20.145_ctp_prm.md)
- [20.150_tcu_budgeting_requirements.md](20.150_tcu_budgeting_requirements.md)
- [20.155_trsch_prim.md](20.155_trsch_prim.md)
- [20.160_randomness_requirements.md](20.160_randomness_requirements.md)
- [20.165_dcb_stability_requirements.md](20.165_dcb_stability_requirements.md)
- [20.166_rex_prm.md](20.166_rex_prm.md)
- [20.167_rpln_prm.md](20.167_rpln_prm.md)
- [20.168_rpu_prm.md](20.168_rpu_prm.md)
- [20.169_reb_prm.md](20.166_reb_prm.md)
- [20.170_safety_requirements.md](20.170_safety_requirements.md)
- [20.180_conversational_relevance_requirements.md](20.180_conversational_relevance_requirements.md)
- [20.200_traceability_matrix.md](20.200_traceability_matrix.md)
- [20.206_pipeline_a_b_synchronization_contract.md](20.206_pipeline_a_b_synchronization_contract.md)
- [20.207_execution_replay_specification.md](20.207_execution_replay_specification.md)

## Coordination Programs (Non-Normative)
- [20.500_refactoring_for_dual_TS_pipeline.md](20.500_refactoring_for_dual_TS_pipeline.md) — dual-pipeline refactor (**complete** 2026-06-07)
- [20.510_refactoring_for_input_correction_track_h.md](20.510_refactoring_for_input_correction_track_h.md) — Track H input correction (IIInB / USP / UPI) — **complete** 2026-06-07
- [20.30.500_old2new_hlr_idx.md](20.30.500_old2new_hlr_idx.md)
- **complete** 2026-06-17
- [20.30.500.000_old_shalls_semantic.md](20.30.500.000_old_shalls_semantic.md)
- **complete** 2026-06-17
- [20.30.500.004_new_hlr_semantics.md](20.30.500.004_new_hlr_semantics.md)
- **complete** 2026-06-17
- [20.40.500_old_hlr_semantic_ref.md](20.40.500_old_hlr_semantic_ref.md)
- **complete** 2026-06-18
- [20.40.510_new_hlr_semantic_ref.md](20.40.510_new_hlr_semantic_ref.md)
- **complete** 2026-06-18

## Reference Documents
- [20.190_glossary.md](20.190_glossary.md)
- [20.700_master_glossary.md](20.700_master_glossary.md)
- [20.700.010_primitives_glossary.md](20.700.010_primitives_glossary.md)
- [20.700.020_processes_glossary.md](20.700.020_processes_glossary.md
- [20.700.030_reference_objects_glossary.md](20.700.030_reference_objects_glossary.md)
- [20.700.040_governance_glossary.md]20.700.040_governance_glossary.md
- [20.700.050_ts_level_concepts_glossary.md](20.700.050_ts_level_concepts_glossary.md)
- [20.705_patha_pathb_flow.md](20.705_patha_pathb_flow.md)
- [20.705.010_ts_flw_glss_cvrg.md](20.705.010_ts_flw_glss_cvrg.md)
- [20.709_ob_data_strc.md](20.709_ob_data_strc.md)
- [20.710_primitive_flows.md](20.710_primitive_flows.md)
- [20.715_process_flows.md](20.715_process_flows.md)
- [20.720_reference_flows.md](20.720_reference_flows.md)
- [20.725_governance_flows.md](20.725_governance_flows.md)
- [20.730_ts_concept_flows.md](20.730_ts_concept_flows.md)
- [20.735_ts_flw_glss_cvrg.md](20.735_ts_flw_glss_cvrg.md)


## Non-Authoritative Supporting Artifacts
- [archive/](archive/)
- [glossary_term_registry.json](glossary_term_registry.json)
- [system_playground/](system_playground/)
- [system_simulation/](system_simulation/)
- [Grok_review_in_20.md](Grok_review_in_20.md)

## Rules
- The files listed in Authoritative Requirement Files are the only authoritative 20-series requirement docs.
- Legacy 20-series files are archived intact under archive/.
- Downstream edits to 30/40/50 are impact-analysis only until explicit user approval.

## Direction-Controlled Flow
- forward flow (typical): 20 -> 40 -> 10
- backward flow (when selected): 20 -> 10 -> 40
- direction MUST be explicitly user-selected before propagation.

## Directory index (coverage-aligned)

- [20.16_gb_responsibility_matrix.md](20.16_gb_responsibility_matrix.md)
- [20.18_failure_modes_and_success_criteria.md](20.18_failure_modes_and_success_criteria.md)
- [20.205_execution_packet_xp_requirements.md](20.205_execution_packet_xp_requirements.md)
- [20.206_pipeline_a_b_synchronization_contract.md](20.206_pipeline_a_b_synchronization_contract.md)
- [20.207_execution_replay_specification.md](20.207_execution_replay_specification.md)
- [20.38_ts_implementation_guidelines.md](20.38_ts_implementation_guidelines.md)
- [20.39_ts_core_data_structures.md](20.39_ts_core_data_structures.md)
- [20.41_opbeh_requirements.md](20.41_opbeh_requirements.md)
- [20.42_obg_requirements.md](20.42_obg_requirements.md)
- [20.43_xlater_requirements.md](20.43_xlater_requirements.md)
- [20.55_srp_requirements.md](20.55_srp_requirements.md)
- [20.56_routing_table_schema.md](20.56_routing_table_schema.md)
- [20.57_trig_rb_semantic_trigger_requirements.md](20.57_trig_rb_semantic_trigger_requirements.md)

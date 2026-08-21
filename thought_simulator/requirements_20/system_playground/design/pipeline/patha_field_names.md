# patha_field_names.md — Canonical Field-Name Dictionary for Path-A

**Document ID:** patha_field_names  
**Version:** 0.1 (First Crystallization)  
**Status:** Draft — derived exclusively from the listed normative and playground documents  
**Scope:** Entire Path-A pipeline field surface for structural programs, testbenches, and dual-mode validation  
**Location:** `thought_simulator/requirements_20/system_playground/design/pipeline/`  

**Source documents (authoritative order):**  
1. 20.32_cob_requirements.md  
2. system_playground/primitives/cob/cob_requirements.md  
3. system_playground/testbenches/progressive_lineup_testing.md  
4. system_playground/design/pipeline/primitive_transfer_table1.md  
5. system_playground/design/pipeline/primitive_transfer_table2.md  
6. 20.107.020_cex-ccr_primitive.md  
7. 20.40.055_mcb_prim.md  
8. 20.15_ts_architecture_scaffold.md  
9. 20.105_tp_requirements.md  
10. 20.105.010_tp_meta_fields.md  
11. 20.105.020_tp_meta_provenance.md  
12. 20.105.030_tp_meta_usage.md  

**Rules applied:**  
- No invented field names.  
- Exact spelling and casing preserved.  
- Collisions resolved by preferring global normative documents (20.32, 20.105 series, 20.15) unless playground explicitly overrides.  
- Synonyms are not merged unless documents state they are identical.  
- Paths are shown with the conventional `TP.` prefix used in architecture documents; runtime resolvers treat paths relative to the TP root (progressive_lineup_testing.md).  
- This dictionary is the single reference for structural programs (`*_py_struc_pgm.md`) and testbenches.

---

## 1. Introduction

This document is the canonical field-name dictionary for the entire Path-A pipeline. It unifies every named structure, TP path, snapshot field, signal, metadata field, provenance field, usage field, transfer-surface field, identity-layer field, referent-map field, ordering-metric field, next-turn context field, lineage field, continuity field, importance field, and register field that appears in the twelve source documents.

It is intended for:

- structural programs (especially `cob_py_struc_pgm.md` and peer programs),  
- progressive dual-mode testbenches,  
- rulecheckers,  
- envelope-boundary guards,  
- deterministic replay validation.

All primitives, testbenches, and dictionaries SHALL resolve field paths against the names listed here.

---

## 2. TP Envelope Field Names

### 2.1 TP.identity.*

- `tp_identity` (block)  
  - `tp_id`  
  - `tp_seq`  
  - `cycle_id`  
  - `lane_id`  
  - `parent_tp_id` (optional)  
  - `schema_version`  
  - `profile_signature`  
  - `wire_map_version`  
  - `policy_signature`  
  - `timestamp_evidence` (optional)  

- `cob_state_snapshot` (identity envelope; architecture scaffold / 20.15)  
- `identity.geometry` (IdOB foundation)  
- `identity.continuity`  
- `identity.pressure`  
- `identity.residuals.{magnitude, pattern}`  
- `identity.freeze.state`  
- `identity.basin_surface.region`  

### 2.2 TP.metadata.*

**Categories (20.105.010):**  

- `TP.metadata.intake_metadata`  
  - `intake_status`  
  - `defect_list`  
  - `token_observations`  
  - `unicode_flags`  
  - `length_flags`  

- `TP.metadata.normalization_metadata`  
  - `normalized_tokens`  
  - `repair_actions`  
  - `repair_confidence`  
  - `token_alignment_map`  

- `TP.metadata.structural_metadata`  
  - `structural_roles`  
  - `segment_boundaries`  
  - `constraint_surfaces`  
  - `smoothing_actions`  

- `TP.metadata.routing_metadata`  
  - `routing_pathway`  
  - `routing_confidence`  
  - `arbitration_trace`  
  - `routing_features`  

- `TP.metadata.expressive_metadata`  
  - `elongation_patterns`  
  - `abbreviation_patterns`  
  - `omission_patterns`  
  - `stylization_flags`  

- `TP.metadata.repair_metadata`  
  - `repair_origin`  
  - `repair_type`  
  - `repair_provenance`  
  - `repair_alignment`  

- `TP.metadata.provenance_metadata`  
  - `commit_id`  
  - `commit_sequence`  
  - `primitive_origin`  
  - `commit_timestamp`  

- `TP.metadata.entropy_metadata`  
  - `delta_h`  
  - `entropy_trace`  
  - `entropy_commit_map`  

- `TP.metadata.continuity_metadata`  
  - `identity_anchors`  
  - `referent_lineage`  
  - `continuity_flags`  
  - `stability_flags`  
  - `clarifying_fields`  
  - `clarifying_subfields`  
  - `clarifying_subsubfields`  
  - `clarifying_subsubsubfields`  
  - `clarifying_subsubsubsubfields`  
  - `clarifying_importance`  
  - `clarifying_topology`  
  - `clarifying_provenance`  

- `TP.metadata.msl_metadata` / `TP.metadata.msl`  
  - `qualifiers`  
  - `clarifications`  
  - `stance`  
  - `shading`  
  - `intent`  
  - `direction`  
  - `coherence`  
  - `subculture`  
  - `msl_provenance`  

- `TP.metadata.context_metadata` / `TP.metadata.context`  
  - `relevance_flags`  
  - `copy_forward_flags`  
  - `reset_flags`  
  - `context_fields`  
  - `context_provenance`  

- `TP.metadata.residue_metadata` / `TP.metadata.residue`  
  - `structural_residue`  
  - `refinement_residue`  
  - `constraint_residue`  
  - `semantic_adjacent_residue`  
  - `presemantic_hash`  
  - `residue_provenance`  

- `TP.metadata.semantic_layer_metadata` / `TP.metadata.semantic_layer`  
  - `semantic_adjacent_signals`  
  - `semantic_layer_hash`  
  - `referent_adjacent_signals`  
  - `modality_stance_cues`  
  - `semantic_layer_provenance`  

- `TP.metadata.scoring_metadata` / `TP.metadata.scoring`  
  - `score_set`  
  - `score_conflict`  
  - `score_reason_code`  
  - `scoring_provenance`  

- `TP.metadata.identity_metadata` / `TP.metadata.identity`  
  - `identity_basin`  
  - `identity_shift_flags`  
  - `subculture_assignment`  
  - `qualifier_cluster`  
  - `identity_provenance`  

- `TP.metadata.next_context_metadata` / `TP.metadata.next_context`  
  - `next_context`  
  - `direction`  
  - `coherence`  
  - `stance`  
  - `subculture`  
  - `next_context_provenance`  

- `TP.metadata.freeze_metadata` / `TP.metadata.freeze`  
  - `freeze_signature`  
  - `rrw_binding`  
  - `policy_signature`  
  - `ssr_projection_map`  
  - `freeze_provenance`  

- `TP.metadata.semantic_residue_metadata` / `TP.metadata.semantic_residue`  
  - `entities[]`  
  - `facts[]`  
  - `alignment_scores`  
  - `provenance`  

- `TP.metadata.cil_metadata` / `TP.metadata.cil`  
  - `selected_conversation`  
  - `cil_reference`  
  - `projection_provenance`  

- `TP.metadata.cognitive_history[]` (append-only; CTP only)  
  - `cycle_id`  
  - `timestamp`  
  - `invariants` { `I_stab`, `R_res`, `P_cont`, `L_depth`, `Rt_adj`, `E_dens`, `C_coh` }  
  - `idob_geometry` { `neighborhood`, `k_id` }  
  - `idob_roles`  
  - `idob_residue`  
  - `idob_stability`  
  - `rb_adjacency_class`  
  - `rb_displacement_scale`  
  - `rb_regime_hint`  
  - `rb_route_proposal`  

### 2.3 TP.next_context.*

- `next_context`  
- `direction`  
- `coherence`  
- `stance`  
- `subculture`  
- `next_context_provenance`  

(Also appears under `TP.metadata.next_context_metadata`.)

### 2.4 TP.cst.core.* / CST-Core signals

- Freeze  
- Thaw  
- Continuity-restoration  
- stability-correction signals  
- stability signals  
- raw metrics  
- metric histories  

### 2.5 TP.cst.ms.* / CST-MS signals

- freeze command  
- thaw command  
- collapse-recovery  
- create-identity-layer  
- split  
- merge  
- strengthen_register  
- weaken_register  
- synthesized stability summaries  
- stability/instability summaries  
- structural commands  

### 2.6 TP.cst.mux.* / CST-Mux outputs

- unified_stability_packet  
- usp_tags  

### 2.7 TP.routing.*

- `routing_path`  
- `routing_filter`  
- `tr_needs_update`  
- `routing_metadata`  
- `RB_out` fields  

### 2.8 TP.cex.*

- `TP.cex.ie` (structural hints from CEx-IE)  
- `TP.cex.ccr`  
  - `alignment.identity`  
  - `alignment.clarifying`  
  - `alignment.context`  
  - `alignment.continuity`  
  - `alignment.reference`  
  - `alignment.semantic_residue`  
  - `scores.ambiguity`  
  - `scores.collapse`  
  - `scores.drift`  
  - `scores.stability`  
  - `decision`  
  - `selected_conversation`  
  - `provenance`  

### 2.9 TP.ob.* / OB-family

- structural maps (SOB, SROB, CnOB, SmOB)  
- residue fragments  
- importance cues  

### 2.10 TP.rb.*

- `routing_filter`  
- `RED` fields (read-only view for some primitives)  

### 2.11 TP.ie.*

- `normalized_text`  
- `ie_tokens`  
- `token_flags`  
- `structure`  
- `repair_annotations`  
- `replay metadata`  

### 2.12 TP.tpu.* / TPU

- `tp_update_request{}`  
- `tpu_audit_record`  
- `tpu_error`  
- `TP(N+1)`  

### 2.13 Other top-level / semantic envelopes

- `TP.semantic.importance`  
  - `entities[]` { `value`, `role`, `score`, `provenance` }  
  - `facts[]` { `value`, `role`, `score`, `provenance` }  
  - `provenance`  

- `TP.ce.candidate_set[]`  
  - `candidate_id`  
  - `fftm_fields`  
  - `structural_features`  
  - `semantic_adjacent_features`  
  - `next_context`  
  - `provenance`  

- `lineage_log[]`  
  - `lineage_seq`  
  - `module_id`  
  - `event_type` (CREATE | SPLIT | MERGE | UPDATE | RETIRE)  
  - `parent_ref`  
  - `child_refs[]`  
  - `partition_rationale_ref`  
  - `merge_contribution_ref`  

- `delta_h_percent` / `ΔH%`  
- `entropy_history[]`  
- `signature_history[]`  
- `policy_markers[]`  
- `difficulty_rating`  
- `mismatch_tags[]`  
- `anomaly_flags[]`  

- Evaluation-derived (read-only downstream):  
  - `TPTB`  
  - `TPSF`  

---

## 3. Primitive Ownership, Read/Write Boundaries

### 3.1 CEx-CCR (20.107.020)

**Owned / writes:**  
- `TP.cex.ccr.alignment.*`  
- `TP.cex.ccr.scores.*`  
- `TP.cex.ccr.decision`  
- `TP.cex.ccr.selected_conversation`  
- `TP.cex.ccr.provenance`  
- `TP.metadata.semantic_residue_metadata` (entities, facts, alignment_scores, provenance)  
- `TP.metadata.cil_metadata` (selected_conversation, cil_reference, projection_provenance)  

**Reads:**  
- `TP.cex.ie` (tokens, token_flags, normalized_text, structural_phrases, topic_hint, intent_hint, continuity_hint, reference_hint, register_hint, politeness_hint, direction_hint, coherence_hint, importance_hint)  
- `TP.cil` / CIL lineage + metrics (identity_lineage, clarifying_lineage, context_lineage, continuity_lineage, topology, metrics: primary_certainty, ambiguity_score, collapse_risk, stability_score, volatility_score, drift_score, lineage_confidence, semantic_residue, next_context)  

**Forbidden:**  
- Modification of upstream TP fields  
- Repackaging (CEx-IE) or downstream packaging (CEx-Pck)  

### 3.2 MCB (20.40.055)

**Owned / writes:**  
- meaning-layer deltas  
- next-turn clarifying/context fields (`TP.metadata.next_context_metadata` / `TP.next_context.*`)  
- `proposition_set` (transfer-table framing)  

**Reads (read-only):**  
- meaning-layer fields (IdOB output)  
- clarifying fields (COB / CIL / CEx / CE / ISc / TPU)  
- `TP.metadata.cil_metadata.identity_lineage`  
- `TP.metadata.cil_metadata.continuity_lineage`  
- `TP.metadata.cil_metadata.topology`  
- `TP.metadata.cil_metadata.metrics` (ambiguity_score, collapse_risk, drift_score, stability_score, lineage_confidence)  
- `TP.metadata.cil_metadata.register_continuity`  
- `TP.metadata.cil_metadata.importance_continuity`  
- applicable TP-stream metadata (context, clarifying, identity, continuity, expressive, normalization, semantic-layer, residue, next_context)  

**Forbidden:**  
- Modification of current-turn clarifying fields  
- Routing vectors / `TP.TR`  
- Structural ΔH%  
- Path-B envelopes  
- SSG / STPX / structural OB primitives  

### 3.3 COB (20.32 + playground cob_requirements)

**Owned / writes:**  
- identity-layer objects (≤20)  
- `cob_state_snapshot`  
- stabilized identity-layer snapshot for CIL  
- ordering metrics (recency, frequency, density, total access count, chronological ordering vector, sliding-window frequency over last 10)  
- clarifying fields (bounded) + importance scores  
- identity_lineage, continuity_lineage, topology  
- metrics: ambiguity_score, collapse_risk, drift_score, stability_score, lineage_confidence  
- register_continuity, importance_continuity  
- structural event markers (MERGE / SPLIT) to CST-Core / CST-MS  
- contributions to `TP.lineage_log[]`  
- (transfer-table framing) `canonical_output_record`, `canonical_output_tags`  

**Reads:**  
- CST-Core signals (Freeze, Thaw, Continuity-restoration, stability-correction)  
- CST-MS structural commands (freeze, thaw, collapse-recovery, create-identity-layer, split, merge, strengthen_register, weaken_register)  
- OuBA meaning packets, strength updates, ambiguity/confidence, lineage continuity, register updates  
- IdOB identity-importance (indirect via TP → OuBA)  
- SmOB semantic-adjacent importance (indirect)  
- MCB next-turn context (`TP.next_context{}` / `TP.metadata.next_context_metadata`)  
- `TP.semantic.importance`  
- `TP.cex.ccr.selected_conversation` / `TP.metadata.cil_metadata`  

**Forbidden:**  
- Interaction with OB, IB, RB, TB, InB, OuB  
- Semantic interpretation or canonical semantics derivation  
- Placeholder promotion, replay/export, compaction, redaction  
- Modification of semantic-importance scores or roles  
- Any signals from CST-Mux  
- Direct signals from IdOB / SmOB / MCB  

**Snapshot fields:**  
- `cob_state_snapshot`  
- stabilized identity-layer snapshot  

**Transfer-block fields (to CIL):**  
- identity layers  
- referent maps  
- clarifying fields  
- importance maps  
- identity-importance  
- semantic-adjacent importance  
- next-turn context  
- ordering metrics  
- register continuity  
- conversation_count  
- initial_state_complete  
- importance continuity  

### 3.4 CIL

**Owned / writes:**  
- linkage_record  
- linkage_tags  
- (possible) basin/continuity_surface adjustments  

**Reads:**  
- COB stabilized identity-layer snapshot  
- canonical_output_record (transfer framing)  
- identity geometry  

**Forbidden:**  
- Writing semantic_core  
- Changing freeze state  

### 3.5 CST-Core

**Owned / writes:**  
- stability signals  
- raw metrics  
- metric histories  
- Freeze / Thaw / Continuity-restoration signals  

**Reads:**  
- identity geometry  
- canonical_output_record / linkage_record  

**Forbidden:**  
- Modification of identity topology  

### 3.6 CST-MS

**Owned / writes:**  
- stability/instability summaries  
- structural commands (freeze/thaw/split/merge/create/etc.)  
- synthesized stability summaries  

**Reads:**  
- raw metrics + thresholds + histories from CST-Core  

### 3.7 CST-Mux

**Owned / writes:**  
- unified_stability_packet  
- usp_tags  

**Forbidden:**  
- Identity or semantic modifications  

---

## 4. Pipeline Transfer-Surface Fields

- `packed_record`  
- `packed_tags`  
- `canonical_output_record`  
- `canonical_output_tags`  
- `routing_path`  
- `lineage_log`  
- `tb_trace`  
- `tp_update_request{}` (may carry isc, cil, cob, cop, idob_update, mcb_update, rbu_update, metadata)  
- `tpu_audit_record`  
- `tpu_error`  

---

## 5. Identity-Layer Fields (from 20.32)

### 5.1 IdentityLayer schema

```
IdentityLayer {
    layer_id: StableID,
    referent_map: ReferentMap,
    lineage: LineageStructure,
    strength: float,
    importance: float,
    ambiguity: float,
    decay_state: float,
    register: string,
    timestamps: {
        created: TurnID,
        updated: TurnID
    }
}
```

### 5.2 ReferentEntry schema

```
ReferentEntry {
    referent_id: StableID,
    surface_forms: [string],
    attributes: { key: value },
    strength: float,
    confidence: float,
    ambiguity: float,
    lineage_pointer: StableID,
    register: string,
    timestamps: {
        created: TurnID,
        updated: TurnID
    }
}
```

### 5.3 Ordering metrics (playground + 20.32)

- recency  
- frequency  
- density  
- total access count / conversation_count  
- chronological ordering vector  
- sliding-window frequency distribution over the last 10 access events  

### 5.4 Ambiguity / Stability / Lineage / Topology / Continuity / Importance / Register

- ambiguity / ambiguity_score  
- collapse_risk  
- drift_score  
- stability_score / stability  
- lineage_confidence  
- identity_lineage  
- continuity_lineage  
- topology  
- register_continuity  
- importance_continuity  
- identity-importance  
- semantic-adjacent importance  
- clarifying fields (max 10 per layer) + subfields (max 100 total, max 4 hierarchical levels) + importance scores  

---

## 6. Next-Turn Context Fields

- `next_context`  
- `direction`  
- `coherence`  
- `stance`  
- `subculture`  
- `next_context_provenance`  
- clarifying fields (structural-only; no semantic interpretation)  
- importance updates via continuity metrics  
- lineage continuity markers  

**Rules (playground HLR-COB-015 … 023):**  
- Ingest from `TP.next_context{}`  
- Validate against stabilized identity-layer objects  
- Merge with deterministic continuity rules  
- Expose to CIL without modification  
- Preserve across freeze/thaw  
- Treat strictly as structural metadata  

---

## 7. CIL Intake Packet Fields

- identity_layers[] / identity layers  
- referent maps  
- clarifying fields  
- importance maps / identity-importance / semantic-adjacent importance  
- next-turn context  
- ordering metrics  
- register continuity  
- conversation_count  
- initial_state_complete  
- importance continuity  
- identity_lineage  
- continuity_lineage  
- topology  
- metrics (ambiguity_score, collapse_risk, drift_score, stability_score, lineage_confidence)  

---

## 8. Alphabetical Canonical Field Name List

(All unique names extracted; casing and spelling preserved.)

- abbreviation_patterns  
- alignment.clarifying  
- alignment.context  
- alignment.continuity  
- alignment.identity  
- alignment.reference  
- alignment.semantic_residue  
- alignment_scores  
- ambiguity  
- ambiguity_score  
- anomaly_flags  
- arbitration_trace  
- attributes  
- basin_surface.region  
- candidate_id  
- candidate_set  
- canonical_output_record  
- canonical_output_tags  
- child_refs  
- cil_reference  
- clarifying_fields  
- clarifying_importance  
- clarifying_lineage  
- clarifying_provenance  
- clarifying_subfields  
- clarifying_subsubfields  
- clarifying_subsubsubfields  
- clarifying_subsubsubsubfields  
- clarifying_topology  
- collapse  
- collapse_risk  
- coherence  
- coherence_hint  
- commit_id  
- commit_sequence  
- commit_timestamp  
- constraint_residue  
- constraint_surfaces  
- context_fields  
- context_lineage  
- context_provenance  
- continuity  
- continuity_flags  
- continuity_hint  
- continuity_lineage  
- continuity_metadata  
- conversation_count  
- copy_forward_flags  
- cycle_id  
- decay_state  
- decision  
- defect_list  
- delta_h  
- delta_h_percent  
- direction  
- direction_hint  
- drift  
- drift_score  
- elongation_patterns  
- entities  
- entropy_commit_map  
- entropy_history  
- entropy_trace  
- event_type  
- facts  
- freeze  
- freeze.state  
- freeze_signature  
- geometric_history  
- geometric_state  
- identity  
- identity_anchors  
- identity_basin  
- identity_importance  
- identity_lineage  
- identity_shift_flags  
- ie_tokens  
- importance  
- importance_continuity  
- importance_hint  
- initial_state_complete  
- intent  
- intent_hint  
- intake_status  
- k_id  
- lane_id  
- layer_id  
- length_flags  
- lineage  
- lineage_confidence  
- lineage_log  
- lineage_pointer  
- lineage_seq  
- merge_contribution_ref  
- mismatch_tags  
- module_id  
- neighborhood  
- next_context  
- next_context_provenance  
- normalized_text  
- normalized_tokens  
- omission_patterns  
- packed_record  
- packed_tags  
- parent_ref  
- parent_tp_id  
- partition_rationale_ref  
- policy_markers  
- policy_signature  
- politeness_hint  
- presemantic_hash  
- primary_certainty  
- primitive_origin  
- profile_signature  
- projection_provenance  
- proposition_set  
- provenance  
- qualifier_cluster  
- qualifiers  
- rb_adjacency_class  
- rb_displacement_scale  
- rb_regime_hint  
- rb_route_proposal  
- reference_hint  
- referent_adjacent_signals  
- referent_id  
- referent_lineage  
- referent_map  
- refinement_residue  
- register  
- register_continuity  
- register_hint  
- relevance_flags  
- repair_actions  
- repair_alignment  
- repair_annotations  
- repair_confidence  
- repair_origin  
- repair_provenance  
- repair_type  
- reset_flags  
- residue_provenance  
- routing_confidence  
- routing_features  
- routing_filter  
- routing_path  
- routing_pathway  
- rrw_binding  
- schema_version  
- score  
- score_conflict  
- score_reason_code  
- score_set  
- scores.ambiguity  
- scores.collapse  
- scores.drift  
- scores.stability  
- scoring_provenance  
- segment_boundaries  
- selected_conversation  
- semantic_adjacent_features  
- semantic_adjacent_importance  
- semantic_adjacent_residue  
- semantic_adjacent_signals  
- semantic_layer_hash  
- semantic_layer_provenance  
- semantic_residue  
- shading  
- signature_history  
- smoothing_actions  
- ssr_projection_map  
- stability  
- stability_flags  
- stability_score  
- stance  
- strength  
- structural_features  
- structural_residue  
- structural_roles  
- structure  
- stylization_flags  
- subculture  
- subculture_assignment  
- surface_forms  
- tb_trace  
- thaw  
- timestamp  
- timestamps.created  
- timestamps.updated  
- token_alignment_map  
- token_flags  
- token_observations  
- topic_hint  
- topology  
- tp_id  
- tp_seq  
- tp_update_request  
- tpu_audit_record  
- tpu_error  
- tr_needs_update  
- unicode_flags  
- unified_stability_packet  
- usp_tags  
- value  
- volatility_score  
- wire_map_version  

---

**End of canonical dictionary.**  
All structural programs and testbenches SHALL treat the names above as authoritative. Any future field addition requires an update to this document and the corresponding HLR sources.

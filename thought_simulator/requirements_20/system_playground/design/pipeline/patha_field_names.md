# patha_field_names.md — Canonical Field-Name Dictionary for Path-A

**Document ID:** patha_field_names  
**Version:** 0.4 (CST-Mux envelope lock)  
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
13. 20.32.010.010_cst-core.md  
14. system_playground/primitives/cst_core/cst_core_py_struc_pgm.md (v0.1 CP-approved path map)  
15. system_playground/primitives/cil/cil_py_struc_pgm.md / 20.33 (CIL intake path)  
16. 20.32.010.020_cst-ms.md  
17. system_playground/primitives/cst_ms/cst_ms_py_struc_pgm.md (v0.1 CP-approved path map)  
18. 20.32.010.030_cst-mux.md  
19. system_playground/primitives/cst_mux/cst_mux_py_struc_pgm.md (v0.1 CP-approved path map)  

**Rules applied:**  
- No invented field names.  
- Exact spelling and casing preserved.  
- Collisions resolved by preferring global normative documents (20.32, 20.105 series, 20.15) unless playground explicitly overrides.  
- Synonyms are not merged unless documents state they are identical.  
- Paths are shown with the conventional `TP.` prefix used in architecture documents; runtime resolvers treat paths relative to the TP root (progressive_lineup_testing.md).  
- This dictionary is the single reference for structural programs (`*_py_struc_pgm.md`) and testbenches.

---

## 1. Introduction

This document is the canonical field-name dictionary for the entire Path-A pipeline. It unifies every named structure, TP path, snapshot field, signal, metadata field, provenance field, usage field, transfer-surface field, identity-layer field, referent-map field, ordering-metric field, next-turn context field, lineage field, continuity field, importance field, and register field that appears in the source documents.

It is intended for:

- structural programs (especially `cob_py_struc_pgm.md`, `cil_py_struc_pgm.md`, `cst_core_py_struc_pgm.md`, `cst_ms_py_struc_pgm.md`, `cst_mux_py_struc_pgm.md` and peer programs),  
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

### 2.4 TP.cst.core.* / CST-Core (LOCKED v0.1)

**Top-level envelope (non-negotiable):**

- `TP.cst.core`

This path is owned exclusively by the CST-Core primitive.  
It is written during `cst_core.process()` and SHALL NOT be written by any other component.

**Canonical nested map (from `cst_core_py_struc_pgm.md` §2, CP-approved):**

```
TP.cst.core.status
  turn_index
  layer_count
  frozen_layers[]

TP.cst.core.signals.freeze
  frozen_objects[]
  reason

TP.cst.core.signals.thaw
  thawed_objects[]
  reason

TP.cst.core.signals.continuity_restoration
  restored_objects[]
  reason

TP.cst.core.signals.drift
  affected_objects[]
  magnitude

TP.cst.core.signals.oscillation
  affected_objects[]
  frequency
  amplitude

TP.cst.core.signals.ambiguity
  affected_objects[]
  increased[]
  decreased[]

TP.cst.core.signals.collapse
  collapsed_objects[]
  severity

TP.cst.core.metrics.per_layer
  <StableID>.drift
  <StableID>.oscillation
  <StableID>.ambiguity
  <StableID>.stability
  <StableID>.collapse
  <StableID>.continuity
  <StableID>.combined_instability

TP.cst.core.metrics.integrated
  (10-turn aggregates as available in v0.1)

TP.cst.core.history
  window_len          # fixed 10
  turns[]             # capped at 10
    turn_index
    per_layer_snapshot_ref_or_digest
    metric_summary

TP.cst.core.lineage_stability
  stable_lineage[]
  unstable_lineage[]

TP.cst.core.audit
  slice
  provisional_metrics
  notes[]
```

**Signal routing (logical consumers; all fields still live under `TP.cst.core`):**

| Fields | Logical consumers |
|--------|-------------------|
| `signals.freeze`, `signals.thaw`, `signals.continuity_restoration` | COB and CST-Mux |
| `signals.drift`, `signals.oscillation`, `signals.ambiguity`, `signals.collapse` + metrics/histories | CST-MS and CST-Mux only (NOT COB structural commands) |

**Notes:**

- Runtime resolvers use paths relative to TP root (`cst.core...`), not a leading `TP.` key.  
- Progressive lineup dual-mode testbenches SHALL assert against this map.  
- Structural programs SHALL NOT invent a second CST-Core envelope outside `TP.cst.core`.  
- See Section 9 for the dedicated CST-Core lock summary.

### 2.5 TP.cst.ms.* / CST-MS (LOCKED v0.1)

**Prior coarse inventory (retained):**  
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

**Top-level envelope (non-negotiable):**

- `TP.cst.ms`

This path is owned exclusively by the CST-MS primitive.  
It is written during `cst_ms.process()` and SHALL NOT be written by any other component.

**Canonical nested map (from `cst_ms_py_struc_pgm.md` §2, CP-approved):**

```
TP.cst.ms.status
  turn_index
  layer_count

TP.cst.ms.normalized_metrics
  per_layer.<StableID>.{drift, oscillation, ambiguity, collapse, continuity}
  aggregate.{drift, oscillation, ambiguity, collapse, continuity}   # optional

TP.cst.ms.weighted_metrics
  per_layer.<StableID>.{...}
  aggregate.{...}   # optional

TP.cst.ms.stability
  per_layer.<StableID>.value
  aggregate.value   # optional

TP.cst.ms.instability
  per_layer.<StableID>.value
  aggregate.value

TP.cst.ms.collapse_risk
  per_layer.<StableID>.value
  aggregate.value

TP.cst.ms.freeze_risk
  per_layer.<StableID>.value
  aggregate.value

TP.cst.ms.thaw_readiness
  per_layer.<StableID>.value
  aggregate.value

TP.cst.ms.ambiguity_summary
  count

TP.cst.ms.drift_summary
  magnitude

TP.cst.ms.oscillation_summary
  frequency
  amplitude

TP.cst.ms.commands.freeze
  layers[]
  reason

TP.cst.ms.commands.thaw
  layers[]
  reason

TP.cst.ms.commands.collapse_recovery
  layers[]
  reason

TP.cst.ms.commands.create_identity_layer
  requests[]

TP.cst.ms.commands.split
  layers[]
  reason

TP.cst.ms.commands.merge
  pairs[]
  reason

TP.cst.ms.command_log[]
  turn_index
  command_type    # freeze|thaw|collapse_recovery|create_identity_layer|split|merge
  targets
  reason
  metrics_snapshot_ref

TP.cst.ms.diagnostics
  sync_mismatch
  sync_mismatch_detail

TP.cst.ms.metadata
  new_context_required

TP.cst.ms.stability_window[]
  turn_index
  stability.value
  instability.value
  collapse_risk.value
  freeze_risk.value
  thaw_readiness.value

TP.cst.ms.history
  window_len          # fixed 10

TP.cst.ms.audit
  slice
  provisional_metrics
  notes[]
```

**Note on strengthen_register / weaken_register:**  
These names remain in the coarse inventory (architecture / transfer tables). They are **not** part of the six sole structural commands in 20.32.010.020 HLR-035. Realization may place them under a future extension; v0.1 progressive lock does not require them under `commands`.

**Routing (logical consumers; fields live under `TP.cst.ms`):**

| Fields | Logical consumers |
|--------|-------------------|
| `commands.*` | COB |
| `command_log` | replay / audit |
| synthesis summaries / risks / window | CST-Mux, downstream summary consumers |
| `diagnostics.sync_mismatch` | CST-Mux only (no extra structural commands from mismatch) |
| `metadata.new_context_required` | COB / context downstream; also packaged into USP by CST-Mux |

**Notes:**  
- Runtime resolvers use paths relative to TP root (`cst.ms...`).  
- See Section 10 for the dedicated CST-MS lock summary.

### 2.6 TP.cst.mux.* / CST-Mux (LOCKED v0.1)

**Prior coarse inventory (retained):**  
- unified_stability_packet  
- usp_tags  

**Top-level envelope (non-negotiable):**

- `TP.cst.mux`

This path is owned exclusively by the CST-Mux primitive.  
It is written during `cst_mux.process()` and SHALL NOT be written by any other component.

**Canonical nested map (from `cst_mux_py_struc_pgm.md` §2, CP-approved):**

```
TP.cst.mux.status
  turn_index
  layer_count

TP.cst.mux.layer_index
  <StableID>: int    # deterministic 0..n-1 by sorted StableID

TP.cst.mux.unified_stability_packet
  turn_index
  layer_index

  core:
    signals:
      freeze / thaw / continuity_restoration / drift / oscillation / ambiguity / collapse
    metrics:
      per_layer / integrated
    status:
      frozen_layers[]   # when present on Core

  ms:
    normalized_metrics / weighted_metrics   # optional pack-through
    stability / instability
    collapse_risk / freeze_risk / thaw_readiness
    ambiguity_summary / drift_summary / oscillation_summary
    commands
    command_log
    diagnostics:
      sync_mismatch
      sync_mismatch_detail
    metadata:
      new_context_required

  flags:
    activation
    freeze
    thaw
    continuity

  new_context_required    # top-level convenience; same value as ms.metadata

TP.cst.mux.usp_tags[]

TP.cst.mux.history
  window_len          # optional; 10 when usp_window used
  usp_window[]        # optional progressive multi-turn history

TP.cst.mux.audit
  slice
  provisional_flags
  notes[]
```

**Routing (logical consumers; fields live under `TP.cst.mux`):**

| Fields | Logical consumers |
|--------|-------------------|
| `unified_stability_packet` | **CIL only** (for replay reconstruction) |
| `usp_tags` | debug / progressive |
| `layer_index` | USP alignment |

**Notes:**  
- USP is **never** sent to COB (20.32.010.030 HLR-011, 012). COB receives Core/MS signals and commands on their own envelopes.  
- Mux SHALL NOT modify, reinterpret, threshold, or synthesize upstream signals (HLR-018).  
- Runtime resolvers use paths relative to TP root (`cst.mux...`).  
- See Section 11 for the dedicated CST-Mux lock summary.

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
- CST-Core signals under `TP.cst.core.signals.freeze|thaw|continuity_restoration`  
- CST-MS structural commands under `TP.cst.ms.commands.*` (freeze, thaw, collapse_recovery, create_identity_layer, split, merge; coarse inventory also lists strengthen_register, weaken_register)  
- CST-MS metadata such as `TP.cst.ms.metadata.new_context_required` when present  
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
- Any signals from CST-Mux / USP (COB does not consume USP)  
- Direct signals from IdOB / SmOB / MCB  
- Treating CST-Core raw metrics (drift/oscillation/ambiguity/collapse) as structural commands  

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
- `TP.cil.intake_packet` (and `TP.cil.intake_packet.audit`) — see Section 7.1  

**Reads:**  
- COB stabilized identity-layer snapshot  
- USP from CST-Mux under `TP.cst.mux.unified_stability_packet`  
- structural cues / intake metadata / next_context  

**Forbidden:**  
- Writing semantic_core  
- Changing freeze state / COB topology  
- Writing `TP.cst.core`  
- Writing `TP.cst.ms`  
- Writing `TP.cst.mux`  

### 3.5 CST-Core (LOCKED)

**Owned / writes:**  
- Entire `TP.cst.core` envelope (Section 2.4 / Section 9)  
  - `status`, `signals`, `metrics`, `history`, `lineage_stability`, `audit`  
- Optional append of module id `cst_core` to `routing_path`  

**Reads (read-only):**  
- `identity.cob_state_snapshot` / COB identity layers  
- Optional OuBA committed identity reference  
- `lineage_log` MERGE/SPLIT markers (hygiene only)  
- Prior `TP.cst.core.history` / freeze status for replay  

**Forbidden:**  
- Modification of identity topology / `cob_state_snapshot`  
- Create / Split / Merge / Collapse-recovery commands  
- Writing `routing_filter`, RED, geometric_state, semantic_core  
- Writing `TP.cil.intake_packet`  
- Writing `TP.cst.ms`  
- Writing `TP.cst.mux`  
- Accepting control commands from CST-MS  

### 3.6 CST-MS (LOCKED)

**Owned / writes:**  
- Entire `TP.cst.ms` envelope (Section 2.5 / Section 10)  
  - `status`, `normalized_metrics`, `weighted_metrics`, `stability`, `instability`  
  - `collapse_risk`, `freeze_risk`, `thaw_readiness`  
  - `ambiguity_summary`, `drift_summary`, `oscillation_summary`  
  - `commands`, `command_log`, `diagnostics`, `metadata`, `stability_window`, `history`, `audit`  
- Optional append of module id `cst_ms` to `routing_path`  
- Coarse inventory names retained: synthesized stability summaries, stability/instability summaries, structural commands, freeze/thaw/collapse-recovery/create-identity-layer/split/merge commands; strengthen_register / weaken_register remain listed for architecture continuity  

**Reads (read-only):**  
- raw metrics + histories from `TP.cst.core` (signals.drift|oscillation|ambiguity|collapse, metrics, history, status, freeze/thaw/continuity_restoration signals)  
- Optional OuBA committed identity-layer snapshots (HLR-044)  
- Optional restricted COB diagnostic view for sync mismatch only (HLR-045–046)  
- `lineage_log` MERGE/SPLIT markers  
- Prior `TP.cst.ms.stability_window` / `command_log` for replay  

**Forbidden:**  
- Modification of identity topology / `cob_state_snapshot` (commands are emitted fields; COB applies them)  
- Writing `TP.cst.core`  
- Writing `TP.cil.intake_packet`  
- Writing `TP.cst.mux`  
- Deriving structural commands from COB internal state (HLR-046)  
- Issuing additional structural commands in response to sync mismatch (HLR-048)  

### 3.7 CST-Mux (LOCKED)

**Owned / writes:**  
- Entire `TP.cst.mux` envelope (Section 2.6 / Section 11)  
  - `status`, `layer_index`, `unified_stability_packet`, `usp_tags`, `history`, `audit`  
- Optional append of module id `cst_mux` to `routing_path`  
- Coarse inventory names retained: `unified_stability_packet`, `usp_tags`  

**Reads (read-only):**  
- CST-Core signals and metrics under `TP.cst.core` for USP packaging / TP replay  
- CST-MS synthesis summaries, risks, commands, diagnostics, metadata under `TP.cst.ms` for USP packaging / TP replay  
- Prior optional `TP.cst.mux.history.usp_window` when multi-turn fixtures seed it  

**Forbidden:**  
- Accepting data, snapshots, or signals from COB (HLR-006)  
- Sending USP (or any derivative) to COB (HLR-011, 012)  
- Issuing any commands to COB, CIL, or other modules (HLR-022)  
- Modifying, reinterpreting, thresholding, or synthesizing received signals (HLR-018)  
- Writing `TP.cst.core`, `TP.cst.ms`, `TP.cil.intake_packet`, or `identity.cob_state_snapshot`  
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

### 7.1 Canonical TP Path for CIL Intake Packet

**Top-level envelope path (non-negotiable):**

- `TP.cil.intake_packet`

This path is owned exclusively by the CIL primitive.  
It is created during `cil.process()` and SHALL NOT be written by any other component.

**Audit location (v0.1 decision):**

- `TP.cil.intake_packet.audit`

The audit records truncation events, clarifying-field drops, and packet-assembly provenance.  
Future versions MAY relocate audit ownership to CEx-CCR, but v0.1 SHALL treat the audit as part of the CIL packet.

**Notes:**

- This path is required for progressive lineup dual-mode testbenches.  
- Structural programs SHALL resolve all CIL envelope references against this canonical path.  
- Subfield names listed in Section 7 remain authoritative and SHALL appear under `TP.cil.intake_packet`.

---

## 8. Alphabetical Canonical Field Name List

(All unique names extracted; casing and spelling preserved.)

- abbreviation_patterns  
- activated  
- activation  
- activation_flags  
- affected_objects  
- aggregate  
- alignment.clarifying  
- alignment.context  
- alignment.continuity  
- alignment.identity  
- alignment.reference  
- alignment.semantic_residue  
- alignment_scores  
- ambiguity  
- ambiguity_score  
- ambiguity_summary  
- amplitude  
- anomaly_flags  
- arbitration_trace  
- attributes  
- audit  
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
- collapse_recovery  
- collapse_risk  
- collapsed_objects  
- combined_instability  
- command_log  
- command_type  
- commands  
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
- continuity_restoration  
- continuous  
- conversation_count  
- copy_forward_flags  
- create_identity_layer  
- cycle_id  
- decay_state  
- decision  
- defect_list  
- decreased  
- delta_h  
- delta_h_percent  
- diagnostics  
- direction  
- direction_hint  
- drift  
- drift_score  
- drift_summary  
- elongation_patterns  
- entities  
- entropy_commit_map  
- entropy_history  
- entropy_trace  
- event_type  
- facts  
- flags  
- freeze  
- freeze.state  
- freeze_flags  
- freeze_risk  
- freeze_signature  
- frequency  
- frozen  
- frozen_layers  
- frozen_objects  
- geometric_history  
- geometric_state  
- history  
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
- increased  
- initial_state_complete  
- instability  
- intake_packet  
- intake_status  
- integrated  
- intent  
- intent_hint  
- k_id  
- lane_id  
- layer_count  
- layer_id  
- layer_index  
- layers  
- length_flags  
- lineage  
- lineage_confidence  
- lineage_log  
- lineage_pointer  
- lineage_seq  
- lineage_stability  
- magnitude  
- merge  
- merge_contribution_ref  
- metric_summary  
- metrics  
- metrics_snapshot_ref  
- mismatch_tags  
- module_id  
- neighborhood  
- new_context_required  
- next_context  
- next_context_provenance  
- normalized_metrics  
- normalized_text  
- normalized_tokens  
- notes  
- omission_patterns  
- oscillation  
- oscillation_summary  
- packed_record  
- packed_tags  
- pairs  
- parent_ref  
- parent_tp_id  
- partition_rationale_ref  
- per_layer  
- per_layer_snapshot_ref_or_digest  
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
- provisional_flags  
- provisional_metrics  
- qualifier_cluster  
- qualifiers  
- rb_adjacency_class  
- rb_displacement_scale  
- rb_regime_hint  
- rb_route_proposal  
- reason  
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
- requests  
- reset_flags  
- residue_provenance  
- restored_objects  
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
- severity  
- shading  
- signature_history  
- signals  
- slice  
- smoothing_actions  
- split  
- ssr_projection_map  
- stability  
- stability_flags  
- stability_score  
- stability_window  
- stable_lineage  
- stance  
- status  
- strength  
- strengthen_register  
- structural_features  
- structural_residue  
- structural_roles  
- structure  
- stylization_flags  
- subculture  
- subculture_assignment  
- surface_forms  
- sync_mismatch  
- sync_mismatch_detail  
- targets  
- tb_trace  
- thaw  
- thaw_flags  
- thaw_readiness  
- thawed  
- thawed_objects  
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
- turn_index  
- turns  
- unicode_flags  
- unified_stability_packet  
- unstable_lineage  
- usp_tags  
- usp_window  
- value  
- volatility_score  
- weaken_register  
- weighted_metrics  
- window_len  
- wire_map_version  

---

## 9. Canonical TP Path for CST-Core Envelope (LOCKED v0.1)

**Top-level envelope path (non-negotiable):**

- `TP.cst.core`

This path is owned exclusively by the CST-Core primitive.  
It is written during `cst_core.process()` and SHALL NOT be written by any other component.

**Required top-level children under `TP.cst.core`:**

| Child | Purpose |
|-------|---------|
| `status` | turn_index, layer_count, frozen_layers |
| `signals` | freeze, thaw, continuity_restoration, drift, oscillation, ambiguity, collapse |
| `metrics` | per_layer, integrated |
| `history` | window_len (10), turns[] (capped at 10) |
| `lineage_stability` | stable_lineage, unstable_lineage |
| `audit` | slice, provisional_metrics, notes |

**Authority:**  
- `20.32.010.010_cst-core.md` (HLRs)  
- `cst_core_py_struc_pgm.md` §2 (CP-approved nested map)  

**Notes:**  
- Progressive dual-mode testbenches SHALL resolve CST-Core expected fields against this section.  
- No second envelope outside `TP.cst.core` is permitted for CST-Core outputs.  
- Final metric formulas and thresholds remain Defer; field **names and paths** are locked.

---

## 10. Canonical TP Path for CST-MS Envelope (LOCKED v0.1)

**Top-level envelope path (non-negotiable):**

- `TP.cst.ms`

This path is owned exclusively by the CST-MS primitive.  
It is written during `cst_ms.process()` and SHALL NOT be written by any other component.

**Required top-level children under `TP.cst.ms`:**

| Child | Purpose |
|-------|---------|
| `status` | turn_index, layer_count |
| `normalized_metrics` | per_layer / optional aggregate |
| `weighted_metrics` | per_layer / optional aggregate |
| `stability` / `instability` | synthesized scores |
| `collapse_risk` / `freeze_risk` / `thaw_readiness` | risk scores |
| `ambiguity_summary` / `drift_summary` / `oscillation_summary` | summaries |
| `commands` | freeze, thaw, collapse_recovery, create_identity_layer, split, merge |
| `command_log` | replay-safe command history |
| `diagnostics` | sync_mismatch, sync_mismatch_detail |
| `metadata` | new_context_required |
| `stability_window` | ≤10 turn synthesis window |
| `history` | window_len (10) |
| `audit` | slice, provisional_metrics, notes |

**Authority:**  
- `20.32.010.020_cst-ms.md` (HLRs)  
- `cst_ms_py_struc_pgm.md` §2 (CP-approved nested map)  

**Notes:**  
- Progressive dual-mode testbenches SHALL resolve CST-MS expected fields against this section.  
- No second envelope outside `TP.cst.ms` is permitted for CST-MS outputs.  
- Final weights, thresholds, and create/split/merge predicates remain Defer; field **names and paths** are locked.  
- Coarse inventory names from earlier dictionary revisions (strengthen_register, weaken_register, synthesized stability summaries, structural commands) are retained in §2.5 and §3.6.

---

## 11. Canonical TP Path for CST-Mux Envelope (LOCKED v0.1)

**Top-level envelope path (non-negotiable):**

- `TP.cst.mux`

This path is owned exclusively by the CST-Mux primitive.  
It is written during `cst_mux.process()` and SHALL NOT be written by any other component.

**Required top-level children under `TP.cst.mux`:**

| Child | Purpose |
|-------|---------|
| `status` | turn_index, layer_count |
| `layer_index` | deterministic StableID → int map |
| `unified_stability_packet` | USP: core + ms packs, flags, new_context_required |
| `usp_tags` | optional short tags |
| `history` | optional window_len / usp_window |
| `audit` | slice, provisional_flags, notes |

**Authority:**  
- `20.32.010.030_cst-mux.md` (HLRs)  
- `cst_mux_py_struc_pgm.md` §2 (CP-approved nested map)  

**Notes:**  
- Progressive dual-mode testbenches SHALL resolve CST-Mux expected fields against this section.  
- No second envelope outside `TP.cst.mux` is permitted for CST-Mux outputs.  
- USP is delivered **only to CIL** (logical consumer). USP is **never** sent to COB.  
- Mux packages without modifying Core/MS signals; field **names and paths** are locked.  
- Coarse inventory names `unified_stability_packet` and `usp_tags` are retained from earlier dictionary revisions.

---

**End of canonical dictionary.**  
All structural programs and testbenches SHALL treat the names above as authoritative. Any future field addition requires an update to this document and the corresponding HLR sources.

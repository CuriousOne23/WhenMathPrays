# 📘 **Primitive Transfer Table (Compressed Hybrid Edition)**  
**Path‑A Pipeline: InB → IIInB → IE → CE → TPU → SOB → SROB → CnOB → SmOB → WrdNm → ISc → SSG → STPX → DCB → RB → IdOB**

**Canonical Field Names:** All field names in this document are governed by  
`thought_simulator/requirements_20/system_playground/design/pipeline/patha_field_names.md`.  
That dictionary is the single authoritative source for structural programs and testbenches.

## Path A – Bounded Semantics Requirement

Path A primitives are semantic, but only within bounded scope. Each primitive must
perform the meaning work inherent to its primary job, and no more. Meaning in Path A
is not forbidden; it is constrained, localized, and explicitly recorded.

### Core Principle
Every primitive in Path A operates under domain‑specific semantic assumptions required
to perform its function (normalization, segmentation, routing, clarification, repair,
naming, classification, update, join, constraint extraction, cue extraction, etc.).
These assumptions must be:
- recognized,
- bounded to the primitive’s domain,
- explicitly defined in the primitive’s transfer function,
- recorded in TP fields for downstream use,
- deterministic and replay‑safe.

Path A primitives do **not** hunt for meaning or perform global interpretation. They
simply acknowledge that their structural operations inherently rely on semantic
assumptions, and they record those assumptions so downstream primitives do not need
to reconstruct them.

### Why Bounded Semantics Are Required
Meaning is subjective, probabilistic, and distributed. If meaning were restricted only
to “meaning primitives,” those primitives would become overloaded, forced to replicate
semantic work that upstream primitives already implicitly performed. Downstream
primitives often operate in different semantic domains (conceptual, unification,
extraction, stability), making reconstruction unreliable and domain‑inappropriate.

Bounded semantics distributes interpretation across the pipeline in a way that mirrors
natural cognition: surface → lexical → structural → routing → update → conceptual →
extraction → stability. Each primitive contributes only the meaning appropriate to its
role.

### Invariants for Bounded Semantics
All Path A primitives must satisfy:

1. **Domain‑Bound Semantics**  
   Semantic effects must remain strictly within the primitive’s defined domain.

2. **Explicit Recording**  
   All semantic assumptions required for the primitive’s job must be written into TP
   fields; no hidden semantics.

3. **Determinism & Replay Safety**  
   All semantic effects must be deterministic, auditable, and replay‑safe.

4. **No Unbounded or Inferential Semantics**  
   No primitive may perform global interpretation, inference, or meaning expansion
   beyond its domain.

5. **Downstream Compatibility**  
   Downstream primitives may rely on upstream recorded semantics and must not be
   forced to reconstruct meaning from scratch.

### Architectural Outcome
Path A is not “structure‑only.”  
Path A is **structure + bounded meaning**, producing a deterministic, domain‑layered,
replay‑safe TP ready for stability (COB/CST) and meaning‑layer progression.

---

# **1. Pipeline Summary Table (Ultra‑Compressed)**

| Primitive | Purpose | Inputs (read‑only unless noted) | Writes | Transfer Function (compressed) | Prohibitions |
|----------|---------|----------------------------------|--------|--------------------------------|--------------|
| **InB** | Create initial TP from raw user input | raw_user_text, metadata | messy_input_record, initial identity/context, provenance | Build TP; seed identity; placeholders; deterministic | No meaning, no normalization, no routing |
| **IIInB** | Inspect intake; propose repairs; detect anomalies | intake.surface, intake.tokens | repair_proposals, anomaly_flags, iiinb metadata | Deterministic token inspection; repair proposals; anomaly flags | No semantic inference; no intake mutation |
| **IE** | Construct committed intake | intake.surface/tokens, repair_proposals, anomaly_flags | normalized_text, ie_tokens, token_flags, structure, repair_annotations, replay metadata | Apply repairs; bounded semantic ops; build structure; classify tokens | No global semantic inference; no rewriting |
| **CE** | Build pre‑semantic context envelope | CEx output | context_metadata, ce_record, relevance/copy/reset flags | Canonical context object; identity‑layer continuity; ordering metrics; clarifying fields; next‑turn context | No semantic layers; no routing metadata; no ΔH% |
| **TPU** | Sole commit authority | tp_update_request{} | TP(N+1), tpu_audit_record, tpu_error | Validate authority; canonical ordering; atomic commit; safe boundaries; 1‑cycle lag | No meaning generation; no structural geometry changes |
| **SOB** | Structural segmentation + hint extraction | TP from TPU, CE/CEx structural metadata | structural_units, structural_metadata, residue_fragments, hint metadata | Segment structure; extract modality/operator/domain/tone/constraint hints; produce residue | No semantic interpretation; no text modification |
| **SROB** | Structural refinement | SOB output, CE/CEx cues | refined structural map/residue/metadata, sharpened hints | Normalize lists/tables; resolve ambiguity; sharpen hints; refine importance; discourse refinement | No semantic inference; no text modification |
| **CnOB** | Constraint extraction | SROB output, CE/CEx cues | constraint_families, missing/underspec/conflict signals, importance, residue_hash | Extract C1–C7; monotonic constraints; encode discourse constraints | No meaning resolution; no routing metadata |
| **SmOB** | Semantic‑adjacent cue extraction + residue compression | CnOB/SROB/SOB residue, CE/CEx cues, metadata | semantic_adjacent_cues, modality/affect/conflict cues, importance, residue_hash, TR‑input vector | Extract semantic‑adjacent cues; compress residue; normalize discourse cues | No semantic interpretation; no meaning generation |
| **WrdNm** | Numeric encoding | All upstream structured fields | wrdnm[] numeric vectors | Deterministic categorical/boolean/scalar/hash encoding | No semantic inference; no tokenization |
| **ISc** | Semantic scoring | candidate_set, FFTM features, WrdNm encodings, discourse cues, metadata, next‑turn context | isc_output, normalized distribution, entropy, ΔH%, confidence, rationale, COP proposals | Deterministic scoring; softmax; entropy; ΔH%; COP escalation | No meaning generation; no TP mutation |
| **SSG** | Structural signature generation | SmOB structural graph, metadata | ssg_signature, layer_bitmap, reason_code, status | Extract invariants; L2 normalize; bitmap; reason code | No semantic interpretation; no routing |
| **STPX** | Structured token & pattern extraction | structural geometry, SSG output, canonical tokens, metadata | stpx_cues, semantic_layer_provenance | Extract lexical/structural/constraint/repair cues; encode discourse cues | No semantic interpretation; no routing metadata |
| **DCB** | Execution‑flow geometry | previous geometric_state, primitive_id, cycle_id, timestamp | geometric_state, geometric_history, dcb_events | Compute position/direction/curvature/step_index/lane; cycle_start/delta events | No semantic/structural/identity/routing reads |
| **RB** | Deterministic routing + TR gating | input_fields, TR, tr_needs_update, ΔH, lineage, routing_metadata, IdOB view, structural metadata, STPX cues, continuity metadata | routing_filter, RB_out fields | TR gating; canonical routing filter; adjacency/displacement/regime; split/merge arbitration | No semantic interpretation; no TR mutation |
| **IdOB** | Identity‑layer update after RB; compute identity geometry/continuity/pressure/residuals/freeze/basin_surface; compute identity‑importance; produce meaning_delta_h + IdOB semantics | TP.identity.*, TP.semantic.*, identity_metadata, continuity_metadata, expressive/normalization/semantic_layer/residue/next_context metadata, RB view (ro), DCB geometric_state (ro), prior IdOB envelope (ro) | identity.geometry, identity.continuity, identity.pressure, identity.residuals.{magnitude,pattern}, identity.freeze.state, identity.basin_surface.region, idob_roles[], idob_candidates[], provenance, lineage_markers[], stability_marker, alignment_marker, regime_label, meaning_delta_h, idob_semantics[], meaning_semantics[], idob_complete, path_b_eligible, idob_next_ob_candidates[] | Deterministic operator‑I transition rules; regime‑conditioned inherit/reset; compute identity‑importance; compute meaning_delta_h; generate IdOB + meaning semantics; produce next‑OB candidates; mark idob_complete; expose identity envelope for MCB/RBU/DCB loop; replay‑safe; strict write‑boundary guard | No semantic interpretation beyond IdOB semantics; no routing; no structural geometry changes; no upstream TP mutation; no OB/IB/RB/TB/InB/OuB interaction; no placeholder promotion/compaction/redaction; no modification of semantic‑importance outside IdOB domain |

---

# **2. Compressed Sections (Full Detail, No Loss)**

Below are the compressed, clarified versions of each primitive.  
All normative requirements preserved.

---

## **InB — Input Block**
**Purpose:** Create initial TP from raw input; seed identity + context placeholders; record messy input.  
**Inputs:** raw_user_text, conversation metadata, system context, continuity markers.  
**Writes:** messy_input_record, initial identity geometry, initial context, provenance (routing_path=["inb"], lineage_log+=["inb"], tb_trace+=TB.inb_ingest).  
**Transfer Function:**  
- Build TP envelope; deterministic identity seeding; context placeholders.  
- Create continuity markers (no inference).  
- Deterministic replay; no randomness.  
**Prohibitions:** No meaning, no normalization, no routing, no semantic objects.

---

## **IIInB — Input Inference / Repair Basin**
**Purpose:** Deterministic intake inspection; propose repairs; detect anomalies; never apply repairs.  
**Inputs:** intake.surface, intake.tokens.  
**Writes:** repair_proposals, anomaly_flags, iiinb metadata.  
**Transfer Function:**  
- Deterministic token inspection; bounded meaning‑adjacent.  
- Repair proposals (rule_id, span, replacement params).  
- Anomaly flags (illegal_character, malformed_token, unicode_anomaly, punctuation_anomaly, repetition_pattern, no_entry).  
- Deterministic tokenization rules; preserve order.  
**Prohibitions:** No semantic inference; no intake mutation; no dictionary validation.

---

## **IE — Intake Envelope**
**Purpose:** Construct committed intake; integrate repairs; bounded semantic normalization; build structure.  
**Inputs:** intake.surface/tokens, repair_proposals, anomaly_flags, iiinb metadata.  
**Writes:** normalized_text, ie_tokens, token_flags, structure, repair_annotations, replay metadata, ruleset_id, error.  
**Transfer Function:**  
- Apply repairs exactly; preserve spans.  
- Bounded semantic ops (classification, consolidation, normalization only when proposed).  
- Build deterministic structure; classify tokens; resolve anomalies.  
- Construct normalized surface; encode replay metadata.  
**Prohibitions:** No global semantic inference; no rewriting beyond proposals.

---

## **CE — Context Envelope**
**Purpose:** Build deterministic pre‑semantic context object for ISc.  
**Inputs:** CEx output (context_fields, extraction_audit, identity‑layer metadata, ordering metrics, clarifying fields, next‑turn context).  
**Writes:** context_metadata, ce_record, relevance/copy/reset flags, context_fields, context_provenance.  
**Transfer Function:**  
- Canonical construction; identity‑layer continuity; ordering metrics; clarifying fields; next‑turn context.  
- Deterministic replay; audit drops/truncations.  
**Prohibitions:** No semantic layers; no routing metadata; no ΔH%.

---

## **TPU — Thought Packet Update Subsystem**
**Purpose:** Sole commit authority; atomic updates; canonical ordering; safe boundaries; replay equivalence.  
**Inputs:** tp_update_request{} (isc, cil, cob, cop, idob_update, mcb_update, rbu_update, metadata).  
**Writes:** TP(N+1), tpu_audit_record, tpu_error.  
**Transfer Function:**  
- Validate writer authority; canonical ordering; safe‑boundary commit; 1‑cycle lag.  
- Commit semantic/process/metadata/clarifying/next‑context fields.  
**Prohibitions:** No meaning generation; no structural geometry changes; no intake/context modification.

---

## **SOB — Structural Object Build**
**Purpose:** Structural segmentation + bounded semantic‑adjacent hint extraction.  
**Inputs:** TP from TPU, CE/CEx structural metadata.  
**Writes:** structural_units, structural_metadata, residue_fragments, operator/domain/tone/constraint hints.  
**Transfer Function:**  
- Segment sentences/clauses/lists/tables/code/math.  
- Extract modality/operator/domain/tone/constraint hints.  
- Produce residue; preserve ordering; reduce entropy.  
**Prohibitions:** No semantic interpretation; no text modification.

---

## **SROB — Structural Refinement OB**
**Purpose:** Normalize + refine SOB output; sharpen hints; refine importance; discourse refinement.  
**Inputs:** SOB output, CE/CEx cues, structural metadata.  
**Writes:** refined structural map/residue/metadata, sharpened hints, refined importance, audit.  
**Transfer Function:**  
- Normalize lists/tables/code/math; resolve boundaries; sharpen hints; refine importance; discourse normalization.  
- Produce refined residue; deterministic.  
**Prohibitions:** No semantic inference; no text modification; no new hint types.

---

## **CnOB — Constraint Object Base**
**Purpose:** Extract constraint families C1–C7; missing/underspec/conflict signals; importance; constraint residue.  
**Inputs:** SROB output, CE/CEx cues.  
**Writes:** constraint_families, missing_slot, underspec, conflict, importance, residue_hash, routing‑eligibility.  
**Transfer Function:**  
- Extract C1–C7; monotonic constraints; encode discourse constraints; refine importance.  
- Hash residue; deterministic.  
**Prohibitions:** No meaning resolution; no routing metadata.

---

## **SmOB — Semantic‑Adjacent Object Base**
**Purpose:** Extract semantic‑adjacent cues; compress residue; produce TR‑input vector.  
**Inputs:** CnOB/SROB/SOB residue, CE/CEx cues, metadata.  
**Writes:** semantic_adjacent_cues, modality/affect/conflict cues, importance, residue_hash, TR‑input vector.  
**Transfer Function:**  
- Extract semantic‑adjacent cues; compress residue; normalize discourse cues; canonical ordering.  
**Prohibitions:** No semantic interpretation; no meaning generation.

---

## **WrdNm — Word‑to‑Numeric Encoder**
**Purpose:** Deterministic numeric encoding of structured fields.  
**Inputs:** All upstream structured fields.  
**Writes:** wrdnm[] numeric vectors.  
**Transfer Function:**  
- Deterministic categorical/boolean/scalar/hash mapping; schema‑driven; replay‑safe.  
**Prohibitions:** No semantic inference; no tokenization.

---

## **ISc — Inference Scorer**
**Purpose:** Deterministic scoring of candidate_set; softmax; entropy; ΔH%; COP escalation.  
**Inputs:** candidate_set, FFTM features, WrdNm encodings, discourse cues, metadata, next‑turn context.  
**Writes:** isc_output, normalized distribution, entropy, ΔH%, confidence, rationale, COP proposals.  
**Transfer Function:**  
- Weighted scoring; softmax; entropy; ΔH%; deterministic replay.  
**Prohibitions:** No meaning generation; no TP mutation.

---

## **SSG — Structural Signature Generator**
**Purpose:** Generate structural invariant vector; bitmap; reason code; status.  
**Inputs:** SmOB structural graph, metadata.  
**Writes:** ssg_signature, layer_bitmap, reason_code, status.  
**Transfer Function:**  
- Extract invariants; L2 normalize; bitmap; reason code; deterministic replay.  
**Prohibitions:** No semantic interpretation; no routing.

---

## **STPX — Structured Token & Pattern Extractor**
**Purpose:** Extract lexical/structural/constraint/repair cues; encode discourse cues.  
**Inputs:** structural geometry, SSG output, canonical tokens, metadata.  
**Writes:** stpx_cues, semantic_layer_provenance.  
**Transfer Function:**  
- Extract L/S/C/R cues; normalize discourse cues; deterministic replay.  
**Prohibitions:** No semantic interpretation; no routing metadata.

---

## **DCB — Directional Conversation Basin**
**Purpose:** Execution‑flow geometry; cycle_start/delta events; geometric history.  
**Inputs:** previous geometric_state, primitive_id, cycle_id, timestamp.  
**Writes:** geometric_state, geometric_history, dcb_events.  
**Transfer Function:**  
- Compute position/direction/curvature/step_index/lane; append history; emit events.  
**Prohibitions:** No semantic/structural/identity/routing reads.

---

## **RB — Relational Basin**
**Purpose:** Deterministic routing; TR gating; adjacency/displacement/regime; split/merge arbitration.  
**Inputs:** input_fields, TR, tr_needs_update, ΔH, lineage, routing_metadata, IdOB view, structural metadata, STPX cues, continuity metadata.  
**Writes:** routing_filter, RB_out fields.  
**Transfer Function:**  
- TR gating; canonical routing filter; adjacency/displacement/regime; deterministic arbitration.  
**Prohibitions:** No semantic interpretation; no TR mutation; no cross‑core merges.

---

## **IdOB — Identity‑Layer Object Builder (post‑RB identity operator)**

**Purpose:**  
Update identity envelope after RB; compute identity geometry/continuity/pressure/residuals/freeze/basin_surface; compute identity‑importance; produce meaning_delta_h + IdOB semantics for downstream MCB/RBU/DCB loop.

**Inputs (read‑only unless noted):**  
Current TP.identity.* (from prior IdOB or initial identity),  
TP.semantic.* (from RB/WrdNm/ISc/RTU/TR/CTP/RB loop),  
TP.metadata.identity_metadata,  
TP.metadata.continuity_metadata,  
TP.metadata.expressive_metadata,  
TP.metadata.normalization_metadata,  
TP.metadata.semantic_layer_metadata,  
TP.metadata.residue_metadata,  
TP.metadata.next_context_metadata,  
RB view (read‑only),  
DCB geometric_state (read‑only),  
prior IdOB envelope (read‑only).

**Writes:**  
identity.geometry, identity.continuity, identity.pressure,  
identity.residuals.{magnitude, pattern},  
identity.freeze.state, identity.basin_surface.region,  
idob_roles[], idob_candidates[], provenance updates, lineage_markers[],  
stability_marker, alignment_marker, regime_label,  
TP.semantic.meaning_delta_h,  
TP.semantic.idob_semantics[],  
TP.semantic.meaning_semantics[],  
idob_complete, path_b_eligible, idob_next_ob_candidates[].

**Transfer Function (compressed):**  
Apply deterministic operator‑I transition rules to identity geometry/continuity/pressure/residuals/freeze/basin_surface using RB/semantic context.  
Apply regime‑conditioned inherit/reset for roles, candidates, provenance, lineage markers, residuals, freeze tendency.  
Compute identity‑importance (monotonic, deterministic).  
Compute meaning_delta_h; generate IdOB semantics + meaning semantics.  
Produce next‑OB candidates; mark idob_complete; expose updated identity envelope for MCB/RBU/DCB loop.  
Replay‑safe; no randomness; strict write‑boundary guard.

**Prohibitions:**  
No semantic interpretation beyond IdOB semantics tagging;  
no routing or structural geometry changes;  
no modification of upstream TP fields;  
no interaction with OB/IB/RB/TB/InB/OuB domains;  
no placeholder promotion, compaction, or redaction;  
no modification of semantic‑importance scores or roles outside IdOB domain.

---

# ✅ **Document Complete — Compressed, Clear, No Loss**  

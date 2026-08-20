## InB — Input Block
**Spec:** 20.100_inb_requirements.md  
**Pipeline Position:** Pipeline entry point (first primitive)  
**Purpose:** Convert raw user input into the initial TP envelope and establish the foundational identity, context, and semantic scaffolding required for all downstream primitives. 

---

### Input Contract
InB consumes:
- raw_user_text (verbatim user input) 
- conversation metadata (turn index, speaker role)  
- system context (global settings, conversation mode)  
- any upstream continuity markers (if present)

All inputs are treated as **opaque raw material**; InB performs no semantic interpretation. 

---

### Output Contract (InB TP)
InB produces the first TP of the pipeline with:

- **semantic_envelope.messy_input_record** — raw, unparsed input preserved exactly as received  
- **identity_envelope.initial_geometry** — initial basin, anchors, and identity surface seeded deterministically  
- **context_envelope.initial_context** — topic guess, stance placeholder, intent placeholder  
- **provenance_envelope.routing_path = ["inb"]**  
- **provenance_envelope.lineage_log += ["inb"]**  
- **trace_envelope.tb_trace += TB.inb_ingest**  

InB does **not**:
- generate meaning  
- create semantic objects  
- perform normalization  
- modify identity geometry after initial seeding  
- apply any routing logic  

All behavior is deterministic and replay‑safe. 

---

### Transfer Function (InB)
InB applies the following transformations:

1. **TP Construction**
   - Create a new TP envelope from raw input  
   - Initialize all envelope fields to their pipeline‑entry defaults  
   - Seed identity geometry deterministically (basin, anchors, lineage)  
   - Establish initial context placeholders  
   - Record messy_input_record exactly as received  
   

2. **Continuity Initialization**
   - Create continuity markers for turn‑0  
   - No continuity inference is performed  
   - No semantic continuity is assumed  
   

3. **Provenance Initialization**
   - routing_path = ["inb"]  
   - lineage_log += ["inb"]  
   - tb_trace += TB.inb_ingest  
   

4. **Determinism**
   - Identical raw input → identical TP  
   - No randomness, no external state, no wall‑clock time  
   - Fully replay‑safe  
   

---

### Notes
- InB is the **pipeline’s root primitive**.  
- All downstream primitives (IIInB → IE → CE → TPU → … → RB) depend on the TP structure created here.  
- InB is intentionally minimal: it ingests, seeds, and records — nothing more.  

## IIInB — Input Inference / Repair Basin
**Spec:** 20.101_iiinb_prim.md  
**Pipeline Position:** After InB, before IE  
**Purpose:** Perform deterministic, bounded meaning‑adjacent inspection of intake surface and tokens; propose repairs; detect anomalies; never apply repairs; never mutate intake; never construct semantic content.

---

### Input Contract
IIInB SHALL read only:
- TP.intake.surface 
- TP.intake.tokens 

IIInB SHALL NOT read:
- TP.semantic  
- TP.structure  
- TP.process  


---

### Output Contract
IIInB SHALL write only:
- TP.repair_proposals 
- TP.anomaly_flags 
- TP.intake.metadata.iiinb 

IIInB SHALL NOT modify:
- TP.intake.normalized_text  
- TP.intake.tokens  
- TP.structure  
- TP.semantic  


---

### Transfer Function (IIInB)

1. **Deterministic Intake Inspection**  
   - Analyze canonicalized surface form from InB   
   - Inspect tokens without mutating them   
   - Operate only in bounded meaning‑adjacent domain (repair + anomaly detection)  
     

2. **Repair Proposal Generation**  
   Each repair proposal SHALL include:  
   - deterministic rule identifier  
   - deterministic token span  
   - deterministic replacement parameters  
   

   IIInB SHALL NOT apply repairs (proposal‑only)  
   

3. **Anomaly Detection**  
   Emit anomaly flags for:  
   - illegal_character.*  
   - malformed_token  
   - unicode_anomaly  
   - punctuation_anomaly  
   - repetition_pattern  
   - no_entry  
   

   Each anomaly flag SHALL include:  
   - deterministic token span  
   - anomaly type  
   - anomaly location  
   

4. **Deterministic Tokenization Rules**  
   IIInB SHALL:  
   - skip whitespace (no whitespace tokens)   
   - recognize `<broken>` as a single token   
   - emit ≥3‑letter runs as standalone tokens   
   - emit contiguous alphanumerics as word tokens   
   - emit illegal characters as standalone tokens   
   - attach trailing commas to word tokens   
   - group punctuation runs   
   - emit all other characters as standalone tokens   
   - preserve exact token order   
   - never merge/split beyond defined rules   
   - ensure full determinism (same surface → same tokens) 

5. **Semantic Isolation**  
   IIInB SHALL NOT:  
   - construct TP.semantic   
   - infer composite meaning (e.g., “Th” + “e” → “The”)   
   - expand shorthand using history or context   
   - perform dictionary validation (IE does this) 

6. **Metadata Emission**  
   IIInB SHALL emit metadata sufficient for deterministic replay:  
   - ruleset_id  
   - timestamp  
   - input_hash  
   - repair_operations  
   

7. **Deterministic Failure Behavior**  
   - fail fast on invalid intake   
   - failure behavior SHALL be deterministic 

---

### Notes
- IIInB is the **last primitive that sees raw intake** before IE constructs committed intake.   
- IIInB is **proposal‑only**: all committed normalization is performed by IE.   
- IIInB ensures deterministic, stable intake for IE → CE → TPU → ISc → SSG → STPX → DCB → RB. 

## IE — Intake Envelope (Committed Intake Constructor)
**Spec:** 20.109_ie_prim.md  
**Pipeline Position:** After IIInB, before CE  
**Purpose:** Convert IIInB’s intake surface + tokens + repair proposals into the first *committed*, machine‑efficient intake substrate of Path‑A. IE integrates repairs, performs bounded semantic normalization, classifies tokens, constructs structural tags, and emits deterministic replay metadata. IE does not perform global semantic inference.  


---

### Input Contract
IE SHALL read only:  
- TP.intake.surface  
- TP.intake.tokens  
- TP.repair_proposals  
- TP.anomaly_flags  
- TP.intake.metadata.iiinb  


IE SHALL NOT read or modify any upstream fields.  


---

### Output Contract
IE SHALL write only:  
- TP.intake.normalized_text  
- TP.intake.ie_tokens  
- TP.intake.token_flags  
- TP.structure (tags, spans, markup)  
- TP.metadata.repair_annotations  
- TP.metadata.replay  
- TP.metadata.ruleset_id  
- TP.error  


Downstream primitives treat **ie_tokens** + **token_flags** as the primary machine substrate.  


---

### Transfer Function (IE)

### 1. Deterministic Repair Integration  
IE SHALL incorporate all IIInB repair proposals **without semantic modification**.  
  
- Apply each repair proposal exactly to its span  
- Preserve rule identifiers and spans  
  
- Surface anomaly_flags as anomaly‑provenance entries  


### 2. Bounded Semantic Operations  
IE MAY perform only bounded semantic operations:  
- semantic classification  
- semantic consolidation when IIInB proposes merges  
- semantic normalization only when IIInB proposes repairs  
- dictionary validation  


IE SHALL NOT perform:  
- semantic inference  
- semantic rewriting  
- semantic expansion not proposed by IIInB  


### 3. Token Normalization  
IE SHALL produce a normalized token sequence including repair integration.  
  
- Preserve token boundaries unless repairs modify them  
  
- Emit tokens suitable for deterministic replay  


### 4. Structural Construction  
IE SHALL construct TP.structure deterministically.  
  
- Validate TP against schema  
  
- Reject malformed structures and emit TP.error  
  
- Record structural provenance  


### 5. Token‑Level Semantic Classification  
IE SHALL classify each token using bounded semantic rules.  
  
IE SHALL emit one token_flag per token.  
  
IE SHALL NOT drop or replace tokens unless explicitly directed by rule.  


### 6. Rule‑Driven Anomaly Handling  
IE SHALL resolve anomaly_flags using bounded semantic rules.  
  
IE SHALL NOT normalize unless IIInB proposes it.  
  
IE SHALL record anomaly resolutions in repair_annotations.  


### 7. Normalized Surface Construction  
IE SHALL construct normalized_text using rule‑driven whitespace behavior.  
  
IE SHALL insert/omit spaces according to rule‑driven behavior.  


### 8. Replay Metadata  
IE SHALL encode all provenance required for deterministic replay.  
  
IE SHALL preserve ordering of tokens, structures, metadata.  


### 9. Determinism & Boundedness  
IE SHALL be deterministically reproducible from identical IIInB output.  
  
IE SHALL NOT include nondeterministic fields.  
  
IE SHALL enforce bounded size limits and record deterministic truncation.  


---

### Notes
- IE is the **semantic compressor** of Path‑A.  
  
- IE is the boundary between IIInB and all downstream primitives.  
  
- IE produces the committed TP intake: `{ intake, structure, metadata, error }`.  
  
## CE — Context Envelope
**Spec:** 20.108_ce_envelope.md  
**Pipeline Position:** After IE, before ISc  
**Purpose:** Produce the deterministic, bounded, pre‑semantic context object that CEx hands off to the first semantic module (ISc). CE contains only explicit, normalized fields extracted by CEx and is the *sole* context object ISc may read.  
CE is canonical, versioned, deterministic, and strictly pre‑semantic.  


---

### Input Contract
CE SHALL consume only CEx output:
- context_fields{} (explicit, normalized, bounded)   
- extraction_audit[] (deterministic audit entries)  
- identity‑layer selection metadata   
- ordering metrics   
- clarifying fields + topology + importance scores   
- next‑turn context fields (topic, stance, intent, etc.)   

CE SHALL NOT read:
- semantic layers  
- routing metadata  
- ΔH%  
- TB/IB fields  
- semantic_core  


---

### Output Contract
CE SHALL write into:
- **TP.metadata.context_metadata** (canonical placement)  
  

CE SHALL produce:
- **ce_record**  
  - context_fields{}  
  - extraction_audit[]  
  - ce_version_tag  
  

CE SHALL update:
- TP.metadata.context.relevance_flags  
- TP.metadata.context.copy_forward_flags  
- TP.metadata.context.reset_flags  
- TP.metadata.context.context_fields  
- TP.metadata.context.context_provenance  


CE SHALL be preserved across freeze/thaw cycles.  


---

### Transfer Function (CE)

#### 1. Canonical Construction
CE SHALL construct a bounded, normalized, deterministic context object:  
- canonical field names  
- canonical ordering  
- canonical encoding  


#### 2. Identity‑Layer Continuity Encoding
CE SHALL encode the identity‑layer chosen by CEx and continuity_status ∈ {continuous, switched, fallback, undetermined}.  
  


Continuity rules:  
- continuous → preserved previous layer   
- switched → override continuity due to high certainty, low ambiguity   
- fallback → collapse_risk threshold exceeded   
- undetermined → ambiguity or indeterminate selection 

#### 3. Ordering‑Metric Integration
CE SHALL include ordering_metrics exactly as provided by CEx:  
- last_referred  
- total_referrals  
- recent_referrals  
- ordering_score  


CE SHALL NOT compute ordering metrics.  


#### 4. Clarifying‑Field Integration
CE SHALL include:  
- clarifying fields  
- subfields  
- hierarchical topology (depth ≤ 4)  
- importance scores  


CE SHALL enforce bounded limits:  
- fields ≤ 10  
- subfields ≤ 100  
- depth ≤ 4  


CE SHALL NOT modify clarifying fields or importance scores.  


#### 5. Next‑Turn Context Integration
CE SHALL include next‑turn context fields exactly as provided by CEx:  
topic, stance, intent, register, politeness, epistemic_shading, continuity, direction, coherence, shift_required, importance  


CE SHALL NOT derive next‑turn context fields.  


#### 6. Extraction Audit
CE SHALL include extraction_audit entries for all:  
- drops  
- truncations  
- normalizations  


#### 7. Determinism & Replay
CE SHALL be fully deterministic:  
- identical CIL + identical policy_signature → identical CE  


Replay must yield byte‑identical CE.  


#### 8. Error Behavior
If CIL is malformed:  
- CE emits only valid extracted fields  
- invalid fields dropped  
- audit records all drops  
- CE never halts pipeline  


---

### Notes
- CE is the **handoff boundary** between extraction (CEx) and semantics (ISc).  
  
- CE is strictly pre‑semantic and contains no inferred meaning.  
  
- CE is a TP‑stream envelope committed by TPU.  
  
## TPU — Thought Packet Update Subsystem
**Spec:** 20.46_tpu_req.md  
**Pipeline Position:** After CE, before SOB  
**Purpose:** TPU is the *sole commit authority* for all TP mutations. Every semantic, process, metadata, clarifying‑field, next‑context, lineage, and meaning‑side update MUST pass through TPU. TPU validates writer authority, enforces safe boundaries, applies canonical ordering, commits atomically, and guarantees replay equivalence.  


---

### Input Contract
TPU receives a single immutable `tp_update_request{}` containing:  
- isc{}  
- cil{}  
- cob{}  
- cop{}  
- idob_update{}  
- mcb_update{}  
- rbu_update{}  
- metadata{ merge_version, canonical_ordering_hash, safe_boundary_marker?, seed }  


TPU SHALL NOT read or modify:  
- TP.intake.*  
- TP.context.current_turn  
- structural geometry (OB‑family)  


---

### Output Contract
TPU produces:  
- **TP(N+1)** — updated Thought Packet  
- **tpu_audit_record{}** — append‑only audit entry  
- **tpu_error{}** — deterministic fallback object  


TPU writes only to:  
- TP.semantic.*  
- TP.process.*  
- TP.metadata.*  
- TP.clarifying_fields.*  
- TP.next_context.*  


---

### Transfer Function (TPU)

### 1. Core Commit Authority  
TPU is the **sole structural‑commit authority** for TP updates.  
It validates update requests, enforces writer‑authority boundaries, applies canonical ordering, commits atomically, and produces audit records.  


### 2. Deterministic Commit  
Identical TP(N) + identical update request → identical TP(N+1).  
Replay equivalence MUST be preserved.  


### 3. Writer Authority Enforcement  
TPU validates writer authority at the block level:  
- each block must appear only in its authorized namespace  
- each block must contain only permitted fields  
- structural/metadata updates originate only from TPU  
- meaning‑layer blocks must not contain structural geometry  
Violations → reject entire request + audit.  


### 4. Canonical Ordering  
TPU SHALL enforce canonical ordering for:  
- arrays  
- maps  
- clarifying‑fields  
- next‑context fields  
- lineage markers  
- ΔH% histories  
- metadata blocks  


### 5. Safe‑Boundary Commit  
TPU commits only at deterministic safe boundaries.  
TPU SHALL NOT commit during:  
- OB execution  
- RB routing  
- TR update  
- IdOB refinement  
- MCB context generation  
- RBU commit  
- OuBA commit window  


### 6. 1‑Primitive‑Cycle Lag  
All updates follow:  
`tp_update_request(N) → TP(N+1)`  
No subsystem may observe updates in the same cycle they were proposed.  


### 7. No Meaning Generation  
TPU SHALL NOT generate meaning or interpret semantics.  
It only commits fields provided by IdOB, MCB, or RBU.  


### 8. Intake/Context Integrity  
TPU SHALL NOT modify:  
- TP.intake.*  
- TP.context.current_turn.*  
- TP.semantic_core  
- structural geometry fields  
TPU commits only next‑turn context fields from MCB.  


---

### Clarifying‑Field Commit Requirements

- Validate field identity, hierarchical level, importance, provenance, topology, boundedness  
    
- Enforce writer authority  
- Commit atomically  
    
- Preserve provenance  
- Apply canonical ordering  
- Maintain continuity  
    
- Audit all updates  
    
- Enforce bounded limits:  
  - ≤10 fields  
  - ≤100 subfields  
  - ≤4 hierarchical levels  
  Violations → deterministic fallback + audit  
  

---

### Next‑Context Commit Requirements (MCB Output)

TPU SHALL validate next‑context fields:  
topic, stance, intent, register, politeness, epistemic_shading, continuity, direction, coherence, shift_required, importance  


TPU SHALL commit next‑context fields into `TP.next_context{}` and SHALL NOT modify current‑turn context.  


Canonical ordering + replay equivalence required.  


---

### Atomicity & Audit

- Atomic commits only  
    
- Append‑only audit logging  
    
- Immutable update request  
    
- Deterministic fallback on validation failure  
    
- Enforce TCU budgets + GB caps  
    

---

### Forbidden Actions
TPU does NOT:  
- generate meaning  
- interpret semantics  
- modify structural geometry  
- bypass writer authority  
- bypass safe boundaries  
- reorder candidate sets  
- call coprocessors  
- introduce nondeterminism  
- create/delete TP fields  
- perform partial commits  


---

### Error Handling
On failure, TPU emits:  
`tpu_error{ code, rationale, fallback_behavior, audit_record }`  


---

### Audit Logging
Audit records include:  
- request hash  
- TP(N) hash  
- TP(N+1) hash  
- writer‑authority validation  
- safe‑boundary evidence  
- TCU usage  
- timestamp  


---

### Verification Focus
Verification ensures:  
- writer authority enforcement  
- 1‑cycle lag  
- replay equivalence  
- safe‑boundary compliance  
- canonical ordering  
- atomicity  
- deterministic fallback  
- bounded clarifying‑fields  
- correct next‑context commits  

## SOB — Structural Object Build
**Spec:** 20.40.010_sob_prim.md  
**Pipeline Position:** After TPU, before SROB  
**Purpose:** Perform deterministic structural segmentation and bounded semantic‑adjacent classification. SOB extracts structural units, modality, operator‑hints, domain‑hints, tone‑hints, constraint‑hints, and structural residue. SOB does not perform deep semantic interpretation.  


---

### Input Contract
SOB SHALL consume:
- TP from TPU (committed intake + structure + metadata)  
- CE/CEx structural metadata (read‑only)  


SOB SHALL NOT consume:
- semantic_core  
- meaning‑layer fields  
- routing_metadata  
- ΔH%  


---

### Output Contract
SOB SHALL produce:
- structural_units  
- structural_metadata  
- residue_fragments  
- operator_hint_metadata  
- domain_hint_metadata  
- tone_hint_metadata  
- constraint_hint_metadata  


SOB SHALL guarantee:
- output is valid input for SROB  


---

### Transfer Function (SOB)

### 1. Structural Segmentation
SOB SHALL segment TP into structural units:  
- sentences  
- clauses  
- lists (ordered, unordered, nested)  
- tables  
- code blocks  
- math blocks  


Ordering MUST be preserved exactly.  


Lists MUST be explicitly represented.  


---

### 2. Modality Extraction
SOB SHALL classify each structural unit by modality:  
- declarative  
- interrogative  
- imperative  
- conditional  
- hypothetical  


Modality MUST be encoded without altering text.  


---

### 3. Operator‑Hint Extraction
SOB SHALL extract operator hints:  
- summarize  
- compare  
- classify  
- derive  
- plan  
- explain  
- rewrite  
- transform  


Operator hints MUST be encoded as residue fragments.  


---

### 4. Domain‑Hint Extraction
SOB SHALL extract domain hints:  
- math‑like  
- code‑like  
- narrative‑like  
- legal‑like  
- technical‑like  
- conversational‑like  


Domain hints MUST be encoded as residue fragments.  


SOB SHALL NOT perform deep semantic interpretation.  


All domain‑hint extraction MUST be bounded and deterministic.  


---

### 5. Tone‑Hint Extraction
SOB SHALL extract tone hints:  
- formal  
- casual  
- technical  
- supportive  
- urgent  
- neutral  


Tone hints MUST be encoded as residue fragments.  


---

### 6. Constraint‑Hint Extraction
SOB SHALL extract constraint hints:  
- precision  
- conciseness  
- politeness  
- safety  
- formatting  


Constraint hints MUST be encoded as residue fragments.  


---

### 7. Structural Integrity
SOB SHALL ensure:
- no structural unit is lost  
- no incorrect merges  
- no reordering  


All metadata MUST be deterministic and reproducible.  


---

### 8. Residue Formation
SOB SHALL produce residue fragments representing:  
- unresolved structure  
- operator hints  
- domain hints  
- tone hints  
- constraint hints  


Residue MUST be addressable by RB.  


Residue entropy MUST be strictly reduced.  


---

### 9. Routing Requirements
SOB SHALL route residue into SROB.  


SOB SHALL NOT route directly into semantic OBs.  


---

### 10. Prohibited Behavior
SOB SHALL NOT:  
- perform deep semantic interpretation  
  
- infer intent  
  
- apply constraints  
  
- modify TP text  
  

---

### 11. Discourse‑Context Propagation (Structural Only)
SOB MAY consume CE/CEx discourse‑context metadata (read‑only).  


SOB SHALL encode discourse‑context only as structural flags.  


SOB SHALL NOT perform semantic interpretation when processing discourse‑context.  


Flags MUST be deterministic and reproducible.  


SOB SHALL NOT modify TP text or semantic_core.  


Flags MUST be representable as addressable residue.  


---

### 12. Metadata Consumption Rules
SOB SHALL consume TP‑stream metadata only when relevant.  


SOB SHALL NOT consume routing_metadata, ΔH%, lineage fields, Pipeline‑B envelopes.  


All metadata interpretation MUST remain structural or semantic‑adjacent.  


---

### 13. Mathematical Requirements
Residue fragments MUST be hashable:  
hᵢ = hash(rᵢ)  


Routing address MUST satisfy:  
q = h₁ ⊕ h₂ ⊕ … ⊕ hₙ  


Residue MUST satisfy monotonicity, smoothness, curvature‑invariance.  


---

### Notes
- SOB is the **first OB layer** and the structural foundation for SROB → CnOB → SmOB.  
- SOB reduces entropy and prepares residue for RB.  
- SOB is deterministic, bounded, and strictly pre‑semantic.  

## SROB — Structural Refinement OB
**Spec:** 20.40.020_srob_prim.md  
**Pipeline Position:** After SOB, before CnOB  
**Purpose:** Normalize, refine, disambiguate, and sharpen SOB structural units, hints, and residue into rigid, canonical structural fields consumable by CnOB, SmOB, RB, and downstream meaning stages. SROB is strictly structural and bounded‑semantic‑adjacent.  


---

### Input Contract
SROB SHALL consume (read‑only):
- SOB structural map, residue, structural metadata, structural‑importance metadata  
  
- CE/CEx context fields (thread summary, entities, temporal/causal markers) as structural cues only  
  
- TP‑stream metadata applicable to structural normalization  
  

SROB SHALL NOT consume:
- routing_metadata, ΔH%, truth/done fields, lineage fields, Pipeline‑B envelopes  
  

---

### Output Contract
SROB SHALL output (SROB‑owned fields only):
- refined structural map  
- refined residue set  
- refined structural metadata  
- sharpened operator/domain/tone/constraint hints (within SOB type space)  
- refined structural‑importance metadata  
- SROB audit record + optional diagnostic metadata  
  

SROB SHALL guarantee output is valid input for CnOB.  


SROB SHALL NOT overwrite SOB‑owned fields or meaning‑layer fields.  


---

### Transfer Function (SROB)

### 1. Structural Normalization
SROB SHALL normalize:
- list structures (depth, numbering, indentation)  
  
- table structures (headers, rows, cell boundaries)  
  
- code/math blocks  
  

SROB SHALL NOT alter original text.  


---

### 2. Ambiguity Resolution
SROB SHALL resolve ambiguous boundaries:
- sentence segmentation  
- nested lists  
- structural similarity consistency  
  

All resolution MUST be deterministic.  


---

### 3. Hint Sharpening (Operator / Domain / Tone / Constraint)
SROB SHALL sharpen SOB hints into more precise categories **within the same type space**:  
  
  
  


SROB SHALL NOT introduce new hint types.  


Sharpening MAY use bounded, deterministic semantic‑adjacent rules.  


Sharpening SHALL NOT perform deep meaning resolution or intent inference.  


---

### 4. Structural‑Importance Refinement
SROB SHALL refine structural‑importance residues into canonical positional/structural cues:  
- subject‑like  
- object‑like  
- header‑like  
- anchor‑like  


These cues SHALL NOT be semantic roles.  


Residues MUST remain addressable by RB and consumable by CnOB/SmOB.  


---

### 5. Discourse‑Context Refinement
SROB SHALL normalize discourse‑context flags (recent‑entity continuity, temporal shifts, causal markers, contrastive markers) into canonical structural metadata.  


SROB SHALL refine discourse‑context residue into deterministic, addressable structural fragments.  


All discourse metadata consumption MUST remain bounded and structural‑adjacent.  


---

### 6. Residue Formation
SROB SHALL produce refined residue fragments representing:
- normalized structure  
- sharpened hints  
- refined structural‑importance cues  


Residue MUST be addressable by RB.  


---

### 7. Mathematical Requirements
Each refined residue fragment rᵢ′ MUST be hashable:  
hᵢ′ = hash(rᵢ′)  


Combined query address MUST satisfy:  
q′ = h₁′ ⊕ h₂′ ⊕ … ⊕ hₙ′  


Residue MUST preserve geometric invariants (smoothness, monotonicity, curvature‑invariance).  


---

### 8. Bounded Behavior & Prohibitions
SROB SHALL NOT:
- perform deep semantic interpretation  
  
- infer intent, task goals, referent identity, entity meaning  
  
- apply or enforce constraint logic  
  
- modify TP text  
  
- overwrite non‑SROB fields  
  

SROB MAY write diagnostic‑only metadata (developer playback only).  


---

### 9. Routing Requirements
SROB SHALL route output to CnOB (next OB layer).  


SROB SHALL NOT route directly into semantic OBs.  


---

### Notes
- SROB is the second OB layer, refining SOB output into rigid structural fields.  
- SROB is deterministic, bounded, and strictly structural/semantic‑adjacent.  
- SROB prepares structure for CnOB → SmOB → WrdNm → ISc → SSG → STPX → DCB → RB.  

## CnOB — Constraint Object Base
**Spec:** 20.40.030_cnob_prim.md  
**Pipeline Position:** After SROB, before SmOB  
**Purpose:** Extract constraint‑level residue from refined structure and tags produced by SROB, forming rigid constraint families (C1–C7), missing‑slot signals, underspecification markers, conflict indicators, constraint‑importance residues, and routing‑eligible constraint metadata. CnOB is strictly bounded‑semantic‑adjacent and never performs deep meaning resolution.  


---

### Input Contract
CnOB SHALL accept:
- refined structural map, refined residue, refined structural metadata, refined structural‑importance metadata from SROB  
  

CnOB MAY read (read‑only):
- CE/CEx context fields as structural or semantic‑adjacent cues  
  

CnOB SHALL normalize discourse‑context structural flags from SROB into canonical constraint metadata  
  

CnOB SHALL encode discourse‑context metadata strictly as constraint‑level residue  
  

CnOB SHALL NOT:
- perform deep meaning resolution, intent inference, referent identity resolution  
  
- consume routing_metadata, truth/done fields, lineage fields, Pipeline‑B envelopes, or ΔH% routing envelopes  
  

---

### Output Contract
CnOB SHALL output (CnOB‑owned fields only):
- constraint_families (C1–C7)  
- missing_slot_signals  
- underspecification_markers  
- conflict_indicators  
- constraint_importance residues  
- constraint_residue_hash  
- lineage‑derived constraints  
- structural‑change‑aligned constraints (C6)  
- routing‑eligibility constraints  
- policy‑derived constraints (when applicable)  
  

CnOB output MUST be valid input for SmOB  
  

CnOB SHALL write only CnOB‑owned fields  
  

---

### Transfer Function (CnOB)

### 1. Deterministic Constraint Extraction
CnOB SHALL extract monotonic constraint families C1–C7 under deterministic rules.  
  

Constraint families:
- **C1** structural existence  
- **C2** structural adjacency  
- **C3** structural ordering  
- **C4** structural boundaries  
- **C5** structural lineage  
- **C6** structural change (ΔH%-aligned from allowed structural cues only)  
  
- **C7** routing‑eligibility  
  

Constraints MUST be monotonic (added, never removed).  
  

### 2. Missing‑Slot, Underspecification, Conflict Indicators
CnOB SHALL extract:
- missing‑slot signals  
- underspecification markers  
- conflict indicators  
  

These are constraint residue, **not** meaning reconstruction.  
  

### 3. Constraint‑Importance Refinement
CnOB SHALL refine structural‑importance residues into constraint‑importance residues.  
  

CnOB SHALL compute constraint‑importance using deterministic structural/semantic‑adjacent cues only.  
  

CnOB SHALL NOT perform semantic‑role assignment or referent resolution.  
  

Constraint‑importance MUST remain addressable by RB and consumable by SmOB/STPX.  
  

### 4. Discourse‑Constraint Encoding
CnOB SHALL normalize and encode discourse‑context structural flags (continuity, temporal shifts, causal markers, contrastive markers) into constraint‑level metadata.  
  

Encoding MUST be deterministic, bounded, monotonic, and reproducible.  
  

### 5. Metadata Consumption (Bounded)
CnOB MAY consume deterministic TP‑stream metadata when applicable to constraint extraction.  
  

CnOB SHALL treat all consumed metadata as structural or semantic‑adjacent features.  
  

CnOB SHALL NOT consume forbidden metadata (routing, truth/done, lineage, Pipeline‑B).  
  

### 6. Residue Hashing & Query Address
Each constraint‑level residue fragment rᵢ′ MUST be hashable:  
hᵢ′ = hash(rᵢ′)  
  

Combined query address MUST satisfy:  
q′ = h₁′ ⊕ h₂′ ⊕ … ⊕ hₙ′  
  

### 7. SROB Preference
When both SOB and SROB fields exist, CnOB SHALL prefer SROB‑refined fields.  
  

### 8. Bounded Behavior & Prohibitions
CnOB SHALL NOT:
- perform deep semantic interpretation  
  
- infer intent or referent identity  
  
- modify TP text or meaning‑layer fields  
  
- overwrite SOB/SROB fields  
  

CnOB MAY write diagnostic‑only metadata (developer playback only).  
  

---

### Notes
- CnOB is the **third OB layer**, converting refined structure into rigid constraint objects.  
- CnOB prepares constraint residue for SmOB → WrdNm → ISc → SSG → STPX → DCB → RB.  
- CnOB is deterministic, bounded, monotonic, and strictly structural/semantic‑adjacent.  

## SmOB — Semantic‑Adjacent Object Base
**Spec:** 20.40.040_smob_prim.md  
**Pipeline Position:** After CnOB, before WrdNm  
**Purpose:** Perform two bounded, deterministic jobs:  
(1) extract semantic‑adjacent cues from SOB→SROB→CnOB residue   
(2) compress upstream residue + SmOB cues into a deterministic pre‑semantic residue hash + TR‑input cue vector .  
SmOB is strictly pre‑semantic and never performs deep meaning resolution, stance assignment, truth evaluation, or referent identity resolution .

---

### Input Contract
SmOB SHALL accept:  
- CnOB constraint residue + structural/semantic‑adjacent metadata   
- SROB/SOB residue when progressive‑lineup requires   
- CE/CEx context fields (thread summary, entities, temporal/causal markers, repair history) **read‑only** as structural/semantic‑adjacent cues   

SmOB SHALL NOT:  
- perform deep meaning resolution, intent inference, truth evaluation, referent identity resolution   
- consume routing_metadata, truth/done fields, lineage fields, Pipeline‑B envelopes, or ΔH% routing envelopes   

---

### Output Contract
SmOB SHALL output (SmOB‑owned fields only) :  
- semantic_adjacent_cues  
- modality_cues  
- affect_markers  
- conflict_adjacent_signals  
- underspecification_adjacent_signals  
- semantic_adjacent_importance_cues   
- presemantic_residue_hash   
- TR‑input cue vector   
- semantic‑adjacent change signals (from allowed fields only)   
- routing_semantic_cues  
- SmOB audit record + optional diagnostic metadata   

Output MUST be valid input for SSG and RB .

SmOB SHALL NOT overwrite SOB/SROB/CnOB fields or meaning‑layer fields .

---

### Transfer Function (SmOB)

### 1. **Job 1 — Pre‑Semantic Cue Extraction**  
SmOB SHALL extract semantic‑adjacent cues from upstream residue (SOB→SROB→CnOB) deterministically .  
Cues include:  
- semantic‑adjacent pattern activations  
- modality cues  
- affect markers  
- conflict‑adjacent signals  
- underspecification‑adjacent signals  
- constraint‑importance‑adjacent signals  
- TR‑input cues  
All extraction MUST be deterministic for identical CnOB inputs .

### 2. **Job 2 — Pre‑Semantic Residue Compression**  
SmOB SHALL compress upstream residue + SmOB cues into:  
- deterministic pre‑semantic residue hash   
- TR‑input cue vector (stable across replay)   
- semantic‑adjacent change signals (from allowed fields only)   

Compression MUST be deterministic and replay‑safe.

### 3. **Discourse‑Context Cue Normalization & Encoding**  
SmOB SHALL normalize discourse‑context structural flags (recent‑entity continuity, temporal shifts, contrastive markers, causal markers) into canonical pre‑semantic cue metadata .  
SmOB SHALL encode normalized discourse‑context metadata strictly as semantic‑adjacent cues in SmOB‑owned fields .  
SmOB SHALL NOT infer stance, semantic roles, referent identity, or truth when encoding discourse cues .

### 4. **Metadata Consumption (Bounded)**  
SmOB MAY consume deterministic TP‑stream metadata when applicable to cue extraction or residue compression (context_metadata, residue_metadata, semantic_layer_metadata, identity_metadata, continuity_metadata, expressive/normalization metadata) .  
SmOB SHALL treat all consumed metadata as structural or semantic‑adjacent features only .  
SmOB SHALL NOT consume forbidden metadata (routing, truth/done, lineage, Pipeline‑B, ΔH% routing envelopes) .

### 5. **Semantic‑Adjacent Importance Refinement**  
SmOB SHALL refine constraint‑importance residues from CnOB into semantic‑adjacent importance cues .  
Importance MUST be computed using deterministic structural/constraint/semantic‑adjacent cues only .  
SmOB SHALL NOT perform semantic‑role assignment or referent resolution when computing importance .  
Importance cues MUST remain addressable by RB and consumable by SSG/IdOB .

### 6. **Canonical Ordering**  
SmOB SHALL apply canonical ordering to all fields, including nested cue structures, ensuring deterministic replay and comparability .

### 7. **Residue Hashing & Query Address**  
Each residue fragment rᵢ′ MUST be hashable:  
hᵢ′ = hash(rᵢ′)   
Combined query address MUST satisfy:  
q′ = h₁′ ⊕ h₂′ ⊕ … ⊕ hₙ′   
Residue MUST preserve geometric invariants (smoothness, monotonicity, curvature‑invariance) .

### 8. **Bounded Behavior & Prohibitions**  
SmOB SHALL NOT:  
- perform deep semantic interpretation, meaning resolution, truth evaluation, intent inference, referent identity resolution   
- modify TP text or meaning‑layer fields   
- overwrite SOB/SROB/CnOB fields   
- consume forbidden metadata (routing, truth/done, lineage, Pipeline‑B, ΔH% routing envelopes)   

SmOB MAY write diagnostic‑only metadata for developer playback (never required by downstream primitives) .

### 9. **CnOB Preference Rule**  
When both earlier OB fields and CnOB fields exist, SmOB SHALL prefer CnOB constraint residue as primary input for Job 1 and Job 2 .

---

### Notes
- SmOB is the **fourth OB layer**, bridging OB residue → SSG signal pipeline.  
- SmOB is deterministic, bounded, and strictly semantic‑adjacent.  
- SmOB is the **sole pre‑semantic input** to SSG .  

## WrdNm — Word‑to‑Numeric Encoder
**Spec:** 20.44_wrdnm_primitive.md  
**Pipeline Position:** After SmOB, before ISc  
**Purpose:** Deterministically convert structured TP fields into numeric feature vectors for ISc. WrdNm is a pure encoder: schema‑driven, bounded, replay‑safe, position‑agnostic, and strictly pre‑semantic.  
WrdNm performs **no** semantic interpretation, truth evaluation, stance assignment, or referent resolution.  


---

### Input Contract
WrdNm SHALL accept structured TP fields produced by **all upstream primitives**:  
IIInB, IE, CEx, CE, TPU, SOB, SROB, CnOB, SmOB, SSG, STPX, RBU, DCB, RB, TR, CTP, IdOB, MCB.  


WrdNm SHALL treat all upstream fields as **read‑only**.  


WrdNm SHALL convert **only** fields listed in the WrdNm schema; all other fields are ignored.  


---

### Output Contract
WrdNm SHALL output:  
- categorical IDs (float32, ≤1/1000 fractional precision)  
- boolean numeric values (0/1)  
- scalar numeric values  
- deterministic hash values  
- complete numeric feature vector  
- WrdNm diagnostic record  


WrdNm output SHALL be valid input for **ISc** and stable across replay.  


WrdNm SHALL write only to **TP.wrdnm[]** (append‑only).  


WrdNm SHALL NOT modify upstream fields or meaning‑layer fields.  


---

### Transfer Function (WrdNm)

### 1. Deterministic Mapping Rules
WrdNm SHALL apply deterministic, bounded mappings:  
- categorical → float32 ID (precision ≤ 1/1000)  
- boolean → 0/1  
- scalar → bounded float  
- long structured fields → deterministic hash  
   

Identical TP inputs MUST produce identical numeric outputs.  


### 2. Schema Discipline
WrdNm SHALL use a **fixed schema file** defining all fields eligible for numeric conversion and their mapping types.  


WrdNm SHALL NOT infer new fields, scan TP text, or perform free‑form tokenization.  


WrdNm SHALL convert each field only if it exists in the TP **and** is listed in the schema.  


### 3. Owned‑Field Write Discipline
WrdNm SHALL write only WrdNm‑owned fields (numeric vectors + diagnostics).  


WrdNm SHALL NOT overwrite earlier WrdNm records; each invocation appends.  


### 4. Determinism & Replay Safety
All dictionary lookups, scalar mappings, and hash functions MUST be deterministic and replay‑safe.  


Numeric encoding MUST remain invariant under repeated Path‑A cycles.  


### 5. Forbidden Behavior
WrdNm SHALL NOT:  
- perform semantic smoothing or reconstruction  
- generate missing content  
- consume routing_metadata, truth/done fields, or Pipeline‑B envelopes  
- modify TP text or meaning‑layer propositions  
 

---

### Mathematical Requirements
Categorical mapping:  


\[
n_i = dict(c_i)
\]

  


Scalar mapping:  


\[
f_i = scalar\_map(s_i)
\]

  


Hashed fields:  


\[
H_i = hash(h_i)
\]

  


---

### Notes
- WrdNm is **pure encoding**, not scoring.  
- WrdNm is **position‑agnostic**: it does not depend on where fields were produced.  


- WrdNm is strictly pre‑semantic and bounded.  
- WrdNm is the final numeric‑encoding stage before **ISc**.

## ISc — Inference Scorer
**Spec:** 20.45_ts_isc_scoring.md  
**Pipeline Position:** After WrdNm, before SSG  
**Purpose:** Deterministically evaluate CE‑derived candidate_set{} using FFTM semantic features, WrdNm structural cues, discourse cues, metadata cues, and next‑turn context cues.  
ISc produces a normalized scoring distribution, entropy, ΔH%, confidence, rationale codes, and COP‑escalation proposals.  
ISc performs **meaning evaluation**, not meaning generation.  
ISc never mutates TP directly; all writes occur only via Merge → TPU.

---

### Input Contract
ISc SHALL consume only immutable inputs:   
- candidate_set{} from CE   
- FFTM semantic‑layer features (token_surface, token_base, token_expression, token_intent)   
- WrdNm structural‑layer numeric encodings (surface_id, lemma_id, expression_id, temporal_id, causal_id, continuity_id, entity_id, modality, affect, underspec, adjacency, ordering_id, constraint_family_id, constraint_importance, missing_slot, routing_id, transform_id, identity_id, next_context_id, thread_hash)   
- discourse‑context cues from STPX (normalized)   
- deterministic TP‑stream metadata (context_metadata, residue_metadata, semantic_layer_metadata, identity_metadata, continuity_metadata, expressive/normalization metadata, next_context_metadata)   
- next‑turn context fields from CE.context_fields{} (topic, stance, intent, continuity, direction, coherence, importance)   

ISc SHALL NOT consume:  
- routing_metadata, ΔH%, truth/done fields, lineage fields, Pipeline‑B envelopes   

---

### Output Contract
ISc SHALL output:  
- isc_output{} (canonical structured scoring object)   
- normalized scoring distribution over candidate_set{}   
- entropy, ΔH%, confidence, rationale codes   
- COP‑escalation proposals (when thresholds met)   

ISc SHALL NOT write directly to TP; all writes occur only via Merge → TPU → TP.   

ISc output becomes visible only in TP(N+1) (1‑cycle lag).   

---

### Transfer Function (ISc)

### 1. Deterministic Scoring  
ISc SHALL produce identical outputs for identical inputs, state, and seed.   

### 2. FFTM‑Based Semantic Scoring  
ISc SHALL score candidates using FFTM fields: token_surface, token_base, token_expression, token_intent.   

Canonical scoring equation:  


\[
score(c) = w_s f_s(c) + w_b f_b(c) + w_e f_e(c) + w_i f_i(c)
\]

  
  

Meaning‑layer cues (expression, intent) SHALL be weighted more heavily than surface‑form cues.   

### 3. Structural‑Layer Scoring  
ISc SHALL consume WrdNm numeric encodings strictly as structural meaning‑adjacent features.   

ISc SHALL NOT modify semantic_core or FFTM fields.   

### 4. Discourse‑Context Scoring  
ISc SHALL consume normalized discourse cues from STPX.   
ISc SHALL treat discourse cues strictly as structural features.   
ISc SHALL apply deterministic scoring to discourse cues.   

### 5. Metadata Scoring  
ISc SHALL consume deterministic TP‑stream metadata only when applicable to scoring.   
ISc SHALL treat all metadata as read‑only.   

### 6. Next‑Turn Context Scoring  
ISc SHALL read next‑turn context fields exclusively from CE.context_fields{}.   
ISc SHALL treat them as structural scoring features.   
ISc SHALL NOT infer or derive next‑turn context.   

### 7. Probability Normalization  
ISc SHALL compute candidate probabilities using canonical softmax:  


\[
p(c) = \frac{\exp(score(c))}{\sum_{c'} \exp(score(c'))}
\]

  
  

### 8. Entropy & ΔH%  
Entropy:  


\[
H = -\sum_{c} p(c)\log p(c)
\]

  
  

ΔH%:  


\[
\Delta H\% = \frac{H_{current} - H_{previous}}{H_{previous}} \times 100
\]

  
  

First‑cycle initialization:  


\[
H_{previous}=0,\quad \Delta H\%=0
\]

  
when TP.process.first_cycle = true.   

### 9. COP Escalation  
ISc SHALL trigger COP escalation when deterministic policy thresholds are met.   

### 10. Forbidden Actions  
ISc SHALL NOT:  
- generate meaning or expand candidate_set{}   
- interact with Pipeline‑B   
- modify TP directly   
- mutate semantic_core   
- bypass Merge or TPU   
- use nondeterministic methods   

---

### Notes
- ISc is the **deterministic scoring primitive** of Path‑A.   
- ISc evaluates meaning; it does not generate meaning.   
- ISc is the final scoring stage before SSG.  

## SSG — Structural Signature Generator
**Spec:** 20.47_ssg_prim.md  
**Pipeline Position:** After SmOB, before RB  
**Purpose:** Convert the SmOB structural graph into a fixed‑length, L2‑normalized structural‑invariant vector `tp.ssg_signature` used by RB for deterministic relational routing.  
SSG encodes **how structure is arranged**, not what it means .  
SSG performs **no semantic interpretation**, **no routing**, and **no meaning‑layer computation** .

---

### Input Contract
SSG SHALL accept **only** the SmOB structural graph as structural input :

- V — residue nodes  
- E — directed arcs  
- λ : V ∪ E → L — structural labels  

SSG SHALL NOT read global state, CIL, CE, or external data sources .

SSG MAY consume deterministic, bounded structural‑adjacent metadata (residue_metadata, semantic_adjacent_metadata, structural_metadata, continuity_metadata, expressive/normalization metadata, provenance_metadata, lineage_metadata, entropy/signature histories) strictly as **structural‑adjacent features** .

SSG SHALL NOT consume routing_metadata, semantic ΔH%, truth/done fields, or Pipeline‑B envelopes .

---

### Output Contract
SSG SHALL write exactly four TP fields :

- `tp.ssg_signature` — float[d]  
- `tp.ssg_layer_bitmap` — 4‑bit mask  
- `tp.ssg_reason_code` — enum  
- `tp.ssg_status` — enum  

SSG SHALL NOT modify any other TP fields .

SSG SHALL append an `ssg_ref` audit record to exec_trace on every successful invocation .

---

### Transfer Function (SSG)

### 1. Structural Invariant Extraction
SSG SHALL compute a deterministic, seed‑free, fixed‑length vector σ ∈ ℝᵈ:  


\[
σ = φ(G) / \|φ(G)\|_2
\]

  
where φ(G) extracts d structural invariants .

Invariant families (five groups) :

1. **Arc patterns** — normalized arc‑label frequencies  
2. **Binding depth** — max/mean depth of directed binding chains  
3. **Residue entropy** — Shannon entropy over residue‑address distribution  
4. **Curvature** — cycle density + clustering coefficient  
5. **Motif frequencies** — normalized counts of canonical structural motifs  

If no invariants are present, signature MUST be zero vector .

### 2. Layer Bitmap Construction
Bitmap bits correspond to OB layers :

- L0 = SOB  
- L1 = SROB  
- L2 = CnOB  
- L3 = SmOB  



\[
bitmap = \sum_{i=0}^{3} b_i \cdot 2^i
\]



where bᵢ = 1 if layer contributed invariants, else 0.

### 3. Reason Code Assignment
Reason codes :

- **FULL** — all layers contributed  
- **PARTIAL** — some layers contributed zero  
- **EMPTY** — no invariants present  

### 4. Status Field
SSG SHALL expose `tp.ssg_status ∈ {OK, MISSING_INPUT, DEGENERATE, PARTIAL}` .

### 5. Determinism & Replay
SSG SHALL produce identical signatures for identical structural graphs across all invocations .

SSG SHALL be invoked exactly once per TP per OB‑chain cycle and never re‑invoked without new SmOB output .

### 6. Failure Modes
**Missing Input** — set status=MISSING_INPUT, do not write signature, escalate to MB‑gov .  
**Absent Layer** — treat invariant contribution as zero, clear bitmap bit, reason_code=PARTIAL .  
**Degenerate Case** — φ(G) non‑empty but norm=0 → status=DEGENERATE, signature=0, escalate to MB‑gov .

---

### Notes
- SSG is the **final structural primitive** in Path‑A before RB .  
- SSG provides RB with a **coordinate chart** on the structural manifold .  
- SSG encodes **structure**, not meaning .  

## STPX — Structured Token & Pattern Extractor
**Spec:** 20.49_stpx_prim.md  
**Pipeline Position:** After SSG, before RBU  
**Purpose:** Extract deterministic lexical, structural, constraint, discourse‑context, and repair‑region cues from structural geometry and canonical tokens, producing a bounded, replay‑safe `cue_envelope` CE = {L, S, C, R}.  
STPX operates strictly on **structural geometry**, never semantic geometry .

---

### Input Contract
STPX SHALL consume (read‑only):

- **Structural geometry**:  
  TP.metadata.structural_metadata.*, TP.metadata.residue_metadata.*   
  SmOB structural graph, constraint surfaces, segment boundaries  

- **SSG output**:  
  tp.ssg_signature, tp.ssg_layer_bitmap, tp.ssg_reason_code, tp.ssg_status  
  (authoritative structural‑adjacent metadata) 

- **Canonical tokens**:  
  normalized tokens from IE, expressive metadata, repair metadata 

- **Structural‑adjacent metadata**:  
  continuity_metadata, expressive_metadata, normalization_metadata, provenance_metadata, lineage_metadata, entropy/signature histories 

STPX SHALL NOT consume:  
semantic envelope, context envelope, routing_metadata, identity_metadata, truth/done fields, Pipeline‑B envelopes .

---

### Output Contract
STPX SHALL write only:

- **TP.metadata.semantic_layer_metadata.stpx_cues**  
- **TP.metadata.semantic_layer_metadata.semantic_layer_provenance**  

No other TP fields may be modified .

Provenance MUST include origin primitive, last update primitive, TPU commit identifier, and full commit lineage .

---

### Cue Envelope Schema
STPX SHALL emit a deterministic cue_envelope:



\[
CE = \{ L, S, C, R \}
\]



Where:  
- **L** — lexical surface cues  
- **S** — structural cues (incl. discourse‑context cues)  
- **C** — constraint cues  
- **R** — repair‑region markers  
All categories MUST be bounded, deterministic, and replay‑safe .

---

### Transfer Function (STPX)

### 1. Deterministic Cue Extraction
STPX SHALL compute:



\[
CE = Extract(G_{\text{struct}}, T_{\text{clean}}, M_{\text{struct-adjacent}})
\]



Identical inputs MUST produce identical cue_envelopes .

### 2. Lexical Surface Cues
Extract lexical cues from canonical tokens (L)  
HLR‑20.49‑003 .

### 3. Structural Cues
Emit structural cues derived from structural geometry + invariant patterns (S)  
HLR‑20.49‑004 .

### 4. Constraint Cues
Emit constraint cues derived from constraint‑level residue + structural constraint metadata (C)  
HLR‑20.49‑005 .

### 5. Repair‑Region Markers
Emit repair‑region markers when present (R)  
HLR‑20.49‑006 .

### 6. Discourse‑Context Cue Handling
STPX SHALL:

- consume normalized discourse‑context structural cues from SmOB  
  HLR‑20.49‑011   
- treat them strictly as structural geometry (no semantic interpretation)  
  HLR‑20.49‑012   
- emit them deterministically  
  HLR‑20.49‑013   
- integrate them into structural cue category (S)  
  HLR‑20.49‑014 

### 7. Metadata Consumption Rules
STPX SHALL:

- consume applicable deterministic TP‑stream metadata when relevant  
  HLR‑20.49‑015   
- treat all metadata as read‑only  
  HLR‑20.49‑016   
- consume metadata only when relevant to cue extraction  
  HLR‑20.49‑017   
- NOT consume routing_metadata, semantic ΔH%, truth/done fields, lineage fields owned by Path‑B, or Pipeline‑B envelopes  
  HLR‑20.49‑018   
- treat all consumed metadata as structural‑adjacent features  
  HLR‑20.49‑019   
- integrate metadata only when it affects cue completeness, determinism, or replay safety  
  HLR‑20.49‑020 

### 8. Provenance Writes
STPX SHALL:

- write cue_envelope to TP.metadata.semantic_layer_metadata.stpx_cues  
  HLR‑20.49‑021   
- write provenance under semantic_layer_provenance  
  HLR‑20.49‑022   
- ensure provenance is deterministic and replay‑safe  
  HLR‑20.49‑023   
- use canonical nested TP paths  
  HLR‑20.49‑024   
- NOT re‑derive upstream observations already encoded in metadata  
  HLR‑20.49‑025   
- treat SSG outputs as authoritative structural‑adjacent metadata  
  HLR‑20.49‑026 

### 9. Prohibited Behavior
STPX SHALL NOT:

- perform semantic interpretation, identity resolution, routing, entropy scoring, or meaning refinement  
  HLR‑20.49‑007   
- modify TPU, meaning geometry, identity fields, routing fields, or truth‑evaluation fields  
  HLR‑20.49‑008 

---

### Notes
- STPX is the **post‑SSG structural cue extractor** in Path‑A .  
- STPX prepares deterministic cues for ISc, RB, IdOB, and routing primitives.  
- STPX is strictly structural, bounded, deterministic, and replay‑safe.

## DCB — Directional Conversation Basin
**Spec:** 20.106_dcb_requirements.md  
**Pipeline Position:** After STPX, before RB  
**Purpose:** DCB is the deterministic execution‑flow indexer for Path‑A.  
It produces:  
- geometric_state snapshot (scalar fields)   
- directional‑change events (delta or cycle_start)   
- geometric_history entries (append‑only)   

DCB is **non‑semantic**, **non‑structural**, **non‑identity**, **non‑routing**.  
It observes execution‑flow only. 

---

### Input Contract
DCB MAY read only:  
- previous TP.metadata.geometric_state (if present)   
- runner‑supplied:  
  - current_primitive_id  
  - cycle_id  
  - timestamp   

DCB SHALL NOT read:  
- semantic metadata  
- structural metadata  
- identity metadata  
- routing metadata 

---

### Output Contract
DCB SHALL write only:  
- TP.metadata.geometric_state.* (overwrite all fields)   
- TP.metadata.geometric_history[] (append‑only, exactly one entry per invocation)   
- TP.metadata.dcb_events[] (append‑only)   
- TP.metadata.provenance.dcb_last_update := timestamp   

DCB SHALL NOT modify any other TP fields. 

---

### Geometric State (Snapshot)
DCB writes five scalar fields:  
- position : int  
- direction : int  
- curvature : float  
- step_index : int  
- lane_id : int  
All overwritten each invocation. 

Constraints:  
- position ∈ [0, N−1]  
- direction ∈ [0, N−1]  
- curvature ∈ [0.0, 1.0]  
- step_index ≥ 0  
- lane_id = 0 (v1) 

---

### Directional‑Change Events
DCB appends events containing prev_* and new_* values.  
- First cycle: **cycle_start** event only (prev_* = null).   
- Later cycles: **delta** event iff any geometric_state field changed. 

---

### Geometric History
DCB appends exactly one history entry per invocation.  
History is strictly ordered by cycle_id and append‑only. 

Each entry contains:  
{ position, direction, curvature, step_index, lane_id, cycle_id, timestamp } 

---

### Computation Contract (v1)
Let:  
- prev = previous geometric_state (if any)  
- curr_primitive = ordinal(current_primitive_id)   
- N = len(PATH_A) (fixed routing‑loop table)   

DCB computes:

1. **position**  
   

\[
   position := curr_primitive
   \]

  
   

2. **direction**  
   

\[
   direction := (curr_primitive + 1) \bmod N
   \]

  
   

3. **step_index**  
   - if no prev: 0  
   - else: prev.step_index + 1  
   

4. **lane_id**  
   

\[
   lane_id := 0
   \]

  
   (v1 only) 

5. **curvature**  
   If no prev: 0.0  
   Else:  
   - expected_direction = (prev.position + 1) mod N  
   - curvature = 0.0 if direction == expected_direction  
   - curvature = 1.0 otherwise  
   

---

### First‑Cycle Policy
If no previous geometric_state exists:  
- write geometric_state  
- append exactly one geometric_history entry  
- emit exactly one cycle_start event  
- **no delta event** on first cycle  


---

### Subsequent‑Cycle Policy
If previous geometric_state exists:  
- write geometric_state  
- append exactly one geometric_history entry  
- emit exactly one delta event **iff** any field changed  


---

### Invariants
- geometric_state has exactly five scalar fields  
- geometric_state overwritten each cycle  
- geometric_history append‑only  
- dcb_events append‑only  
- curvature binary (0.0 or 1.0)  
- lane_id = 0  
- direction follows routing‑loop ordinal table  
- step_index increments deterministically  


---

### Notes
- DCB maintains **no hidden internal state**.   
- DCB provides deterministic execution‑flow visibility for Path‑A.   
- DCB does not interpret semantic, structural, identity, or routing metadata. 

## RB — Relational Basin (Routing Primitive)
**Spec:** 20.50_rb_requirements.md  
**Pipeline Position:** After DCB, before TR  
**Purpose:** Deterministic routing, arbitration, and TR‑gating authority for Pipeline‑A.  
RB computes the routing filter, adjacency class, displacement scale, regime hint, and RB_out fields using relational topology, structural metadata, STPX cues, TR state, ΔH, IdOB view (read‑only), and optional F‑approximations.  
RB performs **no semantic interpretation**, **no identity resolution**, **no TR mutation**, **no Pipeline‑B behavior**.

---

### Input Contract
RB MAY read (all read‑only):
- TP.input_fields   
- TP.TR (read‑only)   
- TP.tr_needs_update   
- TP.process.deltaH (Q32.32)   
- TP.semantic.lineage   
- TP.process.routing_metadata   
- IdOB view fields (read‑only)   
- DCB geometric_state / geometric_history (execution‑flow only)   
- Structural metadata (SOB, SROB, CnOB, SmOB, SSG)   
- STPX cue_envelope metadata   
- Continuity metadata (COB, CIL, CST)   
- Expressive / normalization metadata (IIInB, IE)   
- Semantic_layer_metadata (IdOB, MCB) — read‑only view   
- Entropy & signature histories (TR, OuBA, SSRGn, TPU)   

RB SHALL NOT read:
- Pipeline‑B fields   
- truth_hypotheses, exec_plan, exec_trace, semantic_core   
- messy_input_record as authoritative semantic content   

---

### Output Contract
RB SHALL write only:
- **routing_filter{}** (canonical, deterministic)   
- **RB_out fields** (adjacency_class, displacement_scale, regime_hint, route_proposal) when enabled   

RB SHALL NOT modify:
- TP.TR, tr_needs_update   
- TP.context, semantic_core, IdOB fields, DCB fields, TP.intake, TP.process (except routing metadata)   

---

### Transfer Function (RB)

### 1. TR‑Gating (Normative)
RB SHALL route a TP to TR **iff** `TP.tr_needs_update = true` .  
RB SHALL NOT modify TP.TR or tr_needs_update .

### 2. Deterministic Routing Equation
RB SHALL compute routing as:  


\[
RB_{\text{route}}(TP) = f(TP.input\_fields,\ TP.TR,\ TP.tr\_needs\_update,\ TP.process.\Delta H,\ TP.semantic.lineage,\ TP.process.routing\_metadata,\ policy\_signature,\ IdOB\_view?,\ F\text{-approx}?)
\]

  


All optional inputs remain strictly read‑only and SHALL NOT relax determinism .

### 3. Multi‑Core Routing
RB SHALL route only to OBs whose orthogonality_signature matches the TP’s core domain .  
RB SHALL maintain strict core‑isolation; no cross‑core merges/splits .

### 4. Canonical Routing Filter Construction
RB SHALL compute a deterministic routing filter each cycle .  
Filter MUST be canonical, inspectable, replayable .  
All nested maps and arrays MUST use canonical ordering .

Canonical fields include:  
- selected_ob_ids[]  
- lane_projections[]  
- delta_h_routing_context  
- firing_order[]  
- transition_rationale[]  
- policy_justification{}  
- inquiry_escalation?  
- merge_eligibility?  
- split_directive?  


### 5. Foundation RED Fields (When Enabled)
RB SHALL compute:  
- adjacency_class (local | non_local)   
- displacement_scale (small | medium | large) via RED law   
- regime_hint (Stable, Refinement, Drift, Transition, Collapse) when F‑approx available   

### 6. Split / Merge Arbitration
RB SHALL deterministically arbitrate split events   
and merge events .  
RB SHALL NOT perform cross‑core merges/splits .

### 7. Messy‑Input Routing
RB SHALL treat messy‑input fields as read‑only contextual signals .  
RB SHALL NOT infer new routing semantics from missing/noisy fields .  
RB SHALL route messy inputs using the same deterministic routing equation as clean inputs .  
RB SHALL NOT smooth or repair messy inputs .

### 8. Structural Transition Eligibility (TE)
RB SHALL evaluate TE eligibility using only:  
- committed TP.TR  
- TP.process.routing_metadata  
- relational‑topology constraints  
- optional IdOB view / F‑approx (read‑only)  


### 9. RB Invariants
RB SHALL maintain:  
- Deterministic Routing Invariant: identical inputs → identical routing filters   
- TR‑Gating Invariant: TR only when tr_needs_update=true   
- Core‑Isolation Invariant: no cross‑core merges/splits   
- Read‑Only TR Invariant: RB SHALL NOT modify TP.TR   
- Canonical Ordering Invariant: all arrays/maps canonical   
- Layer‑Separation Invariant: RB SHALL NOT conflate κ_exec, κ_id, κ_route   
- IdOB Non‑Mutation Invariant: RB SHALL NOT mutate IdOB fields   

---

### Notes
- RB is the **deterministic routing authority** of Path‑A.  
- RB is strictly read‑only except for routing_filter + RB_out fields.  
- RB is the final primitive before TR in the Path‑A cycle.  


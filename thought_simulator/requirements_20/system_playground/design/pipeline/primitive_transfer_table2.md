## MCB — Meaning Clarification Block
**Spec:** 20.40.055_mcb_prim.md  
**Pipeline Position:** Immediately after IdOB  
**Purpose:** Clarify meaning, reconcile messy input, update next_context, and prepare TP for RBU.

---

### Input Contract (from IdOB TP)
MCB consumes the full TP envelope produced by IdOB:

- semantic_envelope  
- epistemic_envelope  
- identity_envelope  
- context_envelope  
- provenance_envelope  
- metadata_envelope  
- trace_envelope  

All fields defined in 20.40.060.700 must be present.

---

### Output Contract (MCB TP)
MCB outputs a TP with the same envelope structure, but with:

- **semantic_envelope.proposition_set**: clarified meaning  
- **semantic_envelope.messy_input_record**: consumed or normalized  
- **context_envelope.next_context**: updated based on clarified meaning  
- **epistemic_envelope.delta_h_percent**: adjusted if meaning clarification reduces entropy  
- **trace_envelope.tb_trace**: append `TB.mcb_alignment`  
- **provenance_envelope.lineage_log**: append `mcb`  
- **provenance_envelope.routing_path**: append `mcb`  
- **metadata_envelope.policy_markers**: preserved  
- **identity_envelope**: unchanged (MCB does not alter identity geometry)

MCB does **not** freeze identity, alter basin geometry, or modify continuity.

---

### Transfer Function (MCB)
MCB applies the following transformations:

1. **Meaning Clarification**
   - Convert messy_input_record → clarified proposition_set  
   - Normalize semantic tags  
   - Remove ambiguity where possible  
   - Ensure proposition_set is consistent with IdOB identity geometry

2. **Next Context Update**
   - Derive next_context.topic from clarified meaning  
   - Derive next_context.stance from user intent  
   - Derive next_context.intent from semantic role  
   - Adjust next_context.importance if meaning is sharpened  
   - Preserve continuity unless meaning correction requires adjustment

3. **Epistemic Adjustment**
   - Reduce delta_h_percent if clarification reduces semantic entropy  
   - Append entropy_history entry

4. **Provenance & Routing**
   - Append `mcb` to lineage_log  
   - Append `mcb` to routing_path  
   - Update sob/srob/cnob/smob/idob/mcb IDs

5. **Trace Update**
   - Append `TB.mcb_alignment` to tb_trace  
   - Append `OB.mcb_semantic_pass` if applicable

6. **No Structural Changes**
   - Identity geometry unchanged  
   - Continuity unchanged  
   - Basin surface unchanged  
   - Freeze state unchanged  
   - No SSR seeds created  
   - No boundary conditions applied

---

### Notes
- MCB is the **first primitive after IdOB** and sets the stage for RBU.  
- MCB’s job is *semantic hygiene*: clarify, normalize, and prepare meaning for downstream routing.  
- MCB never freezes meaning, never bifurcates identity, and never applies correction pressure.  
- MCB is deterministic: same input TP → same output TP.

## RBU — Routing Block Update
**Spec:** 20.51_rbu_prim.md  
**Pipeline Position:** After MCB, before TR  
**Purpose:** Commit routing deltas produced by RB/IdOB/MCB into the TP’s routing structures so TR can operate on a stable routing state.

---

### Input Contract (from MCB TP)
RBU consumes the full TP envelope produced by MCB:

- semantic_envelope  
- epistemic_envelope  
- identity_envelope  
- context_envelope  
- provenance_envelope  
- metadata_envelope  
- trace_envelope  

Additionally, RBU requires:

- **routing deltas** generated upstream (RB → IdOB → MCB)  
- **stable identity geometry** (RBU does not modify identity)  
- **next_context** (RBU does not modify stance/intent/topic)

---

### Output Contract (RBU TP)
RBU outputs a TP with the same envelope structure, but with:

- **provenance_envelope.routing_path**: append `rbu`  
- **provenance_envelope.lineage_log**: append `rbu`  
- **routing deltas committed** into the TP’s routing structures  
- **semantic_envelope**: unchanged  
- **identity_envelope**: unchanged  
- **context_envelope**: unchanged  
- **epistemic_envelope.delta_h_percent**: may decrease slightly if routing stabilization reduces entropy  
- **trace_envelope.tb_trace**: append `TB.rbu_commit`  

RBU does **not** alter meaning, identity geometry, continuity, basin surface, or freeze state.

---

### Transfer Function (RBU)
RBU applies the following transformations:

1. **Routing Delta Commitment**
   - Take routing deltas accumulated from RB → IdOB → MCB  
   - Commit them into the TP’s routing structures  
   - Ensure routing state is stable and deterministic for TR

2. **Routing Path Update**
   - Append `rbu` to routing_path  
   - Update primitive IDs (sob/srob/cnob/smob/idob/mcb/rbu)

3. **Provenance Update**
   - Append `rbu` to lineage_log  
   - Preserve all upstream provenance markers

4. **Epistemic Adjustment**
   - If routing stabilization reduces uncertainty, adjust delta_h_percent  
   - Append entropy_history entry

5. **Trace Update**
   - Append `TB.rbu_commit` to tb_trace  
   - Optionally append `OB.rbu_pass` if defined in spec

6. **No Semantic or Identity Changes**
   - semantic_envelope unchanged  
   - identity_envelope unchanged  
   - continuity unchanged  
   - basin geometry unchanged  
   - freeze state unchanged  
   - no SSR seeds created  
   - no boundary conditions applied

---

### Notes
- RBU is a **pure routing primitive**: it commits routing metadata but does not alter meaning or identity.  
- TR depends on RBU’s output; without RBU, TR cannot operate deterministically.  
- RBU is deterministic: same input TP → same committed routing state → same output TP.  
- RBU is lightweight but essential for pipeline stability.

## TR — Thought Router
**Spec:** 20.37_thought_router_tr_specification.md  
**Pipeline Position:** After RBU, before CTP  
**Purpose:** Deterministically select the next semantic processing direction using geometric, relational, and cultural signals. TR does not generate meaning, interpret semantics, or modify TP fields.

---

### Input Contract (from RBU TP)
TR consumes the full TP envelope produced by RBU:

- semantic_envelope  
- epistemic_envelope  
- identity_envelope  
- context_envelope  
- provenance_envelope  
- metadata_envelope  
- trace_envelope  

Additional required inputs:

- **OB outputs** (local meaning fragments, cultural cues)  
- **DCB directional-change events** (geometric curvature signals)  
- **RB topology constraints** (allowed relational transitions)  
- **TP trajectory state** (read-only)  
- **tr_needs_update flag** (must be true for TR to run)

Identity geometry must be stable enough for routing; TR does not modify identity.

---

### Output Contract (TR TP)
TR outputs a TP with the same envelope structure, but with:

- **identity_envelope.tr_needs_update = false** (after successful recompute)  
- **provenance_envelope.routing_path**: append `tr`  
- **provenance_envelope.lineage_log**: append `tr`  
- **trace_envelope.tb_trace**: append `TB.tr_routing_decision`  
- **semantic_envelope**: unchanged  
- **identity_envelope**: unchanged (TR never writes TP fields)  
- **context_envelope**: unchanged  
- **epistemic_envelope.delta_h_percent**: may decrease slightly if routing decision reduces uncertainty  

TR produces **one deterministic routing decision** consumed by RB.

---

### Transfer Function (TR)
TR applies the following transformations:

1. **Routing Decision**
   - Consume OB evidence fragments  
   - Consume DCB directional-change events  
   - Consume RB topology constraints  
   - Evaluate geometric, cultural, and relational signals  
   - Produce a deterministic routing decision for RB  
   - Clear `tr_needs_update = false` after recompute

2. **Deterministic Behavior**
   - Given identical OB/DCB/RB/TP inputs, TR must produce the same routing decision  
   - TR is replay-safe and stable under identical conditions

3. **Provenance & Routing Updates**
   - Append `tr` to routing_path  
   - Append `tr` to lineage_log  
   - Update primitive IDs (sob/srob/cnob/smob/idob/mcb/rbu/tr)

4. **Epistemic Adjustment**
   - If routing decision reduces uncertainty, adjust delta_h_percent  
   - Append entropy_history entry

5. **Trace Update**
   - Append `TB.tr_routing_decision` to tb_trace  
   - Optionally append `OB.tr_pass` if defined in spec

6. **No Semantic or Identity Changes**
   - semantic_envelope unchanged  
   - identity_envelope unchanged  
   - continuity unchanged  
   - basin geometry unchanged  
   - freeze state unchanged  
   - no SSR seeds created  
   - no boundary conditions applied  
   - TR never writes TP fields or semantic_core

---

### Notes
- TR is a **pure routing primitive**: it selects the next relational transition but does not generate or interpret meaning.  
- TR is part of **Path A**, not IB, and not part of Pipeline B.  
- TR is upstream of RB; RB consumes TR’s routing decision.  
- TR only runs when `tr_needs_update = true`.  
- TR is deterministic and replay-safe.

## CTP — Context Transition Primitive
**Spec:** 20.145_ctp_prim.md  
**Pipeline Position:** After TR, before CEx  
**Purpose:** Convert the TP’s current context into the correct “next context” state, ensuring continuity, stance, intent, topic, and importance are properly transitioned for downstream semantic processing.

---

### Input Contract (from TR TP)
CTP consumes the full TP envelope produced by TR:

- semantic_envelope  
- epistemic_envelope  
- identity_envelope  
- context_envelope  
- provenance_envelope  
- metadata_envelope  
- trace_envelope  

Required conditions:

- **context_envelope.next_context** must be populated (MCB creates it; TR preserves it)  
- **identity geometry** must be stable (CTP does not modify identity)  
- **TR routing decision** must be committed (RBU → TR)

---

### Output Contract (CTP TP)
CTP outputs a TP with the same envelope structure, but with:

- **context_envelope.current_context** updated to next_context  
- **context_envelope.next_context** regenerated for the next primitive  
- **continuity_envelope** updated (continuity progression or correction)  
- **provenance_envelope.routing_path**: append `ctp`  
- **provenance_envelope.lineage_log**: append `ctp`  
- **trace_envelope.tb_trace**: append `TB.ctp_transition`  
- **semantic_envelope**: unchanged  
- **identity_envelope**: unchanged  
- **epistemic_envelope.delta_h_percent**: may decrease if context transition reduces uncertainty  

CTP does **not** freeze meaning, modify identity, or alter semantic_core.

---

### Transfer Function (CTP)
CTP applies the following transformations:

1. **Context Transition**
   - Promote next_context → current_context  
   - Generate a new next_context based on:  
     - clarified meaning (from MCB)  
     - routing decision (from TR)  
     - continuity state  
     - semantic role and stance  
   - Ensure topic, stance, intent, and importance are coherent

2. **Continuity Update**
   - If context transition is smooth → continuity = progression  
   - If meaning correction is needed → continuity = adjustment  
   - If routing decision introduces tension → continuity = wobble  
   - Append continuity entry to continuity_envelope

3. **Epistemic Adjustment**
   - Reduce delta_h_percent if context transition reduces entropy  
   - Append entropy_history entry

4. **Provenance & Routing Updates**
   - Append `ctp` to routing_path  
   - Append `ctp` to lineage_log  
   - Update primitive IDs (sob/srob/cnob/smob/idob/mcb/rbu/tr/ctp)

5. **Trace Update**
   - Append `TB.ctp_transition` to tb_trace  
   - Optionally append `OB.ctp_pass` if defined in spec

6. **No Semantic or Identity Changes**
   - semantic_envelope unchanged  
   - identity_envelope unchanged  
   - basin geometry unchanged  
   - freeze state unchanged  
   - no SSR seeds created  
   - no boundary conditions applied

---

### Notes
- CTP is the **bridge** between meaning clarification (MCB) and semantic extraction (CEx).  
- CTP ensures the TP’s context is always “pointing in the right direction” for downstream primitives.  
- CTP is deterministic: same input TP → same context transition → same output TP.  
- CTP never writes semantic_core, never freezes identity, and never alters meaning.

## CEx‑IE — Context Extraction (Interpretive Engine)
**Spec:** 20.107.010_cex-ie_primitive.md  
**Pipeline Position:** After CTP, before CEx‑CCR  
**Purpose:** Extract interpretable semantic structure from the TP’s clarified meaning and transitioned context. CEx‑IE converts meaning + context into a structured interpretive representation consumed by CCR.

---

### Input Contract (from CTP TP)
CEx‑IE consumes the full TP envelope produced by CTP:

- semantic_envelope  
- epistemic_envelope  
- identity_envelope  
- context_envelope  
- provenance_envelope  
- metadata_envelope  
- trace_envelope  

Required conditions:

- **semantic_envelope.proposition_set** must be clarified (MCB)  
- **context_envelope.current_context** must be stable (CTP)  
- **identity geometry** must be stable (CEx‑IE does not modify identity)  
- **continuity** must be valid (CTP ensures this)

---

### Output Contract (CEx‑IE TP)
CEx‑IE outputs a TP with the same envelope structure, but with:

- **semantic_envelope.interpretive_record**: newly created interpretive structure  
- **semantic_envelope.extraction_tags**: tags describing interpretive features  
- **semantic_envelope.proposition_set**: preserved  
- **context_envelope**: unchanged  
- **identity_envelope**: unchanged  
- **epistemic_envelope.delta_h_percent**: may decrease if interpretive extraction reduces entropy  
- **provenance_envelope.routing_path**: append `cex-ie`  
- **provenance_envelope.lineage_log**: append `cex-ie`  
- **trace_envelope.tb_trace**: append `TB.cex_ie_extract`  

CEx‑IE does **not** freeze meaning, modify identity, or alter semantic_core.

---

### Transfer Function (CEx‑IE)
CEx‑IE applies the following transformations:

1. **Interpretive Extraction**
   - Convert proposition_set → interpretive_record  
   - Identify semantic roles, relations, and structural features  
   - Generate extraction_tags describing interpretive structure  
   - Ensure interpretive_record is deterministic and replay-safe

2. **Interpretive Normalization**
   - Normalize interpretive_record for downstream CCR consumption  
   - Ensure structural consistency across all TP fields  
   - Remove ambiguity where possible

3. **Epistemic Adjustment**
   - Reduce delta_h_percent if interpretive extraction reduces entropy  
   - Append entropy_history entry

4. **Provenance & Routing Updates**
   - Append `cex-ie` to routing_path  
   - Append `cex-ie` to lineage_log  
   - Update primitive IDs (sob/srob/cnob/smob/idob/mcb/rbu/tr/ctp/cex-ie)

5. **Trace Update**
   - Append `TB.cex_ie_extract` to tb_trace  
   - Optionally append `OB.cex_ie_pass` if defined in spec

6. **No Semantic or Identity Changes**
   - semantic_envelope.proposition_set unchanged  
   - identity_envelope unchanged  
   - continuity unchanged  
   - basin geometry unchanged  
   - freeze state unchanged  
   - no SSR seeds created  
   - no boundary conditions applied

---

### Notes
- CEx‑IE is the **first stage** of the CEx pipeline (IE → CCR → PCK).  
- CEx‑IE extracts *interpretive meaning*, not canonical meaning.  
- CEx‑IE is deterministic: same input TP → same interpretive_record → same output TP.  
- CEx‑IE never writes semantic_core, never freezes identity, and never alters context.

## CEx‑CCR — Context Extraction (Canonical Core Representation)
**Spec:** 20.107.020_cex-ccr_primitive.md  
**Pipeline Position:** After CEx‑IE, before CEx‑PCK  
**Purpose:** Convert the interpretive_record produced by CEx‑IE into a canonical, stable, replay‑safe semantic representation. CCR is the “semantic stabilizer” of the CEx pipeline.

---

### Input Contract (from CEx‑IE TP)
CEx‑CCR consumes the full TP envelope produced by CEx‑IE:

- semantic_envelope  
- epistemic_envelope  
- identity_envelope  
- context_envelope  
- provenance_envelope  
- metadata_envelope  
- trace_envelope  

Required conditions:

- **semantic_envelope.interpretive_record** must exist (CEx‑IE creates it)  
- **semantic_envelope.extraction_tags** must exist  
- **identity geometry** must be stable (CCR does not modify identity)  
- **context_envelope.current_context** must be valid  
- **continuity** must be valid  

---

### Output Contract (CEx‑CCR TP)
CEx‑CCR outputs a TP with the same envelope structure, but with:

- **semantic_envelope.canonical_record**: canonicalized semantic structure  
- **semantic_envelope.interpretive_record**: preserved (read-only)  
- **semantic_envelope.extraction_tags**: preserved  
- **semantic_envelope.canonical_tags**: newly generated canonical feature tags  
- **epistemic_envelope.delta_h_percent**: may decrease if canonicalization reduces entropy  
- **provenance_envelope.routing_path**: append `cex-ccr`  
- **provenance_envelope.lineage_log**: append `cex-ccr`  
- **trace_envelope.tb_trace**: append `TB.cex_ccr_canonicalize`  

CEx‑CCR does **not** freeze meaning, modify identity, or alter semantic_core.

---

### Transfer Function (CEx‑CCR)
CEx‑CCR applies the following transformations:

1. **Canonicalization**
   - Convert interpretive_record → canonical_record  
   - Remove interpretive ambiguity  
   - Normalize semantic roles, relations, and structural features  
   - Ensure canonical_record is deterministic and replay-safe  
   - Generate canonical_tags describing canonical semantic features

2. **Semantic Stabilization**
   - Ensure canonical_record is stable across pipeline replays  
   - Guarantee structural invariants required by CEx‑PCK  
   - Validate canonical_record against context and identity geometry

3. **Epistemic Adjustment**
   - Reduce delta_h_percent if canonicalization reduces entropy  
   - Append entropy_history entry

4. **Provenance & Routing Updates**
   - Append `cex-ccr` to routing_path  
   - Append `cex-ccr` to lineage_log  
   - Update primitive IDs (sob/srob/cnob/smob/idob/mcb/rbu/tr/ctp/cex-ie/cex-ccr)

5. **Trace Update**
   - Append `TB.cex_ccr_canonicalize` to tb_trace  
   - Optionally append `OB.cex_ccr_pass` if defined in spec

6. **No Semantic or Identity Changes**
   - interpretive_record unchanged  
   - identity_envelope unchanged  
   - continuity unchanged  
   - basin geometry unchanged  
   - freeze state unchanged  
   - no SSR seeds created  
   - no boundary conditions applied

---

### Notes
- CEx‑CCR is the **second stage** of the CEx pipeline (IE → CCR → PCK).  
- CCR produces the **canonical semantic representation**, which is the stable foundation for PCK packing.  
- CCR is deterministic: same interpretive_record → same canonical_record → same output TP.  
- CCR never writes semantic_core, never freezes identity, and never alters context.

## CEx‑PCK — Context Extraction (Packing Engine)
**Spec:** 20.107.030_cex-pck_primitive.md  
**Pipeline Position:** After CEx‑CCR, before COB  
**Purpose:** Pack the canonical semantic representation into a stable, bounded, pipeline‑ready structure. PCK prepares the TP for downstream operational primitives (COB → CIL → CST → OuBA).

---

### Input Contract (from CEx‑CCR TP)
CEx‑PCK consumes the full TP envelope produced by CEx‑CCR:

- semantic_envelope  
- epistemic_envelope  
- identity_envelope  
- context_envelope  
- provenance_envelope  
- metadata_envelope  
- trace_envelope  

Required conditions:

- **semantic_envelope.canonical_record** must exist (CEx‑CCR creates it)  
- **semantic_envelope.canonical_tags** must exist  
- **interpretive_record** must be preserved (read-only)  
- **identity geometry** must be stable (PCK does not modify identity)  
- **context_envelope.current_context** must be valid  
- **continuity** must be valid  

---

### Output Contract (CEx‑PCK TP)
CEx‑PCK outputs a TP with the same envelope structure, but with:

- **semantic_envelope.packed_record**: packed semantic structure  
- **semantic_envelope.packed_tags**: tags describing packing features  
- **semantic_envelope.canonical_record**: preserved  
- **semantic_envelope.canonical_tags**: preserved  
- **semantic_envelope.interpretive_record**: preserved  
- **epistemic_envelope.delta_h_percent**: may decrease if packing reduces entropy  
- **provenance_envelope.routing_path**: append `cex-pck`  
- **provenance_envelope.lineage_log**: append `cex-pck`  
- **trace_envelope.tb_trace**: append `TB.cex_pck_pack`  

CEx‑PCK does **not** freeze meaning, modify identity, or alter semantic_core.

---

### Transfer Function (CEx‑PCK)
CEx‑PCK applies the following transformations:

1. **Packing**
   - Convert canonical_record → packed_record  
   - Compress canonical semantic structure into a bounded, pipeline‑ready format  
   - Generate packed_tags describing packing features  
   - Ensure packed_record is deterministic and replay-safe

2. **Semantic Consolidation**
   - Validate packed_record against canonical_record  
   - Ensure structural invariants required by COB  
   - Guarantee packed_record is stable across pipeline replays

3. **Epistemic Adjustment**
   - Reduce delta_h_percent if packing reduces entropy  
   - Append entropy_history entry

4. **Provenance & Routing Updates**
   - Append `cex-pck` to routing_path  
   - Append `cex-pck` to lineage_log  
   - Update primitive IDs (sob/srob/cnob/smob/idob/mcb/rbu/tr/ctp/cex-ie/cex-ccr/cex-pck)

5. **Trace Update**
   - Append `TB.cex_pck_pack` to tb_trace  
   - Optionally append `OB.cex_pck_pass` if defined in spec

6. **No Semantic or Identity Changes**
   - canonical_record unchanged  
   - interpretive_record unchanged  
   - identity_envelope unchanged  
   - continuity unchanged  
   - basin geometry unchanged  
   - freeze state unchanged  
   - no SSR seeds created  
   - no boundary conditions applied

---

### Notes
- CEx‑PCK is the **final stage** of the CEx pipeline (IE → CCR → PCK).  
- PCK produces the **packed semantic representation**, which is the structure consumed by COB.  
- PCK is deterministic: same canonical_record → same packed_record → same output TP.  
- PCK never writes semantic_core, never freezes identity, and never alters context.

## COB — Canonical Output Block
**Spec:** 20.32_cob_requirements.md  
**Pipeline Position:** After CEx‑PCK, before CIL  
**Purpose:** Convert the packed semantic representation into a stable, canonical output structure. COB prepares the TP for identity linkage (CIL) and final CST processing.

---

### Input Contract (from CEx‑PCK TP)
COB consumes the full TP envelope produced by CEx‑PCK:

- semantic_envelope  
- epistemic_envelope  
- identity_envelope  
- context_envelope  
- provenance_envelope  
- metadata_envelope  
- trace_envelope  

Required conditions:

- **semantic_envelope.packed_record** must exist (CEx‑PCK creates it)  
- **semantic_envelope.packed_tags** must exist  
- **canonical_record** and **interpretive_record** must be preserved  
- **identity geometry** must be stable (COB does not modify identity)  
- **context_envelope.current_context** must be valid  
- **continuity** must be valid  

---

### Output Contract (COB TP)
COB outputs a TP with the same envelope structure, but with:

- **semantic_envelope.canonical_output_record**: the final canonical semantic output  
- **semantic_envelope.canonical_output_tags**: tags describing canonical output features  
- **semantic_envelope.packed_record**: preserved  
- **semantic_envelope.packed_tags**: preserved  
- **semantic_envelope.canonical_record**: preserved  
- **semantic_envelope.interpretive_record**: preserved  
- **epistemic_envelope.delta_h_percent**: may decrease if canonical output reduces entropy  
- **provenance_envelope.routing_path**: append `cob`  
- **provenance_envelope.lineage_log**: append `cob`  
- **trace_envelope.tb_trace**: append `TB.cob_output`  

COB does **not** freeze meaning, modify identity, or alter semantic_core.

---

### Transfer Function (COB)
COB applies the following transformations:

1. **Canonical Output Construction**
   - Convert packed_record → canonical_output_record  
   - Ensure canonical_output_record is stable, bounded, and replay-safe  
   - Generate canonical_output_tags describing output features  
   - Validate canonical_output_record against canonical_record and packed_record

2. **Output Normalization**
   - Normalize canonical_output_record for downstream CIL consumption  
   - Guarantee structural invariants required by identity linkage  
   - Ensure output is deterministic across pipeline replays

3. **Epistemic Adjustment**
   - Reduce delta_h_percent if canonical output reduces entropy  
   - Append entropy_history entry

4. **Provenance & Routing Updates**
   - Append `cob` to routing_path  
   - Append `cob` to lineage_log  
   - Update primitive IDs (sob/srob/cnob/smob/idob/mcb/rbu/tr/ctp/cex-ie/cex-ccr/cex-pck/cob)

5. **Trace Update**
   - Append `TB.cob_output` to tb_trace  
   - Optionally append `OB.cob_pass` if defined in spec

6. **No Semantic or Identity Changes**
   - packed_record unchanged  
   - canonical_record unchanged  
   - interpretive_record unchanged  
   - identity_envelope unchanged  
   - continuity unchanged  
   - basin geometry unchanged  
   - freeze state unchanged  
   - no SSR seeds created  
   - no boundary conditions applied

---

### Notes
- COB is the **first post‑CEx primitive**, converting semantic extraction into canonical output.  
- COB is deterministic: same packed_record → same canonical_output_record → same output TP.  
- COB never writes semantic_core, never freezes identity, and never alters context.  
- COB prepares the TP for identity linkage (CIL) and final CST processing.

## CIL — Canonical Identity Linkage
**Spec:** 20.33_cil_requirements.md  
**Pipeline Position:** After COB, before CST  
**Purpose:** Link the canonical output record to the TP’s identity geometry. CIL ensures the TP’s semantic output is correctly attached to the identity basin, continuity surface, and geometric lineage. CIL is the identity‑binding primitive.

---

### Input Contract (from COB TP)
CIL consumes the full TP envelope produced by COB:

- semantic_envelope  
- epistemic_envelope  
- identity_envelope  
- context_envelope  
- provenance_envelope  
- metadata_envelope  
- trace_envelope  

Required conditions:

- **semantic_envelope.canonical_output_record** must exist (COB creates it)  
- **identity geometry** must be stable (CIL does not create or destroy identity)  
- **continuity** must be valid  
- **context_envelope.current_context** must be valid  
- **packed_record**, **canonical_record**, and **interpretive_record** must be preserved  

---

### Output Contract (CIL TP)
CIL outputs a TP with the same envelope structure, but with:

- **identity_envelope.linkage_record**: identity linkage structure  
- **identity_envelope.linkage_tags**: tags describing linkage features  
- **identity_envelope.basin_geometry**: updated if linkage requires geometric adjustment  
- **identity_envelope.continuity_surface**: updated if linkage requires continuity correction  
- **semantic_envelope.canonical_output_record**: preserved  
- **semantic_envelope.canonical_output_tags**: preserved  
- **epistemic_envelope.delta_h_percent**: may decrease if identity linkage reduces entropy  
- **provenance_envelope.routing_path**: append `cil`  
- **provenance_envelope.lineage_log**: append `cil`  
- **trace_envelope.tb_trace**: append `TB.cil_linkage`  

CIL does **not** freeze meaning, does not create SSR seeds, and does not write semantic_core.

---

### Transfer Function (CIL)
CIL applies the following transformations:

1. **Identity Linkage**
   - Convert canonical_output_record → linkage_record  
   - Bind semantic output to identity geometry  
   - Generate linkage_tags describing identity binding features  
   - Ensure linkage_record is deterministic and replay-safe

2. **Geometric Adjustment**
   - If semantic output requires identity basin correction → adjust basin_geometry  
   - If continuity requires smoothing → adjust continuity_surface  
   - All adjustments must preserve identity invariants

3. **Identity Stabilization**
   - Validate linkage_record against identity geometry  
   - Ensure linkage is stable across pipeline replays  
   - Guarantee linkage_record is compatible with CST processing

4. **Epistemic Adjustment**
   - Reduce delta_h_percent if identity linkage reduces entropy  
   - Append entropy_history entry

5. **Provenance & Routing Updates**
   - Append `cil` to routing_path  
   - Append `cil` to lineage_log  
   - Update primitive IDs (sob/srob/cnob/smob/idob/mcb/rbu/tr/ctp/cex-ie/cex-ccr/cex-pck/cob/cil)

6. **Trace Update**
   - Append `TB.cil_linkage` to tb_trace  
   - Optionally append `OB.cil_pass` if defined in spec

7. **No Semantic Changes**
   - canonical_output_record unchanged  
   - packed_record unchanged  
   - canonical_record unchanged  
   - interpretive_record unchanged  
   - semantic_core not written  
   - freeze state unchanged  
   - no SSR seeds created  
   - no boundary conditions applied

---

### Notes
- CIL is the **identity-binding primitive**: it attaches semantic output to identity geometry.  
- CIL is deterministic: same canonical_output_record → same linkage_record → same output TP.  
- CIL prepares the TP for CST, the final pipeline primitive before OuBA.  
- CIL never writes semantic_core and never freezes identity.

## CST‑Core — Stability Metric Engine
**Spec:** 20.32.010.010_cst-core.md  
**Pipeline Position:** After CIL, before CST‑MS and CST‑Mux  
**Purpose:** Compute structural stability metrics over identity layers, detect instability, and emit Freeze, Thaw, and Continuity‑restoration signals. CST‑Core is a deterministic metric generator; it never modifies identity topology.

---

### Input Contract (from CIL TP)
CST‑Core consumes the full TP envelope produced by CIL:

- identity_envelope (basin geometry, continuity surface, lineage, anchors)  
- semantic_envelope (canonical_output_record, linkage_record)  
- epistemic_envelope  
- context_envelope  
- provenance_envelope  
- metadata_envelope  
- trace_envelope  

Required conditions:

- **identity layers must be stable enough to snapshot**  
- **canonical_output_record** must exist (COB)  
- **linkage_record** must exist (CIL)  
- **TPSnS (OuBA committed snapshots)** may be referenced for topology stability 

---

### Output Contract (CST‑Core TP)
CST‑Core outputs a TP with the same envelope structure, but with:

- **stability signals**: Freeze, Thaw, Continuity‑restoration  
- **raw metric signals**: Drift, Oscillation, Ambiguity, Collapse  
- **metric histories**: 10‑turn sliding window  
- **provenance_envelope.routing_path**: append `cst-core`  
- **provenance_envelope.lineage_log**: append `cst-core`  
- **trace_envelope.tb_trace**: append `TB.cst_core_metrics`  

CST‑Core does **not** modify identity geometry, semantic content, or continuity surfaces.

---

### Transfer Function (CST‑Core)
CST‑Core applies the following transformations:

1. **Snapshot Extraction**
   - Extract deterministic structural snapshots for each identity layer every turn   
   - Include referent maps, temporal anchors, discourse anchors, lineage, register state, field‑importance weights   
   - Use no randomness or external state 

2. **Metric Computation (10‑turn window)**
   - Count structural features and compute normalized frequencies   
   - Maintain ordered histories for all tracked features   
   - Compute drift, oscillation, ambiguity, collapse using deterministic domain‑specific functions  
     - Drift detection and thresholds   
     - Oscillation detection and thresholds   
     - Ambiguity detection and thresholds   
     - Collapse detection and thresholds 

3. **Instability Signals**
   - Emit **Freeze** when combined instability exceeds freeze threshold   
   - Emit **Thaw** when instability falls below recovery threshold   
   - Emit **Continuity‑restoration** when continuity exceeds recovery threshold   
   - Freeze halts snapshot and metric updates for frozen layers (local freeze)   
   - Thaw resumes updates (local thaw) 

4. **Determinism & Replay Safety**
   - All metrics computed as pure functions of snapshots, OuBA cues, previous CST signals, and deterministic history   
   - Threshold updates must be deterministic and monotonic   
   - All signals emitted in fixed deterministic order   
   - Log all metric values required for replay consistency 

5. **Signal Routing**
   - Freeze, Thaw, Continuity‑restoration → **COB** and **CST‑Mux**   
   - Drift, Oscillation, Ambiguity, Collapse → **CST‑MS** and **CST‑Mux** only (never COB)   
   - All signals must be available to CST‑Mux for Unified Stability Packet and TP replay   
   - CST‑Core must not accept commands from CST‑MS (one‑way flow)   
   - CST‑Core has **no structural authority** (cannot create/split/merge identity layers) 

---

### Notes
- CST‑Core is **stateful** (metric histories) but **not a state machine**   
- CST‑Core is fully deterministic and replay‑safe   
- CST‑Core is the stability backbone of the pipeline; CST‑MS and CST‑Mux depend on its signals.  
- CST‑Core never modifies identity topology; only CST‑MS has structural authority.

## CST‑MS — Metric Synthesis Module
**Spec:** 20.32.010.020_cst-ms.md  
**Pipeline Position:** After CST‑Core, before CST‑Mux  
**Purpose:** Synthesize raw CST‑Core stability metrics into deterministic stability/instability signals and issue structural identity‑layer commands to COB. CST‑MS is the *command authority* for identity‑layer structural transitions.

---

### Input Contract (from CST‑Core TP)
CST‑MS consumes:

- Raw CST‑Core metrics: drift, oscillation, ambiguity, collapse, continuity, freeze, thaw, register stability, field‑importance stability   
- Layer‑specific thresholds for all metrics   
- Metric histories for all raw metrics   
- Freeze, thaw, continuity‑restoration signals from CST‑Core   
- Committed identity‑layer snapshots from OuBA (TPSnS) as stable topology reference   
- Optional restricted diagnostic view of COB identity‑layer state (sync‑mismatch detection only)   

CST‑MS does **not** read COB internal state for command decisions. Commands must be driven exclusively by CST‑Core metrics + thresholds + OuBA snapshots. 

---

### Output Contract (CST‑MS TP)
CST‑MS produces:

- Stability summary (per layer)   
- Instability summary (per layer)   
- Collapse‑risk values (per layer)   
- Freeze‑risk values (per layer)   
- Thaw‑readiness values (per layer)   
- Ambiguity, drift, oscillation summaries   
- Structural commands to COB (freeze, thaw, collapse‑recovery, create‑layer, split, merge)   
- Sync‑mismatch diagnostic signals to CST‑Mux   

CST‑MS updates:

- provenance_envelope.routing_path → append `cst-ms`  
- provenance_envelope.lineage_log → append `cst-ms`  
- trace_envelope.tb_trace → append `TB.cst_ms_synthesis`  

---

### Transfer Function (CST‑MS)

1. **Metric Normalization**  
   - Normalize each raw metric to \([0,1]\) using deterministic layer‑specific maxima   
   - Replay‑safe, no randomness   

2. **Metric Weighting**  
   - Apply deterministic layer‑specific weights to normalized metrics   
   - Weights must be monotonic and replay‑safe   

3. **Stability Synthesis**  
   - Compute stability as deterministic function of weighted drift, oscillation, ambiguity, collapse, continuity   
   - Apply synthesis weights per layer   
   - Clip stability to \([0,1]\)   

4. **Instability Synthesis**  
   - Instability = complement of stability   
   - Clip to \([0,1]\)   

5. **Collapse Risk**  
   - Deterministic function of instability + weighted collapse metrics   
   - Clip to \([0,1]\)   

6. **Freeze Risk**  
   - Deterministic function of collapse risk + weighted ambiguity   
   - Clip to \([0,1]\)   

7. **Thaw Readiness**  
   - Deterministic function of stability + weighted continuity   
   - Clip to \([0,1]\)   

8. **Ambiguity / Drift / Oscillation Summaries**  
   - Deterministic summaries from weighted metrics     

9. **Structural Command Authority (to COB)**  
   CST‑MS is the **sole module** authorized to issue:  
   - freeze  
   - thaw  
   - collapse‑recovery  
   - create‑identity‑layer  
   - split  
   - merge  
     

   Commands must be:  
   - deterministic  
   - replay‑safe  
   - logged with full replay information  
     

10. **Synchronization Diagnostics**  
   - Detect mismatches between commanded transitions and COB’s realized topology  
   - Report mismatch to CST‑Mux (diagnostic only)   
   - MUST NOT issue additional commands in response   

11. **Determinism & Replay Safety**  
   - Pure functional synthesis, no randomness, no external state, no wall‑clock time   
   - Threshold updates must be deterministic and monotonic   
   - Identical inputs → identical outputs under replay   

---

### Notes
- CST‑MS is the **commanding authority** for identity‑layer structural transitions.  
- CST‑Core computes raw metrics; CST‑MS interprets them.  
- CST‑MS outputs feed CST‑Mux, COB, and CIL.  
- CST‑MS is fully deterministic and replay‑safe.

## CST‑Mux — Stability Multiplexer
**Spec:** 20.32.010.030_cst-mux.md  
**Pipeline Position:** After CST‑Core and CST‑MS, before OuBA  
**Purpose:** Collect, align, and multiplex all CST‑Core and CST‑MS stability signals into a single, replay‑safe Unified Stability Packet (USP) attached to the TP. CST‑Mux does not compute metrics or issue structural commands; it is the *stability signal router and packer*.

---

### Input Contract (from CST‑Core + CST‑MS TP)
CST‑Mux consumes:

- All CST‑Core outputs:  
  - raw metrics (drift, oscillation, ambiguity, collapse, continuity)  
  - Freeze, Thaw, Continuity‑restoration signals  
  - metric histories (10‑turn window)  
- All CST‑MS outputs:  
  - stability, instability, collapse‑risk, freeze‑risk, thaw‑readiness  
  - ambiguity/drift/oscillation summaries  
  - structural command logs (already sent to COB)  
  - sync‑mismatch diagnostics  
- TP envelopes (identity, semantic, epistemic, context, provenance, metadata, trace)  

CST‑Mux must see a **consistent pair** of CST‑Core + CST‑MS outputs for each TP turn.

---

### Output Contract (CST‑Mux TP)
CST‑Mux outputs a TP with the same envelope structure, but with:

- **stability_envelope.unified_stability_packet (USP)**:  
  - packed CST‑Core metrics  
  - packed CST‑MS synthesized values  
  - packed structural command log references  
  - packed sync‑mismatch diagnostics  
  - packed metric histories (or references)  
- **stability_envelope.usp_tags**: tags describing USP contents  
- **provenance_envelope.routing_path**: append `cst-mux`  
- **provenance_envelope.lineage_log**: append `cst-mux`  
- **trace_envelope.tb_trace**: append `TB.cst_mux_unified_packet`  

CST‑Mux does **not** modify identity geometry, semantic content, continuity surfaces, or thresholds.

---

### Transfer Function (CST‑Mux)

1. **Signal Collection**
   - Collect all CST‑Core and CST‑MS outputs for the current TP turn  
   - Validate that both modules have produced a complete, consistent set of signals  

2. **Alignment & Normalization**
   - Align CST‑Core metrics with CST‑MS synthesized values per identity layer  
   - Normalize representation formats (e.g., fixed ordering, fixed field names)  
   - Ensure replay‑safe, deterministic ordering of all signals  

3. **Unified Stability Packet (USP) Construction**
   - Pack aligned signals into unified_stability_packet  
   - Include:  
     - raw metrics  
     - synthesized metrics  
     - structural command references (not commands themselves)  
     - sync‑mismatch diagnostics  
     - metric history references  
   - Generate usp_tags describing packet contents and layer coverage  

4. **Replay & Trace Integration**
   - Ensure USP is sufficient to replay CST behavior for the TP turn  
   - Append `TB.cst_mux_unified_packet` to tb_trace  
   - Log USP references in provenance for replay tools  

5. **Routing**
   - Make USP available to:  
     - OuBA (for TP snapshot and replay)  
     - any downstream analysis tools  
   - CST‑Mux must not send commands to COB or CIL  

6. **Determinism & Safety**
   - No randomness, no external state, no wall‑clock time  
   - Identical CST‑Core + CST‑MS inputs → identical USP under replay  
   - CST‑Mux must never alter identity topology or semantic content  

---

### Notes
- CST‑Core computes metrics; CST‑MS synthesizes and commands; CST‑Mux **packs and routes**.  
- CST‑Mux is the final CST primitive before OuBA.  
- USP is the stability “black box” for TP replay and OuBA snapshotting.  
- CST‑Mux is deterministic and replay‑safe, with no structural authority.


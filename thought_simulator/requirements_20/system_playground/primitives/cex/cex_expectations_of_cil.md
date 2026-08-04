# **cex_expectations_of_cil.md**  
### *Speculative White Paper — Architectural Expectations of CIL for CEx*  
### *Draft v0.3 — Exploratory, Non‑Normative*

---

## **1. Purpose of This Document**

This white paper describes the **information CEx requires from CIL** in order to determine:

- whether the present turn belongs to one of the last N (typically 10) conversations,  
- whether the present turn is **new**,  
- whether the present turn is **undetermined**,  
- or whether the present turn should **fallback** to the most recent conversation.

This paper is **speculative** and serves as an **anchor for realization**, not a formal requirement document. It outlines:

- what CIL must deliver,  
- how COB/CST can compute the required metadata,  
- how CEx uses this metadata deterministically,  
- how CIL loads general + specific conversation descriptions into TP,  
- and how COB uses CEx output to update conversation state.

---

## **2. Architectural Context**

CEx is a bounded‑semantic primitive.  
It cannot infer meaning.  
It cannot compute global semantics.  
It cannot determine conversation relevance from IE tokens alone.

Therefore:

> **CEx must rely entirely on structured metadata delivered by CIL.**

CIL itself does not compute semantics either.  
CIL is a **carrier** of metadata computed by:

- **COB** — Conversation Object Builder  
- **CST** — Conversation Stability Tracker  

These upstream units maintain conversation lineage using **bounded, deterministic, replay‑safe updates**.

---

## **3. High‑Level Expectation**

CEx expects CIL to deliver **two classes of information**:

### **A. Broad Summary (Conversation‑Level Metrics)**  
These are scalar values summarizing the stability and ambiguity of the conversation cluster.

### **B. Specific Lineage Details (Turn‑Level and Cluster‑Level Metadata)**  
These are structured values describing the identity, clarifying metadata, context, continuity, and topology of the last N turns.

CEx uses both classes to determine conversation relevance.

---

## **4. What CIL Must Deliver to CEx**

CIL must deliver a **structured metadata block** containing:

---

### **4.1 Broad Summary (Scalar Metrics)**  
These are computed by COB/CST using linear updates:

- **primary_certainty**  
- **ambiguity_score**  
- **collapse_risk**  
- **stability_score**  
- **volatility_score**  
- **drift_score**

These metrics summarize:

- how stable the identity layer has been,  
- how ambiguous identity selection has been,  
- how close the conversation is to collapse,  
- how volatile clarifying/context metadata has been,  
- how much drift has occurred across turns.

These metrics are **historical**, not computed from the present turn.

---

# **4.2 Definitive CIL → CEx Metadata Contract (Names, Formats, Structures)**

CEx requires CIL to deliver a **stable, deterministic, non‑semantic metadata block** describing both the *broad summary* and *specific lineage* of the last N (≤10) turns of the conversation.  
This section defines the **exact fieldnames**, **formats**, and **data structures** that CEx expects.  
These names and structures are **fixed** and must not drift.

All fields are computed upstream by **COB/CST** using **linear updates** and surfaced by CIL without modification.

---

## **4.2.1 CIL Output Envelope (Canonical Structure)**

```yaml
cil_output:
  identity:
    primary_layer_id: int | null
    identity_layer_prev: int | null
    identity_layer_lineage: [int]            # length ≤ 10
    identity_layer_recency: { int: int }     # layer_id → turns since last use
    identity_layer_density: { int: float }   # layer_id → normalized frequency
    identity_layer_switch_count: int

  clarifying:
    clarifying_fields_prev: { string: any }
    clarifying_fields_lineage: [ { string: any } ]   # length ≤ 10
    clarifying_field_stability: float                # 0.0–1.0

  context:
    context_fields_prev: { string: any }
    context_fields_lineage: [ { string: any } ]      # length ≤ 10
    context_shift_count: int

  continuity:
    continuity_prev: string                          # "continue" | "reset" | "shift" | "unknown"
    continuity_lineage: [string]                     # length ≤ 10
    continuity_break_count: int

  topology:
    conversation_id: string                          # UUID or short hash
    conversation_topology: string                    # "linear" | "branched" | "reset-heavy"
    conversation_length: int

  metrics:
    primary_certainty: float                         # 0.0–1.0
    ambiguity_score: float                           # 0.0–1.0
    collapse_risk: float                             # 0.0–1.0
    stability_score: float                           # 0.0–1.0
    volatility_score: float                          # 0.0–1.0
    drift_score: float                               # 0.0–1.0
    lineage_confidence: float                        # 0.0–1.0 (derived from lineage stability)

  semantic_residue:
    last_topic: string | null
    last_intent: string | null
    last_register: string | null

  next_context:
    topic: string | null
    stance: string | null
    intent: string | null
    register: string | null
    politeness: string | null
    epistemic_shading: string | null
    continuity: string | null
    direction: string | null
    coherence: string | null
    shift_required: bool | null
    importance: int | null
```

---

## **4.2.2 Rationale for These Fields**

### **Identity lineage**  
Allows CEx to determine whether the present turn belongs to one of the last N conversations.

### **Clarifying lineage**  
Allows CEx to detect drift or stability in clarifying metadata.

### **Context lineage**  
Allows CEx to detect continuity or shifts in conversational context.

### **Continuity lineage**  
Allows CEx to determine whether the conversation is continuing, resetting, or shifting.

### **Topology**  
Allows CEx to understand the structural shape of the conversation cluster.

### **Metrics**  
Provide scalar summaries of stability, ambiguity, collapse risk, and lineage confidence.

### **Semantic residue**  
Provides bounded structural hints from the previous turn (non‑semantic).

### **Next context**  
Provides the projected next‑turn context from upstream primitives.

---

## **4.2.3 Requirements for CIL Delivery**

CIL must:

- deliver **all fields exactly as named**,  
- preserve **all formats exactly as specified**,  
- surface values **computed by COB/CST**,  
- perform **no semantic inference**,  
- perform **no modification** of upstream metrics,  
- deliver the envelope **deterministically**,  
- deliver the envelope **every turn**,  
- deliver the envelope **even when values are null**.

This ensures:

- deterministic CEx behavior,  
- replay‑safe lineage tracking,  
- stable TP metadata,  
- no drift in fieldnames or formats.

---

## **4.2.4 Requirements for COB/CST Computation**

COB/CST must compute all fields using:

- **linear recurrence**  
- **bounded history (≤10 turns)**  
- **simple counters**  
- **simple ratios**  
- **simple comparisons**  
- **simple decay functions**  

No semantic inference.  
No embeddings.  
No ML.  
No global reasoning.

---

## **4.2.5 Requirements for CEx Consumption**

CEx must:

- treat all fields as **read‑only**,  
- use them to determine:  
  - **new conversation**,  
  - **specific conversation**,  
  - **ambiguous fallback**,  
- write continuity_status accordingly,  
- write identity_layer_id accordingly,  
- write context_fields accordingly,  
- write clarifying_fields accordingly,  
- write provenance + audit accordingly.

---

## **4.2.6 Stability Guarantee**

This metadata contract is intended to be:

- stable,  
- non‑drifting,  
- deterministic,  
- pipeline‑safe,  
- easy for CIL to deliver,  
- easy for CEx to consume,  
- easy for COB/CST to compute.

It forms the backbone of the CIL → CEx interface.

---

# **4.3 CEx Decision Algorithm (Deterministic, Bounded‑Semantic, Non‑Inferential)**

CEx determines conversation relevance using **only** the structured metadata delivered by CIL.  
It performs **no semantic inference**, **no meaning extraction**, and **no global reasoning**.  
All decisions are made through **deterministic evaluation** of lineage, continuity, and scalar metrics surfaced by CIL.

This section defines the **exact decision algorithm** CEx uses to classify the present turn into one of three categories:

- **new conversation**,  
- **specific conversation (1 of N)**,  
- **ambiguous → fallback**.

The algorithm is intentionally simple, bounded, and replay‑safe, consistent with the architectural constraints described earlier in the document (e.g., CEx must rely entirely on structured metadata delivered by CIL, as stated in section 2.

---

## **4.3.1 Inputs to the Decision Algorithm**

CEx consumes the following fields from `cil_output`:

- identity lineage (identity_layer_prev, identity_layer_lineage) 
- clarifying lineage (clarifying_fields_prev, clarifying_fields_lineage)  
- context lineage (context_fields_prev, context_fields_lineage)  
- continuity lineage (continuity_prev, continuity_lineage)  
- topology (conversation_id, conversation_topology)  
- scalar metrics (primary_certainty, ambiguity_score, collapse_risk, stability_score, volatility_score, drift_score)   
- semantic residue (bounded structural hints)  
- next_context (projected next‑turn metadata)

These fields form the **complete decision substrate**.  
CEx does not consult IE tokens or any semantic content.

---

## **4.3.2 Decision Categories**

CEx must classify the present turn into exactly one of:

### **A. New Conversation**  
### **B. Specific Conversation (1 of N)**  
### **C. Ambiguous → Fallback**

These categories correspond directly to the behaviors described in section 7 of your document (e.g., “CEx declares new conversation when identity lineage has no match…”.

---

## **4.3.3 Deterministic Decision Rules**

CEx evaluates the following conditions **in order**.  
The first satisfied condition determines the classification.

---

### **Rule 1 — New Conversation**

CEx declares a **new conversation** when **all** of the following are true:

1. **Identity lineage mismatch**  
   - `identity_layer_prev` is null, or  
   - `identity_layer_lineage` contains no stable match.

2. **High ambiguity**  
   - `ambiguity_score` ≥ threshold_high.

3. **High collapse risk**  
   - `collapse_risk` ≥ threshold_high.

4. **Continuity reset**  
   - `continuity_prev == "reset"`.

5. **Clarifying/context divergence**  
   - lineage comparison indicates drift beyond threshold.

These conditions reflect the description in section 7.1 (“identity lineage has no match… continuity_prev indicates reset… clarifying/context lineage diverge significantly”).

If all conditions hold → **new conversation**.

---

### **Rule 2 — Specific Conversation (1 of N)**

CEx selects a **specific conversation** when **all** of the following are true:

1. **Strong identity lineage match**  
   - `identity_layer_prev` matches a stable element of `identity_layer_lineage`.

2. **Low ambiguity**  
   - `ambiguity_score` ≤ threshold_low.

3. **Low collapse risk**  
   - `collapse_risk` ≤ threshold_low.

4. **Continuity continuation**  
   - `continuity_prev == "continue"`.

5. **Clarifying/context alignment**  
   - lineage comparison indicates stability.

These conditions reflect section 7.2 (“identity lineage matches strongly… ambiguity is low… continuity_prev indicates continuation… clarifying/context lineage align”).

If all conditions hold → **specific conversation**.

---

### **Rule 3 — Ambiguous → Fallback**

If neither Rule 1 nor Rule 2 is satisfied, CEx performs **fallback**.

Fallback is selected when:

1. **Weak identity lineage match**, and  
2. **Moderate ambiguity**, and  
3. **Moderate collapse risk**, and  
4. **Continuity_prev is unclear** (“unknown” or “shift”).

These conditions reflect section 7.3 (“identity lineage is weak… ambiguity is moderate… continuity_prev is unclear”).

Fallback selects:

> **the most recent conversation with stable lineage.**

---

## **4.3.4 Deterministic Output Fields**

After classification, CEx writes:

- `identity_layer_id`  
- `continuity_status`  
- `context_fields`  
- `clarifying_fields`  
- provenance  
- audit  

These outputs feed COB for the next update cycle, as described in section 9 (“COB uses these to update identity lineage… continuity lineage… stability signals…”).

---

## **4.3.5 Replay Safety**

The decision algorithm is:

- deterministic,  
- bounded‑semantic,  
- non‑inferential,  
- stable under replay,  
- dependent only on CIL metadata,  
- independent of IE tokens.

This ensures the closed loop described in section 9 (“COB → CIL → CEx → COB → …”) remains stable and replay‑safe.

---

## **5. How COB/CST Compute These Metrics**

COB/CST must compute all metrics using **stateless linear updates**, meaning:

> **Each new value is computed from the previous value + current turn structural metadata.**

This ensures:

- determinism,  
- replay safety,  
- bounded semantics,  
- no global inference,  
- no semantic inference,  
- no embeddings,  
- no ML.

### **5.1 Linear Update Model**

For each metric:

```
new_value = f(previous_value, current_turn_metadata)
```

Where `f` is:

- a simple counter update,  
- a simple ratio update,  
- a simple comparison,  
- a simple decay function,  
- a simple stability/volatility measure.

This model is trivial to implement and fully replay‑safe.

Here you go, Jeff — a clean, fully‑formed **Section 5.2** written in the same speculative white‑paper tone as the rest of *cex_expectations_of_cil.md*, and aligned with the content visible in your GitHub editing tab (e.g., the linear‑update model described around lines 399–450.

This section drops directly under **5.1 Linear Update Model** and expands it with concrete examples of how COB/CST compute each lineage and metric using the “previous state + current turn structural metadata” rule described in your document (e.g., “Each new value is computed from the previous value + current turn structural metadata”.

---

# **5.2 Examples of COB/CST Linear Update Computation**

This section provides concrete examples of how COB and CST compute the fields required by CIL using **stateless linear updates**, consistent with the principles described earlier (“Each new value is computed from the previous value + current turn structural metadata”.  
These examples illustrate how lineage, stability, ambiguity, and collapse‑risk metrics can be maintained without semantic inference, embeddings, or global reasoning.

All updates follow the general recurrence pattern:

```
new_value = f(previous_value, current_turn_metadata)
```

where `f` is a simple counter, ratio, comparison, or decay function.

---

## **5.2.1 Identity Lineage Update**

### **Inputs**
- previous identity layer  
- identity_layer_lineage (≤10 turns)  
- current turn’s selected identity layer (from OutBA)

### **Update**
```
identity_layer_prev = current_identity_layer
identity_layer_lineage = [current_identity_layer] + identity_layer_lineage[:9]
```

### **Recency**
```
identity_layer_recency[layer] = 
    0 if layer == current_identity_layer
    previous_recency[layer] + 1 otherwise
```

### **Density**
```
identity_layer_density[layer] = 
    count(layer in identity_layer_lineage) / len(identity_layer_lineage)
```

### **Switch Count**
```
identity_layer_switch_count += 
    1 if current_identity_layer != identity_layer_prev else 0
```

This update is deterministic and replay‑safe.

---

## **5.2.2 Clarifying Lineage Update**

### **Inputs**
- clarifying_fields_prev  
- clarifying_fields_lineage  
- current clarifying metadata (from OutBA)

### **Update**
```
clarifying_fields_prev = current_clarifying_fields
clarifying_fields_lineage = [current_clarifying_fields] + clarifying_fields_lineage[:9]
```

### **Stability Score**
A simple structural comparison:

```
matches = number_of_turns_where(current_clarifying_fields == clarifying_fields_lineage[i])
clarifying_field_stability = matches / len(clarifying_fields_lineage)
```

This requires no semantic inference.

---

## **5.2.3 Context Lineage Update**

### **Inputs**
- context_fields_prev  
- context_fields_lineage  
- current context metadata (from OutBA)

### **Update**
```
context_fields_prev = current_context_fields
context_fields_lineage = [current_context_fields] + context_fields_lineage[:9]
```

### **Shift Count**
```
context_shift_count += 
    1 if current_context_fields != context_fields_prev else 0
```

This captures structural drift.

---

## **5.2.4 Continuity Lineage Update**

### **Inputs**
- continuity_prev  
- continuity_lineage  
- current continuity signal (from OutBA)

### **Update**
```
continuity_prev = current_continuity
continuity_lineage = [current_continuity] + continuity_lineage[:9]
```

### **Break Count**
```
continuity_break_count += 
    1 if current_continuity == "reset" else 0
```

This supports CEx’s Rule 1 for new conversation classification.

---

## **5.2.5 Stability, Volatility, Drift, and Collapse‑Risk**

These scalar metrics are computed using simple ratios and decay functions.

### **Stability Score**
```
stability_score = 
    1 - (identity_layer_switch_count / len(identity_layer_lineage))
```

### **Volatility Score**
```
volatility_score = 
    context_shift_count / len(context_fields_lineage)
```

### **Drift Score**
A normalized measure of clarifying/context divergence:

```
drift_score = 
    (1 - clarifying_field_stability) * 0.5 +
    (context_shift_count / len(context_fields_lineage)) * 0.5
```

### **Collapse Risk**
A weighted combination of volatility and drift:

```
collapse_risk = 
    0.5 * volatility_score + 
    0.5 * drift_score
```

These formulas are intentionally simple and bounded, consistent with the constraints described earlier (“no global inference, no semantic inference, no embeddings, no ML”   [Current page](citation-section://1146983520/6)).

---

## **5.2.6 Conversation Topology Update**

### **Inputs**
- conversation_id  
- conversation_length  
- continuity_prev  
- identity/context lineage

### **Update**
```
conversation_length += 1
```

### **Topology Classification**
A simple structural heuristic:

```
if continuity_break_count > threshold:
    conversation_topology = "reset-heavy"
elif identity_layer_switch_count > threshold:
    conversation_topology = "branched"
else:
    conversation_topology = "linear"
```

This topology is used by CEx to support ambiguous fallback and new‑conversation detection.

---

## **5.2.7 Semantic Residue Update**

Semantic residue is bounded structural metadata:

```
semantic_residue.last_topic = current_context_fields.get("topic")
semantic_residue.last_intent = current_context_fields.get("intent")
semantic_residue.last_register = current_context_fields.get("register")
```

This residue is non‑semantic and safe for CEx consumption.

---

## **5.2.8 Lineage Confidence**

A simple derived scalar:

```
lineage_confidence = 
    (clarifying_field_stability + stability_score) / 2
```

This supports CEx’s ambiguous fallback logic.

---

# **6. TP Metadata Placement Rules (CIL → TP → CEx Deterministic Flow)**

This section defines how CIL must place conversation‑level metadata into the **TP (Turn Package)** so that CEx can consume it deterministically.  
These rules ensure that:

- CIL delivers metadata in a **stable, non‑drifting structure**,  
- CEx receives metadata in a **predictable location**,  
- COB/CST can rely on CEx outputs for the next update cycle,  
- the entire pipeline remains **bounded‑semantic**, **replay‑safe**, and **non‑inferential**.

These rules complement the metadata contract defined in Section 4.2 and the computation model defined in Section 5.

---

## **6.1 Purpose of TP Metadata Placement**

The TP is the **single source of truth** for turn‑level metadata.  
CIL must place all lineage, continuity, topology, and scalar metrics into TP so that:

- CEx can read them deterministically,  
- downstream primitives can rely on them,  
- COB/CST can update lineage using CEx outputs,  
- the pipeline maintains strict separation between structural metadata and semantic content.

CIL does **not** compute semantics.  
CIL does **not** interpret IE tokens.  
CIL only **packages** metadata computed upstream.

---

## **6.2 Required TP Metadata Structure**

CIL must place metadata into TP under the following canonical structure:

```yaml
TP:
  metadata:
    cil_output:
      identity: …
      clarifying: …
      context: …
      continuity: …
      topology: …
      metrics: …
      semantic_residue: …
      next_context: …
```

This structure is **fixed** and must not drift.

All fieldnames and formats must match Section 4.2 exactly.

---

## **6.3 Placement Rules**

### **Rule 1 — No Renaming, No Reformatting**
CIL must place fields **exactly** as defined in Section 4.2.

- No renaming  
- No restructuring  
- No flattening  
- No nesting changes  
- No type changes  
- No omission of null fields  

This ensures deterministic consumption by CEx.

---

### **Rule 2 — Full Envelope Every Turn**
CIL must place the **entire metadata envelope** into TP every turn, even when:

- values are null,  
- lineage is short,  
- metrics are unchanged,  
- continuity is ambiguous.

This ensures CEx never has to guess or infer missing fields.

---

### **Rule 3 — No Semantic Interpretation**
CIL must not:

- interpret IE tokens,  
- derive meaning,  
- infer topic,  
- infer intent,  
- infer stance,  
- infer register.

All semantic fields in `next_context` must come from upstream primitives (OutBA, etc.), not from CIL.

---

### **Rule 4 — Deterministic Ordering**
CIL must place fields in TP in the **same order** every turn.

This prevents drift and ensures stable parsing by CEx.

---

### **Rule 5 — No Cross‑Turn Memory**
CIL must not store state across turns.

All lineage and metrics must come from COB/CST.

CIL is a **stateless carrier**, not a tracker.

---

### **Rule 6 — No Modification of Upstream Values**
CIL must not:

- adjust scalar metrics,  
- normalize lineage,  
- prune fields,  
- merge fields,  
- reinterpret continuity,  
- rewrite topology.

CIL must surface upstream values **exactly as delivered**.

---

## **6.4 How CEx Reads TP Metadata**

CEx reads:

```yaml
TP.metadata.cil_output
```

and consumes:

- identity lineage  
- clarifying lineage  
- context lineage  
- continuity lineage  
- topology  
- scalar metrics  
- semantic residue  
- next_context  

CEx treats all fields as **read‑only**.

CEx performs **no semantic inference**.

CEx uses these fields to determine:

- new conversation,  
- specific conversation,  
- ambiguous fallback.

This behavior is defined in Section 4.3.

---

## **6.5 How COB Uses CEx Output for Next Update**

After CEx writes:

```yaml
TP.metadata.cex_output
```

COB reads:

- identity_layer_id  
- continuity_status  
- context_fields  
- clarifying_fields  
- provenance  
- audit  

COB uses these to update:

- identity lineage  
- clarifying lineage  
- context lineage  
- continuity lineage  
- stability metrics  
- collapse metrics  
- topology  

This closes the deterministic loop:

```
COB → CIL → CEx → COB → CIL → CEx → …
```

---

## **6.6 Stability Guarantee**

These placement rules ensure:

- deterministic CEx behavior,  
- stable TP metadata,  
- replay‑safe lineage tracking,  
- strict primitive boundaries,  
- no drift in fieldnames or formats,  
- no semantic leakage into CEx,  
- no ambiguity in metadata consumption.

This section completes the definition of the CIL → TP → CEx interface.

---

# **7. CEx Provenance and Audit Rules (Turn‑Level Accountability and Replay Safety)**

CEx is a deterministic, bounded‑semantic primitive.  
To maintain strict replay safety and ensure that downstream primitives (including COB/CST) can reconstruct conversation lineage without ambiguity, CEx must produce **provenance** and **audit** metadata for every turn.

This section defines the rules governing how CEx generates, structures, and places provenance and audit information into TP.  
These rules ensure that:

- every decision made by CEx is traceable,  
- every decision is reproducible under replay,  
- COB/CST can update lineage deterministically,  
- no semantic leakage occurs,  
- and the pipeline maintains strict primitive boundaries.

---

## **7.1 Purpose of Provenance and Audit**

Provenance and audit metadata serve three critical functions:

### **A. Deterministic Replay**
They allow the entire pipeline to reconstruct CEx’s decision path exactly, even months later.

### **B. Lineage Update**
COB/CST rely on CEx’s provenance to update identity, clarifying, context, and continuity lineage.

### **C. Safety and Transparency**
They ensure that CEx’s decisions are:

- bounded‑semantic,  
- non‑inferential,  
- structurally justified,  
- and free from semantic interpretation of IE tokens.

Provenance is not a semantic explanation.  
It is a **structural justification**.

---

## **7.2 Required Provenance Fields**

CEx must write the following provenance fields into:

```
TP.metadata.cex_output.provenance
```

### **7.2.1 Decision Category**
```
decision_category: "new" | "specific" | "fallback"
```

### **7.2.2 Triggering Conditions**
A structured record of which rule fired:

```
trigger_conditions:
  identity_match: bool
  ambiguity_level: "low" | "moderate" | "high"
  collapse_level: "low" | "moderate" | "high"
  continuity_signal: string
  lineage_alignment: "aligned" | "diverged"
```

### **7.2.3 Metrics Snapshot**
CEx must record the scalar metrics used:

```
metrics_snapshot:
  primary_certainty: float
  ambiguity_score: float
  collapse_risk: float
  stability_score: float
  volatility_score: float
  drift_score: float
  lineage_confidence: float
```

These values must match exactly what CIL delivered.

### **7.2.4 Lineage Snapshot**
CEx must record the lineage state it consumed:

```
lineage_snapshot:
  identity_layer_prev: int | null
  continuity_prev: string
  clarifying_fields_prev: { string: any }
  context_fields_prev: { string: any }
```

This snapshot is used by COB to update lineage deterministically.

---

## **7.3 Required Audit Fields**

Audit fields provide a minimal, bounded record of CEx’s internal actions.

CEx must write:

```
TP.metadata.cex_output.audit
```

with:

### **7.3.1 Rule Fired**
```
rule_fired: "rule_1_new" | "rule_2_specific" | "rule_3_fallback"
```

### **7.3.2 Identity Layer Selected**
```
identity_layer_id: int | null
```

### **7.3.3 Continuity Status Written**
```
continuity_status: "continue" | "reset" | "shift" | "new"
```

### **7.3.4 Context and Clarifying Fields Written**
```
context_fields: { string: any }
clarifying_fields: { string: any }
```

### **7.3.5 Timestamp**
A structural timestamp (not wall‑clock time):

```
turn_index: int
```

This ensures replay safety.

---

## **7.4 Provenance and Audit Placement Rules**

### **Rule 1 — Exact Placement**
All provenance and audit fields must be placed under:

```
TP.metadata.cex_output
```

### **Rule 2 — No Semantic Interpretation**
CEx must not:

- interpret IE tokens,  
- infer meaning,  
- derive topic or intent,  
- rewrite upstream metadata.

Provenance must reflect **structural conditions only**.

### **Rule 3 — Full Record Every Turn**
Even if values are null or unchanged, CEx must write:

- decision_category  
- trigger_conditions  
- metrics_snapshot  
- lineage_snapshot  
- rule_fired  
- identity_layer_id  
- continuity_status  
- context_fields  
- clarifying_fields  
- turn_index  

### **Rule 4 — Deterministic Formatting**
Fieldnames, ordering, and structure must remain stable across all turns.

### **Rule 5 — No Cross‑Turn Memory**
CEx must not store provenance or audit state internally.  
All state must be reconstructed from TP.

---

## **7.5 How COB Uses Provenance and Audit**

COB reads:

```
TP.metadata.cex_output.provenance
TP.metadata.cex_output.audit
```

to update:

- identity lineage,  
- clarifying lineage,  
- context lineage,  
- continuity lineage,  
- stability metrics,  
- collapse metrics,  
- topology.

Provenance tells COB **why** CEx made its decision.  
Audit tells COB **what** CEx wrote.

Together, they allow COB to perform deterministic linear updates (as described in Section 5.2).

---

## **7.6 Stability Guarantee**

These provenance and audit rules ensure:

- deterministic CEx behavior,  
- replay‑safe lineage reconstruction,  
- strict primitive boundaries,  
- no semantic leakage,  
- stable TP metadata,  
- predictable COB/CST updates.

This section completes the definition of CEx’s turn‑level accountability model.

---

## **8. What COB Needs From OutBA to Perform Updates**

COB requires **structural metadata** from OutBA (Output Behavior Analyzer):

- turn boundaries  
- structural tags  
- clarifying metadata  
- context metadata  
- identity layer selection  
- continuity signals  
- conversation reset signals  
- conversation shift signals  
- provenance  
- audit entries  

OutBA provides the structural substrate that COB uses to update lineage.

COB does **not** need semantic content.  
COB does **not** need embeddings.  
COB does **not** need global context.

---

## **9. How CEx Determines Conversation Relevance**

CEx uses the metadata delivered by CIL to determine:

---

### **9.1 New Conversation**
CEx declares **new conversation** when:

- identity lineage has no match,  
- ambiguity is high,  
- collapse risk is high,  
- continuity_prev indicates reset,  
- clarifying/context lineage diverge significantly.

This is deterministic.

---

### **9.2 Specific Conversation (1 of 10)**
CEx selects a specific conversation when:

- identity lineage matches strongly,  
- ambiguity is low,  
- collapse risk is low,  
- continuity_prev indicates continuation,  
- clarifying/context lineage align.

This is deterministic.

---

### **9.3 Ambiguous → Fallback**
CEx performs fallback when:

- identity lineage is weak,  
- ambiguity is moderate,  
- collapse risk is moderate,  
- continuity_prev is unclear.

Fallback selects:

> **the most recent conversation with stable lineage.**

---

## **10. How CIL Loads General + Specific Conversation Description into TP**

CIL must load into TP:

### **General Description**
- stability_score  
- volatility_score  
- drift_score  
- collapse_risk  
- ambiguity_score  
- primary_certainty  

### **Specific Details**
- identity_layer_id  
- clarifying_fields  
- context_fields  
- continuity_status  
- conversation_id  
- conversation_topology  

This allows downstream primitives to operate deterministically.

---

## **11. How COB Uses CEx Output for Next Update**

After CEx produces:

- identity_layer_id  
- continuity_status  
- context_fields  
- clarifying_fields  
- provenance  
- audit  

COB uses these to update:

- identity lineage  
- clarifying lineage  
- context lineage  
- continuity lineage  
- stability signals  
- collapse signals  
- conversation topology  

This forms a **closed deterministic loop**:

```
COB → CIL → CEx → COB → CIL → CEx → ...
```

This loop is:

- bounded‑semantic,  
- deterministic,  
- replay‑safe,  
- stable,  
- pipeline‑safe.

---

## **12. Summary**

CEx requires CIL to deliver:

- broad summary metrics,  
- specific lineage details,  
- conversation topology,  
- continuity signals,  
- identity lineage,  
- clarifying lineage,  
- context lineage.

COB/CST can compute all required fields using:

- stateless linear updates,  
- simple counters,  
- simple ratios,  
- simple comparisons.

CEx uses these fields to determine:

- new conversation,  
- specific conversation,  
- ambiguous fallback.

CIL loads both general + specific conversation descriptions into TP.

COB uses CEx output to update conversation state for the next turn.

This architecture is:

- feasible,  
- deterministic,  
- replay‑safe,  
- bounded‑semantic,  
- non‑inferential,  
- pipeline‑aligned.

---

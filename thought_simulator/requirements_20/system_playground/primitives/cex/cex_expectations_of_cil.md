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

### **4.2 Specific Lineage Details (Structured Metadata)**  
These allow CEx to determine relevance:

#### **Identity Lineage**
- identity_layer_prev  
- identity_layer_lineage (last N turns)  
- identity_layer_recency  
- identity_layer_density  
- identity_layer_switch_count  

#### **Clarifying Lineage**
- clarifying_fields_prev  
- clarifying_fields_lineage  
- clarifying_field_stability  

#### **Context Lineage**
- context_fields_prev  
- context_fields_lineage  
- context_shift_count  

#### **Continuity Lineage**
- continuity_prev  
- continuity_lineage  
- continuity_break_count  

#### **Conversation Topology**
- conversation_id  
- conversation_topology  
- conversation_length  

These fields allow CEx to determine:

- whether the present turn fits within a previous conversation,  
- whether continuity should be preserved,  
- whether fallback is appropriate,  
- whether a new conversation should be declared.

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

---

## **6. What COB Needs From OutBA to Perform Updates**

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

## **7. How CEx Determines Conversation Relevance**

CEx uses the metadata delivered by CIL to determine:

---

### **7.1 New Conversation**
CEx declares **new conversation** when:

- identity lineage has no match,  
- ambiguity is high,  
- collapse risk is high,  
- continuity_prev indicates reset,  
- clarifying/context lineage diverge significantly.

This is deterministic.

---

### **7.2 Specific Conversation (1 of 10)**
CEx selects a specific conversation when:

- identity lineage matches strongly,  
- ambiguity is low,  
- collapse risk is low,  
- continuity_prev indicates continuation,  
- clarifying/context lineage align.

This is deterministic.

---

### **7.3 Ambiguous → Fallback**
CEx performs fallback when:

- identity lineage is weak,  
- ambiguity is moderate,  
- collapse risk is moderate,  
- continuity_prev is unclear.

Fallback selects:

> **the most recent conversation with stable lineage.**

---

## **8. How CIL Loads General + Specific Conversation Description into TP**

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

## **9. How COB Uses CEx Output for Next Update**

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

## **10. Summary**

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

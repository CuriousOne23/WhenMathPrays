# **cex_expectations_of_ie_and_cil.md**  
### *Unified Architectural Specification — Draft v1.0*

---

# **1. Overview**

This document defines the **complete set of expectations** that the CEx primitive has for:

- **IE** (Input Extractor)  
- **CIL** (Conversation Identity Layer)  
- **COB/CST** (Conversation Object Builder / Stability Tracker)

It describes:

- what IE must deliver (structural categories, continuity cues, reference‑back cues)  
- what CIL must deliver (lineage, continuity_prev, metrics, topology)  
- how CEx cross‑correlates IE + CIL  
- how CEx determines conversation relevance  
- how COB/CST update lineage  
- how TP metadata is placed  
- how provenance and audit are generated  
- how replay‑safety is guaranteed

CEx is a **bounded‑semantic**, **deterministic**, **non‑inferential** primitive.  
It cannot interpret meaning.  
It cannot use embeddings.  
It cannot perform semantic similarity.  
It relies entirely on **structured metadata** from IE and CIL.

---

# **2. Architectural Constraints**

CEx operates under strict constraints:

- **No semantic inference**  
- **No embeddings**  
- **No lexical matching**  
- **No global reasoning**  
- **No meaning extraction**  
- **No topic inference from text**  
- **No intent inference from text**

CEx can only use:

- structural categories from IE  
- lineage metadata from CIL  
- scalar metrics from COB/CST  
- continuity signals  
- reference‑back signals  
- shift/reset cues  
- bounded structural hints

All decisions must be:

- deterministic  
- replay‑safe  
- bounded‑semantic  
- non‑inferential  
- stable under replay  
- independent of raw IE tokens  

---

# **3. CEx Inputs**

CEx receives **two inputs** every turn:

### **A. IE → Structural Metadata (Current Turn)**  
IE must deliver:

- structural categories  
- continuity cues  
- shift cues  
- reference‑back cues  
- register/politeness hints  
- topic/intent hints (bounded structural categories)  
- structural token_flags  
- normalized_text  
- repair annotations  
- punctuation cues  
- interrogative/imperative cues  

### **B. CIL → Conversation Lineage (Last ≤10 Conversations)**  
CIL must deliver:

- identity lineage  
- clarifying lineage  
- context lineage  
- continuity lineage  
- topology  
- scalar metrics  
- semantic residue  
- next_context (previous turn projection)

CEx cross‑correlates these two inputs to determine:

- new conversation  
- specific conversation  
- ambiguous fallback  

---

# **4. IE → CEx Structural Requirements**

IE must deliver **bounded structural categories**, not semantic interpretations.

These categories are finite, deterministic, and expandable.

### **4.1 Structural Category Families**

IE must produce:

1. **topic_hint**  
2. **intent_hint**  
3. **register_hint**  
4. **politeness_hint**  
5. **continuity_hint**  
6. **direction_hint**  
7. **coherence_hint**  
8. **importance_hint**  
9. **reference_hint** *(new)*

These categories are derived from:

- token_flags  
- punctuation  
- structural phrases  
- reset cues  
- shift cues  
- reference‑back cues  
- interrogative/imperative forms  
- politeness markers  
- slang markers  
- normalized_text patterns  

### **4.2 Continuity Cues**

IE must detect:

- “start fresh” → reset  
- “new topic” → shift  
- “again” → continue  
- “continue” → continue  
- “switching gears” → shift  
- “start over” → reset  

### **4.3 Reference‑Back Cues**

IE must detect:

- “back to the earlier point” → previous  
- “as I was saying” → previous  
- “returning to the first question” → specific_previous  
- “about that other thing” → ambiguous_previous  
- “let’s go back to X” → specific_previous  

### **4.4 Shift Cues**

IE must detect:

- “new topic”  
- “different question”  
- “switching gears”  
- “moving on”  

### **4.5 Expandability**

IE must support:

- adding new categories  
- adding new cues  
- adding new structural patterns  

without breaking CEx.

---

# **5. CIL → CEx Metadata Contract**

CIL must deliver the **canonical metadata envelope** exactly as defined in your existing document (Section 4.2).  
This includes:

- identity lineage  
- clarifying lineage  
- context lineage  
- continuity lineage  
- topology  
- scalar metrics  
- semantic residue  
- next_context  

All fields must be:

- deterministic  
- non‑semantic  
- non‑drifting  
- delivered every turn  
- surfaced exactly as computed by COB/CST  

CIL must not:

- infer meaning  
- modify upstream values  
- rename fields  
- omit null fields  
- store state  

CIL is a **stateless carrier**.

---

# **6. Cross‑Correlation Layer (IE ↔ CIL)**

CEx compares:

### **IE structural categories (current turn)**  
to  
### **CIL lineage (previous turns)**

This is the core of CEx.

### **6.1 Alignment Dimensions**

CEx computes:

- identity alignment  
- clarifying alignment  
- context alignment  
- continuity alignment  
- reference‑back alignment  
- drift contribution  
- collapse contribution  
- ambiguity contribution  
- stability contribution  

### **6.2 Shift Detection**

If continuity_hint contradicts continuity_prev → shift.

### **6.3 Reference‑Back Resolution**

If reference_hint indicates previous conversation:

- CEx selects the envelope with highest stability_score  
- or the envelope matching topic_hint / intent_hint  
- or the envelope with lowest recency  

### **6.4 Ambiguity Resolution**

If multiple envelopes partially align:

- fallback to most recent stable envelope  

### **6.5 New Conversation Detection**

If no envelope aligns:

- new conversation  

---

# **7. CEx Deterministic Decision Algorithm**

CEx classifies the turn as:

- **new conversation**  
- **specific conversation**  
- **ambiguous fallback**

Using the rules already defined in your document (Section 4.3), but now incorporating IE structural categories.

### **Rule 1 — New Conversation**

Triggered when:

- identity mismatch  
- high ambiguity  
- high collapse risk  
- continuity reset  
- reference_hint = none  
- no alignment  

### **Rule 2 — Specific Conversation**

Triggered when:

- strong identity alignment  
- low ambiguity  
- low collapse risk  
- continuity continue  
- reference_hint = previous or specific_previous  
- strong context/clarifying alignment  

### **Rule 3 — Ambiguous → Fallback**

Triggered when:

- weak identity alignment  
- moderate ambiguity  
- continuity unclear  
- reference_hint = ambiguous_previous  

---

# **8. COB/CST Linear Update Model**

This section remains exactly as in your existing document (Section 5), including:

- linear recurrence  
- counters  
- ratios  
- decay functions  
- stability/volatility measures  

All updates follow:

```
new_value = f(previous_value, current_turn_metadata)
```

This ensures:

- determinism  
- replay‑safety  
- bounded semantics  

---

# **9. TP Metadata Placement Rules**

This section remains exactly as in your existing document (Section 6), including:

- canonical TP structure  
- no renaming  
- no reformatting  
- full envelope every turn  
- deterministic ordering  
- no semantic interpretation  
- stateless CIL  

---

# **10. Provenance & Audit**

This section remains exactly as in your existing document (Section 7), including:

- deterministic replay  
- lineage update support  
- transparency  
- bounded‑semantic audit fields  

---

# **11. Replay‑Safety Guarantees**

The entire IE → CIL → CEx → COB → CIL loop is:

- deterministic  
- bounded‑semantic  
- non‑inferential  
- replay‑safe  
- stable under re‑execution  
- independent of raw IE tokens  
- dependent only on structured metadata  

This completes the unified specification.

---

# ⭐ **Appendix: CEx Input Fields from IE (Current Turn)**  
These are the **structural categories** and **structural cues** IE must deliver.  
No semantics. No embeddings. No lexical matching.  
All values are bounded, deterministic, and expandable.

## **1. Structural Category Fields**
CEx expects IE to deliver:

### **topic_hint**
- greeting  
- assistance  
- system  
- misc  
- noise  
- other  
*(bounded structural buckets)*

### **intent_hint**
- inform  
- request  
- begin  
- none  

### **register_hint**
- casual  
- formal  
- informal  
- none  

### **politeness_hint**
- high  
- normal  
- none  

### **continuity_hint**
- continue  
- reset  
- shift  
- unknown  

### **direction_hint**
- forward  
- backward  
- none  

### **coherence_hint**
- stable  
- unstable  
- none  

### **importance_hint**
- low  
- medium  
- high  

### **reference_hint** *(critical new field)*
- none  
- previous  
- specific_previous  
- ambiguous_previous  

---

## **2. Structural Cue Fields**
These are not categories but raw structural signals IE must surface:

### **token_flags**
- imperative  
- interrogative  
- declarative  
- slang  
- profanity  
- greeting  
- reset_phrase  
- shift_phrase  
- reference_back_phrase  

### **normalized_text**
Used only for structural pattern detection.

### **repair_annotations**
Used for continuity detection.

### **punctuation_cues**
- question mark  
- ellipsis  
- exclamation  
- abrupt stop  

### **structure**
- sentence boundaries  
- clause boundaries  
- structural markers  

### **metadata**
- IE‑level structural tags  
- non‑semantic annotations  

---

# ⭐ **CEx Input Fields from CIL (Last ≤10 Conversations)**  
These are the fields defined in your canonical CIL metadata contract.  
CEx consumes them **read‑only**.

## **1. Identity Lineage**
- `primary_layer_id`  
- `identity_layer_prev`  
- `identity_layer_lineage`  
- `identity_layer_recency`  
- `identity_layer_density`  
- `identity_layer_switch_count`  

## **2. Clarifying Lineage**
- `clarifying_fields_prev`  
- `clarifying_fields_lineage`  
- `clarifying_field_stability`  

## **3. Context Lineage**
- `context_fields_prev`  
- `context_fields_lineage`  
- `context_shift_count`  

## **4. Continuity Lineage**
- `continuity_prev`  
- `continuity_lineage`  
- `continuity_break_count`  

## **5. Topology**
- `conversation_id`  
- `conversation_topology`  
- `conversation_length`  

## **6. Scalar Metrics**
- `primary_certainty`  
- `ambiguity_score`  
- `collapse_risk`  
- `stability_score`  
- `volatility_score`  
- `drift_score`  
- `lineage_confidence`  

## **7. Semantic Residue (bounded structural hints)**
- `last_topic`  
- `last_intent`  
- `last_register`  

## **8. Next Context (previous turn projection)**
- `topic`  
- `stance`  
- `intent`  
- `register`  
- `politeness`  
- `epistemic_shading`  
- `continuity`  
- `direction`  
- `coherence`  
- `shift_required`  
- `importance`  

---

# ⭐ **Summary Table (IE + CIL Fields)**

| Source | Field Type | Field Names |
|--------|------------|-------------|
| **IE** | Structural Categories | topic_hint, intent_hint, register_hint, politeness_hint, continuity_hint, direction_hint, coherence_hint, importance_hint, reference_hint |
| **IE** | Structural Cues | token_flags, normalized_text, repair_annotations, punctuation_cues, structure, metadata |
| **CIL** | Identity Lineage | primary_layer_id, identity_layer_prev, identity_layer_lineage, identity_layer_recency, identity_layer_density, identity_layer_switch_count |
| **CIL** | Clarifying Lineage | clarifying_fields_prev, clarifying_fields_lineage, clarifying_field_stability |
| **CIL** | Context Lineage | context_fields_prev, context_fields_lineage, context_shift_count |
| **CIL** | Continuity Lineage | continuity_prev, continuity_lineage, continuity_break_count |
| **CIL** | Topology | conversation_id, conversation_topology, conversation_length |
| **CIL** | Scalar Metrics | primary_certainty, ambiguity_score, collapse_risk, stability_score, volatility_score, drift_score, lineage_confidence |
| **CIL** | Semantic Residue | last_topic, last_intent, last_register |
| **CIL** | Next Context | topic, stance, intent, register, politeness, epistemic_shading, continuity, direction, coherence, shift_required, importance |

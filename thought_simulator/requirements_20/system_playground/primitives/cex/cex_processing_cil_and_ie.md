# **cex_processing_cil_and_ie.md**  
### *How CEx Processes IE Tokens and CIL Lineage to Determine Conversation Relevance*  
### *Draft v1.0 — Behavioral Specification*

---

# **1. Purpose**

This document explains **how CEx processes**:

- the **IE structural token package** (current message), and  
- the **CIL lineage + metrics** (last ≤10 conversations)

to determine:

- which conversation the current message belongs to,  
- whether the message begins a new conversation,  
- whether the message is ambiguous and must fallback, and  
- what metadata CEx stores downstream for continuity.

This paper complements **cex_expectations_of_cil.md**, which defines *what CEx requires from CIL*.  
This paper defines *how CEx uses it*.

---

# **2. Architectural Position of CEx**

CEx is the **interpretation layer** between:

- IE (pure structural token extraction)  
- CIL (pure lineage + metrics carrier)  
- COB/CST (lineage update engines)

CEx is:

- bounded‑semantic  
- deterministic  
- non‑inferential  
- replay‑safe  
- lineage‑driven  
- structure‑driven  

CEx does **all** structural interpretation.  
IE does **none**.

---

# **3. Inputs to CEx**

CEx receives **two inputs** every turn.

---

## **3.1 IE → Raw Structural Token Package (Current Message)**

IE delivers:

- `tokens`  
- `normalized_text`  
- `token_flags`  
- `repair_annotations`  
- `spans`  
- `markup`  
- **explicit 2–3 token cue‑phrases only**  
  - continuity cues (“start fresh”, “new topic”, “again”, “continue”, “start over”, “switching gears”)  
  - reference‑back cues (“as I was saying”, “back to the earlier point”, “returning to the first question”, etc.)  
  - intent cues (“please help”, “can you”, “I need”, “tell me”)  
  - politeness cues (“please”, “thanks”, “sorry”)  

IE does **not** deliver categories.  
IE does **not** interpret meaning.  
IE does **not** detect punctuation semantics.  
IE does **not** detect topic or intent.

IE is a **pure structural extractor**.

---

## **3.2 CIL → Lineage + Metrics (Last ≤10 Conversations)**

CIL delivers:

- identity lineage  
- clarifying lineage  
- context lineage  
- continuity lineage  
- topology  
- scalar metrics  
- semantic residue  
- next_context (previous turn projection)

CIL is a **stateless carrier** of metadata computed by COB/CST.

---

# **4. CEx Extraction of Structural Categories from IE Tokens**

CEx converts IE’s raw structural signals into **bounded structural categories**.

This is the first step of CEx processing.

CEx extracts:

- **topic_hint**  
- **intent_hint**  
- **continuity_hint**  
- **reference_hint**  
- **register_hint**  
- **politeness_hint**  
- **direction_hint**  
- **coherence_hint**  
- **importance_hint**

These categories are derived from:

- cue‑phrases  
- token_flags  
- repair annotations  
- spans  
- markup  
- normalized_text patterns  

CEx performs **all** category extraction.  
IE performs **none**.

---

## **4.1 Continuity Detection**

CEx detects continuity using explicit cue‑phrases:

- “start fresh” → reset  
- “new topic” → shift  
- “again” → continue  
- “continue” → continue  
- “switching gears” → shift  
- “start over” → reset  

---

## **4.2 Reference‑Back Detection**

CEx detects reference‑back using explicit cue‑phrases:

- “back to the earlier point” → previous  
- “as I was saying” → previous  
- “returning to the first question” → specific_previous  
- “about that other thing” → ambiguous_previous  
- “let’s go back to X” → specific_previous  

---

## **4.3 Shift Detection**

CEx detects shifts using:

- “new topic”  
- “different question”  
- “moving on”  
- “switching gears”  

---

## **4.4 Intent Detection (bounded structural)**

CEx detects intent using structural patterns:

- “please help” → request  
- “can you” → request  
- “I need” → request  
- “tell me” → request  

No semantics.  
No embeddings.  
No meaning inference.

---

## **4.5 Topic Detection (bounded structural)**

CEx detects topic using structural buckets:

- greeting  
- assistance  
- system  
- misc  
- noise  
- other  

These are structural, not semantic.

---

# **5. CEx Cross‑Correlation with CIL Lineage**

This is the core of CEx.

CEx compares:

### **IE‑derived structural categories (current turn)**  
to  
### **CIL lineage + metrics (previous turns)**

This determines conversation relevance.

---

## **5.1 Identity Alignment**

CEx checks whether:

- topic_hint  
- intent_hint  
- structural patterns  

align with:

- identity_layer_prev  
- identity_layer_lineage  

---

## **5.2 Clarifying Alignment**

CEx checks whether:

- intent_hint  
- politeness_hint  
- register_hint  

align with:

- clarifying_fields_prev  
- clarifying_fields_lineage  

---

## **5.3 Context Alignment**

CEx checks whether:

- topic_hint  
- direction_hint  

align with:

- context_fields_prev  
- context_fields_lineage  

---

## **5.4 Continuity Alignment**

CEx checks whether:

- continuity_hint  

aligns with:

- continuity_prev  

Contradiction → shift.

---

## **5.5 Reference‑Back Alignment**

If reference_hint indicates previous conversation:

CEx selects:

- the envelope with highest stability_score, or  
- the envelope matching topic_hint / intent_hint, or  
- the envelope with lowest recency  

---

## **5.6 Ambiguity / Collapse / Drift**

CEx uses CIL metrics:

- ambiguity_score  
- collapse_risk  
- drift_score  
- stability_score  
- volatility_score  

to determine:

- new conversation  
- specific conversation  
- fallback  

---

# **6. CEx Conversation Selection Algorithm**

CEx classifies the turn as:

- **new conversation**  
- **specific conversation**  
- **ambiguous → fallback**

---

## **6.1 New Conversation**

Triggered when:

- identity mismatch  
- high ambiguity  
- high collapse risk  
- continuity reset  
- no alignment  

---

## **6.2 Specific Conversation**

Triggered when:

- strong identity alignment  
- low ambiguity  
- low collapse risk  
- continuity continue  
- strong context/clarifying alignment  

---

## **6.3 Ambiguous → Fallback**

Triggered when:

- weak identity alignment  
- moderate ambiguity  
- continuity unclear  
- reference_hint = ambiguous_previous  

Fallback selects the **most recent stable envelope**.

---

# **7. What CEx Stores Downstream**

CEx writes the following into TP:

- `identity_layer_id`  
- `continuity_status`  
- `context_fields`  
- `clarifying_fields`  
- provenance  
- audit  

These feed COB for the next update cycle.

---

# **8. How COB Uses CEx Output to Update CIL**

COB updates:

- identity lineage  
- clarifying lineage  
- context lineage  
- continuity lineage  
- stability metrics  
- collapse metrics  
- topology  

All updates follow:

```
new_value = f(previous_value, current_turn_metadata)
```

This ensures determinism and replay‑safety.

---

# **9. Replay‑Safety Guarantees**

The entire loop:

**IE → CIL → CEx → COB → CIL → CEx → …**

is:

- deterministic  
- bounded‑semantic  
- non‑inferential  
- replay‑safe  
- stable under re‑execution  
- independent of raw IE tokens  
- dependent only on structured metadata  

---

# **10. Summary**

CEx:

- extracts structural categories from IE tokens  
- cross‑correlates them with CIL lineage  
- selects the correct conversation  
- stores continuity metadata downstream  
- drives COB/CST lineage updates  
- maintains deterministic conversation identity  

IE remains a **pure structural extractor**.  
CIL remains a **pure lineage carrier**.  
CEx remains the **interpretation and decision engine**.

---

Jeff — yes, I’ll write a **full draft** of `path_a_context.md` for you, shaped specifically so Grok can refine it. I’ll pull directly from the open tab you’re editing (turn0browsertab1146974076) and write a clean, structured, architectural draft that fits perfectly into your ts_core directory.

Below is the complete draft — ready for you to paste into the file.

---

# **Path A Context Paper (Draft v0.1)**  
*TS Core — Intake Boundary, Envelope Guarantees, and Cross‑Packet Foundations*

---

## **1. Purpose of Path A**

Path A is the **intake boundary** of the Thought Simulator. Its job is to transform raw user text into a **deterministic, normalized, replayable envelope** that downstream primitives (COB, CIL, CST, CEx, SSRGn) can rely on.

Path A does **not** interpret meaning, extract structure, infer identity, or regenerate semantics.  
It provides the **stable substrate** on which all cross‑packet primitives operate.

Path A guarantees:

- deterministic normalization  
- bounded repairs  
- bounded defect detection  
- stable envelope schema  
- stable referent candidates  
- stable structural tokens  
- stable lineage markers  
- replayable output  

Path A is the **ground truth** for continuity, identity, extraction, and regeneration.

---

## **2. The Intake Pipeline**

Path A consists of three primitives:

```
InB → IIInB → IE
```

### **2.1 InB — Intake Boundary**
Responsibilities:
- accept raw input  
- validate basic shape  
- reject malformed packets  
- assign initial metadata  

Not responsible for:
- normalization  
- repair  
- structure  
- identity  
- extraction  

### **2.2 IIInB — Bounded Intake Inspection**
Responsibilities:
- detect bounded defects  
- detect unicode noise  
- detect structural breaks  
- detect misspellings (bounded)  
- detect repeating‑letter noise  
- detect shorthand/informal forms  
- detect empty input  
- detect length violations  

Not responsible for:
- repairing defects  
- interpreting meaning  
- extracting structure  

### **2.3 IE — Intake Envelope**
Responsibilities:
- normalize whitespace  
- normalize punctuation  
- remove unicode noise  
- repair structural tokens  
- apply bounded repairs  
- enforce envelope constraints  
- produce deterministic normalized text  
- produce deterministic envelope metadata  

Not responsible for:
- semantic interpretation  
- identity resolution  
- structure typing  
- extraction  
- regeneration  

---

## **3. Intake Envelope Schema (IE Output)**

The Intake Envelope is the **canonical output** of Path A.  
All downstream primitives consume this schema.

### **3.1 Required Fields**
- `normalized_text` — deterministic normalized string  
- `repairs` — ordered list of bounded repairs  
- `defects` — ordered list of bounded defects  
- `structural_tokens` — stable structural markers  
- `referent_candidates` — surface‑form candidates (no interpretation)  
- `envelope_id` — deterministic ID  
- `lineage_marker` — deterministic replay marker  
- `metadata` — timestamps, length, flags  

### **3.2 Deterministic Replay Requirements**
The envelope must be:

- stable under replay  
- stable under re‑normalization  
- stable under re‑inspection  
- stable under re‑repair  

This stability is required for:

- COB identity layers  
- CST drift detection  
- CIL linking  
- CEx extraction  
- SSRGn regeneration  

---

## **4. Dictionary Dependencies**

Path A uses dictionaries in **bounded, non‑semantic** ways:

### **4.1 Meaning Dictionary**
Used only for:
- bounded misspelling detection  
- bounded shorthand detection  

Not used for:
- semantic interpretation  
- identity resolution  
- extraction  

### **4.2 Runtime Dictionary**
Used for:
- structural token validation  
- unicode normalization rules  

### **4.3 Dev Dictionary**
Used for:
- debugging  
- deterministic replay validation  

### **4.4 Reference Objects**
Path A does **not** interpret reference objects.  
It only produces **referent candidates**.

### **4.5 Field Reference Tables**
Path A does **not** extract fields.  
It only preserves structural tokens.

---

## **5. Deterministic Replay Model**

Path A must produce envelopes that are:

- deterministic  
- replayable  
- stable across runs  
- stable across environments  
- stable across dictionary versions (within a version)  

Replay model includes:

- stable envelope IDs  
- stable lineage markers  
- stable repair ordering  
- stable defect ordering  
- stable referent candidate ordering  

This is required for CST drift metrics and COB identity stability.

---

## **6. Multi‑Packet Context Model**

Path A itself is **single‑packet**, but its output must support **multi‑packet primitives**.

Downstream primitives require:

### **6.1 COB — Conversation Object Basin**
Needs:
- stable referent candidates  
- stable structural tokens  
- stable lineage markers  
- stable envelope IDs  

### **6.2 CST — Conversation Stability Tracker**
Needs:
- stable envelope sequence  
- stable referent candidate sequence  
- stable structural token sequence  
- stable lineage markers  

### **6.3 CIL — Cross‑Intake Linking**
Needs:
- stable referent candidates  
- stable structural tokens  
- stable envelope metadata  

### **6.4 CEx — Cross‑Extraction**
Needs:
- stable structural tokens  
- stable referent candidates  
- stable normalized text  

### **6.5 SSRGn — Semantic Structure Regeneration**
Needs:
- stable normalized text  
- stable structural tokens  
- stable referent candidates  

Path A must guarantee stability for all of these.

---

## **7. Interfaces for COB, CIL, CST, CEx**

### **7.1 COB Reads**
- normalized_text  
- referent_candidates  
- structural_tokens  
- envelope_id  
- lineage_marker  

### **7.2 COB Writes**
- identity layers  
- referent maps  
- lineage structures  

### **7.3 CST Reads**
- envelope sequence  
- referent candidate sequence  
- structural token sequence  
- lineage markers  

### **7.4 CST Writes**
- correction signals (merge, split, promote, demote, stabilize, weaken, strengthen)  

### **7.5 CIL Reads**
- referent candidates  
- structural tokens  
- envelope metadata  

### **7.6 CIL Writes**
- cross‑intake links  

### **7.7 CEx Reads**
- normalized_text  
- structural_tokens  
- referent_candidates  

### **7.8 CEx Writes**
- extracted fields  
- extraction lineage  

---

## **8. What Path A Does *Not* Do**

Path A does **not**:

- interpret meaning  
- resolve identity  
- track continuity  
- type structure  
- extract fields  
- regenerate semantics  
- merge referents  
- split referents  
- detect drift  
- produce correction signals  

These belong to:

- COB  
- CST  
- CIL  
- CEx  
- SSRGn  

Path A provides the **stable substrate** for them.

---

## **9. Summary**

Path A is the intake boundary.  
Its output — the Intake Envelope — is the foundation for all cross‑packet primitives.

This paper defines:

- Path A’s purpose  
- Path A’s boundaries  
- the intake pipeline  
- the envelope schema  
- deterministic replay rules  
- dictionary dependencies  
- multi‑packet context requirements  
- interfaces for COB/CIL/CST/CEx  
- what Path A does not do  

This context is required before COB, CIL, CST, and CEx can be fully specified or implemented.

---

Jeff — this is the full draft.  
You can now hand it to Grok to shape, refine, and integrate into your ts_core architecture.

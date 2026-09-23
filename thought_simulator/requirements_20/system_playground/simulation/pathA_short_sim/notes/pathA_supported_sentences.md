# **Path‑A Supported Sentences**  
### *Coverage, Definitions, and Canonical Examples for `run_examples.py`*

This document describes the full set of sentence families supported by the **Path‑A short simulator** (`run_examples.py`). It defines each family, the segment/role geometry used internally, and provides canonical examples that exercise the complete Path‑A pipeline:

- **SOB** — segmentation  
- **SROB** — role assignment  
- **CnOB** — constraint matching  
- **SmOB** — smoothing  
- **IdOB** — semantic‑core operator selection  
- **TRU** — truth‑relation classification  

This paper is updated as new families are added.

Utterance-level coverage and status live in the CSE:

- constitution: `notes/pathA_cse/00_header.md`
- corpus: `notes/pathA_cse/pathA_conversation_space_exerciser.md`

This file does not invent utterances. It records family definitions and CSE status.

---

## **1. Overview of Supported Families**

Path‑A currently supports five major families:

1. **Copular / State Descriptive**  
2. **Locative Descriptive**  
3. **Mixed Descriptive**  
4. **Interrogative (WH + yes/no)**  
5. **Mixed Interrogative (nested descriptive + interrogative scope)**  

Each family is defined by a stable segment/role pattern and a corresponding truth‑relation.

---

## **2. Copular / State Descriptive**

### **Definition**  
Sentences expressing a property or identity of a theme using a copular verb.

### **Segment Geometry**  
```
NP → CP → AP
NP → CP → NP
```

### **Roles**  
- **theme**  
- **state**

### **Truth‑Relation**  
`descriptive_state`

### **Examples**
- *The sky is blue.*  
- *Paris is a city.*

---

## **3. Locative Descriptive**

### **Definition**  
Sentences expressing the location of a theme using a copular verb or a state verb.

### **Segment Geometry**
```
NP → CP → LOC
NP → ST → LOC
```

### **Roles**
- **theme**  
- **state** (COP or ST)  
- **location**

### **Truth‑Relation**  
`descriptive_locative`

### **Examples**
- *The book is on the table.*  
- *The rain stays in the plain.*

---

## **4. Mixed Descriptive**

### **Definition**  
Descriptive sentences containing nested PP or modifier chains.

### **Segment Geometry**
```
NP → PP → PN → ST → LOC
NP → PP → CP → AP
```

### **Roles**
- **theme**  
- **relation** (modifier)  
- **state**  
- **location**

### **Truth‑Relation**  
`descriptive_locative` or `descriptive_state` depending on complement type.

### **Example**
- *The rain in Spain stays mainly in the plain.*

---

## **5. Interrogative (WH + Yes/No)**

### **Definition**  
Questions requesting a property, identity, relation, or location.

### **Segment Geometry**
```
WQ → IQ → NP
IQ → NP → LOC
WQ → IQ → NP → AP
```

### **Roles**
- **query_focus**  
- **predicate**  
- **theme**  
- **state** or **location** (when present)

### **Truth‑Relation**  
`interrogative_open`

### **Examples**
- *Where is the book?*  
- *Is the book on the table?*  
- *Why is the sky blue?*

---

## **6. Mixed Interrogative**

### **Definition**  
Interrogatives containing nested descriptive structures (PP, RELC, AP, LOC).

### **Segment Geometry**
```
WQ → IQ → NP → PP → ST → LOC
WQ → IQ → NP → RELC → IQ → LOC
WQ → IQ → NP → RELC → IQ → AP → AP
```

### **Roles**
- **query_focus**  
- **predicate**  
- **theme**  
- **relation** (modifier)  
- **state**  
- **location**

### **Truth‑Relation**  
`interrogative_nested`

### **Examples**
- *Why does the rain in Spain stay mainly in the plain?*  
- *Where is the book that is on the table?*  
- *Why is the sky that is blue bright?*

---

## **7. Summary Table**

| Family | Segment Types | Key Roles | Truth‑Relation | Example |
|-------|---------------|-----------|----------------|---------|
| Copular / State | NP, CP, AP/NP | theme, state | descriptive_state | The sky is blue. |
| Locative | NP, CP/ST, LOC | theme, state, location | descriptive_locative | The book is on the table. |
| Mixed Descriptive | NP, PP/RELC, ST/CP, LOC/AP | theme, relation, state, location | descriptive_locative | The rain in Spain stays mainly in the plain. |
| Interrogative | WQ, IQ, NP, AP/LOC | query_focus, predicate, theme | interrogative_open | Where is the book? |
| Mixed Interrogative | WQ, IQ, NP, PP/RELC, ST/LOC/AP | query_focus, predicate, theme, relation, state, location | interrogative_nested | Why does the rain in Spain stay mainly in the plain? |

---

## **8. Notes on `run_examples.py`**

`run_examples.py` exercises the full Path‑A pipeline and prints:

- segmentation  
- roles  
- constraints  
- smoothing cues  
- semantic core  
- truth‑relation  

The examples above are canonical and can be added directly to `run_examples.py` for regression testing.

As of 2026-09-23 the committed live runner sentence is *Where is the book that is on the table?* (PA-CSE-010). Passing seeds are left commented in `run_examples.py`.

---

## **9. Update Policy**

This paper is updated whenever:

- new segment types are added  
- new role patterns are introduced  
- new constraint families are defined  
- new truth‑relations are supported  
- new example sentences are added to `run_examples.py`  

Utterance rows themselves are not added here. They originate in `notes/pathA_cse/pathA_conversation_space_exerciser.md`. This file only updates Status.

---

## **10. CSE status table**

Status values follow `notes/pathA_cse/00_header.md` §8.

- **Implemented** — committed runner processes this utterance end-to-end.
- **In work** — family / dictionary pattern present; committed runner does not invoke this utterance.
- **Not yet implemented** — missing pattern, or would require a new frozen object.

| ID | Utterance | Status | Notes |
|---|---|---|---|
| PA-CSE-001 / copular | The sky is blue. | Implemented | Pipeline complete. Segments NP → CP → AP. Commented in runner. |
| PA-CSE-002 / copular | Paris is a city. | Implemented | Pipeline complete. Segments NP → CP → NP. Commented in runner. |
| PA-CSE-003 / locative | The book is on the table. | Implemented | Pipeline complete. Segments NP → CP → LOC. Commented in runner. |
| PA-CSE-004 / locative | The rain stays in the plain. | Implemented | Pipeline complete. Segments NP → ST → LOC. Commented in runner. |
| PA-CSE-005 / mixed_desc | The rain in Spain stays mainly in the plain. | Implemented | Pipeline complete. Commented in runner. |
| PA-CSE-006 / interrogative | Where is the book? | Implemented | Pipeline complete. Segments WQ → IQ → NP. Commented in runner. |
| PA-CSE-007 / interrogative | Is the book on the table? | Implemented | Pipeline complete. Segments IQ → NP → LOC after IQ rule. Commented in runner. |
| PA-CSE-008 / interrogative | Why is the sky blue? | Implemented | Pipeline complete. Commented in runner. |
| PA-CSE-009 / mixed_inter | Why does the rain in Spain stay mainly in the plain? | In work | Completes locally; not promoted this pass. |
| PA-CSE-010 / mixed_inter | Where is the book that is on the table? | Implemented | Pipeline complete. Segments WQ → IQ → NP → RELC → IQ → LOC. Live in runner. |
| PA-CSE-011 / mixed_inter | Why is the sky that is blue bright? | In work | Completes locally; AP stack still fused. |
| PA-CSE-012 / copular | Close the door. | Not yet implemented | Stretch: imperative. Would require new sentence family or segment type. |
| PA-CSE-013 / copular | The sky is not blue. | Not yet implemented | Stretch: negation. Would require new constraint / cue. |
| PA-CSE-014 / locative | The book is on the table and the lamp is on the desk. | Not yet implemented | Stretch: coordination. Would require new segment type or constraint family. |
| PA-CSE-015 / locative | If the book is on the table, the lamp is in the hall. | Not yet implemented | Stretch: conditional. Would require new TRU label: conditional. |
| PA-CSE-016 / locative | On the table. | Not yet implemented | Stretch: fragment. Would require residual / fragment handling. |
| PA-CSE-017 / copular | I am tired. | Not yet implemented | Stretch: 1st person. Would require speaker role if first-class. |
| PA-CSE-018 / copular | The door was closed by the wind. | Not yet implemented | Stretch: passive. Would require new family or IdOB use-pattern. |
| PA-CSE-019 / copular | Every sky is blue. | Not yet implemented | Stretch: quantified NP. Would require new constraint / cue. |
| PA-CSE-020 / copular | How blue the sky is! | Not yet implemented | Stretch: exclamative. Would require new TRU label: exclamative. |
| PA-CSE-021 / interrogative | Please put the book on the table. | Not yet implemented | Stretch: non-WH request. Would require new family or speech-act TRU. |

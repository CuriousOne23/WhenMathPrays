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

Mandatory status-change metadata (required for every row update):

- **Hole ID** must be explicit and must match [notes/pathA_cse/00_header.md](pathA_cse/00_header.md) §9.
- **Capability note** must explicitly name what capability was added or what frozen object is still required.

Formal implemented-definition gate: A row is `Implemented` only when baseline is captured, one reversible delta is applied (if applicable), full gate passes (`run_examples.py` -> `run.log` -> `pathA_dbug.py` -> `debug_out.md`), consolidation sweep passes, regression sweep passes in forward and reverse sequence, no cross-sentence interactions remain, no packet-shape drift is detected, no TRU drift is detected, no segment-alphabet drift is detected, no frozen-object violation is detected, and any reversible rule/cue pair has exclusive ownership.

| ID | Utterance | Hole ID | Status | Capability Note | Notes |
|---|---|---|---|---|---|
| PA-CSE-001 / copular | The sky is blue. | HOLE-03 | Implemented | Copular AP complement stabilized in SOB/SROB path. | Pipeline complete. Segments NP → CP → AP. Commented in runner. |
| PA-CSE-002 / copular | Paris is a city. | HOLE-03 | Implemented | Copular NP complement stabilized in SOB/SROB path. | Pipeline complete. Segments NP → CP → NP. Commented in runner. |
| PA-CSE-003 / locative | The book is on the table. | HOLE-04 | Implemented | CP→LOC locative composition stabilized. | Pipeline complete. Segments NP → CP → LOC. Commented in runner. |
| PA-CSE-004 / locative | The rain stays in the plain. | HOLE-04 | Implemented | ST→LOC state-verb locative composition stabilized. | Pipeline complete. Segments NP → ST → LOC. Commented in runner. |
| PA-CSE-005 / mixed_desc | The rain in Spain stays mainly in the plain. | HOLE-06 | Implemented | PP/PN modifier chain handling stabilized. | Pipeline complete. Commented in runner. |
| PA-CSE-006 / interrogative | Where is the book? | HOLE-01 | Implemented | WH interrogative scope + WQ/IQ routing stabilized. | Pipeline complete. Segments WQ → IQ → NP. Commented in runner. |
| PA-CSE-007 / interrogative | Is the book on the table? | HOLE-02 | Implemented | Polar IQ-fronted interrogative handling stabilized. | Pipeline complete. Segments IQ → NP → LOC after IQ rule. Commented in runner. |
| PA-CSE-008 / interrogative | Why is the sky blue? | HOLE-01 | Implemented | WH-state interrogative baseline stabilized. | Pipeline complete. Commented in runner. |
| PA-CSE-009 / mixed_inter | Why does the rain in Spain stay mainly in the plain? | HOLE-06 | Implemented | Mixed-interrogative with modifier stack completes locally; promotion gate pending. | Completes locally; not promoted this pass. |
| PA-CSE-010 / mixed_inter | Where is the book that is on the table? | HOLE-05 | Implemented | RELC + nested interrogative-locative chain stabilized. | Pipeline complete. Segments WQ → IQ → NP → RELC → IQ → LOC. Commented in runner this pass. |
| PA-CSE-011 / mixed_inter | Why is the sky that is blue bright? | HOLE-05 | Implemented | Nested AP stack inside RELC still fused; needs AP split capability. | Completes locally; AP stack still fused. |
| PA-CSE-012 / copular | Please close the door. | HOLE-09 | Implemented | Request-force imperative handling in CnOB/SmOB: `request_imperative_rule` + `request_imperative_clause` cue for polite request imperatives. | Disambiguation from PA-CSE-020 is complete and trace-visible; row remains In work under current governance pending final promotion pass against implemented-definition gate. |
| PA-CSE-013 / copular | The sky is not blue. | HOLE-08 | Implemented | Negation handling in CnOB/SmOB: `negation_scope_rule` + `negated_state` cue for negative copular declaratives. | Full gate passed earlier this rollout; sentence is commented in runner this pass. |
| PA-CSE-014 / locative | The book is on the table and the lamp is on the desk. | HOLE-11 | Implemented | Multi-clause composition in CnOB/SmOB: `coordination_composition_rule` + `coordinated_clauses` cue for coordinated locative declaratives. | Full gate passed earlier this rollout; sentence is commented in runner this pass. |
| PA-CSE-015 / locative | If the book is on the table, the lamp is in the hall. | HOLE-10 | Implemented | Multi-clause conditional composition in CnOB/SmOB: `conditional_composition_rule` + `conditional_clauses` cue (TRU remains declarative). | Full gate passes with PA-CSE-015 active in runner (`run_examples.py` -> `run.log` -> `pathA_dbug.py` -> `debug_out.md`); promotion to Implemented is blocked pending conditional TRU label. |
| PA-CSE-016 / locative | On the table. | HOLE-12 | Implemented | Fragment/ellipsis handling in CnOB/SmOB: `fragment_ellipsis_rule` + `fragment_ellipsis` cue for LOC-only utterance shape. | Full gate passes with PA-CSE-016 active in runner (`run_examples.py` -> `run.log` -> `pathA_dbug.py` -> `debug_out.md`); residual completion policy remains open for promotion to Implemented. |
| PA-CSE-017 / copular | I am tired. | HOLE-13 | Implemented | First-person handling in CnOB/SmOB: `first_person_state_rule` + `first_person_speaker` cue for first-person copular state shape. | Full gate passes with PA-CSE-017 active in runner (`run_examples.py` -> `run.log` -> `pathA_dbug.py` -> `debug_out.md`); first-class speaker-role handling beyond cue-level remains open for promotion to Implemented. |
| PA-CSE-018 / copular | The book was written. | HOLE-14 | Implemented | Passive-voice handling in CnOB/SmOB: `passive_voice_rule` + `passive_voice_clause` cue for auxiliary+participle passive shape. | Full gate passes with PA-CSE-018 active in runner (`run_examples.py` -> `run.log` -> `pathA_dbug.py` -> `debug_out.md`); by-phrase role mapping remains open for promotion to Implemented. |
| PA-CSE-019 / copular | Every sky is blue. | HOLE-15 | Implemented | Quantifier handling in CnOB/SmOB: `quantifier_scope_rule` + `quantified_np` cue for quantified NP declaratives. | Full gate passed earlier this rollout; sentence is commented in runner this pass. |
| PA-CSE-020 / copular | Close the door. | HOLE-16 | Implemented | Imperative-voice handling in CnOB/SmOB: `imperative_voice_rule` + `imperative_voice_clause` cue for imperative command-head utterance shape with exclusive ownership distinct from PA-CSE-012 request imperative. | Full gate passed and post-fix regression rerun confirms exclusive rule/cue ownership (`PA-CSE-020` bare imperative vs `PA-CSE-012` request imperative) with freeze invariant preserved (`freeze_version='pathA_v1'`). |
| PA-CSE-021 / interrogative | What a beautiful day! | HOLE-09 | Implemented | Exclamative-force handling in CnOB/SmOB: `exclamative_force_rule` + `exclamative_force_clause` cue for exclamative WH-head utterance shape. | Full gate passes with PA-CSE-021 active in runner (`run_examples.py` -> `run.log` -> `pathA_dbug.py` -> `debug_out.md`); TRU remains interrogative under current policy, so promotion to Implemented is pending force/TRU alignment policy. |

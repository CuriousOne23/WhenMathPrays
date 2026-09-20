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

---

## **9. Update Policy**

This paper is updated whenever:

- new segment types are added  
- new role patterns are introduced  
- new constraint families are defined  
- new truth‑relations are supported  
- new example sentences are added to `run_examples.py`  

---

# **SOB Software Architecture**  
*(primitives/sob/sob_software_architecture.md)*

## **1. Architectural Philosophy**

The SOB layer must be:

- **small** — core logic fits in one file (`sob.py`)  
- **linear** — no branching complexity or semantic inference  
- **modular** — dictionaries and reference files externalized  
- **deterministic** — identical input → identical output  
- **bounded** — only structural and semantic‑adjacent classification  
- **debuggable** — every behavior traceable to a small module  
- **expandable** — new lexical markers added without touching core logic  

The goal is that reading `sob.py` feels **unimpressive** — simple, predictable, and easy to maintain.

SOB is strictly **pre‑semantic** and **pre‑identity**.  
It consumes upstream metadata **read‑only**, and produces structural residue for downstream routing.

---

## **2. Directory Structure**

```
primitives/
  sob/
    sob.py                     # tiny execution core
    sob_dictionary.yaml        # morphological + lexical forms (SOB-owned)
    sob_punctuation.yaml       # punctuation rules (SOB-owned)
    sob_markers.yaml           # wh-markers, conditional markers (SOB-owned)
    sob_operators.yaml         # operator verbs (SOB-owned)

    sob_domains.yaml           # domain-hint markers (TP-read-only)
    sob_tones.yaml             # tone-hint markers (TP-read-only)
    sob_constraints.yaml       # constraint-hint markers (TP-read-only)
    sob_morphology.yaml        # morphology rules (TP-read-only or SOB-owned)

    sob_testbench.yaml         # deterministic tests
```

This structure ensures:

- SOB is **self‑contained**  
- SOB core remains **tiny**  
- debugging is **trivial**  
- expansion is **safe**  
- upstream/downstream boundaries remain intact  

---

## **3. SOB Core (`sob.py`)**

### **3.1 Responsibilities**

`sob.py` performs exactly six operations:

1. **Load dictionaries**  
2. **Segment TP**  
3. **Classify structural modality**  
4. **Extract structural‑adjacent hints**  
   - operator  
   - domain (TP‑read‑only)  
   - tone (TP‑read‑only)  
   - constraint (TP‑read‑only)  
   - discourse‑context (TP‑read‑only)  
5. **Form residue fragments**  
6. **Return structured TP + residue**

No semantic interpretation.  
No intent inference.  
No meaning resolution.  
No identity resolution.  
No continuity enforcement.  
No drift detection.  
No routing.  
No commit logic.

### **3.2 Execution Flow**

```
load_all_yaml_files()
tp_units = segment(tp)
modality = classify_modality(tp_units)
operators = extract_operator_hints(tp_units)
domains = extract_domain_hints(tp_units)        # TP-read-only
tones = extract_tone_hints(tp_units)            # TP-read-only
constraints = extract_constraint_hints(tp_units)# TP-read-only
discourse = extract_discourse_flags(tp_units)   # TP-read-only
residue = form_residue(tp_units, modality, operators, domains, tones, constraints, discourse)
return structured_tp, residue
```

This is the entire SOB core.  
It should fit in ~200 lines of code.

---

## **4. YAML Dictionary Files**

Each YAML file is:

- **tiny**  
- **bounded**  
- **non‑semantic**  
- **deterministic**  
- **easy to update**  
- **safe to expand**  

### **4.1 SOB‑Owned Dictionaries (Required)**

These files contain lexical forms SOB *must* use for structural classification.

#### **sob_dictionary.yaml**
Auxiliaries, modals, pronouns, determiners.

#### **sob_punctuation.yaml**
Sentence endings, list markers, block markers.

#### **sob_markers.yaml**
Wh‑markers, conditional markers.

#### **sob_operators.yaml**
Operator verbs.

These four files are **required** for SOB to satisfy 20.40.010.

---

# **4.2 TP‑Read‑Only Dictionaries (Required for SOB Tagging)**

These YAML files contain **lexical markers** that SOB uses to perform its specialized structural‑adjacent tagging.  
Upstream TP primitives (CEx, CE, Context Layer, Identity Layer, Semantic Layer) may already produce **semantic or contextual signals** such as tone, domain, or constraints, but they **do not** provide the lexical marker lists SOB requires for **lexical‑level tagging**.

Therefore, SOB must always load these dictionaries and perform its own tagging, regardless of upstream judgments.

### **How SOB Uses Upstream Signals**

- **Reuse** — SOB may reuse upstream semantic signals when they align with lexical markers.  
- **Affirmation** — SOB may use upstream signals to increase confidence in its own lexical tagging.  
- **Ignore** — SOB may ignore upstream signals if they are irrelevant to lexical structure.  
- **Override** — SOB may override upstream signals *inside SOB’s own residue* if its lexical logic disagrees.  
- **Never overwrite upstream fields** — SOB only overrides its own tagging, never upstream metadata.

Disagreement between SOB and upstream primitives is **allowed and informative**.  
TS debugging, replay determinism, and routing benefit from having **two independent reference points**: upstream semantic/contextual signals and SOB lexical/structural signals.

### **Files Treated as TP‑Read‑Only (Required for SOB Tagging)**

These dictionaries are **required** for SOB’s lexical tagging.  
SOB loads them every turn and treats their contents as **TP‑read‑only**, meaning SOB does not compute or enforce semantic meaning — only lexical tagging.

#### **sob_domains.yaml**  
Lexical domain markers (math‑like, code‑like, legal‑like, technical‑like).

#### **sob_tones.yaml**  
Lexical tone markers (formal, casual, urgent).

#### **sob_constraints.yaml**  
Lexical constraint markers (precision, conciseness, politeness).

#### **sob_morphology.yaml**  
Morphology rules (suffixes, infinitive markers).  
May be SOB‑owned or TP‑read‑only depending on design.

### **Purpose**

These dictionaries allow SOB to produce **structural‑adjacent residue** even when upstream components have already produced semantic/contextual signals.  
SOB’s residue is **lexical**, not semantic — and SOB must always perform its own tagging.

Upstream signals help SOB, but never replace SOB.

---

## **5. Why YAML Files Exist**

### **5.1 Modularity**  
SOB core stays tiny and readable.

### **5.2 Debuggability**  
If modality misclassifies, you check:

- segmentation  
- dictionary  
- classifier  

Three places.  
Not fifty.

### **5.3 Expandability**  
Adding new operator verbs or domain markers requires:

- editing a YAML file  
- running the testbench  

No core logic changes.

### **5.4 Determinism**  
YAML files are:

- versioned  
- explicit  
- stable  
- reproducible  

### **5.5 Safety**  
No semantic dictionary.  
Only structural forms.

---

## **6. Upstream Metadata Consumption (Non‑Duplicative)**

SOB consumes upstream metadata produced by:

- **IIInB**  
- **CEx**  
- **CE**  
- **Context Layer**  
- **Identity Layer**  
- **Continuity Layer**  
- **Semantic Layer**  
- **Routing Layer**

SOB treats all upstream metadata as **read‑only**:

- SOB does **not** re‑compute meaning  
- SOB does **not** re‑compute identity  
- SOB does **not** re‑compute continuity  
- SOB does **not** detect drift  
- SOB does **not** stabilize referents or commitments  
- SOB does **not** interpret freeze signatures  
- SOB does **not** compute semantic‑layer cues  
- SOB does **not** compute routing signals  

SOB only:

- reads upstream metadata  
- uses metadata to improve segmentation and hint extraction  
- encodes applicable metadata into residue  

---

## **7. Downstream Stability Boundaries (Non‑Duplicative)**

SOB must not duplicate downstream responsibilities handled by:

- **IdOB**  
- **MCB**  
- **DCB**  
- **TR**  
- **RB**  
- **OuBA**

SOB does **not**:

- freeze meaning  
- freeze identity  
- freeze commitments  
- enforce continuity  
- enforce identity constraints  
- compute semantic‑layer stability  
- compute curvature  
- compute routing vectors  
- compute commit eligibility  
- perform correction  
- perform inference  

SOB only produces structural residue for downstream routing.

---

## **8. Testbench (`sob_testbench.yaml`)**

The SOB testbench validates:

- segmentation  
- modality  
- operator hints  
- domain hints  
- tone hints  
- constraint hints  
- discourse‑context flags  

It should also validate:

- dictionary loading  
- dictionary coverage  
- dictionary determinism  
- dictionary expansion safety  

---

## **9. Summary**

The SOB software architecture is:

- **modular**  
- **dictionary‑driven**  
- **linear**  
- **bounded**  
- **deterministic**  
- **debuggable**  
- **expandable**  
- **non‑duplicative** (upstream + downstream)  
- **unimpressive** (in the best way)  

This architecture keeps SOB tractable, maintainable, and perfectly aligned with:

- **20.40.010_sob_prim.md**  
- **tp_path_a_map.md**  
- **tp_context_layer.md**  
- **tp_commit.md**

---

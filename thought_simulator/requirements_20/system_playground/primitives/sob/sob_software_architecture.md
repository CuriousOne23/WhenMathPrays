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

---

## **2. Directory Structure**

```
primitives/
  sob/
    sob.py                     # tiny execution core
    sob_dictionary.yaml        # morphological + lexical forms
    sob_punctuation.yaml       # punctuation rules
    sob_markers.yaml           # wh-markers, conditional markers
    sob_operators.yaml         # operator verbs
    sob_domains.yaml           # domain-hint lexical markers
    sob_tones.yaml             # tone-hint lexical markers
    sob_constraints.yaml       # constraint-hint lexical markers
    sob_morphology.yaml        # morphological rules
    sob_testbench.yaml         # deterministic tests
```

This structure ensures:

- SOB is **self‑contained**  
- all lexical resources are **local**  
- SOB core remains **tiny**  
- debugging is **trivial**  
- expansion is **safe**  

---

## **3. SOB Core (`sob.py`)**

### **3.1 Responsibilities**

`sob.py` performs exactly six operations:

1. **Load dictionaries**  
2. **Segment TP**  
3. **Classify structural modality**  
4. **Extract structural‑adjacent hints**  
   - operator  
   - domain  
   - tone  
   - constraint  
   - discourse‑context  
5. **Form residue fragments**  
6. **Return structured TP + residue**

No semantic interpretation.  
No intent inference.  
No meaning resolution.

### **3.2 Execution Flow**

```
load_all_yaml_files()
tp_units = segment(tp)
modality = classify_modality(tp_units)
operators = extract_operator_hints(tp_units)
domains = extract_domain_hints(tp_units)
tones = extract_tone_hints(tp_units)
constraints = extract_constraint_hints(tp_units)
discourse = extract_discourse_flags(tp_units)
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

### **4.1 sob_dictionary.yaml**  
Contains lexical forms needed for structural classification:

```yaml
auxiliaries:
  - is
  - are
  - was
  - were
  - do
  - does
  - did
  - has
  - have
  - had

modals:
  - can
  - could
  - would
  - should
  - might
  - may
  - must

pronouns:
  - it
  - they
  - this
  - that
  - these
  - those

determiners:
  - the
  - a
  - an
  - this
  - that
  - these
  - those
```

### **4.2 sob_punctuation.yaml**

```yaml
sentence_endings:
  - "."
  - "?"
  - "!"

list_markers:
  - "-"
  - "*"
  - "+"
```

### **4.3 sob_markers.yaml**

```yaml
wh_markers:
  - what
  - why
  - how
  - when
  - where
  - which
  - who

conditional_markers:
  - if
  - unless
  - provided
  - assuming
```

### **4.4 sob_operators.yaml**

```yaml
operators:
  - summarize
  - compare
  - classify
  - derive
  - plan
  - explain
  - rewrite
  - transform
```

### **4.5 sob_domains.yaml**

```yaml
domains:
  math_like:
    - theorem
    - lemma
    - proof
  code_like:
    - def
    - class
    - return
  narrative_like:
    - story
    - character
  legal_like:
    - hereby
    - pursuant
  technical_like:
    - system
    - module
```

### **4.6 sob_tones.yaml**

```yaml
tones:
  formal:
    - therefore
    - accordingly
  casual:
    - basically
    - kinda
  urgent:
    - immediately
    - asap
```

### **4.7 sob_constraints.yaml**

```yaml
constraints:
  precision:
    - exactly
    - strictly
  conciseness:
    - briefly
    - concise
  politeness:
    - please
    - kindly
```

### **4.8 sob_morphology.yaml**

```yaml
morphology:
  suffixes:
    third_person_singular: "s"
    past_tense: "ed"
    progressive: "ing"
  infinitive_marker: "to"
```

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

## **6. Testbench (`sob_testbench.yaml`)**

Your existing SOB testbench  already validates:

- segmentation  
- modality  
- operator hints  
- domain hints  
- tone hints  
- constraint hints  
- discourse‑context flags  

It should be extended to validate:

- dictionary loading  
- dictionary coverage  
- dictionary determinism  
- dictionary expansion safety  

---

## **7. Summary**

The SOB software architecture is:

- **modular**  
- **dictionary‑driven**  
- **linear**  
- **bounded**  
- **deterministic**  
- **debuggable**  
- **expandable**  
- **unimpressive** (in the best way)  

This is exactly the architecture required to make SOB tractable, maintainable, and aligned with your rewritten 20.40.010 spec.

---

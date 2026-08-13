# ⭐ **`sob_py_struc_pgm.md` (Version 1.0)**  
### *Python & C++ Implementation Blueprint for the SOB Primitive*  
### *Aligned with 20.40.010 (SOB Requirements), 20.105.*, 20.15, and the Thought Pipeline Description*

---

# **1. SOB’s Role in the Pipeline**

SOB is the **lexical‑structural tagging primitive** of Path‑A.  
It immediately follows TPU in the pipeline:

1. **CEx‑IE** — structural hints  
2. **CEx‑CCR** — alignment + decision  
3. **CEx‑Pck** — metadata packaging  
4. **CE** — canonical context envelope  
5. **TPU** — authoritative commit  
6. **SOB** — lexical tagging + structural residue

SOB is responsible for:

- loading **TP‑read‑only dictionaries**  
- performing **lexical tagging**  
- performing **structural segmentation**  
- applying **morphology normalization**  
- forming **sob_structural_map**  
- producing **sob_residue{}**  
- preserving **upstream semantic/context fields**  
- allowing **disagreement** with upstream primitives  
- writing only **SOB‑owned fields**  
- producing **sob_audit_record{}**

SOB consumes:

- committed TP(N+1) from TPU  
- context_fields  
- semantic_residue  
- semantic_importance  
- MSL metadata  
- CIL metadata  
- CCR output  
- provenance metadata  
- TP‑read‑only dictionaries:
  - sob_domains.yaml  
  - sob_tones.yaml  
  - sob_constraints.yaml  
  - sob_morphology.yaml  

SOB produces:

- sob_structural_map  
- sob_residue{}  
- sob_audit_record{}  

SOB does **not**:

- generate semantic meaning  
- interpret identity or continuity  
- modify upstream metadata  
- modify semantic_core  
- modify intake/context fields  
- perform routing  
- perform inference  
- overwrite upstream fields  
- collapse semantic signals into lexical signals

SOB is deterministic, bounded, replay‑safe, and the **sole lexical‑tagging authority** of Path‑A.

---

# **2. Public API (Python & C++)**

```python
sob = SOB(tp_input)
sob.process()
```

SOB SHALL populate or update the following TP envelopes/metadata:

### **SOB‑written fields**

- `TP.structural.sob_structural_map`  
- `TP.structural.sob_residue`  
- `TP.metadata.sob_audit_record`  

### Required method

```python
def process(self):
    # load dictionaries
    # perform segmentation
    # apply morphology
    # perform lexical tagging
    # form sob_structural_map
    # form sob_residue
    # produce audit record
    # return updated TP
```

---

# **3. Intake Model (Single Input)**

SOB receives **one** bounded input:

---

## **3.1 TP Input (Committed TP(N+1))**

SOB reads:

- semantic envelope  
- context envelope  
- context metadata  
- semantic_residue metadata  
- semantic_importance  
- MSL metadata  
- CIL metadata  
- CCR output  
- provenance metadata  
- structural metadata (read‑only)  
- freeze metadata (read‑only)  
- entropy metadata (read‑only)

SOB treats all TP fields as **read‑only** except:

- `TP.structural.sob_structural_map`  
- `TP.structural.sob_residue`  
- `TP.metadata.sob_audit_record`

---

# **4. Deterministic Rule Ordering**

SOB must apply operations in **exact order**:

1. Read TP(N+1)  
2. Load dictionaries  
3. Perform segmentation  
4. Apply morphology normalization  
5. Perform lexical tagging  
6. Form sob_structural_map  
7. Form sob_residue  
8. Produce sob_audit_record{}  
9. Emit deterministic TP(N+1)+SOB

This ordering ensures:

- replay determinism  
- Python/C++ parity  
- stable integration with SROB, CnOB, SmOB, ISc, TR, RB, IdOB

---

# **5. Lexical Tagging Normalization**

SOB normalizes lexical tagging using:

- TP‑read‑only dictionaries  
- morphology rules  
- segmentation rules  
- operator‑verb detection  
- domain/tone/constraint markers  
- override rules (SOB overrides only its own residue)  
- upstream‑signal reuse/affirmation/ignore rules

Normalization includes:

- stripping suffixes (`summarizing → summarize`)  
- detecting infinitive forms (`to classify`)  
- normalizing variants (`explained → explain`)  
- tagging lexical tone markers  
- tagging lexical domain markers  
- tagging lexical constraint markers  
- forming structural adjacency  
- forming residue fields

SOB does **not** interpret meaning.

---

# **6. SOB Residue Construction**

SOB constructs:

```
TP.structural.sob_structural_map {
    segments[]
    operators[]
    lexical_domains[]
    lexical_tones[]
    lexical_constraints[]
    morphology_flags[]
}
```

And:

```
TP.structural.sob_residue {
    lexical_tags[]
    structural_adjacent[]
    override_flags[]
    disagreement_flags[]
}
```

Rules:

- All fields must be deterministic  
- All fields must support replay  
- All fields must preserve provenance  
- All updates must follow writer‑authority rules  
- All updates must be bounded and lexical‑only  

Downstream consumers:

- SROB  
- CnOB  
- SmOB  
- ISc  
- TR  
- RB  
- IdOB

---

# **7. SOB Audit Record**

SOB produces an audit record containing:

- dictionary load status  
- segmentation decisions  
- morphology decisions  
- lexical tagging decisions  
- override decisions  
- disagreement flags  
- provenance lineage  
- sob_structural_map hash  
- sob_residue hash  
- timestamp

Audit record is read‑only for downstream primitives.

---

# **8. Forbidden Behavior**

SOB must not:

- generate meaning  
- interpret semantics  
- modify semantic_core  
- modify intake/context fields  
- modify routing metadata  
- modify identity metadata  
- modify freeze metadata  
- modify entropy metadata  
- infer meaning  
- use embeddings or global semantics  
- write outside SOB‑owned TP envelopes  
- overwrite upstream fields  
- collapse semantic signals into lexical signals

---

# **9. Implementation Skeleton (Python)**

```python
class SOB:
    def __init__(self, tp_input):
        self.tp = tp_input

    def process(self):
        # 1. Load dictionaries
        dicts = self._load_dictionaries()

        # 2. Segment text
        segments = self._segment(self.tp)

        # 3. Apply morphology
        normalized = self._apply_morphology(segments, dicts)

        # 4. Perform lexical tagging
        tags = self._lexical_tag(normalized, dicts)

        # 5. Build structural map
        structural_map = self._build_structural_map(tags)

        # 6. Build residue
        residue = self._build_residue(tags)

        # 7. Write SOB fields
        self.tp["structural"]["sob_structural_map"] = structural_map
        self.tp["structural"]["sob_residue"] = residue

        # 8. Produce audit record
        audit = self._build_audit_record(structural_map, residue)
        self.tp["metadata"]["sob_audit_record"] = audit

        return self.tp

    # Internal helpers:
    # _load_dictionaries
    # _segment
    # _apply_morphology
    # _lexical_tag
    # _build_structural_map
    # _build_residue
    # _build_audit_record
```

---

# **10. Implementation Skeleton (C++)**

```cpp
class SOB {
public:
    SOB(TP& tp_input) : tp(tp_input) {}

    TP process() {
        auto dicts = load_dictionaries();
        auto segments = segment(tp);
        auto normalized = apply_morphology(segments, dicts);
        auto tags = lexical_tag(normalized, dicts);

        auto structural_map = build_structural_map(tags);
        auto residue = build_residue(tags);

        tp.structural.sob_structural_map = structural_map;
        tp.structural.sob_residue = residue;

        tp.metadata.sob_audit_record = build_audit_record(structural_map, residue);

        return tp;
    }

private:
    TP& tp;

    // deterministic helper methods
};
```

---

# **11. Downstream Consumption Map (Normative)**

SOB writes:

- sob_structural_map  
- sob_residue  
- sob_audit_record{}  

Downstream consumers:

| Primitive | Consumes | Purpose |
|----------|----------|---------|
| **SROB** | sob_structural_map, sob_residue | structural refinement |
| **CnOB** | sob_structural_map | semantic geometry |
| **SmOB** | sob_structural_map | semantic geometry |
| **ISc** | sob_residue | scoring metadata |
| **TR/RB** | sob_residue | routing cues |
| **IdOB** | sob_residue | identity‑conditioned meaning |

SOB output must support deterministic replay and read‑only consumption.

---

# ⭐ **End of Document — `sob_py_struc_pgm.md` (Version 1.0)**

---.

# ⭐ **`wrdnm_py_struc_pgm.md` (Version 1.0)**  
### *Python & C++ Implementation Blueprint for the WrdNm Primitive*  
### *Aligned with 20.44, wrdnm_software_architecture.md, 20.15, 20.105, 20.108*

**Schema authority:** `wrdnm_schema.yaml`  
**Coupling authority:** TP structured‑field contract (20.44, 20.105)

---

# **1. WrdNm’s Role in the Pipeline**

```
TPU → SOB → SROB → CnOB → SmOB → SSG → TR/RB/IdOB → ISc → WrdNm → ISc (numeric scoring)
```

WrdNm is responsible for:

- loading **WrdNm‑owned** YAML dictionaries, scalar tables, and hash config  
- reading **structured TP fields** from upstream primitives  
- **Job 1:** deterministic categorical / boolean / scalar / hashed conversion  
- **Job 2:** assembling a numeric feature vector  
- writing `TP.wrdnm[]` (append‑only)  
- producing optional diagnostic records  

WrdNm does **not**: semantic interpretation, stance assignment, truth evaluation, referent identity, generative fill, scanning TP text, modifying metadata, or consuming CE / CCR / semantic‑importance / CIL metadata.

---

# **2. Public API**

```python
wrdnm = WrdNm(tp_input)
wrdnm.process()
```

### **WrdNm‑written fields**

- `TP.wrdnm[]` (numeric feature vector record)
- optional diagnostic keys under `TP.metadata.wrdnm_audit_record`

---

# **3. Intake Model and Coupling Discipline**

WrdNm consumes **structured TP fields only**, as defined in:

- IIInB / IE  
- CEx / CE  
- SOB / SROB  
- CnOB  
- SmOB  
- RB / TR / CTP  
- IdOB / MCB  

### **3.1 Normative coupling rules**

1. WrdNm **SHALL NOT** load upstream primitive YAMLs (`sob_*.yaml`, `srob_*.yaml`, `cnob_*.yaml`, `smob_*.yaml`).  
2. WrdNm **SHALL** depend solely on **TP field names** and **schema‑declared mapping types**.  
3. Missing expected fields → **TP defect**, not WrdNm inference.  
4. WrdNm **SHALL NOT** infer meaning, stance, truth, or referent identity.  
5. WrdNm **SHALL** treat all upstream TP fields as read‑only.

**Debug order:** TP(structured fields) → schema → WrdNm encode.

---

# **4. Deterministic Rule Ordering**

1. Read TP structured fields  
2. Load WrdNm YAML dictionaries  
3. Load scalar tables  
4. Load hash configuration  
5. Job 1: convert fields
   - categorical → float32 (fractional precision ≤ 1/1000)
   - boolean → 0/1
   - scalar → float32
   - hashed → uint32
6. Canonical ordering of numeric fields  
7. **Job 2:** assemble numeric feature vector  
8. Build diagnostic record  
9. Append new `TP.wrdnm[]` entry  
10. Emit TP

Ordering SHALL be identical in Python and C++.

---

# **5. Normative v1 Schemas**

## **5.1 Numeric entry**

```
numeric_entry:
  field: string          # TP field name
  value: int | float | uint
  mapping_type: categorical | boolean | scalar | hashed
  source: tp_field
  note: string           # optional machine note
```

## **5.2 `TP.wrdnm[]` (append‑only)**

Each WrdNm record SHALL contain:

```
wrdnm_record:
   surface_id: float32
   lemma_id: float32
   expression_id: float32
   
   temporal_id: float32
   causal_id: float32
   continuity_id: float32
   entity_id: float32
   thread_hash: uint32
   
   adjacency: int8
   ordering_id: float32
   structural_importance: float32
   
   constraint_family_id: float32
   constraint_importance: float32
   missing_slot: int8
   
   modality: float32
   affect: float32
   underspec: float32
   semantic_adjacent_importance: float32
   
   routing_id: float32
   transform_id: float32
   
   identity_id: float32
   next_context_id: float32

  provenance:
    origin: WrdNm
    last_update: WrdNm
    timestamp: iso8601
```

All categorical IDs SHALL be float32 values with fractional precision ≤ 1/1000 (nnn.xxx).
All numeric types SHALL match wrdnm_software_architecture.md.

## **5.3 Dictionary lookup**

```
n_i = dict[field_value] or 0
```

## **5.4 Scalar mapping**

```
f_i = scalar_map[field_value] or 0.0
```

## **5.5 Hash mapping**

```
H_i = hash32(field_string, seed)
```

## **5.6 Diagnostic record**

```
wrdnm_audit_record:
  dictionary_load_status: ok | partial | fail
  scalar_table_load_status: ok | partial | fail
  hash_config_status: ok | fail
  conversion_decisions: []
  missing_fields: []
  provenance_lineage:
    origin: WrdNm
    last_update: WrdNm
  timestamp: iso8601
```

---

# **6. v1 Conversion Behaviors**

### **6.1 Categorical**

- lookup in dictionary (float32 categorical ID, fractional precision ≤ 1/1000)
- fallback ID = `0.000`
- log missing key 

### **6.2 Boolean**

- `True → 1`  
- `False → 0`  

### **6.3 Scalar**

- lookup in scalar table  
- fallback = `0.0`  

### **6.4 Hashed**

- deterministic hash  
- fixed seed  
- uint32 output  

### **6.5 Canonical ordering**

All numeric fields SHALL be ordered exactly as defined in the schema.

---

# **7. Forbidden Behavior**

WrdNm must not:

- load upstream primitive YAMLs  
- infer meaning, stance, truth, referents  
- generative‑fill missing content  
- scan TP text or tokenize free‑form strings  
- modify upstream TP fields  
- write outside `TP.wrdnm[]`  
- consume CE metadata, CCR output, semantic‑importance, CIL metadata, semantic‑residue metadata  
- require other primitives to read diagnostic metadata  

---

# **8. Implementation Skeleton (Python)**

```python
class WrdNm:
    def __init__(self, tp_input):
        self.tp = tp_input

    def process(self):
        schema = self._load_schema()
        dicts = self._load_dictionaries()
        scalars = self._load_scalar_tables()
        hash_cfg = self._load_hash_config()

        numeric_fields = self._convert_fields(self.tp, schema, dicts, scalars, hash_cfg)
        record = self._assemble_record(numeric_fields)
        audit = self._build_audit_record(numeric_fields)

        self.tp.setdefault("wrdnm", [])
        self.tp["wrdnm"].append(record)

        self.tp.setdefault("metadata", {})
        self.tp["metadata"]["wrdnm_audit_record"] = audit

        return self.tp
```

---

# **9. Downstream Consumption**

| Primitive | Consumes | Purpose |
|-----------|----------|---------|
| **ISc** | numeric feature vector | scoring, ΔH%, candidate ranking |
| **TR / RB** | numeric fields | routing escalation, eligibility |
| **IdOB** | numeric fields | identity‑conditioned rails |
| **SSG** | numeric fields | structural signal integration |

WrdNm is the **sole numeric encoder** for ISc.

---

# **10. Locked Policies (W1–W9)**

| ID | Topic | Lock |
|----|--------|------|
| **W1** | Schema | `wrdnm_schema.yaml` authoritative |
| **W2** | Dictionaries | bounded, deterministic |
| **W3** | Scalars | bounded, deterministic |
| **W4** | Hash | fixed seed, deterministic |
| **W5** | Ordering | canonical numeric field order |
| **W6** | Write discipline | append‑only `TP.wrdnm[]` |
| **W7** | No inference | no semantic or generative behavior |
| **W8** | No upstream YAMLs | TP‑only coupling |
| **W9** | Replay | identical inputs → identical outputs |

---

# **11. Testbench Contract**

- Inputs: **TP structured fields** (`normalized_surface`, `lemma`, `temporal_marker`, etc.)  
- Expected: numeric feature vector matching schema  
- Minimum scenarios:
  1. clean categorical + scalar fields  
  2. missing dictionary keys → fallback IDs  
  3. missing scalar keys → fallback floats  
  4. hashed fields present → deterministic hash  
  5. boolean fields present → 0/1  
  6. routing + transform markers present → correct IDs  

---

# ⭐ **End of Document — `wrdnm_py_struc_pgm.md` (Version 1.0)**

---


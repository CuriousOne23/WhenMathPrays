# **wrdnm_software_architecture.md**  
**Location:**  
`thought_simulator/requirements_20/system_playground/primitives/wrdnm/wrdnm_software_architecture.md`  


---

# **WrdNm Software Architecture**  
**Audience:** Software engineers implementing or maintaining the WrdNm primitive  
**Purpose:** Provide a complete, deterministic, implementation‑ready description of WrdNm’s structure, modules, dictionaries, field groups, numeric ranges, formulas, and output semantics.

---

# **1. Overview**

WrdNm is the **Word‑to‑Numeric Encoder** used in Path‑A.  
Its job is simple and strict:

> **Convert structured TP fields into numeric feature values using bounded dictionaries, scalar tables, and deterministic hashing.**

WrdNm does **not** interpret meaning, does **not** perform NLP, and does **not** inspect raw text.  
It only converts **known fields** defined in the WrdNm schema.

WrdNm is **position‑agnostic**: it does not care where a field came from or how many times a primitive was invoked.

---

# **2. Core Responsibilities**

1. Load the WrdNm schema  
2. Load all dictionaries and scalar tables  
3. Read TP structured fields  
4. Convert each field to a numeric value  
5. Produce a numeric feature vector  
6. Write WrdNm‑owned output fields into the TP  
7. Never overwrite earlier WrdNm records  
8. Guarantee deterministic replay

---

# **3. Input Field Groups**

WrdNm consumes structured fields from upstream primitives.  
These fields are grouped by functional families.

## **3.1 Intake Fields (IIInB, IE)**

| Field | Description | Type |
|-------|-------------|------|
| `normalized_surface` | Normalized token surface | categorical |
| `lemma` | Lemma form | categorical |
| `expression_type` | Expression category | categorical |

## **3.2 Context Extraction Fields (CEx, CE)**

| Field | Description | Type |
|-------|-------------|------|
| `temporal_marker` | Past/present/future/etc. | categorical |
| `causal_marker` | Cause/effect markers | categorical |
| `continuity_status` | Same entity / new entity | categorical |
| `entity_reference` | Entity ID or tag | categorical |
| `thread_summary` | Summary of thread context | hashed |

## **3.3 Structural Fields (SOB, SROB)**

| Field | Description | Type |
|-------|-------------|------|
| `adjacency_flag` | Boolean adjacency | boolean |
| `ordering_marker` | Ordering category | categorical |
| `structural_importance` | Importance scalar | scalar |

## **3.4 Constraint Fields (CnOB)**

| Field | Description | Type |
|-------|-------------|------|
| `constraint_family` | Constraint category | categorical |
| `constraint_importance` | Importance scalar | scalar |
| `missing_slot_flag` | Boolean | boolean |

## **3.5 Semantic‑Adjacent Fields (SmOB)**

| Field | Description | Type |
|-------|-------------|------|
| `modality_cue` | Assertive / hypothetical / etc. | scalar |
| `affect_cue` | Emotional tone | scalar |
| `underspec_cue` | Underspecification level | scalar |
| `semantic_adjacent_importance` | Importance scalar | scalar |

## **3.6 Routing Fields (RB)**

| Field | Description | Type |
|-------|-------------|------|
| `routing_marker` | Continue / branch / escalate | categorical |

## **3.7 Transform Fields (TR, CTP)**

| Field | Description | Type |
|-------|-------------|------|
| `transform_marker` | Normalize / refine / adjust | categorical |

## **3.8 Identity & Next‑Context Fields (IdOB, MCB)**

| Field | Description | Type |
|-------|-------------|------|
| `identity_continuity_marker` | Same identity / new identity | categorical |
| `next_context_marker` | Next‑turn context | categorical |

---

# **4. Dictionaries and Scalar Tables (YAML)**

All dictionaries are stored as **YAML files**, not JSON.  
Each dictionary is a simple key→value mapping.

---

## **4.1 Categorical Dictionaries (YAML)**

Each dictionary is a YAML file containing string keys and integer values.

### **surface_dict.yaml**
```yaml
run: 104
walk: 105
jump: 106
```

### **lemma_dict.yaml**
```yaml
run: 22
walk: 23
jump: 24
```

### **expression_dict.yaml**
```yaml
verb_motion: 7
noun_entity: 8
adj_quality: 9
```

### **temporal_dict.yaml**
```yaml
past: 3
present: 4
future: 5
```

### **causal_dict.yaml**
```yaml
cause: 1
effect: 2
none: 0
```

### **continuity_dict.yaml**
```yaml
same_entity: 1
new_entity: 2
unknown: 0
```

### **constraint_family_dict.yaml**
```yaml
temporal_constraint: 12
causal_constraint: 13
identity_constraint: 14
```

### **routing_dict.yaml**
```yaml
continue: 2
branch: 3
escalate: 4
```

### **transform_dict.yaml**
```yaml
normalize: 4
refine: 5
adjust: 6
```

### **identity_dict.yaml**
```yaml
same: 1
new: 2
unknown: 0
```

### **next_context_dict.yaml**
```yaml
topic_shift: 3
topic_continue: 4
topic_close: 5
```

### **Numeric Type:**  
`int32`

### **Range:**  
`0–65535` (bounded by dictionary size)

---

## **4.2 Scalar Tables (YAML)**

Scalar tables map symbolic values to floats.

### **modality_scalars.yaml**
```yaml
assertive: 0.8
hypothetical: 0.4
question: 0.6
```

### **affect_scalars.yaml**
```yaml
neutral: 0.0
positive: 0.7
negative: -0.7
```

### **underspec_scalars.yaml**
```yaml
low: 0.2
medium: 0.5
high: 0.8
```

### **importance_scalars.yaml**
```yaml
low: 0.2
medium: 0.5
high: 0.9
```

### **Numeric Type:**  
`float32`

### **Range:**  
`0.0–1.0` (except affect, which may be −1.0–1.0)

---

## **4.3 Hash Configuration (YAML)**

### **hash_config.yaml**
```yaml
algorithm: murmur3_32
seed: 918273645
bit_width: 32
```

### **Hash Type:**  
`uint32`

### **Formula:**  

$$
H = \mathrm{murmur3\_32}(input\_string, seed)
$$

---

# ⭐ **5. WrdNm Schema (YAML)**

This is the file that tells the encoder exactly which fields to convert and how.

### **wrdnm_schema.yaml**
```yaml
fields:
  normalized_surface: categorical
  lemma: categorical
  expression_type: categorical

  temporal_marker: categorical
  causal_marker: categorical
  continuity_status: categorical
  entity_reference: categorical
  thread_summary: hashed

  adjacency_flag: boolean
  ordering_marker: categorical
  structural_importance: scalar

  constraint_family: categorical
  constraint_importance: scalar
  missing_slot_flag: boolean

  modality_cue: scalar
  affect_cue: scalar
  underspec_cue: scalar
  semantic_adjacent_importance: scalar

  routing_marker: categorical
  transform_marker: categorical

  identity_continuity_marker: categorical
  next_context_marker: categorical
```

---

# ⭐ **6. Output Format (YAML)**

WrdNm writes its output into the TP as YAML‑structured fields.

Example:

```yaml
wrdnm:
  - surface_id: 104
    lemma_id: 22
    expression_id: 7
    temporal_id: 3
    causal_id: 1
    continuity_id: 1
    entity_id: 55
    thread_hash: 91827364

    adjacency: 1
    ordering_id: 2
    structural_importance: 0.7

    constraint_family_id: 12
    constraint_importance: 0.5
    missing_slot: 0

    modality: 0.8
    affect: 0.0
    underspec: 0.2
    semantic_adjacent_importance: 0.5

    routing_id: 2
    transform_id: 4

    identity_id: 1
    next_context_id: 3
```

---

# ⭐ **7. Summary**

You now have:

- **YAML dictionaries**  
- **YAML scalar tables**  
- **YAML hash config**  
- **YAML schema**  
- **YAML output format**

This is exactly what a software engineer needs to implement WrdNm correctly.

If you want, I can now generate:

- `wrdnm_schema.yaml`  
- dictionary starter files  
- scalar table starter files  
- hash config starter  
- or the Python module skeleton (`wrdnm.py`)  

Just tell me what you want next.

---

# **5. Core Module Structure**

WrdNm is implemented as a single module:

```
wrdnm/
    wrdnm.py
    wrdnm_schema.yaml
    dictionaries/
    scalars/
    hash_config.json
```

## **5.1 wrdnm.py Responsibilities**

1. Load schema  
2. Load dictionaries  
3. Load scalar tables  
4. Load hash config  
5. Walk TP fields  
6. Convert each field  
7. Build numeric feature vector  
8. Write WrdNm output record  
9. Append record (never overwrite)

---

# **6. Conversion Logic**

## **6.1 Categorical Conversion**

$$
n_i = \mathrm{dict}(c_i)
$$

If missing:

- log warning  
- use fallback ID `0`

## **6.2 Boolean Conversion**

$$
b_i = 
\begin{cases}
1 & \text{if true} \\
0 & \text{if false}
\end{cases}
$$

## **6.3 Scalar Conversion**

$$
f_i = \mathrm{scalar\_map}(s_i)
$$

## **6.4 Hash Conversion**

$$
H_i = \mathrm{hash}(field\_string)
$$

---

# **7. Output Structure**

WrdNm writes:

```
TP.wrdnm[n] = {
    "surface_id": int,
    "lemma_id": int,
    "expression_id": int,
    "temporal_id": int,
    "causal_id": int,
    "continuity_id": int,
    "entity_id": int,
    "thread_hash": int,
    "adjacency": int,
    "ordering_id": int,
    "structural_importance": float,
    "constraint_family_id": int,
    "constraint_importance": float,
    "missing_slot": int,
    "modality": float,
    "affect": float,
    "underspec": float,
    "semantic_adjacent_importance": float,
    "routing_id": int,
    "transform_id": int,
    "identity_id": int,
    "next_context_id": int
}
```

### **Numeric Types:**

- IDs → `int32`  
- Booleans → `int8`  
- Scalars → `float32`  
- Hashes → `uint32`  

---

# **8. Downstream Usage (ISc)**

ISc consumes the numeric feature vector to compute:

- entropy  
- ΔH%  
- candidate scoring  
- routing escalation  
- COP evaluation  
- progressive lineup scoring  

WrdNm guarantees:

- stable numeric encoding  
- deterministic replay  
- no semantic leakage  
- no overwrites  
- no inference  

---

# **9. Error Handling**

- Missing dictionary entry → fallback ID `0`  
- Missing scalar entry → fallback `0.0`  
- Missing field → skip  
- Hash failure → fallback `0`  
- Schema mismatch → log error, skip field  

---

# **10. Implementation Notes**

- All dictionaries must be loaded once and cached  
- Hashing must use fixed seed  
- Output records must be append‑only  
- No mutation of upstream TP fields  
- No semantic interpretation  
- No free‑form text scanning  

---

# **End of Document — wrdnm_software_architecture.md**

---


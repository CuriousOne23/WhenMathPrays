# **wrdnm_software_architecture.md**  
**Location:**  
`thought_simulator/requirements_20/system_playground/primitives/wrdnm/wrdnm_software_architecture.md`  

---

# **1. Overview**

WrdNm is the **Word‑to‑Numeric Encoder** used in Path‑A. Its job is simple and strict:

> Convert structured TP fields into numeric feature values using bounded dictionaries, scalar tables, and deterministic hashing.

WrdNm does not interpret meaning, does not perform NLP, and does not inspect raw text. It only converts known fields defined in the WrdNm schema. WrdNm is position‑agnostic: it does not care where a field came from or how many times a primitive was invoked.

---

# **2. Core Responsibilities**

1. **Load schema:** Load the WrdNm schema (`wrdnm_schema.yaml`).
2. **Load resources:** Load all dictionaries, scalar tables, and hash configuration.
3. **Read TP fields:** Read structured TP fields from upstream primitives.
4. **Convert fields:** Convert each field to a numeric value according to the schema.
5. **Build feature vector:** Assemble a numeric feature vector for each TP instance.
6. **Write outputs:** Write WrdNm‑owned output fields into the TP envelope `TP.wrdnm[]`.
7. **Append‑only behavior:** Never overwrite earlier WrdNm records; always append.
8. **Deterministic replay:** Guarantee deterministic, replay‑safe numeric encoding.

---

# **3. Input Field Groups**

WrdNm consumes structured fields from upstream primitives, grouped by functional families.

## **3.1 Intake Fields (IIInB, IE)**

| Field                | Description               | Type        |
|----------------------|---------------------------|------------|
| `normalized_surface` | Normalized token surface  | categorical |
| `lemma`              | Lemma form                | categorical |
| `expression_type`    | Expression category       | categorical |

## **3.2 Context Extraction Fields (CEx, CE)**

| Field              | Description                         | Type        |
|--------------------|-------------------------------------|------------|
| `temporal_marker`  | Past/present/future/etc.            | categorical |
| `causal_marker`    | Cause/effect markers                | categorical |
| `continuity_status`| Same entity / new entity            | categorical |
| `entity_reference` | Entity ID or tag                    | categorical |
| `thread_summary`   | Summary of thread context           | hashed      |

## **3.3 Structural Fields (SOB, SROB)**

| Field                  | Description             | Type     |
|------------------------|-------------------------|---------|
| `adjacency_flag`       | Boolean adjacency       | boolean |
| `ordering_marker`      | Ordering category       | categorical |
| `structural_importance`| Importance scalar       | scalar  |

## **3.4 Constraint Fields (CnOB)**

| Field                  | Description             | Type     |
|------------------------|-------------------------|---------|
| `constraint_family`    | Constraint category     | categorical |
| `constraint_importance`| Importance scalar       | scalar  |
| `missing_slot_flag`    | Boolean                 | boolean |

## **3.5 Semantic‑Adjacent Fields (SmOB)**

| Field                         | Description                         | Type   |
|-------------------------------|-------------------------------------|--------|
| `modality_cue`                | Assertive / hypothetical / etc.    | scalar |
| `affect_cue`                  | Emotional tone                     | scalar |
| `underspec_cue`               | Underspecification level           | scalar |
| `semantic_adjacent_importance`| Importance scalar                  | scalar |

## **3.6 Routing Fields (RB)**

| Field            | Description                      | Type        |
|------------------|----------------------------------|------------|
| `routing_marker` | Continue / branch / escalate     | categorical |

## **3.7 Transform Fields (TR, CTP)**

| Field             | Description                     | Type        |
|-------------------|---------------------------------|------------|
| `transform_marker`| Normalize / refine / adjust     | categorical |

## **3.8 Identity & Next‑Context Fields (IdOB, MCB)**

| Field                      | Description                 | Type        |
|----------------------------|-----------------------------|------------|
| `identity_continuity_marker`| Same identity / new identity| categorical |
| `next_context_marker`      | Next‑turn context           | categorical |

---

# **4. Dictionaries and Scalar Tables (YAML)**

All dictionaries and scalar tables are stored as **YAML files**. Each dictionary is a simple key→value mapping.

## **4.1 Categorical Dictionaries**

Each dictionary maps string keys to integer IDs (`int32`).

- `surface_dict.yaml`
- `lemma_dict.yaml`
- `expression_dict.yaml`
- `temporal_dict.yaml`
- `causal_dict.yaml`
- `continuity_dict.yaml`
- `constraint_family_dict.yaml`
- `routing_dict.yaml`
- `transform_dict.yaml`
- `identity_dict.yaml`
- `next_context_dict.yaml`

Example:

```yaml
# surface_dict.yaml
run: 104
walk: 105
jump: 106
```

Numeric type: `int32`  
Range: `0–65535` (bounded by dictionary size)

## **4.2 Scalar Tables**

Scalar tables map symbolic values to floats (`float32`).

- `modality_scalars.yaml`
- `affect_scalars.yaml`
- `underspec_scalars.yaml`
- `importance_scalars.yaml`

Example:

```yaml
# modality_scalars.yaml
assertive: 0.8
hypothetical: 0.4
question: 0.6
```

Typical ranges:

- Modality, underspec, importance: `0.0–1.0`
- Affect: `-1.0–1.0`

## **4.3 Hash Configuration**

Hash configuration is stored in `hash_config.yaml`:

```yaml
algorithm: murmur3_32
seed: 918273645
bit_width: 32
```

Hash type: `uint32`  

Formula:

$$
H = \mathrm{murmur3\\_32}(input\\_string, seed)
$$

---

# **5. WrdNm Schema (YAML)**

The schema file `wrdnm_schema.yaml` defines which TP fields are converted and how.

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

# **6. Core Module Structure**

WrdNm is implemented as a single module:

```text
wrdnm/
    wrdnm.py
    wrdnm_schema.yaml
    dictionaries/
    scalars/
    hash_config.yaml
```

WrdNm writes into the TP envelope: `TP.wrdnm[]`.

## **6.1 wrdnm.py Responsibilities**

1. Load `wrdnm_schema.yaml`.
2. Load all categorical dictionaries.
3. Load all scalar tables.
4. Load `hash_config.yaml`.
5. Walk TP fields according to the schema.
6. Convert each field to its numeric representation.
7. Build the numeric feature vector.
8. Write a new `TP.wrdnm[n]` record.
9. Append records without overwriting earlier ones.

---

# **7. Conversion Logic**

## **7.1 Categorical Conversion**

For a categorical field value $c_i$:

$$
n_i = \mathrm{dict}(c_i)
$$

If the key is missing:

- log a warning, and  
- use fallback ID `0`.

## **7.2 Boolean Conversion**

For a boolean field:

$$
b_i =
\begin{cases}
1 & \text{if true} \\
0 & \text{if false}
\end{cases}
$$

## **7.3 Scalar Conversion**

For a scalar field value $s_i$:

$$
f_i = \mathrm{scalar\\_map}(s_i)
$$

If missing:

- log a warning, and  
- use fallback `0.0`.

## **7.4 Hash Conversion**

For hashed fields:

$$
H_i = \mathrm{hash}(field\\_string)
$$

Using the algorithm and seed from `hash_config.yaml`.

---

# **8. TP.wrdnm Envelope (Output Structure)**

WrdNm writes its numeric outputs into the TP envelope `TP.wrdnm[]`. Each invocation appends a new record:

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

Numeric types:

- IDs → `int32`
- Booleans → `int8`
- Scalars → `float32`
- Hashes → `uint32`

---

# **9. Downstream Usage (ISc)**

ISc consumes the numeric feature vectors from `TP.wrdnm[]` to compute:

- entropy and ΔH%,
- candidate scoring,
- routing escalation decisions,
- COP evaluation,
- progressive lineup scoring.

WrdNm guarantees:

- stable numeric encoding,
- deterministic replay,
- no semantic leakage,
- no overwrites,
- no inference or NLP.

---

# **10. Error Handling**

- Missing dictionary entry → fallback ID `0`.
- Missing scalar entry → fallback `0.0`.
- Missing field → skip conversion for that field.
- Hash failure → fallback `0`.
- Schema mismatch → log error and skip the affected field.

---

# **11. Implementation Notes**

- Load dictionaries, scalar tables, and hash config once and cache them.
- Use a fixed hash seed for deterministic replay.
- Ensure `TP.wrdnm[]` is append‑only; never overwrite previous records.
- Do not mutate upstream TP fields.
- Do not perform semantic interpretation or free‑form text scanning.
- Keep all mappings bounded and deterministic.

---

# **End of Document — wrdnm_software_architecture.md**
```

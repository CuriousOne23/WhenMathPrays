# ✅ **`ie_py_struc_pgm.md` — One‑Stop IE Programming Reference**  
### *Python & C++ Implementation Blueprint for the Intake Envelope Primitive (IE)*

This document is the **canonical programming blueprint** for implementing the **IE primitive** in Python or C++.  
It synchronizes the following authoritative sources:

- `ie.py` (implementation)   [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/primitives/ie/ie.py)  
- `ie_testbench.yaml` (expected behavior)   [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/ie_testbench.yaml)  
- `ie_testbench.py` (execution harness)   [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/ie_testbench.py)  
- `run.py` (pipeline runner)   [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/run.py)  
- `20.109_ie_prim.md` (formal primitive specification)   [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)  

Everything required to understand IE’s behavior, rule ordering, structural schema, repair integration, anomaly propagation, and deterministic replay constraints is here.

---

# 1. IE’s Role in the Pipeline

IE is the **Intake Envelope**, the **final pre‑semantic representation** of user input in Path‑A.  
It is produced **after IIInB** and **before CEx**.

IE receives:

- `IIInB_Output.normalized`  
- `IIInB_Output.tokens`  
- `IIInB_Output.repair_operations`  
- `IIInB_Output.anomaly_flags`  

IE produces:

- `IE.intake.normalized_text`  
- `IE.intake.tokens`  
- `IE.structure.tags`  
- `IE.metadata.repair_annotations`  
- `IE.metadata.replay`  
- `IE.error` (deterministic envelope)

IE is:

- **pre‑semantic**  
- **deterministic**  
- **replay‑safe**  
- **bounded**  
- **structurally validated**  
- **non‑inferential**  

IE ensures downstream modules (CEx → CE → ISc → TPU) receive **clean, normalized, structurally stable, replay‑equivalent input**.  
  [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)

---

# 2. Public API (Python & C++)

The testbench invokes IE exactly like this:

```python
ie = IE(iiinb_output)
ie.inspect()
```

IE must expose:

### Required fields

- `intake.normalized_text`
- `intake.tokens`
- `structure.tags`
- `metadata.repair_annotations`
- `metadata.replay`
- `error`

### Required method

```python
def inspect(self):
    # populate all IE fields deterministically
```

### Required behavior

- IE **must not** perform semantic inference.  
- IE **must not** modify IIInB’s repair proposals.  
- IE **must not** reorder tokens.  
- IE **must** surface anomaly provenance into `TP.repairs[]` (HLR‑20.109‑016).  
    [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)

---

# 3. Intake Model

IE receives the fully normalized IIInB output:

```python
normalized = iiinb_output.normalized
tokens = iiinb_output.tokens
repairs = iiinb_output.repair_operations
anomalies = iiinb_output.anomaly_flags
```

Rules:

- IE **must apply** all IIInB repairs to produce `IE.intake.normalized_text`.  
- IE **must preserve** token boundaries exactly.  
- IE **must surface** anomalies into `repair_annotations`.  
- IE **must not** reinterpret or re‑tokenize input.  
  [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)

---

# 4. Deterministic Rule Ordering  
### (Enforced by `ie_testbench.yaml`)

IE must apply its operations in **exactly this order**:

1. **Receive IIInB normalized surface**  
2. **Apply IIInB repairs deterministically**  
3. **Construct normalized token sequence**  
4. **Build structural tags**  
5. **Integrate repair annotations**  
6. **Surface anomaly provenance**  
7. **Construct replay metadata**  
8. **Validate schema**  
9. **Emit deterministic error envelope if malformed**

This ordering is required for deterministic replay and matches all IE testbench expectations.  
  [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/ie_testbench.yaml)

---

# 5. Repair Integration

IE must incorporate **all** IIInB repair proposals **without modification**:

```python
{
    "type": "<rule>",
    "target": "<surface substring>",
    "proposal": "<replacement>"
}
```

IE must:

- apply repairs to produce `IE.intake.normalized_text`  
- annotate repaired spans in `IE.metadata.repair_annotations`  
- preserve ordering of repairs  
  [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)

IE must **not**:

- merge repairs  
- reinterpret repairs  
- drop repairs  
- reorder repairs  

---

# 6. Anomaly Propagation

IE must surface IIInB anomaly flags into `TP.metadata.repair_annotations`:

{
    "kind": "anomaly",
    "type": "<anomaly_type>",
    "target": "<char>",
    "location": <index>
}

IE must:

- preserve anomaly order  
- preserve anomaly location  
- surface anomalies as provenance entries in `TP.metadata.repair_annotations`  
- ensure deterministic propagation downstream  

This satisfies **HLR‑20.109‑016** in the TP‑aligned IE specification.

---

# 7. Structural Schema

IE must produce the canonical schema:

```
IE {
    intake: {
        tokens: [Token],
        normalized_text: string
    },
    structure: {
        tags: [StructuralTag],
        spans: [Span],
        markup: [MarkupIndicator]
    },
    metadata: {
        repair_annotations: [RepairAnnotation],
        replay: ReplayMetadata,
        ruleset_id: string
    },
    error: IEError | null
}
```

  [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)

IE must validate this schema before passing output to CEx.

---

# 8. Token Normalization

IE must:

- preserve IIInB token boundaries  
- apply whitespace normalization deterministically  
- integrate repairs into token sequence  
- produce canonical token list in `IE.intake.tokens`  

IE must not:

- re‑tokenize  
- drop tokens  
- infer semantic boundaries  

  [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)

---

# 9. Structural Integrity

IE must:

- validate structural tags  
- validate spans  
- validate markup indicators  
- reject malformed structures  
- produce deterministic error envelope in `IE.error`  

  [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)

---

# 10. Replay Metadata

IE must encode all information required for deterministic replay:

- repair operations  
- structural tags  
- token boundaries  
- normalization metadata  
- ruleset identifiers  

Replay systems must be able to reconstruct the exact input state without external context.  
  [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)

---

# 11. Forbidden Behavior

IE must not:

- infer meaning  
- perform semantic casing  
- reorder tokens  
- drop tokens  
- reinterpret repairs  
- generate nondeterministic metadata  
- access CEx, CE, ISc, TPU, TP.semantic  

  [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)

---

# 12. Implementation Skeleton (Python)

```python
class IE:
    def __init__(self, iiinb_output):
        self._src = iiinb_output
        self.intake = {}
        self.structure = {}
        self.metadata = {}
        self.error = None

    def inspect(self):
        # 1. Receive IIInB output
        normalized = self._src.normalized
        tokens = self._src.tokens
        repairs = self._src.repair_operations
        anomalies = self._src.anomaly_flags

        # 2. Apply repairs
        applied = apply_repairs(normalized, repairs)

        # 3. Build intake
        self.intake["normalized_text"] = applied
        self.intake["tokens"] = tokens

        # 4. Build structure
        self.structure["tags"] = build_structural_tags(tokens)

        # 5. Repair annotations
        self.metadata["repair_annotations"] = annotate_repairs(repairs)

        # 6. Anomaly propagation
        self.metadata["repair_annotations"] += surface_anomalies(anomalies)

        # 7. Replay metadata
        self.metadata["replay"] = build_replay_metadata(tokens, repairs)

        # 8. Schema validation
        self.error = validate_ie_schema(self)

        return self
```

This skeleton matches the behavior tested in `ie_testbench.py`.  
  [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/ie_testbench.py)

---

# 13. Implementation Skeleton (C++)

Equivalent structure:

- `class IE`  
- constructor receives IIInB output  
- `inspect()` populates:  
  - `intake.normalized_text`  
  - `intake.tokens`  
  - `structure.tags`  
  - `metadata.repair_annotations`  
  - `metadata.replay`  
  - `error`

All rule logic mirrors Python version.

---

# 14. Change Management

When IE evolves:

- update rule ordering deterministically  
- update testbench expectations  
- update this document  
- update `20.109_ie_prim.md`  
- ensure replay metadata remains stable  
- ensure anomaly provenance remains deterministic  

This document is the **authoritative programming reference** for IE.

---

# 15. Reference Documents (Canonical IE Synchronization Set)

To safely modify IE without breaking determinism, replayability, or testbench alignment, the following documents form the complete, synchronized contract:

1. **ie_py_struc_pgm.md** — programming blueprint  
2. **20.109_ie_prim.md** — conceptual spec   [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.109_ie_prim.md)  
3. **ie_testbench.yaml** — expected behavior   [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/ie_testbench.yaml)  
4. **ie_testbench.py** — execution harness   [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/ie_testbench.py)  
5. **ie.py** — implementation logic   [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/primitives/ie/ie.py)  
6. **run.py** — pipeline runner   [github.com](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/run.py)  

These documents define the **complete IE universe**.

---

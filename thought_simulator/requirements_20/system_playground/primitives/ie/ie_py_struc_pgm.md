# ⭐ **`ie_py_struc_pgm.md` — One‑Stop IE Programming Reference (Version 3.2)**  
### *Python & C++ Implementation Blueprint for the Intake Envelope Primitive (IE)*  
### *Aligned with 20.109 Version 3.2 (Model‑A, IIInB v3.2)*

This document is the **canonical programming blueprint** for implementing the **IE primitive** in Python or C++.  
It synchronizes the following authoritative sources:

- `ie.py` (implementation)  
- `ie_testbench.yaml` (expected behavior)  
- `ie_testbench.py` (execution harness)  
- `run.py` (pipeline runner)  
- `20.109_ie_prim.md` (formal primitive specification, Version 3.2)  

Everything required to implement IE’s behavior, rule ordering, structural schema, repair integration, anomaly propagation, token‑level normative classification, composite merge behavior, dictionary validation, and deterministic replay constraints is here.

---

# **1. IE’s Role in the Pipeline**

IE is the **Intake Envelope**, the **first committed intake constructor** and **first mild‑semantic primitive** in Path‑A.

IE receives IIInB’s output:

- canonicalized surface  
- raw IIInB tokens  
- deterministic repair proposals  
- anomaly flags  
- IIInB metadata  

IE produces:

- committed normalized surface  
- committed IE tokens (`ie_tokens`)  
- token‑level normative classification (`token_flags`)  
- structural tags, spans, markup  
- repair provenance  
- anomaly provenance  
- replay metadata  
- deterministic error envelope  

IE is:

- deterministic  
- rule‑driven  
- replay‑safe  
- bounded  
- structurally validated  
- non‑inferential  
- meaning‑adjacent but not meaning‑inferential  

IE ensures downstream primitives (CEx → CE → ISc → TPU) receive **clean, normalized, structurally stable, replay‑equivalent input**.

---

# **2. Public API (Python & C++)**

The testbench invokes IE exactly like this:

```python
ie = IE(iiinb_output)
ie.inspect()
```

IE must expose:

### Required fields

- `intake.normalized_text`  
- `intake.ie_tokens`  
- `intake.token_flags`  
- `structure.tags`  
- `structure.spans`  
- `structure.markup`  
- `metadata.repair_annotations`  
- `metadata.replay`  
- `error`  

### Required method

```python
def inspect(self):
    # populate all IE fields deterministically
```

### Required behavior

IE:

- applies IIInB repairs deterministically  
- performs composite merges when repairs require them  
- validates dictionary entries for merged tokens  
- constructs committed normalized surface  
- constructs committed IE tokens  
- classifies each token using rule‑driven behavior  
- surfaces anomaly provenance  
- preserves IIInB token order except where repairs modify spans  
- follows rule‑driven normalization and spacing  
- constructs structure deterministically  
- produces replay metadata  
- validates schema  
- emits deterministic error envelope when malformed  

IE does **not**:

- infer meaning  
- reinterpret IIInB repairs  
- invent repairs  
- re‑tokenize  
- drop tokens unless rule‑driven  
- perform normalization not proposed by IIInB  
- access downstream primitives  

---

# **3. Intake Model**

IE receives IIInB output:

```python
surface      = iiinb_output.surface
tokens       = iiinb_output.tokens          # raw IIInB tokens
repairs      = iiinb_output.repair_proposals
anomalies    = iiinb_output.anomaly_flags
iiinb_meta   = iiinb_output.metadata.iiinb
```

IE must:

- apply all IIInB repairs  
- perform composite merges when repairs require merging tokens  
- validate dictionary entries for merged tokens  
- apply unicode normalization only when IIInB proposes it  
- apply repetition collapse only when IIInB proposes it  
- remove illegal characters only when IIInB proposes it  
- mark malformed tokens and `no_entry` tokens as anomalous  
- preserve IIInB token order except where repairs modify spans  
- classify tokens using rule‑driven behavior  
- construct committed normalized surface  
- construct committed IE tokens  
- surface anomaly provenance  
- construct structure deterministically  
- encode replay metadata  

---

# **4. Deterministic Rule Ordering**  
### (Enforced by `ie_testbench.yaml`)

IE must apply its operations in **exactly this order**:

1. Receive IIInB surface + tokens + repairs + anomalies  
2. Apply IIInB repairs deterministically  
3. Perform composite merges when required  
4. Validate dictionary entries for merged tokens  
5. Construct committed normalized_text  
6. Construct committed IE tokens  
7. Construct token_flags (normative classification)  
8. Build structural tags, spans, markup  
9. Integrate repair annotations  
10. Surface anomaly provenance  
11. Construct replay metadata  
12. Validate schema  
13. Emit deterministic error envelope if malformed  

This ordering is required for deterministic replay.

---

# **5. Repair Integration (Updated for v3.2)**

IE incorporates **all** IIInB repair proposals **without modification**:

```python
{
    "rule_id": "<identifier>",
    "span": "<token indices>",
    "replacement": "<replacement text>"
}
```

IE must:

- apply repairs exactly  
- perform composite merges when replacement spans cover multiple tokens  
- validate dictionary entries for merged tokens  
- apply unicode normalization only when IIInB proposes it  
- apply repetition collapse only when IIInB proposes it  
- remove illegal characters only when IIInB proposes it  
- annotate repaired spans in `metadata.repair_annotations`  
- preserve repair ordering  

IE must not:

- merge repairs  
- reinterpret repairs  
- drop repairs  
- reorder repairs  
- invent normalization  

---

# **6. Anomaly Propagation (Updated for v3.2)**

IE surfaces IIInB anomaly flags into `metadata.repair_annotations`:

```json
{
    "kind": "anomaly",
    "type": "<anomaly_type>",
    "target": "<char or token>",
    "location": <index>
}
```

IE must:

- preserve anomaly order  
- preserve anomaly location  
- classify token_flags accordingly  
- surface anomalies as provenance entries  
- handle new anomaly types:  
  - `no_entry`  
  - `malformed_token`  
  - `illegal_character.*`  
  - `unicode_anomaly`  
  - `repetition_pattern`  
- ensure deterministic propagation downstream  

---

# **7. Token‑Level Normative Classification (Updated for v3.2)**

IE produces:

```json
IE.intake.token_flags = [
    "normative",
    "repaired",
    "anomalous",
    "unrecognized",
    "null"
]
```

Classification rules:

- normative → valid dictionary entry, no anomalies  
- repaired → token modified by IIInB repair  
- anomalous → token flagged by IIInB anomaly  
- unrecognized → token not in dictionary and not repaired  
- null → structural or placeholder tokens  

IE must classify tokens based on:

- repair proposals  
- anomaly flags  
- dictionary validation  
- composite merge results  
- unicode normalization repairs  
- repetition collapse repairs  
- illegal character removal repairs  

Downstream primitives use:

- `ie_tokens` + `token_flags` as the **primary machine substrate**  
- `normalized_text` only for structural geometry, replay, and debugging  

---

# **8. Structural Schema (Updated for v3.2)**

IE produces:

```
IE {
    intake: {
        ie_tokens: [Token],
        token_flags: [TokenFlag],
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

IE constructs structure:

- exclusively from IIInB structural tags  
- plus deterministic IE structural rules  
- without semantic inference  

---

# **9. Token Normalization (Updated for v3.2)**

IE must:

- preserve IIInB token order except where repairs modify spans  
- apply whitespace normalization only when rule‑driven  
- apply spacing between tokens only when rule‑driven  
- integrate repairs into committed IE tokens  
- produce canonical committed token list  

IE must not:

- re‑tokenize  
- drop tokens unless rule‑driven  
- infer semantic boundaries  

---

# **10. Structural Integrity (Updated for v3.2)**

IE must:

- validate structural tags  
- validate spans  
- validate markup indicators  
- reject malformed structures  
- produce deterministic error envelope  

IE constructs structure exclusively from:

- IIInB structural tags  
- deterministic IE structural rules  

---

# **11. Replay Metadata (Updated for v3.2)**

IE encodes all information required for deterministic replay:

- repair operations  
- anomaly propagation  
- composite merge provenance  
- dictionary validation provenance  
- structural tags  
- token boundaries  
- token_flags  
- normalization metadata  
- ruleset identifiers  

Replay systems must reconstruct the exact input state without external context.

---

# **12. Forbidden Behavior**

IE must not:

- infer meaning  
- perform semantic casing  
- reorder tokens except where repairs require it  
- drop tokens unless rule‑driven  
- reinterpret repairs  
- generate nondeterministic metadata  
- access CEx, CE, ISc, TPU, TP.semantic  

---

# **13. Implementation Skeleton (Python, Updated for v3.2)**

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
        surface   = self._src.surface
        tokens    = self._src.tokens
        repairs   = self._src.repair_proposals
        anomalies = self._src.anomaly_flags

        # 2. Apply repairs (including composite merges)
        committed_surface, committed_tokens = apply_repairs_and_merges(
            surface, tokens, repairs
        )

        # 3. Dictionary validation for merged tokens
        committed_tokens = validate_dictionary(committed_tokens)

        # 4. Build intake
        self.intake["normalized_text"] = committed_surface
        self.intake["ie_tokens"] = committed_tokens

        # 5. Token-level normative classification
        self.intake["token_flags"] = classify_tokens(
            committed_tokens, anomalies, repairs
        )

        # 6. Build structure deterministically
        self.structure["tags"]   = build_structural_tags(committed_tokens)
        self.structure["spans"]  = build_spans(committed_tokens)
        self.structure["markup"] = build_markup(committed_tokens)

        # 7. Repair annotations
        self.metadata["repair_annotations"] = annotate_repairs(repairs)

        # 8. Anomaly propagation
        self.metadata["repair_annotations"] += surface_anomalies(anomalies)

        # 9. Replay metadata
        self.metadata["replay"] = build_replay_metadata(
            committed_tokens, repairs, anomalies
        )

        # 10. Schema validation
        self.error = validate_ie_schema(self)

        return self
```

---

# **14. Implementation Skeleton (C++, Updated for v3.2)**

Equivalent structure:

- `class IE`  
- constructor receives IIInB output  
- `inspect()` populates all IE fields  
- composite merges + dictionary validation  
- rule‑driven classification  
- deterministic structural construction  
- replay metadata generation  

---

# **15. Change Management**

When IE evolves:

- update rule ordering  
- update testbench expectations  
- update this document  
- update `20.109_ie_prim.md`  
- ensure replay metadata remains stable  
- ensure anomaly provenance remains deterministic  
- ensure token_flags remain aligned with downstream consumption  

This document is the **authoritative programming reference** for IE v3.2.

---

# **16. Reference Documents (Canonical IE Synchronization Set)**

1. **ie_py_struc_pgm.md** — programming blueprint  
2. **20.109_ie_prim.md** — conceptual spec  
3. **ie_testbench.yaml** — expected behavior  
4. **ie_testbench.py** — execution harness  
5. **ie.py** — implementation logic  
6. **run.py** — pipeline runner  

These documents define the **complete IE universe**.

---

# ✅ **`ie_py_struc_pgm.md` — One‑Stop IE Programming Reference (Version 3.1)**  
### *Python & C++ Implementation Blueprint for the Intake Envelope Primitive (IE)*  
### *Aligned with 20.109 Version 3.1 (Model A)*

This document is the **canonical programming blueprint** for implementing the **IE primitive** in Python or C++.  
It synchronizes the following authoritative sources:

- `ie.py` (implementation)  
- `ie_testbench.yaml` (expected behavior)  
- `ie_testbench.py` (execution harness)  
- `run.py` (pipeline runner)  
- `20.109_ie_prim.md` (formal primitive specification)  

Everything required to understand IE’s behavior, rule ordering, structural schema, repair integration, anomaly propagation, token‑level normative classification, and deterministic replay constraints is here.

---

# 1. IE’s Role in the Pipeline

IE is the **Intake Envelope**, the **final pre‑semantic** and **first mild‑semantic** primitive in Path‑A.

IE is the **boundary between human input and machine‑efficient representation**.

IE receives:

- `IIInB_Output.surface`  
- `IIInB_Output.tokens`  
- `IIInB_Output.repair_proposals`  
- `IIInB_Output.anomaly_flags`  
- `IIInB_Output.metadata.iiinb`  

IE produces:

- `IE.intake.normalized_text`  
- `IE.intake.tokens`  
- `IE.intake.token_flags`  
- `IE.structure.tags`  
- `IE.structure.spans`  
- `IE.structure.markup`  
- `IE.metadata.repair_annotations`  
- `IE.metadata.replay`  
- `IE.error`  

IE is:

- **deterministic**  
- **rule‑driven**  
- **replay‑safe**  
- **bounded**  
- **structurally validated**  
- **non‑inferential**  
- **meaning‑adjacent but not meaning‑inferential**  

IE ensures downstream modules (CEx → CE → ISc → TPU) receive **clean, normalized, structurally stable, replay‑equivalent input**.

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

- IE **must not** perform semantic inference.  
- IE **must not** modify IIInB’s repair proposals.  
- IE **must not** reorder tokens.  
- IE **must** classify each token as normative, repaired, anomalous, unrecognized, or null.  
- IE **must** surface anomaly provenance.  
- IE **must** apply IIInB repairs deterministically.  
- IE **must** follow rule‑driven behavior defined in `ie_rules.yaml`.

---

# 3. Intake Model

IE receives IIInB output:

```python
surface      = iiinb_output.surface
tokens       = iiinb_output.tokens
repairs      = iiinb_output.repair_proposals
anomalies    = iiinb_output.anomaly_flags
iiinb_meta   = iiinb_output.metadata.iiinb
```

Rules:

- IE **must apply** all IIInB repairs to produce `IE.intake.normalized_text`.  
- IE **must preserve** token boundaries except where repairs modify them.  
- IE **must classify** each token using rule‑driven behavior.  
- IE **must surface** anomalies into `repair_annotations`.  
- IE **must not** reinterpret or re‑tokenize input.  
- IE **must not** infer meaning.  
- IE **must** follow rule‑driven normalization and spacing.

---

# 4. Deterministic Rule Ordering  
### (Enforced by `ie_testbench.yaml`)

IE must apply its operations in **exactly this order**:

1. **Receive IIInB surface + tokens + repairs + anomalies**  
2. **Apply IIInB repairs deterministically**  
3. **Construct committed normalized_text**  
4. **Construct committed tokens**  
5. **Construct token_flags (normative classification)**  
6. **Build structural tags, spans, markup**  
7. **Integrate repair annotations**  
8. **Surface anomaly provenance**  
9. **Construct replay metadata**  
10. **Validate schema**  
11. **Emit deterministic error envelope if malformed**

This ordering is required for deterministic replay.

---

# 5. Repair Integration

IE must incorporate **all** IIInB repair proposals **without modification**:

```python
{
    "rule_id": "<identifier>",
    "span": "<token indices>",
    "replacement": "<replacement text>"
}
```

IE must:

- apply repairs to produce `IE.intake.normalized_text`  
- update tokens if repair modifies token boundaries  
- annotate repaired spans in `IE.metadata.repair_annotations`  
- preserve ordering of repairs  

IE must **not**:

- merge repairs  
- reinterpret repairs  
- drop repairs  
- reorder repairs  

---

# 6. Anomaly Propagation

IE must surface IIInB anomaly flags into `TP.metadata.repair_annotations`:

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
- ensure deterministic propagation downstream  

---

# 7. Token‑Level Normative Classification

IE must produce:

```json
IE.intake.token_flags = ["normative", "repaired", "anomalous", "unrecognized", "null"]
```

Rules:

- classification is **rule‑driven** via `ie_rules.yaml`  
- IE must not drop tokens unless rule says so  
- IE must not infer meaning  
- IE must not invent corrections  
- IE must not expand shorthand unless IIInB proposes it  
- IE must not correct spelling unless IIInB proposes it  

Downstream primitives use:

- `tokens` + `token_flags` as the **primary machine substrate**  
- `normalized_text` only for structural geometry, replay, and debugging

---

# 8. Structural Schema

IE must produce:

```
IE {
    intake: {
        tokens: [Token],
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

IE must validate this schema before passing output to CEx.

---

# 9. Token Normalization

IE must:

- preserve IIInB token boundaries  
- apply whitespace normalization **only if rule says so**  
- apply spacing between tokens **only if rule says so**  
- integrate repairs into token sequence  
- produce canonical token list  

IE must not:

- re‑tokenize  
- drop tokens unless rule says so  
- infer semantic boundaries  

---

# 10. Structural Integrity

IE must:

- validate structural tags  
- validate spans  
- validate markup indicators  
- reject malformed structures  
- produce deterministic error envelope  

---

# 11. Replay Metadata

IE must encode all information required for deterministic replay:

- repair operations  
- anomaly propagation  
- structural tags  
- token boundaries  
- token_flags  
- normalization metadata  
- ruleset identifiers  

Replay systems must reconstruct the exact input state without external context.

---

# 12. Forbidden Behavior

IE must not:

- infer meaning  
- perform semantic casing  
- reorder tokens  
- drop tokens unless rule says so  
- reinterpret repairs  
- generate nondeterministic metadata  
- access CEx, CE, ISc, TPU, TP.semantic  

---

# 13. Implementation Skeleton (Python)

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

        # 2. Apply repairs
        committed_surface = apply_repairs(surface, repairs)

        # 3. Build intake
        self.intake["normalized_text"] = committed_surface
        self.intake["tokens"] = tokens

        # 4. Token-level normative classification
        self.intake["token_flags"] = classify_tokens(tokens, anomalies, repairs)

        # 5. Build structure
        self.structure["tags"]   = build_structural_tags(tokens)
        self.structure["spans"]  = build_spans(tokens)
        self.structure["markup"] = build_markup(tokens)

        # 6. Repair annotations
        self.metadata["repair_annotations"] = annotate_repairs(repairs)

        # 7. Anomaly propagation
        self.metadata["repair_annotations"] += surface_anomalies(anomalies)

        # 8. Replay metadata
        self.metadata["replay"] = build_replay_metadata(tokens, repairs, anomalies)

        # 9. Schema validation
        self.error = validate_ie_schema(self)

        return self
```

---

# 14. Implementation Skeleton (C++)

Equivalent structure:

- `class IE`  
- constructor receives IIInB output  
- `inspect()` populates all IE fields  
- rule‑driven behavior mirrors Python version  

---

# 15. Change Management

When IE evolves:

- update rule ordering  
- update testbench expectations  
- update this document  
- update `20.109_ie_prim.md`  
- ensure replay metadata remains stable  
- ensure anomaly provenance remains deterministic  
- ensure token_flags remain aligned with downstream consumption  

This document is the **authoritative programming reference** for IE.

---

# 16. Reference Documents (Canonical IE Synchronization Set)

1. **ie_py_struc_pgm.md** — programming blueprint  
2. **20.109_ie_prim.md** — conceptual spec  
3. **ie_testbench.yaml** — expected behavior  
4. **ie_testbench.py** — execution harness  
5. **ie.py** — implementation logic  
6. **run.py** — pipeline runner  

These documents define the **complete IE universe**.

---

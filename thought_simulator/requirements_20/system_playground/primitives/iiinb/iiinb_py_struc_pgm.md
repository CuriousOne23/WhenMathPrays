# ✅ **REWRITTEN `iiinb_py_struc_pgm.md` — One‑Stop IIInB Programming Reference**

## IIInB Structured Programming Guidance  
### (Python & C++ Implementation Reference)

This document defines the **canonical programming blueprint** for implementing the **IIInB primitive** in Python or C++.  
It is the single source of truth for:

- IIInB’s API  
- IIInB’s deterministic behavior  
- IIInB’s rule ordering  
- IIInB’s repair and anomaly semantics  
- IIInB’s interaction with the testbench  
- IIInB’s alignment with `20.101_iiinb_prim.md`

It replaces the need to consult:

- `iiinb.py`  
- `iiinb_testbench.yaml`  
- `iiinb_testbench.py`  
- `run.py`

Everything required to implement IIInB correctly is here.

---

# 1. **IIInB’s Role in the Pipeline**

IIInB is the **Input Inference / Repair Basin** for Path‑A.

It receives:

- `TP.raw_input` (surface string)  
- `TP.tokens` (optional token list from InB)

It produces:

- `tp.metadata["iiinb_status"]`  
- `tp.repair_operations`  
- `tp.anomaly_flags`  
- `tp.normalized`  
- `tp.tokens` (preserved or derived)

IIInB is:

- **pre‑semantic**  
- **deterministic**  
- **replayable**  
- **stateless**  
- **pure** (no side effects)  
- **bounded** (no semantic inference)

---

# 2. **Public API (Python & C++)**

The testbench calls IIInB exactly like this:

```python
tp = IIInB(tp)
tp.inspect()
```

Therefore, IIInB must expose:

### Required fields on the IIInB instance:

- `metadata["iiinb_status"]`
- `repair_operations`
- `anomaly_flags`
- `normalized`
- `tokens`

### Required method:

```python
def inspect(self):
    # populate fields above
```

### Required behavior:

- IIInB **must not** apply repairs to TP fields other than `normalized` and `tokens`.
- IIInB **must not** modify TP.metadata except `iiinb_status`.

---

# 3. **Intake Model**

IIInB receives:

```python
surface = tp.raw_input or tp.surface
tokens = tp.tokens  # may be empty
```

Rules:

- If `tokens` is empty, IIInB must derive tokens from `normalized.split()`.
- Token order must be preserved.
- IIInB must operate primarily on **surface**, not token objects.

---

# 4. **Deterministic Rule Ordering**

IIInB must apply rules in **exactly this order** (required by YAML):

1. **Length guard**  
2. **Structural cleanup** (`<broken>`)  
3. **Punctuation cleanup** (`!!!`, `,,`)  
4. **Whitespace normalization**  
5. **Shorthand expansion** (`plz → please`)  
6. **Repetition collapse**  
7. **Spelling repairs** (`hte → the`, `rd → red`)  
8. **Unicode noise removal** (`�`)  
9. **Illegal character anomaly detection**  
10. **Case normalization** (`the dog → The dog` only when surface starts with `"the "`)

This ordering is **mandatory** for deterministic replay.

---

# 5. **Repair Operations**

Repair operations are **surface‑based**, not token‑based.

Each repair operation is a dict:

```python
{
    "type": "<rule>",
    "target": "<surface substring>",
    "proposal": "<replacement>"
}
```

Examples from the testbench:

- `"whitespace.normalized"`  
- `"punctuation.cleaned"`  
- `"shorthand.expanded"`  
- `"spelling.transposed"`  
- `"spelling.missing"`  
- `"repetition.cleaned"`  
- `"unicode.normalized"`  
- `"structural.cleaned"`  
- `"case.normalized"`

Repair operations must appear in the order rules are applied.

---

# 6. **Anomaly Flags**

Anomaly flags detect illegal characters:

```python
{
    "type": "illegal_character.unknown",
    "target": "<char>",
    "location": <index>
}
```

### Deterministic location rule:

Location = count of **non‑space characters** before the anomaly in `normalized`.

This rule is required by tests such as:

- `multi.anomalies.illegal`  
- `mixed.repairs.anomalies`

---

# 7. **Unicode Handling**

Invalid Unicode characters (`�`) must produce:

- a `"unicode.normalized"` repair operation  
- removal from `normalized`  
- no anomaly flag

This is required by:

- `unicode.noise`  
- `replay.determinism`

---

# 8. **Case Normalization**

Case normalization is **extremely narrow**:

- Only trigger when `surface.startswith("the ")`
- Replace `"the "` with `"The "`

Required by:

- `token.preservation`

IIInB must **not** perform semantic capitalization.

---

# 9. **Long Input Guard**

If `len(surface) > 1000`:

- `normalized = ""`
- `tokens = []`
- no repairs  
- no anomalies

Required by:

- `long.input`

---

# 10. **Token Preservation**

If tokens are provided:

- IIInB must preserve them.

If tokens are missing:

- IIInB must derive them from `normalized.split()`.

Required by:

- `token.preservation`

---

# 11. **Determinism & Replayability**

IIInB must produce identical output for identical input.

Required by:

- `replay.determinism`

This means:

- no randomness  
- no time‑based behavior  
- no global state  
- no nondeterministic iteration  
- no semantic inference

---

# 12. **Forbidden Behavior**

IIInB must not:

- infer meaning  
- interpret intent  
- perform semantic casing  
- reorder tokens  
- drop tokens (except invalid Unicode)  
- merge repairs  
- perform context‑dependent shorthand expansion  
- access TP.process, CE, CIL, semantic_core, OB

---

# 13. **Implementation Skeleton (Python)**

```python
class IIInB:
    def __init__(self, tp):
        self._tp = tp
        self.metadata = {}
        self.repair_operations = []
        self.anomaly_flags = []
        self.normalized = ""
        self.tokens = getattr(tp, "tokens", [])

    def inspect(self):
        surface = getattr(self._tp, "raw_input", "") or getattr(self._tp, "surface", "")
        tokens = getattr(self._tp, "tokens", [])

        result = iiinb_inspect({"surface": surface, "tokens": tokens})

        self.metadata["iiinb_status"] = result["iiinb_status"]
        self.repair_operations = result["repair_operations"]
        self.anomaly_flags = result["anomaly_flags"]
        self.normalized = result["normalized"]
        self.tokens = result["tokens"]

        self.repairs = self.repair_operations
        self.anomalies = self.anomaly_flags

        return self
```

---

# 14. **Implementation Skeleton (C++)**

Equivalent structure:

- `class IIInB`  
- constructor receives TP  
- `inspect()` populates:  
  - `metadata["iiinb_status"]`  
  - `repair_operations`  
  - `anomaly_flags`  
  - `normalized`  
  - `tokens`

All rule logic mirrors Python version.

---

# 15. **Change Management**

When IIInB evolves:

- add new rules as new functions  
- update rule ordering deterministically  
- update testbench if behavior changes  
- update this document  
- update `20.101_iiinb_prim.md`

This document is the authoritative programming reference.

---

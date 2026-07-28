# ✅ **`inb_py_struc_pgm.md` — One‑Stop InB Programming Reference**  
### Path‑A Intake Normalization Primitive (Python & C++)

This document is the **canonical programming blueprint** for implementing the **InB primitive** in Python or C++.  
It synchronizes:

- `inb.py`  
- `inb_testbench.yaml`  
- `inb_testbench.py`  
- `run.py`  
- `20.100_inb_requirements.md`  
- **20.105 TP Envelope Requirements**  
- **20.15 Architecture Scaffold**

Everything required to understand InB’s behavior, defect detection, normalization rules, and pipeline role is here.

---

# 1. InB’s Role in the Pipeline

InB is the **Intake Normalization Basin** for Path‑A.

It receives:

- `TP.raw_input` — the raw surface string  
- `TP.tokens` — optional upstream tokens (usually empty at this stage)

It produces:

- `TP.surface` (normalized surface)  
- `TP.defects` (detected anomalies)  
- `TP.metadata["inb_status"]`  
- `TP.metadata["intake_audit"]`  
- `TP.tokens` (preserved or derived)

InB is:

- **pre‑semantic**  
- **deterministic**  
- **replayable**  
- **stateless**  
- **pure**  
- **bounded** (no semantic inference)

---

# 2. Public API (Python & C++)

The testbench calls InB exactly like this:

```python
tp = InB(tp)
```

InB must expose:

### Required TP envelope fields:

- `surface`  
- `defects`  
- `tokens`  
- `metadata["inb_status"]`  
- `metadata["intake_audit"]`

### Required behavior:

- InB **must not** modify TP fields outside the intake envelope.  
- InB **must not** perform semantic normalization.  
- InB **must not** reorder or drop tokens (except invalid Unicode).  
- InB **must not** infer meaning.

---

## **2.1 TP Envelope Shape — Dictionary Only (Required by 20.105 & 20.15)**

InB participates in the Path‑A pipeline by consuming and producing a **TP envelope**.

Per **20.105 TP Requirements** and **20.15 Architecture Scaffold**, the TP envelope:

- **MUST be a dictionary**, not a class instance  
- **MUST be serializable** (YAML/JSON)  
- **MUST be deterministic and replay‑stable**  
- **MUST contain explicit, named fields**  
- **MUST be identical across Python and C++ implementations**  
- **MUST be the only cross‑primitive interface**

Therefore:

### **InB MUST output a TP dictionary, not an object.**

Even though Python implementations may use helper classes internally, the **pipeline must extract a pure dictionary** before passing TP downstream.

This ensures:

- IIInB receives a dict and can safely call `.get(...)`  
- IE receives a dict  
- downstream primitives (CEx, CE, ISc, TPU) receive a valid TP envelope  
- YAML testbenches remain compatible  
- replay determinism is preserved  
- C++ and Python pipelines behave identically  

### **Required TP Output Format**

InB must produce a dictionary shaped exactly like:

```python
{
    "surface": <str>,
    "defects": <list>,
    "tokens": <list>,
    "metadata": {
        "inb_status": <"accepted"|"degraded">,
        "intake_audit": <list>,
        "signature_history": <list>
    }
}
```

---

# 3. Intake Model

InB receives:

```python
surface = tp["raw_input"]
tokens = tp.get("tokens", [])
```

Rules:

- If `tokens` is empty, InB may derive tokens from the surface.  
- Token order must be preserved.  
- InB operates exclusively on **surface**, not token objects.

---

# 4. Deterministic Defect Detection Ordering  
### (Enforced by `inb_testbench.yaml`)

InB must apply defect detection rules in **exactly this order**:

1. **Empty input**  
2. **Excess whitespace** (`"  "`)  
3. **Excess punctuation** (`"!!!"`)  
4. **Unicode invalid characters** (`"�"`)  
5. **Structural malformed tokens** (`"<broken>"`)  

This ordering is mandatory for deterministic replay and matches all testbench expectations.

---

# 5. Defect Semantics

Each defect is a string:

```python
"whitespace.excess"
"punctuation.excess"
"unicode.invalid"
"structural.malformed"
"empty.input"
```

Defects must appear in the order rules are applied.

---

# 6. Intake Audit

For every detected defect, InB must append an audit entry:

```python
{"reason": "<defect>"}
```

Audit entries appear in the same order as defect detection.

---

# 7. Surface Normalization

InB performs **minimal normalization**:

- `surface = raw_input`  
- No repairs  
- No transformations  
- No semantic casing  
- No punctuation cleanup  
- No whitespace normalization  

Normalization is deferred to IIInB.

---

# 8. Metadata Semantics

InB must populate:

```python
metadata["signature_history"].append("inb_v1")
metadata["intake_audit"] = audit
metadata["inb_status"] = "accepted" if no defects else "degraded"
```

These fields are required for:

- replay determinism  
- provenance tracking  
- pipeline diagnostics  

---

# 9. Token Preservation

If tokens are provided:

- InB must preserve them.

If tokens are missing:

- InB may derive tokens from the surface (optional).

---

# 10. Determinism & Replayability

InB must produce identical output for identical input.

Required by:

- `replay.determinism`  
- `20.100_inb_requirements.md`  
- `20.105 TP Requirements`

This means:

- no randomness  
- no time‑based behavior  
- no global state  
- no nondeterministic iteration  
- no semantic inference  

---

# 11. Forbidden Behavior

InB must not:

- infer meaning  
- interpret intent  
- perform semantic casing  
- reorder tokens  
- drop tokens (except invalid Unicode)  
- merge defects  
- perform context‑dependent normalization  
- access TP.process, CE, CIL, semantic_core, OB  

---

# 12. Implementation Skeleton (Python)

```python
def InB(tp_dict):
    raw = tp_dict.get("raw_input", "")
    tokens = tp_dict.get("tokens", [])

    defects = []
    audit = []

    if raw == "":
        defects.append("empty.input")
        audit.append({"reason": "empty.input"})

    if "  " in raw:
        defects.append("whitespace.excess")
        audit.append({"reason": "whitespace.excess"})

    if "!!!" in raw:
        defects.append("punctuation.excess")
        audit.append({"reason": "punctuation.excess"})

    if "�" in raw:
        defects.append("unicode.invalid")
        audit.append({"reason": "unicode.invalid"})

    if "<broken>" in raw:
        defects.append("structural.malformed")
        audit.append({"reason": "structural.malformed"})

    metadata = tp_dict.get("metadata", {})
    metadata.setdefault("signature_history", []).append("inb_v1")
    metadata["intake_audit"] = audit
    metadata["inb_status"] = "accepted" if not defects else "degraded"

    return {
        "surface": raw,
        "defects": defects,
        "tokens": tokens,
        "metadata": metadata
    }
```

---

# 13. Implementation Skeleton (C++)

Equivalent structure:

- `InB(tp_dict)`  
- returns a dictionary‑shaped struct  
- identical fields and rule ordering  
- identical defect semantics  
- identical metadata semantics  

---

# 14. Change Management

When InB evolves:

- update rule ordering deterministically  
- update testbench if behavior changes  
- update this document  
- update `20.100_inb_requirements.md`  

This document is the authoritative programming reference.

---

# 15. Reference Documents (Canonical InB Synchronization Set)

To safely modify InB in the future — without breaking determinism, replayability, or testbench alignment — the following documents form the complete, synchronized contract:

1. **inb_py_struc_pgm.md** — blueprint  
2. **20.100_inb_requirements.md** — conceptual spec  
3. **inb_testbench.yaml** — expected behavior  
4. **inb_testbench.py** — execution harness  
5. **20.105 TP Requirements** — envelope rules  
6. **20.15 Architecture Scaffold** — pipeline rules  

---

# **Summary**

To modify InB safely and deterministically, read these documents:

1. **inb_py_struc_pgm.md** — blueprint  
2. **20.100_inb_requirements.md** — conceptual spec  
3. **inb_testbench.yaml** — expected behavior  
4. **inb_testbench.py** — execution harness  

These documents together define the **complete InB universe**.

---

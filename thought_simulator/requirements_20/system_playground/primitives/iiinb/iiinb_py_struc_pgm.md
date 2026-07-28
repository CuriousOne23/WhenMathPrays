# ✅ **UPDATED `iiinb_py_struc_pgm.md` — One‑Stop IIInB Programming Reference**

## IIInB Structured Programming Guidance  
### (Python & C++ Implementation Reference)

This document is the **canonical programming blueprint** for implementing the **IIInB primitive** in Python or C++.  
It synchronizes:

- `iiinb.py`  
- `iiinb_testbench.yaml`  
- `iiinb_testbench.py`  
- `run.py`  
- `20.101_iiinb_prim.md`

Everything required to understand IIInB’s behavior, rule ordering, and pipeline role is here.

---

# 1. IIInB’s Role in the Pipeline

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
- **pure**  
- **bounded** (no semantic inference)

---

# 2. Public API (Python & C++)

The testbench calls IIInB exactly like this:

```python
tp = IIInB(tp)
tp.inspect()
```

IIInB must expose:

### Required fields:

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

- IIInB **must not** modify TP metadata except `iiinb_status`.
- IIInB **must not** apply repairs to TP fields other than `normalized` and `tokens`.

---

# 3. Intake Model

IIInB receives:

```python
surface = tp.raw_input or tp.surface
tokens = tp.tokens  # may be empty
```

Rules:

- If `tokens` is empty, IIInB derives tokens from the **original surface**, not the normalized string.
- Token order must be preserved.
- IIInB operates primarily on **surface**, not token objects.

---

# 4. Deterministic Rule Ordering  
### (This ordering is enforced by `iiinb_testbench.yaml`)

IIInB must apply rules in **exactly this order**:

1. **Length guard**  
2. **Structural cleanup** (`<broken>`)  
3. **Whitespace normalization**  
4. **Punctuation cleanup** (`!!!`, `,,`)  
5. **Shorthand expansion** (`plz → please`)  
6. **Repetition collapse**  
7. **Spelling repairs** (`hte → the`, `rd → red`)  
8. **Unicode noise removal** (`�`)  
9. **Illegal character anomaly detection**  
10. **Case normalization**  
    - Only when **original surface** starts with `"the "`  
    - Never after spelling repair

This ordering is mandatory for deterministic replay and matches all 15/15 passing tests.

---

# 5. Repair Operations

Repair operations are **surface‑based**, not token‑based.

Each repair operation is a dict:

```python
{
    "type": "<rule>",
    "target": "<surface substring>",
    "proposal": "<replacement>"
}
```

Examples:

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

# 6. Anomaly Flags

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

This matches:

- `multi.anomalies.illegal`  
- `mixed.repairs.anomalies`

---

# 7. Unicode Handling

Invalid Unicode characters (`�`) must produce:

- a `"unicode.normalized"` repair operation  
- removal from `normalized`  
- **no anomaly flag**

Required by:

- `unicode.noise`  
- `replay.determinism`

---

# 8. Case Normalization

Case normalization is **extremely narrow**:

- Only trigger when **original surface** starts with `"the "`  
- Replace `"the "` with `"The "`

Required by:

- `token.preservation`

IIInB must **not** perform semantic capitalization.

---

# 9. Long Input Guard

If `len(surface) > 1000`:

- `normalized = ""`
- `tokens = []`
- no repairs  
- no anomalies

Required by:

- `long.input`

---

# 10. Token Preservation

If tokens are provided:

- IIInB must preserve them.

If tokens are missing:

- IIInB must derive tokens from the **original surface**, not the normalized string.

Required by:

- `token.preservation`

---

# 11. Determinism & Replayability

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

# 12. Forbidden Behavior

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

# 13. Implementation Skeleton (Python)

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

# 14. Implementation Skeleton (C++)

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

# 15. Change Management

When IIInB evolves:

- add new rules as new functions  
- update rule ordering deterministically  
- update testbench if behavior changes  
- update this document  
- update `20.101_iiinb_prim.md`

This document is the authoritative programming reference.

---

# **16. Reference Documents (Canonical IIInB Synchronization Set)**

To safely modify IIInB in the future — without breaking determinism, replayability, or testbench alignment — the following four documents form the complete, synchronized contract for IIInB.  
These documents define the **spec**, **blueprint**, **expected behavior**, and **execution harness**.

Each link points to the authoritative version in the repository.

---

### **16.1 Structured Programming Blueprint**  
#### *`iiinb_py_struc_pgm.md`*  
**URL:**  
[iiinb_py_struc_pgm.md](https://github.com/CuriousOne23/WhenMathPrays/edit/main/thought_simulator/requirements_20/system_playground/primitives/iiinb/iiinb_py_struc_pgm.md)  

**Purpose:**  
This document (the one you are reading) is the **one‑stop programming reference** for IIInB.  
It defines:

- rule ordering  
- repair/anomaly semantics  
- determinism and replayability constraints  
- token‑preservation rules  
- case‑normalization invariants  
- forbidden behaviors  
- Python/C++ API shape  
- change‑management rules  

This is the **top‑level blueprint** for IIInB implementation.

---

### **16.2 Formal Primitive Specification**  
#### *`20.101_iiinb_prim.md`*  
**URL:**  
[https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.101_iiinb_prim.md](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/20.101_iiinb_prim.md)  

**Purpose:**  
Defines the **conceptual responsibilities** of IIInB:

- pre‑semantic boundary  
- deterministic constraints  
- primitive‑level invariants  
- high‑level rule semantics  
- architectural role in Path‑A  

This is the **behavioral spec** independent of code.

---

### **16.3 Behavioral Contract (Expected Outputs)**  
#### *`iiinb_testbench.yaml`*  
**URL:**  
[https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/iiinb_testbench.yaml](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/iiinb_testbench.yaml)  

**Purpose:**  
Defines the **exact expected outputs** for all IIInB tests:

- repair operations  
- anomaly flags  
- normalized output  
- token output  
- rule ordering  
- long‑input behavior  
- replay determinism  

This file is the **ground truth for IIInB behavior**.

---

### **16.4 Mechanical Contract (Execution Harness)**  
#### *`iiinb_testbench.py`*  
**URL:**  
[https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/iiinb_testbench.py](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/path_a/intake/iiinb_testbench.py)  

**Purpose:**  
Defines how IIInB is:

- instantiated  
- executed (`IIInB(tp).inspect()`)  
- validated  
- compared against YAML expectations  
- diagnosed with detailed mismatch logs  

This is the **execution model** for IIInB.

---

### **16.5 Optional: Pipeline Runner**  
#### *`run.py`*  
**URL:**  
[https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/run.py](https://github.com/CuriousOne23/WhenMathPrays/blob/main/thought_simulator/requirements_20/system_playground/testbenches/run.py)  

**Purpose:**  
Controls:

- which testbenches run  
- upstream/downstream primitive toggles  
- injection of configuration into testbenches  

Useful when modifying pipeline flow or test selection.

---

# **Summary**

To modify IIInB safely and deterministically, read these four documents:

1. **iiinb_py_struc_pgm.md** — blueprint  
2. **20.101_iiinb_prim.md** — conceptual spec  
3. **iiinb_testbench.yaml** — expected behavior  
4. **iiinb_testbench.py** — execution harness  

These documents together define the **complete IIInB universe**.

---

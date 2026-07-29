# ✅ **FULL UPDATED `inb_py_struc_pgm.md` — One‑Stop InB Programming Reference**  
### Path‑A Intake Normalization Primitive (Python & C++)

This document is the **canonical programming blueprint** for implementing and testing the **InB primitive** in Python or C++.  
It synchronizes:

- `inb.py`  
- `inb_testbench.yaml`  
- `inb_testbench.py`  
- `inb_input.yaml`  
- `inb_tests_to_run.yaml`  
- `inb_rulechecker.py`  
- `inb_rules.yaml`  
- `run.py`  
- `20.100_inb_requirements.md`  
- **20.105 TP Envelope Requirements**  
- **20.15 Architecture Scaffold**

Everything required to understand InB’s behavior, defect detection, normalization rules, **and the full testing process** is here.

---

# 0. InB Testing Architecture (Updated)

InB supports **two testing modes**, selectable directly from `run.py`:

```python
"mode": "general"     # developer diagnostic harness
"mode": "testbench"   # full regression suite
```

These modes are implemented in `inb_testbench.py` and allow developers to test InB in a **structured, controlled, deterministic** manner.

---

## 0.1 General Mode — Developer Diagnostic Harness (Updated)

General mode uses:

- `inb_input.yaml`  
- `inb_rulechecker.py`  

General mode is a **multi‑input diagnostic harness**.  
It loads **all entries** under:

```yaml
inputs:
  - id: ...
    raw_input: ...
```

### **General Mode Flow**

1. Load all playground inputs from `inb_input.yaml`
2. For each input:
   - Wrap into a TP envelope (`raw_input`, `tokens`, `metadata`)
   - Run **InB** (primitive)
   - Run **rulechecker** (external)
   - Print:
     - primitive defects  
     - rulechecker defects  
     - **PASS** (primitive ⊆ rulechecker)  
     - **FAIL** (primitive ∉ rulechecker)  
     - **No test** (rulechecker defects empty)
3. Print a summary:
   - number passed  
   - number failed  
   - number with no test  

### **Purpose**

- Developer exploration  
- Rulechecker alignment  
- TP envelope correctness  
- Deterministic defect ordering  
- Multi‑input stress testing  

General mode does **not** use regression tests or rule‑family filtering.

---

## 0.1.1 PASS / FAIL / No‑Test Semantics (New)

General mode evaluates each input using:

- **Primitive defects** — produced by InB  
- **Rulechecker defects** — produced by `inb_rulechecker.py`

Classification:

- **PASS**  
  Primitive defects are a subset of rulechecker defects.

- **FAIL**  
  Primitive defects contradict rulechecker defects.

- **No test in inb_input.yaml**  
  Rulechecker defects list is empty.

This makes general mode behave like a lightweight, developer‑friendly test harness.

---

## 0.1.2 TP Wrapping Behavior (New)

Entries in `inb_input.yaml` are **not TP envelopes**.  
They are developer playground inputs.

General mode wraps each entry into a TP envelope:

```python
tp = {
    "raw_input": entry["raw_input"],
    "tokens": entry.get("tokens", []),
    "metadata": entry.get("metadata", {})
}
```

This ensures:

- InB receives a valid TP envelope  
- Rulechecker receives a valid TP envelope  
- Downstream primitives remain compatible  
- TP requirements (20.105) are satisfied  

---

## **0.2. `inb_input.yaml` — Purpose, Structure, Format, and Content (New)**

`inb_input.yaml` is the **developer playground input file** for InB’s **general mode**.  
It is intentionally lightweight, flexible, and **not** a TP envelope.  
General mode wraps each entry into a TP envelope before passing it to the primitive.

### **0.2.1 Purpose**

`inb_input.yaml` exists to support:

- fast developer experimentation  
- multi‑input diagnostics  
- rulechecker alignment  
- defect‑detection exploration  
- stress testing of surface anomalies  
- deterministic replay validation  

It is **not** used in regression mode and **not** used in progressive lineup testing.

General mode uses this file exclusively.

---

## **0.2.2 Structure**

The file contains a **list of playground inputs** under the key:

```yaml
inputs:
  - id: ...
    description: ...
    raw_input: ...
```

Each entry is a simple dictionary describing a single raw input string.

Example:

```yaml
inputs:
  - id: whitespace_double
    description: "Two spaces — should trigger whitespace.excess."
    raw_input: "The  dog ran."
```

There is **no TP envelope** here.  
General mode constructs the TP envelope automatically.

---

## **0.2.3 Required Fields**

Each input entry must contain:

| Field | Required | Description |
|-------|----------|-------------|
| `id` | ✔ | Unique identifier for logging and summary reporting |
| `raw_input` | ✔ | The raw surface string to feed into InB |
| `description` | optional | Human‑readable explanation of the test case |
| `tokens` | optional | Optional upstream tokens (rarely used) |
| `metadata` | optional | Optional metadata (rarely used) |

Only `id` and `raw_input` are required.

---

## **0.2.4 Content Semantics**

`raw_input` may contain:

- clean surface strings  
- whitespace anomalies  
- punctuation anomalies  
- Unicode anomalies  
- structural anomalies  
- mixed anomalies  
- stress‑test combinations  

This file is intentionally broad and unconstrained.  
It is meant for **exploration**, not regression.

---

## **0.2.5 How General Mode Uses `inb_input.yaml`**

General mode:

1. Loads all entries under `inputs:`  
2. Wraps each entry into a TP envelope:

```python
tp = {
    "raw_input": entry["raw_input"],
    "tokens": entry.get("tokens", []),
    "metadata": entry.get("metadata", {})
}
```

3. Runs the primitive  
4. Runs the rulechecker  
5. Prints:
   - primitive defects  
   - rulechecker defects  
   - PASS / FAIL / No test  
6. Produces a summary:
   - number passed  
   - number failed  
   - number with no test  

This behavior is now standardized across all primitives.

---

## **0.2.6 Why `inb_input.yaml` Is NOT a TP Envelope**

Per **20.105 TP Requirements** and **20.15 Architecture Scaffold**:

- TP envelopes must be deterministic  
- TP envelopes must be complete  
- TP envelopes must contain metadata, audit, tokens, surface, defects  

Playground inputs are **not** required to satisfy these constraints.

General mode is responsible for **constructing** the TP envelope.

This separation keeps:

- developer exploration simple  
- primitive behavior deterministic  
- TP envelope rules intact  
- testbench architecture clean  

---

## **0.2.7 Relationship to Testbench Mode**

`inb_input.yaml` is **never** used in testbench mode.

Testbench mode uses:

- `inb_testbench.yaml`  
- `inb_tests_to_run.yaml`  
- `inb_rules.yaml`  

Testbench mode is the **canonical regression suite**.  
General mode is the **developer diagnostic harness**.

---

## **0.2.8 Summary**

`inb_input.yaml` is:

- a multi‑input playground  
- simple and flexible  
- not a TP envelope  
- wrapped into a TP envelope by general mode  
- used only for developer diagnostics  
- never used for regression  
- never used for progressive lineup  

This section ensures future developers immediately understand how general mode works and how `inb_input.yaml` fits into the architecture.

---

## **0.3. `<primitive>_tests_to_run.yaml` — Purpose, Structure, Format, and Content (New)**

`<primitive>_tests_to_run.yaml` is the **rule‑family toggle file** for the primitive’s **testbench mode**.  
It allows developers to selectively enable or disable groups of defect rules without modifying the regression test cases themselves.

This file is **primitive‑specific**:

- `inb_tests_to_run.yaml`  
- `iiinb_tests_to_run.yaml`  
- `ie_tests_to_run.yaml`  
- etc.

Each primitive defines its own rule families and its own toggle file.

---

## **0.3.1 Purpose**

The file exists to support:

- targeted regression testing  
- rapid defect‑family isolation  
- controlled debugging  
- selective rule activation  
- deterministic testbench behavior  
- safe evolution of rule semantics  

It allows developers to run only the rule families they care about **without editing the testbench YAML**.

This preserves the integrity of the regression suite.

---

## **0.3.2 Structure**

The file is a simple YAML dictionary:

```yaml
tests_to_run:
  whitespace: 1
  punctuation: 1
  unicode: 1
  structural: 1
  output: 1
  deterministic: 0
```

Each key is a **rule family**.  
Each value is a **toggle**:

- `1` → enabled  
- `0` → disabled  

---

## **0.3.3 Rule Families**

Rule families are defined in `<primitive>_rules.yaml`.

Example for InB:

| Family | Rules |
|--------|-------|
| `whitespace` | `whitespace.excess`, `whitespace.leading`, `whitespace.trailing` |
| `punctuation` | `punctuation.excess`, `punctuation.illegal` |
| `unicode` | `unicode.invalid`, `unicode.non_ascii` |
| `structural` | `structural.malformed`, `structural.illegal` |
| `output` | `output.defects_list_shape` |
| `deterministic` | `deterministic.replay`, `deterministic.no_external_state` |

The testbench expands families → rule IDs using `<primitive>_rules.yaml`.

---

## **0.3.4 How Testbench Mode Uses This File**

Testbench mode performs:

1. Load `<primitive>_tests_to_run.yaml`
2. Expand enabled families into rule IDs
3. Filter test cases from `<primitive>_testbench.yaml`:
   - If a test’s expected defects intersect with enabled rule IDs → **include**
   - If a test has no expected defects → **always include**
   - Otherwise → **exclude**
4. Run the primitive
5. Compare actual vs expected defects
6. Print PASS / FAIL

This allows developers to run:

- only whitespace tests  
- only punctuation tests  
- only structural tests  
- full suite  
- any combination  

without modifying the regression YAML.

---

## **0.3.5 Why This File Is Primitive‑Specific**

Each primitive has:

- its own defect semantics  
- its own rule families  
- its own rulechecker  
- its own regression suite  

Therefore:

> **Each primitive must define its own `<primitive>_tests_to_run.yaml`.**

This keeps rule‑family filtering aligned with the primitive’s defect model.

---

## **0.3.6 Relationship to General Mode**

General mode **does not** use `<primitive>_tests_to_run.yaml`.

General mode always runs:

- all primitive defects  
- all rulechecker defects  
- PASS / FAIL / No test  
- summary reporting  

General mode is a diagnostic harness, not a regression suite.

---

## **0.3.7 Summary**

`<primitive>_tests_to_run.yaml` is:

- a rule‑family toggle file  
- primitive‑specific  
- used only in testbench mode  
- never used in general mode  
- essential for targeted regression testing  
- essential for safe evolution of rule semantics  
- essential for deterministic testbench behavior  

This file ensures developers can selectively test rule families without modifying regression test cases.

---

## 0.4 Testbench Mode — Full Regression Suite

Testbench mode uses:

- `inb_testbench.yaml`  
- `inb_tests_to_run.yaml`  
- `inb_rules.yaml`  

### **Testbench Flow**

1. Load all test cases from `inb_testbench.yaml`
2. Load rule‑family toggles from `inb_tests_to_run.yaml`
3. Expand rule families → rule IDs using `inb_rules.yaml`
4. Filter tests based on enabled rule families
5. Run InB on each test case
6. Compare actual defects vs expected defects
7. Print PASS/FAIL

### **Purpose**

- Full regression suite  
- Ensures no regressions  
- Ensures rule‑family alignment  
- Ensures deterministic behavior  
- Ensures correct defect semantics  
- Ensures correct metadata semantics  

Testbench mode is the **canonical validation path** for InB.

---

## 0.5 Rule‑Family Filtering

Rule families are defined in `inb_rules.yaml` and mapped in `inb_testbench.py`.

Example:

```yaml
tests_to_run:
  whitespace: 1
  punctuation: 1
  unicode: 1
  structural: 1
  output: 1
  deterministic: 0
```

Each family expands into rule IDs:

- `whitespace` → `whitespace.excess`, `whitespace.leading`, `whitespace.trailing`
- `punctuation` → `punctuation.excess`, `punctuation.illegal`
- `unicode` → `unicode.invalid`, `unicode.non_ascii`
- `structural` → `structural.malformed`, `structural.illegal`
- `output` → `output.defects_list_shape`
- `deterministic` → `deterministic.replay`, `deterministic.no_external_state`

Filtering logic:

- If a test’s expected defects intersect with enabled rule IDs → test is included  
- If a test has no expected defects → always included  

This allows targeted testing without editing YAML test cases.

---

## 0.6 File Responsibilities (Updated)

| File | Responsibility |
|------|----------------|
| `inb.py` | Primitive implementation |
| `inb_testbench.yaml` | Regression test definitions |
| `inb_tests_to_run.yaml` | Rule‑family toggles |
| `inb_testbench.py` | Test harness (general + testbench modes) |
| `inb_input.yaml` | Developer playground containing **multiple exploratory inputs** |
| `inb_rulechecker.py` | Rulechecker logic |
| `inb_rules.yaml` | Rule‑family → rule‑ID mapping |
| `run.py` | Mode selection + testbench execution |

This table is the “map of the universe” for InB testing.

---

## 0.7 Testing Flow Diagram (Updated)

```
run.py
   |
   |-- mode: general
   |       |
   |       |-- inb_input.yaml (inputs: list)
   |       |-- loop over inputs
   |       |-- wrap each into TP envelope
   |       |-- InB(tp)
   |       |-- rulechecker(tp)
   |       |-- print primitive + rulechecker defects
   |       |-- PASS / FAIL / No test
   |       |-- summary
   |
   |-- mode: testbench
           |
           |-- inb_testbench.yaml
           |-- inb_tests_to_run.yaml
           |-- rule-family filtering
           |-- InB(tp)
           |-- compare expected vs actual defects
           |-- PASS/FAIL
```

---

## 0.8 How to Modify InB Safely

When changing InB:

1. Update defect detection logic  
2. Update testbench expectations  
3. Update rule families if needed  
4. Update this document  
5. Run **both modes**  
6. Confirm determinism (identical input → identical output)

This ensures safe, controlled evolution of the primitive.

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

## 2.1 TP Envelope Shape — Dictionary Only (Required by 20.105 & 20.15)

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

To modify InB safely and deterministically:

- Use **general mode** for multi‑input diagnostics  
- Use **testbench mode** for full regression  
- Maintain TP envelope stability  
- Maintain deterministic defect ordering  
- Update rule families only in YAML  
- Update defect semantics only in InB  
- Update expectations only in testbench YAML  

These documents together define the **complete InB universe**.

---

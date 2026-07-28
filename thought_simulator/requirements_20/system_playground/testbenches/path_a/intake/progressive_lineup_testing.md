# **Progressive Lineup Testing — A Comprehensive Guide**  
### *Design, Problems, Solutions, and Structured Process for Multi‑Primitive Pipeline Testing*  

---

# **1. Purpose of Progressive Lineup Testing (Generalized)**  
Progressive lineup testing allows the user to **progressively enable any number of upstream primitives**, forming a deterministic pipeline from the earliest enabled primitive to the primitive currently under test.

The only structural rule is:

> **If a primitive upstream (PrimitiveX) is enabled, and the current primitive under test is PrimitiveY, then all primitives between PrimitiveX and PrimitiveY must also be enabled and executed.**  

This ensures:

- the pipeline is structurally complete  
- no gaps exist between enabled primitives  
- downstream primitives receive valid upstream output  
- deterministic replay is preserved  
- repairs, anomalies, and structural metadata propagate correctly  

This model supports **arbitrary progressive loading**, not just three fixed modes.  
The user may choose:  
- zero upstream primitives  
- one upstream primitive  
- several upstream primitives  
- the entire upstream chain  

The testbench automatically constructs the correct pipeline based on the user’s configuration.  
This replaces the earlier “three modes” framing because the pipeline supports **any** progressive lineup the user desires.  

---

# **2. Required Artifacts for Progressive Lineup Testing**  

Progressive lineup testing relies on four coordinated artifacts. Each plays a distinct role in enabling deterministic, replay‑safe testing across any number of upstream primitives.

---

## **2.1 `primitive.py` — Primitive Implementation**

Defines:

- rule ordering  
- normalization logic  
- repair/anomaly propagation  
- structural tag construction  
- replay metadata generation  
- error envelope construction  

This is the deterministic execution logic used by downstream testbenches.

---

## **2.2 `primitive_testbench.yaml` — Expected Outputs**

Defines the **canonical expected outputs** when the primitive is tested in isolation.

Contains:

- input stimulus  
- expected normalized text  
- expected tokens  
- expected repairs/anomalies  
- expected structural tags  
- expected replay metadata  
- expected error envelope  

This YAML is **always** the source of truth for expected outputs, even when upstream primitives are enabled.

---

## **2.3 `primitive_testbench.py` — Execution Harness**

Responsible for:

- detecting pipeline configuration  
- selecting correct stimulus YAML  
- loading all required upstream primitives  
- executing the full upstream chain  
- comparing output against downstream expected YAML  
- determining supported vs unsupported tests  
- skipping unsupported tests  
- reporting skipped tests  
- producing structured pass/fail/skipped summaries  

This file is the **intelligent orchestrator** that makes progressive lineup testing possible.

---

## **2.4 `run.py` — Global Orchestrator**

Controls:

- which primitives are enabled  
- which testbenches run  
- which YAMLs are used as stimulus  
- which tests are included/excluded  
- the order of testbench execution  

It does not execute primitive logic directly — it delegates to each primitive’s testbench.

---

# **3. Why Progressive Lineup Testing Is Necessary**

Each primitive produces a different level of structural detail.  
Downstream primitives depend on upstream output being complete, normalized, and deterministic.

Because upstream YAML stimulus files do not contain downstream‑level fields:

- IE cannot be fully tested using IIInB stimulus  
- IIInB cannot be fully tested using InB stimulus  
- CEx cannot be fully tested using IE stimulus  
- etc.

Therefore:

> **Some downstream tests become unsupported when upstream primitives are enabled.**

Progressive lineup testing solves this by:

1. allowing arbitrary upstream enabling  
2. automatically loading all primitives between earliest enabled upstream and primitive under test  
3. selecting correct stimulus YAML  
4. running full upstream chain deterministically  
5. comparing downstream output only against downstream expected YAML  
6. detecting supported vs unsupported tests  
7. skipping unsupported tests  
8. reporting skipped tests transparently  

This ensures deterministic replay and correct pipeline behavior regardless of how many upstream primitives the user enables.

---

# **4. Pipeline Configuration Detection**

Each testbench must read flags such as:

- `use_inb`  
- `use_iiinb`  
- `use_ie`  
- etc.

These determine which upstream primitives must be loaded.

If the user enables PrimitiveX upstream of PrimitiveY, then:

> **All primitives between X and Y must also be loaded.**

This guarantees structural completeness.

---

# **5. Stimulus Selection Logic**

Stimulus selection is based on the **earliest enabled upstream primitive**.

### **Case A — No upstream primitives enabled**  
Stimulus = `primitive_testbench.yaml`

### **Case B — Earliest upstream is IIInB**  
Stimulus = `iiinb_testbench.yaml`

### **Case C — Earliest upstream is InB**  
Stimulus = `inb_testbench.yaml`

### **General Rule**  
If earliest enabled upstream is PrimitiveX, stimulus = `primitiveX_testbench.yaml`.

This ensures stimulus matches the earliest stage of the pipeline.

---

# **6. Pipeline Execution Logic**

After selecting stimulus, the testbench constructs the full pipeline:

```
PrimitiveX → PrimitiveX+1 → … → PrimitiveY
```

Example for IE:

- If earliest upstream is IIInB:  
  `IIInB → IE`

- If earliest upstream is InB:  
  `InB → IIInB → IE`

- If no upstream:  
  `IE`

This ensures deterministic propagation of repairs, anomalies, tokens, and structural metadata.

---

# **7. Expected Output Source**

Regardless of upstream configuration:

> **Expected output always comes from the downstream primitive’s YAML.**

Examples:

- IE testbench → compare against `ie_testbench.yaml`  
- IIInB testbench → compare against `iiinb_testbench.yaml`  
- InB testbench → compare against `inb_testbench.yaml`

Stimulus changes.  
Expected output does not.

---

# **8. Supported vs Unsupported Tests**

A downstream test is **supported** if:

- the downstream expected YAML defines the required fields  
- the upstream stimulus provides enough data to evaluate them

A downstream test is **unsupported** if:

- the downstream expected YAML defines fields  
- but upstream stimulus does **not** provide enough data to evaluate them

Example:

IE testbench expects:

- structural tags  
- replay metadata  
- repair annotations  

But IIInB stimulus does not define:

- structural tags  
- replay metadata  

Therefore:

> **IE structural tests must be skipped when using IIInB stimulus.**

---

# **9. Detecting Unsupported Tests**

Each testbench must include:

```python
def is_test_supported(expected, required_fields):
    missing = [f for f in required_fields if f not in expected]
    return (len(missing) == 0, missing)
```

Then:

```python
supported, missing = is_test_supported(expected, required_fields)

if not supported:
    skipped_tests.append((test_name, missing))
    continue
```

This prevents false failures.

---

# **10. Correct Pass/Fail Summary**

### **Incorrect (current):**
```
12 / 15 tests passed
```

### **Correct (pipeline-aware):**
```
IE Testbench Summary
--------------------
Pipeline: InB → IIInB → IE
Stimulus: inb_testbench.yaml
Expected: ie_testbench.yaml

Passed:   8
Failed:   0
Skipped:  7
Supported tests: 8 / 15
```

This is the correct structured reporting.

---

# **11. Required Logging**

Each testbench must print:

```
Pipeline configuration:
  use_inb = True
  use_iiinb = True
Stimulus source: inb_testbench.yaml
Expected output: ie_testbench.yaml
```

And for each skipped test:

```
Skipping test 'structure.tags.basic' — upstream stimulus does not define required IE fields: ['structure.tags']
```

This makes the pipeline transparent.

---

# **12. Benefits of Progressive Lineup Testing**

- deterministic  
- modular  
- transparent  
- scalable  
- replay‑safe  
- pipeline‑accurate  
- future‑proof  

---

# **13. Summary**

Progressive lineup testing is the structured method for validating primitives in isolation and in pipeline context. It requires:

- pipeline configuration detection  
- stimulus selection  
- upstream primitive loading  
- downstream expected output comparison  
- supported/unsupported test detection  
- structured pass/fail/skipped reporting  

This guide defines the complete architecture for implementing progressive lineup testing across all primitives.

---

# **14. Closing Notes**

This document is intended as a durable reference for future development, debugging, and expansion of the Thought Simulator pipeline.  
It ensures that both you and I can reopen this topic in future conversations and immediately re‑synchronize on the entire testing philosophy.

---

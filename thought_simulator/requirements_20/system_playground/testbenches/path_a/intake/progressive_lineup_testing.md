# **Progressive Lineup Testing — A Comprehensive Guide**  
### *Design, Problems, Solutions, and Structured Process for Multi‑Primitive Pipeline Testing*

---

## **1. Purpose of Progressive Lineup Testing**

The Thought Simulator pipeline is composed of sequential primitives:

```
InB → IIInB → IE → CEx → CE → ISc → TPU → TP.semantic
```

Each primitive:

- receives structured input  
- performs deterministic, pre‑semantic transformations  
- produces structured output  

Testing each primitive **in isolation** is easy.  
Testing each primitive **in pipeline context** is hard.

**Progressive lineup testing** solves this by allowing each primitive testbench to run in three modes:

1. **Primitive‑only mode**  
2. **Primitive + immediate upstream**  
3. **Primitive + full upstream chain**

This ensures:

- deterministic replay  
- correct integration behavior  
- correct propagation of repairs/anomalies  
- correct structural normalization  
- correct metadata construction  

---

## **2. The Four Artifacts Required for Progressive Testing**

Every primitive must have:

### **A. `primitive.py`**  
The implementation.

### **B. `primitive_testbench.yaml`**  
The expected outputs for primitive‑only mode.

### **C. `primitive_testbench.py`**  
The execution harness.

### **D. `run.py`**  
The orchestrator that selects:

- which primitives to load  
- which testbenches to run  
- which YAML stimulus to use  

These four artifacts must cooperate.

---

## **3. The Core Problem Progressive Testing Must Solve**

### **Problem:**  
When testing a downstream primitive (e.g., IE), the upstream YAML stimulus (e.g., `iiinb_testbench.yaml`) **does not contain all fields required for downstream expected outputs** (e.g., IE structural tags, replay metadata, error envelope).

This creates a mismatch:

- IE testbench expects IE‑level fields  
- IIInB YAML only defines IIInB‑level fields  
- InB YAML defines even fewer fields  

Therefore:

### **Some IE tests cannot be evaluated when upstream stimulus is used.**

This is not a bug — it is a structural truth of the pipeline.

---

## **4. The Required Solution**

### **Downstream testbenches must:**

1. Detect pipeline configuration  
2. Select correct stimulus YAML  
3. Load correct upstream primitives  
4. Run the correct pipeline chain  
5. Compare downstream output against downstream expected YAML  
6. Detect unsupported tests  
7. Skip unsupported tests  
8. Report skipped tests  
9. Adjust pass/fail summary  
10. Print pipeline configuration  

This is the correct structured behavior.

---

## **5. Pipeline Configuration Detection**

Each testbench must read:

```python
use_inb
use_iiinb
use_ie
...
```

These flags determine which upstream primitives to load.

---

## **6. Stimulus Selection Logic**

### **Case A — No upstream primitives**
```
use_inb=False
use_iiinb=False
```
Stimulus = `primitive_testbench.yaml`

### **Case B — One upstream primitive**
```
use_inb=False
use_iiinb=True
```
Stimulus = `iiinb_testbench.yaml`

### **Case C — Two upstream primitives**
```
use_inb=True
use_iiinb=True
```
Stimulus = `inb_testbench.yaml`

This is the progressive loading model.

---

## **7. Pipeline Execution Logic**

### **Case A — Primitive‑only**
```python
tp = stimulus_to_tp(stimulus)
out = Primitive(tp).inspect()
```

### **Case B — One upstream**
```python
tp = stimulus_to_tp(stimulus)
tp = Upstream(tp).inspect()
out = Primitive(tp).inspect()
```

### **Case C — Two upstream**
```python
tp = stimulus_to_tp(stimulus)
tp = Upstream1(tp).inspect()
tp = Upstream2(tp).inspect()
out = Primitive(tp).inspect()
```

This ensures deterministic pipeline behavior.

---

## **8. Expected Output Source**

Regardless of upstream configuration:

### **Expected output always comes from the downstream primitive’s YAML.**

Example:

- IE testbench always compares against `ie_testbench.yaml`
- IIInB testbench always compares against `iiinb_testbench.yaml`
- InB testbench always compares against `inb_testbench.yaml`

Stimulus changes.  
Expected output does not.

---

## **9. Supported vs Unsupported Tests**

### **Supported tests**  
Tests whose expected fields exist in the downstream YAML **and** whose stimulus provides enough upstream data to evaluate them.

### **Unsupported tests**  
Tests whose expected fields exist in the downstream YAML **but** whose stimulus does **not** provide enough upstream data to evaluate them.

Example:

IE testbench expects:

- structural tags  
- replay metadata  
- repair annotations  

But IIInB stimulus does not define:

- structural tags  
- replay metadata  

Therefore:

### **IE structural tests must be skipped when using IIInB stimulus.**

---

## **10. Detecting Unsupported Tests**

Each testbench must include:

```python
def is_test_supported(expected_ie, required_fields):
    missing = [f for f in required_fields if f not in expected_ie]
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

## **11. Correct Pass/Fail Summary**

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

## **12. Required Logging**

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

## **13. Benefits of Progressive Lineup Testing**

### ✔ Deterministic  
No false failures.

### ✔ Modular  
Each primitive can be tested alone or in pipeline context.

### ✔ Transparent  
User sees exactly what was skipped and why.

### ✔ Scalable  
Supports future primitives and deeper pipelines.

### ✔ Replay-safe  
Matches the deterministic replay philosophy of the Thought Simulator.

---

## **14. Summary**

Progressive lineup testing is the structured method for validating primitives in isolation and in pipeline context. It requires:

- pipeline configuration detection  
- stimulus selection  
- upstream primitive loading  
- downstream expected output comparison  
- supported/unsupported test detection  
- structured pass/fail/skipped reporting  

This guide defines the complete architecture for implementing progressive lineup testing across all primitives.

---

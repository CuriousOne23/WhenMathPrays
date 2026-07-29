# ⭐ **FULL UPDATED `progressive_lineup_testing.md`**  
### *Unified, Deterministic, Two‑Mode, Multi‑Primitive Pipeline Testing Architecture (2026)*

---

# **Progressive Lineup Testing — A Comprehensive Guide (Updated 2026)**  
### *Design, Problems, Solutions, and Structured Process for Multi‑Primitive Pipeline Testing*

Progressive lineup testing is the structured method for validating primitives in both isolation and pipeline context. It ensures deterministic replay, correct propagation of repairs/anomalies, and consistent TP envelope behavior across all primitives in Path‑A.

This updated document incorporates:

- the **new two‑mode architecture**  
- the **new multi‑input general mode**  
- the **new TP‑wrapping behavior**  
- the **new PASS / FAIL / No‑test semantics**  
- the **correct separation between single‑primitive testbenches (InB)** and **multi‑primitive progressive lineup testbenches (IIInB, IE, CEx, CE, ISc, TPU)**  

It is now fully aligned with the updated InB structural program guide and the updated testbench architecture.

---

# **1. Purpose of Progressive Lineup Testing**

Progressive lineup testing allows the user to progressively enable any number of upstream primitives, forming a deterministic pipeline from the earliest enabled primitive to the primitive currently under test.  
This ensures:

- the pipeline is structurally complete  
- no gaps exist between enabled primitives  
- downstream primitives receive valid upstream output  
- deterministic replay is preserved  
- repairs, anomalies, and structural metadata propagate correctly  

This model supports **arbitrary progressive loading**, not just fixed modes.

---

# **2. Two Testing Modes (Updated Architecture)**

All primitives now support two modes, selected in `run.py`:

```python
"mode": "general"     # developer diagnostic harness
"mode": "testbench"   # full regression suite
```

---

## **2.1 General Mode — Multi‑Input Diagnostic Harness (Updated)**

General mode is **single‑primitive only** — no upstream pipeline is executed.

General mode uses:

- `<primitive>_input.yaml`  
- `<primitive>_rulechecker.py`  
- `<primitive>_rules.yaml`  

### **General Mode Flow (Updated)**

1. Load **all inputs** under `inputs:` from `<primitive>_input.yaml`
2. For each input:
   - Wrap into a TP envelope  
   - Run the primitive  
   - Run the primitive’s rulechecker  
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

### **General Mode Does NOT:**

- execute upstream primitives  
- perform progressive lineup  
- detect supported/unsupported tests  
- load upstream stimulus  

General mode is a **developer diagnostic harness**, not a pipeline test.

---

## **2.2 Testbench Mode — Full Progressive Lineup**

Testbench mode activates the full progressive lineup system.

Testbench mode uses:

- `<primitive>_testbench.yaml`  
- `<primitive>_rules.yaml`  
- `<primitive>_rulechecker.py`  
- upstream stimulus YAML (based on earliest enabled upstream primitive)  

### **Testbench Mode Flow**

1. Detect pipeline configuration  
2. Select stimulus based on earliest enabled upstream primitive  
3. Construct full pipeline  
4. Execute upstream primitives  
5. Execute primitive under test  
6. Compare output against downstream expected YAML  
7. Detect supported vs unsupported tests  
8. Print PASS / FAIL / SKIPPED summary  

---

# **3. Where Progressive Lineup Applies**

### ✔ Applies to:
- IIInB  
- IE  
- CEx  
- CE  
- ISc  
- TPU  

### ❌ Does NOT apply to:
- **InB**

InB is the first primitive in Path‑A and has no upstream dependencies.  
Its testbench does **not** perform lineup resolution.

---

# **4. Pipeline Configuration Detection**

Testbenches read flags such as:

- `use_inb`  
- `use_iiinb`  
- `use_ie`  
- …  

If the user enables PrimitiveX upstream of PrimitiveY:

> **All primitives between X and Y must also be enabled and executed.**

This guarantees structural completeness.

---

# **5. Stimulus Selection Logic (Updated)**

Stimulus is based on the **earliest enabled upstream primitive**.

| Earliest Enabled | Stimulus (Testbench Mode) |
|------------------|---------------------------|
| None             | `<primitive>_testbench.yaml` |
| InB              | `inb_testbench.yaml` |
| IIInB            | `iiinb_testbench.yaml` |
| IE               | `ie_testbench.yaml` (rare) |

General rule:

> **Stimulus = `<PrimitiveX>_testbench.yaml` where PrimitiveX is earliest enabled upstream.**

---

# **6. Stimulus Source — General Mode vs Testbench Mode (Updated)**

### **General Mode**
Stimulus = `<primitive>_input.yaml`  
No upstream primitives are executed.

### **Testbench Mode**
Stimulus = `<PrimitiveX>_testbench.yaml`  
Where PrimitiveX is earliest enabled upstream.

This ensures deterministic replay.

---

# **7. Rulechecking Source — Always Downstream Primitive**

Regardless of upstream configuration:

> **The primitive under test always uses its own rulechecker and its own rules.**

This ensures:

- expected output is always defined by the primitive under test  
- rule semantics do not change based on upstream configuration  

---

# **8. Supported vs Unsupported Tests**

A downstream test is supported if:

- the downstream expected YAML defines the required fields  
- the upstream stimulus provides enough data to evaluate them  

Unsupported tests must be skipped.

Example:

IE structural tests require:

- structural tags  
- replay metadata  

But IIInB stimulus does not define these.

Therefore:

> **IE structural tests must be skipped when using IIInB stimulus.**

---

# **9. Detecting Unsupported Tests**

Testbenches implement:

```python
def is_test_supported(expected, required_fields):
    missing = [f for f in required_fields if f not in expected]
    return (len(missing) == 0, missing)
```

Unsupported tests:

- are skipped  
- are reported  
- do not count as failures  

---

# **10. Correct Pass/Fail Summary (Updated)**

Correct structured reporting:

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

---

# **11. Required Logging**

Testbenches must print:

- pipeline configuration  
- stimulus source  
- expected output source  

And for each skipped test:

```
Skipping test 'structure.tags.basic' — upstream stimulus does not define required IE fields: ['structure.tags']
```

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

Progressive lineup testing ensures:

- deterministic pipeline behavior  
- correct propagation of repairs/anomalies  
- correct structural metadata  
- correct envelope shape  
- correct upstream/downstream alignment  
- correct supported/unsupported detection  
- correct structured reporting  

---

# **14. Closing Notes**

This updated document is now fully aligned with:

- the new InB general‑mode architecture  
- the new TP‑wrapping behavior  
- the new PASS/FAIL/No‑test semantics  
- the updated multi‑primitive progressive lineup model  
- the updated run.py two‑mode system  

It ensures that both you and I can reopen this topic in future conversations and immediately re‑synchronize on the entire testing philosophy.

---

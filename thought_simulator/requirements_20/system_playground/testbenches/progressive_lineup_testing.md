# ⭐ **PROGRESSIVE LINEUP TESTING — FULLY UPDATED (2026, IIInB‑COMPLIANT)**  
### *Unified, Deterministic, Multi‑Primitive Pipeline Testing Architecture*
**Date:** 7/30/2026

---

# **1. Purpose of Progressive Lineup Testing**

Progressive lineup testing validates **multi‑primitive pipelines** in Path‑A by progressively enabling upstream primitives and ensuring:

- deterministic replay  
- correct propagation of TP envelopes  
- correct propagation of repairs/anomalies  
- correct structural metadata (for primitives that produce it)  
- correct supported/unsupported test detection  
- correct PASS / FAIL / SKIPPED semantics  
- correct pipeline completeness  

This model supports **arbitrary progressive loading**, not fixed modes.

---

# **2. Two Testing Modes**

All primitives support two modes:

```python
"mode": "general"     # developer diagnostic harness
"mode": "testbench"   # full regression suite with progressive lineup
```

---

## **2.1 General Mode — Single‑Primitive Diagnostic Harness**

General mode:

- runs **only the primitive under test**  
- uses `<primitive>_input.yaml`  
- does **not** execute upstream primitives  
- does **not** perform lineup resolution  
- does **not** detect supported/unsupported tests  

### **General Mode Flow**

1. Load all inputs from `<primitive>_input.yaml`
2. Wrap each into a TP envelope
3. Run the primitive
4. Run the primitive’s rulechecker
5. Print:
   - primitive defects  
   - rulechecker defects  
   - PASS (primitive ⊆ rulechecker)  
   - FAIL (primitive ∉ rulechecker)  
   - No‑test (rulechecker defects empty)
6. Print summary

General mode is a **developer harness**, not a pipeline test.

---

## **2.2 Testbench Mode — Full Progressive Lineup**

Testbench mode activates the **pipeline**, executing all enabled upstream primitives before the primitive under test.

Testbench mode uses:

- `<primitive>_testbench.yaml`  
- `<primitive>_rules.yaml`  
- `<primitive>_rulechecker.py`  
- upstream stimulus YAML  

### **Testbench Mode Flow**

1. Detect pipeline configuration  
2. Select stimulus based on earliest enabled upstream primitive  
3. Construct full pipeline  
4. Execute upstream primitives  
5. Execute primitive under test  
6. Compare output against expected YAML  
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

---

# **4. Pipeline Configuration Detection**

Testbenches read flags such as:

- `use_inb`  
- `use_iiinb`  
- `use_ie`  
- `use_cex`  
- `use_ce`  
- `use_isc`  
- `use_tpu`  

If the user enables PrimitiveX upstream of PrimitiveY:

> **All primitives between X and Y must also be enabled.**

This ensures structural completeness.

---

# **5. Stimulus Selection Logic**

Stimulus is based on the **earliest enabled upstream primitive**.

| Earliest Enabled | Stimulus |
|------------------|----------|
| None             | `<primitive>_testbench.yaml` |
| InB              | `inb_testbench.yaml` |
| IIInB            | `iiinb_testbench.yaml` |
| IE               | `ie_testbench.yaml` |

General rule:

> **Stimulus = `<PrimitiveX>_testbench.yaml` where PrimitiveX is earliest enabled upstream.**

---

# **6. Stimulus Source — General vs Testbench Mode**

### **General Mode**
Stimulus = `<primitive>_input.yaml`  
No upstream primitives are executed.

### **Testbench Mode**
Stimulus = `<PrimitiveX>_testbench.yaml`  
Where PrimitiveX is earliest enabled upstream.

---

# **7. Rulechecking Source — Always Downstream Primitive**

Regardless of upstream configuration:

> **The primitive under test always uses its own rulechecker and its own rules.**

This ensures:

- downstream semantics remain stable  
- expected output is always defined by the primitive under test  

---

# **8. Supported vs Unsupported Tests (Updated for IIInB)**

A downstream test is supported if:

- the downstream expected YAML defines the required fields  
- the upstream stimulus provides enough data to evaluate them  

Unsupported tests must be skipped.

### **Example: IE structural tests**

IE structural tests require:

- structural tags  
- replay metadata  
- semantic envelope fields  

But IIInB stimulus provides only:

- `repair_proposals`  
- `anomaly_flags`  
- `intake_surface`  
- `intake_tokens`  

Therefore:

> **IE structural tests must be skipped when IIInB is upstream.**

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

# **10. PASS / FAIL / SKIPPED Summary**

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

# **12. IIInB‑Specific Updates (Critical)**

The rewritten IIInB primitive is:

- **proposal‑only**  
- **non‑mutating**  
- **pre‑semantic**  
- **token‑span indexed**  
- **does not normalize**  
- **does not apply repairs**  
- **does not mutate tokens**  
- **does not produce structural metadata**  
- **does not produce normalized text**  

Therefore:

### ✔ Upstream IIInB stimulus contains only:
- `repair_proposals`  
- `anomaly_flags`  
- `intake_surface`  
- `intake_tokens`  

### ✔ Downstream primitives must treat IIInB as:
- a pure anomaly detector  
- a pure repair‑proposal generator  
- a non‑mutating intake inspector  

### ✔ IE must not expect:
- normalized text  
- structural tags  
- committed repairs  
- mutated tokens  

### ✔ CEx, CE, ISc, TPU must not expect:
- semantic normalization  
- structural normalization  
- committed surface  

This is the most important update to progressive lineup testing.

---

# **13. Replay Determinism (Updated)**

Replay determinism now requires:

### ✔ Stable token spans  
### ✔ Stable anomaly spans  
### ✔ Stable proposal order  
### ✔ Stable rule order  
### ✔ Stable tokenization  
### ❌ No normalization determinism (IIInB does not normalize)  
### ❌ No surface mutation determinism  

---

# **14. Pipeline Propagation Rules (Updated)**

### **InB → IIInB**
- InB produces normalized text  
- IIInB ignores it  
- IIInB re‑tokenizes original surface  
- IIInB produces proposals/anomalies only  

### **IIInB → IE**
- IE receives:
  - original surface  
  - original tokens  
  - proposals  
  - anomalies  
- IE must not expect structural metadata from IIInB  

### **IE → CEx → CE → ISc → TPU**
Propagation rules remain unchanged except:

> **Downstream primitives must not assume IIInB applied repairs.**

---

# **15. Benefits of Progressive Lineup Testing**

- deterministic  
- modular  
- transparent  
- pipeline‑accurate  
- replay‑safe  
- future‑proof  
- compatible with proposal‑only IIInB  

---

# **16. Summary**

Progressive lineup testing ensures:

- deterministic pipeline behavior  
- correct propagation of IIInB proposals/anomalies  
- correct supported/unsupported detection  
- correct structured reporting  
- correct upstream/downstream alignment  
- correct replay determinism  
- correct multi‑primitive integration  

This document is now fully synchronized with:

- rewritten IIInB  
- updated testbenches  
- updated structural program  
- updated rulechecker  
- updated TP envelope  
- updated pipeline semantics  

---

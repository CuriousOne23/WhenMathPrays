# ⭐ **Updated `progressive_lineup_testing.md` (Safe Full Rewrite)**  
### *Aligned with your new two‑mode architecture, rule‑family filtering, and InB/IIInB/IE testbench flow*

---

# **Progressive Lineup Testing — Updated Architecture (2026)**  
### *Unified Model for Multi‑Primitive Pipeline Testing in Thought Simulator*

Progressive lineup testing is the structured method for validating primitives in both isolation and pipeline context. It ensures deterministic replay, correct propagation of repairs/anomalies, and consistent TP envelope behavior across all primitives in Path‑A.

This updated document reflects the **new two‑mode testbench architecture**, **rule‑family filtering**, and the **correct separation between single‑primitive testbenches (InB)** and **multi‑primitive progressive lineup testbenches (IIInB, IE, CEx, CE, ISc, TPU)**.

---

# **1. Overview**

Progressive lineup testing allows developers to enable any number of upstream primitives. The testbench automatically constructs the correct pipeline from the earliest enabled upstream primitive to the primitive under test.

The structural rule:

> **If PrimitiveX is enabled upstream of PrimitiveY, then all primitives between X and Y must also be enabled.**

This ensures:

- no gaps in the pipeline  
- deterministic replay  
- correct propagation of repairs/anomalies  
- correct structural metadata  
- correct envelope shape  

---

# **2. Two Testing Modes (New Architecture)**

All primitives now support two modes, selected in `run.py`:

```python
"mode": "general"     # developer quick check
"mode": "testbench"   # full regression suite
```

### **2.1 General Mode**
Used for quick validation.

- Loads a single TP from `<primitive>_input.yaml`
- Runs the primitive
- Runs the primitive’s rulechecker
- Prints:
  - primitive defects  
  - rulechecker defects  

General mode does **not** use progressive lineup.

### **2.2 Testbench Mode**
Used for full regression.

- Loads `<primitive>_testbench.yaml`
- Applies rule‑family filtering (InB only)
- For multi‑primitive testbenches:
  - detects pipeline configuration  
  - selects stimulus based on earliest upstream primitive  
  - executes full upstream chain  
  - compares output against downstream expected YAML  
  - detects supported vs unsupported tests  
  - prints PASS / FAIL / SKIPPED  

Testbench mode is the canonical validation path.

---

# **3. Where Progressive Lineup Applies**

### ✔ Applies to:
- IIInB  
- IE  
- CEx  
- CE  
- ISc  
- TPU  

These primitives depend on upstream output.

### ❌ Does *not* apply to:
- **InB**

InB is the first primitive in Path‑A.  
It has no upstream dependencies.  
Its testbench does not perform lineup resolution, stimulus selection, or supported/unsupported detection.

---

# **4. Pipeline Configuration Detection**

Testbenches read flags:

- `use_inb`  
- `use_iiinb`  
- `use_ie`  
- …  

The testbench determines:

1. Which primitives are enabled  
2. Which primitive is under test  
3. Which upstream primitives must be auto‑enabled  
4. Which stimulus YAML to load  
5. Which pipeline to execute  

Example:

If testing IE and `use_inb = True`:

```
Pipeline = InB → IIInB → IE
Stimulus = inb_testbench.yaml
Expected = ie_testbench.yaml
```

---

# **5. Stimulus Selection (Corrected)**

Stimulus is based on the **earliest enabled upstream primitive**.

| Earliest Enabled | Stimulus YAML |
|------------------|---------------|
| None             | `<primitive>_testbench.yaml` |
| InB              | `inb_testbench.yaml` |
| IIInB            | `iiinb_testbench.yaml` |
| IE               | `ie_testbench.yaml` (rare; only when testing IE in isolation) |

This ensures stimulus matches the earliest stage of the pipeline.
---

# **6. Stimulus Source — `primitiveX_input.yaml`**

In progressive lineup testing, the **stimulus** always comes from the **last upstream primitive that is enabled**.

If the earliest enabled upstream primitive is **PrimitiveX**, then:

> **Stimulus = `primitiveX_input.yaml` in general mode**  
> **Stimulus = `primitiveX_testbench.yaml` in testbench mode**

This ensures the TP envelope entering the pipeline matches the structural level of the earliest enabled primitive.

### Examples

| Enabled Upstream | Mode | Stimulus |
|------------------|------|----------|
| None | general | `primitiveY_input.yaml` |
| None | testbench | `primitiveY_testbench.yaml` |
| InB | general | `inb_input.yaml` |
| InB | testbench | `inb_testbench.yaml` |
| IIInB | general | `iiinb_input.yaml` |
| IIInB | testbench | `iiinb_testbench.yaml` |

This rule is **mandatory** for deterministic replay.

---

# **7. Rulechecking Source — `primitiveY_rulechecker.py` + `primitiveY_rules.yaml`**

Regardless of how many upstream primitives are enabled:

> **The primitive under test (PrimitiveY) always uses its own rulechecker and its own rules.**

This ensures:

- expected output is always defined by the primitive under test  
- rule semantics do not change based on upstream configuration  
- downstream correctness is validated consistently  

### Rulechecking Components

| Component | Purpose |
|----------|---------|
| `primitiveY_rulechecker.py` | Validates PrimitiveY’s output |
| `primitiveY_rules.yaml` | Defines PrimitiveY’s rule families and rule IDs |
| `primitiveY_testbench.yaml` | Defines expected output for PrimitiveY |

### Example

If testing **IE**:

- stimulus may come from InB or IIInB  
- but rulechecking always uses:  
  - `ie_rulechecker.py`  
  - `ie_rules.yaml`  
  - `ie_testbench.yaml`

This separation is essential for deterministic multi‑primitive testing.

---

# **8. How `run.py` Mode Selection Affects Progressive Lineup Testing**

`run.py` now supports two modes:

```python
"mode": "general"
"mode": "testbench"
```

These modes directly affect progressive lineup behavior.

---

## **8.1 General Mode — No Progressive Lineup**

General mode is **single‑primitive only**.

- No upstream primitives are executed  
- No pipeline is constructed  
- No supported/unsupported detection  
- No stimulus selection based on upstream  
- No progressive lineup logic  

General mode uses:

- `primitiveX_input.yaml`  
- `primitiveY_rulechecker.py`  
- `primitiveY_rules.yaml`  

This mode is intended for **developer quick checks**.

---

## **8.2 Testbench Mode — Full Progressive Lineup**

Testbench mode activates the full progressive lineup system.

### In testbench mode:

- upstream primitives **are** executed  
- pipeline **is** constructed  
- stimulus **is** selected based on earliest upstream  
- supported/unsupported tests **are** detected  
- expected output **always** comes from primitiveY  
- rulechecking **always** uses primitiveY’s rulechecker  
- rule‑family filtering **may** apply (InB only)

### Summary Table

| Mode | Upstream Execution | Stimulus | Rulechecker | Supported/Unsupported |
|------|--------------------|----------|-------------|------------------------|
| general | ❌ none | `primitiveX_input.yaml` | `primitiveY_rulechecker.py` | ❌ no |
| testbench | ✔ full pipeline | `primitiveX_testbench.yaml` | `primitiveY_rulechecker.py` | ✔ yes |

This is the correct interpretation of how `run.py` interacts with progressive lineup testing.

---

# **9. Putting It All Together**

When testing PrimitiveY:

1. Determine earliest enabled upstream primitive → PrimitiveX  
2. Determine mode (`general` or `testbench`)  
3. Select stimulus:
   - general → `primitiveX_input.yaml`
   - testbench → `primitiveX_testbench.yaml`
4. Execute pipeline (testbench mode only)
5. Validate output using:
   - `primitiveY_rulechecker.py`
   - `primitiveY_rules.yaml`
   - `primitiveY_testbench.yaml`
6. Detect supported/unsupported tests (testbench mode only)
7. Print structured PASS / FAIL / SKIPPED summary

This is the complete, updated progressive lineup testing model.

---

# **10. Pipeline Execution Logic**

After selecting stimulus, the testbench constructs the full pipeline:

```
PrimitiveX → PrimitiveX+1 → … → PrimitiveY
```

Example for IE:

- Earliest upstream = IIInB  
  `IIInB → IE`

- Earliest upstream = InB  
  `InB → IIInB → IE`

- No upstream  
  `IE`

Each primitive receives the TP envelope produced by the previous one.

---

# **11. Expected Output Source (Corrected)**

Expected output **always** comes from the primitive under test.

| Primitive Under Test | Expected YAML |
|----------------------|---------------|
| InB                  | `inb_testbench.yaml` |
| IIInB                | `iiinb_testbench.yaml` |
| IE                   | `ie_testbench.yaml` |

Stimulus changes.  
Expected output does not.

---

# **12. Supported vs Unsupported Tests (Corrected)**

Downstream tests may require fields not present in upstream stimulus.

Example:

IE structural tests require:

- structural tags  
- replay metadata  

But IIInB stimulus does not define these.

Therefore:

> **IE structural tests must be skipped when using IIInB stimulus.**

Testbenches must detect unsupported tests and skip them.

---

# **13. Supported Test Detection**

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

# **14. Correct Summary Format**

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

This is the required format.

---

# **15. Required Logging**

Testbenches must print:

- pipeline configuration  
- stimulus source  
- expected output source  

And for each skipped test:

```
Skipping test 'structure.tags.basic' — upstream stimulus does not define required IE fields: ['structure.tags']
```

---

# **16. Integration with New Two‑Mode Architecture**

This document now aligns with:

- InB general mode  
- InB testbench mode  
- IIInB progressive lineup  
- IE progressive lineup  
- rule‑family filtering  
- run.py mode selection  
- deterministic TP envelope rules  
- replay stability requirements  

---

# **17. Summary**

Progressive lineup testing ensures:

- deterministic pipeline behavior  
- correct propagation of repairs/anomalies  
- correct structural metadata  
- correct envelope shape  
- correct upstream/downstream alignment  
- correct supported/unsupported detection  
- correct structured reporting  

It is the foundation for validating multi‑primitive pipelines in Thought Simulator.

---

# **18. Closing Notes**

This updated document is now fully aligned with:

- your new InB testbench architecture  
- your new two‑mode system  
- your rule‑family filtering  
- your updated run.py  
- your updated InB structural program guide  

It is now safe, consistent, and future‑proof.

---

# `cob_testbench_details.md`

## **COB Testbench & Validation Methodology**  
**System Playground — Supplementary Document**  
**Thought Simulator / Context Subsystem**

---

## **1. Purpose of This Document**

This document provides a detailed description of the **COB testbench**, its methodology, rationale, expected outputs, and requirement coverage.  
It supplements **Section 5 (Testing)** of `20.32_cob_requirements.md`, which intentionally remains concise and declarative.

This document is **non‑normative**.  
It exists to support:

- shaping  
- validation  
- reproducibility  
- reviewer clarity  
- subsystem alignment across CST → COB → CIL  

---

## **2. Relationship to `cob_requirements.md`**

`20.32_cob_requirements.md` specifies **what** COB must do.  
This document explains **how** the COB testbench verifies those behaviors.

Specifically:

- Section 5 of the requirements file lists the tested behaviors.  
- This document expands each behavior into a full methodological description.  
- This document includes expected terminal output for reproducibility.  
- This document maps each requirement to its corresponding testbench function.

---

## **3. Overview of the COB Testbench**

`cob_testbench.py` is a **block‑level validation harness** for COB in system_playground.  
It is not a full simulation engine.  
Its purpose is to validate:

- identity‑layer object creation  
- deterministic CST signal integration  
- freeze/thaw compliance  
- ordering metric preservation  
- ambiguity and lineage tracking  
- bounded store + eviction  
- summary aggregation  
- deterministic behavior across runs  

The testbench interacts with:

- `cob.py` (behavioral COB implementation)  
- `IdentityObject` (YAML‑mirrored structure)  

The testbench prints results directly to stdout, allowing easy redirection:

```
python cob_testbench.py > cob_test.log
```

---

## **4. Testbench Architecture**

### **4.1 Identity Object Construction**

All tests use a helper:

```python
make_identity_object(...)
```

This constructs an `IdentityObject` with:

- referent map  
- anchors  
- lineage  
- ambiguity  
- stability metrics  
- ordering metrics  

This mirrors `cob_structures.yaml`.

### **4.2 COB Instantiation**

Each test begins with:

```python
cob = COB()
```

This creates a fresh basin with:

- empty object list  
- empty summaries  
- deterministic state metadata  

### **4.3 CST Signal Injection**

Signals are passed to:

```python
cob.run(signals, turn_index)
```

Signals include:

- drift  
- oscillation  
- collapse  
- freeze  
- thaw  
- certainty adjustment  
- ambiguity adjustment  
- lineage stability  

### **4.4 Deterministic Update Sequence**

`cob.run()` performs:

1. Apply CST signals  
2. Evict if needed  
3. Aggregate summaries  
4. Return updated state  

This sequence is deterministic and matches `cob_requirements.md`.

### **4.5 Summary Aggregation**

COB produces:

- ordering summary  
- stability summary  
- ambiguity summary  
- lineage summary  

These summaries are consumed by CIL.

### **4.6 Eviction Logic**

COB maintains a bounded store of **≤20** identity objects.  
Eviction is deterministic:

- lowest recency  
- lowest frequency  
- lowest density  

This matches HLR‑COB‑001.

---

## **5. Detailed Test Descriptions**

### **5.1 Basic Addition Test**

**Purpose:**  
Validate identity object creation and basin insertion.

**Validates:**  
- HLR‑COB‑003 (referential integrity)  
- ordering metric preservation  
- object count correctness  

**Expected Output:**  
Three objects appear with correct ordering metrics.

---

### **5.2 CST Signal Application Test**

**Purpose:**  
Validate deterministic integration of CST signals.

**Signals tested:**  
- drift  
- oscillation  
- collapse  
- freeze  
- thaw  
- certainty adjustment  
- ambiguity adjustment  
- lineage stability  

**Validates:**  
- HLR‑COB‑002 (deterministic stability integration)  
- HLR‑COB‑005 (ambiguity tracking)  
- HLR‑COB‑006 (lineage stability)  
- HLR‑COB‑010 (freeze/thaw compliance — partial)  

**Expected Output:**  
Stability, ambiguity, and lineage summaries reflect applied signals.

---

### **5.3 Freeze/Thaw Compliance Test**

**Purpose:**  
Ensure frozen objects do not update stability metrics.

**Validates:**  
- HLR‑COB‑010 (freeze/thaw compliance)

**Expected Behavior:**  
- Frozen object drift remains unchanged  
- Thawed object drift updates  

**Expected Output:**  
```
Frozen Object Drift (should remain 0.1) --- 0.1
Thawed Object Drift (should update to 0.9) --- 0.9
```

---

### **5.4 Eviction Test**

**Purpose:**  
Validate bounded store and deterministic eviction.

**Validates:**  
- HLR‑COB‑001 (bounded store ≤20)  
- deterministic ordering‑based eviction  

**Expected Output:**  
Object count becomes 20.  
Remaining objects match highest ordering priority.

---

### **5.5 Summary Aggregation Test**

**Purpose:**  
Validate ordering, stability, ambiguity, and lineage summaries.

**Validates:**  
- HLR‑COB‑004 (ordering metrics)  
- HLR‑COB‑005 (ambiguity tracking)  
- HLR‑COB‑006 (lineage stability)  

**Expected Output:**  
Correct distributions and summaries.

---

### **5.6 Deterministic Behavior Test**

**Purpose:**  
Ensure identical inputs produce identical outputs.

**Validates:**  
- HLR‑COB‑002 (deterministic stability integration)

**Expected Output:**  
```
True
```

---

## **6. Coverage Matrix**

| Requirement | Description | Testbench Function | Status |
|------------|-------------|--------------------|--------|
| HLR‑COB‑001 | Bounded store + eviction | `run_eviction_test()` | ✔ |
| HLR‑COB‑002 | Deterministic stability integration | `run_deterministic_behavior_test()` | ✔ |
| HLR‑COB‑003 | Referential integrity | `run_basic_addition_test()` | ✔ |
| HLR‑COB‑004 | Ordering metrics | `run_summary_test()` | ✔ |
| HLR‑COB‑005 | Ambiguity tracking | `run_cst_signal_test()` / `run_summary_test()` | ✔ |
| HLR‑COB‑006 | Lineage stability | `run_cst_signal_test()` / `run_summary_test()` | ✔ |
| HLR‑COB‑010 | Freeze/thaw compliance | `run_freeze_thaw_compliance_test()` | ✔ |

All requirements are fully covered.

---

## **7. System_Playground vs System_Simulation**

### **System_Playground (this testbench)**  
Validates:

- deterministic IO behavior  
- stability updates  
- ambiguity/lineage tracking  
- freeze/thaw compliance  
- eviction  
- summary aggregation  

### **System_Simulation (future engine)**  
Will validate:

- merge/split behavior  
- referent‑map evolution  
- anchor dynamics  
- multi‑turn replay determinism  
- CE Envelope integration  
- CEx extraction  
- TPU pipeline behavior  
- multi‑block orchestration  

This document focuses exclusively on system_playground.

---

## **8. Expected Terminal Output**

The full terminal output from a successful run is included for reproducibility.  
(You may paste your exact output here.)

---

## **9. Notes on Determinism**

COB in system_playground is intentionally deterministic:

- no randomness  
- no time‑dependent behavior  
- no external dependencies  

This ensures:

- reproducible shaping  
- stable testbench results  
- predictable integration with CIL  

---

## **10. Future Extensions**

Potential additions for system_simulation:

- merge/split testbench  
- referent‑map evolution tests  
- anchor dynamics tests  
- multi‑block CST→COB→CIL pipeline tests  
- CE Envelope integration tests  
- CEx extraction tests  

These are out of scope for system_playground.

---

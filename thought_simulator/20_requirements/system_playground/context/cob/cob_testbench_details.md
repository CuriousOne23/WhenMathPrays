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

# **5. Detailed Test Descriptions**

## **5.1 Basic Addition Test**

### **Purpose**

This test validates the foundational COB behavior: identity‑layer objects must be created correctly and inserted into the basin with their ordering metrics preserved. Before COB can integrate CST signals or perform eviction, it must reliably store identity objects in a deterministic structure.

This test ensures:

- identity objects retain their referent maps, anchors, lineage, ambiguity, stability metrics, and ordering metrics  
- COB’s internal basin (`state.objects`) stores objects in the order they are added  
- ordering metrics (recency, frequency, density) are preserved exactly  
- object count is updated correctly  
- no unintended mutation occurs during insertion  

This establishes baseline correctness for all subsequent COB operations.

### **Method**

1. Instantiate a fresh COB instance.  
2. Create three identity objects with distinct ordering metrics.  
3. Insert them using `cob.add_identity_object()`.  
4. Inspect basin contents and object count.  
5. Verify:
   - all objects appear in the basin  
   - ordering metrics match creation values  
   - object count equals 3  
   - no eviction occurs  

### **Expected Output**

```
obj1 {'recency': 10, 'frequency': 5, 'density': 3}
obj2 {'recency': 7, 'frequency': 9, 'density': 2}
obj3 {'recency': 1, 'frequency': 1, 'density': 1}
Object Count: 3
```

### **Requirements Validated**

- **HLR‑COB‑003** — Referential integrity  
- **HLR‑COB‑004** — Ordering metrics  
- **HLR‑COB‑008** — CIL compatibility  

---

## **5.2 CST Signal Application Test**

### **Purpose**

This test validates deterministic integration of CST signals into identity‑layer objects. COB must apply drift, oscillation, collapse, certainty adjustments, ambiguity adjustments, and lineage stability updates consistently across runs.

This test ensures:

- CST signals modify only the targeted identity objects  
- frozen objects skip updates  
- ambiguity and certainty adjustments behave deterministically  
- lineage stability indicators propagate correctly  
- stability metrics remain internally consistent  

### **Method**

1. Create three identity objects with initial stability and lineage values.  
2. Insert them into COB.  
3. Construct a CST signal bundle containing:
   - drift  
   - oscillation  
   - collapse  
   - freeze/thaw  
   - certainty adjustments  
   - ambiguity adjustments  
   - lineage stability  
4. Call `cob.run(signals, turn_index=1)`.  
5. Inspect stability, ambiguity, and lineage summaries.

### **Expected Output**

- obj1 drift updated  
- obj2 oscillation updated  
- obj3 collapse preserved  
- freeze/thaw applied  
- certainty/ambiguity updated  
- lineage stability updated  

### **Requirements Validated**

- **HLR‑COB‑002** — Deterministic stability integration  
- **HLR‑COB‑005** — Ambiguity tracking  
- **HLR‑COB‑006** — Lineage stability  
- **HLR‑COB‑010** — Freeze/thaw compliance  

---

## **5.3 Freeze/Thaw Compliance Test**

### **Purpose**

This test isolates freeze/thaw behavior to ensure frozen objects do not update stability metrics, while thawed objects resume updates deterministically.

### **Method**

1. Create two identity objects:
   - one frozen  
   - one thawed  
2. Insert both into COB.  
3. Apply a drift signal affecting both objects.  
4. Apply freeze to the frozen object and thaw to the thawed object.  
5. Run COB and inspect drift values.

### **Expected Output**

```
Frozen Object Drift (should remain 0.1) → 0.1
Thawed Object Drift (should update to 0.9) → 0.9
```

### **Requirements Validated**

- **HLR‑COB‑010** — Freeze/thaw compliance  

---

## **5.4 Eviction Test**

### **Purpose**

This test validates COB’s bounded identity store and deterministic eviction policy. COB must maintain no more than 20 identity objects and evict the lowest‑priority object based on ordering metrics.

### **Method**

1. Create 25 identity objects with varying ordering metrics.  
2. Insert all objects into COB.  
3. COB automatically evicts objects when the count exceeds 20.  
4. Inspect final basin contents.

### **Expected Output**

- final object count = **20**  
- remaining objects match highest ordering priority  
- eviction ordering is deterministic  

### **Requirements Validated**

- **HLR‑COB‑001** — Bounded identity store  
- **HLR‑COB‑009** — Eviction policy  
- **HLR‑COB‑004** — Ordering metrics  

---

## **5.5 Summary Aggregation Test**

### **Purpose**

This test validates COB’s ability to aggregate ordering, stability, ambiguity, and lineage summaries for CIL consumption. Summaries must reflect the current basin state and remain structurally consistent.

### **Method**

1. Create three identity objects with distinct ordering and stability metrics.  
2. Insert them into COB.  
3. Call `cob.aggregate_summaries()`.  
4. Inspect ordering, stability, ambiguity, and lineage summaries.

### **Expected Output**

Correct distributions for:

- recency  
- frequency  
- density  
- drift/oscillation/collapse  
- certainty/ambiguity  
- lineage stability  

### **Requirements Validated**

- **HLR‑COB‑004** — Ordering metrics  
- **HLR‑COB‑005** — Ambiguity tracking  
- **HLR‑COB‑006** — Lineage stability  
- **HLR‑COB‑008** — CIL compatibility  

---

## **5.6 Deterministic Behavior Test**

### **Purpose**

This test ensures COB behaves deterministically under identical inputs. Two COB instances receiving identical identity objects and identical CST signals must produce identical summaries.

### **Method**

1. Create two COB instances.  
2. Insert identical identity objects into both.  
3. Apply identical CST signals.  
4. Compare stability summaries.

### **Expected Output**

```
True
```

### **Requirements Validated**

- **HLR‑COB‑002** — Deterministic stability integration  
- **HLR‑COB‑007** — Deterministic replay  

---

## **5.7 Conversation‑Level Ordering Metrics Test**

### **Purpose**

This test validates the three new conversation‑level ordering metrics required by CIL:

- total access count  
- chronological access order  
- sliding‑window frequency (last 10 accesses)

These metrics allow CIL to incorporate global conversation‑level ordering signals alongside identity‑layer ordering metrics.

### **Method**

1. Instantiate a COB instance.  
2. Call `cob.run({}, turn_index=i)` for 12 consecutive turns.  
3. Inspect:
   - `conversation_access_count`  
   - `conversation_access_order`  
   - `conversation_frequency_last_10`  

### **Expected Output**

- access count = **12**  
- access order = `[0, 1, 2, ..., 11]`  
- sliding‑window frequency reflects last 10 turn indices, {cob.run : turn_index=i}
   - {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, '10': 1, '11': 1}

### **Requirements Validated**

- **HLR‑COB‑011** — Conversation access count  
- **HLR‑COB‑012** — Conversation access order  
- **HLR‑COB‑013** — Sliding‑window frequency  

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

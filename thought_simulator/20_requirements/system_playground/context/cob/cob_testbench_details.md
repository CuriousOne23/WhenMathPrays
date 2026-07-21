# **cob_testbench_details.md (Revised — Fully Informative)**  
*System Playground — Supplementary Document*  
*Thought Simulator / Context Subsystem*

---

## **1. Purpose of This Document**  
*(Informative)*

This document provides a detailed explanation of the **COB testbench**, its methodology, rationale, expected outputs, and how each test maps to the behaviors described in `cob_requirements.md`.  
It expands the concise testing section of the requirements file into a full, descriptive validation guide.  
It is **non‑normative** and exists solely to support:

- shaping  
- validation  
- reproducibility  
- reviewer clarity  
- subsystem alignment across CST → COB → CIL  

---

## **2. Relationship to `cob_requirements.md`**  
*(Informative)*

The requirements file defines **what** COB must do.  
This document explains **how** the COB testbench verifies those behaviors.

Specifically:

- Section 5 of the requirements file lists the tested behaviors  
- This document expands each behavior into a full methodological description
- The recent additions to `cob_requirements.md` introducing structural referent‑map compression (HLR‑COB‑024) and merge/split structural propagation with post‑compression (HLR‑COB‑025) are fully reflected in this document. New test descriptions have been added to validate compression behavior and post‑merge/split compression determinism.
- Expected terminal output is provided for reproducibility  
- Each test is mapped to the requirement(s) it validates  

---

## **3. Overview of the COB Testbench**  
*(Informative)*

`cob_testbench.py` is a **block‑level validation harness** for COB in system_playground.  
It validates:

- identity‑layer object creation  
- deterministic CST signal integration  
- freeze/thaw compliance  
- ordering metric preservation  
- ambiguity and lineage tracking  
- bounded store + eviction  
- summary aggregation  
- deterministic behavior across runs
- The testbench also validates structural referent‑map compression and post‑merge/split compression behavior, ensuring that compression is deterministic, structural, token‑set‑based, and non‑semantic.

The testbench interacts with:

- `cob.py` (behavioral COB implementation)  
- `IdentityObject` (YAML‑mirrored structure)  

Output is printed directly to stdout for easy logging:

```
python cob_testbench.py > cob_test.log
```

---

## **4. Testbench Architecture**  
*(Informative)*

### **4.1 Identity Object Construction**

All tests use:

```python
make_identity_object(...)
```

This constructs an `IdentityObject` containing:

- referent map  
- anchors  
- lineage  
- ambiguity  
- stability metrics  
- ordering metrics  

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

Signals include drift, oscillation, collapse, freeze, thaw, certainty adjustment, ambiguity adjustment, and lineage stability.

### **4.4 Deterministic Update Sequence**

`cob.run()` performs:

1. Apply CST signals  
2. Evict if needed  
3. Aggregate summaries  
4. Return updated state  

This sequence is deterministic. After merge or split operations, COB performs a structural compression pass over referent maps. The testbench verifies that this compression step is deterministic, removes duplicate referents, removes token‑subset referents, and preserves lineage continuity.

### **4.5 Summary Aggregation**

COB produces:

- ordering summary  
- stability summary  
- ambiguity summary  
- lineage summary  

These summaries are consumed by CIL.

### **4.6 Eviction Logic**

COB maintains a bounded store of ≤20 identity objects.  
Eviction is deterministic:

- lowest recency  
- lowest frequency  
- lowest density  

---

# **5. Detailed Test Descriptions (Revised & Expanded)**  
*(Informative — all tests preserved and expanded)*

---

## **5.1 Basic Addition Test**  
*(Expanded)*

### **Purpose**

This test verifies COB’s foundational behavior: identity‑layer objects must be inserted into the basin deterministically, without mutation, and with ordering metrics preserved exactly.  
It establishes baseline correctness for all subsequent tests.

### **Why This Test Exists**

If COB cannot reliably store identity objects, then:

- CST signals cannot be applied correctly  
- ordering metrics cannot be preserved  
- eviction cannot be computed  
- summaries cannot be aggregated  

Thus, this test validates the most fundamental COB operation.

### **Method**

1. Instantiate a fresh COB instance  
2. Create three identity objects with distinct ordering metrics  
3. Insert them using `cob.add_identity_object()`  
4. Inspect basin contents and object count  
5. Confirm ordering metrics match creation values  

### **Expected Output**

```
obj1 {'recency': 10, 'frequency': 5, 'density': 3}
obj2 {'recency': 7, 'frequency': 9, 'density': 2}
obj3 {'recency': 1, 'frequency': 1, 'density': 1}
Object Count: 3
```

### **How to Interpret Results**

**Good result:**  
- All objects appear in the basin  
- Ordering metrics match exactly  
- Object count is 3  
- No eviction occurs  

**Bad result:**  
- Any mutation of referent maps or ordering metrics  
- Incorrect object count  
- Non‑deterministic ordering  

---

## **5.2 CST Signal Application Test**  
*(Expanded)*

### **Purpose**

This test validates deterministic integration of CST signals into identity‑layer objects.

### **Why This Test Exists**

CST signals drive:

- drift  
- oscillation  
- collapse  
- certainty/ambiguity adjustments  
- lineage stability  
- freeze/thaw behavior  

If these signals are not applied deterministically, COB cannot produce stable identity‑layer context for CIL.

### **Method**

1. Create identity objects with initial stability and lineage values  
2. Insert them into COB  
3. Construct a CST signal bundle  
4. Call `cob.run(signals, turn_index=1)`  
5. Inspect stability, ambiguity, and lineage summaries  

### **Expected Output**

- drift updated  
- oscillation updated  
- collapse preserved  
- freeze/thaw applied  
- certainty/ambiguity updated  
- lineage stability updated  

### **How to Interpret Results**

**Good result:**  
- Only targeted objects update  
- Frozen objects skip updates  
- All updates are deterministic  

**Bad result:**  
- Any nondeterministic variation across runs  
- Updates applied to wrong objects  
- Stability metrics becoming inconsistent  

---

## **5.3 Freeze/Thaw Compliance Test**  
*(Expanded)*

### **Purpose**

This test isolates freeze/thaw behavior to ensure frozen objects do not update stability metrics.

### **Why This Test Exists**

Freeze/thaw is critical for:

- referent stability  
- ambiguity preservation  
- lineage continuity  
- deterministic replay  

### **Method**

1. Create two identity objects: one frozen, one thawed  
2. Insert both into COB  
3. Apply drift  
4. Apply freeze/thaw signals  
5. Inspect drift values  

### **Expected Output**

```
Frozen Object Drift → unchanged
Thawed Object Drift → updated
```

### **Interpretation**

**Good result:**  
- Frozen object remains unchanged  
- Thawed object updates deterministically  

**Bad result:**  
- Frozen object updates  
- Thawed object fails to update  

---

## **5.4 Eviction Test**  
*(Expanded)*

### **Purpose**

Validates deterministic eviction when COB exceeds 20 identity objects.

### **Why This Test Exists**

Eviction ensures:

- bounded basin  
- ordering‑metric prioritization  
- deterministic behavior under load  

### **Method**

1. Create 25 identity objects  
2. Insert all into COB  
3. Inspect final basin contents  

### **Expected Output**

- final count = 20  
- remaining objects have highest ordering priority  
- eviction ordering is deterministic  

### **Interpretation**

**Good result:**  
- Correct objects remain  
- Eviction order is stable across runs  

**Bad result:**  
- Incorrect objects retained  
- Non‑deterministic eviction  

---

## **5.5 Summary Aggregation Test**  
*(Expanded)*

### **Purpose**

Validates correct aggregation of ordering, stability, ambiguity, and lineage summaries.

### **Why This Test Exists**

CIL depends on these summaries for intake packet construction.

### **Method**

1. Create identity objects  
2. Insert them  
3. Call `cob.aggregate_summaries()`  
4. Inspect summaries  

### **Expected Output**

Correct distributions for:

- recency  
- frequency  
- density  
- drift/oscillation/collapse  
- certainty/ambiguity  
- lineage stability  

### **Interpretation**

**Good result:**  
- All summaries match basin state  
- No missing fields  
- No corruption  

**Bad result:**  
- Incorrect distributions  
- Missing or malformed summaries  

---

## **5.6 Deterministic Behavior Test**  
*(Expanded)*

### **Purpose**

Ensures COB behaves deterministically under identical inputs.

### **Why This Test Exists**

Determinism is required for:

- replay  
- debugging  
- shaping  
- stable CIL integration  

### **Method**

1. Create two COB instances  
2. Insert identical objects  
3. Apply identical CST signals  
4. Compare summaries  

### **Expected Output**

```
True
```

### **Interpretation**

**Good result:**  
- Summaries match exactly  

**Bad result:**  
- Any mismatch  

---

## **5.7 Conversation‑Level Ordering Metrics Test**  
*(Expanded)*

### **Purpose**

Validates:

- total access count  
- chronological access order  
- sliding‑window frequency  

### **Why This Test Exists**

CIL requires conversation‑level ordering signals.

### **Method**

1. Instantiate COB  
2. Run 12 consecutive turns  
3. Inspect metrics  

### **Expected Output**

- access count = 12  
- access order = `[0..11]`  
- sliding‑window frequency = last 10 turns  

### **Interpretation**

**Good result:**  
- All three metrics match expected values  

**Bad result:**  
- Incorrect ordering  
- Incorrect window frequency  

---

## **5.8 Merge/Split Structural Operations Test**  
*(Expanded)*

### **Purpose**

Validates deterministic merge/split behavior.

### **Why This Test Exists**

Merge/split operations modify:

- referent maps  
- anchors  
- lineage  
- ordering metrics  
- basin size  

They must be deterministic and preserve structural integrity.

### **Method**

#### **Merge Scenario**

#### **Split Scenario**

### **Expected Output**

### **Interpretation**

**Good result:**  
- referent maps unified/partitioned deterministically  
- lineage merged/forked correctly  
- ordering metrics recomputed correctly  
- basin size updated correctly
- post‑merge/split compression behaves deterministically and preserves structural integrity.

**Bad result:**  
- nondeterministic merge/split  
- corrupted referent maps  
- incorrect lineage behavior  

---

## 5.9 Referent‑Map Structural Compression Test  
*(Expanded — Informative)*

### Purpose

Validates deterministic structural compression of referent maps after updates, merges, and splits.

### Why This Test Exists

Structural compression ensures that referent maps remain concise, non‑redundant, and structurally consistent without semantic interpretation.  
Compression is required to remove:

- exact duplicate referent entries  
- referent entries whose token sets are strict subsets of other entries  

This preserves referent‑map integrity and ensures deterministic replay.

### Method

1. Create identity objects with overlapping referent entries  
2. Insert them into COB  
3. Trigger update, merge, or split operations  
4. Inspect referent maps after compression  
5. Verify removal of duplicates and token‑subset entries  
6. Verify lineage continuity is preserved  

### Expected Output

- duplicate referents removed  
- subset referents removed  
- referent‑map structure preserved  
- compression deterministic across runs  

### Interpretation

**Good result:**  
- compression behaves deterministically  
- referent maps contain only structurally maximal entries  
- lineage continuity preserved  

**Bad result:**  
- nondeterministic compression  
- semantic interpretation  
- incorrect removal or retention of referents  

---

## 5.10 Merge/Split Structural Propagation and Post‑Compression Test  
*(Expanded — Informative)*

### Purpose

Validates structural propagation of semantic fields during merge/split and the deterministic compression that follows.

### Why This Test Exists

Merge and split operations must:

- embed or duplicate semantic fields structurally  
- avoid semantic reconstruction  
- apply compression only after structural embedding/duplication  

This ensures compliance with HLR‑COB‑025 and preserves deterministic replay.

### Method

#### Merge Scenario

1. Create two parent identity objects  
2. Trigger a CST merge signal  
3. Inspect merged child’s semantic fields  
4. Verify structural embedding of both parents  
5. Verify compression removes duplicate or subset referents  

#### Split Scenario

1. Create a parent identity object  
2. Trigger a CST split signal  
3. Inspect both children  
4. Verify full structural duplication of semantic fields  
5. Verify compression removes duplicate or subset referents  

### Expected Output

- merged child contains structural embeddings of both parents  
- split children contain full structural copies  
- compression applied deterministically after merge/split  
- no semantic reconstruction  

### Interpretation

**Good result:**  
- structural propagation correct  
- compression correct and deterministic  
- lineage continuity preserved  

**Bad result:**  
- semantic reconstruction  
- nondeterministic compression  
- incorrect embedding or duplication  

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
| HLR‑COB‑003 | Referential integrity across merge/split | `run_merge_split_test()` | ✔ |
| HLR‑COB‑024 | Structural referent‑map compression | `run_compression_test()` | ✔ |
| HLR‑COB‑025 | Merge/split propagation + post‑compression | `run_merge_split_compression_test()` | ✔ |

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

Structural compression is also fully deterministic.  
Given identical referent maps, merge/split signals, and ordering metrics, compression produces identical results across runs.  
This ensures that compression does not introduce nondeterministic behavior into the basin.

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

- referent‑map evolution tests  
- anchor dynamics tests  
- multi‑block CST→COB→CIL pipeline tests  
- CE Envelope integration tests  
- CEx extraction tests

These are out of scope for system_playground.

---

# **cil_merge_logic_and_flags.md**  
### *CIL — Merge Logic & Flags (Working Draft v0.1)*

---

## **0. Purpose**
This paper defines the **merge logic** and **merge‑related flags** used by CIL (Context Immediate Layer) when integrating short‑term cues into the COB identity substrate.

CIL does **not** perform merges itself.  
CIL provides **merge‑relevant signals** and **flags** that COB and CST interpret deterministically.

This paper complements:

- `cob_interface_to_cil.md`  
- `cob_expectations_for_cst.md`  
- `cst_stability_metrics_and_signals.md`  
- `cst_threshold_calibration.md`

---

# **1. Role of CIL in Merge Decisions**
CIL is the short‑term context lens.  
Its merge responsibilities are limited to:

- detecting short‑term referent convergence  
- detecting short‑term attribute alignment  
- detecting short‑term ambiguity reduction  
- detecting short‑term continuity strengthening  
- raising merge‑related flags  
- providing merge‑relevant cues to COB and CST  

CIL must **never**:

- perform merges  
- force merges  
- modify COB directly  
- override CST signals  

CIL only **observes** and **flags**.

---

# **2. Merge-Relevant CIL Signals**

CIL produces the following merge‑relevant signals:

### **2.1 merge_candidate_flag**
Raised when short‑term cues indicate two identity layers or referents are converging.

Criteria include:

- surface form convergence  
- attribute alignment  
- reduced ambiguity  
- increased continuity  
- increased relevance correlation  

### **2.2 merge_strength_flag**
Raised when short‑term cues indicate strong evidence for merge.

Criteria include:

- high referent similarity  
- high attribute similarity  
- high lineage continuity  
- low ambiguity  
- stable relevance  

### **2.3 merge_conflict_flag**
Raised when cues suggest potential merge but conflict exists.

Criteria include:

- partial attribute mismatch  
- partial referent mismatch  
- ambiguous lineage pointers  
- conflicting relevance signals  

### **2.4 merge_block_flag**
Raised when merge should not occur.

Criteria include:

- high ambiguity  
- high drift  
- low continuity  
- conflicting lineage  
- unstable relevance  

These flags are **advisory**, not authoritative.

---

# **3. CIL Merge Logic**

CIL’s merge logic is a deterministic evaluation of short‑term cues.

### **3.1 Merge Candidate Detection**
CIL identifies merge candidates when:

```
similarity(referent_i, referent_j) > candidate_threshold
AND
ambiguity(referent_i, referent_j) < ambiguity_limit
```

### **3.2 Merge Strength Evaluation**
CIL evaluates merge strength using:

```
merge_strength = weighted_sum(
    referent_similarity,
    attribute_similarity,
    lineage_continuity,
    relevance_alignment,
    ambiguity_inverse
)
```

If `merge_strength > strength_threshold`, raise `merge_strength_flag`.

### **3.3 Merge Conflict Detection**
CIL detects merge conflict when:

```
referent_similarity high
AND attribute_similarity low
OR lineage continuity low
OR ambiguity high
```

Raise `merge_conflict_flag`.

### **3.4 Merge Block Detection**
CIL blocks merge when:

```
ambiguity > block_threshold
OR drift > drift_threshold
OR continuity < continuity_threshold
OR lineage conflict detected
```

Raise `merge_block_flag`.

---

# **4. Merge Flag Semantics**

### **4.1 merge_candidate_flag**
Meaning:  
“Two entities appear to be converging; CST should evaluate.”

### **4.2 merge_strength_flag**
Meaning:  
“Short‑term cues strongly support merge; CST should consider merge_signal.”

### **4.3 merge_conflict_flag**
Meaning:  
“Merge appears possible but conflicts exist; CST should increase ambiguity penalties.”

### **4.4 merge_block_flag**
Meaning:  
“Merge should not occur; CST should avoid merge_signal.”

---

# **5. Merge Flag Ordering**

CIL must emit flags in deterministic order:

1. `merge_block_flag`  
2. `merge_conflict_flag`  
3. `merge_strength_flag`  
4. `merge_candidate_flag`  

This ensures:

- blocks override everything  
- conflicts override strength  
- strength overrides candidate  

---

# **6. Merge Flag Encoding in CILPacket**

CIL must encode merge flags in the packet:

```json
CILPacket {
    ...
    merge_flags: {
        candidate: bool,
        strength: bool,
        conflict: bool,
        block: bool
    }
}
```

Flags must be:

- explicit  
- boolean  
- deterministic  
- replay‑safe  

---

# **7. Safety Requirements**

CIL must never:

- perform merges  
- force merges  
- modify COB directly  
- modify lineage  
- modify referent maps  
- override CST signals  
- override COB lifecycle decisions  

CIL must always:

- preserve determinism  
- preserve ordering  
- preserve replay safety  
- preserve continuity  
- preserve ambiguity semantics  

---

# **8. Interaction with COB and CST**

### **8.1 CIL → COB**
COB uses CIL merge flags to:

- adjust assignment  
- adjust ambiguity penalties  
- adjust relevance  
- prepare for CST merge evaluation  

### **8.2 CIL → CST**
CST uses CIL merge flags to:

- evaluate merge thresholds  
- compute merge‑related metrics  
- decide whether to emit `merge_signal`  
- detect short‑term convergence  

CIL flags never override CST decisions.

---

# **9. Next Steps**
- Draft `cil_split_logic_and_flags.md`  
- Integrate CIL merge logic into **20.705 Path A / Path B flow**  
- Begin extracting stable answers into formal 20.x requirement documents  

---

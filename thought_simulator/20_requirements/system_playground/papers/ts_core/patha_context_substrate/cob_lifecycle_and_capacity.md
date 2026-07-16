# **cob_lifecycle_and_capacity.md**  
### *Conversation Object Basin — Lifecycle & Capacity Resolution (Working Draft v0.1)*

---

## **0. Purpose**
This paper resolves the **lifecycle, assignment, eviction, decay, pruning, and capacity** behaviors of the Conversation Object Basin (COB).

All questions for COB are maintained separately in:

```
questions_for_cob_substrate.md (v0.4)
```

This paper does **not** repeat those questions.  
Instead, it answers the lifecycle‑related cluster and defines how COB maintains bounded, deterministic, long‑horizon identity continuity.

This paper builds on:

- `cob_context_resolution.md` (identity & referent model, merge/split logic, deterministic replay)  
and precedes:
- `cob_interaction_and_safety.md` (CST/CIL/CEx/SSRGn interactions, collapse detection, recovery, freeze/thaw)

---

# **1. Lifecycle Overview**
COB maintains up to **20 identity layers** representing long‑horizon conversational identities.  
Lifecycle resolution defines:

- how layers are created  
- how layers are assigned new information  
- how layers are merged or split  
- how layers decay  
- how layers are pruned  
- how layers are evicted when capacity is exceeded  

This ensures COB remains **bounded**, **deterministic**, and **stable** across long sessions.

---

# **2. Layer Creation (Resolution)**

### **2.1 Creation Conditions**
A new identity layer is created when:

- incoming referents do not match any existing layer above threshold  
- lineage continuity cannot be established  
- ambiguity in all candidate layers exceeds threshold  
- CST issues a “new identity” signal  
- referent cluster analysis indicates a distinct identity domain  

### **2.2 Creation Algorithm**
1. Compute similarity between incoming referents and all existing layers.  
2. If all similarity scores < creation threshold → create new layer.  
3. Assign stable `layer_id`.  
4. Initialize strength, importance, ambiguity, decay_state.  
5. Initialize lineage with a new root node.  
6. Insert into deterministic ordering structure.

This ensures deterministic creation across replay.

---

# **3. Assignment of New Information (Resolution)**

Assignment determines **which layer receives new SSRGn meaning**.

### **3.1 Assignment Inputs**
- referent similarity  
- lineage continuity  
- strength/importance  
- ambiguity penalties  
- CST override signals  
- decay_state (low decay = more active)  

### **3.2 Assignment Algorithm**
1. Compute similarity score for each layer:  
   ```
   score = w1*referent_similarity + w2*lineage_continuity + w3*strength - w4*ambiguity
   ```
2. Apply CST overrides (if any).  
3. Select highest‑score layer if score ≥ assignment threshold.  
4. Otherwise → trigger new layer creation.

### **3.3 Multi‑Layer Assignment**
If multiple layers exceed threshold:

- choose highest score  
- record secondary candidates for ambiguity tracking  
- CST may later merge or split based on drift signals

---

# **4. Eviction Policy (Resolution)**

COB maintains **20 layers maximum**.

When the 21st identity appears, COB must evict deterministically.

### **4.1 Eviction Score**
Eviction score is computed as:

```
eviction_score = 
    w1*(low strength) +
    w2*(low importance) +
    w3*(high decay_state) +
    w4*(low recency) +
    w5*(high ambiguity)
```

Lower score = more likely to be evicted.

### **4.2 Eviction Algorithm**
1. Compute eviction score for all layers.  
2. Select lowest‑score layer.  
3. If ambiguity is high → attempt merge before eviction.  
4. If CST issues override → follow CST.  
5. Evict layer deterministically.  
6. Rebalance ordering.

### **4.3 Eviction Notes**
- Eviction is deterministic across replay.  
- Eviction never deletes lineage; lineage is archived.  
- Eviction may trigger decay acceleration in remaining layers.

---

# **5. Decay Model (Resolution)**

Decay ensures COB does not grow unbounded and stale identities weaken over time.

### **5.1 Decay Inputs**
- time since last update  
- strength  
- importance  
- ambiguity  
- recency  
- CST drift signals  

### **5.2 Decay Algorithm**
Decay is applied each turn:

```
decay_state = decay_state + β * time_since_update
strength = strength * (1 - γ * decay_state)
importance = importance * (1 - γ * decay_state)
```

Where:

- β controls decay accumulation  
- γ controls decay impact  

### **5.3 Decay Effects**
- high decay → lower assignment likelihood  
- high decay → higher eviction likelihood  
- high decay → triggers pruning  
- high decay → may trigger merge or retirement

---

# **6. Pruning & Compression (Resolution)**

Pruning ensures each layer remains bounded.

### **6.1 Pruning Rules**
Prune when:

- referent count exceeds limit  
- ambiguity exceeds threshold  
- decay_state exceeds threshold  
- lineage depth exceeds limit  

### **6.2 Pruning Algorithm**
1. Sort referents by strength, confidence, recency.  
2. Remove lowest‑value referents.  
3. Compress attributes (drop low‑confidence fields).  
4. Summarize lineage (collapse older nodes).  
5. Normalize ordering.

### **6.3 Compression Rules**
Compression reduces storage cost:

- collapse repeated surface forms  
- merge low‑confidence attributes  
- summarize lineage into checkpoints  
- reduce ambiguity entries to top‑k conflicts

---

# **7. Size Control (Resolution)**

COB must remain bounded in:

- number of layers (20)  
- number of referents per layer  
- lineage depth  
- ambiguity entries  
- update operations per turn  

### **7.1 Size Control Mechanisms**
- decay  
- pruning  
- compression  
- eviction  
- merge/split  
- CST drift correction  

### **7.2 Deterministic Size Control**
All size control operations must be:

- deterministic  
- replay‑safe  
- ordering‑stable  
- lineage‑consistent  

This ensures COB remains stable across long sessions.

---

# **8. Retirement (Resolution)**

Retirement removes layers that are no longer relevant.

### **8.1 Retirement Conditions**
- decay_state exceeds retirement threshold  
- strength and importance both below minimum  
- CST issues retirement signal  
- referent map collapses  
- lineage continuity breaks irrecoverably  

### **8.2 Retirement Algorithm**
1. Archive lineage.  
2. Remove layer deterministically.  
3. Rebalance ordering.  
4. Update decay_state of remaining layers.

---

# **9. Next Steps**
- Draft `cob_interaction_and_safety.md` (CST/CIL/CEx/SSRGn interactions, collapse detection, recovery, freeze/thaw).  
- Begin extracting stable answers into formal 20.x requirement documents.  
- Shrink this paper as answers stabilize.

---

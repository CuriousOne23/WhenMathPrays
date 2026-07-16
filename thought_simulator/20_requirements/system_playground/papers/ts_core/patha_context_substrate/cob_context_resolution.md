# **cob_context_resolution.md**  
### *Conversation Object Basin — Resolution Paper (Working Draft v0.3)*

---

## **0. Purpose**
This paper provides the **answers and design resolutions** for the Conversation Object Basin (COB), the long‑horizon identity substrate of the TS context layer.

All **questions** for COB are maintained separately in:

```
papers/ts_core/patha_context_substrate/questions_for_cob_substrate.md
```

This paper does **not** repeat those questions.  
Instead, it answers them — directly or indirectly — and will grow into multiple resolution papers if needed.

COB is the keystone of the TS context layer.  
Once COB is resolved, CST, CIL, CEx, SSRGn, temporal ordering, snapshot strategy, and collapse/recovery follow naturally.

---

# **1. Reference: COB Question Substrate**
All operational, structural, determinism, interaction, and failure‑mode questions for COB are defined in:

**`questions_for_cob_substrate.md` (v0.4)**

This resolution paper answers those questions in structured form.

---

# **2. Resolution Scope**
COB resolution will be delivered across **three papers**:

1. **`cob_context_resolution.md`**  
   *Core identity model, referent model, merge/split logic, deterministic replay.*

2. **`cob_lifecycle_and_capacity.md`**  
   *Layer lifecycle, assignment, eviction, decay, pruning, compression.*

3. **`cob_interaction_and_safety.md`**  
   *CST/CIL/CEx/SSRGn interactions, collapse detection, recovery, freeze/thaw.*

This paper (v0.3) covers the **core identity substrate**, which must be answered first.

---

# **3. COB Identity Layer Model (Resolution)**

The identity layer is the atomic unit of long‑horizon continuity.

### **3.1 Identity Layer Schema (Foundational Answer)**
Each identity layer is a structured object:

```
IdentityLayer {
    layer_id: StableID,
    referent_map: ReferentMap,
    lineage: LineageStructure,
    strength: float,
    importance: float,
    ambiguity: float,
    decay_state: float,
    timestamps: {
        created: TurnID,
        updated: TurnID
    }
}
```

**Notes:**

- `layer_id` is deterministic across replay.  
- `strength` measures how central the identity is to the user.  
- `importance` measures how central the identity is to the conversation.  
- `ambiguity` measures internal referent conflict.  
- `decay_state` controls pruning and aging.  
- `lineage` provides continuity across turns.

This schema answers the highest‑priority question in the substrate.

---

# **4. Referent Map Model (Resolution)**

The referent map is the structured representation of identity‑linked referents.

### **4.1 Referent Map Entry Schema**
```
ReferentEntry {
    referent_id: StableID,
    surface_forms: [string],
    attributes: { key: value },
    strength: float,
    confidence: float,
    ambiguity: float,
    lineage_pointer: StableID,
    timestamps: {
        created: TurnID,
        updated: TurnID
    }
}
```

### **4.2 Referent Map Structure**
```
ReferentMap {
    entries: [ReferentEntry],
    ordering: DeterministicOrderingRule
}
```

**Notes:**

- `surface_forms` supports multi‑word referents.  
- `attributes` supports structured semantic fields.  
- `ambiguity` supports referent collision detection.  
- `lineage_pointer` ties referents to identity history.  
- `ordering` ensures deterministic replay.

This resolves the second keystone question.

---

# **5. Merge Logic (Resolution)**

Merge logic determines how new SSRGn meaning integrates into COB.

### **5.1 Deterministic Merge Algorithm**
When new meaning arrives:

1. **Identify target layer** using assignment rules (defined in lifecycle paper).  
2. **Match referents** by referent_id or surface_form similarity.  
3. **Merge attributes** using deterministic field‑wise rules.  
4. **Update strength** using weighted averaging:  
   ```
   new_strength = α * old_strength + (1 - α) * incoming_strength
   ```
5. **Update ambiguity** based on referent conflict.  
6. **Update timestamps** deterministically.  
7. **Normalize ordering** using deterministic sort.

### **5.2 Conflict Resolution**
Conflicts are resolved by:

- confidence weighting  
- ambiguity penalties  
- lineage continuity  
- CST override signals  

This resolves the third keystone question.

---

# **6. Split / Merge Lifecycle (Resolution)**

### **6.1 Split Conditions**
A layer splits when:

- ambiguity exceeds threshold  
- referent clusters diverge  
- CST issues a split signal  
- lineage continuity breaks  

### **6.2 Split Algorithm**
1. Cluster referents deterministically.  
2. Create new layers with stable IDs.  
3. Distribute referents based on cluster membership.  
4. Copy lineage pointers.  
5. Normalize strength/importance.  
6. Update timestamps.

### **6.3 Merge Conditions**
Layers merge when:

- referent clusters converge  
- ambiguity drops below threshold  
- CST issues a merge signal  
- decay suggests consolidation  

This resolves the fourth keystone question.

---

# **7. Deterministic Replay Model (Resolution)**

Replay determinism is required for CST, CIL, CEx, SSRGn, and Path B.

### **7.1 Deterministic Replay Requirements**
COB replay must guarantee:

- stable layer IDs  
- stable referent IDs  
- stable ordering  
- stable merge/split outcomes  
- stable decay outcomes  
- stable timestamps (normalized)  
- stable lineage reconstruction  

### **7.2 Replay Algorithm**
Replay reconstructs COB state by:

1. Replaying SSRGn packets in deterministic order.  
2. Applying merge/split rules deterministically.  
3. Applying decay rules deterministically.  
4. Reconstructing lineage deterministically.  
5. Producing identical snapshots.

This resolves the fifth keystone question.

---

# **8. Assignment & Eviction (Resolution Overview)**

Full details will be in `cob_lifecycle_and_capacity.md`, but core rules are:

### **8.1 Assignment**
New information is assigned based on:

- referent similarity  
- lineage continuity  
- strength/importance  
- ambiguity thresholds  
- CST override signals  

### **8.2 Eviction**
When the 21st conversation appears:

- compute eviction score = f(strength, importance, recency, decay)  
- evict the lowest‑score layer  
- optionally merge before eviction  
- CST may override eviction

---

# **9. Next Steps**
- Expand lifecycle and capacity rules in `cob_lifecycle_and_capacity.md`.  
- Expand interaction and safety rules in `cob_interaction_and_safety.md`.  
- Begin integrating answers into formal 20.x requirement documents.  
- Shrink this paper as answers stabilize.

---

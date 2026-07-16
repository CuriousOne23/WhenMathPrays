# **cob_interaction_and_safety.md**  
### *Conversation Object Basin — Interaction & Safety Resolution (Working Draft v0.1)*

---

## **0. Purpose**
This paper resolves the **interaction, safety, and cross‑block behavior** of the Conversation Object Basin (COB). It defines how COB interacts with CST, CIL, CEx, and SSRGn, and how COB maintains stability, determinism, and safety under correction, extraction, regeneration, and drift.

All questions for COB are maintained separately in:

```
questions_for_cob_substrate.md (v0.4)
```

This paper does **not** repeat those questions.  
It builds directly on:

- `cob_context_resolution.md` (identity & referent model, merge/split logic, deterministic replay)  
- `cob_lifecycle_and_capacity.md` (creation, assignment, eviction, decay, pruning, compression)

This paper precedes the interface‑specific contracts:

- `cob_expectations_for_cst.md`  
- `cob_interface_to_ssrgn.md`  
- `cob_interface_to_cex.md`

---

# **1. Interaction Overview**
COB is the long‑horizon identity substrate.  
It interacts with four major blocks:

- **CST** — stabilizes COB by detecting drift and issuing corrective signals.  
- **CIL** — merges short‑term cues into COB.  
- **CEx** — extracts identity information from COB.  
- **SSRGn** — regenerates meaning that COB ingests.

This paper defines **how COB behaves** during these interactions — not what the other blocks must do.  
Those expectations are defined in separate interface papers.

---

# **2. COB Interaction with CST (Resolution)**

CST is the stability layer.  
COB must remain deterministic under CST correction.

### **2.1 CST Inputs to COB**
CST may send the following signals:

- **split_signal** — identity drift detected  
- **merge_signal** — identity convergence detected  
- **weaken_signal** — reduce strength/importance  
- **strengthen_signal** — increase strength/importance  
- **freeze_signal** — temporarily halt updates  
- **thaw_signal** — resume updates  
- **retire_signal** — remove stale identity  
- **ambiguity_signal** — referent conflict detected  
- **drift_signal** — long‑horizon drift detected

### **2.2 COB Response Rules**
COB must respond deterministically:

1. **Split signals**  
   - Trigger deterministic split algorithm.  
   - Reassign referents based on cluster analysis.  
   - Preserve lineage continuity.

2. **Merge signals**  
   - Trigger deterministic merge algorithm.  
   - Combine referent maps.  
   - Normalize strength/importance.

3. **Weaken/strengthen signals**  
   - Adjust strength/importance using deterministic scaling.  
   - Update decay_state accordingly.

4. **Freeze/thaw signals**  
   - Freeze: COB halts updates, merges, splits, pruning.  
   - Thaw: COB resumes updates and applies queued operations.

5. **Retire signals**  
   - Trigger deterministic retirement algorithm.  
   - Archive lineage.  
   - Rebalance ordering.

6. **Ambiguity/drift signals**  
   - Increase ambiguity penalties.  
   - Adjust assignment thresholds.  
   - Possibly trigger split or merge.

### **2.3 Safety Rules**
- CST cannot delete lineage.  
- CST cannot reorder layers arbitrarily.  
- CST cannot modify referent attributes directly.  
- CST corrections must be replay‑safe.  
- COB must log all CST overrides for deterministic replay.

---

# **3. COB Interaction with CIL (Resolution)**

CIL merges short‑term cues into COB.

### **3.1 CIL Inputs to COB**
CIL provides:

- short‑term referent cues  
- short‑term attribute updates  
- short‑term ambiguity signals  
- short‑term lineage hints  
- short‑term strength/importance adjustments

### **3.2 COB Response Rules**
COB integrates CIL cues using:

- deterministic merge logic  
- referent similarity  
- lineage continuity  
- ambiguity penalties  
- decay adjustments

### **3.3 Safety Rules**
- CIL cannot force layer creation.  
- CIL cannot force layer deletion.  
- CIL cannot override CST signals.  
- CIL updates must be idempotent and replay‑safe.

---

# **4. COB Interaction with CEx (Resolution)**

CEx extracts identity information from COB.

### **4.1 CEx Reads**
CEx may read:

- referent maps  
- lineage  
- strength/importance  
- ambiguity  
- decay_state  
- timestamps  
- ordering

### **4.2 CEx Must Not Modify**
CEx cannot:

- modify referent maps  
- modify lineage  
- modify strength/importance  
- modify ambiguity  
- modify decay_state  
- modify ordering  
- create or delete layers

### **4.3 Safety Rules**
- CEx reads must be deterministic.  
- CEx must not read frozen layers unless allowed.  
- CEx must not trigger merge/split.  
- CEx must not trigger eviction or retirement.

---

# **5. COB Interaction with SSRGn (Resolution)**

SSRGn regenerates meaning that COB ingests.

### **5.1 SSRGn Inputs to COB**
SSRGn provides:

- regenerated referents  
- regenerated attributes  
- regenerated ambiguity  
- regenerated lineage hints  
- regenerated structure  
- regenerated confidence scores

### **5.2 COB Response Rules**
COB ingests SSRGn packets using:

- deterministic merge logic  
- assignment algorithm  
- ambiguity penalties  
- lineage continuity  
- decay adjustments

### **5.3 Safety Rules**
- SSRGn cannot force layer creation.  
- SSRGn cannot force layer deletion.  
- SSRGn cannot override CST signals.  
- SSRGn packets must be ordered deterministically.  
- SSRGn must not modify lineage directly.

---

# **6. Freeze/Thaw Mechanism (Resolution)**

Freeze/thaw is essential for deterministic correction and recovery.

### **6.1 Freeze Conditions**
COB enters freeze state when:

- CST issues freeze_signal  
- collapse detection triggers freeze  
- multi‑turn reasoning requires stability  
- ambiguity exceeds critical threshold  
- lineage continuity is at risk

### **6.2 Freeze Behavior**
While frozen:

- COB does not merge  
- COB does not split  
- COB does not prune  
- COB does not decay  
- COB does not assign new information  
- COB logs incoming updates for later replay

### **6.3 Thaw Behavior**
When thawed:

- COB replays queued updates deterministically  
- COB applies merges/splits if needed  
- COB resumes normal lifecycle operations

---

# **7. Collapse Detection & Recovery (Resolution)**

### **7.1 Collapse Types**
COB may detect:

- **identity collapse** — layer loses coherent referent structure  
- **referent collapse** — referent map becomes contradictory  
- **lineage collapse** — lineage continuity breaks  
- **continuity collapse** — long‑horizon identity becomes unstable

### **7.2 Collapse Detection**
Collapse is detected via:

- ambiguity thresholds  
- drift thresholds  
- lineage discontinuity  
- referent conflict  
- CST signals  
- SSRGn uncertainty  
- CIL conflict signals

### **7.3 Recovery Algorithm**
1. Freeze COB.  
2. Identify collapse type.  
3. Apply deterministic recovery strategy:  
   - split  
   - merge  
   - prune  
   - retire  
   - reassign  
4. Thaw COB.  
5. Resume deterministic replay.

---

# **8. Next Steps**
- Draft `cob_expectations_for_cst.md` (COB → CST contract).  
- Draft `cob_interface_to_ssrgn.md` (COB → SSRGn contract).  
- Draft `cob_interface_to_cex.md` (COB → CEx contract).  
- Begin extracting stable answers into formal 20.x requirement documents.  
- Shrink this paper as answers stabilize.

---

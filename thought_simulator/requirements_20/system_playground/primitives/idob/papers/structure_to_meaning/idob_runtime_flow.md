# **idob_runtime_flow.md**  
### *Cycle‑by‑Cycle Runtime Execution Flow for IdOB*

---

## **1. Purpose**

This document defines the **runtime execution flow** of IdOB — the exact sequence of operations IdOB performs when converting:

> **structural geometry → meaning groups → meaning semantics → stabilized meaning → OuBA handoff**

It is the operational companion to:

- `idob_struc_to_meaning.md` (architecture)  
- `idob_meaning_dictionary.yaml`  
- `meaning_groups.yaml`  
- `struct_to_meaning_map.yaml`  
- `idob_object.yaml`  

This paper describes **how IdOB runs**, cycle by cycle, under the unified search schema (4–6 cycles).

---

## **2. Runtime Overview**

IdOB runtime consists of **four phases**:

1. **Initialization**  
2. **Meaning Group Search (coarse → medium → fine)**  
3. **Meaning Refinement & Stabilization**  
4. **Finalization & OuBA Handoff**

Each phase consumes part of the **IdOB search budget**, which is unified across depth and parallelism:

> **IdOB_search_budget_max = 6**  
> **IdOB_search_budget_min = 4**

IdOB stops when:

- meaning_delta_h stabilizes, or  
- identity envelope stabilizes, or  
- search budget is exhausted, or  
- CTP signals time exhaustion.

---

## **3. Phase 1 — Initialization**

### **3.1 Input from PT1**
PT1 provides:

- structural_hash  
- semantic_field_id  
- semantic_role_id  
- semantic_object_id  
- gradient_id  
- universe_id  
- subfield_id  
- residue_hash  
- routing_signature  
- identity metadata  

### **3.2 Create IdOB Object**
IdOB creates a new `idob_object`:

```yaml
idob_object:
  structural: {...}
  meaning_group: {...}
  meaning_semantics: {...}
  idob_semantics: {...}
  identity_envelope: {...}
  search_control: {...}
  finalization: {...}
```

### **3.3 Initialize Search Control**
```yaml
idob_search_budget_max: 6
idob_search_budget_min: 4
idob_search_budget_used: 0
idob_search_mode: single
```

### **3.4 Initialize Identity Envelope**
Identity envelope begins with:

- identity_tags  
- identity_vector  
- identity_importance = baseline  
- identity_delta = 0  

---

## **4. Phase 2 — Meaning Group Search**

Meaning group search has **three tiers**:

1. **Coarse Tier**  
2. **Medium Tier**  
3. **Fine Tier**

Each tier consumes **one unit** of search budget.

### **4.1 Coarse Tier**

IdOB performs:

1. Lookup structural_hash in `struct_to_meaning_map.yaml`  
2. Retrieve meaning_group_candidates  
3. Rank candidates using:
   - identity envelope  
   - cue envelopes  
   - invariants  
   - routing signatures  

IdOB selects **2–3 coarse candidates**.

Budget used: **+1**

---

### **4.2 Medium Tier**

IdOB narrows candidates by:

- comparing meaning dimensions  
- comparing invariants  
- comparing identity anchors  
- comparing cue envelopes  

IdOB selects **1–2 medium candidates**.

Budget used: **+1**

---

### **4.3 Fine Tier**

IdOB selects the **final meaning_group_id**.

Budget used: **+1**

At this point:

- meaning group is chosen  
- meaning is NOT yet stabilized  
- identity envelope is NOT yet stabilized  
- meaning_semantics[] is NOT yet final  

IdOB must continue to **refinement**.

---

## **5. Phase 3 — Meaning Refinement & Stabilization**

This phase consumes **1–3 cycles**, depending on:

- meaning_delta_h  
- identity_delta  
- CTP time pressure  
- search budget remaining  

### **5.1 Compute Meaning Semantics**

IdOB computes meaning_semantics[] using:

- meaning dimensions  
- meaning invariants  
- meaning cues  
- meaning triggers/suppressors  
- identity envelope modulation  

### **5.2 Compute meaning_delta_h**

$$
\Delta h_{\text{meaning}} = \| M_{i} - M_{i-1} \|
$$

If:

$$
|\Delta h_{\text{meaning}}| < \varepsilon_{\text{meaning}}
$$

→ meaning stabilized.

### **5.3 Update Identity Envelope**

Identity envelope is updated using:

- identity tags  
- identity cues  
- identity anchors  
- meaning dimensions  
- meaning group invariants  

Identity envelope may shift meaning_semantics[].

### **5.4 Check Identity Stabilization**

If:

$$
|\Delta h_{\text{identity}}| < \varepsilon_{\text{identity}}
$$

→ identity stabilized.

### **5.5 Increment Budget**

Budget used: **+1 per refinement cycle**

### **5.6 Continue or Stop**

IdOB continues refinement until:

- meaning stabilized, or  
- identity stabilized, or  
- budget exhausted, or  
- CTP signals time exhaustion  

Typical refinement cycles: **1–2**

Total cycles: **4–6**

---

## **6. Phase 4 — Finalization & OuBA Handoff**

### **6.1 Finalize Meaning**

IdOB freezes:

- meaning_semantics[]  
- idob_semantics[]  
- identity envelope  
- meaning_resolution_status  

### **6.2 Set Finalization Status**

Possible statuses:

- `stable`  
- `budget_exhausted`  
- `identity_stable`  
- `time_exhausted`  

### **6.3 Mark Ready for OuBA**

```yaml
ready_for_ouba: true
```

### **6.4 Handoff**

IdOB hands off:

- meaning_semantics[]  
- idob_semantics[]  
- identity envelope  
- meaning_resolution_status  

OuBA performs:

- truth evaluation  
- belief evaluation  
- output generation  

IdOB does **not** perform truth or belief.

---

## **7. Full Runtime Flow (Summary)**

### **Cycle 0 — Initialization**
- Create IdOB object  
- Load structural geometry  
- Initialize identity envelope  
- Initialize search control  

### **Cycle 1 — Coarse Tier**
- Retrieve meaning_group_candidates  
- Rank candidates  
- Select coarse candidates  

### **Cycle 2 — Medium Tier**
- Narrow candidates  
- Select medium candidates  

### **Cycle 3 — Fine Tier**
- Select final meaning_group_id  

### **Cycle 4 — Refinement**
- Compute meaning_semantics[]  
- Compute meaning_delta_h  
- Update identity envelope  

### **Cycle 5 — Stabilization**
- Check meaning_delta_h  
- Check identity_delta  
- If stable → finalize  

### **Cycle 6 — Finalization (if needed)**
- Freeze meaning  
- Freeze identity envelope  
- Set resolution status  
- Handoff to OuBA  

---

## **8. Determinism & Replay‑Safety**

IdOB runtime is deterministic because:

- structural_hash is stable  
- meaning groups are stable  
- meaning dimensions are stable  
- identity envelope is stable  
- search budget is bounded  
- refinement cycles converge  
- stabilization thresholds are fixed  

Replay‑safety is guaranteed.

---

## **9. CTP Coordination**

CTP coordinates:

- parallel meaning candidates  
- parallel refinement branches  
- time pressure  
- global TS budget  

CTP may:

- prune candidates  
- reduce refinement cycles  
- force early stabilization  
- force early OuBA handoff  

CTP ensures TS responsiveness.

---

## **10. Conclusion**

This paper defines the **complete runtime flow** of IdOB:

- initialization  
- meaning group search  
- meaning refinement  
- stabilization  
- finalization  
- OuBA handoff  

It is the operational backbone of IdOB’s structure→meaning mapping.

---

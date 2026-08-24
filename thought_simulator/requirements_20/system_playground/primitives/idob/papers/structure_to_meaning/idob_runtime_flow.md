# **idob_runtime_flow.md**  
### *Cycle‑by‑Cycle Runtime Execution Flow for IdOB (CvThP‑Supervised)*

---

## **1. Purpose**

This document defines the **runtime execution flow** of IdOB — the exact sequence of operations IdOB performs when converting:

> **structural geometry → meaning groups → meaning semantics → stabilized meaning → OuBA handoff**

It integrates:

- CvThP (Conversational Thread Processor)  
- conversational identity envelope (CIE)  
- meaning dimensions  
- meaning groups  
- struct_to_meaning_map  
- unified search schema (4–6 cycles)  
- stabilization rules  

This is the authoritative runtime description.

---

## **2. Runtime Overview**

IdOB runtime consists of **four phases**:

1. **Initialization**  
2. **Meaning Group Search (coarse → medium → fine)**  
3. **Meaning Refinement & Stabilization**  
4. **Finalization & OuBA Handoff**

CvThP supervises:

- cycle scheduling  
- parallel branch management  
- stabilization detection  
- budget enforcement  
- time‑pressure handling  

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
idob_search_budget_min: 4
idob_search_budget_max: 6
idob_search_budget_used: 0
```

### **3.4 Initialize Conversational Identity Envelope (CIE)**

Identity envelope begins with:

- identity_tags  
- identity_vector  
- identity_importance = baseline  
- identity_delta = 0  

---

## **4. Phase 2 — Meaning Group Search**

Meaning group search has **three tiers**, each consuming **one unit** of search budget.

### **4.1 Coarse Tier**

Steps:

1. Lookup structural_hash in `struct_to_meaning_map.yaml`  
2. Retrieve meaning_group_candidates  
3. Rank candidates using:  
   - conversational identity envelope  
   - cue envelopes  
   - invariants  
   - routing signatures  

Output: **2–3 coarse candidates**

Budget used: **+1**

---

### **4.2 Medium Tier**

Narrow candidates using:

- meaning dimensions  
- invariants  
- identity anchors  
- cue envelopes  

Output: **1–2 medium candidates**

Budget used: **+1**

---

### **4.3 Fine Tier**

Select **final meaning_group_id**.

Budget used: **+1**

At this point:

- meaning group chosen  
- meaning not yet stabilized  
- identity envelope not yet stabilized  

IdOB proceeds to refinement.

---

## **5. Phase 3 — Meaning Refinement & Stabilization**

This phase consumes **1–3 cycles**, depending on:

- meaning_delta_h  
- identity_delta  
- CvThP time pressure  
- remaining budget  

### **5.1 Compute Meaning Semantics**

IdOB computes meaning_semantics[] using:

- meaning dimensions  
- meaning invariants  
- meaning cues  
- triggers/suppressors  
- conversational identity modulation  

### **5.2 Compute meaning_delta_h**

$$
\Delta h_{\text{meaning}} = \| M_{i} - M_{i-1} \|
$$

If:

$$
|\Delta h_{\text{meaning}}| < \varepsilon_{\text{meaning}}
$$

→ meaning stabilized.

### **5.3 Update Conversational Identity Envelope**

Identity envelope updated using:

- identity tags  
- identity cues  
- identity anchors  
- meaning dimensions  
- meaning invariants  

### **5.4 Compute identity_delta**

$$
\Delta h_{\text{identity}} = \| I_{i} - I_{i-1} \|
$$

If:

$$
|\Delta h_{\text{identity}}| < \varepsilon_{\text{identity}}
$$

→ identity stabilized.

### **5.5 Increment Budget**

Budget used: **+1 per refinement cycle**

### **5.6 Continue or Stop**

IdOB continues refinement until:

- meaning stabilized  
- identity stabilized  
- budget exhausted  
- **CvThP signals time exhaustion**  

---

## **6. Phase 4 — Finalization & OuBA Handoff**

### **6.1 Freeze Meaning**

IdOB freezes:

- meaning_semantics[]  
- idob_semantics[]  
- conversational identity envelope  

### **6.2 Set Finalization Status**

Possible statuses:

- `stable`  
- `identity_stable`  
- `budget_exhausted`  
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
- semantic consistency evaluation  

IdOB does **not** perform truth or belief.

---

## **7. Full Runtime Flow (Summary)**

### **Cycle 0 — Initialization**
- Create IdOB object  
- Load structural geometry  
- Initialize CIE  
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
- Update CIE  

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

## **8. CvThP Coordination (Updated)**

CvThP supervises:

- parallel meaning candidates  
- parallel refinement branches  
- stabilization detection  
- pruning unstable branches  
- enforcing search budget  
- enforcing time pressure  
- guaranteeing deterministic convergence  

CvThP ensures IdOB remains:

- bounded  
- deterministic  
- replay‑safe  
- conversationally responsive  

---

## **9. Determinism & Replay‑Safety**

IdOB runtime is deterministic because:

- structural_hash is stable  
- meaning groups are stable  
- meaning dimensions are stable  
- identity envelope is stable  
- search budget is bounded  
- stabilization thresholds are fixed  
- CvThP scheduling is deterministic  

Replay‑safety is guaranteed.

---

## **10. Conclusion**

This paper defines the **complete CvThP‑supervised runtime flow** of IdOB:

- initialization  
- meaning group search  
- meaning refinement  
- stabilization  
- finalization  
- OuBA handoff  

It is the operational backbone of IdOB’s structure→meaning mapping.

---

# **cvthp_runtime.md**  
### *Conversational Thread Processor — Runtime Model, Scheduling, Parallelism, and Stabilization Supervision*

---

## **1. Purpose**

The **Conversational Thread Processor (CvThP)** is the runtime subsystem that supervises:

- IdOB’s multi‑cycle execution  
- IdOB’s parallel meaning branches  
- IdOB’s stabilization detection  
- IdOB’s search budget enforcement  
- conversational identity pressure  
- global conversational timing  
- deterministic replay across TS runs  

CvThP is **not** part of IdOB.  
It is the **execution coordinator** that ensures IdOB behaves safely, deterministically, and within bounded runtime.

This paper defines CvThP’s runtime model.

---

## **2. Why CvThP Exists**

IdOB is the only OB that:

- runs 4–6 cycles  
- spawns parallel meaning candidates  
- refines meaning across cycles  
- modulates meaning using conversational identity  
- must detect stabilization  
- must converge deterministically  
- must remain replay‑safe  

Without CvThP, IdOB could:

- run too long  
- spawn too many branches  
- oscillate meaning or identity  
- fail to stabilize  
- break replay‑safety  
- degrade TS responsiveness  

CvThP prevents all of these failure modes.

---

## **3. CvThP Responsibilities**

CvThP supervises IdOB in **seven domains**:

### **1. Scheduling**
Controls when IdOB starts, stops, and how many cycles it receives.

### **2. Parallelism**
Manages parallel meaning‑candidate branches.

### **3. Stabilization Detection**
Monitors meaning_delta_h and identity_delta across branches.

### **4. Budget Enforcement**
Ensures IdOB stays within:

- min cycles = 4  
- max cycles = 6  

### **5. Time Pressure Handling**
Forces early stabilization when TS is under load.

### **6. Branch Merging & Pruning**
Selects the best branch and eliminates others.

### **7. Deterministic Replay**
Guarantees identical results across identical inputs.

---

## **4. CvThP Runtime Model**

CvThP operates as a **cycle‑based scheduler**.

IdOB cycles:

1. Coarse Tier  
2. Medium Tier  
3. Fine Tier  
4. Refinement  
5. Stabilization  
6. (Optional) Finalization under pressure  

CvThP supervises each cycle.

---

## **5. Scheduling Rules**

CvThP applies the following scheduling rules:

### **Rule 1 — Start IdOB only after structural geometry is complete**
IdOB begins only when PT1 has produced:

- structural_hash  
- semantic_field_id  
- semantic_role_id  
- semantic_object_id  
- gradient_id  
- universe_id  
- subfield_id  
- residue_hash  
- routing_signature  

### **Rule 2 — Enforce cycle limits**
IdOB must run at least **4 cycles** and at most **6 cycles**.

### **Rule 3 — Check stabilization after each cycle**
CvThP checks:

- meaning_delta_h  
- identity_delta  

### **Rule 4 — Stop IdOB immediately if stabilized**
Meaning or identity stabilization ends the runtime.

### **Rule 5 — Stop IdOB if time pressure is signaled**
CvThP may force early stabilization.

---

## **6. Parallelism Management**

CvThP supervises parallel meaning branches.

### **6.1 Branch Creation**
When IdOB has multiple meaning_group_candidates:

```
[g1, g2, g3]
```

CvThP spawns:

```
branch(g1)
branch(g2)
branch(g3)
```

### **6.2 Branch Execution**
Each branch independently:

- computes meaning_semantics[]  
- applies conversational identity modulation  
- computes meaning_delta_h  
- computes identity_delta  
- checks stabilization  

### **6.3 Branch Limits**
CvThP enforces:

- max parallel branches = 2–3  
- no unbounded parallelism  

---

## **7. Parallel Stabilization Detection**

CvThP selects the winning branch using:

### **Rule A — First stabilized branch wins**
If any branch stabilizes:

- prune all others  
- adopt stabilized branch  

### **Rule B — Lowest meaning_delta_h wins**
If multiple branches stabilize:

- choose smallest semantic change  

### **Rule C — Lowest identity_delta wins**
If meaning_delta_h ties:

- choose smallest identity change  

### **Rule D — Highest identity_importance alignment wins**
If both deltas tie:

- choose branch most aligned with conversational identity  

These rules guarantee deterministic convergence.

---

## **8. Branch Pruning**

CvThP prunes branches when:

- meaning_delta_h diverges  
- identity_delta diverges  
- branch conflicts with conversational identity  
- branch violates invariant tags  
- branch violates meaning dimension cohesion  
- branch violates routing signature alignment  
- branch exceeds parallelism budget  

Pruning ensures:

- bounded runtime  
- stable convergence  
- replay‑safe behavior  

---

## **9. Budget Enforcement**

CvThP enforces IdOB’s unified search budget:

```
min cycles = 4
max cycles = 6
```

If IdOB reaches max cycles without stabilization:

- CvThP forces finalization  
- meaning_resolution_status = budget_exhausted  

---

## **10. Time Pressure Handling**

CvThP may force early stabilization when:

- TS is under conversational load  
- latency must be reduced  
- global parallelism is high  
- multiple OBs are active  

CvThP signals:

```
time_exhausted = true
```

IdOB must stop immediately.

---

## **11. Deterministic Replay**

CvThP guarantees replay‑safety:

- same structural_hash → same meaning  
- same meaning groups → same branch set  
- same identity envelope → same modulation  
- same stabilization thresholds → same stop point  
- same parallelism rules → same branch selection  

Parallelism never introduces nondeterminism.

---

## **12. Interaction with IdOB**

CvThP interacts with IdOB through:

- cycle scheduling  
- parallel branch management  
- stabilization detection  
- budget enforcement  
- time pressure signals  
- branch merging/pruning  

IdOB provides:

- meaning_semantics[]  
- meaning_delta_h  
- identity_delta  
- stabilization state  

CvThP decides:

- when IdOB stops  
- which branch wins  
- when to hand off to OuBA  

---

## **13. Interaction with OuBA**

CvThP signals OuBA when IdOB is ready:

```
ready_for_ouba: true
```

OuBA then performs:

- truth evaluation  
- belief evaluation  
- semantic consistency evaluation  

CvThP does not modify meaning or identity.

---

## **14. Summary**

CvThP is the **runtime supervisor** for IdOB.

It provides:

- multi‑cycle scheduling  
- parallel branch management  
- stabilization detection  
- budget enforcement  
- time pressure handling  
- deterministic replay  
- branch merging/pruning  
- coordination with OuBA  

CvThP ensures IdOB is:

- safe  
- bounded  
- deterministic  
- replay‑safe  
- conversationally responsive  

CvThP completes the IdOB subsystem.

---

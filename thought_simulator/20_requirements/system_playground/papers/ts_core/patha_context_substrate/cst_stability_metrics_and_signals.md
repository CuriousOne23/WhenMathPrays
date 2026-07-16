# **cst_stability_metrics_and_signals.md**  
### *Context Stability Theory — Stability Metrics & Signals (Working Draft v0.1)*

---

## **0. Purpose**
This paper defines the **stability metrics** CST computes and the **signals** CST emits to maintain long‑horizon identity stability across the context substrate (COB + CIL + SSRGn).

All questions for CST are maintained separately in:

```
questions_for_cst_substrate.md
```

This paper does **not** repeat those questions.  
It complements:

- `cob_context_resolution.md`  
- `cob_lifecycle_and_capacity.md`  
- `cob_interaction_and_safety.md`  
- `cob_expectations_for_cst.md`  
- `cob_interface_to_cil.md`  
- `cob_interface_to_ssrgn.md`

and precedes CST’s deterministic replay paper.

---

# **1. CST Stability Overview**
CST is the **stability layer** for Path A.  
Its responsibilities:

- detect drift  
- detect ambiguity  
- detect lineage discontinuity  
- detect referent conflict  
- detect collapse  
- compute stability metrics  
- emit corrective signals  
- ensure deterministic replay  

CST never modifies COB directly.  
CST acts only through **signals**.

---

# **2. Stability Metrics (Resolution)**

CST computes a set of deterministic metrics each turn.  
These metrics drive all CST signals.

---

## **2.1 Drift Metrics**

### **Identity Drift**
Measures divergence between expected identity trajectory and current referent/lineage state.

```
identity_drift = f(referent_shift, lineage_shift, strength_drop, importance_drop)
```

### **Referent Drift**
Measures movement of referent clusters over time.

```
referent_drift = Δ(cluster_centroid)
```

### **Lineage Drift**
Measures discontinuity or branching in lineage.

```
lineage_drift = discontinuity_score(lineage_graph)
```

---

## **2.2 Ambiguity Metrics**

### **Referent Ambiguity**
```
referent_ambiguity = Σ ambiguity(referent_i)
```

### **Attribute Ambiguity**
```
attribute_ambiguity = Σ ambiguity(attribute_j)
```

### **Structural Ambiguity**
```
structural_ambiguity = ambiguity(structure)
```

### **Identity Ambiguity**
```
identity_ambiguity = weighted_sum(referent + attribute + structural)
```

---

## **2.3 Continuity Metrics**

### **Lineage Continuity**
```
lineage_continuity = continuity_score(lineage_graph)
```

### **Identity Continuity**
```
identity_continuity = f(lineage_continuity, referent_stability)
```

---

## **2.4 Collapse Metrics**

CST computes four collapse metrics:

- **identity_collapse_score**  
- **referent_collapse_score**  
- **lineage_collapse_score**  
- **continuity_collapse_score**

Each is a weighted combination of drift + ambiguity + continuity failure.

---

## **2.5 Relevance Metrics**

### **Strength Stability**
```
strength_stability = Δ(strength)
```

### **Importance Stability**
```
importance_stability = Δ(importance)
```

These help detect weakening identities.

---

## **2.6 Decay Metrics**

CST monitors decay progression:

```
decay_progress = Δ(decay_state)
```

High decay + high drift → retirement candidate.

---

# **3. CST Thresholds (Resolution)**

CST uses deterministic thresholds for all metrics.

### **3.1 Threshold Types**
- drift_threshold  
- ambiguity_threshold  
- continuity_threshold  
- collapse_threshold  
- retirement_threshold  
- freeze_threshold  
- thaw_threshold  

### **3.2 Threshold Requirements**
Thresholds must be:

- deterministic  
- replay‑safe  
- monotonic  
- stable across turns  
- stable across sessions  
- never stochastic  

---

# **4. CST Signals (Resolution)**

CST emits signals when metrics cross thresholds.

Signals are the **only** way CST influences COB.

---

## **4.1 Structural Signals**

### **split_signal**
Triggered when:

- identity_drift > drift_threshold  
- identity_ambiguity > ambiguity_threshold  
- lineage_drift > continuity_threshold  

### **merge_signal**
Triggered when:

- referent clusters converge  
- identity continuity increases  
- ambiguity drops below merge threshold  

### **retire_signal**
Triggered when:

- decay_progress > retirement_threshold  
- strength_stability < minimum  
- importance_stability < minimum  

---

## **4.2 Strength/Importance Signals**

### **weaken_signal**
Triggered when:

- strength_stability drops sharply  
- importance_stability drops sharply  

### **strengthen_signal**
Triggered when:

- referent stability increases  
- lineage continuity increases  

---

## **4.3 Stability Signals**

### **freeze_signal**
Triggered when:

- collapse_score > freeze_threshold  
- ambiguity > critical threshold  
- lineage continuity at risk  
- multi‑turn reasoning requires stability  

### **thaw_signal**
Triggered when:

- collapse resolved  
- ambiguity reduced  
- continuity restored  

---

## **4.4 Ambiguity & Drift Signals**

### **ambiguity_signal**
Triggered when:

- referent_ambiguity > ambiguity_threshold  
- attribute_ambiguity > ambiguity_threshold  
- structural_ambiguity > ambiguity_threshold  

### **drift_signal**
Triggered when:

- identity_drift > drift_threshold  
- referent_drift > drift_threshold  

---

## **4.5 Collapse Signals**

### **identity_collapse_signal**
### **referent_collapse_signal**
### **lineage_collapse_signal**
### **continuity_collapse_signal**

Triggered when collapse metrics exceed collapse_threshold.

---

# **5. Signal Semantics (Resolution)**

Each signal has deterministic semantics.

### **5.1 Split**
CST instructs COB to run deterministic split algorithm.

### **5.2 Merge**
CST instructs COB to run deterministic merge algorithm.

### **5.3 Weaken/Strengthen**
CST instructs COB to adjust relevance.

### **5.4 Freeze/Thaw**
CST instructs COB to halt/resume lifecycle operations.

### **5.5 Retire**
CST instructs COB to archive lineage and remove layer.

### **5.6 Ambiguity/Drift**
CST instructs COB to adjust assignment thresholds and ambiguity penalties.

### **5.7 Collapse**
CST instructs COB to enter recovery mode.

---

# **6. Deterministic Replay Requirements**

CST must ensure:

- metric computation is deterministic  
- threshold evaluation is deterministic  
- signal emission is deterministic  
- ordering of signals is deterministic  
- replay produces identical signals  

CST must log all signals for replay.

---

# **7. Safety Requirements**

CST must never:

- modify COB directly  
- modify referent maps  
- modify lineage  
- modify timestamps  
- modify decay_state  
- reorder layers  
- delete referents  
- create referents  
- create layers  
- delete layers (except via retire_signal)

CST must always:

- preserve determinism  
- preserve continuity  
- preserve ordering  
- preserve replay safety  

---

# **8. Next Steps**
- Draft `cst_deterministic_replay.md`  
- Draft `cst_signals_and_thresholds.md` (optional deeper dive)  
- Begin extracting stable answers into formal 20.x requirement documents  
- Shrink this paper as answers stabilize

---

# **ts_cognitive_invariants.md (v1.2)**  
**Status:** Draft v1.2  
**Purpose:** Define TS cognitive invariants, operationalize “recoverability,” specify quantitative thresholds, and outline concrete probe methods.  
**Goal:** Provide a falsifiable, experimentally runnable framework for testing TS cognitive pressures using LLM geometry.

---

## **1. Purpose and Posture**

This document asks a single scientific question:

> **Do the cognitive invariants proposed by TS appear as recoverable geometric features in trained LLMs?**

It does **not** claim:

- TS is the true form of cognition  
- LLMs contain TS objects  
- TS is buried inside transformer math  

Instead:

> **TS and LLMs are different realizations of shared cognitive pressures.  
TS is explicit; LLMs are implicit.  
Neither is the pure form of the other.**

The goal is **measurement**, not metaphysics.

---

## **2. Operational Definition of “Invariant”**

An invariant, in this document, means:

> **A cognitive feature that is recoverable from internal model geometry under controlled transformations.**

Recoverability is measured through:

- **linear probes**  
- **causal interventions**  
- **cluster stability**  
- **layer-wise persistence**  

This matches current mechanistic interpretability practice.  
It does **not** imply mathematical invariance under all transformations.

---

## **3. Threshold Rationale (New Section)**

Grok is correct: thresholds must be justified or marked provisional.

### **Chance Baselines**  
Chance accuracy depends on:

- number of classes  
- class balance  
- probe capacity  

Thus:

- **15% above chance** (Probe 1) is a *minimum detectable lift* for binary or ternary adjacency tasks.  
- **20% above chance** (Probe 2) is a *minimum meaningful lift* for contradiction detection, where class balance is typically 50/50.  
- **25% above chance** (Probe 3) is a *minimum ancestry reconstruction lift* for multi-class referent tracking.

These thresholds are **provisional** and must be validated through pilot runs.

### **Effect Size Normalization**  
“Normalized units” refer to:

> **Standardized mean difference (Cohen’s d) between ablated and non-ablated activation magnitudes.**

This is now explicitly defined.

### **Cluster Purity Threshold**  
Purity ≥ **0.7** is chosen because:

- below 0.6 clusters are typically unstable  
- above 0.7 clusters show meaningful semantic coherence  
- 0.7 is a standard interpretability heuristic

These thresholds may be adjusted after pilot data.

---

## **4. TS Cognitive Invariants (Operational Form)**

### **Invariant 1 — Structural Adjacency**  
Recoverable adjacency/boundary features across early-to-mid layers.

### **Invariant 2 — Constraint Geometry**  
Recoverable conflict/gap signatures across layers.

### **Invariant 3 — Cue Stability**  
Recoverable cue clusters across deep layers.

### **Invariant 4 — Routing Specialization**  
Recoverable path-selection specialization in attention heads.

### **Invariant 5 — Identity Basins**  
Recoverable identity features forming attractor-like regions.

---

## **5. Probes (Complete, Quantitative, and Expanded)**

### **Probe 1 — Structural Adjacency Recovery**  
**Tests:** Invariant 1  
**Method:**  
- Construct controlled paraphrases and reorderings.  
- Extract hidden states from layers 1–12.  
- Train linear probes (L2-regularized logistic regression).  
- Evaluate on held-out paraphrase/reordering sets.

**Pass:**  
- ≥ **15% above chance**  
- Stable across **≥ 4 consecutive layers**  
- Robust across **≥ 3 model scales**

**Fail:**  
- No recoverable adjacency features  
- Instability across layers  
- No multi-scale robustness

---

### **Probe 2 — Conflict/Gaps Signatures**  
**Tests:** Invariant 2  
**Method:**  
- Construct contradiction pairs (balanced binary classes).  
- Extract residual streams across layers.  
- Train linear probes.  
- Run causal mediation tests using activation patching.

**Pass:**  
- ≥ **20% above chance**  
- Causal effect size ≥ **0.1 (Cohen’s d)**  
- Stability across **≥ 5 layers**

**Fail:**  
- No recoverable conflict signature  
- No causal effect  
- No stability window

---

### **Probe 3 — Referent Lineage Reconstruction**  
**Tests:** Invariant 5  
**Method:**  
- Create long-context referent chains (≥ 8 mentions).  
- Extract hidden states across layers.  
- Train multi-class probes to reconstruct ancestry.  
- Score via top-k accuracy.

**Pass:**  
- ≥ **25% above chance**  
- Works across **≥ 2 architectures**  
- Lineage persists across **≥ 8 layers**

**Fail:**  
- No recoverable ancestry  
- Architecture-specific failure  
- No layer-wise persistence

---

### **Probe 4 — Identity Ablation**  
**Tests:** Invariant 5  
**Method:**  
- Identify identity features via causal tracing.  
- Ablate identity features in final layers.  
- Measure selective collapse of self-reference.

**Pass:**  
- Self-reference collapses  
- General reasoning ≥ **90% intact**  
- Collapse is selective

**Fail:**  
- No selective collapse  
- General reasoning collapses equally  
- Identity not recoverable

---

### **Probe 5 — Cue Manifold Stability**  
**Tests:** Invariant 3  
**Method:**  
- Inject modality/discourse cues.  
- Cluster deep-layer embeddings (k-means).  
- Measure cluster purity and stability.

**Pass:**  
- Purity ≥ **0.7**  
- Stability across **≥ 6 layers**  
- Robust across random seeds

**Fail:**  
- No stable cue clusters  
- No layer-wise persistence  
- No robustness

---

### **Probe 6 — Routing Specialization**  
**Tests:** Invariant 4  
**Method:**  
- Construct controlled path-selection tasks.  
- Measure attention head specialization via causal tracing.

**Pass:**  
- ≥ **3 heads** show specialization  
- Persistence across **≥ 4 layers**  
- Effect size ≥ **0.15 (Cohen’s d)**

**Fail:**  
- No specialized heads  
- Inconsistent specialization  
- No persistence

---

## **6. Evidential Strength Ranking**

1. **Causal ablation**  
2. **Causal mediation**  
3. **Linear probe recovery**  
4. **Cluster stability**  
5. **Correlation-only signals**

Interpretation must follow this order.

---

## **7. Scope Conditions**

These probes apply only when:

- the model is performing multi-turn reasoning  
- referent continuity matters  
- conflict resolution matters  
- identity stability matters  
- routing matters  

Short-context tasks are excluded.

---

## **8. Interpretation Framework**

### **Local failures → local revisions**  
A failure on conflict signatures revises the constraint geometry claim.  
It does **not** invalidate identity basins.

### **Global failures → TS revision**  
If **multiple invariants** fail across **multiple probes**, TS must be revised.

### **Global successes → TS support**  
If **multiple invariants** pass across **multiple probes**, TS is supported.

---

## **9. Cost Acknowledgment**

Robustness across:

- ≥ 3 model scales  
- ≥ 2 architectures  

is scientifically correct but computationally expensive.  
This is intentional.

---

## **10. Why this document matters**

This is the first TS document that is:

- falsifiable  
- quantitative  
- operational  
- testable  
- non-hierarchical  
- scientifically grounded  

It does not try to prove TS.  
It tries to **test TS**.

This is the shortest path from fog → terrain.

---

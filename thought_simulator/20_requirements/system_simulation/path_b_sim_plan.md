# **path_b_sim_plan.md**  
### *Path B Simulation Plan — Validation, Structure, and Proof Objectives*

---

## **1. Purpose of Path B Simulation**
Path B simulations validate that **realization** (expression) is:

- deterministic under fixed seed  
- meaning‑read‑only  
- invariant‑compliant  
- pipeline‑pure  
- replay‑safe  
- structurally correct (REx → RPlan → RPU → ReB)  

The goal is to **prove** that Path B behaves as a *closed algebra* that never invents meaning, never mutates semantic_core, and always respects constraints.

---

# **2. Simulation Overview Table (with Metrics)**

| Sim ID | Name | Input Complexity | Primary Goal | Key Metrics | Success Thresholds |
|--------|------|------------------|--------------|-------------|--------------------|
| **B1** | Minimal “Hello World” | Very Low | Wiring + determinism | - Replay Hash Match Rate<br>- Invariant Violation Count | - **100%** identical replay<br>- **0** invariant violations |
| **B2** | Style Variation | Low | Meaning vs expression separation | - semantic_core Drift Score<br>- Surface Variation Entropy | - Drift Score **0.00**<br>- Entropy **> 0.25** across seeds |
| **B3** | Multi‑Step Planning | Medium | Validate RPlan/RPU planning | - Plan Fidelity Score<br>- Step Alignment Ratio | - Fidelity **≥ 0.95**<br>- Alignment **≥ 0.90** |
| **B4** | Hard Constraints | Medium | Constraint enforcement | - Constraint Violation Count<br>- Token Budget Accuracy | - Violations **0**<br>- Token error **≤ 5%** |
| **B5** | Failure Modes | Medium | Graceful degradation | - Failure‑State Correctness<br>- Invariant Violation Count | - Correctness **= 1.0**<br>- Violations **0** |
| **B6** | Replay Consistency | Low | Deterministic replay | - Replay Hash Stability<br>- Seed Sensitivity Index | - Stability **= 1.0**<br>- Sensitivity **> 0.20** |
| **B7** | Plan Swapping | Medium | Plan independence from meaning | - Meaning Drift Score<br>- Structural Divergence Score | - Drift **0.00**<br>- Divergence **≥ 0.40** |
| **B8** | Stress Test | High | Stability under load | - Invariant Violation Count<br>- Latency Delta<br>- Memory Footprint Delta | - Violations **0**<br>- Latency Δ **< 15%**<br>- Memory Δ **< 10%** |

---

# **3. Simulation Details (with Metrics)**

---

## **B1 — Minimal “Hello World”**

| Metric | Description | Target |
|--------|-------------|--------|
| **Replay Hash Match Rate** | Hash(output₁) == Hash(output₂) | **100%** |
| **Invariant Violations** | Count of broken Path B rules | **0** |
| **Pipeline Latency** | REx→RPlan→RPU→ReB time | Informational only |

**Why:**  
This proves the pipeline is wired correctly and deterministic.

---

## **B2 — Style Variation**

| Metric | Description | Target |
|--------|-------------|--------|
| **semantic_core Drift Score** | Δ between meaning snapshots | **0.00** |
| **Surface Variation Entropy** | Shannon entropy across outputs | **> 0.25** |
| **Seed Sensitivity Index** | Δoutput / Δseed | **> 0.20** |

**Why:**  
This is the *core TS claim*: meaning is invariant, expression is variable.

---

## **B3 — Multi‑Step Planning**

| Metric | Description | Target |
|--------|-------------|--------|
| **Plan Fidelity Score** | How closely output follows plan | **≥ 0.95** |
| **Step Alignment Ratio** | Steps realized / steps planned | **≥ 0.90** |
| **Semantic Drift Score** | Meaning deviation | **0.00–0.02** |

**Why:**  
Proves Path B is a real planner, not a text generator.

---

## **B4 — Hard Constraints**

| Metric | Description | Target |
|--------|-------------|--------|
| **Constraint Violations** | Tone, channel, length errors | **0** |
| **Token Budget Accuracy** | |tokens_out − tokens_max| / tokens_max | **≤ 5%** |
| **Tone Compliance Score** | Match to required tone | **≥ 0.95** |

**Why:**  
Shows Path B respects constraints without mutating meaning.

---

## **B5 — Failure Modes**

| Metric | Description | Target |
|--------|-------------|--------|
| **Failure‑State Correctness** | Correct failure type returned | **1.0** |
| **Invariant Violations** | Should remain zero | **0** |
| **Fallback Attempts** | Attempts to call Path A | **0** |

**Why:**  
Path B must fail safely, not by breaking architecture.

---

## **B6 — Replay Consistency**

| Metric | Description | Target |
|--------|-------------|--------|
| **Replay Hash Stability** | Hash(output₁) == Hash(output₂) | **1.0** |
| **Seed Sensitivity Index** | Variation across seeds | **> 0.20** |
| **Plan Stability** | Plan unchanged across replays | **1.0** |

**Why:**  
Replay invariants are foundational to TS.

---

## **B7 — Plan Swapping**

| Metric | Description | Target |
|--------|-------------|--------|
| **Meaning Drift Score** | semantic_core change | **0.00** |
| **Structural Divergence Score** | Δstructure(plan₁, plan₂) | **≥ 0.40** |
| **Output Structural Fidelity** | Output matches plan | **≥ 0.95** |

**Why:**  
Proves Path B is modular and composable.

---

## **B8 — Stress Test**

| Metric | Description | Target |
|--------|-------------|--------|
| **Invariant Violations** | Under heavy load | **0** |
| **Latency Delta** | (latency_stress − latency_base) / base | **< 15%** |
| **Memory Footprint Delta** | Memory change under load | **< 10%** |
| **Output Stability Score** | No structural collapse | **≥ 0.90** |

**Why:**  
This is the final confidence test before implementation.

---

# **4. What We Are Trying to Prove (with Metrics)**

| Claim | Simulation(s) | Metric(s) | Threshold |
|-------|----------------|-----------|-----------|
| **Meaning ≠ Expression** | B2, B7 | Drift Score | **0.00** |
| **Deterministic Replay** | B1, B6 | Replay Hash Stability | **1.0** |
| **Constraint Obedience** | B4 | Violation Count | **0** |
| **No Semantic Writes in Path B** | All | Drift Score | **0.00** |
| **Plan‑Driven Realization** | B3, B7 | Fidelity Score | **≥ 0.95** |
| **Graceful Failure** | B5 | Failure Correctness | **1.0** |
| **Pipeline Purity** | All | Invariant Violations | **0** |

---

## **5. Recommended Execution Order**

1. **B1** — Wiring + determinism  
2. **B2** — Meaning vs expression  
3. **B3** — Planning correctness  
4. **B4** — Constraint enforcement  
5. **B5** — Failure modes  
6. **B6** — Replay consistency  
7. **B7** — Plan swapping  
8. **B8** — Stress test  

This order builds confidence layer‑by‑layer, exactly like validating a compiler pipeline.

---

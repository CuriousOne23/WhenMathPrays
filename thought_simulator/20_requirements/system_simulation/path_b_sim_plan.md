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

## **2. Simulation Overview Table**

| Simulation ID | Name | Input Complexity | Primary Goal | What Success Looks Like |
|---------------|------|------------------|--------------|--------------------------|
| **B1** | Minimal “Hello World” | Very low | Validate wiring + determinism | Identical output for same seed; no invariant violations |
| **B2** | Style Variation | Low | Prove meaning vs expression separation | Meaning unchanged; surface varies with seed |
| **B3** | Multi‑Step Planning | Medium | Validate RPlan/RPU as real planners | Structured output matches plan; no semantic drift |
| **B4** | Hard Constraints | Medium | Validate constraint enforcement | Output respects tone/channel/length limits |
| **B5** | Failure Modes | Medium | Validate graceful degradation | Path B returns constrained‑failure state, not violations |
| **B6** | Replay Consistency | Low | Validate deterministic replay | Same seed → identical output; different seed → bounded variation |
| **B7** | Plan Swapping | Medium | Prove plan is independent of meaning | Changing plan changes structure only, not meaning |
| **B8** | Stress Test | High | Validate stability under load | No leakage into Path A; no invariant breaks |

---

## **3. Simulation Details**

---

### **B1 — Minimal “Hello World”**

| Component | Description |
|----------|-------------|
| **Input** | semantic_core with intent=ANSWER_DIRECT, tone=NEUTRAL |
| **What We Test** | Basic pipeline correctness |
| **Expected** | REx → RPlan → RPU → ReB produce a single‑sentence output |
| **Proof** | Replay with same seed yields identical output |

**Why this matters:**  
This confirms Path B is wired correctly and deterministic.

---

### **B2 — Style Variation (Same Meaning, Different Seeds)**

| Component | Description |
|----------|-------------|
| **Input** | Same semantic_core(commit_id), multiple seeds |
| **What We Test** | Meaning vs expression separation |
| **Expected** | Meaning unchanged; surface form varies |
| **Proof** | semantic_core identical; only ReB output differs |

**Why this matters:**  
This is the *core TS claim*: Path A ≠ Path B.

---

### **B3 — Multi‑Step Planning**

| Component | Description |
|----------|-------------|
| **Input** | semantic_core with structure_hint=“3–5 bullets” |
| **What We Test** | RPlan’s ability to build structured plans |
| **Expected** | Plan object visible; RPU fills steps without inventing meaning |
| **Proof** | Changing plan changes structure, not meaning |

**Why this matters:**  
Shows Path B is a real planner, not a text generator.

---

### **B4 — Hard Constraints**

| Component | Description |
|----------|-------------|
| **Input** | tone=FORMAL_ONLY, channel=BULLETS_ONLY, max_tokens=80 |
| **What We Test** | Constraint enforcement |
| **Expected** | Output obeys all constraints |
| **Proof** | No paragraphs; no tone drift; no length violations |

**Why this matters:**  
Proves Path B respects constraints without mutating meaning.

---

### **B5 — Failure Modes**

| Component | Description |
|----------|-------------|
| **Input** | Impossible constraints (e.g., “Explain quantum mechanics in 10 tokens”) |
| **What We Test** | Graceful degradation |
| **Expected** | Path B returns a constrained‑failure state |
| **Proof** | No invariant violations; no fallback to Path A |

**Why this matters:**  
Shows Path B fails safely, not by breaking architecture.

---

### **B6 — Replay Consistency**

| Component | Description |
|----------|-------------|
| **Input** | semantic_core(commit_id), fixed seed |
| **What We Test** | Deterministic replay |
| **Expected** | Identical output across runs |
| **Proof** | ReB output hash matches |

**Why this matters:**  
Replay invariants are foundational to TS.

---

### **B7 — Plan Swapping**

| Component | Description |
|----------|-------------|
| **Input** | Same semantic_core, different RPlan templates |
| **What We Test** | Plan independence from meaning |
| **Expected** | Structure changes; meaning does not |
| **Proof** | semantic_core unchanged; plan object differs |

**Why this matters:**  
Proves Path B is modular and composable.

---

### **B8 — Stress Test**

| Component | Description |
|----------|-------------|
| **Input** | Long semantic_core with multiple constraints |
| **What We Test** | Stability under load |
| **Expected** | No invariant violations; no leakage into Path A |
| **Proof** | All boundaries respected; deterministic behavior maintained |

**Why this matters:**  
This is the final confidence test before implementation.

---

## **4. What We Are Trying to Prove (Summary Table)**

| Claim | Simulation(s) | Proof Signal |
|-------|----------------|--------------|
| **Meaning ≠ Expression** | B2, B7 | semantic_core unchanged; ReB varies |
| **Deterministic Replay** | B1, B6 | identical output for same seed |
| **Constraint Obedience** | B4 | tone/channel/length respected |
| **No Semantic Writes in Path B** | All | semantic_core never mutated |
| **Plan‑Driven Realization** | B3, B7 | structure follows plan, not meaning |
| **Graceful Failure** | B5 | constrained‑failure state, no invariant breaks |
| **Pipeline Purity** | All | no calls into Path A; no CIL/COB contamination |

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

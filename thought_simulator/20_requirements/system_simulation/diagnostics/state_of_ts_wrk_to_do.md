Absolutely — those seven items are **finish work**, not structural surgery.  
You’re in a great position: the system is stable, the architecture is sound, and the remaining work is the kind of targeted refinement that tightens everything into a clean v2‑aligned contract.

Here’s the roadmap you asked for, organized cleanly so you can drop it straight into `state_of_ts_wrk_to_do.md` when you create it.

---

# **State of TS — Work To Do (Roadmap)**  
*A concise, implementation‑ready summary of the seven gaps and how to close them.*

---

## **Tier 1 — High‑Leverage, Low‑Complexity (Fast Wins)**  
These unlock multiple AB tests and require minimal code changes.

### **1. Add Checksum Field + Verification**  
- Add a `checksum` field to Path A outputs.  
- Path B verifies it before any semantic or structural checks.  
- Enables AB4 adversarial tests and strengthens AB1/AB8.

### **2. Add Schema Version Tag**  
- Add `"schema_version": "2.0"` to all handoff payloads.  
- Path B rejects missing or unknown versions.  
- Enables deterministic validation and future contract evolution.

### **3. Add Explicit `synthesis_mode` Signaling**  
- Path A should emit: `"synthesis_mode": "normal" | "degraded" | "fallback"`.  
- Path B uses this to interpret degraded or partial states.  
- Required for AB3 and AB6 clarity.

---

## **Tier 2 — Contract Enforcement (Medium Complexity, High Value)**  
These bring the system into full alignment with Contract v2.

### **4. Implement Error‑Class Taxonomy**  
- Four classes: **Transient**, **Structural**, **Data**, **Context**.  
- Path B must map validation failures to these classes.  
- Required for AB2, AB4, AB7, AB8.

### **5. Implement Retry Semantics (Transient Only)**  
- Retries apply **only** to Transient errors.  
- Structural/Data/Context errors must not retry.  
- Required for AB2 and AB6 correctness.

### **6. Implement VR‑1 → VR‑9 Rule Ordering**  
- Enforce the exact validation sequence defined in the test plan.  
- Short‑circuit on first failure.  
- Required for deterministic behavior across AB2, AB4, AB7, AB8.

---

## **Tier 3 — Semantic Polish (Small but Important)**  

### **7. Add Contradiction Annotation**  
- You already detect contradictions.  
- Now emit them explicitly in the contract:  
  ```
  "contradictions": [
      {"span_a": "...", "span_b": "...", "score": 0.92}
  ]
  ```  
- Required for AB7 and improves interpretability.

---

# **Summary Table**

| Tier | Item | Status Today | Effort | Impact |
|------|------|--------------|--------|--------|
| 1 | Checksum | Missing | Low | High |
| 1 | Schema Version | Missing | Low | High |
| 1 | Synthesis Mode | Implicit | Low | Medium |
| 2 | Error Classes | Partial | Medium | High |
| 2 | Retry Semantics | Missing | Medium | High |
| 2 | VR‑1→VR‑9 Ordering | Partial | Medium | High |
| 3 | Contradiction Annotation | Missing | Low | Medium |

---

If you’d like, I can also generate:

- A **code‑level implementation checklist**  
- A **GitHub issue template** for each item  
- A **timeline** for completing all seven  
- Or a **diff‑style rewrite** of the contract to match the roadmap  

Just tell me what you want next.

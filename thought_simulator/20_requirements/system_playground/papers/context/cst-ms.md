# **CST‑MS: Metric Synthesis Module**  
**Context Stability Tracking — Metric Synthesis**  
**Version 1.0 — July 2026**

---

# **1. Overview**

CST‑MS synthesizes raw stability metrics produced by CST‑Core into unified, layer‑specific stability signals.  
Where CST‑Core measures drift, oscillation, ambiguity, collapse, continuity, and freeze/thaw, CST‑MS **combines** these metrics into deterministic stability summaries that COB can consume.

CST‑MS is a pure functional module:

- no randomness  
- no external state  
- no wall‑clock time  
- deterministic replay  
- monotonic threshold behavior  
- identical outputs under replay  

CST‑MS transforms raw CST‑Core metrics into:

- stability score  
- instability score  
- collapse risk  
- freeze risk  
- thaw readiness  
- ambiguity summary  
- drift summary  
- oscillation summary  

These synthesized signals form the **stability packet** that CST‑Mux will multiplex across layers.

---

# **2. Inputs and Outputs**

## **2.1 Inputs**

CST‑MS receives raw metrics from CST‑Core:

- drift  
- oscillation  
- ambiguity  
- collapse  
- continuity  
- freeze  
- thaw  
- register stability  
- field‑importance stability  

Each metric arrives as:

$$
M^f(L, t)
$$

where:

- $f$ = feature  
- $L$ = identity layer  
- $t$ = turn index  

CST‑MS also receives:

- layer‑specific thresholds  
- metric histories  
- freeze/thaw events  
- continuity restoration signals  

---

## **2.2 Outputs**

CST‑MS produces synthesized signals:

- **stability summary**  
- **instability summary**  
- **collapse risk**  
- **freeze risk**  
- **thaw readiness**  
- **ambiguity summary**  
- **drift summary**  
- **oscillation summary**  

These outputs are deterministic and layer‑specific.

---

# **3. Metric Normalization**

Raw CST‑Core metrics may have different ranges.  
CST‑MS normalizes each metric to $[0, 1]$.

Let $M^f(L, t)$ be a raw metric.  
Normalization is:

$$
\hat{M}^f(L, t) = \frac{M^f(L, t)}{M_{\max}^f(L)}
$$

where $M_{\max}^f(L)$ is the deterministic maximum for that metric and layer.

Normalization ensures:

- consistent synthesis  
- replay safety  
- deterministic scaling  
- monotonic behavior  

---

# **4. Metric Weighting**

Each identity layer has different stability sensitivities.  
CST‑MS applies layer‑specific weights:

$$
w_{\text{drift}}(L),\ 
w_{\text{osc}}(L),\ 
w_{\text{amb}}(L),\ 
w_{\text{coll}}(L),\ 
w_{\text{cont}}(L)
$$

Weights are deterministic and monotonic.

Weighted metrics:

$$
\tilde{M}^f(L, t) = w_f(L) \cdot \hat{M}^f(L, t)
$$

Weights allow CST‑MS to reflect:

- referent sensitivity  
- temporal sensitivity  
- discourse sensitivity  
- lineage sensitivity  
- register sensitivity  

---

# **5. Stability Synthesis**

CST‑MS synthesizes normalized, weighted metrics into a unified stability score.

Let:

- $\tilde{D}(L, t)$ = weighted drift  
- $\tilde{O}(L, t)$ = weighted oscillation  
- $\tilde{A}(L, t)$ = weighted ambiguity  
- $\tilde{C}(L, t)$ = weighted collapse  
- $\tilde{K}(L, t)$ = weighted continuity  

The stability score is:

$$
S(L, t) = \alpha_K(L)\tilde{K}(L, t)
           - \alpha_D(L)\tilde{D}(L, t)
           - \alpha_O(L)\tilde{O}(L, t)
           - \alpha_A(L)\tilde{A}(L, t)
           - \alpha_C(L)\tilde{C}(L, t)
$$

where $\alpha_f(L)$ are layer‑specific synthesis weights.

Stability is clipped to $[0, 1]$:

$$
S(L, t) = \min\big(1, \max(0, S(L, t))\big)
$$

---

# **6. Instability Synthesis**

Instability is the complement of stability:

$$
U(L, t) = 1 - S(L, t)
$$

Instability is used for:

- collapse risk  
- freeze risk  
- thaw readiness  
- continuity restoration  

---

# **7. Collapse Risk**

Collapse risk is synthesized from instability and collapse metrics:


$$  
R_{\text{coll}}(L, t) = \beta_U(L) U(L, t) + \beta_C(L) \tilde{C}(L, t)
$$  
  
Clipped to $[0, 1]$.

Collapse risk determines:

- collapse signals  
- freeze triggers  
- continuity restoration requirements  

---

# **8. Freeze Risk**

Freeze risk is synthesized from collapse risk and ambiguity:

$$
R_{\text{freeze}}(L, t) = \gamma_{\text{coll}}(L) R_{\text{coll}}(L, t) + \gamma_{\text{amb}}(L) \tilde{A}(L, t)
$$

Freeze risk determines whether CST‑Core’s freeze condition should be activated.

---

# **9. Thaw Readiness**

Thaw readiness is synthesized from stability and continuity:

$$
R_{\text{thaw}}(L, t) = \delta_S(L) S(L, t) + \delta_K(L) \tilde{K}(L, t)
$$

Thaw readiness determines whether CST‑Core’s thaw condition should be activated.

---

# **10. Ambiguity Summary**

Ambiguity summary is:

$$
A_{\text{sum}}(L, t) = \eta_A(L) \tilde{A}(L, t)
$$

Used by:

- COB identity evolution  
- CIL ambiguity aggregation  
- CEx correction expansion  

---

# **11. Drift Summary**

$$
D_{\text{sum}}(L, t) = \eta_D(L) \tilde{D}(L, t)
$$

Used by:

- COB identity evolution  
- CIL ordering aggregation  

---

# **12. Oscillation Summary**

$$
O_{\text{sum}}(L, t) = \eta_O(L) \tilde{O}(L, t)
$$

Used by:

- COB identity evolution  
- CIL ordering aggregation  

---

# **13. Determinism and Replay**

CST‑MS is fully deterministic:

- pure functional synthesis  
- no randomness  
- no external state  
- no wall‑clock time  
- monotonic thresholds  
- replay‑safe behavior  

Replay reconstructs:

- normalized metrics  
- weighted metrics  
- synthesized stability  
- collapse/freeze/thaw signals  
- ambiguity/drift/oscillation summaries  

Replay must produce identical outputs.

---

# **14. Summary**

CST‑MS transforms raw CST‑Core metrics into deterministic stability signals:

- stability  
- instability  
- collapse risk  
- freeze risk  
- thaw readiness  
- ambiguity summary  
- drift summary  
- oscillation summary  

These synthesized signals are consumed by CST‑Mux, COB, and CIL.

CST‑MS is the second module in the CST suite:

1. CST‑Core — raw metrics  
2. **CST‑MS — metric synthesis**  
3. CST‑Mux — signal multiplexing  
4. CST‑CIL‑Stability — stability integration into CIL  

---

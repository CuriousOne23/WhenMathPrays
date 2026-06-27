# **ts_wndw_indpndc_valdtn.md**  
### *Windowing and Independence Validation for TS*  
**White Paper — System Simulation / Requirements**

---

## **1. Motivation**

TS enforces independence **not** on the raw field graph $G$ (which is inherently interconnected), but on the **windowed embedding**:

$$
W(\phi(G(t)), t)
$$

This windowed embedding is what feeds into the TS manifold and dynamical law.  
Therefore:

- All **windowing**,  
- All **pdf shaping**,  
- All **independence enforcement**,  

must occur **before TS runtime**.

TS itself must remain a **primitive, deterministic engine** performing only:

- mapping  
- addition/subtraction  
- fixed‑form $\Delta_t$ updates  
- $\Gamma$ corrections  
- invariant enforcement  

This paper formalizes the **pre‑TS windowing pipeline**, defines **good vs bad windows**, and specifies the **validation metrics** required before higher‑D simulations.

---

## **2. Pre‑TS Windowing Pipeline**

All heavy computation occurs **before** TS runs.

### **Pipeline Steps**

1. **Build $G$**  
   Structured field graph (roles, modes, basins, governance, etc.).

2. **Compute $\phi(G)$**  
   Block‑structured numerical embedding.

3. **Compute time‑indexed $\phi(G(t))$**  
   Activation pattern over the input stream.

4. **Apply windowing**  
   $$
   x_t = W(\phi(G(t)), t)
   $$
   with overlap and tapering.

5. **Validate independence**  
   Using metrics (IS, LI, BD, GRL, CIP).

6. **Export clean activation tracks**  
   TS receives only $x_t$ — already windowed, independent, stable.

### **TS Runtime Does NOT:**

- compute windows  
- multiply embeddings by window weights  
- interpolate  
- enforce independence  
- shape pdfs  

TS only consumes $x_t$ and applies the dynamical law.

---

## **3. Overlap & Tapering Requirements**

Windowing **cannot** use hard boundaries.

### **Required Properties**

- Windows **overlap**  
- Edges **taper smoothly**  
- Influence **tends to zero only** at true statement start/end  
- No discontinuities  
- No binary masks  
- No step functions  

### **Why**

Hard boundaries cause:

- discontinuities in $\phi(G(t))$  
- spikes in $\nabla \Phi$  
- curvature instability  
- excessive $\Gamma$ load  
- basin transition errors  
- manifold violations  

Overlapping, tapered windows preserve:

- continuity  
- differentiability  
- bounded drift  
- stable curvature  
- clean CTP composition  

---

## **4. Good vs Bad Windows for TS**

### **Good Windows (Recommended)**  
Smooth, differentiable, low‑leakage:

1. **Hann Window**  
   Smooth cosine taper, excellent stability.

2. **Gaussian Window**  
   Smooth everywhere, tunable via $\sigma$.

3. **Tukey Window** (α = 0.5–0.75)  
   Flat center + smooth cosine edges.

**Why good:**  
Stable gradients, minimal boundary drift, low $\Gamma$ load, clean CTP behavior.

---

### **Bad Windows (Avoid)**

- Rectangular  
- Step functions  
- Binary masks  
- Any discontinuous window  

**Why bad:**  
Cause discontinuities → gradient spikes → instability → manifold violations.

---

## **5. Proposed Metrics**

### **Independence Score (IS)**  
$$
IS = 1 - \text{NMI}(\text{window}_i, \text{window}_j)
$$  
Target: **close to 1**

### **Leakage Index (LI)**  
$$
LI = \| \text{Proj}_{B_j}(B_i) \|
$$  
Target: **near 0**

### **Boundary Drift (BD)**  
Max $\|\Delta H\%\|$ and curvature change within $K$ steps of window edges.  
Target: **within TS thresholds**

### **$\Gamma$ Repair Load (GRL)**  
Average $\|\Gamma(s_t)\|$ during independence violations.  
Target: **low and stable**

### **CTP Independence Preservation (CIP)**  
Compare IS before vs after CTP.  
Target: **minimal degradation**

---

## **6. Minimal Validation Experiment Design**

For each candidate window (Hann, Gaussian, Tukey):

1. Construct synthetic $\phi(G)$ with known independent blocks.  
2. Apply windowing with overlap (20–50%) and taper parameters.  
3. Measure IS, LI, BD, GRL, CIP.  
4. Vary:
   - window size  
   - overlap ratio  
   - taper strength  
5. Document:
   - safe configurations  
   - unsafe configurations  
   - $\Gamma$ load patterns  
   - drift behavior  

**Only validated windows may be used in higher‑D TS simulations.**

---

## **7. Per‑Field Windowing & Pre‑Computed Lookup Tables**

Windowing is applied **per field** (or per block of fields) in $\phi(G)$.

### **7.1 Per‑Field Windowing**

For each field $f_i$:

$$
\phi_i^{\text{wnd}}(t) = w_i(t) \cdot \phi_i(G(t))
$$

This ensures:

- independent activation tracks  
- smooth support  
- controlled pdf shaping  
- clean manifold embedding  

Block‑level windows (e.g., GBMn, IBMn) follow the same rule.

---

### **7.2 TS Must Not Compute Window Weights**

TS primitives must remain:

- deterministic  
- primitive  
- lightweight  
- replayable  

Therefore TS **must not**:

- multiply embeddings by window weights  
- compute window functions  
- interpolate window values  

All windowing is done **before** TS runs.

---

### **7.3 Pre‑Computed Lookup Tables**

The pre‑TS pipeline computes:

$$
x_{t,i} = \phi_i^{\text{wnd}}(t)
$$

These values are stored in an efficient lookup structure:

- per‑statement tensor of shape $(T, D)$  
- block index tables for fast access  
- optional sparse storage for inactive fields  

TS runtime receives only:

$$
x_t = W(\phi(G(t)), t)
$$

as a **fully windowed, ready‑to‑use vector**.

---

### **7.4 No Interpolation**

To preserve:

- smoothness  
- differentiability  
- curvature stability  
- deterministic replay  

**Interpolation is not used.**  
All window values are precomputed exactly.

---

## **8. Guidelines & Next Steps**

- Use Hann, Gaussian, or Tukey windows.  
- Avoid rectangular or discontinuous windows.  
- Validate independence before higher‑D simulations.  
- Use per‑field (or per‑block) windowing with pre‑computed lookup tables.  
- TS runtime must remain primitive.

**Next:**  
Run windowing validation experiments → select preferred windows → proceed to 16D+ multi‑track TS simulations.

---

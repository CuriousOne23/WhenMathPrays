# **ts_wndw_indpndc_valdtn.md**

### *Windowing and Independence Validation for TS*

**White Paper — System Simulation / Requirements**

---

## **1. Motivation**

TS enforces independence on the windowed embedding φ(G(t)), not on raw G. All windowing, pdf shaping, and independence enforcement must occur in a pre-TS pipeline. TS itself remains a primitive deterministic engine.

This paper formalizes the pre-TS windowing pipeline and validates it for higher-D simulations.

---

## **2. Pre-TS Windowing Pipeline**

1. Build G
2. Compute φ(G)
3. Compute time-indexed φ(G(t))
4. Apply windowing W(φ(G(t)), t) with overlap and tapering
5. Validate independence (metrics below)
6. Export clean activation tracks for TS

TS runtime only performs mapping, Δ_t updates, Γ corrections, and invariant enforcement.

---

## **3. Overlap & Tapering Requirements**

Windows **must** overlap and taper smoothly. Hard boundaries are prohibited.

Requirements:
- Adjacent windows overlap
- Influence decays gradually (taper)
- Influence tends to zero only at true statement start/end
- Preserve differentiability and curvature stability

---

## **4. Good vs Bad Windows for TS**

### **Good Windows (Recommended)**
These are differentiable, smooth, low-leakage, and manifold-friendly:

1. **Hann Window** — Excellent smoothness, low spectral leakage.
2. **Gaussian Window** — Smooth, controllable taper via σ.
3. **Tukey Window** (tapered cosine, α=0.5–0.75) — Good flat top + smooth edges.

**Why good**: Produce stable gradients, minimal boundary drift, low Γ load, clean CTP composition.

### **Bad Windows (Avoid)**
- Rectangular (hard cut)
- Step functions
- Binary masks
- Any discontinuous window

**Why bad**: Cause discontinuities → gradient spikes in ∇Φ → basin instability, excessive Γ corrections, drift violations, manifold incompatibility.

---

## **5. Proposed Metrics**

(Independence Score (IS), Leakage Index (LI), Boundary Drift (BD), Γ Repair Load (GRL), CTP Independence Preservation (CIP) — unchanged from previous draft.)

---

## **6. Minimal Validation Experiment Design**

For each candidate window (Hann, Gaussian, Tukey):
- Construct synthetic φ(G) with known independent blocks
- Apply windowing with defined overlap (e.g., 20–50%) and taper parameters
- Measure IS, LI, BD, GRL, CIP
- Vary: window size, overlap ratio, taper strength
- Document best configurations and unsafe ones

**Next**: Run experiments, select preferred windows, then proceed to 16D+ multi-track simulations.

---

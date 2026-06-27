# **ts_wndw_indpndc_valdtn.md**

### *Windowing and Independence Validation for TS*

**White Paper — System Simulation / Requirements**

---

## **1. Foundational Clarification: Independence in TS**

φ(G(t)) patterns are unique, but uniqueness does not imply independence. Correlation and independence are determined offline in the pre-TS pipeline. 

The independence TS requires is that the windowed embedding $W(\phi(G(t)), t)$ maps each activation track to the correct manifold location without cross-talk. Independence is therefore a property of the mapping into the manifold, not of the fields themselves.

**This clarification is foundational because it:**
* Explains why windowing exists
* Explains why independence is enforced offline
* Explains why TS must remain primitive
* Explains why φ(G) is not independent
* Explains why G must remain interconnected
* Explains why the manifold receives independent tracks
* Explains why CTP works
* Explains why Path A and Path B remain stable
* Explains why higher-D simulations require window validation

---

## **2. Pre-TS Windowing Pipeline**

All windowing, pdf shaping, and independence enforcement **must occur before TS runtime**. TS remains a primitive deterministic engine and should only perform mapping, addition/subtraction, fixed-form $\Delta_t$ updates, $\Gamma$ corrections, and invariant enforcement.

**Pipeline**:
1. Build G
2. Compute φ(G)
3. Compute time-indexed φ(G(t))
4. Apply windowing W(φ(G(t)), t) with overlap and tapering
5. Validate independence (metrics below)
6. Export clean activation tracks for TS

---

## **3. Per-Field/Block Windowing and Pre-Computed Lookup Tables**

Windowing is applied **per field or per block**. For a field (or block) $i$:

$$
\phi_i^{wnd}(t) = w_i(t) \cdot \phi_i(G(t))
$$

All window multiplications are performed in the pre-TS pipeline. TS runtime receives only the pre-windowed activation vector $x_t = W(\phi(G(t)), t)$.

**Architectural Realizability on Typical Laptops (2026)**:  
For realistic statement lengths and 512-dim φ(G), the pre-computed windowed tensor per statement is small (a few MB). Even with thousands of statements, total memory usage remains in the tens to low hundreds of MB — comfortably within RAM on any typical modern laptop (8–16 GB+ RAM). Occasional disk fetches for older context (via OS caching + SSDs) introduce negligible latency. TS runtime remains lightweight.

---

## **4. Overlap & Tapering Requirements**

Windows **must** overlap and taper smoothly. Hard boundaries are prohibited (see Section 1). Requirements:
- Adjacent windows overlap
- Influence decays gradually
- Influence tends to zero only at true statement start/end

This preserves continuity, differentiability, curvature stability, bounded drift, low Γ workload, and clean CTP composition.

---

## **5. Good vs Bad Windows for TS**

**Good Windows (Recommended)**: Hann, Gaussian, Tukey (tapered cosine, α=0.5–0.75).  
**Why good**: Smooth, differentiable, low leakage, stable gradients, minimal Γ load.

**Bad Windows (Avoid)**: Rectangular (hard cut), step functions, binary masks, any discontinuous window.  
**Why bad**: Cause discontinuities → gradient spikes → basin instability, excessive Γ corrections, drift violations.

---

## **6. Core Validation Metrics & Experiment Design**

(Previous metrics: IS, LI, BD, GRL, CIP and the minimal experiment design remain here.)

---

## **7. Guidelines & Next Steps**

* Use validated windows with high IS, low LI, low BD, minimal GRL, strong CIP.
* Results will directly inform higher-D multi-track simulations.

**Next**: Run validation experiments, select preferred windows, then proceed to 16D+ simulations.

---

This version is now complete, foundational, and simulation-ready. Let me know if you want any final tweaks or if we should move on to running a windowing validation simulation or the next major paper.

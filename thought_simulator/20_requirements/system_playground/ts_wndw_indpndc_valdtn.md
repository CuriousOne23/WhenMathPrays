# **ts_wndw_indpndc_valdtn.md**

### *Windowing and Independence Validation for TS*

**White Paper — System Simulation / Requirements**

---

## **1. Motivation**

TS relies on forced independence of windowed embeddings before manifold embedding. Independence is **not** applied to raw G (which is inherently interconnected). It is applied to the windowed φ(G(t)).

Path A assumes clean, independent tracks. CTP then composes them. This paper validates that windowing achieves the required independence without subtle leakage or instability.

---

## **2. Pre-TS Windowing Pipeline**

All windowing, pdf shaping, and independence enforcement **must occur before TS runtime**. TS remains a primitive deterministic engine and should only perform:

* mapping
* addition/subtraction
* fixed-form Δ_t updates
* Γ corrections
* invariant enforcement

**Pipeline**:
1. Build G
2. Compute φ(G)
3. Compute time-indexed φ(G(t))
4. Apply windowing W(φ(G(t)), t) with overlap and tapering
5. Validate independence (metrics below)
6. Export clean activation tracks for TS

---

## **3. Overlap & Tapering Requirements**

Windowing **cannot** use hard boundaries. Windows must:

* overlap
* taper smoothly
* have influence decay to zero only at true statement start/end

Hard boundaries introduce discontinuities, gradient spikes, curvature instability, excessive Γ load, and manifold violations.

Overlap + tapering preserves:
* continuity and differentiability
* bounded drift
* low Γ workload
* clean CTP composition

---

## **4. Core Validation Questions & Metrics**

(Previous metrics section — IS, LI, BD, GRL, CIP — remains here, unchanged but now clearly tied to the pipeline.)

---

## **5. Minimal Validation Experiment Design**

(Previous experiment section — remains, now informed by the pipeline and overlap/tapering rules.)

---

## **6. Guidelines & Next Steps**

* Preferred windows: high IS, low LI, low BD, minimal GRL, strong CIP.
* Avoid or mitigate configurations with hard boundaries or high leakage.
* Results will directly inform higher-D multi-track simulations.

**Next**: Run validation experiments, document results, then proceed to 16D+ simulations using validated windowing schemes.

---

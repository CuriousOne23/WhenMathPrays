# **cst-ms_requirements.md**  
**CST‑MS Testbench Requirements**

---

## **0. Document Purpose (Informative)**  
This document defines the testbench requirements for **CST‑MS**, the Metric Synthesis Module in the Context Stability Tracking pipeline. The purpose of this testbench is to verify that CST‑MS correctly normalizes raw CST‑Core metrics, applies deterministic layer‑specific weights, synthesizes stability and instability values, computes collapse/freeze/thaw risks, produces ambiguity/drift/oscillation summaries, and maintains full determinism and replay‑safe behavior.

The testbench evaluates:

- basic synthesis functionality  
- normalization correctness  
- weighting correctness  
- stability and instability synthesis  
- collapse/freeze/thaw risk computation  
- summary signal correctness  
- determinism and replay consistency  
- operational functions required for TS integrity  

---

# **1. Input Acceptance Tests**

## **1.1 Purpose (Informative)**  
CST‑MS must accept all raw CST‑Core metrics and layer‑specific thresholds. The testbench verifies correct ingestion and deterministic handling of inputs.

## **1.2 Requirements (Normative)**  
**HLR‑CST‑MS‑001**  
The testbench SHALL verify that CST‑MS accepts raw drift, oscillation, ambiguity, collapse, continuity, freeze, thaw, register stability, and field‑importance stability metrics.

**HLR‑CST‑MS‑002**  
The testbench SHALL verify that CST‑MS accepts layer‑specific thresholds for all metrics.

**HLR‑CST‑MS‑003**  
The testbench SHALL verify that CST‑MS accepts metric histories for all raw CST‑Core metrics.

**HLR‑CST‑MS‑004**  
The testbench SHALL verify that CST‑MS accepts freeze, thaw, and continuity restoration signals from CST‑Core.

---

# **2. Normalization Tests**

## **2.1 Purpose (Informative)**  
Normalization ensures all raw metrics are mapped to \([0, 1]\) using deterministic maxima. The testbench verifies correct normalization behavior.

## **2.2 Requirements (Normative)**  
**HLR‑CST‑MS‑005**  
The testbench SHALL verify that each raw metric is normalized to the range \([0, 1]\).

**HLR‑CST‑MS‑006**  
The testbench SHALL verify that normalization uses deterministic layer‑specific maxima.

**HLR‑CST‑MS‑007**  
The testbench SHALL verify that normalization is replay‑safe and free of randomness.

---

# **3. Weighting Tests**

## **3.1 Purpose (Informative)**  
CST‑MS applies deterministic layer‑specific weights to normalized metrics. The testbench ensures weighting is correct and stable.

## **3.2 Requirements (Normative)**  
**HLR‑CST‑MS‑008**  
The testbench SHALL verify that deterministic layer‑specific weights are applied to normalized metrics.

**HLR‑CST‑MS‑009**  
The testbench SHALL verify that all weights are monotonic and replay‑safe.

**HLR‑CST‑MS‑010**  
The testbench SHALL verify that weighted metrics are computed as pure functions of normalized metrics and layer‑specific weights.

---

# **4. Stability Synthesis Tests**

## **4.1 Purpose (Informative)**  
CST‑MS synthesizes normalized, weighted metrics into a unified stability score. The testbench ensures stability synthesis is correct and deterministic.

## **4.2 Requirements (Normative)**  
**HLR‑CST‑MS‑011**  
The testbench SHALL verify that stability is computed as a deterministic function of weighted drift, oscillation, ambiguity, collapse, and continuity.

**HLR‑CST‑MS‑012**  
The testbench SHALL verify that deterministic synthesis weights are applied for each identity layer.

**HLR‑CST‑MS‑013**  
The testbench SHALL verify that stability values are clipped to the range \([0, 1]\).

---

# **5. Instability Synthesis Tests**

## **5.1 Purpose (Informative)**  
Instability is the complement of stability. The testbench ensures instability is computed correctly and clipped.

## **5.2 Requirements (Normative)**  
**HLR‑CST‑MS‑014**  
The testbench SHALL verify that instability is computed as the complement of stability.

**HLR‑CST‑MS‑015**  
The testbench SHALL verify that instability is clipped to the range \([0, 1]\).

---

# **6. Collapse Risk Tests**

## **6.1 Purpose (Informative)**  
Collapse risk is synthesized from instability and weighted collapse metrics. The testbench ensures collapse risk is computed correctly.

## **6.2 Requirements (Normative)**  
**HLR‑CST‑MS‑016**  
The testbench SHALL verify that collapse risk is computed as a deterministic function of instability and weighted collapse metrics.

**HLR‑CST‑MS‑017**  
The testbench SHALL verify that collapse risk is clipped to \([0, 1]\).

---

# **7. Freeze Risk Tests**

## **7.1 Purpose (Informative)**  
Freeze risk is synthesized from collapse risk and weighted ambiguity. The testbench ensures freeze risk is computed correctly.

## **7.2 Requirements (Normative)**  
**HLR‑CST‑MS‑018**  
The testbench SHALL verify that freeze risk is computed as a deterministic function of collapse risk and weighted ambiguity.

**HLR‑CST‑MS‑019**  
The testbench SHALL verify that freeze risk is clipped to \([0, 1]\).

---

# **8. Thaw Readiness Tests**

## **8.1 Purpose (Informative)**  
Thaw readiness is synthesized from stability and weighted continuity. The testbench ensures thaw readiness is computed correctly.

## **8.2 Requirements (Normative)**  
**HLR‑CST‑MS‑020**  
The testbench SHALL verify that thaw readiness is computed as a deterministic function of stability and weighted continuity.

**HLR‑CST‑MS‑021**  
The testbench SHALL verify that thaw readiness is clipped to \([0, 1]\).

---

# **9. Ambiguity, Drift, and Oscillation Summary Tests**

## **9.1 Purpose (Informative)**  
CST‑MS produces deterministic summaries for ambiguity, drift, and oscillation. The testbench ensures these summaries are computed correctly.

## **9.2 Requirements (Normative)**  
**HLR‑CST‑MS‑022**  
The testbench SHALL verify that ambiguity summaries are computed as deterministic functions of weighted ambiguity.

**HLR‑CST‑MS‑023**  
The testbench SHALL verify that drift summaries are computed as deterministic functions of weighted drift.

**HLR‑CST‑MS‑024**  
The testbench SHALL verify that oscillation summaries are computed as deterministic functions of weighted oscillation.

---

# **10. Determinism and Replay Tests**

## **10.1 Purpose (Informative)**  
CST‑MS must behave identically under replay. The testbench ensures full determinism.

## **10.2 Requirements (Normative)**  
**HLR‑CST‑MS‑025**  
The testbench SHALL verify that all outputs are computed as pure functions of normalized metrics, weighted metrics, synthesis weights, and raw CST‑Core inputs.

**HLR‑CST‑MS‑026**  
The testbench SHALL verify that threshold updates are deterministic and monotonic.

**HLR‑CST‑MS‑027**  
The testbench SHALL verify that replay produces identical synthesized outputs for identical inputs.

**HLR‑CST‑MS‑028**  
The testbench SHALL verify that all synthesized outputs are emitted in a deterministic, fixed order.

---

# **11. Merge/Split Stability Window Tests**

## **11.1 Purpose (Informative)**  
CST‑MS must treat merge and split events as structural transitions that do not, by themselves, produce instability signals. A merge or split event should not trigger drift, oscillation, ambiguity, collapse, freeze, thaw, or any instability‑related synthesis unless a genuine instability occurs within the 10‑turn CST‑MS state window. The testbench verifies that merge/split events are stability‑neutral and that real instability occurring after a merge or split is still detected correctly.

---

## **11.2 Requirements (Normative)**  

**HLR‑CST‑MS‑029**  
The testbench SHALL verify that a merge event does not produce any instability signal when no genuine instability occurs within the 10‑turn CST‑MS state window.

**HLR‑CST‑MS‑030**  
The testbench SHALL verify that a split event does not produce any instability signal when no genuine instability occurs within the 10‑turn CST‑MS state window.

**HLR‑CST‑MS‑031**  
The testbench SHALL verify that merge and split events do not alter normalized metrics, weighted metrics, or synthesized stability values unless a genuine instability occurs.

**HLR‑CST‑MS‑032**  
The testbench SHALL verify that merge and split events do not cause drift, oscillation, ambiguity, collapse, freeze, thaw, or continuity‑related signals to be emitted unless a genuine instability occurs.

**HLR‑CST‑MS‑033**  
The testbench SHALL verify that if a genuine instability occurs after a merge event but within the 10‑turn CST‑MS state window, CST‑MS emits the correct instability signal.

**HLR‑CST‑MS‑034**  
The testbench SHALL verify that if a genuine instability occurs after a split event but within the 10‑turn CST‑MS state window, CST‑MS emits the correct instability signal.

**HLR‑CST‑MS‑035**  
The testbench SHALL verify that merge/split events do not suppress or delay instability signals when genuine instability occurs within the 10‑turn window.

**HLR‑CST‑MS‑036**  
The testbench SHALL verify that merge/split events do not modify layer‑specific thresholds used for drift, oscillation, ambiguity, collapse, freeze, thaw, or continuity synthesis.

**HLR‑CST‑MS‑037**  
The testbench SHALL verify that replay of merge/split events produces identical stability‑neutral behavior and identical instability detection for identical input sequences.

## **11.3 Merge/Split Detection Requirements (Normative)**  
*(These continue numbering from HLR‑CST‑MS‑037)*

**HLR‑CST‑MS‑038**  
The testbench SHALL verify that CST‑MS detects a valid merge event when two identity‑layer structures combine into a single unified structure as defined by CST‑Core.

**HLR‑CST‑MS‑039**  
The testbench SHALL verify that CST‑MS detects a valid split event when one identity‑layer structure divides into two distinct structures as defined by CST‑Core.

**HLR‑CST‑MS‑040**  
The testbench SHALL verify that merge and split detection is deterministic and replay‑safe for identical input sequences.

**HLR‑CST‑MS‑041**  
The testbench SHALL verify that merge/split detection does not emit any instability signal by itself when no genuine instability occurs within the 10‑turn CST‑MS state window.

**HLR‑CST‑MS‑042**  
The testbench SHALL verify that merge/split detection correctly updates CST‑MS’s internal state window without altering normalized metrics, weighted metrics, or synthesized stability values.

**HLR‑CST‑MS‑043**  
The testbench SHALL verify that if a genuine instability occurs after a detected merge event but within the 10‑turn CST‑MS state window, CST‑MS emits the correct instability signal.

**HLR‑CST‑MS‑044**  
The testbench SHALL verify that if a genuine instability occurs after a detected split event but within the 10‑turn CST‑MS state window, CST‑MS emits the correct instability signal.

**HLR‑CST‑MS‑045**  
The testbench SHALL verify that merge/split detection does not suppress, delay, or modify instability signals when genuine instability occurs within the 10‑turn window.

### **12. Conversation Boundary Detection Tests**  
with requirements:

- **HLR‑CST‑MS‑046** — detect continuity break  
- **HLR‑CST‑MS‑047** — detect multi‑turn instability boundary  
- **HLR‑CST‑MS‑048** — detect ambiguity drift boundary  
- **HLR‑CST‑MS‑049** — emit “new conversation required” signal  
- **HLR‑CST‑MS‑050** — deterministic and replay‑safe boundary detection  


---

# **End of Document**

---

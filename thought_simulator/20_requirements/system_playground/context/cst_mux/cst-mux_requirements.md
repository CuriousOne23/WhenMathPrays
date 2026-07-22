# **cst-mux_requirements.md**  
**CST‑Mux Testbench Requirements**

---

## **0. Document Purpose (Informative)**  
This document defines the testbench requirements for **CST‑Mux**, the Stability Signal Multiplexing Module in the Context Stability Tracking pipeline. The purpose of this testbench is to verify that CST‑Mux correctly aligns, indexes, and multiplexes synthesized CST‑MS signals into the Unified Stability Packet (USP), maintains deterministic ordering, handles activation/freeze/thaw/continuity flags correctly, and behaves deterministically under replay.

The testbench evaluates:

- basic multiplexing functionality  
- layer indexing correctness  
- signal alignment correctness  
- flag computation correctness  
- merge/split neutrality  
- replay determinism  
- operational functions required for TS integrity  

---

# **1. Input Acceptance Tests**

## **1.1 Purpose (Informative)**  
CST‑Mux must accept all synthesized CST‑MS signals and layer‑state flags. The testbench verifies correct ingestion and deterministic handling of inputs.

## **1.2 Requirements (Normative)**  
**HLR‑CST‑MUX‑001**  
The testbench SHALL verify that CST‑Mux accepts stability, instability, collapse risk, freeze risk, thaw readiness, ambiguity summary, drift summary, and oscillation summary for each identity layer.

**HLR‑CST‑MUX‑002**  
The testbench SHALL verify that CST‑Mux accepts deterministic layer ordering.

**HLR‑CST‑MUX‑003**  
The testbench SHALL verify that CST‑Mux accepts activation, freeze, thaw, and continuity flags for each identity layer.

**HLR‑CST‑MUX‑034 — New Context Creation Signal Acceptance**
The testbench SHALL verify that CST‑Mux accepts the CST‑MS control signal new_context_required and SHALL propagate this flag into the Unified Stability Packet (USP) without modification.

---

# **2. Layer Indexing Tests**

## **2.1 Purpose (Informative)**  
CST‑Mux assigns deterministic indices to identity layers. The testbench ensures indexing is stable and replay‑safe.

## **2.2 Requirements (Normative)**  
**HLR‑CST‑MUX‑004**  
The testbench SHALL verify that CST‑Mux assigns deterministic indices to all identity layers.

**HLR‑CST‑MUX‑005**  
The testbench SHALL verify that layer indexing is stable across replay.

---

# **3. Signal Alignment Tests**

## **3.1 Purpose (Informative)**  
CST‑Mux aligns all synthesized signals by identity layer. The testbench ensures alignment is correct and deterministic.

## **3.2 Requirements (Normative)**  
**HLR‑CST‑MUX‑006**  
The testbench SHALL verify that CST‑Mux aligns all synthesized signals by identity layer.

**HLR‑CST‑MUX‑007**  
The testbench SHALL verify that aligned signals maintain deterministic ordering.

**HLR‑CST‑MUX‑008**  
The testbench SHALL verify that aligned signals are replay‑safe.

---

# **4. Activation Flag Tests**

## **4.1 Purpose (Informative)**  
Activation flags determine whether a layer participates in identity evolution. The testbench ensures activation flags are computed correctly.

## **4.2 Requirements (Normative)**  
**HLR‑CST‑MUX‑009**  
The testbench SHALL verify that activation flags are computed using deterministic activation thresholds.

**HLR‑CST‑MUX‑010**  
The testbench SHALL verify that activation flags are included correctly in USP.

---

# **5. Freeze and Thaw Flag Tests**

## **5.1 Purpose (Informative)**  
Freeze and thaw flags determine whether a layer is allowed to evolve or integrate. The testbench ensures freeze/thaw flags are computed correctly.

## **5.2 Requirements (Normative)**  
**HLR‑CST‑MUX‑011**  
The testbench SHALL verify that freeze flags are computed using deterministic freeze thresholds.

**HLR‑CST‑MUX‑012**  
The testbench SHALL verify that thaw flags are computed using deterministic thaw thresholds.

**HLR‑CST‑MUX‑013**  
The testbench SHALL verify that freeze and thaw flags are included correctly in USP.

---

# **6. Continuity Flag Tests**

## **6.1 Purpose (Informative)**  
Continuity flags indicate whether a layer is stable enough for integration. The testbench ensures continuity flags are computed correctly.

## **6.2 Requirements (Normative)**  
**HLR‑CST‑MUX‑014**  
The testbench SHALL verify that continuity flags are computed using deterministic continuity thresholds.

**HLR‑CST‑MUX‑015**  
The testbench SHALL verify that continuity flags are included correctly in USP.

---

# **7. USP Construction Tests**

## **7.1 Purpose (Informative)**  
USP is the final multiplexed packet consumed by COB and CIL. The testbench ensures USP is constructed deterministically and completely.

## **7.2 Requirements (Normative)**  
**HLR‑CST‑MUX‑016**  
The testbench SHALL verify that USP is constructed as a deterministic, layer‑indexed packet.

**HLR‑CST‑MUX‑017**  
The testbench SHALL verify that USP includes all aligned signals and flags.

**HLR‑CST‑MUX‑035 — USP Inclusion of New Context Creation Signal**
The testbench SHALL verify that the USP includes the new_context_required flag exactly as emitted by CST‑MS, and SHALL ensure that this flag is indexed and ordered deterministically with other USP fields

**HLR‑CST‑MUX‑018**  
The testbench SHALL verify that USP is replay‑safe.

---

# **8. Merge/Split Neutrality Tests**

## **8.1 Purpose (Informative)**  
Merge and split events are structural transitions that should not produce instability signals or alter USP unless genuine instability occurs. The testbench ensures merge/split neutrality.

## **8.2 Requirements (Normative)**  
**HLR‑CST‑MUX‑019**  
The testbench SHALL verify that merge events do not produce instability signals when no genuine instability occurs.

**HLR‑CST‑MUX‑020**  
The testbench SHALL verify that split events do not produce instability signals when no genuine instability occurs.

**HLR‑CST‑MUX‑021**  
The testbench SHALL verify that merge/split events do not alter aligned signals or flags unless genuine instability occurs.

**HLR‑CST‑MUX‑022**  
The testbench SHALL verify that merge/split events do not modify USP structure or ordering.

---

# **9. Merge/Split Detection Tests**

## **9.1 Purpose (Informative)**  
CST‑Mux must detect merge/split events correctly and update USP state without producing instability unless genuine instability occurs. The testbench ensures correct detection behavior.

## **9.2 Requirements (Normative)**  
**HLR‑CST‑MUX‑023**  
The testbench SHALL verify that CST‑Mux detects valid merge events when two identity‑layer structures unify.

**HLR‑CST‑MUX‑024**  
The testbench SHALL verify that CST‑Mux detects valid split events when one identity‑layer structure divides.

**HLR‑CST‑MUX‑025**  
The testbench SHALL verify that merge/split detection is deterministic and replay‑safe.

**HLR‑CST‑MUX‑026**  
The testbench SHALL verify that merge/split detection does not emit instability signals unless genuine instability occurs.

**HLR‑CST‑MUX‑027**  
The testbench SHALL verify that merge/split detection correctly updates USP state without altering stability‑neutral behavior.

**HLR‑CST‑MUX‑028**  
The testbench SHALL verify that if genuine instability occurs after a merge event, CST‑Mux emits the correct instability‑related flags.

**HLR‑CST‑MUX‑029**  
The testbench SHALL verify that if genuine instability occurs after a split event, CST‑Mux emits the correct instability‑related flags.

---

# **10. Determinism and Replay Tests**

## **10.1 Purpose (Informative)**  
CST‑Mux must behave identically under replay. The testbench ensures full determinism.

## **10.2 Requirements (Normative)**  
**HLR‑CST‑MUX‑030**  
The testbench SHALL verify that all outputs are computed as pure functions of CST‑MS inputs and layer states.

**HLR‑CST‑MUX‑031**  
The testbench SHALL verify that threshold comparisons are deterministic and monotonic.

**HLR‑CST‑MUX‑032**  
The testbench SHALL verify that replay produces identical USP outputs for identical inputs.

**HLR‑CST‑MUX‑036 — Replay Determinism for New Context Creation Signal**
The testbench SHALL verify that replaying identical CST‑MS inputs produces identical new_context_required values in the USP.

**HLR‑CST‑MUX‑033**  
The testbench SHALL verify that all USP outputs are emitted in a deterministic, fixed order.

---

# **End of Document**

---

# **cst-core_requirements.md**  
**CST‑Core Testbench Requirements**

---

## **0. Document Purpose (Informative)**  
This document defines the testbench requirements for **CST‑Core**, the foundational module responsible for structural stability tracking in the Thought Simulator. The purpose of this testbench is to verify that CST‑Core behaves deterministically, computes stability metrics correctly, handles dynamic conditions such as drift, oscillation, ambiguity, collapse, freeze, thaw, and continuity restoration, and maintains replay‑safe behavior across all identity layers.

The testbench evaluates:

- basic functionality  
- dynamic stability behavior  
- threshold behavior  
- freeze/thaw correctness  
- continuity restoration  
- determinism and replay consistency  
- operational functions required for TS integrity  

---

# **1. Snapshot Extraction Tests**

## **1.1 Purpose (Informative)**  
Snapshot extraction is the foundation of CST‑Core. The testbench verifies that snapshots are produced deterministically and contain all required structural fields.

## **1.2 Requirements (Normative)**  
**HLR‑CST‑CORE‑001**  
The testbench SHALL verify that CST‑Core extracts a structural snapshot for every identity layer at each turn.

**HLR‑CST‑CORE‑002**  
The testbench SHALL verify that snapshot extraction is deterministic under replay.

**HLR‑CST‑CORE‑003**  
The testbench SHALL verify that snapshots contain all required structural fields: referent structure, temporal anchors, discourse anchors, lineage continuity, register state, and field‑importance weights.

---

# **2. Counting and History Tests**

## **2.1 Purpose (Informative)**  
CST‑Core maintains counts, frequencies, and histories over a 10‑turn window. The testbench ensures these values are computed correctly and consistently.

## **2.2 Requirements (Normative)**  
**HLR‑CST‑CORE‑004**  
The testbench SHALL verify that feature counts are computed over a fixed 10‑turn sliding window.

**HLR‑CST‑CORE‑005**  
The testbench SHALL verify that normalized feature frequencies are computed correctly.

**HLR‑CST‑CORE‑006**  
The testbench SHALL verify that ordered feature histories are maintained for all tracked features.

---

# **3. Drift Tests**

## **3.1 Purpose (Informative)**  
Drift measures structural change across turns. The testbench ensures drift is computed deterministically and triggers instability when appropriate.

## **3.2 Requirements (Normative)**  
**HLR‑CST‑CORE‑007**  
The testbench SHALL verify that per‑turn drift is computed using deterministic structural distance functions.

**HLR‑CST‑CORE‑008**  
The testbench SHALL verify that integrated drift over 10 turns is computed correctly.

**HLR‑CST‑CORE‑009**  
The testbench SHALL verify that drift signals are emitted when integrated drift exceeds the layer‑specific threshold.

---

# **4. Oscillation Tests**

## **4.1 Purpose (Informative)**  
Oscillation measures how often structural features flip state. The testbench ensures oscillation detection is correct and stable.

## **4.2 Requirements (Normative)**  
**HLR‑CST‑CORE‑010**  
The testbench SHALL verify that oscillation is computed as the count of state flips between consecutive turns.

**HLR‑CST‑CORE‑011**  
The testbench SHALL verify that oscillation signals are emitted when oscillation exceeds the layer‑specific threshold.

---

# **5. Ambiguity Tests**

## **5.1 Purpose (Informative)**  
Ambiguity measures uncertainty in structural interpretation. The testbench ensures ambiguity is computed correctly and contributes to instability.

## **5.2 Requirements (Normative)**  
**HLR‑CST‑CORE‑012**  
The testbench SHALL verify that per‑turn ambiguity is computed using deterministic ambiguity functions.

**HLR‑CST‑CORE‑013**  
The testbench SHALL verify that integrated ambiguity over 10 turns is computed correctly.

**HLR‑CST‑CORE‑014**  
The testbench SHALL verify that ambiguity signals are emitted when integrated ambiguity exceeds the layer‑specific threshold.

---

# **6. Collapse Tests**

## **6.1 Purpose (Informative)**  
Collapse indicates structural failure. The testbench ensures collapse detection is correct and deterministic.

## **6.2 Requirements (Normative)**  
**HLR‑CST‑CORE‑015**  
The testbench SHALL verify that stability scores are computed per turn for all structural domains.

**HLR‑CST‑CORE‑016**  
The testbench SHALL verify that integrated stability over 10 turns is computed correctly.

**HLR‑CST‑CORE‑017**  
The testbench SHALL verify that collapse is computed as the complement of integrated stability.

**HLR‑CST‑CORE‑018**  
The testbench SHALL verify that collapse signals are emitted when collapse exceeds the layer‑specific threshold.

---

# **7. Freeze Tests**

## **7.1 Purpose (Informative)**  
Freeze prevents further degradation when instability becomes unsafe. The testbench ensures freeze behavior is correct and deterministic.

## **7.2 Requirements (Normative)**  
**HLR‑CST‑CORE‑019**  
The testbench SHALL verify that combined instability is computed from drift, oscillation, ambiguity, and collapse.

**HLR‑CST‑CORE‑020**  
The testbench SHALL verify that freeze is triggered when combined instability exceeds the layer‑specific freeze threshold.

**HLR‑CST‑CORE‑021**  
The testbench SHALL verify that snapshot updates halt for frozen layers.

**HLR‑CST‑CORE‑022**  
The testbench SHALL verify that stability‑metric updates halt for frozen layers.

**HLR‑CST‑CORE‑023**  
The testbench SHALL verify that threshold adaptation halts for frozen layers.

---

# **8. Thaw Tests**

## **8.1 Purpose (Informative)**  
Thaw restores normal structural evolution once stability returns. The testbench ensures thaw behavior is correct and deterministic.

## **8.2 Requirements (Normative)**  
**HLR‑CST‑CORE‑024**  
The testbench SHALL verify that thaw is triggered when combined instability falls below the layer‑specific recovery threshold.

**HLR‑CST‑CORE‑025**  
The testbench SHALL verify that snapshot updates resume upon thaw.

**HLR‑CST‑CORE‑026**  
The testbench SHALL verify that stability‑metric updates resume upon thaw.

**HLR‑CST‑CORE‑027**  
The testbench SHALL verify that threshold adaptation resumes upon thaw.

---

# **9. Continuity Restoration Tests**

## **9.1 Purpose (Informative)**  
Continuity restoration repairs structural stability after freeze or collapse. The testbench ensures continuity restoration behaves correctly.

## **9.2 Requirements (Normative)**  
**HLR‑CST‑CORE‑028**  
The testbench SHALL verify that continuity scores are computed per turn for each identity layer.

**HLR‑CST‑CORE‑029**  
The testbench SHALL verify that integrated continuity over 10 turns is computed correctly.

**HLR‑CST‑CORE‑030**  
The testbench SHALL verify that continuity restoration is triggered when integrated continuity exceeds the layer‑specific recovery threshold.

**HLR‑CST‑CORE‑031**  
The testbench SHALL verify that queued structural corrections are applied deterministically during continuity restoration.

---

# **10. Determinism and Replay Tests**

## **10.1 Purpose (Informative)**  
CST‑Core must behave identically under replay. The testbench ensures full determinism.

## **10.2 Requirements (Normative)**  
**HLR‑CST‑CORE‑032**  
The testbench SHALL verify that all metrics are computed as pure functions of snapshots, OuBA cues, previous CST signals, and deterministic history.

**HLR‑CST‑CORE‑033**  
The testbench SHALL verify that threshold updates follow deterministic, monotonic rules.

**HLR‑CST‑CORE‑034**  
The testbench SHALL verify that replay produces identical metric values, thresholds, and signals.

**HLR‑CST‑CORE‑035**  
The testbench SHALL verify that stability signals are emitted in a deterministic, fixed order.

**HLR‑CST‑CORE‑036**  
The testbench SHALL verify that all logged values required for replay consistency are present and correct.

---

# **End of Document**

---

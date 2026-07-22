# **CST Requirements (Revised, Consolidated HLR Section)**  
*Conversation Stability Tracker — Context Subsystem*  
*System Playground Version*

---

## **1. Purpose**  
*(Informative — no SHALL statements)*

The Conversation Stability Tracker (CST) evaluates stability conditions across identity‑layer objects.  
It detects drift, oscillation, collapse, merge, split, freeze, thaw, and certainty/ambiguity changes.  
CST produces stability signals consumed by COB and indirectly by CIL.

CST is the first stage of the context subsystem:

$$
\text{CST} \rightarrow \text{COB} \rightarrow \text{CIL} \rightarrow \text{CEx}
$$

---

## **2. Scope**  
*(Informative — no SHALL statements)*

This document defines the **system_playground implementation** of CST.  
It describes stability signal generation, drift detection, oscillation detection, collapse conditions, merge/split rules, freeze/thaw behavior, and ambiguity/certainty adjustments.

Global architecture defined in **20.32.010** remains authoritative.

---

## **3. Inputs**  
*(Informative — no SHALL statements)*

### **3.1 Identity‑Layer Objects from COB**  
CST receives identity‑layer objects containing referent maps, anchors, lineage, ambiguity indicators, and ordering metrics.

### **3.2 Conversation Turn Identity Fragments**  
CST receives identity‑layer fragments extracted from the current turn before COB integration.

---

## **4. Outputs**  
*(Informative — no SHALL statements)*

### **4.1 Stability Signals**  
CST produces stability signals including:

- drift  
- oscillation  
- collapse  
- merge  
- split  
- freeze  
- thaw  
- certainty adjustments  
- ambiguity adjustments  
- lineage stability indicators  

These signals are consumed by COB and indirectly by CIL.

---

## **5. Testing (system_playground)**  
*(Informative — no SHALL statements)*

The system_playground version of CST is validated using a block‑level Python testbench (`cst_testbench.py`).  
Tests ensure CST produces deterministic stability signals, correctly interprets structural continuity markers from TP, and remains synchronized with COB across merge, split, drift, oscillation, collapse, and ambiguity conditions.

---

## **5.1 Drift, Oscillation, and Collapse Tests**  
*(Informative)*

### **Drift Tests**  
Evaluate CST’s ability to detect referent‑map and anchor divergence.

**Expected behavior:**  
- Drift reported only when divergence exceeds thresholds  
- Drift magnitude reflects divergence  
- No oscillation/collapse when divergence is monotonic  

### **Oscillation Tests**  
Evaluate CST’s ability to detect alternating incompatible states.

**Expected behavior:**  
- Oscillation frequency reflects alternation  
- No collapse when oscillation is reversible  
- Freeze/thaw exercised when oscillation exceeds limits  

### **Collapse Tests**  
Evaluate CST’s ability to detect structural failure.

**Expected behavior:**  
- Collapse reported when structural integrity is lost  
- Drift/oscillation may accompany collapse  
- Collapse signals deterministic  

---

## **5.2 Merge/Split Stability Tests**  
*(Informative)*

### **Merge Stability Tests**  
Ensure CST interprets MERGE markers as legitimate consolidation.

### **Split Stability Tests**  
Ensure CST interprets SPLIT markers as legitimate divergence.

### **Merge/Split Compensation Tests**  
Ensure CST remains synchronized with COB across structural transformations.

---

## **5.3 Freeze/Thaw, Certainty, and Ambiguity Tests**  
*(Informative)*

### **Freeze/Thaw Tests**  
Freeze issued when instability exceeds thresholds; thaw issued when stability restored.

### **Certainty/Ambiguity Adjustment Tests**  
Certainty increases when ambiguity decreases; ambiguity increases when drift/oscillation rises.

---

## **5.4 Deterministic Replay Tests**  
*(Informative)*

### **Single‑Turn Determinism**  
Identical inputs → identical signals.

### **Multi‑Turn Determinism**  
Merge/split sequences produce identical signal sequences across runs.

---

# **6. Consolidated High‑Level Requirements (HLRs)**  
*(All SHALL statements appear only here; new HLRs begin at 018)*

### **Core Stability Detection**

**HLR‑CST‑001**  
CST SHALL detect drift conditions in identity‑layer objects.

**HLR‑CST‑002**  
CST SHALL detect oscillation conditions in identity‑layer objects.

**HLR‑CST‑003**  
CST SHALL detect collapse conditions and produce collapse signals.

### **Structural Transformations**

**HLR‑CST‑004**  
CST SHALL detect merge conditions between identity‑layer objects.

**HLR‑CST‑005**  
CST SHALL detect split conditions within identity‑layer objects.

### **Stability Signaling**

**HLR‑CST‑006**  
CST SHALL issue freeze and thaw signals based on stability conditions.

**HLR‑CST‑007**  
CST SHALL adjust certainty indicators for identity‑layer objects.

**HLR‑CST‑008**  
CST SHALL adjust ambiguity indicators for identity‑layer objects.

**HLR‑CST‑009**  
CST SHALL evaluate lineage stability for identity‑layer objects.

### **Determinism**

**HLR‑CST‑010**  
CST SHALL produce deterministic stability signals under identical inputs.

---

### **Next‑Turn Context Compatibility (New HLRs begin here)**

**HLR‑CST‑011**  
CST SHALL treat next‑turn context fields as external structural metadata without generating, modifying, or interpreting them.

**HLR‑CST‑012**  
CST SHALL propagate stability signals deterministically alongside next‑turn context fields without corrupting or altering them.

**HLR‑CST‑013**  
CST SHALL NOT emit instability signals solely due to the presence, absence, or content of next‑turn context fields.

**HLR‑CST‑014**  
CST SHALL preserve structural continuity during merge/split events such that next‑turn context fields remain stable across turns.

**HLR‑CST‑015**  
CST SHALL preserve next‑turn context continuity across freeze/thaw cycles.

**HLR‑CST‑016**  
CST SHALL guarantee deterministic replay of stability signals such that identical inputs produce identical downstream next‑turn context behavior.

**HLR‑CST‑017**  
CST SHALL NOT define next‑turn context field names.

---

### **New HLRs Added for Global Alignment (Option C)**

**HLR‑CST‑018**  
CST SHALL synchronize its internal topology with COB’s identity‑layer structure across merge and split events.

**HLR‑CST‑019**  
CST SHALL interpret TP lineage markers deterministically when evaluating merge, split, drift, oscillation, and collapse.

**HLR‑CST‑020**  
CST SHALL maintain deterministic structural continuity across multi‑turn sequences involving merge, split, drift, oscillation, and collapse.

**HLR‑CST‑021**  
CST SHALL ensure freeze/thaw signals do not cause loss, mutation, or reordering of identity‑layer objects in downstream modules.

**HLR‑CST‑022**  
CST SHALL ensure certainty/ambiguity adjustments remain consistent with drift, oscillation, and collapse metrics across turns.

**HLR‑CST‑023**  
CST SHALL ensure merge/split compensation does not introduce spurious instability signals.

**HLR‑CST‑024**  
CST SHALL ensure lineage stability evaluation remains consistent across structural transformations.

---

## **7. Stability Metrics**  
*(Informative — no SHALL statements)*

CST evaluates stability using metrics such as:

- referent drift  
- anchor drift  
- lineage divergence  
- ambiguity density  
- oscillation frequency  

Example:

$$
\text{StabilityScore} = \text{Drift} + \text{Oscillation} + \text{AmbiguityDensity}
$$

---

## **8. Drift Rules**  
*(Informative — no SHALL statements)*

Drift is detected when referent or anchor positions diverge across turns.  
Drift magnitude influences certainty and ambiguity adjustments.

---

## **9. Oscillation Rules**  
*(Informative — no SHALL statements)*

Oscillation occurs when identity‑layer objects alternate between incompatible states across turns.  
Oscillation frequency influences freeze/thaw decisions.

---

## **10. Collapse Rules**  
*(Informative — no SHALL statements)*

Collapse occurs when identity‑layer objects lose structural integrity or become incompatible with referent maps.  
Collapse signals trigger COB merge or eviction behavior.

---

## **11. Merge/Split Rules**  
*(Informative — no SHALL statements)*

Merge conditions arise when identity‑layer objects converge in referent or anchor space.  
Split conditions arise when identity‑layer objects diverge into incompatible states.

---

## **12. Freeze/Thaw Behavior**  
*(Informative — no SHALL statements)*

Freeze signals prevent COB from modifying identity‑layer objects.  
Thaw signals restore normal update behavior.

---

## **13. Interface Contracts**  
*(Informative — no SHALL statements)*

### **CST → COB**  
CST provides stability signals directly to COB.

### **CST → CIL**  
CST influences CIL indirectly through COB and directly when required by global rules.

### **CST → CEx (Indirect)**  
CST influences CEx only through COB and CIL.

---

## **14. Determinism Notes**  
*(Informative — no SHALL statements)*

Deterministic signal generation ensures reproducible behavior in COB and CIL under identical identity‑layer inputs.

---

## **15. Error Handling**  
*(Informative — no SHALL statements)*

CST rejects malformed identity‑layer objects.  
CST rejects invalid referent or anchor structures.  
CST ensures internal consistency of stability signals.

---

## **16. Playground Notes**  
*(Informative — no SHALL statements)*

This document defines the system_playground version of CST.  
It mirrors global architecture while remaining scoped for simulation and testing.

---

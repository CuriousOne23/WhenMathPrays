# **CST Requirements**  
*Conversation Stability Tracker — Context Subsystem*  
*System Playground Version*

---

## **1. Purpose**

The **Conversation Stability Tracker (CST)** evaluates stability conditions across identity‑layer objects.  
It detects drift, oscillation, collapse, merge, split, freeze, thaw, and certainty/ambiguity changes.  
CST produces stability signals consumed by COB and indirectly by CIL.

CST is the first stage of the context subsystem:

$$
\text{CST} \rightarrow \text{COB} \rightarrow \text{CIL} \rightarrow \text{CEx}
$$

---

## **2. Scope**

This document defines the **system_playground implementation** of CST.  
It describes stability signal generation, drift detection, oscillation detection, collapse conditions, merge/split rules, freeze/thaw behavior, and ambiguity/certainty adjustments.

This document does **not** redefine the global CST architecture in **20.32.010**; global requirements remain authoritative.

---

## **3. Inputs**

### **3.1 Identity‑Layer Objects from COB**  
CST receives identity‑layer objects containing referent maps, anchors, lineage, ambiguity indicators, and ordering metrics.

### **3.2 Conversation Turn Identity Fragments**  
CST receives identity‑layer fragments extracted from the current turn before COB integration.

---

## **4. Outputs**

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

---

## **5. Testing (system_playground)**

The system_playground version of CST is validated using a block‑level Python testbench (`cst_testbench.py`).  
This testbench verifies that CST produces deterministic stability signals based on identity‑layer object inputs.

### **5.1 Tested Behaviors**

The following CST behaviors are explicitly tested:

- **Drift Detection**  
  CST identifies identity‑layer objects exhibiting referent or anchor divergence and reports affected objects and drift magnitude.

- **Oscillation Detection**  
  CST detects alternating incompatible states and reports affected objects, oscillation frequency, and amplitude.

- **Collapse Detection**  
  CST identifies identity‑layer objects that have structurally collapsed and reports severity.

- **Freeze / Thaw Detection**  
  CST reports objects marked as frozen or thawed based on stability conditions.

- **Certainty Adjustment**  
  CST increases or decreases certainty indicators based on ambiguity and referent stability.

- **Ambiguity Adjustment**  
  CST increases or decreases ambiguity indicators based on identity‑layer conditions.

- **Lineage Stability Detection**  
  CST identifies stable and unstable lineage conditions across identity‑layer objects.

### **5.2 Behaviors Not Tested in system_playground**

The following behaviors are **not** tested at this stage:

- **Merge Detection (full implementation)**  
- **Split Detection (full implementation)**  
- **Multi‑block interactions with COB or CIL**  
- **Full pipeline stability propagation**  
- **Deterministic replay across multiple turns**

These behaviors are reserved for **system_simulation**, where CST participates in multi‑block, multi‑stage flows.

### **5.3 Testbench Characteristics**

- Deterministic execution  
- No external dependencies  
- No multi‑block orchestration  
- Pure block‑level validation  
- Mirrors the structure of `cst_signals.yaml` and `cst_state.yaml`

The testbench ensures that CST behaves consistently with the system_playground requirements and produces stability signals suitable for COB integration.

---

## **6. High‑Level Requirements (HLRs)**  
*(All SHALL statements appear only here. Each HLR contains exactly one SHALL.)*

### **HLR‑CST‑001: Drift Detection**  
CST SHALL detect drift conditions in identity‑layer objects.

### **HLR‑CST‑002: Oscillation Detection**  
CST SHALL detect oscillation conditions in identity‑layer objects.

### **HLR‑CST‑003: Collapse Detection**  
CST SHALL detect collapse conditions and produce collapse signals.

### **HLR‑CST‑004: Merge Conditions**  
CST SHALL detect merge conditions between identity‑layer objects.

### **HLR‑CST‑005: Split Conditions**  
CST SHALL detect split conditions within identity‑layer objects.

### **HLR‑CST‑006: Freeze/Thaw Signaling**  
CST SHALL issue freeze and thaw signals based on stability conditions.

### **HLR‑CST‑007: Certainty Adjustment**  
CST SHALL adjust certainty indicators for identity‑layer objects.

### **HLR‑CST‑008: Ambiguity Adjustment**  
CST SHALL adjust ambiguity indicators for identity‑layer objects.

### **HLR‑CST‑009: Lineage Stability Evaluation**  
CST SHALL evaluate lineage stability for identity‑layer objects.

### **HLR‑CST‑010: Deterministic Signal Generation**  
CST SHALL produce deterministic stability signals under identical inputs.

---

## **7. Stability Metrics**  
*(Informative — no SHALL statements)*

CST evaluates stability using metrics such as:

- referent drift  
- anchor drift  
- lineage divergence  
- ambiguity density  
- oscillation frequency  

Example block equation:

$$
\text{StabilityScore} = \text{Drift} \ + \ \text{Oscillation} \ + \ \text{AmbiguityDensity}
$$

Curly braces example:

$$
\text{SignalSet} = \\{ \text{Drift},\ \text{Oscillation},\ \text{Collapse} \\}
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

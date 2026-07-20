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

### **5. Testing (system_playground)**  
The system_playground version of CST is validated using a block‑level Python testbench (`cst_testbench.py`).  
These tests ensure CST produces deterministic stability signals, correctly interprets structural continuity markers from TP, and remains synchronized with COB across merge, split, drift, oscillation, collapse, and ambiguity conditions.

---

## **5.1 Drift, Oscillation, and Collapse Tests**

### **Drift Tests**  
These tests evaluate CST’s ability to detect referent‑map and anchor divergence.

**Setup:**  
Identity‑layer objects are constructed with gradually diverging referent maps or anchor values across synthetic turns.

**Execution:**  
Objects and turn fragments are fed into CST. Drift signals are recorded.

**Expected Behavior:**  
- Drift is reported only when divergence exceeds configured thresholds.  
- Drift magnitude reflects the degree of divergence.  
- No oscillation or collapse signals appear when divergence is monotonic.

---

### **Oscillation Tests**  
These tests evaluate CST’s ability to detect alternating incompatible states.

**Setup:**  
Identity‑layer objects alternate between incompatible referent or anchor states across turns.

**Execution:**  
Alternating states are fed into CST. Oscillation signals are recorded.

**Expected Behavior:**  
- Oscillation frequency reflects the alternation pattern.  
- No collapse signals appear when oscillation remains reversible.  
- Freeze/thaw behavior is exercised when oscillation exceeds stability limits.

---

### **Collapse Tests**  
These tests evaluate CST’s ability to detect structural failure.

**Setup:**  
Identity‑layer objects are constructed with invalid referent maps, contradictory anchors, or lineage inconsistencies.

**Execution:**  
Objects are fed into CST. Collapse signals are recorded.

**Expected Behavior:**  
- Collapse is reported when structural integrity is lost.  
- Drift or oscillation may accompany collapse but do not suppress it.  
- Collapse signals are deterministic under identical inputs.

---

## **5.2 Merge/Split Stability Tests**

These tests ensure CST correctly interprets structural continuity markers from COB and TP, and does not misclassify legitimate structural transformations as instability.

### **Merge Stability Tests**

**Setup:**  
COB performs a deterministic MERGE of two identity‑layer objects.  
`TP.lineage_log[]` and `TP.cob_state_snapshot` are captured.

**Execution:**  
CST consumes the post‑merge snapshot and lineage markers.  
Stability signals are recorded.

**Expected Behavior:**  
- MERGE markers in `TP.lineage_log[]` are interpreted as legitimate consolidation.  
- CST does not emit false collapse or oscillation signals due to parent disappearance.  
- CST updates its internal topology to track the merged child layer.  
- CST remains synchronized with COB’s identity‑layer state.

---

### **Split Stability Tests**

**Setup:**  
COB performs a deterministic SPLIT of one identity‑layer object into two child layers.  
`TP.lineage_log[]` and `TP.cob_state_snapshot` are captured.

**Execution:**  
CST consumes the post‑split snapshot and lineage markers.  
Stability signals are recorded.

**Expected Behavior:**  
- SPLIT markers in `TP.lineage_log[]` are interpreted as legitimate divergence.  
- CST does not emit false oscillation or collapse signals due to child appearance.  
- CST updates its internal topology to track both child layers.  
- Lineage continuity is preserved across the split.

---

### **Merge/Split Compensation Tests**

**Setup:**  
Sequences of MERGE and SPLIT events are generated across multiple turns.  
Each turn produces updated TP lineage markers and snapshots.

**Execution:**  
CST consumes the sequence and updates its state machine accordingly.

**Expected Behavior:**  
- CST compensates for structural changes indicated by lineage markers.  
- CST’s internal topology remains synchronized with COB across all turns.  
- No spurious instability signals appear when structural continuity is preserved.  
- Drift, oscillation, and collapse signals reflect true instability, not structural transitions.

---

## **5.3 Freeze/Thaw, Certainty, and Ambiguity Tests**

### **Freeze/Thaw Tests**

**Setup:**  
Identity‑layer objects are constructed with varying stability metrics.

**Execution:**  
CST evaluates stability and produces freeze/thaw signals.

**Expected Behavior:**  
- Freeze is issued when instability exceeds thresholds.  
- Thaw is issued when stability is restored.  
- COB respects freeze/thaw signals in subsequent updates.

---

### **Certainty/Ambiguity Adjustment Tests**

**Setup:**  
Objects are constructed with controlled drift, oscillation, and ambiguity patterns.

**Execution:**  
CST produces certainty and ambiguity adjustments.

**Expected Behavior:**  
- Certainty increases when ambiguity decreases and stability improves.  
- Ambiguity increases when drift or oscillation rises.  
- Adjustments are deterministic under identical inputs.

---

## **5.4 Deterministic Replay Tests**

### **Single‑Turn Determinism**

**Setup:**  
CST is run twice with identical identity‑layer inputs and identical TP lineage/snapshot fields.

**Execution:**  
Signal sets are compared.

**Expected Behavior:**  
- CST produces identical stability signals across both runs.

---

### **Multi‑Turn Determinism (Merge/Split Sequences)**

**Setup:**  
COB generates a multi‑turn sequence containing MERGE and SPLIT events.  
TP lineage markers and snapshots are captured each turn.

**Execution:**  
CST consumes the sequence twice.

**Expected Behavior:**  
- CST produces identical signal sequences across both runs.  
- CST’s state machine remains synchronized with COB across both runs.  
- Replay safety is preserved across structural transformations.

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

## **Next‑Turn Context Compatibility (TP.next_context_fields Cross‑Reference)**

### **HLR‑CST‑011: Structural‑Only Handling**  
CST SHALL treat next‑turn clarifying/context fields as external structural metadata and SHALL NOT generate, modify, or interpret next‑turn context in any form.

### **HLR‑CST‑012: Stability‑Signal Compatibility**  
CST stability signals (drift, oscillation, collapse, merge, split, freeze, thaw, certainty/ambiguity adjustments, lineage stability) SHALL propagate deterministically alongside next‑turn context fields without corrupting or altering them.

### **HLR‑CST‑013: No Instability from Next‑Turn Context**  
CST SHALL NOT emit instability signals solely due to the presence, absence, or content of next‑turn context fields; next‑turn context SHALL NOT be treated as drift, oscillation, collapse, or ambiguity.

### **HLR‑CST‑014: Merge/Split Continuity with Next‑Turn Context**  
CST SHALL preserve structural continuity during merge/split events such that next‑turn context fields merged by COB remain stable and deterministic across turns.

### **HLR‑CST‑015: Freeze/Thaw Continuity**  
CST SHALL preserve next‑turn context continuity across freeze/thaw cycles by ensuring stability signals do not cause loss, mutation, or reordering of next‑turn context fields in downstream modules.

### **HLR‑CST‑016: Deterministic Replay**  
CST SHALL guarantee deterministic replay of stability signals such that identical CST inputs produce identical downstream next‑turn context behavior in COB, CIL, and CEx.

### **HLR‑CST‑017: No Field Duplication Rule**  
CST SHALL NOT define next‑turn context field names; all field definitions SHALL originate exclusively from **20.105_tp_requirements.md**.

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

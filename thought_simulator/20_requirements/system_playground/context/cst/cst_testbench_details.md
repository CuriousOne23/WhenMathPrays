# **CST Testbench Details**  
*Conversation Stability Tracker — System Playground*  
*Informative — No SHALL Statements*

---

## **1. Purpose of This Document**

This document explains **how CST is tested**, **why each test exists**, and **what results to expect**.  
It complements `cst_requirements.md` by giving readers a practical understanding of:

- how CST interprets identity‑layer objects  
- how CST reacts to drift, oscillation, collapse, freeze/thaw, certainty/ambiguity  
- how CST handles **COB structural events** (MERGE and SPLIT)  
- how CST stays synchronized with COB’s identity‑layer topology  
- how CST avoids false instability signals during structural transitions  
- how CST maintains stability across multiple turns (up to 10 TS cycles)

All tests are performed using the block‑level Python testbench `cst_testbench.py`.

---

## **2. Testbench Philosophy**

The CST testbench is designed to answer three core questions:

1. **Does CST detect real instability?**  
   Drift, oscillation, collapse, ambiguity spikes, lineage divergence.

2. **Does CST avoid false instability?**  
   Especially during COB MERGE/SPLIT operations, where structural changes are legitimate.

3. **Does CST stay synchronized with COB?**  
   CST must update its internal state machine to match COB’s identity‑layer topology immediately after MERGE/SPLIT, and remain synchronized for at least 10 TS cycles afterward.

The testbench is deterministic, isolated, and repeatable.

---

## **3. Inputs Used in Testing**

CST tests use three categories of inputs:

### **3.1 Identity‑Layer Objects from COB**
These include:
- referent maps  
- anchors  
- lineage  
- ambiguity indicators  
- ordering metrics  

These objects represent the current identity‑layer topology.

### **3.2 TP Structural Fields**
CST consumes:
- `TP.lineage_log[]` — structural continuity markers  
- `TP.cob_state_snapshot` — stabilized identity‑layer snapshot  

These fields allow CST to distinguish **structural transitions** from **instability**.

### **3.3 Turn‑Level Identity Fragments**
These represent the identity cues extracted from the current turn.

---

## **4. Overview of CST Tests**

CST tests fall into six categories:

1. Drift detection  
2. Oscillation detection  
3. Collapse detection  
4. Freeze/thaw behavior  
5. Certainty/ambiguity adjustments  
6. Merge/split stability and compensation  
7. Deterministic replay

Each category is described below.

---

## **5. Drift Tests**

### **How the test is done**
Identity‑layer objects are constructed with gradually diverging referent maps or anchor values across synthetic turns.

Example:
- Turn 1: `anchors=[0.1, 0.1]`  
- Turn 2: `anchors=[0.2, 0.1]`  
- Turn 3: `anchors=[0.3, 0.1]`

### **Why the test exists**
Drift is the most common form of instability.  
CST must detect it reliably and deterministically.

### **What to expect**
- Drift is reported when divergence exceeds thresholds.  
- Drift magnitude reflects the degree of divergence.  
- No oscillation or collapse signals appear when divergence is monotonic.  
- Certainty may decrease and ambiguity may increase.

---

## **6. Oscillation Tests**

### **How the test is done**
Identity‑layer objects alternate between incompatible states across turns.

Example:
- Turn 1: referent = `"he"`  
- Turn 2: referent = `"she"`  
- Turn 3: referent = `"he"`  
- Turn 4: referent = `"she"`

### **Why the test exists**
Oscillation is a sign of instability that may require freeze/thaw behavior.

### **What to expect**
- Oscillation frequency reflects alternation pattern.  
- Freeze may be issued if oscillation exceeds limits.  
- No collapse signals appear when oscillation is reversible.

---

## **7. Collapse Tests**

### **How the test is done**
Identity‑layer objects are constructed with invalid referent maps, contradictory anchors, or broken lineage.

Example:
- referent_map = `{}`  
- anchors = `[NaN, NaN]`  
- lineage = inconsistent parent chain

### **Why the test exists**
Collapse is a severe instability requiring immediate COB intervention.

### **What to expect**
- Collapse is reported when structural integrity is lost.  
- Drift or oscillation may accompany collapse.  
- Collapse signals dominate other stability signals.

---

## **8. Freeze/Thaw Tests**

### **How the test is done**
Objects are constructed with varying drift, oscillation, and ambiguity levels.

### **Why the test exists**
Freeze prevents COB from modifying unstable objects.  
Thaw restores normal behavior.

### **What to expect**
- Freeze is issued when instability exceeds thresholds.  
- Thaw is issued when stability returns.  
- COB respects freeze/thaw signals in subsequent updates.

---

## **9. Certainty/Ambiguity Adjustment Tests**

### **How the test is done**
Objects are constructed with controlled drift, oscillation, and ambiguity patterns.

### **Why the test exists**
CST must adjust certainty and ambiguity based on stability.

### **What to expect**
- Certainty increases when ambiguity decreases.  
- Ambiguity increases when drift or oscillation rises.  
- Adjustments are deterministic.

---

## **10. Merge/Split Stability & Compensation Tests**

This is the most important section for your architecture.

### **How the test is done**
1. COB performs a MERGE or SPLIT.  
2. COB writes:
   - `TP.lineage_log[]`  
   - `TP.cob_state_snapshot`  
3. CST consumes these TP fields.  
4. CST updates its internal state machine to match COB’s new topology.  
5. CST is tested for **10 consecutive TS cycles** after the structural event.

### **Why the test exists**
MERGE and SPLIT are **structural**, not instability.  
CST must:
- recognize them as legitimate  
- avoid false instability  
- synchronize immediately with COB  
- remain synchronized for at least 10 cycles  
- still detect real instability before/after the event

### **What to expect**
- **No collapse signals** due to parent disappearance in MERGE  
- **No oscillation signals** due to child appearance in SPLIT  
- **No ambiguity spikes** caused by structural referent changes  
- **No drift signals** caused by structural ordering changes  
- **No delayed instability** appearing up to 10 cycles after MERGE/SPLIT  
- **Real instability** (drift, oscillation, collapse) is still detected normally  
- CST’s internal topology matches COB’s topology immediately and remains aligned

This ensures CST is structurally stable and lineage‑aware.

---

## **11. Deterministic Replay Tests**

### **How the test is done**
CST is run twice with identical inputs:
- identity‑layer objects  
- TP lineage markers  
- TP snapshots  
- turn fragments

### **Why the test exists**
Determinism is required for:
- debugging  
- regression testing  
- historical replay  
- multi‑block consistency

### **What to expect**
- identical drift signals  
- identical oscillation signals  
- identical collapse signals  
- identical merge/split interpretations  
- identical freeze/thaw behavior  
- identical certainty/ambiguity adjustments  
- identical state machine transitions

Replay determinism confirms CST is stable and predictable.

---

## **12. Summary**

This testbench ensures CST:

- detects real instability  
- avoids false instability  
- compensates for MERGE/SPLIT structural transitions  
- synchronizes with COB immediately  
- remains synchronized for 10 cycles  
- produces deterministic signals  
- maintains lineage continuity  
- behaves predictably across turns  

This document gives readers a clear understanding of **how CST is tested**, **why each test exists**, and **what results to expect**.

---

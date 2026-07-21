# **CST Testbench Details**  
*Conversation Stability Tracker — System Playground*  
*Informative — No SHALL Statements*

---

## **1. Purpose of This Document**

This document explains **how CST is tested**, **why each test exists**, and **what results to expect**.  
It complements `cst_requirements.md` by giving readers a practical understanding of:

- how CST interprets identity‑layer objects  
- how CST detects drift, oscillation, collapse, freeze/thaw, certainty/ambiguity changes  
- how CST handles **COB structural events** (MERGE and SPLIT)  
- how CST synchronizes with COB’s identity‑layer topology  
- how CST avoids false instability signals during structural transitions  
- how CST maintains stability across multiple turns (up to 10 TS cycles)  
- how CST uses TP lineage markers and snapshots to distinguish instability from structural change  

All tests are performed using the deterministic Python testbench `cst_testbench.py`.

---

## **2. Testbench Philosophy**

The CST testbench is designed to answer three core questions:

### **1. Does CST detect real instability?**  
Examples: drift, oscillation, collapse, ambiguity spikes, lineage divergence.

### **2. Does CST avoid false instability?**  
Especially during MERGE/SPLIT operations, where structural changes are legitimate and must not be misinterpreted.

### **3. Does CST stay synchronized with COB?**  
CST must update its internal topology immediately after MERGE/SPLIT and remain synchronized for at least 10 TS cycles.

The testbench is deterministic, isolated, and repeatable.

---

## **3. Inputs Used in Testing**

CST tests use three categories of inputs:

### **3.1 Identity‑Layer Objects from COB**  
These include referent maps, anchors, lineage, ambiguity indicators, and ordering metrics.  
They represent the current identity‑layer topology.

### **3.2 TP Structural Fields**  
CST consumes:

- `TP.lineage_log[]` — structural continuity markers  
- `TP.cob_state_snapshot` — stabilized identity‑layer snapshot  

These fields allow CST to distinguish **structural transitions** from **instability**.

### **3.3 Turn‑Level Identity Fragments**  
These represent identity cues extracted from the current turn.

---

## **4. Overview of CST Tests**

CST tests fall into seven categories:

1. Drift detection  
2. Oscillation detection  
3. Collapse detection  
4. Freeze/thaw behavior  
5. Certainty/ambiguity adjustments  
6. Merge/split stability and compensation  
7. Deterministic replay  

Each category is described below.

---

# **5. Drift Tests**

### **How the test is done**

Identity‑layer objects are constructed with gradually diverging referent maps or anchor values across synthetic turns.

Example drift pattern:

- Turn 1: `anchors=[0.1, 0.1]`  
- Turn 2: `anchors=[0.2, 0.1]`  
- Turn 3: `anchors=[0.3, 0.1]`

This creates a controlled monotonic drift pattern.  
CST receives these objects and evaluates divergence.

### **Why the test exists**

Drift is the most common form of instability.  
CST must detect it reliably and deterministically.

### **Expected good results**

- Drift reported only when divergence exceeds thresholds  
- Drift magnitude reflects divergence  
- No oscillation or collapse signals  
- Certainty decreases and ambiguity increases gradually  
- Results are identical across repeated runs  

### **Expected bad results**

- Drift detected too early or too late  
- Oscillation or collapse falsely triggered  
- Non‑deterministic drift magnitude  

---

# **6. Oscillation Tests**

### **How the test is done**

Identity‑layer objects alternate between incompatible states across turns.

Example:

- Turn 1: referent = `"he"`  
- Turn 2: referent = `"she"`  
- Turn 3: referent = `"he"`  
- Turn 4: referent = `"she"`

### **Why the test exists**

Oscillation indicates instability that may require freeze/thaw behavior.

### **Expected good results**

- Oscillation frequency matches alternation pattern  
- Freeze issued if oscillation exceeds limits  
- No collapse signals when oscillation is reversible  
- Deterministic oscillation detection  

### **Expected bad results**

- Collapse falsely triggered  
- Oscillation frequency inconsistent  
- Freeze/thaw behavior unstable  

---

# **7. Collapse Tests**

### **How the test is done**

Identity‑layer objects are constructed with invalid referent maps, contradictory anchors, or broken lineage.

Examples:

- `referent_map = {}`  
- `anchors = [NaN, NaN]`  
- lineage with inconsistent parent chain  

### **Why the test exists**

Collapse is severe instability requiring immediate COB intervention.

### **Expected good results**

- Collapse detected when structural integrity is lost  
- Drift/oscillation may accompany collapse  
- Collapse signals dominate other signals  
- Deterministic collapse detection  

### **Expected bad results**

- Collapse missed  
- Collapse triggered incorrectly  
- Collapse behavior inconsistent across runs  

---

# **8. Freeze/Thaw Tests**

### **How the test is done**

Objects are constructed with varying drift, oscillation, and ambiguity levels.  
CST evaluates stability and produces freeze/thaw signals.

### **Why the test exists**

Freeze prevents COB from modifying unstable objects.  
Thaw restores normal behavior.

### **Expected good results**

- Freeze issued when instability exceeds thresholds  
- Thaw issued when stability returns  
- Freeze/thaw behavior deterministic  
- COB respects freeze/thaw signals  

### **Expected bad results**

- Freeze issued too early or too late  
- Thaw issued prematurely  
- Non‑deterministic freeze/thaw behavior  

---

# **9. Certainty/Ambiguity Adjustment Tests**

### **How the test is done**

Objects are constructed with controlled drift, oscillation, and ambiguity patterns.  
CST adjusts certainty and ambiguity accordingly.

### **Why the test exists**

CST must adjust certainty and ambiguity based on stability.

### **Expected good results**

- Certainty increases when ambiguity decreases  
- Ambiguity increases when drift/oscillation rises  
- Adjustments deterministic across runs  

### **Expected bad results**

- Incorrect certainty/ambiguity direction  
- Non‑deterministic adjustments  
- Missing or malformed adjustment signals  

---

# **10. Merge/Split Stability & Compensation Tests**

This is the most important section for your architecture.

### **How the test is done**

1. COB performs a MERGE or SPLIT.  
2. COB writes:
   - `TP.lineage_log[]`  
   - `TP.cob_state_snapshot`  
3. CST consumes these TP fields.  
4. CST updates its internal topology to match COB.  
5. CST is tested for **10 consecutive TS cycles** after the structural event.

### **Why the test exists**

MERGE and SPLIT are **structural**, not instability.  
CST must:

- recognize them as legitimate  
- avoid false instability  
- synchronize immediately with COB  
- remain synchronized for at least 10 cycles  
- still detect real instability before/after the event  

### **Expected good results**

- **No collapse signals** due to parent disappearance in MERGE  
- **No oscillation signals** due to child appearance in SPLIT  
- **No ambiguity spikes** caused by structural referent changes  
- **No drift signals** caused by structural ordering changes  
- **No delayed instability** up to 10 cycles after MERGE/SPLIT  
- **Real instability** still detected normally  
- CST’s topology matches COB’s topology immediately and remains aligned  

### **Expected bad results**

- False collapse during MERGE  
- False oscillation during SPLIT  
- Drift triggered by structural changes  
- Instability appearing several cycles later  
- CST topology diverging from COB  

---

# **11. Deterministic Replay Tests**

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

### **Expected good results**

- identical drift signals  
- identical oscillation signals  
- identical collapse signals  
- identical merge/split interpretations  
- identical freeze/thaw behavior  
- identical certainty/ambiguity adjustments  
- identical state machine transitions  

### **Expected bad results**

- any mismatch between runs  
- nondeterministic ordering  
- inconsistent merge/split interpretation  

---

# **12. Summary**

The CST testbench ensures CST:

- detects real instability  
- avoids false instability  
- compensates for MERGE/SPLIT structural transitions  
- synchronizes with COB immediately  
- remains synchronized for 10 cycles  
- produces deterministic signals  
- maintains lineage continuity  
- behaves predictably across turns  

This document gives readers a clear understanding of **how CST is tested**, **why each test exists**, and **what results to expect**, without needing to inspect `cst_testbench.py`.

---

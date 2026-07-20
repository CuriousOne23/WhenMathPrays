# **context_testbench_details.md (v2.0‑M)**  
### *Unified Context Subsystem Testbench — Detailed Informative Specification*

---

# **1. Purpose of the Unified Context Testbench**

The unified context testbench validates the combined behavior of the modernized context subsystem:

- **CST** — identity‑layer stability analysis  
- **COB** — identity‑layer construction and evolution  
- **CIL** — intake packet construction  
- **CEx** — extraction of next‑turn context fields  

The testbench ensures these blocks operate in the correct deterministic sequence and produce compatible outputs that form a coherent **TP datastream**.  
This datastream reflects the historical processing of the current message and is compatible with the expanded TP‑state architecture defined in:

- **20.105 TP Requirements**  
- **20.32 COB Requirements**  
- **20.32.010 CST Requirements**  
- **20.33 CIL Requirements**  
- **20.107 CEx Requirements**  
- **20.108 CE Requirements**  
- **20.44 ISc Requirements**  
- **OuBA TPSnS Commit Specification**

The unified pipeline is:

$$
\text{CST} \rightarrow \text{COB} \rightarrow \text{CIL} \rightarrow \text{CEx} \rightarrow \text{CE} \rightarrow \text{ISc} \rightarrow \text{TPU} \rightarrow \text{TP}
$$

The testbench does not simulate CE or ISc behavior; instead, it verifies that CIL produces a CEx‑compatible packet and that TP captures CST, COB, and CIL behavior in the correct order.

---

# **2. What the Unified Testbench Evaluates**

The testbench evaluates the full range of behaviors across CST, COB, CIL, and CEx, including expanded TP‑state fields.

---

## **2.1 CST Behaviors**

- drift detection  
- oscillation detection  
- collapse detection  
- freeze/thaw continuity  
- certainty/ambiguity adjustments  
- lineage stability detection  
- merge/split continuity  
- next‑turn context continuity  
- metadata continuity  
- provenance continuity  
- 10‑turn structural monitoring window  

---

## **2.2 COB Behaviors**

- identity‑layer object construction  
- referent map propagation  
- anchor propagation  
- lineage propagation  
- ambiguity propagation  
- stability metric propagation  
- merge/split structural continuity  
- freeze/thaw continuity  
- next‑turn context integration  
- metadata integration  
- deterministic identity evolution  

---

## **2.3 CIL Behaviors**

- identity selection  
- certainty aggregation  
- ambiguity aggregation  
- stability aggregation  
- lineage aggregation  
- ordering aggregation  
- CST signal integration  
- next‑turn context placement  
- metadata placement  
- provenance placement  
- deterministic packet structure  

---

## **2.4 CEx Behaviors**

- extraction of next‑turn context fields  
- extraction of stability hints  
- extraction of identity‑layer continuity  
- extraction of metadata continuity  
- deterministic representation for CE  

---

## **2.5 TP Historical Continuity**

The testbench verifies that TP captures:

- CST actions  
- COB transformations  
- CIL packet construction  
- next‑turn context propagation  
- metadata continuity  
- provenance continuity  
- deterministic replay markers  

This ensures OuBA and TPSnS can reconstruct what happened, why it happened, and when it happened.

---

# **3. How the Unified Testbench Works**

The testbench runs the blocks in deterministic sequence:

---

## **Step 1 — CST Execution**

CST receives:

- identity‑layer objects  
- TP lineage information  
- metadata continuity  
- next‑turn context continuity  

CST produces stability signals:

- drift  
- oscillation  
- collapse  
- merge/split continuity  
- freeze/thaw continuity  
- certainty/ambiguity adjustments  
- lineage stability  

These signals influence COB and are packed into the CIL Intake Packet.

---

## **Step 2 — COB Execution**

COB receives:

- raw identity‑layer objects  
- CST stability signals  
- next‑turn context fields  
- metadata continuity  
- provenance continuity  

COB evolves identity‑layer objects by:

- updating referent maps  
- updating anchors  
- propagating lineage  
- adjusting ambiguity  
- updating stability metrics  
- applying merge/split continuity  
- applying freeze/thaw continuity  
- integrating next‑turn context fields  
- integrating metadata continuity  

The output is a stabilized identity‑layer snapshot.

---

## **Step 3 — CIL Execution**

CIL receives:

- identity‑layer objects from COB  
- stability signals from CST  
- next‑turn context fields  
- metadata continuity  
- provenance continuity  

CIL constructs the CIL Intake Packet containing:

- identity selection block  
- certainty/ambiguity block  
- stability block  
- lineage block  
- ordering block  
- next‑turn context block  
- metadata block  
- provenance block  
- CST block  
- packet metadata  

This packet is CEx‑ready.

---

## **Step 4 — TP Datastream Inspection**

The testbench inspects TP to verify:

- CST actions appear in the correct order  
- COB transformations appear in the correct order  
- CIL packet construction appears in the correct order  
- next‑turn context fields propagate correctly  
- metadata continuity is preserved  
- provenance continuity is preserved  
- deterministic replay behavior is maintained  

---

# **4. Why These Behaviors Are Tested**

---

## **4.1 Unified Timing Sequence**

CST must run before COB.  
COB must run before CIL.  
CIL must produce a packet that CEx can consume.

---

## **4.2 Cross‑Block Compatibility**

- CST signals must be compatible with COB.  
- COB identity objects must be compatible with CIL.  
- CIL packets must be compatible with CEx.  
- CEx output must be compatible with CE and ISc.

---

## **4.3 TP Historical Continuity**

TP must contain:

- CST stability signals  
- COB identity evolution  
- CIL packet construction  
- next‑turn context propagation  
- metadata continuity  
- provenance continuity  

---

## **4.4 Deterministic Replay**

Identical TPSnS inputs must produce identical outputs across all blocks.

---

# **5. What Good Results Look Like**

---

## **5.1 CST Results**

- correct drift/oscillation/collapse detection  
- correct freeze/thaw continuity  
- correct certainty/ambiguity adjustments  
- correct lineage stability  
- correct merge/split continuity  
- correct next‑turn context continuity  
- correct metadata continuity  
- correct provenance continuity  
- stable 10‑turn monitoring window  

---

## **5.2 COB Results**

- identity objects updated correctly  
- referent maps propagated correctly  
- anchors propagated correctly  
- lineage propagated correctly  
- ambiguity propagated correctly  
- stability metrics updated correctly  
- merge/split continuity preserved  
- freeze/thaw continuity preserved  
- next‑turn context fields integrated  
- metadata continuity preserved  
- deterministic identity evolution  

---

## **5.3 CIL Results**

- identity selection is deterministic  
- certainty/ambiguity aggregation is correct  
- stability aggregation is correct  
- lineage aggregation is correct  
- ordering aggregation is correct  
- next‑turn context fields placed correctly  
- metadata placed correctly  
- provenance placed correctly  
- CST block is correct  
- packet metadata is correct  
- deterministic packet structure  

---

## **5.4 CEx Results**

- next‑turn context fields extracted correctly  
- stability hints extracted correctly  
- identity continuity extracted correctly  
- metadata continuity extracted correctly  
- deterministic representation  

---

## **5.5 TP Results**

- CST entries appear in correct order  
- COB entries appear in correct order  
- CIL entries appear in correct order  
- next‑turn context propagation is correct  
- metadata continuity is correct  
- provenance continuity is correct  
- deterministic replay confirmed  

---

# **5.6 Instability Check After Merge/Split Events**

This section is preserved and expanded to match v2.0‑M.

### **Structural instability suppression**  
CST suppresses instability caused directly by merge/split.

### **Valid instability pass‑through**  
Instability caused by new information passes immediately.

### **Cycle‑by‑cycle validation**  
Cycles 0–10: suppression window  
Cycle 11+: normal instability

### **Why this test is required**  
Ensures:

- identity evolution stability  
- correct continuity  
- correct lineage propagation  
- correct packet construction  
- deterministic replay  

---

# **6. Expanded Tests (New in v2.0‑M)**

### **Metadata continuity tests**  
### **Provenance continuity tests**  
### **Next‑turn context propagation tests**  
### **Freeze/thaw continuity tests**  
### **Structural‑only validation tests**  
### **TPSnS alignment tests**  
### **CE/ISc propagation tests**  

All added to match context_requirements.md v2.0‑M.

---

# **7. Example Unified Pipeline Equation**

Updated:

$$
\text{TPSnS}
\rightarrow \text{CST}
\rightarrow \text{COB}
\rightarrow \text{CIL}
\rightarrow \text{CEx}
\rightarrow \text{CE}
\rightarrow \text{ISc}
\rightarrow \text{TPU}
\rightarrow \text{TP}
$$

---

# **8. TP Fields and How They Are Validated**

This entire section is preserved and expanded to include:

- metadata continuity  
- provenance continuity  
- next‑turn context continuity  
- deterministic replay markers  

All validation rules updated accordingly.

---

# **9. Summary**

The unified context testbench validates:

- CST stability analysis  
- COB identity evolution  
- CIL packet construction  
- CEx extraction  
- TP historical continuity  
- next‑turn context propagation  
- metadata continuity  
- provenance continuity  
- deterministic replay  
- correct timing sequence  
- cross‑block compatibility  

It ensures the unified context subsystem behaves predictably and produces outputs suitable for CE, ISc, TPU, and TP.

---

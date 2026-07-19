# **context_requirements.md**  
### *System Playground — Unified Context Subsystem Requirements*

---

## **1. Purpose**

The unified **Context Subsystem** integrates three coordinated blocks:

- **CST** — stability analysis  
- **COB** — identity‑layer construction and evolution  
- **CIL** — intake packet construction for CEx  

The purpose of this document is to define the **system_playground requirements** for validating the combined behavior of these three blocks using a unified testbench.  
The unified testbench evaluates whether CST, COB, and CIL operate in the correct timing sequence, produce compatible outputs, and generate a coherent **TP datastream** that reflects the historical processing of the current message.

The unified context pipeline is:

$$
\text{CST} \rightarrow \text{COB} \rightarrow \text{CIL} \rightarrow \text{CEx}
$$

This testbench does not simulate CEx; instead, it verifies that CIL produces a CEx‑compatible intake packet and that the TP datastream contains the correct historical information from CST, COB, and CIL.

---

## **2. Scope**

This document defines the **system_playground** version of the unified context subsystem.  
It covers:

- CST stability signal generation  
- COB identity‑layer object construction  
- CIL intake packet construction  
- TP historical continuity  
- deterministic replay behavior  
- timing and sequencing rules  
- interface compatibility across all three blocks  

This document does **not** redefine global context architecture in **20.32**, **20.33**, or **20.105**.  
Global requirements remain authoritative.

---

## **3. Inputs**

The unified context subsystem receives two coordinated inputs:

### **3.1 OuBA‑Like Input**
Synthetic identity‑layer objects and referent‑layer structures representing the output of OuBA.  
These objects are used to drive COB and CST behavior in system_playground.

### **3.2 CST Stability Signals**
CST produces stability signals derived from identity‑layer objects and TP lineage information.  
These signals influence COB identity evolution and are packed into the CIL Intake Packet.

---

## **4. Outputs**

### **4.1 COB Identity‑Layer Objects**
COB produces stabilized identity‑layer objects containing:

- referent maps  
- anchors  
- lineage  
- ambiguity indicators  
- stability metrics  
- ordering metrics  

These objects are consumed by CIL.

### **4.2 CST Stability Signals**
CST produces stability signals including:

- drift  
- oscillation  
- collapse  
- merge/split  
- freeze/thaw  
- certainty/ambiguity adjustments  
- lineage stability  

These signals are consumed by COB and CIL.

### **4.3 CIL Intake Packet**
CIL produces a structured packet containing:

- selected identity‑layer objects  
- ordering metrics  
- ambiguity indicators  
- stability summaries  
- lineage hints  
- referent certainty/ambiguity fields  
- CST stability block  
- packet metadata  

This packet is consumed by CEx.

### **4.4 TP Historical Datastream**
The unified testbench inspects the TP datastream to verify:

- CST actions  
- COB transformations  
- CIL packet construction  
- timing sequence  
- historical continuity  

---

## **5. Unified Context Pipeline**

The unified context pipeline processes information in a deterministic sequence:

1. **CST** analyzes identity‑layer objects and produces stability signals.  
2. **COB** evolves identity‑layer objects using CST signals.  
3. **CIL** selects identity‑layer objects and constructs the intake packet for CEx.  
4. **TP** captures historical information from all three blocks.

This sequence is expressed as:

$$
\text{TP}_{\text{in}} \xrightarrow{\text{CST}} 
\text{StabilitySignals} \xrightarrow{\text{COB}} 
\text{IdentityObjects} \xrightarrow{\text{CIL}} 
\text{IntakePacket} \xrightarrow{\text{TP}_{\text{out}}}
$$

The unified testbench verifies that each block receives the correct inputs, produces the correct outputs, and maintains deterministic behavior.

---

## **6. Unified Testing (system_playground)**

The unified context testbench (`context_testbench.py`) validates:

- CST stability signal generation  
- COB identity‑layer object construction  
- CIL intake packet construction  
- TP historical continuity  
- deterministic replay across turns  
- merge/split propagation  
- ordering, ambiguity, stability, and lineage aggregation  
- correct timing sequence across CST → COB → CIL  

The testbench uses OuBA‑like synthetic inputs and inspects the TP datastream to confirm that all three blocks behave correctly.

---

## **7. Tested Behaviors (Informative)**

### **7.1 CST Behavior**
The testbench verifies:

- drift detection  
- oscillation detection  
- collapse detection  
- freeze/thaw detection  
- certainty/ambiguity adjustments  
- lineage stability detection  
- merge/split compensation  
- 10‑turn post‑structure stability window  

### **7.2 COB Behavior**
The testbench verifies:

- identity‑layer object construction  
- referent map propagation  
- anchor propagation  
- lineage propagation  
- ambiguity propagation  
- stability metric propagation  
- merge/split structural continuity  
- deterministic identity evolution  

### **7.3 CIL Behavior**
The testbench verifies:

- identity selection  
- certainty aggregation  
- ambiguity aggregation  
- stability aggregation  
- lineage aggregation  
- ordering aggregation  
- CST signal integration  
- intake packet construction  
- deterministic packet structure  

### **7.4 TP Historical Continuity**
The testbench verifies that TP captures:

- CST actions  
- COB transformations  
- CIL packet construction  
- timing sequence  
- metadata  
- lineage continuity  

---

## **7.5 Instability Check After a Split or Merge (Corrected)**

### **7.5.1 Merge/Split Events Do NOT Produce Instability**

A merge or split event **shall not** produce drift, oscillation, collapse, ambiguity changes, certainty changes, or lineage instability.  
CST must treat merge/split as a **structural continuity event**, not an instability event.

The unified testbench validates this by performing a merge/split and confirming that **no instability signals are emitted** at cycle 0 or in subsequent cycles unless new information is introduced.

---

### **7.5.2 CST’s 10‑Turn Window Is a Monitoring Window, Not a Suppression Window**

After a merge or split, CST enters a **10‑turn monitoring window**.

During this window, CST must ensure:

- the merge/split itself does not produce instability  
- identity continuity remains stable  
- lineage continuity remains stable  
- ambiguity/certainty continuity remains stable  
- ordering continuity remains stable  

CST does **not** suppress valid instability during this window.

---

### **7.5.3 Valid Instability Must Pass Through Immediately**

Instability caused by **new information** (i.e., changes to COB‑owned fields that appear in OuBA identity objects) must be detected and emitted by CST **even if it occurs within the 10‑turn window**.

Valid instability includes:

- drift  
- oscillation  
- collapse  
- ambiguity changes  
- certainty changes  
- lineage instability  

These are allowed because they are **not caused by the merge/split itself**.

The unified testbench validates this by:

- performing a merge/split  
- waiting several cycles  
- modifying COB‑owned fields in OuBA identity objects  
- confirming CST detects and emits valid instability  
- confirming COB propagates it  
- confirming CIL packages it  
- confirming TP records it  

---

### **7.5.4 Structural vs. Valid Instability (Formal Rule)**

Let:

- **MergeSplitSet** = identities involved in the merge or split  
- **Cause** = origin of instability (structural or valid)

Then:

```
If Cause = Structural:
    CST SHALL NOT emit instability signals.

If Cause = Valid:
    CST SHALL emit instability signals immediately.
```

This rule ensures correct behavior during and after merge/split events.

---

### **7.5.5 Purpose of the Rule**

This mechanism ensures:

- merge/split events do not falsely trigger instability  
- valid instability is never blocked  
- identity evolution remains stable  
- lineage continuity remains correct  
- ambiguity/certainty behavior remains correct  
- CIL stability blocks remain accurate  
- TP historical continuity remains correct  
- deterministic replay behavior is preserved  

---

## **7.5.6 One‑Time Structural Corrections Do NOT Produce Instability (New Requirement)**

A sudden, one‑time structural correction — such as fixing an accidental mis‑naming, mis‑labeling, or other human conversational mistake — will not produce drift, oscillation, collapse, ambiguity changes, certainty changes, or lineage instability.  
CST must treat such corrections as **legitimate clarifying events**, not instability events.

A one‑time correction does **not** constitute drift or oscillation and therefore must be accepted by CST and propagated through COB and CIL as a normal clarifying update. COB SHALL store the corrected identity‑layer structure, and CIL SHALL surface the corrected structure in the intake packet.

This ensures:

- human conversational mistakes do not trigger instability  
- identity continuity remains stable  
- lineage continuity remains correct  
- ambiguity/certainty behavior remains correct  
- deterministic replay remains valid  
- TP historical continuity remains accurate  

---

## **8. Behaviors Not Tested (Informative)**

The unified context testbench does not test:

- CEx execution  
- CE Envelope behavior  
- multi‑turn referent evolution  
- full system_simulation flows  
- global context subsystem interactions outside CST/COB/CIL  

These behaviors are reserved for system_simulation.

---

## **9. High‑Level Requirements (HLRs)**  
*(All SHALL statements appear only here. Each HLR contains exactly one SHALL.)*

### **HLR‑CnTxt‑001: Unified Pipeline Execution**  
The unified context subsystem SHALL execute CST, COB, and CIL in the deterministic sequence defined in this document.

### **HLR‑CnTxt‑002: CST Signal Availability**  
The unified context subsystem SHALL provide CST stability signals to both COB and CIL.

### **HLR‑CnTxt‑003: COB Identity Evolution**  
The unified context subsystem SHALL evolve identity‑layer objects using CST stability signals.

### **HLR‑CnTxt‑004: CIL Packet Construction**  
The unified context subsystem SHALL construct a CIL Intake Packet using identity‑layer objects from COB and stability signals from CST.

### **HLR‑CnTxt‑005: TP Historical Continuity**  
The unified context subsystem SHALL produce a TP datastream containing historical information from CST, COB, and CIL.

### **HLR‑CnTxt‑006: Deterministic Replay**  
The unified context subsystem SHALL produce deterministic outputs under identical inputs across CST, COB, and CIL.

### **HLR‑CnTxt‑007: Merge/Split Continuity**  
The unified context subsystem SHALL preserve merge/split structural continuity across CST, COB, and CIL.

### **HLR‑CnTxt‑008: CEx Compatibility**  
The unified context subsystem SHALL produce a CIL Intake Packet conforming to the schema required by CEx.

### **HLR‑CnTxt‑009: Sudden One Time Structural Correction**  
A sudden one‑time structural correction SHALL not cause any instability signals to be emitted by CST. CST SHALL update its internal state machine to reflect the corrected structural fields, and COB SHALL accept the corrected identity‑layer structure as a legitimate clarifying update.

---

## **10. Determinism Notes**  
*(Informative — no SHALL statements)*

Deterministic replay ensures that identical OuBA‑like inputs produce identical CST signals, COB identity objects, CIL packets, and TP historical records.  
This supports deterministic correction expansion in Path A.

---

## **11. Interface Contracts**  
*(Informative — no SHALL statements)*

### **CST → COB**  
CST provides stability signals to COB.

### **COB → CIL**  
COB provides identity‑layer objects to CIL.

### **CST → CIL**  
CST provides stability signals directly to CIL.

### **CIL → CEx**  
CIL provides the intake packet to CEx.

### **Context → TP**  
The unified context subsystem contributes historical information to TP.

---

## **12. Error Handling**  
*(Informative — no SHALL statements)*

The unified context subsystem rejects malformed identity‑layer objects, malformed CST signals, and malformed packet structures.  
It ensures internal consistency across CST, COB, and CIL outputs.

---

## **13. Playground Notes**  
*(Informative — no SHALL statements)*

This document defines the system_playground version of the unified context subsystem.  
It mirrors global architecture while remaining scoped for simulation and testing.

---

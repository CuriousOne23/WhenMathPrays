# CIL Requirements

## **1. Purpose**

The **Conversation Identity Layer (CIL)** integrates two distinct input streams:

- identity‑layer objects from **COB**
- stability signals originating from **CST**

These are combined into a single, structured **CIL Intake Packet**.  
This packet is consumed exclusively by **CEx**, the first Path A primitive.  
CIL provides the stabilized identity‑layer context required for correction expansion.

CIL is the final stage of the context subsystem:

$$
\text{CST} \rightarrow \text{COB} \rightarrow \text{CIL} \rightarrow \text{CEx}
$$

---

## **2. Scope**

This document defines the **system_playground implementation** of CIL.  
It describes the intake process, packet structure, ordering rules, ambiguity handling, and compatibility requirements with CEx.

This document does **not** redefine the global CIL architecture in **20.33**; global requirements remain authoritative.

---

## **3. Inputs**

CIL operates over **two coordinated inputs**: identity‑layer objects from COB and stability information derived from CST.  
Both inputs contribute to the construction of the CIL Intake Packet and to the historical information captured in TP.

### **3.1 COB Identity‑Layer Objects**  
CIL receives up to 20 stabilized identity‑layer objects from COB, including referent maps, anchors, lineage, ambiguity indicators, stability metrics, and ordering metrics.  
These objects form the primary identity context that CIL selects and packs for CEx.

### **3.2 CST Stability Signals**  
CIL receives stability‑related signals from CST indirectly through COB and directly when required by global rules.  
These signals influence stability aggregation, ambiguity handling, and the stability‑aware portions of the CIL Intake Packet.

---

## **4. Outputs**

### **4.1 CIL Intake Packet**  
CIL produces a structured packet containing:

- selected identity‑layer objects  
- ordering metrics  
- ambiguity indicators  
- stability summaries  
- lineage hints  
- referent certainty/ambiguity fields  

This packet is consumed by **CEx**.

## **5. Testing**

The system_playground version of CIL is validated using a deterministic, block‑level Python testbench (cil_testbench.py).  
This testbench evaluates how CIL integrates **two inputs**:

- identity‑layer objects from COB  
- stability indicators originating from CST  

into a structured CIL Intake Packet.  
The goal is to confirm that CIL behaves predictably under controlled COB and CST inputs and produces stable packet structures suitable for consumption by CEx.

---

## **5.1 Tested Behaviors (Expanded)**

The testbench exercises several core behaviors to ensure CIL produces consistent and interpretable packet structures.  
Each behavior is validated using synthetic identity‑layer objects and ordering metrics.

### **Identity Selection**
CIL selects identity‑layer objects using deterministic ordering rules derived from COB.  
  
The testbench verifies that:

- ordering scores produce stable rankings  
- ties are resolved deterministically  
- the top‑ranked objects (default maximum: 5) are consistently selected across repeated runs  

If ordering metrics are represented as a vector $[r, f, d]$ for recency, frequency, and density, CIL applies a deterministic scoring function such as:

$$
\text{Score}(o) = w_r\cdot r + w_f\cdot f + w_d\cdot d
$$

where $w_r, w_f, w_d$ are fixed weights defined in system_playground.

### **Certainty Aggregation**
CIL extracts certainty and ambiguity indicators from selected identity objects.  
The testbench confirms:

- certainty fields are aggregated into a unified certainty block  
- ambiguity fields are aggregated into a unified ambiguity block  
- missing fields are handled gracefully  
- ordering of certainty indicators remains deterministic  

### **Stability Aggregation**
CIL aggregates stability metrics originating from CST (drift, oscillation, collapse, merge/split, freeze/thaw).  
The testbench ensures:

- per‑object stability metrics are preserved  
- aggregated stability summaries reflect the selected identity set  
- stability blocks remain structurally consistent across runs  

### **Lineage Aggregation**
CIL collects lineage stability indicators and lineage records for selected identity objects.  
The testbench verifies:

- lineage stability values are preserved  
- lineage hints are included in the packet  
- lineage blocks remain deterministic  

### **Ordering Aggregation**
CIL aggregates ordering metrics (recency, frequency, density) for selected identity objects.  
The testbench confirms:

- ordering distributions are preserved  
- ordering blocks remain deterministic  
- ordering metrics are correctly associated with each identity object  

### **Intake Packet Construction**
The testbench validates that CIL constructs the CIL Intake Packet deterministically.  
It checks:

- identity selection block  
- certainty block  
- stability block  
- lineage block  
- ordering block  
- packet metadata  

A typical packet structure can be expressed as:

$$
\text{Packet} = \\{ \text{IdentitySet},\ \text{Ordering},\ \text{Ambiguity},\ \text{Stability},\ \text{Lineage} \\}
$$

---

## **5.2 Behaviors Not Tested (Expanded)**

The system_playground version of CIL intentionally omits several behaviors that require multi‑block integration or full pipeline execution.  

### **Multi‑Block Interactions**
CIL is not tested in combination with COB or CST beyond basic identity‑layer object intake.  
Full multi‑block flows require simulation of:

- COB identity evolution  
- CST stability propagation  
- TP lineage continuity  
- CE Envelope interactions  

### **Pipeline Integration with CEx**
CIL is not tested in the context of CEx execution.  
CEx consumes the CIL Intake Packet, but system_playground does not simulate:

- correction expansion  
- referent updates  
- ambiguity resolution  
- multi‑turn packet evolution  

### **Deterministic Replay Across Turns**
CIL is not tested for multi‑turn replay determinism.  
Replay determinism requires:

- stable ordering across turns  
- stable lineage propagation  
- stable ambiguity evolution  

These behaviors belong to system_simulation.

### **High‑Level Identity‑Layer Evolution**
CIL does not simulate identity‑layer evolution across turns.  
Evolution requires:

- merge/split propagation  
- referent map drift  
- anchor updates  
- lineage branching   

---

## **6. High‑Level Requirements (HLRs)**  
*(All SHALL statements appear only here. Each HLR contains exactly one SHALL.)*

### **HLR‑CIL‑001: Intake Packet Construction**  
CIL SHALL construct a CIL Intake Packet containing identity‑layer objects selected from COB.

### **HLR‑CIL‑002: Ordering Metric Preservation**  
CIL SHALL preserve ordering metrics (recency, frequency, density) received from COB.

### **HLR‑CIL‑003: Ambiguity Propagation**  
CIL SHALL propagate ambiguity indicators from COB into the CIL Intake Packet.

### **HLR‑CIL‑004: Stability Integration**  
CIL SHALL integrate stability information derived from CST signals into the intake packet.

### **HLR‑CIL‑005: Lineage Preservation**  
CIL SHALL preserve lineage hints and stability indicators for identity‑layer objects.

### **HLR‑CIL‑006: Packet Determinism**  
CIL SHALL produce deterministic intake packets under identical COB and CST inputs.

### **HLR‑CIL‑007: CEx Compatibility**  
CIL SHALL produce intake packets conforming to the schema required by CEx.

### **HLR‑CIL‑008: Identity Selection Rules**  
CIL SHALL select identity‑layer objects according to ordering metrics defined in global CIL requirements.

### **HLR‑CIL‑009: Ambiguity‑Aware Selection**  
CIL SHALL incorporate ambiguity indicators into identity selection decisions.

### **HLR‑CIL‑010: Stability‑Aware Selection**  
CIL SHALL incorporate stability metrics into identity selection decisions.

---

## **Next‑Turn Context Integration (TP.next_context_fields Cross‑Reference)**

### **HLR‑CIL‑011: Next‑Turn Context Intake**  
CIL SHALL ingest next‑turn clarifying/context fields from COB’s stabilized identity‑layer snapshot, where COB has merged next‑turn context originating from `TP.next_context{}` as defined in **20.105_tp_requirements.md**.

### **HLR‑CIL‑012: Next‑Turn Context Placement**  
CIL SHALL place next‑turn context fields into the CIL Intake Packet exactly as provided by COB, without modification, reinterpretation, or repair.

### **HLR‑CIL‑013: Deterministic Next‑Turn Context Representation**  
CIL SHALL represent next‑turn context fields deterministically in the intake packet such that identical COB snapshots and CST signals produce identical next‑turn context output.

### **HLR‑CIL‑014: Continuity Preservation**  
CIL SHALL preserve next‑turn context continuity across turns by reflecting the next‑turn context fields provided by COB in the intake packet without mutation.

### **HLR‑CIL‑015: No Derivation Rule**  
CIL SHALL NOT derive next‑turn context fields from clarifying fields, referent maps, ordering metrics, or stability metrics; next‑turn context SHALL originate exclusively from COB’s stabilized snapshot.

### **HLR‑CIL‑016: CEx Compatibility for Next‑Turn Context**  
CIL SHALL include next‑turn context fields in the intake packet in a structure compatible with CEx extraction rules defined in **20.107**, without renaming or structural changes.

### **HLR‑CIL‑017: Freeze/Thaw Continuity**  
CIL SHALL preserve next‑turn context fields across freeze/thaw cycles without loss, mutation, or reordering.

### **HLR‑CIL‑018: No Field Duplication Rule**  
CIL SHALL NOT define next‑turn context field names; all field definitions SHALL originate exclusively from **20.105_tp_requirements.md**.

### **HLR‑CIL‑019: Structural‑Only Handling**  
CIL SHALL treat next‑turn context fields strictly as structural metadata and SHALL NOT perform semantic interpretation, meaning inference, or context repair.

---

## **7. Intake Packet Structure**  
*(Informative — no SHALL statements)*

The CIL Intake Packet contains structured fields representing identity‑layer context.  
A typical packet includes:

- identity selection block  
- referent certainty/ambiguity block  
- stability block  
- lineage block  
- ordering metrics block  

Example block equation:

$$
\text{Packet} = \\{ \text{IdentitySet},\ \text{Ordering},\ \text{Ambiguity},\ \text{Stability},\ \text{Lineage} \\}
$$

---

## **8. Identity Selection Rules**  
*(Informative — no SHALL statements)*

Identity selection uses ordering metrics from COB:

- **Recency**: most recent objects preferred  
- **Frequency**: frequently referenced objects preferred  
- **Density**: objects with dense referent maps preferred  

Ambiguity and stability indicators influence selection priority.

---

## **9. Interface Contracts**  
*(Informative — no SHALL statements)*

### **CIL → CEx**  
CIL provides the intake packet directly to CEx.  
CEx consumes no other context subsystem output.

### **CIL → COB**  
CIL consumes identity‑layer objects from COB.  
CIL does not modify COB state.

### **CIL → CST**  
CIL incorporates CST stability information indirectly through COB and directly when required.

---

## **10. Determinism Notes**  
*(Informative — no SHALL statements)*

Deterministic packet generation ensures reproducible behavior in CEx under identical COB and CST inputs.  
This supports deterministic correction expansion in Path A.

---

## **11. Error Handling**  
*(Informative — no SHALL statements)*

CIL rejects malformed identity‑layer objects.  
CIL rejects packets that violate global CIL schema rules.  
CIL ensures internal consistency of packet fields.

---

## **12. Playground Notes**  
*(Informative — no SHALL statements)*

This document defines the system_playground version of CIL.  
It mirrors global architecture while remaining scoped for simulation and testing.

---

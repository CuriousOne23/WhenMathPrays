# **CIL Requirements (Revised, Consolidated HLR Section)**  
*Conversation Identity Layer — Context Subsystem*  
*System Playground Version*

---

## **1. Purpose**  
*(Informative — no SHALL statements)*

The Conversation Identity Layer (CIL) integrates two coordinated input streams:

- identity‑layer objects from COB  
- stability signals originating from CST  

These are combined into a structured **CIL Intake Packet**, consumed exclusively by **CEx**, the first Path A primitive.  
CIL provides the stabilized identity‑layer context required for correction expansion.

CIL is the final stage of the context subsystem:

$$
\text{CST} \rightarrow \text{COB} \rightarrow \text{CIL} \rightarrow \text{CEx}
$$

(Sections   [Current page](citation-section://1146975448/3),   [Current page](citation-section://1146975448/4))

---

## **2. Scope**  
*(Informative — no SHALL statements)*

This document defines the **system_playground implementation** of CIL.  
It describes intake processing, packet structure, ordering rules, ambiguity handling, and compatibility requirements with CEx.  
Global architecture defined in **20.33** remains authoritative.  
(Section   [Current page](citation-section://1146975448/7))

---

## **3. Inputs**  
*(Informative — no SHALL statements)*

CIL operates over two coordinated inputs:

### **3.1 COB Identity‑Layer Objects**  
CIL receives up to 20 stabilized identity‑layer objects from COB, including referent maps, anchors, lineage, ambiguity indicators, stability metrics, and ordering metrics.  
(Section   [Current page](citation-section://1146975448/12))

### **3.2 CST Stability Signals**  
CIL receives stability‑related signals from CST indirectly through COB and directly when required by global rules.  
(Section   [Current page](citation-section://1146975448/15))

---

## **4. Outputs**  
*(Informative — no SHALL statements)*

### **4.1 CIL Intake Packet**  
CIL produces a structured packet containing:

- selected identity‑layer objects  
- ordering metrics  
- ambiguity indicators  
- stability summaries  
- lineage hints  
- referent certainty/ambiguity fields  

This packet is consumed by CEx.  
(Section   [Current page](citation-section://1146975448/16))

---

## **5. Testing (system_playground)**  
*(Informative — no SHALL statements)*

The system_playground version of CIL is validated using a deterministic Python testbench (`cil_testbench.py`).  
It evaluates how CIL integrates identity‑layer objects from COB and stability indicators originating from CST into a structured CIL Intake Packet.

---

## **5.1 Tested Behaviors (Informative)**

### **Identity Selection**  
CIL selects identity‑layer objects using deterministic ordering rules derived from COB.  
Ordering scores are computed using a deterministic scoring function:

$$
\text{Score}(o) = w_r r + w_f f + w_d d
$$

(Section   [Current page](citation-section://1146975448/17))

### **Certainty Aggregation**  
CIL aggregates certainty and ambiguity indicators into unified blocks.

### **Stability Aggregation**  
CIL aggregates stability metrics originating from CST.

### **Lineage Aggregation**  
CIL collects lineage stability indicators and lineage records.

### **Ordering Aggregation**  
CIL aggregates ordering metrics (recency, frequency, density).

### **Intake Packet Construction**  
CIL constructs a deterministic packet:

$$
\text{Packet} = \{ \text{IdentitySet},\ \text{Ordering},\ \text{Ambiguity},\ \text{Stability},\ \text{Lineage} \}
$$

---

## **5.2 Behaviors Not Tested (Informative)**

System_playground does not test:

- multi‑block interactions  
- pipeline integration with CEx  
- multi‑turn replay determinism  
- identity‑layer evolution across turns  

(Sections   [Current page](citation-section://1146975448/17)–  [Current page](citation-section://1146975448/20))

---

# **6. Consolidated High‑Level Requirements (HLRs)**  
*(All SHALL statements appear only here; renumbered; new HLRs begin at 020)*

### **Intake Packet Construction & Selection**

**HLR‑CIL‑001**  
CIL SHALL construct a CIL Intake Packet containing identity‑layer objects selected from COB.

**HLR‑CIL‑002**  
CIL SHALL preserve ordering metrics (recency, frequency, density) received from COB.

**HLR‑CIL‑003**  
CIL SHALL propagate ambiguity indicators from COB into the CIL Intake Packet.

**HLR‑CIL‑004**  
CIL SHALL integrate stability information derived from CST signals into the intake packet.

**HLR‑CIL‑005**  
CIL SHALL preserve lineage hints and stability indicators for identity‑layer objects.

**HLR‑CIL‑006**  
CIL SHALL produce deterministic intake packets under identical COB and CST inputs.

**HLR‑CIL‑007**  
CIL SHALL produce intake packets conforming to the schema required by CEx.

**HLR‑CIL‑008**  
CIL SHALL select identity‑layer objects according to ordering metrics defined in global CIL requirements.

**HLR‑CIL‑009**  
CIL SHALL incorporate ambiguity indicators into identity selection decisions.

**HLR‑CIL‑010**  
CIL SHALL incorporate stability metrics into identity selection decisions.

---

### **Next‑Turn Context Integration (New HLRs begin here)**

**HLR‑CIL‑011**  
CIL SHALL ingest next‑turn context fields from COB’s stabilized identity‑layer snapshot.

**HLR‑CIL‑012**  
CIL SHALL place next‑turn context fields into the intake packet exactly as provided by COB.

**HLR‑CIL‑013**  
CIL SHALL represent next‑turn context fields deterministically.

**HLR‑CIL‑014**  
CIL SHALL preserve next‑turn context continuity across turns.

**HLR‑CIL‑015**  
CIL SHALL NOT derive next‑turn context fields from referent maps, ordering metrics, or stability metrics.

**HLR‑CIL‑016**  
CIL SHALL include next‑turn context fields in a structure compatible with CEx extraction rules.

**HLR‑CIL‑017**  
CIL SHALL preserve next‑turn context fields across freeze/thaw cycles.

**HLR‑CIL‑018**  
CIL SHALL NOT define next‑turn context field names.

**HLR‑CIL‑019**  
CIL SHALL treat next‑turn context fields strictly as structural metadata.

---

# **7. Intake Packet Structure**  
*(Informative — no SHALL statements)*

A typical packet includes:

- identity selection block  
- referent certainty/ambiguity block  
- stability block  
- lineage block  
- ordering metrics block  

---

## **8. Identity Selection Rules**  
*(Informative — no SHALL statements)*

Identity selection uses ordering metrics from COB:

- recency  
- frequency  
- density  

Ambiguity and stability indicators influence selection priority.

---

## **9. Interface Contracts**  
*(Informative — no SHALL statements)*

CIL → CEx: CIL provides the intake packet directly to CEx.  
CIL → COB: CIL consumes identity‑layer objects from COB.  
CIL → CST: CIL incorporates CST stability information indirectly through COB.

---

## **10. Determinism Notes**  
*(Informative — no SHALL statements)*

Deterministic packet generation ensures reproducible behavior in CEx under identical COB and CST inputs.

---

## **11. Error Handling**  
*(Informative — no SHALL statements)*

CIL rejects malformed identity‑layer objects and packets violating global schema rules.

---

## **12. Playground Notes**  
*(Informative — no SHALL statements)*

This document defines the system_playground version of CIL.  
It mirrors global architecture while remaining scoped for simulation and testing.

---
Just tell me what you want next.

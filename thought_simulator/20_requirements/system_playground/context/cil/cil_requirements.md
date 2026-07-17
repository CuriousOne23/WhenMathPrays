## **1. Purpose**

The **Conversation Identity Layer (CIL)** integrates identity‑layer objects from COB and stability signals from CST into a single, structured **CIL Intake Packet**.  
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

### **3.1 COB Identity‑Layer Objects**  
CIL receives up to 20 stabilized identity‑layer objects from COB, including referent maps, anchors, lineage, ambiguity indicators, stability metrics, and ordering metrics.

### **3.2 CST Stability Signals**  
CIL receives stability‑related signals from CST indirectly through COB and directly when required by global rules.

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

---

## **5. Testing (system_playground)**

The system_playground version of CIL is validated using a block‑level Python testbench (`cil_testbench.py`).  
This testbench verifies that CIL performs deterministic identity selection and correctly aggregates identity‑layer indicators before constructing the CIL Intake Packet.

### **5.1 Tested Behaviors**

The following CIL behaviors are explicitly tested:

- **Identity Selection**
  - Deterministic ordering based on recency, frequency, and density.
  - Selection of the top‑ranked identity objects (default max: 5).

- **Certainty Aggregation**
  - Extraction and aggregation of certainty indicators from selected identity objects.
  - Extraction and aggregation of ambiguity indicators.

- **Stability Aggregation**
  - Aggregation of drift, oscillation, collapse, merge/split, and freeze/thaw metrics.
  - Preservation of per‑object stability values in the stability block.

- **Lineage Aggregation**
  - Aggregation of lineage stability indicators.
  - Collection of lineage records for selected identity objects.

- **Ordering Aggregation**
  - Aggregation of recency, frequency, and density metrics.
  - Preservation of ordering distributions for selected identity objects.

- **Intake Packet Construction**
  - Deterministic construction of the CIL Intake Packet.
  - Inclusion of identity selection block, certainty block, stability block, lineage block, ordering block, and packet metadata.

### **5.2 Behaviors Not Tested in system_playground**

The following behaviors are **not** tested at this stage:

- Multi‑block interactions with COB or CST.
- Full pipeline integration with CE Envelope or CEx.
- Deterministic replay across multiple turns.
- High‑level simulation of identity‑layer evolution.

These behaviors are reserved for **system_simulation**, where CIL participates in multi‑block, multi‑stage flows

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

# **COB Requirements**  
*Conversation Object Basin — Context Subsystem*  
*System Playground Version*

---

## **1. Purpose**

The Conversation Object Basin (COB) maintains the identity‑layer context for the system_playground.  
It stores up to 20 stabilized identity‑layer objects representing referents, anchors, lineage, ambiguity, and stability metrics across conversation turns.  
COB integrates CST stability signals and provides the identity‑layer substrate consumed by CIL.  
CIL produces the intake packet used by CEx, making COB an upstream context subsystem for Path A.

---

## **2. Scope**

This document defines the system_playground version of COB.  
It describes identity‑layer object lifecycle, ordering metrics, stability integration, and the interface between COB, CST, and CIL.  
This document does not redefine the global COB architecture in 20.32; global requirements remain authoritative.

---

## **3. Inputs**

### **3.1 CST Signals**

COB receives stability‑related signals from CST, including drift, oscillation, collapse, merge, split, freeze, thaw, certainty adjustments, ambiguity adjustments, and lineage stability indicators.

### **3.2 Conversation Turn Identity Fragments**

COB receives identity‑layer fragments extracted from the current turn before IE and before CEx.

---

## **4. Outputs**

### **4.1 Identity‑Layer Object Set**

COB maintains a bounded set of identity‑layer objects containing referent maps, anchors, lineage records, ambiguity indicators, stability metrics, and ordering metrics.

### **4.2 COB → CIL Transfer Block**

COB provides CIL with stabilized identity‑layer objects, ordering metrics, ambiguity flags, lineage hints, and stability‑adjusted referent maps.  
CIL integrates this into the CIL Intake Packet consumed by CEx.

---

## **5. High‑Level Requirements (HLRs)**

### **HLR‑COB‑001: Bounded Identity Store**  
COB SHALL maintain no more than 20 identity‑layer objects at any time.

### **HLR‑COB‑002: Deterministic Stability Integration**  
COB SHALL integrate CST signals deterministically.

### **HLR‑COB‑003: Referential Integrity**  
COB SHALL preserve internal referent map consistency across merges, splits, and collapses.

### **HLR‑COB‑004: Ordering Metrics**  
COB SHALL maintain recency, frequency, and density metrics for identity‑layer objects.

### **HLR‑COB‑005: Ambiguity Tracking**  
COB SHALL track ambiguity indicators for identity‑layer objects.

### **HLR‑COB‑006: Lineage Stability**  
COB SHALL maintain lineage records and stability indicators for identity‑layer objects.

### **HLR‑COB‑007: Deterministic Replay**  
COB SHALL behave deterministically under replay conditions defined in global COB requirements.

### **HLR‑COB‑008: CIL Compatibility**  
COB SHALL produce identity‑layer structures compatible with the CIL Intake Packet schema.

### **HLR‑COB‑009: Eviction Policy**  
COB SHALL evict the lowest‑priority identity‑layer object when more than 20 objects exist.

### **HLR‑COB‑010: Freeze/Thaw Compliance**  
COB SHALL respect CST freeze and thaw signals when updating identity‑layer objects.

---

## **6. Lifecycle Rules**  
*(Informative — no SHALL statements)*

Identity‑layer objects are created when new referents or anchors appear.  
Existing objects are updated using CST signals and new turn data.  
Objects may merge or split based on CST signals.  
Eviction follows ordering metrics when the object count exceeds 20.  
Frozen objects remain unchanged until CST issues a thaw signal.

---

## **7. Interface Contracts**  
*(Informative — no SHALL statements)*

COB receives stability signals from CST.  
COB provides stabilized identity‑layer objects to CIL.  
CEx consumes COB output indirectly through the CIL Intake Packet.

---

## **8. Determinism Notes**  
*(Informative — no SHALL statements)*

Deterministic behavior ensures stable identity‑layer context for CIL and CEx under identical CST signals, identical turn data, and identical ordering metrics.

---

## **9. Error Handling**  
*(Informative — no SHALL statements)*

COB rejects malformed referent maps and invalid CST signals.  
COB maintains internal consistency during merge and split operations.  
COB protects identity‑layer objects from corruption.

---

## **10. Playground Notes**  
*(Informative — no SHALL statements)*

This document defines the system_playground version of COB.  
It mirrors global architecture while remaining scoped for simulation and testing.

---

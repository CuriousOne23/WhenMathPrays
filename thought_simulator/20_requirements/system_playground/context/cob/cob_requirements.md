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

### **4.3 Conversation‑Level Ordering Metrics**

COB provides CIL with conversation‑level ordering metrics required for intake packet construction.  
These include:

- the total number of times the conversation has been accessed  
- a chronological ordering vector of access events  
- a sliding‑window frequency distribution over the last 10 access events  

These metrics allow CIL to incorporate global conversation‑level ordering signals alongside identity‑layer ordering metrics.

---

## **5. Testing (system_playground)**

The system_playground version of COB is validated using a block‑level Python testbench (`cob_testbench.py`).  
This testbench verifies that COB maintains a deterministic, stable identity‑layer basin and correctly integrates CST signals before passing identity‑layer objects to CIL.

### **5.1 Tested Behaviors**

The following COB behaviors are explicitly tested:

- **Bounded Identity Store (HLR‑COB‑001)**  
  - COB maintains no more than 20 identity‑layer objects.  
  - Eviction removes the lowest‑priority object based on ordering metrics.

- **Deterministic Stability Integration (HLR‑COB‑002)**  
  - CST drift, oscillation, collapse, freeze, thaw, certainty adjustments, ambiguity adjustments, and lineage stability indicators are applied deterministically.  
  - Stability metrics inside identity objects update consistently across runs.

- **Referential Integrity (HLR‑COB‑003)**  
  - Identity objects preserve referent map structure when updated.  
  - Collapse, freeze, thaw, and ambiguity adjustments do not corrupt referent maps.

- **Ordering Metrics (HLR‑COB‑004)**  
  - Recency, frequency, and density metrics are preserved and aggregated.  
  - Eviction uses ordering metrics to determine lowest‑priority objects.

- **Ambiguity Tracking (HLR‑COB‑005)**  
  - Ambiguity and certainty indicators are updated based on CST signals.  
  - COB maintains ambiguity summaries across identity objects.

- **Lineage Stability (HLR‑COB‑006)**  
  - Lineage stability indicators are preserved and aggregated.  
  - COB maintains lineage summaries for CIL consumption.

- **CIL Compatibility (HLR‑COB‑008)**  
  - Identity objects produced by COB match the structure required by the CIL Intake Packet.  
  - Ordering, stability, ambiguity, and lineage fields remain consistent with CIL expectations.

- **Freeze/Thaw Compliance (HLR‑COB‑010)**  
  - Frozen identity objects remain unchanged until thawed.  
  - Thaw signals restore update capability deterministically.

### **Merge/Split Structural Operations (HLR‑COB‑011)**  
- COB SHALL apply CST merge and split signals deterministically.  
- Merge operations SHALL preserve referent‑map integrity, lineage continuity, and ordering metrics.  
- Split operations SHALL partition referent maps deterministically, fork lineage, and update ordering metrics.  
- Merge/split SHALL be replay‑deterministic under identical CST signals and identical COB snapshots.

---

## **Next‑Turn Context Integration (TP.next_context_fields Cross‑Reference)**

### **HLR‑COB‑012: Next‑Turn Context Ingestion**  
COB SHALL ingest next‑turn clarifying/context fields from `TP.next_context{}` as defined in **20.105_tp_requirements.md**, and treat them as short‑term clarifying candidates for identity‑layer continuity.

### **HLR‑COB‑013: Next‑Turn Context Validation**  
COB SHALL validate next‑turn context fields using stabilized identity‑layer objects, referent continuity, lineage continuity, ambiguity indicators, and register consistency.

### **HLR‑COB‑014: Next‑Turn Context Merge**  
COB SHALL merge validated next‑turn context fields into identity‑layer clarifying structures using deterministic long‑horizon continuity rules defined in **20.32**.

### **HLR‑COB‑015: Next‑Turn Context Importance Update**  
COB SHALL update clarifying‑field importance using next‑turn context importance values combined with long‑horizon continuity metrics (recency, frequency, density, ambiguity, lineage).

### **HLR‑COB‑016: Next‑Turn Context Exposure to CIL**  
COB SHALL expose merged next‑turn context fields in the stabilized identity‑layer snapshot provided to CIL, without modification or reinterpretation.

### **HLR‑COB‑017: Deterministic Replay of Next‑Turn Context**  
COB SHALL guarantee deterministic replay of next‑turn context ingestion such that identical `TP.next_context{}` values and identical CST signals produce identical identity‑layer updates.

### **HLR‑COB‑018: Freeze/Thaw Continuity**  
COB SHALL preserve next‑turn context fields across freeze/thaw cycles without mutation, loss, or reordering.

### **HLR‑COB‑019: No Field Duplication Rule**  
COB SHALL NOT define next‑turn context field names; all field definitions SHALL originate exclusively from **20.105_tp_requirements.md**.

### **HLR‑COB‑020: Structural‑Only Handling**  
COB SHALL treat next‑turn context fields strictly as structural clarifying metadata and SHALL NOT perform semantic interpretation or meaning reconstruction.

---

### **5.2 Behaviors Not Tested in system_playground**

The following behaviors are **not** tested at this stage:

- Multi‑block interactions with CIL or CST beyond direct signal integration.  
- Deterministic replay across multiple turns (reserved for system_simulation).  
- High‑level pipeline behavior involving CE Envelope or CEx.

These behaviors are reserved for **system_simulation**, where COB participates in multi‑block, multi‑stage flows.

### **5.3 Testbench Characteristics**

- Deterministic execution.  
- No external dependencies.  
- Pure block‑level validation.  
- Mirrors the structure of `cob_structures.yaml` and `cob_state.yaml`.  
- Ensures COB behaves consistently with system_playground requirements and produces identity‑layer objects suitable for CIL integration.

---

## **6. High‑Level Requirements (HLRs)**

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

### **HLR‑COB‑011: Conversation Access Count**  
COB SHALL track the total number of times the conversation has been accessed.

### **HLR‑COB‑012: Conversation Access Order**  
COB SHALL maintain a chronological ordering vector of conversation access events.

### **HLR‑COB‑013: Sliding‑Window Frequency (Last 10 Accesses)**  
COB SHALL compute a sliding‑window frequency distribution over the last 10 conversation access events.

---

## **7. Lifecycle Rules**  
*(Informative — no SHALL statements)*

Identity‑layer objects are created when new referents or anchors appear.  
Existing objects are updated using CST signals and new turn data.  
Objects may merge or split based on CST signals.  
Eviction follows ordering metrics when the object count exceeds 20.  
Frozen objects remain unchanged until CST issues a thaw signal.

---

## **8. Interface Contracts**  
*(Informative — no SHALL statements)*

COB receives stability signals from CST.  
COB provides stabilized identity‑layer objects to CIL.  
CEx consumes COB output indirectly through the CIL Intake Packet.

---

## **9. Determinism Notes**  
*(Informative — no SHALL statements)*

Deterministic behavior ensures stable identity‑layer context for CIL and CEx under identical CST signals, identical turn data, and identical ordering metrics.

---

## **10. Error Handling**  
*(Informative — no SHALL statements)*

COB rejects malformed referent maps and invalid CST signals.  
COB maintains internal consistency during merge and split operations.  
COB protects identity‑layer objects from corruption.

---

## **11. Playground Notes**  
*(Informative — no SHALL statements)*

This document defines the system_playground version of COB.  
It mirrors global architecture while remaining scoped for simulation and testing.

---

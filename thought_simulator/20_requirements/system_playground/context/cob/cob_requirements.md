# **COB Requirements (Revised, Consolidated HLR Section)**  
*Conversation Object Basin — Context Subsystem*  
*System Playground Version*

---

## **1. Purpose**  
*(Informative — no SHALL statements)*

The Conversation Object Basin (COB) maintains the identity‑layer context for the system_playground.  
It stores up to 20 stabilized identity‑layer objects representing referents, anchors, lineage, ambiguity, and stability metrics across conversation turns.  
COB integrates CST stability signals and provides the identity‑layer substrate consumed by CIL.  
CIL produces the intake packet used by CEx, making COB an upstream context subsystem for Path A.

---

## **2. Scope**  
*(Informative — no SHALL statements)*

This document defines the system_playground version of COB.  
It describes identity‑layer object lifecycle, ordering metrics, stability integration, and the interface between COB, CST, and CIL.  
This document does not redefine the global COB architecture in 20.32; global requirements remain authoritative.

---

## **3. Inputs**  
*(Informative — no SHALL statements)*

### **3.1 CST Signals**  
COB receives stability‑related signals from CST, including drift, oscillation, collapse, merge, split, freeze, thaw, certainty adjustments, ambiguity adjustments, and lineage stability indicators.

### **3.2 Conversation Turn Identity Fragments**  
COB receives identity‑layer fragments extracted from the current turn before IE and before CEx.

---

## **4. Outputs**  
*(Informative — no SHALL statements)*

### **4.1 Identity‑Layer Object Set**  
COB maintains a bounded set of identity‑layer objects containing referent maps, anchors, lineage records, ambiguity indicators, stability metrics, and ordering metrics.

### **4.2 COB → CIL Transfer Block**  
COB provides CIL with stabilized identity‑layer objects, ordering metrics, ambiguity flags, lineage hints, and stability‑adjusted referent maps.  
CIL integrates this into the CIL Intake Packet consumed by CEx.

### **4.3 Conversation‑Level Ordering Metrics**  
COB provides CIL with conversation‑level ordering metrics required for intake packet construction.  
These include:

- total access count  
- chronological ordering vector  
- sliding‑window frequency distribution over the last 10 access events  

---

## **5. Testing (system_playground)**  
*(Tests preserved, corrected, expanded)*

The system_playground version of COB is validated using a block‑level Python testbench (`cob_testbench.py`).  
This testbench verifies deterministic identity‑layer basin behavior and correct CST signal integration.

### **5.1 Tested Behaviors**

- **Bounded Identity Store (HLR‑COB‑001)**  
  - Test ensures COB never exceeds 20 identity‑layer objects.  
  - Eviction removes the lowest‑priority object based on ordering metrics.

- **Deterministic Stability Integration (HLR‑COB‑002)**  
  - Test verifies deterministic application of CST drift, oscillation, collapse, freeze, thaw, certainty adjustments, ambiguity adjustments, and lineage stability indicators.

- **Referential Integrity (HLR‑COB‑003)**  
  - Test ensures referent maps remain structurally consistent across updates, merges, splits, and collapses. Referent‑map integrity includes deterministic structural compression as defined in HLR‑COB‑024.
  - Test verifies referent‑map integrity after structural compression.

- **Ordering Metrics (HLR‑COB‑004)**  
  - Test verifies recency, frequency, and density metrics are preserved and aggregated correctly.

- **Ambiguity Tracking (HLR‑COB‑005)**  
  - Test ensures ambiguity and certainty indicators update deterministically.

- **Lineage Stability (HLR‑COB‑006)**  
  - Test verifies lineage stability indicators are preserved and aggregated.

- **Deterministic Replay (HLR‑COB‑007)**  
  - Test ensures identical CST signals and identical COB snapshots produce identical updates.

- **CIL Compatibility (HLR‑COB‑008)**  
  - Test ensures COB output matches the CIL Intake Packet schema.

- **Eviction Policy (HLR‑COB‑009)**  
  - Test ensures eviction selects the lowest‑priority object.

- **Freeze/Thaw Compliance (HLR‑COB‑010)**  
  - Test ensures frozen objects remain unchanged until thawed.

- **New Context Creation Signal (HLR‑COB‑010A)**
  - Test verifies COB accepts new_context_required=True from CST‑MS.
  - Test verifies COB creates a new identity‑layer object in the same turn.
  - Test verifies COB evolves the new object using current OuBA fragments.
  - Test verifies COB does not evolve the previous identity object when the signal is True.
  - Test verifies deterministic replay: identical CST‑MS signals produce identical COB state snapshots.

- **Conversation Access Count (HLR‑COB‑011)**  
  - Test verifies access count increments deterministically.

- **Conversation Access Order (HLR‑COB‑012)**  
  - Test verifies chronological ordering vector updates deterministically.

- **Sliding‑Window Frequency (HLR‑COB‑013)**  
  - Test verifies correct computation of sliding‑window frequency over last 10 accesses.

- **Referent‑Map Structural Compression (HLR‑COB‑024)**  
  - Test verifies deterministic structural compression of referent maps after updates, merges, and splits.  
  - Test ensures exact duplicate referent entries are removed.  
  - Test ensures referent entries whose token sets are strict subsets of other entries are removed.  
  - Test verifies compression preserves referent‑map integrity and lineage continuity.  
  - Test ensures compression operates strictly on token‑set structure without semantic interpretation.  
  - Test verifies deterministic replay of compression behavior.

- **Merge/Split Structural Propagation and Post‑Compression (HLR‑COB‑025)**  
  - Test verifies MERGE structurally embeds each parent’s semantic fields before compression.  
  - Test verifies SPLIT duplicates all semantic fields structurally into each child before compression.  
  - Test ensures compression occurs only after structural embedding or duplication.  
  - Test verifies compression does not modify semantic fields except through structural compression rules.  
  - Test ensures deterministic replay of merge/split propagation and post‑compression behavior.

**HLR‑COB‑014**  
COB SHALL apply CST merge and split signals deterministically, preserving referent‑map integrity, lineage continuity, and ordering metrics, and SHALL NOT perform semantic reconstruction of identity‑layer fields. COB SHALL perform structural compression after merge and split operations as defined in HLR‑COB‑024 and SHALL NOT treat compression as semantic reconstruction.

- For **MERGE**, COB SHALL:
  - preserve each parent’s referent map, anchors, ambiguity, and stability metrics structurally in the merged child;  
  - combine ordering metrics using deterministic, non‑semantic rules;  
  - record MERGE events in `TP.lineage_log[]` with explicit parent and child references.

- For **SPLIT**, COB SHALL:
  - copy all semantic fields (referent map, anchors, ambiguity, stability metrics, ordering metrics) from the parent to each child;  
  - avoid any semantic partitioning or probabilistic splitting of fields;  
  - record SPLIT events in `TP.lineage_log[]` with explicit parent and child references.

### **5.1.1 Merge/Split Difficulty and TS‑Correct Solution**  
*(Informative — clarifies rationale behind HLR‑COB‑014)*  

Merge and split at the identity‑layer are structurally simple but semantically dangerous.  
Naïve implementations tend to:

- average anchors  
- union referent lists  
- invent lineage history strings  
- reset stability metrics  
- reinterpret ambiguity  

All of these behaviors violate TS constraints on determinism, referent‑map integrity, and non‑semantic handling of identity‑layer fields.

To avoid semantic reconstruction while still honoring CST merge/split commands, COB in system_playground adopts the following TS‑correct solution:

- **MERGE (structural only):**  
  - COB SHALL preserve *both* parents’ semantic fields structurally.  
  - `referent_map` for the merged child SHALL contain a structural embedding of each parent’s referent map (e.g., a `parents{}` sub‑structure keyed by parent id).  
  - `anchors`, `ambiguity`, and `stability_metrics` for the merged child SHALL preserve each parent’s values structurally, without averaging, unioning, or reinterpretation.  
  - `ordering_metrics` for the merged child SHALL be combined using deterministic, non‑semantic rules (e.g., max of recency/frequency/density).  

- **SPLIT (structural only):**  
  - COB SHALL copy *all* semantic fields from the parent object to *each* child object.  
  - `referent_map`, `anchors`, `ambiguity`, `stability_metrics`, and `ordering_metrics` SHALL be duplicated, not partitioned, and SHALL NOT be modified semantically at split time.  
  - Subsequent CST/COB cycles MAY prune or differentiate children over time based on drift, oscillation, collapse, and turn‑level identity fragments, but SPLIT itself SHALL NOT perform semantic partitioning.

This behavior is validated in `cob_testbench_merge_split.py`, which asserts:

- merged children structurally embed both parents’ semantics;  
- split children receive full semantic copies;  
- replay of identical CST merge/split signals produces identical COB state, lineage_log, and cob_state_snapshot.

**Structural Compression After Merge/Split (Informative)**  
After structural embedding (MERGE) or structural duplication (SPLIT), COB applies a deterministic structural compression step.  
Compression removes duplicate referent entries and removes referent entries whose token sets are strict subsets of other entries.  
Compression is structural, deterministic, and non‑semantic, and therefore does not violate the prohibition on semantic reconstruction.

### **Next‑Turn Context Integration Tests**

- **Next‑Turn Context Ingestion (HLR‑COB‑015)**  
- **Next‑Turn Context Validation (HLR‑COB‑016)**  
- **Next‑Turn Context Merge (HLR‑COB‑017)**  
- **Next‑Turn Context Importance Update (HLR‑COB‑018)**  
- **Next‑Turn Context Exposure to CIL (HLR‑COB‑019)**  
- **Deterministic Replay of Next‑Turn Context (HLR‑COB‑020)**  
- **Freeze/Thaw Continuity for Next‑Turn Context (HLR‑COB‑021)**  
- **No Field Duplication Rule (HLR‑COB‑022)**  
- **Structural‑Only Handling (HLR‑COB‑023)**

**HLR‑COB‑024**  
COB SHALL apply a deterministic structural compression step to each identity‑layer referent map after updates, merges, and splits.  
Compression SHALL:  
1. remove exact duplicate referent entries;  
2. remove referent entries whose token sets are strict subsets of other referent entries;  
3. preserve referent‑map integrity and lineage continuity;  
4. operate strictly on token‑set structure without semantic interpretation;  
5. maintain deterministic replay behavior.

**HLR‑COB‑025**  
COB SHALL apply deterministic structural propagation of semantic fields during merge and split operations.  
For MERGE, COB SHALL embed each parent’s semantic fields structurally in the merged child before compression.  
For SPLIT, COB SHALL duplicate all semantic fields structurally into each child before compression.  
Compression SHALL occur only after structural embedding or duplication, and SHALL NOT modify semantic fields except through structural compression defined in HLR‑COB‑024.


### **5.2 Behaviors Not Tested**  
*(Informative)*

Multi‑block interactions, multi‑turn replay, and pipeline‑level behavior are reserved for system_simulation.

### **5.3 Testbench Characteristics**  
*(Informative)*

Deterministic, pure block‑level validation mirroring `cob_structures.yaml` and `cob_state.yaml`. The testbench includes deterministic validation of structural compression and post‑merge/split compression behavior.

---

## **6. Consolidated High‑Level Requirements (HLRs)**  
*(All SHALL statements consolidated here; renumbered; new HLRs begin at 021)*

### **Identity Store & Ordering**

**HLR‑COB‑001**  
COB SHALL maintain no more than 20 identity‑layer objects.

**HLR‑COB‑002**  
COB SHALL integrate CST stability signals deterministically.

**HLR‑COB‑003**  
COB SHALL preserve referent‑map integrity across updates, merges, splits, and collapses.

**HLR‑COB‑004**  
COB SHALL maintain recency, frequency, and density ordering metrics.

**HLR‑COB‑009**  
COB SHALL evict the lowest‑priority identity‑layer object when more than 20 objects exist.

### **Ambiguity, Lineage, Stability**

**HLR‑COB‑005**  
COB SHALL track ambiguity indicators for identity‑layer objects.

**HLR‑COB‑006**  
COB SHALL maintain lineage records and stability indicators.

**HLR‑COB‑010**  
COB SHALL respect CST freeze/thaw signals.

### **Determinism & Replay**

**HLR‑COB‑007**  
COB SHALL behave deterministically under replay conditions.

### **CIL Compatibility**

**HLR‑COB‑008**  
COB SHALL produce identity‑layer structures compatible with the CIL Intake Packet schema.

### **Conversation‑Level Ordering Metrics**

**HLR‑COB‑011**  
COB SHALL track total conversation access count.

**HLR‑COB‑012**  
COB SHALL maintain a chronological ordering vector of access events.

**HLR‑COB‑013**  
COB SHALL compute a sliding‑window frequency distribution over the last 10 access events.

### **Merge/Split Structural Operations**

**HLR‑COB‑014**  
COB SHALL apply CST merge and split signals deterministically, preserving referent‑map integrity, lineage continuity, and ordering metrics.

### **Next‑Turn Context Integration (New HLRs begin here)**

**HLR‑COB‑015**  
COB SHALL ingest next‑turn context fields from `TP.next_context{}`.

**HLR‑COB‑016**  
COB SHALL validate next‑turn context fields using stabilized identity‑layer objects.

**HLR‑COB‑017**  
COB SHALL merge validated next‑turn context fields using deterministic continuity rules.

**HLR‑COB‑018**  
COB SHALL update clarifying‑field importance using continuity metrics.

**HLR‑COB‑019**  
COB SHALL expose merged next‑turn context fields to CIL without modification.

**HLR‑COB‑020**  
COB SHALL guarantee deterministic replay of next‑turn context ingestion.

**HLR‑COB‑021**  
COB SHALL preserve next‑turn context fields across freeze/thaw cycles.

**HLR‑COB‑022**  
COB SHALL NOT define next‑turn context field names.

**HLR‑COB‑023**  
COB SHALL treat next‑turn context fields strictly as structural metadata without semantic interpretation.

---

## **7. Lifecycle Rules**  
*(Informative — no SHALL statements)*

Identity‑layer objects are created when new referents or anchors appear.  
Existing objects update using CST signals and new turn data.  
Objects may merge or split based on CST signals.  
Eviction follows ordering metrics.  
Frozen objects remain unchanged until thawed.

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

A special case of determinism applies to merge/split:

- MERGE determinism requires that identical CST merge signals over identical COB state produce merged children with structurally identical embeddings of parent semantics and identical `TP.lineage_log[]` entries.  
- SPLIT determinism requires that identical CST split signals over identical COB state produce children with identical full copies of the parent’s semantic fields and identical `TP.lineage_log[]` entries.

COB SHALL rely only on structural, non‑semantic rules for merge/split, ensuring that no content‑based or random decisions affect identity‑layer continuity.

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

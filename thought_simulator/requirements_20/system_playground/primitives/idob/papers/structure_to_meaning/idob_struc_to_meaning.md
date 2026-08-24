# **IdOB Structure‑to‑Meaning Architecture**  
*A deterministic, replay‑safe mapping from structural geometry to meaning‑layer semantics*

---

## **1. Purpose**  
IdOB is the Thought Simulator’s **structure→meaning bridge**.  
Upstream OBs (SOB → SROB → CnOB → SmOB → SSG → STPX → RB) produce **pure structural geometry**   [Current page](citation-section://1147006296/3).  
Downstream OBs (OuBA → TR) consume **meaning‑layer semantics**   [Current page](citation-section://1147006296/4).

This paper defines:

- the structural hash contract required from upstream OBs,  
- the meaning‑layer architecture IdOB must use,  
- the structure→meaning mapping layer,  
- the IdOB object definition,  
- the unified depth/parallel search schema,  
- the meaning stabilization rules,  
- the conversational identity envelope refinement,  
- the stopping conditions for meaning resolution,  
- the handoff rules to OuBA.   [Current page](citation-section://1147006296/5)

This document is normative for IdOB implementation.   [Current page](citation-section://1147006296/6)

---

## **2. Architectural Boundary**

### **Upstream OBs**  
- Produce **structure only**. Never encode meaning.   [Current page](citation-section://1147006296/7)  
- Must provide stable, deterministic structural geometry and structural hashes.  

### **IdOB**  
- Consumes structure.  
- Produces meaning.  
- Maintains the **Conversational Identity Envelope (CIE)**.  
- Performs meaning refinement.  
- Stops when meaning is stable or search budget exhausted.   [Current page](citation-section://1147006296/9)  

### **Downstream OBs**  
- Consume meaning.  
- Perform truth/belief evaluation.  
- Produce final output.   [Current page](citation-section://1147006296/9)

---

## **3. Structural Hash Contract (Upstream Responsibility)**  
Upstream OBs must provide the following decomposed structural geometry:  
semantic_field_id, semantic_role_id, semantic_object_id, gradient_id, universe_id, subfield_id.  
Plus the composite structural hash:  

$$
h_{\text{struct}} = H(field \mid role \mid object \mid gradient \mid universe \mid subfield)
$$

And:  
- residue_hash  
- routing_signature.struct_hash  
- routing_signature.feature_hashes  
- identity metadata (adjacent, not baked into hash)   [Current page](citation-section://1147006296/10)

Required properties: stable, replay‑safe, collision‑bounded, meaning‑agnostic, identity‑adjacent.  
Upstream OBs already satisfy these constraints.   [Current page](citation-section://1147006296/11)

---

## **4. Lexical Meaning Dictionary (External Source)**  
IdOB consumes meaning from the lexical meaning dictionary, whose entries contain: lemma, gloss, primitive, invariants, cue envelopes, routing signatures, identity anchors.   [Current page](citation-section://1147006296/12)

IdOB digests this into meaning units, meaning groups, meaning dimensions, meaning cues, meaning invariants, meaning triggers, meaning suppressors.   [Current page](citation-section://1147006296/13)

---

## **5. Meaning‑Layer Architecture (IdOB Responsibility)**  
IdOB organizes lexical meaning into:  
- **Meaning Units**  
- **Meaning Groups**  
- **Meaning Dimensions**  
- **Meaning Cues**  
- **Meaning Invariants**  
- **Meaning Triggers/Suppressors**  
- **Meaning‑Layer Feature Layout**   [Current page](citation-section://1147006296/14)

---

## **6. Structure→Meaning Mapping Layer**  
IdOB maintains:

```yaml
struct_to_meaning_map:
  <structural_hash>:
    - meaning_group_id_1
    - meaning_group_id_2
    - meaning_group_id_3
```

Ranking influenced by:  
- conversational identity envelope,  
- cue_envelope,  
- routing_signature,  
- decomposed structural geometry,  
- meaning invariants,  
- triggers/suppressors.   [Current page](citation-section://1147006296/21)

Properties: one‑way, non‑intrusive, extensible, testable.   [Current page](citation-section://1147006296/22)

---

## **7. IdOB Object Definition**  
An IdOB object contains structural fields, meaning fields, identity fields, and search control fields.  
These fields allow **CvThP** (Conversational Thread Processor) to coordinate parallel IdOB work.  
(Original text referenced “CTP”; updated to CvThP.)   [Current page](citation-section://1147006296/24)

---

## **8. Unified Search Schema (Depth = Parallel Budget)**  
IdOB depth and parallelism are unified:

> **IdOB search budget = total number of IdOB passes allowed per TP segment.**   [Current page](citation-section://1147006296/25)

Each pass may be:

- a recursive refinement cycle, or  
- a parallel meaning‑candidate evaluation.   [Current page](citation-section://1147006296/26)

### **Why the budget is 4–6**  
IdOB meaning resolution has five phases:  
coarse → medium → fine → identity‑conditioned refinement → stabilization.  
Parallel candidates consume additional budget.  
Thus the correct operational range is **4–6 cycles**.   [Current page](citation-section://1147006296/28)

### **Budget Fields**  
- idob_search_budget_max (default: 6)  
- idob_search_budget_min (default: 4)  
- idob_search_budget_used  

### **CvThP Coordination (Updated)**  
Original text: “CTP schedules parallel IdOB branches…”   [Current page](citation-section://1147006296/28)  
Updated:

> **CvThP schedules parallel IdOB branches, enforces search budget, prunes unstable branches, and ensures TS responsiveness.**

---

## **9. Meaning Refinement Process**  
Cycle steps:  
- read structural geometry,  
- retrieve meaning_group candidates,  
- rank using conversational identity envelope + cue_envelope,  
- select meaning_group_id,  
- compute meaning_semantics[],  
- compute meaning_delta_h,  
- update conversational identity envelope,  
- increment search budget,  
- check stopping conditions.   [Current page](citation-section://1147006296/29)

---

## **10. Meaning Stabilization**  
Meaning is stable when:

$$
|\Delta h_{\text{meaning}}| < \varepsilon_{\text{meaning}}
$$

Identity envelope must also stabilize.  
If meaning is not stable, IdOB performs another refinement cycle (budget permitting).   [Current page](citation-section://1147006296/32)

---

## **11. Stopping Conditions**  
IdOB stops when any of the following are true:

1. meaning stabilized,  
2. identity envelope stable,  
3. no better meaning candidate,  
4. budget exhausted,  
5. **CvThP signals time exhaustion** (updated from “CTP”).   [Current page](citation-section://1147006296/38)

When stopped: meaning_semantics[] frozen, identity envelope finalized, meaning_resolution_status set.   [Current page](citation-section://1147006296/39)

---

## **12. Handoff to OuBA**  
IdOB writes meaning_semantics[], idob_semantics[], identity envelope, meaning_resolution_status.  
OuBA performs truth/belief evaluation.  
IdOB never performs truth or belief.   [Current page](citation-section://1147006296/40)

---

## **13. Summary**  
This document defines:

- structural hash contract,  
- meaning‑layer architecture,  
- structure→meaning mapping layer,  
- IdOB object definition,  
- unified depth/parallel search schema,  
- meaning stabilization rules,  
- conversational identity envelope refinement,  
- stopping conditions,  
- OuBA handoff rules.   [Current page](citation-section://1147006296/41)

This is the complete architecture required for deterministic, replay‑safe structure→meaning mapping.   [Current page](citation-section://1147006296/42)

---

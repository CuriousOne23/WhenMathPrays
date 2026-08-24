# **IdOB Structure‑to‑Meaning Architecture**  
### *A deterministic, replay‑safe mapping from structural geometry to meaning‑layer semantics*

---

## **1. Purpose**

IdOB is the Thought Simulator’s **structure→meaning bridge**.  
Upstream OBs (SOB → SROB → CnOB → SmOB → SSG → STPX → RB) produce **pure structural geometry**.  
Downstream OBs (OuBA → TR) consume **meaning‑layer semantics**.

This paper defines:

- the **structural hash contract** required from upstream OBs,  
- the **meaning‑layer architecture** IdOB must use,  
- the **mapping layer** that connects structure to meaning,  
- the **IdOB object definition**,  
- the **unified depth/parallel search schema**,  
- the **meaning stabilization rules**,  
- the **identity envelope refinement**,  
- the **stopping conditions** for meaning resolution,  
- the **handoff rules** to OuBA.

This document is normative for IdOB implementation.

---

## **2. Architectural Boundary**

### **Upstream OBs (SOB, SROB, CnOB, SmOB, SSG, STPX, RB)**  
- Produce **structure only**.  
- Never encode meaning.  
- Must provide stable, deterministic structural geometry and structural hashes.

### **IdOB**  
- Consumes structure.  
- Produces meaning.  
- Maintains identity envelope.  
- Performs meaning refinement.  
- Stops when meaning is stable or search budget exhausted.

### **Downstream OBs (OuBA, TR)**  
- Consume meaning.  
- Perform truth/belief evaluation.  
- Produce final output.

---

## **3. Structural Hash Contract (Upstream Responsibility)**

Upstream OBs must provide the following **decomposed structural geometry**:

- `semantic_field_id`  
- `semantic_role_id`  
- `semantic_object_id`  
- `gradient_id`  
- `universe_id`  
- `subfield_id`

Plus the **composite structural hash**:

$$
h_{\text{struct}} = H(\text{field} \,\|\, \text{role} \,\|\, \text{object} \,\|\, \text{gradient} \,\|\, \text{universe} \,\|\, \text{subfield})
$$

And:

- `residue_hash`  
- `routing_signature.struct_hash`  
- `routing_signature.feature_hashes`  
- identity metadata (adjacent, not baked into hash)

### **Required properties**

- **Stable:** same structure → same hash  
- **Replay‑safe:** deterministic across runs  
- **Collision‑bounded:** collisions rare and monitored  
- **Meaning‑agnostic:** upstream never encodes meaning  
- **Identity‑adjacent:** identity metadata separate from structural hash  

This contract is acceptable to SOB, SROB, CnOB, SmOB, and RB because:

- It does not change their responsibilities.  
- It does not require meaning awareness.  
- It does not require new routing logic.  
- It only requires stable structural hashing, which they already perform.

---

## **4. Lexical Meaning Dictionary (External Source)**

IdOB consumes meaning from the lexical meaning dictionary, whose entries contain:

- `lemma`  
- `gloss`  
- `primitive`  
- `invariant.core_features`  
- `invariant.tags`  
- `cue_envelope.feature_cues`  
- `cue_envelope.tag_cues`  
- `routing_signature`  
- `identity_anchor`

This dictionary is **too large and too ungrouped** to be used directly.  
IdOB must digest it into:

- **meaning units**  
- **meaning groups**  
- **meaning dimensions**  
- **meaning cues**  
- **meaning invariants**  
- **meaning triggers**  
- **meaning suppressors**

This digestion is performed once at startup.

---

## **5. Meaning‑Layer Architecture (IdOB Responsibility)**

IdOB must organize lexical meaning into:

### **Meaning Units**  
Atomic meaning elements derived from lexical entries.

### **Meaning Groups**  
Clusters of meaning units aligned with structural geometry.

### **Meaning Dimensions**  
Axes along which meaning_delta_h is computed.

### **Meaning Cues**  
Identity‑conditioned meaning signals.

### **Meaning Invariants**  
Stable meaning features across cycles.

### **Meaning Triggers / Suppressors**  
Features that increase or decrease meaning_delta_h.

### **Meaning‑Layer Feature Layout**  
The vector IdOB uses to encode meaning_semantics[].

---

## **6. Structure→Meaning Mapping Layer**

IdOB must maintain a **bridge dictionary**:

```yaml
struct_to_meaning_map:
  <structural_hash>:
    - meaning_group_id_1
    - meaning_group_id_2
    - meaning_group_id_3
```

### **Ranking influenced by:**

- identity envelope  
- cue_envelope  
- routing_signature  
- decomposed structural geometry  
- meaning invariants  
- meaning triggers/suppressors  

### **Properties**

- **One‑way:** upstream OBs never read this.  
- **Non‑intrusive:** upstream OBs unchanged.  
- **Extensible:** new meaning groups can be added without touching upstream.  
- **Testable:** progressive_lineup_testing can assert mapping stability.

---

## **7. IdOB Object Definition**

An IdOB object contains:

### **Structural Fields**
- structural_hash  
- semantic_field_id  
- semantic_role_id  
- semantic_object_id  
- gradient_id  
- universe_id  
- subfield_id  
- residue_hash  
- routing_signature  
- identity metadata (from TP)

### **Meaning Fields**
- meaning_group_id  
- meaning_group_candidates[]  
- meaning_semantics[]  
- idob_semantics[]  
- meaning_delta_h  
- meaning_resolution_status

### **Identity Fields**
- identity_importance  
- identity_envelope (updated each cycle)

### **Search Control Fields**
- idob_search_budget_max  
- idob_search_budget_used  
- idob_search_mode  
- idob_search_history[]  

These fields allow CTP to coordinate parallel IdOB work.

---

## **8. Unified Search Schema (Depth = Parallel Budget)**

IdOB depth and parallelism are unified:

> **IdOB search budget = total number of IdOB passes allowed per TP segment.**

Each pass may be:

- a recursive refinement cycle, or  
- a parallel meaning candidate evaluation.

### **Why the budget is 4–6 (not 3–5)**

IdOB meaning resolution has **five phases**:

1. **Coarse meaning group selection**  
2. **Medium meaning group narrowing**  
3. **Fine meaning group selection**  
4. **Identity‑conditioned meaning refinement**  
5. **Meaning_delta_h stabilization**

Parallel candidates consume additional budget.

Thus the correct operational range is:

> **4–6 cycles**  
> (bounded, deterministic, replay‑safe)

### **Budget fields**

- `idob_search_budget_max` (default: 6)  
- `idob_search_budget_min` (default: 4)  
- `idob_search_budget_used` (incremented each pass)

### **CTP coordination**

CTP:

- schedules parallel IdOB branches,  
- stops spawning new work when budget exhausted,  
- ensures TS responsiveness.

---

## **9. Meaning Refinement Process**

### **Cycle Steps**

1. Read structural geometry + hashes.  
2. Retrieve meaning_group candidates from struct_to_meaning_map.  
3. Rank candidates using identity envelope + cue_envelope.  
4. Select meaning_group_id.  
5. Compute meaning_semantics[].  
6. Compute meaning_delta_h.  
7. Update identity envelope.  
8. Increment search budget.  
9. Check stopping conditions.

---

## **10. Meaning Stabilization**

Meaning is considered stable when:

$$
|\Delta h_{\text{meaning}}| < \varepsilon_{\text{meaning}}
$$

Identity envelope must also stabilize:

- no new high‑importance cues,  
- identity_importance converged.

If meaning is not stable, IdOB performs another refinement cycle (budget permitting).

---

## **11. Stopping Conditions**

IdOB stops meaning refinement when **any** of the following are true:

### **1. Meaning stabilized**
$$
|\Delta h_{\text{meaning}}| < \varepsilon_{\text{meaning}}
$$

### **2. Identity envelope stable**
No new high‑importance cues.

### **3. No better meaning candidate**
Search space exhausted or pruned.

### **4. Budget exhausted**
`idob_search_budget_used >= idob_search_budget_max`

### **5. Global TS time/budget pressure**
CTP signals time exhaustion.

When stopped:

- meaning_semantics[] is frozen,  
- idob_semantics[] finalized,  
- identity envelope finalized,  
- meaning_resolution_status set to `"stable"` or `"budget_exhausted"`.

---

## **12. Handoff to OuBA**

IdOB writes:

- meaning_semantics[]  
- idob_semantics[]  
- identity envelope  
- meaning_resolution_status  

Then OuBA performs:

- truth evaluation  
- belief evaluation  
- output generation

IdOB never performs truth or belief.

---

## **13. Summary**

This document defines:

- the structural hash contract,  
- the meaning‑layer architecture,  
- the structure→meaning mapping layer,  
- the IdOB object definition,  
- the unified depth/parallel search schema,  
- the meaning stabilization rules,  
- the identity envelope refinement,  
- the stopping conditions,  
- the OuBA handoff rules.

This is the complete architecture required for IdOB to perform deterministic, replay‑safe structure→meaning mapping.

---

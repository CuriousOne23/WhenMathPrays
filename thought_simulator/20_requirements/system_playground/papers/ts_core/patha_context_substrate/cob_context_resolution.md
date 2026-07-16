# **cob_context_resolution.md**  
### *Conversation Object Basin — Working Paper v0.1*  
*(Questions first, then highest‑priority proposed answers)*

---

## **0. Purpose**
This working paper defines the open questions and early proposed answers for the **Conversation Object Basin (COB)** — the long‑horizon identity substrate for Path A → Path B continuity.

COB is the keystone block:  
CST measures it, CIL merges with it, CEx extracts from it, and SSRGn regenerates meaning into it.

This paper will grow until the questions saturate, then shrink as answers stabilize and move into formal 20.x requirement documents.

---

# **1. Open Questions for COB (Full Set)**  
*(These are the questions we must answer before COB can be implemented.)*

---

## **1.1 Identity Layer Model**
- What is the exact schema of an identity layer?  
- What fields must each layer contain (referent map, lineage, strength, ambiguity, timestamps)?  
- Are identity layers a fixed array of 20 slots or dynamic with a hard cap?  
- How is lineage represented (tree, DAG, linked list, versioned history)?  
- How are multi‑word referents represented?  
- How is ambiguity represented inside a layer?  
- How is referent strength/importance stored?  
- How is confidence stored?  
- How are “competing referents” stored?

---

## **1.2 Referent Map Model**
- What is the schema of a referent map entry?  
- How are surface forms stored?  
- How are attributes stored?  
- How are strength/importance scores stored?  
- How are ambiguity scores stored?  
- How are timestamps stored?  
- How are lineage pointers stored?  
- How are multi‑turn referent updates merged?

---

## **1.3 Layer Lifecycle**
- How are new identity layers created?  
- How are layers split?  
- How are layers merged?  
- How are layers weakened?  
- How are layers strengthened?  
- How are layers retired?  
- How does aging/decay work?  
- What happens when all 20 layers are full?  
- What triggers a new layer creation vs. merging into an existing layer?

---

## **1.4 Update Mechanics**
- How does COB ingest new SSRGn meaning?  
- How does COB merge SSRGn referents with existing referent maps?  
- How does COB handle conflicting referents?  
- How does COB handle ambiguous referents?  
- How does COB handle partial referents?  
- How does COB handle referent collapse?  
- How does COB handle referent explosion?  
- How does COB handle multi‑turn referent drift?

---

## **1.5 Determinism & Replay**
- How is COB state replayed deterministically?  
- How are identity layer IDs stabilized?  
- How are referent map IDs stabilized?  
- How are lineage markers stabilized?  
- How are updates ordered deterministically?  
- How are merge/split operations made deterministic?  
- How are decay operations made deterministic?  
- How are timestamps normalized for replay?

---

## **1.6 Interaction with CST**
- What COB fields does CST read?  
- What COB fields does CST write?  
- How does COB acknowledge CST signals?  
- How does COB reject CST signals?  
- How does COB apply merge/split signals?  
- How does COB apply weaken/strengthen signals?  
- How does COB apply freeze/unfreeze signals?  
- How does COB maintain determinism under CST correction?

---

## **1.7 Interaction with CIL**
- What COB fields does CIL read?  
- How does CIL merge short‑term cues with COB identity layers?  
- How does CIL handle ambiguous COB layers?  
- How does CIL handle conflicting COB layers?  
- How does CIL handle partial COB layers?  
- How does CIL produce flags based on COB state?

---

## **1.8 Interaction with CEx**
- What COB fields does CEx read?  
- How does CEx use referent maps?  
- How does CEx use lineage?  
- How does CEx use strength/importance?  
- How does CEx handle ambiguous referents?  
- How does CEx handle multi‑turn referents?

---

## **1.9 Interaction with SSRGn**
- What SSRGn fields does COB ingest?  
- How does COB merge regenerated meaning?  
- How does COB handle regenerated ambiguity?  
- How does COB handle regenerated structure?  
- How does COB handle regenerated referents?  
- How does COB handle regenerated lineage?

---

## **1.10 Collapse & Recovery**
- What constitutes identity collapse?  
- What constitutes referent collapse?  
- What constitutes lineage collapse?  
- What constitutes continuity collapse?  
- What emergency signals exist?  
- How does COB recover from collapse?  
- How does COB prevent collapse?  
- How does COB detect collapse early?

---

## **1.11 Resource Constraints**
- Maximum referents per identity layer?  
- Maximum ambiguity entries per referent?  
- Maximum lineage depth?  
- Maximum strength/importance resolution?  
- Maximum number of updates per turn?  
- Maximum number of merges per turn?  
- Maximum number of splits per turn?

---

# **2. Highest‑Priority Questions (Must Answer First)**  
*(These unlock all other COB, CST, CIL, CEx, SSRGn design.)*

These are the **keystone questions** — the ones we must answer before anything else.

---

## **2.1 What is the exact schema of an identity layer?**  
This is the single most important question.

Everything depends on it:

- CST metrics  
- CIL merge logic  
- CEx extraction  
- SSRGn regeneration  
- temporal ordering  
- snapshot strategy  
- collapse/recovery  

**Proposed direction (early answer):**

An identity layer should contain:

```
{
  layer_id: stable deterministic ID,
  referent_map: { ... },
  lineage: { ... },
  strength: float,
  importance: float,
  ambiguity: { ... },
  timestamps: { created, updated },
  decay_state: float
}
```

This is a *proposal*, not a final answer.

---

## **2.2 What is the schema of a referent map entry?**  
This is the second most important question.

CIL, CEx, and SSRGn all depend on referent map structure.

**Proposed direction (early answer):**

```
{
  referent_id: stable deterministic ID,
  surface_forms: [ ... ],
  attributes: { ... },
  strength: float,
  confidence: float,
  ambiguity: float,
  lineage_pointer: ID,
  timestamps: { created, updated }
}
```

Again: proposal, not final.

---

## **2.3 How does COB merge new SSRGn meaning?**  
This is the third keystone question.

If merge logic is undefined, continuity collapses.

**Proposed direction (early answer):**

- Merge by referent_id  
- Strength‑weighted averaging  
- Ambiguity‑weighted conflict resolution  
- Timestamp‑weighted decay  
- Deterministic ordering of merge operations  

---

## **2.4 How does COB split identity layers?**  
This is the fourth keystone question.

Split logic is required for:

- ambiguity resolution  
- drift correction  
- collapse prevention  

**Proposed direction (early answer):**

Split when:

- ambiguity > threshold  
- referent clusters diverge  
- CST signals “split”  

---

## **2.5 How does COB maintain deterministic replay?**  
This is the fifth keystone question.

Replay safety is required for:

- CST drift detection  
- CIL merging  
- CEx extraction  
- SSRGn regeneration  

**Proposed direction (early answer):**

- deterministic IDs  
- deterministic ordering  
- deterministic merge/split rules  
- deterministic decay  
- deterministic timestamps (normalized)  

---

# **3. Next Steps**
1. Review the keystone questions (2.1–2.5).  
2. Decide which proposed directions should be expanded first.  
3. Begin drafting the next version of this paper with partial answers.  
4. Extract stable answers into formal 20.x requirement documents.  

---
- expand any of the proposed answers  
- generate diagrams  
- generate a merge/split algorithm  
- generate a referent map schema  
- generate a deterministic replay model  

Just tell me which part you want to deepen next.

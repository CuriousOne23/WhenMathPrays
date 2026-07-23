**questions_for_cob_substrate.md**  
**COB Substrate — Operational Questions** (Working Paper v0.4)

### 0. Purpose
This working paper collects all operational questions that must be answered before the Conversation Object Basin (COB) can be fully specified.  

COB is the keystone of the TS context layer. Once COB is solid, CST, CIL, CEx, SSRGn, temporal ordering, snapshot strategy, and collapse/recovery become straightforward.

This paper will shrink as answers stabilize.

### 1. Core Operational Questions (Highest Priority)

**Identity Layer Model**
- What is the exact schema of an identity layer?
- What fields must each layer contain (referent map, lineage, strength, ambiguity, timestamps, decay state)?
- Fixed array of 20 slots or dynamic with a hard cap?
- How is lineage represented (tree, DAG, linked list, versioned history)?
- How are multi-word referents and competing referents represented?

**Referent Map Model**
- Exact schema of a referent map entry?
- How are surface forms, attributes, strength, confidence, ambiguity, and lineage pointers stored?
- How are multi-turn referent updates merged?

**Layer Lifecycle & Capacity**
- How are new layers created, split, merged, weakened, strengthened, or retired?
- Aging/decay policy?
- What happens when all 20 layers are occupied or when a new distinct identity appears?

**Update Mechanics**
- How does COB ingest and merge new SSRGn meaning?
- Rules for conflict resolution between new meaning and existing layers?
- How does COB handle ambiguous, partial, or conflicting referents?
- How does COB handle referent explosion or collapse?

### 2. Supporting Operational Questions

**Determinism & Replay**
- How is the full COB state replayed deterministically from the SSRGn sequence?
- How are layer IDs, referent IDs, and snapshots versioned for auditability?
- How are merge/split/decay operations made deterministic?

**Interaction with CST**
- What COB fields does CST read?
- What signals does CST send and how are they applied or rejected?
- How does COB maintain determinism under CST corrections?

**Interaction with CIL**
- What COB fields does CIL read?
- How does CIL merge short-term cues with COB identity layers?
- How does CIL handle ambiguous or conflicting COB layers?

**Interaction with CEx**
- What COB fields does CEx read?
- How does CEx use referent maps, lineage, and strength/importance?

**Interaction with SSRGn & Path B**
- What SSRGn fields does COB ingest?
- How does COB merge regenerated meaning, ambiguity, and structure?
- What COB information is relevant to Path B (via CoHI or other mechanisms)?

**Collapse & Recovery**
- What constitutes identity collapse, referent collapse, lineage collapse, or continuity collapse?
- What emergency signals exist?
- How does COB detect and recover from collapse?

**Resource Constraints & Scaling**
- Maximum referents per identity layer?
- Maximum ambiguity entries, lineage depth, or updates per turn?
- How do we prevent memory blow-up across long sessions?

### 3. Additional Operational Questions (System-Identified)

**Timing & Turn Integration**
- When exactly does COB update during a turn?
- Is COB updated once per turn or multiple times?
- Does COB update synchronously or asynchronously with CST signals?
- Does COB produce a stable snapshot each turn?

**Merge / Split / Pruning Behavior**
- How does COB handle partial, contradictory, or noisy updates?
- What operational threshold triggers a split?
- How does COB split a layer without losing continuity?
- What information is pruned or compressed?
- How does COB summarize lineage instead of storing full history?

**Assignment & Eviction**
- What is the operational algorithm for assigning new information to a layer?
- What similarity metrics are used?
- What is the eviction policy when the 21st conversation appears?
- Do we evict the weakest, oldest, or least-used?
- Can CST override eviction decisions?

**Failure Modes**
- How does COB detect identity collapse, referent collapse, lineage collapse, or continuity collapse?
- How does COB recover from collapse?

### 4. Next Steps
- Confirm that the COB question surface is now saturated.
- Begin answering the keystone questions in `cob_context_resolution.md`.
- Extract stable answers into formal 20.x requirement documents.
- Shrink this paper as answers accumulate.

---

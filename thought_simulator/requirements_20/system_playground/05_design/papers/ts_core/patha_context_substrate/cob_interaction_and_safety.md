**cob_interaction_and_safety.md**  
**Conversation Object Basin — Interaction & Safety Resolution** (Working Draft v0.2)

### 0. Purpose
This paper resolves the interaction, safety, and cross-block behavior of the Conversation Object Basin (COB).

All questions for COB are maintained separately in:
`questions_for_cob_substrate.md` (v0.4)

This paper builds directly on:
- `cob_context_resolution.md` (identity & referent model, merge/split logic, deterministic replay)
- `cob_lifecycle_and_capacity.md` (creation, assignment, eviction, decay, pruning, compression)

It defines how COB interacts with CST, CIL, CEx, and SSRGn while maintaining stability, determinism, and safety.

### 1. Interaction Overview
COB is the long-horizon identity substrate. It interacts with four major blocks:
- **CST** — stabilizes COB via drift detection and correction signals.
- **CIL** — merges short-term cues into COB.
- **CEx** — extracts identity information from COB.
- **SSRGn** — regenerates meaning that COB ingests.

This paper defines COB’s behavior during these interactions. Expectations placed on the other blocks are defined in separate interface papers.

### 2. COB Interaction with CST (Resolution)

**2.1 CST Signals to COB**
CST may send:
- split_signal
- merge_signal
- weaken_signal / strengthen_signal
- freeze_signal / thaw_signal
- retire_signal
- ambiguity_signal / drift_signal

**2.2 COB Response Rules**
- Split/merge: Trigger deterministic split/merge algorithms (see core resolution paper).
- Weaken/strengthen: Adjust strength/importance using deterministic scaling; update decay_state.
- Freeze/thaw: Freeze halts merges, splits, pruning, decay, and assignment. Thaw replays queued updates deterministically.
- Retire: Archive lineage and remove layer deterministically.
- Ambiguity/drift: Increase ambiguity penalties and adjust assignment thresholds.

**2.3 Safety Rules**
- CST cannot delete lineage.
- CST cannot reorder layers arbitrarily.
- CST cannot modify referent attributes directly.
- All corrections must be replay-safe and logged.
- COB must reject or queue invalid signals.

### 3. COB Interaction with CIL (Resolution)

**3.1 CIL Inputs to COB**
- Short-term referent cues
- Short-term attribute updates
- Short-term ambiguity signals
- Short-term lineage hints
- Short-term strength/importance adjustments

**3.2 COB Response Rules**
- Integrate using deterministic merge logic, referent similarity, lineage continuity, ambiguity penalties, and decay adjustments.

**3.3 Safety Rules**
- CIL cannot force layer creation or deletion.
- CIL cannot override CST signals.
- CIL updates must be idempotent and replay-safe.

### 4. COB Interaction with CEx (Resolution)

**4.1 CEx Reads from COB**
- Referent maps
- Lineage
- Strength/importance
- Ambiguity
- Decay_state
- Timestamps
- Ordering

**4.2 CEx Must Not Modify**
- Referent maps, lineage, strength/importance, ambiguity, decay_state, ordering, layers.

**4.3 Safety Rules**
- CEx reads must be deterministic.
- CEx must not read frozen layers unless explicitly allowed.
- CEx must not trigger merge/split, eviction, or retirement.

### 5. COB Interaction with SSRGn (Resolution)

**5.1 SSRGn Inputs to COB**
- Regenerated referents
- Regenerated attributes
- Regenerated ambiguity
- Regenerated lineage hints
- Regenerated structure
- Regenerated confidence scores

**5.2 COB Response Rules**
- Ingest using deterministic merge logic, assignment algorithm, ambiguity penalties, lineage continuity, and decay adjustments.

**5.3 Safety Rules**
- SSRGn cannot force layer creation or deletion.
- SSRGn cannot override CST signals.
- SSRGn packets must be ordered deterministically.
- SSRGn must not modify lineage directly.

### 6. Freeze/Thaw Mechanism (Resolution)

**6.1 Freeze Conditions**
- CST freeze_signal
- Collapse detection
- High ambiguity or lineage risk
- Multi-turn reasoning requiring stability

**6.2 Freeze Behavior**
- Halt merges, splits, pruning, decay, assignment.
- Log incoming updates for later replay.

**6.3 Thaw Behavior**
- Replay queued updates deterministically.
- Apply merges/splits if needed.
- Resume normal lifecycle.

### 7. Collapse Detection & Recovery (Resolution)

**7.1 Collapse Types**
- Identity collapse
- Referent collapse
- Lineage collapse
- Continuity collapse

**7.2 Detection**
- Ambiguity thresholds
- Drift thresholds
- Lineage discontinuity
- CST signals
- SSRGn/CIL conflict signals

**7.3 Recovery Algorithm**
1. Freeze COB.
2. Identify collapse type.
3. Apply deterministic recovery (split, merge, prune, retire, reassign).
4. Thaw COB.
5. Resume deterministic replay.

### 8. Next Steps
- Draft interface contracts (`cob_expectations_for_cst.md`, `cob_interface_to_ssrgn.md`, `cob_interface_to_cex.md`).
- Begin extracting stable answers into formal 20.x requirement documents.
- Shrink this paper as answers stabilize.

---

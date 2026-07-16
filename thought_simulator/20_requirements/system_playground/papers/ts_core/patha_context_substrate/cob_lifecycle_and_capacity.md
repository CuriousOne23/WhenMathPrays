**cob_lifecycle_and_capacity.md**  
**Conversation Object Basin — Lifecycle & Capacity Resolution** (Working Draft v0.2)

### 0. Purpose
This paper resolves the lifecycle, assignment, eviction, decay, pruning, compression, and capacity behaviors of the Conversation Object Basin (COB).

All questions for COB are maintained separately in:
`questions_for_cob_substrate.md` (v0.4)

This paper does not repeat those questions. It builds directly on `cob_context_resolution.md` (core identity & referent model) and precedes `cob_interaction_and_safety.md`.

### 1. Lifecycle Overview
COB maintains up to 20 identity layers representing long-horizon conversational identities. Lifecycle resolution defines how layers are created, assigned, merged/split, decayed, pruned, evicted, and retired — all deterministically and within bounded resources.

### 2. Layer Creation (Resolution)

**2.1 Creation Conditions**
A new identity layer is created when:
- Incoming referents do not match any existing layer above similarity threshold.
- Lineage continuity cannot be established.
- Ambiguity in all candidate layers exceeds threshold.
- CST issues a “new identity” signal.
- Referent cluster analysis indicates a distinct identity domain.

**2.2 Creation Algorithm**
1. Compute similarity between incoming referents and existing layers.
2. If all similarity scores < creation threshold → create new layer.
3. Assign stable `layer_id`.
4. Initialize strength, importance, ambiguity, decay_state.
5. Initialize lineage with a new root node.
6. Insert into deterministic ordering structure.

### 3. Assignment of New Information (Resolution)

**3.1 Assignment Inputs**
- Referent similarity
- Lineage continuity
- Strength / importance
- Ambiguity penalties
- CST override signals
- Decay state (lower decay = more active)

**3.2 Assignment Algorithm**
1. Compute similarity score for each layer:
   ```math
   score = w1·referent_similarity + w2·lineage_continuity + w3·strength - w4·ambiguity
   ```
2. Apply CST overrides (if any).
3. Select highest-score layer if score ≥ assignment threshold.
4. Otherwise → trigger new layer creation.

**3.3 Multi-Layer Assignment**
If multiple layers exceed threshold:
- Choose highest score.
- Record secondary candidates for ambiguity tracking.
- CST may later merge or split based on drift signals.

### 4. Eviction Policy (Resolution)

COB maintains a maximum of 20 layers.

**4.1 Eviction Score**
```math
eviction_score = w1·(low strength) + w2·(low importance) + w3·(high decay_state) + w4·(low recency) + w5·(high ambiguity)
```
Lower score = more likely to be evicted.

**4.2 Eviction Algorithm**
1. Compute eviction score for all layers.
2. Select lowest-score layer.
3. If ambiguity is high → attempt merge before eviction.
4. If CST issues override → follow CST.
5. Evict layer deterministically.
6. Rebalance ordering.

**4.3 Eviction Notes**
- Eviction is deterministic across replay.
- Eviction never deletes lineage; lineage is archived.
- Eviction may trigger decay acceleration in remaining layers.

### 5. Decay Model (Resolution)

Decay ensures COB does not grow unbounded and stale identities weaken over time.

**5.1 Decay Inputs**
- Time since last update
- Strength / importance / ambiguity
- Recency
- CST drift signals

**5.2 Decay Algorithm**
Applied each turn:
```math
decay_state = decay_state + β · time_since_update
strength = strength × (1 - γ · decay_state)
importance = importance × (1 - γ · decay_state)
```

**5.3 Decay Effects**
- High decay → lower assignment likelihood
- High decay → higher eviction likelihood
- High decay → triggers pruning or retirement

### 6. Pruning & Compression (Resolution)

**6.1 Pruning Rules**
Prune when:
- Referent count exceeds limit
- Ambiguity exceeds threshold
- Decay state exceeds threshold
- Lineage depth exceeds limit

**6.2 Pruning Algorithm**
1. Sort referents by strength, confidence, recency.
2. Remove lowest-value referents.
3. Compress attributes (drop low-confidence fields).
4. Summarize lineage (collapse older nodes).
5. Normalize ordering.

**6.3 Compression Rules**
- Collapse repeated surface forms.
- Merge low-confidence attributes.
- Summarize lineage into checkpoints.
- Reduce ambiguity entries to top-k conflicts.

### 7. Size Control (Resolution)

COB must remain bounded in:
- Number of layers (≤20)
- Referents per layer
- Lineage depth
- Ambiguity entries
- Update operations per turn

**7.1 Size Control Mechanisms**
- Decay
- Pruning
- Compression
- Eviction
- Merge/split
- CST drift correction

**7.2 Deterministic Size Control**
All size control operations must be deterministic, replay-safe, ordering-stable, and lineage-consistent.

### 8. Retirement (Resolution)

**8.1 Retirement Conditions**
- Decay state exceeds retirement threshold
- Strength and importance both below minimum
- CST issues retirement signal
- Referent map collapses
- Lineage continuity breaks irrecoverably

**8.2 Retirement Algorithm**
1. Archive lineage.
2. Remove layer deterministically.
3. Rebalance ordering.
4. Update decay_state of remaining layers.

### 9. Next Steps
- Draft `cob_interaction_and_safety.md` (CST/CIL/CEx/SSRGn interactions, collapse detection, recovery, freeze/thaw).
- Begin extracting stable answers into formal 20.x requirement documents.
- Shrink this paper as answers stabilize.

---

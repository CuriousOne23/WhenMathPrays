**cst_deterministic_replay.md**  
**Context Stability Theory — Deterministic Replay** (Working Draft v0.2)

### 0. Purpose
This paper defines how CST guarantees deterministic replay of all stability operations across the context substrate (COB + CIL + SSRGn).

Deterministic replay means that identical inputs, regeneration, cue packets, metric values, thresholds, and signals produce identical CST signals and therefore identical COB state.

This paper complements the stability metrics paper and the COB papers.

### 1. Deterministic Replay Overview
CST is responsible for ensuring the entire Path A substrate is replay-safe.

Replay safety means the system must reconstruct the same identity layers, referent maps, lineage, ambiguity, relevance, and stability signals given the same sequence of inputs.

CST achieves this through:
- Deterministic metric computation
- Deterministic threshold evaluation
- Deterministic signal emission and ordering
- Deterministic freeze/thaw behavior
- Deterministic collapse recovery
- Deterministic logging

CST never modifies COB directly. Replay safety is achieved entirely through signals.

### 2. Deterministic Metric Computation
CST must compute all stability metrics deterministically:
- Identity drift
- Referent drift
- Lineage drift
- Referent / attribute / structural / identity ambiguity
- Lineage / identity continuity
- Collapse scores
- Strength / importance stability
- Decay progression

**Inputs**: Stabilized COB state, CIL cue packets, SSRGn packets, previous CST signals, deterministic thresholds.

**Forbidden**: Stochastic sampling, randomization, nondeterministic ordering, external state, time-dependent heuristics.

### 3. Deterministic Threshold Evaluation
Thresholds must be deterministic, replay-safe, monotonic, and stable across turns/sessions.

No stochastic thresholds or adaptive behavior that depends on external state or timing.

### 4. Deterministic Signal Emission
CST emits signals only when metrics cross thresholds.

Signal emission must be deterministic, ordered, replay-safe, and idempotent.

**Signal Ordering** (deterministic):
1. Collapse signals
2. Freeze/thaw signals
3. Structural signals (split/merge/retire)
4. Ambiguity/drift signals
5. Relevance signals (weaken/strengthen)

This ordering ensures collapse is handled first, stability is restored before structural changes, etc.

### 5. Deterministic Freeze/Thaw Behavior

**Freeze**
- Halt merges, splits, pruning, decay, assignment
- Queue incoming updates
- Log all signals

**Thaw**
- Replay queued updates deterministically
- Apply merges/splits if needed
- Resume normal lifecycle

Freeze/thaw must produce identical results under replay.

### 6. Deterministic Collapse Recovery

**Collapse Types**
- Identity collapse
- Referent collapse
- Lineage collapse
- Continuity collapse

**Recovery Algorithm**
1. Freeze COB
2. Identify collapse type
3. Apply deterministic recovery (split, merge, prune, retire, reassign)
4. Thaw COB
5. Resume deterministic replay

Recovery must never use stochastic heuristics or modify lineage/referent maps directly.

### 7. Deterministic Logging
CST must log:
- All metric values
- All threshold evaluations
- All signals
- All signal ordering
- All freeze/thaw events
- All collapse recovery events

Logs must be complete, ordered, deterministic, and replay-safe.

### 8. Replay Guarantees
CST guarantees that:
- Identical inputs → identical metrics
- Identical metrics → identical thresholds
- Identical thresholds → identical signals
- Identical signals → identical COB state
- Identical COB state → identical downstream extraction

Replay must reconstruct the same 20 identity layers, referent maps, lineage, ambiguity, relevance, decay, and stability signals.

### 9. Next Steps
- Draft `cst_threshold_calibration.md` (if needed).
- Begin extracting stable answers into formal 20.x requirement documents.
- Shrink this paper as answers stabilize.

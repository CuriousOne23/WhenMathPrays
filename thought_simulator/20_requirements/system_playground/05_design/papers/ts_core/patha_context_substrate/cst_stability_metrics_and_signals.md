**cst_stability_metrics_and_signals.md**  
**Context Stability Theory — Stability Metrics & Signals** (Working Draft v0.2)

### 0. Purpose
This paper defines the stability metrics CST computes and the signals CST emits to maintain long-horizon identity stability across the context substrate (COB + CIL + SSRGn).

All questions for CST are maintained separately in the question substrate.

This paper complements the COB papers and precedes CST’s deterministic replay paper.

### 1. CST Stability Overview
CST is the stability layer for Path A. Its responsibilities:
- Detect drift, ambiguity, lineage discontinuity, referent conflict, and collapse
- Compute stability metrics
- Emit corrective signals
- Ensure deterministic replay

CST never modifies COB directly. It acts only through signals.

### 2. Stability Metrics (Resolution)

**2.1 Drift Metrics**
- **Identity Drift**: Divergence between expected identity trajectory and current referent/lineage state.
- **Referent Drift**: Movement of referent clusters over time.
- **Lineage Drift**: Discontinuity or branching in lineage.

**2.2 Ambiguity Metrics**
- Referent Ambiguity
- Attribute Ambiguity
- Structural Ambiguity
- Identity Ambiguity (weighted sum)

**2.3 Continuity Metrics**
- Lineage Continuity
- Identity Continuity

**2.4 Collapse Metrics**
- identity_collapse_score
- referent_collapse_score
- lineage_collapse_score
- continuity_collapse_score

**2.5 Relevance & Decay Metrics**
- Strength Stability
- Importance Stability
- Decay Progress

All metrics are deterministic, replay-safe, and computed each turn.

### 3. CST Thresholds (Resolution)
CST uses deterministic thresholds for all metrics (drift, ambiguity, continuity, collapse, retirement, freeze/thaw).

Thresholds must be:
- Deterministic
- Replay-safe
- Monotonic
- Stable across turns/sessions
- Never stochastic

### 4. CST Signals (Resolution)

**Structural Signals**
- split_signal
- merge_signal
- retire_signal

**Strength/Importance Signals**
- weaken_signal
- strengthen_signal

**Stability Signals**
- freeze_signal
- thaw_signal

**Ambiguity & Drift Signals**
- ambiguity_signal
- drift_signal

**Collapse Signals**
- identity_collapse_signal, etc.

### 5. Signal Semantics (Resolution)

Each signal has deterministic semantics and triggers specific COB actions (see COB papers):
- Split/merge: Run deterministic algorithms.
- Weaken/strengthen: Adjust relevance deterministically.
- Freeze/thaw: Halt/resume lifecycle operations.
- Retire: Archive lineage and remove layer.
- Ambiguity/drift: Adjust thresholds and penalties.
- Collapse: Enter recovery mode.

### 6. Deterministic Replay Requirements
CST must ensure:
- Metric computation is deterministic
- Threshold evaluation is deterministic
- Signal emission and ordering is deterministic
- Replay produces identical signals

CST must log all signals for replay.

### 7. Safety Requirements
CST must never:
- Modify COB directly
- Modify referent maps or lineage
- Modify timestamps or decay_state
- Reorder layers
- Delete referents (except via retire_signal)

CST must always:
- Preserve determinism
- Preserve continuity
- Preserve ordering
- Preserve replay safety
- Limit correction frequency/magnitude to avoid oscillation

### 8. Next Steps
- Draft `cst_deterministic_replay.md`.
- Begin extracting stable answers into formal 20.x requirement documents.
- Shrink this paper as answers stabilize.

---

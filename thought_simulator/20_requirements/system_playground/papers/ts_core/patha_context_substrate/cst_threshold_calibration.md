**cst_threshold_calibration.md**  
**Context Stability Theory — Threshold Calibration** (Working Draft v0.2)

### 0. Purpose
This paper defines how CST calibrates, maintains, and applies deterministic thresholds for all stability metrics across the context substrate (COB + CIL + SSRGn).

Threshold calibration ensures that drift, ambiguity, continuity, collapse, relevance, and decay are evaluated consistently, producing deterministic CST signals and therefore deterministic COB state.

This paper complements the metrics, signals, and replay papers.

### 1. Threshold Calibration Overview
CST uses thresholds to decide when stability metrics require corrective action.

Thresholds must be:
- Deterministic
- Replay-safe
- Monotonic
- Stable across turns and sessions
- Independent of external state or timing
- Never stochastic

### 2. Threshold Types

**Drift Thresholds**
- identity_drift_threshold
- referent_drift_threshold
- lineage_drift_threshold

**Ambiguity Thresholds**
- referent_ambiguity_threshold
- attribute_ambiguity_threshold
- structural_ambiguity_threshold
- identity_ambiguity_threshold

**Continuity Thresholds**
- lineage_continuity_threshold
- identity_continuity_threshold

**Collapse Thresholds**
- identity_collapse_threshold, etc.

**Lifecycle Thresholds**
- retirement_threshold
- decay_threshold

**Stability Thresholds**
- freeze_threshold
- thaw_threshold

**Relevance Thresholds**
- strength_stability_threshold
- importance_stability_threshold

### 3. Threshold Calibration Inputs
Calibration must depend only on:
- Stabilized COB state
- Previous CST signals
- Previous threshold values
- Deterministic metric history
- Bounded relevance and decay values

**Forbidden Inputs**
- Stochastic sampling
- Randomization
- External state
- Wall-clock time
- Nondeterministic ordering
- Regeneration or CIL variability

### 4. Threshold Calibration Rules

**Monotonicity**
Thresholds must change only in monotonic, bounded ways (e.g., tightening as identity stabilizes).

**Bounded Adjustment**
Thresholds must remain within fixed min/max bounds.

**Replay-Safe Adjustment**
Threshold adjustments must produce identical values under replay.

**No Oscillation**
Thresholds must not oscillate (tighten → relax → tighten) unless driven by deterministic state transitions.

**No Cascading Adjustments**
Threshold changes must not trigger further threshold changes.

### 5. Threshold Calibration Algorithms
CST uses deterministic algorithms to update thresholds, for example:

- Drift thresholds: function of previous threshold + drift history
- Ambiguity thresholds: function of previous threshold + ambiguity history
- Continuity thresholds: function of previous threshold + continuity history
- Collapse thresholds: function of previous threshold + collapse history
- Freeze/thaw thresholds: function of previous threshold + collapse and recovery history

All functions must be deterministic and replay-safe.

### 6. Threshold Application Rules
Thresholds determine when CST emits signals, for example:
- If drift > drift_threshold → emit drift_signal
- If identity_drift > identity_drift_threshold → emit split_signal
- If ambiguity > ambiguity_threshold → emit ambiguity_signal
- If collapse_score > collapse_threshold → emit collapse_signal

### 7. Deterministic Replay Requirements
Threshold calibration must be replay-safe:
- Identical metric history → identical thresholds
- Identical thresholds → identical signals
- Identical signals → identical COB state

Threshold logs must be complete, ordered, deterministic, and replay-safe.

### 8. Safety Requirements
CST must never:
- Use stochastic threshold updates
- Use external state or nondeterministic ordering
- Modify COB directly

CST must always:
- Preserve determinism
- Preserve continuity
- Preserve ordering
- Preserve replay safety

### 9. Next Steps
- Draft `cst_signal_ordering.md` (if needed).
- Begin extracting stable answers into formal 20.x requirement documents.
- Shrink this paper as answers stabilize.

---

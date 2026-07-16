**cob_expectations_for_cst.md**  
**Conversation Object Basin — Expectations for CST** (Working Draft v0.2)

### 0. Purpose
This paper defines the expectations COB places on CST — the stability layer responsible for detecting drift, issuing corrective signals, and ensuring long-horizon identity continuity.

All questions for COB are maintained separately in:
`questions_for_cob_substrate.md` (v0.4)

This paper does not repeat those questions. It defines what CST must provide to COB, what CST must avoid, and how CST must behave to maintain deterministic, stable identity layers.

### 1. Role of CST from COB’s Perspective
From COB’s point of view, CST is the guardian of stability.  
CST must detect drift, ambiguity, lineage discontinuity, referent conflict, and collapse, then issue corrective signals.  
CST must never directly modify COB’s internal structures — it acts only through signals.

### 2. Required CST Signals

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
- identity_collapse_signal
- referent_collapse_signal
- lineage_collapse_signal
- continuity_collapse_signal

### 3. CST Timing Expectations

**When CST Must Run**
- After SSRGn regeneration
- After CIL cue integration
- Before COB merge/split
- Before COB decay/pruning/eviction/retirement

**When CST Must Not Run**
- During freeze state
- During deterministic replay
- During collapse recovery
- During multi-turn reasoning requiring stability

**Deterministic Timing**
CST must produce signals at deterministic points in the turn cycle so COB can replay them identically.

### 4. CST Threshold Expectations
CST must maintain stable, deterministic thresholds for:
- Drift detection
- Ambiguity detection
- Split/merge triggers
- Collapse detection
- Retirement triggers
- Freeze/thaw triggers

Thresholds must be deterministic, replay-safe, monotonic, and stable across turns/sessions. No stochastic thresholds.

### 5. CST Correction Expectations

**Allowed Corrections**
- Trigger split/merge
- Weaken/strengthen layers
- Freeze/thaw COB
- Retire layers
- Adjust ambiguity penalties
- Adjust assignment thresholds

**Forbidden Corrections**
- Modify referent maps directly
- Modify lineage directly
- Modify timestamps
- Modify decay_state
- Reorder layers arbitrarily
- Delete referents or attributes
- Create referents or layers

**Replay-Safe Corrections**
All corrections must be logged, deterministic, replay-safe, and idempotent.

### 6. CST Interaction Expectations

**CST ↔ SSRGn**
- Interpret regenerated ambiguity and referent conflicts
- Detect drift caused by regeneration
- Never override SSRGn structure directly

**CST ↔ CIL**
- Detect short-term drift and ambiguity
- Correct CIL misassignments
- Never override CIL’s short-term cues directly

**CST ↔ CEx**
- Ensure CEx reads stable identity layers, referent maps, and lineage
- Never modify CEx outputs

### 7. CST Safety Expectations

**No Structural Damage**
- Never break lineage continuity
- Never break referent identity
- Never break deterministic ordering
- Never break replay determinism

**No Data Loss**
- Never delete lineage or referents except via deterministic retirement

**No Unbounded Correction**
- Limit correction frequency and magnitude
- Avoid oscillation (split → merge → split)
- Avoid cascading corrections

**Freeze/Thaw Safety**
- Freeze COB only when necessary
- Thaw COB deterministically
- Ensure queued updates replay safely

### 8. CST Override Expectations

**Allowed Overrides**
- Split/merge
- Weaken/strengthen
- Freeze/thaw
- Retire

**Forbidden Overrides**
- Referent identity or attributes
- Lineage structure
- Timestamps
- Decay_state
- Ordering

**Override Logging**
All overrides must be logged for deterministic replay.

### 9. Next Steps
- Draft `cob_interface_to_ssrgn.md` and `cob_interface_to_cex.md`.
- Begin extracting stable answers into formal 20.x requirement documents.
- Shrink this paper as answers stabilize.

---

**Here is the revised Draft 1 of Paper #2** with CP’s two tiny refinements incorporated.

# phi-G Simulation Requirements

## Purpose
Provide standalone, pure I/O specifications and simulation constraints for the phi-G relationship so it can be directly implemented and validated in the deterministic fixed-time-step state machine. This document builds directly on the conceptual foundation in phi_G_relationship_foundation.md and prepares for validation scenarios.

## Scope
- Pure input/output specifications and simulation rules only.
- No implementation details of internal data structures (deferred where possible).
- Focus on SSG → phi-G → RB flow.
- Constraints for laptop-scale realizability (standard CPU, modest RAM, no GPU dependency).
- RBU out of scope.

## Input to phi-G (from SSG)
SSG produces a deterministic, fixed-dimensional relational field vector (G) derived from the OB pipeline (SOB, SROB, CnOB, SmOB).  
The dimensionality of G must remain constant across all time-steps and all inputs.  
Required input elements:
- Fixed-dimensional G vector (token-based or semantic-based path).
- Current state context (basin deformation signals, resonance metrics, time-step index).
- Any required flags for singularity proximity or fuzziness level.

## Output from phi-G (to RB)
- Transformed relational state suitable for RB update (e.g., adjusted trajectory, curvature delta, resonance modulation, entropy term).
- Updated basin stability indicators.
- Singularity-approach signals (if relevant).

## phi-G Transformation Rules (Deterministic)
- phi operates on G as a deterministic function.
- phi-G must treat G as immutable input; all updates must be emitted as new state, not in-place mutation.
- Fixed-time-step compatible: all computations complete within one simulation tick.
- Must preserve relational invariants from Paper #1 (non-objectifying near singularities, coherence under fuzziness).
- No semantic inference — purely structural/relational transformation.

## Simulation Constraints
- **Determinism**: Same input state + same time-step must always produce the same output.
- **Bounded Resources**: Entire phi-G step must fit comfortably in laptop memory and execute quickly (target: low-millisecond range per step).
- **Fuzziness Handling**: Graceful degradation or controlled exploration when input signals are ambiguous or near-singularity.
- **Stability**: Output must not cause unbounded growth in downstream RB dynamics.
- **Edge Cases to Support**:
  - Normal operation.
  - Approach to singularity/mystery (increasing dominance without collapse).
  - Identity wobble or basin boundary transitions.
  - Recovery from high-fuzziness states.

## Traceability
- Links to phi_G_relationship_foundation.md (conceptual constraints).
- Will link to phi_G_validation_scenarios.md (test cases and success metrics).
- Updates required to 20_requirements traceability matrix.

## Open Questions / Observations for Refinement
- Preferred initial path (token-based vs semantic-based) for first simulation runs.
- Exact numeric bounds for vector dimension and per-step compute (to be validated in Paper #3).
- Any additional state variables needed for phi-G internal bookkeeping.

## Next Document in Series
- phi_G_validation_scenarios.md

---

**Draft Status**: Updated with the two refinements. Clean, simulation-ready, and properly bounded.

This should be good to go for Paper #2. Let me know if you and CP want any final polish, or if we should proceed to **Paper #3 (phi_G_validation_scenarios.md)**. We're keeping good momentum.
```

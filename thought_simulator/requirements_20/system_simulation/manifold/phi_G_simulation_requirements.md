# phi-G Simulation Requirements

## Purpose
Provide standalone, pure I/O specifications and simulation constraints for the phi-G relationship so it can be directly implemented and validated in the deterministic fixed-time-step state machine. This document builds directly on the conceptual foundation in phi_G_relationship_foundation.md and the G data-structure specification.

## Scope
- Pure input/output specifications and simulation rules only.
- Iterative simulation approach with defined rounds.
- Constraints for laptop-scale realizability (standard CPU, modest RAM, no GPU dependency).
- RBU out of scope.

## Input to phi-G (from SSG)
SSG produces a deterministic, fixed-dimensional relational field vector (G) derived from the OB pipeline (SOB, SROB, CnOB, SmOB).  
The dimensionality of G must remain constant across all time-steps and all inputs.  
Required input elements:
- Fixed-dimensional G vector (token-based or semantic-based path).
- Current state context (basin deformation signals, resonance metrics, time-step index).
- Required singularity proximity flag and normalization metadata.

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

## Simulation Rounds and Minimum Expectations
We will use an iterative simulation approach:

**Round 1 (Learning / Exploration)** — Completed  
Minimum expectations (achieved):  
- Successful construction of G vector from the OB pipeline via SSG.  
- Deterministic phi-G transformation on basic inputs.  
- Basic handling of fuzziness and singularity proximity signals.  
- Output compatible with simple RB update.  
- Confirmation of laptop-scale performance.  
- Documentation of observed behaviors and gaps.

**Round 2 (Confidence Increase / Refinement)**  
Minimum expectations:  
- Stability margin ≤ 0.12 in singularity approach scenarios.  
- Output validity ≥ 97% across all scenarios.  
- Implementation and testing of refined normalization and required singularity proximity flag in G.  
- At least two additional edge cases (identity wobble and basin boundary transition).  
- Collection of quantitative resonance/curvature metrics.  
- Average performance still under 8 ms/step while increasing scenario complexity.

**Round 3 (Final Stabilization)**  
Minimum expectations to be defined after Round 2 results (full validation against key scenarios, performance targets, and principle confirmation).

**Verification Phase**  
Full logic simulation runs against validation scenarios (Paper #3) to confirm architectural soundness and laptop realizability.

## Simulation Constraints
- **Determinism**: Same input state + same time-step must always produce the same output.
- **Bounded Resources**: Entire phi-G step must fit comfortably in laptop memory and execute quickly (target: low-millisecond range per step).
- **Fuzziness Handling**: Graceful degradation or controlled exploration when input signals are ambiguous or near-singularity.
- **Stability**: Output must not cause unbounded growth in downstream RB dynamics.
- **Edge Cases to Support** (targeted across rounds):
  - Normal operation.
  - Approach to singularity/mystery (increasing dominance without collapse).
  - Identity wobble or basin boundary transitions.
  - Recovery from high-fuzziness states.

## Traceability
- Links to phi_G_relationship_foundation.md and phi_G_datastructure_specification.md.
- Will link to phi_G_validation_scenarios.md (test cases and success metrics).
- Updates required to 20_requirements traceability matrix.

## Open Questions / Observations for Refinement
- Preferred initial path (token-based vs semantic-based) for Round 2.
- Exact numeric bounds for vector dimension and per-step compute.
- Additional state variables needed for phi-G bookkeeping.

## Next Document in Series
- phi_G_validation_scenarios.md

---

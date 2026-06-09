# 40.130_gb_prototypes / requirements_delta.md

**Last Updated:** 2026-06-04  
**Status:** Phase B - 3-Tier Iteration

## Flows Alignment Statement

- **Forward Flow (20-series)**: Driven by core guidance in 20.10 (supervisory separation), 20.16 (responsibility matrix), 20.17 (messy input), and 20.18 (failure modes).
- **Backward Flow (40-series evidence)**: The initial flat prototype demonstrated basic drift/oscillation detection but surfaced risks of overload, mixed timescales, and verification difficulty.
- **Iterative Design Flow (50-series influence)**: Incorporates the minimal 3-tier hierarchy (Signal Monitors → Supervisory Integrator → Boundary Enforcer) defined in 50.36.

**Agreement Statement**: The three flows are aligned. The 50-series hierarchy directly addresses the overload and clarity risks identified in the 20-series and observed in the first version of this prototype, while preserving all core invariants.

---

## Summary
This file tracks how the GB prototype aligns with and explores the 20-series guidance, with explicit HLR traceability.

## Key 20-Series Guidance Being Explored

| 20-Series Document | HLR References                        | Key Guidance / SHALL                              | Status in This Prototype      | Notes |
|--------------------|---------------------------------------|---------------------------------------------------|-------------------------------|-------|
| **20.10**          | HLR-20.010-018 to HLR-20.010-026    | GB as non-mutating supervisory layer             | Strong                        | 3-tier structure enforces it |
| **20.16**          | HLR-20.016-001 to HLR-20.016-015    | GB Responsibility Matrix                          | Good                          | Implemented via Integrator |
| **20.17**          | HLR-20.017-001 to HLR-20.017-006    | Messy / contradictory input handling              | Good                          | ContradictionMonitor added |
| **20.18**          | HLR-20.018-001 to HLR-20.018-006    | Failure modes & success criteria                  | Good                          | Drift & oscillation detection |

## Requirements Delta Summary

**Strongly Demonstrated:**
- Supervisory-only behavior (no semantic mutation)
- Deterministic decision making with reason codes
- Detection of high ΔH% drift, oscillation, and high IB population

**Partially Demonstrated:**
- Nuanced supervisory action selection
- Long-term stability under sustained load

**Not Covered in this Prototype:**
- Full IB lifecycle supervision
- Learned component oversight

## Open Questions / Gaps for 10-series
- Exact thresholds for triggering supervisory actions
- Final taxonomy and priority of reason codes
- Formal definition of safe-boundary operations

# 40.36_gb_prototypes / requirements_delta.md

**Last Updated:** 2026-06-04  
**Status:** Phase B - In Progress

## Summary
This file tracks how the GB prototype aligns with and explores the 20-series guidance, with explicit HLR traceability.

## Key 20-Series Guidance Being Explored

| 20-Series Document       | HLR References                          | Key Guidance / SHALL                                      | Status in This Prototype      | Notes |
|--------------------------|-----------------------------------------|-----------------------------------------------------------|-------------------------------|-------|
| **20.10**                | HLR-20.010-018 to HLR-20.010-026      | GB as non-mutating supervisory layer only                | Fully Implemented            | Core constraint enforced |
| **20.10**                | HLR-20.010-011, HLR-20.010-040        | Determinism, auditability, replayability                 | Fully Implemented            | Reason codes + history |
| **20.10**                | HLR-20.010-099 to HLR-20.010-108      | Risk mitigation (GB overload, messy input, etc.)         | In Progress                  | Being actively explored |
| **20.16**                | HLR-20.016-001 to HLR-20.016-015      | GB Responsibility Matrix                                  | Partially Implemented        | Core actions covered |
| **20.17**                | HLR-20.017-001 to HLR-20.017-006      | Messy / contradictory input handling                      | In Progress                  | Dedicated test scenario |
| **20.18**                | HLR-20.018-001 to HLR-20.018-006      | Failure modes & success criteria                          | In Progress                  | Drift, oscillation, overload |
| **20.80**                | GB Component Requirements              | General GB responsibilities                               | Partially Implemented        | Supervisory loop focus |

## Requirements Delta (What This Prototype Addresses)

**Strongly Covered:**
- HLR-20.010-018 ~ HLR-20.010-026: Supervisory-only behavior (no meaning mutation)
- HLR-20.010-011, HLR-20.010-040: Deterministic logging and reason codes
- HLR-20.016-001 ~ HLR-20.016-009: Core supervisory duties (drift detection, population control, etc.)

**Partially Covered / Under Exploration:**
- HLR-20.017-001 ~ HLR-20.017-006: Messy input and contradiction handling
- HLR-20.018-001 ~ HLR-20.018-006: Failure mode detection (drift vs oscillation)
- HLR-20.016-002, HLR-20.016-032: Coherence & stability monitoring

**Not in Scope for this Prototype:**
- Full learned component validation
- Production performance tuning
- Human oversight escalation UI

## Open Questions / Gaps for 10-series

- Exact deterministic thresholds for supervisory actions (e.g., when to Dampen vs Slow)
- Final taxonomy and priority ordering of supervisory reason codes
- Precise rules for IB promotion / retirement under sustained load
- Formal definition of "safe boundary" operations
- Optimal intervention frequency targets

## Evidence Status
- Prototype demonstrates basic supervisory loop and decision making.
- Harness and verification capsule provide reproducible evidence.
- Further exploration in Phase B will continue to surface ambiguities for the 10-series.

---
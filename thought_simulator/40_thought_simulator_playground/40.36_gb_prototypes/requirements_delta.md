# 40.36_gb_prototypes / requirements_delta.md

**Last Updated:** 2026-06-04  
**Status:** Phase B - In Progress

## Summary
This file tracks the mapping between 20-series guidance (with HLR numbers) and what this GB prototype is implementing/exploring.

## Key 20-Series Guidance Being Explored

| 20-Series Document | HLR Reference | Key Guidance / SHALL | Status in This Prototype | Notes |
|--------------------|---------------|----------------------|--------------------------|-------|
| **20.10** | HLR-20.010-018 to HLR-20.010-026 | GB as non-mutating supervisory layer only | Fully Implemented | Enforced in prototype.py |
| **20.10** | HLR-20.010-011, HLR-20.010-040 | Determinism, auditability, replayability | Fully Implemented | Full history + reason codes |
| **20.16** | HLR-20.016-001 to HLR-20.016-015 | GB Responsibility Matrix | Partially Implemented | Core supervisory actions covered |
| **20.17** | HLR-20.017-001 to HLR-20.017-006 | Messy / contradictory input handling | In Progress | Harness includes messy_input scenario |
| **20.18** | HLR-20.018-001 to HLR-20.018-006 | Failure modes & success criteria | In Progress | Oscillation, overload, drift detection |
| **20.80** | (GB Component Requirements) | GB component responsibilities | Partially Implemented | Focus on supervisory loop |

## Requirements Delta (What This Prototype Addresses)

**Strongly Covered:**
- HLR-20.010-018 ~ HLR-20.010-026: Supervisory-only role (no direct mutation)
- HLR-20.010-011, HLR-20.010-040: Deterministic decisions with reason codes
- HLR-20.016-001 ~ HLR-20.016-009: Core supervisory responsibilities

**Partially Covered / To Be Expanded:**
- HLR-20.017-001 ~ HLR-20.017-006: Messy input handling
- HLR-20.018-001 ~ HLR-20.018-006: Failure mode detection
- HLR-20.016-002, HLR-20.016-032: ΔH% drift and oscillation detection

**Not in Scope for this Prototype:**
- Full learned component oversight
- Production performance optimizations
- Human oversight UI flows

## Open Questions for 10-series
- Exact thresholds for supervisory actions (e.g., when to Dampen vs Slow)
- Final taxonomy and priority of supervisory reason codes
- Precise rules for IB promotion/retirement under high load
- Formal definition of "safe boundary" operations

---
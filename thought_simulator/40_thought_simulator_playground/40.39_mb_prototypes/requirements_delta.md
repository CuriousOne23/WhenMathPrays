# 40.39_mb_prototypes / requirements_delta.md

**Last Updated:** 2026-06-05  
**Status:** Scaffold - Phase A pending

## Flows Alignment Statement

- **Forward Flow (20-series)**: Driven by 20.70 (MB Requirements — 36 HLRs for non-intrusive diagnostics, drift observation, stability reporting, bounded what-if, determinism, telemetry, visibility modes, overflow handling per 20.30 schema).
- **Backward Flow (40-series evidence)**: No evidence collected yet; this is the initial scaffold.
- **Iterative Design Flow (50-series influence)**: Placeholder awaiting 50.39 or integration into logging/observability design (50.80 / 50.05). 50.05 lists MB as .39.

**Agreement Statement**: Scaffold stage only. Alignment will be asserted after Phase A software_description approval and Phase B execution.

---

## Summary
This file will track how the MB prototype aligns with and explores the 20.70 guidance, with explicit HLR traceability.

## Key 20-Series Guidance Being Explored (from 20.70)

| 20-Series Document | HLR References                          | Key Guidance / SHALL                                      | Status in This Prototype | Notes |
|--------------------|-----------------------------------------|-----------------------------------------------------------|--------------------------|-------|
| **20.70**          | HLR-20.070-001 to HLR-20.070-036        | Non-intrusive diagnostics, deterministic drift observation, stability reporting, bounded what-if, telemetry I/O, visibility modes, overflow schema, reproducibility, no core-state mutation | Scaffold                 | Primary |
| **20.30**          | (functional model, overflow §8.3)       | Canonical overflow fields, pipeline placement of MB, determinism invariants | Scaffold                 | Cross-ref |
| **20.10**          | (architectural principles)              | Non-intrusion, supervision boundaries, safe observability | Scaffold                 | Cross-ref |

## Requirements Delta Summary

**Strongly Demonstrated:** (none — scaffold)

**Partially Demonstrated:** (none)

**Not Covered in this Prototype:** (all 36 HLRs — awaiting implementation)

## Open Questions / Gaps for 10-series
- Exact shape of the canonical MB input and output objects (to be explored in Phase B, then promoted)
- Final TCU budgets and visibility mode policies (20.95 / 50-series)
- Precise what-if probe policy gating and interaction with GB
- How MB drift indicators feed IB/GB without creating supervision loops

## Traceability Targets
- thought_simulator/20_requirements/20.70_mb_requirements.md
- thought_simulator/20_requirements/20.30_ts_functional_model.md
- ../40.20_master_program_guide.md
- 50.05_software_spec_construction_guide.md

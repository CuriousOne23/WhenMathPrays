# experiments

## Experiment Log for 40.240 TR Router Prototypes

### Experiment 1: Basic Deterministic Routing (2026-06-03)
- Goal: Validate that identical inputs always produce identical route + delta_h decisions.
- Implementation: 4 hand-crafted test cases in harness (math, thought, general, mixed).
- Result: 4/4 PASS. Route and ΔH% both validated.
- Artifact: artifacts/tr_verification_run_2026-06-03.json
- Observations: Keyword proxy works for this narrow scope. Clean error path for invalid input.

### Experiment 2: ΔH% Consistency Under Variation (2026-06-03)
- Goal: Confirm ΔH% values are fixed per route class and not affected by minor input variations.
- Added: Case with "Explain quantum entanglement mathematically" → still math_basin + 0.15.
- Result: PASS. Values are constant functions of the route decision.

### Planned / Future Experiments (post approval)
- Full semantic TR field population prototype (when driven by 50.37).
- Integration with simulated RB dirty-flag + OB semantic write scenarios.
- GB read-only TR consumption test (supervisory signal generation).
- Determinism across "multiple runs" with explicit nonce if identity is added.
- Messy input handling (per 20.17) for routing stability.
- Split/merge lineage effects on routing_semantics.

## Notes
All experiments must produce artifacts in `artifacts/`.
All scenarios must reference relevant HLRs from 20.10, 20.30, 20.37, 10.10.10, 10.10.50, 10.10.36.
See verification_capsule.md for the canonical run record and evidence.
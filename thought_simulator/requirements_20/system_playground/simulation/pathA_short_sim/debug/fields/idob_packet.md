# idob_packet

## Meaning
Contract-shaped IdOB payload carrying structural key, candidates, selected operation, and readiness flags.

## Shape
- Mapping with deterministic keys
- Includes completion and eligibility indicators

## Produced By
- IdOB

## Debug Checks
- Required keys are present for non-empty inputs.
- selected_candidate_index is valid for available candidates.


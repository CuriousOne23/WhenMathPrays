# IdOB

## Purpose
Construct contract-shaped identity packet and select operation candidates.

## Inputs
- committed_stream
- constraints_matched
- semantic_adjacent_cues

## Outputs
- idob_packet
- idob_complete
- path_b_eligible

## Debug Checks
- Packet contains required contract keys.
- Selection is deterministic for identical signal sets.

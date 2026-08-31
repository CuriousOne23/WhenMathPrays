# 12_reduction — First Conviction Artifact
# Date: 2026-08-31
# Commit: <insert commit hash>

## Per‑rival failed walls

### idob_native
- contaminated: false
- failed: none
- pair checks:
  - P_rock_cie:W4=PASS
- cross notes:
  - R_prior:native_first_cycle=False
- claim: Goal v2 fails for that rival. IdOB shrinks toward naming.

### frame_fill
- contaminated: false
- failed:
  - P_rock_cie:W4
  - R_empty:W2
- pair checks:
  - P_rock_cie:W4=FAIL
- claim: That theory is not a sufficient cheaper operator.

### embed_nn
- contaminated: false
- failed:
  - P_rock_cie:W4
  - R_empty:W2
- pair checks:
  - P_rock_cie:W4=FAIL
- claim: That theory is not a sufficient cheaper operator.

### dict_lookup
- contaminated: false
- failed:
  - P_rock_cie:W1
  - P_rock_cie:W4
  - R_empty:W2
- pair checks:
  - P_rock_cie:W4=FAIL
- claim: That theory is not a sufficient cheaper operator.

## Global claim
Package does work those styles do not. First conviction. Still not a completed necessity theorem.

## Locked verdict table
- IdOB-native fails any wall: Bench broken. Stop. Fix idob.py / fixtures first.
- Rival fails >=1 wall, contaminated false: That theory is not a sufficient cheaper operator.
- Rival passes all walls, contaminated false: Goal v2 fails for that rival. IdOB shrinks toward naming.
- Rival passes only after reading our map: Contaminated. Not a pass. Not a fail. Discard.
- All three cheap rivals fail >=1 wall, uncontaminated: Package does work those styles do not. First conviction. Still not a completed necessity theorem.

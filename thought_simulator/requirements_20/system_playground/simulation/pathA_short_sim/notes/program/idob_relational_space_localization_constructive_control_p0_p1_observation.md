# IdOB Relational-Space Localization Observation (Constructive Control P0/P1)

**Date:** 2026-11-27  
**Status:** Executed characterization observation record (non-normative).  
**Method authority:** [idob_relational_space_localization_constructive_control_p0_p1_proposal.md](idob_relational_space_localization_constructive_control_p0_p1_proposal.md).  
**Mechanical design authority:** [idob_relational_space_localization_constructive_control_p0_p1_design.md](idob_relational_space_localization_constructive_control_p0_p1_design.md).

Review state: **BEING REVIEWED**

## 1) Scope

Executed the frozen constructive-control package only:

- `P0`: exact deterministic structural-information constructive control;
- `P1`: informative-but-nondeterminative structural-information constructive control;
- arms `S0`, `S1`, `S2`;
- frozen permutation-audit presentation variants:
  - identity;
  - entity permutation A;
  - entity permutation B;
  - feature-channel rename.

No natural-structure discovery probe was designed or executed.

## 2) Characterization implementation and evidence

Characterization implementation:

- [idob_relational_space_localization_constructive_control_p0_p1_characterization.py](../../support/tools/idob_relational_space_localization_constructive_control_p0_p1_characterization.py)

Machine-readable evidence artifact:

- `local_characterization/sessions/idob_relational_space_localization_constructive_control_p0_p1/runs/20261127_222033__idob_rel_space_localization_constructive_control_p0_p1.json`

## 3) Underlying-fixture results (identity presentation)

### P0

- `S0`: `48/48 = 100%`
- `S1`: `24/48 = 50%`
- `S2`: `24/48 = 50%`

### P1

- `S0`: `36/48 = 75%`
- `S1`: `24/48 = 50%`
- `S2`: `24/48 = 50%`

## 4) Comparison to frozen analytic expectations

Expected:

| Control | S0 | S1 | S2 |
|---|---:|---:|---:|
| P0 | 48/48 | 24/48 | 24/48 |
| P1 | 36/48 | 24/48 | 24/48 |

Observed underlying-fixture counts exactly matched expected counts for both controls.

## 5) Permutation audit

Permutation variants reproduced the same per-arm outcomes as identity presentation for both controls:

- P0: `S0=48/48`, `S1=24/48`, `S2=24/48` for all four presentation variants.
- P1: `S0=36/48`, `S1=24/48`, `S2=24/48` for all four presentation variants.

Permutation presentations are audit replications, not additional independent evidence beyond the underlying fixture conditions.

## 6) Anti-shortcut audits

Recorded audits include:

- outcome withholding: pass;
- evaluator isolation: pass;
- entity-order-only prediction;
- entity-identity-only prediction;
- feature-channel-name-only prediction;
- output-frequency baseline;
- X-only baseline;
- S2-only shortcut audit;
- fixture-index/seed prediction;
- arm-identity prediction;
- direct evaluator-label leakage: pass;
- indirect evaluator-label leakage: pass;
- S1 ambiguity: pass;
- held-out/permutation generalization.

All non-procedure shortcut baselines in the artifact were at chance-level (`24/48 = 50%`) for both controls under identity/S0 audit measurement.

## 7) Completeness and exact replay

- completeness: pass (`1152/1152` required records present);
- exact replay: pass (record fingerprints reproduced exactly on full second pass).

## 8) Mechanical classification

- `P0`: `CONTROL_VALIDATED`
- `P1`: `CONTROL_VALIDATED`

Package-level bounded summary:

The frozen constructive controls behaved as analytically specified and passed required control contracts within this fixture.

## 9) Explicit boundary statement

**P0 and P1 are constructive controls. Their generative distributions deliberately contain known structural utility. Execution validates the characterization framework and its controls; it does not discover utility in naturally occurring TS structure.**

This observation does not establish:

- a naturally occurring TS localization mechanism;
- localization-source authorization;
- architecture change;
- HOW-2;
- Gate C;
- production integration.

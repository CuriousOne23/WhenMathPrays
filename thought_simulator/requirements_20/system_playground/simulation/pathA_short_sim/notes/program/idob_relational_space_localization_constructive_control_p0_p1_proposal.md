# IdOB Relational-Space Localization Constructive Control P0/P1 Proposal

**Date:** 2026-11-27  
**Status:** Research proposal for controlled discrimination (non-normative).  
**Purpose:** Define a bounded constructive-control phase that validates the characterization framework against two frozen preconstructed structural-information regimes.

Review state: **BEING REVIEWED**

## 1) Scientific distinction (frozen)

P0 and P1 are constructive controls. Their generative distributions are deliberately constructed to contain known structural utility. Execution validates the characterization framework and its controls; it does not discover utility in naturally occurring TS structure.

- **P0:** exact deterministic structural-information constructive control.
- **P1:** informative-but-nondeterminative structural-information constructive control.

Neither control is a natural-structure discovery probe. That research object remains undesigned and unauthorized.

## 2) Program question addressed (bounded)

Functional question:

Can contextual differentiation of relational material improve meaning construction under non-oracle conditions?

This proposal addresses that question only through frozen synthetic controls with strict information boundaries.

## 3) Phase scope and non-authorization boundary

In scope for the P0/P1 package:

- synthetic fixture construction for P0 and P1;
- frozen procedures and perturbation schedules `S0/S1/S2`;
- frozen anti-shortcut audits and expected behavior contracts.

Not authorized by this proposal:

- implementation or execution;
- evidence generation;
- natural-structure discovery probes;
- localization source selection;
- architecture proposal/change;
- HOW-2;
- Gate C;
- production selector work;
- Category/YAML integration.

## 4) Frozen control definitions

### 4.1 P0 (exact deterministic structural-information control)

Latent tuple:

- `U=(P,Q,R)`, with `P,Q,R in {0,1}`.

Opaque structural features:

- `F(Ea)=P xor Q`
- `F(Eb)=Q xor R`
- `F(Ec)=R`

Outcome:

- `O=P xor R`.

Deterministic invariant:

- `F(Ea) xor F(Eb) = O`.

Construction rule:

- compute `d = F(Ea) xor F(Eb)`;
- emit `R_A` if `d=0`;
- emit `R_B` if `d=1`.

If required structural inputs are unavailable/invalid, apply the frozen abstention/fallback rule defined in the mechanical design.

P0 therefore satisfies `S => O` and is an exact deterministic positive control.

Expected `S0` behavior: `48/48 = 100%`.

### 4.2 P1 (informative-but-nondeterminative structural-information control)

Latent tuple and outcome:

- `U=(P,Q)`, `P,Q in {0,1}`;
- `S=P xor Q`;
- `O=P`.

Frozen distribution:

- `P(U=(0,0))=3/8`
- `P(U=(0,1))=1/8`
- `P(U=(1,0))=3/8`
- `P(U=(1,1))=1/8`.

So:

- `P(O=0)=P(O=1)=1/2`.

Non-determinacy:

- `S=0` preimages: `(0,0)` and `(1,1)` include both outcome values;
- `S=1` preimages: `(0,1)` and `(1,0)` include both outcome values;
- therefore `S` does not determine `O` (`S =/> O`).

Informativeness:

- `P(S=0)=1/2`, `P(O=0|S=0)=3/4`;
- `P(S=1)=1/2`, `P(O=0|S=1)=1/4`;
- so `P(O|S=s) != P(O)`.

Frozen P1 rule:

- `S=0 => R_A`
- `S=1 => R_B`.

The procedure must not receive latent tuples, outcomes, correct action labels, oracle answers, answer tables, evaluator outputs, or reversible encodings of these.

Expected `S0` accuracy: `36/48 = 75%`.  
Strongest balanced `S`-blind baseline: `24/48 = 50%`.

## 5) Frozen finite schedule

The P1 schedule is fixed at 48 instances:

- `U=(0,0)`: 18 instances;
- `U=(0,1)`: 6 instances;
- `U=(1,0)`: 18 instances;
- `U=(1,1)`: 6 instances.

This exactly realizes `3/8, 1/8, 3/8, 1/8` and analytically yields `36/48` under the frozen P1 rule in `S0`.

## 6) Frozen perturbation expectations

- **P0:** `S0=48/48`, `S1=24/48`, `S2=24/48`.
- **P1:** `S0=36/48`, `S1=24/48`, `S2=24/48`.

The P0/P1 contrast is intentional and scientifically central.

## 7) Feature-permutation wording (frozen)

Feature-channel identifiers may be renamed or permuted per fixture instance. The canonical structural values consumed by the procedure remain invariant.

Do not swap canonical binary values `{0,1}` under label-permutation wording unless a value-invariant rule is explicitly defined.

## 8) Required anti-shortcut audits (frozen set)

The package preserves requirement for:

- outcome withholding;
- evaluator isolation;
- entity-order-only audit;
- entity-identity-only audit;
- feature-label-only audit;
- output-frequency baseline;
- `X`-only baseline;
- `S2`-only shortcut audit;
- fixture-index/seed audit;
- arm-identity audit;
- direct/indirect evaluator-label leakage audit;
- `S1` ambiguity;
- held-out/permutation generalization;
- deterministic trace;
- exact replay;
- completeness checks.

## 9) Explicit non-claims

- P0 validates the exact/deterministic information case.
- P1 validates the incomplete/informative but nondeterminative case.
- Neither control discovers utility in naturally occurring TS structural information.
- Successful execution would validate the experimental framework's ability to detect two preconstructed regimes only.
- Successful execution would not establish a naturally occurring TS mechanism, localization requirement, or meaning theory.

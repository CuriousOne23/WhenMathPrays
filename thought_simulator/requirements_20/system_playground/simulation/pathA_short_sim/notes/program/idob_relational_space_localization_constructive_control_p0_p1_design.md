# IdOB Relational-Space Localization Constructive Control P0/P1 Design

**Date:** 2026-11-27  
**Status:** Frozen mechanical design for characterization planning (non-normative).  
**Purpose:** Mechanically specify a bounded P0/P1 constructive-control characterization so implementation/execution (if authorized later) requires no new consequential experimental choice.

Review state: **BEING REVIEWED**

## 1) Design objective

Freeze a deterministic characterization that distinguishes:

- structure-sensitive success when informative structure is present;
- collapse to baseline when informative structure is absent or neutralized.

No production source or architecture is selected by this design.

## 2) Scope and non-scope

In scope:

- synthetic fixtures for P0 and P1;
- frozen procedure `I`;
- frozen perturbation schedule `S0/S1/S2`;
- frozen audits, outcomes, and evidence fields.

Out of scope:

- architecture/source authorization;
- HOW-2;
- Gate C;
- production selector;
- Category/YAML integration.

## 3) Common notation and contracts

- outcome space: `O in {0,1}`;
- action space: `R_A` predicts `O=0`, `R_B` predicts `O=1`;
- deterministic fixture id required for every instance;
- deterministic replay required for generators, transforms, and procedure;
- no stochastic branch points in runtime evaluation.

## 4) P0 fixture model (no-structure control)

Latent tuple:

- `U=(P,Q,R)` with `P,Q,R in {0,1}`.

Outcome:

- `O = P xor R`.

Decoy channels:

- `x1 = P xor Q`
- `x2 = Q xor R`

Structural channels:

- `Ea = P`
- `Eb = R`
- `Ec = Q`

Frozen dataset:

- all 8 latent tuples included;
- each tuple repeated 6 times;
- total `48` instances;
- fixture order is lexicographic by `(P,Q,R,repeat_index)`;
- this yields exactly `24` instances with `O=0` and `24` with `O=1`.

## 5) P1 fixture model (single informative structural bit)

Latent tuple:

- `V=(S,N1,N2)` with all bits in `{0,1}`.

Outcome:

- `O=S`.

Decoys (independent of `S` under full enumeration):

- `y1=N1`
- `y2=N2`.

Structural payload:

- `S` is encoded as structural bit `Es`.

Frozen dataset:

- all 8 tuples `(S,N1,N2)` included;
- each tuple repeated 6 times;
- total `48` instances;
- fixture order lexicographic by `(S,N1,N2,repeat_index)`;
- exactly `24` instances with `O=0` and `24` with `O=1`.

## 6) Frozen procedure I

### 6.1 P0 procedure

Inputs consumed by `I`:

- `Ea`, `Eb`.

Rule:

- compute `d = Ea xor Eb`;
- emit `R_A` if `d=0`;
- emit `R_B` if `d=1`.

### 6.2 P1 procedure

Inputs consumed by `I`:

- `Es`.

Rule:

- emit `R_B` if `Es=1`;
- emit `R_A` if `Es=0`.

Procedure boundary:

- `I` must not read outcome labels, ranking, coverage, or any post-hoc performance field.

## 7) Frozen perturbation schedule S0/S1/S2

### 7.1 S0 (unaltered)

- provide the fixture exactly as generated.

### 7.2 S1 (no-structure)

Structural channels are removed before `I`.

Frozen no-structure behavior:

- when required structural inputs are absent, `I` emits fallback action `R_A` deterministically.

No adaptive fallback is permitted.

### 7.3 S2 (neutralized structure)

Principle:

- preserve structural shape and marginals while breaking informative correspondence to outcome.

#### P0 S2 transform

- keep `x1,x2` unchanged;
- set `Ea2 = Q`;
- set `Eb2 = P`;
- set `Ec2 = R`.

This preserves channel shape and balanced marginals while making the decoded bit `Ea2 xor Eb2 = Q xor P`, which is independent of `O = P xor R` under full enumeration.

#### P1 S2 transform

Assign neutralized bit:

- `Es2 = N1` (equivalently decoy channel `y1`).

By full tuple enumeration:

- `P(Es2=1) = 1/2`;
- `P(O=1 | Es2=1) = 1/2`;
- `P(O=1 | Es2=0) = 1/2`.

So `Es2` is balanced and outcome-independent in the finite fixture.

## 8) Information boundaries

Procedure `I` may consume only:

- declared structural channels for the condition;
- fixed channel identifiers;
- frozen deterministic rules.

`I` may not consume:

- latent tuples directly;
- outcome labels;
- evaluation metrics;
- ranking/oracle fields;
- any non-declared auxiliary channel.

## 9) Pre-execution expected behaviors (frozen)

### 9.1 P0 expectations

- `P0-S0`: `48/48` correct.
- `P0-S1`: `24/48` correct (constant `R_A` fallback on balanced outcomes).
- `P0-S2`: `24/48` correct.

### 9.2 P1 expectations

- `P1-S0`: `48/48` correct.
- `P1-S2`: `24/48` correct.
- `P1-S1`: `24/48` correct.

These expectations are frozen reference contracts for execution validation.

## 10) Required audits

The characterization must include and report:

1. fixture balance audit (`O=0`/`O=1` counts per regime);
2. transform audit (S1 removal and S2 mapping reproducibility);
3. replay audit (identical outputs from same frozen inputs);
4. boundary audit (no unauthorized field reads by `I`);
5. expected-behavior contract audit versus Section 9.

## 11) Outcome labels

Per regime outcome:

- `CONTROL_VALIDATED`: observed equals frozen expected;
- `CONTROL_FAILED`: observed differs from frozen expected;
- `INVALID_EXECUTION`: missing required fields or failed determinism/replay contract.

Overall characterization state:

- `VALIDATED_WITHIN_FIXTURE` only if all required regimes are `CONTROL_VALIDATED`;
- else `NOT_VALIDATED_WITHIN_FIXTURE`.

## 12) Evidence schema requirements

Each reported regime record must include:

- `phase_id` (`P0` or `P1`);
- `regime_id` (`S0`,`S1`,`S2`);
- `fixture_size`;
- `correct_count`;
- `accuracy`;
- `expected_correct_count`;
- `expected_accuracy`;
- `outcome_label`;
- balance summary (`count_O0`,`count_O1`);
- transform trace id and deterministic replay hash;
- boundary-audit pass/fail.

## 13) Completion requirements

A completed characterization record requires:

- all mandated regimes evaluated (`P0:S0,S1,S2` and `P1:S0,S1,S2`);
- all Section 10 audits present;
- deterministic replay pass;
- no missing evidence fields from Section 12.

## 14) Explicit non-authorization statement

This design does not authorize implementation, execution, architecture proposal, source selection, production selector development, HOW-2, Gate C, or Category/YAML integration.

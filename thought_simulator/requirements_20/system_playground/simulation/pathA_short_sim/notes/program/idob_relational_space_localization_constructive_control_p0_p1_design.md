# IdOB Relational-Space Localization Constructive Control P0/P1 Design

**Date:** 2026-11-27  
**Status:** Frozen mechanical design for characterization planning (non-normative).  
**Purpose:** Mechanically specify the reviewed P0/P1 constructive controls so implementation/execution (if later authorized) requires no new consequential experimental choice.

Review state: **BEING REVIEWED**

## 1) Scientific role (frozen)

P0 and P1 are constructive controls with intentionally preconstructed structural utility. They are for framework/control validation only and are not natural-structure discovery probes.

- **P0:** exact deterministic structural-information control (`S => O`).
- **P1:** informative-but-nondeterminative structural-information control (`S =/> O`, while `P(O|S) != P(O)`).

## 2) Common contracts

- action space: `R_A` predicts `O=0`, `R_B` predicts `O=1`;
- deterministic fixture IDs and ordering required;
- deterministic replay required for generators, transforms, and procedure;
- runtime procedure may consume only declared structural inputs and frozen rule logic.

Procedure must not read: latent tuples, outcome labels, correct actions, evaluator outputs, oracle answers, answer tables, ranking fields, or equivalent encodings.

## 3) P0 frozen definition

Latent tuple:

- `U=(P,Q,R)`, `P,Q,R in {0,1}`.

Structural features:

- `F(Ea)=P xor Q`
- `F(Eb)=Q xor R`
- `F(Ec)=R`.

Outcome:

- `O=P xor R`.

Invariant:

- `F(Ea) xor F(Eb)=O`.

Frozen procedure:

- `d = F(Ea) xor F(Eb)`;
- emit `R_A` if `d=0`;
- emit `R_B` if `d=1`.

Do not replace structural channels with direct `P`, `Q`, or `R` channels.

P0 fixture schedule:

- all 8 tuples `(P,Q,R)`;
- each repeated 6 times;
- total 48 instances;
- lexicographic order by `(P,Q,R,repeat_index)`;
- balanced outcomes: 24 with `O=0`, 24 with `O=1`.

## 4) P1 frozen definition

Latent tuple:

- `U=(P,Q)`, `P,Q in {0,1}`.

Structural bit:

- `S=P xor Q`.

Outcome:

- `O=P`.

Frozen distribution:

- `(0,0): 3/8`
- `(0,1): 1/8`
- `(1,0): 3/8`
- `(1,1): 1/8`.

Finite 48-instance realization:

- `(0,0)`: 18 instances;
- `(0,1)`: 6 instances;
- `(1,0)`: 18 instances;
- `(1,1)`: 6 instances.

So:

- `P(O=0)=P(O=1)=1/2`;
- `P(S=0)=P(S=1)=1/2`;
- `P(O=0|S=0)=3/4`;
- `P(O=0|S=1)=1/4`.

Therefore `S` is informative but not determinative.

Frozen P1 procedure:

- `S=0 => R_A`
- `S=1 => R_B`.

## 5) Frozen perturbation schedule

### 5.1 S0 (unaltered)

Use fixtures exactly as generated.

### 5.2 S1 (no tested structural information)

Remove tested structural input channels before the procedure.

Frozen deterministic S-blind fallback:

- emit `R_A` whenever required structural input is unavailable/invalid.

This fallback is fixed pre-execution and cannot be chosen after observing outcomes.

### 5.3 S2 (neutralized structure)

S2 preserves structural count/type/interface/availability/marginal value distribution while destroying association with `O`.

#### P1 S2 neutralization (frozen deterministic schedule)

Use the 48 fixed-order P1 instances as listed in Section 4.

1. Partition indices into two strata by true outcome `O`:  
   `I0 = [indices with O=0]` and `I1 = [indices with O=1]`.  
   Each stratum has 24 indices.
2. Within each stratum, keep frozen index order.
3. Assign neutralized structural bit by alternating within each stratum:  
   for the `j`-th index in either stratum, set `S_neutral = j mod 2`.

This is deterministic, predeclared, replayable, and auditable from the frozen schedule.

It yields exactly:

- `P(S_neutral=0)=P(S_neutral=1)=1/2`;
- `P(O=0|S_neutral=0)=P(O=0|S_neutral=1)=1/2`.

Applying the frozen P1 rule (`S_neutral=0 => R_A`, `S_neutral=1 => R_B`) therefore yields exactly `24/48 = 50%`.

#### P0 S2 neutralization (restored to frozen P0 semantics)

Keep decoy channels unchanged.

For each instance, define neutralized structural features:

- `F(Ea)_neutral = P xor Q`
- `F(Eb)_neutral = Q xor P = P xor Q`
- `F(Ec)_neutral = R`.

Then:

- decoded bit `d_neutral = F(Ea)_neutral xor F(Eb)_neutral = 0` for all instances;
- procedure emits constant `R_A`;
- with balanced outcomes, expected accuracy is exactly `24/48 = 50%`.

This preserves channel shape and blocks the informative deterministic invariant without exposing shortcuts.

## 6) Expected behavior contracts (frozen)

### P0

- `S0`: `48/48 = 100%`
- `S1`: `24/48 = 50%`
- `S2`: `24/48 = 50%`.

### P1

- `S0`: `36/48 = 75%`
- `S1`: `24/48 = 50%`
- `S2`: `24/48 = 50%`.

## 7) Feature-permutation contract

Feature-channel identifiers may be renamed or permuted per fixture instance. The canonical structural values consumed by the procedure remain invariant.

The permutation audit targets dependence on arbitrary labels. It must not swap canonical binary values `{0,1}` unless the procedure is explicitly invariant to that swap.

### 7.1 Frozen permutation audit schedule
Permutation audits are deterministic, predeclared, and do not alter the canonical structural values consumed by the procedure.

For every P0 and P1 fixture instance, evaluate the following presentation variants:

   1. Identity presentation

      - entity order: (Ea, Eb, Ec)
      - feature-channel identifiers: canonical ordering
   
   2. Entity permutation A

      - entity order: (Eb, Ec, Ea)
      - -channel identifiers: canonical ordering

   3. Entity permutation B

      - entity order: (Ec, Ea, Eb)
      - feature-channel identifiers: canonical ordering

   4. Feature-channel rename

      - entity order: (Ea, Eb, Ec)
      - feature-channel identifiers renamed by a fixed cyclic permutation
      - canonical structural values are unchanged

The procedure must operate on canonical entity/structural relationships rather than presentation position or arbitrary feature-channel names.

The permutation audit passes only if, for each underlying fixture instance and regime:

   * entity permutation does not change the emitted interpretation;
   * feature-channel renaming does not change the emitted interpretation;
   * expected S0/S1/S2 outcome counts remain unchanged;
   * transform traces identify the applied presentation variant;
   * exact replay reproduces the same variant and result.

Canonical binary values {0,1} are never swapped by the feature-channel rename.

These presentation variants are audit replications of the same underlying fixture conditions. They do not change the frozen P0/P1 generative distributions or create additional independent experimental conditions.

## 8) Required anti-shortcut audits

The characterization must preserve:

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
- completeness.

The held-out/permutation-generalization audit uses the frozen presentation schedule in Section 7.1; no implementation-time permutation schedule may be substituted.

## 9) Evidence fields and outcomes

Each regime record must include:

- phase (`P0`/`P1`);
- regime (`S0`/`S1`/`S2`);
- fixture size;
- expected correct;
- observed correct;
- expected accuracy;
- observed accuracy;
- balance counts (`O=0`,`O=1`);
- transform trace identity;
- replay hash;
- boundary-audit pass/fail.

Per-regime outcome labels:

- `CONTROL_VALIDATED`
- `CONTROL_FAILED`
- `INVALID_EXECUTION`.

Overall state:

- `VALIDATED_WITHIN_FIXTURE` only if all required regimes are `CONTROL_VALIDATED`.

## 10) Explicit non-authorization

This design does not authorize implementation, execution, evidence generation, natural-structure discovery probing, architecture changes, HOW-2, Gate C, production integration, or Category/YAML integration.

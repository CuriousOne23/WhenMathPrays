# IdOB Relational-Space Localization: Information/Representation Sufficiency Characterization Design

**Date:** 2026-11-27  
**Status:** Corrected mechanical design approved for implementation/execution; execution completed with observation recorded (non-normative).  
**Authority:** [idob_relational_space_localization_information_representation_sufficiency_proposal.md](idob_relational_space_localization_information_representation_sufficiency_proposal.md)

This document defines frozen mechanical design for characterization only.  
It does not authorize implementation or execution.

**Execution status note:** Human pre-execution review approved this corrected design for Phase 2. Characterization execution and evidence recording are documented in [idob_relational_space_localization_information_representation_sufficiency_observation.md](idob_relational_space_localization_information_representation_sufficiency_observation.md).

## 1) Design objective

Characterize which activation-relevant distinctions, if any, must be preserved at the runtime representation boundary for Gate A-like localization leverage to remain recoverable in principle within the frozen fixture.

## 2) Frozen controls (reused)

Hold fixed exactly:

- eight organizational groups and stable group IDs;
- relation identities, cardinality family, overlap family, and `k` family;
- necessary-set construction;
- active-surface deterministic deduplicated union;
- exhaustive matched size-`k` baseline construction;
- coverage/reduction measurements;
- ordered trace and exact replay requirements;
- runtime information boundary and comparable dominance criterion from Gate A/Gate B.

The intended variable is representation-preserved distinction only.

## 3) Decoder neutrality contract (all levels)

Every level-specific decoder must:

- receive only frozen representation payload, fixed group IDs, and `k`;
- be deterministic and fully frozen before implementation authorization;
- emit ordered trace and support exact replay.

No decoder may inspect:

- necessary relations;
- group membership contents;
- coverage/reduction;
- oracle ranking;
- outcomes.

Decoders are information-preservation probes, not intelligent or production selectors.

## 4) Frozen Gate A comparison domains

Two domains are frozen and must be reported separately.

### 4.1 Applicable fixture domain (execution/reproduction domain)

All frozen comparable fixture conditions under this characterization scope.

R0 exact-reproduction/plumbing checks apply to this domain.

### 4.2 Gate A-qualified leverage domain (primary sufficiency domain)

Primary R1-R4 representation-sufficiency comparison uses only Gate A conditions where the Gate A oracle activation actually satisfied the frozen nontrivial dominance criterion.

Frozen qualification predicate for domain membership:

- `nontrivial_useful_domain = true`
- `candidate_dominates_every_nonidentical_matched_activation = true`

using the frozen Gate A records.

Conditions outside this domain may be executed and reported separately, but:

- they are not described as Gate A-demonstrated leverage conditions;
- lack of dominance there is not interpreted as representation insufficiency;
- they are not used for primary sufficiency claims.

## 5) Representation ladder

The representation ladder is preserved exactly:

- R0 = exact activation identifier;
- R1 = exact unordered group set / representation-equivalence control;
- R2 = partial activation identity with frozen neutral completion;
- R3 = best single-group identity supplied directly;
- R4 = frozen coarsened activation class with neutral canonical decoder.

### R0 — Exact activation identifier (lossless positive/plumbing control)

R0 representation carries a canonical identifier for the Gate A oracle-selected size-`k` activation for the comparable fixture.

Frozen canonical identifier:

`gatea-oracle::<fixture_id>::k<k>::fp::<deterministic_fingerprint>`

where:

- `fixture_id` is the frozen Gate A fixture identifier (`phase3_n{n}_o{o}_k{k}`);
- `deterministic_fingerprint` is the exact Gate A `candidate_record.deterministic_fingerprint` for that fixture.

#### R0 frozen fixture map contract

Before characterization execution, freeze a Gate A fixture map containing, at minimum, for each valid comparable condition:

- `fixture_id`
- `k`
- `deterministic_fingerprint`
- resolved oracle-selected activation (canonical ordered group list)
- Gate A-qualified-domain membership flag (per Section 4.2)

Contract requirements:

- each valid R0 token resolves to exactly one recorded Gate A oracle-selected activation;
- decoder may only parse token and perform frozen map lookup;
- decoder must not recompute, optimize, substitute, or alter oracle choice;
- decoder must not receive additional oracle-only information beyond frozen token-to-activation resolution.

#### R0 exact-reproduction/plumbing evaluation (separate from leverage)

Per condition in applicable fixture domain, evaluate:

Did R0 deterministically decode to the exact Gate A oracle-selected activation for the corresponding fixture condition?

Allowed results:

- `R0_EXACT_REPRODUCTION_PASS`
- `R0_EXACT_REPRODUCTION_FAIL`

`R0_EXACT_REPRODUCTION_FAIL` is required on any of:

- missing map resolution;
- duplicate or ambiguous map resolution;
- fixture/fingerprint mismatch;
- decoded activation mismatch;
- token construction/parsing mismatch;
- ordered-trace or replay mismatch.

#### R0 leverage evaluation (independent)

Separately evaluate:

Did the exactly reproduced Gate A oracle activation satisfy the frozen leverage/dominance criterion for that condition?

A condition may pass exact reproduction yet fail leverage, and that is not an R0 reproduction/plumbing failure.

### R1 — Exact unordered group set (representation-equivalence control)

R1 representation carries the exact selected group identities only, as canonical unordered set.

Canonical encoding:

- sort by ascending numeric group ID (`G_1`..`G_8`);
- serialize as stable tuple/list of group IDs.

R1 and R0 contain equivalent activation information in different representations.  
R1 is representation-equivalence control, not information reduction.

R1 decoder:

- parse canonical group set and emit the same activation.

### R2 — Partial activation identity

R2 representation carries only a frozen partial subset of selected group identities.

Frozen supplied amount and order:

- supplied count `m = 1` for all tested `k` values;
- supplied item = lowest numeric group ID from exact selected activation;
- representation payload is one-item ordered list `[G_i]`.

Frozen neutral completion rule (unchanged):

Given partial representation `P`, fixed global group IDs `G_1..G_8`, and `k`:

1. initialize output activation with `P` in provided order;
2. append remaining group IDs in ascending numeric order, skipping any already present;
3. stop when output length equals `k`.

No other information source is allowed.

#### R2 interpretation at `k=1`

For `k=1`, supplied identity is the entire activation.  
At `k=1`, R2 is representation-equivalent to exact activation identity and is not information reduction.

Successful `k=1` R2 behavior is treated as equivalence/control evidence only and is not used as evidence that partial representation is sufficient for multi-group localization.

### R3 — Best single-group identity

R3 representation carries fixture-derived identity of strongest individual group directly (`i*`, same tie rule as frozen Gate B `X_base` construction).

R3 is neither Gate B repeated nor strict Gate B ablation:

- Gate B encoded related group distinction into `X_t` and passed it through modular scoring;
- R3 supplies group identity directly.

R3 decoder:

1. receive `[G_i*]`;
2. place `G_i*` first;
3. append ascending remaining group IDs until size `k`.

#### R3 interpretation at `k=1`

If R3 reproduces Gate A oracle activation for `k=1`, report that exactly as condition-level reproduction/equivalence behavior.

Do not generalize `k=1` R3 reproduction into evidence that single-group identity is sufficient for multi-group localization.  
Interpret `k=1` R3 evidence separately from `k>1` R3 evidence.

### R4 — Coarsened activation class

R4 maps multiple exact activations to one representation.

Frozen equivalence class key (unchanged):

`class_key = (k, min_group_id(exact_activation))`

All size-`k` activations with same minimum numeric group ID are in one class.

Frozen canonical decoder within class (unchanged):

Given `class_key = (k, G_j)`:

1. initialize activation with `G_j`;
2. append ascending group IDs greater than or equal to `G_j` first, then wrap to lower IDs, skipping duplicates;
3. stop when activation size reaches `k`.

This canonical choice uses only class key, fixed group IDs, and `k`, and never inspects outcomes or oracle-only information.

## 6) Baseline and leverage criterion

Baseline and leverage/dominance criterion remain frozen as Gate A/Gate B comparable criterion:

- exhaustive matched size-`k` baselines;
- same frozen dominance predicate and measurement contract.

No new baseline or dominance rule is introduced.

## 7) Per-level outcomes and reporting partition

Primary representation-sufficiency classifications for R1-R4 are made on Gate A-qualified leverage domain only.

Per level:

- **SUFFICIENT_WITHIN_FIXTURE**: criterion satisfied on required Gate A-qualified conditions under frozen completeness/contract checks.
- **INSUFFICIENT_WITHIN_FIXTURE**: criterion not satisfied on Gate A-qualified conditions while required controls pass.
- **INCONCLUSIVE**: contract, trace, replay, exhaustive-baseline, completeness, domain-membership, or required-control conditions fail.

Required reporting partition:

1. R0 exact-reproduction/plumbing results over applicable fixture domain.
2. R0 leverage results over same conditions (separate field, not plumbing pass/fail).
3. Primary R1-R4 sufficiency results over Gate A-qualified leverage domain.
4. Optional supplemental results outside Gate A-qualified domain, clearly labeled out-of-domain for primary sufficiency interpretation.

## 8) Required evidence fields

Per condition/level evidence must include at minimum:

- representation level (`R0`..`R4`);
- fixture identifiers (`n`, `o`, `k`, `fixture_id`);
- Gate A-qualified-domain membership flag and qualification basis;
- encoded representation payload;
- decoded activation;
- R0 token (for R0), map-resolution status, and unique-resolution status;
- exact-reproduction status (`R0_EXACT_REPRODUCTION_PASS` / `R0_EXACT_REPRODUCTION_FAIL`) where applicable;
- leverage/dominance outcome;
- baseline comparison outcome;
- ordered trace fingerprint and replay status;
- completeness/contract checks.

These fields are required to separate representation behavior, exact reproduction, domain membership, `k`, and leverage outcome without ambiguity.

## 9) Null-preserving interpretation rule

Explicitly allowed:

No tested reduced representation preserved enough distinction to recover frozen leverage.

Success at R0/R1 establishes only representability of oracle-derived exact activation information across runtime boundary within this fixture. It does not establish production obtainability or generatability.

## 10) Non-claims and authorization boundary

This design does not establish:

- Path A generation of successful representation;
- production input availability of successful information;
- production selector existence;
- optimality/necessity of current organizational layer;
- meaning semantics;
- necessary existence/non-existence of satisfactory non-oracle realization;
- HOW-2 authorization;
- Gate C authorization.

Authorization remains:

- design-stage documentation only;
- pre-execution design review required;
- implementation/execution not authorized.

## 11) Phase 1 correction status

Phase 1 corrections applied:

1. R0 exact reproduction separated from leverage success;
2. Gate A-qualified comparison domain frozen for primary sufficiency;
3. R2 `k=1` equivalence/control handling frozen;
4. R3 `k=1` interpretation boundary frozen;
5. R0 token/fixture-map unique-resolution and failure contract tightened.

No implementation or execution authorization is implied by these corrections.

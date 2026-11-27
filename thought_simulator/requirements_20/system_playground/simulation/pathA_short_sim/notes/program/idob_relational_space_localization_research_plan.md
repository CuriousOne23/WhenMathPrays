# IdOB Relational-Space Localization Research Plan

**Date:** 2026-11-25  
**Status:** Frozen research/characterization skeleton (non-normative).  
**Track:** IdOB Relational-Space Organization for Tractable Path A Selection.

**Execution status note:** This document preserves the frozen pre-execution research and characterization authority. Gate A / Phase 3 has subsequently been executed. The bounded fixture-relative and oracle-relative Gate A classification is CONTINUE. See [idob_relational_space_localization_observation.md](idob_relational_space_localization_observation.md) for characterization evidence and [idob_relational_space_localization_index.md](idob_relational_space_localization_index.md) for current track status and navigation.

## 1) Purpose

This plan defines a bounded research track for evaluating whether a **replaceable organizational/index layer** over stable IdOB relational identities can help Path A identify a tractable active relational surface.

This track does **not** treat organizational selection as meaning, and does **not** assert that localization is already implemented in IdOB.

## 2) Starting boundary and dependency context

The prior S2M IdOB traversal characterization cycle is treated as **closed** at its present-realization boundary.  
This track starts downstream of that closeout boundary and does not reopen that cycle by default.

Primary prior navigation entry (only when specifically needed): [s2m_index.md](s2m_index.md).

General engineering-method guidance used by this track: [20.740_ts_realization_qualification_guidance.md](../../../../../20.740_ts_realization_qualification_guidance.md).

## 3) Scope and non-goals

In scope:

- bounded research into organizational leverage for tractable active-surface selection;
- gate/phase characterization discipline;
- explicit stop/defer boundaries.

Out of scope in this plan state:

- production selector design;
- Category integration design;
- final YAML/IdOB representation design;
- implementation authorization.

## 4) Three-gate skeleton (frozen)

### Gate A — organizational leverage under oracle/surrogate localization information

Goal: determine whether organizational localization information provides practical tractability leverage without recasting organization as meaning.

Gate A pass intent (bounded): evidence that organizational localization can reduce/organize active relational working surface in a way that is mechanically inspectable and useful for next-step selector research planning.

### Gate B — one provisional real HOW (conditional)

Opened only if Gate A is explicitly passed.  
Goal: define one provisional, bounded realization path for localization/selection mechanics under the constraints discovered in Gate A.

### Gate C — structural-health / representation qualification

Goal: qualify what Gate B actually produces against structural-health criteria (replaceability, contract stability, surrogate discipline, and bounded validity statements).

## 5) Gate A phase structure and current phase

Gate A is frozen with phased progression.  
**Current next gate/phase:** **Gate A / Phase 3** (not yet executed).

### Frozen Gate A / Phase 3 fixture specification

#### Purpose

Gate A tests whether an organizational layer over stable IdOB relation identities contains exploitable localization structure when supplied with explicitly oracle-like surrogate localization information.

This is an upper-bound organizational-leverage test.

It does NOT test whether production Path A can discover or generate the localization signal.

#### 1. Relational universe

For each cardinality n construct:

R_total^(n) = {r_1, r_2, ..., r_n}

Use:

n in {32, 64, 128, 256}

Relations contain only stable identity and deterministic fixture ordering.

These values are fixture scales, not TS architectural thresholds.

Relation identity must remain unchanged across group reassignment, splitting, merging, overlap changes, and activation changes.

#### 2. Organizational groups

Construct:

O = {G_1, G_2, ..., G_8}

Group construction MUST:

- occur before necessary-set designation;
- receive no information about the future necessary set;
- be deterministic and reproducible;
- operate only on stable relation identities and frozen fixture parameters;
- keep base group sizes approximately balanced;
- permit zero, one, or multiple organizational memberships;
- contain no semantic, Category, or meaning-bearing labels;
- never redefine relation identity.

Deterministic base-group construction (frozen executable rule):

- Use zero-based relation index `j`.
- Assign:
  - `base_group(r_j) = G_((j mod 8) + 1)`
- Therefore:
  - `r_0 -> G_1`, `r_1 -> G_2`, ..., `r_7 -> G_8`, `r_8 -> G_1`, then cyclic repeat.

For frozen cardinalities this yields exactly balanced base group sizes:

- `n = 32`  -> 4 relations/group
- `n = 64`  -> 8 relations/group
- `n = 128` -> 16 relations/group
- `n = 256` -> 32 relations/group

Do not replace this with randomized allocation.

Use activated-group counts:

k in {1, 2, 3, 4}

With eight groups, enumerate matched activations exhaustively:

C(8,1) = 8  
C(8,2) = 28  
C(8,3) = 56  
C(8,4) = 70

#### 3. Overlap axis

Use:

o in {0, 0.10, 0.25, 0.50}

where o is the target fraction of relations receiving at least one additional organizational membership beyond base membership.

For each overlap condition:

1. begin with the same base assignment;
2. compute `N_overlap = round(o * n)`;
3. select the first `N_overlap` relation identities in frozen deterministic relation-ID order;
4. for each selected relation whose base group is `G_i`, preserve base membership and add exactly one additional membership in the next group cyclically (`G_1 -> G_2`, ..., `G_7 -> G_8`, `G_8 -> G_1`);
5. do not consult the necessary set;
6. preserve relation identity and base membership;
7. record all added memberships.

Report realized overlap count and fraction.

Do not replace this procedure with random sampling.

#### 4. Necessary-set designation

Only AFTER organizational groups and memberships have been constructed, designate:

R_necessary subset R_total

Use:

|R_necessary| = max(4, round(0.125 * n))

The necessary-set procedure:

- may inspect R_total;
- MUST NOT inspect group membership;
- must use the frozen deterministic index rule below;
- must record selected identities before activation;
- must not change after candidate or baseline results are observed.

Frozen deterministic necessary-set construction:

- Let `q(n) = max(4, round(0.125 * n))`.
- For `j = 0, 1, ..., q(n)-1`, compute:
  - `p_j = (5*j + 3) mod n`
- Define:
  - `R_necessary = { r_(p_j) }`

This procedure may use only `n` and frozen relation ordering, and must never inspect organizational membership.

For all frozen `n` values, resulting required indices are unique.

Do not replace this procedure with a random sample.

R_necessary represents fixture-designated downstream need only.

It does not establish meaning or information actually possessed by Path A.

#### 5. Oracle-only surrogate key

The surrogate key is explicitly ORACLE-ONLY.

It may inspect:

- completed organizational memberships;
- R_necessary;
- requested k;
- frozen deterministic tie rules.

It may NOT:

- modify groups;
- modify memberships;
- modify R_necessary;
- modify relation identities;
- create a secondary relation filter;
- use semantic or Category labels;
- imply that production Path A possesses equivalent information.

For every size-k activation A construct:

R_active(A) = union of members(G_i), for G_i in A

Calculate:

coverage(A) = |R_necessary intersection R_active(A)| / |R_necessary|

and:

reduction(A) = 1 - |R_active(A)| / |R_total|

Select the oracle candidate deterministically by:

1. highest necessary-relation coverage;
2. among equal-coverage activations, highest reduction;
3. among remaining ties, lexicographically lowest ordered group-ID sequence.

This explicitly tests upper-bound exploitability. It is NOT a production selector.

#### 6. Matched uninformed baseline

For:

k = |A_candidate|

enumerate:

A_k = {A subset O : |A| = k}

The baseline is matched by ACTIVATED-GROUP COUNT k, not final active-surface size.

For this initial eight-group fixture, enumerate all members of A_k exhaustively.

Do not use a single random baseline draw.

For every matched activation record the same measurements and traces as for the candidate.

Exclude the candidate activation from comparison against itself.

If a later fixture makes exhaustive enumeration impractical, its sampling rule, sample size, and seed must be frozen before execution.

#### 7. Active relational surface

For candidate and baseline activations:

R_active = dedupe( union of members(G_i) for G_i in A_t )

Deduplication operates solely on stable relation identity.

Emit the final surface in frozen deterministic relation-ID order.

Do not perform ranking, weighting, secondary filtering, or interpretation after activation.

#### 8. Required measurements

Record:

- |R_active|;
- activated-group count;
- pre-deduplication count;
- deduplication count;
- reduction;
- necessary-relation coverage;
- unnecessary inclusion count;
- unnecessary inclusion fraction;
- candidate position relative to matched baseline outcomes;
- Pareto relationship to matched activations;
- deterministic replay status;
- identity-stability/reorganization status.

Use:

reduction = 1 - |R_active| / |R_total|

coverage = |R_necessary intersection R_active| / |R_necessary|

unnecessary inclusion count = |R_active \\ R_necessary|

When R_active is non-empty:

unnecessary inclusion fraction = |R_active \\ R_necessary| / |R_active|

#### 9. Required trace

For every activation record:

1. fixture ID;
2. n;
3. overlap condition o;
4. k;
5. candidate/baseline designation;
6. activated group IDs in deterministic order;
7. group-membership identities before union;
8. pre-deduplication identity sequence;
9. duplicate identities removed;
10. final active relation identities;
11. necessary identities admitted;
12. necessary identities excluded;
13. unnecessary identities admitted;
14. reduction;
15. coverage;
16. deterministic fingerprint or equivalent replay identifier.

Equivalent reruns must reproduce the same ORDERED trace, not merely mathematical set equality.

#### 10. Frozen dominance predicate

Candidate C dominates matched activation B iff:

reduction(C) >= reduction(B)

AND

coverage(C) >= coverage(B)

with at least one strict inequality.

For this frozen initial fixture, C satisfies the Gate A dominance condition only if C dominates EVERY non-identical matched activation in A_k.

The candidate's own activation is excluded from comparison against itself.

A condition qualifies as a nontrivial useful domain only when:

0 < |R_active| < |R_total|

|R_necessary| > 0

at least one necessary relation is admitted

at least one relation is excluded

and the frozen dominance predicate is satisfied.

Do not change this criterion after observing results.

#### 11. Pressure schedules

##### A. Overlap expansion

Hold n and k fixed.

Vary:

o in {0, 0.10, 0.25, 0.50}

Observe:

- active-surface expansion;
- deduplication growth;
- reduction change;
- coverage change;
- candidate dominance position.

Do not require degradation in advance.

##### B. Activation expansion

Hold n and overlap construction fixed.

Vary:

k in {1, 2, 3, 4}

Observe:

- active-surface expansion;
- coverage change;
- reduction change;
- unnecessary inclusion;
- candidate dominance position.

Do not require crossing the dominance boundary.

##### C. False exclusion

Create explicit derivative conditions in which a predeclared number of necessary identities are made unreachable from the already-established candidate activation.

Use:

f in {0, 1, 2, floor(|R_necessary| / 2)}

Frozen deterministic false-exclusion derivative (per base fixture condition):

1. First compute the frozen oracle candidate activation `A_candidate` and `R_active(A_candidate)`.
2. Define:
   - `C = R_necessary intersection R_active(A_candidate)`
   - `U = R_total \ R_active(A_candidate)`
3. For requested `f`, select:
   - `C_f`: first `f` identities from `C` in frozen deterministic relation-ID order;
   - `U_f`: first `f` eligible identities from `U` in frozen deterministic relation-ID order that are not already members of `R_necessary`.
4. Construct derivative necessary set:
   - `R_necessary^(f) = (R_necessary \ C_f) union U_f`

Preserve unchanged:

- `R_total`;
- relation identities;
- organizational groups;
- memberships;
- `n`;
- `o`;
- `k`;
- the original base `A_candidate` being stressed.

Critical:

- Do NOT rerun the oracle to choose a different candidate activation before measuring the false-exclusion derivative.
- If either `|C| < f` or fewer than `f` eligible replacement relations exist in `U`, classify the requested derivative `NOT_CONSTRUCTIBLE`.
- Do not improvise or modify the fixture to force construction.
- `NOT_CONSTRUCTIBLE` is not automatically a Gate A failure.

Preserve the unchanged base fixture and record each derivative transformation.

Observe:

- coverage loss;
- reduction behavior;
- necessary identities excluded;
- trace visibility of exclusions;
- ability to distinguish false exclusion from organizational non-utility.

Force the pressure condition, not a desired result.

#### 12. Identity-stability check

For at least one condition at every n:

1. split one organizational group into two replacement groups;
2. reassign its existing membership without changing relation identities;
3. regenerate the relevant activation;
4. verify that admitted relations retain their original identities;
5. verify that active-surface changes are attributable only to changed organization or activation;
6. emit a before/after trace.

This tests organizational replaceability, not semantic equivalence between groupings.

#### 13. Deterministic replay

Execute every candidate condition at least twice from identical frozen inputs.

Replay passes only if these are identical:

- activated group ordering;
- membership expansion;
- duplicate-removal trace;
- final active relation ordering;
- reduction;
- coverage;
- unnecessary inclusion;
- output fingerprint.

Set equality alone is insufficient.

#### 14. Gate A decision

**CONTINUE**

Continue to selector research only if at least one nontrivial bounded fixture condition satisfies the frozen dominance predicate and the fixture mechanically distinguishes:

- false exclusion;
- overlap pressure;
- activation-count pressure;
- deterministic replay;
- identity preservation under reorganization.

A positive result establishes organizational leverage under oracle-quality fixture information only.

**STOP_THIS_ABSTRACTION**

Stop this tested organizational construction if no tested nontrivial condition satisfies the frozen dominance predicate even under the oracle-only surrogate key.

This stops the tested construction. It does not establish that all relational-space localization abstractions are invalid.

**INSUFFICIENT_EVIDENCE**

Return INSUFFICIENT_EVIDENCE if:

- group construction is not independent of R_necessary;
- the oracle information path is incompletely recorded;
- exhaustive baseline comparison is incomplete;
- necessary-set or baseline rules change after observing results;
- fixture construction prevents organizational leverage from being distinguished from oracle-information advantage;
- replay or trace requirements cannot be satisfied.

#### 15. Phase 3 stopping rule

Once all predeclared fixture conditions, exhaustive baseline comparisons, pressure schedules, replay checks, identity-stability checks, and Gate A comparisons are complete, Phase 3 STOPS.

Observed limitations do not authorize additional Phase 3 redesign unless the result is formally classified INSUFFICIENT_EVIDENCE under the frozen criteria.

#### 16. Explicit non-claims

Phase 3 does NOT establish:

- a production Path A selector;
- that Path A possesses oracle information;
- meaning;
- semantic regions;
- contextual support;
- evidence-specific correspondence;
- door legality;
- traversal legality;
- final interpretation;
- Category dependence;
- final IdOB organization;
- final YAML representation;
- global thresholds;
- globally valid localization utility.

### Present-realization closeout template (for future Phase 3 completion)

When Phase 3 completes, the closeout record must include, at minimum:

1. fixture conditions executed (n, o, k, and derivative f schedule conditions);
2. candidate and exhaustive matched-baseline comparison summary per condition;
3. dominance result per nontrivial condition;
4. pressure-schedule observations;
5. deterministic replay verdict;
6. identity-stability verdict;
7. Gate A verdict (`CONTINUE`, `STOP_THIS_ABSTRACTION`, or `INSUFFICIENT_EVIDENCE`);
8. explicit not-established/non-claims section aligned with the frozen non-claims list above.

## 6) Authorization state (frozen at plan creation)

- Gate A / Phase 3: **next authorized research gate**
- Gate A passed: **NO**
- Phase 3 executed: **NO**
- production selector research authorized: **NO**
- Category integration authorized: **NO**
- final YAML/IdOB representation design authorized: **NO**
- implementation work authorized: **NO**

## 7) Anti-treadmill and anti-fabrication rules

1. Do not auto-advance beyond Gate A without explicit review/pass.
2. Do not promote fixture constants/surrogates into architecture by drift.
3. Do not convert organizational localization into meaning semantics.
4. Do not represent unavailable prerequisites as if realized.
5. Do not collapse unresolved questions into implicit defaults.
6. If Gate A evidence is insufficient, record `INSUFFICIENT_EVIDENCE` and stop.

## 8) Present-realization closeout boundary (track boundary statement)

The prior traversal characterization closeout remains authoritative for the completed cycle boundary; this plan does not override it.

This track only defines the next research skeleton and execution gate discipline for localization research.

## 9) Immediate next step

Execute/review the frozen **Gate A / Phase 3** fixture against Gate A criteria.  
Do not proceed automatically beyond Gate A.

## Gate B — Provisional Non-Oracle Localization HOW and Frozen Characterization Design

### PURPOSE

Gate B tests whether one provisional non-oracle runtime selector can extract useful localization leverage from the organizational layer whose oracle-relative exploitability was established under Gate A.

Gate B does not establish that production Path A can generate the required localization signal.

### ORACLE INFORMATION BOUNDARY

The following Gate A oracle information remains unavailable at Gate B runtime:

- R_necessary;
- direct necessary-relation identity;
- group memberships;
- coverage values;
- Gate A oracle candidate;
- oracle group ranking.

### PROVISIONAL HOW

\( X_t \rightarrow S \rightarrow A_t \rightarrow R_{\text{active},t} \)

For each \( G_i \):

\( \text{score}(G_i) = (X_t + i) \bmod 8 \)

Then:

- rank groups by descending score;
- break remaining ties by ascending group ID;
- activate the top-k groups;
- form \( R_{\text{active},t} \) using the same deterministic deduplicated union used by Gate A.

No secondary filtering.  
No Category.  
No semantic labels.  

This is one provisional engineering HOW, not established TS architecture.

### FIXTURE-DERIVED BASE SIGNAL

After organizational groups and \( R_{\text{necessary}} \) exist, fixture construction may calculate:

- single-group coverage for every \( G_i \);
- \( i^* \) = group with highest single-group coverage;
- ties resolved by lowest group ID;
- \( X_{\text{base}} = (8 - i^*) \bmod 8 \).

This construction uses fixture-only characterization knowledge and is NOT available to the runtime selector.  
\( X_{\text{base}} \) does not establish that production Path A can generate an equivalent signal.

### SIGNAL QUALITY SCHEDULE

Signal quality is an INPUT property of the supplied fixture signal. Coverage and reduction remain OUTPUT observations.

- \( q_0 \) (highest-quality characterized fixture signal): \( X_t = X_{\text{base}} \)
- \( q_1 \): \( X_t = (X_{\text{base}} + 1) \bmod 8 \)
- \( q_2 \): \( X_t = (X_{\text{base}} + 2) \bmod 8 \)
- \( q_3 \): \( X_t = (X_{\text{base}} + 3) \bmod 8 \)
- \( q_4 \): \( X_t = (X_{\text{base}} + 4) \bmod 8 \)

\( q_0 \) is the highest-quality characterized fixture signal. It is not an established production Path A signal.

### RUNTIME INFORMATION CONTRACT

Runtime selector \( S \) may read only:

- \( X_t \);
- eight group IDs;
- requested \( k \).

Runtime selector \( S \) may NOT read:

- \( R_{\text{necessary}} \);
- identities designated necessary;
- membership lists;
- coverage;
- oracle candidate;
- oracle ranking.

### FIXTURE-CONSTRUCTION INFORMATION CONTRACT

Fixture construction may inspect completed groups and \( R_{\text{necessary}} \) only to derive and record \( X_{\text{base}} \) and its predetermined q-level perturbations.

That knowledge is not passed to runtime \( S \).

Fixture-construction knowledge and runtime-selector knowledge are explicitly separated.

### INHERITED GATE A FIXTURE

The following Gate A mechanisms are reused:

- \( R_{\text{total}} \) cardinality family;
- eight organizational groups;
- base grouping;
- overlap schedule;
- necessary-set construction;
- \( k \) activation family;
- deterministic active-surface construction;
- exhaustive matched size-k baseline;
- reduction;
- coverage;
- unnecessary inclusion;
- trace/replay procedures;
- applicable false-exclusion characterization.

Gate A authority is not rewritten.

### BASELINE

For each \( k \), exhaustively enumerate all size-k activations exactly as in Gate A.

Exclude the Gate B candidate from comparison against itself.

Use the same frozen dominance predicate:

reduction(C) >= reduction(B)  
AND  
coverage(C) >= coverage(B)

with at least one strict inequality.

The Gate A oracle is not the Gate B baseline. It may be retained only as a clearly labeled upper-bound reference if useful.

### PRESSURE SCHEDULES

Gate B must characterize:

- \( q_0 \) through \( q_4 \) signal quality;
- inherited overlap conditions;
- inherited \( k \) / activation breadth conditions;
- false-exclusion derivatives where mechanically applicable.

Force each pressure, not an expected result. Non-degradation is valid evidence.

### TRACE AND REPLAY

Require deterministic ordered trace and exact replay from identical frozen inputs.

Record \( X_t \) and q-level in Gate B characterization traces.

### OUTCOME PREDICATES

- **CONTINUE**: At least one nontrivial \( q_0 \) condition satisfies the dominance predicate against every non-identical matched size-k activation, and quality, overlap, and activation-breadth pressures are mechanically distinguishable.
- **PARTIAL**: Dominance, or strict improvement on at least one axis with no deterioration on the other, appears under \( q_0 \) but fails under one or more predeclared lower-quality levels, while the pressures remain mechanically distinguishable.
- **NEGATIVE**: No tested \( q_0 \) condition satisfies the frozen dominance predicate.
- **INSUFFICIENT_EVIDENCE**: Runtime \( X_t \) independence from \( R_{\text{necessary}} \) is broken, quality levels are incompletely applied, exhaustive matched baseline enumeration is incomplete, or required traces/replay cannot be verified.

Do not invent another outcome after execution.

### STOPPING RULE

Once all predeclared Gate B fixture conditions, signal-quality levels, matched baselines, pressure schedules, replay checks, traces, and outcome comparisons are complete, Gate B stops. Observed limitations do not authorize a second selector HOW within this research cycle.

### NON-CLAIMS

Gate B design and any later characterization do not automatically establish:

- a production Path A selector;
- that Path A can generate \( X_{\text{base}} \);
- that Path A possesses equivalent signal information;
- meaning;
- semantic regions;
- contextual support;
- evidence-specific correspondence;
- traversal legality;
- final interpretation;
- Category dependence;
- final IdOB/YAML organization;
- globally valid signal thresholds;
- globally valid localization.

### CURRENT STATUS

- Gate B design: FROZEN
- Gate B execution: PERFORMED (2026-11-27)
- Gate B mechanical classification: NEGATIVE (see gate_b_observation)
- Gate B observations: RECORDED
- Gate C: NOT AUTHORIZED
- Production selector implementation: NOT AUTHORIZED
- CATEGORY/YAML integration: NOT AUTHORIZED
- HOW-2 within this cycle: NOT AUTHORIZED

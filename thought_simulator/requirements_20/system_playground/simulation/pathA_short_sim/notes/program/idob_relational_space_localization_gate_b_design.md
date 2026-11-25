# IdOB Relational-Space Localization — Gate B Mechanical Characterization Design

**Document:** notes/program/idob_relational_space_localization_gate_b_design.md  
**Status:** FROZEN / READY FOR LATER IMPLEMENTATION AND EXECUTION (non-normative).  
**Authority:** Subordinate to [idob_relational_space_localization_research_plan.md](idob_relational_space_localization_research_plan.md). If any conflict exists, the research plan wins.

## Authority relationship

The research plan remains authoritative for:

- research proposition;
- epistemic boundaries;
- frozen provisional HOW;
- Gate B fixture contracts;
- outcome predicates;
- stopping rules;
- anti-treadmill discipline;
- non-claims.

This document is the mechanical realization/characterization design for the already-frozen Gate B research proposition. It does not create a new research proposition, a production Path A design, a Gate B observation, an implementation result, Gate C, a YAML design, or a Category redesign.

## 1. Gate B objective

Bounded question: Can the one frozen non-oracle provisional selector extract useful localization leverage from the organizational layer when driven only by the allowed runtime signal $X_t$?

Fixture-derived signal construction is not runtime selector knowledge. Gate B does not establish that production Path A can generate $X_{\text{base}}$ or an equivalent signal.

## 2. Provisional HOW

$$
X_t \rightarrow S \rightarrow A_t \rightarrow R_{\text{active},t}
$$

For each group $G_i$:

$$
\text{score}(G_i) = (X_t + i) \bmod 8
$$

Then:

1. calculate all eight group scores;
2. rank descending by score;
3. resolve ties by ascending group ID;
4. activate the top-$k$ groups;
5. construct the active relational surface using the inherited deterministic deduplicated union.

No secondary filtering. No Category. No semantic interpretation. No oracle inspection at runtime.

## 3. $X_{\text{base}}$ construction

After groups and $R_{\text{necessary}}$ exist (fixture construction only):

1. calculate single-group coverage of $R_{\text{necessary}}$ for each $G_i$;
2. choose $i^*$ = group ID with highest single-group coverage;
3. tie → lowest group ID;
4. calculate $X_{\text{base}} = (8 - i^*) \bmod 8$.

Fixture construction may use this knowledge. Runtime $S$ may not. This information boundary is absolute.

## 4. Signal-quality levels

- $q_0$ (highest-quality characterized fixture signal): $X_t = X_{\text{base}}$
- $q_1$: $X_t = (X_{\text{base}} + 1) \bmod 8$
- $q_2$: $X_t = (X_{\text{base}} + 2) \bmod 8$
- $q_3$: $X_t = (X_{\text{base}} + 3) \bmod 8$
- $q_4$: $X_t = (X_{\text{base}} + 4) \bmod 8$

$q_0$ is the highest-quality characterized fixture signal. It is not a proven production Path A signal, not meaning, not evidence-specific correspondence, and not a semantic-match score.

Quality level is an INPUT fixture property. Coverage and reduction remain OUTPUT measurements.

## 5. Runtime information contract

Runtime selector $S$ may inspect only:

- $X_t$;
- the eight organizational group IDs;
- requested $k$.

Runtime $S$ may not inspect:

- $R_{\text{necessary}}$;
- necessary-relation identities;
- group membership lists;
- group coverage;
- Gate A oracle candidate;
- Gate A oracle ranking;
- later characterization outcome.

An implementation must be able to verify that the selector function receives only the allowed arguments.

## 6. Inherited Gate A fixture

The following are reused without modification (see research plan for exact rules):

- $R_{\text{total}}$ cardinality: $n \in \{32, 64, 128, 256\}$
- organizational groups: $G_1 \dots G_8$
- base grouping: $\text{base_group}(r_j) = G_{((j \bmod 8) + 1)}$
- overlap: $o \in \{0, 0.10, 0.25, 0.50\}$ with the already-frozen cyclic overlap injection
- $R_{\text{necessary}}$: the already-frozen deterministic Gate A necessary-set construction
- activation counts: $k \in \{1, 2, 3, 4\}$
- active surface: deterministic deduplicated union by stable relation identity

## 7. Gate B condition matrix

Cartesian product of the frozen factors:

- $n \in \{32, 64, 128, 256\}$ (4 values)
- $o \in \{0, 0.10, 0.25, 0.50\}$ (4 values)
- $k \in \{1, 2, 3, 4\}$ (4 values)
- $q \in \{q_0, q_1, q_2, q_3, q_4\}$ (5 values)

Exact base Gate B condition count: $4 \times 4 \times 4 \times 5 = 320$.

False-exclusion derivatives, where mechanically applicable, attach to base conditions exactly as defined in the Gate A fixture (same $f$ schedule and `NOT_CONSTRUCTIBLE` rule). They stress the already-chosen Gate B activation; the oracle is not re-run. `NOT_CONSTRUCTIBLE` is recorded and is not automatically a failure.

## 8. Baseline

Inherited exhaustive matched size-$k$ uninformed baseline.

For each Gate B candidate activation, enumerate all size-$k$ group activations. Exclude the Gate B candidate from comparison against itself.

Frozen dominance predicate:

$$
\text{reduction}(C) \ge \text{reduction}(B)
$$

$$
\text{AND}
$$

$$
\text{coverage}(C) \ge \text{coverage}(B)
$$

with at least one strict inequality.

Gate A oracle results are not the Gate B baseline. If retained, they are labeled upper-bound reference only.

## 9. Measurements

Exact Gate B evidence fields required:

- fixture/condition ID
- $n$
- $o$
- $k$
- q level
- $X_{\text{base}}$
- supplied $X_t$
- group scores
- ordered group ranking
- activated group IDs
- pre-dedupe relation identities/count
- deduplicated active relation identities/count
- necessary relations admitted
- necessary relations excluded
- coverage
- reduction
- unnecessary inclusion
- exhaustive baseline comparison
- dominance status
- replay fingerprint/status
- false-exclusion status where applicable

## 10. Trace

A deterministic ordered trace must recover:

fixture construction → $X_{\text{base}}$ → q transform → $X_t$ → scores → ranking → $A_t$ → $R_{\text{active}}$ → measured outputs.

A reviewer must be able to determine why a particular group activation occurred without consulting hidden runtime state.

## 11. Replay

Identical frozen fixture inputs and $X_t$ must produce identical:

- $X_{\text{base}}$;
- q transform;
- $X_t$;
- group scores;
- ranking;
- activated groups;
- deduplication trace;
- $R_{\text{active}}$ ordering;
- metrics;
- fingerprint.

Set equality alone is insufficient.

## 12. Signal-quality pressure

$q_0$ through $q_4$ constitute a frozen pressure schedule. Increasing q index is a deterministic modular displacement. Observed degradation, non-monotonic behavior, or no degradation are all valid evidence. Do not require monotonic decline.

## 13. Overlap and activation pressures

Reuse $o \in \{0, 0.10, 0.25, 0.50\}$ and $k \in \{1, 2, 3, 4\}$ as independent characterization factors. Do not force an expected outcome.

## 14. False-exclusion pressure

Apply the already-frozen Gate A false-exclusion derivative to the Gate B activation being stressed. Preserve the Gate B selector activation. Use the existing `NOT_CONSTRUCTIBLE` behavior. Do not re-run the oracle. No new research decision is required.

## 15. Outcome evaluation

Frozen classes from the research plan (not redefined):

- **CONTINUE**: At least one nontrivial $q_0$ condition satisfies the dominance predicate against every non-identical matched size-$k$ activation, and quality, overlap, and activation-breadth pressures are mechanically distinguishable.
- **PARTIAL**: Dominance, or strict improvement on at least one axis with no deterioration on the other, appears under $q_0$ but fails under one or more predeclared lower-quality levels, while the pressures remain mechanically distinguishable.
- **NEGATIVE**: No tested $q_0$ condition satisfies the frozen dominance predicate.
- **INSUFFICIENT_EVIDENCE**: Runtime $X_t$ independence from $R_{\text{necessary}}$ is broken, quality levels are incompletely applied, exhaustive matched baseline enumeration is incomplete, or required traces/replay cannot be verified.

Mechanical evaluation sequence:

1. Verify runtime information contract and completeness of traces/replay. If violated → INSUFFICIENT_EVIDENCE.
2. Check whether any nontrivial $q_0$ condition satisfies full dominance against every non-identical matched activation. If none → NEGATIVE.
3. If at least one such $q_0$ condition exists and pressures are distinguishable, check whether the same dominance (or non-deteriorating improvement) holds for all lower q levels. If yes → CONTINUE. If it fails for one or more lower q levels → PARTIAL.

The predicates do not overlap: CONTINUE requires dominance under $q_0$ that survives the quality schedule; PARTIAL requires it under $q_0$ but not under the full schedule; NEGATIVE requires its absence under $q_0$.

## 16. Stopping rule

Once all predeclared Gate B fixture conditions, signal-quality levels, matched baselines, pressure schedules, replay checks, traces, and outcome comparisons are complete, Gate B stops. Observed limitations do not authorize a second selector HOW within this research cycle.

No HOW-2. No repeated tuning. No post-hoc q levels. No changed baseline. No changed dominance rule.

## 17. Expected implementation boundary

A later characterization implementation (not production Path A) must:

- accept the frozen fixture parameters and quality schedule as inputs;
- execute the deterministic construction sequence (groups → necessary set → $X_{\text{base}}$ → q transforms → selector → active surface → baselines);
- emit the required evidence fields and ordered traces;
- produce a machine-readable evidence artifact;
- support exact replay verification.

Gate B implementation is characterization machinery only.

## 18. Expected observation document

The later Gate B observation (not created today) must report:

- executed conditions;
- measured evidence;
- signal-quality behavior;
- overlap behavior;
- activation-breadth behavior;
- false-exclusion behavior;
- replay;
- outcome classification;
- limitations;
- non-claims.

Do not pre-write findings.

## 19. Non-claims

Gate B does not establish:

- production Path A selector capability;
- that Path A can generate $X_{\text{base}}$;
- that Path A has equivalent signal information;
- meaning;
- semantic regions;
- contextual support;
- evidence-specific correspondence;
- door legality;
- traversal legality;
- final interpretation;
- Category dependence;
- final IdOB organization;
- final YAML structure;
- global signal thresholds;
- globally valid localization.

## 20. Design completeness check

Could a later GitHub AI Agent implement and execute Gate B from the research plan, this design document, and the inherited Gate A characterization machinery without inventing any consequential experimental rule?

YES. All generation rules, information contracts, condition matrix, baseline, measurements, pressures, outcome predicates, and stopping rule are fully specified and deterministic.

**Design status: FROZEN / READY FOR LATER IMPLEMENTATION AND EXECUTION**

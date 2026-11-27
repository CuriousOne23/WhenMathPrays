# IdOB Relational-Space Localization: Information/Representation Sufficiency Characterization Design

**Date:** 2026-11-27  
**Status:** Authorized mechanical design development; pre-execution review required (non-normative).  
**Authority:** [idob_relational_space_localization_information_representation_sufficiency_proposal.md](idob_relational_space_localization_information_representation_sufficiency_proposal.md)

This document defines a frozen mechanical design for characterization only.  
It does not authorize implementation or execution.

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

## 4) Representation ladder

### R0 — Exact activation identifier (lossless positive/plumbing control)

R0 representation carries a canonical identifier for the Gate A oracle-selected size-`k` activation for the comparable fixture.

Frozen canonical identifier:

`gatea-oracle::<fixture_id>::k<k>::fp::<deterministic_fingerprint>`

where:

- `fixture_id` is the frozen Gate A fixture identifier (`phase3_n{n}_o{o}_k{k}`);
- `deterministic_fingerprint` is the exact Gate A `candidate_record.deterministic_fingerprint` for that fixture.

This identifier is frozen as the authoritative exact-activation token for this characterization design.

R0 decoder:

1. parse canonical identifier;
2. resolve exact activation from frozen Gate A fixture map by `(fixture_id, deterministic_fingerprint)`;
3. emit resolved activation.

### R1 — Exact unordered group set (representation-equivalence control)

R1 representation carries the exact selected group identities only, as a canonical unordered set.

Canonical encoding:

- sort by ascending numeric group ID (`G_1`..`G_8`);
- serialize as stable tuple/list of group IDs.

R1 and R0 contain equivalent activation information in different representational forms.  
R1 is a representation-equivalence control, not an information reduction.

R1 decoder:

- parse canonical group set and emit the same activation.

### R2 — Partial activation identity

R2 representation carries only a frozen partial subset of selected group identities.

Frozen supplied amount and order:

- supplied count `m = 1` for all tested `k` values;
- supplied item = lowest numeric group ID from the exact selected activation;
- representation payload is the one-item ordered list `[G_i]`.

Frozen neutral completion rule:

Given partial representation `P`, fixed global group IDs `G_1..G_8`, and `k`:

1. initialize output activation with `P` in provided order;
2. append remaining group IDs in ascending numeric order, skipping any already present;
3. stop when output length equals `k`.

No other information source is allowed.

### R3 — Best single-group identity

R3 representation carries the fixture-derived identity of the strongest individual group directly (`i*`, same tie rule as frozen Gate B `X_base` construction).

R3 is not Gate B repeated and is not a strict Gate B ablation:

- Gate B encoded a related group distinction into `X_t` and passed it through modular scoring;
- R3 supplies the group identity directly.

Comparison value is bounded: it can help distinguish insufficiency of single-group distinction from representation/decoder loss in Gate B, but cannot independently prove which component caused Gate B failure.

R3 decoder:

1. receive `[G_i*]`;
2. place `G_i*` first;
3. append ascending remaining group IDs until size `k`.

### R4 — Coarsened activation class

R4 maps multiple exact activations to one representation.

Frozen equivalence class key:

`class_key = (k, min_group_id(exact_activation))`

All size-`k` activations with the same minimum numeric group ID are in one class.

Frozen canonical decoder within class:

Given `class_key = (k, G_j)`:

1. initialize activation with `G_j`;
2. append ascending group IDs greater than or equal to `G_j` first, then wrap to lower IDs, skipping duplicates;
3. stop when activation size reaches `k`.

This canonical choice uses only class key, fixed group IDs, and `k`, and never inspects outcomes or oracle-only information.

## 5) Per-level outcomes

For each representation level:

- **SUFFICIENT_WITHIN_FIXTURE**: representation+decoder recover activation satisfying frozen leverage criterion.
- **INSUFFICIENT_WITHIN_FIXTURE**: criterion not satisfied while lossless positive control succeeds.
- **INCONCLUSIVE**: contract/trace/replay/exhaustive-baseline/completeness/positive-control requirement failed.

After per-level classifications, produce a bounded ladder summary.  
Do not replace per-level results with one label that hides where distinctions were lost.

## 6) Null-preserving interpretation rule

Explicitly allowed:

No tested reduced representation preserved enough distinction to recover frozen leverage.

Success at R0/R1 only establishes representability of oracle-derived exact activation information across the runtime boundary within this fixture. It does not establish production obtainability/generatability.

## 7) Non-claims and authorization boundary

This design does not establish:

- Path A generation of successful representation;
- production input availability of successful information;
- production selector existence;
- optimality/necessity of current organizational layer;
- meaning semantics;
- necessary existence/non-existence of a satisfactory non-oracle realization;
- HOW-2 authorization;
- Gate C authorization.

Authorization remains:

- design-stage documentation only;
- pre-execution design review required;
- implementation/execution not authorized.

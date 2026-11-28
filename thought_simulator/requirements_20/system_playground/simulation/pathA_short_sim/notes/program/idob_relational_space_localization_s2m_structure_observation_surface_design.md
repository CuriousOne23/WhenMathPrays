# IdOB Relational-Space Localization S2M Structure Observation Surface Design

**Date:** 2026-11-27  
**Status:** Scientific characterization design completion prepared for review (non-normative).  
**Purpose:** Freeze bounded execution prerequisites for S2M-structure observation-surface characterization without executing it.

Review state: **BEING REVIEWED**

## 1) Design intent and scope

This design characterizes observable organization in already-realized S2M transition surfaces, without presupposing basis-parameter, narrowing, or localization form.

Primary objective: structure characterization.  
Secondary objective: separately record measurable leverage where present.

This document is not execution authorization.

## 2) Candidate observation surfaces used by this design

From current authority/observation record:

1. **S_surface_seed** — bounded realized seed/written-relation surface (`S_t` bounded surface).  
   Authority: [s2m_idob_traversal_program_reference.md](s2m_idob_traversal_program_reference.md), [s2m_idob_traversal_observation.md](s2m_idob_traversal_observation.md), [s2m_idob_traversal_characterization_closeout.md](s2m_idob_traversal_characterization_closeout.md).
2. **S_surface_candidates** — surrogate finite endpoint-association candidate surface (`C_t` surrogate).  
   Authority: same as above.
3. **S_surface_support** — aggregate candidate-support/correspondence-state surface (including unresolved/unavailable states).  
   Authority: [s2m_idob_traversal_correspondence_observation.md](s2m_idob_traversal_correspondence_observation.md), [s2m_idob_traversal_characterization_closeout.md](s2m_idob_traversal_characterization_closeout.md).

Boundary preserved: surrogate surfaces remain surrogate; no promotion to door-legal surfaces.

## 3) Frozen first-run bounded case matrix

The first-run matrix is frozen as the smallest discriminative set that covers:

- cue absence vs cue presence;
- sentence-only vs prior-context provenance;
- repeated vs non-repeated prior evidence;
- mixed-source prior evidence;
- candidate-surface available vs unresolved/unavailable.

### 3.1 Retained matrix cells

| Cell ID | Condition class | Authority case anchor(s) | Surface availability |
|---|---|---|---|
| M1 | cue absent, sentence-only, candidate available | `TC02_no_correspondence` in [s2m_idob_traversal_observation.md](s2m_idob_traversal_observation.md) | seed/candidates/support observable |
| M2 | cue present, sentence-only, candidate available | `TC10_multi_candidate` in [s2m_idob_traversal_observation.md](s2m_idob_traversal_observation.md) | seed/candidates/support observable |
| M3 | cue present, prior-context single-source, candidate available | `TC01_support` in [s2m_idob_traversal_observation.md](s2m_idob_traversal_observation.md) | seed/candidates/support observable |
| M4 | cue present, prior-context repeated evidence, candidate available | `CR06_duplicate_dependency` in [s2m_idob_traversal_correspondence_observation.md](s2m_idob_traversal_correspondence_observation.md) | seed/candidates/support observable |
| M5 | cue present, prior-context mixed-source, candidate available | `CR08_independence_unavailable` in [s2m_idob_traversal_correspondence_observation.md](s2m_idob_traversal_correspondence_observation.md) | seed/candidates/support observable |
| M6 | candidate-surface unresolved/unavailable boundary condition | `CR03_unresolved_record` and `TC04_unresolved_correspondence` anchors in [s2m_idob_traversal_correspondence_observation.md](s2m_idob_traversal_correspondence_observation.md) and [s2m_idob_traversal_observation.md](s2m_idob_traversal_observation.md) | unresolved/unavailable state explicitly represented |

### 3.2 Why this matrix is sufficient for first bounded characterization

This matrix is not exhaustive over S2M space. It is sufficient for first bounded characterization because it includes:

- both cue regimes (present/absent),
- both provenance regimes (sentence-only/prior-context),
- repeated vs non-repeated prior context,
- mixed-source prior context,
- an explicit unresolved/unavailable boundary class.

It therefore supports first-pass organization and boundary/stage observations without introducing new condition classes.

## 4) Primary observation classes

Primary structure-characterization outputs:

1. observed organization class (stable configuration/partition patterns);
2. observed dependency class (interaction/dependence patterns where represented);
3. observed boundary/stage class (available vs unresolved/unavailable transitions);
4. observed trajectory-like class (reproducible directional ordering without monotonic-narrowing assumption);
5. observed invariance class (organization preserved under legitimate controls).

## 5) Secondary utility channel

Secondary channel is separately reported:

- measurable leverage indications over transition behavior.

No utility finding is required for primary structural observation validity.

## 6) Frozen per-surface control mappings

Control mappings are frozen only where current represented fields support them without semantic invention.

### 6.1 S_surface_seed

- **Removal control (frozen):** compare M3 (prior-context present) vs M1 (no prior cue) under documented cases.
  - Affected represented fields: seed/written-relation presence/count and associated cue-observation context (no seed semantic change).
- **Permutation control:** unavailable for this surface in current authority (no independent canonical channel-permutation contract for this surface analogous to P0/P1 channel audits).
- **Neutralization control:** unavailable without introducing synthetic semantics.

Disposition: retain surface; use removal + boundary comparisons only.

### 6.2 S_surface_candidates

- **Removal control (frozen):** M3 vs M1 cue-removal comparison on candidate-state outcomes.
- **Boundary control (frozen):** M3/M1/M2/M4/M5 (available) vs M6 (unresolved/unavailable) to characterize stage/boundary behavior.
- **Permutation control:** unavailable without introducing new candidate-presentation semantics.
- **Neutralization control:** unavailable for faithful association disruption without semantic invention.

Disposition: retain surface; available/removal/boundary controls are sufficient for bounded interpretation.

### 6.3 S_surface_support

- **Removal control (frozen):** compare support-state transitions between M3 and M1.
- **Provenance-variation control (frozen):** compare M3 vs M4 vs M5 for single-source/repeated/mixed-source represented dependency behavior.
- **Boundary control (frozen):** compare available support-state cells vs M6 unresolved/unavailable class.
- **Neutralization control:** unavailable without introducing new evidence/candidate semantics.
- **Permutation control:** unavailable without new correspondence representation semantics.

Disposition: retain surface; no fabricated neutralization substitutes introduced.

## 7) Shortcut/leakage checks (frozen)

Required checks for any later execution:

- oracle/privileged information exclusion;
- post-transition leakage exclusion;
- evaluator isolation;
- direct/indirect label leakage checks;
- position/name shortcut checks where applicable;
- unresolved/unavailable-state handling integrity.

Failure handling: classify invalid; do not post-hoc patch semantics.

## 8) Frozen semantic-slice replay policy

Replay identity is evaluated on a **semantic experimental slice**.

### 8.1 Fields requiring exact replay identity

For each retained matrix cell:

1. cell identity (`M1..M6`) and authority-anchored condition class;
2. qualified surface availability state (available / unresolved / unavailable as represented);
3. represented cue-provenance state (sentence-only/prior-context where present);
4. represented candidate/support state outputs used for scientific comparison;
5. control identity (removal/boundary/provenance-variation comparison role);
6. derived characterization outputs computed from the semantic slice.

### 8.2 Legitimate exclusions from exact identity

Excluded from strict identity only when non-semantic and runtime-volatile:

- runtime timestamps and generated run metadata fields documented as unstable in prior observations;
- artifact-run identifiers/path wrappers that do not alter semantic case content.

Authority basis for this exclusion:

- [s2m_idob_traversal_observation.md](s2m_idob_traversal_observation.md) explicitly records full-object mismatch from timestamp churn while semantic replay controls pass.
- [s2m_idob_traversal_correspondence_observation.md](s2m_idob_traversal_correspondence_observation.md) records semantic-slice duplicate-run equality.

No semantic field may be excluded for convenience.

## 9) Outcome classes

### 9.1 Informative negative outcomes

- **NO_STABLE_ORGANIZATION_OBSERVED_WITHIN_SURFACE**
- **SURFACE_TOO_COARSE_FOR_PRIMARY_OBJECTIVE**
- **UTILITY_NEGATIVE_WITH_STRUCTURE_OBSERVED**

### 9.2 Invalid/boundary-violation outcomes

- **BOUNDARY_VIOLATION_ORACLE_OR_PRIVILEGED**
- **BOUNDARY_VIOLATION_POST_TRANSITION**
- **BOUNDARY_VIOLATION_NEW_AUTHORITY_OR_SEMANTIC_CHANGE**
- **LEAKAGE_OR_SHORTCUT_CONTAMINATION**
- **REPLAY_OR_COMPLETENESS_FAILURE**

### 9.3 Hold outcome

- **HOLD_NO_LEGITIMATE_SURFACE**

## 10) Stopping rules

Stop and return invalid/HOLD rather than inventing rules if:

1. new read authority/architecture is needed;
2. required condition depends on oracle/post-transition information;
3. control definition requires semantic invention;
4. closed S2M traversal cycle would be reopened;
5. semantic replay slice cannot be deterministically reproduced.

## 11) Authority-integrity audit of resolved prerequisites

### 11.1 Case matrix prerequisite

- Result: **PASS**
- No new information class, read edge, or architecture introduced.
- All retained cells are authority-anchored to existing recorded cases.

### 11.2 Control-mapping prerequisite

- Result: **PASS (bounded)**
- Legitimate removal/boundary/provenance-variation controls frozen.
- Unsupported neutralization/permutation mappings explicitly marked unavailable; none fabricated.

### 11.3 Replay-policy prerequisite

- Result: **PASS**
- Semantic-slice replay scope frozen.
- Runtime-volatile metadata exclusions justified by existing observation records.

## 12) Remaining unresolved items

None.

## 13) Execution-readiness assessment

**READY FOR REVIEW**

Meaning of this assessment:

- design prerequisites are frozen sufficiently for a later explicit authorization decision;
- execution remains not authorized by this document.

## 14) Non-authorizations preserved

This design does not authorize:

- implementation or experiment execution;
- localization source selection/read-edge creation;
- architecture changes;
- HOW-2;
- Gate C;
- production integration;
- Category/YAML changes;
- reopening the closed S2M traversal characterization cycle.

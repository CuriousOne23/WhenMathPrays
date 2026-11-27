# IdOB Relational-Space Localization: Pre-Localization Information-Provenance Contract

**Date:** 2026-11-27  
**Status:** Human-reviewed and approved research boundary/contract document (non-normative).  
**Purpose:** Define provenance boundaries for any future pre-localization candidate input without selecting an input, authorizing localization use, or asserting sufficiency.

This document is not a normative 20-series requirements change.

## 0) Review state and approval boundary

- Review state: **APPROVED**
- Document kind remains: **non-normative research boundary/contract**
- Approval does not change any normative TS requirement.
- Approval does not select a localization source.
- Approval does not create a localization read/access edge.
- Approval does not establish localization sufficiency.

## 1) Governing distinction

`present before localization != authorized for localization != sufficient for localization`

A field or source being present and readable before IdOB does not by itself authorize its use for localization.

Authorization for localization does not establish experimental sufficiency.

Experimental sufficiency does not establish production availability or architectural authorization.

Additional status distinction used by the candidate analysis:

`present != readable != research-eligible != localization-authorized != sufficient`

## 2) Definitions

Pre-localization runtime information is a datum already present in runtime state, or deterministically derivable from authorized runtime state, before an active relational region has been selected, whose existence and value do not depend upon the outcome of localization.

Circularity guard:

Localization must not require as input information that exists or obtains its value only after localization has already succeeded.

## 3) Current architectural boundary

Bounded finding:

- A distinct relational-space localization step, its exact placement, and its input contract are not currently defined by authoritative TS documents.

Therefore:

- pre-localization information can be present;
- IdOB can read some upstream envelopes under existing authority;
- no source is currently designated as an authorized localization input.

Current conclusion:

**PRE-LOCALIZATION INFORMATION EXISTS, BUT LOCALIZATION AUTHORITY IS NOT DEFINED.**

This contract selects no localization input, authorizes no representation, establishes no sufficiency, and defines no selector.

## 4) Architecturally present source categories and classification

Classification labels:

- **A. ESTABLISHED PRE-LOCALIZATION AVAILABLE** — architecture establishes presence and readable availability before localization.
- **B. PRESENT, BUT LOCALIZATION ACCESS NOT ESTABLISHED** — exists pre-localization; localization use authority is not established.
- **C. CANDIDATE / HYPOTHETICAL** — potentially relevant; authoritative availability/access not established.
- **D. PROHIBITED / CIRCULAR** — depends on localization outcome, oracle answer, or prohibited routes.

### 4.1 Source categories (bounded audit table)

| Source category | Established presence before IdOB | Owner/writer authority | Existing read authority context | Localization use authorized | Sufficiency evaluated | Classification |
|---|---|---|---|---|---|---|
| Intake / IE envelope (`TP.intake.*`, `TP.structure.*`) | Yes | IE (`20.116.010`) | Upstream pipeline data in TP | No | No | B |
| Correction-selected TP / context envelopes (`TP.cex.*`, `TP.metadata.context*`) | Yes, when produced | CEx/CE (`20.116.010`) | Downstream readers consume envelope | No | No | B |
| Structural substrate (`TP.metadata.structural_metadata`, SOB/SROB/CnOB/SmOB outputs, SSG-derived substrate) | Yes | OB-set / SSG-path owners (`20.105.010`, `20.116.010`) | IdOB reads frozen structure contextually | No | No | B |
| Structural-key / crossing components (`TP.idob.*` crossing fields) | Not pre-localization by definition for localization-to-IdOB question | IdOB-prm (`20.105-116`, `20.116.020`) | Downstream readers after IdOB write | No | No | D (post-localization for this boundary) |
| Routing metadata and filters (`TP.metadata.routing_metadata`, `process.routing_filter`, `routing_update`) | Yes | RBU/RB/RTU/CTP (`20.116.010`, `20.116.020`) | IdOB may read routing metadata/filter read-only (`20.105.010`) | No | No | B |
| Utterance carrier (`utterance`) | Yes | Intake/isolation-carrier authority (`20.116.010`, `20.105-117`) | Available as carrier | No | No | B |
| CIE row / crossing semantics (`TP.idob`, `meaning_delta_h`, identity exports) | Produced at IdOB crossing | IdOB-prm (`20.105-116`, `20.116.020`) | Readable downstream post-write | No | No | D (post-localization / circular for pre-localization input) |
| Prior-cycle IdOB envelope / lineage markers (`TP.idob` in prior runtime state, `TP.lineage_log[]`) | May exist in replay/continuity state | Authorized appenders (`20.116.010`) | Replay and continuity readers | No | No | B |
| Continuity / COB / CIL / CST metadata (`TP.metadata.continuity*`, `TP.cst.*`, `TP.cil.*`, COB snapshots) | Yes where emitted | COB/CIL/CST owners (`20.116.010`, `20.116.020`) | Consumer-limited by owner/read walls | No | No | B |
| Already-authorized Path A inputs to existing primitives | Yes within owned primitive contracts | Per primitive owner | Read scope limited by ownership walls | No (for localization) | No | B |
| Replay-stable prior runtime state (when authoritatively established) | Yes in replay frameworks | As specified by source envelope owners | Replay-specific read context | No | No | B |

Notes:

- Classifications above are bounded to current authority documents and this localization question.
- Presence/readability in existing primitive contracts does not imply localization authorization.

## 5) Ownership and read boundaries (preserved)

- ownership and write walls remain intact (`20.116.020`);
- read access must be explicitly established per owned envelope;
- existence does not imply read authority;
- IdOB read authority does not automatically imply authority for a new localization mechanism;
- absent data must not be replaced with zero, guesses, or helpful defaults;
- no field may cross a localization boundary until that boundary and its read contract are explicitly authorized.

## 6) Explicitly prohibited provenance

A future localization input must not derive from:

- Gate A oracle activation;
- activation fingerprint or unique oracle identifier;
- necessary-set identities;
- oracle rankings;
- coverage outcomes;
- reduction outcomes;
- dominance outcomes;
- fixture-specific answer-recovery keys;
- candidate evaluation against desired result;
- meaning stand-in `M` / `M'` born inside IdOB;
- `tp.idob`;
- post-IdOB MCB state;
- post-localization traversal or meaning;
- any value computed by first examining the oracle answer.

## 7) Provenance requirement for any future non-oracle claim

Required form:

`authorized pre-localization source -> candidate input value`

Trace must be deterministic and replayable, and must not pass through:

- oracle activation;
- necessary-set identities;
- evaluation outcomes;
- post-localization state;
- fixture-specific answer encoding;
- equivalent indirect routes.

This is a provenance requirement only. It does not define the transformation or authorize an input.

## 8) Gate B `X_t` classification (preserved)

Gate B `X_t` was an experimental surrogate. Fixture construction of `X_base` used privileged single-group coverage knowledge derived from `R_necessary`. The runtime selector received only `X_t`, group IDs, and `k`, making the decoding step information-restricted. That restricted decoder contract did not make generation of `X_t` a permitted production non-oracle source.

## 9) Availability versus sufficiency

- architecture may establish that information is present;
- separate authorization is required before localization use;
- separate experiment is required before sufficiency claims;
- an experimentally useful surrogate does not automatically become architecturally available;
- an architecturally available input does not automatically become sufficient.

## 10) Non-authorizations preserved

- localization source selection: **NOT AUTHORIZED**
- representation-family design: **NOT AUTHORIZED**
- new characterization: **NOT AUTHORIZED**
- implementation/execution: **NOT AUTHORIZED**
- HOW-2: **NOT AUTHORIZED**
- Gate C: **NOT AUTHORIZED**
- production selector: **NOT AUTHORIZED**
- Category/YAML integration: **NOT AUTHORIZED**

## 11) Authority references used by this contract

- [20.105_tp_requirements.md](../../../../../20.105_tp_requirements.md)
- [20.105.010_tp_meta_fields.md](../../../../../20.105.010_tp_meta_fields.md)
- [20.116_field_catalog.md](../../../../../20.116_field_catalog.md)
- [20.116.010_tp_envelope_index.md](../../../../../20.116.010_tp_envelope_index.md)
- [20.116.020_ownership_rw.md](../../../../../20.116.020_ownership_rw.md)
- [path_a_realization_charter.md](../../architecture/path_a_realization_charter.md)
- [idob_seam.md](../../architecture/idob_seam.md)

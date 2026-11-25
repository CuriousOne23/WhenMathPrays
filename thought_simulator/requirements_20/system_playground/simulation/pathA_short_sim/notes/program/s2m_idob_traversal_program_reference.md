# S2M IdOB Traversal Program Reference

**Date:** 2026-11-25  
**Status:** Implementation-facing mapping for current realization; non-normative.  
**Primary conceptual authority:** [s2m_idob_traversal_proposal.md](s2m_idob_traversal_proposal.md).  
**Normative boundaries:** [20.705_patha_pathb_flow.md](../../../20.705_patha_pathb_flow.md), [20.45_ts_isc_scoring.md](../../../20.45_ts_isc_scoring.md), [20.40.050_idob_prim.md](../../../20.40.050_idob_prim.md).  

## Purpose

Map the provisional traversal chain

`S_t → door → C_t → E_t → L_t → (D_t, Q_t) → B_t → P_t → H_t → continue / OuBA`

onto currently realized software/config/data surfaces, explicitly marking:

1. directly realizable surfaces;
2. experimentally derivable surfaces without semantic-policy change;
3. bounded observability gaps;
4. architecture-blocked surfaces.

This document does not define traversal architecture.

## Current realization anchors

- Runtime pipeline/order: [pathA_short_simulator.py](../../pathA_short_simulator.py)
- Category evidence/candidate/scoring path: [primitives_pathA_short.py](../../primitives_pathA_short.py) (`CEx`, `CE`, `ISc`, `TPU`)
- Seed and S2M meaning transfer: [idob/experimental_seed.py](../../idob/experimental_seed.py), [idob/experimental_meaning.py](../../idob/experimental_meaning.py), [s2m/loop.py](../../s2m/loop.py)
- Candidate inventory and active space: [s2m/data/associations/](../../s2m/data/associations/), [s2m/data/majors.yaml](../../s2m/data/majors.yaml), [s2m/data/spaces/default.yaml](../../s2m/data/spaces/default.yaml)
- Bounded legitimation table: [s2m/legitimate.py](../../s2m/legitimate.py)
- Existing replay controls: [support/tools/s2m_canonical_sentences_replay.py](../../support/tools/s2m_canonical_sentences_replay.py), [support/tools/s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py)

## Traversal-stage realization map

| Traversal stage | Current realization surface | Status | Notes / boundary |
|---|---|---|---|
| `S_t` | `s2m_seed.written_relations` and default meaning seed in [idob/experimental_seed.py](../../idob/experimental_seed.py) | **Directly realizable** | Structural relation is emitted for bounded canonical patterns only; empty otherwise. |
| `door` | No realized `structural_key -> meaning_group_candidates` map. `crossing_fields.structural_key` is null in seed. | **Blocked (unresolved architecture)** | Current code has no traversal-door contract for meaning groups. |
| `C_t` | `s2m_meaning.candidate_interpretations` from [s2m/propose.py](../../s2m/propose.py) over endpoint association files | **Directly observable (surrogate only)** | Finite candidate list exists, but it is endpoint-association based, not the proposal’s legal meaning-group set from a door map. |
| `E_t` correspondence (`+/-/0`) | Category cue support and candidate `selection_state` in [s2m/loop.py](../../s2m/loop.py) plus `meaning_relations` | **Partially observable; blocked for full contract** | Positive support-like effects are visible (`category_supported`, `legitimized`). Explicit opposition relation (`-`) is not represented as a declared correspondence primitive. |
| `L_t` provenance/dependency | Provenance fields in `CE`/`CEx` outputs and `qualification_observation` in `ISc` trace | **Provenance observable; dependency classification blocked** | No current Independent/Dependent/Unknown family classification mechanism. |
| `D_t=(S_t,O_t)` | No directional support/opposition ledger in current realization | **Blocked (unresolved architecture)** | Cannot compute proposal-level directional tuple without introducing new correspondence semantics. |
| `Q_t=(U_t,I_t)` | No dedicated unknown-dependency/internal-conflict qualifier tuple | **Blocked (unresolved architecture)** | Current outputs expose some cue provenance and refusal states, but not proposal-level `Q_t`. |
| `B_t=S_t-O_t` (provisional baseline) | Not computed in code | **Blocked by missing `D_t`** | Experimental baseline cannot be computed legitimately without realized `D_t`. |
| `P_t` normalization | `ISc` softmax distribution over category candidates (`category_weighted_distribution`) | **Directly observable for category scoring only** | This is not traversal-candidate normalization over door-legal `C_t`. |
| `H_t` over `P_t` | 20.45 defines entropy ownership; current category program reference marks nonconformance/open for entropy implementation | **Blocked / unavailable in current bounded realization** | `infra_smoke` characterization explicitly records entropy unavailable. |
| `continue / OuBA` | [primitives_pathA_short.py](../../primitives_pathA_short.py) `OuBA` sets path commit flag | **Blocked for traversal sufficiency rule** | No traversal-specific continue/exit sufficiency rule is defined here. |

## Experimental reach without semantic change

Allowed from current surfaces:

1. finite candidate-set observability under canonical seeded structures;
2. cue provenance observability (sentence vs prior context);
3. category-scoring distribution and deterministic ordering;
4. candidate state outcomes (`candidate_unselected`, `legitimized`, `refused`);
5. replay invariants via existing replay tools.

Not allowed without unresolved architecture decisions:

1. explicit opposition correspondence operator;
2. dependency-family classification policy;
3. directional tuple computation (`D_t`, `Q_t`);
4. traversal-baseline discrimination (`B_t`) and traversal-candidate normalization (`P_t`);
5. traversal entropy (`H_t`) and continue/OuBA sufficiency policy.

## Observability insufficiency statement (pre-instrumentation)

Current observability is insufficient to reconstruct proposal-level `E_t/L_t/D_t/Q_t/B_t/P_t/H_t` as defined in the traversal proposal because:

- no explicit correspondence primitive records `+/-/0` between evidence items and door-legal traversal candidates;
- no evidence-family identity/dependency model exists;
- no directional support/opposition tuple is produced;
- no proposal-level qualifier tuple is produced;
- no traversal-candidate normalization and entropy fields are produced.

Any future instrumentation must remain behaviorally inert and replay-safe and must not modify candidate construction, scoring semantics, Category Selection policy, IdOB commitments, or OuBA behavior.

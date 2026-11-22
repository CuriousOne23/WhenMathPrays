# Category Selection Stage-1 Current-Software Modification Map

## Status and authority

- **Status:** Stage-1 observation/mapping document (non-normative; not an implementation contract).
- **Authority split used in this map:**
  - Normative requirements authority: `20.45`, `20.105`, `20.116.010`, `20.40.050`.
  - Architectural proposal authority: [category_selection_proposal.md](category_selection_proposal.md).
  - Stage-1 objectives authority: [category_selection_research_plan.md](category_selection_research_plan.md).
  - Current software evidence authority: inspected code/data/log/test artifacts listed below.

## Purpose

Map what the current Path A short simulator actually contains that affects the category-selection research program, including where behavior appears generic/data-driven versus bounded scaffolding or category-specific procedure.

## Documents reviewed

- [category_selection_proposal.md](category_selection_proposal.md)
- [category_selection_research_plan.md](category_selection_research_plan.md)
- [category_structure_observation.md](category_structure_observation.md)
- [s2m_relational_proposal.md](s2m_relational_proposal.md)
- [s2m_program_reference.md](s2m_program_reference.md)
- [20.45_ts_isc_scoring.md](../../../20.45_ts_isc_scoring.md)
- [20.105_tp_requirements.md](../../../20.105_tp_requirements.md)
- [20.116.010_tp_envelope_index.md](../../../20.116.010_tp_envelope_index.md)
- [20.40.050_idob_prim.md](../../../20.40.050_idob_prim.md)
- [README.md](../../README.md)
- [user_guide.md](../../user_guide.md)

## Mapping method

1. Static inspection of runner/primitives/S2M/data/replay artifacts.
2. Trace-path inspection from cue entry through commit and S2M consumption.
3. Targeted baseline verification using existing replay tools only (no new fixtures, no edits).
4. Divergence recording where current realization differs from normative wording.

## Current high-level execution path

Observed execution order in [pathA_short_simulator.py](../../pathA_short_simulator.py) `PRIMITIVES`:

`InB -> IIInB -> IE -> CEx -> CE -> ISc -> TPU -> SOB -> SROB -> CnOB -> SmOB -> SSG -> RBU -> RB -> TR -> TRU -> RTU -> CTP -> IdOB -> OuBA`

Category/S2M relevant subpath in current short realization:

`CEx (prior cue) + CE (sentence/prior cue + category_candidate_set) -> ISc (score+distribution) -> TPU (optional commit to TP.semantic.isc_category_result when enable_category_selection=True) -> IdOB (sum + optional S2M attach) -> s2m.loop.apply (category result read from tp.semantic)`

## Category-evidence entry map

### Entry points

1. **Prior-context cue path**
   - Evidence source: `tp.prior_context` (set by `run_pathA_short(...)`).
   - Extraction: [primitives_pathA_short.py](../../primitives_pathA_short.py) `CEx`.
   - Mapping data: [support/dictionaries/category_cues.yaml](../../support/dictionaries/category_cues.yaml) `prior_context`.
   - Output structure: `tp.cex_output = {"category_cue": [...], "provenance": {...}}`.
   - Provenance fields written: `source`, `origin`, `prior_context_used`.
   - Label: **Existing data-driven behavior**.

2. **Sentence-internal cue path**
   - Evidence source: `tp.raw_text`.
   - Extraction: [primitives_pathA_short.py](../../primitives_pathA_short.py) `CE`.
   - Mapping data: [support/dictionaries/category_cues.yaml](../../support/dictionaries/category_cues.yaml) `sentence_internal`.
   - Output structure: `tp.ce_output["category_cue"]`, plus `cue_provenance` list.
   - Label: **Existing data-driven behavior**.

3. **Combined CE output for scorer**
   - `tp.ce_output["category_candidate_set"]` built by iterating `load_majors()` and deriving `f_s/f_b/f_e/f_i` per major in [primitives_pathA_short.py](../../primitives_pathA_short.py) `CE`.
   - Candidate shape includes major-specific feature slots and is consumed by `ISc`.
   - Label: **Candidate scaffolding — requires review** (major-level synthetic candidate set in CE, not endpoint/candidate inventory).

### Provenance carriage at entry

- CEx provenance is explicit in `tp.cex_output.provenance`.
- CE summarizes provenance in `cue_provenance` (sentence/prior_context_cex).
- No token-level provenance for category-cue extraction is recorded on CE/ISc path.

## Category knowledge: data versus procedure

### YAML/data artifacts

- Cue marker -> majors map: [support/dictionaries/category_cues.yaml](../../support/dictionaries/category_cues.yaml).
- Scoring weights (`w_s,w_b,w_e,w_i,w_cat`): [support/dictionaries/isc_weights.yaml](../../support/dictionaries/isc_weights.yaml).
- Known majors: [s2m/data/majors.yaml](../../s2m/data/majors.yaml).
- Active space list: [s2m/data/spaces/default.yaml](../../s2m/data/spaces/default.yaml).
- Endpoint association inventory (candidate interpretations): [s2m/data/associations/](../../s2m/data/associations).

Labels: **Existing data-driven behavior**.

### Generic procedural logic

- Cue extraction by substring match (`marker in lowered`): `_extract_category_cues_from_text` in [primitives_pathA_short.py](../../primitives_pathA_short.py).
- ISc additive scoring + softmax normalization in `ISc` function.
- S2M candidate proposal from endpoint YAMLs in [s2m/propose.py](../../s2m/propose.py).
- S2M state progression (`candidate_unselected -> category_supported -> legitimized/refused`) in [s2m/loop.py](../../s2m/loop.py).

Label: **Existing generic mechanism** (within current bounded design).

### Category-specific or bounded procedural behavior

- Direct `major in cue_set` indicator term in ISc (`w_cat * indicator`) in [primitives_pathA_short.py](../../primitives_pathA_short.py) `ISc`.
- S2M selection space narrowed to `[top_category]` when top category is present and in active/proposed majors in [s2m/loop.py](../../s2m/loop.py).
- Licensed extension tuples are hardcoded constant table in [s2m/legitimate.py](../../s2m/legitimate.py) `LICENSED_EXTENSIONS`.
- Seed relation generation is canonical-utterance-specific rule logic in [idob/experimental_seed.py](../../idob/experimental_seed.py) `_build_written_relations`.

Labels: **Category-specific procedural behavior** / **Candidate scaffolding — requires review**.

## Direct major-matching map

Direct major identity dependencies found:

1. `ISc` indicator:
   - `indicator = 1.0 if major in cue_set else 0.0`
   - Score term uses exact major identity with `w_cat`.
   - Evidence: [primitives_pathA_short.py](../../primitives_pathA_short.py) `ISc`.
   - Classification: **Normative correspondence found (20.45 additive indicator form)** + **Existing direct major match**.

2. CE candidate set built per `load_majors()`:
   - Major identity determines candidate rows and feature slots.
   - Evidence: [primitives_pathA_short.py](../../primitives_pathA_short.py) `CE`.
   - Classification: **Bounded simulator scaffolding**.

3. S2M relevance gating by major:
   - proposal major compared to selected space/top category.
   - Evidence: [s2m/loop.py](../../s2m/loop.py).
   - Classification: **Category-specific procedural behavior**.

4. Active space filtering by majors list:
   - `resolve_active_space` filters requested majors against known majors.
   - Evidence: [s2m/active_space.py](../../s2m/active_space.py).
   - Classification: **Existing generic mechanism**.

No evidence found that major matching is abstracted beyond string equality in current path.

## Candidate inventory map

### Sources

1. **ISc scoring candidate set (category-level)**
   - Built in CE from majors (one candidate row per major) with `f_s/f_b/f_e/f_i`.
   - Source function: [primitives_pathA_short.py](../../primitives_pathA_short.py) `CE`.

2. **S2M interpretation candidates (endpoint-level)**
   - Loaded from endpoint YAML association files via [s2m/loader.py](../../s2m/loader.py) `load_endpoint_associations`.
   - Proposed from seed endpoints in [s2m/propose.py](../../s2m/propose.py).
   - Recorded under `candidate_interpretations` in [s2m/record.py](../../s2m/record.py).

### Changeability from data

- Adding/removing endpoint associations for existing endpoints is data-only (YAML under [s2m/data/associations/](../../s2m/data/associations)).
- Adding a new endpoint association file is data-only if endpoint appears in seed written relations.
- Adding/removing majors currently affects:
  - CE candidate_set row creation (via majors data),
  - active-space resolution,
  - possible cue mapping (if marker maps provided),
  - but may also require updating cue map and possibly licensed tuples depending on behavior target.

### Code-change dependence observed

- Category expansion can require code-neutral path for scoring rows (major list driven), but extension participation still constrained by hardcoded licensed tuples in [s2m/legitimate.py](../../s2m/legitimate.py).
- Seed endpoint coverage currently depends on canonical utterance pattern logic in [idob/experimental_seed.py](../../idob/experimental_seed.py), which is not fully data-driven.

## Licensed-region / S2M scaffolding map

Current licensed-region mechanism:

- Store: hardcoded `LICENSED_EXTENSIONS` dict in [s2m/legitimate.py](../../s2m/legitimate.py).
- Key: structural relation string (`is`, `is_on`, `queries_location_of`).
- Value: exact `(from, relation, to)` tuple list.
- Lookup: `relation_is_licensed = structural_relation in LICENSED_EXTENSIONS`; if licensed relation, only listed tuples pass.
- Decision:
  - cue inactive -> immediate no legitimization.
  - cue active + major in active_space + tuple licensed -> legitimized.
  - cue active + major supported but tuple not licensed -> excluded, then marked `refused` in [s2m/loop.py](../../s2m/loop.py).

Classification: **Candidate scaffolding — requires review** (explicit bounded fixture, exact tuples).

## ISc category-scoring map

Evidence: [primitives_pathA_short.py](../../primitives_pathA_short.py) `ISc`.

### Implemented

- Inputs: `tp.ce_output.category_candidate_set`, `tp.ce_output.category_cue`.
- Features: `f_s`, `f_b`, `f_e`, `f_i`.
- Weights: loaded from [support/dictionaries/isc_weights.yaml](../../support/dictionaries/isc_weights.yaml).
- Category indicator: `1[major in cue_set]`.
- Score: weighted linear combination + category term.
- Normalization: softmax with max-subtraction.
- Output fields:
  - `category_cue`
  - `category_weighted_distribution` (major, probability, category_hit)
  - `top_category` (or null if cue_set empty)
  - `category_confidence`
  - `category_rationale`
  - `provenance` (`source`, `upstream`, `weights`)
- Determinism aids:
  - cue ordering via `_ordered_unique` and sorted cue output;
  - distribution sorted by `(-probability, major)` for tie stability.

### Partially implemented / represented differently / absent

- **Entropy:** not implemented in ISc output path.
- **Explicit top-vs-second margin field:** not emitted (derivable from distribution externally).
- **Explicit candidate rationale per-candidate term breakdown:** not emitted beyond `category_hit`.
- **Cue-less behavior:** implemented as forced `top_category = None`, `category_confidence = 0.0`, rationale includes `empty_category_cue`.

Classification:
- **Normative correspondence found:** additive category cue term + distribution/top/confidence/rationale output.
- **Short-realization divergence:** no entropy/ΔH exposure in this short path.

## Merge / TPU / TP handoff map

Evidence: [primitives_pathA_short.py](../../primitives_pathA_short.py) `TPU`, and [tp_substrate.py](../../tp_substrate.py).

- `merge_output` is a condensed dict from `_merge_isc_output(tp)` containing `{"isc_output": ...}`.
- Commit to `TP.semantic.isc_category_result` occurs only when `enable_category_selection=True`.
- Current writer in short realization: `TPU` function directly.
- Fields committed match ISc output subset (`category_cue`, distribution, top, confidence, rationale, provenance).
- Immutability in practice:
  - guarded by `if "isc_category_result" not in semantic_block` (single write within one run unless pre-populated).
  - no other writer found for `isc_category_result` in inspected path.
- Provenance survives from CE/ISc into committed block as summary source list + weights.

Classification: **Short-realization divergence** (condensed Merge/TPU representation, direct in-function merge model).

## IdOB / S2M consumption map

Evidence: [idob/experimental_meaning.py](../../idob/experimental_meaning.py), [s2m/loop.py](../../s2m/loop.py), [s2m/record.py](../../s2m/record.py).

- IdOB attaches S2M additively when `enable_s2m_seed=True`:
  - seed from [idob/experimental_seed.py](../../idob/experimental_seed.py),
  - meaning from `s2m.loop.apply`.
- S2M reads category result through `_category_result(tp)` from `tp.semantic.isc_category_result`.
- Read-only behavior observed:
  - inspected S2M path reads committed category block and does not write back to `tp.semantic.isc_category_result`.
- Relevance vs legitimation separation:
  - relevance stage sets `selection_state = category_supported` when proposal major in selected space.
  - legitimation stage applies licensed-region constraints.
  - post-check marks `selection_state` as `legitimized` or `refused`.
  - final participating extensions written only from legitimized set by [s2m/write.py](../../s2m/write.py).

Bypass check:
- No direct path found in inspected category/S2M flow where category support immediately writes meaning_relations without legitimation.

## Structural non-mutation findings

Evidence path:

- Category cue/scoring/commit code is in correction macro (`CEx`, `CE`, `ISc`, `TPU`) before structural OB-set stages in [pathA_short_simulator.py](../../pathA_short_simulator.py).
- S2M writes additive fields (`tp.s2m_seed`, `tp.s2m_meaning`) in [primitives_pathA_short.py](../../primitives_pathA_short.py) `IdOB`.
- No inspected code writes back from category/S2M path into SOB/SROB/CnOB/SmOB-owned structural fields after they are produced.

Observed relation:
- **Read-only relationship** from committed category block to S2M consumption.
- **No direct structural mutation found** from category-selection code path.

## Provenance trace

Observed trace:

`source evidence (raw sentence / prior_context)`
-> `CEx/CE category_cue extraction`
-> `ISc scoring provenance`
-> `TP.semantic.isc_category_result.provenance`
-> `s2m_meaning.cue_state.provenance`
-> `candidate_interpretations selection_state`

Per transition:

- source evidence -> category cue: **transformed/summarized** (marker-match extraction).
- category cue -> scoring: **retained/summarized** (`source` list + weights).
- scoring -> committed result: **retained** (copied fields in TPU).
- committed result -> candidate relevance: **retained but reduced to cue/top usage in loop selection logic**.
- candidate relevance -> final meaning relations: **category provenance not copied into each written meaning relation item** (relations carry from/relation/to/major/subcategory/legitimized).

## Existing observability map

### Present observability

Primary output surfaces:

- [run_examples.py](../../run_examples.py):
  - labeled category observation blocks with:
    - CEx cue/provenance
    - CE cue + candidate set
    - ISc scoring/result
    - TPU merge handoff + commit payload
    - committed `TP.semantic.isc_category_result`
    - S2M cue_state consumption
    - candidate interpretation states
    - meaning_relations
    - default-vs-selected output
- [run_phase4_obs_1.txt](../../run_phase4_obs_1.txt), [run_phase4_obs_2.txt](../../run_phase4_obs_2.txt): captured examples of the above.
- `trace` entries in `run_pathA_short` include primitive-level `cex_output`, `ce_output`, `isc_output`, `merge_output`, `isc_category_result`.

### Directly observable now

- cue values
- cue provenance source summary
- category candidate set features (`f_s/f_b/f_e/f_i`)
- normalized category distribution
- top category
- confidence
- rationale
- committed TP category result
- candidate relevance states
- legitimized/refused states
- final participation (`meaning_relations`)
- default-only outcome

### Observable gaps

- no explicit entropy output
- no explicit top-to-second margin output (derivable externally)
- no explicit per-candidate rationale decomposition beyond `category_hit`
- no explicit unsupported-inventory classifier field

## Current unsupported/no-category behavior

Evidence from code and replay outputs:

- A. **No cue**:
  - `top_category = null`, `category_confidence = 0.0`, rationale includes `empty_category_cue`, S2M extensions remain empty.
  - Evidence: `ISc` in [primitives_pathA_short.py](../../primitives_pathA_short.py), replay in [support/tools/s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py).

- B. **Weak/ambiguous evidence**:
  - Current path always computes a distribution over majors when candidate_set exists; no separate ambiguity-class output field found.
  - Distinction appears limited to resulting distribution/confidence and downstream legitimation result.
  - Classification: **Unable to determine statically** for richer ambiguity semantics beyond these fields.

- C. **No applicable candidate**:
  - Category may support proposals, but licensed-region gating can refuse all, yielding empty meaning_relations with `refused` candidate states.
  - Evidence: [s2m/loop.py](../../s2m/loop.py), [s2m/legitimate.py](../../s2m/legitimate.py), replay assertions.

- D. **Apparently relevant category absent from inventory**:
  - If cue names major not present in active/proposal majors intersection, no proposal is category_supported; behavior degrades to unselected/refused outcomes depending on path.
  - No explicit unsupported-inventory label found.

- E. **Competition among available categories**:
  - Softmax distribution includes all CE major candidates; top category chosen by highest probability then major-name tie-break order.
  - If cue_set empty, top forced null despite distribution existence.

No explicit no-category decision function object found beyond the current empty-cue/null handling and downstream refusal/default-only outcomes.

## Sequential-state baseline

Observed baseline: **stateless recomputation per run** for category path.

- `run_pathA_short` initializes a new TP each call.
- No retained prior category state between runs in inspected path.
- No smoothing/persistence/hysteresis logic found for category results across runs.
- `prior_context` affects current run only through explicit input list.

## Determinism and replay map

### Existing mechanisms

- Deterministic primitive order in [pathA_short_simulator.py](../../pathA_short_simulator.py) `PRIMITIVES`.
- Deterministic cue extraction and ordered uniqueness helper.
- Stable distribution ordering in ISc (`(-probability, major)`).
- Deterministic registry digest / ordered loading in [idob/registry.py](../../idob/registry.py).
- Replay fixtures/tools:
  - [support/tools/s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py)
  - [support/tools/s2m_canonical_sentences_replay.py](../../support/tools/s2m_canonical_sentences_replay.py)
  - [support/tools/s2m_meaning_replay.py](../../support/tools/s2m_meaning_replay.py)
  - [replay_parity_harness.py](../../replay_parity_harness.py)

### Baseline verification executed in Stage-1

- `python support/tools/s2m_category_selection_replay.py` -> passed
- `python support/tools/s2m_canonical_sentences_replay.py` -> passed
- `python replay_parity_harness.py --format json` -> pass

### Gaps

- No explicit random seed controls are needed/seen in inspected category path because no RNG usage was found.
- No dedicated category entropy replay fixture found (entropy field not present).

## Existing tests and fixtures

### Category/S2M-focused replays

- [support/tools/s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py)
  - Classification: **contract-oriented + regression fixture** for category cue, commit envelope, refusal/legitimation, determinism.
- [support/tools/s2m_canonical_sentences_replay.py](../../support/tools/s2m_canonical_sentences_replay.py)
  - Classification: **canonical demonstration + contract-oriented** (three-sentence default meaning/candidate baseline).
- [support/tools/s2m_meaning_replay.py](../../support/tools/s2m_meaning_replay.py)
  - Classification: **regression fixture** for additive S2M non-mutation.

### Evidence corpora

- [run_phase4_obs_1.txt](../../run_phase4_obs_1.txt), [run_phase4_obs_2.txt](../../run_phase4_obs_2.txt)
  - Classification: **experimental observation artifacts** (already-generated outputs).
- [regression_evidence/](../../regression_evidence) and [consolidation_evidence/](../../consolidation_evidence)
  - Classification: **regression/consolidation fixture artifacts** for broader path coverage.

### Other replay harness

- [replay_parity_harness.py](../../replay_parity_harness.py)
  - Classification: **contract-oriented deterministic intake/replay harness** (not category-specific but relevant to deterministic baseline).

## Architectural-generality map

Central relation mapped: `M(E,K) -> D_K`

Current observed decomposition:

- **M (mechanism-like parts):**
  - cue extraction helper logic,
  - ISc scoring equation and softmax,
  - TPU commit shape logic,
  - S2M relevance/legitimation state progression.

- **K (category/candidate space carriers):**
  - cue marker maps (`category_cues.yaml`),
  - major inventory (`majors.yaml`, active space YAML),
  - endpoint associations (S2M association YAMLs),
  - licensed tuple table (`LICENSED_EXTENSIONS` in code, not YAML).

### K -> K + X (add category X), static assessment

- Data-only touchpoints likely:
  - [support/dictionaries/category_cues.yaml](../../support/dictionaries/category_cues.yaml)
  - [s2m/data/majors.yaml](../../s2m/data/majors.yaml)
  - [s2m/data/spaces/default.yaml](../../s2m/data/spaces/default.yaml) (if activation needed)
  - relevant endpoint association YAML files under [s2m/data/associations/](../../s2m/data/associations)
- Code that appears unchanged for basic scoring loop:
  - `CE` per-major candidate row generation
  - `ISc` scoring mechanics
  - `s2m.propose`/`s2m.loader` generic YAML loading
- Code/tables likely requiring extension or review:
  - hardcoded licensed tuples in [s2m/legitimate.py](../../s2m/legitimate.py)
  - canonical seed relation builder in [idob/experimental_seed.py](../../idob/experimental_seed.py) for new structural relations/endpoints
- Fixed assumptions that may block pure data-only expansion:
  - seed relation derivation tied to specific canonical utterance patterns
  - licensed extension table not externalized to data

### K -> K - X (remove category X), static assessment

- Removing from major inventory likely reduces CE candidate rows and active space membership.
- Cue markers that still reference removed major would produce cue values with no matching CE major/proposal major intersection.
- S2M relevance may produce no supported proposals (default-only/refusal outcomes).
- No explicit unsupported-inventory diagnostic found for this case.

Overall classification:

- **Mixed architecture:** partially data-driven, with bounded category/scenario scaffolding in code.

## Candidate scaffolding requiring review

1. Hardcoded licensed extension table in [s2m/legitimate.py](../../s2m/legitimate.py).
2. Canonical utterance pattern seed builder in [idob/experimental_seed.py](../../idob/experimental_seed.py).
3. CE major-level synthetic candidate_set (not endpoint-derived candidate semantics).
4. `TPU` commit gated by runtime flag `enable_category_selection`.
5. Dead/unused IdOB contract helper path (`_idob_expected_override`) appears present but not called in inspected execution path.

## Gaps between research-plan needs and current observability

Compared to Stage-1 research-plan measurement needs:

- Entropy and explicit boundary metrics are not emitted on current category result path.
- No explicit top-second margin field (derivable but not first-class emitted value).
- No explicit B-vs-C separator output (weak/ambiguous support vs unsupported inventory).
- No explicit unsupported-inventory condition marker.
- Provenance is preserved at cue/result summary level, but not per-written-meaning-relation provenance lineage.

## Potential future modification locations

> This section is inventory only (no implementation instructions).

| Location | Present responsibility | Why it may matter later | Research-plan relevance | Normative linkage |
|---|---|---|---|---|
| [primitives_pathA_short.py](../../primitives_pathA_short.py) `CEx` | prior-context cue extraction + provenance summary | entry-path provenance, cue-source separability | provenance, boundary characterization | 20.45 cue-source usage context |
| [primitives_pathA_short.py](../../primitives_pathA_short.py) `CE` | sentence cue extraction + major candidate_set assembly | major-space behavior and `K` sensitivity | architectural generality (`K` variation) | 20.45 scorer inputs |
| [primitives_pathA_short.py](../../primitives_pathA_short.py) `ISc` | scoring/distribution/top/confidence/rationale | boundary behavior, ambiguity characterization, observability | confidence dimensions, measurement framework | 20.45 |
| [primitives_pathA_short.py](../../primitives_pathA_short.py) `TPU` | commit path to `semantic.isc_category_result` | commit ownership and immutability boundaries | contract measurements | 20.105, 20.116.010 |
| [s2m/loop.py](../../s2m/loop.py) | category-result consumption, relevance state transitions, refused/legitimized mapping | relevance vs legitimation separation | meaning-transition, preservation | 20.40.050 read-only cue use context |
| [s2m/legitimate.py](../../s2m/legitimate.py) | licensed-region gate via fixed tuple table | key bounded scaffolding for future boundary experiments | boundary/stability, architectural boundedness | proposal/s2m docs (bounded fixture) |
| [s2m/data/associations/](../../s2m/data/associations) | candidate interpretation inventory data | candidate-space expansion/removal tests | generalization/generality | proposal + research plan |
| [support/dictionaries/category_cues.yaml](../../support/dictionaries/category_cues.yaml) | cue marker-to-major mapping | cue-source experiments, withheld/add-as-data category probes | category-evidence entry | 20.45 cue feature context |
| [idob/experimental_seed.py](../../idob/experimental_seed.py) | canonical structural relation seed generation | determines which endpoints enter proposal inventory | architectural generality constraints | s2m program realization context |
| [run_examples.py](../../run_examples.py) | current observation/debug print surface | available observability for Stage-1 and later controlled runs | measurement/observation discipline | non-normative observation runner |
| [support/tools/s2m_category_selection_replay.py](../../support/tools/s2m_category_selection_replay.py) | deterministic replay assertions for category path | baseline contract verification | determinism/replay | regression evidence |

## Stage-1 findings

1. The short realization has a complete observable path from cue entry to S2M outcomes, including explicit refusal states.
2. Category knowledge is partly data-driven (cue maps, majors, associations, weights) and partly code-scaffolded (licensed tuples, seed relation builder).
3. Relevance and legitimation are separated in current S2M path; category support does not automatically produce extension writing.
4. Commit path for `isc_category_result` exists and appears single-writer in current inspected code.
5. Determinism tooling exists and passes for inspected baseline replay commands.
6. Observability is strong for cue/scoring/commit/relevance/refusal/participation, but explicit entropy/boundary-specific fields are absent.

## What Stage 1 does NOT establish

- It does not prove architectural generality.
- It does not define a no-category decision function.
- It does not select thresholds, hysteresis, or persistence mechanisms.
- It does not establish B-vs-C separability beyond currently exposed fields.
- It does not authorize implementation or requirements changes.

## Inputs required for the future coordinated software references

From this Stage-1 map, post-review drafting would need (after review):

1. Agreed list of bounded scaffolding to preserve vs isolate in experiments.
2. Explicit observability requirements for missing metrics/diagnostics (if any are approved later).
3. Confirmed experiment harness scope (which existing replay fixtures are reused as baseline checks).
4. Agreed treatment of seed-generation dependence on canonical utterance patterns.
5. Agreed change-accounting approach for any `K`-variation experiment.

Drafting responsibilities split across:

- [category_selection_program_reference.md](category_selection_program_reference.md): bounded category-selection realization contract.
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md): bounded characterization instrumentation, invocation, artifact-handling, and experimental-support contract.

## Review gate

Before expanding [category_selection_program_reference.md](category_selection_program_reference.md) and/or [category_selection_characterization_reference.md](category_selection_characterization_reference.md), review should explicitly confirm:

- Stage-1 findings accepted/rejected with rationale.
- Scaffolding items classified as intentional baseline versus candidate redesign targets.
- Observability gaps acknowledged (including entropy/boundary diagnostics) without silently filling them.
- Normative/current-realization divergences logged and accepted as current baseline facts.
- No implementation directives are inferred from this Stage-1 map alone.

## Post-review disposition addendum

Post-review disposition: Stage-1 findings feed two coordinated successor software references:

- [category_selection_program_reference.md](category_selection_program_reference.md) for the bounded category-selection realization contract.
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md) for bounded characterization instrumentation, invocation, artifact handling, and experimental support.

This disposition does not alter any Stage-1 factual findings recorded above.

## Category-selection document family

For the complete category-selection document map, document roles, authority relationships, software references, characterization documents, and observation records, see:

[category_selection_index.md](category_selection_index.md)

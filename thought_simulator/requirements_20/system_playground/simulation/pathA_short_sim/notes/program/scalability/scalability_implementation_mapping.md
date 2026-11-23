# Path A Scalability Implementation Mapping

**Document:** notes/program/scalability/scalability_implementation_mapping.md  
**Status:** Approved implementation mapping for first bounded scalability implementation.  
**Date:** 2026-11-23  
**Scope:** First implementation-mapping task required by [scalability_implementation_plan.md](scalability_implementation_plan.md). No runtime/tooling/test/schema behavior is implemented by this document.

## Inputs read (required order)

1. [scalability_program.md](scalability_program.md)  
2. [scalability_design.md](scalability_design.md)  
3. [scalability_gap_analysis.md](scalability_gap_analysis.md)  
4. [scalability_implementation_plan.md](scalability_implementation_plan.md)

## Review-directed mapping decisions (applied)

1. **Deterministic structural identity contracts are recorded below for currently supported proposal classes.**
2. **If qualification coverage cannot be established from explicit existing evidence, mapping mandates `unresolved` (no invented qualification registry).**
3. **Category/Major × Licensed Region behavior remains bounded to existing licensed-region scaffold semantics in [legitimate.py](../../../s2m/legitimate.py); no generalization is mapped.**
4. **Report representation remains provisional, while still satisfying the mandatory evidence contract from the implementation plan.**

## 1) Existing facilities to reuse

### Runtime and data surfaces
- S2M loaders for majors/active space/associations: [loader.py](../../../s2m/loader.py) (`load_majors`, `load_active_space`, `load_endpoint_associations`).
- Candidate proposal generation from endpoint associations: [propose.py](../../../s2m/propose.py) (`propose`).
- Category-conditioned active-space selection + candidate state transitions (`candidate_unselected`, `category_supported`, `legitimized`, `refused`): [loop.py](../../../s2m/loop.py) (`apply`).
- Licensed Region scaffolding (bounded tuple table): [legitimate.py](../../../s2m/legitimate.py) (`LICENSED_EXTENSIONS`, `legitimate`).
- Existing category/major cues and weights in dictionaries: [category_cues.yaml](../../../support/dictionaries/category_cues.yaml), [isc_weights.yaml](../../../support/dictionaries/isc_weights.yaml).

### Regression/replay/check infrastructure
- Existing replay/check style and scripts: [support/tools/](../../../support/tools/).
- Pipeline readiness check: [pipeline_readiness_check.py](../../../support/tools/pipeline_readiness_check.py).
- Category-selection replay: [s2m_category_selection_replay.py](../../../support/tools/s2m_category_selection_replay.py).
- Deterministic harness pattern for machine-readable replay output: [replay_parity_harness.py](../../../replay_parity_harness.py).

### Characterization artifact/persistence discipline
- Envelope and persistence behavior (canonical identity, non-overwrite): [artifacts.py](../../../characterization/artifacts.py) (`build_success_envelope`, `persist_success_envelope`, `find_existing_canonical_identity_artifact`).
- Characterization persistence replay pattern: [characterization_artifact_replay.py](../../../support/tools/characterization_artifact_replay.py).

### Local/generated-output conventions
- Local output ignore boundary pattern: [local_characterization/.gitignore](../../../local_characterization/.gitignore).
- Root ignore policy including `*.tschar.json` and local characterization subtree: [.gitignore](../../../../../../../../../.gitignore).

## 2) Proposed files/modules under `scalability/`

Proposed package (new):

- `scalability/__init__.py`
- `scalability/run.py`  
  Entry orchestration for proposal analysis run.
- `scalability/proposal.py`  
  Proposal YAML load + structural validation.
- `scalability/discovery.py`  
  Read established environment surfaces (dictionary, associations, majors, active space, licensed-region scaffold).
- `scalability/relationships.py`  
  `already_defined` / `missing` / `extension_of` / `additional_to` / `incompatible` classification.
- `scalability/dependencies.py`  
  Dependency alignment checks for supported classes.
- `scalability/obligations.py`  
  Compute first-pass progression obligations for Dictionary/Association/Major and derived Candidate surfaces.
- `scalability/qualification.py`  
  Qualification-state determination (`qualified`, `unqualified`, `deferred_bounded`, `unresolved`) using available records/evidence inputs.
- `scalability/regression.py`  
  Adapter that invokes existing replay/check infrastructure (no reinvention).
- `scalability/disposition.py`  
  `PROCEED` / `HOLD` / `REVISE` / `RETURN_TO_CHARACTERIZATION` decision assembly from evidence.
- `scalability/report.py`  
  Machine-readable + human/Agent-readable report assembly from one shared evidence model.
- `scalability/session_store.py`  
  Local scalability run/session identity and output-path utilities under `local_scalability/`.

## 3) Proposal-entry/run interface

Runner/interface inconsistency resolution against repository convention:
- Existing repository convention uses top-level `run_*.py` command runners (for example [run_examples.py](../../../run_examples.py)) with argparse-driven flags and explicit output routing.
- Mapping therefore proposes a top-level runner name aligned to that convention: `run_scalability.py` (not `scalability_run.py`).

First-pass interface (runner style analogous to [run_examples.py](../../../run_examples.py)):

- `python run_scalability.py --proposal-file <path> --session-id <id> --run-index <n> [--report-version <v>] [--run-regression]`

Required input contract mapping (from implementation plan):
- Proposal identity.
- Items with resource class, resource identity, proposed delta, provenance.
- Fail-closed on missing identity/structural content.

This interface has been implemented in the first bounded scalability pass.

## 4) Proposed support/reference files under `support/scalability/`

Necessary support/reference files (proposed):

- `support/scalability/examples/`  
  Optional tracked proposal examples used by replay tests/documentation.
- `support/scalability/README.md`  
  Explicit statement that example proposals are reference-only and not established resources.

Optional but likely useful (if accepted later):
- `support/scalability/contracts/proposal_input.notes.md`  
  Human-readable contract notes for proposal fields (non-schema, since report/schema freeze is out of scope).

## 4A) Deterministic structural identity contracts (currently supported proposal classes)

These contracts are mapped for first-pass supported proposal-capable classes only. They are deterministic comparison bases for identity-vs-delta handling in proposal analysis.

| Proposal class | Deterministic identity contract | Existing surface used |
|---|---|---|
| Dictionary entry mapping | `(scope, marker, major)` where `scope ∈ {sentence_internal, prior_context}` and `marker/major` are normalized lowercase strings | [category_cues.yaml](../../../support/dictionaries/category_cues.yaml) |
| Association entry | `(endpoint, relation, to, major, subcategory?)` where `endpoint` comes from association file identity and tuple fields are normalized strings; `subcategory` is optional but identity-significant when present | [s2m/data/associations/](../../../s2m/data/associations/), [loader.py](../../../s2m/loader.py) |
| Major/category membership | `major` normalized lowercase string | [majors.yaml](../../../s2m/data/majors.yaml), [default.yaml](../../../s2m/data/spaces/default.yaml) |
| Candidate (derived surface, not proposal-capable) | `(from, relation, to, major, subcategory?)` as generated from associations through existing proposal logic | [propose.py](../../../s2m/propose.py), [loop.py](../../../s2m/loop.py) |

Notes:
- No independent Candidate proposal class is introduced.
- Seed and generalized Licensed Region identity contracts remain intentionally unresolved/out of scope for first pass.

## 5) Stage-to-existing-function/module dependency mapping

| Scalability stage (plan) | Existing function/module dependencies to reuse | Notes |
|---|---|---|
| 1. Read/validate proposal YAML | `yaml.safe_load` pattern from [loader.py](../../../s2m/loader.py) | Proposal parser is new, YAML handling pattern is reused. |
| 2. Identify deltas | Established surfaces from [category_cues.yaml](../../../support/dictionaries/category_cues.yaml), [majors.yaml](../../../s2m/data/majors.yaml), [default.yaml](../../../s2m/data/spaces/default.yaml), [associations/*.yaml](../../../s2m/data/associations/) | Delta logic is new; sources are existing. |
| 3. Discover existing related definitions | [loader.py](../../../s2m/loader.py), [legitimate.py](../../../s2m/legitimate.py) (`LICENSED_EXTENSIONS`) | Distinguish missing vs discovery-failed in new logic. |
| 4. Classify relationships | Existing data + contract terms from [scalability_design.md](scalability_design.md) | Classification implementation is new, data sources are existing. |
| 5. Evaluate dependencies | Existing resource relations in loaders + proposal items | Dependency checker is new. |
| 6. Compute `$O_Δ` | Candidate derivation via [propose.py](../../../s2m/propose.py), active-space constraints via [active_space.py](../../../s2m/active_space.py), licensing gate via [legitimate.py](../../../s2m/legitimate.py) | Progression computation is new but should call existing candidate/licensing surfaces. |
| 7. Determine qualification state | Existing characterization records under [local_characterization/](../../../local_characterization/) and formal docs (for bounded interpretation) | If explicit coverage evidence is absent or ambiguous, return `unresolved`; no invented qualification registry. |
| 8. Invoke regression | Existing scripts in [support/tools/](../../../support/tools/), notably [pipeline_readiness_check.py](../../../support/tools/pipeline_readiness_check.py) and [s2m_category_selection_replay.py](../../../support/tools/s2m_category_selection_replay.py) | Use adapter/subprocess orchestration; do not re-implement regressions. |
| 9. Evaluate boundary + disposition | Decision framework in [scalability_program.md](scalability_program.md) + evidence from stages 4–8 | Disposition assembly is new. |
| 10. Emit findings/reports | Local artifact/persistence discipline pattern from [artifacts.py](../../../characterization/artifacts.py) and ignore conventions in [.gitignore](../../../../../../../../../.gitignore) | Scalability report writer/session store is new but should mirror proven persistence/identity discipline. |

## 6) Proposed report/session output structure under `local_scalability/`

Proposed structure (mirrors characterization locality discipline):

```
local_scalability/
  .gitignore
  sessions/
    <session_id>/
      runs/
        <run_index>__scalability_check__<version>.json
        <run_index>__scalability_check__<version>.md
```

Proposed report identity fields:
- `session_id`
- `run_index`
- `proposal_id`
- `scalability_type` (bounded first-pass value)
- `version`
- creation timestamp

Proposed report body groups (from design/plan):
- proposal/item identity + delta,
- relationship classifications with evidence,
- dependencies/missing support,
- progression obligations,
- qualification states,
- regression (separate),
- findings in ORIGIN→WHERE→WHAT→WHY→EVIDENCE→CONSEQUENCE→ROUTE shape,
- final disposition.

Report-field naming remains provisional in this mapping; only mandatory evidence content is fixed by [scalability_implementation_plan.md](scalability_implementation_plan.md).

## 7) Required `.gitignore` changes

Implemented in the first bounded pass:

- `thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_scalability/*`
- `!thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/local_scalability/.gitignore`
- Optional defensive pattern for report class (if introduced): `*.tsscale.json` (name provisional).

## 8) Proposed tests and acceptance-test mapping

Existing test style in this area is replay/check scripts under [support/tools/](../../../support/tools/) rather than pytest package tests. Proposed first-pass scalability tests follow that convention.

### Proposed new test files (mapping only)
- `support/tools/scalability_proposal_replay.py`
- `support/tools/scalability_progression_replay.py`
- `support/tools/scalability_seed_hold_replay.py`
- `support/tools/scalability_output_boundary_replay.py`

### Acceptance test to proposed test mapping

| First-pass acceptance requirement (implementation plan) | Proposed test coverage |
|---|---|
| Existing identity + relation ⇒ `already_defined`, no false progression obligations | `scalability_proposal_replay.py::case_already_defined_no_false_obligation` |
| New dictionary key→cue mapping yields new relation + obligations; does not equate green regression with qualification | `scalability_progression_replay.py::case_new_dictionary_mapping_obligation_and_disposition` |
| Extend existing dictionary word with new category ⇒ `extension_of` notification | `scalability_proposal_replay.py::case_dictionary_extension_of` |
| Add association entry and enumerate newly reachable candidate proposals | `scalability_progression_replay.py::case_association_expansion_candidate_derivation` |
| Add major and show downstream eligibility consequences | `scalability_progression_replay.py::case_major_expansion_eligibility` |
| Generalized seed expansion proposal ⇒ unresolved finding + `HOLD` | `scalability_seed_hold_replay.py::case_seed_generalization_hold` |
| Generated output under `local_scalability/` and untracked | `scalability_output_boundary_replay.py::case_local_scalability_ignored` |
| Proposal input never written into established Path A resources | `scalability_output_boundary_replay.py::case_no_write_to_established_resources` |

## 9) Implementation-plan elements not fully mappable onto existing code at mapping time

1. **Qualification-boundary lookup is not machine-encoded today.**  
   Mapping resolution: use explicit existing evidence when present; otherwise emit `unresolved` (no invented qualification registry).

2. **Cross-surface dependency-closure semantics are not currently implemented as one callable.**  
   Existing checks are localized (schema/loader/replay), not unified for scalability dependency closure.

3. **Progression obligation computation (`$O_Δ`) is not currently implemented.**  
   Candidate/association/licensing surfaces exist, but obligation-set construction across proposal deltas is new.

4. **No existing scalability session/report writer at mapping time.**  
   Characterization artifact handling exists and is reusable by pattern, but not directly reusable as-is without adaptation.

## 10) Items that would require unresolved-contract invention if forced now

If implemented without additional review constraints, the following would risk architectural invention:

1. **Formal machine-readable mapping from obligations to qualification boundaries**  
   (needed for deterministic `qualified` vs `unqualified` vs `deferred_bounded` vs `unresolved`).

2. **Precise generalized rule for deriving valid progression combinations when Licensed Region and Category/Major both change**  
   beyond current bounded `LICENSED_EXTENSIONS` scaffold. First-pass mapping explicitly does not generalize this.

3. **Normative report-field schema freeze**  
   explicitly out of scope in current authorities.

These are recorded as mapping risks and should be resolved by review decisions, not autonomous invention.

## Proposed implementation structure summary (non-binding)

- Create a new `scalability/` runtime package with orchestration + stage modules.
- Reuse existing S2M loaders/proposal/licensing/replay infrastructure and characterization persistence conventions.
- Keep Seed generalized expansion as unresolved-route `HOLD` only.
- Treat Candidate as derived only (no independent proposal class).
- Keep Licensed Region bounded to existing scaffolding behavior; report boundary crossings rather than inventing generalized licensing machinery.

---

**Review gate:** Mapping review is complete; this document is approved as the first bounded implementation mapping authority.

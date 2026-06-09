# 40.160_tp_lifecycle / software_description.md

## Approval State

- Legacy baseline: **approved** (pre–Two-Phase policy migration)
- **W3 Phase A** (40.510-402 targeted redo): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- W3 Phase B (intake repair fields; `commit_id` boundary alignment): **cleared to start** — pending implementation
- Program row: **40.510-402** (W3)

## W3 Targeted Redo Scope (40.510-402)

Per [40.510](../40.510_refactor.md) and [20.105](../../20_requirements/20.105_tp_requirements.md), Phase B SHALL extend the existing TP macro to support:

- Track H **intake-bound** repair fields (IIInB write set per 20.38 §6; no `semantic_core` / `TP.TR`)
- Lane-local carrier semantics aligned with normative A-chain ([20.36](../../20_requirements/20.36_canonical_end_to_end_trace.md) §2.1)
- `commit_id` boundary awareness — TP drafts post-`mtp_update` MUST NOT alter committed snapshot for same cycle
- Handoff shapes for [40.170](../40.170_split_merge_prototypes/software_description.md) split/merge and [40.190](../40.190_rb_prototypes/software_description.md) routing

**Agreement Statement (W3 Phase A)**: Aligned — CP review 2026-06-08 confirms W3 targeted redo scope (intake-bound repair fields, `commit_id` boundary, lane-local A-chain semantics, 40.170/40.190 handoffs) with no structural defects. Legacy macro API and `tp_lifecycle_io_schema_v1` remain valid; Phase B delta scoped to 20.105 §3.4 + 20.101 handoff only.

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 redo scope vs 40.510-402 | Pass |
| Two-phase model (stop after Phase A) | Pass |
| 20.105 / 20.101 / 20.38 §6 intake-bound writes | Pass |
| `commit_id` boundary (no post-commit draft mutation) | Pass |
| Macro purity + harness entrypoint preserved | Pass |
| Schema bump required | No — `tp_lifecycle_io_schema_v1` stands |
| Blockers | **None** — Phase B authorized |

## Two-Phase Execution Model (Global 40.* Rule)

- Phase A: generate and review `software_description.md` only.
- Mandatory stop after Phase A until explicit human approval.
- Phase B (only after approval): `prototype.py`, `harness.py`, `verification_capsule.md`, `requirements_delta.md`, and artifacts.

## 1. Purpose
The purpose of the TP is to record the thought processing it undergoes.

The canonical system requirements for the TP are defined in `thought_simulator/20_requirements/20.105_tp_requirements.md`.

This module explores and prototypes the **ThoughtPoint (TP) lifecycle** - the atomic, mobile unit of thought in the Thought Manifold Simulator.

A ThoughtPoint carries identity, entropy, provenance, and relational state as it moves, splits, merges, and evolves.

## 2. Scope & Alignment with Master Guide
- `prototype.py` must be a **pure macro-style module** (self-contained, importable, no top-level execution, deterministic when `deterministic_mode=True`).
- `harness.py` is the **sole execution entrypoint** - it imports the macro, runs verification scenarios, collects evidence, and attaches to requirements.
- All work follows `40.05_master_program_guide.md` (philosophy, variable control, macro rules, reporting standards, Verification Capsule process).

## 3. Core Responsibilities (from GRP)
- Carry and metabolize unified entropy (H_rep, H_pred, H_struct)
- Maintain strict identity, monotonic state_counter, and observable provenance/history
- Support movement between basins
- Enable safe split/merge with lineage tracking
- Provide rich observability (history, metrics, state dumps)
- Remain lightweight, deterministic, and parallel-safe

## 4. Key Invariants
- Unique `tp_id` + strictly monotonic `state_counter`
- Entropy components stay non-negative
- Provenance tree is immutable after creation events
- No TP can be in two basins simultaneously
- All public operations are deterministic when `deterministic_mode=True`
- History is append-only (bounded in future iterations)

## 5. Formal Requirement Pointers
High-level requirements live in:
- `00_program_governance/10_architecture/` (Manifold, TP, Basins)
- `20_requirements/` (Lifecycle, Entropy, Identity/Provenance, Stability)

Traceability will be maintained in `verification_capsule.md` and `requirements_delta.md`, with shared vocabulary defined in `../../30_verification/30.30_verification_glossary.md`.

## 6. Public Macro API (prototype.py)
```python
ThoughtPoint.new(
	basin_id,
	entropy,
	embedding,
	created_at_tick,
	energy=1.0,
	created_from="seed",
	deterministic_mode=True,
	deterministic_nonce=0,
	tp_id=None,
)
tp.move_to_basin(basin_id, tick, note="")
tp.update_entropy(tick, d_rep=0, d_pred=0, d_struct=0)
tp.add_tag(tag, tick)
tp.remove_tag(tag, tick)
tp.split(tick, child_count=2) -> list[ThoughtPoint]
tp.rb_should_route_to_tr() -> bool
tp.run_tr_routine(tick, success=True, tr_payload=None, error_note="") -> bool
ThoughtPoint.merge(
	sources: list[ThoughtPoint],
	tick,
	basin_id=None,
	deterministic_mode=True,
) -> ThoughtPoint
tp.to_dict() -> dict
```

## 7. Prototype IO, Formatting, and Variable Identity Contract

This section is the module-level contract for how `prototype.py` accepts inputs, produces outputs, and names/interprets state variables for interoperability with other programs.

### 7.1 Input Variables (Inbound IO)

| Function | Input Variable | Type | Required Attributes | Function Role |
|---|---|---|---|---|
| `ThoughtPoint.new` | `basin_id` | `str` | non-empty, stable domain label | Initial basin assignment for lifecycle routing |
| `ThoughtPoint.new` | `entropy` | `EntropyComponents` | each component non-negative | Initial TP entropy state |
| `ThoughtPoint.new` | `embedding` | `Iterable[float]` | numeric, finite, consistent dimensionality | Vector state used by downstream basin/routing logic |
| `ThoughtPoint.new` | `created_at_tick` | `int` | `>= 0` | Temporal identity anchor |
| `ThoughtPoint.new` | `energy` | `float` | finite, expected `>= 0` | Relative TP activity/mass budget |
| `ThoughtPoint.new` | `deterministic_mode` | `bool` | explicit True/False | Enables deterministic identity behavior |
| `ThoughtPoint.new` | `deterministic_nonce` | `int` | stable value for reproducible creation variants | Deterministic tie-break for equivalent inputs |
| `ThoughtPoint.new` | `tp_id` | `str | None` | UUID-like when provided | External ID override for integration/replay |
| `move_to_basin` | `basin_id` | `str` | non-empty | Target basin transition |
| `move_to_basin` | `tick` | `int` | monotonic in caller flow | Event timestamp |
| `update_entropy` | `d_rep`, `d_pred`, `d_struct` | `float` | finite values | Entropy delta application |
| `add_tag` / `remove_tag` | `tag` | `str` | non-empty, semantically stable label | Metadata identity and control |
| `split` | `child_count` | `int` | `>= 2` | Deterministic branching cardinality |
| `merge` | `sources` | `list[ThoughtPoint]` | non-empty, equal embedding dimensions | Deterministic TP convergence inputs |

### 7.2 Output Variables (Outbound IO)

| Function | Output | Type | Required Attributes | Consumer Use |
|---|---|---|---|---|
| `ThoughtPoint.new` | ThoughtPoint instance | `ThoughtPoint` | initialized `tp_id`, `state_counter=1`, creation history entry present | Harness scenario setup and other module orchestration |
| `split` | children | `list[ThoughtPoint]` | length equals `child_count`, parent provenance recorded, energy partitioned | Branch simulation, regulator flow, batch experimenting |
| `merge` | merged TP | `ThoughtPoint` | merge provenance includes all source ids, deterministic id when enabled | Convergence simulation and reduction workflows |
| `to_dict` | serialized state | `dict[str, object]` | JSON-serializable primitives/lists/maps | Inter-program exchange, logging, artifact persistence |

### 7.3 Variable Identity and Semantics

- `tp_id`: persistent TP identity token across lifecycle events.
- `state_counter`: strictly monotonic per TP; increments on each mutating operation.
- `current_basin_id`: exclusive basin membership label at current state.
- `tr_needs_update`: boolean dirty flag controlling RB -> TR invocation eligibility.
- `TR`: semantic routing block committed by successful TR routine execution.
- `entropy.h_rep`, `entropy.h_pred`, `entropy.h_struct`: non-negative entropy components.
- `history`: append-only event chronology for audit and replay.
- `provenance.parent_ids`, `provenance.merge_sources`, `provenance.split_children`: lineage identity channels.

### 7.4 Formatting and Interoperability Rules

- All public API inputs/outputs must use explicit named parameters in callers where practical.
- Serialized outputs from `to_dict` must remain JSON-compatible for tooling outside Python.
- Numeric arrays must be exported as plain numeric lists (no numpy-specific binary encoding).
- Field names must remain stable across module revisions or be versioned if changed.
- External programs should treat unknown future fields as optional (forward compatibility).

### 7.5 Cross-Program Applicability

The outbound `to_dict` payload is the canonical interchange format for:

- `harness.py` verification artifacts
- experiment runner inputs/outputs
- observability/log processing tools
- replay and snapshot comparison scripts

Any non-Python consumer should ingest this payload as schema-validated JSON and preserve `tp_id`, `state_counter`, `current_basin_id`, entropy components, and provenance fields without lossy transforms.

### 7.6 IO Schema Version and Compatibility Policy

- Current IO schema version: `tp_lifecycle_io_schema_v1`.
- Canonical producer: `ThoughtPoint.to_dict()` output consumed by harness artifacts.
- Required fields for compatibility:
	- `tp_id`
	- `current_basin_id`
	- `entropy.h_rep`, `entropy.h_pred`, `entropy.h_struct`, `entropy.total`
	- `state_counter`
	- `history`
	- `provenance`
- Backward compatibility rule:
	- New fields may be added as optional fields without breaking v1 consumers.
	- Existing required field names/types must not change within v1.
- Breaking change rule:
	- Renaming/removing required fields or changing semantic meaning requires schema version increment (v2+).
	- Producer and consumer docs must include migration notes.
- Deprecation window:
	- Keep prior schema support for at least one module iteration cycle after introducing a new version.
- Inter-program expectation:
	- External programs must preserve required fields exactly and ignore unknown optional fields.

### 7.7 Verification Structure and Artifact Layout

- Canonical verification report: `verification_capsule.md`
- Requirement evolution log: `requirements_delta.md`
- Canonical glossary: `../../30_verification/30.30_verification_glossary.md`
- Artifact directory: `artifacts/`

Required artifact expectations:

- `tp_state.json` for the current canonical deterministic run output
- `artifacts/determinism_run2.json` and `artifacts/determinism_run3.json` for reproducibility comparisons
- a failure artifact JSON payload only when a run fails and a failure payload exists

The verification capsule must migrate content from the legacy run-record, summary, and failure files without losing information.

The requirements delta file must preserve the prior requirement-change log and add any migration-related corrections.




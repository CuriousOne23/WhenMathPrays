# ouba_py_struc_pgm.md - OuBA Structural Program (Python Realization)

Document ID: ouba_py_struc_pgm
Version: 0.1 (First Crystallization)
Status: Draft - for CP review
Scope: Path-A Output Basin Primitive (OuBA-prm)
Location: thought_simulator/requirements_20/system_playground/primitives/ouba/
Companion code: ouba.py (to be realized from this program)

Normative parents:
- 20.40.060_ouba_prim.md (v2.1)
- 20.40.060.010_ouba_input_data_spec.md (v2.1)
- progressive_lineup_testing.md (v4.0+)

Informational companion:
- 20.40.060.700_ouba_field_ref.md

---

## 0. Purpose of This Structural Program

This document converts the OuBA normative HLR set and data specification into a deterministic Python realization plan.

It resolves four implementation-critical items:

1. Commit-layer ownership: exactly which fields OuBA may construct and emit.
2. Commit algorithm: deterministic freeze flow from TP snapshot to TPSnS.
3. Write-boundary discipline: explicit prohibition of Path-A recomputation and Path-B ownership writes.
4. Fidelity testing model: strict testbench equality vs general-mode rule validation.

This is a structural program, not a requirements document. Normative HLRs remain authoritative.

---

## 1. Python Module Shape (ouba.py)

### 1.1 Required surface

```python
PRIMITIVE_NAME = "ouba"

def process(tp: dict, mode: str = "general", **kwargs) -> dict:
	"""
	Main entry. Consumes final Path-A TP snapshot and returns a commit object
	containing TPSnS/CTP fields per pipeline convention.
	mode is injected by run.py / testbench ("testbench" | "general").
	"""
```

### 1.2 Internal structure (recommended)

```
ouba.py
|- extract_commit_view(tp)              # read-only extraction of commit-relevant fields
|- validate_commit_preconditions(view)  # required structure/invariants; fail-fast on violations
|- build_semantic_envelope(view)        # proposition_set, truth_evidence, tags, etc.
|- build_context_envelope(view)         # TP.next_context.* freeze
|- build_provenance_envelope(view)      # lineage ids, routing_path, ruleset_ids, lineage_log
|- build_metadata_envelope(view)        # histories, policy markers, traces, cob snapshot, etc.
|- derive_routing_epoch_id(view)        # deterministic routing epoch derivation
|- derive_commit_timestamp(kwargs)      # deterministic testbench override support
|- derive_commit_hash(tpsns_body)       # canonical hash over stable serialization
|- assemble_tpsns(...)                  # final immutable snapshot object
|- write_boundary_guard(tp_before, out) # assert forbidden writes / recomputation absence
|- process(...)                         # orchestration
```

All functions must be deterministic for identical TP snapshots and identical deterministic inputs.

### 1.3 Serializer and hash convention

Use a canonical serializer before hashing:

1. Stable key ordering for dictionaries.
2. Stable ordering for all already-ordered arrays (no reordering step).
3. UTF-8 encoding.
4. Hash function fixed by implementation constant (for example SHA-256).

The hash policy must never vary by machine, locale, or runtime process state.

---

## 2. Input/Output Commit Contract

### 2.1 OuBA accepted input shape (read-only)

OuBA consumes a final Path-A TP snapshot containing commit-relevant fields, including:

- proposition_set[]
- truth_evidence[]
- completion_state
- TP.semantic.semantic_tags[]
- TP.semantic.lane_local_identity
- TP.metadata.messy_input_record
- TP.metadata.delta_h_percent
- ob_trace[]
- tb_trace[]
- policy_markers[]
- TP.next_context.*
- TP.lineage_log[]
- TP.cob_state_snapshot
- TP.metadata.entropy_history[]
- TP.metadata.signature_history[]
- sob_id, srob_id, cnob_id, smob_id, idob_id
- routing_path
- ruleset_ids[]

OuBA treats input fields as immutable read-only source data.

### 2.2 OuBA produced output shape

OuBA emits exactly one commit object per accepted input, containing:

- tpsns_id
- commit_timestamp
- commit_hash
- routing_epoch_id
- semantic_envelope fields (verbatim fidelity)
- context_envelope fields (verbatim fidelity)
- provenance and lineage fields (verbatim fidelity)
- metadata and trace fields required for replay/audit

Naming of the top-level envelope (TPSnS vs CTP) may follow current pipeline adapter conventions, but field fidelity requirements are unchanged.

### 2.3 Immutability expectation

The emitted snapshot is commit-final and must be treated as read-only by downstream systems.

---

## 3. Owned Fields and Write Boundaries

### 3.1 Commit-layer ownership (OuBA-owned output fields)

OuBA owns only commit-layer construction and emission, including:

- tpsns_id
- commit_timestamp
- commit_hash
- routing_epoch_id
- final commit envelope assembly

It may copy required TP fields into committed structures but does not reinterpret them.

### 3.2 Strict non-ownership

OuBA must not perform any of the following:

- semantic inference
- candidate generation
- routing decisions
- OB-family recomputation (SOB/SROB/CnOB/SmOB/IdOB)
- TR/RB/DCB invocation
- structural recomputation or entropy recomputation
- mutation of TP source fields
- writing Path-B truth/done/safety fields

### 3.3 Write-boundary guard behavior

Write-boundary guard checks run in both modes:

- testbench mode: boundary violation is hard FAIL.
- general mode: boundary violation is FAIL (not warning), because ownership is invariant.

---

## 4. Deterministic Commit Algorithm

### 4.1 Precondition validation

Before assembly, validate required invariants:

1. Required fields present.
2. Required field types valid.
3. Input consistency checks for commit-safe structure.

On violation, fail fast with explicit invariant error metadata.

### 4.2 Freeze flow (single-pass)

Deterministic flow:

1. Extract read-only commit view.
2. Build semantic envelope from verbatim source fields.
3. Build context envelope from TP.next_context.*.
4. Build provenance/lineage envelope from lineage and OB lineage IDs.
5. Build metadata/trace envelope from policy markers, traces, histories, and identity snapshot.
6. Derive routing_epoch_id deterministically.
7. Assemble commit body without timestamp/hash.
8. Resolve commit_timestamp from deterministic source policy.
9. Hash canonical serialized body + commit_timestamp policy inputs.
10. Emit immutable snapshot object.

Exactly one output is emitted for one accepted input.

### 4.3 Deterministic timestamp policy

Implementation must support deterministic testbench replay:

- If a deterministic commit timestamp override is provided by fixture/config, use it.
- Otherwise use runtime timestamp policy for non-testbench operation.

In deterministic testbench mode, timestamp source must be controlled so equality tests remain stable.

### 4.4 Deterministic identifier policy

tpsns_id and routing_epoch_id must be deterministically derived from stable commit inputs (or deterministic fixture overrides) and must not use nondeterministic random sources.

---

## 5. Fidelity Rules for Field Transfer

### 5.1 Verbatim preservation requirements

OuBA preserves these fields exactly from TP into committed output:

- proposition_set[]
- truth_evidence[]
- completion_state
- TP.semantic.semantic_tags[]
- TP.semantic.lane_local_identity
- TP.metadata.messy_input_record
- TP.metadata.delta_h_percent
- policy_markers[]
- ob_trace[]
- tb_trace[]
- TP.next_context.*
- TP.lineage_log[]
- TP.cob_state_snapshot
- TP.metadata.entropy_history[]
- TP.metadata.signature_history[]
- sob_id, srob_id, cnob_id, smob_id, idob_id
- routing_path
- ruleset_ids[]

No omission, elision, reordering, or silent defaulting is allowed for required fields.

### 5.2 Residue/uncertainty representation rule

Any residue/uncertainty present in source fields must remain explicit in output and must not be dropped.

### 5.3 Metadata applicability rule

OuBA consumes only commit-adjacent and provenance-adjacent metadata and ignores irrelevant metadata classes, while preserving required commit fields.

---

## 6. Error Handling and Failure Semantics

### 6.1 Fail-fast classes

Fail-fast classes include:

1. Missing required fields.
2. Type/schema mismatch for required fields.
3. Invariant violation that prevents safe commit.
4. Write-boundary violation.

### 6.2 Failure payload expectation

Failure output should include deterministic diagnostics:

- error_code
- failing_field_path
- invariant_id or reason tag
- short human-readable message

Diagnostics must be replay-stable for identical failing inputs.

---

## 7. Dual-Mode Testbench Alignment

Per progressive lineup framework:

| mode      | Input file              | Validation method |
|-----------|-------------------------|-------------------|
| testbench | ouba_testbench.yaml     | exact expected equality |
| general   | ouba_input.yaml         | rulechecker only |

Category placement:

- testbenches/path_a/identity/ (if project keeps OuBA in identity lane)
- or testbenches/path_a/routing/ (if project classifies OuBA as final routing-stage commit)

One category must be selected and kept stable for discovery.

Rulechecker in testbench mode may run for diagnostics only and must not override exact expected comparison.

---

## 8. Observability Hooks (Non-semantic)

When enabled, attach deterministic commit diagnostics:

- commit input completeness summary
- preserved-field counts
- lineage/provenance attach summary
- deterministic ID/hash derivation trace (high-level, no secret material)
- boundary-guard pass/fail markers

Observability output must not change semantic or commit payload fields.

---

## 9. Must-Prove for v0.1 Implementation

1. Identical input snapshots (with deterministic timestamp policy) yield identical output snapshots.
2. Exactly one output emitted per accepted input.
3. No forbidden writes or recomputation steps occur.
4. Required fidelity fields are preserved exactly.
5. Dual-mode testbench behavior matches progressive framework.
6. Commit hash and IDs are stable across platforms for identical canonical input.

Defer for later versions:

- additional optional metadata projection layers
- alternate commit envelope adapters for external consumers
- versioned hash algorithm migration strategy

---

## 10. Research Questions / Open Items for CP Review

1. Stable category placement for OuBA testbench discovery: identity vs routing.
2. Canonical source for deterministic commit_timestamp in testbench fixtures.
3. Canonical derivation formula for routing_epoch_id in v0.1.
4. Whether tpsns_id should be hash-derived or independently deterministic.
5. Exact failure-code taxonomy for commit invariant violations.
6. Minimum required vs optional metadata set for first production cut.

---

## 11. Implementation Order Recommendation

1. Define dataclasses or schema maps for commit-required fields.
2. Implement extract + precondition validation.
3. Implement deterministic envelope builders.
4. Implement canonical serialization + hash + ID derivations.
5. Implement write-boundary guard.
6. Wire dual-mode testbench files and rulechecker.
7. Add deterministic fixture cases and negative invariant tests.

---

End of ouba_py_struc_pgm.md (v0.1)
Ready for CP review before full ouba.py realization.


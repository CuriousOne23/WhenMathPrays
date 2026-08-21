# cob_py_struc_pgm.md — COB Structural Program (Python Realization)

**Document ID:** cob_py_struc_pgm  
**Version:** 0.1 (First Crystallization)  
**Status:** Draft — for CP review  
**Scope:** Path-A Conversation Object Basin (COB)  
**Location:** `thought_simulator/requirements_20/system_playground/primitives/cob/`  
**Companion code:** `cob.py` (to be realized / refined from this program)  

**Normative parents:**  
- `20.32_cob_requirements.md` (v0.7 Cognitive-Field Update)  
- `system_playground/primitives/cob/cob_requirements.md` (playground subset)  
- `progressive_lineup_testing.md` (v4.2+)  
- `patha_field_names.md` (canonical field dictionary)  

**Behavioral contracts / supporting documents:**  
- `20.15_ts_architecture_scaffold.md`  
- `20.105_tp_requirements.md` + `20.105.010` / `.020` / `.030`  
- `system_playground/design/pipeline/primitive_transfer_table2.md` (aligned)  

**Local structures (this directory):**  
- `cob_structures.yaml` / `cob_state.yaml` (mentioned in testing notes; loaders look first in primitives/cob/)  

---

## 0. Purpose of This Structural Program

This document converts the normative HLRs of 20.32 and the playground cob_requirements into an explicit, deterministic Python realization plan for COB.

It resolves the previously open realization items:

1. **Store update operator** — deterministic mapping from (prior cob_state_snapshot + CST signals + OuBA fragments + next-turn context) → next identity-layer set + ordering metrics + lineage events.  
2. **Envelope ownership** — which fields COB may write under `cob_state_snapshot` and the CIL transfer block, versus fields that remain read-only or are owned by TPU / other primitives.  
3. **Structural-only discipline** — explicit rules for MERGE / SPLIT / compression that never perform semantic reconstruction.  

It also defines the module shape, write-boundary guards, dual-mode testbench contract, and the first-order algorithms that `cob.py` must implement.

This is a structural program, not a requirements document. HLRs remain authoritative; this program must stay inside them.

---

## 1. Python Module Shape (`cob.py`)

### 1.1 Required surface

```python
PRIMITIVE_NAME = "cob"

def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """
    Main entry. Returns updated TP (or a TPU request structure per pipeline convention).
    mode is injected by run.py / testbench ("testbench" | "general").
    """
```

### 1.2 Internal structure (recommended)

```
cob.py
├── load_structures()                    # local YAML under primitives/cob/
├── extract_cob_view(tp)                 # read-only view of prior cob_state_snapshot + CST signals + next_context
├── apply_cst_core_signals(...)          # Freeze / Thaw / Continuity-restoration
├── apply_cst_ms_commands(...)           # create / split / merge / collapse-recovery / register strengthen|weaken
├── integrate_ouba_fragments(...)        # strength, ambiguity, lineage continuity, register updates
├── integrate_next_context(...)          # HLR-COB-015 … 023 structural merge
├── apply_structural_compression(...)    # HLR-COB-024 / 025 (token-set exact-duplicate + strict-subset)
├── update_ordering_metrics(...)         # recency, frequency, density, access count, chronological vector, sliding window
├── enforce_bound_and_evict(...)         # max 20 layers; lowest-priority eviction
├── compute_lineage_topology_metrics(...)# identity_lineage, continuity_lineage, topology, scalar metrics
├── build_cob_state_snapshot(...)        # durable state
├── build_cil_transfer_block(...)        # stabilized snapshot fields required by CIL
├── issue_tpu_request_or_write(...)      # TPU-mediated or direct snapshot write per pipeline convention
├── write_boundary_guard(tp_before, tp_after)
└── process(...)                         # orchestration
```

All functions must be pure with respect to identical TP snapshots + identical prior COB state (HLR-20.32-007, HLR-COB-007).

### 1.3 Dictionary / structure lookup rule

1. Look first in `primitives/cob/`.  
2. Fall back only if explicitly directed later.  
Do **not** hard-code paths into `papers/` or other trees.

---

## 2. Owned Fields and Write Boundaries

### 2.1 Fields COB owns / may write

Per `patha_field_names.md` and 20.32 / playground:

- `cob_state_snapshot` (primary durable state)  
- identity-layer objects (≤ 20) conforming to IdentityLayer schema  
- referent maps conforming to ReferentEntry schema  
- ordering metrics: recency, frequency, density, total access count / conversation_count, chronological ordering vector, sliding-window frequency (last 10)  
- clarifying fields (bounded ≤ 10 per layer) + importance scores  
- `identity_lineage`, `continuity_lineage`, `topology`  
- scalar metrics: `ambiguity_score`, `collapse_risk`, `drift_score`, `stability_score`, `lineage_confidence`  
- `register_continuity`, `importance_continuity`  
- structural event markers (MERGE / SPLIT) recorded in `TP.lineage_log[]`  
- CIL transfer-block fields (stabilized snapshot)  
- transfer-surface artifacts when required: `canonical_output_record`, `canonical_output_tags`  
- appends to `routing_path` / `lineage_log` / `tb_trace` with module id `"cob"`

### 2.2 Strict non-ownership (write-boundary guard)

COB MUST NOT write or mutate:

- any OB / IB / RB / TB / InB / OuB internal state  
- routing vectors, `routing_filter`, RED fields  
- structural ΔH% / SSG / STPX fields  
- Path-B truth/done envelopes  
- semantic_core  
- current-turn clarifying fields owned by other primitives (MCB may generate next-turn; COB merges them structurally)  
- semantic-importance scores or roles (read-only projection only)  
- any field outside the declared envelope boundaries

The guard runs after every process call in both modes. Violation → hard fail in testbench mode; diagnostic in general mode.

### 2.3 Read-only inputs

- CST-Core signals: Freeze, Thaw, Continuity-restoration, stability-correction signals  
- CST-MS structural commands: freeze/thaw/collapse-recovery/create-identity-layer/split/merge/strengthen_register/weaken_register  
- OuBA meaning packets, strength updates, ambiguity/confidence, lineage continuity, register updates  
- IdOB identity-importance and SmOB semantic-adjacent importance (indirect via TP → OuBA)  
- `TP.next_context` / `TP.metadata.next_context_metadata` (from MCB)  
- `TP.semantic.importance`  
- `TP.cex.ccr.selected_conversation` / `TP.metadata.cil_metadata`  
- prior `cob_state_snapshot`

---

## 3. Core Deterministic Operators

### 3.1 CST-Core signal application (HLR-20.32-002, HLR-COB-002 / 010)

| Signal | Effect on identity-layer objects |
|--------|----------------------------------|
| Freeze | Mark targeted layer(s) frozen; subsequent updates ignored until Thaw |
| Thaw | Clear frozen flag; allow normal evolution |
| Continuity-restoration | Restore continuity markers / lineage pointers from last stable snapshot; deterministic |
| stability-correction | Adjust stability_score / related metrics within bounded rules |

Frozen objects remain byte-identical until thawed.

### 3.2 CST-MS structural commands (HLR-COB-014 / 025)

**CREATE / create-identity-layer**  
- Allocate new IdentityLayer with fresh layer_id.  
- Initialize from current OuBA fragments if present.  
- Do not evolve previous object when new_context_required=True (HLR-COB-010A).

**MERGE** (structural only)  
- Create child layer.  
- Structurally embed each parent’s referent_map, anchors, ambiguity, stability metrics (e.g. under parents{} keyed by parent id).  
- Combine ordering metrics with deterministic non-semantic rules (e.g. max of recency/frequency/density).  
- Record MERGE event in lineage_log with explicit parent and child references.  
- Apply structural compression after embedding.

**SPLIT** (structural only)  
- Duplicate all semantic fields of the parent into each child (full copy, no partitioning).  
- Record SPLIT event in lineage_log.  
- Apply structural compression after duplication.

**collapse-recovery / strengthen_register / weaken_register**  
- Apply the corresponding metric or register adjustment deterministically; never reinterpret content.

### 3.3 Structural compression (HLR-COB-024)

After any update, merge, or split:

1. Remove exact duplicate referent entries (identical token sets).  
2. Remove referent entries whose token sets are strict subsets of other entries.  
3. Preserve referent-map integrity and lineage continuity.  
4. Operate strictly on token-set structure; no semantic interpretation.  
5. Result must be deterministic and replay-safe.

### 3.4 Ordering metrics update (HLR-COB-004 / 011 / 012 / 013)

On every access / evolution of a layer:

- Increment total access count / conversation_count.  
- Append layer_id to chronological ordering vector.  
- Recompute sliding-window frequency over the last 10 access events.  
- Update per-layer recency, frequency, density.  

Eviction priority is derived deterministically from these metrics (lowest-priority = first to evict when bound of 20 is exceeded). Exact arithmetic remains first-order and must be made explicit and observable in implementation; it is a Must-Prove item.

### 3.5 Next-turn context integration (HLR-COB-015 … 023)

- Ingest fields from `TP.next_context` / `TP.metadata.next_context_metadata`.  
- Validate against stabilized identity-layer objects.  
- Merge with deterministic continuity rules.  
- Update clarifying-field importance using continuity metrics.  
- Expose merged fields to CIL without modification.  
- Preserve across freeze/thaw cycles.  
- Treat strictly as structural metadata (no semantic interpretation).  
- Do not invent field names.

### 3.6 Lineage / topology / scalar metrics exposure (HLR-COB-026 … 033)

COB SHALL compute and expose to CIL:

- `identity_lineage`  
- `continuity_lineage`  
- `topology` (parent/child + referent-map graph structure)  
- `ambiguity_score`, `collapse_risk`, `drift_score`, `stability_score`, `lineage_confidence`  
- `register_continuity`, `importance_continuity`  

All are deterministic, read-only for downstream consumers, and replay-safe.

---

## 4. CIL Transfer Block

The stabilized snapshot handed to CIL contains at minimum:

- identity layers (IdentityLayer objects)  
- referent maps  
- clarifying fields + importance  
- ordering metrics  
- identity_lineage, continuity_lineage, topology  
- scalar metrics listed above  
- register_continuity, importance_continuity  
- next-turn context fields  
- conversation_count  
- initial_state_complete  

No semantic reconstruction is performed when building this block.

---

## 5. Dual-Mode Testbench Alignment

Follow progressive_lineup_testing.md exactly:

| mode      | Input file              | Validation                                      |
|-----------|-------------------------|-------------------------------------------------|
| testbench | cob_testbench.yaml (or equivalent) | exact or structural comparison of owned fields |
| general   | cob_input.yaml          | rulechecker only                                |

Category placement: under the progressive Path-A identity / context lineup.

Mandatory:

- deterministic testbench mode (input + expected)  
- general rule-driven mode  
- directory schema for primitive discovery  
- import-path initialization  
- naming discipline and registration  
- standardized PASS/FAIL output  
- progressive upstream selection rules  
- envelope-boundary discipline  
- write-boundary assertions (hard fail in testbench)

Tested behaviors already enumerated in playground §5.1 (HLR-COB-001 through 025 and lineage metrics) remain the acceptance criteria.

---

## 6. Foundation Observability Hooks

When enabled, log or attach diagnostic block:

- which CST signals were applied  
- MERGE / SPLIT parent → child mappings  
- compression actions taken (duplicates / subsets removed)  
- eviction decisions and priority values  
- next-context merge summary  
- final layer count and ordering-metric snapshot  

These support progressive foundation observation without affecting PASS/FAIL in testbench mode.

---

## 7. Must-Prove for v0.1 Implementation

- Deterministic outputs for fixed inputs + fixed prior COB state (HLR-20.32-007, HLR-COB-007).  
- Correct ownership: only declared fields written.  
- Write-boundary guard rejects all forbidden writes.  
- MERGE embeds parents structurally; SPLIT full-copies; compression is pure token-set.  
- Bound of 20 layers enforced; eviction selects lowest priority.  
- Freeze/Thaw compliance.  
- Next-turn context integration is structural-only.  
- CIL transfer block contains exactly the required fields.  
- Dual-mode contracts and progressive discovery paths work.  
- Replay of identical CST signals + identical prior state produces identical lineage_log and cob_state_snapshot.

---

## 8. Defer (Future Crystallization)

- Concrete nested TP paths for CST-Core / CST-MS signals (currently descriptive names only).  
- Full internal schema expansion of `cob_state_snapshot` beyond the fields already required by CIL.  
- Exact arithmetic formula that turns (recency, frequency, density, access count, sliding window) into a total priority score for eviction.  
- Continuous or probabilistic extensions of any metric (must remain deterministic).  
- Learned parameters of any kind.

These items are acknowledged residual fog; they do not block the v0.1 structural program or testbench construction.

---

**End of structural program.**  
HLRs remain authoritative. This program is a realization plan only.

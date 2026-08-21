# cil_py_struc_pgm.md — CIL Structural Program (Python Realization)

**Document ID:** cil_py_struc_pgm  
**Version:** 0.1 (First Crystallization)  
**Status:** Draft — for CP review  
**Scope:** Path-A Conversation Integration Layer (CIL)  
**Location:** `thought_simulator/requirements_20/system_playground/primitives/cil/`  
**Companion code:** `cil.py` (to be realized / refined from this program)  

**Normative parents:**  
- `20.33_cil_requirements.md` (v1.2 Importance Integration Update)  
- `system_playground/primitives/cil/cil_requirements.md` (playground subset)  
- `progressive_lineup_testing.md` (v4.2+)  
- `patha_field_names.md` (canonical field dictionary)  

**Behavioral contracts / supporting documents:**  
- `20.32_cob_requirements.md` (COB snapshot source)  
- `20.105_tp_requirements.md` + meta series (next_context, intake_metadata)  
- `system_playground/design/pipeline/primitive_transfer_table2.md` (pipeline position)  
- `cil_intake_packet.yaml` (local schema reference, when present)  

**Local structures (this directory):**  
- `cil_intake_packet.yaml`  
- `cil_state.yaml` (if used for fixtures)  

---

## 0. Purpose of This Structural Program

This document converts the normative HLRs of 20.33 and the playground cil_requirements into an explicit, deterministic Python realization plan for CIL.

CIL is a **normalize / freeze / package** layer only. It does not integrate conversational material, does not exercise structural authority, does not compute new importance or ordering scores, and does not own durable conversation state. Structural integration is performed exclusively by COB; CIL reflects COB’s stabilized identity-layer snapshot, the USP from CST-Mux, structural cues, intake metadata, importance signals, and next-turn context into a bounded, ordered, replay-safe intake packet for CEx.

This structural program resolves:

1. **Packet construction operator** — deterministic mapping from (COB snapshot + USP + structural_cues + intake_metadata + importance signals + next_context) → CILIntakePacket.  
2. **Envelope ownership** — which fields CIL may write (intake packet and its blocks) versus fields that remain strictly read-only or owned by other primitives.  
3. **Reflect-only discipline** — explicit rules so that ordering metrics, importance, lineage, topology, metrics, and completeness flags are never recomputed or reinterpreted.

It also defines the module shape, write-boundary guards, dual-mode testbench contract, and the first-order algorithms that `cil.py` must implement.

This is a structural program, not a requirements document. HLRs remain authoritative; this program must stay inside them.

---

## 1. Python Module Shape (`cil.py`)

### 1.1 Required surface

```python
PRIMITIVE_NAME = "cil"

def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """
    Main entry. Returns updated TP carrying the CIL intake packet.
    mode is injected by run.py / testbench ("testbench" | "general").
    """
```

### 1.2 Internal structure (recommended)

```
cil.py
├── load_packet_schema()                 # local cil_intake_packet.yaml if present
├── extract_cob_snapshot(tp)             # read-only COB stabilized identity-layer snapshot
├── extract_usp(tp)                      # read-only USP from CST-Mux
├── extract_structural_cues(tp)          # TP.process.structural_cues
├── extract_intake_metadata(tp)          # TP.metadata.intake_metadata
├── extract_register_cues(tp)            # TP.process.register_cues
├── extract_next_context(tp)             # TP.next_context{} / metadata
├── extract_importance_signals(tp)       # structural / constraint / semantic-adjacent /
│                                        # identity / long-horizon (all read-only)
├── build_identity_selection_block(...)  # reflect COB ordering; no new scores
├── build_certainty_ambiguity_blocks(...)
├── build_stability_block(...)           # from USP + COB; no new freeze/thaw decisions
├── build_structural_hints_block(...)
├── build_referent_mapping_block(...)
├── derive_register_hint(...)            # deterministic, non-semantic
├── extract_clarifying_fields(...)       # bounds: 10 fields / 100 subfields / depth 4
├── reflect_importance_blocks(...)
├── reflect_completeness_flags(...)
├── reflect_lineage_topology_metrics(...)
├── build_next_context_block(...)
├── assemble_intake_packet(...)
├── write_boundary_guard(tp_before, tp_after)
└── process(...)                         # orchestration
```

All functions must be pure with respect to identical TP snapshots (HLR-20.33-008, HLR-20.33-022, HLR-CIL-006).

### 1.3 Dictionary / schema lookup rule

1. Look first in `primitives/cil/`.  
2. Fall back only if explicitly directed later.  
Do **not** hard-code paths into `papers/` or other trees.

---

## 2. Owned Fields and Write Boundaries

### 2.1 Fields CIL owns / may write

Per 20.33 and `patha_field_names.md`:

- CIL intake packet (and its blocks), conventionally under a CIL-owned envelope such as:
  - `TP.cil.intake_packet` / `TP.cil.*` block fields, or the transfer-surface name used by the progressive pipeline for CEx intake  
- Blocks required by the schema:
  - `identity_selection` (IdentitySelectionBlock)  
  - `certainty`, `ambiguity`, `stability`  
  - `structural_hints`  
  - `referent_mapping`  
  - `register_hint`  
  - `clarifying_fields`, `clarifying_importance`, `clarifying_topology`  
  - `structural_importance`, `constraint_importance`, `semantic_adjacent_importance`, `identity_importance`, `long_horizon_importance`  
  - `conversation_count_complete`, `initial_state_complete`  
  - `next_context` (NextContextBlock — reflected)  
  - `timestamps.generated_turn`  
  - lineage / topology / metrics reflections: `identity_lineage`, `continuity_lineage`, `topology`, `metrics` (ambiguity_score, collapse_risk, drift_score, stability_score, lineage_confidence), `register_continuity`, `importance_continuity`  
- appends to `routing_path` / `lineage_log` / `tb_trace` with module id `"cil"` when the pipeline convention requires provenance markers  
- extraction-audit records for clarifying-field drops / truncations (written to the audit path required by HLR-20.33-047, typically CE.metadata.extraction_audit or CIL-local audit that CE may later consume)

Exact top-level TP path for the packet remains first-order; prefer the path already used by progressive CEx fixtures or `patha_field_names.md`. Do not invent a second competing envelope.

### 2.2 Strict non-ownership (write-boundary guard)

CIL MUST NOT write or mutate:

- `TP.semantic` / semantic_core  
- durable COB identity-layer store or `cob_state_snapshot` contents  
- USP content for control purposes; no stability commands back to COB  
- routing vectors, `routing_filter`, RED fields  
- structural geometry, ΔH%, SSG / STPX ownership fields  
- Path-B truth/done envelopes  
- clarification FIFO or supervisory escalation state  
- any field owned by ISc, Merge, TPU, IB, TB, RBU, OB, RB, DCB except through approved supervisory wires  
- next-turn context field *names* or derived coherence/shift scores  
- new importance values, ordering scores, recency/frequency/density (reflect only)

The guard runs after every process call in both modes. Violation → hard fail in testbench mode; diagnostic in general mode.

### 2.3 Read-only inputs

- COB stabilized identity-layer snapshot (`cob_state_snapshot` / COB transfer block)  
- USP from CST-Mux  
- `TP.process.structural_cues`  
- `TP.metadata.intake_metadata`  
- `TP.process.register_cues`  
- `TP.next_context{}` (and metadata forms)  
- importance signals: structural (SOB/SROB via COB), constraint (CnOB via COB), semantic-adjacent (SmOB via COB), identity (IdOB via COB), long-horizon (COB)  
- `conversation_count_complete`, `initial_state_complete` from COB  
- COB lineage / topology / metrics / register_continuity / importance_continuity  
- referent maps, temporal anchors, discourse anchors as present in the snapshot

---

## 3. Core Deterministic Operators

### 3.1 Identity selection (HLR-20.33-020, 032–039, 083–085; HLR-CIL-001, 008–010)

- Derive identity selection solely from COB snapshot + structural_cues + intake_metadata.  
- Reflect COB ordering metrics without modification:  
  - `last_referred` (recency)  
  - `total_referrals` (frequency)  
  - `recent_referrals` (density)  
  - `ordering_score`  
- Primary / secondary layer ids and `layer_ranking` MUST use COB’s ordering_score (+ importance continuity when present).  
- CIL SHALL NOT compute new ordering scores or importance values.  
- Playground scoring formula `Score(o) = w_r r + w_f f + w_d d` is **not** normative for realization; prefer pure reflection of COB’s `ordering_score`. Any local diagnostic ranking must be marked non-authoritative and deferred from Must-Prove.

### 3.2 Certainty, ambiguity, stability (HLR-20.33-002, 070; HLR-CIL-003, 004)

- Generate referent / temporal / discourse certainty and ambiguity flags deterministically from snapshot + cues.  
- Reflect stability indicators from USP and COB snapshot.  
- SHALL NOT invent new freeze, thaw, collapse, or topology decisions.  
- USP is packaging / replay material only (HLR-20.33-066–069).

### 3.3 Clarifying-field extraction (HLR-20.33-040–050)

- Extract clarifying fields, subfields, hierarchical sub-subfields up to depth 4 from the COB snapshot.  
- Bounds: max 10 clarifying fields; max 100 subfields; max depth 4.  
- Drop / truncate excess with deterministic extraction-audit records.  
- Preserve topology, importance scores, provenance, and continuity; do not modify values.  
- Include clarifying metadata even when identity selection is ambiguous or fallback; mark continuity `"undetermined"` when applicable.

### 3.4 Register hint (HLR-20.33-029, 031)

- Derive `register_hint` deterministically from `TP.process.register_cues` and COB register fields.  
- No semantic interpretation.

### 3.5 Importance reflection (HLR-20.33-071–078)

- Ingest and reflect without modification:  
  - structural_importance  
  - constraint_importance  
  - semantic_adjacent_importance  
  - identity_importance  
  - long_horizon_importance  
- Treat as read-only metadata; never compute or reinterpret.

### 3.6 Completeness flags (HLR-20.33-079–082)

- Reflect `conversation_count_complete` and `initial_state_complete` from COB.  
- Read-only; expose to CEx for alignment / fallback.

### 3.7 Next-turn context (HLR-20.33-051–065; HLR-CIL-011–019)

- Read `TP.next_context{}` deterministically.  
- Place fields into NextContextBlock exactly as defined; no rename, no derivation from clarifying fields or COB metrics.  
- Missing / partial → canonical empty-context case.  
- Structural metadata only; preserve continuity across turns; no coherence/shift computation.

### 3.8 Lineage / topology / metrics (HLR-20.33-086–094; HLR-CIL-020–027)

Reflect without modification:

| COB source | CIL target |
|------------|------------|
| identity_lineage | cil.identity_lineage |
| continuity_lineage | cil.continuity_lineage |
| topology | cil.topology |
| metrics.ambiguity_score | cil.metrics.ambiguity_score |
| metrics.collapse_risk | cil.metrics.collapse_risk |
| metrics.drift_score | cil.metrics.drift_score |
| metrics.stability_score | cil.metrics.stability_score |
| metrics.lineage_confidence | cil.metrics.lineage_confidence |
| register_continuity | cil.register_continuity |
| importance_continuity | cil.importance_continuity |

All read-only; deterministic replay required.

### 3.9 Packet assembly (HLR-20.33-013, 001, 006–008)

Assemble `CILIntakePacket` containing the blocks listed in §2.1 and §5 of 20.33. Output is consumed exclusively by CEx. Identical inputs → identical packets.

---

## 4. Intake Packet Schema (Realization View)

```
CILIntakePacket {
  identity_selection: IdentitySelectionBlock,
  certainty: CertaintyBlock,
  ambiguity: AmbiguityBlock,
  stability: StabilityBlock,
  structural_hints: StructuralHintBlock,
  referent_mapping: ReferentMappingBlock,
  register_hint: string,

  clarifying_fields: ClarifyingFieldBlock,
  clarifying_importance: ClarifyingImportanceBlock,
  clarifying_topology: ClarifyingTopologyBlock,

  structural_importance: StructuralImportanceBlock,
  constraint_importance: ConstraintImportanceBlock,
  semantic_adjacent_importance: SemanticAdjacentImportanceBlock,
  identity_importance: IdentityImportanceBlock,
  long_horizon_importance: LongHorizonImportanceBlock,

  conversation_count_complete: boolean,
  initial_state_complete: boolean,

  next_context: NextContextBlock,
  timestamps: { generated_turn: TurnID },

  # lineage / topology / metrics reflections
  identity_lineage,
  continuity_lineage,
  topology,
  metrics: { ambiguity_score, collapse_risk, drift_score, stability_score, lineage_confidence },
  register_continuity,
  importance_continuity
}
```

IdentitySelectionBlock (minimum):

```
{
  primary_layer_id: StableID | null,
  secondary_layer_ids: [StableID],
  layer_ranking: [{ layer_id, score }],  # score = COB ordering_score reflection
  last_referred: TurnID,
  total_referrals: int,
  recent_referrals: int,
  ordering_score: float
}
```

Block internals not fully expanded in 20.33 remain first-order containers; only HLR-required fields are Must-Prove in v0.1.

---

## 5. Dual-Mode Testbench Alignment

Follow progressive_lineup_testing.md exactly:

| mode      | Input file              | Validation                                      |
|-----------|-------------------------|-------------------------------------------------|
| testbench | cil_testbench.yaml      | exact or structural comparison of owned fields |
| general   | cil_input.yaml          | rulechecker only                                |

Category placement: `testbenches/path_a/context/` (alongside COB).

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

Suggested first test set (Must-Prove coverage):

- reflect COB ordering metrics unchanged  
- clarifying-field bound enforcement + audit  
- next_context empty vs populated reflection  
- importance blocks present and unmodified  
- completeness flags reflected  
- lineage / topology / metrics reflection  
- USP stability indicators reflected without new commands  
- write-boundary: no semantic_core / routing_filter / cob_state mutation  
- deterministic replay of identical inputs

---

## 6. Foundation Observability Hooks

When enabled, log or attach diagnostic block:

- primary / secondary layer ids selected  
- ordering_score values reflected  
- clarifying-field drop / truncation counts  
- presence / absence of USP and each importance block  
- next_context empty-context vs populated  
- completeness flags  
- write-boundary guard result  

These support progressive foundation observation without affecting PASS/FAIL in testbench mode.

---

## 7. Must-Prove for v0.1 Implementation

- Deterministic outputs for fixed inputs (HLR-20.33-008, 022; HLR-CIL-006).  
- Intake packet conforms to required blocks (HLR-20.33-013).  
- Ordering metrics and ordering_score reflected, not recomputed (HLR-20.33-036–038, 084).  
- All five importance signal classes reflected read-only (HLR-20.33-071–076).  
- Completeness flags reflected (HLR-20.33-079–081).  
- Clarifying-field bounds enforced with audit (HLR-20.33-043, 047).  
- next_context reflected exactly; empty-context case deterministic (HLR-20.33-053, 065).  
- Lineage / topology / metrics / continuity reflected without modification (HLR-20.33-086–094).  
- USP treated as read-only packaging; no control signals to COB (HLR-20.33-066–069).  
- Write-boundary guard rejects forbidden writes.  
- Dual-mode contracts and progressive discovery paths work.  
- Output path is CEx-facing only (HLR-20.33-006, 007).

---

## 8. Defer (Future Crystallization)

- Exact nested TP path for every sub-field of each *Block type (lock to patha_field_names.md + CEx fixtures).  
- Full field-by-field expansion of CertaintyBlock, AmbiguityBlock, StabilityBlock, StructuralHintBlock, ReferentMappingBlock beyond HLR-required content.  
- Internal USP schema (owned by CST-Mux; CIL remains opaque consumer).  
- Any weighted scoring formula for identity ranking (normative rule is reflect COB ordering_score).  
- Multi-turn continuity stress beyond single-packet determinism.  
- Full pipeline integration tests with live CEx (beyond packet schema compatibility).

These items are acknowledged residual fog; they do not block the v0.1 structural program or testbench construction.

---

## 9. Implementation Order Recommendation

1. Load local packet schema if present; establish extract_* pure views.  
2. Implement write-boundary guard.  
3. Implement identity_selection reflection + ordering metrics.  
4. Implement clarifying-field extraction with bounds and audit.  
5. Reflect importance, completeness, next_context, lineage/topology/metrics.  
6. Assemble intake packet; wire `process(tp, mode=...)`.  
7. Dual-mode testbench (mirror COB / IdOB progressive pattern).  
8. Expand tests once Must-Prove items pass.

---

**End of structural program.**  
HLRs remain authoritative. This program is a realization plan only.

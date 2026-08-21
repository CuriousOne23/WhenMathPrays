# cst_mux_py_struc_pgm.md — CST-Mux Structural Program (Python Realization)

**Document ID:** cst_mux_py_struc_pgm  
**Version:** 0.1 (First Crystallization)  
**Status:** Draft — for CP review  
**Scope:** Path-A Context Stability Tracking — Stability Signal Multiplexing (CST-Mux)  
**Location:** `thought_simulator/requirements_20/system_playground/primitives/cst_mux/`  
**Companion code:** `cst_mux.py` (to be realized from this program)  

**Normative parents:**  
- `20.32.010.030_cst-mux.md`  
- `system_playground/primitives/cst_mux/cst-mux_requirements.md`  
- `progressive_lineup_testing.md` (v4.2+)  
- `patha_field_names.md` (coarse names today; nested path lock **after CP agrees §2**)  

**Upstream / interface context:**  
- Locked `TP.cst.core` (`cst_core_py_struc_pgm.md`, patha §2.4 / §9)  
- Locked `TP.cst.ms` (`cst_ms_py_struc_pgm.md`, patha §2.5 / §10)  
- CIL consumer of USP (`TP.cil.intake_packet` path; Mux does not write CIL)  
- Heritage shapes: existing `cst_mux.py` (non-authoritative)  

---

## 0. Purpose of This Structural Program

This document converts CST-Mux HLRs and the progressive dual-mode contract into an explicit, deterministic Python realization plan.

CST-Mux is the **Stability Signal Multiplexing Module**. It:

- reads stability and structural signals from **CST-Core** and **CST-MS**  
- assigns deterministic **layer indices**  
- **aligns and packages** them into a **Unified Stability Packet (USP)**  
- delivers the USP **exclusively for CIL consumption** (logical consumer; field lives on TP under Mux ownership)  
- has **no structural authority** (issues no commands to COB, CIL, or peers)  
- does **not** accept data from COB and does **not** send USP to COB  

This program locks for v0.1:

1. **Module surface** — `process(tp, mode=...)`  
2. **Proposed TP envelope** — `TP.cst.mux.*` including USP  
3. **Write-boundary** (pack-only; no Core/MS/COB mutation)  
4. **Pure packaging policy** (no reinterpretation of upstream signals)  
5. **Dual-mode progressive alignment**  
6. **Must-Prove / Defer**  

HLRs remain authoritative. After CP approves §2, field paths SHALL be locked in `patha_field_names.md` and become the reference names for implementation and testbenches.

---

## 1. Python Module Shape (`cst_mux.py`)

### 1.1 Required surface

```python
PRIMITIVE_NAME = "cst_mux"

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """
    Main entry. Returns updated TP with TP.cst.mux.* owned fields.
    mode is injected by run.py / testbench ("testbench" | "general").
    """
```

### 1.2 Internal structure (recommended)

```
cst_mux.py
├── extract_cst_core(tp)              # read-only TP.cst.core
├── extract_cst_ms(tp)                # read-only TP.cst.ms
├── collect_layer_ids(...)            # deterministic sorted StableID set
├── assign_layer_indices(...)         # stable index map
├── package_core_signals(...)
├── package_ms_signals(...)
├── package_commands_and_diagnostics(...)
├── package_presence_flags(...)       # recorded as received / derived only from upstream presence
├── assemble_usp(...)
├── write_cst_mux_envelope(tp, ...)
├── write_boundary_guard(tp_before, tp_after)
└── process(...)
```

CST-Mux is **pure** given identical Core + MS inputs (HLR-019–021). Prefer no multi-turn internal state required for correctness; optional USP history on TP is allowed for progressive fixtures only.

### 1.3 Non-goals

- No freeze/thaw/create/split/merge **commands**  
- No mutation of COB topology  
- No rewriting of Core or MS payloads  
- No threshold-based **policy** that substitutes for MS/Core decisions (see §4.3)  

---

## 2. Proposed TP Envelope (`TP.cst.mux.*`) — v0.1

Paths are relative to the TP root at runtime (no leading `TP.` in resolvers). Prose uses `TP.cst.mux` for clarity.

**After CP agreement, these paths SHALL be locked in `patha_field_names.md` and become the reference names.**

### 2.1 Owned write surface

```
cst:
  mux:
    status:
      turn_index: int
      layer_count: int

    layer_index:
      # deterministic map StableID → int (0..n-1), sorted by StableID string
      <StableID>: int

    # Canonical USP (also exposed as unified_stability_packet for dictionary continuity)
    unified_stability_packet:
      turn_index: int
      layer_index: { <StableID>: int }

      # From CST-Core (packaged, not modified)
      core:
        signals:
          freeze: { frozen_objects[], reason }
          thaw: { thawed_objects[], reason }
          continuity_restoration: { restored_objects[], reason }
          drift: { affected_objects[], magnitude }
          oscillation: { affected_objects[], frequency, amplitude }
          ambiguity: { affected_objects[], increased[], decreased[] }
          collapse: { collapsed_objects[], severity }
        metrics:
          per_layer: { <StableID>: { ... } }   # as present on Core
          integrated: { ... }                  # as present on Core
        status:
          frozen_layers: []                    # if present on Core

      # From CST-MS (packaged, not modified)
      ms:
        normalized_metrics: { ... }            # optional pack-through
        weighted_metrics: { ... }              # optional pack-through
        stability: { per_layer / aggregate }
        instability: { per_layer / aggregate }
        collapse_risk: { per_layer / aggregate }
        freeze_risk: { per_layer / aggregate }
        thaw_readiness: { per_layer / aggregate }
        ambiguity_summary: { count }
        drift_summary: { magnitude }
        oscillation_summary: { frequency, amplitude }
        commands: { freeze, thaw, collapse_recovery, create_identity_layer, split, merge }
        command_log: [ ... ]                   # reference or shallow copy
        diagnostics:
          sync_mismatch: bool
          sync_mismatch_detail: string | null
        metadata:
          new_context_required: bool

      # Presence / status flags recorded for CIL convenience
      # Prefer reflection of upstream presence over Mux-owned threshold policy (see §4.3)
      flags:
        activation: { <StableID>: bool } | { activated: bool }   # v0.1 may use aggregate
        freeze: { <StableID>: bool } | { frozen: bool }
        thaw: { <StableID>: bool } | { thawed: bool }
        continuity: { <StableID>: bool } | { continuous: bool }

      # Explicit top-level convenience for progressive tests (HLR-MUX-034/035)
      new_context_required: bool

    usp_tags: [string]   # optional short tags for routing/debug; empty list valid

    history:
      window_len: 10     # optional USP history cap if progressive fixtures need it
      usp_window: [ ... ]  # optional; pure pack does not require multi-turn state

    audit:
      slice: string
      provisional_flags: true | false   # true if any diagnostic threshold flags used
      notes: [string]
```

**Dictionary continuity:**  
Coarse patha names `unified_stability_packet` and `usp_tags` are retained as first-class children under `TP.cst.mux`.

### 2.2 Optional provenance markers

- Append `"cst_mux"` to `routing_path` when pipeline convention requires it.  
- Do not invent a second top-level USP outside `cst.mux`.

### 2.3 Strict non-ownership (write-boundary guard)

CST-Mux MUST NOT write or mutate:

- `identity.cob_state_snapshot` / COB object store  
- `TP.cst.core` (read-only)  
- `TP.cst.ms` (read-only)  
- `TP.cil.intake_packet` (CIL owns intake; Mux only places USP for CIL to **read**)  
- `routing_filter`, RED, geometric_state, semantic_core / TP.semantic  
- Any command fields directed at COB (commands stay under MS ownership; Mux may **copy** command records into USP for logging only)  

Guard runs after every `process` call. Violation → hard fail in testbench mode; diagnostic in general mode.

### 2.4 Read-only inputs

- `TP.cst.core` — status, signals, metrics, history as needed for pack completeness  
- `TP.cst.ms` — synthesis fields, commands, command_log, diagnostics, metadata  
- Optional prior `cst.mux.history.usp_window` if fixtures seed multi-turn history  
- **Not** COB snapshots or COB internal state (HLR-006)  

### 2.5 Logical routing (normative)

| Emit | Write under | Logical consumer | Must NOT |
|------|-------------|------------------|----------|
| USP | `cst.mux.unified_stability_packet` | **CIL** | be sent to COB |
| usp_tags | `cst.mux.usp_tags` | debug / progressive | control COB |
| layer_index | `cst.mux.layer_index` | USP alignment | — |

COB continues to receive structural signals/commands **directly** from Core/MS field surfaces — not via Mux USP (HLR-011, 012, 022).

---

## 3. Operator Spine (v0.1)

### 3.1 Collect layer IDs (deterministic)

Union of StableIDs from:

- `cst.core.metrics.per_layer` keys  
- `cst.ms.*.per_layer` keys when present  
- objects listed in Core freeze/thaw/continuity/drift/oscillation/ambiguity/collapse signal lists  

Sort lexicographically by string form of StableID. Assign indices `0 .. n-1` in that order (HLR-013, 014).

### 3.2 Package Core block

Shallow-copy (or structured extract) Core `signals` and available `metrics` into `unified_stability_packet.core` **without modification** (HLR-008, 009, 018).

Missing Core → empty structured stubs with audit note; do not invent metric values.

### 3.3 Package MS block

Shallow-copy MS synthesis summaries, risks, command shells, diagnostics, and `metadata.new_context_required` into `unified_stability_packet.ms` **without modification** (HLR-010, 018).

Propagate `new_context_required` also to top-level USP field for progressive HLR-MUX-034/035.

### 3.4 Presence flags (policy)

**Normative preference (authoritative):**  
Record flags **as supplied** by upstream when available (Core freeze/thaw lists, MS command freeze/thaw layers, Core frozen_layers). Do **not** reinterpret metrics into new control decisions (HLR-018, §4 informative).

**Playground tension (HLR-MUX-009–015):**  
Heritage `cst_mux.py` applied thresholds (activation 0.2, freeze 0.7, thaw 0.5, continuity 0.5) to MS risk scores. That is **not** preferred for v0.1 normative packaging.

**v0.1 rule:**

1. Primary: set flags from upstream **presence**  
   - freeze flag true for layer if in Core `signals.freeze.frozen_objects` or MS `commands.freeze.layers`  
   - thaw similarly from Core thaw / MS thaw commands  
   - continuity from Core continuity_restoration lists or MS continuity when present  
   - activation: true if layer appears in layer_index (or MS stability present) — presence, not threshold  
2. Optional diagnostic threshold flags **only if** CP later requires playground HLR-MUX-009–015 literally; if used, set `audit.provisional_flags: true` and keep them under a clearly named diagnostic sub-block, not as replacement for upstream command authority.  

Default implementation path for progressive Must-Prove: **presence-based flags**, `provisional_flags: false`.

### 3.5 Assemble USP

Fixed key order for deterministic serialization/comparison:

1. `turn_index`  
2. `layer_index`  
3. `core`  
4. `ms`  
5. `flags`  
6. `new_context_required`  

### 3.6 Merge/split neutrality

Mux does not emit instability. If MERGE/SPLIT markers exist in lineage_log, they must **not** cause Mux to invent instability signals; USP only reflects what Core/MS already emitted (playground HLR-MUX-019–022).

### 3.7 Determinism

Identical Core + MS inputs → identical USP (HLR-019–021). No randomness, wall-clock, or unordered dict iteration without sorting keys.

---

## 4. Dual-Mode Testbench Alignment

Follow progressive_lineup_testing.md:

| mode | Input | Validation |
|------|--------|------------|
| testbench | `cst_mux_testbench.yaml` | exact/structural match on owned `cst.mux` fields |
| general | `cst_mux_input.yaml` | `cst_mux_rules.yaml` + rulechecker only |

Category: `testbenches/path_a/context/`.

Suggested first Must-Prove tests:

- Envelope present at `cst.mux`  
- `unified_stability_packet` present with core + ms blocks  
- `layer_index` deterministic under key permutation of inputs  
- Core freeze/thaw packaged without alteration  
- MS stability/risks/commands packaged without alteration  
- `new_context_required` pass-through from MS  
- USP not written into COB paths  
- No mutation of `TP.cst.core` / `TP.cst.ms` / cob snapshot  
- Deterministic replay  
- Merge neutrality (no invented instability)  

---

## 5. Must-Prove for v0.1

- `process(tp, mode=...)` and `PRIMITIVE_NAME == "cst_mux"`  
- Writes only under proposed `cst.mux` (+ optional routing_path marker)  
- `unified_stability_packet` and `layer_index` present  
- Packs Core signals and MS synthesis/commands when present  
- `new_context_required` reflected from MS without modification  
- Deterministic layer index order  
- No COB / Core / MS mutation  
- Dual-mode progressive wiring  
- Write-boundary guard  

---

## 6. Defer

- Final per-layer flag schema richness vs aggregate-only fixtures  
- Optional diagnostic threshold flag policy (if CP elevates playground HLR-MUX-009–015 over pure packaging)  
- Live CIL read integration beyond USP presence on TP  
- Multi-turn `usp_window` necessity (optional)  
- patha_field_names hard lock (**immediately after CP path approval**)  

---

## 7. Implementation Order Recommendation

1. Envelope helpers + write-boundary guard  
2. Layer ID collect + index assignment  
3. Package Core + MS + commands/diagnostics  
4. Presence-based flags + `new_context_required`  
5. Assemble USP + `usp_tags`  
6. `process` orchestration  
7. Progressive dual-mode testbench (replace heritage dataclass runner)  
8. patha_field_names path lock once CP signs §2  

---

## 8. Research Questions for CP

1. Confirm §2 nested map (`cst.mux` with `unified_stability_packet`, `layer_index`, `usp_tags`, `audit`) as the single envelope.  
2. Confirm **presence-based flags** as v0.1 default vs heritage threshold flags.  
3. Prefer **shallow copy** of full Core/MS subtrees into USP vs minimal field subset?  
4. Is optional `usp_window` required for v0.1 progressive tests or omit until needed?  
5. Confirm USP is **CIL-only** logical consumer (normative), rejecting playground wording that USP is consumed by COB.  

---

**End of cst_mux_py_struc_pgm.md (v0.1)**  
Ready for CP review. Realization of progressive `cst_mux.py` and patha lock should wait for path confirmation (§2) and flag-policy answer (§8.2).

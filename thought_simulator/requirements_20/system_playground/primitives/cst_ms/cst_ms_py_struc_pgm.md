# cst_ms_py_struc_pgm.md — CST-MS Structural Program (Python Realization)

**Document ID:** cst_ms_py_struc_pgm  
**Version:** 0.1 (First Crystallization)  
**Status:** Draft — for CP review  
**Scope:** Path-A Context Stability Tracking — Metric Synthesis (CST-MS)  
**Location:** `thought_simulator/requirements_20/system_playground/primitives/cst_ms/`  
**Companion code:** `cst_ms.py` (to be realized from this program)  

**Normative parents:**  
- `20.32.010.020_cst-ms.md`  
- `system_playground/primitives/cst_ms/cst-ms_requirements.md`  
- `progressive_lineup_testing.md` (v4.2+)  
- `patha_field_names.md` (canonical names; nested path lock after CP agrees §2)  
- `cst_ms_capabilities.md` (capability surface + gaps)  

**Upstream / interface context:**  
- Locked `TP.cst.core` (`cst_core_py_struc_pgm.md`, patha §2.4 / §9)  
- `20.32_cob_requirements.md` (COB consumes MS structural commands)  
- Heritage shapes: `cst_ms_bak.py` (non-authoritative)  

---

## 0. Purpose of This Structural Program

This document converts CST-MS HLRs and the progressive dual-mode contract into an explicit, deterministic Python realization plan.

CST-MS is the **Metric Synthesis Module**. It:

- reads raw metrics and signals from **CST-Core** (and optional OuBA / diagnostic COB views)  
- normalizes, weights, and synthesizes stability / instability / risks / summaries  
- holds **sole authority** to issue structural control **commands to COB** (freeze, thaw, collapse-recovery, create-identity-layer, split, merge)  
- reports synchronization mismatches **diagnostically** to CST-Mux (no command feedback from mismatch)

This program locks for v0.1:

1. **Module surface** — `process(tp, mode=...)`  
2. **Proposed TP envelope** — `TP.cst.ms.*`  
3. **Write-boundary + command vs topology discipline**  
4. **Placeholder synthesis policy** — deterministic stubs, labeled provisional  
5. **Dual-mode progressive alignment**  
6. **Must-Prove / Defer**  

HLRs remain authoritative. Final layer weights, threshold tables, and full create/split/merge predicates remain Defer where noted.

---

## 1. Python Module Shape (`cst_ms.py`)

### 1.1 Required surface

```python
PRIMITIVE_NAME = "cst_ms"

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """
    Main entry. Returns updated TP with TP.cst.ms.* owned fields.
    mode is injected by run.py / testbench ("testbench" | "general").
    """
```

### 1.2 Internal structure (recommended)

```
cst_ms.py
├── extract_cst_core(tp)                 # read-only TP.cst.core
├── extract_ouba_snapshot(tp)            # optional OuBA / committed identity ref (HLR-044)
├── extract_cob_diagnostic(tp)           # optional restricted COB view (HLR-045)
├── extract_lineage_structural_events(tp)
├── normalize_metrics(...)
├── apply_weights(...)
├── synthesize_stability_instability(...)
├── compute_risks(...)
├── compute_summaries(...)
├── update_stability_window(...)         # ≤ 10 turns
├── detect_new_context_required(...)
├── decide_cob_commands(...)             # threshold gates → command shells
├── detect_sync_mismatch(...)            # diagnostic only (HLR-047–048)
├── write_cst_ms_envelope(tp, ...)
├── write_boundary_guard(tp_before, tp_after)
└── process(...)
```

All synthesis and command decisions must be pure given identical TP + carried window state (HLR-031–034, 042).

### 1.3 Stateful instance note

CST-MS maintains a **stability window** across turns. Prefer **window carried on TP** under `cst.ms.history` / `cst.ms.stability_window` so progressive tests stay snapshot-replayable. Internal instance state is allowed when multi-turn fixtures explicitly seed/restore it.

---

## 2. Proposed TP Envelope (`TP.cst.ms.*`) — v0.1

Paths are relative to the TP root at runtime (no leading `TP.` in resolvers). Prose uses `TP.cst.ms` for clarity.

**After CP agreement, these paths SHALL be locked in `patha_field_names.md`.**

### 2.1 Owned write surface

```
cst:
  ms:
    status:
      turn_index: int
      layer_count: int

    normalized_metrics:
      # per-layer preferred when layers present; aggregate scalars allowed in v0.1 fixtures
      per_layer: { <StableID>: { drift, oscillation, ambiguity, collapse, continuity } }
      aggregate: { drift, oscillation, ambiguity, collapse, continuity }   # optional

    weighted_metrics:
      per_layer: { <StableID>: { ... } }
      aggregate: { ... }   # optional

    stability:
      per_layer: { <StableID>: { value } }
      aggregate: { value }   # optional

    instability:
      per_layer: { <StableID>: { value } }
      aggregate: { value }

    collapse_risk:
      per_layer: { <StableID>: { value } }
      aggregate: { value }

    freeze_risk:
      per_layer: { <StableID>: { value } }
      aggregate: { value }

    thaw_readiness:
      per_layer: { <StableID>: { value } }
      aggregate: { value }

    ambiguity_summary:
      count: int
      # optional per_layer detail in later versions

    drift_summary:
      magnitude: number

    oscillation_summary:
      frequency: number
      amplitude: number

    # Structural commands issued TO COB (HLR-035–041)
    commands:
      freeze:
        layers: [StableID]
        reason: string
      thaw:
        layers: [StableID]
        reason: string
      collapse_recovery:
        layers: [StableID]
        reason: string
      create_identity_layer:
        requests: [ { provisional_id?, reason } ]
      split:
        layers: [StableID]
        reason: string
      merge:
        pairs: [ [StableID, StableID] ]
        reason: string

    command_log: [
      {
        turn_index: int
        command_type: freeze|thaw|collapse_recovery|create_identity_layer|split|merge
        targets: [StableID] | pairs | requests
        reason: string
        metrics_snapshot_ref: string | null
      }
    ]

    diagnostics:
      sync_mismatch: bool
      sync_mismatch_detail: string | null   # no structural command from mismatch

    metadata:
      new_context_required: bool

    stability_window: [
      {
        turn_index: int
        stability: { value }
        instability: { value }
        collapse_risk: { value }
        freeze_risk: { value }
        thaw_readiness: { value }
      }
    ]   # length ≤ 10

    history:
      window_len: 10

    audit:
      slice: string
      provisional_metrics: true | false
      notes: [string]
```

Heritage `MSSignals` field names are retained where possible (`normalized_metrics`, `stability.value`, `collapse_risk`, etc.). Commands are a **required** normative addition beyond bak.

### 2.2 Optional provenance markers

- Append `"cst_ms"` to `routing_path` when pipeline convention requires it.  
- Do not invent a second top-level envelope outside `cst.ms`.

### 2.3 Strict non-ownership (write-boundary guard)

CST-MS MUST NOT write or mutate:

- `identity.cob_state_snapshot` / COB object store contents (COB applies commands; MS only **emits** them)  
- `TP.cst.core` (read-only upstream)  
- `TP.cil.intake_packet`  
- `routing_filter`, RED, geometric_state, semantic_core / TP.semantic  
- Direct topology edits (Create/Split/Merge executed inside MS rather than as command fields)  

Guard runs after every `process` call. Violation → hard fail in testbench mode; diagnostic in general mode.

### 2.4 Read-only inputs

- `TP.cst.core` — signals, metrics, history, status (locked)  
- Optional OuBA committed identity reference (HLR-044)  
- Optional restricted COB diagnostic view (HLR-045) — **not** a command source (HLR-046)  
- `lineage_log` MERGE/SPLIT markers for neutrality / detection  
- Prior `cst.ms.stability_window` / command_log on TP for replay  

---

## 3. Signal / Command Routing (Normative Realization)

| Emit | Write under | Logical consumers | Must NOT |
|------|-------------|-------------------|----------|
| synthesized summaries / risks | `cst.ms.*` metrics fields | CST-Mux, CIL/CEx consumers of summaries | be written as COB topology |
| freeze / thaw / collapse_recovery / create / split / merge | `cst.ms.commands.*` | **COB** | be derived from COB internal state (HLR-046) |
| command_log entries | `cst.ms.command_log` | replay / audit | be omitted when a command is issued |
| sync_mismatch | `cst.ms.diagnostics` | **CST-Mux** | trigger additional structural commands (HLR-048) |
| new_context_required | `cst.ms.metadata` | COB / downstream context | — |

CST-MS SHALL NOT accept control inputs that invert command authority from COB.

---

## 4. Core Operators (v0.1)

### 4.1 Input adaptation from locked Core

Map `TP.cst.core.signals` and `TP.cst.core.metrics` into synthesis inputs:

- drift ← `signals.drift.magnitude` and/or `metrics.per_layer.*.drift`  
- oscillation ← `signals.oscillation.frequency` / amplitude  
- ambiguity ← `signals.ambiguity` lists and/or per-layer ambiguity  
- collapse ← `signals.collapse.severity` / per-layer collapse  
- continuity ← per-layer continuity if present; else provisional `1 - collapse` (heritage)  
- freeze/thaw/continuity_restoration signals from Core are **inputs to awareness**, not substitutes for MS command authority  

Missing fields → neutral defaults (0 / empty), noted in audit.

### 4.2 Merge/split neutrality (playground HLR-029–037)

- Detect MERGE/SPLIT from `lineage_log` and/or Core-adjacent structural markers.  
- Structural events **must not by themselves** force instability emission.  
- Genuine metric instability within the 10-turn window remains detectable.  

### 4.3 Placeholder synthesis policy (provisional)

Until CP locks final tables, v0.1 SHALL use **deterministic provisional rules** and set `cst.ms.audit.provisional_metrics: true`.

**Default weights (heritage, global):**  
`drift = oscillation = ambiguity = collapse = continuity = 0.25`

**Default maxima:** all `1.0`

**Normalize:** `min(raw / maximum, 1.0)` per metric family (heritage rules for aggregate path).

**Stability:** `clip(sum(weighted), 0, 1)`  
**Instability:** `1 - stability`  
**Collapse risk:** weighted collapse  
**Freeze risk:** `min(weighted_ambiguity + weighted_collapse, 1)`  
**Thaw readiness:** weighted continuity  

**Forbidden:** random, wall-clock, nondeterministic id iteration without sorting.

### 4.4 Command decision (v0.1)

Always include full `commands` key set under the envelope (empty lists valid).

**Provisional gates (CP may replace):**

| Command | v0.1 gate |
|---------|-----------|
| freeze | freeze_risk ≥ 0.5 for layer (or aggregate) |
| thaw | thaw_readiness ≥ 0.5 and layer previously frozen if known |
| collapse_recovery | collapse_risk ≥ 0.5 |
| create_identity_layer | `metadata.new_context_required == true` (optional linkage) |
| split | **Defer** — empty unless CP supplies predicate |
| merge | **Defer** — empty unless CP supplies predicate |

Every non-empty command SHALL append a `command_log` entry (HLR-043).

### 4.5 new_context_required (playground HLR-046–050)

Deterministic OR of provisional detectors (heritage-aligned):

- continuity_break: continuity < 0.40  
- instability_trend: window mean instability > 0.60  
- collapse_spike: collapse_risk > 0.50  
- ambiguity_spike: ambiguity_summary.count > 3  
- freeze_spike: freeze_risk > 0.50  
- fragmentation: structural event present and continuity < 0.75  

### 4.6 Sync mismatch diagnostic

If diagnostic COB view is present and commanded transitions disagree with realized topology, set `diagnostics.sync_mismatch = true` with a deterministic detail string. **Do not** issue further structural commands from this path (HLR-047–048).

### 4.7 Stability window

Append per-turn summary; cap length at **10**. Expose `history.window_len = 10`.

---

## 5. Dual-Mode Testbench Alignment

Follow progressive_lineup_testing.md:

| mode | Input | Validation |
|------|--------|------------|
| testbench | `cst_ms_testbench.yaml` | exact/structural match on owned `cst.ms` fields |
| general | `cst_ms_input.yaml` | `cst_ms_rules.yaml` + rulechecker only |

Category: `testbenches/path_a/context/`.

Suggested first Must-Prove tests:

- Envelope present at `cst.ms`  
- normalized/weighted/stability/instability shapes  
- risks and summaries present  
- commands keys always present; freeze gate on high freeze_risk  
- command_log entry when command non-empty  
- merge neutrality  
- stability_window length ≤ 10  
- new_context_required on continuity break  
- no COB snapshot mutation  
- deterministic replay  
- write-boundary guard  

---

## 6. Must-Prove for v0.1

- `process(tp, mode=...)` and `PRIMITIVE_NAME == "cst_ms"`  
- Writes only under proposed `cst.ms` (+ optional routing_path marker)  
- Synthesis fields from §2.1 present  
- `commands` object always present with all six command keys  
- At least freeze (and preferably thaw / collapse_recovery) gated by provisional thresholds  
- `command_log` updated when commands non-empty  
- `stability_window` length ≤ 10  
- Merge/split structural neutrality when events present without genuine instability  
- `metadata.new_context_required` boolean present  
- Deterministic outputs for fixed inputs + window  
- Dual-mode progressive wiring  
- `audit.provisional_metrics` true while stubs used  
- No mutation of `identity.cob_state_snapshot` or `TP.cst.core`  

---

## 7. Defer

- Final layer-specific weights, maxima, and threshold tables  
- Final stability / risk formulas if CP replaces heritage stubs  
- Full deterministic **create / split / merge** predicates (HLR-039–041)  
- Rich per-layer command targeting vs aggregate-only fixtures  
- Live Mux packaging beyond diagnostic field presence  
- patha_field_names hard lock (immediately after CP path approval)  

---

## 8. Implementation Order Recommendation

1. Envelope helpers + write-boundary guard + empty command shells  
2. Core extract + normalize/weight/stability/risks/summaries (heritage stubs)  
3. Stability window + new_context_required  
4. Freeze/thaw/collapse_recovery command gates + command_log  
5. Sync-mismatch diagnostic shell  
6. `process` orchestration  
7. Progressive dual-mode testbench (replace bak runner)  
8. patha_field_names path lock once CP signs §2  

---

## 9. Research Questions for CP

1. Confirm §2 nested map (`cst.ms` with synthesis + `commands` + `command_log` + `diagnostics` + `stability_window`) as the single envelope.  
2. Prefer **per_layer** synthesis as primary, with aggregate optional — or aggregate-only acceptable for v0.1 fixtures?  
3. Accept heritage weights/maxima/risk gates in §4.3–4.4, or supply alternate constants before coding?  
4. Should `create_identity_layer` fire from `new_context_required` in v0.1, or remain Defer-empty?  
5. Split/merge: empty command shells only until predicates exist, confirmed?  
6. Field name `new_context_required` under `cst.ms.metadata` vs a dedicated top-level child?  

---

**End of cst_ms_py_struc_pgm.md (v0.1)**  
Ready for CP review. Realization of `cst_ms.py` should wait for path confirmation (§2) and any constant overrides.

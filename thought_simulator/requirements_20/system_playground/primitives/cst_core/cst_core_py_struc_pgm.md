# cst_core_py_struc_pgm.md — CST-Core Structural Program (Python Realization)

**Document ID:** cst_core_py_struc_pgm  
**Version:** 0.1 (First Crystallization)  
**Status:** Draft — for CP review  
**Scope:** Path-A Conversation Stability Tracker — Core (CST-Core)  
**Location:** `thought_simulator/requirements_20/system_playground/primitives/cst_core/`  
**Companion code:** `cst_core.py` (to be realized from this program)  

**Normative parents:**  
- `20.32.010.010_cst-core.md`  
- `system_playground/primitives/cst_core/cst-core_requirements.md`  
- `progressive_lineup_testing.md` (v4.2+)  
- `patha_field_names.md` (canonical names; nested path lock after CP agrees §2)  
- `cst_core_capability.md` (capability surface + gaps)  

**Behavioral / interface context:**  
- `20.32_cob_requirements.md` (COB consumes Freeze / Thaw / Continuity only)  
- Heritage shapes: `cst_core_bak.py`, `cst_core_testbench_bak.py` (non-authoritative)  

---

## 0. Purpose of This Structural Program

This document converts CST-Core HLRs and the progressive dual-mode contract into an explicit, deterministic Python realization plan.

CST-Core is a **stateful metric generator**. It maintains sliding-window histories, computes (or provisionally approximates) stability metrics, and emits:

- **Structural signals** to COB and CST-Mux: Freeze, Thaw, Continuity-restoration  
- **Raw metric signals** to CST-MS and CST-Mux only: Drift, Oscillation, Ambiguity, Collapse  

It has **no structural authority** (no Create / Split / Merge / Collapse-recovery commands to COB) and does not accept commands from CST-MS.

This program locks for v0.1:

1. **Module surface** — `process(tp, mode=...)`  
2. **Proposed TP envelope** — `TP.cst.core.*`  
3. **Write-boundary + signal routing**  
4. **Placeholder metric policy** — deterministic stubs, labeled provisional  
5. **Dual-mode progressive alignment**  
6. **Must-Prove / Defer**  

HLRs remain authoritative. Final distance/ambiguity/collapse formulas and threshold adaptation remain Defer.

---

## 1. Python Module Shape (`cst_core.py`)

### 1.1 Required surface

```python
PRIMITIVE_NAME = "cst_core"

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """
    Main entry. Returns updated TP with TP.cst.core.* owned fields.
    mode is injected by run.py / testbench ("testbench" | "general").
    """
```

### 1.2 Internal structure (recommended)

```
cst_core.py
├── extract_cob_layers(tp)              # read-only identity layers / snapshot
├── extract_ouba_cues(tp)               # optional committed OuBA reference (HLR-040)
├── extract_lineage_log(tp)             # MERGE/SPLIT markers for metric hygiene only
├── build_layer_snapshots(...)          # structural snapshot per layer (minimal v0.1)
├── update_histories(...)               # 10-turn counts / frequencies / ordered histories
├── compute_drift(...)                  # provisional deterministic stub
├── compute_oscillation(...)
├── compute_ambiguity(...)
├── compute_collapse_stability(...)
├── compute_combined_instability(...)
├── decide_freeze_thaw_continuity(...)  # threshold compare → emit flags
├── apply_local_freeze_policy(...)      # halt/resume metric updates for frozen layers
├── apply_merge_split_hygiene(...)      # exclude structural parents from false instability
├── emit_signals_and_metrics(...)
├── write_cst_core_envelope(tp, ...)
├── write_boundary_guard(tp_before, tp_after)
└── process(...)
```

All metric and emission decisions must be pure given identical TP + internal history state (HLR-035–037).

### 1.3 Stateful instance note

CST-Core is **stateful across turns** (histories). Progressive single-call tests may construct a fresh instance per test or pass history inside `TP.cst.core.history` for replay. Prefer **history carried on TP** under the owned envelope so testbench mode stays snapshot-replayable without hidden process globals when possible. Internal instance state is allowed when matching multi-turn fixtures explicitly seed/restore it.

---

## 2. Proposed TP Envelope (`TP.cst.core.*`) — v0.1

Paths are relative to the TP root at runtime (no leading `TP.` in resolvers). Prose uses `TP.cst.core` for clarity.

**After CP agreement, these paths SHALL be locked in `patha_field_names.md`.**

### 2.1 Owned write surface

```
cst:
  core:
    status:
      turn_index: int
      layer_count: int
      frozen_layers: [StableID]
    signals:
      # COB + Mux facing
      freeze:
        frozen_objects: [StableID]
        reason: string
      thaw:
        thawed_objects: [StableID]
        reason: string
      continuity_restoration:
        restored_objects: [StableID]
        reason: string
      # MS + Mux facing (raw metrics) — NOT COB commands
      drift:
        affected_objects: [StableID]
        magnitude: number
      oscillation:
        affected_objects: [StableID]
        frequency: number
        amplitude: number
      ambiguity:
        affected_objects: [StableID]
        # heritage also used certainty/ambiguity adjustment lists; map here or under metrics
        increased: [StableID]
        decreased: [StableID]
      collapse:
        collapsed_objects: [StableID]
        severity: number
    metrics:
      per_layer: { <StableID>: { drift, oscillation, ambiguity, stability, collapse, continuity, combined_instability } }
      integrated: { ... }   # 10-turn aggregates as available in v0.1
    history:
      window_len: 10
      turns: [ { turn_index, per_layer_snapshot_ref_or_digest, metric_summary } ]  # capped at 10
    lineage_stability:
      stable_lineage: [StableID]
      unstable_lineage: [StableID]
    audit:
      slice: string
      provisional_metrics: true | false
      notes: [string]
```

Heritage field names for drift/oscillation/collapse/freeze/thaw are retained where possible (`affected_objects`, `magnitude`, etc.). Continuity-restoration is **required** as a first-class signal (normative), even if v0.1 emission is rare under provisional thresholds.

### 2.2 Optional provenance markers

- Append `"cst_core"` to `routing_path` when pipeline convention requires it.  
- Do not invent a second top-level envelope outside `cst.core`.

### 2.3 Strict non-ownership (write-boundary guard)

CST-Core MUST NOT write or mutate:

- COB identity-layer store / `identity.cob_state_snapshot` contents (except indirectly via signals COB may consume later — CST-Core does not edit the snapshot)  
- Create / Split / Merge / Collapse-recovery **commands**  
- `routing_filter`, RED, geometric_state, semantic_core / TP.semantic  
- CIL intake packet  
- CST-MS / CST-Mux internal state (CST-Core only **emits** toward them via TP fields Mux/MS read)  

Guard runs after every `process` call. Violation → hard fail in testbench mode; diagnostic in general mode.

### 2.4 Read-only inputs

- COB stabilized layers / `cob_state_snapshot` (or equivalent object list in fixtures)  
- Optional OuBA committed identity reference (HLR-040)  
- `lineage_log` MERGE/SPLIT markers (hygiene only)  
- Prior `cst.core.history` / freeze status on TP for replay  

---

## 3. Signal Routing (Normative Realization)

| Emit | Write under | Consumers (logical) | Must NOT |
|------|-------------|---------------------|----------|
| freeze, thaw, continuity_restoration | `cst.core.signals.*` | COB, CST-Mux | be omitted from Mux-visible package |
| drift, oscillation, ambiguity, collapse | `cst.core.signals.*` + metrics | CST-MS, CST-Mux | be treated as COB structural commands |
| metric histories | `cst.core.history` / metrics | CST-MS, Mux replay | — |

CST-Core SHALL NOT accept control inputs from CST-MS fields.

---

## 4. Core Operators (v0.1)

### 4.1 Snapshot extraction (minimal)

For each layer in the COB snapshot, record a deterministic minimal snapshot:

- `layer_id`  
- referent_map (as present)  
- anchors (as present)  
- lineage (as present)  
- register (as present)  
- field-importance / importance fields if present  
- freeze flag if present on layer  

Full domain distance inputs may be sparse in early fixtures; missing fields → neutral defaults (0 / empty), documented in audit.

### 4.2 Histories (10-turn window)

- Maintain ordered history length ≤ 10.  
- On each process, append current turn summary; drop oldest when length > 10.  
- Feature counts / frequencies: first-order counts of observed structural keys or metric bins available in fixtures; expand when snapshot schema crystallizes.

### 4.3 Placeholder metric policy (provisional)

Until CP locks final formulas, v0.1 SHALL use **deterministic provisional rules** and set `cst.core.audit.provisional_metrics: true`.

**Allowed provisional sources (priority):**

1. Explicit metric fields already on the layer (fixture-injected) — treated as **inputs to history**, not as “CST invented the physics.”  
2. Simple deterministic functions of consecutive snapshots (e.g. referent_map inequality → drift contribution 1 else 0; flip counts → oscillation).  
3. Combined instability = deterministic aggregate of available provisional components (e.g. max or sum of normalized stubs).

**Forbidden:** random, wall-clock, nondeterministic iteration order without sorting ids.

**Thresholds (v0.1 fixed defaults — Defer for real tables):**

Document constants in code and structural program; example placeholders (CP may replace):

| Threshold | v0.1 default (provisional) |
|-----------|----------------------------|
| freeze | combined_instability ≥ 1.0 |
| thaw / recovery | combined_instability ≤ 0.2 |
| continuity restoration | continuity ≥ 0.8 over window (if computed; else inactive) |
| drift / oscillation / ambiguity / collapse emit | component ≥ 0.5 or boolean flag true |

These defaults exist only so emission paths and tests can run. They are **not** normative physics.

### 4.4 Local freeze / thaw policy

- When Freeze is emitted for a layer, subsequent turns **halt** snapshot-driven metric updates and threshold adaptation for that layer until Thaw (HLR-024–026, 028–030).  
- Histories may still record “frozen, no update” markers for replay.  

### 4.5 MERGE/SPLIT hygiene (not structural authority)

If `lineage_log` contains MERGE/SPLIT events, exclude parent ids from collapse/drift **false positives** for that turn (heritage behavior). Do **not** issue merge/split commands.

### 4.6 Continuity-restoration

Always include `signals.continuity_restoration` in the envelope. Emission of non-empty `restored_objects` follows provisional continuity threshold when continuity is computed; otherwise empty list is valid v0.1 behavior if documented.

---

## 5. Dual-Mode Testbench Alignment

Follow progressive_lineup_testing.md:

| mode | Input | Validation |
|------|--------|------------|
| testbench | `cst_core_testbench.yaml` | exact/structural match on owned `cst.core` fields |
| general | `cst_core_input.yaml` | `cst_core_rules.yaml` + rulechecker only |

Category: `testbenches/path_a/context/`.

Suggested first Must-Prove tests:

- Envelope present at `cst.core`  
- Signal dict shapes for drift / freeze / thaw / continuity_restoration  
- Raw metrics not written as COB snapshot mutations  
- 10-turn history cap  
- MERGE parent exclusion hygiene  
- Deterministic replay  
- Write-boundary guard  

---

## 6. Must-Prove for v0.1

- `process(tp, mode=...)` and `PRIMITIVE_NAME == "cst_core"`  
- Writes only under proposed `cst.core` (+ optional routing_path marker)  
- Freeze / Thaw / Continuity-restoration keys always present under `signals`  
- Drift / Oscillation / Ambiguity / Collapse keys present; not applied as COB topology edits  
- History window length ≤ 10  
- Local freeze halts metric updates for frozen layer ids  
- MERGE/SPLIT parent hygiene when lineage events present  
- Deterministic outputs for fixed inputs + history  
- Dual-mode progressive wiring  
- `audit.provisional_metrics` true while stubs used  

---

## 7. Defer

- Final structural distance functions per domain  
- Final ambiguity / stability / collapse formulas  
- Combined-instability weighting  
- Layer-specific threshold tables and monotonic adaptation law  
- Continuity restoration **queue** semantics (HLR-034 full meaning)  
- Full snapshot field schema beyond minimal extract  
- Live CST-MS / Mux integration tests beyond TP field presence  
- patha_field_names hard lock (immediately after CP path approval)  

---

## 8. Implementation Order Recommendation

1. Envelope helpers + write-boundary guard + empty signal shells  
2. Snapshot extract + history window  
3. Provisional metrics + threshold emission for freeze/thaw  
4. Continuity-restoration shell + lineage hygiene  
5. `process` orchestration  
6. Progressive dual-mode testbench (replace bak runner)  
7. patha_field_names path lock once CP signs §2  

---

## 9. Research Questions for CP

1. Confirm §2 nested map (`cst.core.signals|metrics|history|status|audit`) as the single envelope.  
2. Prefer history **on TP** for all progressive tests, or allow instance-held history for multi-turn fixtures?  
3. Accept v0.1 threshold defaults in §4.3 or supply alternate constants before coding?  
4. Should certainty_adjustment remain a separate signal block (heritage) or fold only under `signals.ambiguity`?  
5. Continuity-restoration: empty list OK for v0.1 when continuity not yet computed, or require a stub continuity score immediately?  

---

**End of cst_core_py_struc_pgm.md (v0.1)**  
Ready for CP review. Realization of `cst_core.py` should wait for path confirmation (§2) and any threshold constant overrides.

# **ctp_py_struc_pgm.md — Structural Program for CTP (Python Implementation Scaffold)**
### *Aligned with 20.145 (v3.0) and progressive_lineup_testing.md (v4.2)*
### *Informative — Implementation Guidance Only*

---

## 1. Purpose

`ctp.py` implements the **Collect Thought Point (CTP‑prm)** as defined in **20.145 (v3.0)**.

CTP’s structural program:

- runs as the **always‑before‑RB** barrier on Path A (`… → TR → CTP → RB → …`)
- applies a **policy freeze** only (no deep‑copy snapshot object, no required `TP.CTP` block, no freeze flag)
- appends **exactly one** schema‑stable `metadata.cognitive_history[]` entry per invocation
- writes `metadata.provenance.ctp_last_update`
- copies foundation / IdOB / RB observation fields when present; writes **`null`** when missing; never invents; never omits required keys
- does **not** wait for IdOB, collect multi‑IdOB outputs, validate IdOB‑chains, route, score, or mutate semantics
- supports deterministic replay and progressive lineup dual‑mode testing

This scaffold is designed so that, given:

- `progressive_lineup_testing.md` (v4.2+)
- `20.145_ctp_prim.md` (v3.0+)
- `ctp_py_struc_pgm.md`

a capable AI can write:

- `ctp.py`
- `ctp_testbench.py`
- `ctp_testbench.yaml`
- `ctp_input.yaml`
- `ctp_tests_to_run.yaml`
- `ctp_rules.yaml`
- `ctp_rulechecker.py`

and activate CTP in `run.py`.

**Testbench category (progressive_lineup §11):** `path_a/routing/`

```
testbenches/path_a/routing/
  ctp_testbench.py
  ctp_testbench.yaml
  ctp_input.yaml
  ctp_tests_to_run.yaml
  ctp_rules.yaml
  ctp_rulechecker.py

primitives/ctp/
  ctp.py
  ctp_py_struc_pgm.md
```

**Path‑A adjacency (locked)**

```
DCB → TR → CTP → RB → WrdNm → ISc → RTU → TR → CTP → RB → …
```

---

## 2. Inputs and Outputs

### 2.1 Inputs (v1 read‑set)

CTP may **read** any TP fields needed to **copy** into cognitive‑history. It must not interpret them.

| Source | Path / key | Notes |
|--------|------------|-------|
| Full TP | current envelope | Freeze‑as‑is; no IdOB required |
| Cycle id | `metadata.provenance` DCB markers if present; else runner / fixture | See §2.3 |
| Timestamp | runner‑supplied in testbench; system/runner otherwise | Deterministic in tests |
| Foundation proxies | optional `_ctp_foundation` or existing TP foundation locations | Copy if present |
| IdOB observation | `semantic.idob` / equivalent if present | Copy if present |
| RB observation | `process.routing_filter` RED fields if present | Copy if present |

**Recommended fixture convenience (optional, not a required owned write target)**

```yaml
_ctp_cycle_context:
  cycle_id: 0
  timestamp: 1000.0

_ctp_foundation:
  I_stab: 0.8
  R_res: 0.7
  P_cont: 0.6
  L_depth: 1
  Rt_adj: 0.2
  delta_H: 0.05
  E_dens: 0.4
  C_coh: 0.9
```

`ctp.py` may read `_ctp_cycle_context` / `_ctp_foundation` for isolation tests. Prefer real TP paths when present (`metadata.provenance`, `process.routing_filter`, `semantic.idob`).

**Forbidden uses**

- inventing missing foundation / IdOB / RB values
- waiting for IdOB or multi‑IdOB collection
- semantic merge, routing, scoring, arbitration
- reading Pipeline‑B as authority
- hidden mutable global state across invocations

### 2.2 Outputs (CTP‑owned only)

| Path | Behavior |
|------|----------|
| `metadata.cognitive_history[]` | Append exactly one entry |
| `metadata.provenance.ctp_last_update` | Set to invocation timestamp |
| optional `exec_trace` CTP ref | Diagnostic side channel only |

**Must not write**

- IdOB envelope / semantic identity ownership
- RB `process.routing_filter`
- TR / `tr_needs_update`
- DCB `geometric_state` / `geometric_history` / `dcb_events`
- context metadata, routing_metadata, semantic_core, intake
- required `TP.CTP` block or freeze‑flag field (v1)

### 2.3 Cycle id and timestamp resolution (v1)

```python
def _resolve_cycle_id(tp, ctx) -> int | None:
    # 1. explicit fixture/runner context
    if ctx.get("cycle_id") is not None:
        return int(ctx["cycle_id"])
    # 2. DCB provenance markers if present (playground convention)
    prov = (tp.get("metadata") or {}).get("provenance") or {}
    if prov.get("dcb_cycle_id") is not None:
        return int(prov["dcb_cycle_id"])
    # 3. last geometric_history cycle_id if present
    hist = (tp.get("metadata") or {}).get("geometric_history") or []
    if hist and isinstance(hist[-1], dict) and hist[-1].get("cycle_id") is not None:
        return int(hist[-1]["cycle_id"])
    return None  # stored as null in history entry

def _resolve_timestamp(tp, ctx) -> float | None:
    if ctx.get("timestamp") is not None:
        return float(ctx["timestamp"])
    prov = (tp.get("metadata") or {}).get("provenance") or {}
    if prov.get("dcb_last_update") is not None:
        return float(prov["dcb_last_update"])
    return None  # testbench fixtures should always supply timestamp
```

In **testbench mode**, fixtures **must** supply deterministic `timestamp` (and should supply `cycle_id`) via `_ctp_cycle_context` or constructor kwargs.

### 2.4 Cognitive‑history entry shape (schema‑stable)

Every entry **must** include all keys below. Missing sources → `null`.

```python
{
    "cycle_id": int | None,
    "timestamp": float | None,
    "invariants": {
        "I_stab": float | None,
        "R_res": float | None,
        "P_cont": float | None,
        "L_depth": float | int | None,
        "Rt_adj": float | None,
        "delta_H": float | None,
        "E_dens": float | None,
        "C_coh": float | None,
    },
    "idob_geometry": {
        "neighborhood": Any | None,
        "k_id": Any | None,
    },
    "idob_roles": Any | None,
    "idob_residue": Any | None,
    "idob_stability": Any | None,
    "rb_adjacency_class": str | None,
    "rb_displacement_scale": str | None,
    "rb_regime_hint": str | None,
    "rb_route_proposal": Any | None,
}
```

Key order should be stable for deterministic serialization in tests.

---

## 3. High‑Level Program Structure

```python
PRIMITIVE_NAME = "ctp"

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

class CTP:
    def __init__(self, tp_input=None, cycle_id=None, timestamp=None):
        self.tp = copy.deepcopy(tp_input or {})
        ctx = self.tp.get("_ctp_cycle_context") or {}
        if not isinstance(ctx, dict):
            ctx = {}
        self.cycle_id = cycle_id if cycle_id is not None else ctx.get("cycle_id")
        self.timestamp = timestamp if timestamp is not None else ctx.get("timestamp")

    def process(self) -> dict:
        # 1. Resolve cycle_id / timestamp (null allowed if truly absent)
        cycle_id = self._resolve_cycle_id()
        timestamp = self._resolve_timestamp()

        # 2. Policy freeze: no semantic/routing mutation (identity operation on owned domains)
        #    (explicit no-op marker for readability; no TP.CTP block)

        # 3. Build cognitive-history entry (copy or null)
        entry = self._build_cognitive_history_entry(cycle_id, timestamp)

        # 4. Append exactly one entry
        self._append_cognitive_history(entry)

        # 5. Provenance
        self._write_provenance(timestamp)

        # 6. Optional audit
        self._append_audit_optional(cycle_id, timestamp)

        return self.tp

def run(tp: dict, **kwargs) -> dict:
    return CTP(tp, **kwargs).process()
```

**Mandatory helpers**

| Helper | Responsibility |
|--------|----------------|
| `_resolve_cycle_id` | Fixture → DCB provenance → geometric_history → None |
| `_resolve_timestamp` | Fixture → dcb_last_update → None |
| `_build_cognitive_history_entry` | Fixed key schema; copy or null; never invent |
| `_read_foundation_value` | From `_ctp_foundation` or declared TP paths |
| `_read_idob_observation` | From semantic.idob / equivalent |
| `_read_rb_observation` | From process.routing_filter RED fields |
| `_append_cognitive_history` | Append‑only; create list if missing |
| `_write_provenance` | `metadata.provenance.ctp_last_update` |
| `_append_audit_optional` | Optional exec_trace ctp_ref |

---

## 4. Computation Contracts (v1 Foundation)

### 4.1 Policy freeze

CTP does not create a snapshot object. “Freeze” means:

- CTP does not mutate non‑owned fields
- CTP’s only durable side effects are history append + provenance (+ optional audit)
- RB may read the same TP continuum after CTP returns

### 4.2 One history entry per invocation

```python
hist = meta.setdefault("cognitive_history", [])
# ensure list
hist.append(entry)  # exactly once
```

### 4.3 Null policy

```python
def _copy_or_null(value):
    return value if value is not None else None
```

All required keys always present.

### 4.4 Source priority for foundation fields (recommended)

1. `_ctp_foundation[key]` if isolation fixture present  
2. else `process.routing_filter` / known foundation TP paths if present  
3. else `null`

Do not recompute ΔH, regimes, or geometry.

### 4.5 Determinism

Identical TP + identical cycle_id/timestamp inputs → identical history entry and provenance timestamp write.

No randomness; stable key order in entry dict.

### 4.6 Messy / partial TP

Still succeeds. History filled with nulls where sources missing. No reject.

---

## 5. Primitive Boundary Discipline

| Action | Allowed |
|--------|---------|
| Read TP for copy into history | Yes |
| Read optional `_ctp_cycle_context` / `_ctp_foundation` | Yes |
| Append `metadata.cognitive_history[]` | Yes |
| Write `metadata.provenance.ctp_last_update` | Yes |
| Optional exec_trace CTP ref | Yes |
| Write TR / RB filter / IdOB / DCB ownership | **No** |
| Create required `TP.CTP` / freeze flag | **No** (v1) |
| Wait for / validate IdOB | **No** |
| Semantic merge / routing / scoring | **No** |

---

## 6. Determinism, Replay, Testbench Compatibility

| mode | Input | Validation |
|------|--------|------------|
| `testbench` | `ctp_testbench.yaml` | Structural foundation comparison |
| `general` | `ctp_input.yaml` | `ctp_rules.yaml` + rulechecker |

Follow progressive_lineup §3.7 import path, §3.8 naming, §3.9 report format, §3.11 structural comparison.

**Structural comparison focus**

- history length delta == 1
- last history entry schema keys present
- expected null vs concrete values when specified
- `provenance.ctp_last_update`
- write‑boundary: TR, RB filter, DCB geometry, semantic IdOB, residue, context unchanged
- replay: two runs → identical last entry (given same timestamp/cycle_id)

---

## 7. Error Handling

- Missing IdOB / foundation / RB fields: **null**, no error
- Missing cognitive_history list: create empty list then append
- Malformed `metadata` (not a dict): normalize to dict in controlled way or raise `ValueError` in test/dev if metadata is a non‑dict incompatible type
- Never silent semantic repair of meaning fields

---

## 8. Relationship to Other Artifacts

| Artifact | Role |
|----------|------|
| `20.145` v3.0+ | Normative HLRs |
| `progressive_lineup_testing.md` v4.2+ | Dual‑mode testing contract |
| `ctp.py` | Implementation |
| Testbench suite | Foundation lock |
| `run.py` | `use_ctp: True` activation |
| TR | Upstream producer of `TP.TR` before CTP |
| RB | Downstream consumer after CTP |
| DCB | Source of geometric_history / provenance for cycle_id hints |

---

## 9. Concrete Fixture Shapes (Foundation Cases)

Aim for **≥12 enabled foundation cases** covering placement‑independent isolation behavior.

### 9.1 Minimal — no foundation, no IdOB, no RB filter

```yaml
id: ctp_minimal_null_history
description: Missing sources → full schema with nulls; history len +1
enabled: true
input:
  _ctp_cycle_context:
    cycle_id: 0
    timestamp: 1000.0
  metadata:
    context:
      topic: minimal
      stance: neutral
      intent: test
      continuity: new
      direction: forward
      coherence: stable
      importance: low
expected:
  history_len: 1
  last_entry:
    cycle_id: 0
    timestamp: 1000.0
    invariants:
      I_stab: null
      R_res: null
      P_cont: null
      L_depth: null
      Rt_adj: null
      delta_H: null
      E_dens: null
      C_coh: null
    idob_geometry:
      neighborhood: null
      k_id: null
    idob_roles: null
    idob_residue: null
    idob_stability: null
    rb_adjacency_class: null
    rb_displacement_scale: null
    rb_regime_hint: null
    rb_route_proposal: null
  provenance_ctp_last_update: 1000.0
  check_write_boundary: true
```

### 9.2 Foundation present via `_ctp_foundation`

```yaml
id: ctp_foundation_copy
input:
  _ctp_cycle_context: { cycle_id: 1, timestamp: 1001.0 }
  _ctp_foundation:
    I_stab: 0.85
    R_res: 0.75
    P_cont: 0.7
    L_depth: 2
    Rt_adj: 0.2
    delta_H: 0.05
    E_dens: 0.4
    C_coh: 0.9
  metadata:
    context: { topic: foundation, stance: neutral, intent: test, continuity: same, direction: forward, coherence: stable, importance: medium }
expected:
  history_len: 1
  last_entry:
    cycle_id: 1
    timestamp: 1001.0
    invariants:
      I_stab: 0.85
      R_res: 0.75
      P_cont: 0.7
      L_depth: 2
      Rt_adj: 0.2
      delta_H: 0.05
      E_dens: 0.4
      C_coh: 0.9
```

### 9.3 IdOB observation present

```yaml
id: ctp_idob_present
input:
  _ctp_cycle_context: { cycle_id: 2, timestamp: 1002.0 }
  semantic:
    idob:
      roles: [observer]
      residue: persist
      stability: 0.8
      geometry:
        neighborhood: local
        k_id: 3
  metadata:
    context: { topic: idob, stance: neutral, intent: test, continuity: same, direction: forward, coherence: stable, importance: medium }
expected:
  history_len: 1
  last_entry:
    idob_roles: [observer]
    idob_residue: persist
    idob_stability: 0.8
    idob_geometry:
      neighborhood: local
      k_id: 3
  check_idob_unchanged: true
```

### 9.4 RB RED fields present on routing_filter

```yaml
id: ctp_rb_fields_present
input:
  _ctp_cycle_context: { cycle_id: 3, timestamp: 1003.0 }
  process:
    routing_filter:
      selected_ob_ids: [ob_a]
      adjacency_class: local
      displacement_scale: small
      regime_hint: Stable
      route_proposal: null
  metadata:
    context: { topic: rb, stance: neutral, intent: test, continuity: same, direction: forward, coherence: stable, importance: medium }
expected:
  history_len: 1
  last_entry:
    rb_adjacency_class: local
    rb_displacement_scale: small
    rb_regime_hint: Stable
    rb_route_proposal: null
  check_rb_filter_unchanged: true
```

### 9.5 Write boundary — TR / DCB / residue / context unchanged

```yaml
id: ctp_write_boundary
input:
  _ctp_cycle_context: { cycle_id: 4, timestamp: 1004.0 }
  tr_needs_update: false
  TR:
    stance: neutral
    intent: inform
  process:
    routing_filter:
      selected_ob_ids: [ob_locked]
  semantic:
    identity:
      persona: locked
  metadata:
    geometric_state:
      position: 3
      direction: 4
      curvature: 0.0
      step_index: 2
      lane_id: 0
    residue:
      marker: locked
    context:
      topic: boundary
      stance: neutral
      intent: test
      continuity: same
      direction: forward
      coherence: stable
      importance: high
expected:
  history_len: 1
  check_write_boundary: true
  check_tr_unchanged: true
  check_dcb_unchanged: true
  check_rb_filter_unchanged: true
```

### 9.6 Append‑only — pre‑seeded history

```yaml
id: ctp_append_only
input:
  _ctp_cycle_context: { cycle_id: 5, timestamp: 1005.0 }
  metadata:
    cognitive_history:
      - { cycle_id: 0, timestamp: 900.0, invariants: { I_stab: null, R_res: null, P_cont: null, L_depth: null, Rt_adj: null, delta_H: null, E_dens: null, C_coh: null }, idob_geometry: { neighborhood: null, k_id: null }, idob_roles: null, idob_residue: null, idob_stability: null, rb_adjacency_class: null, rb_displacement_scale: null, rb_regime_hint: null, rb_route_proposal: null }
    context: { topic: append, stance: neutral, intent: test, continuity: same, direction: forward, coherence: stable, importance: low }
expected:
  history_len: 2
  prior_entry_unchanged: true
  last_entry:
    cycle_id: 5
    timestamp: 1005.0
```

### 9.7 Cycle_id from geometric_history when context omits cycle_id

```yaml
id: ctp_cycle_from_dcb_history
input:
  _ctp_cycle_context:
    timestamp: 1006.0
    # cycle_id omitted on purpose
  metadata:
    geometric_history:
      - { position: 2, direction: 3, curvature: 0.0, step_index: 1, lane_id: 0, cycle_id: 7, timestamp: 1005.0 }
    context: { topic: cycle_src, stance: neutral, intent: test, continuity: same, direction: forward, coherence: stable, importance: low }
expected:
  history_len: 1
  last_entry:
    cycle_id: 7
    timestamp: 1006.0
```

### 9.8 Deterministic replay

```yaml
id: ctp_replay_identical
input:
  _ctp_cycle_context: { cycle_id: 8, timestamp: 1008.0 }
  _ctp_foundation: { I_stab: 0.5, R_res: 0.5, P_cont: 0.5, L_depth: 1, Rt_adj: 0.1, delta_H: 0.0, E_dens: 0.2, C_coh: 0.8 }
  metadata:
    context: { topic: replay, stance: neutral, intent: test, continuity: same, direction: forward, coherence: stable, importance: medium }
expected:
  history_len: 1
  check_replay: true
```

### 9.9 Schema completeness (all keys present)

```yaml
id: ctp_schema_complete
input:
  _ctp_cycle_context: { cycle_id: 9, timestamp: 1009.0 }
  metadata:
    context: { topic: schema, stance: neutral, intent: test, continuity: new, direction: forward, coherence: stable, importance: low }
expected:
  history_len: 1
  check_history_schema_complete: true
```

### 9.10 No invent — partial foundation only some keys

```yaml
id: ctp_partial_foundation
input:
  _ctp_cycle_context: { cycle_id: 10, timestamp: 1010.0 }
  _ctp_foundation:
    I_stab: 0.9
    # others omitted
  metadata:
    context: { topic: partial, stance: neutral, intent: test, continuity: new, direction: forward, coherence: stable, importance: low }
expected:
  history_len: 1
  last_entry:
    invariants:
      I_stab: 0.9
      R_res: null
      P_cont: null
      L_depth: null
      Rt_adj: null
      delta_H: null
      E_dens: null
      C_coh: null
```

### 9.11 Combined TR + foundation + IdOB (pre‑RB package view)

```yaml
id: ctp_combined_pre_rb
input:
  _ctp_cycle_context: { cycle_id: 11, timestamp: 1011.0 }
  _ctp_foundation: { I_stab: 0.7, R_res: 0.6, P_cont: 0.5, L_depth: 1, Rt_adj: 0.3, delta_H: 0.1, E_dens: 0.3, C_coh: 0.7 }
  TR:
    stance: neutral
    intent: inform
    tension: low
  semantic:
    idob:
      roles: [assistant]
      stability: 0.7
      residue: light
      geometry: { neighborhood: local, k_id: 1 }
  metadata:
    context: { topic: combined, stance: neutral, intent: test, continuity: same, direction: forward, coherence: stable, importance: medium }
expected:
  history_len: 1
  last_entry:
    invariants:
      I_stab: 0.7
      delta_H: 0.1
    idob_stability: 0.7
  check_tr_unchanged: true
```

### 9.12 Empty / missing metadata resilience

```yaml
id: ctp_missing_metadata_block
input:
  _ctp_cycle_context: { cycle_id: 12, timestamp: 1012.0 }
  # no metadata key at all
expected:
  history_len: 1
  last_entry:
    cycle_id: 12
    timestamp: 1012.0
  provenance_ctp_last_update: 1012.0
```

---

## 10. Rules / Rulechecker Mapping (v1)

| rule id | check method | Intent |
|---------|--------------|--------|
| ctp_output_001 | `deterministic_output_present` | Output TP exists |
| ctp_history_001 | `one_history_append` | History grew by exactly 1 |
| ctp_schema_001 | `history_entry_schema_complete` | All required keys on last entry |
| ctp_null_001 | `missing_sources_are_null` | Absent sources are null, not omitted/invented |
| ctp_append_001 | `prior_history_unchanged` | Prior entries unmodified |
| ctp_provenance_001 | `provenance_ctp_last_update` | provenance.ctp_last_update set when timestamp known |
| ctp_boundary_001 | `only_ctp_fields_written` | No TR/RB/IdOB/DCB/context mutation |
| ctp_no_reject_001 | `succeeds_without_idob` | Completes with no IdOB present |
| ctp_progressive_001 | `progressive_lineup_compatibility` | Output usable in lineup |

---

## 11. Testbench Comparison Strategy (v1)

**Structural foundation comparison** (not full TP deep equality):

- `history_len` or delta
- `last_entry` field equality where specified
- `check_history_schema_complete`
- `provenance_ctp_last_update`
- write‑boundary flags (`check_tr_unchanged`, `check_dcb_unchanged`, `check_rb_filter_unchanged`, `check_idob_unchanged`, `check_write_boundary`)
- `check_replay`
- `prior_entry_unchanged`

Print context summary + CTP extras:

```
- history_len
- last cycle_id / timestamp
- rb_regime_hint (if any)
- idob_stability (if any)
```

---

## 12. What v1 Must Prove vs Defer

**Must prove**

- Always runs without requiring IdOB
- Exactly one cognitive‑history append per invocation
- Schema‑stable entry; missing → null; no key omission; no invention
- Append‑only (priors untouched)
- Provenance `ctp_last_update` when timestamp available
- Write boundary vs TR, RB filter, DCB geometry, IdOB, residue, context
- Deterministic replay under fixed cycle_id/timestamp
- cycle_id resolution from fixture and from geometric_history fallback
- Dual‑mode progressive compatibility
- No reject on empty/partial TP

**Defer**

- Multi‑IdOB collect/combine/wait
- Deep‑copy snapshot object / `TP.CTP` block / freeze flag
- IdOB‑chain validation / reject paths
- Parallel IdOB fan‑in packaging
- Recomputation of invariants or RED labels

---

## 13. Implementation Order (Recommended)

1. Lock read of 20.145 v3.0 + this scaffold + progressive_lineup §3.11  
2. Implement `ctp.py` (resolve → build entry → append → provenance)  
3. `ctp_rules.yaml` + `ctp_rulechecker.py`  
4. Foundation fixtures in `ctp_testbench.yaml` + `ctp_tests_to_run.yaml` (enable all §9 cases)  
5. `ctp_testbench.py` dual mode  
6. `ctp_input.yaml`  
7. Activate only CTP in `run.py`  
8. Green pass → treat as foundation before CTP↔RB pipeline smoke  

---

## 14. Versioned Free Parameters (Provisional Defaults)

| Parameter | Provisional default | Change policy |
|-----------|---------------------|---------------|
| History schema key set | §2.4 | minor version + fixtures |
| Missing value | `null` | locked |
| Snapshot object / TP.CTP | not created | deferred |
| IdOB wait/collect | disabled | deferred |
| cycle_id resolution order | fixture → provenance → geometric_history → null | minor version |

---

**End of Document — ctp_py_struc_pgm.md (Deterministic Policy‑Freeze + Cognitive‑History Scaffold)**

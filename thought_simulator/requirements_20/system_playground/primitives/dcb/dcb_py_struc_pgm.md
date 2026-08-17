# **dcb_py_struc_pgm.md — Structural Program for DCB (Python Implementation Scaffold)**
### *Aligned with 20.106_dcb_prim.md (v5.3) and progressive_lineup_testing.md*
### *Informative — Implementation Guidance Only*

---

## 1. Purpose

`dcb.py` implements the **Directional Conversation Basin (DCB‑prm)** as defined in **20.106 (v5.3)**.

DCB’s structural program:

- indexes TP movement through the Path‑A routing loop using a fixed ordinal table
- overwrites a five‑field scalar `geometric_state` snapshot each invocation
- appends one `geometric_history` entry per invocation
- emits `cycle_start` (first cycle) or delta events (subsequent field changes)
- writes minimal provenance (`dcb_last_update`)
- obeys a narrow read‑set and strict write boundary (no semantic / structural / identity / routing interpretation)
- supports deterministic replay and progressive lineup testing

This scaffold is designed so that, given:

- `progressive_lineup_testing.md`
- `20.106` (v5.3 or later, implementation‑bound)
- `dcb_py_struc_pgm.md`

a capable AI can write:

- `dcb.py`
- `dcb_testbench.py`
- `dcb_testbench.yaml`
- `dcb_input.yaml`
- `dcb_tests_to_run.yaml`
- `dcb_rules.yaml`
- `dcb_rulechecker.py`

and activate DCB in `run.py`.

**Testbench category (progressive_lineup §11):** `path_a/routing/`

```
testbenches/path_a/routing/
  dcb_testbench.py
  dcb_testbench.yaml
  dcb_input.yaml
  dcb_tests_to_run.yaml
  dcb_rules.yaml
  dcb_rulechecker.py

primitives/dcb/
  dcb.py
  dcb_py_struc_pgm.md
```

---

## 2. Inputs and Outputs

### 2.1 Inputs (v1 read‑set only)

DCB may read **only**:

| Source | Field / key | Notes |
|--------|-------------|-------|
| TP | `metadata.geometric_state` | Previous snapshot if present; else absent |
| Runner cycle context | `current_primitive_id` | String name in PATH_A (e.g. `"RBU"`, `"DCB"`, `"TR"`) |
| Runner cycle context | `cycle_id` | Integer |
| Runner cycle context | `timestamp` | Float; deterministic in testbench mode |

**How cycle context is supplied (implementation convention)**

For progressive isolation tests, embed runner context under a reserved TP key that DCB reads and does **not** treat as a general metadata domain:

```yaml
# Recommended fixture convention (not a DCB-owned write target)
_dcb_cycle_context:
  current_primitive_id: "RBU"
  cycle_id: 0
  timestamp: 1000.0
```

`dcb.py` reads `_dcb_cycle_context` (or an equivalent constructor argument) and **must not** persist or reinterpret any other TP fields.

Alternatively, the class may accept explicit kwargs:

```python
DCB(tp_input, current_primitive_id="RBU", cycle_id=0, timestamp=1000.0)
```

Testbench mode should prefer explicit kwargs or the `_dcb_cycle_context` block so fixtures stay self‑contained.

**Forbidden reads (HLR‑20.106‑001)**

DCB shall not read semantic, structural, identity, or routing metadata for indexing or any other purpose.

---

### 2.2 Outputs (DCB‑owned fields only)

`dcb.py` writes **only**:

| Path | Behavior |
|------|----------|
| `TP.metadata.geometric_state` | Overwrite entire five‑field snapshot |
| `TP.metadata.geometric_history[]` | Append exactly one entry |
| `TP.metadata.dcb_events[]` | Append `cycle_start` or one delta event |
| `TP.metadata.provenance.dcb_last_update` | Set to runner `timestamp` |

**geometric_state shape**

```python
geometric_state = {
    "position": int,      # ordinal(current_primitive_id) ∈ [0, N-1]
    "direction": int,     # (position + 1) mod N
    "curvature": float,   # 0.0 or 1.0 (v1)
    "step_index": int,    # 0 on first cycle; else prev + 1
    "lane_id": int,       # always 0 in v1
}
```

**geometric_history entry shape**

```python
{
    "position": int,
    "direction": int,
    "curvature": float,
    "step_index": int,
    "lane_id": int,
    "cycle_id": int,
    "timestamp": float,
}
```

**dcb_events entry shapes**

Delta (subsequent cycle, any field changed):

```python
{
    "prev_position": int,
    "new_position": int,
    "prev_direction": int,
    "new_direction": int,
    "prev_curvature": float,
    "new_curvature": float,
    "prev_step_index": int,
    "new_step_index": int,
    "prev_lane_id": int,
    "new_lane_id": int,
    "cycle_id": int,
    "timestamp": float,
    "event_type": "delta",   # recommended discriminant for tests
}
```

First cycle (`cycle_start`):

```python
{
    "prev_position": None,
    "new_position": int,
    "prev_direction": None,
    "new_direction": int,
    "prev_curvature": None,
    "new_curvature": float,
    "prev_step_index": None,
    "new_step_index": int,
    "prev_lane_id": None,
    "new_lane_id": int,
    "cycle_id": int,
    "timestamp": float,
    "event_type": "cycle_start",
}
```

All `prev_*` keys are present; values are JSON `null` / Python `None` on first cycle.

**Provenance**

```python
TP.metadata.provenance.dcb_last_update = timestamp  # float from runner
```

No other provenance fields are required in v1.

Optional audit (recommended, non‑normative parity with STPX/RBU):

```python
TP.exec_trace.append({
    "dcb_ref": {
        "origin": "DCB",
        "last_update": "DCB",
        "cycle_id": cycle_id,
        "event_type": "cycle_start" | "delta" | "none",
    }
})
```

If used, `exec_trace` append is allowed as a diagnostic side channel; it must not replace `dcb_events`.

---

## 3. Path‑A Routing‑Loop Ordinal Table (v1)

Normative for DCB indexing (from 20.106 §3.1):

```python
PATH_A = ["STPX", "RBU", "DCB", "TR", "CTP", "ISc", "RTU", "RB", "IdOB", "MCB"]
N = len(PATH_A)  # 10

def ordinal(primitive_id: str) -> int:
    # case-sensitive match to PATH_A entries
    return PATH_A.index(primitive_id)
```

- `position ∈ [0, N-1]`
- `direction ∈ [0, N-1]`
- Unknown `current_primitive_id` → raise `ValueError` in development/test modes

Intake / encoder / pre‑STPX structure primitives are outside DCB’s v1 index domain.

---

## 4. High‑Level Program Structure (ISc / STPX / RBU‑Aligned)

`dcb.py` follows the **class + `process()`** pattern so the progressive testbench can instantiate and call it uniformly.

```python
PRIMITIVE_NAME = "dcb"  # lowercase — must match directory and progressive naming

PATH_A = ["STPX", "RBU", "DCB", "TR", "CTP", "ISc", "RTU", "RB", "IdOB", "MCB"]
N = len(PATH_A)

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

class DCB:
    def __init__(
        self,
        tp_input=None,
        current_primitive_id=None,
        cycle_id=None,
        timestamp=None,
    ):
        self.tp = copy.deepcopy(tp_input or {})
        ctx = (self.tp.get("_dcb_cycle_context") or {})
        self.current_primitive_id = current_primitive_id or ctx.get("current_primitive_id")
        self.cycle_id = cycle_id if cycle_id is not None else ctx.get("cycle_id")
        self.timestamp = timestamp if timestamp is not None else ctx.get("timestamp")

    def process(self) -> dict:
        # 1. Validate cycle context
        self._validate_cycle_context()

        # 2. Read previous geometric_state (if any)
        prev = self._read_prev_geometric_state()

        # 3. Compute new geometric_state (pure)
        new_state = self._compute_geometric_state(prev)

        # 4. Write geometric_state (overwrite)
        self._write_geometric_state(new_state)

        # 5. Emit events (cycle_start XOR delta)
        self._emit_events(prev, new_state)

        # 6. Append history
        self._append_history(new_state)

        # 7. Write provenance
        self._write_provenance()

        # 8. Optional audit
        self._append_audit(prev, new_state)

        return self.tp

def run(tp: dict, **kwargs) -> dict:
    """Functional entrypoint matching structural-program language."""
    return DCB(tp, **kwargs).process()
```

**Mandatory helpers (names may vary; responsibilities may not)**

| Helper | Responsibility |
|--------|----------------|
| `_validate_cycle_context()` | Ensure `current_primitive_id`, `cycle_id`, `timestamp` present; `current_primitive_id` in PATH_A |
| `_read_prev_geometric_state()` | Return previous five‑field dict or `None` |
| `_compute_geometric_state(prev)` | Pure §5 formulas → new five‑field dict |
| `_write_geometric_state(state)` | Overwrite `metadata.geometric_state` |
| `_emit_events(prev, new_state)` | First cycle → one `cycle_start`; else delta iff any field changed |
| `_append_history(state)` | Append one history entry with cycle_id + timestamp |
| `_write_provenance()` | Set `metadata.provenance.dcb_last_update = timestamp` |
| `_append_audit(prev, new_state)` | Optional `exec_trace` `dcb_ref` |
| `_ordinal(primitive_id)` | PATH_A index |
| `_fields_changed(prev, new_state)` | Boolean comparison of five scalars |

Lifecycle order is normative in spirit (20.106 §9): compute → events → history → provenance.

---

## 5. Computation Contract (v1) — Pure Functions

Aligned with 20.106 §4.

```python
curr = ordinal(current_primitive_id)
position = curr
direction = (curr + 1) % N
lane_id = 0

if prev is None:
    step_index = 0
    curvature = 0.0
else:
    step_index = prev["step_index"] + 1
    expected_direction = (prev["position"] + 1) % N
    curvature = 0.0 if direction == expected_direction else 1.0
```

### 5.1 First‑cycle event policy

If `prev is None`:

- write geometric_state
- append exactly one history entry
- emit exactly one `cycle_start` event (`prev_* = None`, `new_* = state`)
- do **not** also emit a delta event on the same invocation

### 5.2 Subsequent‑cycle event policy

If `prev` exists and any of the five fields differs from `prev`:

- emit exactly one delta event with full prev/new pairs

If `prev` exists and no field differs (should not occur when `step_index` increments):

- emit no event

Because `step_index` always increments when `prev` exists, a delta is expected on every subsequent invocation under normal v1 rules.

---

## 6. Primitive Boundary Discipline

`dcb.py` enforces:

**Reads**

- previous `geometric_state`
- runner cycle context only (`current_primitive_id`, `cycle_id`, `timestamp`)
- no semantic / structural / identity / routing metadata

**Writes**

- `metadata.geometric_state` (overwrite)
- `metadata.geometric_history` (append‑only)
- `metadata.dcb_events` (append‑only)
- `metadata.provenance.dcb_last_update` only

**Forbidden**

- no modification of `semantic.*`, residue, SSG fields, process, intake, context payload, routing_metadata, identity_metadata, TPTB/TPSF, truth/done
- no hidden internal state across invocations (HLR‑20.106‑012); all durable state lives in the TP outputs above

---

## 7. Determinism, Replay, and Testbench Compatibility

`dcb.py` is expected to:

- produce identical outputs for identical TP + cycle context
- use pure functions for geometric_state
- avoid randomness and non‑deterministic key ordering in emitted structures
- rely on runner‑supplied deterministic timestamps in testbench mode

The DCB testbench will verify:

- five‑field snapshot overwrite
- exactly one history entry per invocation
- `cycle_start` on first cycle; delta on subsequent change
- `prev_* is null` only on `cycle_start`
- `lane_id == 0`
- binary curvature (0.0 / 1.0)
- write boundary (no non‑geometric leakage)
- deterministic replay for fixed fixtures

**Modes (progressive_lineup)**

| mode | Input | Validation |
|------|--------|------------|
| `testbench` | `dcb_testbench.yaml` (input + expected) | Exact / structural equality |
| `general` | `dcb_input.yaml` | `dcb_rules.yaml` + `dcb_rulechecker.py` only |

---

## 8. Error Handling

`dcb.py` should:

- raise `ValueError` if `current_primitive_id` missing or not in PATH_A
- raise `ValueError` if `cycle_id` or `timestamp` missing in development/test modes
- raise `ValueError` / `TypeError` if previous geometric_state exists but is malformed (missing keys or wrong types)
- not invent ordinal mappings outside PATH_A
- not silently read forbidden metadata domains

---

## 9. Relationship to Other Artifacts

| Artifact | Role |
|----------|------|
| `20.106` (v5.3+) | Normative HLRs and computation contract |
| `progressive_lineup_testing.md` | Dual‑mode testing, naming, import path, report format |
| `dcb.py` | Python realization |
| `dcb_testbench.py` / `dcb_testbench.yaml` | Deterministic cases |
| `dcb_rulechecker.py` / `dcb_rules.yaml` | Rule enforcement |
| `dcb_input.yaml` / `dcb_tests_to_run.yaml` | General fixture + test selection |
| `run.py` | Activation (`use_dcb: True`, others False) |

Downstream consumer (informative): TR reads `geometric_state` as current snapshot; replay/diagnostics use `geometric_history` + `dcb_events`.

---

## 10. Concrete Fixture Shapes (Foundation Cases)

### 10.1 First cycle (no previous geometric_state)

```yaml
id: dcb_first_cycle
input:
  _dcb_cycle_context:
    current_primitive_id: "RBU"
    cycle_id: 0
    timestamp: 1000.0
  metadata:
    context:
      topic: first
      stance: neutral
      intent: test
      continuity: new
      direction: forward
      coherence: stable
      importance: low
expected:
  geometric_state:
    position: 1          # ordinal(RBU)
    direction: 2         # DCB
    curvature: 0.0
    step_index: 0
    lane_id: 0
  history_len: 1
  event_type: cycle_start
  provenance_dcb_last_update: 1000.0
```

### 10.2 Steady sequential step (prev at RBU → current RBU again is unusual; prefer prev at RBU, current DCB)

```yaml
id: dcb_steady_from_rbu
input:
  _dcb_cycle_context:
    current_primitive_id: "DCB"
    cycle_id: 1
    timestamp: 1001.0
  metadata:
    geometric_state:
      position: 1      # RBU
      direction: 2      # expected DCB
      curvature: 0.0
      step_index: 0
      lane_id: 0
    geometric_history: []   # may be empty or pre-seeded; DCB only appends
    context:
      topic: steady
      stance: neutral
      intent: test
      continuity: same
      direction: forward
      coherence: stable
      importance: medium
expected:
  geometric_state:
    position: 2          # DCB
    direction: 3         # TR
    curvature: 0.0       # direction matches (prev.position+1)%N
    step_index: 1
    lane_id: 0
  history_len_delta: 1
  event_type: delta
  curvature: 0.0
```

### 10.3 Deviation (curvature = 1.0)

```yaml
id: dcb_deviation
input:
  _dcb_cycle_context:
    current_primitive_id: "TR"
    cycle_id: 2
    timestamp: 1002.0
  metadata:
    geometric_state:
      position: 0        # STPX — not the predecessor of TR
      direction: 1
      curvature: 0.0
      step_index: 5
      lane_id: 0
expected:
  geometric_state:
    position: 3          # TR
    direction: 4         # CTP
    curvature: 1.0       # expected_direction from prev was 1, actual direction is 4
    step_index: 6
    lane_id: 0
  event_type: delta
  curvature: 1.0
```

### 10.4 Write‑boundary / no leakage

Input includes residue / semantic / ssg fields; expected: those fields unchanged after `process()`.

### 10.5 History growth across two sequential calls (testbench may simulate by chaining)

Optional case: run DCB twice in one test with updated cycle context; assert `len(geometric_history) == 2` and increasing `step_index`.

---

## 11. Rules / Rulechecker Mapping (v1)

Suggested `dcb_rules.yaml` checks (method names on rulechecker):

| rule id | check method | Intent |
|---------|--------------|--------|
| dcb_output_001 | `deterministic_output_present` | Output TP exists |
| dcb_state_shape_001 | `geometric_state_five_scalars` | Exactly five scalar fields, types OK |
| dcb_lane_001 | `lane_id_zero` | lane_id == 0 |
| dcb_history_001 | `one_history_append` | History length increased by 1 (or == 1 on empty start) |
| dcb_events_001 | `event_policy` | cycle_start XOR delta as appropriate |
| dcb_curvature_001 | `binary_curvature` | curvature in {0.0, 1.0} |
| dcb_write_boundary_001 | `only_dcb_fields_written` | No semantic/residue/ssg/process mutation |
| dcb_provenance_001 | `provenance_dcb_last_update` | provenance.dcb_last_update set |
| dcb_progressive_001 | `progressive_lineup_compatibility` | Output present for lineup |

---

## 12. Testbench Comparison Strategy (v1)

In `testbench` mode, prefer **structural foundation comparison** (not full TP deep equality):

- `geometric_state` exact five fields
- `event_type` / presence of cycle_start vs delta
- `prev_* is None` on cycle_start
- history length delta == 1
- `provenance.dcb_last_update`
- optional: curvature value, position/direction from PATH_A ordinals

Rulechecker runs as diagnostics in testbench mode; PASS/FAIL is structural match.

In `general` mode, PASS/FAIL is rulechecker only.

Follow progressive_lineup §3.7 import path block and §3.9 report format exactly (headers, context summary, final summary).

Context summary may print geometric fields in addition to the standard context keys:

```
- position / direction / curvature / step_index / lane_id
- last event_type
- history_len
```

---

## 13. What v1 Must Prove vs Defer

**Must prove**

- five‑field geometric_state overwrite each invocation
- position / direction from `ordinal(current_primitive_id)` and `(pos+1) mod N`
- step_index 0 on first cycle; else prev+1
- lane_id always 0
- curvature binary rule (§5)
- exactly one history append per invocation
- first cycle: cycle_start only; later: delta on change
- write boundary (HLR‑20.106‑011)
- no hidden internal state
- deterministic I/O under fixed cycle context
- progressive_lineup dual‑mode compatibility

**Deferred**

- multi‑lane `lane_id` semantics
- rich / continuous curvature geometry
- external (non‑TP) history sinks
- TR reaction policy to events
- expanding PATH_A to full intake/structure prefix

---

## 14. Implementation Order (Recommended)

1. Confirm 20.106 v5.3+ locked (Option B: runner `current_primitive_id`)
2. Implement `dcb.py` pure compute + write boundary
3. Write `dcb_rules.yaml` + `dcb_rulechecker.py`
4. Write foundation fixtures in `dcb_testbench.yaml` + `dcb_tests_to_run.yaml`
5. Write `dcb_testbench.py` (both modes)
6. Write `dcb_input.yaml` for general mode
7. Activate only DCB in `run.py`
8. Green pass → treat as foundation before TR

---

**End of Document — dcb_py_struc_pgm.md (Deterministic Execution‑Flow Indexer Scaffold)**

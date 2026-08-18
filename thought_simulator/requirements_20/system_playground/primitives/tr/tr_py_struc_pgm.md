# **tr_py_struc_pgm.md — Structural Program for TR (Python Implementation Scaffold)**
### *Aligned with 20.37 (v3.0), progressive_lineup_testing.md (v4.2), and TR theory suite*
### *Informative — Implementation Guidance Only*

---

## 1. Purpose

`tr.py` implements the **Thought Router (TR‑prm)** as defined in **20.37 (v3.0)**.

TR’s structural program:

- constructs the **canonical Path‑A routing‑vector block** `TP.TR` each gated invocation
- runs **only** when `TP.tr_needs_update is True`
- clears `tr_needs_update = false` only after successful TR recompute and write
- is the **exclusive writer** of `TP.TR`
- reads only the **narrow normative read‑set** from 20.37 (diagnostic signals optional; deterministic omission when absent)
- produces deterministic stance, intent, affect, epistemic_shading, tension, politeness, commitment, reservation, logical_structure, epistemic_delta_h, lineage_additions, and routing_fields
- never mutates IdOB, DCB ownership fields, RB routing_filter, semantic residue topology, or Pipeline‑B fields
- supports deterministic replay and progressive lineup testing

This scaffold is designed so that, given:

- `progressive_lineup_testing.md` (v4.2+)
- `20.37_thought_router_tr_specification.md` (v3.0+)
- `tr_py_struc_pgm.md`
- TR theory companions (readset proposal, mapping families, geometry, invariant drift, lineage, routing_fields, adjacency, continuity‑curvature)

a capable AI can write:

- `tr.py`
- `tr_testbench.py`
- `tr_testbench.yaml`
- `tr_input.yaml`
- `tr_tests_to_run.yaml`
- `tr_rules.yaml`
- `tr_rulechecker.py`

and activate TR in `run.py`.

**Testbench category (progressive_lineup §11):** `path_a/routing/`

```
testbenches/path_a/routing/
  tr_testbench.py
  tr_testbench.yaml
  tr_input.yaml
  tr_tests_to_run.yaml
  tr_rules.yaml
  tr_rulechecker.py

primitives/tr/
  tr.py
  tr_py_struc_pgm.md
```

**Theory references (informative):**

- `ts_tr_semantic_routing_theory.md` — core mapping families + open questions
- `ts_tr_readset_update_proposal.md` — normative vs diagnostic read‑set
- `ts_tr_mapping_families.md` — field mapping families + omission defaults
- `ts_tr_semantic_geometry.md` — 5‑axis geometry, composition order, minimal‑input path
- `ts_tr_invariant_drift_theory.md` — $H_t$, $\Delta H$
- `ts_tr_lineage_extension_theory.md` — append predicate, bound $k$
- `ts_tr_routing_fields_spec.md` — complete routing_fields key set
- `ts_tr_continuity_and_curvature_interaction.md` — $C$, $K$
- `ts_tr_semantic_adjacency_theory.md` — adjacency scalar $A$

---

## 2. Inputs and Outputs

### 2.1 Normative reads (authoritative under 20.37)

TR is normatively allowed to read **only**:

| Source | Path / key | Notes |
|--------|------------|-------|
| Dirty flag | `tr_needs_update` | Gate; must be True to run |
| Meaning layer | `semantic` meaning‑layer fields | TP‑local |
| Meaning semantics | `semantic.meaning_semantics` / idob_semantics lists if present | As available |
| IdOB semantics | `semantic.idob_semantics[]` | Read‑only |
| Routing metadata | `process.routing_metadata` | Structural routing context |
| Lineage | `semantic.lineage` | Canonical lineage |
| STPX cues | STPX structural cue envelope (if present on TP) | Structural only |
| DCB (permitted) | `metadata.geometric_state` (minimal) and/or ephemeral dcb_events | Curvature / directional hint only; not ownership |

**Fixture convention for optional diagnostic enrichment (v1 isolation tests)**

```yaml
_tr_diagnostics:
  enable_diagnostics: true
  adjacency: 0            # A ∈ {-1,0,+1}; omit → treat as missing
  continuity: 0           # C ∈ {-1,0,+1}
  identity_geometry: 0    # I ∈ {-1,0,+1}
  invariant_H_t: 0
  invariant_H_t1: 0
  commitments: null
  freeze_signatures: null
  referent_lineage: []
  qualifier_lineage: []
```

`tr.py` may read `_tr_diagnostics` for isolation tests of enriched mappings. It **must not require** this block for core TR computation when only the narrow 20.37 read‑set is present. Missing diagnostics → deterministic omission defaults (see §4.5).

**Forbidden reads / uses**

- Pipeline‑B fields, truth_hypotheses, exec_plan as routing authority
- messy‑input tags
- semantic residue topology ownership fields (IdOB/RB owned)
- inventing signals from missing/noisy fields
- other TPs except through canonical lineage fields
- hidden mutable global state

### 2.2 Outputs (TR‑owned only)

Primary write target:

```python
TP["TR"] = { ... }   # full routing-vector block
TP["tr_needs_update"] = False   # only after successful recompute
```

Optional provenance:

```python
TP["metadata"]["provenance"]["tr_last_update"] = timestamp  # if available
```

Optional audit:

```python
TP["exec_trace"].append({"tr_ref": {"origin": "TR", "last_update": "TR", ...}})
```

**Must not write**

- IdOB envelope / semantic identity ownership
- DCB geometric_state / geometric_history / dcb_events ownership
- `process.routing_filter` (RB‑owned)
- semantic residue topology ownership
- STPX cue ownership
- Pipeline‑B fields, truth hypotheses

### 2.3 Canonical TP.TR shape (v1)

```python
TR = {
    "stance": "neutral",              # supportive|neutral|corrective|adversarial|exploratory
    "intent": "inform",               # inform|request|correct|clarify|commit|speculate
    "affect": "neutral",              # negative|neutral|positive  (or -1|0|+1)
    "epistemic_shading": "neutral",   # confident|neutral|uncertain|speculative
    "tension": "low",                 # low|medium|high
    "politeness": "neutral",          # direct|neutral|polite
    "commitment": "weak",             # weak|medium|strong
    "reservation": "none",            # none|mild|strong
    "logical_structure": "additive",  # conditional|causal|contrastive|additive|corrective
    "epistemic_delta_h": 0,           # int / Q32.32 proxy; v1 int OK
    "lineage_additions": [],          # bounded list, len ≤ k (provisional k=3)
    "routing_fields": {               # complete key set; all present
        "semantic_drift": False,
        "identity_drift": False,
        "commitment_instability": False,
        "freeze_conflict": False,
        "topology_instability": False,
        "curvature_level": 0,
        "stance_instability": False,
        "shading_instability": False,
        "tension_instability": False,
        "lineage_instability": False,
        "adjacency_valence": 0,
        "continuity_state": 0,
        "invariant_delta_h": 0,
        "routing_severity": 0,
    },
}
```

All maps use **canonical key order** before export. Arrays use stable ordering.

**Provisional ordinal tables (lock for progressive tests)**

| Field | Values |
|-------|--------|
| stance | supportive=0, neutral=1, corrective=2, adversarial=3, exploratory=4 |
| affect | negative=-1, neutral=0, positive=+1 |
| epistemic_shading | confident=0, neutral=1, uncertain=2, speculative=3 |
| tension | low=0, medium=1, high=2 |
| politeness | direct=0, neutral=1, polite=2 |
| commitment | weak=0, medium=1, strong=2 |
| reservation | none=0, mild=1, strong=2 |

String labels or integer codes are both acceptable in v1 **if** the testbench compares consistently; prefer **string labels** in exported `TP.TR` for inspectability unless a fixture locks integers.

---

## 3. High‑Level Program Structure

```python
PRIMITIVE_NAME = "tr"

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

class TR:
    def __init__(self, tp_input=None):
        self.tp = copy.deepcopy(tp_input or {})

    def process(self) -> dict:
        # 1. Gate: no-op when clean
        if not self._needs_update():
            return self.tp

        # 2. Extract normative (+ optional diagnostic) inputs
        inputs = self._extract_tr_inputs(self.tp)

        # 3. Geometry / mapping under composition order (minimal path if diagnostics absent)
        geometry = self._compute_geometry(inputs)          # respects geometry §9.1
        mappings = self._compute_mapping_fields(inputs, geometry)

        # 4. Lineage additions (bounded)
        lineage_additions = self._compute_lineage_additions(inputs)

        # 5. epistemic_delta_h
        delta_h = self._compute_epistemic_delta_h(inputs)

        # 6. routing_fields complete dict
        routing_fields = self._build_routing_fields(inputs, geometry, mappings, delta_h, lineage_additions)

        # 7. Assemble canonical TR block
        tr_block = self._build_tr_block(mappings, delta_h, lineage_additions, routing_fields)

        # 8. Write TR-owned paths only; clear dirty flag
        self._write_tr(tr_block)
        self._clear_dirty_flag()
        self._write_provenance_optional(inputs)
        self._append_audit_optional(tr_block)

        return self.tp

def run(tp: dict) -> dict:
    return TR(tp).process()
```

**Mandatory helper responsibilities**

| Helper | Responsibility |
|--------|----------------|
| `_needs_update` | Return True iff `tr_needs_update is True` |
| `_extract_tr_inputs` | Collect normative reads; optional `_tr_diagnostics`; normalize missing → omission defaults; **never invent** |
| `_compute_geometry` | 5‑axis state; composition order from geometry paper; minimal‑input path when diagnostics absent |
| `_compute_mapping_fields` | stance, intent, affect, shading, tension, politeness, commitment, reservation, logical_structure |
| `_compute_lineage_additions` | Bounded list; empty under omission; $k$ provisional default 3 |
| `_compute_epistemic_delta_h` | From invariant signals or 0 |
| `_build_routing_fields` | Complete key set; all keys present; deterministic |
| `_build_tr_block` | Canonical dict; stable key order |
| `_write_tr` | Write only `TP.TR` |
| `_clear_dirty_flag` | Set `tr_needs_update = False` only after successful write |
| `_write_provenance_optional` | `metadata.provenance.tr_last_update` if used |
| `_append_audit_optional` | Optional `exec_trace` tr_ref |

---

## 4. Computation Contracts (v1 Foundation)

### 4.1 Dirty‑flag gate

```python
if not bool(tp.get("tr_needs_update")):
    return tp  # no-op; do not write TR; do not clear flag
```

After successful write:

```python
tp["tr_needs_update"] = False
```

### 4.2 Composition order (geometry‑backed fields)

When diagnostic signals are present, apply projections in this order (geometry §9.1):

1. Base from meaning‑semantics
2. Adjacency
3. Continuity
4. Identity
5. Curvature
6. Clamp to ordinal ranges

When diagnostics are absent, use **minimal‑input path**:

```
stance = neutral
affect = neutral
epistemic_shading = neutral
politeness = neutral
tension = low
```

Meaning‑semantics / STPX (if present) may still seed intent and logical_structure deterministically.

### 4.3 Mapping omission defaults (global)

| Field | Default when inputs missing |
|-------|-----------------------------|
| stance | neutral |
| intent | inform |
| affect | neutral |
| epistemic_shading | neutral |
| tension | low |
| politeness | neutral |
| commitment | weak |
| reservation | none |
| logical_structure | additive |
| epistemic_delta_h | 0 |
| lineage_additions | [] |
| routing_fields | all keys present; False/0 defaults |

### 4.4 routing_fields construction

Every key in the complete set **must** appear. No extra keys. Deterministic boolean/ordinal assignment from available signals; defaults when missing.

Provisional: $\tau_s = 2$ for semantic_drift threshold when geometry drift is computed; otherwise `semantic_drift = False` under minimal path.

### 4.5 Lineage bound

```python
k = 3  # provisional; versioned free parameter
lineage_additions = lineage_additions[:k]
```

### 4.6 Canonical ordering

```python
# routing_fields keys in fixed declaration order
# lineage_additions stable order as produced
# no randomized structures
```

### 4.7 Messy / partial input

- still run the **same** TR function when gated
- do not invent adjacency, continuity, identity, $\Delta H$, or lineage elements
- produce full TR block with omission defaults

---

## 5. Primitive Boundary Discipline

| Action | Allowed |
|--------|---------|
| Read normative 20.37 read‑set | Yes |
| Read optional `_tr_diagnostics` in isolation tests | Yes |
| Read DCB geometric_state / events as permitted ephemeral hint | Yes |
| Write `TP.TR` | Yes |
| Clear `tr_needs_update` after successful write | Yes |
| Write optional provenance / audit | Yes |
| Write IdOB / semantic identity ownership | **No** |
| Write DCB geometric_* ownership | **No** |
| Write `process.routing_filter` | **No** |
| Write residue topology ownership | **No** |
| Read/write Pipeline‑B / truth hypotheses | **No** |
| Run when `tr_needs_update` is false | **No** (no‑op) |

---

## 6. Determinism, Replay, Testbench Compatibility

- Identical TP (+ diagnostics block) → identical `TP.TR`
- No randomness; stable key order
- Progressive dual‑mode: structural foundation comparison; general rulechecker

**Modes**

| mode | Input | Validation |
|------|--------|------------|
| `testbench` | `tr_testbench.yaml` | Structural foundation comparison |
| `general` | `tr_input.yaml` | `tr_rules.yaml` + rulechecker |

Follow progressive_lineup §3.7 import path, §3.8 naming, §3.9 report format, §3.11 structural comparison.

---

## 7. Error Handling

- Malformed `TR` target container types: raise clear `ValueError` in test/dev
- Missing optional diagnostics: omission defaults; still produce full TR when gated
- `tr_needs_update` false: return TP unchanged (including existing TR if any)
- Never silent semantic repair of missing meaning fields

---

## 8. Relationship to Other Artifacts

| Artifact | Role |
|----------|------|
| `20.37` v3.0+ | Normative HLRs |
| `progressive_lineup_testing.md` v4.2+ | Dual‑mode testing contract |
| TR theory suite | Mapping, geometry, drift, lineage, routing_fields |
| `ts_tr_readset_update_proposal.md` | Normative vs diagnostic discipline |
| `tr.py` | Implementation |
| Testbench suite | Foundation lock |
| `run.py` | `use_tr: True` activation |
| RB | Primary consumer of `TP.TR` (read‑only) |

---

## 9. Concrete Fixture Shapes (Foundation Cases)

### 9.1 Clean gate true — minimal inputs (omission defaults)

```yaml
id: tr_minimal_gate_true
input:
  tr_needs_update: true
  semantic:
    lineage: []
  process:
    routing_metadata:
      core_id: "core_0"
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
  tr_needs_update: false
  TR:
    stance: neutral
    intent: inform
    affect: neutral
    epistemic_shading: neutral
    tension: low
    politeness: neutral
    commitment: weak
    reservation: none
    logical_structure: additive
    epistemic_delta_h: 0
    lineage_additions: []
    routing_fields:
      semantic_drift: false
      identity_drift: false
      commitment_instability: false
      freeze_conflict: false
      topology_instability: false
      curvature_level: 0
      stance_instability: false
      shading_instability: false
      tension_instability: false
      lineage_instability: false
      adjacency_valence: 0
      continuity_state: 0
      invariant_delta_h: 0
      routing_severity: 0
  check_write_boundary: true
```

### 9.2 Gate false — no‑op

```yaml
id: tr_gate_false_noop
input:
  tr_needs_update: false
  TR:
    stance: corrective
    intent: correct
    affect: neutral
    epistemic_shading: neutral
    tension: low
    politeness: neutral
    commitment: weak
    reservation: none
    logical_structure: additive
    epistemic_delta_h: 0
    lineage_additions: []
    routing_fields: {}
  metadata:
    context:
      topic: noop
      stance: neutral
      intent: test
      continuity: same
      direction: forward
      coherence: stable
      importance: low
expected:
  tr_needs_update: false
  TR_unchanged: true
  # existing TR block must not be rewritten
```

### 9.3 STPX cues seed intent / logical_structure

```yaml
id: tr_stpx_intent
input:
  tr_needs_update: true
  semantic:
    lineage: []
  process:
    routing_metadata: {}
  # fixture may place STPX cues under a conventional path TR is allowed to read
  STPX:
    cues:
      structural: ["question"]
  metadata:
    context:
      topic: question
      stance: neutral
      intent: test
      continuity: new
      direction: forward
      coherence: stable
      importance: medium
expected:
  tr_needs_update: false
  TR:
    intent: request          # or inform if cue mapping not yet rich — lock one
    # other fields follow omission defaults unless seeded
```

### 9.4 Diagnostics present — adjacency positive

```yaml
id: tr_diag_positive_adjacency
input:
  tr_needs_update: true
  semantic:
    lineage: []
  process:
    routing_metadata: {}
  _tr_diagnostics:
    enable_diagnostics: true
    adjacency: 1
    continuity: 1
    identity_geometry: 1
  metadata:
    context:
      topic: soft
      stance: neutral
      intent: test
      continuity: same
      direction: forward
      coherence: stable
      importance: medium
expected:
  tr_needs_update: false
  TR:
    affect: positive
    politeness: polite
    routing_fields:
      adjacency_valence: 1
      continuity_state: 1
```

### 9.5 Write boundary / no leakage

Include IdOB‑like semantic identity fields, DCB geometric_state, `process.routing_filter`, residue fields on input; after process:

- those fields **unchanged**
- only `TR`, `tr_needs_update` (cleared), and optional TR provenance/audit updated

### 9.6 Dirty flag must clear

```yaml
id: tr_clears_dirty_flag
input:
  tr_needs_update: true
  semantic: {}
  process:
    routing_metadata: {}
  metadata:
    context:
      topic: clear
      stance: neutral
      intent: test
      continuity: new
      direction: forward
      coherence: stable
      importance: low
expected:
  tr_needs_update: false
  TR_present: true
```

### 9.7 Deterministic replay

Same minimal fixture twice → byte‑stable / structurally identical `TP.TR`.

### 9.8 routing_fields complete key set

Assert all 14 keys present; no extras.

### 9.9 Lineage bound

If diagnostics force many candidates, `len(lineage_additions) ≤ 3`.

### 9.10 DCB curvature hint (optional)

```yaml
id: tr_dcb_curvature_hint
input:
  tr_needs_update: true
  semantic: {}
  process:
    routing_metadata: {}
  metadata:
    geometric_state:
      position: 3
      direction: 4
      curvature: 1.0
      step_index: 2
      lane_id: 0
    context:
      topic: curve
      stance: neutral
      intent: test
      continuity: new
      direction: forward
      coherence: unstable
      importance: high
expected:
  tr_needs_update: false
  # tension may rise if implementation maps curvature→tension; else low under strict minimal path
  # lock policy: if geometric_state.curvature used as normative minimal envelope, tension medium/high
  # if treated diagnostic-only until 20.37 promotion, tension remains low
  # Document chosen policy in tr.py and fixtures consistently with readset proposal
```

**v1 recommended policy:** treat `metadata.geometric_state.curvature` as **allowed minimal normative DCB envelope** per 20.37 “permitted ephemeral DCB events / geometric hints,” mapping curvature 0→tension low, 1→tension medium or high deterministically. Document the exact map in `tr.py` and fixtures.

---

## 10. Rules / Rulechecker Mapping (v1)

| rule id | check method | Intent |
|---------|--------------|--------|
| tr_output_001 | `deterministic_output_present` | Output TP exists |
| tr_block_001 | `tr_block_present` | `TP.TR` exists after gated run |
| tr_fields_001 | `tr_required_fields_present` | All required TR keys present |
| tr_rf_001 | `routing_fields_complete` | All routing_fields keys present |
| tr_gate_001 | `dirty_flag_cleared_when_ran` | After gated success, `tr_needs_update` is false |
| tr_noop_001 | `noop_when_clean` | When flag false, TR unchanged |
| tr_boundary_001 | `idob_dcb_rb_untouched` | No IdOB/DCB ownership/RB filter writes |
| tr_omission_001 | `omission_defaults_when_minimal` | Minimal inputs → defaults |
| tr_order_001 | `canonical_field_ordering` | Stable serialization order |
| tr_lineage_001 | `lineage_bounded` | len(lineage_additions) ≤ k |
| tr_progressive_001 | `progressive_lineup_compatibility` | Output usable in lineup |

---

## 11. Testbench Comparison Strategy (v1)

**Structural foundation comparison** (not full TP deep equality):

- `tr_needs_update` expected value
- `TR` required fields exact (labels or locked ordinals)
- `routing_fields` complete key set + expected key values when specified
- `lineage_additions` exact list when specified
- write‑boundary fields unchanged when requested
- gate‑false cases: TR byte/structural unchanged

Print context summary + TR extras (`stance`, `intent`, `tension`, `epistemic_delta_h`, `routing_severity`, lineage count) per progressive_lineup §3.9.

---

## 12. What v1 Must Prove vs Defer

**Must prove**

- Dirty‑flag gate: no‑op when false; run when true
- Clear `tr_needs_update` only after successful write
- Full `TP.TR` block with all required fields
- Complete `routing_fields` key set
- Deterministic omission defaults under minimal 20.37 inputs
- Write boundary: no IdOB / DCB ownership / RB filter / residue ownership mutation
- Deterministic replay for fixed fixtures
- Lineage bound $k=3$
- Progressive dual‑mode compatibility
- Exclusive writer discipline (tests assume only TR writes `TP.TR`)

**Defer**

- Full promotion of diagnostic signals into 20.37
- Rich STPX→intent taxonomy beyond a small locked map
- Learned / non‑ordinal geometry
- Freezing severity_classifier sophistication beyond provisional table
- Cross‑primitive optimization with RB RED fields
- Q32.32 hard requirement if playground uses int/float proxies (document proxy)

---

## 13. Implementation Order (Recommended)

1. Lock read of 20.37 v3.0 + this scaffold + progressive_lineup §3.11 + readset proposal  
2. Implement `tr.py` gate + minimal‑input path + full TR block + dirty clear  
3. `tr_rules.yaml` + `tr_rulechecker.py`  
4. Foundation fixtures in `tr_testbench.yaml` + `tr_tests_to_run.yaml`  
5. `tr_testbench.py` dual mode  
6. `tr_input.yaml`  
7. Activate only TR in `run.py`  
8. Green pass → optionally enable `_tr_diagnostics` enrichment without revamping ownership  

---

## 14. Versioned Free Parameters (Provisional Defaults)

| Parameter | Provisional default | Change policy |
|-----------|---------------------|---------------|
| lineage bound $k$ | 3 | minor version + fixtures |
| $\tau_s$ | 2 | minor version + fixtures |
| omission field defaults | §4.3 table | minor version + fixtures |
| curvature→tension map | 0→low, 1→medium (or high) | document + fixtures |
| adjacency_modifier | $\{-1,0,+1\}$ | minor version |
| severity_classifier | severity 0 under minimal path | lock before golden expansion |

---

**End of Document — tr_py_struc_pgm.md (Deterministic Routing‑Vector Scaffold)**

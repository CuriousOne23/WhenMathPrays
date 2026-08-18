# **rb_py_struc_pgm.md — Structural Program for RB (Python Implementation Scaffold)**
### *Aligned with 20.50_rb_requirements.md (v3.0), progressive_lineup_testing.md (v4.2), and ts_rb_idob_foundations*
### *Informative — Implementation Guidance Only*

---

## 1. Purpose

`rb.py` implements the **Relational Basin (RB‑prm)** as defined in **20.50 (v3.0)**.

RB’s structural program:

- computes a **deterministic routing filter** each cycle
- enforces **TR gating** (`tr_needs_update` only)
- enforces **multi‑core isolation** and split/merge arbitration bounds
- treats messy inputs as read‑only contextual signals
- optionally emits first‑order **RED** fields (`adjacency_class`, `displacement_scale`, `regime_hint`, `rt_adj`, `route_proposal`)
- reads IdOB / $\mathbf{F}$ approximations and DCB geometric_state **only** as routing‑adjacent context
- never mutates IdOB, TR, or DCB‑owned geometry ownership
- supports deterministic replay and progressive lineup testing

This scaffold is designed so that, given:

- `progressive_lineup_testing.md` (v4.2+)
- `20.50_rb_requirements.md` (v3.0+)
- `rb_py_struc_pgm.md`

a capable AI can write:

- `rb.py`
- `rb_testbench.py`
- `rb_testbench.yaml`
- `rb_input.yaml`
- `rb_tests_to_run.yaml`
- `rb_rules.yaml`
- `rb_rulechecker.py`

and activate RB in `run.py`.

**Testbench category (progressive_lineup §11):** `path_a/routing/`

```
testbenches/path_a/routing/
  rb_testbench.py
  rb_testbench.yaml
  rb_input.yaml
  rb_tests_to_run.yaml
  rb_rules.yaml
  rb_rulechecker.py

primitives/rb/
  rb.py
  rb_py_struc_pgm.md
```

**Theory references (informative):**

- `ts_routing_entropy_dynamics.md` — operator $\mathcal{R}$
- `ts_invariant_relational_model.md` — $\mathbf{F}$, shared regimes
- `ts_invariant_to_idob_theory.md` — IdOB view only
- `ts_identity_geometry.md` / `ts_semantic_residue_topology.md` — layer language

---

## 2. Inputs and Outputs

### 2.1 Approved reads (v1 foundation)

| Source | Path / key | Notes |
|--------|------------|-------|
| Input fields | `input_fields` | Routing context |
| TR | `TR` | **Read‑only**; committed topology |
| TR gate | `tr_needs_update` | Boolean gate |
| Entropy | `process.deltaH` | Q32.32 or float proxy |
| Lineage | `semantic.lineage` | Routing‑adjacent |
| Routing metadata | `process.routing_metadata` | OB lists, core_id, orthogonality, bounds |
| IdOB view | semantic identity / foundation view fields | **Read‑only** |
| $\mathbf{F}$ approx | optional scalars under metadata or `_rb_foundation` | **Read‑only** |
| DCB context | `metadata.geometric_state` | Execution‑flow **only**; not $\kappa_{\text{route}}$ |
| Context | `metadata.context` | Continuity markers for logs |

**Fixture convention for optional foundation inputs**

```yaml
_rb_foundation:
  enable_red: true
  I_stab: 0.8
  R_res: 0.7
  P_cont: 0.6
  L_depth: 3
  Rt_adj: 0.2
  delta_H: 0.05
  E_dens: 0.4
  C_coh: 0.7
  prior_neighborhood: ["ob_a", "ob_b"]
```

`rb.py` may read `_rb_foundation` for v1 RED classification in isolation tests. It must not require this block for core routing‑filter computation when classic 20.50 inputs alone are present.

**Forbidden reads / uses**

- Pipeline‑B fields, truth_hypotheses, exec_plan, exec_trace (as routing authority)
- supervisory fields, semantic $\Delta H\%$
- inventing semantics from missing/noisy fields
- treating DCB `geometric_state.curvature` as $\kappa_{\text{id}}$ or $\kappa_{\text{route}}$

### 2.2 Outputs (RB‑owned only)

Primary write target:

```
process.routing_filter   # or process.routing_metadata.routing_filter — pick ONE canonical path and stick to it
```

**Recommended canonical path for v1 playground:**

```python
TP["process"]["routing_filter"] = { ... }
```

Optional provenance:

```python
TP["metadata"]["provenance"]["rb_last_update"] = timestamp  # if timestamp available
```

Optional audit:

```python
TP["exec_trace"].append({"rb_ref": {"origin": "RB", "last_update": "RB", ...}})
```

**Must not write**

- `TR`, `tr_needs_update`
- IdOB envelope / semantic identity ownership
- DCB geometric_state / geometric_history / dcb_events ownership
- semantic_core, intake, context mutation, Path‑B fields

### 2.3 Canonical routing_filter shape (v1)

```python
routing_filter = {
    "selected_ob_ids": [],          # sorted by ob_id ascending
    "lane_projections": [],         # deterministic list
    "delta_h_routing_context": 0.0, # from process.deltaH
    "firing_order": [],             # deterministic sequence of ob_ids
    "transition_rationale": [],     # stable strings, canonical order
    "policy_justification": {},     # stable key order when serialized
    "inquiry_escalation": None,     # or structured bound-respecting value
    "merge_eligibility": None,
    "split_directive": None,
    # foundation RED fields (v1 enable_red)
    "adjacency_class": None,        # "local" | "non_local"
    "rt_adj": None,
    "regime_hint": None,            # shared regime labels only
    "displacement_scale": None,     # "small" | "medium" | "large"
    "route_proposal": None,
}
```

All arrays/maps use **canonical ordering** before export.

---

## 3. High‑Level Program Structure

```python
PRIMITIVE_NAME = "rb"

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

class RB:
    def __init__(self, tp_input=None):
        self.tp = copy.deepcopy(tp_input or {})

    def process(self) -> dict:
        # 1. Extract read-only inputs
        inputs = self._extract_routing_inputs(self.tp)

        # 2. TR gating observation (does not write TR)
        route_to_tr = self._tr_gate(inputs)

        # 3. Core-local candidate OBs from routing_metadata + TR
        candidates = self._select_core_local_obs(inputs)

        # 4. Apply fanout / lane-depth / escalation bounds
        candidates = self._apply_bounds(candidates, inputs)

        # 5. Deterministic split/merge arbitration (no cross-core)
        split_merge = self._arbitrate_split_merge(candidates, inputs)

        # 6. Build firing_order and rationales
        firing_order = self._compute_firing_order(candidates, inputs)
        rationales = self._transition_rationale(candidates, inputs, route_to_tr)

        # 7. Optional RED foundation fields
        red = self._compute_red_fields(inputs)  # may be all None if disabled/missing

        # 8. Assemble canonical routing_filter
        rf = self._build_routing_filter(
            candidates, firing_order, rationales, split_merge, inputs, red, route_to_tr
        )

        # 9. Write only RB-owned paths
        self._write_routing_filter(rf)
        self._write_provenance_optional(inputs)
        self._append_audit_optional(rf)

        return self.tp

def run(tp: dict) -> dict:
    return RB(tp).process()
```

**Mandatory helper responsibilities**

| Helper | Responsibility |
|--------|----------------|
| `_extract_routing_inputs` | Collect approved read fields; normalize missing to safe defaults without invention |
| `_tr_gate` | Return bool: route consideration toward TR iff `tr_needs_update is True` |
| `_select_core_local_obs` | Filter OBs by matching `core_id` / `orthogonality_signature` |
| `_apply_bounds` | Enforce max fanout, lane depth, inquiry escalation, merge/split eligibility caps |
| `_arbitrate_split_merge` | Deterministic split/merge directives; never cross‑core |
| `_compute_firing_order` | Stable ordered list of selected_ob_ids |
| `_transition_rationale` | Inspectable strings; include TR-gate reason when relevant |
| `_compute_red_fields` | local/non_local, displacement_scale, regime_hint when enable_red |
| `_build_routing_filter` | Canonical dict; sorted arrays; stable keys |
| `_write_routing_filter` | Write only RB-owned process path |
| `_write_provenance_optional` | `metadata.provenance.rb_last_update` if used |
| `_append_audit_optional` | Optional `exec_trace` rb_ref |

---

## 4. Computation Contracts (v1 Foundation)

### 4.1 TR gating

```python
route_to_tr = bool(tr_needs_update) is True
# RB never writes TR or tr_needs_update
```

Include in `transition_rationale` something stable such as:

- `"tr_gate:true"` or `"tr_gate:false"`

### 4.2 Core isolation

```python
tp_core = routing_metadata.get("core_id")
# keep only OBs where ob.core_id == tp_core and orthogonality_signature matches policy
# never merge/split across core_id
```

### 4.3 Bounds (configurable via routing_metadata.policy or defaults)

Suggested v1 defaults (override via input policy deterministically):

| Bound | Default |
|-------|---------|
| max_ob_fanout | 8 |
| max_lane_depth | 4 |
| max_inquiry_escalation | 2 |
| merge/split eligibility | false unless metadata explicitly allows |

### 4.4 Messy input

If fields are missing/partial/noisy:

- still run the **same** routing function
- do not invent new OB ids from noise
- do not smooth/repair input fields
- selected_ob_ids may be empty if no valid core‑local OBs exist

### 4.5 RED fields (when `_rb_foundation.enable_red` or build flag true)

Use shared placeholders from foundation relational model unless policy overrides deterministically:

```python
H_small = 0.15
H_crit = 0.40
a_local = 0.30
a_nonlocal = 0.70

rt = float(Rt_adj)
dh = abs(float(delta_H))

if rt < a_local and dh < H_small:
    adjacency_class = "local"
elif rt > a_nonlocal or dh > H_crit:
    adjacency_class = "non_local"
else:
    adjacency_class = "local" if rt <= 0.5 else "non_local"  # deterministic midpoint rule

# displacement_scale
if adjacency_class == "local" and dh < H_small:
    displacement_scale = "small"
elif adjacency_class == "non_local" and dh > H_crit:
    displacement_scale = "large"
else:
    displacement_scale = "medium"

# regime_hint from shared table using I_stab, R_res, P_cont, |delta_H|, adjacency
# labels only: Stable | Refinement | Drift | Transition | Collapse
```

**Regime preference rules (20.50):**

- Stable / Refinement → prefer local unless hard topology forces otherwise
- Transition / Collapse → must not force false `local` to mask conditions

If foundation inputs missing: leave RED fields `None` deterministically (do not invent).

### 4.6 Canonical ordering

```python
selected_ob_ids = sorted(selected_ob_ids)
firing_order = list(selected_ob_ids)  # or stable secondary key
transition_rationale = sorted(transition_rationale)
```

---

## 5. Primitive Boundary Discipline

| Action | Allowed |
|--------|---------|
| Read TR, tr_needs_update, routing_metadata, deltaH, lineage | Yes |
| Read IdOB view / $\mathbf{F}$ approx / DCB geometric_state | Yes, routing‑adjacent only |
| Write `process.routing_filter` | Yes |
| Write optional `provenance.rb_last_update` / audit | Yes |
| Write TR / tr_needs_update | **No** |
| Write IdOB / semantic identity ownership | **No** |
| Write DCB geometric_* ownership | **No** |
| Cross‑core merge/split | **No** |
| Semantic interpretation / identity resolution | **No** |

---

## 6. Determinism, Replay, Testbench Compatibility

- Identical TP (+ foundation block) → identical routing_filter  
- No randomness; sort all exported lists  
- Progressive dual‑mode: testbench structural compare; general rulechecker  

**Modes**

| mode | Input | Validation |
|------|--------|------------|
| `testbench` | `rb_testbench.yaml` | Structural foundation comparison |
| `general` | `rb_input.yaml` | `rb_rules.yaml` + rulechecker |

Follow progressive_lineup §3.7 import path, §3.8 naming, §3.9 report format, §3.11 structural comparison, §3.12 foundation observability.

---

## 7. Error Handling

- Malformed `process` / non‑dict metadata: raise clear `ValueError` in test/dev  
- Missing optional foundation: RED fields null; core filter still produced  
- Empty OB candidate set: empty `selected_ob_ids` / `firing_order`, explicit rationale e.g. `"no_core_local_obs"`  
- Never silent semantic repair of messy inputs  

---

## 8. Relationship to Other Artifacts

| Artifact | Role |
|----------|------|
| `20.50` v3.0+ | Normative HLRs |
| `progressive_lineup_testing.md` v4.2+ | Dual‑mode testing contract |
| Foundation papers | $\mathcal{R}$, regimes, layer separation |
| `rb.py` | Implementation |
| Testbench suite | Foundation lock |
| `run.py` | `use_rb: True` activation |

---

## 9. Concrete Fixture Shapes (Foundation Cases)

### 9.1 Clean local route + TR gate false

```yaml
id: rb_clean_local
input:
  tr_needs_update: false
  TR: { "version": 1, "committed": true }
  process:
    deltaH: 0.05
    routing_metadata:
      core_id: "core_0"
      orthogonality_signature: "A"
      candidate_obs:
        - { ob_id: "ob_b", core_id: "core_0", orthogonality_signature: "A" }
        - { ob_id: "ob_a", core_id: "core_0", orthogonality_signature: "A" }
        - { ob_id: "ob_x", core_id: "core_1", orthogonality_signature: "B" }
  metadata:
    context: { topic: clean, stance: neutral, intent: test, continuity: same, direction: forward, coherence: stable, importance: medium }
  _rb_foundation:
    enable_red: true
    I_stab: 0.85
    R_res: 0.75
    P_cont: 0.7
    Rt_adj: 0.2
    delta_H: 0.05
expected:
  selected_ob_ids: ["ob_a", "ob_b"]   # sorted; core_1 excluded
  tr_gate_rationale_contains: "tr_gate:false"
  adjacency_class: local
  displacement_scale: small
  regime_hint: Stable
  check_write_boundary: true
```

### 9.2 TR gate true

```yaml
id: rb_tr_gate_true
input:
  tr_needs_update: true
  TR: { "version": 1, "committed": true }
  process:
    deltaH: 0.1
    routing_metadata:
      core_id: "core_0"
      orthogonality_signature: "A"
      candidate_obs:
        - { ob_id: "ob_a", core_id: "core_0", orthogonality_signature: "A" }
  metadata:
    context: { topic: gate, stance: neutral, intent: test, continuity: new, direction: forward, coherence: stable, importance: high }
expected:
  selected_ob_ids: ["ob_a"]
  tr_gate_rationale_contains: "tr_gate:true"
  # RB still must not write TR or tr_needs_update
  check_tr_unchanged: true
```

### 9.3 Core isolation (reject foreign core)

```yaml
id: rb_core_isolation
input:
  tr_needs_update: false
  process:
    deltaH: 0.0
    routing_metadata:
      core_id: "core_0"
      orthogonality_signature: "A"
      candidate_obs:
        - { ob_id: "ob_foreign", core_id: "core_9", orthogonality_signature: "Z" }
  metadata:
    context: { topic: iso, stance: neutral, intent: test, continuity: new, direction: forward, coherence: stable, importance: low }
expected:
  selected_ob_ids: []
  rationale_contains: "no_core_local_obs"  # or equivalent stable token
```

### 9.4 Non‑local RED (high ΔH)

```yaml
id: rb_nonlocal_entropy
input:
  tr_needs_update: false
  process:
    deltaH: 0.55
    routing_metadata:
      core_id: "core_0"
      orthogonality_signature: "A"
      candidate_obs:
        - { ob_id: "ob_a", core_id: "core_0", orthogonality_signature: "A" }
  _rb_foundation:
    enable_red: true
    I_stab: 0.4
    R_res: 0.4
    P_cont: 0.3
    Rt_adj: 0.8
    delta_H: 0.55
  metadata:
    context: { topic: jump, stance: neutral, intent: test, continuity: new, direction: forward, coherence: unstable, importance: high }
expected:
  selected_ob_ids: ["ob_a"]
  adjacency_class: non_local
  displacement_scale: large
  # regime_hint in {Transition, Drift, Collapse} depending on table; assert membership not false local
```

### 9.5 Write boundary / no leakage

Include `semantic.identity`, residue, DCB geometric_state, `TR`, `tr_needs_update` on input; after process:

- those fields **unchanged**
- only `process.routing_filter` (and optional rb provenance/audit) added/updated

### 9.6 Messy input determinism

Missing `candidate_obs` → empty selection, stable rationales, no throw if policy allows empty; second run identical.

### 9.7 Fanout bound

Many core‑local OBs → `selected_ob_ids` length ≤ max_ob_fanout; sorted.

---

## 10. Rules / Rulechecker Mapping (v1)

| rule id | check method | Intent |
|---------|--------------|--------|
| rb_output_001 | `deterministic_output_present` | Output TP exists |
| rb_filter_001 | `routing_filter_present` | `process.routing_filter` exists |
| rb_order_001 | `canonical_ob_ordering` | selected_ob_ids sorted |
| rb_tr_readonly_001 | `tr_fields_unchanged` | TR and tr_needs_update not mutated |
| rb_core_001 | `no_foreign_core_obs` | selected OBs match core_id |
| rb_boundary_001 | `idob_dcb_semantic_untouched` | No IdOB/DCB/semantic ownership writes |
| rb_red_001 | `red_fields_consistent` | If enable_red, adjacency in {local,non_local} or null |
| rb_gate_001 | `tr_gate_rationale_present` | Rationale reflects tr_needs_update |
| rb_progressive_001 | `progressive_lineup_compatibility` | Output usable in lineup |

---

## 11. Testbench Comparison Strategy (v1)

**Structural foundation comparison** (not full TP deep equality):

- `selected_ob_ids` exact list
- presence of `firing_order` / ordered equality if expected
- `transition_rationale` contains required tokens
- TR / tr_needs_update unchanged
- write‑boundary fields unchanged when requested
- when RED expected: `adjacency_class`, `displacement_scale`, optional `regime_hint`

Print context summary + RB extras (`adjacency_class`, `displacement_scale`, `regime_hint`, selected count) per progressive_lineup §3.9.

---

## 12. What v1 Must Prove vs Defer

**Must prove**

- Deterministic routing_filter for fixed inputs  
- Canonical ordering of OB ids  
- TR gating observation without TR writes  
- Core isolation (no foreign core OBs)  
- Bounds enforcement (fanout at minimum)  
- Messy/missing candidates → deterministic empty or reduced set  
- Write boundary: no IdOB / DCB ownership / TR mutation  
- When RED enabled: local/non_local + displacement_scale deterministic  
- Progressive dual‑mode compatibility  

**Defer**

- Rich multi‑lane geometry  
- Learned adjacency metrics  
- Full attractor discovery  
- Final TR policy beyond gating  
- Freezing provisional regime thresholds as permanent truth  
- Cross‑primitive optimization of routing density  

---

## 13. Implementation Order (Recommended)

1. Lock read of 20.50 v3.0 + this scaffold + progressive_lineup §3.11–3.12  
2. Implement `rb.py` core filter + boundaries (RED behind `enable_red`)  
3. `rb_rules.yaml` + `rb_rulechecker.py`  
4. Foundation fixtures in `rb_testbench.yaml` + `rb_tests_to_run.yaml`  
5. `rb_testbench.py` dual mode  
6. `rb_input.yaml`  
7. Activate only RB in `run.py`  
8. Green pass → extend RED/regime sophistication without revamping filter ownership  

---

**End of Document — rb_py_struc_pgm.md (Deterministic Routing / RED Foundation Scaffold)**

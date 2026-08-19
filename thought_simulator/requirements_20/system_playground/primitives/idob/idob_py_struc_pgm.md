# idob_py_struc_pgm.md — IdOB Structural Program (Python Realization)

**Document ID:** idob_py_struc_pgm  
**Version:** 0.1 (First Crystallization)  
**Status:** Draft — for CP review  
**Scope:** Path-A Identity Object Basin Primitive (IdOB-prm)  
**Location:** `thought_simulator/requirements_20/system_playground/primitives/idob/`  
**Companion code:** `idob.py` (to be realized from this program)  

**Normative parents:**  
- `20.40.050_idob_prim.md` (v3.0)  
- `progressive_lineup_testing.md` (v4.2+)  

**Behavioral contracts:**  
- `papers/idob_realization_input_output_examples.md` (10 strict examples)  
- `papers/world_to_ts_process.md`  

**Local dictionaries (this directory, for now):**  
- `idob_schema.yaml`  
- `semantic_universe_dictionary.yaml`  
- `semantic_roles_dictionary.yaml`  
- `semantic_field_definitions.yaml`  
- `semantic_gradients.yaml`  
- `semantic_objects.yaml`  
- `semantic_subfields.yaml`  

*(Dictionaries currently live under `papers/`; they are to be treated as local to `primitives/idob/` for this structural program and may be moved later. Loaders look first in the primitive directory.)*

---

## 0. Purpose of This Structural Program

This document converts the normative HLRs, the ten identity-behavior examples, the schema, and the progressive dual-mode contract into an explicit, deterministic Python realization plan for IdOB.

It resolves three previously open items:

1. **Transition function** — explicit first-order mapping from (geometry, pressure, residuals, stance, regime-adjacent signals) → next geometry / continuity / freeze / basin_surface.  
2. **Envelope ownership** — which fields IdOB may write under the foundation-export path vs the mandatory TPU payload.  
3. **Regime-conditioned inherit/reset** — first-order policy for roles, candidates, provenance, and lineage markers.

It also defines the module shape, write-boundary guards, serial-pass handling, and identity-importance computation that `idob.py` must implement.

This is a structural program, not a requirements document. HLRs remain authoritative; this program must stay inside them.

---

## 1. Python Module Shape (`idob.py`)

### 1.1 Required surface

```python
PRIMITIVE_NAME = "idob"

def process(tp: dict, mode: str = "general", **kwargs) -> dict:
    """
    Main entry. Returns updated TP (or a TPU request structure per pipeline convention).
    mode is injected by run.py / testbench ("testbench" | "general").
    """
```

### 1.2 Internal structure (recommended)

```
idob.py
├── load_schema_and_dicts()          # local YAML under primitives/idob/
├── extract_identity_view(tp)        # read-only view of identity-adjacent fields
├── determine_regime_hint(tp)        # optional F / RB / prior IdOB signals → shared regime label
├── apply_transition_rules(...)      # core deterministic operator I
├── apply_regime_inherit_reset(...)  # roles / candidates / provenance / lineage
├── compute_identity_importance(...) # deterministic, monotonic
├── build_envelope(...)              # foundation export shape
├── issue_tpu_request(...)           # HLR-024 payload only
├── write_boundary_guard(tp_before, tp_after)  # assert no RB / DCB / structural ownership
└── process(...)                     # orchestration
```

All functions must be pure with respect to identical TP snapshots (HLR-042).

### 1.3 Dictionary lookup rule

Per progressive §3.6.3 (small exclusive tables):

1. Look first in `primitives/idob/`.  
2. Fall back only if explicitly directed later.  

Do **not** hard-code paths into `papers/`.

---

## 2. Owned Fields and Write Boundaries

### 2.1 Mandatory TPU payload (HLR-024)

IdOB SHALL issue `TPU.idob_update` containing **only**:

| Field | Type / Notes |
|-------|--------------|
| `meaning_delta_h` | scalar / structured delta |
| `idob_semantics[]` | list of identity-conditioned meaning units |
| `meaning_semantics[]` | broader meaning units when produced |
| `idob_complete` | bool |
| `path_b_eligible` | bool |
| `idob_next_ob_candidates[]` | list (serial-pass support) |
| foundation envelope fields (when export enabled) | see §2.2 |

No routing updates, no structural updates, no TR updates.

### 2.2 Foundation envelope fields (IdOB-owned when export enabled)

First-order set required by this structural program:

```
identity.geometry
identity.continuity
identity.pressure
identity.residuals.{magnitude, pattern}
identity.freeze.state
identity.basin_surface.region

# optional but recommended for foundation observability
roles[]                    # from semantic_roles_dictionary
candidates[]               # provisional identity candidates
provenance.extend_or_truncate
lineage_markers[]          # identity-adjacent continuity only
stability_marker           # derived
alignment_marker           # derived
regime_label               # shared vocabulary only
```

These are written only under the foundation-export path declared by the structural program. They remain readable by RB as a view (20.50) and by subsequent IdOB passes.

### 2.3 Strict non-ownership (write-boundary guard)

IdOB MUST NOT write or mutate:

- any `process.routing_filter` or RED fields (RB-owned)
- `geometric_state`, `geometric_history`, `dcb_events` (DCB-owned)
- structural residue / structural ΔH% / SSG fields
- Path-B truth/done envelopes
- TP text surface

The guard runs after every process call in both modes. Violation → hard fail in testbench mode; diagnostic in general mode.

### 2.4 Read-only identity-adjacent inputs

Allowed (informative list from 20.40.050 §1.1):

- prior IdOB envelope
- continuity_metadata (COB / CIL / CST)
- expressive / normalization metadata (IIInB, IE)
- semantic-layer commits (SSG, STPX, RBU) as adjacent signals
- residue_metadata (SOB family) as identity-adjacent only
- optional F approximations / regime hints
- optional read-only RB routing filter / RED view
- optional read-only DCB geometric_state (execution-flow context only; never treated as κ_id)

---

## 3. Shared Regime Vocabulary and First-Order Inherit/Reset Policy

Shared labels (locked):

```
Stable | Refinement | Drift | Transition | Collapse
```

### 3.1 First-order policy (v0.1)

| Regime     | Roles / Candidates          | Provenance          | Lineage markers     | Residuals direction          | Freeze tendency          |
|------------|-----------------------------|---------------------|---------------------|------------------------------|--------------------------|
| Stable     | inherit                     | extend              | inherit             | dissipate / collapse toward small | none                  |
| Refinement | inherit + refine            | extend              | inherit             | reduce                       | none                     |
| Drift      | inherit with caution        | extend (flag drift) | inherit             | accumulate / medium          | identity_freeze possible |
| Transition | selective inherit / reset   | truncate or bridge  | bridge if needed    | large / explosion possible   | identity_freeze common   |
| Collapse   | reset                       | truncate            | reset               | clear or explosion then clear| release after reset      |

This is a **directional** policy. Exact thresholds remain provisional (Must-Prove vs Defer). Implementation must make the chosen action deterministic and observable for foundation logging.

### 3.2 Regime hint sources (priority order)

1. Explicit prior IdOB `regime_label` if present and fresh.  
2. Optional F-block components when supplied by progressive fixture or upstream.  
3. Derived from current geometry + pressure + residuals (fallback heuristic, still deterministic).  
4. Default to `Refinement` when insufficient signal (safe neutral for meaning refinement).

---

## 4. Transition Rules (Core of Operator I)

Seeded directly from the ten strict examples in `idob_realization_input_output_examples.md` and generalized into a deterministic first-order table.

Geometry vocabulary (schema):

```
formation | refinement | correction | drift | conflict | bifurcation |
stabilization | convergence | alignment | closure
```

### 4.1 Primary transition table (v0.1)

Input signals considered: current `identity.geometry`, `identity.pressure`, `identity.residuals`, `stance.category`, `routing.mode` (read-only), and regime hint.

| Current Geometry   | Dominant Signals                          | Next Geometry     | Continuity (typical) | Freeze (typical)     | Basin/Surface (typical)   | Notes |
|--------------------|-------------------------------------------|-------------------|----------------------|----------------------|---------------------------|-------|
| formation          | low pressure, small residuals, clarify/confirm | formation or refinement | continuation        | none                 | basin                     | Example 1→2 |
| refinement         | low–medium, confirm/emphasize             | refinement or stabilization | continuation     | none                 | basin                     | Example 2 |
| correction         | medium pressure, clarify/reject           | correction or drift | correction / drift  | none → identity_freeze | unstable                 | Example 3 |
| drift              | medium–high, uncertain/reject             | drift or conflict | correction / drift  | identity_freeze       | unstable                  | Example 4 |
| conflict           | high, reject/explosion                    | conflict or bifurcation | correction       | identity_freeze      | transition_surface        | Example 5 |
| bifurcation        | high, two_clusters, clarify               | bifurcation or stabilization | bifurcation   | identity_freeze      | split                     | Example 6 |
| stabilization      | medium → low, emphasize/merge             | stabilization or convergence | continuation / stabilization | none          | basin                     | Example 7 |
| convergence        | low, clarify/merge                        | convergence or alignment | continuation      | none                 | basin                     | Example 8 |
| alignment          | low, confirm                              | alignment or closure | continuation       | none                 | basin                     | (extension of examples) |
| closure            | low, resolved residuals                   | closure           | continuation        | none                 | basin                     | terminal for cluster |

### 4.2 Residual and freeze side-effects (deterministic)

- residuals.pattern `explosion` or `two_clusters` → strongly prefer conflict / bifurcation and identity_freeze.  
- residuals.pattern `collapsed` → favor stabilization / convergence and freeze=none.  
- pressure `high` + stance `reject` → escalate freeze and move basin_surface toward transition_surface or split.  
- routing.mode `merge` under stabilization/convergence → favor basin and freeze=none.  
- routing.mode `branch` under drift/conflict → favor unstable / split.

### 4.3 Implementation note

The transition function must be a pure lookup + small deterministic adjustments. No stochastic choice. When multiple rows could apply, priority is:

1. Explicit high-pressure / explosion signals  
2. Current geometry continuity (prefer staying in family unless forced)  
3. Regime hint (Collapse forces reset path)

All decisions must be logged when foundation observability is enabled.

---

## 5. Identity-Importance (HLR-032 … 036)

- Deterministic function of identity metadata + semantic-adjacent cues only.  
- Monotonic and reproducible for identical TP snapshots.  
- Produces identity-importance cues that reduce meaning entropy for downstream TR / Path-B eligibility.  
- Never modifies TP text or structural fields.  
- Exposed as a read-only view to RB and subsequent IdOB passes.

First-order realization: map importance.level (schema) and residual magnitude / pressure into a small ordered set of cues; no learned weights in v0.1.

---

## 6. Serial Passes and Completion

- `idob_complete = true` when current geometry is in {stabilization, convergence, alignment, closure} **and** residuals are small/collapsed **and** freeze is none (or explicitly released).  
- Otherwise `idob_complete = false` and `idob_next_ob_candidates[]` may list further IdOB or related OB-family work.  
- Multiple serial IdOB passes are legal (HLR-004). Each pass consumes the prior envelope as identity-adjacent input.

`path_b_eligible` follows HLR-021/022: true only when meaning refinement is sufficient for TR / Path-B checks; IdOB never initiates Path-B.

---

## 7. Dual-Mode Testbench Alignment

Follow progressive_lineup_testing.md exactly:

| mode        | Input file                  | Validation                          |
|-------------|-----------------------------|-------------------------------------|
| testbench   | idob_testbench.yaml         | exact or structural foundation comparison |
| general     | idob_input.yaml             | rulechecker only                    |

Category placement: `testbenches/path_a/identity/`.

Structural foundation comparison (allowed): envelope shape + regime-conditioned inherit/reset markers + the TPU fields listed in §2.1.

Write-boundary assertions are mandatory in both modes (hard fail in testbench).

---

## 8. Foundation Observability Hooks

When enabled, log (or attach diagnostic block):

- chosen regime_label  
- inherit vs reset decision per category (roles, provenance, lineage)  
- geometry transition taken  
- κ_id-related markers (never confuse with κ_exec or κ_route)  
- F-component approximations if supplied  

These support the progressive foundation observation questions without affecting PASS/FAIL in testbench mode.

---

## 9. Must-Prove for v0.1 Implementation

- Deterministic outputs for fixed inputs (HLR-042).  
- Correct TPU payload only (HLR-024).  
- No RB / DCB / structural ownership writes.  
- Transition table reproduces the ten examples exactly.  
- Regime inherit/reset follows the directional policy in §3.1.  
- Dual-mode contracts and progressive discovery paths work.  
- Identity-importance is deterministic and monotonic.

Defer (per 20.40.050 §10): final role taxonomies, continuous geometry beyond markers, learned parameters, permanent regime thresholds.

---

## 10. Research Questions / Open Items for CP Review

These questions are intentionally left open so that CP (architectural lead) and the realization can converge without hidden assumptions.

1. **Transition table completeness**  
   Does the first-order table in §4.1 adequately cover the ten examples and the expected serial-pass cases, or should additional rows (especially alignment → closure and Collapse-driven resets) be made more explicit before coding?

2. **Envelope field list**  
   Is the §2.2 set the right minimal foundation export, or should `roles[]` / `candidates[]` / `lineage_markers[]` be deferred until a later increment?

3. **Regime derivation fallback**  
   When no explicit F-block or prior regime_label is present, is “default to Refinement” the preferred safe neutral, or should the heuristic be stronger (e.g., derive directly from geometry + pressure)?

4. **Identity-importance shape**  
   Should the first realization emit only the schema `importance.level`, or a richer ordered cue list that TR can consume directly?

5. **Serial-pass candidate generation**  
   What is the minimal useful content of `idob_next_ob_candidates[]` in v0.1 (empty list vs explicit “IdOB again” vs downstream OB names)?

6. **Dictionary location stability**  
   Confirm that keeping the dictionary YAMLs under `primitives/idob/` (local exclusive tables) is acceptable for the near term; any preferred naming or versioning convention?

7. **Structural foundation comparison details**  
   For testbench mode, which exact subset of the envelope must be compared when full deep equality is too brittle (geometry + freeze + basin_surface + regime_label + idob_complete)?

8. **Collapse behavior**  
   Under Collapse, should all identity-owned fields hard-reset, or is a soft residual “scar” marker allowed for continuity diagnostics?

---

## 11. Implementation Order Recommendation

1. Load local schema + dictionaries.  
2. Implement write-boundary guard and pure extract view.  
3. Implement transition table so the ten examples pass exactly.  
4. Add regime inherit/reset and completion flags.  
5. Add identity-importance and TPU issuance.  
6. Wire dual-mode testbench and foundation comparison.  
7. Expand test cases toward the 40–60 range once the rules are stable.

---

**End of idob_py_struc_pgm.md (v0.1)**  
Ready for CP review. Realization of `idob.py` should not begin until the research questions above have been resolved or explicitly deferred.

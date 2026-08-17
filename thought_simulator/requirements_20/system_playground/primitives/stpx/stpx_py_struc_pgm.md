# **stpx_py_struc_pgm.md — Structural Program for STPX (Python Implementation Scaffold)**  
### *Aligned with 20.49_stpx_prim.md and progressive_lineup_testing.md*  
### *Informative — Implementation Guidance Only*

---

## 1. Purpose

`stpx.py` implements the **Structured Token & Pattern Extractor (STPX‑prm)** as defined in **20.49 (v4.0)**.

STPX’s structural program:

- consumes structural geometry, SSG outputs, canonical tokens, and structural‑adjacent metadata  
- computes a bounded set of **cue families**  
- assembles a deterministic **cue_envelope**  
- writes its cues into `TP.metadata.semantic_layer_metadata.stpx_cues`  
- writes provenance into `TP.metadata.semantic_layer_metadata.semantic_layer_provenance`  
- obeys primitive boundary discipline (read‑only TP except its own envelope)  
- supports deterministic replay and progressive lineup testing  

This scaffold is designed so that, given:

- `progressive_lineup_testing.md`  
- `20.49_stpx_prim.md`  
- `stpx_py_struc_pgm.md`  

one can write:

- `stpx.py`  
- `stpx_testbench.py`  
- `stpx_testbench.yaml`  
- `stpx_input.yaml`  
- `stpx_tests_to_run.yaml`  
- `stpx_rules.yaml`  
- `stpx_rulechecker.py`.

---

## 2. Inputs and Outputs

### 2.1 Inputs (read‑only)

STPX consumes **only structural‑adjacent inputs**, consistent with 20.49 and 20.105.xxx.

**Structural geometry and residues**

- `TP.metadata.structural_metadata.*`  
  - structural roles  
  - segment boundaries  
  - constraint surfaces  
  - smoothing actions  
- `TP.metadata.residue_metadata.*`  
  - structural_residue  
  - refinement_residue  
  - constraint_residue  
  - semantic_adjacent_residue  
  - presemantic_hash  
  - residue_provenance  

**SSG outputs**

- `tp.ssg_signature`  
- `tp.ssg_layer_bitmap`  
- `tp.ssg_reason_code`  
- `tp.ssg_status`  

These are treated as structural‑adjacent features, not semantic geometry.

**Canonical tokens and expressive metadata**

- `TP.metadata.normalization_metadata.*` (normalized tokens, alignment maps)  
- `TP.metadata.expressive_metadata.*` (elongation, abbreviation, omission, stylization)  

**Continuity / entropy / provenance**

- `TP.metadata.continuity_metadata.*` (identity anchors, referent lineage, clarifying topology)  
- `TP.metadata.entropy_metadata.*` (entropy trace, ΔH history)  
- `TP.metadata.provenance_metadata.*` (commit_id, primitive_origin, timestamps)  
- `TP.lineage_log[]`  

**Forbidden inputs**

STPX does not read:

- `TP.semantic.*` (semantic envelope)  
- `TP.metadata.context.*` (context_metadata)  
- `TP.metadata.routing_metadata.*`  
- `TP.metadata.identity_metadata.*`  
- `TP.cex.ccr.*` (CCR output)  
- truth/done fields  
- any Pipeline‑B envelopes.

---

### 2.2 Outputs (STPX‑owned fields only)

`stpx.py` writes **only**:

- `TP.metadata.semantic_layer_metadata.stpx_cues`  
- `TP.metadata.semantic_layer_metadata.semantic_layer_provenance`  

No other TP fields are modified.

**Cue envelope shape**

The cue_envelope is a deterministic structure:

```python
stpx_cues = {
    "lexical": [...],      # L
    "structural": [...],   # S (includes discourse-context cues)
    "constraint": [...],   # C
    "repair": [...],       # R
}
```

Each family is bounded and replay‑safe.

**Provenance**

`semantic_layer_provenance` records:

```python
semantic_layer_provenance = {
    "origin": "STPX",
    "last_update": "STPX",
    "commit_id": ...,
    "commit_sequence": [...],
}
```

---

## 3. High‑Level Program Structure (ISc‑Aligned)

`stpx.py` follows the **class + `process()`** pattern used by the gold‑standard ISc implementation so the progressive testbench can instantiate and call it uniformly.

```python
PRIMITIVE_NAME = "stpx"   # lowercase — must match directory and progressive naming

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

class STPX:
    def __init__(self, tp_input=None):
        # deep-copy input TP so upstream is not mutated by reference accidents
        self.tp = copy.deepcopy(tp_input or {})

    def process(self) -> dict:
        # 1. Extract structural inputs
        geom = self._extract_structural_geometry(self.tp)
        ssg = self._extract_ssg_outputs(self.tp)
        tokens = self._extract_tokens(self.tp)
        meta = self._extract_struct_adjacent_metadata(self.tp)

        # 2. If required inputs missing, write minimal envelope and provenance
        if geom is None or tokens is None:
            cues = self._empty_cues()
            self._write_cues(cues)
            self._write_provenance(empty=True)
            self._append_audit(empty=True)
            return self.tp

        # 3. Compute cue families
        lexical = self._compute_lexical_cues(tokens, meta)
        structural = self._compute_structural_cues(geom, ssg, meta)
        constraint = self._compute_constraint_cues(geom, meta)
        repair = self._compute_repair_markers(geom, tokens, meta)

        # 4. Assemble deterministic cue_envelope
        cues = self._assemble_cue_envelope(lexical, structural, constraint, repair)

        # 5. Write outputs and audit
        self._write_cues(cues)
        self._write_provenance(empty=False)
        self._append_audit(empty=False)
        return self.tp

def run(tp: dict) -> dict:
    """Functional alias matching older scaffold language."""
    return STPX(tp).process()
```

**Mandatory helpers (names may vary; responsibilities may not)**

| Helper | Responsibility |
|--------|----------------|
| `_extract_structural_geometry(tp)` | Read structural_metadata / residue_metadata; return normalized geometry object or `None` |
| `_extract_ssg_outputs(tp)` | Read SSG fields; return a small struct with signature, bitmap, reason, status |
| `_extract_tokens(tp)` | Read normalized tokens and expressive metadata; return canonical token list or `None` |
| `_extract_struct_adjacent_metadata(tp)` | Read continuity, entropy, provenance, lineage; return a metadata bundle |
| `_compute_lexical_cues(tokens, meta)` | Compute lexical surface cues from canonical tokens and expressive hints |
| `_compute_structural_cues(geom, ssg, meta)` | Compute structural cues from geometry, SSG invariants, and continuity metadata |
| `_compute_constraint_cues(geom, meta)` | Compute constraint cues from constraint surfaces and residues |
| `_compute_repair_markers(geom, tokens, meta)` | Compute repair‑region markers from repair metadata and structural anomalies |
| `_assemble_cue_envelope(L, S, C, R)` | Assemble deterministic cue_envelope dict |
| `_empty_cues()` | Return a zero/empty cue_envelope with all families present but empty |
| `_write_cues(cues)` | Write `stpx_cues` into `TP.metadata.semantic_layer_metadata` only |
| `_write_provenance(empty: bool)` | Write semantic_layer_provenance with origin, last_update, commit lineage |
| `_append_audit(empty: bool)` | Append a deterministic `stpx_ref` record to `exec_trace` or equivalent audit log |

This structure is deterministic, testbench‑friendly, and C++‑parity‑friendly.

---

## 4. Cue Family Computation

STPX computes four cue families, aligned with 20.49:

### 4.1 Lexical Surface Cues (L)

Lexical cues are derived from canonical tokens and expressive metadata:

- token categories (e.g., contrastive markers, temporal adverbs, discourse markers)  
- stylization patterns (elongation, abbreviation, omission)  
- surface repair hints (e.g., corrected vs original segments)

A typical representation:

```python
lexical = [
    {"type": "contrast_marker", "token": "but"},
    {"type": "temporal_marker", "token": "then"},
]
```

### 4.2 Structural Cues (S)

Structural cues are derived from:

- structural roles and segment boundaries  
- SSG signature and layer bitmap (e.g., high cycle density, motif presence)  
- continuity metadata (recent‑entity continuity, temporal shifts)  

Examples:

- `{"type": "temporal_shift", "segment": "s2"}`  
- `{"type": "contrastive_structure", "segments": ["s1", "s2"]}`  
- `{"type": "cycle_density_high", "layer": 3}`  

Discourse‑context structural cues (recent‑entity continuity, contrastive markers, causal markers) are included in this family.

### 4.3 Constraint Cues (C)

Constraint cues are derived from:

- constraint surfaces  
- constraint residues  
- structural roles indicating causal or referential constraints  

Examples:

- `{"type": "causal_link", "from": "event_a", "to": "event_b"}`  
- `{"type": "referential_stability", "entity": "x"}`  

### 4.4 Repair‑Region Markers (R)

Repair markers highlight regions affected by intake/normalization repairs:

- spans where IIInB/IE applied corrections  
- segments with high repair confidence or alignment anomalies  

Examples:

- `{"type": "repair_span", "start": 10, "end": 15}`  
- `{"type": "alignment_anomaly", "segment": "s3"}`  

---

## 5. Cue Envelope Assembly

The cue_envelope is assembled as:

```python
def _assemble_cue_envelope(L, S, C, R):
    return {
        "lexical": sorted(L, key=_lexical_sort_key),
        "structural": sorted(S, key=_structural_sort_key),
        "constraint": sorted(C, key=_constraint_sort_key),
        "repair": sorted(R, key=_repair_sort_key),
    }
```

Stable sorting is used to ensure deterministic ordering.  
Empty families are represented as empty lists, not omitted.

---

## 6. Primitive Boundary Discipline

`stpx.py` enforces:

- read‑only access to all upstream TP fields  
- write‑only access to `TP.metadata.semantic_layer_metadata.stpx_cues` and `TP.metadata.semantic_layer_metadata.semantic_layer_provenance`  
- no semantic‑layer writes outside its own envelope  
- no routing‑layer writes  
- no identity‑layer writes  
- no truth/done writes  
- no Pipeline‑B interaction  

This keeps STPX purely structural‑adjacent and preserves downstream responsibilities (TR, RB, IdOB, MCB, OuBA).

---

## 7. Determinism, Replay, and Testbench Compatibility

`stpx.py` is expected to:

- produce identical outputs for identical inputs  
- avoid randomness and non‑deterministic ordering  
- use stable sorting for canonicalization  
- use pure functions for cue computation  
- record provenance deterministically  

The STPX testbench will verify:

- correct cue_envelope shape and families  
- correct use of SSG outputs  
- correct metadata boundaries (no forbidden reads/writes)  
- deterministic replay across runs  
- correct audit/provenance behavior  

---

## 8. Error Handling

`stpx.py` should:

- raise clear exceptions (`ValueError`, `KeyError`) for malformed TP structures in development/test modes  
- fall back to an empty cue_envelope when critical structural inputs are missing, while still writing provenance and audit  
- avoid silent repair of structural errors; upstream components are responsible for structural correctness  

---

## 9. Relationship to Other Artifacts

This scaffold is the implementation guide for:

- `20.49_stpx_prim.md` (normative STPX primitive)  
- `progressive_lineup_testing.md` (testbench discipline)  
- `stpx.py` (Python implementation)  
- `stpx_testbench.py` / `stpx_testbench.yaml` (deterministic tests)  
- `stpx_rulechecker.py` / `stpx_rules.yaml` (rule enforcement)  
- `stpx_input.yaml` / `stpx_tests_to_run.yaml` (fixtures and test selection)

It ensures that all STPX artifacts can be written deterministically and consistently, without semantic‑layer leakage.

---

## 10. Concrete Fixture Shape (Provisional)

A minimal TP fixture for STPX tests might include:

```yaml
metadata:
  structural_metadata:
    structural_roles: [...]
    segment_boundaries: [...]
    constraint_surfaces: [...]
  residue_metadata:
    structural_residue: {...}
    refinement_residue: {...}
    constraint_residue: {...}
    semantic_adjacent_residue: {...}
    presemantic_hash: "..."
    residue_provenance: {...}
  normalization_metadata:
    normalized_tokens: ["but", "then", "however"]
    token_alignment_map: {...}
  expressive_metadata:
    elongation_patterns: []
    abbreviation_patterns: []
    omission_patterns: []
    stylization_flags: []
  continuity_metadata:
    identity_anchors: [...]
    referent_lineage: [...]
    continuity_flags: [...]
  entropy_metadata:
    delta_h: 0.0
    entropy_trace: []
  provenance_metadata:
    commit_id: "c123"
    primitive_origin: "IE"
    commit_timestamp: "..."
ssg_signature: [0.0, 0.1, ...]   # length d
ssg_layer_bitmap: 15
ssg_reason_code: "FULL"
ssg_status: "OK"
```

Expected `stpx_cues` for such a fixture would include:

- lexical markers for contrast/temporal tokens  
- structural cues for segment transitions  
- constraint cues for any explicit constraint surfaces  
- repair markers if repair metadata indicates modified spans.

---

## 11. What v1 Must Prove vs Defer

**Must prove:**

- correct four‑family cue_envelope shape  
- correct use of SSG outputs and structural metadata  
- no upstream TP mutation outside STPX‑owned fields  
- deterministic ordering and replay behavior  
- correct provenance and audit entries  
- compatibility with progressive lineup testing harness.

**Deferred:**

- final cue taxonomy and naming conventions  
- empirical tuning of cue thresholds for TR/RB/IdOB  
- cross‑primitive optimization of cue density.

---

**End of Document — stpx_py_struc_pgm.md (Deterministic Structural‑Only Scaffold)**

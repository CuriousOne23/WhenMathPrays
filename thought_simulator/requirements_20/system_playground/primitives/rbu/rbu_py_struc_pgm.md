# **rbu_py_struc_pgm.md — Structural Program for RBU (Python Implementation Scaffold)**  
### *Aligned with 20.51_rbu_prim.md and progressive_lineup_testing.md*  
### *Informative — Implementation Guidance Only*

---

## 1. Purpose

`rbu.py` implements the **Register / Belief / Usage Commit (RBU‑prm)** as defined in **20.51 (v4.0)**.

RBU’s structural program:

- consumes IdOB‑refined meaning fields and meaning‑adjacent metadata  
- commits identity‑conditioned meaning fields into the TP semantic envelope  
- writes lineage markers and provenance for meaning‑side commits  
- obeys primitive boundary discipline (no structural or Path‑B writes)  
- supports deterministic replay and progressive lineup testing  

This scaffold is designed so that, given:

- `progressive_lineup_testing.md`  
- `20.51_rbu_prim.md`  
- `rbu_py_struc_pgm.md`  

a capable AI can write:

- `rbu.py`  
- `rbu_testbench.py`  
- `rbu_testbench.yaml`  
- `rbu_input.yaml`  
- `rbu_tests_to_run.yaml`  
- `rbu_rules.yaml`  
- `rbu_rulechecker.py`.

---

## 2. Inputs and Outputs

### 2.1 Inputs (read‑only except RBU‑owned fields)

RBU consumes **meaning‑adjacent inputs** consistent with 20.51 and 20.105.xxx.

**IdOB‑refined meaning and identity**

- `TP.semantic.identity` (IdOB provisional identity payload)  
- `TP.semantic.stance` (IdOB stance)  
- `TP.semantic.register`  
- `TP.semantic.tone`  
- `TP.semantic.tags`  
- `TP.metadata.lineage_markers` (provisional lineage markers from IdOB / prior cycles)  
- `TP.metadata.identity_metadata.*` (identity continuity flags, profiles)  

**Semantic‑layer and continuity metadata**

- `TP.metadata.semantic_layer_metadata.*` (IdOB, MCB, STPX cues if relevant)  
- `TP.metadata.continuity_metadata.*` (COB, CIL, CST continuity signals)  
- `TP.metadata.expressive_metadata.*` (register/tone hints from intake)  
- `TP.metadata.normalization_metadata.*` (normalized tokens, alignment maps)  

**Provenance and entropy**

- `TP.metadata.provenance.*` (prior commit lineage)  
- `TP.lineage_log[]`  
- `TP.metadata.entropy_metadata.*` (entropy and signature histories)  

**Forbidden inputs**

RBU does not read:

- `TP.semantic.tptb` (truth‑to‑belief)  
- `TP.semantic.tpsf` (truth/safety fields)  
- Pipeline‑B envelopes  
- truth/done fields  
- semantic ΔH%  
- supervisory fields  
- structural geometry fields (SOB/SROB/CnOB/SmOB/SSG outputs) except as read‑only context if present.

---

### 2.2 Outputs (RBU‑owned fields only)

`rbu.py` writes **only**:

- `TP.semantic.identity`  
- `TP.semantic.stance`  
- `TP.semantic.register`  
- `TP.semantic.tone`  
- `TP.semantic.tags`  
- `TP.metadata.lineage_markers`  
- `TP.metadata.provenance` (RBU provenance entries only)

No structural geometry, routing, context, or Path‑B fields are modified.

**Meaning‑side commit shape**

```python
rbu_commit = {
    "identity": TP.semantic.identity,
    "stance": TP.semantic.stance,
    "register": TP.semantic.register,
    "tone": TP.semantic.tone,
    "tags": TP.semantic.tags,
    "lineage_markers": TP.metadata.lineage_markers,
}
```

**Provenance**

RBU provenance records:

```python
rbu_provenance = {
    "origin": "RBU",
    "last_update": "RBU",
    "commit_id": ...,
    "commit_sequence": [...],  # including TPU, IdOB, RBU steps
}
```

---

## 3. High‑Level Program Structure (ISc‑Aligned)

`rbu.py` follows the **class + `process()`** pattern used by ISc and STPX so the progressive testbench can instantiate and call it uniformly.

```python
PRIMITIVE_NAME = "rbu"   # lowercase — must match directory and progressive naming

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

class RBU:
    def __init__(self, tp_input=None):
        # deep-copy input TP so upstream is not mutated by reference accidents
        self.tp = copy.deepcopy(tp_input or {})

    def process(self) -> dict:
        # 1. Extract IdOB-refined meaning and metadata
        meaning = self._extract_meaning_fields(self.tp)
        meta = self._extract_meaning_adjacent_metadata(self.tp)

        # 2. If required inputs missing, perform minimal, replay-safe commit
        if not self._has_required_inputs(meaning):
            self._commit_minimal_meaning(meaning, meta)
            self._write_provenance(empty=True)
            self._append_audit(empty=True)
            return self.tp

        # 3. Compute committed identity, stance, register, tone, tags, lineage
        identity = self._commit_identity(meaning, meta)
        stance = self._commit_stance(meaning, meta)
        register = self._commit_register(meaning, meta)
        tone = self._commit_tone(meaning, meta)
        tags = self._commit_tags(meaning, meta)
        lineage_markers = self._commit_lineage_markers(meaning, meta)

        # 4. Write meaning-side commit fields
        self._write_meaning_commit(
            identity, stance, register, tone, tags, lineage_markers
        )

        # 5. Write provenance and audit
        self._write_provenance(empty=False)
        self._append_audit(empty=False)
        return self.tp

def run(tp: dict) -> dict:
    """Functional alias matching older scaffold language."""
    return RBU(tp).process()
```

**Mandatory helpers (names may vary; responsibilities may not)**

| Helper | Responsibility |
|--------|----------------|
| `_extract_meaning_fields(tp)` | Read IdOB‑refined semantic fields and provisional lineage markers; return a normalized meaning bundle |
| `_extract_meaning_adjacent_metadata(tp)` | Read semantic_layer_metadata, continuity, expressive, normalization, provenance, lineage; return a metadata bundle |
| `_has_required_inputs(meaning)` | Check presence of minimal IdOB‑refined fields needed for a valid commit |
| `_commit_identity(meaning, meta)` | Compute committed identity (subculture, persona, role) from IdOB payload and continuity metadata |
| `_commit_stance(meaning, meta)` | Compute committed stance from IdOB payload and expressive/continuity hints |
| `_commit_register(meaning, meta)` | Compute committed register from IdOB payload and expressive metadata |
| `_commit_tone(meaning, meta)` | Compute committed tone from IdOB payload and expressive metadata |
| `_commit_tags(meaning, meta)` | Consolidate semantic tags into `TP.semantic.tags` deterministically |
| `_commit_lineage_markers(meaning, meta)` | Consolidate lineage markers into `TP.metadata.lineage_markers` deterministically |
| `_commit_minimal_meaning(meaning, meta)` | Write a minimal, replay‑safe commit when inputs are incomplete, preserving invariants |
| `_write_meaning_commit(identity, stance, register, tone, tags, lineage)` | Write meaning‑side commit fields into canonical TP paths only |
| `_write_provenance(empty: bool)` | Write RBU provenance under `TP.metadata.provenance` with origin, last_update, commit lineage |
| `_append_audit(empty: bool)` | Append a deterministic `rbu_ref` record to `exec_trace` or equivalent audit log |

This structure is deterministic, testbench‑friendly, and consistent with STPX and ISc scaffolds.

---

## 4. Meaning‑Side Commit Computation

RBU computes six meaning‑side components, aligned with 20.51.

### 4.1 Identity Commit

Identity is derived from:

- IdOB identity payload (subculture, persona, role)  
- identity continuity flags  
- referent lineage  

Representation example:

```python
identity = {
    "persona": "assistant",
    "subculture": "technical",
    "role": "explainer",
    "continuity_flags": [...],
}
```

### 4.2 Stance Commit

Stance is derived from:

- IdOB stance payload  
- continuity_metadata (direction, coherence)  
- expressive_metadata (hedging, certainty markers)

Example:

```python
stance = {
    "polarity": "neutral",
    "certainty": "high",
    "direction": "explanatory",
}
```

### 4.3 Register Commit

Register is derived from:

- IdOB register payload  
- expressive_metadata (formality, slang, abbreviation patterns)

Example:

```python
register = {
    "formality": "formal",
    "domain": "technical",
}
```

### 4.4 Tone Commit

Tone is derived from:

- IdOB tone payload  
- expressive_metadata (elongation, emphasis, emotive markers)

Example:

```python
tone = {
    "affect": "calm",
    "intensity": "moderate",
}
```

### 4.5 Semantic Tags Commit

Tags are consolidated from:

- IdOB semantic tags  
- STPX cue_envelope (if used as tag hints)  
- continuity_metadata (topic continuity)

Example:

```python
tags = [
    "path_a",
    "routing",
    "identity_conditioned",
]
```

### 4.6 Lineage Markers Commit

Lineage markers are consolidated from:

- `TP.metadata.lineage_markers` (prior cycles)  
- `TP.lineage_log[]`  
- IdOB referent lineage

Example:

```python
lineage_markers = {
    "conversation_id": "...",
    "turn_id": "...",
    "identity_cycle": 3,
}
```

---

## 5. Primitive Boundary Discipline

`rbu.py` enforces:

- read‑only access to all upstream TP fields except its own commit targets  
- write‑only access to:  
  - `TP.semantic.identity`  
  - `TP.semantic.stance`  
  - `TP.semantic.register`  
  - `TP.semantic.tone`  
  - `TP.semantic.tags`  
  - `TP.metadata.lineage_markers`  
  - `TP.metadata.provenance` (RBU entries)  
- no structural geometry writes  
- no routing_metadata writes  
- no context_metadata writes  
- no identity resolution (IdOB owns that)  
- no TPTB/TPSF writes (Path‑B owns those)  
- no Pipeline‑B interaction  

This keeps RBU purely **meaning‑side commit** and preserves downstream responsibilities (DCB, TR, CTP, ISc, RTU, RB, IdOB, MCB, OuBA).

---

## 6. Determinism, Replay, and Testbench Compatibility

`rbu.py` is expected to:

- produce identical outputs for identical inputs  
- avoid randomness and non‑deterministic ordering  
- use stable canonicalization for tags and lineage markers  
- use pure functions for commit computation  
- record provenance deterministically  

The RBU testbench will verify:

- correct meaning‑side commit shape  
- correct use of IdOB outputs and meaning‑adjacent metadata  
- correct metadata boundaries (no forbidden reads/writes)  
- deterministic replay across runs  
- correct audit/provenance behavior  

---

## 7. Error Handling

`rbu.py` should:

- raise clear exceptions (`ValueError`, `KeyError`) for malformed TP structures in development/test modes  
- fall back to a minimal, replay‑safe commit when critical meaning inputs are missing, while still writing provenance and audit  
- avoid silent semantic inference or identity resolution; IdOB is responsible for those upstream  

---

## 8. Relationship to Other Artifacts

This scaffold is the implementation guide for:

- `20.51_rbu_prim.md` (normative RBU primitive)  
- `progressive_lineup_testing.md` (testbench discipline)  
- `rbu.py` (Python implementation)  
- `rbu_testbench.py` / `rbu_testbench.yaml` (deterministic tests)  
- `rbu_rulechecker.py` / `rbu_rules.yaml` (rule enforcement)  
- `rbu_input.yaml` / `rbu_tests_to_run.yaml` (fixtures and test selection)

It ensures all RBU artifacts can be written deterministically and consistently, without structural or Path‑B leakage.

---

## 9. Concrete Fixture Shape (Provisional)

A minimal TP fixture for RBU tests might include:

```yaml
semantic:
  identity:
    persona: "assistant"
    subculture: "technical"
    role: "explainer"
  stance:
    polarity: "neutral"
    certainty: "high"
    direction: "explanatory"
  register:
    formality: "formal"
    domain: "technical"
  tone:
    affect: "calm"
    intensity: "moderate"
  tags:
    - "path_a"
    - "routing"
metadata:
  lineage_markers:
    conversation_id: "conv_001"
    turn_id: "t_005"
    identity_cycle: 2
  semantic_layer_metadata:
    idob_origin: "IdOB"
    idob_cycle: 2
  continuity_metadata:
    continuity_flags: [...]
  expressive_metadata:
    formality_hint: "formal"
    affect_hint: "calm"
  provenance:
    commit_id: "c123"
    primitive_origin: "IdOB"
    commit_timestamp: "..."
lineage_log:
  - { primitive: "IdOB", cycle: 1 }
  - { primitive: "IdOB", cycle: 2 }
```

Expected RBU behavior:

- confirm and commit identity, stance, register, tone, tags  
- consolidate lineage_markers  
- write RBU provenance entries  
- leave all structural and Path‑B fields untouched.

---

## 10. What v1 Must Prove vs Defer

**Must prove:**

- correct meaning‑side commit shape  
- correct use of IdOB outputs and meaning‑adjacent metadata  
- no upstream TP mutation outside RBU‑owned fields  
- deterministic ordering and replay behavior  
- correct provenance and audit entries  
- compatibility with progressive lineup testing harness.

**Deferred:**

- final stance/register/tone taxonomies  
- empirical tuning of commit thresholds for downstream routing  
- cross‑primitive optimization of meaning density.

---

**End of Document — rbu_py_struc_pgm.md (Deterministic Meaning‑Side Commit Scaffold)**

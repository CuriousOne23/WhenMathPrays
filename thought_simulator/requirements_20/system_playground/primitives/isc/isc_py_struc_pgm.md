# ⭐ **`isc_py_struc_pgm.md` (Version 2.0)**
### *Python & C++ Implementation Blueprint for the ISc Primitive*

**Developer reading set (authoritative, complete for ISc code + YAML work):**
1. `progressive_lineup_testing.md` (v4.0) — dual-mode testing, file layout, import path, output format
2. `20.45_ts_isc_scoring.md` (v2.0) — normative HLRs (scoring, FFTM, COP, forbidden actions)
3. **This document** — concrete schemas, file list, rule order, skeleton, and playground write paths

No other documents are required to create or modify ISc Python or YAML artifacts.

**Aligned with:** 20.45, 20.108 / 20.108.010 (CE candidate_set authority), progressive_lineup_testing.md

| Authority | Source |
|-----------|--------|
| Candidate-set authority | `TP.ce.candidate_set[]` emitted by CE (20.108.010) |
| Numeric-feature authority | `TP.wrdnm[]` (when present) |
| Scoring authority | FFTM equation + weights in ISc-owned config (20.45) |
| Testing authority | progressive_lineup_testing.md dual mode |

---

# **1. ISc’s Role**

ISc is the **sole scoring primitive** for a finite interpretation candidate set.

```
… → CE (emits TP.ce.candidate_set[]) → … → WrdNm (optional numeric vectors) → ISc → …
```

**CE is the sole emitter of the candidate set.**  
IE / CEx contribute upstream features that CE uses during construction; they do **not** emit candidates for ISc.

ISc is responsible for:

- loading **ISc-owned** scoring configuration (weights, FFTM tables, COP thresholds)
- reading **`TP.ce.candidate_set[]`** (required)
- reading **`TP.wrdnm[]`** numeric feature vectors when present (optional reinforcement)
- reading CE context / next-context fields as **read-only structural cues**
- **Job 1:** deterministic scoring of each candidate (FFTM + structural + semantic-adjacent cues)
- **Job 2:** normalized distribution, entropy, ΔH%, confidence, rationale codes
- **Job 3:** COP escalation when thresholds are met
- writing scoring results into the in-memory TP under the ISc write envelope (playground)
- writing `metadata.scoring_metadata` (rationale, conflict, provenance)

ISc does **not**: generate meaning, expand candidates, modify CE/CCR/semantic-importance/CIL, tokenize free text, or perform semantic inference.

### Normative HLRs (20.45) — implementer checklist

| HLR | Constraint |
|-----|------------|
| 002 | Operate only on finite CE-derived candidate_set |
| 003 | No meaning generation; no candidate expansion |
| 004 | Deterministic scoring |
| 005 | Interpretable features; log in rationale |
| 006 | Normalized distribution |
| 007 | Entropy, ΔH%, confidence, rationale |
| 008 | COP when thresholds met |
| 009–022 | Architectural commit via Merge→TPU; playground writes `isc` / `isc_output` / scoring_metadata only |
| 030–037 | Forbidden actions |
| 058–065 | FFTM four-field scoring |

---

# **2. File Map (What a Developer Creates / Edits)**

### **2.1 Primitive implementation**

```
primitives/isc/
  isc.py                 # executable module (required)
  isc_py_struc_pgm.md    # this blueprint
  isc_scoring.yaml       # optional: weights, FFTM tables, COP thresholds (ISc-owned)
```

`PRIMITIVE_NAME = "isc"` and `get_primitive_name()` are required (progressive_lineup 3.8).

### **2.2 Testbench suite (category: routing)**

```
testbenches/path_a/routing/
  isc_testbench.py         # dual-mode runner
  isc_testbench.yaml       # mode=testbench: input + expected
  isc_tests_to_run.yaml    # enabled test list
  isc_input.yaml           # mode=general: input only
  isc_rules.yaml           # rule ids + check names
  isc_rulechecker.py       # implements each check
```

Directory schema, import-path init, dual mode, and output format are defined exclusively by **progressive_lineup_testing.md**. Do not invent alternate layouts.

### **2.3 Definition reference (optional read)**

```
primitives/definitions/path_a/isc.yaml
```

Useful for envelope naming; **20.45 + this file override** if any conflict on playground behavior.

---

# **3. Public API**

```python
PRIMITIVE_NAME = "isc"

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

class ISc:
    def __init__(self, tp_input: dict):
        ...

    def process(self) -> dict:
        """Score TP.ce.candidate_set[]; write isc outputs; return tp."""
        ...
```

Playground convention matches other primitives: mutate the in-memory TP dict and return it. Architectural Merge→TPU (20.45 HLR-009/020) remains the runtime commit path outside the unit testbench.

### **ISc-written fields (playground)**

| Path (relative to TP root — never prefix `TP.`) | Content |
|------------------------------------------------|---------|
| `isc_output` (list, append-only) | Full scoring records |
| `isc` (object, optional mirror) | Latest score_set / conflict / reason helpers for routing consumers |
| `metadata.scoring_metadata` | Rationale, COP, provenance, feature logs |

---

# **4. Intake Model and Coupling Discipline**

### **4.1 Required inputs**

| Field path | Source | Role |
|------------|--------|------|
| `ce.candidate_set[]` | CE (20.108.010) | Finite candidates to score |
| `metadata.context` (flattened CE envelope) | CE | Read-only continuity / next-context cues |

### **4.2 Optional inputs**

| Field path | Source | Role |
|------------|--------|------|
| `wrdnm[]` | WrdNm | Numeric structural feature vectors |
| prior `isc_output` / scoring_metadata | prior ISc | ΔH% baseline (read-only) |

### **4.3 Candidate object shape (from CE — do not invent fields)**

Each element of `ce.candidate_set[]` SHALL contain at minimum:

```yaml
candidate_id: int
fftm_fields:
  token_surface: string
  token_base: string
  token_expression: string
  token_intent: string
structural_features:
  surface_id: float
  lemma_id: float
  expression_id: float
  ordering_id: float
  constraint_family_id: float
  next_context_id: float
  # additional WrdNm-aligned ids may be present; score if present, ignore if absent
semantic_adjacent_features:
  semantic_residue: string
  structural_residue: string
next_context:
  topic: ...
  stance: ...
  intent: ...
  direction: ...
  coherence: ...
  importance: ...
provenance:
  origin: CE
  last_update: CE
  note: string
```

**Missing required candidate keys or empty `candidate_set` = TP defect.**  
ISc SHALL NOT repair, expand, or invent candidates. Emit a deterministic error/fallback record per 20.45 error HLRs; do not halt TS.

### **4.4 Normative coupling rules**

1. ISc **SHALL NOT** load upstream primitive YAMLs (`ce_*.yaml`, `sob_*.yaml`, etc.).
2. ISc **SHALL** depend solely on: TP fields above + **ISc-owned** scoring config.
3. Missing candidate fields → **TP defect**, not ISc inference.
4. ISc **SHALL NOT** generate meaning, stance, truth, or referent identity.
5. Upstream TP fields are **read-only**.
6. ISc **SHALL NOT** expand candidate sets.
7. ISc **SHALL NOT** modify `semantic_core`, CE envelope, CCR, semantic-importance, or CIL.
8. Nested field paths are **relative to TP root** (no `TP.` prefix) — progressive_lineup 3.6.6.

**Debug order:** `ce.candidate_set` + `wrdnm` → scoring config → ISc scoring.

---

# **5. Deterministic Rule Ordering**

Ordering SHALL be identical in Python and C++.

1. Read `ce.candidate_set[]` from TP (required; defect if missing/empty/schema-invalid)
2. Read optional `wrdnm[]` vectors
3. Read CE context / next_context cues (read-only)
4. Load ISc scoring configuration YAML (weights, tables, COP thresholds)
5. Load FFTM weight table
6. Load COP thresholds
7. **Job 1:** score each candidate in **canonical order** (CE order; stable by candidate_id, ordering_id, token_surface)
   - FFTM components from `fftm_fields`
   - structural cues from `structural_features` (+ wrdnm match if available)
   - semantic-adjacent cues from `semantic_adjacent_features`
   - next_context structural cues
8. Normalize distribution (sum → 1.0; all-zero → uniform)
9. Compute entropy H and ΔH% vs prior (if available; else ΔH% = 0)
10. COP escalation check
11. Build rationale record (all features that affected ranking)
12. Append new `isc_output` entry; update `metadata.scoring_metadata`; optional `isc` mirror
13. Return TP

---

# **6. Normative Schemas**

## **6.1 FFTM scoring equation (20.45 HLR-063)**

```
score(c) = w_s * f_s(c) + w_b * f_b(c) + w_e * f_e(c) + w_i * f_i(c)
```

Where:
- `f_s` ← token_surface (bounded lookup / identity match, deterministic)
- `f_b` ← token_base
- `f_e` ← token_expression  (meaning-layer; weight ≥ surface unless config says otherwise)
- `f_i` ← token_intent      (meaning-layer; weight ≥ surface unless config says otherwise)

Weights live only in ISc-owned config. No Path-A test overfitting (HLR-064).

Structural / semantic-adjacent / next_context terms MAY be added as **bounded additive** terms with their own weights in the same config, without changing the FFTM four-field core.

## **6.2 Per-candidate score entry**

```yaml
isc_score_entry:
  candidate_id: int
  raw_score: float
  normalized_score: float
  reason_codes: [string]
  fftm_components:
    f_s: float
    f_b: float
    f_e: float
    f_i: float
  structural_cues: {}
  semantic_adjacent_cues: {}
```

## **6.3 `isc_output` record (append-only list element)**

```yaml
isc_output_record:
  distribution:
    - candidate_id: int
      normalized_score: float
      rationale: string
  entropy: float
  delta_h_percent: float
  confidence: float
  cop_triggered: bool
  score_set:            # convenience aggregate for consumers
    - candidate_id: int
      score: float
  score_conflict: float
  score_reason_code: string
  provenance:
    origin: ISc
    last_update: ISc
    timestamp: string   # deterministic placeholder allowed in playground
```

## **6.4 `metadata.scoring_metadata`**

```yaml
scoring_metadata:
  score_set: []
  score_conflict: float
  score_reason_code: string
  cop_triggered: bool
  entropy: float
  delta_h_percent: float
  rationale_record:
    fftm_components: {}
    structural_cues: {}
    semantic_adjacent_cues: {}
    scoring_decisions: []
    cop_flags: []
  provenance:
    origin: ISc
    last_update: ISc
```

## **6.5 Entropy and ΔH%**

```
H = - Σ p_i * log(p_i)     # use a fixed base (e.g. natural or 2); document in config
ΔH% = 0 if no prior H
ΔH% = (H_current - H_previous) / H_previous * 100   otherwise
```

## **6.6 COP**

```
cop_triggered = (ambiguity > threshold_amb) OR
                (collapse > threshold_col) OR
                (drift > threshold_drift)
```

Ambiguity / collapse / drift are **deterministic functions** of the distribution (e.g. entropy vs max, top-2 gap, ΔH%). Thresholds only in ISc config.

## **6.7 Normalization**

- Sum raw scores; divide each by sum.
- If all raw scores == 0 → uniform distribution over candidates.
- Preserve candidate order from input set after scoring (do not reorder by score unless a downstream consumer does).

---

# **7. Forbidden Behavior**

ISc must not:

- generate meaning or expand candidate sets
- modify upstream TP fields (CE, CCR, semantic-importance, CIL, wrdnm, etc.)
- modify semantic_core or FFTM source fields
- scan TP text or tokenize free-form strings
- perform semantic smoothing or generative fill
- load non-ISc primitive YAMLs
- require other primitives to read diagnostic-only fields for correctness
- use nondeterministic methods (time, RNG, hash seed variance)

---

# **8. Implementation Skeleton (Python)**

```python
PRIMITIVE_NAME = "isc"

def get_primitive_name() -> str:
    return PRIMITIVE_NAME

class ISc:
    def __init__(self, tp_input):
        self.tp = tp_input

    def process(self):
        candidates = self._load_candidates(self.tp)       # ce.candidate_set
        wrdnm_vectors = self._load_wrdnm_vectors(self.tp) # optional
        scoring_cfg = self._load_scoring_config()
        fftm_tables = self._load_fftm_tables(scoring_cfg)
        cop_cfg = self._load_cop_thresholds(scoring_cfg)

        raw_scores = self._score_candidates(
            candidates, wrdnm_vectors, scoring_cfg, fftm_tables
        )
        distribution = self._normalize(raw_scores)
        entropy, delta_h = self._compute_entropy(distribution)
        cop_flag = self._check_cop(distribution, entropy, delta_h, cop_cfg)

        record = self._assemble_record(
            distribution, entropy, delta_h, cop_flag, raw_scores
        )
        metadata = self._build_scoring_metadata(
            raw_scores, distribution, entropy, delta_h, cop_flag
        )

        self.tp.setdefault("isc_output", [])
        self.tp["isc_output"].append(record)

        self.tp.setdefault("metadata", {})
        self.tp["metadata"]["scoring_metadata"] = metadata

        # Optional mirror for routing consumers
        self.tp["isc"] = {
            "score_set": record.get("score_set"),
            "score_conflict": record.get("score_conflict"),
            "score_reason_code": record.get("score_reason_code"),
            "cop_triggered": cop_flag,
        }

        return self.tp

    def _load_candidates(self, tp):
        cs = (tp.get("ce") or {}).get("candidate_set")
        if not isinstance(cs, list) or len(cs) < 1:
            # TP defect path: deterministic empty/error handling — no expansion
            return []
        return cs
```

Implement `_score_candidates` strictly from candidate `fftm_fields` + config tables; use structural/semantic-adjacent/next_context only as bounded deterministic additives.

---

# **9. Scoring Config (ISc-owned YAML)**

Suggested `primitives/isc/isc_scoring.yaml` shape:

```yaml
version: "1.0"
fftm_weights:
  w_s: 0.15
  w_b: 0.20
  w_e: 0.30
  w_i: 0.35
structural_weight: 0.0    # raise only with architecture justification
semantic_adjacent_weight: 0.0
next_context_weight: 0.0
cop:
  threshold_amb: 0.85     # e.g. high entropy fraction of log(N)
  threshold_col: 0.95     # e.g. top mass
  threshold_drift: 25.0   # |ΔH%|
entropy_log_base: 2
```

v1 may hard-code equivalent constants inside `isc.py` if YAML is not yet present; when both exist, YAML wins.

---

# **10. Downstream Consumption**

| Consumer | Consumes | Purpose |
|----------|----------|---------|
| TPU | distribution / score_set | commit boundary |
| RB / TR | entropy, ΔH%, conflict, reason codes | routing / escalation |
| IdOB | scoring metadata | identity-conditioned rails |
| CIL / CST | entropy trajectory | stability (read-only history) |

ISc is the **sole** candidate-ranking scorer.

---

# **11. Locked Policies (I1–I9)**

| ID | Topic | Lock |
|----|--------|------|
| **I1** | Scoring config | ISc-owned config authoritative |
| **I2** | FFTM tables | bounded, deterministic |
| **I3** | COP thresholds | deterministic |
| **I4** | Ordering | CE candidate order preserved |
| **I5** | Write discipline | append-only `isc_output`; scoring_metadata overwrite of ISc block only |
| **I6** | No inference | no semantic or generative behavior |
| **I7** | No upstream YAMLs | TP-only coupling |
| **I8** | Replay | identical inputs → identical outputs |
| **I9** | No candidate expansion | `ce.candidate_set` is authoritative |

---

# **12. Testbench Contract (implements progressive_lineup)**

### **12.1 Modes**

| mode | Input | Validation |
|------|-------|------------|
| `testbench` | `isc_testbench.yaml` (`input` + `expected`) | exact equality on ISc write fields |
| `general` | `isc_input.yaml` | `isc_rules.yaml` + `isc_rulechecker.py` only |

Rulechecker is **diagnostic only** in testbench mode (does not decide PASS/FAIL).

### **12.2 Required testbench YAML shape (testbench mode)**

```yaml
tests:
  - id: isc_test_001
    description: "..."
    input:
      # minimal TP including ce.candidate_set[] (and optional wrdnm[])
      ce:
        candidate_set: [...]
      metadata:
        context: {...}
      wrdnm: []   # optional
    expected:
      isc_output: [...]
      metadata:
        scoring_metadata: {...}
      # optional: isc: {...}
```

Compare at least: latest `isc_output` record distribution, entropy, cop_triggered, and scoring_metadata conflict/reason fields. Ignore non-ISc envelopes unless explicitly asserted.

### **12.3 Minimum scenarios**

1. Clean FFTM scoring (single dominant candidate)
2. Zero-score fallback → uniform distribution
3. Multi-candidate set from CE (ordering preserved)
4. COP threshold crossing
5. Deterministic entropy / ΔH% with prior present and absent
6. Replay determinism (identical inputs → identical outputs)
7. TP defect: missing/empty candidate_set (deterministic fallback, no expansion)
8. Forbidden-field integrity: CE / CCR / semantic-importance unchanged

### **12.4 Suggested rules (`isc_rules.yaml`)**

- `isc_replay_001` — output present
- `isc_candidate_source_001` — scored only `ce.candidate_set`
- `isc_distribution_001` — normalized scores sum ≈ 1.0
- `isc_distribution_002` — zero-score → uniform
- `isc_entropy_001` — entropy present and finite
- `isc_cop_001` — COP flag boolean and threshold-consistent
- `isc_no_expansion_001` — candidate count out == count in
- `isc_forbidden_001` — CE / CCR / semantic-importance unchanged
- `isc_write_envelope_001` — only isc_output / isc / scoring_metadata written by ISc
- `isc_ordering_001` — distribution candidate_id order matches input order

### **12.5 `isc_testbench.py` obligations**

- Mandatory import-path init (progressive_lineup 3.7)
- `set_testbench_config` / `run_testbench`
- Dual mode
- Assert `get_primitive_name() == "isc"`
- Mandatory output format (headers, sources, PASS/FAIL, context summary, final summary)
- Context summary may include `candidate_set_count` and top normalized score

---

# **13. Downstream / Upstream Handoff Notes (for fixtures)**

When building `isc_testbench.yaml` or `isc_input.yaml` fixtures:

- Prefer **CE-shaped** `ce.candidate_set[]` objects (section 4.3) so fixtures match real CE output.
- Classic CE context may be flattened under `metadata.context` (topic, stance, intent, …).
- `wrdnm[]` may be omitted in early tests; scoring must still run on FFTM fields alone.
- Do not embed IE/CEx-only candidate formats as the primary contract.

---

# **14. Versioning**

| Version | Change |
|---------|--------|
| 1.0 | Initial FFTM / entropy / COP skeleton |
| **2.0** | CE `TP.ce.candidate_set[]` as sole candidate authority; progressive_lineup file map; developer three-document reading set; reconciled write envelope; explicit defect path |

---

# ⭐ **End of Document — `isc_py_struc_pgm.md` (Version 2.0)**

---

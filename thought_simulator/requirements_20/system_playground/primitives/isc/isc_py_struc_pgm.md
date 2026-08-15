# ⭐ **`isc_py_struc_pgm.md` (Version 1.0)**  
### *Python & C++ Implementation Blueprint for the ISc Primitive*  
### *Aligned with 20.45_ts_isc_scoring.md, wrdnm_py_struc_pgm.md, 20.15, 20.105, 20.108*

**Numeric‑feature authority:** `TP.wrdnm[]`  
**Scoring authority:** FFTM scoring rules (20.45)  
**Coupling authority:** TP candidate‑set contract (20.45, 20.105)

---

# **1. ISc’s Role in the Pipeline**

```
… → WrdNm → ISc → TPU → RB → (refinement loop) → OuBA → TPSnS
```

ISc is responsible for:

- loading **ISc‑owned** YAML scoring configuration (weights, FFTM tables, COP thresholds)  
- reading **numeric feature vectors** from `TP.wrdnm[]`  
- reading **candidate sets** from CE/IE/CEx (20.45)  
- **Job 1:** deterministic scoring of each candidate  
- **Job 2:** producing normalized distribution, entropy, ΔH%, rationale codes  
- **Job 3:** COP escalation when thresholds are met  
- writing `TP.isc_output{}` (append‑only)  
- writing `TP.metadata.scoring_metadata`  

ISc does **not**: generate meaning, expand candidates, modify TP fields, perform semantic interpretation, or mutate CE/CCR/semantic‑importance/CIL metadata.

---

# **2. Public API**

```python
isc = ISc(tp_input)
isc.process()
```

### **ISc‑written fields**

- `TP.isc_output{}` (normalized distribution, entropy, ΔH%, rationale)  
- `TP.metadata.scoring_metadata` (score_set, conflict flags, reason codes, provenance)

---

# **3. Intake Model and Coupling Discipline**

ISc consumes:

- **numeric feature vectors** from WrdNm (`TP.wrdnm[]`)  
- **candidate sets** from CE/IE/CEx (20.45)  
- **structural + semantic‑adjacent metadata** (20.105.030 usage rules)  
- **continuity + identity metadata** (read‑only)  
- **entropy history** (read‑only)

### **3.1 Normative coupling rules**

1. ISc **SHALL NOT** load upstream primitive YAMLs (`sob_*.yaml`, `cex_*.yaml`, etc.).  
2. ISc **SHALL** depend solely on:
   - numeric features from WrdNm  
   - candidate sets from CE/IE/CEx  
   - scoring configuration YAML  
3. Missing candidate fields → **TP defect**, not ISc inference.  
4. ISc **SHALL NOT** generate meaning, stance, truth, or referent identity.  
5. ISc **SHALL** treat all upstream TP fields as read‑only.  
6. ISc **SHALL NOT** expand candidate sets.  
7. ISc **SHALL NOT** modify semantic_core or meaning‑layer fields.

**Debug order:** TP(candidate set + wrdnm vectors) → scoring config → ISc scoring.

---

# **4. Deterministic Rule Ordering**

1. Read candidate set from TP  
2. Read numeric feature vectors from `TP.wrdnm[]`  
3. Load scoring configuration YAML  
4. Load FFTM tables  
5. Load COP thresholds  
6. **Job 1:** score each candidate  
   - FFTM scoring  
   - weighted sum  
   - structural + semantic‑adjacent cues  
7. Normalize distribution  
8. Compute entropy + ΔH%  
9. COP escalation check  
10. Build rationale record  
11. Append new `TP.isc_output{}` entry  
12. Write scoring metadata  
13. Emit TP

Ordering SHALL be identical in Python and C++.

---

# **5. Normative v1 Schemas**

## **5.1 Candidate scoring entry**

```
isc_score_entry:
  candidate_id: int
  raw_score: float
  normalized_score: float
  entropy: float
  delta_h_percent: float
  reason_codes: []
  cop_escalation: bool
  provenance:
    origin: ISc
    last_update: ISc
    timestamp: iso8601
```

## **5.2 `TP.isc_output{}` (append‑only)**

Each ISc record SHALL contain:

```
isc_output:
  distribution[]:
    - candidate_id: int
      normalized_score: float32
      rationale: string
  entropy: float32
  delta_h_percent: float32
  cop_triggered: bool
  provenance:
    origin: ISc
    last_update: ISc
    timestamp: iso8601
```

## **5.3 FFTM scoring**

```
score(c) = w_s * f_s(c) +
           w_b * f_b(c) +
           w_e * f_e(c) +
           w_i * f_i(c)
```

## **5.4 COP escalation**

```
cop_triggered = (ambiguity > threshold_amb) OR
                (collapse > threshold_col) OR
                (drift > threshold_drift)
```

## **5.5 Rationale record**

```
isc_rationale_record:
  fftm_components: {}
  structural_cues: {}
  semantic_adjacent_cues: {}
  scoring_decisions: []
  cop_flags: []
  provenance_lineage:
    origin: ISc
    last_update: ISc
  timestamp: iso8601
```

---

# **6. v1 Scoring Behaviors**

### **6.1 FFTM scoring**

- deterministic weighted sum  
- bounded weights  
- no inference  
- no semantic generation  

### **6.2 Normalization**

- sum of raw scores → 1.0  
- fallback uniform distribution if all scores = 0  

### **6.3 Entropy**

```
H = - Σ p_i log(p_i)
```

### **6.4 ΔH%**

```
ΔH% = (H_current - H_previous) / H_previous * 100
```

### **6.5 COP escalation**

- deterministic thresholds  
- no inference  
- no candidate expansion  

### **6.6 Canonical ordering**

All candidates SHALL be ordered exactly as defined in CE/IE candidate set.

---

# **7. Forbidden Behavior**

ISc must not:

- generate meaning  
- expand candidate sets  
- modify upstream TP fields  
- modify semantic_core  
- modify CE envelope  
- modify CCR output  
- modify semantic‑importance  
- modify CIL metadata  
- scan TP text or tokenize free‑form strings  
- perform semantic smoothing  
- perform generative fill  
- require other primitives to read diagnostic metadata  

---

# **8. Implementation Skeleton (Python)**

```python
class ISc:
    def __init__(self, tp_input):
        self.tp = tp_input

    def process(self):
        candidates = self._load_candidates(self.tp)
        wrdnm_vectors = self._load_wrdnm_vectors(self.tp)
        scoring_cfg = self._load_scoring_config()
        fftm_tables = self._load_fftm_tables()
        cop_cfg = self._load_cop_thresholds()

        raw_scores = self._score_candidates(candidates, wrdnm_vectors, scoring_cfg, fftm_tables)
        distribution = self._normalize(raw_scores)
        entropy, delta_h = self._compute_entropy(distribution)
        cop_flag = self._check_cop(distribution, cop_cfg)

        record = self._assemble_record(distribution, entropy, delta_h, cop_flag)
        metadata = self._build_scoring_metadata(raw_scores, cop_flag)

        self.tp.setdefault("isc_output", [])
        self.tp["isc_output"].append(record)

        self.tp.setdefault("metadata", {})
        self.tp["metadata"]["scoring_metadata"] = metadata

        return self.tp
```

---

# **9. Downstream Consumption**

| Primitive | Consumes | Purpose |
|-----------|----------|---------|
| **TPU** | normalized distribution | commit boundary scoring |
| **RB** | entropy + ΔH% | routing escalation |
| **TR** | scoring metadata | truth‑relation mapping |
| **IdOB** | scoring metadata | identity‑conditioned rails |
| **CIL / CST** | entropy trajectory | stability evaluation |

ISc is the **sole scoring primitive** for candidate ranking.

---

# **10. Locked Policies (I1–I9)**

| ID | Topic | Lock |
|----|--------|------|
| **I1** | Scoring config | `isc_scoring.yaml` authoritative |
| **I2** | FFTM tables | bounded, deterministic |
| **I3** | COP thresholds | deterministic |
| **I4** | Ordering | canonical candidate order |
| **I5** | Write discipline | append‑only `TP.isc_output{}` |
| **I6** | No inference | no semantic or generative behavior |
| **I7** | No upstream YAMLs | TP‑only coupling |
| **I8** | Replay | identical inputs → identical outputs |
| **I9** | No candidate expansion | CE/IE candidate set is authoritative |

---

# **11. Testbench Contract**

- Inputs:  
  - candidate set (CE/IE/CEx)  
  - numeric feature vectors (`TP.wrdnm[]`)  
  - scoring config YAML  
- Expected:  
  - normalized distribution  
  - entropy + ΔH%  
  - rationale codes  
  - COP escalation flags  

### Minimum scenarios:

1. clean FFTM scoring  
2. zero‑score fallback → uniform distribution  
3. COP threshold crossing  
4. deterministic entropy trajectory  
5. deterministic ordering  
6. replay determinism (identical inputs → identical outputs)

---

# ⭐ **End of Document — `isc_py_struc_pgm.md` (Version 1.0)**

---

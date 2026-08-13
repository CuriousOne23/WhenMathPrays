# ⭐ **`cnob_py_struc_pgm.md` (Version 1.1)**
### *Python & C++ Implementation Blueprint for the CnOB Primitive*
### *Aligned with 20.40.030 v2.0, cnob_software_architecture.md, cnob_srob_comm_architect.md v1.1*

**Schema authority:** This document owns the **normative v1** field schemas for `cnob_constraint_map` and `cnob_residue` (Q6). Testbench expected blocks SHALL match.  
**Coupling authority:** SROB↔CnOB is a **TP surface contract**, not dictionary sync — full matrix in `cnob_srob_comm_architect.md` §2.4 (Q9).

---

# **1. CnOB’s Role in the Pipeline**

1. TPU → SOB → **SROB** → **CnOB** → SmOB → … → routing / IdOB

CnOB is responsible for:

- loading **CnOB-owned** support YAMLs only
- reading **SROB-owned TP fields** (not `srob_*.yaml`)
- encoding **C1–C7** constraint families
- emitting missing-slot, underspecification, conflict signals
- refining structural-importance → constraint-importance
- forming **`cnob_constraint_map`** (full — Q1)
- producing **`cnob_residue{}`**
- producing **`cnob_audit_record{}`**
- hashing constraint outputs for exact addressing / replay
- preserving upstream fields (read-only)
- referencing **SROB segment ids** (Q2)

CnOB does **not**: re-normalize structure; re-lex text; invent tag types; enforce constraints; resolve meaning/referents; modify semantic_core / routing envelopes / identity; **require hierarchical key sync with `srob_*.yaml`**.

---

# **2. Public API**

```python
cnob = CnOB(tp_input)
cnob.process()
```

### **CnOB-written fields**

- `TP.structural.cnob_constraint_map`
- `TP.structural.cnob_residue`
- `TP.metadata.cnob_audit_record`
- optional diagnostic-only keys

---

# **3. Intake Model and Coupling (Q9)**

SROB fields required for normal operation:

- `structural.srob_structural_map`
- `structural.srob_residue` (preferred)

Fallback: if SROB absent and isolation mode, may read SOB fields — **not** default Path-A.

All non-CnOB fields are **read-only**.

### **3.1 Normative coupling rules (support-critical)**

1. CnOB **SHALL NOT** load `srob_*.yaml` or `sob_*.yaml`.
2. CnOB **SHALL NOT** require hierarchical dictionary synchronization with SROB support files (unlike SOB↔SROB parent/child maps).
3. CnOB **SHALL** depend only on the **SROB TP surface contract**: field names and tag-space conventions written on the TP (segments, operators, lexical_*, modality, discourse_flags, structural_importance, residue cues).
4. Every rule condition that depends on SROB **SHALL** use an **explicit predicate** whose meaning is mappable to those fields (evident in YAML `if:` blocks).
5. Missing expected **fields** on the TP **SHALL** be treated as a **handoff/support defect** (SROB gap or rename), not as a reason to invent tags or re-lex inside CnOB.
6. Absence of a particular SROB **fine-id child** is **not** a CnOB desync by itself when rules only require “operator present” / parent-space match.

**Debug order:** inspect TP(SROB) → match rule `if:` → then CnOB encode logic.

---

# **4. Deterministic Rule Ordering**

1. Read TP (post-SROB)
2. Load CnOB YAMLs only
3. Read `srob_structural_map` / `srob_residue`
4. Encode C1–C7 (`cnob_constraint_rules.yaml`)
5. Apply missing-slot / underspec rules
6. Apply conflict rules
7. Apply constraint-importance rules (multi-label OK)
8. Canonical-order all lists (family, rule_id, segment_id)
9. Build **full** `cnob_constraint_map`
10. Build `cnob_residue`
11. Compute hashes
12. Build `cnob_audit_record`
13. Emit TP

---

# **5. Normative v1 Schemas**

## **5.1 Constraint entry**

```
constraint_entry:
  family: C1 | C2 | C3 | C4 | C5 | C6 | C7
  rule_id: string
  segment_ids: []
  payload: {}
```

## **5.2 `TP.structural.cnob_constraint_map` (full every run — Q1)**

```
cnob_constraint_map:
  constraint_families:
    C1: []
    C2: []
    C3: []
    C4: []
    C5: []
    C6: []
    C7: []
  missing_slot_signals: []
  underspecification_markers: []
  conflict_indicators: []
  constraint_importance: []
  discourse_constraints: []
  lineage_constraints: []
  routing_constraints: []
  policy_constraints: []
```

Empty lists are valid (Q4). Keys C1–C7 **must** be present.

## **5.3 Signal object**

```
signal:
  id: string
  kind: missing_slot | underspecification | conflict
  rule_id: string
  segment_ids: []
  participants: []
  note: string
```

## **5.4 Constraint-importance object**

```
constraint_importance_item:
  labels: []
  segment_ids: []
  source: structural | gap | conflict | mixed
```

## **5.5 `TP.structural.cnob_residue`**

```
cnob_residue:
  missing_slot_signals: []
  underspecification_markers: []
  conflict_indicators: []
  constraint_importance: []
  constraint_family_summary: []
  disagreement_flags: []
  override_flags: []
  constraint_residue_hash: string
```

Residue **must** include gap/conflict/importance arrays and **`constraint_residue_hash`**.

## **5.6 Hash (Q7)**

Canonical serialization of map + signal arrays (excluding the hash field); project-standard digest length (e.g. sha256 hex truncated like SOB/SROB).

## **5.7 Audit record**

```
cnob_audit_record:
  support_yaml_load_status: ok | partial | fail
  family_encoding_decisions: []
  gap_decisions: []
  conflict_decisions: []
  importance_decisions: []
  provenance_lineage:
    origin: CnOB
    last_update: CnOB
  cnob_constraint_map_hash: string
  constraint_residue_hash: string
  timestamp: iso8601
```

---

# **6. v1 Rule Behaviors (enough for goldens)**

### **6.1 Structural families**

| Condition | Emit |
|-----------|------|
| `len(segments) >= 1` | C1 `c1_segment_exists` |
| `len(segments) >= 2` | C3 `c3_multi_segment_order` |
| any `list_item` | C4 `c4_list_boundary` |
| any list_item with `parent_id` | C2 `c2_list_parent_child` |
| any segment with id | C5 `c5_segment_id_lineage` (once) |
| `len(segments) >= 2` | C6 `c6_multi_segment_change_surface` |

### **6.2 Tag-driven**

| Condition | Emit |
|-----------|------|
| any operator | C1 `c1_operator_present` |
| any lexical_constraints | C7 `c7_constraint_hint_present` |
| discourse_flags non-empty | C2 `c2_discourse_present` |

### **6.3 Gaps**

| Condition | Emit |
|-----------|------|
| empty/whitespace text | missing_slot `miss_empty_text` |
| interrogative, no operators | underspec `under_question_no_operator` |
| constraints, no operators | underspec `under_constraint_no_operator` |

### **6.4 Conflicts (Q8)**

| Condition | Emit |
|-----------|------|
| precision + conciseness in lexical_constraints | `conf_precision_vs_conciseness` |
| imperative + interrogative modalities | `conf_imperative_vs_interrogative` |

### **6.5 Importance**

| Condition | Labels |
|-----------|--------|
| `anchor_like` | `constraint_anchor` |
| any missing_slot | `gap_high` |
| any conflict | `conflict_high` |
| `list_lead` | `order_sensitive` |

---

# **7. Forbidden Behavior**

CnOB must not:

- load `srob_*.yaml` or `sob_*.yaml`
- require hierarchical key sync with SROB YAML trees (wrong sync model)
- re-segment or renumber segment ids
- invent operators/domains/tones/constraint **types** not on TP
- fill missing content as meaning
- enforce constraints on TP text
- evaluate truth or assign stance-as-conclusion
- resolve referent identity
- consume routing_metadata / Pipeline-B ΔH% envelopes
- write outside CnOB-owned fields
- require other primitives to read diagnostic-only metadata

---

# **8. Implementation Skeleton (Python)**

```python
class CnOB:
    def __init__(self, tp_input):
        self.tp = tp_input

    def process(self):
        rules = self._load_support_yamls()  # CnOB only
        srob_map = self._read_srob_map(self.tp)
        srob_residue = self._read_srob_residue(self.tp)

        families = self._encode_families(srob_map, srob_residue, rules)
        missing, under = self._apply_gap_rules(srob_map, srob_residue, rules)
        conflicts = self._apply_conflict_rules(srob_map, srob_residue, rules)
        importance = self._apply_importance(
            srob_map, missing, under, conflicts, rules
        )

        cnob_map = self._build_constraint_map(
            families, missing, under, conflicts, importance
        )
        residue = self._build_residue(cnob_map, missing, under, conflicts, importance)
        audit = self._build_audit_record(cnob_map, residue)

        self.tp.setdefault("structural", {})
        self.tp["structural"]["cnob_constraint_map"] = cnob_map
        self.tp["structural"]["cnob_residue"] = residue
        self.tp.setdefault("metadata", {})
        self.tp["metadata"]["cnob_audit_record"] = audit
        return self.tp
```

---

# **9. Downstream Consumption**

| Primitive | Consumes | Purpose |
|-----------|----------|--------|
| **SmOB** | cnob map/residue | semantic-adjacent cues from constraints/gaps |
| **SSG/TR/RB** | residue hash + C7 / routing_constraints | exact addressing + eligibility |
| **ISc** | constraint features | scoring |
| **IdOB** | gaps/conflicts/importance | reduced search; content often TPU |

---

# **10. Locked Policies (Q1–Q9)**

| ID | Topic | Lock |
|----|--------|------|
| **Q1** | Map style | Full `cnob_constraint_map` every run |
| **Q2** | Segment ids | Reference SROB ids; do not renumber |
| **Q3** | Importance | Multi-label allowed |
| **Q4** | Empty | Empty family lists OK; keys present |
| **Q5** | Input | Prefer/require SROB in full Path-A |
| **Q6** | Schema | **This document** |
| **Q7** | Hash | Canonical map + signal arrays |
| **Q8** | Conflict example | precision vs conciseness |
| **Q9** | Coupling | **TP surface contract only — not dictionary sync** |

---

# **11. Testbench contract (normative intent)**

- Inputs: **SROB-shaped** TP (`structural.srob_*`)
- Expected: schemas §5; triage “sync” failures with §3.1 / comm_architect §2.4
- Minimum scenarios:
  1. Single declarative + operator → C1; no conflict
  2. List parent/child → C2/C4
  3. Empty text → missing_slot
  4. Interrogative, no operator → underspecification
  5. precision + conciseness → conflict Q8
  6. anchor_like → constraint_anchor

---

# ⭐ **End of Document — `cnob_py_struc_pgm.md` (Version 1.1)**

---

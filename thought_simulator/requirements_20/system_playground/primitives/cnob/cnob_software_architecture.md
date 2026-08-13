# **CnOB Software Architecture**
*(primitives/cnob/cnob_software_architecture.md)*

**Status:** Working design; **Q1–Q8 locked for v1** (see `cnob_srob_comm_architect.md`, `cnob_py_struc_pgm.md`)  
**Aligned with:** 20.40.030 v2.0, 20.40.020 v2.0, cnob_srob_comm_architect.md  
**Non-goals:** Full rule depth, testbench file bodies (schemas support writing them), full `cnob.py`

---

## **1. Architectural Philosophy**

The CnOB layer must be:

- **small** — core logic in one file (`cnob.py`)
- **linear** — project SROB TP surface → constraint objects; no second structure engine
- **modular** — C1–C7, gap, conflict, importance rules externalized
- **deterministic** — identical TP(SROB) + rules → identical CnOB output
- **bounded** — constraint-domain interpretation only
- **debuggable** — every signal traceable to a rule id
- **expandable** — deepen rules under fixed family names
- **orthogonal to SROB** — constraint window, not finer SROB

**Invariant:** SROB does not surprise CnOB.  
**Schema authority (Q6):** Normative v1 shapes live in **`cnob_py_struc_pgm.md`**.

---

## **2. Directory Structure**

```
primitives/
  srob/
    srob.py
    srob_*.yaml

  cnob/
    cnob.py
    cnob_software_architecture.md
    cnob_py_struc_pgm.md
    cnob_srob_comm_architect.md

    cnob_constraint_rules.yaml     # C1–C7 (+ discourse fold if small)
    cnob_missing_slot_rules.yaml   # missing-slot + underspec
    cnob_conflict_rules.yaml       # conflict indicators
    cnob_importance_rules.yaml     # → constraint-importance
```

**Testbench YAMLs** live under progressive-lineup paths (not defined here).

---

## **3. CnOB Core (`cnob.py`)**

### **3.1 Responsibilities**

1. Load CnOB support YAMLs only (not `srob_*.yaml` / `sob_*.yaml`)
2. Read **SROB** map/residue from TP (required when present)
3. Optionally read allowed CE/context cues read-only
4. Encode **C1–C7** from structure + tags per rules
5. Emit **missing-slot** and **underspecification** signals
6. Emit **conflict** indicators
7. Map structural-importance → **constraint-importance** (multi-label OK)
8. Canonical-order all constraint collections
9. Build full **`cnob_constraint_map`** + **`cnob_residue`**
10. Hash constraint residue / map
11. Write CnOB-owned fields + audit

**Does not:** re-normalize structure; re-lex text; invent tag types; renumber segment ids; enforce constraints; resolve meaning/referents; write upstream or meaning-layer fields; read routing ΔH% envelopes.

### **3.2 Execution flow**

```
load_cnob_yaml_files()
srob_map, srob_residue = read_srob_fields(tp)  # prefer SROB; SOB fallback only if absent

families = encode_constraint_families(...)      # C1–C7
gaps = apply_missing_slot_rules(...)
conflicts = apply_conflict_rules(...)
importance = apply_importance_rules(...)

families, gaps, conflicts, importance = canonicalize_order(...)

map = build_full_constraint_map(...)            # Q1 full map
residue = form_residue(...)
audit = build_audit(...); hashes

write owned fields only
return tp
```

---

## **4. Support YAML Roles**

### **4.1 `cnob_constraint_rules.yaml`**

- Per-family rules: `id`, `family` (C1–C7), `if` conditions over SROB fields, `emit` payload
- Conditions may reference: segment type/modality/depth, operators, domains, tones, lexical_constraints, discourse_flags, segment count
- Output entries include `family`, `rule_id`, optional `segment_ids[]`, optional `note`

### **4.2 `cnob_missing_slot_rules.yaml`**

- Patterns → `missing_slot` or `underspecification`
- Bind to `segment_ids` when local

### **4.3 `cnob_conflict_rules.yaml`**

- Pair/set conditions on tags or modalities → `conflict` entries with `rule_id` and participants

### **4.4 `cnob_importance_rules.yaml`**

- Map structural_importance labels and/or gap/conflict presence → constraint-importance labels
- Multi-label allowed (Q3)

---

## **5. Upstream / Downstream**

**Reads:** `srob_structural_map`, `srob_residue`, optional context; not SROB YAML files.  
**Writes:** `cnob_constraint_map`, `cnob_residue`, `cnob_audit_record`.  
**Consumers:** SmOB (primary), then SSG/TR/RB/ISc/IdOB (features/cues).

**Sufficiency:** starved CnOB ⇒ fix SROB/handoff.

---

## **6. Owned Fields**

| Field | Role |
|-------|------|
| `TP.structural.cnob_constraint_map` | Full constraint view (Q1) |
| `TP.structural.cnob_residue` | Gaps, conflicts, importance fragments, hash handles |
| `TP.metadata.cnob_audit_record` | Decisions, rule ids, hashes, lineage |
| optional diagnostics | Developer-only |

---

## **7. Locked policies (summary)**

| ID | Lock |
|----|------|
| Q1 | Full map every run |
| Q2 | Preserve / reference SROB segment ids |
| Q3 | Multi-label constraint-importance |
| Q4 | Empty families allowed; still emit map |
| Q5 | Prefer/require SROB in full Path-A |
| Q6 | Schema in `cnob_py_struc_pgm.md` |
| Q7 | Hash canonical map+residue core |
| Q8 | v1 conflict example: precision vs conciseness tags |

---

## **8. Summary**

CnOB software architecture is **SROB-shaped but constraint-domain**: small core, policy YAMLs, orthogonal projection, deterministic, owned-field writes, hash for exact addressing — not soft coherence.

---

**End of `cnob_software_architecture.md`**

---

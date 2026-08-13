# **CnOB Software Architecture**
*(primitives/cnob/cnob_software_architecture.md)*

**Status:** Working design; **Q1–Q9 locked for v1** (see `cnob_srob_comm_architect.md`, `cnob_py_struc_pgm.md`)  
**Aligned with:** 20.40.030 v2.0, 20.40.020 v2.0, cnob_srob_comm_architect.md v1.1  
**Non-goals:** Full rule depth, testbench file bodies, full `cnob.py`

---

## **1. Architectural Philosophy**

The CnOB layer must be:

- **small** — core logic in one file (`cnob.py`)
- **linear** — project SROB TP surface → constraint objects; no second structure engine
- **modular** — C1–C7, gap, conflict, importance rules externalized
- **deterministic** — identical TP(SROB) + rules → identical CnOB output
- **bounded** — constraint-domain interpretation only
- **debuggable** — every signal traceable to a rule id; coupling model explicit
- **expandable** — deepen rules under fixed family names
- **orthogonal to SROB** — constraint window, not finer SROB

**Invariant:** SROB does not surprise CnOB.  
**Schema authority (Q6):** Normative v1 shapes live in **`cnob_py_struc_pgm.md`**.  
**Coupling authority (Q9):** Full statement in **`cnob_srob_comm_architect.md` §2.4**.

---

## **2. Directory Structure**

```
primitives/
  srob/
    srob.py
    srob_*.yaml                 # NOT loaded by CnOB

  cnob/
    cnob.py
    cnob_software_architecture.md
    cnob_py_struc_pgm.md
    cnob_srob_comm_architect.md

    cnob_constraint_rules.yaml     # predicates over SROB TP surface only
    cnob_missing_slot_rules.yaml
    cnob_conflict_rules.yaml
    cnob_importance_rules.yaml
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

**Does not:** re-normalize structure; re-lex text; invent tag types; renumber segment ids; enforce constraints; resolve meaning/referents; write upstream or meaning-layer fields; read routing ΔH% envelopes; **maintain a hierarchical key sync with `srob_*.yaml`**.

### **3.2 Execution flow**

```
load_cnob_yaml_files()                      # CnOB YAMLs only
srob_map, srob_residue = read_srob_fields(tp)

families = encode_constraint_families(...)
gaps = apply_missing_slot_rules(...)
conflicts = apply_conflict_rules(...)
importance = apply_importance_rules(...)

canonicalize_order(...)
map = build_full_constraint_map(...)
residue = form_residue(...)
audit = build_audit(...); hashes
write owned fields only
return tp
```

---

## **4. Support YAML Roles**

Conditions in these files are **TP surface predicates**, not indexes into SROB YAML key trees.

### **4.1 `cnob_constraint_rules.yaml`**

- Per-family rules: `id`, `family` (C1–C7), `if` over SROB TP fields, `emit` payload
- May reference: segment type/modality/depth, operators, domains, tones, lexical_constraints, discourse_flags, segment count

### **4.2 `cnob_missing_slot_rules.yaml`**

- Patterns → `missing_slot` or `underspecification`

### **4.3 `cnob_conflict_rules.yaml`**

- Pair/set conditions on tags or modalities → `conflict` entries

### **4.4 `cnob_importance_rules.yaml`**

- structural_importance / gap / conflict → constraint-importance labels (multi-label OK)

---

## **5. Upstream / Downstream and Coupling**

### **5.1 Upstream**

**Reads from TP:** `srob_structural_map`, `srob_residue`, optional context.  
**Does not read or load:** `srob_*.yaml`, `sob_*.yaml`.

**Sufficiency:** starved CnOB ⇒ fix SROB/handoff.

### **5.2 Coupling: surface contract (not dictionary sync)**

| Do | Do not |
|----|--------|
| Depend on SROB **field names and tag-space conventions** on the TP | Depend on key-for-key parity with `srob_sharpen_maps.yaml` |
| Keep every SROB dependency **visible in rule `if:`** | Hide assumptions in prose-only comments |
| Treat missing expected **fields** as handoff defects | Treat missing SROB *fine-id children* as CnOB desync |
| Match constraint-hint names to SROB `lexical_constraints` space | Invent a second constraint-hint lexicon inside CnOB |

**Debug order:** TP(SROB) fields → rule `if:` match → CnOB encode logic. Never load SROB YAMLs to “repair” CnOB.

Full matrix and support classification: **`cnob_srob_comm_architect.md` §2.4**.

### **5.3 Downstream**

**Writes:** `cnob_constraint_map`, `cnob_residue`, `cnob_audit_record`.  
**Consumers:** SmOB (primary), then SSG/TR/RB/ISc/IdOB.

---

## **6. Owned Fields**

| Field | Role |
|-------|------|
| `TP.structural.cnob_constraint_map` | Full constraint view (Q1) |
| `TP.structural.cnob_residue` | Gaps, conflicts, importance, hash |
| `TP.metadata.cnob_audit_record` | Decisions, rule ids, hashes, lineage |
| optional diagnostics | Developer-only |

---

## **7. Locked policies (summary)**

| ID | Lock |
|----|------|
| Q1 | Full map every run |
| Q2 | Reference SROB segment ids |
| Q3 | Multi-label constraint-importance |
| Q4 | Empty families OK; keys present |
| Q5 | Prefer/require SROB in full Path-A |
| Q6 | Schema in `cnob_py_struc_pgm.md` |
| Q7 | Hash canonical map+residue core |
| Q8 | Conflict example: precision vs conciseness |
| **Q9** | **Surface-contract coupling only — not dictionary sync** |

---

## **8. Summary**

CnOB is **SROB-shaped in software layout** but **constraint-domain in function**.  
Synchronization with SROB is a **TP surface contract** made obvious in rule predicates — not a hierarchical vocab mirror of `srob_*.yaml`.

---

**End of `cnob_software_architecture.md`**

---

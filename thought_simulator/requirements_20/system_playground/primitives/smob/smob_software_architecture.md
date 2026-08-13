# **SmOB Software Architecture**
*(primitives/smob/smob_software_architecture.md)*

**Status:** Working design; **R1–R9 locked for v1**  
**Aligned with:** 20.40.040 v2.0, smob_cnob_comm_architect.md, sob_to_smob_chain.md  
**Non-goals:** Full cue depth, testbench bodies, full `smob.py`

---

## **1. Architectural Philosophy**

The SmOB layer must be:

- **small** — core in `smob.py`
- **two-phase** — Job 1 cues, then Job 2 compress (R9)
- **modular** — cue / discourse / importance / compress YAMLs
- **deterministic** — identical TP(CnOB) + rules → identical SmOB output
- **bounded** — semantic-adjacent only; no deep meaning
- **debuggable** — every cue traceable to a rule id; coupling explicit
- **orthogonal to CnOB** — cue+compress window, not re-constraint

**Invariant:** CnOB does not surprise SmOB.  
**Schema authority (R5):** `smob_py_struc_pgm.md`.  
**Coupling authority (R4):** `smob_cnob_comm_architect.md` §2.6.

---

## **2. Directory Structure**

```
primitives/
  cnob/
    cnob.py
    cnob_*.yaml                 # NOT loaded by SmOB

  smob/
    smob.py
    smob_software_architecture.md
    smob_py_struc_pgm.md
    smob_cnob_comm_architect.md
    sob_to_smob_chain.md

    smob_cue_rules.yaml
    smob_discourse_rules.yaml    # optional fold into cue_rules
    smob_importance_rules.yaml
    smob_compress_rules.yaml
```

Testbench YAMLs live under progressive-lineup paths.

---

## **3. SmOB Core (`smob.py`)**

### **3.1 Responsibilities**

1. Load SmOB YAMLs only  
2. Read **CnOB** map/residue from TP (required when present)  
3. Optionally read SROB surface / CE cues read-only  
4. **Job 1:** extract cue families  
5. Normalize discourse-adjacent cues  
6. Map constraint-importance → semantic-adjacent importance  
7. Canonical-order all cue collections  
8. **Job 2:** build TR-input vector + pre-semantic residue hash  
9. Optional change signals from allowed fields  
10. Write SmOB-owned fields + audit  

**Does not:** load upstream OB YAMLs; re-encode C1–C7 as primary product; invent meaning; read routing_metadata / Pipeline-B ΔH% envelopes; overwrite upstream OB fields.

### **3.2 Execution flow**

```
load_smob_yaml_files()
cnob_map, cnob_residue = read_cnob_fields(tp)  # prefer CnOB

cues = extract_cues(...)                 # Job 1
cues = normalize_discourse(...)
importance_adj = apply_importance(...)
cues = canonicalize(cues, importance_adj)

tr_vector = form_tr_input(...)           # Job 2
hash = compress_hash(...)
change = optional_delta_signals(...)

map = build_full_cue_map(...)
residue = form_residue(...)
audit = build_audit(...)
write owned fields
return tp
```

---

## **4. Support YAML Roles**

### **4.1 `smob_cue_rules.yaml`**

- Predicates over CnOB signals (and optional SROB modality/tags) → cue ids  
- Families: conflict_adjacent, underspec_adjacent, routing_semantic, modality, etc.

### **4.2 `smob_discourse_rules.yaml`**

- Canonical names for discourse-adjacent cues  
- May fold into cue_rules if still thin

### **4.3 `smob_importance_rules.yaml`**

- `constraint_importance` labels → semantic-adjacent importance labels  
- Multi-label allowed

### **4.4 `smob_compress_rules.yaml`**

- Ordered TR vector **slots** and which cue families feed each slot  
- Hash inclusion list (canonical)

---

## **5. Upstream / Downstream and Coupling**

**Reads:** `cnob_constraint_map`, `cnob_residue` (prefer); optional `srob_*` surface; allowed CE read-only.  
**Does not load:** any upstream `*_rules.yaml` from other OB folders.  
**Writes:** `smob_cue_map`, `smob_residue`, `smob_audit_record` (names normative in py_struc).  
**Consumers:** SSG (primary), TR/RB, IdOB, ISc.

**Coupling:** surface + residue contract only — see comm_architect §2.6.

---

## **6. Owned Fields**

| Field | Role |
|-------|------|
| `TP.structural.smob_cue_map` | Full cue view (R1) |
| `TP.structural.smob_residue` | Compact signals + `presemantic_residue_hash` + `tr_input_cues` |
| `TP.metadata.smob_audit_record` | Decisions, hashes, lineage |
| optional diagnostics | Developer-only |

---

## **7. Locked policies**

| ID | Lock |
|----|------|
| R1 | Full cue map every run |
| R2 | Reference segment ids only |
| R3 | Prefer/require CnOB in full Path-A |
| R4 | Surface + residue contract |
| R5 | Schema in `smob_py_struc_pgm.md` |
| R6 | Canonical hash input |
| R7 | Affect thin/optional v1 |
| R8 | Fixed ordered TR slots |
| R9 | Job 1 then Job 2 |

---

## **8. Summary**

SmOB is **CnOB-shaped in software layout**, **cue+compress in function**, and **SSG-facing in responsibility**.  
Synchronization is a **CnOB TP residue contract**, not a dictionary mirror of `cnob_*.yaml`.

---

**End of `smob_software_architecture.md`**

---

# **SmOB ↔ CnOB Communication Architecture**
**Document:** `primitives/smob/smob_cnob_comm_architect.md`  
**Status:** Design / deliberation (implementation-ready contract)  
**Version:** 1.0  
**Purpose:** Make the CnOB → SmOB handoff explicit before YAML bodies or `smob.py`  
**Aligned with:** 20.40.040 v2.0 (SmOB), 20.40.030 v2.0 (CnOB), 20.40.020, sob_to_smob_chain.md  
**Non-goals:** Coding, full testbench bodies (schemas in `smob_py_struc_pgm.md` must enable them)

---

## **1. Why this document exists**

SmOB is the **fourth OB layer** and the **boundary object** to SSG.  
It must not become a meaning engine, a second CnOB, or a generative filler.  
This file is the **communication contract**: what CnOB guarantees, what SmOB does, coupling for support, and open choices.

**Support note:** Sync bugs between OB layers are expensive. Coupling type is stated **blatantly**.

---

## **2. Core invariants**

### **2.1 CnOB does not surprise SmOB**

**Settled.**

1. **Constraint objects** — C1–C7 keys, missing-slot, underspec, conflict, constraint-importance shapes SmOB sees are those CnOB committed (full map, Q1).
2. **Segment binding** — Constraint signals that carry `segment_ids` use stable SROB/SOB ids; SmOB does not renumber.
3. **No re-constraint pass** — SmOB does not re-emit C1–C7 as its primary job; it **projects** constraint residue into **semantic-adjacent cues** and **compresses**.

If SmOB is starved, that is a **CnOB (or handoff) gap** — not a reason to re-implement CnOB inside SmOB.

### **2.2 Orthogonal window**

| Viewer | Window | Focus |
|--------|--------|--------|
| **CnOB** | Constraint | C1–C7, gaps, conflicts, constraint-importance |
| **SmOB** | Semantic-adjacent + compress | cues, TR-input vector, pre-semantic hash, change/importance-adjacent signals |

Same TP; SmOB **derives cue-space attributes** and **fixed-size addresses** CnOB does not own.

### **2.3 Two jobs (normative intent from 20.40.040)**

| Job | Name | Output class |
|-----|------|--------------|
| **1** | Pre-semantic cue extraction | Semantic-adjacent cues in SmOB-owned fields |
| **2** | Pre-semantic residue compression | Hash + TR-input vector (+ change signals from allowed fields) |

Jobs are **distinct phases** in process order; both bounded and deterministic.

### **2.4 Sufficiency rule (hard)**

> If SmOB cannot perform Jobs 1–2 using **only** what CnOB wrote on the TP (plus SmOB policy YAMLs and allowed read-only context), then **CnOB or the handoff must be modified**.  
> SmOB must not silently re-implement CnOB, re-lex raw text as SOB, or invent free-form meaning.

### **2.5 CnOB field preference (HLR-034)**

When CnOB fields are present, SmOB **SHALL prefer** `cnob_constraint_map` / `cnob_residue` as primary input.  
SROB/SOB fields MAY be used only for progressive isolation or explicit applicability (secondary).

---

### **2.6 Coupling type: SURFACE + RESIDUE CONTRACT — not dictionary sync** *(support-critical)*

| Coupling | SOB ↔ SROB | CnOB ↔ SmOB |
|----------|------------|-------------|
| **Kind** | Vocabulary / dictionary sync | **TP surface + residue contract** |
| **Mechanism** | Parent keys ⊆ coarse; `parent.child` | Rule predicates over **CnOB-owned TP fields** (+ optional SROB surface) |
| **YAML load** | Maps nest under SOB vocab | SmOB **SHALL NOT** load `cnob_*.yaml` / `srob_*.yaml` / `sob_*.yaml` |
| **Key-for-key tree sync** | Required | **Forbidden as design goal** |
| **Alignment evidence** | Hierarchical ids + desync fail | Explicit `if:` predicates + §3 field table |
| **If rule never fires** | Map parents | Did CnOB still emit the residue/field? |

#### **Blatant support rules**

1. SmOB does **not** dictionary-sync to CnOB YAML trees.  
2. SmOB syncs to **CnOB TP outputs** (map + residue + hash handles).  
3. Every CnOB dependency in SmOB rules must be **named in predicates**.  
4. Debug order: TP after CnOB → match `if:` → then SmOB encode/compress — never load `cnob_*.yaml` inside SmOB.  
5. Starvation classification: missing CnOB fields → handoff gap; fields present, bad predicates → SmOB rule bug; wrong objects → SmOB encode bug; expecting YAML key trees → **wrong sync model**.

#### **One-line summary**

**CnOB↔SmOB = synchronized TP constraint-residue contract by explicit predicates — not a parallel dictionary tree.**

---

## **3. What CnOB guarantees on the TP (minimum contract)**

| Field / surface | Required Path-A | SmOB use |
|-----------------|-----------------|----------|
| `structural.cnob_constraint_map` | **Yes** | Job 1 seeds; Job 2 compression input |
| `constraint_families` C1–C7 keys present | **Yes** | Family-adjacent cues; routing-adjacent |
| `missing_slot_signals` | Prefer | Underspec-adjacent / gap cues |
| `underspecification_markers` | Prefer | Underspec-adjacent cues |
| `conflict_indicators` | Prefer | Conflict-adjacent cues |
| `constraint_importance` | Prefer | → semantic-adjacent importance |
| `structural.cnob_residue` | Prefer | Mirror signals + `constraint_residue_hash` |
| `constraint_residue_hash` | Prefer | Composition into pre-semantic hash |
| `metadata.cnob_audit_record` | Optional | Provenance / debug |
| SROB map (secondary) | Optional | Modality/discourse pass-through when needed |

**CnOB does not guarantee:** TR-input vector, SmOB cue taxonomy, pre-semantic residue hash as SmOB defines it, affect markers as SmOB objects, SSG-ready compression package.

---

## **4. Defined duties of SmOB**

### **4.1 Core duty (one sentence)**

SmOB **extracts bounded semantic-adjacent cues from CnOB residue and compresses them into a deterministic pre-semantic hash and TR-input vector**, writing only SmOB-owned fields so SSG/RB/IdOB are not overwhelmed by unconstrained structure.

### **4.2 Work streams**

| Stream | What it is | What it is not |
|--------|------------|----------------|
| **A. Cue extraction (Job 1)** | Map constraint/structure signals → cue families | Deep meaning / truth / stance conclusion |
| **B. Discourse-adjacent normalize** | Canonical pre-semantic discourse cues | Intent inference |
| **C. Importance-adjacent** | Constraint-importance → semantic-adjacent importance | Semantic role labeling |
| **D. Compression (Job 2)** | Canonical order → hash + TR vector | Soft similarity / generative fill |
| **E. Change signals** | From allowed SmOB/upstream cue fields only | Reading forbidden routing ΔH% envelopes |

### **4.3 v1 cue families (thin, testable)**

| Cue family | v1 seed from CnOB / SROB |
|------------|--------------------------|
| `modality_cues` | Segment modalities (prefer SROB surface if present; else secondary) |
| `conflict_adjacent_signals` | CnOB `conflict_indicators` |
| `underspecification_adjacent_signals` | CnOB missing_slot + underspec markers |
| `constraint_importance_adjacent_signals` | CnOB `constraint_importance` |
| `routing_semantic_cues` | Non-empty C7 / routing_constraints; constraint_hint presence |
| `semantic_adjacent_cues` | Aggregated/normalized cue ids for SSG |
| `affect_markers` | Thin v1: empty unless explicit tone→affect map later |
| `discourse_adjacent_cues` | CnOB discourse_constraints / SROB discourse_flags |

### **4.4 Shall / shall not**

| SmOB shall | SmOB shall not |
|------------|----------------|
| Prefer CnOB fields when present | Load `cnob_*.yaml` / `srob_*.yaml` / `sob_*.yaml` |
| Run Job 1 then Job 2 | Re-emit CnOB C1–C7 as primary product |
| Write owned fields only | Overwrite CnOB/SROB/SOB |
| Hash + TR vector deterministically | Deep meaning, truth, referent identity |
| Keep predicates explicit | Dictionary-sync to CnOB rule trees |
| Optional diagnostic-only metadata | Require diagnostics for routing |

---

## **5. Handoff diagram**

```
SROB → CnOB
         │  writes cnob_constraint_map, cnob_residue, cnob_audit_record
         ▼
       SmOB  ← reads CnOB TP fields (prefer); optional SROB surface
         │      surface+residue contract only (§2.6)
         │  writes smob_cue_map / smob_residue, hash, TR vector, audit
         ▼
       SSG → TR / RB / IdOB …
```

---

## **6. Candidate SmOB support files (thin pack)**

| File | Duty |
|------|------|
| `smob_cue_rules.yaml` | Job 1: CnOB/SROB predicates → cue families |
| `smob_discourse_rules.yaml` | Discourse-adjacent normalize (or fold into cue_rules if thin) |
| `smob_importance_rules.yaml` | Constraint-importance → semantic-adjacent importance |
| `smob_compress_rules.yaml` | Job 2: which fields enter hash / TR vector slots |

Header on each: **depends on CnOB TP surface/residue, not on `cnob_*.yaml` key trees.**

---

## **7. Downstream value**

| Consumer | Why SmOB matters |
|----------|------------------|
| **SSG** | Sole pre-semantic package |
| **TR / RB** | Exact TR vector + hash addressing |
| **IdOB** | Cue rails; reduced search |
| **ISc** | Importance / conflict / gap features |

---

## **8. Advantages / risks**

**Advantages:** Clear SSG boundary; two-job split; same software family as CnOB; supportable coupling.  
**Risks:** Semantic creep under “adjacent”; TR vector schema churn; ignoring CnOB and reading only SROB.

---

## **9. Locked leans (R1–R9) for v1**

| ID | Topic | Lean |
|----|--------|------|
| **R1** | Map style | Full SmOB cue map every run |
| **R2** | Segment ids | Reference only; no renumber |
| **R3** | CnOB required | Required in full Path-A |
| **R4** | Coupling | Surface + residue contract (not dictionary sync) |
| **R5** | Schema home | `smob_py_struc_pgm.md` |
| **R6** | Hash | Canonical SmOB cue+signal body |
| **R7** | Affect v1 | Empty / optional unless rule fires |
| **R8** | TR vector | Fixed ordered slots from compress rules |
| **R9** | Jobs order | Cue extraction then compression |

---

## **10. Testbench readiness**

`smob_testbench.yaml` SHALL use **CnOB-shaped TP inputs** (post-CnOB), parallel to CnOB tests using SROB-shaped inputs.  
Triage “sync” failures with §2.6.

---

**End of `smob_cnob_comm_architect.md` (v1.0)**

---

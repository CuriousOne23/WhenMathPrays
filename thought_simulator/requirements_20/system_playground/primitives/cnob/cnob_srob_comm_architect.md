# **CnOB ↔ SROB Communication Architecture**
**Document:** `primitives/cnob/cnob_srob_comm_architect.md`  
**Status:** Design / deliberation (implementation-ready contract)  
**Version:** 1.1  
**Purpose:** Make the SROB → CnOB handoff explicit before YAML bodies or `cnob.py`  
**Aligned with:** 20.40.020 v2.0 (SROB), 20.40.030 v2.0 (CnOB), 20.40.010, tp_path_a_map.md  
**Non-goals:** Coding, full testbench YAML content (schemas must be enough to write them)

---

## **1. Why this document exists**

CnOB is the third OB layer. It must not become “SROB 2” or a meaning engine.  
This file is the **communication contract**: what SROB guarantees, what CnOB does with it, what new object types CnOB owns, **how CnOB is coupled to SROB for support/debug**, and what remains open.

**Support note:** Synchronization bugs between OB layers are expensive. This document states the coupling type **blatantly** so debuggers do not apply the wrong sync model.

---

## **2. Core invariants**

### **2.1 SROB does not surprise CnOB**

**Settled.**

1. **Units** — Segment ids, types, and geometry CnOB sees are those SROB committed (preserving SOB ids). CnOB does not invent new segments from prose.
2. **Tag field space** — Operators, domains, tones, constraint *hints*, discourse flags, structural-importance labels appear only in families already on the SROB TP surface (coarse or fine).
3. **No second structure pass** — CnOB does not re-normalize lists/tables/boundaries. That is SROB’s job.

If CnOB is starved, that is an **SROB (or handoff) gap** — not a reason to re-implement SROB inside CnOB.

### **2.2 Orthogonal window (same object, different attributes)**

| Viewer | Window | Focus |
|--------|--------|--------|
| **SROB** | Structure / tag | Form, sharpened tags, structural-importance |
| **CnOB** | Constraint | C1–C7, missing-slot, underspec, conflict, constraint-importance |

Same TP object; CnOB **projects** into constraint space and **derives** constraint objects SROB never named.

### **2.3 Sufficiency rule (hard)**

> If CnOB cannot perform its duties using **only** what SROB wrote on the TP (plus CnOB’s own policy YAMLs and allowed read-only context), then **SROB or the handoff must be modified**.  
> CnOB must not silently re-implement SROB or re-lex raw text as a second SOB.

---

### **2.4 Coupling type: SURFACE CONTRACT — not dictionary sync** *(normative for support)*

**This is the synchronization model. Do not confuse it with SOB ↔ SROB.**

| Coupling | SOB ↔ SROB | **SROB ↔ CnOB** |
|----------|------------|-----------------|
| **Kind** | **Vocabulary / dictionary sync** | **TP surface contract** |
| **Mechanism** | Sharpen-map parents ⊆ SOB coarse ids; fine ids `parent.child` | Rule `if:` predicates over **fields SROB wrote on the TP** |
| **YAML load** | SROB does not load `sob_*.yaml` for extraction, but maps **must** nest under SOB vocab | CnOB **SHALL NOT** load `srob_*.yaml` or `sob_*.yaml` |
| **Key-for-key tree sync** | **Required** (desync = hard failure) | **Forbidden as a design goal** — there is no parallel CnOB parent tree of SROB fine ids |
| **What must stay aligned** | Category inventory | **Field names + tag-space conventions** on the TP |
| **Where alignment is evident** | Hierarchical ids + load-time `SROB_MAP_DESYNC` | **Readable rule `if:` clauses** + SROB TP field table (§3) |
| **If a rule “never fires”** | Check map parents vs SOB | Check whether SROB still **emits** the field/convention the `if:` names |
| **If SROB adds `explain.detail`** | Must hang under `explain` | CnOB usually **unchanged** (cares “operator present,” not which fine child) |
| **If SROB renames or drops `lexical_constraints`** | N/A to this row | **Handoff/support defect** — update SROB or CnOB predicates; do **not** invent tags inside CnOB |

#### **Blatant support rules**

1. **CnOB does not dictionary-sync to SROB YAMLs.** Never require CnOB rule files to list every `srob_sharpen_maps` parent/child.
2. **CnOB is synchronized to the SROB TP surface.** Allowed dependencies are only:
   - `segments[]` (`id`, `type`, `text`, `modality`, list geometry, …)
   - `operators`, `lexical_domains`, `lexical_tones`, `lexical_constraints`
   - `discourse_flags`, structural_importance labels
   - `srob_residue` cues as secondary
3. **Evidence of coupling must stay in the open:** every CnOB rule condition that depends on SROB must use an **explicit predicate name** that matches §3 field language (e.g. `operators_non_empty`, `lexical_constraints_contains_all`, `any_list_item`). Hidden implicit assumptions are a support hazard.
4. **Tag-space convention:** names such as `precision` / `conciseness` in conflict rules mean the **same constraint-hint space** SROB puts on `lexical_constraints` (full id or parent/suffix of a fine id). CnOB does not invent a second constraint-hint lexicon.
5. **Debug order when CnOB looks “wrong”:**
   1. Inspect **TP after SROB** (map/residue present? field names?)
   2. Match **rule `if:`** to those fields  
   3. Only then change CnOB YAMLs  
   4. Never “fix” by loading `srob_*.yaml` inside CnOB
6. **Starvation classification:**
   - Missing SROB fields CnOB needs → **SROB/handoff gap**
   - Fields present, rule predicates wrong → **CnOB rule bug**
   - Fields present, predicates OK, wrong constraint *objects* → **CnOB encode bug**
   - Expectation that CnOB keys track SROB fine-id trees → **wrong sync model** (read this section)

#### **One-line summary**

**SOB↔SROB = synchronized vocab by hierarchical construction.**  
**SROB↔CnOB = synchronized TP surface contract by explicit rule predicates — evident in `if:` clauses, not by a parallel dictionary tree.**

---

## **3. What SROB guarantees on the TP (minimum contract)**

After SROB, CnOB expects:

| Field / surface | Required for normal Path-A | CnOB use |
|-----------------|----------------------------|----------|
| `structural.srob_structural_map.segments[]` | **Yes** | C1–C4; missing-slot/underspec; bind signals to `id` |
| Segment `id` stable (SOB→SROB preserved) | **Yes** | Lineage / alignment of constraint signals |
| `type`, `text`, `modality` on segments | **Yes** | Boundary/order/existence cues |
| List geometry (`depth`, `parent_id`, …) when list_item | When lists present | C2–C4 nesting/order |
| `operators`, `lexical_domains`, `lexical_tones`, `lexical_constraints` | Prefer present | Seed constraint patterns; conflict |
| `discourse_flags` | Optional | Discourse → constraint-relevant metadata |
| Per-segment or aggregate structural_importance | Optional | → constraint-importance |
| `structural.srob_residue` | Prefer present | pass-through/refined tags as cues |
| `metadata.srob_audit_record` | Optional | Provenance / debug only |

**SROB does not guarantee:** C1–C7 objects, missing-slot signals, conflict indicators, constraint-importance residues, constraint-residue hash. Those are **CnOB outputs**.

**Support:** This table is the **authoritative surface checklist** for SROB↔CnOB synchronization issues.

---

## **4. Defined duties of CnOB**

### **4.1 Core duty (one sentence)**

CnOB **extracts monotonic constraint residue** from SROB’s refined structure and tags, writing only CnOB-owned fields, so SmOB and routing receive rigid constraint objects rather than rediscovering obligation, absence, and conflict from structure alone.

### **4.2 Work streams**

| Stream | What it is | What it is not |
|--------|------------|----------------|
| **A. Family encoding (C1–C7)** | Map structure + tags → typed constraint family membership | Re-sharpen operator/domain tags |
| **B. Gap signals** | Missing-slot + underspecification markers | Filling in missing meaning |
| **C. Conflict indicators** | Structured clashes among cues/constraints | Resolving which side “wins” as meaning |
| **D. Constraint-importance** | Refine structural-importance into constraint-importance | Semantic role labeling |
| **E. Addressing** | Canonicalize + hash constraint residue | Soft similarity / “like ideas” |

### **4.3 C1–C7 — meaning for implementation (v1 thin definitions)**

| Family | Name | v1 trigger examples (from SROB surface) |
|--------|------|----------------------------------------|
| **C1** | Existence | Segment exists; operator present; required unit type present/absent |
| **C2** | Adjacency | Consecutive segments; list child↔parent; discourse adjacency flags |
| **C3** | Ordering | Segment order; `index_in_parent`; imperative-then-list patterns |
| **C4** | Boundary | list vs sentence boundary; depth changes; block boundaries if present |
| **C5** | Lineage | Stable segment `id` continuity; parent_id links; provenance last_update chain cues |
| **C6** | Structural-change | Allowed structural cues only (e.g. multi-segment vs single); **not** routing ΔH% envelopes |
| **C7** | Routing-eligibility | Constraint-form eligibility flags derived from constraint residue (not router decisions) |

### **4.4 Missing-slot / underspec / conflict (v1)**

| Signal | v1 rule lean (deterministic, thin) |
|--------|-------------------------------------|
| **missing_slot** | Empty/whitespace `text` on a segment; list_item with no substance; operator requires object-like continuation that next segment lacks (structural only) |
| **underspecification** | Interrogative modality with no operator; single vague segment with no domain/constraint hints; constraint hint present but no operator |
| **conflict** | Competing constraint *hints* on same TP (e.g. precision + conciseness tags both present); imperative + interrogative modality mix across segments without discourse reconciliation |

CnOB **records** conflict; it does **not** enforce a resolution.

### **4.5 Constraint-importance (v1)**

| Example structural cue | Example constraint-importance labels |
|------------------------|--------------------------------------|
| `anchor_like` / first sentence | `constraint_anchor` |
| `list_lead` | `missing_slot_watch`, `order_sensitive` |
| conflict present | `conflict_high` |
| missing_slot present | `gap_high` |

Multi-label **allowed**.

### **4.6 Shall / shall not**

| CnOB shall | CnOB shall not |
|------------|----------------|
| Prefer SROB fields when present | Load `srob_*.yaml` or `sob_*.yaml` |
| Emit C1–C7, gap, conflict, importance | Re-normalize structure |
| Write owned fields only | Invent segments or tag **types** |
| Hash constraint residue | Enforce constraints on user text |
| Keep rule predicates explicit vs §3 surface | Assume hierarchical sync with `srob_*.yaml` |
| Stay bounded constraint-domain | Deep meaning, truth, referents, stance-as-conclusion |
| Monotonic within one `process()` | Remove constraints mid-construction |

---

## **5. Handoff diagram**

```
SOB → SROB
        │  writes:
        │    structural.srob_structural_map
        │    structural.srob_residue
        │    metadata.srob_audit_record
        ▼
      CnOB   ← reads SROB fields from TP only
        │       (does not load srob_*.yaml / sob_*.yaml)
        │       surface-contract coupling only (§2.4)
        │  writes:
        │    structural.cnob_constraint_map
        │    structural.cnob_residue
        │    metadata.cnob_audit_record
        │    (+ optional diagnostic-only)
        ▼
      SmOB → SSG / TR / RB / IdOB …
```

---

## **6. Candidate CnOB support files (thin pack)**

| File | Duty |
|------|------|
| `cnob_constraint_rules.yaml` | C1–C7 detection/encoding; discourse→constraint folds here if small |
| `cnob_missing_slot_rules.yaml` | missing-slot + underspec patterns |
| `cnob_conflict_rules.yaml` | conflict indicators |
| `cnob_importance_rules.yaml` | structural-importance → constraint-importance |

Each file’s header SHALL state: depends on **SROB TP surface**, not on `srob_*.yaml` key trees.

---

## **7. Downstream value**

| Consumer | Why CnOB matters |
|----------|------------------|
| **SmOB** | Constraint residue + importance → semantic-adjacent cues without rediscovering gaps |
| **SSG / TR / RB** | Routing-eligible constraint features + hashes for exact addressing |
| **IdOB** | Reduced space: obligations/gaps visible; content still often TPU |
| **ISc** | Constraint features for scoring |

---

## **8. Advantages / disadvantages / holes / concerns**

**Advantages:** Orthogonal to SROB; falsifiable sufficiency; parallel software shape; testable C1–C7; explicit surface-contract for support.

**Disadvantages:** More TP maps; thin C1–C7 until rules grow; conflict rules can be noisy.

**Holes:** Exact conflict inventory; progressive-lineup without SROB.

**Concerns:** Semantic creep; wrong sync model (treating CnOB like SROB vocab maps); consumers ignoring CnOB.

---

## **9. Open decisions**

| # | Choice | Lean (v1 lock for testbench) |
|---|--------|------------------------------|
| **Q1** | Map style | **Full** `cnob_constraint_map` every run |
| **Q2** | Segment binding | Constraint signals **reference SROB/SOB segment ids**; no renumber |
| **Q3** | Multi-label importance | **Allowed** |
| **Q4** | Empty constraints | Allowed; still emit full map |
| **Q5** | SROB required | **Required** in full Path-A |
| **Q6** | Schema authority | **`cnob_py_struc_pgm.md`** |
| **Q7** | Hash input | Canonical map + core residue signals |
| **Q8** | Conflict precision+conciseness | **Yes** v1 example |
| **Q9** | Coupling model | **Surface contract only** (§2.4) — settled |

---

## **10. Settled vs open**

**Settled:** Orthogonal window; no-surprise; TP-only handoff; **surface-contract coupling (not dictionary sync)**; no YAML load of SROB/SOB; owned fields; C1–C7; Q1–Q9.

**Still open for later depth:** Richer C6; policy_constraints body; soft similarity (out of scope for hash).

---

## **11. Testbench readiness note**

`cnob_testbench.yaml` SHALL use **SROB-shaped TP inputs** and expected blocks matching `cnob_py_struc_pgm.md`.  
Failures that look like “sync” issues SHALL be triaged with §2.4 debug order.

---

**End of `cnob_srob_comm_architect.md` (v1.1)**

---

# **SOB → SROB → CnOB → SmOB Chain**
**Document:** `design/papers/ts_patha_architecture/sob_to_smob_chain.md`  
**Status:** Support / orientation (implementation-aligned)  
**Version:** 1.1  
**Purpose:** Progressive-digestion picture for the OB quartet; what each layer does differently; **which YAML files and TP fields must stay synchronized**, how, and why  
**Aligned with:** 20.40.010, 20.40.020 v2.0, 20.40.030 v2.0, 20.40.040 v2.0, tp_path_a_map.md, layer `*_comm_architect.md` files

---

## **1. Why this document exists**

The Path-A OB family exists to **shrink the open meaning/search space** before SSG, TR/RB, and IdOB.  
Each layer has a **different window** on the same TP. Treating SmOB as “finer CnOB” or CnOB as “finer SROB” is a design error and a support trap.

This paper is the **chain-level support authority** for:

1. What each layer *earns*  
2. What SmOB does that the first three do **not**  
3. **Synchronization contracts** (YAML + TP fields) required for SOB → SmOB to operate correctly  

---

## **2. Progressive lineup (macro)**

```
TPU / text surface
        │
        ▼
      SOB     — coarse structure + lexical tags (wide lexicon)
        │
        ▼
      SROB    — normalize structure + sharpen tags (deeper policy, same families)
        │
        ▼
      CnOB    — constraint objects (C1–C7, gaps, conflicts, constraint-importance)
        │
        ▼
      SmOB    — semantic-adjacent cues + compression (hash, TR-input vector)
        │
        ▼
   SSG / TR / RB / IdOB / …
```

**Goal of the chain:** human-league, non-omniscient digestion — rigid fields, visible gaps, exact addressing — not perfect meaning.

---

## **3. Layer comparison (summary)**

| Layer | Window | Primary writes | Coupling to previous |
|-------|--------|----------------|----------------------|
| **SOB** | Text → coarse units/tags | `sob_structural_map`, `sob_residue` | Lexicons / extraction |
| **SROB** | Structure/tag refinement | `srob_structural_map`, `srob_residue` | **Dictionary sync** to SOB parents |
| **CnOB** | Constraint projection | `cnob_constraint_map`, `cnob_residue` | **TP surface contract** with SROB |
| **SmOB** | Semantic-adjacent cue + compress | `smob_cue_map` / residue, hash, TR vector | **TP surface + residue contract** with CnOB (prefer CnOB) |

---

## **4. What each layer *earns***

| Layer | Earns its place by… |
|-------|---------------------|
| **SOB** | Making structure and coarse tags **exist** from text |
| **SROB** | Making structure **canonical** and tags **higher-resolution** without a second lexicon |
| **CnOB** | Making **obligation, absence, conflict** explicit as constraint objects |
| **SmOB** | Making **SSG/TR-ready cues** and a **fixed-size pre-semantic address** without deep meaning |

Without SmOB, SSG would re-chew CnOB+SROB surfaces and risk unbounded “soft semantics.”  
Without CnOB, SmOB would rediscover gaps/conflicts from structure alone.

---

## **5. What SmOB does differently than SOB, SROB, and CnOB**

**SmOB is not a finer version of the first three.** It changes *what kind of object* is produced and *who it is for*.

### **5.1 Upstream family (shared job class)**

| Layer | Does |
|-------|------|
| **SOB** | Make structure and coarse tags *exist* from text |
| **SROB** | Make structure *canonical* and tags *higher-resolution* (same families, deeper policy) |
| **CnOB** | Project the same TP into *constraint space*: existence, order, gaps, conflicts, importance |

They stay in the **OB residue pipeline**: rigid tags so later stages are not overwhelmed by prose.

### **5.2 SmOB’s distinct jobs**

| Job | Name | Output class |
|-----|------|--------------|
| **1** | Pre-semantic cue extraction | Semantic-adjacent cues in SmOB-owned fields |
| **2** | Pre-semantic residue compression | TR-input vector + presemantic residue hash |

SOB/SROB/CnOB do **not** form a TR vector or a sole pre-semantic package for SSG.

### **5.3 Different product type**

Upstream outputs are mostly **maps of structure / tags / constraints**.  
SmOB’s distinctive outputs are:

- `tr_input_cues` (ordered slots: modality, conflict, underspec, importance, routing, discourse)
- `presemantic_residue_hash`
- cue families aimed at **SSG as sole pre-semantic input**

### **5.4 Consumer, not peer**

- SOB → SROB → CnOB feed **each other** in the OB lineup.  
- SmOB is the **boundary object** to the **SSG signal path**. After SmOB, the next primary consumer is SSG / TR / RB, not another “SmOB-like” OB.

### **5.5 Bounded “semantics” of a different kind**

| Layer | Kind of bounded interpretation |
|-------|--------------------------------|
| SOB / SROB | Lexical / structural tagging (operators, domains, tones, constraints) |
| CnOB | Obligation / absence / conflict as **constraint objects** |
| **SmOB** | **Pre-semantic / semantic-adjacent** signals (“there is a conflict cue,” “gap cue,” “TR slot X is set”) — **not** truth, stance-as-conclusion, referent identity, or free-form meaning |

### **5.6 One-line distinction**

**SOB, SROB, CnOB chew the input into structure and constraints.**  
**SmOB compresses that chew into a routing-ready, SSG-facing pre-semantic package.**

---

## **6. Coupling types (support-critical)**

| Edge | Coupling kind | Fail mode |
|------|---------------|-----------|
| SOB ↔ SROB | Hierarchical **vocab / dictionary sync** | `SROB_MAP_DESYNC` / illegal parents |
| SROB ↔ CnOB | **TP surface contract** (field predicates) | Rule never fires; wrong field names |
| CnOB ↔ SmOB | **TP surface + residue contract** (prefer CnOB map/residue) | Starved cues; wrong sync model if SmOB tries to key-sync CnOB YAML trees |

**Never** apply SOB↔SROB dictionary rules to CnOB or SmOB policy files by default.

---

## **7. Synchronization inventory — what must stay aligned**

This section is the **support checklist**. Wrong sync model is the most expensive class of OB bugs.

### **7.1 Edge A — SOB ↔ SROB (dictionary / vocab sync)**

**Kind:** Hierarchical vocabulary synchronization.  
**Why:** SROB only *sharpens* within families SOB already introduced. If parents diverge, SROB invents illegal fine ids or starves on coarse tags SOB never emits.

#### **YAML files that must stay in sync**

| SOB side | SROB side | Sync rule |
|----------|-----------|-----------|
| `primitives/sob/sob_dictionary.yaml` (and related SOB lexicon packs if split) | `primitives/srob/srob_sharpen_maps.yaml` (and related SROB map packs) | Every SROB fine id **SHALL** hang under a **SOB coarse parent** (`parent.child` or equivalent). Parents ⊆ SOB coarse inventory. |
| SOB operator / domain / tone / constraint inventories | SROB sharpen maps for those same families | Family inventory **must not be disjoint**. Grow together; never fork a second lexicon. |

**How evidence of sync is visible:** hierarchical ids (`explain` → `explain.clarify`); load-time / map validation (`SROB_MAP_DESYNC` or equivalent).

**What SROB does *not* load for extraction:** `sob_*.yaml` at runtime for re-tagging — but **map construction** remains vocabulary-coupled to SOB.

#### **TP fields that must stay aligned**

| Field family | Why |
|--------------|-----|
| Segment `id` (SOB → SROB preserved) | Lineage; CnOB/SmOB bind signals to these ids |
| Segment `type`, `text`, `modality` | Structure + modality cues downstream |
| `operators`, `lexical_domains`, `lexical_tones`, `lexical_constraints` | Same **tag space** SOB named; SROB only refines resolution |
| List geometry (`depth`, `parent_id`, …) when present | CnOB C2–C4 |

**If broken:** SROB looks “wrong,” CnOB rules under-fire, progressive lineup becomes undebugable.

---

### **7.2 Edge B — SROB ↔ CnOB (TP surface contract — not dictionary sync)**

**Kind:** Surface-contract synchronization on **fields SROB wrote on the TP**.  
**Why:** CnOB encodes constraints from structure/tags already present. It must **not** re-implement SROB or mirror `srob_*.yaml` key trees.

#### **YAML files**

| File | Sync requirement |
|------|------------------|
| `cnob_constraint_rules.yaml`, `cnob_missing_slot_rules.yaml`, `cnob_conflict_rules.yaml`, `cnob_importance_rules.yaml` | **SHALL NOT** key-sync to `srob_*.yaml` / `sob_*.yaml` trees. **SHALL** use explicit `if:` predicates over **SROB TP field names/conventions**. |
| Headers on CnOB YAMLs | State: depends on **SROB TP surface**, not SROB YAML key trees. |

**How evidence is visible:** readable rule predicates (`operators_non_empty`, `any_list_item`, `lexical_constraints_contains_all`, …) matching the SROB field table in `cnob_srob_comm_architect.md`.

#### **TP fields CnOB depends on (must remain stable names + conventions)**

| TP surface (after SROB) | Required for normal Path-A | CnOB use |
|-------------------------|----------------------------|----------|
| `structural.srob_structural_map.segments[]` | **Yes** | C1–C4; missing-slot/underspec; bind to `id` |
| Segment `id` stable | **Yes** | Lineage of constraint signals |
| `type`, `text`, `modality` | **Yes** | Boundary / order / existence |
| List geometry when list_item | When lists present | C2–C4 |
| `operators`, `lexical_domains`, `lexical_tones`, `lexical_constraints` | Prefer present | Seed constraint patterns; conflict |
| `discourse_flags` | Optional | Discourse → constraint-relevant metadata |
| structural_importance labels | Optional | → constraint-importance |
| `structural.srob_residue` | Prefer | Secondary cues |

**Tag-space convention:** names such as `precision` / `conciseness` in CnOB conflict rules mean the **same constraint-hint space** SROB puts on `lexical_constraints` (full id or parent/suffix of a fine id). CnOB does **not** invent a second constraint-hint lexicon.

**If SROB renames or drops a field CnOB predicates name:** **handoff/support defect** — update SROB or CnOB predicates; do **not** invent tags inside CnOB.

---

### **7.3 Edge C — CnOB ↔ SmOB (TP surface + residue contract — not dictionary sync)**

**Kind:** Surface + residue contract on **CnOB-owned TP outputs**.  
**Why:** SmOB extracts cues and compresses from constraint residue. Preferring CnOB (HLR-034) keeps the chain monotonic and prevents SmOB from rediscovering obligation from structure alone.

#### **YAML files**

| File | Sync requirement |
|------|------------------|
| `smob_cue_rules.yaml`, `smob_discourse_rules.yaml`, `smob_importance_rules.yaml`, `smob_compress_rules.yaml` | **SHALL NOT** load or key-sync to `cnob_*.yaml` / `srob_*.yaml` / `sob_*.yaml`. **SHALL** depend on **CnOB TP field names and residue conventions**. |
| Headers on SmOB YAMLs | State: CnOB TP surface/residue contract only. |

**How evidence is visible:** predicates such as `cnob_any_conflict`, `cnob_any_missing_slot`, `cnob_c7_or_routing_non_empty`, importance label maps (`gap_high` → `sa_gap_high`) matching CnOB residue shapes.

#### **TP fields SmOB depends on (prefer CnOB)**

| TP surface (after CnOB) | Required Path-A | SmOB use |
|-------------------------|-----------------|----------|
| `structural.cnob_constraint_map` | **Yes** | Job 1 seeds; Job 2 compression input |
| `constraint_families` C1–C7 keys present | **Yes** | Family-adjacent / routing-adjacent cues |
| `missing_slot_signals` | Prefer | Gap-adjacent cues |
| `underspecification_markers` | Prefer | Underspec-adjacent cues |
| `conflict_indicators` | Prefer | Conflict-adjacent cues |
| `constraint_importance` | Prefer | → semantic-adjacent importance (`sa_*`) |
| `structural.cnob_residue` | Prefer | Mirror signals + `constraint_residue_hash` |
| `constraint_residue_hash` | Prefer | Composition into presemantic hash context |
| Optional secondary: `srob_structural_map` modalities / `discourse_flags` | Optional | Modality / discourse-adjacent when applicable |

**Importance label map (v1 closed set — must stay aligned with CnOB emit labels):**

| CnOB `constraint_importance` label | SmOB adjacent |
|------------------------------------|---------------|
| `gap_high` | `sa_gap_high` |
| `conflict_high` | `sa_conflict_high` |
| `constraint_anchor` | `sa_anchor` |
| `order_sensitive` | `sa_order_sensitive` |

If CnOB introduces a new importance label without updating `smob_importance_rules.yaml` (and allow_passthrough policy), SmOB will drop or mis-map it — **support defect on the label contract**, not “SmOB is broken.”

---

### **7.4 What does *not* need YAML tree sync**

| Pair | Not required |
|------|--------------|
| CnOB ↔ SOB dictionary files | No parallel parent tree |
| SmOB ↔ SROB sharpen maps | No hierarchical vocab mirror |
| SmOB ↔ CnOB rule trees | No key-for-key C1–C7 rule file sync |
| Cross-layer loading of upstream YAMLs at runtime | **Forbidden** for CnOB and SmOB extraction |

---

### **7.5 End-to-end field chain (must remain coherent)**

```
SOB writes:
  structural.sob_structural_map / sob_residue
        │  vocab parents
        ▼
SROB writes (preserves segment ids; sharpens tags):
  structural.srob_structural_map / srob_residue
        │  surface field names + tag conventions
        ▼
CnOB writes:
  structural.cnob_constraint_map / cnob_residue
  (+ constraint_residue_hash)
        │  surface + residue shapes / importance labels
        ▼
SmOB writes:
  structural.smob_cue_map / smob_residue
  (tr_input_cues, presemantic_residue_hash)
        │
        ▼
SSG / TR / RB / IdOB
```

**Segment ids** are a **chain invariant** from SOB through SmOB: no renumbering at SROB, CnOB, or SmOB.

---

## **8. Why synchronization matters (failure modes)**

| Break | Symptom | Wrong fix |
|-------|---------|-----------|
| SOB↔SROB vocab desync | Illegal fine tags; empty sharpen; map errors | Re-lex inside SROB without fixing maps |
| SROB renames surface CnOB depends on | CnOB rules never fire | Re-implement structure inside CnOB |
| CnOB stops emitting missing/conflict/importance | SmOB cues starve | Soft “semantics” inside SmOB |
| SmOB expected to track `cnob_*.yaml` trees | Phantom “sync” bugs | Loading CnOB YAMLs in SmOB |
| Segment id renumber | Constraint/cue binding breaks | Ad-hoc re-binding |

**Correct fix order:** prior layer TP → consumer predicates → then policy YAML — do not re-implement upstream inside the starved layer.

---

## **9. Downstream of SmOB**

| Consumer | Uses |
|----------|------|
| **SSG** | Sole pre-semantic input: cues + compressed residue |
| **TR / RB** | TR-input vector + residue hash for exact route keys |
| **IdOB** | Reduced cue/constraint rails; content still often TPU |
| **ISc** | Scoring features from cues/importance |

---

## **10. Support debug order (chain)**

1. Which layer failed?  
2. Inspect **TP owned fields of the prior layer** (not prior YAML trees, **except** SOB↔SROB vocab maps).  
3. Match consumer rule predicates to those fields.  
4. Fix handoff or rules — do not re-implement upstream inside the starved layer.  
5. If the expectation was “dictionary sync all the way down,” re-read §6–§7 — that model applies **only** to SOB↔SROB.

---

## **11. Pointers**

| Topic | Document |
|-------|----------|
| SmOB ↔ CnOB handoff | `primitives/smob/smob_cnob_comm_architect.md` |
| SmOB software shape | `primitives/smob/smob_software_architecture.md` |
| SmOB schemas / process | `primitives/smob/smob_py_struc_pgm.md` |
| CnOB ↔ SROB handoff | `primitives/cnob/cnob_srob_comm_architect.md` |
| SROB ↔ SOB handoff | `primitives/srob/srob_sob_comm_architect.md` |
| Requirements | `20.40.010`, `20.40.020`, `20.40.030`, `20.40.040` |

---

## **12. Change summary (v1.1)**

| Area | Change |
|------|--------|
| Location | Moved under `design/papers/ts_patha_architecture/` |
| §5 | Full “what SmOB does differently” |
| §7 | Explicit YAML + TP field synchronization inventory for all three edges |
| §8 | Failure modes / wrong fixes |
| Path pointers | Updated for architecture paper home |

---

**End of `sob_to_smob_chain.md` (v1.1)**

---

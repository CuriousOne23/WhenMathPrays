# **SROB ↔ SOB Communication Architecture**
**Document:** `primitives/srob/srob_sob_comm_architect.md`  
**Status:** Design / deliberation (not implementation lock-in)  
**Purpose:** Slow down and make the SOB → SROB handoff explicit before software architecture, YAML bodies, or `srob.py`  
**Aligned with:** 20.40.010 (SOB), 20.40.020 v2.0 (SROB), tp_path_a_map.md  
**Non-goals:** Coding, testbench YAML, final dictionary schemas

---

## **1. Why this document exists**

SROB was about to inherit SOB’s document pattern (`*_software_architecture.md`, `*_py_struc_pgm.md`) and a proposed set of refinement YAMLs. That moved too fast.

Before locking structure, we need a clear answer to:

- What does SOB **owe** SROB on the TP?
- What is SROB **allowed** to do with that?
- What must SROB **never** re-do (because that is SOB’s job)?
- Where are the holes, risks, and open design choices?

This file is the communication contract and design board—not the coding blueprint.

---

## **2. Defined duties of SROB**

### **2.1 Core duty (one sentence)**

SROB **refines and normalizes structural tags and residue already placed on the TP by SOB**, writing only SROB-owned fields, so downstream primitives (CnOB, SmOB, routing, meaning stages) receive bite-sized, rigidly defined structural information.

### **2.2 SROB shall (intent)**

| Duty | Meaning |
|------|--------|
| **Normalize structure** | Canonical lists, tables, code/math block structure, consistent unit types—without changing original text content |
| **Resolve structural ambiguity** | Boundaries, nesting, attachment—deterministic structural rules only |
| **Sharpen existing hints** | Greater detail **inside** operator / domain / tone / constraint **types SOB already used** |
| **Refine structural-importance** | Positional/structural labels only (header-like, anchor-like, subject-like, object-like as cues—not semantic roles) |
| **Normalize discourse flags** | Canonical form for discourse-adjacent flags SOB already propagated |
| **Write owned fields only** | e.g. `srob_structural_map`, `srob_residue`, `srob_audit_record` (+ optional diagnostic-only metadata) |
| **Stay bounded** | High-confidence, deterministic, domain-limited structural / semantic-adjacent work only |

### **2.3 SROB shall not (intent)**

| Prohibition | Reason |
|-------------|--------|
| Re-load SOB lexical dictionaries and re-tag raw text as a second SOB | Ownership leak; hides SOB gaps |
| Invent **new hint types** outside SOB’s field space | 20.40.020; breaks type contract |
| Modify TP text, meaning-layer fields, Context Frame, MSL, identity, freeze, routing_metadata | Writer authority |
| Enforce constraints | CnOB / later stages |
| Resolve referent identity or entity meaning | IdOB / meaning stages |
| Route to semantic OBs directly | Lineup: SROB → CnOB |
| Require other primitives to read diagnostic metadata | HLR-style diagnostic-only |

### **2.4 Downstream purpose**

SOB + SROB (and later CnOB, SmOB) exist to **digest structural and structural-adjacent space into rigid tags** so primary meaning and routing primitives are not overwhelmed. SROB is the second chew—not a second full extraction engine.

---

## **3. Proposed handoff structure (SOB → SROB)**

```
TP text + upstream context (CE/CEx, etc.)
              │
              ▼
            SOB
              │  writes (SOB-owned):
              │    structural.sob_structural_map
              │    structural.sob_residue
              │    metadata.sob_audit_record
              ▼
            SROB   ← reads SOB fields from TP only
              │     (does not load sob_*.yaml)
              │  writes (SROB-owned):
              │    structural.srob_structural_map
              │    structural.srob_residue
              │    metadata.srob_audit_record
              │    (+ optional diagnostic-only metadata)
              ▼
            CnOB → SmOB → … → routing / meaning
```

### **3.1 Sufficiency rule (hard design rule)**

> If SROB cannot perform its duties using **only** what SOB wrote on the TP (plus SROB’s own refinement rules/maps), then **SOB (or SOB requirements/architecture) must be modified**.  
> SROB must not silently re-implement SOB.

### **3.2 What SROB expects to find on the TP (minimum)**

From SOB, SROB should be able to answer:

1. What structural units exist, in order?  
2. What coarse operators / domains / tones / constraints were tagged?  
3. What discourse-adjacent flags exist (if any)?  
4. What structural-importance cues exist (if any)?  
5. Enough audit/provenance that refinement decisions can be traced relative to SOB output  

If any of (1)–(4) is systematically missing when SROB needs it, that is an **SOB gap**.

---

## **4. Proposed SROB support files (names only — not yet locked)**

These are **candidates** for later architecture docs. They are **not** approved implementation until this communication design settles.

| Candidate file | Proposed duty | Primary input | Primary output contribution |
|----------------|---------------|---------------|------------------------------|
| `srob_normalize_rules.yaml` | List/table/code/math/unit canonical form | SOB segments / structure | Refined structure in SROB map |
| `srob_boundary_rules.yaml` | Boundary / nesting disambiguation | SOB segments + optional discourse flags | Disambiguated units |
| `srob_sharpen_maps.yaml` | Coarse → finer tags **within SOB type space** | SOB operators/domains/tones/constraints | Sharpened parallel fields |
| `srob_importance_rules.yaml` | Positional structural-importance labels | SOB structure (+ importance residue if present) | Refined importance metadata |
| `srob_discourse_normalize.yaml` | Canonical discourse flag schema | SOB discourse-adjacent residue | Normalized discourse fragments |

**Optional:** `srob_diagnostic_schema.yaml` — shapes for developer-only playback metadata.

**Thinner alternative (if we collapse):**

1. `srob_normalize_rules.yaml` (include boundary rules)  
2. `srob_sharpen_maps.yaml`  
3. `srob_importance_rules.yaml`  

Discourse normalize folds into (1).

### **4.1 Relation of these files to SOB dictionaries**

| SOB (`sob_*.yaml`) | SROB candidates |
|--------------------|-----------------|
| Lexical extraction vocab (what tags exist and how to spot them in text) | Refinement **policy** (how to normalize/sharpen tags already on the TP) |
| Loaded by SOB every run | Loaded by SROB every run |
| Never loaded by SROB (proposed) | Never replace SOB’s vocab authority |

Sharpen maps may **reference** SOB category names (e.g. `technical_like` → finer subtypes) but do not redefine SOB’s extraction lexicon.

---

## **5. Interplay matrix**

| Concern | SOB | SROB |
|---------|-----|------|
| Tag text from lexicons | Yes | No |
| Own first structural map/residue | Yes | No (reads) |
| Canonical lists/tables/blocks | Coarse OK | Yes |
| Nested/boundary ambiguity | First cut | Yes |
| Invent operator/domain/tone/constraint **types** | Yes (vocab) | **No** |
| Sharpen those tags | No | Yes |
| Structural-importance positional cues | Optional/coarse | Yes (refine) |
| Write meaning / identity / routing | No | No |
| Fix missing tags on TP | **SOB must improve** | Do not re-lex |

---

## **6. Advantages of this split**

1. **Clear writer authority** — SOB and SROB each own fields; no in-place overwrite war.  
2. **Falsifiable handoff** — If SROB is starved, the bug is localized (SOB output or SROB rules), not a blended re-tagger.  
3. **Downstream load reduction** — Coarse then refined tags match the “bite-size the space” goal for CnOB/SmOB/RB.  
4. **Determinism and replay** — Refinement is pure function of TP(SOB) + SROB rules; no second lexical pass over raw text.  
5. **Aligns with 20.40.020 v2.0** — Bounded semantics, no new hint types, owned-field writes, CnOB next.  
6. **Debuggability** — Disagreement between coarse (SOB) and refined (SROB) is visible and informative.  
7. **Slows accidental scope creep** — SROB cannot quietly become “SOB 2 with more dictionaries.”

---

## **7. Disadvantages and costs**

1. **Two structural maps on the TP** — Downstream must know to prefer SROB when present; need an explicit consumer rule (CnOB reads SROB first, falls back to SOB only if SROB absent—policy TBD).  
2. **Duplication of shape** — Refined map may largely mirror SOB map with deltas; need a convention (full refined map vs delta-only). Full map is simpler for consumers; delta is smaller but harder.  
3. **Sharpen vocabulary governance** — Finer subtypes must stay inside agreed type families or the “no new types” rule erodes.  
4. **SOB completeness pressure** — SROB cannot paper over weak SOB extraction; SOB quality becomes a hard dependency.  
5. **Extra stage latency** — Always a second pass even when SOB output is already clean (acceptable for lineup clarity; optional short-circuit later).  
6. **More files to design** — Even a thin YAML set needs careful schemas before coding.

---

## **8. Holes (known unknowns)**

1. **Exact field schemas** for `sob_structural_map` / `sob_residue` vs `srob_*` — not fully frozen beyond current SOB implementation and 20.40.020 outputs list.  
2. **Whether SOB already emits structural-importance** in a form SROB can refine — may be sparse today.  
3. **Discourse flag inventory** — what SOB actually propagates vs what CE/CEx put on TP vs what SROB should normalize.  
4. **Consumer precedence** — Does CnOB **require** SROB, or is SROB optional in progressive lineup toggles? Path map order says SROB is in sequence; test harness may still allow SOB-only.  
5. **Sharpen depth** — How fine is “enough” before SmOB/IdOB? No metric yet.  
6. **Entropy / ambiguity metrics** — 20.40.020 treats reduction as visibility *should*, not hard SHALL; no agreed measure.  
7. **Modality** — Does SROB refine modality, or leave SOB modality untouched? Not explicitly settled.  
8. **Empty / minimal SOB residue** — Behavior when SOB emits almost nothing (valid text, no operators/domains): SROB normalize-only path needs definition.

---

## **9. Concerns**

1. **Semantic creep under “bounded semantics”** — Realizing SROB must “chew” its domain can slide into meaning work that belongs to SmOB/IdOB. Need sharp examples of allowed vs forbidden refinements before coding.  
2. **Double-tagging confusion** — Operators appear on both SOB and SROB maps; routing must not double-count.  
3. **Testing order** — Progressive lineup for SROB needs synthetic TP with **realistic SOB-shaped fields**, not raw text only—or tests will push SROB to re-extract.  
4. **Architecture docs timing** — `srob_software_architecture.md` and `srob_py_struc_pgm.md` should wait until this handoff and the YAML *roles* (not necessarily full contents) are agreed.  
5. **SOB retrofit risk** — Making SROB “TP-sufficient” may force new SOB HLRs or map fields; budget that as explicit work, not surprise.  
6. **Diagnostic metadata** — Useful for development; must stay non-normative for other primitives or it becomes a hidden API.

---

## **10. Design choices still open (decision list)**

| # | Choice | Options (examples) |
|---|--------|---------------------|
| A | YAML pack size | 5 files vs thin 3 |
| B | Refined map style | Full replacement map vs delta + pointer to SOB |
| C | CnOB input rule | SROB required vs SROB preferred |
| D | Modality | SOB-final vs SROB may refine |
| E | Sharpen without SOB tag | Forbidden (default) vs narrow allow list |
| F | Structural-importance origin | SOB always emits coarse cues vs SROB may derive positional cues from structure alone |
| G | Short-circuit | Always run SROB vs skip when SOB signals “already canonical” |

**Default lean (not locked):** A thin 3; full refined map; SROB required in full Path-A sequence; modality SOB-final unless boundary fix requires update; sharpen only when SOB tag present; SROB may derive positional importance from structure alone; always run SROB for lineup clarity.

---

## **11. Recommended next steps (still slow)**

1. Review and mark agreement / disagreement on **duties** (§2) and **sufficiency rule** (§3.1).  
2. Decide open choices A–G (§10), especially B, C, E, F.  
3. Audit current **SOB TP output** against SROB’s minimum expectations (§3.2); list concrete SOB gaps if any.  
4. Only then draft `srob_software_architecture.md` and `srob_py_struc_pgm.md`.  
5. Only then define YAML schemas and `srob.py`.

---

## **12. Summary**

- SROB is a **refinement and normalization** stage over **SOB’s TP tags**, not a second lexical SOB.  
- Handoff is **TP-mediated**; SROB does not load `sob_*.yaml`.  
- Support YAMLs (when built) are **refinement policies**, not extraction lexicons.  
- Advantages favor clarity, authority, and downstream load reduction.  
- Costs include dual maps, governance of sharpen types, and SOB quality pressure.  
- Holes and concerns are listed so they are not solved accidentally in code.

This document is the brake and the map for the next agreement cycle.

---

**End of `srob_sob_comm_architect.md`**

---

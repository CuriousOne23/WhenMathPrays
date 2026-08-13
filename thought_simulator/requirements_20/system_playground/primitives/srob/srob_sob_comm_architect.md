# **SROB ↔ SOB Communication Architecture**
**Document:** `primitives/srob/srob_sob_comm_architect.md`  
**Status:** Design / deliberation (not implementation lock-in)  
**Version:** 1.1  
**Purpose:** Make the SOB → SROB handoff explicit before software architecture, YAML bodies, or `srob.py`  
**Aligned with:** 20.40.010 (SOB), 20.40.020 v2.0 (SROB), tp_path_a_map.md  
**Non-goals:** Coding, testbench YAML, final dictionary schemas

---

## **1. Why this document exists**

SROB was about to inherit SOB’s document pattern (`*_software_architecture.md`, `*_py_struc_pgm.md`) and a proposed set of refinement YAMLs. That moved too fast.

This file is the **communication contract and design board**—not the coding blueprint. It records what is settled and what remains open.

---

## **2. Core invariant: SOB does not surprise SROB**

**Settled.**

SOB does not surprise SROB in two senses:

1. **Units** — Segment kinds and order SROB sees are ones SOB already committed to the TP (sentence, list_item, table structure, etc.). SROB may normalize or disambiguate attachment; it should not meet a structural world SOB never described.

2. **Lexical / hint field space** — Operators, domains, tones, constraints (and discourse-adjacent flags) appear only inside families SOB already used. SROB goes **deeper inside** those families; it is not ambushed by new field types or tags from outside the SOB contract.

If SROB is surprised, that is a **contract failure** (usually SOB under-specified, or SROB overreaching)—not normal operation.

**Picture:** The TP after SOB is a **closed, coarse coordinate system**. SROB only increases resolution inside it.

```
SOB (coarse)                         SROB (higher resolution, same families)
────────────                         ─────────────────────────────────────
operator: explain               →    explain.clarify | explain.detail | …
domain: technical_like          →    technical_like.architecture | …
tone: supportive                →    supportive.polite_request | …
constraint: precision           →    precision.parameter_level | …
```

SOB opens the drawer; SROB organizes what is inside the drawer. It does not build new drawers.

**Knowledge shape:** SOB knowledge is **wide** (lexical coverage of the text surface). SROB knowledge is **deeper** (refinement policy and structural rules)—not a larger second lexicon. If SROB’s files start looking like a second, larger SOB dictionary, that is a design smell.

---

## **3. Defined duties of SROB**

### **3.1 Core duty (one sentence)**

SROB **refines and normalizes structural tags and residue already placed on the TP by SOB**, writing only SROB-owned fields, so downstream primitives receive bite-sized, rigidly defined structural information.

### **3.2 Two work streams**

SROB does two different kinds of work. Both matter; they are not the same.

| Stream | What it is | What it is not |
|--------|------------|----------------|
| **A. Structure normalization** | Canonical shape of units SOB already proposed (lists, tables, blocks, boundaries, nesting) | Re-tagging operator/domain/tone/constraint from raw text |
| **B. Tag sharpening** | Higher-resolution labels **inside** SOB’s existing hint families | New hint **types**; re-lex of the sentence |

---

### **3.3 Stream A — List / table / boundary normalization**

Lexical tagging is straightforward. Structural normalization is about the **shape of units**, not about operator/domain/tone/constraint labels.

**SOB’s first cut** may emit rough segments (by line / `.?!` / simple list markers), rough types (`sentence` vs `list_item`), preserved order, and coarse lexical tags. It need not produce a fully canonical document model.

**SROB’s structural job** answers: *Given the units SOB already named, what is the canonical structural description of this TP?*

| Job | Example problem | What SROB does |
|-----|-----------------|----------------|
| **List normalization** | Mix of `-`, `*`, `1)`, `1.`; unclear depth | One list model: ordered/unordered, depth, parent index, stable item ids |
| **Nesting / attachment** | Is a sub-bullet under Setup or top-level? | Bind child → parent by indentation/numbering rules |
| **Boundary disambiguation** | New sentence vs list continuation vs callout? | Fixed rules → one unit type + attachment |
| **Table normalization** | Pipe rows vs prose; header vs body unclear | header row, body rows, cell list — **content unchanged** |
| **Code/math blocks** | Fences left as plain sentences | Mark as `code_block` / `math_block`; do not edit contents |
| **Unit consistency** | Same role labeled differently across the TP | One canonical type per structural role |

**Tiny before/after (list):**

SOB (coarse):
```text
seg_0 sentence   "Steps:"
seg_1 list_item  "- open file"
seg_2 list_item  "  - check encoding"   # depth only in spaces
seg_3 list_item  "- save"
```

SROB (normalized structure):
```text
seg_0 sentence      "Steps:"
seg_1 list_item     depth=1  parent=null   "open file"
seg_2 list_item     depth=2  parent=seg_1  "check encoding"
seg_3 list_item     depth=1  parent=null   "save"
list_structure: unordered
```

No new operator/domain. **Geometry of the list** is what changed.

**Why SROB, not SOB:** Nested lists, tables, and boundaries are layout/structure rules. Putting all of that into SOB bloats SOB or forces CnOB/SmOB to re-parse text—the failure mode the OB family is meant to prevent.

**No-surprise on structure:** SROB re-describes and binds units SOB already proposed. It does not invent a table from pure prose SOB called a single sentence (unless a later explicit exception is agreed; default **no**).

---

### **3.4 Stream B — Tagged information (operator / domain / tone / constraint)**

#### **SOB — detect and attach (coarse)**

SOB looks at **text** (and may read upstream context read-only) and answers: *Which coarse tags fire, on which units?*

| Tag family | SOB does | SOB does not |
|------------|----------|--------------|
| **Operator** | Spot surface/morph forms; attach to segment | Decide refined subtypes (`explain` vs `explain.clarify`) |
| **Domain** | Spot lexical domain markers; attach coarse domain | Build fine taxonomy under that domain |
| **Tone** | Spot tone markers; attach coarse tone | Deep speech-act interpretation |
| **Constraint** | Spot constraint markers; attach coarse constraint | Enforce constraints or invent new constraint **types** |
| **Modality** | Classify unit (declarative / interrogative / imperative / …) | Reinterpret as user intent/goal |
| **Discourse-adjacent** | Optionally propagate CE/CEx-derived flags as coarse flags | Fully canonicalize discourse schema |
| **Structural-importance** | Optional/coarse cues if easy and high-confidence | Full positional importance model |

**SOB write target:** `sob_structural_map` + `sob_residue` (+ audit).

#### **SROB — sharpen and normalize tags (finer, same families)**

SROB does **not** re-scan the lexicon like SOB. It reads **SOB’s tags on the TP** and answers: *Given these coarse tags (and structure), what is the higher-resolution, canonical tag picture?*

| Tag family | SROB does | SROB does not |
|------------|-----------|---------------|
| **Operator** | If SOB said `explain`, map to finer label in the **explain** family when maps allow | Invent `operator=translate` if SOB never tagged an operator |
| **Domain** | Sharpen inside SOB’s domain family | Open a new domain type outside SOB vocab |
| **Tone** | Sharpen inside SOB’s tone family | New tone axis outside SOB’s set |
| **Constraint** | Sharpen inside SOB’s constraint family; still **no enforcement** | Apply or enforce constraint logic |
| **Modality** | Default lean: leave SOB modality as-is (unless a boundary fix forces a unit change that carries modality) | Intent inference |
| **Discourse flags** | Canonical names/shapes for flags SOB already put on residue | Re-derive discourse from raw text if SOB omitted it |
| **Structural-importance** | Positional labels from structure (+ refine coarse cues if SOB emitted any) | Semantic roles / referent identity |

**SROB write target:** `srob_structural_map` + `srob_residue` (+ audit / optional diagnostic).

#### **Example sentence**

Input: *“Please implement the function with precise parameter checking.”*

| Field | SOB (coarse) | SROB (higher resolution, same space) |
|-------|----------------|--------------------------------------|
| Modality | imperative | imperative (unchanged) |
| Operator | `implement` | `implement` or finer under implement if map defines it |
| Domain | conversational_like, code_like, technical_like | finer **under those only** |
| Tone | supportive, technical | finer under those only |
| Constraint | politeness, precision | finer under those only (e.g. precision.parameter_level) |
| Structure | one sentence segment | same unit; optional positional importance cues |

SROB never adds `domain=legal_like` because SOB missed it. If that domain is needed, **SOB** must tag it (or requirements change).

#### **One-line summary (tags)**

| Stage | Tagged information |
|-------|-------------------|
| **SOB** | **What coarse tags exist** and on which units (from text + dictionaries) |
| **SROB** | **Higher-resolution, canonical form of those same tags** (from TP + refinement maps/rules) |

---

### **3.5 SROB shall / shall not (intent)**

| SROB shall | Meaning |
|------------|--------|
| Normalize structure | Canonical lists, tables, code/math, consistent unit types—without changing original text content |
| Resolve structural ambiguity | Boundaries, nesting, attachment—deterministic structural rules only |
| Sharpen existing hints | Greater detail **inside** operator / domain / tone / constraint **types SOB already used** |
| Refine structural-importance | Positional/structural cues only—not semantic roles |
| Normalize discourse flags | Canonical form for flags SOB already propagated |
| Write owned fields only | `srob_structural_map`, `srob_residue`, `srob_audit_record` (+ optional diagnostic-only) |
| Stay bounded | High-confidence, deterministic, domain-limited structural / semantic-adjacent work only |

| SROB shall not | Reason |
|----------------|--------|
| Re-load SOB lexical dictionaries and re-tag raw text | Ownership leak; hides SOB gaps |
| Invent **new hint types** outside SOB’s field space | 20.40.020; breaks type contract |
| Modify TP text, meaning-layer, Context Frame, MSL, identity, freeze, routing_metadata | Writer authority |
| Enforce constraints | CnOB / later stages |
| Resolve referent identity or entity meaning | IdOB / meaning stages |
| Route directly into semantic OBs | Lineup: SROB → CnOB |
| Require other primitives to read diagnostic metadata | Diagnostic-only |

---

## **4. Handoff structure and sufficiency**

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

### **4.1 Sufficiency rule (hard design rule)**

> If SROB cannot perform its duties using **only** what SOB wrote on the TP (plus SROB’s own refinement rules/maps), then **SOB (or SOB requirements/architecture) must be modified**.  
> SROB must not silently re-implement SOB.

### **4.2 Minimum SROB expects on the TP after SOB**

1. What structural units exist, in order?  
2. What coarse operators / domains / tones / constraints were tagged?  
3. What discourse-adjacent flags exist (if any)?  
4. What structural-importance cues exist (if any)?  
5. Enough audit/provenance that refinement decisions can be traced relative to SOB output  

If any of (1)–(4) is systematically missing when SROB needs it, that is an **SOB gap**.

---

## **5. Downstream value — is this work meaningful?**

**Yes — if kept inside the contract.** Meaningful as **prep**, not as “almost meaning.”

| Downstream | Structure work | Sharper tags | Why it helps |
|------------|----------------|--------------|--------------|
| **CnOB** | **Primary** | **Primary** (constraint family) | Canonical layout + sharper constraint hints without re-parsing text |
| **SmOB** | Strong | Strong (domain/operator/tone) | Stable units + finer cues; less re-segmentation |
| **ISc** | Moderate | Moderate | Scoring on consistent structure and clearer residue |
| **SSG / STPX** | Moderate | Moderate | Cues sit on better-indexed structure/tags |
| **TR / DCB / RBU** | Moderate | Moderate | More stable routing features turn-to-turn |
| **RB** | Strong (indirect) | Strong (indirect) | Better residue/structure **axis quality**; not RB’s policy itself |
| **IdOB** | Moderate | Light–moderate | Better boundaries/cues for binding; IdOB still owns referents/identity |
| **OuBA** | Indirect | Indirect | Cleaner upstream inputs to commit path |

**Not a substitute for:** CnOB constraint logic, SmOB semantic-adjacent work, RB decisions, IdOB identity/meaning.

**When it would not be meaningful:** SROB only copies SOB; sharpen maps become pseudo-semantics; downstream never prefers SROB fields when present.

**Bottom line:** Structure normalization + tag sharpening mainly serve **CnOB**, then **SmOB**, then **scoring/routing**. Same goal: make later jobs smaller and more reliable on a rigid base.

---

## **6. Candidate SROB support files (names only — not locked)**

These are **refinement policies**, not extraction lexicons. SROB does not load `sob_*.yaml`.

| Candidate file | Proposed duty |
|----------------|---------------|
| `srob_normalize_rules.yaml` | List/table/code/math/unit canonical form |
| `srob_boundary_rules.yaml` | Boundary / nesting disambiguation |
| `srob_sharpen_maps.yaml` | Coarse → finer tags **within SOB type space** |
| `srob_importance_rules.yaml` | Positional structural-importance labels |
| `srob_discourse_normalize.yaml` | Canonical discourse flag schema |

**Optional:** `srob_diagnostic_schema.yaml` for developer-only playback.

**Thinner alternative:** (1) normalize+boundary, (2) sharpen maps, (3) importance; discourse folds into (1).

| SOB (`sob_*.yaml`) | SROB candidates |
|--------------------|-----------------|
| Lexical extraction vocab | Refinement **policy** |
| Loaded by SOB | Loaded by SROB |
| Never loaded by SROB | Never replace SOB vocab authority |

---

## **7. Interplay matrix**

| Concern | SOB | SROB |
|---------|-----|------|
| Tag text from lexicons | Yes | No |
| Own first structural map/residue | Yes | No (reads) |
| Canonical lists/tables/blocks | Coarse OK | Yes |
| Nested/boundary ambiguity | First cut | Yes |
| Invent operator/domain/tone/constraint **types** | Yes (vocab) | **No** |
| Sharpen those tags | No | Yes |
| Structural-importance positional cues | Optional/coarse | Yes (refine / derive from structure) |
| Write meaning / identity / routing | No | No |
| Fix missing tags on TP | **SOB must improve** | Do not re-lex |

---

## **8. Advantages**

1. Clear writer authority (owned fields only).  
2. Falsifiable handoff (starved SROB → SOB gap or SROB rules).  
3. Downstream load reduction (coarse then refined).  
4. Determinism: pure function of TP(SOB) + SROB rules.  
5. Aligns with 20.40.020 v2.0.  
6. Coarse vs refined disagreement is visible and useful.  
7. Blocks SROB from becoming “SOB 2 with more dictionaries.”

---

## **9. Disadvantages and costs**

1. Two structural maps — need explicit consumer precedence.  
2. Full refined map vs delta — design choice still open.  
3. Sharpen subtype governance must not invent new types.  
4. SOB quality becomes a hard dependency.  
5. Always-on second stage (unless short-circuit later).  
6. Refinement YAML schemas still to design.

---

## **10. Holes (known unknowns)**

1. Exact field schemas for `sob_*` vs `srob_*`.  
2. How much structural-importance SOB emits today.  
3. Discourse flag inventory (SOB vs CE/CEx vs SROB normalize).  
4. CnOB: SROB required vs preferred in progressive lineup.  
5. How fine “enough” sharpen depth is.  
6. Entropy/ambiguity visibility metrics (should, not SHALL).  
7. Modality: SOB-final vs refine-with-boundary (lean: SOB-final).  
8. Normalize-only path when SOB residue is nearly empty.

---

## **11. Concerns**

1. Semantic creep under bounded semantics.  
2. Double-counting coarse + refined tags in routing.  
3. SROB tests must use **SOB-shaped TP inputs**, not raw text only.  
4. Architecture docs (`srob_software_architecture.md`, `srob_py_struc_pgm.md`) wait until this contract is agreed.  
5. SOB retrofit if TP is not sufficient.  
6. Diagnostic metadata must not become a hidden API for other primitives.

---

## **12. Design choices still open**

| # | Choice | Options | Lean (not locked) |
|---|--------|---------|-------------------|
| A | YAML pack size | 5 files vs thin 3 | Thin 3 |
| B | Refined map style | Full map vs delta | Full map |
| C | CnOB input rule | Required vs preferred | Required in full Path-A sequence |
| D | Modality | SOB-final vs SROB refine | SOB-final unless boundary forces unit change |
| E | Sharpen without SOB tag | Forbidden vs allow list | **Forbidden** |
| F | Importance origin | SOB only vs SROB from structure | SROB may derive positional cues from structure alone |
| G | Short-circuit | Always run vs skip | Always run (lineup clarity) |

---

## **13. What is settled vs still open**

**Settled (v1.1):**

- No-surprise invariant (units + field space)  
- Sufficiency rule (TP-only for SOB outputs; no `sob_*.yaml` in SROB)  
- Coarse SOB → finer SROB **within same families**  
- Two streams: structure normalization ≠ tag sharpening  
- SROB knowledge is deeper policy, not wider lexicon  
- Downstream value ranking (CnOB, SmOB, then scoring/routing)  
- Owned-field writes; no constraint enforcement; no semantic OB direct route  

**Still open:** A–G above; exact schemas; SOB gap audit against live SOB output.

---

## **14. Recommended next steps (still slow)**

1. Confirm agreement on settled items (§13).  
2. Decide A–G as needed (especially B, C, E, F).  
3. Audit current SOB TP output against §4.2; list concrete SOB gaps.  
4. Only then draft `srob_software_architecture.md` and `srob_py_struc_pgm.md`.  
5. Only then YAML schemas and `srob.py`.

---

## **15. Summary**

- SROB is **refinement and normalization** over SOB’s TP tags—not a second lexical SOB.  
- **SOB does not surprise SROB** in units or in lexical field space.  
- **Structure stream:** canonical lists/tables/boundaries/nesting.  
- **Tag stream:** higher resolution inside SOB’s operator/domain/tone/constraint families.  
- Handoff is **TP-mediated**; support files are **refinement policies**.  
- Work is **meaningful** mainly for CnOB and SmOB, then scoring/routing—as prep, not as meaning.  
- Open choices and holes remain listed so they are not solved accidentally in code.

---

**End of `srob_sob_comm_architect.md` (v1.1)**

---

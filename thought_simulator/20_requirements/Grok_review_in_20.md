# Grok commentary on updated process + Stage 1.5 (opinion only)

Commentary only — no edits, diffs, or insertions. This responds to the revised proposal including the global naming pass across all file types (including CI files, CI-referenced files, and CI tables).

---

## 1. Is the staged process correct?

**Yes — with Stage 0 added and Stage 1.5 scoped tightly.**

The five-stage arc (naming → global apply → B rough drafts → selective A reposition → approval) is a reasonable control model for a multi-day refactor. **20.500** as coordination hub with dates, dependencies, and approval status is appropriate.

**Add Stage 0 before Stage 1:**

| Stage 0 | Content |
|---------|---------|
| **Phase 0 invariants** | Seven bullets all three sign: TP/MTP roles, one B pass per MTP, no lanes in B, meaning replay vs B regeneration, seed scope, XP one-per-commit |

Naming and mechanical renames should not run until those invariants are recorded in 20.500.

**Clarify 20.500 authority:** Source of truth for the **refactor program** — not for TS runtime semantics. Normative law remains 20.12 and approved module HLRs.

---

## 2. Is the ordering correct?

**Mostly — Stage 1.5 is the main ordering risk.**

| Stage | Verdict |
|-------|---------|
| **1 — Naming resolution** | Correct first step (with 1a blocking / 1b deferred split) |
| **1.5 — Global naming apply** | **Conditionally correct** — see §3 below |
| **2 — B rough drafts** | Correct; refine **internal order** (20.206 → 20.205 → 20.115 rough → 20.207 → 20.55/56 → 20.57 → 20.41–43 → 20.58) |
| **3 — A reposition (comment-only)** | Correct for **20.10 / 20.30 only**; not uniform for CP-approved docs |
| **4 — Approval** | Correct |

**Gap:** **20.115 MTP** is still absent from Stage 2. Add it — MTP is the B input boundary; XP and 20.206 depend on it.

**Gap:** **Stage 4.5 / final step** — repo-wide consistency grep (`lane_id` in B, `per TP` + Pipeline B, TP-B) before closing 20.500.

---

## 3. Is Stage 1.5 (global naming across all file types, including CI) required?

**Partially required — not as a single unconstrained repo-wide pass.**

### What is right about Stage 1.5

Naming is architectural. If glossary says **XP** but JSON schemas, Python harnesses, CI validation tables, routing table fixtures, and trace exemplars still say old identifiers, traceability and replay harnesses **will** fracture. Something like Stage 1.5 is necessary **eventually**.

Including **CI files, CI-referenced files, CI tables, schemas, configs, tests, and examples** in scope is correct **in principle** — anything that participates in validation or golden fixtures must align with the naming registry.

### What is risky about Stage 1.5 as proposed

| Risk | Why |
|------|-----|
| **Premature mechanical rename** | Stage 1 resolves *terms*; XP/MTP handoff field names may still move when 20.206/20.115 are drafted → **second rename pass** |
| **HLR / requirement IDs** | `HLR-20.105-046` etc. should not change in a mechanical pass — breaks traceability |
| **CP-approved modules** | 20.105 v0.4 — field renames need explicit re-review, not bulk replace |
| **“No semantic changes”** | Hard to guarantee across `.py` + tests + JSON — easy to break CI without meaning to |
| **Blast radius** | Full-repo pass before B topology docs exist may encode wrong assumptions (e.g. per-TP exec artifacts) |

### Recommended refinement (for 20.500 to record)

Split Stage 1.5 into two sub-stages:

**Stage 1.5a — Naming registry (no mass edit)**  
- Single table in 20.500: `canonical_name | aliases | deprecated | scope | owner`  
- Covers OpBeh/OBG/XlateR, XP, TrigRB, IMR Type B, CI table columns, fixture keys  
- Includes **CI pipeline configs** and **every file CI reads** (manifest list in 20.500)

**Stage 1.5b — Mechanical apply (allowlist only)**  
- Only files on an **explicit allowlist** approved by all three  
- Categories: glossary, non-normative examples, harness labels, CI table headers — **not** bootstrap HLR text or CP-approved normative modules until Stage 4 per doc  
- Each change: PR-sized batch, CI green, logged in 20.500 with date + file list  
- Rule: **identifier renames in requirements MDs happen per document in Stage 4**, not bulk Stage 1.5

**Verdict on your question:**  
- **Is a global naming alignment pass required?** **Yes**, for CI-referenced artifacts and schemas.  
- **Must it be one unconstrained pre-Stage-2 pass across everything?** **No** — that ordering is likely to cause rework and accidental semantic drift.  
- **Better:** Registry in Stage 1 → **targeted** 1.5b on CI/schemas/harnesses → full normative renames during Stage 4 approvals.

### CI scope clarification for 20.500

Record explicitly what **“CI”** means in the inventory:

- Continuous integration configs (workflows, validation scripts)  
- **CI reference files** (golden fixtures, schema registries, routing table seeds)  
- **CI tables** (column names, enum dictionaries used by validators)  
- If **CIL** (Conversation Input Layer, 20.33) is in scope, list it separately — different subsystem, same naming pass rules

---

## 4. Are responsibilities correctly assigned?

**Mostly yes — add constraints on who runs Stage 1.5b.**

| Role | Assessment |
|------|------------|
| **Grok — Stage 2 B drafts** | Appropriate |
| **Grok — Stage 1.5b mechanical pass** | OK **only** with allowlist + Jeff/Copilot review of batch before merge |
| **All three — Stage 1 naming** | Correct |
| **All three — Stage 4 approval** | Correct |

**Jeff/Copilot** should own **CI manifest** (complete list of CI-referenced paths) before 1.5b starts — Grok should not guess which tables CI consumes.

---

## 5. Is the document inventory complete?

**Extend 20.500 §C with:**

**Stage 2 drafts:** add **20.115 MTP** (rough).

**Stage 1.5 scope inventory (new section):**

- All CI workflow / validation entrypoints  
- Schema JSON / wire maps (`wire_map_version` alignment)  
- 30-series verification / 40-series playground fixtures  
- 20.200 traceability matrix  
- 20.190 glossary (may be first 1.5b target)  
- Existing **20.110 OuB**, **20.45 IMR**, **20.33 CIL** — harden vs create for 20.58  

**Re-review queue (Stage 4, minimal touch):** 20.105, 20.106, 20.140, 20.36, 20.37, 20.40, 20.50, 20.60

**Explicit no-touch / annex-only:** 20.12 (unless three-way approves annex)

---

## 6. Are “comment-only updates” to existing docs the right approach?

**Yes for 20.10 and 20.30 — not for the full Stage 3 list.**

| Doc | Stage 3 approach |
|-----|------------------|
| **20.10, 20.30** | Reposition under Pipeline A + dual-pipeline placeholders — **good** |
| **20.115** | Needs Stage 2 rough + Stage 4 substance — **not** comment-only |
| **20.105** (CP-approved) | **Defer** Stage 3; Stage 4 boundary sentence only if CP approves bump |
| **20.36** | Prefer 20.500 assertion checklist over many inline TODOs |

**Do not run Stage 1.5b on CP-approved modules** at the same time as Stage 3 comments — two parallel mutation streams will desync 20.500.

---

## 7. Risks and missing steps

| Risk | Mitigation |
|------|------------|
| 1.5 breaks CI while “no semantic changes” claimed | Allowlist batches; CI must pass per batch |
| Rename before XP/MTP fields finalized | Registry now; mechanical apply on stable subsets only |
| 20.500 status drift | Mandatory columns: `stage`, `date`, `approver`, `blocked_by` |
| Namespace collision OB vs OpBeh | Stage 1 blocking set; glossary entry with “never alias” rule |
| Per-TP B reintroduced in renamed fixtures | Stage 0 invariant + 1.5b review checklist |
| Multi-day parallel edits | **Freeze** rows in 20.500 while in CP review |

**Missing steps:**

1. **Stage 0** invariant sign-off  
2. **CI manifest** before 1.5b  
3. **20.115** in Stage 2  
4. **Naming registry** (1.5a) before mechanical apply (1.5b)  
5. **Final consistency grep** before closing 20.500  

---

## 8. Direct answers to your seven questions

1. **Staged process correct?** **Yes**, with Stage 0 + split 1.5a/1.5b + 20.115 in Stage 2 + final grep.  
2. **Ordering correct?** **Mostly** — global mechanical pass **after registry**, not necessarily **before** all Stage 2 drafts; CI/schemas can lead; normative MDs trail Stage 4.  
3. **Global naming pass required (incl. CI)?** **Yes in substance**; **no** as one unconstrained pre-Stage-2 repo sweep.  
4. **Responsibilities correct?** **Yes**, with allowlist governance on 1.5b and Jeff/Copilot owning CI manifest.  
5. **Inventory complete?** **Not yet** — add 20.115, CI manifest section, 12/31/38/39/45/190/200, re-review queue.  
6. **Comment-only updates right?** **For 20.10/20.30 yes**; narrow Stage 3 elsewhere.  
7. **Risks/missing steps?** See §7; biggest risk is **Stage 1.5 scope creep before architecture docs stabilize**.

---

## 9. Recommendation

**Agree to create 20.500** with the staged process **as amended:**

```
Stage 0  → Invariants (signed)
Stage 1  → Naming resolution (blocking vs deferred)
Stage 1.5a → Naming registry in 20.500
Stage 1.5b → Mechanical apply (CI/schemas/harness allowlist only; CI green per batch)
Stage 2  → B + 20.115 rough drafts (ordered: 206 → 205 → 115 → …)
Stage 3  → Selective A reposition (20.10, 20.30 primarily)
Stage 4  → Per-doc approval + normative renames + light re-review queue
Stage 5  → Consistency grep + close 20.500
```

**Commentary only — ready for three-way alignment on whether to draft the 20.500 skeleton with this amended stage list.**
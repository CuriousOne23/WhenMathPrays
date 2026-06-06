# Grok commentary on the staged process + 20.500 (opinion only)

Commentary only — no edits, diffs, or insertions. This responds to the four-stage proposal and 20.500 as controlling document.

---

## 1. Is the staged process correct?

**Yes in spirit — with three structural additions and two guardrails.**

The four-stage shape (naming → new B docs → reposition A docs → iterative approval) is disciplined and appropriate for a multi-day, cross-cutting refactor. Tracking dates, approval status, dependencies, and open questions in **20.500** is the right coordination mechanism.

**Additions I recommend baking into 20.500:**

| Addition | Where | Why |
|----------|--------|-----|
| **Stage 0 — Phase 0 invariants** | Before Stage 1 (or §A of 20.500) | Seven signed bullets: TP/MTP/XP roles, one B pass per MTP, meaning vs full-trace replay, seed scope. Naming alone is not enough architecture lock. |
| **Dependency graph** | 20.500 §C | Prevents drafting 20.41–58 before XP/sync/MTP handoff concepts exist even in rough form. |
| **Re-review queue** | 20.500 §B or §E | CP-approved modules (20.105, 20.106, 20.140, etc.) tracked for second-pass boundary check, not ad hoc edits. |

**Guardrails:**

1. **20.500 is source of truth for the *refactor program***, not for TS runtime semantics. Normative authority stays in 20.12 and module requirements. State that explicitly in 20.500 purpose to avoid future confusion.

2. **Bootstrap documents (20.10, 20.12, 20.20, 20.30)** need an **additive-only rule** in 20.500: no HLR renumbering or weakening without explicit three-way approval and downstream re-review list.

---

## 2. Is the ordering correct?

**Mostly — I would refine within stages, not replace the stage model.**

### Stage 1 (Naming) — **approve, with scope discipline**

Naming-first is correct for OpBeh/OBG/XlateR vs OB/TR/RB, TrigRB, XP, IMR Type B, epoch/routing table terms.

**Do not let Stage 1 block all progress indefinitely.** Split naming into:

- **Stage 1a — Blocking names** (must resolve before B rough drafts): XP, MTP commit marker (`mtp_snapshot_id` vs `commit_id`), Pipeline A/B, envelope names, namespace for TrigRB vs TR  
- **Stage 1b — Deferred names** (can resolve during Stage 2/4): fine-grained trigger IDs, table column names, etc.

20.500 should record both buckets with dates.

### Stage 2 (New B docs — Grok rough drafts) — **approve, with internal order**

Drafting unapproved placeholders before integration is sound. **Internal order within Stage 2 matters:**

| Priority | Draft first | Reason |
|----------|-------------|--------|
| 1 | **20.206** (A↔B sync) | Smallest; locks handoff predicate |
| 2 | **20.205** (XP) | Topology: one XP per MTP commit; no lanes |
| 3 | **20.207** (execution replay) | Stub acceptable; references 20.12-011/012 precision |
| 4 | **20.55 + 20.56** (SRP + routing table) | Epoch coherence depends on table shape |
| 5 | **20.57** (semantic triggers / TrigRB) | Reads committed `semantic_core` only |
| 6 | **20.41–43** (OpBeh/OBG/XlateR) | Table-driven realization |
| 7 | **20.58** (OuB ↔ manifold) | Expression layer last in B chain |

**Also include in Stage 2 (not only Stage 3):** **20.115 MTP rough draft** — it is the B input boundary, not optional. Without a rough 20.115, XP and 20.206 float without a defined commit object.

### Stage 3 (Existing docs — comment-only reposition) — **approve selectively**

Right approach for **20.10** and **20.20** (if touched) and **20.30**: regroup under Pipeline A, insert dual-pipeline placeholders, preserve all A semantics.

**Defer or minimize Stage 3 for:**

| Doc | Reason |
|-----|--------|
| **20.105** (v0.4 CP-approved) | Placeholder comments add noise; Stage 4 light cross-refs only |
| **20.106, 20.140, 20.37, 20.50, 20.60** | Same — re-review queue in Stage 4, not placeholder surgery |
| **20.12** | Annex/gloss only, or zero touch — track decision in 20.500 |

**20.115** needs more than comment placeholders in Stage 3 — it needs **substantive hardening in Stage 4**, possibly starting from a Stage 2 rough draft.

### Stage 4 (Iterative approval) — **strongly approve**

Date-stamped approval per document in 20.500 is exactly what prevents drift over several days. Include **approval role** (Jeff / Copilot / Grok consensus vs two-of-three for placeholders).

---

## 3. Are responsibilities correctly assigned?

**Mostly yes — one gap and one risk.**

| Assignment | Verdict |
|------------|---------|
| **Grok drafts Stage 2 B cluster (unapproved)** | Appropriate — Grok has context from hardened A modules |
| **Stage 3 limited reposition on existing docs** | Appropriate for 20.10/20.30; **not** for all listed docs equally |
| **All three approve in Stage 4** | Correct for normative requirements |
| **20.500 tracks dates/status** | Correct |

**Gap:** **20.115 MTP** is not in Stage 2 draft list but is **tier-1** for B topology. Assign it explicitly: Grok rough draft in Stage 2 (or parallel with 20.206), full hardening in Stage 4.

**Risk:** Stage 3 “comment-only” on **20.36** — acceptable if comments are **fixture taxonomy placeholders** (MTP-scoped B, no `lane_id`), not scattered TODOs. Prefer a short **20.500 checklist** of 20.36 assertions to add in Stage 4 rather than many inline comments in Stage 3.

**Copilot/Jeff role:** Stage 1 naming and Stage 4 approval are collaborative; 20.500 should record **decision owner** per row (who proposed, who approved).

---

## 4. Is the document inventory complete?

**Core list is good — extend 20.500 §C with:**

### Add to “existing — update or re-review”

- 20.12 (annex/gloss or explicit no-touch)  
- 20.31 (`mtp_update` freeze)  
- 20.38 / 20.39 (read boundaries, snapshot types)  
- 20.45 (IMR Type B → next A cycle)  
- 20.110 or existing OuB doc (**harden vs 20.58 create**)  
- 20.190 glossary  
- 20.200 traceability  
- `README.md` (20_requirements)  
- 40-series harness guide (non-20, in scope)

### Add to “Stage 2 drafts”

- **20.115 MTP Requirements** (rough draft)

### Add to “re-review queue (Stage 4, light touch)”

- 20.105, 20.106, 20.140, 20.36, 20.37, 20.40, 20.50, 20.60

### Add to 20.500 metadata columns

- `depends_on`  
- `blocks`  
- `approval_date`  
- `version_target`  
- `second_pass_required` (Y/N)

---

## 5. Is “comment-only updates” to existing docs the right approach?

**Yes for 20.10 and 20.30 — no for the full list uniformly.**

**Works well when:**

- Document is bootstrap or topology-heavy (20.10, 20.30)  
- Goal is **re-shelving** Pipeline A content under clear headings  
- Placeholders mark **where** B principles will land, not **what** B semantics are  

**Poor fit when:**

- Document is **recently CP-approved** with tight HLRs (20.105) — inline “B goes here” comments confuse implementers  
- Document needs **substantive new sections** (20.115) — comments are insufficient; need real draft in Stage 2/4  
- Document is **invariant registry** (20.12) — prefer annex or 20.500-tracked “no change” decision  

**Alternative for CP-approved modules:** Stage 3 = **no file change**; Stage 4 = **targeted boundary paragraph** only if CP approves version bump. 20.500 tracks “deferred — re-review only.”

---

## 6. Risks and missing steps

| Risk | Mitigation (record in 20.500 §F) |
|------|--------------------------------|
| Naming stage blocks progress | 1a blocking / 1b deferred split |
| B rough drafts embed per-TP B | 20.206 + 20.205 drafted before 20.41–58; XP invariant in Stage 0 |
| Stage 3 distorts signed modules | Re-review queue; minimal touch on 20.105+ |
| XP collapses exec_plan/exec_trace | 20.205 draft must state wrapper model vs 20.12 |
| Duplicate OuB/IMR specs | Harden-vs-create column before 20.58 |
| Equivalence class ambiguity | Phase 0: meaning strip vs full-trace regenerate |
| Multi-day desync | Status board + approval dates mandatory |
| 20.500 becomes normative by accident | Header: `status: coordination` only |

**Missing step:** **Stage 4.5 or final sub-step — consistency grep** (repo-wide: `per TP` + Pipeline B, `lane_id` in exec fixtures, TP-B) before closing 20.500.

**Missing step:** **Freeze window** — while a module is in CP review, 20.500 marks it locked; no parallel Stage 3 edits.

---

## 7. Direct answers to your six questions

1. **Staged process correct?** **Yes**, with Stage 0 invariants + dependency graph + re-review queue.  
2. **Ordering correct?** **Yes at stage level**; refine Stage 2 internal order; add 20.115 to Stage 2; narrow Stage 3 doc list.  
3. **Responsibilities correct?** **Yes**; explicitly assign 20.115; limit Stage 3 on CP-approved docs.  
4. **Inventory complete?** **Not yet** — add 20.115, 12/31/38/39/45/190/200, harness, harden-vs-create.  
5. **Comment-only updates right?** **For 20.10/20.30 yes**; **not uniform** across 20.105/115/36.  
6. **Risks/missing steps?** See §6 above; add consistency grep and freeze windows.

---

## 8. Recommendation on 20.500 itself

**Agree to create 20.500** as the controlling refactor document with:

- Stages 0–4 (0 = invariants, 1 = naming, 2 = rough drafts, 3 = selective A reposition, 4 = approval)  
- Per-document status table with dates  
- Re-review queue for signed A modules  
- Non-negotiable invariants block (no per-TP B, one XP per MTP commit)  
- Explicit statement: 20.500 does not override 20.12 or approved HLRs  

**First artifact after three-way OK on this commentary:** 20.500 **skeleton only** (sections A–H empty tables) — still no normative module edits until Stage 0 is signed.

**Commentary only — ready for alignment on whether to draft the 20.500 skeleton next.**
# Grok commentary on 20.500 (opinion only — no edits)

This is commentary only in response to the 20.500 proposal. No document changes are proposed below.

---

## 1. Is the structure and purpose of 20.500 correct?

**Yes — with one classification caveat.**

A **master coordination plan** is the right artifact for a multi-day, cross-cutting dual-pipeline refactor. The problem you describe is real: vocabulary, sequencing, dependencies, re-review of recently signed modules, and open questions will not stay in sync across three reviewers without a single hub.

**What 20.500 should be:**

| Attribute | Recommendation |
|-----------|----------------|
| **Role** | Coordination / program plan — not normative requirements |
| **Status** | `planning` or `coordination` (not `requirements` / `source_of_truth`) |
| **Authority** | Tracks decisions and order; does **not** override 20.12 or signed module HLRs |
| **Lifecycle** | Living doc during refactor; archive or fold into README/traceability when done |

That avoids 20.500 competing with 20.10/20.12 as architecture law while still being the **operational source of truth for the refactor program**.

**Proposed sections A–F are sound.** I would add two lightweight sections:

- **G. Phase 0 invariants** — the 7 bullets all three sign before any normative MD work (can live in §A or standalone)
- **H. Status board** — per-document: `not started | drafting | CP review | approved | blocked | deferred` with version target

Otherwise the structure matches what this refactor needs.

---

## 2. Is the proposed ordering correct?

**Directionally yes; sequencing needs two adjustments.**

Your order:

1. 20.10 refactor  
2. Create B docs (XP, sync, replay, 20.41–58)  
3. Update 20.30, 20.105, 20.115, 20.36  
4. Consistency pass  

**What works:** Principles/vocabulary before submodule sprawl; consistency pass last.

**Adjustment 1 — Insert Phase 0 before Step 1**  
20.500 §A should embed or reference signed invariants before anyone edits 20.10.

**Adjustment 2 — Elevate 20.115 before 20.41–58**  
MTP is the B input boundary. XP (20.205) and 20.206 need a defined commit object (`mtp_snapshot_id`, hash, freeze semantics). 20.115 should be **tier-1**, not bundled only with “minor” updates in step 3.

**Recommended sequencing for 20.500 §D:**

| Step | Work |
|------|------|
| **0** | Phase 0 one-pager — all three sign |
| **1** | 20.10 dual-pipeline principles expansion (**additive**, not destructive) |
| **2** | **20.115 MTP hardening** |
| **3** | 20.206 A↔B synchronization contract |
| **4** | 20.205 XP requirements |
| **5** | 20.41–58 execution-manifold cluster (parent topology before deep submodule detail) |
| **6** | 20.207 execution replay (or 20.36 Class 6 stub first) |
| **7** | 20.30 + 20.36 clarifications |
| **8** | 20.105 light cross-refs (re-review, not rewrite) |
| **9** | Full 20-series consistency grep + glossary |

**Note on 20.10:** Call it **“dual-pipeline principles expansion”** in 20.500, not “major refactor,” unless you explicitly track HLR renumbering risk and downstream re-review of signed modules.

---

## 3. Is the document inventory complete?

**Good core list — several gaps to add to §C.**

### Missing from “existing documents to update”

| Doc | Why include |
|-----|-------------|
| **20.12** | Annex/gloss for “B derived, A authoritative” — avoid silent bootstrap edits |
| **20.31** | `mtp_update` = B input freeze; `semantic_core` authority |
| **20.38** | Implementation read guards: B must not index by `tp_id` |
| **20.39** | `SemanticCoreSnapshot` vs `TpLaneView` vs XP/exec envelopes |
| **20.45 (IMR)** | Type B triggers → next A cycle; not per-TP B |
| **20.190 glossary** | XP, MTP commit, meaning vs full-trace replay |
| **20.200 traceability matrix** | New doc IDs and dependencies |
| **README (20_requirements)** | Index 20.500 and new cluster |

### Missing from “re-review after B formalized”

Recently CP-approved modules that need **second-pass boundary check**, not necessarily rewrite:

- **20.105** (v0.4) — B never consumes TP  
- **20.106, 20.140, 20.37, 20.50, 20.60** — confirm no implied per-TP B  
- **20.36** (v0.3) — MTP-scoped B fixtures  

20.500 §B should have an explicit **“re-review queue”** so second-pass work is tracked, not accidental.

### Missing from “new documents to create”

| Candidate | Purpose |
|-----------|---------|
| **20.12 annex or 20.500 §A only** | If you want zero bootstrap touch, keep replay precision in Phase 0 + 20.206 |
| **40-series harness guide** (non-20) | Negative tests: no `lane_id` in XP/B fixtures |

### Overlap check before creating 20.41–58

Inventory should note **harden vs create**:

- **20.110 OuB** (if present) vs **20.58 OuB ↔ Execution Manifold**  
- **20.45 IMR** vs trigger content in 20.57/20.58  
- **20.35 reference algorithms** — B pseudocode alignment  

20.500 §C should list **“existing doc may subsume planned ID”** to prevent duplicate specs.

---

## 4. Do XP + sync + replay fit with the execution-manifold cluster?

**Yes — with a clear hierarchy.**

```
20.10 (principles)
    ↓
20.115 (MTP commit boundary)
    ↓
20.206 (when/how A hands off to B)
    ↓
20.205 (XP topology — one per MTP commit)
    ↓
20.41–58 (submodule semantics: OpBeh, OBG, XlateR, SRP, TrigRB, OuB)
    ↓
20.207 (B replay rules)
```

**Roles:**

| Doc | Owns |
|-----|------|
| **20.205 XP** | Cycle-scoped B carrier; one-per-MTP; envelope aggregation; audit; **no lanes** |
| **20.206** | Handoff, immutability, equivalence-class wording, IMR queue boundary |
| **20.207** | Regeneration semantics, golden B trace, seed/epoch scope |
| **20.41–58** | How each subsystem writes into XP/`exec_plan`/`exec_trace` |

**Fit constraint:** 20.205 must state **single B pass per MTP** so 20.41–58 cannot reintroduce per-TP or per-lane B. 20.500 should record that as a **non-negotiable invariant** in §A or §F.

**Envelope note for 20.500:** XP is a logical packet over existing `exec_plan` + `exec_trace` (per 20.12), not a replacement meaning envelope.

---

## 5. Missing components and risks for §F

### Missing components

1. **Phase 0 signed invariant block** (prerequisite gate)  
2. **20.115 as tier-1**, not step-3 afterthought  
3. **Re-review queue** for CP-approved 20.105/106/140/etc.  
4. **Harden-vs-create map** for OuB/IMR/SRP before 20.41–58  
5. **Harness / 40-series** conformance rules in scope  
6. **Canonical commit marker** (`mtp_snapshot_id` vs `commit_id`) — resolve in 20.206 early  

### Risks to track in §F

| Risk | Mitigation in 20.500 |
|------|----------------------|
| Bootstrap churn (20.10/12/30) | Additive-only rule; explicit approval gate |
| Signed module drift | Re-review queue with version targets |
| XP collapses 20.12 envelopes | XP = logical wrapper; exec_plan/trace stay separate |
| Duplicate OuB/IMR specs | Inventory overlap column |
| “Equivalence class” ambiguity | Phase 0: meaning (strip) vs full-trace (regenerate) |
| Namespace collision OB/TR vs OpBeh/OBG | Cross-ref 20.12-015; glossary |
| Per-TP B creeping back in harnesses | Negative fixture rules in scope |
| Multi-day desync | §E approval workflow + §H status board |

---

## 6. Direct answers to your four questions

1. **Is 20.500 structure/purpose correct?** **Yes** — as a **coordination plan**, not normative requirements. Add Phase 0 + status board.  
2. **Is proposed ordering correct?** **Mostly** — insert Phase 0; move **20.115 before 20.41–58**; treat 20.10 as additive principles expansion.  
3. **Is inventory complete?** **Not yet** — add 20.12/31/38/39/45/190/200, re-review queue, harden-vs-create, harness scope.  
4. **Do XP + sync + replay fit the cluster?** **Yes** — 20.205/206 parent topology; 20.41–58 children; 20.207 after XP exists.

---

## 7. Recommendation on next step (still no MD edits)

**Agree to create 20.500** as the coordination hub **before** normative drafting begins.

**First content inside 20.500 (when you draft it):**

1. Phase 0 invariants (pending three-way sign-off)  
2. Document inventory with status column  
3. Sequencing table (adjusted order above)  
4. Re-review queue for signed modules  
5. Open questions (commit marker naming, XP/envelope model)

Once Jeff, Copilot, and I sign Phase 0 inside or alongside 20.500, **20.10 additive expansion** and **20.115** can start in parallel with clear gates.

**Commentary only — ready for three-way alignment on whether to draft the 20.500 skeleton next.**
Checking what's already explicit in the key docs so we can define the minimal statements needed to close the InB thread.
Yes — **CP is right**. InB is already normatively correct in **20.100**; what’s missing is **explicit scope language** so “input error correction” stops being read as InB’s job. That’s a **small, boundary-only** pass across **three or four docs** — not a refactor.

No new basin HLRs are required to **close the InB thread**. You’re recording a **decision**, not designing IIInB/UPI yet.

---

## What to add (minimal)

### 1. `20.100_inb_requirements.md` — **primary closure doc**

Add **`## Non-Goals`** (after Purpose or after Functional Boundaries):

```markdown
## Non-Goals

- **Semantic input error correction** — inferring user intent, choosing between plausible meanings, or applying user-specific shorthand meaning. That capability is **out of scope for InB** and is specified in the input-correction follow-on program (IIInB / UPI / USP — see 20.500 §7.7).
- **Meaning construction, routing, truth, or inquiry** — delegated to downstream Pipeline A components and GB-governed pathways per HLR-20.100-026.

## Input correction scope (terminology)

| Term | InB role |
|------|----------|
| **Structural / non-inferential correction** | **In scope** — encoding normalization, schema validation, deterministic lexical canonicalization, bounded reject/degrade, `MI_NOISE`-class surface handling per 20.17. |
| **Semantic input error correction** | **Out of scope** — InB SHALL NOT perform; downstream optional stages (IIInB + user clarification + UPI) own this when enabled by profile. |
```

Add one line under **`## Functional Boundaries`**:

```markdown
- InB **error correction** means **non-inferential intake normalization only**; semantic repair before Pipeline A is explicitly **not** an InB obligation.
```

**Version:** patch bump (e.g. v0.2) + changelog one-liner. No new HLR IDs required unless you want a formal HLR-027 later.

---

### 2. `20.17_messy_input_handling.md` — **align messy-input vs semantic repair**

Add to **`## Non-Goals`** (or a short **`## Relationship to input correction`**):

```markdown
- **Semantic input repair** — resolving ambiguous or user-invented constructions by inferring intended meaning. Messy-input handling **tags and preserves** conditions (`MI_*`); it does not substitute for IIInB/UPI semantic correction when that profile is enabled.
- InB messy-input actions at intake are **classification and deterministic surface normalization only** (HLR-20.017-030), not semantic guessing.
```

One cross-ref line is enough:

```markdown
**InB boundary:** InB participates in `MI_*` detection and non-inferential normalization only; semantic input error correction is defined outside 20.17 (IIInB/UPI follow-on).
```

---

### 3. `20.500_refactoring_for_dual_TS_pipeline.md` — **program pointer (coordination only)**

Add **`§7.7 Input correction follow-on (post–Stage 5)`** and one row in archived open items:

```markdown
### 7.7 Input correction follow-on (post–Stage 5)

**Decision (2026-06-07):** InB scope closed — non-inferential intake normalization only. **Semantic input error correction** is a separate follow-on slice: IIInB (bounded pre–Pipeline A correction), clarification path (CIL), UPI/USP (user-specific rules). **Not** InB, IB, or IMR.

| Track | Action | Status |
|-------|--------|--------|
| **H — Input correction** | IIInB + UPI/USP spec draft; CIL clarification interface | `not_started` |
```

In **§7.6 archived open items**, add:

```markdown
| H | Semantic input error correction (IIInB / UPI / USP) | Follow-on program; InB closed per §7.7 |
```

This lets you move on **without** reopening the closed dual-pipeline GATE.

---

### 4. `20.190_glossary.md` — **optional but stops terminology drift**

Under Core Terms or a small **Input correction terms** block:

```markdown
- **InB (Input Basin):** Deterministic intake normalization and non-inferential surface correction only; SHALL NOT perform semantic input error correction.
- **Semantic input error correction:** Pre–Pipeline A repair of user-specific or ambiguous meaning; **out of scope for InB**; follow-on IIInB/UPI program.
```

---

## What you do **not** need for InB closure

| Doc | Why skip for now |
|-----|------------------|
| **20.90 IB** | Already inquiry-only; add only if IB keeps getting dragged into the thread |
| **20.45 IMR** | Output-side; separate from input correction |
| **20.30** | §10 already says no probabilistic inference at InB; optional one clarifying sentence |
| **New IIInB/UPI specs** | Next discussion — **not** required to bury InB |

---

## Approval weight

This is **boundary clarification**, same class as Stage 5 polish:

- **20.100 / 20.17:** light CP review + changelog  
- **20.500:** coordination note only (already `complete`)  
- **20.190:** optional glossary align  

Not a GATE unless you add new numbered HLRs or change topology.

---

## One sentence to adopt as team decision

> **InB corrects surface form deterministically; semantic input error correction is a separate, profiled pre–Pipeline A program (IIInB + clarification + UPI/USP), not an InB, IB, or IMR responsibility.**

Paste the blocks above into the four docs (three required + glossary optional), bump 20.100/20.17 patch versions, and the InB discussion is **closed** so you can focus on IIInB/UPI design.

I can apply these edits directly in the repo if you want.
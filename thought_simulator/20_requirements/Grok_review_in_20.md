You're right to treat **20.190 as the intent enforcement layer**. Today it’s doing three jobs at once and doing none of them fully:

1. **Thin one-liners** (Core Terms) — easy to drift  
2. **Better dual-pipeline block** — still incomplete  
3. **Registry-Aligned dump** — duplicates Core Terms with **different wording** (e.g. OB, RB, InB, OuB appear twice)

That duplication is already a drift vector. **One-stop shopping** needs a deliberate **Primitive Intent Catalog** format, not more bullet sprawl.

---

## Recommended glossary shape (before expanding IMR)

Replace “expand everything” with **four sections**, each entry using the same template:

| Field | Purpose |
|--------|---------|
| **Focus** | One sentence: what it owns |
| **When** | Pipeline A / B / conversation layer / optional |
| **Why it exists** | Problem it solves |
| **Is not** | 1–3 common confusions |
| **Example** | One concrete scenario (for fuzzy terms) |
| **Normative home** | Link to 20.xx |

Keep **Registry-Aligned** as legacy/reference or merge duplicates into the catalog and mark registry entries as aliases.

---

## Tier 1 — Expand first (highest drift risk)

These are the primitives people keep assigning the wrong work to (your IIInB/IMR/InB thread is the pattern).

| Primitive | Why expand | Example worth including |
|-----------|------------|-------------------------|
| **InB** | vs IIInB, vs “error correction” | `"teh"` → canonical token; `"Yeah Baby!"` → hand off tagged, not guessed |
| **IIInB / UPI / USP** | New, easy to overload | User shorthand `"easier/quicker-ish"` → clarify → USP rule → next turn applied |
| **IB** | vs InB, vs input repair, vs IMR | `MI_VAGUE` → IB-Creation-Request → GB-approved inquiry, not gap-fill |
| **IMR** | vs input repair, vs IB, vs GB | “Output wrong factually” → Type B record; “too formal” → Type A |
| **OuB** | vs OpBeh/OBG, vs meaning writer | Same `semantic_core`, different seed → different surface text only |
| **GB** | vs rule store, vs COP, vs UPI | Veto unsafe USP rule; not store user lexicon |
| **CIL** | vs InB, vs clarification “Path B” | FIFO intake + escalate ambiguity; clarification event to UPI |
| **COB** | vs MTP, vs USP dump | Conversation continuity + where USP snapshots live |
| **COP** | vs GB executor, vs meaning | Proposes IB lifecycle action; GB commits at safe boundary |
| **TR** (Thought Router) | **Missing from glossary**; vs TrigRB, vs RB, vs XlateR | Stance/intent channels on TP; `tr_needs_update` after bounded correction |
| **TrigRB** | Namespace collision with TR/RB | Reads frozen `semantic_core` triggers; not lane routing |
| **OpBeh / OBG / XlateR** | vs OB/TR/RB basins | Planning triple on `exec_plan`; seed doesn’t pick OpBeh |
| **SRP** | vs RB (Pipeline A) | Cold compile tables; hot path lookup by `routing_epoch_id` |
| **TP vs MTP vs `semantic_core`** | Lane vs global vs committed envelope | TP on lane → merge → MTP → `mtp_update` → frozen `semantic_core` |
| **XP / `exec_plan` / `exec_trace`** | vs TP, vs MTP | One XP per `commit_id`; B audit separate from meaning |

**IMR belongs in Tier 1** — expand as we discussed, with Types A/B/C, `CorrectionTrigger`, `evaluator_signal`, and explicit “is not.”

---

## Tier 2 — Expand second (boundary / namespace drift)

| Primitive | Why | Example |
|-----------|-----|---------|
| **OB** | vs OpBeh, vs semantic interpreter | Pattern evidence on lane TP; no stance assignment |
| **RB** | vs SRP, vs TrigRB | Deterministic fan-out to OB/TB; not B routing tables |
| **TB** | vs Truth/Done (20.140), vs OuB | Interpretation into truth hypotheses; not final user text |
| **DCB** | “meta-basin” is fuzzy | Curvature spike → ephemeral event to TR; no OB semantics |
| **MB** | vs IMR, vs GB | Read-only diagnostics; no corrective authority |
| **Merge / splitting** | Easy to conflate with B | Lane TPs → MTP; not Pipeline B |
| **Pipeline A vs B** | Foundational | A writes meaning once per cycle; B realizes one pass per `commit_id` |
| **`commit_id` / `semantic_snapshot_ref`** | Replay vocabulary | Post-`mtp_update` freeze id; hash of committed meaning |
| **`routing_epoch_id`** | A vs B confusion | On B envelopes only; published SRP tables |

---

## Tier 3 — Metrics & cross-cutting (need examples, lighter “is not”)

Fuzzy without scenarios:

| Term | Example to add |
|------|----------------|
| **ΔH% (DeltaHPercent)** | Lane contribution to merged hypothesis mass; missing mass logged on truncate |
| **HPercent / truth_hypotheses** | TB output band; not same as “done” |
| **TCU** | Budget unit; OpBeh plan costs vs OuB expression costs |
| **Random Seed Boundary** | Same `semantic_core`, seed A vs B → different OuB pick only |
| **messy-input (`MI_*`)** | Not a primitive — glossary **taxonomy** entry: `MI_CONTRA` vs `MI_VAGUE` with one line each + mini example |
| **done_state / Truth-Done** | 20.140 evaluation; not “user satisfied” |

---

## Terms that should **not** be expanded in 20.190

Keep one line + pointer; detail lives in 20.35 / 20.90 / 40-series:

- Highway, Flow Modulator, Interpretive Manifold, Anti-Collapse Stabilizer, etc. (registry fluff)
- Generic: Canonicalization, Replayability, Watchdog (unless tied to a specific primitive)

**Action:** Collapse **Registry-Aligned** duplicates into the catalog or mark `*(registry alias)*` so OB isn’t defined two different ways.

---

## Primitives **missing** from the glossary today

Add intent entries (not just IMR):

- **TR** (Thought Router) — biggest omission  
- **Merge** (and **splitting** if lane primitive)  
- **InB** is there; **Input Basin** registry duplicate should defer to catalog entry  
- **`CorrectionTrigger`**, **`evaluator_signal`**  
- **Truth/Done** (or pointer to 20.140)  
- **IB-Creation-Request** (wire between 20.17 and IB)  
- **Envelopes**: `semantic_core`, `supervisory` (four-envelope model from 20.36)

---

## Example format (template for rigor)

For each Tier 1 entry, something like:

```markdown
### IMR (Interpretation Mismatch Routine) — [20.45](20.45_imr_requirements.md)

- **Focus:** Post-realization mismatch detection and trigger scheduling on Pipeline B.
- **When:** After `oub_expression` / `imr_evaluation`; reads frozen `semantic_snapshot_ref`.
- **Why:** Separate “output doesn’t match committed meaning or evaluator feedback” from input repair and from meaning construction.
- **Is not:** InB/IIInB (input), IB (inquiry), direct `semantic_core` writer, GB rule store.
- **Example:** User says “that’s factually wrong” → Type B `imr_record` + optional `CorrectionTrigger` for listed fields next cycle; “too casual” → Type A realization retry same snapshot.
```

Fuzzy terms get **one italicized example**; crisp wire terms (`commit_id`) can skip example.

---

## Suggested rollout (so this doesn’t become a 3-week rewrite)

| Phase | Scope |
|-------|--------|
| **Phase 1** (now) | Restructure Purpose of 20.190; add **Primitive Intent Catalog** skeleton; Tier 1: InB, IB, IMR, OuB, GB, CIL/COB/COP, TR, Pipeline A/B, TP/MTP/`semantic_core` |
| **Phase 2** | Tier 2 basins + B manifold (OpBeh, OBG, XlateR, TrigRB, SRP, XP envelopes) |
| **Phase 3** | Metrics + `MI_*` taxonomy + dedupe Registry-Aligned |
| **Phase 4** | IIInB/UPI/USP when Track H spec lands |

Each phase = one changelog bump; normative HLRs stay in 20.xx modules.

---

## Bottom line

**Yes — expand the glossary**, but as a **Primitive Intent Catalog** with a fixed template (Focus / When / Why / Is not / Example / Link), not longer ad hoc bullets.

**Highest priority expansions:** IMR, InB, IB, OuB, GB, CIL, COB, COP, TR, Pipeline A/B, TP/MTP/`semantic_core`, plus **dedupe** the Registry-Aligned basin definitions.

**Fuzzy terms that most need examples:** IB, DCB, ΔH%, messy-input classes, Random Seed Boundary, GB vs COP, semantic vs expression correction, IIInB unknown-segment path.

When you’re ready to execute, I’d do **Phase 1 + IMR block** in one edit to `20.190`, add a short **“How to read this catalog”** at the top, and fold duplicate OB/RB/InB/OuB registry lines to point at the catalog entry. Say the word and I’ll implement Phase 1.
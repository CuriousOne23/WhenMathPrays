Reviewing how INB/error correction is specified in the requirements so the comment is grounded in your docs, not generic.
CP is pointing at a real realizability concern, but in **your** stack the answer depends heavily on **which “INB” means** — and the right place to tighten requirements is probably **not** 20.100 InB.

## Terminology first

In `20_requirements`, the closest match to CP’s “INB” is **InB** (Input Basin, [20.100](thought_simulator/20_requirements/20.100_inb_requirements.md)). There is also **IB** (Inquiry Basin, 20.90), which handles ambiguity — a different animal.

If the question is “can **InB** realize error correction?”, the short answer is already normative:

> **InB SHALL NOT perform inference or truth arbitration** (HLR-20.100-002).

So CP’s “not yet satisfied unless there’s an inference-capable substrate” is **correct as a systems warning**, but **mis-aimed if the fix is proposed for InB**. In TS, error correction is **architecturally delegated** downstream.

## Where TS actually puts the correction loop

CP’s five-step loop maps reasonably well onto the **IMR / Type B** path, not InB:

| CP step | TS analogue | Status |
|--------|-------------|--------|
| 1. Target vs observed state | `semantic_snapshot_ref` vs `oub_artifact_ref` + `evaluator_signal` | Partially specified (20.45) |
| 2. Discrepancy detection | IMR taxonomy (A/B/C), deterministic precedence | Specified (20.45 HLR-001–003) |
| 3. Cause inference | `target_field_ids[]` / `correction_context` on `CorrectionTrigger` | **Bounded, not fully inferred** (20.45 HLR-007–010) |
| 4. Corrective action | Bounded Pipeline A recompute (TR, listed basins); **not** same-cycle `semantic_core` write | Specified (20.45, 20.206, 20.37 §3.4) |
| 5. Loop closure | Next-cycle E3 replay; 20.36 Class 3b strip tests | Specified in replay/fixture layer |

So TS **does** have an error-correction *architecture*. What it **does not** have is a general “infer the cause, then repair anything” substrate — and that appears **intentional**, consistent with 20.12/20.17’s repeated **no latent inference** posture.

## Where CP is right for *this* project

Three gaps CP surfaces that **do** bite TS, mainly in **20.45 IMR** (still draft) and adjacent modules:

1. **`evaluator_signal` realizability** — IMR classification is defined over it (HLR-20.045-002), but the **producer, schema, and admissible signal codes** are not fully closed in one normative place. That’s CP’s step 2 without a wired input.

2. **Cause localization is shallow by design** — Type B says *which fields to reconsider* via `target_field_ids[]`, but there’s no normative story for **how those IDs get chosen** (external user annotation? deterministic mapping from `evaluator_signal_code`? GB policy table?). CP’s step 3 is the weak link.

3. **Evidence → structure update** — The loop closes through **Pipeline A pathways**, not through editing an “independence graph.” CP’s INB-R2/R3 (editable dependencies + evidence integration) don’t map cleanly onto InB; they’d need to live in **correction routing** (20.45, 20.37, maybe 20.18), with explicit bounds already partly present (caps, cooldowns, `max_correction_depth_per_cycle`).

CP is right that **conceptual independence ≠ operational error correction**. TS sidesteps that by saying: correction is **supervisory + bounded re-interpretation**, not InB self-repair.

## Where I’d push back on CP’s draft INB-R1..R4

If pasted into **20.100** as written, INB-R1..R4 would **fight existing HLRs**:

- InB must not infer (HLR-20.100-002).
- Pipeline A/B broadly forbid latent/probabilistic inference (20.17, 20.12, 20.90, etc.).
- InB must not mutate MTP/OB/RB/TB/IB state (HLR-20.100-019).

A full “infer candidate causes and revise structure/parameters” loop sounds more like a **learning/repair layer** than Input Basin — outside the deterministic TS contract unless heavily bounded and externalized (evaluator + GB gate).

## Practical recommendation

**Agree with CP’s diagnosis, disagree with default placement.**

| Action | Rationale |
|--------|-----------|
| **Do not** add INB-R1..R4 to 20.100 | Conflicts with InB’s charter |
| **Do** add a small **“Correction realizability”** block — call it IMR-R or ECR — in **20.45** (or cross-ref from 20.18) | That’s where the loop actually lives |
| Minimum contents | (a) `evaluator_signal` schema + authority; (b) deterministic mapping from signal → trigger class; (c) admissible rules for populating `target_field_ids[]`; (d) explicit re-test contract (ties to 20.36 Class 3b / 20.207 E3) |
| **Clarify with CP** | InB vs IB vs abstract “independence framework” — three different answers |

## Bottom line for your question

> “Per INB requirements, have we examined INB enough that it can be realized [for error correction]?”

**For InB (20.100):** Yes for its **actual** job — deterministic intake, canonicalization, reject/degrade, handoff. **No** for error correction — and it **shouldn’t** be yes; that’s by design.

**For error correction realizability in TS overall:** CP is **partially right** — the loop is sketched (IMR + Type B + E3), but **evaluator substrate** and **target-field derivation** are the fuzzy nerves. Tighten **20.45**, not 20.100.

If you want to take CP up on the line-by-line draft, I’d frame it as an **IMR realizability appendix** with explicit cross-refs to 20.36/20.207 replay classes — that slots cleanly into the structure you already closed in Stage 5 without reopening the dual-pipeline program.
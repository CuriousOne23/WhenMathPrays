The summary is **mostly well-argued** and fair to attribute back to the review thread — but it over-tightens a few steps. IIInB is the **cleanest** place for pre-A semantic repair if that capability stays a **hard requirement**. It is not literally the **only** architecture that satisfies the constraints.

## What the summary gets right

**1–3 (IMR / InB / IB)** — Solid. Grounded in actual HLRs:

- IMR is post-`mtp_update` / post-expression; it reads `semantic_snapshot_ref`, not raw intake.
- InB is explicitly non-inferential (HLR-20.100-002).
- IB is inquiry/ambiguity under GB, not input janitorial repair (20.90).

So the requirement *“correct semantic input before A goes down the wrong path”* cannot land in those three modules without violating their charters.

**4 (no systematic A→B→A)** — That’s a **product/architecture decision** (Jeff’s stance + CP’s v0 proposal), not something the earlier review **proved** impossible. Type B was specified as **bounded, deterministic, next-cycle** recompute — a control loop, yes, but not “uncontrolled” in the sense 20.45 caps/cooldowns were written to prevent. The summary is right to **reject** it for v0 if that’s the chosen posture; weaker to say it “violates determinism posture” as a blanket fact.

**5 (IIInB placement)** — Topologically sound: **after InB, before OB/RB-heavy meaning work**, profile-gated, correction trace emitted, doesn’t steal IB or IMR roles. Matches the module-contract style you’ve been using.

## Where the logic overreaches

### “Only one architecture remains viable”

Several other designs meet the same constraints without a new basin:

| Alternative | How it satisfies “pre-A” without breaking InB/IB/IMR |
|-------------|------------------------------------------------------|
| **v0 deferral (honest non-repair)** | 20.17 tags (`MI_VAGUE`, `MI_INCOMP`); IB-Creation-Request / user clarification **before** full A commitment. No semantic guessing; requirement softened to “surface ambiguity early.” |
| **External / CIL pre-pass** | Inference runs **outside** TS core (human, host app, optional service); InB ingests **already-canonicalized** corrected text. TS stays deterministic; repair isn’t a basin. |
| **COP propose-only (extension profile)** | COP proposes corrected reading; GB approves at safe boundary; Pipeline A sees approved snapshot only. Reuses optional-async pattern (20.34), no IIInB topology. |
| **Pipeline A stage, not new primitive** | A profiled `input_repair` **stage** in 20.30 (between InB and RB) without full “basin” ontology — lighter spec surface than 20.xx IIInB. |

So the honest conclusion is:

> Given **pre-A semantic repair as a mandatory, in-core capability**, IIInB (or equivalent dedicated stage) is the **best fit**.  
> Given **minimal v0 / no in-core semantic guessing**, you can satisfy the *spirit* of the constraints **without** IIInB by deferring repair.

The summary collapses those into one fork too aggressively.

### “Does not require a GPU”

True for **heuristic / lexicon / edit-distance** IIInB. If IIInB allows a **small model**, you still need the same profile/TCU/replay story CP described — and strict determinism gets harder unless the model is frozen, versioned, and replay-bound. IIInB doesn’t magically remove that; it **relocates** it to pre-A.

### “IMR is non-inferential”

IMR classification is **deterministic rule application** over `evaluator_signal` — not latent inference, but still **discrepancy → class → action**. The review’s point was **wrong layer** (output vs input), not “IMR doesn’t infer anything.”

## Comment on sending this to Grok

As a message **to me (Grok)**, the summary is **90% fair** if you soften two lines:

1. Replace *“only one architecture remains”* with *“only one **in-core basin** remains if pre-A semantic repair is a **normative v0 requirement**.”*
2. Replace *“violates determinism posture”* (re A→B→A) with *“Jeff does not want a **mandated** feedback controller in v0; Type B remains an **extension profile**.”*

That keeps the letter aligned with what the review actually said and avoids boxing you in if you later choose deferral or external repair.

## Recommendation

| If Jeff’s must-have is… | Direction |
|-------------------------|-----------|
| **“Fix wrong input before A runs”** (in-core, semantic) | **Yes → IIInB** (or profiled `input_repair` stage with same semantics). Draft skeleton is reasonable next step. |
| **“Don’t go wrong silently”** (PoC / v0) | **No IIInB yet** — tighten 20.100 + 20.17 non-goals; IB/CIL clarification path; IMR Type A monitor only. |
| **“Fix input but TS stays pure deterministic core”** | **External pre-pass or COP+GB** — repair outside or propose-only, not inside InB. |

**On the skeleton offer:** A minimal `20.xx_iiinb_requirements.md` is useful **if** you’ve picked the first row. It should state upfront:

- Optional / profile-gated (`execution_signature`)
- Sits after InB handoff
- One-shot, bounded, append-only `input_correction_record`
- SHALL NOT write `semantic_core` or trigger IMR Type B
- Deterministic replay over correction trace (even for heuristic path)
- Explicit non-goals: IB, InB, IMR, systematic A→B→A

That slots cleanly as a **post–20.500 follow-on slice**, not a silent edit to closed docs.

**Bottom line for the summary:** Send it with the two softenings above. The constraint chain is sound; the conclusion should be **“IIInB is the preferred in-core solution if we insist on pre-A semantic repair”**, not **“the constraints force IIInB with no alternatives.”**
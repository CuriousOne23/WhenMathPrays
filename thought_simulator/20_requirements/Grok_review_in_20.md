Checking how InB, IB, and input repair are scoped in the requirements so the comment stays grounded.
CP’s second note is sharper than the first: it separates **three different problems** that were getting conflated. Here’s how that lands against your actual `20_requirements` stack and the earlier Grok review.

## CP is right about the tangle

The three tensions are real and should stay separate:

| Tension | What it is |
|--------|------------|
| **A** | Promised *input* error correction vs what InB normatively does |
| **B** | IB’s charter (information / inquiry) vs “janitorial” input repair |
| **C** | Semantic inference under **no-GPU / deterministic** constraints |

Your prior Grok review mostly answered **output-side** correction (IMR Type B, `CorrectionTrigger`, E3 replay). CP is now asking about **input-side** semantic repair (“user wrote X, probably meant Y”). That’s a different lifecycle point and a different module boundary.

## What the docs actually say today (important)

On **A**, the normative picture is already fairly strict — not fuzzy delegation to IB:

- **20.100 InB:** SHALL NOT perform inference or truth arbitration (HLR-20.100-002); canonicalization + bounded reject/degrade only.
- **20.30 §10:** InB maps noisy surface forms **without probabilistic inference**; RB shall not hallucinate corrections.
- **20.17:** messy-input is **tag and preserve** (`MI_*` classes), not gap-fill; vague/incomplete paths route to **IB-Creation-Request via GB**, not silent repair.

So if someone “originally scoped InB as semantic input error correction,” that promise is **not reflected in the current HLR set**. That’s either stakeholder/architecture drift or informal language (“error correction” = normalization) that never got claim-classified. CP’s smell is valid as a **traceability / honest-claims** issue, not necessarily as “we already moved it to IB in the specs.” IB isn’t doing input repair in 20.90 either (no probabilistic inference, inquiry over bounded explicit inputs).

**Bottom line on A:** Don’t silently assign semantic input repair to IB. But also: **the written requirements already say InB doesn’t do it** — the fix is explicit **out-of-scope / profile** language, not a stealth IB rewrite.

## CP vs the earlier Grok review

| Topic | Grok review (prior) | CP (this note) |
|-------|---------------------|----------------|
| Primary correction loop | IMR / Type B / post-expression | Input-time semantic repair |
| Right doc to tighten | 20.45 (`evaluator_signal`, `target_field_ids`) | 20.100 boundary + optional new capability |
| InB role | Correctly excluded from inference | Same, plus narrow “non-inferential correction” wording |

Both can be true. TS currently sketches **two** correction stories:

1. **Ingress:** InB + 20.17 — deterministic normalization + messy-input taxonomy (no semantic guessing).
2. **Egress / feedback:** IMR Type B — bounded Pipeline A recompute after expression mismatch.

What’s **missing** is an explicit normative slot for **ingress semantic repair** if you still want that product capability.

## On IB vs IIInB — CP’s fork

CP’s framing matches your architecture style (rigid module contracts, profiled optional capability).

**Keep IB pure** — strongly aligned with 20.90 today. IB is for ambiguity / inquiry evolution under GB, not fixing typos or guessing intent at the wire.

**IIInB (Input Inference/Repair Basin)** — architecturally clean *if* you want semantic input repair as a first-class, optional feature:

- Slots naturally **after InB, before heavy meaning construction** (or as a profile-gated branch off InB handoff).
- Mirrors patterns you already use: **optional subsystem** (like COP), **execution_signature / profile** gating, **TCU bounds** (20.90, 20.150).
- Avoids polluting IB and keeps 20.100 honest.

**Cost:** New basin = real program weight: 20.30 topology, routing, 20.200 row, Stage-4-style review, fixtures. Per 20.500, that’s not a casual polish pass — it’s a bounded follow-on program slice.

## No-GPU constraint — CP is pragmatic

CP’s three CPU options match how TS is already written to think:

- **Heuristic / lexicon / edit-distance repair** → fits deterministic InB-adjacent or IIInB **light profile**.
- **Tiny model under strict TCU** → optional **rich profile**, not minimal conformance.
- **Defer semantic repair** → aligns with v1 posture already implied by 20.17 (tag + IB request, don’t invent).

Full LM-style repair as a **hard** PoC requirement would fight 20.12/20.17/20.100. CP is right to make it **profile-dependent**.

## Recommendation (if picking a direction today)

**First choice (matches CP’s preference and your docs):**

1. **Keep IB unchanged** — reaffirm no input-level repair.
2. **Tighten InB** — rename/clarify “error correction” → **non-inferential correction only** (normalization, canonical token repair, `MI_NOISE` handling); explicit delegation line: semantic repair is **out of scope for minimal profile**.
3. **Do not use IMR for input repair** — IMR is post-`oub_expression` feedback; wrong layer for “user meant Y at intake.”
4. **Either:**
   - **v1:** Document semantic input repair as **explicitly deferred** (20.100 + 20.17 non-goals + 20.500 §7.6-style open item), **or**
   - **v1.1:** Add **optional IIInB** as a profiled extension doc (not folded into IB).

**Second-best (CP’s fallback)** — also defensible for PoC momentum:

- No new basin now.
- Semantic input repair = **documented future extension**.
- InB + 20.17 + IB-Creation-Request = complete **honest** minimal story: surface cleanup, explicit flags, supervised inquiry — no guessing.

**What I would not do:** Let IB absorb input repair without a Purpose/Scope rewrite and GB routing overhaul. That blurs the clean Pipeline A story you just closed in Stage 5.

## Direct answer to CP’s closing question

> Keep IB pure or let it absorb repair?

**Keep IB pure.** If semantic input repair stays a requirement, **IIInB (optional/profiled)** or **explicit v1 deferral** — not IB, not InB, and not IMR.

If you want a single next doc action without a new basin: add a short **“Input repair scope”** subsection to **20.100** and **20.17** (non-inferential vs semantic; minimal vs rich profile). That closes the honest-claims gap CP flagged without reopening the dual-pipeline program. IIInB can be a separate design ticket when you’re ready to pay the topology cost.
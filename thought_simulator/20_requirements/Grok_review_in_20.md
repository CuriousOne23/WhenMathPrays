Comparing CP's summary against our agreed definitions in `20.190` and related specs.
CP’s write-up is useful as a **design stress-test**, but it describes a **different system** than the one you closed on 2026-06-07. Several parts are architecturally sound; the primitive definitions and placements largely **conflict** with `20.190`, `20.100`, and `20.500` §7.7. I would not adopt it as-is.

## Verdict at a glance

| Question | CP summary | Agreed program (20.190 / 20.500 §7.7) |
|----------|------------|----------------------------------------|
| Are three primitives needed? | Yes, as a front→mid→late semantic stack | **One** follow-on program with **three roles** — not a parallel meaning pipeline |
| IIInB purpose | Input integrity & canonicalization | **Bounded semantic input repair** using USP rules |
| USP purpose | Early semantic intent structuring on TP | **Versioned rule store** (user shorthand); read-only to IIInB |
| UPI purpose | Late routable job contract before exec | **Profile writer** after clarification; writes USP only |
| Placement | IIInB pre-OB; USP post-OB/TR; UPI pre-routing | **Pre–Pipeline A** repair path + **conversation-layer** clarification/UPI; not mid-A basin stages |

---

## What CP gets right

These align with your closure and `20.190`:

1. **IMR separation** — Post-output, Pipeline B, no direct rewrite of input-repair primitives. Type B only schedules bounded A re-runs via `CorrectionTrigger` / `target_field_ids[]`. Good.

2. **Authority model** — IMR does not own IIInB/USP/UPI definitions; it points at fields, Path A re-executes deterministically. Matches `20.45` and the catalog.

3. **Determinism / replay** — Same inputs + profile snapshot → same outputs. Required for Track H.

4. **CIL governance spirit** — No hidden inference, no silent scope expansion. Right *principle*, but CP applies it to the wrong primitives (see below).

5. **Need for the program** — The underlying problem is real: user-specific shorthand and ambiguous meaning cannot live in InB (closed) or IMR (post-B). Track H is justified.

---

## Where CP diverges (material)

### 1. IIInB = duplicate of InB

CP defines IIInB as:
> normalize whitespace, typos, encoding; segment units; syntactic disambiguation only; no semantic correction

That is **InB’s closed scope** per `20.100` v0.2. You already decided surface canonicalization is **not** a second basin.

**Agreed IIInB:** optional **semantic** repair — apply explicit USP rules, escalate unknowns to clarification, never guess.

If IIInB does what CP says, you don’t need IIInB; you need to reopen InB, which breaks the closure line.

### 2. USP = new meaning-construction primitive

CP places USP **after OB/TR** to write `tp.intent_type`, `tp.intent_slots[]`, task shape, constraints.

That encroaches on primitives that already exist:

| CP assigns to USP | Already owned by |
|-------------------|------------------|
| Task / intent type | **TR** (`TP.TR` stance/intent channels) |
| Structured interpretation | **OB** + **TB** |
| User constraints for expression | **B side** (`obg_id`, OpBeh) after meaning is committed |
| Persistent preferences | **USP store** (agreed) — but as **rules**, not live TP semantics |

A profile **store** should not be a Pipeline A basin that writes intent fields every cycle. That creates a second meaning path parallel to OB → TR → TB → Merge.

### 3. UPI = duplicate of routing / exec planning

CP defines UPI as a late-semantic **job contract**: `tp.upi_contract`, `mtp.route_plan_ref`, tool binding, safety guardrails.

That overlaps:

- **RB** — Pipeline A routing
- **SRP + `exec_plan`** — Pipeline B planning contract
- **GB** — safety gates and supervisory policy

Agreed **UPI** is narrow: **after clarification**, deterministically **writes shorthand rules into USP**. It is not a per-turn routable contract generator.

### 4. Wrong layer names weaken the review

CP uses **CIL = “Cognitive Integrity Layer”** and **COB = “Cognitive Output Boundary.”** In your stack:

- **CIL** = Conversation Integration Layer (`20.33`)
- **COB** = Conversation Object Basin (`20.32`)

The governance arguments are directionally fine, but anchoring them to the wrong expansions will confuse every downstream doc.

### 5. Placement table doesn’t match the dual pipeline

CP’s stack:

```
IIInB (pre-semantic) → OB/TR → USP → UPI → routing/exec → … → IMR
```

Agreed stack:

```
External → CIL (conversation) → InB (surface, Pipeline A input)
         → [optional IIInB reads USP; unknown → clarification]
         → Pipeline A: RB → OB → DCB → TR → TB → Merge → Truth/Done → mtp_update
         → Pipeline B: TrigRB → SRP → exec_plan → OuB → IMR
```

**UPI** sits on the **clarification path** (conversation layer), not between USP and routing. **USP** sits under **COB** as durable profile state, not as an early-A semantic writer.

---

## Correct rigid definitions (for Track H spec)

These are what `20.190` already pins; CP should be reconciled to them:

### IIInB (Input Inference/Repair Basin — draft)
- **Focus:** Apply **explicit, versioned USP rules** to ambiguous/user-shorthand segments before full meaning construction.
- **When:** Optional, profile-enabled, **pre–Pipeline A semantic repair** (after InB surface norm or as gated pre-A slice — ordering is a Track H spec decision, not “replace InB”).
- **Writes:** Bounded repair tags / resolved-segment refs on intake-bound fields — **not** `semantic_core`, **not** `TP.TR`, **not** MTP semantics.
- **Is not:** InB; IB; IMR; USP (it reads USP); UPI (UPI writes rules, IIInB consumes them).

### USP (User Semantic Profile — draft)
- **Focus:** Auditable store of **user/conversation shorthand rules** (post-clarification commitments).
- **When:** Durable; COB-governed; **read-only to IIInB** at intake.
- **Writes:** Profile snapshots / rule versions — **not** per-cycle TP intent construction.
- **Is not:** TR; OB; exec_plan; GB policy table.

### UPI (User Preference Integrator — draft)
- **Focus:** Deterministic integrator that **commits clarification outcomes into USP**.
- **When:** **After** CIL clarification event — conversation layer, not late Pipeline A.
- **Writes:** USP rule entries only (GB veto on unsafe rules).
- **Is not:** Routing planner; contract builder; IMR; IIInB.

---

## IMR / CIL / COB — CP’s relationship section

**Keep:**
- IMR indirect-only coupling to Track H primitives.
- No IMR ownership of input repair.
- Bounded re-application via Type B field lists.

**Revise:**
- CIL’s role for Track H is **clarification FIFO + escalation to UPI**, not “cognitive integrity” at three semantic stages.
- COB’s role is **USP versioning + conversation continuity**, not “output boundary checks against UPI contracts.” Output mismatch → **IMR** (+ OuB/`exec_trace`), not COB-vs-UPI contract diff (unless COB later stores export policy only).

---

## Do you need three primitives?

**Yes, but as three roles in one program — not three new meaning-pipeline stages.**

| Role | Needed? | Why not fold into existing? |
|------|---------|------------------------------|
| **IIInB** | Yes | Semantic repair is out of InB scope and pre-B; IMR is too late |
| **USP** | Yes | Durable user shorthand must survive turns and be auditable; doesn’t belong in TP/MTP per cycle |
| **UPI** | Yes | Clarification → rule commit needs a single writer with GB gate; not InB (no inference) or IB (inquiry ≠ profile write) |

What you **don’t** need is CP’s reinterpretation where USP/UPI become a second OB/TR/routing stack.

---

## Recommended next step

Don’t paste CP’s summary into `Grok_review_in_20.md` as the shared model. Use it as a **rejection checklist**:

1. **Reject** IIInB-as-canonicalization → stays in InB.
2. **Reject** USP-as-intent-structurer → stays TR/OB/TB.
3. **Reject** UPI-as-route-contract → stays RB / SRP / `exec_plan`.
4. **Accept** IMR separation and determinism framing.
5. **Expand** `20.190` Phase 4 into **three separate catalog entries** (IIInB, USP, UPI) with the rigid definitions above when Track H `20.xxx` opens.

If you want, I can draft that Phase 4 glossary split plus a one-page **CP reconciliation note** for `Grok_review_in_20.md` that maps CP’s good instincts to the correct primitive owners — without editing normative modules until you and CP sign the placement table.
**Verdict: CP’s corrected summary is aligned.** It can serve as the shared conceptual map for Track H review. I would sign it as a mental model with a few small clarifications to lock before normative text.

---

## What CP fixed (material)

The first draft’s three failures are gone:

1. **IIInB** is semantic repair via USP rules, not InB-style canonicalization.
2. **USP** is a COB-governed rule store, not an OB/TR intent writer.
3. **UPI** is a post-clarification USP writer, not SRP/`exec_plan` routing.

Also corrected: CIL/COB expansions, the dual-pipeline placement diagram, TP/MTP write table (none write meaning semantics), and IMR as indirect-only supervisor. That matches `20.190`, `20.100` closure, and `20.500` §7.7.

---

## Remaining nits (spec-level, not blockers)

### 1. “Not a basin” vs “Repair Basin”

CP says IIInB is **not a basin** but also uses **Input Inference/Repair Basin**. Both can be true if you mean:

- **Not** a Pipeline A basin in the RB → OB → TR → TB chain  
- **Possibly** still a named Track H primitive (basin-class or profiled `input_semantic_repair` stage)

Track H should pick one wire form. The behavior is settled; the naming bucket is not.

### 2. InB → IIInB ordering (open decision)

CP places **InB before IIInB** (IIInB expects canonicalized input). That is the better default: surface norm first, semantic repair second.

`20.190` still says “before Pipeline A `input` stage,” which is ambiguous because InB *is* the input stage. Track H should explicitly adopt:

```
CIL → InB (surface) → [optional IIInB reads USP] → RB → …
```

and bump the glossary line when that is signed.

### 3. IMR §6 — one overreach

> “UPI may be invoked if clarification is needed”

Too loose. IMR does not invoke UPI. The chain is:

- **IIInB** escalates unknown segments → **CIL** clarification → **UPI** writes USP  
- **IMR** may schedule bounded A re-runs (including re-application of IIInB rules on already-known USP entries) via `CorrectionTrigger` — not clarification initiation

Keep IMR out of the clarification write path.

### 4. IIInB escalation vs IB-Creation-Request

CP does not conflate them (good). Track H spec should still document both paths:

| Trigger | Path |
|---------|------|
| Unknown shorthand (no USP rule) | CIL clarification → UPI → USP |
| `MI_INCOMP` / commitment blocked | IB-Creation-Request → GB → IB |

Same program, different wires. Worth one row in the Track H outline.

### 5. “USP is not re-run per turn”

Fine as intuition. Precise wording: USP is **read** when IIInB runs; it is not a per-cycle Pipeline A stage.

---

## Alignment check against your review criteria

| Criterion | CP v2 |
|-----------|-------|
| Primitives needed? | Yes — three roles, one program |
| Rigid purpose? | Yes — “is / does / is not” blocks are crisp |
| Correct placement? | Yes — matches §8 diagram |
| Coordinates with TS primitives? | Yes — no duplicate OB/TR/routing stack |
| IMR boundary? | Yes (minor §6 wording fix) |
| InB closure respected? | Yes |

---

## Recommendation

**Accept** CP v2 as the shared mental model. Suggested next moves:

1. **Append to `Grok_review_in_20.md`** — CP reconciliation (v2) + my three nits above as “Track H open items”
2. **`20.190` Phase 4** — split the combined IIInB/UPI/USP entry into three catalog entries using CP’s “is / is not” blocks
3. **Track H `20.xxx` skeleton** — wire schemas only: USP rule record, IIInB repair tag, UPI commit event, InB→IIInB ordering, escalation vs IB path

I would **not** wait on a diagram; the ASCII in §8 is enough for sign-off. The glossary split is the highest-value next edit because it prevents the drift that motivated `20.190` in the first place.

If you want me to execute, I can append the reconciliation to `Grok_review_in_20.md` and do the Phase 4 glossary split in one pass.
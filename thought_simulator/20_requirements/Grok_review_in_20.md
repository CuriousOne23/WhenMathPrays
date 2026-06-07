## Grok review — UPI / USP / IIInB (RFC commentary)

This draft is in good shape to send. The problem statement is clear, boundaries are mostly honest, and the open questions are the right ones. Below is commentary you can use as my response without locking implementation yet.

---

### What works well

**The IIInB split (correct vs clarify)** is the right decomposition:

- IIInB applies **only** when a rule or deterministic transform applies.
- Unknown / ambiguous segments → **no guess** → clarification path.
- Learned meaning → **external store**, not self-modifying IIInB.

That preserves everything the 20-series already insists on: no latent inference in InB (HLR-20.100-002), messy-input tagging in 20.17, IB for inquiry not janitorial repair, IMR on the wrong side of A for input repair.

**UPI as “profile writer, not meaning constructor”** is a credible pattern. It mirrors how TS already treats `execution_signature` / `policy_signature`: versioned, auditable, bound at safe boundaries — not live mutation inside a basin.

**GB as oversight, not dictionary** aligns with 20.80 / 20.16. GB should veto unsafe or globally incoherent rules, not own user lexicon storage.

---

### Critical naming fix before this hits 20-series

**Do not call the clarification path “Path B.”**

In your stack, **Pipeline B** already means the execution manifold (OpBeh/OBG/XlateR → OuB → IMR). “Path B = ask the user” will collide in every review, fixture, and grep.

Rename now, e.g.:

| Avoid | Prefer |
|-------|--------|
| Path A | **Pipeline A** (existing) |
| Path B | **Clarification path**, **CIL clarify lane**, or **UCR** (user clarification request) |

Same for “Path B triggers UPI” — use **clarification completion event** or similar.

---

### Is UPI the right location?

**Mostly yes**, with one refinement: UPI is probably not a new *basin* but a **deterministic integrator** sitting in the **conversation / identity layer**, not Pipeline A or B.

Strongest existing anchors:

| Candidate home | Fit |
|----------------|-----|
| **New 20.xx `upi_requirements.md`** | Cleanest if UPI is a first-class subsystem |
| **20.33 CIL** (extension) | Natural if clarification is conversation-intake UX |
| **20.32 COB** (extension) | Natural if USP is **per-conversation-object / per-user continuity** state |
| **COP + GB approve** (20.34) | If rule writes are **proposals** until GB commits |

**Recommendation:** UPI as its own thin spec (20.xx), with USP stored under **COB-scoped user/conversation identity** (20.32 cross-ref). CIL owns *delivery* of clarification; UPI owns *rule integration*; COB owns *persistence scope*; GB owns *veto/safety*.

That avoids inventing a second “basin” when you already have conversation-layer primitives.

---

### Answers to your open questions (provisional)

**(1) Right architectural location?**  
Yes — **UPI integrator + USP store**, not inside IIInB/IB/IMR/GB. Persist via COB (or CIL handoff), expose read-only to IIInB via `user_semantic_profile_ref` on the intake tuple.

**(2) Rule acceptance constraints?**  
Minimum normative set:

- **Safety:** no policy bypass, no suppressed `MI_CONTRA`, no auto-resolution of conflicts (20.17).
- **Determinism:** rules are **ordered, versioned, content-hashed**; IIInB consult is `f(raw_segment, USP_snapshot, policy_signature)` — replayable.
- **Scope:** rule must declare `match_kind` (exact, prefix, regex-bounded), `max_span`, `priority`, `expiry` or `confirm_by`.
- **Conflict:** same pattern → two meanings → **reject new rule** or **GB arbitration**, never silent overwrite.
- **Global coherence:** GB may veto rules that contradict published policy tables or safety invariants (20.170).

**(3) Per-user vs per-session vs per-context?**  
**Layered scopes**, default order for IIInB lookup:

1. `session` (ephemeral, clarification this thread)  
2. `conversation_id` / COB object  
3. `user_id`  
4. `domain_profile` (optional, policy-published)

PoC minimum: **conversation + user**. Session-only without promotion to user is fine for v0.

**(4) GB veto vs advisory?**  
**Veto on commit**, advisory on read. Pattern:

- UPI **proposes** rule → GB **approve / deny / safe-boundary defer** (same as COP/IB flows).
- IIInB **reads only committed** USP snapshots; never draft rules.
- Type C / safety rules: GB **mandatory** gate, not optional.

**(5) Aging / decay / confirmation?**  
Yes for v1 credibility:

- `created_at`, `last_used`, `use_count`, optional `expires_at`
- **Explicit user confirm** for promotion session → user scope
- Deterministic **decay** = rule inactive after expiry, not deleted silently (audit retains history)

**(6) Risks of IIInB consulting USP?**

| Risk | Mitigation |
|------|------------|
| IIInB becomes hidden learner | IIInB **read-only** USP; writes only via UPI |
| Nondeterminism | Frozen `usp_snapshot_ref` per cycle; bind in `execution_signature` |
| Rule explosion | Cap rules per user/conversation (20.90-style parameter) |
| Cross-user bleed | USP keyed by `user_id` + COB; IIInB forbidden from global merge |
| Routing contamination | USP affects **segment normalization only**, not RB/TR routing tables |
| Feedback loop | Clarification → UPI → IIInB is **open-loop per input**, not A→B→A IMR loop |
| GB bloat | GB stores **decisions**, not rules; UPI/COB store rules |

---

### Gaps to add to the draft (small, high value)

1. **IIInB read contract** — one paragraph: when USP matches vs when to emit `UNKNOWN_SEGMENT` and escalate to clarification.
2. **`usp_snapshot_ref`** — same pattern as `semantic_snapshot_ref` / `commit_id` for replay.
3. **Relationship to 20.17** — USP resolution must not clear `MI_VAGUE` / `MI_CONTRA` without explicit taxonomy update; shorthand ≠ contradiction resolution.
4. **Program placement** — post–20.500 **follow-on slice** (IIInB + UPI + COB/CIL touch), not amendment smuggled into closed 20.45/20.100 without version bumps.
5. **v0 vs extension** — state explicitly: minimal conformance may omit IIInB+UPI; honest path = 20.17 tag + clarification only.

---

### Summary verdict

| Element | Verdict |
|---------|---------|
| Problem statement | **Accept** — real gap, correctly identified |
| IIInB non-learning + clarify fork | **Accept** |
| UPI / USP direction | **Accept with refinement** — integrator + COB-backed store, not ninth basin unless you need basin lifecycle |
| GB role | **Accept** — veto on commit, not rule DB |
| “Path B” naming | **Reject** — rename before 20-series |
| Request for comment | **Appropriate** — no premature HLR commitment |

**I would not finalize UPI spec until:** (a) Path naming fixed, (b) persistence owner chosen (COB vs standalone), (c) IIInB read API sketched in one page, (d) v0 optional vs required profile declared.

---

If you want a next artifact, the highest-value one is a **one-page interface box diagram** (InB → IIInB ↔ USP read → UPI write ← clarification ← CIL; GB veto on UPI commit) plus a **minimal `20.xxx_upi_requirements.md` skeleton** with Purpose, Non-Goals, and HLR placeholders only — no full taxonomy yet. That gives CP something concrete without reopening the closed dual-pipeline stack.
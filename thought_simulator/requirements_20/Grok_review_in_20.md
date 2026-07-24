Reviewing Track H definitions and related constraints to ground the assessment.
Overall: the **IIInB / USP / UPI** design is sound, lean, and fits the TS model. It is implementable as a **rule-table + audit-log** subsystem, not an inference engine. The main gaps are **spec detail**, not architectural holes.

---

## Executive scorecard

| Dimension | Assessment | Confidence |
|-----------|------------|------------|
| **Completeness (concept)** | ~85% — roles and boundaries are right; wire-level detail missing | High |
| **Implementable** | Yes — v0 is straightforward deterministic code | High |
| **Compute / power cost** | Very low when profile-enabled; **zero** when disabled | High |
| **Robustness** | Strong if bounded; weak if rules/clarifications are unbounded | Medium (needs caps) |
| **Tractable** | High — three roles, narrow writes, no `semantic_core` touch | High |
| **Expandable** | Yes — versioned rules/profiles; watch scope creep | Medium |
| **Visible / debuggable** | Good fit with existing audit/MB model; schemas not written yet | Medium |

---

## Are we missing anything?

**Not missing at the architecture level.** CP v2 + `20.190` / `20.500` §7.7 cover placement, authority, and IMR separation.

**Missing for implementation** (Track H spec work):

| Gap | Why it matters |
|-----|----------------|
| **Wire schemas** | `usp_rule`, `iiinb_repair_record`, `upi_commit_event`, `clarification_event` (CIL) |
| **InB → IIInB ordering** | Sign `InB (surface) → IIInB (semantic repair) → RB` |
| **Rule matching model** | How segments are bounded, longest-match vs priority, conflict resolution |
| **Rule scope & precedence** | User vs conversation vs channel; newer rule vs older; GB override |
| **Caps** | Max rules per profile, max repairs per turn, max clarification loops per conversation |
| **TCU budget** | IIInB min/typ/max per `20.150`; UPI amortized on rare clarification events |
| **Profile gate** | `profile_enabled` binding to execution signature; disabled = skip IIInB entirely |
| **Escalation vs IB path** | Unknown shorthand → CIL/UPI; `MI_INCOMP` → IB-Creation-Request (two wires, one program) |
| **GB veto criteria** | Unsafe rule classes (e.g. rules that rewrite factual claims, policy bypass) |
| **USP lifecycle** | Revoke, expire, supersede, export/redaction under COB |
| **Replay fixtures** | Track H test class: rule apply, unknown escalate, UPI commit, re-read next turn |
| **MB hooks** | Which fields MB exports for repair/clarification debugging |

None of these challenge the three-role model. They are the normal next layer of a bounded subsystem spec.

---

## Is it implementable?

**Yes.** v0 is a small, deterministic pipeline:

```
InB output → IIInB:
  load USP snapshot (read-only)
  scan bounded segments
  for each segment: lookup rule table
    match → emit repair tag + resolved ref
    no match → emit escalation ref (no guess)
  append iiinb_repair_record

Clarification (async, human-paced):
  CIL clarification_event → UPI:
    validate + GB gate
    append USP rule version (COB pins version)
    append upi_commit_record
```

No ML, no embeddings, no latent state. That matches TS determinism and replay requirements.

**Implementation risk is low** if you keep IIInB to **explicit pattern → replacement/expansion** rules, not open-ended “interpret this.” The moment rules become fuzzy matchers, cost and debuggability rise fast — that would be scope creep.

---

## Cost: power, hardware, execution speed

**This is one of the cheapest subsystems you could add.**

| Component | When it runs | Typical cost |
|-----------|--------------|--------------|
| **IIInB** | Every turn (if profile on) | Small table scans over bounded segments × bounded rules — microseconds to low milliseconds on CPU |
| **USP read** | When IIInB runs | One snapshot load per cycle — negligible vs OB/TB |
| **UPI** | Only after clarification | Human-timescale; amortized cost ≈ 0 per turn |
| **Disabled profile** | Never | **Zero** — skip IIInB entirely |

Why it stays cheap:

1. **Optional** — not on the hot path for deployments that don't enable it.
2. **No GPU / no model inference** — pure deterministic logic.
3. **No `semantic_core` writes** — no extra Merge/Truth/Done work from Track H itself.
4. **No Pipeline B coupling** — no OpBeh/OuB/IMR overhead from input repair.
5. **Clarification is rare** in steady state — users train the profile once, then IIInB hits cache-like rule lookups.

Compared to OB → TR → TB → Merge, IIInB should be **noise in the TCU budget** if capped (e.g. max 128–512 rules, max 32 segment spans per turn). Add explicit TCU rows in Track H per `20.150`.

**Hardware:** runs on the same CPU footprint as InB. No special accelerators. Edge/mobile viable if rule store stays small.

---

## Robustness

**Strong properties (by design):**

- **No guessing** — unknown → clarify, not silent repair.
- **Single writer** — UPI alone commits USP; GB can veto.
- **Read-only USP at intake** — IIInB cannot corrupt the profile mid-read.
- **Deterministic replay** — same InB output + same USP version → same repair tags.
- **IMR separation** — output errors don't redefine input repair.

**Risks to bound in spec:**

| Risk | Mitigation |
|------|------------|
| Rule conflicts (two rules match one span) | Deterministic precedence: specificity > scope > version > rule_id sort |
| Rule explosion over long conversations | Cap + COB compaction/archival policy |
| Clarification storms (user never confirms) | Max pending clarifications; degrade to tagged unknown + IB path |
| Bad rule poisons future turns | GB veto + rule revocation + replay tests per rule version |
| Cross-turn stale rules | USP version pin on `iiinb_repair_record`; replay uses pinned version |
| Adversarial shorthand | Treat like `MI_NOISE`/bounds — segment length caps, reject malformed rules at UPI |

With caps and audit, robustness is **high**. Without caps, clarification loops and rule tables can grow without bound — that's an ops problem, not a design flaw.

---

## Tractability

**High.** The program decomposes cleanly:

| Role | Inputs | Outputs | Complexity |
|------|--------|---------|------------|
| IIInB | InB text, USP snapshot | Repair tags | O(rules × segments) |
| USP | UPI commits | Rule set | Storage + versioning |
| UPI | Clarification payload | USP append | O(1) per event |

No feedback loop inside Track H (IIInB doesn't call UPI; UPI doesn't call IIInB same-turn). Cross-turn loop is intentional and human-gated:

```
turn N: unknown → clarify
turn N+1: UPI wrote rule → IIInB applies
```

That is **easy to reason about, test, and replay** — much more tractable than IMR Type B partial A-cycles.

---

## Expandability

**Expandable along safe axes:**

- New **rule types** (versioned schema): expansion, alias, disambiguation pick-list (post-clarification only).
- New **scopes**: user, household, project, conversation.
- New **profiles**: strict (escalate always) vs permissive (apply only exact rules).
- **COB export** of USP for portability / backup.

**Do not expand into:**

- Live intent structuring (that's TR/OB/TB).
- Routing contracts (RB/SRP/`exec_plan`).
- Learning from implicit behavior without clarification (breaks CIL/GB governance).

The catalog's "is not" lines are the guardrails. Expandability is good **if USP stays a rule store**, not a second meaning pipeline.

---

## Visibility and debuggability

**Good fit** with TS audit culture. Track H should emit append-only records analogous to `messy_input_record` and `imr_record`:

| Record | Carries |
|--------|---------|
| `iiinb_repair_record` | `usp_version_ref`, matched `rule_id[]`, segment spans, repair outcome, escalation refs |
| `upi_commit_record` | clarification ref, new rule id, GB approval, superseded rules |
| `usp_version_record` | COB pin, rule count, content hash |

**MB** can surface: rules applied, escalations, cap hits, GB denials — same pattern as suppressed IMR triggers.

**Replay/debug:** golden fixtures are simple:

1. No USP → escalation only  
2. USP with rule → deterministic repair tag  
3. UPI commit → next-turn IIInB applies new rule  
4. Conflicting rules → deterministic winner  

**Visibility gap today:** schemas aren't normative yet, so debug story is designed but not wired. Low effort to close.

---

## Bottom line

| Question | Answer |
|----------|--------|
| Missing anything fundamental? | **No** — missing spec artifacts, not missing primitives |
| Implementable? | **Yes** — rule table + audit log; no exotic tech |
| Low cost? | **Yes** — optional, CPU-trivial, zero when disabled; UPI is rare |
| Robust? | **Yes with caps** — no-guess + GB gate is the right robustness model |
| Tractable? | **Yes** — narrow writes, clear turn boundaries, no IMR coupling |
| Expandable? | **Yes** — versioned rules/scopes; guard against meaning-pipeline creep |
| Visible/debuggable? | **Yes** — fits append-only audit + MB; needs Track H schemas |

**Recommendation:** Proceed with Track H. Treat v0 as a **bounded rule engine**, not an inference basin. The highest-leverage spec items are: caps, rule precedence, three audit record schemas, and one replay test class. Those turn a good conceptual design into a provably cheap, robust, debuggable subsystem.

If you want execution next, I'd open Track H with a minimal `20.xxx` skeleton covering those five items before any implementation in 40-series.
Checking how deeply Type B and the A→B→A loop are embedded in approved requirements before commenting.
CP’s proposal is **architecturally coherent** and matches the stance you described (“monitor / one-shot flag, not a baked-in A→B→A controller”). But it is **not** a small non-goal tweak. It would **reverse a chunk of normative work you already approved** in the dual-pipeline program.

## Where CP is right

The control-loop concern is real. A mandated IMR Type B path implies:

- `CorrectionTrigger` schema and supervisory queue semantics  
- Bounded partial A-cycles and `target_field_ids[]` routing  
- Caps, cooldowns, dedup, `max_correction_depth_per_cycle`  
- E3 replay (20.207) and Class 3b/5 fixtures (20.36)  
- TR `tr_needs_update` scheduling (20.37)

That *is* a feedback controller, even if bounded. If your product intent is **mostly single-pass A→B with observability**, CP’s framing — **IMR as monitor + optional flag, not closed loop** — is the sane way to say that.

Type A-only v0 also fits the deterministic/no-latent-inference posture better: expression retry on the **same** `semantic_snapshot_ref` is a B-side retry, not meaning recompute.

## Where CP understates the conflict

Today’s specs **do** define systematic correction as normative, not implementation-specific:

| Doc | What’s already in scope |
|-----|-------------------------|
| **20.45** | ~33 Type B / `CorrectionTrigger` touchpoints; Type B is first-class, not optional |
| **20.206** | Equivalence class **E3** (post-correction meaning) |
| **20.207** | E3 replay rules; Type B regen constraints |
| **20.36** | **Class 3b** (Type B + partial A-cycle); Class 5 includes Type B IMR |
| **20.37** | IMR Type B schedules bounded TR recompute |
| **20.500** | IMR Type B agreed in §5 registry; program closed with this model |

So CP’s suggested line:

> “Any use of IMR to trigger recompute is implementation-specific and out of normative scope”

would **contradict** existing HLRs unless you run a deliberate **scope rollback** (version bumps + CP Edit List), not a paragraph in non-goals.

## “Type A only in v0” — what it would actually mean

If you adopt CP’s v0 shape honestly:

**Keep (minimal IMR):**
- Taxonomy reduced to **Type A + Type C** (safety still needs GB), or Type A monitoring only if you also defer Type C  
- `evaluator_signal` ingestion, `imr_record` append to `exec_trace`  
- Logging, caps as **observability**, not mandatory recompute scheduling  
- Optional status flags (`imr_recommend_recompute`) — **non-normative consumer** may act once; TS core does not close the loop  

**Demote to extension profile (not PoC conformance):**
- Type B and `CorrectionTrigger`  
- E3 replay as required equivalence class (keep E1/E2)  
- 20.36 Class 3b (and Type B portions of Class 5)  
- 20.37 §3.4 TR recompute-on-trigger  

**Align with your IIInB / input-repair thread:** input semantic repair stays **out of v0** either way; that’s orthogonal but consistent with “no systematic feedback.”

## On CP’s “tiny non-goals” draft

Good **intent**, wrong **weight class**. A single non-goal in 20.45 without editing cross-refs creates a **normative contradiction**. Minimum honest change set:

1. **20.45** — v0 scope: Type A required; Type B/C → extension or safety-only per your call  
2. **20.206** — E3 optional / extension-only  
3. **20.207** — E3 demoted; E2 (regeneration) can stay as PoC minimum  
4. **20.36** — Class 3b optional; Class 3a (Type A retry) remains  
5. **20.37** — IMR Type B TR scheduling → extension  
6. **20.500** — new **follow-on program slice** (don’t silently edit a `complete` hub without changelog + approval)

That’s a **Track D-style scope decision**, not a freshness polish.

## Recommendation

**Agree with CP’s product stance; treat it as a new GATE, not a footnote.**

| If you want… | Do this |
|--------------|---------|
| Lock “no mandated feedback loop” now | CP Edit List for v0 IMR scope rollback across 20.45 / 20.206 / 20.207 / 20.36 / 20.37 + 20.500 follow-on note |
| Avoid reopening closed docs immediately | Record **architecture decision ADR**: “v0 = Type A IMR monitor; Type B/E3/Class 3b = extension profile” and **don’t implement** Type B in 40-series until specs catch up |
| Worst path | Add non-goals only → harnesses and HLRs disagree; Stage 5 consistency wins on paper, product intent loses |

**Practical v0 story (single-pass, honest):**

> Pipeline A → `mtp_update` → Pipeline B → IMR evaluates → append `imr_record` + optional flags. **No normative requirement** that cycle N+1 re-runs A because of cycle N’s IMR. External operator or future **IMR-B profile** may do one-shot recompute; not TS core conformance.

That preserves IMR, kills the convergent controller, and matches what you said you’re okay with.

## Bottom line

- **Yes** to CP: IMR as monitor / one-shot signal, not mandated A→B→A loop.  
- **No** to treating it as three lines in 20.45 — the loop is already woven through six docs.  
- **Yes** to drafting the non-goals **as part of a bounded v0 scope package** if you want it locked while it’s fresh.

If you want to proceed, the next step is a short **CP Edit List** (“IMR v0 = Type A only; demote B/C/E3/Class 3b to extension”) rather than prose-only agreement. I can draft that list against the current HLR IDs when you’re ready.
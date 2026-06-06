Checking for new dual-pipeline, IMR, and TrigRB definitions in the repo before recommending refactor vs dual pipeline.
# Architectural Review: Refactor vs Dual Pipeline

**Decision context:** Pipeline 1 = meaning construction (today's basin/MTP path); Pipeline 2 = execution/realization (SRP cold + TrigRB / OpBeh / OBG / XlateR / IMR hot).  
**Recommendation upfront:** **Yes — proceed with dual pipeline as the PoC vehicle.** Refactor can wait until the concept is validated and you have trace evidence.

---

## 1. Dual-Pipeline Runtime Penalty — Negligible?

**Mostly agree, with PoC-scoped conditions.**

Your cost model is sound:

| Component | Path | Expected cost |
|-----------|------|----------------|
| Pipeline 1 | Hot, per meaning-construction cycle | Dominant (same as today) |
| SRP | Cold, epoch compile | Amortized; not per turn |
| TrigRB | Hot, trigger detection | Small — pattern/table scan over bounded triggers |
| SRP table lookup | Hot | O(1)–O(log n) |
| OpBeh + OBG + XlateR | Hot | Depends on realization depth |

For PoC, Pipeline 2 is **not a second LLM pass** and should sit in the **microseconds–low-milliseconds** range if XlateR is deterministic template/map application, not open-ended generation. That matches existing TS budgeting intuition (RB ≈ 5% of cycle; OuB isolated at output boundary per 20.30).

**Conditions where penalty is not negligible:**

- XlateR performs unbounded transform work (generation, search, inference).
- Pipeline 2 runs per-token instead of per-expression-boundary.
- TrigRB scans large unstructured trigger sets without bounds.
- SRP tables are not pre-indexed and lookups degrade to linear search.

**PoC viability:** **Not threatened**, provided you cap XlateR to table-driven realization and bound TrigRB trigger cardinality. Document those as explicit PoC constraints, not assumptions.

**Verdict:** **Agree** — negligible for PoC if Pipeline 2 stays lookup + bounded realization.

---

## 2. PoC Sufficiency — Does Dual Pipeline Prove TS?

**Agree on the core thesis; disagree that it proves the full TS architecture.**

A clean dual-pipeline PoC **would validate**:

- Meaning and expression can be separated.
- Realization can route over a large sparse compositional manifold.
- SRP can compile routing tables deterministically (cold path).
- Expression does not corrupt meaning (with metadata-only writes + boundary enforcement).
- Feedback can be explicit, gated, and auditable (IMR → trigger, not mutation).

That is the **central architectural claim** this expansion is making. If it works, the remaining work is largely **engineering and normative documentation**, not re-deriving the separation principle.

**What it does not fully validate** (conceptual blockers elsewhere):

| TS claim | Dual-pipeline PoC coverage |
|----------|---------------------------|
| Basin meaning construction (OB/RB/TB/ΔH%) at scale | Only as Pipeline 1 exists today — may be thin in PoC |
| Geometric substrate (DCB, trajectory invariants) | Peripheral unless P1 exercises it |
| GB supervisory under load | Not exercised by P2 alone |
| Messy-input stability (20.17) | P1 concern |
| Full conversation lifecycle (CIL/COB/COP) | Partial |
| TCU/cost superiority claims | Needs measured P1+P2 envelope |

**Verdict:** **Agree** that dual pipeline is **sufficient to validate the meaning/expression separation + table-driven realization thesis**. **Do not claim** it validates the entire geometric + semantic TS program end-to-end. State PoC scope explicitly: *"validates Execution Manifold; Pipeline 1 assumed or stubbed at agreed depth."*

---

## 3. Stability — Pipeline 2 Feedback Delay via IMR

**Agree, conditional on explicit bounds.**

The path:

```text
OuB → IMR → semantic correction trigger → Pipeline 1 TR (Thought Router)
```

is **logically delayed feedback**, not uncontrolled coupling — **if** IMR is strictly:

- Read-only on MTP semantic content.
- Trigger-only output (no meaning writes).
- Bounded in frequency and depth per cycle/conversation.

This aligns with 20.10 invariants: no unbounded recursion (HLR-20.010-012), GB bounded intervention, deterministic safe boundaries.

**Stability risks to gate in PoC design:**

1. **Oscillation:** IMR trigger → P1 TR recompute → new OuB output → IMR trigger again.  
   **Mitigation:** `max_correction_depth_per_cycle`, cooldown epochs, trigger deduplication on `(exec_trigger_id, routing_epoch_id)`.

2. **TR cascade:** IMR triggers Thought Router, which may route to basin-OB processing — that is intentional but costly.  
   **Mitigation:** IMR emits typed triggers (`correction_class`, `severity`); P1 TR ignores low-severity triggers unless GB/policy permits.

3. **Epoch skew:** P2 realizes against epoch N while IMR triggers P1 against stale tables.  
   **Mitigation:** IMR tags triggers with `routing_epoch_id`; P1 rejects mismatched epochs.

**Verdict:** **Agree** — Pipeline 2 does not inherently introduce uncontrolled feedback loops. IMR-mediated feedback is **safe if bounded and trigger-only**. Add 3–5 explicit stability HLRs before PoC commit.

---

## 4. TP/MTP Visibility — Metadata-Only Correct?

**Strong agree. Required, not optional.**

Pipeline 2 writing only:

- `opbeh_id`, `obg_id`, `xlater_id`, `routing_epoch_id`, `exec_trigger_id`

…and **not** stance, goals, semantic fields, or MTP content is the correct enforcement of meaning/expression separation. It matches:

- HLR-20.010-006 (deterministic core vs output variability).
- HLR-20.110-004 (OuB does not alter upstream meaning construction).
- HLR-20.020-012 (non-overlapping primitive authority).

**One refinement:** place these fields in a dedicated **`TP.exec_meta`** (or `TP.realization_meta`) envelope, not scattered in core semantic slots. That makes audit queries and replay diffs trivial and prevents accidental consumption by P1 RB/TR routing.

**Caveat:** P1 may **read** `exec_trigger_id` as a routing *signal* (like `tr_needs_update`), but must not treat it as semantic evidence. Document read-only trigger consumption separately from semantic field mutation.

**Verdict:** **Agree** — metadata-only visibility is required for determinism and auditability.

---

## 5. Decision Guidance — Refactor vs Dual Pipeline

**Explicit recommendation: Dual pipeline now; refactor later only if validated and justified.**

| Criterion | Refactor (single pipeline) | Dual pipeline (PoC) |
|-----------|---------------------------|----------------------|
| Architectural honesty | Merges two concerns under shared symbols | Keeps meaning and realization inspectably separate |
| Falsifiability | Hard to tell whether bugs are P1 or P2 | Clear per-pipeline traces |
| Namespace risk | High — OB/TR/RB already normative | Low — OpBeh/TrigRB/XlateR/SRP are distinct |
| 20-series disruption | Requires rewriting 20.30, 20.37, 20.40, 20.50 | Additive 20.4x/20.55 cluster |
| Premature optimization | High — entanglement before proof | Low — prove separation first |
| Playground fit (40.xx) | Blurs playground vs canon boundaries | Natural 40.1xx execution playground |

Refactoring today would force you to **re-host realization inside a pipeline already dense with basin semantics**, before you have trace proof that the Execution Manifold works. That inverts the project's usual flow (20 → 40 prototype → validate → promote).

**Verdict:** **Agree** — dual pipeline is the correct next step. Refactor only after:

1. PoC demonstrates stable separation across N scripted scenarios.
2. Trace logs show zero semantic-field writes from P2.
3. Integration cost of two pipelines exceeds maintainability threshold (unlikely in PoC phase).

---

## 6. Additional Concerns Before Commit

### Must resolve before PoC kickoff

**A. Namespace (blocking for 20-series hygiene)**

| Proposed | Canonical PoC name | Never reuse |
|----------|---------------------|-------------|
| OB | `OpBeh` | Object Basin (20.40) |
| TR | `XlateR` | Thought Router (20.37) |
| RB | `TrigRB` | Relational Basin (20.50) |

Freeze a one-page **symbol table** in 40.1xx disclaimers and 20.190 draft entries.

**B. IMR primitive — currently underspecified**

Define before build:

- Full name and type (monitor vs basin vs routine).
- Inputs: OuB output artifact only, or also `TP.exec_meta`?
- Outputs: trigger schema (`trigger_type`, `severity`, `routing_epoch_id`, `correction_target`).
- Authority: may it set `tr_needs_update` in P1, or only emit a separate `correction_pending` flag?
- GB gate: which trigger classes require GB approval?

Without IMR HLRs, the feedback path is the highest stability risk in the design.

**C. Epoch lifecycle**

Specify:

- SRP compile trigger (manual, MTP delta threshold, scheduled).
- Atomic table swap semantics.
- In-flight TP behavior during epoch rollover.
- Replay binding: `(routing_epoch_id, table_hash)` in trace.

**D. OuB role split**

Clarify whether OuB is:

- Terminal renderer of P2's resolved `(OpBeh, OBG, XlateR)` address, or
- Upstream of P2 (emitting content IMR monitors).

Your feedback path implies **OuB → IMR**, so OuB likely sits at P2 output. Document that OuB consumes exec address + MTP read-only, consistent with 20.110.

**E. Invalid combination matrix**

SRP must emit or reference a policy of illegal `(opbeh_id, obg_id, xlater_id)` triples (safety, incoherent register/behavior pairings). Without it, sparse manifold claims are incomplete.

**F. PoC scope statement (falsifiability)**

Write a short **in-scope / out-of-scope** block:

- **In:** separation, routing, epoch determinism, IMR bounded feedback, metadata-only writes.
- **Out:** full GB load, production TCU proof, complete basin catalog, 50-series implementation.

**G. Canonical trace extension**

20.36 stage order needs P2 stages appended after `output_realization` (or as sub-stages): `trigrb_detect → exec_lookup → xlate_realize → oub_emit → imr_evaluate → [optional p1_correction_trigger]`.

**H. Thought Router coexistence**

IMR → "Pipeline 1 TR" must mean **Thought Router routine** (20.37), not XlateR. PoC docs should always say `ThoughtRouter` or `TP.TR recompute`, never bare `TR`.

### Lower priority (can run parallel to PoC)

- Discourse/goal manager ownership of `obg_id` selection (CIL vs COP vs policy table).
- GB policy injection into SRP compile inputs.
- COB/OBG boundary (conversation object vs register identity).

---

## Summary Decision Table

| Question | Answer |
|----------|--------|
| 1. Runtime penalty negligible? | **Yes**, with bounded XlateR and TrigRB |
| 2. Dual pipeline proves TS thesis? | **Yes** for separation + realization; **no** for full TS program |
| 3. IMR feedback safe? | **Yes**, with depth/epoch/cooldown bounds |
| 4. Metadata-only TP/MTP correct? | **Yes** — use `TP.exec_meta` envelope |
| 5. Dual pipeline correct next step? | **Yes** — refactor later if needed |
| 6. Ready to commit? | **Yes, after** namespace table, IMR spec, epoch rules, PoC scope doc |

---

## Commit Checklist (minimal gate)

1. Symbol table frozen (`OpBeh`, `OBG`, `XlateR`, `TrigRB`, `SRP`, `IMR`).
2. IMR trigger schema + bounded feedback HLRs drafted.
3. `TP.exec_meta` field envelope defined (5 metadata fields).
4. Epoch swap + replay binding specified.
5. PoC in/out scope paragraph written.
6. 40.1xx playground disclaimer: *non-authoritative execution-manifold prototype*.

I agree with your direction. Dual pipeline is the architecturally honest, inspectable, falsifiable vehicle. Commit once the six checklist items above are pinned — not after a monolithic refactor of today's single pipeline.
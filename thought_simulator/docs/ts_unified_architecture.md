# TS Unified Architecture (Exploratory)

**Document ID:** `docs/ts_unified_architecture`  
**Version:** 0.1  
**Date:** 2026-06-06  
**Status:** Exploratory — not prescriptive  
**Author:** Grok (architectural analysis for TS research)

---

## Disclaimer

This document describes a **hypothetical unified Thought Simulator (TS) architecture** — a single-pipeline design with internal phases, not two physically separated pipelines.

It is an **intellectual exercise** to:

- clarify the conceptual space TS occupies,
- understand what a from-scratch unified design might look like,
- identify invariants that must survive any future refactor, and
- inform long-term architectural thinking.

**This document does not change project direction.**

The active implementation path is the **dual-pipeline Execution Manifold**:

- **Pipeline A** — meaning construction (basin/MTP path; today's core)
- **Pipeline B** — execution/realization (OpBeh × OBG × XlateR + SRP + TrigRB + IMR)

Readers should treat this unified sketch as a **counterfactual reference model**, comparable to a textbook "alternative design" chapter — useful for reasoning, not for implementation without explicit human approval and PoC validation.

---

## 1. Purpose and Scope

### 1.1 What this document is

A clean description of what TS **might** look like if meaning construction and execution/realization were integrated into **one orchestrated control loop** over **one layered state object**, rather than two inspectable pipelines.

### 1.2 What this document is not

- Not a proposal to implement unified architecture now
- Not a replacement for 20-series normative requirements
- Not a 40-series playground artifact (see §8 for placement)
- Not an endorsement of end-to-end latent/ML training through meaning fields
- Not permission to collapse namespace distinctions (`basin.OB` vs `exec.OpBeh`, `ThoughtRouter` vs `XlateR`, `RelationalBasin` vs `TrigRB`)

### 1.3 Relationship to the Execution Manifold PoC

The dual-pipeline PoC is the **contract discovery phase**. It proves:

- meaning and expression can be separated in practice,
- SRP can compile routing tables deterministically off the hot path,
- realization can traverse a sparse compositional manifold,
- IMR-mediated feedback can remain bounded and auditable.

A future unified refactor — if ever undertaken — would **package proven boundaries** into one runtime. It would not eliminate those boundaries.

---

## 2. Design Premise: Unified but Not Entangled

A credible unified TS architecture is:

```text
One runtime  +  One state object  +  Hard internal phases  +  Partitioned write authority
```

It is **not**:

```text
One flat state blob  +  Interleaved meaning/realization writes  +  Implicit feedback
```

TS principles from 20.10 and 20.30 that constrain any unified design:

| Principle | Unified interpretation |
|-----------|------------------------|
| Determinism (HLR-20.010-001) | Identical inputs, MTP state, seed, and epoch → identical outputs |
| Fixed phase ordering (HLR-20.010-004, -066) | Phases are sequential within a cycle; "unified" ≠ "unordered" |
| Meaning/expression separation (HLR-20.010-006) | Logical separation via envelopes; not architectural pipeline split |
| No latent entanglement (20.30 §1.2) | OpBeh/OBG/XlateR are explicit registry IDs, not learned latent heads |
| GB bounded supervision (HLR-20.010-018–025) | Unified planner must not become a monolithic god module |
| Seed boundary (20.30 §1.7) | Variability confined to expression phase only |

---

## 3. Unified Architecture Overview

### 3.1 Single integrated control loop

One **TS Cycle Orchestrator** drives four internal phases per cycle:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                         UNIFIED TS CYCLE N                              │
├─────────────────────────────────────────────────────────────────────────┤
│  Phase 1 — INTERPRETATION (semantic construction)                       │
│    InB → RelationalBasin → ObjectBasin → DCB → ThoughtRouter → TB      │
│    → Merge → MTP semantic_core update                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  Phase 2 — PLANNING (realization planning)                              │
│    Unified Discourse Manager (UDM):                                     │
│      trigger detection + SRP table lookup + PlanningDecision commit     │
├─────────────────────────────────────────────────────────────────────────┤
│  Phase 3 — REALIZATION (expression)                                     │
│    OuB: MTP (read-only) + exec_plan + seed → surface artifact           │
├─────────────────────────────────────────────────────────────────────────┤
│  Phase 4 — FEEDBACK (mediated correction)                               │
│    IMR: evaluate mismatch → CorrectionTrigger (bounded, auditable)      │
│    → schedule gated re-entry to Phase 1 (next cycle or partial pass)    │
└─────────────────────────────────────────────────────────────────────────┘
         ▲
         │  cold path (not per turn)
         │
    SRP Compiler ──► routing tables + routing_epoch_id
```

### 3.2 Cold vs hot path (unchanged role)

Even in a unified design, **SRP does not run per turn on the hot path**.

| Component | Path | Role |
|-----------|------|------|
| SRP Compiler | Cold | Compile routing tables from MTP structure, GB policy, OpBeh/OBG/XlateR registries |
| UDM Plan Resolver | Hot | O(1) table lookup + deterministic trigger match |
| ObjectBasin / ThoughtRouter | Hot | Semantic construction (Phase 1) |
| OuB | Hot | Expression only (Phase 3) |

"SRP integrated into the planner" means the **hot planner reads SRP products** — not that compilation merges into per-turn inference.

---

## 4. Single Shared State Representation

### 4.1 Layered state, one substrate

Unified TS uses one `TP` / `MTP` pair, partitioned into **logical envelopes** with **distinct write authorities**:

```text
TP / MTP
├── semantic_core          # Phase 1 writers only
│   ├── propositions, stance, affect, intent
│   ├── ΔH%, lineage, semantic tags
│   └── TP.TR (Thought Router semantic routing vector)
│
├── exec_plan              # Phase 2 writers only
│   ├── opbeh_id
│   ├── obg_id
│   ├── xlater_id
│   ├── routing_epoch_id
│   └── planning_decision_ref
│
├── exec_trace             # Phase 3–4 writers only
│   ├── exec_trigger_id
│   ├── oub_artifact_ref
│   └── imr_evaluation_record
│
└── supervisory            # GB at safe boundaries only
    ├── policy markers
    ├── blocked_relation_logs
    └── correction_trigger_queue
```

### 4.2 InteractionMode (unified mode concept)

A single struct correlates facets that are separate axes in the dual-pipeline PoC:

```text
InteractionMode {
  semantic_mode_id,     # task/epistemic context (from MTP / COB / CIL)
  obg_id,               # register / voice identity
  opbeh_id,             # discourse act structure
  xlater_id,            # mapping routine
  routing_epoch_id      # table era binding
}
```

`semantic_mode_id` and `obg_id` may correlate but are **not identical**:

- semantic mode = what kind of reasoning or task context applies,
- OBG = who/what voice the surface realization uses.

### 4.3 PlanningDecision (inspectable unified routing artifact)

Every Phase 2 resolution produces an explicit record:

```text
PlanningDecision {
  cycle_id,
  semantic_snapshot_ref,    # read-only hash of semantic_core at plan time
  opbeh_id,
  obg_id,
  xlater_id,
  routing_epoch_id,
  trigger_id,               # from internalized TrigRB
  rationale_codes[],        # deterministic reason codes
  invalid_triple_rejected   # boolean + reject_code if applicable
}
```

This preserves the dual-pipeline guarantee: routing remains **explicit and inspectable**, not implicit drift.

---

## 5. Module Integration: What Collapses, What Stays Separate

### 5.1 Collapse / merge map

| Dual-pipeline PoC module | Unified architecture home |
|--------------------------|---------------------------|
| Pipeline A orchestrator | Phase 1 (Interpretation) — largely unchanged |
| TrigRB | UDM.trigger_detector |
| OpBeh/OBG/XlateR resolver | UDM.plan_resolver |
| Pipeline B orchestrator | Cycle Orchestrator phases 2–4 |
| IMR | Phase 4 (Feedback) — logic preserved, deployment internalized |
| SRP | Cold SRP Compiler — **does not merge into hot path** |
| Separate exec metadata store | `TP.exec_plan` + `TP.exec_trace` envelopes |

### 5.2 What must not collapse

| Module | Reason to keep distinct |
|--------|-------------------------|
| Object Basin (20.40) | Basin evidence extraction; not OpBeh |
| Relational Basin (20.50) | Topology, split/merge; not TrigRB |
| Thought Router (20.37) | `TP.TR` semantic routing; not XlateR |
| GB (20.80) | Supervisory isolation; planner must not absorb GB |
| OuB (20.110) | Seed-bound expression; sole variability entry |
| ΔH% / TB / Merge | Meaning construction authority |

Namespace discipline remains permanent. Unification merges **orchestration**, not **semantic roles**.

### 5.3 Unified Discourse Manager (UDM)

The primary integration hub in a unified design. UDM subsumes:

1. **Trigger detection** (former TrigRB) — match semantic events against trigger tables
2. **Plan resolution** — map `(semantic_snapshot, trigger, policy)` → `(OpBeh, OBG, XlateR)` via SRP tables
3. **OBG authority** — validate or select register identity (may read CIL/COB context)
4. **IMR interface** — accept OuB artifacts for mismatch evaluation; emit `CorrectionTrigger` events

UDM is **table-driven and deterministic**. It does not perform open-ended inference.

### 5.4 Thought Router extension (optional deep integration)

A further refactor step extends `TP.TR` with realization hints:

```text
TP.TR = {
  // existing semantic routing fields (20.37)
  stance, intent, affect, routing_semantics, ...

  // optional realization hints (resolved by UDM in Phase 2)
  realization_hints: {
    preferred_obg_id?,
    opbeh_family?,
    xlater_class?
  }
}
```

UDM **materializes** hints into concrete registry IDs. Semantic routing and realization planning become **facets of one planning story** while remaining **separate fields with separate writers**.

---

## 6. Phase-by-Phase Behavior

### 6.1 Phase 1 — Interpretation

Equivalent to today's meaning construction pipeline. Authority unchanged:

- Relational Basin routes lane topology
- Object Basin extracts evidence; sets `tr_needs_update` when needed
- DCB observes trajectory geometry (ephemeral, no TP writes)
- Thought Router recomputes `TP.TR` when stale
- TB interprets; Merge updates MTP `semantic_core`

**Invariant:** Phase 1 completes before Phase 2 begins. Phase 2 reads `semantic_core` through a **read-only snapshot** (copy-on-write view or snapshot hash).

### 6.2 Phase 2 — Planning

UDM executes:

```text
1. trigger_set = trigger_detector(semantic_snapshot, exec_trigger_tables[epoch])
2. for each trigger in trigger_set (deterministic order):
     decision = plan_resolver(semantic_snapshot, trigger, SRP_tables[epoch], policy)
3. commit exec_plan envelope + PlanningDecision record
4. pin routing_epoch_id for remainder of cycle
```

Invalid `(OpBeh, OBG, XlateR)` triples are rejected with fixed audit codes — same invalid-combination matrix as dual-pipeline PoC.

### 6.3 Phase 3 — Realization

OuB consumes:

- `MTP.semantic_core` (read-only)
- `TP.exec_plan` (opbeh_id, obg_id, xlater_id)
- seed (expression variability only)

OuB does **not** write semantic fields. Output goes to `exec_trace.oub_artifact_ref`.

### 6.4 Phase 4 — Feedback

IMR evaluates OuB artifact against semantic snapshot and exec plan:

```text
CorrectionTrigger {
  trigger_type,
  severity,
  routing_epoch_id,
  semantic_snapshot_ref,
  exec_plan_ref,
  cause_codes[],
  max_depth_remaining
}
```

Triggers queue for **bounded** re-entry to Phase 1 (typically Thought Router recompute or targeted basin pass — not full unbounded cascade).

IMR may be **represented** as a discourse event type, but its **mediation rules** remain distinguishable: no direct `semantic_core` writes.

---

## 7. Invariants That Must Survive Any Unified Refactor

These are the non-negotiable correctness conditions. Violating any one means the design is entangled, not unified.

### 7.1 Write authority partition

```text
semantic_core writers ∩ exec_plan writers = ∅
exec_plan writers ∩ OuB variability logic = ∅
IMR writers ∩ semantic_core writers = ∅
```

### 7.2 Phase immutability within a cycle

Realization and expression phases cannot mutate `semantic_core` committed in the same cycle's interpretation phase.

### 7.3 Explicit routing artifacts

Every realization resolution produces a `PlanningDecision` with `rationale_codes`. No silent defaults.

### 7.4 SRP off hot path

Table compilation never blocks per-turn execution. Epoch publish is atomic.

### 7.5 Epoch coherence

All exec fields carry `routing_epoch_id`. Stale epoch → reject or deterministic fallback with audit code.

### 7.6 IMR bounded feedback

- `max_correction_depth_per_cycle`
- trigger deduplication on `(exec_trigger_id, routing_epoch_id)`
- cooldown epochs for repeated mismatch classes
- no unbounded Phase 1 re-entry (HLR-20.010-012)

### 7.7 Seed boundary

Seed influences Phase 3 only. No seed-dependent branches in Phase 1 or Phase 2.

### 7.8 Replay equivalence

**Acceptance criterion for any unified refactor:**

```text
replay(unified_trace).semantic_core
  ==
replay(dual_pipeline_trace).pipeline_a_semantic_core
```

Stripping `exec_plan` and `exec_trace` from a unified trace must yield a Pipeline A replay identical to the dual-pipeline PoC.

### 7.9 Namespace discipline

Permanent qualified symbols:

| Basin / meaning layer | Execution layer |
|-----------------------|-----------------|
| Object Basin (`OB`) | OpBeh |
| Thought Router (`TP.TR`) | XlateR |
| Relational Basin (`RB`) | TrigRB (absorbed into UDM in unified form) |

---

## 8. Risks and Failure Modes

| Risk | Failure mode | Detection |
|------|--------------|-----------|
| **Planner monolith** | UDM absorbs GB, basin routing, and policy — single point of failure | TCU overrun; unclear audit trail |
| **Silent semantic drift** | Phase 2/3 writes stance or goals "for convenience" | Replay diff shows semantic_core changed without Phase 1 |
| **False simplicity** | Team treats one diagram as one writer | Invariant violations in 30-series replay tests |
| **Implicit feedback** | Mode changes without `CorrectionTrigger` | Missing IMR audit records |
| **Epoch races** | Mixed-era table lookups in one cycle | `routing_epoch_id` mismatch in trace |
| **OuB seed leak** | Seed influences Thought Router | Nondeterministic semantic replay |
| **Verification collapse** | Cannot isolate interpretation vs planning bugs | Failed replay equivalence suite |
| **Namespace regression** | `OB`/`TR`/`RB` reused for execution primitives | Glossary collision; 20.200 traceability breaks |

The largest risk is **authority blur** — one state object inviting one writer too many.

---

## 9. Comparison: Dual Pipeline vs Unified Architecture

| Dimension | Dual pipeline (PoC path) | Unified architecture (this document) |
|-----------|--------------------------|--------------------------------------|
| **Primary goal** | Validate contracts; maximize inspectability | Packaging convenience; reader simplicity |
| **Failure isolation** | High — per-pipeline traces | Lower — requires envelope/phase tags |
| **Implementation complexity** | Two orchestrators | One orchestrator, stricter phase guards |
| **Conceptual clarity for new readers** | Two diagrams | One diagram (invariants harder) |
| **Normative 20-series impact** | Additive (20.4x, 20.55) | Consolidation + rewrite risk |
| **Long-term correctness** | Logical separation explicit | Logical separation via envelopes |
| **Recommended timing** | Now | Post-PoC + verification + equivalence proof |

---

## 10. Long-Term Evolution: Plausible but Not Inevitable

### 10.1 Is unified architecture a plausible evolution?

**Yes**, after dual-pipeline PoC succeeds and 30-series verification proves:

1. metadata-only writes from execution layer,
2. SRP epoch coherence,
3. IMR bounded feedback stability,
4. replay equivalence between representations.

### 10.2 Is unified architecture inevitable?

**No.** For a deterministic, auditable system, **logical separation is a feature**, not technical debt.

A mature TS may deploy as:

- **one physical runtime** (unified orchestrator), with
- **permanent logical decomposition** in traces, tests, and docs (dual-pipeline audit lens).

This is analogous to compiler phases or database transaction stages: one process, hard internal boundaries.

### 10.3 Recommended evolution path

```text
Now        → Dual-pipeline Execution Manifold PoC (40.1xx)
PoC pass   → Normative 20.4x / 20.55 contract docs
Verify     → 30-series replay + equivalence criteria defined
Optional   → Unified orchestrator refactor (if economics justify)
Permanent  → Logical meaning/realization separation in verification
```

Refactor only if:

- dual orchestration cost is measurably painful, **and**
- replay equivalence is proven, **and**
- team maintains phase/envelope discipline under unified codebase.

Do **not** refactor for diagram simplicity alone.

---

## 11. Refactor Gate Checklist (Future Reference)

Before any unified refactor is approved:

- [ ] Dual-pipeline PoC passes scripted scenario classes (stable meaning, flexible expression, bounded IMR correction)
- [ ] Zero semantic_core writes from Pipeline B demonstrated in traces
- [ ] `PlanningDecision` / `exec_plan` schema frozen
- [ ] Invalid triple matrix defined and tested
- [ ] Epoch swap semantics specified and replay-tested
- [ ] IMR trigger taxonomy and depth bounds verified
- [ ] Replay equivalence test: unified trace semantic_core == dual Pipeline A trace
- [ ] Namespace table in 20.190 updated
- [ ] 20.36 canonical trace extended with unified phase tags
- [ ] Explicit human approval for direction change from dual-pipeline to unified

---

## 12. Document Placement in TS Hierarchy

| Tier | Status of this document |
|------|-------------------------|
| 20_requirements | **Not authoritative** — exploratory only |
| 40_playground | PoC implements dual pipeline, not this document |
| 50_design | May inform future 50.xx orchestrator design after PoC |
| docs/ | Correct home for non-normative architectural exploration |

Related authoritative references:

- [20.10_ts_architectural_principles.md](../20_requirements/20.10_ts_architectural_principles.md)
- [20.30_ts_functional_model.md](../20_requirements/20.30_ts_functional_model.md)
- [20.37_thought_router_tr_specification.md](../20_requirements/20.37_thought_router_tr_specification.md)
- [Grok_review_in_20.md](../20_requirements/Grok_review_in_20.md) — Execution Manifold review

---

## 13. Summary

A unified TS architecture is **feasible in principle** and **desirable only under strict conditions**. It looks like:

- **one runtime, one layered state, four hard phases**;
- **UDM** absorbing TrigRB and plan resolution;
- **SRP** remaining cold;
- **IMR** remaining mediated;
- **meaning/expression separation** preserved logically via envelopes, not via pipeline split.

The dual-pipeline Execution Manifold remains the correct implementation path. This document maps the adjacent architectural territory so future decisions are informed, not improvised.

---

*End of exploratory document.*
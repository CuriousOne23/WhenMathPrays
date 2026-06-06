# TS Unified Architecture (Exploratory)

**Document ID:** `docs/ts_unified_architecture`  
**Version:** 0.4  
**Date:** 2026-06-06  
**Status:** Exploratory — defensive prior art publication (public MIT repo)
**Author:** Grok (architectural analysis for TS research)  
**Project:** WhenMathPrays / Thought Simulator (open research)

---

## Reader's Guide

This document intentionally uses **TS terminology** in later sections to maintain continuity with the existing 20-series and dual-pipeline PoC. **It is not a normative specification.** No HLRs are defined here; nothing in this file overrides 20-series requirements.

**How to read it:**

| If you want… | Read |
|--------------|------|
| A from-scratch mental model (no basin jargon) | §2 Pure Conceptual Overview |
| The unified architecture as one control loop | §3 Single Control Loop |
| How this maps onto today's TS modules | §17 TS Continuity Mapping |
| What must never break in any refactor | §9 Invariants |
| Defensive prior art / patent-blocking scope | Defensive Publication section + §20 Design Space Coverage |
| Concrete walkthroughs | §19 Worked Examples |
| Term definitions in one place | §21 Glossary |
| Whether to actually build this | **Don't** — dual-pipeline PoC is the active path (Reader's Guide box above) |

The level of detail is deliberate: it supports **falsifiability** for researchers and **defensive publication** for the open project — establishing public, timestamped prior art for unified TS architectures without mandating implementation.

### Why this is not the implementation path

We build **dual-pipeline** (Pipeline A + Pipeline B) for the PoC because it is inspectable, falsifiable, and avoids namespace entanglement. This unified document exists to map the adjacent design space and establish **public prior art** for collapsed or optimized variants — not to redirect implementation. If a unified runtime is ever adopted, it must pass replay equivalence (§9.8) and the refactor gate (§16).

---

## Disclaimer

This document describes a **hypothetical unified Thought Simulator (TS) architecture** — a single control loop over one layered state object, not two physically separated pipelines.

It is an **intellectual exercise** to:

- clarify the conceptual space TS occupies,
- understand what a from-scratch unified design might look like,
- identify invariants that must survive any future refactor, and
- inform long-term architectural thinking.

**This document does not change project direction.**

The active implementation path is the **dual-pipeline Execution Manifold**:

- **Pipeline A** — meaning construction
- **Pipeline B** — execution/realization (OpBeh × OBG × XlateR + SRP + TrigRB + IMR)

Readers should treat this unified sketch as a **counterfactual reference model** — useful for reasoning, not for implementation without explicit human approval and PoC validation.

---

## Defensive Publication and Prior Art Rationale

> **Note:** This section states project intent. It is not legal advice. Consult qualified counsel for patent strategy.

### Publication intent

This document is published openly and timestamped in the project repository to establish **public prior art** for unified Thought Simulator (TS) architectures and adjacent design space.

Publication intent includes, but is not limited to, documenting prior art for systems that:

- use a **single structured state** with logically separated meaning and expression layers;
- run a **unified control loop** with interpretation, planning, realization, and mediated feedback phases;
- integrate **behavior, identity, and mapping** as explicit native control dimensions (OpBeh, OBG, XlateR or equivalents);
- employ a **discourse manager** (UDM or equivalent) that performs trigger detection, policy gating, identity selection, plan resolution, and realization selection;
- integrate **cold-path routing-table compilation** (SRP or equivalent) with hot-path table lookup planning;
- maintain **replay equivalence** between unified traces and meaning-construction-only traces;
- enforce **write-authority partitions** so realization does not silently overwrite meaning;
- support **epoch-versioned routing tables** with deterministic fallback behavior;
- apply **bounded feedback mediation** (IMR or equivalent) without uncontrolled semantic drift.

### Why this matters for the project

The active implementation path is the **dual-pipeline Execution Manifold** (Pipeline A + Pipeline B). If dual-pipeline TS is released and succeeds, third parties may attempt to:

- collapse, fuse, or optimize the two pipelines into a unified runtime;
- patent the unified form or obvious rearrangements of the same invariants;
- restrict access to identity-aware, table-driven realization architectures derived from the same separation principles.

Publishing this unified architecture **before** such filings establishes that the design space was already publicly known — including the integration patterns, invariants, and subsystem structures — as part of an open research program.

This follows the same defensive pattern used by major open-source ecosystems: publish the general solution architecture openly so downstream innovation remains unencumbered by surprise patents on obvious unifications.

### Relationship to dual-pipeline prior art

Dual-pipeline and unified architectures are **two deployments of the same logical separation**:

| Logical separation | Dual-pipeline deployment | Unified deployment |
|--------------------|--------------------------|-------------------|
| Meaning construction | Pipeline A | Phase 1 (Interpretation) |
| Realization planning | Pipeline B (TrigRB + resolver) | Phase 2 (UDM) |
| Expression | OuB in Pipeline B | Phase 3 (Realization) |
| Mediated feedback | IMR across pipelines | Phase 4 (Evaluate) |

Prior art for unified integration is therefore **complementary** to dual-pipeline prior art, not a substitute. Both should remain publicly documented.

---

## 1. Purpose and Scope

### 1.1 What this document is

A description of what TS **might** look like if meaning construction and execution/realization were integrated into **one orchestrated control loop**, rather than two inspectable pipelines.

### 1.2 What this document is not

- Not a proposal to implement unified architecture now
- Not a replacement for 20-series normative requirements
- Not a 40-series playground artifact
- Not an endorsement of end-to-end latent/ML training through meaning fields
- Not a collapsed dual pipeline wearing a unified label — see §3

### 1.3 Relationship to the Execution Manifold PoC

The dual-pipeline PoC is the **contract discovery phase**. A future unified refactor — if ever undertaken — would **package proven boundaries** into one runtime. It would not eliminate those boundaries.

### 1.4 Defensive publication scope (summary)

This document serves three purposes simultaneously:

1. **Exploration** — map the conceptual space adjacent to the dual-pipeline design
2. **Invariant preservation** — record constraints any unified refactor must satisfy
3. **Defensive prior art** — establish public disclosure of unified TS architecture patterns (see Defensive Publication section above and §20)

---

## 2. Pure Conceptual Overview (From Scratch)

*This section describes the unified architecture without reference to basins, Thought Packets, or existing TS module names.*

### 2.1 Core idea

A **Cognitive Engine** maintains one **World State** and runs one **Control Loop** per interaction cycle. The World State has two logical layers that share one storage substrate:

- **Meaning Layer** — what is true, intended, uncertain, and structurally relevant
- **Expression Layer** — how that meaning is voiced, formatted, and surfaced

The engine never confuses the two layers, even though they live in one object.

### 2.2 Native control dimensions

Three explicit control axes govern expression (not meaning):

| Dimension | Question it answers |
|-----------|---------------------|
| **Behavior** | What discourse act? (explain, compare, classify, refuse, …) |
| **Identity** | In what register/voice? (scientific, casual, pedagogical, …) |
| **Mapping** | Which deterministic translation routine maps meaning → surface? |

A fourth meta-dimension binds them:

| Dimension | Question it answers |
|-----------|---------------------|
| **Epoch** | Which compiled routing-table era is authoritative? |

These are **registry IDs and table keys**, not latent embeddings.

### 2.3 One control loop, four responsibilities

Each cycle, the engine performs four responsibilities in order:

1. **Interpret** — update the Meaning Layer from input and prior state
2. **Plan** — select (Behavior, Identity, Mapping) from compiled tables + triggers
3. **Realize** — produce surface output from Meaning Layer (read-only) + plan + optional seed
4. **Evaluate** — detect mismatch; emit bounded correction signals; never silently rewrite meaning

A **Table Compiler** (offline) maintains routing tables from World State structure and policy. It does not run per cycle.

### 2.4 Central integrator: Discourse Manager

One module — the **Discourse Manager** — owns planning and discourse coordination:

- detects when expression should change or proceed,
- selects Behavior × Identity × Mapping,
- validates against policy and invalid-combination rules,
- hands off to the Realizer,
- receives evaluation feedback.

This is the conceptual heart of unification: **one planner, many facets**, table-driven, fully logged.

### 2.5 What "unified" means here

Unified means:

- one runtime,
- one World State object with layered write authority,
- one Discourse Manager coordinating expression decisions.

Unified does **not** mean:

- one undifferentiated state blob,
- free interleaving of meaning and expression writes,
- implicit feedback or silent drift.

---

## 3. Single Control Loop (Not a Collapsed Dual Pipeline)

A unified architecture is **not** "Pipeline A stacked on Pipeline B in one document." It is a **single cyclic controller** where interpretation, planning, realization, and feedback are **responsibilities of one loop**, not ownership of separate runtimes.

```mermaid
flowchart LR
  subgraph loop [Unified Control Loop — one runtime]
    direction TB
    WS[(World State\nlayered envelopes)]
    INT[Interpret]
    PLAN[Plan]
    REAL[Realize]
    EVAL[Evaluate]
    INT --> PLAN --> REAL --> EVAL
    EVAL -.->|bounded correction signal| INT
    INT <--> WS
    PLAN <--> WS
    REAL <--> WS
    EVAL <--> WS
  end
  TC[[Table Compiler\ncold path]] -.->|epoch tables| PLAN
  IN([Input]) --> INT
  REAL --> OUT([Surface Output])
```

**Conceptual difference from dual pipeline:**

| Dual pipeline | Unified loop |
|---------------|--------------|
| Two orchestrators, two trace namespaces | One orchestrator, phase-tagged trace |
| Separation is **architectural** (visible in deployment) | Separation is **logical** (visible in envelopes + write guards) |
| Inspectability via pipeline boundary | Inspectability via replay equivalence (§9.8) |

The four phases (Interpret → Plan → Realize → Evaluate) are **responsibilities within the loop**, analogous to lexer → parser → codegen in a compiler. Compiler phases are not "dual pipelines collapsed" — they are one pass with hard internal order.

---

## 4. Design Premise: Unified but Not Entangled

```text
One runtime  +  One state object  +  Hard phase order  +  Partitioned write authority
```

Constraints (stated generically; TS-specific mapping in §17):

| Constraint | Unified interpretation |
|------------|------------------------|
| Determinism | Identical inputs, state, seed, epoch → identical outputs |
| Phase order | Phases are sequential within a cycle; unified ≠ unordered |
| Meaning/expression separation | Logical envelopes; not architectural pipeline split |
| No latent entanglement | Control dimensions are explicit IDs, not learned latent heads |
| Bounded supervision | Discourse Manager must not absorb all policy authority |
| Seed boundary | Variability confined to realization only |

---

## 5. Unified Architecture Overview (TS-Oriented)

### 5.1 Four phases per cycle

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    UNIFIED TS CYCLE N (one orchestrator)                │
├─────────────────────────────────────────────────────────────────────────┤
│  Phase 1 — INTERPRETATION                                               │
│  Phase 2 — PLANNING (UDM)                                               │
│  Phase 3 — REALIZATION (OuB)                                            │
│  Phase 4 — FEEDBACK (IMR)                                               │
└─────────────────────────────────────────────────────────────────────────┘
         ▲
         │  cold path
    SRP Compiler ──► routing tables + routing_epoch_id
```

Phase-by-phase module detail appears in §8. TS module names appear in §17.

### 5.2 Cold vs hot path

| Component | Path | Role |
|-----------|------|------|
| SRP Compiler | Cold | Compile routing tables from semantic structure + policy + registries |
| UDM Plan Resolver | Hot | O(1) lookup + deterministic trigger match |
| Interpretation phase | Hot | Meaning construction |
| OuB | Hot | Expression only |

"SRP integrated into the planner" means the hot planner **reads SRP products** — not that compilation runs per turn.

---

## 6. Single Shared State Representation

### 6.1 Layered state, one substrate

```text
World State (TP / MTP)
├── semantic_core          # Phase 1 writers only
├── exec_plan              # Phase 2 writers only
├── exec_trace             # Phase 3–4 writers only
└── supervisory            # Policy supervisor at safe boundaries only
```

See §17 for field-level mapping to TS schemas.

### 6.2 InteractionMode

```text
InteractionMode {
  semantic_mode_id,     # task/epistemic context
  obg_id,               # register / voice
  opbeh_id,             # discourse act
  xlater_id,            # mapping routine
  routing_epoch_id
}
```

`semantic_mode_id` and `obg_id` correlate but are not identical.

### 6.3 PlanningDecision

Every planning resolution produces an explicit, inspectable record:

```text
PlanningDecision {
  cycle_id,
  semantic_snapshot_ref,
  opbeh_id, obg_id, xlater_id,
  routing_epoch_id,
  trigger_id,
  rationale_codes[],
  invalid_triple_rejected
}
```

---

## 7. Module Integration and UDM

### 7.1 Collapse / merge map

| Dual-pipeline PoC module | Unified architecture home |
|--------------------------|---------------------------|
| Pipeline A orchestrator | Phase 1 (Interpretation) |
| TrigRB | UDM.trigger_detector |
| OpBeh/OBG/XlateR resolver | UDM.plan_resolver + identity_selector + realization_selector |
| Pipeline B orchestrator | Cycle orchestrator phases 2–4 |
| IMR | Phase 4 — via UDM.imr_interface |
| SRP | Cold compiler — **not** hot path |
| Separate exec metadata store | exec_plan + exec_trace envelopes |

### 7.2 What must not collapse

Meaning-layer primitives (Object Basin, Relational Basin, Thought Router, GB, ΔH%, TB, Merge) retain distinct authority. Unification merges **orchestration**, not **semantic roles**. See §17.

### 7.3 Unified Discourse Manager (UDM) — internal structure

UDM is the integration hub. Internally it decomposes into six components with **strict call order** and **separate audit records**:

```mermaid
flowchart TB
  subgraph udm [Unified Discourse Manager — Phase 2]
    TD[1. trigger_detector]
    PG[2. policy_gate]
    IS[3. identity_selector]
    PR[4. plan_resolver]
    RS[5. realization_selector]
    IMR[6. imr_interface]
    TD --> PG --> IS --> PR --> RS
  end
  SNAP[(semantic_snapshot\nread-only)] --> TD
  SNAP --> IS
  SNAP --> PR
  TRIG[(trigger_tables)] --> TD
  SRP[(SRP_tables\nrouting_epoch_id)] --> PR
  SRP --> RS
  POL[(GB / policy)] --> PG
  RS --> PLAN[(exec_plan +\nPlanningDecision)]
  OUB_OUT[OuB artifact] --> IMR
  IMR --> CT[CorrectionTrigger queue]
```

```text
UDM
├── 1. trigger_detector      # Match semantic events → TriggerSet (deterministic order)
├── 2. policy_gate             # Filter triggers against GB/policy; emit reject codes
├── 3. identity_selector       # Resolve or validate obg_id (register/voice)
├── 4. plan_resolver           # Map (snapshot, trigger, epoch) → candidate triple
├── 5. realization_selector    # Materialize xlater_id + opbeh_id; validate triple matrix
└── 6. imr_interface           # Accept OuB artifact; emit CorrectionTrigger; no meaning writes
```

**Decision model (Phase 2):**

```text
1. triggers = trigger_detector(semantic_snapshot, trigger_tables[epoch])
2. triggers = policy_gate(triggers, policy)           # may drop triggers with audit
3. for t in triggers (deterministic order):
     obg_id  = identity_selector(snapshot, t, context)
     triple  = plan_resolver(snapshot, t, obg_id, SRP_tables[epoch])
     triple  = realization_selector(triple, invalid_matrix)
     commit PlanningDecision + exec_plan envelope
4. pin routing_epoch_id for remainder of cycle
```

**Relationship to semantic mode:**

- `semantic_mode_id` lives in `semantic_core` (Phase 1 product).
- `identity_selector` **reads** semantic mode; it does not write it.
- Semantic mode constrains **which OBG IDs are legal**, not which one is automatically selected.
- Selection is table-driven: `(semantic_mode, trigger, policy) → obg_id` via SRP-compiled index.

**Relationship to SRP tables:**

| Table | Produced by SRP | Consumed by |
|-------|-----------------|-------------|
| `trigger_index` | semantic structure patterns | trigger_detector |
| `plan_index` | (semantic_mode, trigger) → triple candidates | plan_resolver |
| `invalid_triple_matrix` | policy + registry | realization_selector |
| `obg_legality_index` | semantic_mode → allowed obg_ids | identity_selector |

SRP publishes all tables under one `routing_epoch_id`. UDM pins epoch at cycle start.

**UDM invariants:**

- Table-driven only; no open-ended inference on hot path
- TCU-bounded; degrades deterministically on overload
- Does not write `semantic_core`
- Does not absorb GB policy authority — `policy_gate` reads GB product, does not replace GB
- Every selection produces `PlanningDecision` with `rationale_codes`

### 7.4 Optional Thought Router extension

`TP.TR` may carry realization **hints** (not IDs) that UDM materializes in Phase 2. Hints are written in Phase 1; concrete IDs are written in Phase 2. Separate writers, one planning story.

---

## 8. Phase-by-Phase Behavior

### 8.1 Phase 1 — Interpretation

Updates `semantic_core` only. Phase 2 reads via read-only snapshot. Phase 1 completes before Phase 2 begins.

### 8.2 Phase 2 — Planning

UDM executes decision model (§7.3). Invalid triples rejected with fixed audit codes.

### 8.3 Phase 3 — Realization

OuB: `semantic_core` (read-only) + `exec_plan` + seed → surface artifact in `exec_trace`.

### 8.4 Phase 4 — Feedback

IMR via `UDM.imr_interface`: mismatch → `CorrectionTrigger` → bounded re-entry to Phase 1 next cycle. No direct `semantic_core` writes.

---

## 9. Invariants That Must Survive Any Unified Refactor

1. **Write authority partition** — semantic / exec_plan / exec_trace / supervisory writers are disjoint
2. **Phase immutability** — later phases cannot mutate same-cycle semantic_core
3. **Explicit routing artifacts** — every resolution produces PlanningDecision + rationale_codes
4. **SRP off hot path** — compilation never blocks per-turn execution
5. **Epoch coherence** — all exec fields carry routing_epoch_id; stale epoch → reject or audited fallback
6. **IMR bounded feedback** — depth limits, dedup, cooldown; no unbounded re-entry
7. **Seed boundary** — seed affects realization only
8. **Replay equivalence** — stripping exec envelopes from unified trace ≡ Pipeline A replay (dual-pipeline PoC)
9. **Namespace discipline** — meaning-layer and execution-layer symbols never alias

---

## 10. Risks and Failure Modes

| Risk | Failure mode |
|------|--------------|
| Planner monolith | UDM absorbs GB + basin routing |
| Silent semantic drift | Phase 2/3 writes meaning fields |
| False simplicity | One diagram → one writer mentally |
| Implicit feedback | Mode changes without CorrectionTrigger |
| Epoch races | Mixed-era lookups in one cycle |
| Seed leak | Seed influences interpretation or planning |
| Verification collapse | Cannot isolate phase bugs |
| Namespace regression | OB/TR/RB reused for execution primitives |

The largest risk is **authority blur**.

---

## 11. Learning and Training Implications

*Exploratory — describes design space, not TS commitment.*

A unified architecture changes **where** learning hooks attach, not whether TS permits end-to-end latent training through meaning fields.

### 11.1 TS-native learning (determinism-preserving)

| Target | Mechanism | Path |
|--------|-----------|------|
| Routing tables | SRP recompile from annotated MTP structure | Cold |
| OpBeh/OBG/XlateR registries | Split/merge/deprecate with alias maps | Cold |
| Invalid triple matrix | Policy update + verification | Cold |
| Trigger definitions | Registry evolution + golden replay | Cold |
| IMR thresholds | Supervised threshold tuning against logged triggers | Cold / offline |

TS-native learning **updates compiled artifacts and registries**, then verifies via replay. Meaning-layer determinism is preserved.

### 11.2 ML-hybrid learning (fork, not default TS)

A unified loop is *architecturally* more tempting for end-to-end training because one state object exists. That path implies:

- differentiable or RL-updated planner weights,
- joint loss over semantic correctness + voice consistency + realization quality,
- risk of violating seed boundary and write-authority partition.

**This is a different system** — call it TS-ML fork, not TS refactor. The unified document assumes **table-driven UDM**, not learned latent control heads.

### 11.3 Implication summary

| Approach | Compatible with TS invariants? |
|----------|-------------------------------|
| SRP table updates from logged traces | Yes |
| Registry evolution (OBG split/merge) | Yes |
| Behavior cloning on PlanningDecision logs | Yes, if hot path stays table lookup |
| End-to-end RL through semantic_core | No (without abandoning TS determinism claims) |

---

## 12. Concurrency and Parallelism

Unified architecture does not require serial **implementation**, only serial **phase authority** within a cycle.

### 12.1 Safe parallelism

| Parallelism | Constraint |
|-------------|------------|
| Lane-parallel interpretation (Phase 1) | Merge serializes; semantic_core commit at phase end |
| Prefetch SRP tables for epoch N+1 | While cycle runs on epoch N |
| OuB realization pipelining | Phase 3 may stream output; exec_trace append-only |
| Batch IMR evaluation | Phase 4 may evaluate multiple artifacts; triggers queued deterministically |

### 12.2 Unsafe parallelism

| Parallelism | Why unsafe |
|-------------|------------|
| Plan while interpreting same cycle | Violates phase immutability |
| Realize while planning same cycle | exec_plan not yet committed |
| IMR writes semantic_core concurrently | Violates write authority |
| Parallel UDM selections without ordering | Nondeterministic tie-break |

### 12.3 Deterministic ordering rule

Any parallel work must **reduce to a canonical serial order** in the trace. Replay must reconstruct that order from `(cycle_id, phase, seq)`.

---

## 13. Memory and Long-Term State

Unified architecture does not collapse memory tiers — it **tags** them in one World State.

### 13.1 Memory classes

| Class | Content | Writer | Persistence |
|-------|---------|--------|-------------|
| **Working semantic** | Current cycle semantic_core | Phase 1 | Per conversation session |
| **Working exec** | exec_plan, exec_trace | Phases 2–4 | Per cycle / per expression tick |
| **Episodic** | PlanningDecision log, CorrectionTrigger log | Append-only | Replay horizon |
| **Semantic memory** | Stable facts, commitments in MTP | Phase 1 via Merge | Long-term |
| **Identity persistence** | OBG registry + conversation-scoped obg_id history | Cold registry + COB/CIL context | Long-term |
| **Routing memory** | SRP tables per epoch | SRP Compiler | Versioned; epoch-addressable |

### 13.2 Unified vs dual-pipeline memory difference

In dual pipeline, exec metadata is physically separable (Pipeline B store). In unified design, exec envelopes sit beside semantic envelopes in one object — but **write authority and retention policy** remain distinct.

Compaction and replay-horizon rules apply per envelope, not per object.

### 13.3 Identity persistence

`obg_id` may persist across cycles as a **conversation preference** without becoming semantic truth. Distinction:

- "User prefers casual register" → identity persistence (exec/COB layer)
- "User believes X" → semantic memory (semantic_core)

Collapsing these is a primary long-term failure mode.

---

## 14. Comparison: Dual Pipeline vs Unified Architecture

| Dimension | Dual pipeline (PoC path) | Unified architecture |
|-----------|--------------------------|----------------------|
| Primary goal | Validate contracts; maximize inspectability | Packaging; single-loop mental model |
| Separation mechanism | Architectural (two pipelines) | Logical (envelopes + phases) |
| Failure isolation | High | Medium — needs phase tags |
| "Feels like" | Two systems cooperating | One engine, four responsibilities |
| Normative 20-series impact | Additive | Consolidation risk |
| Replay audit lens | Per-pipeline traces | Replay equivalence to Pipeline A |
| Recommended timing | **Now** | Post-PoC + verification |

---

## 15. Long-Term Evolution

**Plausible after PoC — not inevitable.** A mature TS may run one physical orchestrator while retaining dual-pipeline decomposition in verification traces permanently.

Refactor only if dual orchestration cost is painful **and** replay equivalence is proven **and** envelope discipline holds in code.

---

## 16. Refactor Gate Checklist

- [ ] Dual-pipeline PoC passes scenario classes
- [ ] Zero semantic_core writes from Pipeline B in traces
- [ ] PlanningDecision / exec_plan schema frozen
- [ ] Invalid triple matrix tested
- [ ] Epoch swap replay-tested
- [ ] IMR bounds verified
- [ ] Replay equivalence: unified semantic_core == Pipeline A
- [ ] Namespace table updated
- [ ] Explicit human approval for direction change

---

## 17. TS Continuity Mapping

*This section bridges the pure model (§2) to existing TS terminology. It is a Rosetta stone, not the architecture itself.*

| Pure concept (§2) | TS module / artifact |
|-------------------|----------------------|
| World State | TP / MTP with layered envelopes |
| Meaning Layer | semantic_core |
| Expression Layer | exec_plan + exec_trace + OuB output |
| Interpret | InB → Relational Basin → Object Basin → DCB → Thought Router → TB → Merge |
| Plan | UDM (Phase 2) |
| Realize | OuB (Phase 3) |
| Evaluate | IMR (Phase 4) |
| Table Compiler | SRP |
| Behavior | OpBeh |
| Identity | OBG |
| Mapping | XlateR |
| Policy supervisor | GB (safe boundaries) |

| Principle source | Reference |
|------------------|-----------|
| Architectural principles | 20.10 |
| Functional model | 20.30 |
| Thought Router | 20.37 |
| Object Basin | 20.40 |
| Relational Basin | 20.50 |
| OuB | 20.110 |
| Execution Manifold review | [Grok_review_in_20.md](../20_requirements/Grok_review_in_20.md) |

---

## 18. Document Placement

| Tier | Status |
|------|--------|
| 20_requirements | Not authoritative |
| 40_playground | Dual-pipeline PoC, not this document |
| 50_design | May inform post-PoC orchestrator design |
| docs/ | Correct home for exploratory architecture |

---

## 19. Worked Examples

*Concrete scenarios illustrating the unified architecture. Names are exemplary; registries and tables are illustrative.*

### 19.1 Example A — One turn through the unified control loop

**Setup:** `routing_epoch_id = 7`. User input: *"Why does water expand when it freezes?"*

| Step | Phase | Action | State effect |
|------|-------|--------|--------------|
| 1 | Interpret | Ingest input; basin path extracts evidence; Thought Router updates semantic routing | `semantic_core` updated: proposition set, epistemic stance = explanatory, `semantic_mode_id = SCIENCE_QA` |
| 2 | Plan | UDM `trigger_detector` fires `TRIGGER_EXPLAIN_REQUEST` | — |
| 3 | Plan | `identity_selector`: `(SCIENCE_QA, trigger) → obg_id = OBG_PEDAGOGIC` | — |
| 4 | Plan | `plan_resolver` + `realization_selector`: triple `(OpBeh_EXPLAIN, OBG_PEDAGOGIC, XlateR_PLAIN_PHYSICS)` | `exec_plan` committed; `PlanningDecision pd-42` logged |
| 5 | Realize | OuB maps meaning → surface using triple + seed | `exec_trace.oub_artifact_ref` set; user sees plain-language explanation |
| 6 | Evaluate | IMR: no mismatch (surface matches meaning plan) | No `CorrectionTrigger` |

**Key prior-art points demonstrated:** single cycle, four phases, meaning updated only in Phase 1, execution metadata only in Phases 2–4, SRP tables read but not compiled per turn.

### 19.2 Example B — UDM selecting OpBeh × OBG × XlateR under policy gate

**Setup:** Same epoch 7. `semantic_mode_id = FAMILY_CHAT`. Trigger: `TRIGGER_COMPARE_OPTIONS` (user asks to compare two vacation choices).

```text
1. trigger_detector → { TRIGGER_COMPARE_OPTIONS }
2. policy_gate → pass (no safety block)
3. identity_selector:
     input:  semantic_mode=FAMILY_CHAT, conversation obg_preference=OBG_CASUAL
     output: obg_id=OBG_CASUAL
4. plan_resolver (SRP plan_index[epoch=7]):
     (FAMILY_CHAT, TRIGGER_COMPARE_OPTIONS, OBG_CASUAL)
       → candidates: [
            (OpBeh_COMPARE, OBG_CASUAL, XlateR_CONVERSATIONAL),
            (OpBeh_COMPARE, OBG_CASUAL, XlateR_BULLET)
          ]
5. realization_selector:
     policy: family mode disallows XlateR_BULLET
     → select (OpBeh_COMPARE, OBG_CASUAL, XlateR_CONVERSATIONAL)
     → PlanningDecision { rationale_codes: [RC_MODE_FAMILY, RC_COMPARE_ACT] }
6. exec_plan committed with routing_epoch_id=7
```

**Rejected alternate:** `(OpBeh_COMPARE, OBG_CASUAL, XlateR_BULLET)` — blocked by `invalid_triple_matrix` / policy gate, not silent fallback.

### 19.3 Example C — Replay equivalence (unified trace vs meaning-only trace)

**Setup:** Two traces of the same conversation through cycle 12.

**Unified trace** contains:

- `semantic_core_12` (propositions, stance, ΔH%, Thought Router fields)
- `exec_plan_12` (opbeh_id, obg_id, xlater_id, routing_epoch_id=7)
- `exec_trace_12` (oub artifact, IMR record)
- `PlanningDecision pd-88`

**Meaning-only trace** (Pipeline A / dual-pipeline PoC):

- `semantic_core_12` only — no exec envelopes

**Replay equivalence test:**

```text
strip(unified_trace, exec_plan, exec_trace, PlanningDecision)
  → semantic_replay_A

replay(meaning_only_trace) → semantic_replay_B

assert semantic_replay_A == semantic_replay_B
```

**Failure illustration (what prior art prevents):** If Phase 3 (Realize) silently wrote `stance=CONVERSATIONAL` into `semantic_core`, the strip-and-replay test would fail — detecting expression→meaning corruption. Unified architectures that lack this test are a distinct, inferior design space.

---

## 20. Design Space Coverage

This section defines the **design space** publicly disclosed by this document. It is intended to foreclose patent claims on obvious rearrangements of the same architectural ideas.

### 20.1 Core design space (unified TS family)

A system falls within this disclosed design space if it implements **all** of the following:

1. **Single structured state** — one primary state object (or equivalent) holding both meaning and expression-related data
2. **Logical meaning/expression separation** — distinct write authorities or envelopes; expression does not silently overwrite meaning
3. **Explicit control dimensions** — behavior (discourse act), identity (register/voice), and mapping (translation routine) as first-class selectors, not implicit style tokens
4. **Unified control loop** — interpretation → planning → realization → mediated feedback within one orchestrated cycle (order may be serial; parallelism allowed only with canonical trace reduction per §12)
5. **Integrated discourse manager** — single planner module or equivalent coordinating trigger detection, policy gating, identity selection, plan resolution, and realization selection
6. **Cold-path routing compilation** — routing tables (or equivalent) compiled outside the per-turn hot path; hot path performs lookup only
7. **Epoch-versioned routing** — routing decisions bound to a compile epoch with deterministic stale-epoch behavior
8. **Inspectable planning artifacts** — each realization decision produces an explicit logged record with rationale codes (or equivalent)
9. **Replay equivalence** — meaning-layer replay invariant under stripping of execution envelopes (or equivalent isolation test)

### 20.2 Obvious variants also disclosed

The following rearrangements are **not novel** relative to this publication and are considered part of the same design space:

| Variant | Disclosed as |
|---------|--------------|
| Dual runtime → single runtime merge | §3, §14, §15 — same phases, different deployment |
| Renaming OpBeh/OBG/XlateR | §2 — Behavior/Identity/Mapping dimensions |
| Renaming UDM | §7.3 — Discourse Manager with six internal components |
| Renaming SRP | §5.2, §7.3 — Table Compiler / cold-path compiler |
| ML-trained planner on hot path | §11.2 — disclosed as TS-incompatible fork, not excluded from design space |
| Parallel phase execution | §12 — with canonical serial trace |
| Memory tier variations | §13 — working/episodic/semantic/identity/routing |
| Hint-based planning (materialized IDs) | §7.4 — Thought Router hints → UDM materialization |
| Feedback as discourse events | §8.4 — IMR mediation with bounded triggers |
| Invalid combination matrices | §7.3, §19.2 — policy-blocked triples |
| Identity persistence vs semantic belief | §13.3 — separate memory classes |

### 20.3 What lies outside this design space

Systems **outside** this disclosure (not blocked by this document alone) include:

- Pure end-to-end neural generation with no explicit behavior/identity/mapping selectors
- Systems with no meaning/expression write partition
- Systems with no cold-path routing compilation and no epoch semantics
- Systems with no replay equivalence or equivalent meaning-isolation test
- Unrelated basin-geometry correlators with no realization planning layer

### 20.4 Complementary design space (dual-pipeline TS)

Dual-pipeline TS — meaning construction pipeline + execution/realization pipeline with metadata-only cross-pipeline writes — is a **separate but complementary** public design path documented by the Execution Manifold PoC and related 20-series artifacts. Unified and dual-pipeline forms share logical separation; they differ in deployment topology.

**Defensive posture:** maintain public documentation for **both** topologies so neither can be patented as the "only" way to achieve TS-style meaning/expression separation.

---

## 21. Glossary

| Term | Definition |
|------|------------|
| **semantic_core** | Meaning-layer envelope: propositions, stance, goals, ΔH%, Thought Router fields; Phase 1 writers only |
| **exec_plan** | Execution-plan envelope: opbeh_id, obg_id, xlater_id, routing_epoch_id; Phase 2 writers only |
| **exec_trace** | Execution-trace envelope: OuB artifact refs, IMR records, exec_trigger_id; Phases 3–4 writers only |
| **supervisory** | Policy/supervision envelope: GB markers, blocked-relation logs, correction queue; safe-boundary writers only |
| **OpBeh** | Operational Behavior — discourse act structure (explain, compare, classify, …); explicit registry ID |
| **OBG** | Operational Behavior Group — register/voice identity (pedagogic, casual, scientific, …); explicit registry ID |
| **XlateR** | Translation Routine — deterministic mapping from meaning to surface for a given OBG; not Thought Router |
| **UDM** | Unified Discourse Manager — Phase 2 integrator (trigger, policy, identity, plan, realization, IMR interface) |
| **SRP** | Semantic Routing Planner — cold-path compiler producing epoch-versioned routing tables |
| **IMR** | Interpretation Mismatch Routine — Phase 4 bounded feedback; trigger-only, no semantic_core writes |
| **InteractionMode** | Correlated tuple: semantic_mode_id + obg_id + opbeh_id + xlater_id + routing_epoch_id |
| **PlanningDecision** | Inspectable audit record for each Phase 2 resolution, with rationale_codes |
| **routing_epoch_id** | Era binding for SRP-compiled tables; stale epoch → reject or audited fallback |
| **Replay equivalence** | Stripping exec envelopes from unified trace yields semantic replay identical to Pipeline A |
| **World State** | Generic term for TP/MTP layered substrate (§2, §6) |
| **Discourse Manager** | Generic term for UDM (§2); owns planning and discourse coordination |

---

## 22. Summary

A unified TS architecture is **one control loop with four responsibilities**, not two pipelines folded together. The Discourse Manager (UDM) is its heart — six internal components, table-driven, fully logged. Meaning/expression separation survives as **write authority over layered envelopes**, not as a deployment boundary.

The dual-pipeline Execution Manifold remains the correct **implementation** path. This document additionally serves as **defensive prior art** for the unified topology: complete conceptual architecture (§2–§3), UDM internals (§7.3), invariants (§9), worked examples (§19), and explicit design-space coverage (§20).

---

## Revision History

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-06-06 | Initial exploratory draft |
| 0.2 | 2026-06-06 | CP critique: pure overview (§2), control-loop diagram (§3), UDM expansion (§7.3), learning/concurrency/memory (§11–13), reader's guide, TS mapping isolated (§17) |
| 0.3 | 2026-06-06 | Defensive prior art: publication rationale, worked examples (§19), design-space coverage (§20); Jeff/CP patent-protection intent |
| 0.4 | 2026-06-06 | CP v0.2 review follow-up: UDM diagram (§7.3), glossary (§21), implementation-path summary (Reader's Guide) |

---

*End of exploratory document.*
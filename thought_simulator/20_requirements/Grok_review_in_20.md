Reviewing the existing 20-series architecture so the critique is grounded in your current documents.
# TS 20-Series Architectural Review: OB / OBG / TR / SRP Proposal

**Reviewer:** Grok  
**Scope:** Correctness, completeness, architectural coherence against current 20-series canon  
**Status:** Advisory — blocking namespace conflicts must be resolved before normative inclusion

---

## Executive Summary

The **conceptual decomposition** (structure → identity → translation → offline planning) is sound and aligns well with TS principles: determinism, auditability, hot/cold path separation, and sparse compositional growth.

The proposal is **not yet safe for 20-series inclusion** because it reuses three established primitive names — **OB**, **TR**, and **RB** — with incompatible meanings. In current canon:

| Symbol | Established meaning (20.20, 20.30, 20.37, 20.40, 20.50) | Proposed meaning |
|--------|----------------------------------------------------------|------------------|
| **OB** | Object/Observation Basin — lane-local evidence extraction, ΔH% | Operational Behavior — explain/compare/classify |
| **TR** | Thought Router — `TP.TR` semantic routing vector; TR routine lifecycle | Translation Routine — semantic mapping into OBG |
| **RB** | Relational Basin — topology, split/merge, OB firing order | Semantic trigger detector → `TP.rb_trigger_id` |

Until naming and layer placement are resolved, traceability, glossary, and verification will fracture. The ideas are worth keeping; the integration strategy needs redesign, not just new documents.

**Recommendation:** Treat this as a new **Execution Manifold** (or **Realization Layer**) sitting above meaning construction, with renamed symbols. Do not redefine basin primitives.

---

## 1. New Primitives — Definitions, Purpose, Boundaries

### What works

The four-way split is internally coherent:

```
SRP (offline)  →  routing tables + epoch
RB (hot)       →  trigger detection
TR (hot)       →  semantic mapping into register
OBG (overlay)  →  discourse/register identity
OB (hot)       →  structural behavior execution
```

Each axis has a clear "does / does not" boundary. OBG evolvability (split/merge/deprecate) matches how COB and IB registries already behave. SRP as a non-hot-path compiler respects HLR-20.010-004 (fixed phase ordering) and the inference-off-hot-path goal.

### Critical issues

**A. OB (Operational Behavior) vs Object Basin**

Current OB is a **basin primitive** — pattern detection, evidence extraction, TR-input emission. It does not "explain" or "classify" in the discourse sense; TB and OuB own interpretation and expression.

Your proposed OB reads like **expression-structure templates** or **OuB realization modes**, not basin correlators. Putting it in 20.40 would corrupt an existing normative module.

**B. TR (Translation Routine) vs Thought Router**

20.37 defines TR as the **exclusive writer of `TP.TR`**, consumed by RB for deterministic routing. Your TR writes `TP.tr_id` and `TP.ob_id` — a different contract entirely. Two "TR" modules cannot coexist without qualified naming (`TP.TR` vs `TP.exec_tr_id` or similar).

**C. OBG — strong and needed, but overlaps COB/COP**

OBG (scientific, casual, family, etc.) fills a real gap: **register/voice identity** as a first-class axis. COB owns conversation-object lifecycle; OuB owns expression realization. Neither currently owns "who is speaking as whom." OBG is the right concept; its boundary vs COB and CIL must be explicit.

**D. SRP — well-scoped**

SRP as "compiles routing tables from MTP semantic structure, never hot path" is architecturally clean and matches the routing-table concept in `00.10.50_TS_data_model.md`. Strong candidate for normative inclusion once boundaries are pinned.

### Verdict (Area 1)

| Primitive | Internal definition | 20-series ready? |
|-----------|--------------------|--------------------|
| OB (proposed) | Good internally | **No** — rename; not a basin |
| OBG | Good; fills gap | **Yes, with COB/CIL boundary doc** |
| TR (proposed) | Good internally | **No** — rename; conflicts with Thought Router |
| SRP | Good | **Yes** |

**Suggested renames (minimum):** `OpBeh` / `OpB`, `OBG` (keep), `XlateR` or `TRmap`, `SRP` (keep). If you keep `OB`, require qualified namespaces everywhere: `basin.OB` vs `exec.OpBeh`.

---

## 2. Process Flow Integration

### Proposed flow (restated)

```
OB = structural behavior
OBG = identity/register overlay
TR = semantic mapping into identity
SRP = compiles routing tables from MTP (offline)
RB = detects semantic triggers
TS core = executes composite address (OB, OBG, TR)
```

### Coherence assessment

The layering is **minimal and logically ordered** within the proposal. Cold compile → hot trigger → hot address resolution → hot execution is a standard, defensible pattern.

### Integration conflict with current canon

Existing normative cycle (20.30, 20.37):

```text
RB → OB(basin) → DCB observes → RB checks tr_needs_update
  → (if true) TR routine(Thought Router) → RB
```

Your flow uses the same symbols for different actors. These are **two pipelines**, not one:

| Layer | Current 20-series | Proposed addition |
|-------|-------------------|-------------------|
| Meaning construction | InB → RB → OB(basin) → TR(router) → TB → Merge → MTP | (unchanged) |
| Execution/realization | OuB (expression from MTP) | SRP → tables; RB(triggers) → composite(OpBeh, OBG, XlateR) |

**Recommendation:** Frame explicitly as a **second phase** or **OuB sub-pipeline**, not a replacement for the meaning-construction loop:

```text
[MTP finalized] → SRP(epoch N) compiles tables
[Per expression tick] → TriggerRB → resolve (OpBeh, OBG, XlateR) → TS-exec/OuB realize
```

Without this framing, 20.30 section 3 and 20.37's Semantic Interpretation Flow Contract become inconsistent.

### Verdict (Area 2)

Conceptually coherent **as a separate realization layer**. Not coherent **as a rewrite of existing OB/TR/RB flow**. Needs explicit dual-pipeline architecture in 20.10 and 20.30.

---

## 3. Communication Boundaries

### Proposed boundaries (evaluated)

| Actor | Reads | Writes | Assessment |
|-------|-------|--------|------------|
| SRP | MTP, GB policy, OpBeh/OBG/XlateR defs | routing tables, routing_epoch_id | **Clean** — classic offline compiler |
| SRP | Must not touch TP, basin-OB, basin-RB, XlateR execution | — | **Correct** |
| RB (proposed) | routing tables, semantic triggers | `TP.rb_trigger_id` | **Clean IF renamed** — not Relational Basin |
| XlateR | routing tables, OBG identity | `TP.tr_id`, `TP.ob_id` | **Needs field rename** — `TP.ob_id` collides with basin OB registry |
| Discourse/goal manager | — | `TP.obg_id` | **Underspecified** — no 20-series home yet |

### Gaps to close

1. **Who is "discourse/goal manager"?** Candidates: CIL (conversation integration), COP (propose-only), GB-supervised sub-module, or new `20.4x` Discourse Manager. Without placement, `TP.obg_id` writer authority is unenforceable (violates HLR-20.010-070).

2. **Epoch coherence.** When SRP publishes `routing_epoch_id`, hot-path readers must reject stale tables. Specify atomic swap, version pinning per TP/tick, and replay binding.

3. **Thought Router interaction.** If `TP.TR` (stance, intent, routing_semantics) influences trigger detection, define read-only consumption rules. Current RB already routes on `TP.TR` (HLR-20.050-021).

4. **GB policy input to SRP.** Align with HLR-20.010-018–025: SRP reads policy; GB does not compile tables at runtime.

### Verdict (Area 3)

Boundaries are **clean in the abstract** and **enforceable with renamed modules and explicit TP field schema**. Not enforceable while sharing OB/TR/RB names and `TP.ob_id` with basin semantics.

---

## 4. Address Space — Expandability, Size, Overlap

### Design: `ADDR = (OB_ID, OBG_ID, TR_ID)`

**Scalability:** Sound. Sparse realized subsets over a large ID space is the right model. Trillions of combinations cost nothing if storage is table-driven and hot path is O(1) lookup.

**Semantic cleanliness:** Allowing OB×OBG overlap is fine **if** axes are orthogonal:
- OpBeh = *what structural operation*
- OBG = *in which register/voice*
- XlateR = *which mapping routine*

Overlap across axes is composition, not duplication.

### Requirements to add

1. **Invalid triple registry** — some (OpBeh, OBG, XlateR) combinations must be explicitly illegal (safety, policy).
2. **Deprecation aliasing** — when OBG splits/merges, routing tables carry `alias_of` / `deprecated_by` for audit replay.
3. **Hierarchical IDs** — flat numeric IDs scale; structured IDs (tier + family + variant) aid traceability and SRP compilation.
4. **Collision with basin OB IDs** — if both manifolds use `OB_ID`, namespace separation is mandatory.

### Verdict (Area 4)

**Scalable and future-proof** with sparse tables and epoch versioning. Formalize in TP/schema docs, not in 20.10 principles alone. Require invalid-combination matrix and deprecation map in SRP output.

---

## 5. System-Level Advantages

| Claim | Justified? | Notes |
|-------|------------|-------|
| High-resolution interpretation | **Partially** | Resolution = table granularity + trigger specificity, not the address tuple alone |
| Flexibility / evolvability | **Yes** | New OBG/XlateR rows without TS core rewire — core claim holds |
| Fast hot-path (lookups only) | **Yes** | If SRP, inference, and MTP walks stay off hot path — enforce strictly |
| Low cost/area/power | **Yes** | Consistent with TS vs GPU table in 20.30 §11; conditional on no hidden inference in TR |
| No re-architect as OBGs/TRs emerge | **Mostly** | Table extension yes; SRP recompilation and epoch migration still required |
| Separation of identity, structure, translation | **Yes** | Best part of the proposal |
| Semantic manifold growth | **Yes** | Sparse compositional space is the right mental model |

### Overclaim risk

"High-resolution interpretation" must not imply **finer meaning construction** — that remains MTP/basin work. This layer provides **finer realization/routing resolution**. Attribute correctly.

### Verdict (Area 5)

Advantages are **real and correctly attributed to the cold-compile / hot-lookup pattern**, not to 50-series implementation detail. Tighten wording on resolution vs construction.

---

## 6. Problems Solved / System Issues Addressed

| Problem | Legitimate? | Addressed by proposal? |
|---------|-------------|------------------------|
| Stable TS core despite evolving discourse modes | **Yes** | **Yes** — via table indirection |
| High-resolution semantic routing | **Yes** | **Partially** — 20.37 TR already routes; this adds register-aware realization routing |
| Large sparse compositional space | **Yes** | **Yes** |
| Evolve OBGs without breaking TS | **Yes** | **Yes** — with epoch/alias rules |
| Add TRs without re-wiring | **Yes** | **Yes** — if XlateR is table-driven |
| Deterministic auditable routing | **Yes** | **Yes** — SRP compile logs + epoch + immutable tables |
| Inference off hot path | **Yes** | **Yes** — if SRP boundary holds |

### What already exists (don't duplicate)

- **Thought Router (20.37):** semantic routing vector on TP
- **Relational Basin (20.50):** OB topology and lane arbitration
- **COB (20.32):** conversation-scoped discourse state
- **OuB (20.110):** expression realization from MTP

### Novel contribution

**Register identity (OBG) as a compositional axis** + **offline routing-table compilation (SRP)**. That is the genuine architectural addition — not a replacement for basin/TR/RB meaning construction.

### Verdict (Area 6)

All listed concerns are legitimate. The proposal **meaningfully addresses** them **as a realization-layer extension**. It **does not need to subsume** existing basin primitives to do so.

---

## 7. Placement in the 20 Directory

### Recommended document map

| Topic | Recommended location | Rationale |
|-------|---------------------|-----------|
| Cold/hot path + dual-pipeline principle | **20.10** (new §1.16) | Foundational; constrains all modules |
| Execution-manifold primitives (renamed) | **20.20** (new § tier B) OR **20.21_execution_primitives.md** | Keep 20.20 basin primitives intact; add second tier explicitly |
| OpBeh definitions + catalog rules | **20.41_operational_behavior_requirements.md** | 20.40 is Object Basin — do not overload |
| OBG definitions + lifecycle (split/merge/deprecate) | **20.42_obg_requirements.md** | Parallel to COB but register-focused |
| XlateR definitions + mapping contracts | **20.43_translation_routine_requirements.md** | Keep 20.37 as Thought Router |
| SRP compiler block | **20.55_srp_requirements.md** | **Yes — own 20.5x cluster** (between RB 20.50 and TB 20.60) |
| Routing table schema + epoch semantics | **20.56_routing_table_schema.md** | SRP output contract |
| Trigger detector (proposed RB) | **20.57_semantic_trigger_requirements.md** | Do not redefine 20.50 Relational Basin |
| Composite address + TP fields | **20.105** (extend) + **20.39** (guidance) | Normative TP ownership |
| Discourse/goal manager | **20.43** or **20.33** (CIL extension) | Depends on whether OBG selection is conversational intake vs goal policy |
| Glossary + registry | **20.190** + `glossary_term_registry.json` | Mandatory before any merge |
| Traceability | **20.200** | New HLR rows for all of the above |
| End-to-end trace | **20.36** | Add realization-phase trace after MTP finalize |

### Direct answers to your placement questions

- **SRP own 20.6x cluster?** → **No. Use 20.55/20.56** (SRP sits between routing and interpretation, not after TB).
- **OB/OBG/TR defs in 20.30 or 20.40?** → **Neither.** 20.30 stays functional model; 20.40 stays Object Basin. Use **20.41–20.43**.
- **Composite address in 20.10 or 20.20?** → **Split:** invariant statement in **20.10**; formal tuple + ID policy in **20.105** (or **20.56** if table-keyed).

### Additional documents needed

1. **20.10.xx** — Namespace/disambiguation policy (basin vs execution symbols)
2. **20.56** — Routing table schema + epoch + invalid-triple matrix
3. **20.58** — OuB ↔ execution manifold integration (how composite address reaches expression)
4. **20.200** delta — HLR IDs before 30-series verification

---

## Bottom Line

| Dimension | Rating |
|-----------|--------|
| Internal conceptual coherence | **Strong** |
| Alignment with TS principles (determinism, auditability, bounded hot path) | **Strong** |
| Fit with existing 20-series without rename | **Blocked** |
| Completeness | **~75%** — missing discourse-manager placement, epoch coherence, OuB handoff, Thought Router coexistence |
| Recommended path forward | **Adopt as Execution Manifold; rename colliding symbols; add 20.41–20.43, 20.55–20.58** |

The equilibrium CP and you aligned on for 40.100 (playground vs source of truth) applies here too: prototype the execution manifold in **40.1xx** with full disclaimers while 20.4x/20.55 normative docs are drafted and namespace collisions are resolved in **20.10/20.190** first.

---

I can next draft a concrete **namespace resolution table** (every colliding symbol → canonical name → TP field → owning document) or a **minimal 20.10 §1.16 patch outline** for CP review — whichever you want to tackle first.
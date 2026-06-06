Checking how the current specs describe Pipeline A vs B and MTP integration so the opinion is grounded in the repo.
## 1. Is the clarified model correct and internally consistent?

**Yes — with one precision worth locking in.**

The model you described is the natural conclusion of what the repo already implies but has not stated plainly:

| Claim | Already supported by |
|-------|----------------------|
| TP is lane-local, Pipeline A only | 20.105 (v0.4), 20.31-012/013, 20.39 `TpLaneView` |
| MTP / `semantic_core` is global, integrates lanes | 20.30 §3.6 Merge, 20.31, strip-replay invariants |
| Pipeline B runs after meaning commit | 20.36 §2.1–2.2 (`mtp_update` then B stages), 20.12-005 |
| Pipeline B does not write meaning | 20.12-003, 20.12-014 |
| B is not required for meaning replay | 20.12-011 (strip `exec_plan` + `exec_trace` → identical `semantic_core`) |

What was **implicit** and is now **explicit** — and I agree with it:

- **One B pass per committed `semantic_core` / MTP per cycle**, not per TP.
- **B has no lane topology** (no split/merge, no `tp_seq`, no TP-B).
- **B state is derived/regenerable**, not co-authoritative with meaning for replay equivalence.

That is internally consistent with the dual-pipeline contract: Pipeline A is the **meaning construction graph** (lane-parallel); Pipeline B is the **realization compiler** (MTP-scoped, sequential).

### The one precision to nail down

**“Pipeline B has no replay-critical state”** is correct **for meaning replay** (HLR-20.012-011), but not for **full-trace replay** (HLR-20.012-012).

I would phrase it this way:

- **Meaning replay authority:** `semantic_core` (+ supervisory triggers that affect A, bounded).
- **B envelopes (`exec_plan`, `exec_trace`):** reproducible from `(committed semantic_core, routing_epoch_id, policy_signature, seed)` but **strippable** without changing meaning bytes.

That matches your “regenerated from `semantic_core` during replay” without contradicting 20.12-012’s full-trace reproducibility claim.

### Minor tensions to resolve in docs (not in the model)

1. **20.30** still describes the system heavily in lane/TP terms; B is named but not scoped as MTP-single-pass.
2. **20.115** is still a thin v0.1 and does not yet own “MTP = global integrator + B input boundary.”
3. **GB reads TP lane-local state** (20.30) — fine for supervision; must not be read as “B also runs per lane.”
4. **IMR Type B** schedules A-cycle TR recompute — that’s a **bounded A trigger**, not per-TP B execution.

None of these break your model; they just need clearer boundary language.

---

## 2. What existing documents need updates?

### 20.105 (TP) — **light touch**

**Current fit:** Strong. Already says Pipeline A only, lane-local projection, forbidden exec fields, Merge → `mtp_update`, B forbidden on TP.

**Likely gaps relative to your clarification:**

- Does not yet say plainly: **“Pipeline B never consumes TP instances; it consumes only post-commit `semantic_core`.”**
- History/audit role (your point about TP recording lane history) could be contrasted with **“B does not depend on TP audit logs.”**
- Worked example ends at Merge/`mtp_update` — good; could conceptually note B starts **after** that boundary (not a rewrite of 20.105 structure).

**Update type:** Boundary statements and cross-pipeline consumption notes — not structural overhaul. 20.105 is mostly already correct.

---

### 20.115 (MTP) — **major hardening (highest priority)**

**Current fit:** Weak relative to the clarified model. Still generic v0.1; no dual-pipeline section, no explicit role as:

- global aggregator of lane TPs
- authoritative `semantic_core` container post-`mtp_update`
- **sole stable input snapshot for Pipeline B**

**Likely gaps:**

- No statement that MTP is **global** (not lane-scoped).
- No **A→B handoff contract** at `mtp_update`.
- No replay note: MTP/`semantic_core` is strip-stable; B output is derived.
- No “forbidden on MTP” mirror of TP (e.g., B should not leave lane artifacts on MTP).

**Update type:** Full hardening pass (same pattern as 20.105/20.140): dual-pipeline discipline table, field model, writer authority, replay section, conformance harness notes. This is where your architectural clarification **lands normatively**.

---

### 20.30 (Functional model) — **conceptual realignment**

**Current fit:** Good on Pipeline A basin chain; HLR-20.030-322–324 exist but B is under-specified as MTP-scoped.

**Likely gaps:**

- §2–3 read as **lane-parallel meaning construction** (correct) but do not state **B is singular per cycle**.
- Cycle allocation table (% of cycle) may imply B is peer to per-lane work — may need reframing as **one B slice per committed MTP**.
- GB/TP lane-local reads could use a footnote: supervisory observation ≠ B parallelism.

**Update type:**

- New subsection: **“Pipeline B: MTP-scoped realization pass”** (conceptual, not algorithmic).
- Clarify stage graph: A (fan-out lanes) → Merge → `mtp_update` → B (single fan-in from `semantic_core`).
- Replay note tying to 20.12-011.

**Caution:** 20.30 is bootstrap — per your hardening rules, additions should be **clarifying**, not a rewrite of HLR semantics other modules depend on.

---

### 20.36 (Replay / trace fixtures) — **fixture taxonomy and assertions**

**Current fit:** Stage order is already correct (B after `mtp_update`). Strip tests are aligned.

**Likely gaps:**

- Fixtures may still **look** TP-centric in places; B stages should be **MTP-scoped** in fixture shape (one B segment per cycle, not per lane).
- Assertions could explicitly state: **no `lane_id` in Pipeline B stage records**; no TP references in B envelopes.
- “Regenerate B from stripped `semantic_core`” could be a named replay class or sub-assertion (complements strip equivalence).

**Update type:** Replay notes, fixture preconditions, assertion checklist — conceptual + taxonomy, not new algorithms.

---

### Documents you didn’t list but I’d include in the pass

| Doc | Why |
|-----|-----|
| **20.12** | Canonical home for “B is derived, A is authoritative” — may need a **clarifying annex or HLR gloss** without changing bootstrap semantics |
| **20.39** | `SemanticCoreSnapshot` vs `TpLaneView` vs `ExecPlanRecord` — ideal place for “B reads snapshot only” |
| **20.38** | Implementation read-boundary guard: A modules must not import B; B must not index by `tp_id` |
| **20.31** | `semantic_core` commit boundary = B input freeze |
| **20.45 (IMR)** | Triggers affect **next A cycle**, not per-TP B |
| **20.190 glossary** | Dual-pipeline terms: MTP-scoped B, no TP-B |
| **README / 20.200 traceability** | Index new B contract doc |

---

## 3. What kind of updates (by category)?

| Category | Where | Purpose |
|----------|-------|---------|
| **Boundary statements** | 20.105, 20.115, 20.39, 20.38 | “B never sees TP”; “MTP is B input” |
| **Topology / lifecycle diagrams** | 20.30, 20.36 | Fan-out A → fan-in MTP → single B pass |
| **Replay semantics** | 20.36, 20.115, new B spec | Strip vs regenerate vs full-trace fidelity |
| **Writer authority matrices** | 20.115, new B spec | Who writes what envelope, when |
| **Negative conformance rules** | 20.36, 40-series harness | Reject `lane_id` on B records, TP refs in `exec_plan` |
| **Conceptual only (no new HLR IDs in bootstrap)** | 20.30, possibly 20.12 | Clarify without destabilizing signed modules |

I would **not** start by rewriting 20.105 again — it’s CP-approved and already encodes the A-side correctly. The gap is mostly **MTP + B scope + replay taxonomy**.

---

## 4. What new documents should exist?

I’d recommend **two** normative modules (numbers tentative):

### A. **Pipeline B / Execution Manifold requirements** (e.g. 20.1xx)

**Owns:**

- Single-pass-per-`mtp_update` lifecycle
- Inputs: frozen `semantic_core` snapshot + `routing_epoch_id` + policy
- Outputs: `exec_plan`, `exec_trace` only
- Explicit non-goals: no lanes, no split/merge, no TP, no `semantic_core` writes
- Seed scope (expression only)
- Determinism: `(semantic_core, epoch, policy, seed)` → B envelopes
- Submodule delegation: OuB, TrigRB, IMR, SRP lookup (cross-refs, not re-spec)

This becomes the **definitive B spec** so OuB/IMR docs don’t each imply their own topology.

### B. **A↔B synchronization contract** (e.g. 20.1yy or § in 20.115)

**Owns:**

- Handoff predicate: `mtp_update` complete → B may start
- Snapshot immutability during B pass (B reads frozen commit)
- IMR / supervisory trigger queue back to A (bounded, next-cycle)
- Epoch coherence: B consumes published `routing_epoch_id` only
- Failure modes: B reject does not mutate `semantic_core`

Could be a standalone doc or a **major section of hardened 20.115** (“§ MTP as Pipeline B input boundary”). I slightly prefer **standalone contract + 20.115 cross-ref** so 20.115 stays about MTP structure and the contract stays about timing/handoff.

### Optional third (later)

- **20.36 Class 6** or harness guide: “B regeneration equivalence” (regenerate B after strip, compare to golden `exec_*` OR assert only `semantic_core` if strip-focused)

---

## 5. How I would approach the update process (once aligned)

**Phase 0 — Canonical one-pager (no repo edits)**  
Agree on 5–7 bullet invariants everyone signs:

1. TP = lane-local, A-only, replay-critical for **lane history**, not for B.  
2. MTP/`semantic_core` = global meaning authority after Merge.  
3. B runs **once per cycle** after `mtp_update`.  
4. B inputs = committed `semantic_core` only (no TP, no lanes).  
5. B outputs = `exec_plan` + `exec_trace` (+ bounded supervisory triggers).  
6. Meaning replay = strip B; B may be regenerated.  
7. Seed affects B expression only.

**Phase 1 — MTP hardening (20.115)**  
Biggest normative gap. Dual-pipeline table, global vs lane, `mtp_update` commit, B input freeze, replay. CP review pattern you’ve been using.

**Phase 2 — New Pipeline B spec + A↔B contract**  
Draft in parallel: B spec defines *what B is*; contract defines *when and how A hands off*. Cross-check against 20.12, 20.45, OuB/IMR modules.

**Phase 3 — 20.30 + 20.36 clarifications**  
Bootstrap-safe additions: topology subsection, fixture assertions, no new contradictions with signed 20.105/20.140.

**Phase 4 — Light cross-refs (20.105, 20.39, 20.38, glossary)**  
One boundary paragraph each; avoid version bumps unless CP wants them.

**Phase 5 — Verification alignment**  
40-series harness rules: MTP-scoped B fixtures, negative tests for TP-in-B, regenerate-B test optional for full trace.

**Phase 6 — Consistency grep**  
Repo-wide search for “per TP” near Pipeline B, `lane` in exec modules, TP-B — fix conceptual drift in non-bootstrap docs only.

**Ordering rationale:** Harden **MTP first**, because your clarification’s center of gravity is **“B runs on committed MTP, not TP.”** 20.105 is already aligned; 20.115 is not. B spec and contract follow MTP so handoff has a well-defined input object.

---

## Bottom line

Your clarified model is **correct, simpler than a per-TP B would be, and consistent with 20.12/20.36** if we sharpen “replay-critical” to mean **meaning-authoritative vs derivable**.

The work is less “fix 20.105” and more **elevate 20.115, add a Pipeline B spec + A↔B contract, and tighten 20.30/20.36 replay language**. 20.105 needs only boundary cross-references, not a structural rewrite.

When you’re ready to proceed, I’d start with the Phase 0 invariant one-pager for CP sign-off, then **20.115**.
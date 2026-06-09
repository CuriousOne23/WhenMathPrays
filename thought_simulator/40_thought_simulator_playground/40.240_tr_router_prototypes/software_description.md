# 40.240_tr_router_prototypes / software_description.md

## Approval State

- Legacy Phase A/B (proxy routing): **approved** (Copilot; proxy subset only)
- **W3 Phase A** (40.510-410 extension): **approved** (CP W3 Phase A review, 2026-06-08 — no blockers)
- W3 Phase B (DCB ephemeral TR events; `tr_needs_update` gating per 20.37): **cleared to start** — pending implementation
- Program row: **40.510-410** (W3)

## W3 Extension Scope (40.510-410)

Phase B SHALL extend beyond the standalone `route({"content": ...})` proxy to implement on-TP semantics:

- Consume OB TR-input + optional [40.210](../40.210_dcb_prototypes/software_description.md) ephemeral events when `tr_needs_update = true`
- Atomic `TP.TR` write; clear `tr_needs_update` on success only (20.37 steps 5–6)
- Negative: reject TR run when flag false; reject DCB-direct RB consumption
- Preserve existing proxy scenarios as regression subset until full integration supersedes

**W3 Phase B maps to legacy Phase C (on-TP integration)** below — scoped to 40.510-410 handoffs with 40.200/40.210/40.190.

**Agreement Statement (W3 Phase A)**: Aligned — CP review 2026-06-08 confirms W3 extension scope against 20.37 Semantic Interpretation Flow Contract (HLR-20.037-049/050/051). Legacy proxy Phase B evidence retained as regression baseline; integration HLRs deferred to W3 Phase B.

## CP W3 Phase A Review Record (2026-06-08)

| Check | Result |
|-------|--------|
| W3 extension scope vs 40.510-410 | Pass |
| `tr_needs_update` gating + atomic `TP.TR` write | Pass |
| DCB ephemeral events via 40.210 (not RB-direct) | Pass |
| Proxy regression subset preserved | Pass |
| Two-phase model (stop after Phase A) | Pass |
| Blockers | **None** — Phase B authorized |

**2026-06-05 alignment pass:** Synchronized with `20.37` flow contract and 10.50.180 / 30.180 artifacts. W3 Phase A CP-approved 2026-06-08; proxy-only code remains until W3 Phase B lands.

## Execution Phases (40.* Model)

| Phase | Status | Scope |
|-------|--------|--------|
| **A** | Complete (approved) | This `software_description.md` only |
| **B** | Complete (executed) | Proxy: `prototype.py`, `harness.py`, verification artifacts, proxy-only evidence |
| **C** | Not started | Full 20.37 integration on TP structures (see Phase C section below) |

**Global 40.* rule:** Mandatory stop after Phase A until human approval. Phase B followed approval. Phase C requires separate approval before implementation.

---

## Role in the Development Flow

This document defines the **desired / explored behavior** for the Thought Router (TR) prototype in the 40-series. It is guided by the 20-series and 10-series documents listed below.

The **authoritative full TR integration model** is the Semantic Interpretation Flow Contract in `20.37_thought_router_tr_specification.md` (OB → TR-input → `tr_needs_update` → TR routine → `TP.TR` → RB, with optional DCB geometric overlay). This 40.240 module executed only a **minimal basin-selection proxy**; it does not implement that contract.

Insights and evidence from the proxy inform `10.50.180` (promoted routing) and document open work toward full 20.37 conformance.

---

## Semantic Interpretation Flow Contract (20.37 — Target Architecture)

The following is the normative cycle this prototype **defers**; it is summarized here for alignment only (detail in 20.37).

| Step | Actor | Action |
|------|--------|--------|
| 1 | RB | Route TP to OB |
| 2 | OB | Write pre-semantic TR-input fields to `TP.input_fields`; set `tr_needs_update = true` when semantic-relevant inputs change |
| 3 | DCB | (When enabled) Observe TP trajectory; emit ephemeral directional-change events; no TP writes; does not set `tr_needs_update` |
| 4 | RB | Evaluate `tr_needs_update` |
| 5 | TR routine | Run **iff** `tr_needs_update = true`; read TR-input, TP/MTP snapshots, permitted DCB events |
| 6 | TR routine | Write `TP.TR` atomically; clear `tr_needs_update` on success only |
| 7 | RB | Route downstream using committed `TP.TR` and explicit routing inputs |

**Precedence:** `tr_needs_update` semantics — `20.31` §10; integration HLRs — `HLR-20.037-049`, `-050`, `-051`; DCB — `20.106` and 20.37 §4.4.

**Proxy mapping (this module):** Standalone `route({"content": ...})` approximates an early **basin-selection + ΔH%** decision only. It does not perform steps 2–7 on real TP structures.

---

## Phase A Deliverables

- High-level routing behavior description
- Mapping of 20/10-series intent to prototype responsibilities (simplified basin selection as proxy)
- Identification of unknowns relative to full 20.37 flow contract
- Definition of what Phase B must / did explore
- No final algorithms or numeric policy for production TR (20.95 / 50-series)

---

## Phase B Deliverables (Executed + 40.05-aligned)

- Minimal deterministic content-based router (keyword proxy for semantic cues)
- Consistent ΔH% assignment per route decision
- Explicit error route for invalid input, no side effects
- Harness with deterministic pass/fail + ΔH% validation + multi-run support (run1/run2/run3)
- JSON artifacts in `artifacts/`
- `docs/` with experiments.md, prototype_notes.md, reasoning_trail.md
- Expanded verification_capsule.md and requirements_delta.md
- Forward-flow sync to 10.50.180 and 30.180 (2026-06-05)

---

## Phase C (Future Integration Prototype — Not Implemented)

**Status:** Not started. Out of scope for the current proxy package and for the next **40.05** run.

Phase C will implement the full `20.37` Semantic Interpretation Flow Contract on real TP structures, including:

- OB TR-input field writes and `tr_needs_update = true` when semantic-relevant inputs change
- RB route to TR routine iff `tr_needs_update`
- TR routine atomic `TP.TR` commit and clear-on-success / preserve-on-failure dirty-flag semantics
- RB downstream routing from committed `TP.TR`
- Full `TP.TR` semantic field population per 20.37 §6
- DCB post-OB / pre-TR ephemeral event consumption under TR gate (20.106, 20.37 §4.4)
- Conformance evidence for `HLR-20.037-049`, `-050`, `-051`

Until Phase C exists, **40.240 Phase B artifacts remain the authoritative evidence** for basin-selection proxy only (`HLR-20.437-*`). 40.05 must not treat proxy harness output as proof of integration HLRs.

---

## 1. Purpose

Define a deterministic Thought Router (TR) **proxy** that performs **initial basin selection** and **ΔH% tagging** as exploratory validation—**not** full semantic interpretation per 20.37.

The TR proxy **SHALL**:

- deterministically map input characteristics to a basin route (`math_basin`, `thought_basin`, `general_basin`)
- assign fixed, consistent ΔH% values based on the chosen route
- return explicit `{"route": "error", "reason": "invalid_input"}` for malformed/empty input with no side effects
- remain strictly deterministic: identical input always yields identical route + delta_h
- respect separation of concerns (routing decision only; no meaning construction, no TP/MTP mutation)

**Core principle (full TR, from 20.37 + 10.10):**  
In production TS, the TR routine is the **exclusive writer** of `TP.TR`, executes only when RB routes because `tr_needs_update = true`, and clears the dirty flag only on successful commit. OB writes TR-input fields and may set stale; RB consumes committed `TP.TR` for downstream routing. GB supervises read-only.

---

## 2. Guidance from Specified Sources

This prototype was developed under guidance from (and must be traceable to):

- **20.10_ts_architectural_principles.md** — Determinism, explicit meaning construction, GB as supervisor only, bounded feedback elements (§1.14 Geometric Feedback Elements / DCB at architecture level).

- **20.16_gb_responsibility_matrix.md** — GB must not perform meaning construction; routing remains in deterministic core; GB reads TR for gating only.

- **20.30_ts_functional_model.md** — Pipeline including OB → DCB (§3.4.1) → TR gate; HLR-20.030-311..315 (`tr_needs_update`); HLR-20.030-316..321 (DCB placement). Proxy does not execute this pipeline.

- **20.31_semantic_specification.md** §10 — Authoritative `tr_needs_update` stale/fresh/writer/clear/routing semantics (deferred in proxy).

- **20.37_thought_router_tr_specification.md** — **Primary anchor.** Semantic Interpretation Flow Contract; `TP.TR` field set (§6); OB→TR (§4); TR geometric inputs / DCB (§4.4); TR→RB (§5); lifecycle (§7); HLR-20.037-001..051. This prototype explores **only** a routing+ΔH% subset; HLR-20.037-049/050/051 are canonical targets for future 40.x iterations, not proven here.

- **20.106_dcb_requirements.md** — DCB geometric meta-basin, ephemeral TR inputs, no `tr_needs_update` from DCB (out of proxy scope).

- **20.38_ts_implementation_guidelines.md** — Modularity, deterministic core separation, replay, auditability (process guidance for prototypes).

- **10.10.10, 10.10.20, 10.10.40, 10.10.50** — TR execution gating, `TP.TR` / `tr_needs_update` contracts, RB→TR iff dirty, TR clear-on-success-only.

- **10.10.36 / 20.80** — GB read-only, safe-boundary supervision; no TR mutation by GB.

- **10.50.180_tr_requirements.md** — Canonical anchor: promoted proxy (`HLR-20.437-*`, `10.50.180.TR.*`) plus integration flow (`10.50.180.FLOW.*` → 20.37).

- **30.180** — Verification capsule/delta; proves proxy only; integration contract marked open (2026-06-05).

---

## 3. What Phase B Explored (and Future Iterations)

### Phase B evidence (executed)

- Deterministic routing from input content (keyword proxy standing in for OB TR-input cues)
- Fixed ΔH% per route class (math=0.15, thought=0.08, general=0.05)
- Input validation and error path without side effects
- Multi-run determinism (run1/2/3 identical)
- Routing-only separation of concerns

### Future iterations **SHALL** explore (20.37 alignment)

- **Semantic Interpretation Flow Contract** end-to-end on TP structures (20.37 contract steps 1–9)
- OB TR-input field writes + `tr_needs_update = true` on semantic-relevant change
- RB route to TR routine iff `tr_needs_update`
- TR routine: read TR-input + MTP (read-only); atomic `TP.TR` write; clear dirty on success; preserve on failure
- Full `TP.TR` block per 20.37 §6 (12 semantic fields + `routing_semantics`)
- RB downstream routing from committed `TP.TR` (not proxy dict alone)
- DCB post-OB / pre-TR ephemeral events consumed only when TR runs (20.106, 20.37 §4.4)
- Split/merge lineage in TR; safe-boundary GB read paths

**Note:** Phase B prototypes explore feasibility; they do not define final system behavior.

---

## 4. What the 10-series Must Eventually Define

The prototype surfaced requirements the 10-series **SHALL** maintain (partially in 10.50.180 today):

- Full TR routine contract per 20.37 (field rules, rejection, versioning)
- Dirty-flag enforcement aligned with 20.31 §10 and 10.10.50
- TR ↔ GB read-only supervisory interaction at safe boundaries
- DCB geometric overlay boundaries (no semantic extraction by DCB)
- Serialization / numeric policy (20.95, 20.39) for TR subfields
- IPC and module visibility for TR (10.10.20, 10.10.50)

Promotion path: proxy evidence → `10.50.180.TR.*` + `30.180` (done); integration scenarios → extend `30.180` or sibling harness → `50.180` design spec.

---

## 5. Non-Goals (This Iteration)

This prototype **does not** define or implement:

- Semantic Interpretation Flow Contract on real TP/MTP (20.37 steps 1–9)
- `TP.TR` population or TR routine commit semantics
- `tr_needs_update` lifecycle or RB iff gating inside the prototype
- DCB trajectory observation or directional-change events (20.106)
- MTP snapshot consumption or pipeline integration
- GB/COP safe-boundary signaling from TR outputs
- Stochastic behavior, wall-clock dependence, or TCU budgeting for full TR
- Full IB/Merge/Truth/OB consumer contracts

Reserved for subsequent 40.x iterations or 50.180 after integration harness evidence.

---

## 6. Risks & Unknowns (Aligned with 20.10 §1.14)

- Scaling keyword/proxy rules to full TR field derivation under messy input (20.17)
- Dirty-flag interaction with parallel traces, split/merge, and GB arbitration
- Stability of proxy ΔH% once `semantic_deltaH` and lineage rules apply in TR
- DCB geometric feedback boundedness under full cycle (20.165) when integrated with TR
- GB supervisory load if TR refresh frequency grows (20.16 mitigation: RB + basin-local rules)

---

## 7. Deterministic Invariants (Observed in Executed Prototype)

- Identical input → identical `{"route", "priority", "delta_h"}` (or error form)
- No randomness, no global mutable state, no wall-clock dependence
- Error paths produce no side effects
- ΔH% fixed per route class
- Harness JSON artifacts fully replayable

---

## 8. IO Contract (Current Prototype)

**Inbound (harness → router):**

- `{"content": string}` — free text; keyword scan as TR-input proxy

**Outbound (router → caller):**

- Success: `{"route": "math_basin"|"thought_basin"|"general_basin", "priority": "high"|"medium"|"low", "delta_h": float}`
- Error: `{"route": "error", "reason": "invalid_input"}`

**Full TR (20.37 target, not implemented here):**

- OB writes `TP.input_fields`; TR routine writes `TP.TR`; `tr_needs_update` governs execution; RB consumes `TP.TR` for routing; optional ephemeral DCB events at TR input boundary.

---

## 9. Promotion Readiness Conditions

**Achieved (proxy scope):**

- Harness 4/4 pass; multi-run determinism artifacts
- `requirements_delta.md` and `verification_capsule.md` with three-flow statements
- Phase A software_description approved; 40.05 structural alignment
- Partial promotion to 10.50.180 (`HLR-20.437-*`) and 30.180

**Open before integration promotion:**

- Harness scenarios for 20.37 flow contract (dirty flag, TR commit/clear, RB gate)
- 30.180 `proves:` extension to HLR-20.037-049/050/051
- 50.180 design spec update per 50.05 after integration evidence

---

## Flows Alignment Statement

- **Forward Flow (20/10-series):** Authoritative integration model is 20.37 Semantic Interpretation Flow Contract + 20.31 §10 + 20.106 DCB overlay + 20.30 pipeline HLRs + 10.10.* module contracts. This document defers to those sources for full TR behavior.

- **Backward Flow (40-series evidence):** Executed proxy proves deterministic basin routing + ΔH% + error path (`HLR-20.437-*`). Evidence does **not** prove HLR-20.037-049/050/051 or full OB→TR→`TP.TR` cycle.

- **Iterative Design Flow:** 10.50.180 and 30.180 synchronized 2026-06-05 to split proxy vs integration scope; 50.180 remains proxy-based until integration scenarios exist.

**Agreement Statement:** Flows agree on **bounded proxy scope**. Full 20.37 semantic interpretation flow is canonical and documented here as the target; verification and prototype code for that flow remain **open**.

---

## Traceability

Phase B evidence and this description **SHALL** trace to:

- 20.37 (Semantic Interpretation Flow Contract, module rules, HLR-20.037-*)
- 20.31 §10 (`tr_needs_update`)
- 20.106 (DCB)
- 20.10, 20.16, 20.30, 20.38
- 10.10.10, 10.10.20, 10.10.40, 10.10.50, 10.10.36
- 10.50.180 (proxy + FLOW sections)
- 30.180 verification package
- 40.240 local artifacts (`artifacts/`, harness, capsule, delta)

---

## Scaffold / Execution Metadata

- intended_20_anchor: thought_simulator/20_requirements/20.37_thought_router_tr_specification.md
- intended_20_flow_contract: Semantic Interpretation Flow Contract (20.37); tr_needs_update: 20.31 §10; DCB: 20.106
- intended_10_10_anchor: thought_simulator/10_thought_simulator_req/10_system_architecture/10.10.50_module_contracts_and_visibility_rules.md
- executed_as: minimal basin-selection router (proxy); full TP.TR + flow contract deferred
- disposition_target: promote proxy (10.50.180.TR + 30.180); integration verification open
- last_20_37_sync: 2026-06-05
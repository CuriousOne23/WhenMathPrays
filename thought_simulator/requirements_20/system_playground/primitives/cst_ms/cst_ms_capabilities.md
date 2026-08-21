# cst_ms_capabilities.md — CST-MS Capability Surface

**Document ID:** cst_ms_capabilities  
**Version:** 0.1  
**Status:** Draft — for CP review  
**Location:** `thought_simulator/requirements_20/system_playground/primitives/cst_ms/`  
**Scope:** Capability inventory for the live CST-MS primitive in system_playground  

**Normative parents:**  
- `20.32.010.020_cst-ms.md`  
- `system_playground/primitives/cst_ms/cst-ms_requirements.md`  
- `progressive_lineup_testing.md` (context pipeline, dual-mode)  
- `patha_field_names.md` (coarse CST-MS names; nested path lock pending structural program)  
- Locked upstream: `TP.cst.core` (`cst_core_py_struc_pgm.md`, patha §2.4 / §9)  

**Shaping heritage (non-authoritative):**  
- `cst_ms_bak.py`  
- Prior standalone runner: `cst_ms_testbench.py` / `cst_ms_testbench_bak.py` (or local rename) under `testbenches/path_a/context/`  

**Related (not this document):**  
- `cst_ms_py_struc_pgm.md` / `cst_py_struc_pgm.md` — realization plan (to be written)  
- `cst_ms.py` — live implementation  

---

## 0. Purpose

This document states **what CST-MS is expected to be able to do** in the system_playground realization, what **synthesis shapes and provisional formulas** the heritage path already demonstrated, and what remains **gap / Defer** relative to 20.32.010.020.

It is **not** a requirements document and **not** a structural program.  
HLRs remain authoritative. Structural program and progressive testbenches must not treat heritage `run(cst_signals) → MSSignals` as the progressive `process(tp)` contract.

---

## 1. Architectural Capability (Normative Intent)

CST-MS is the **Metric Synthesis Module** in the CST pipeline. It:

- consumes raw CST-Core metrics and related signals  
- normalizes, weights, and synthesizes stability / instability / risks / summaries  
- holds **decision authority** for structural control commands issued **to COB**  
- reports synchronization mismatches **diagnostically** to CST-Mux (no command feedback loop from COB state)

### 1.1 What CST-MS SHALL be capable of

| Capability | Source |
|------------|--------|
| Accept raw Core metrics: drift, oscillation, ambiguity, collapse, continuity, freeze, thaw, register stability, field-importance stability | HLR-001 |
| Accept layer-specific thresholds and metric histories | HLR-002, 003 |
| Accept freeze / thaw / continuity-restoration signals from Core | HLR-004 |
| Accept OuBA committed identity-layer snapshots as stable reference | HLR-044 |
| Optional diagnostic read of COB topology **only** for sync mismatch | HLR-045 |
| **Must not** derive structural commands from COB internal state | HLR-046 |
| Normalize each metric to [0, 1] with deterministic maxima | HLR-011–013 |
| Apply deterministic layer-specific weights | HLR-014–016 |
| Compute stability (weighted synthesis) and instability (complement), clipped [0, 1] | HLR-017–021 |
| Compute collapse risk, freeze risk, thaw readiness | HLR-022–027 |
| Produce ambiguity / drift / oscillation summaries | HLR-028–030 |
| Issue COB commands: freeze, thaw, collapse-recovery, create-identity-layer, split, merge | HLR-035–041 |
| Commands deterministic, replay-safe; log every command for replay | HLR-042–043 |
| Report sync mismatch to Mux; **no** extra structural commands from mismatch | HLR-047–048 |
| Pure functional synthesis w.r.t. metrics: no randomness, no wall-clock, identical under replay | HLR-031–034 |

### 1.2 Command authority (normative)

CST-MS is the **sole** module authorized to issue the six structural commands to COB:

1. freeze  
2. thaw  
3. collapse-recovery  
4. create-identity-layer  
5. split  
6. merge  

Commands are driven by **CST-Core metrics + thresholds + OuBA snapshots**, not by COB internal decision loops.

### 1.3 Role boundaries

- **Is:** metric synthesizer + COB command authority + Mux diagnostic reporter.  
- **Is not:** COB itself; does not own identity topology storage.  
- **Does not:** accept control commands from CST-MS peers that would invert authority; does not treat Core raw metrics as COB-facing structural commands without synthesis/thresholding where HLRs require CST-MS ownership.

---

## 2. Progressive / Playground Operational Capability

CST-MS participates in the **context pipeline** under progressive lineup:

```
testbenches/path_a/context/
  cst_ms_testbench.py
  cst_ms_testbench.yaml
  cst_ms_tests_to_run.yaml
  cst_ms_input.yaml
  cst_ms_rules.yaml
  cst_ms_rulechecker.py
```

Required operational capabilities:

| Capability | Notes |
|------------|--------|
| `process(tp, mode="testbench"\|"general")` module surface | Align with CST-Core / COB / CIL progressive contract |
| Dual-mode validation | testbench = input+expected; general = rules only |
| Deterministic identical-input → identical-output | Replay |
| Write-boundary discipline | Only CST-MS-owned TP paths (+ optional routing_path marker) |
| Standardized PASS/FAIL output | progressive §3.9 |

**Canonical TP surface (to be locked in structural program / field dictionary):**  
Conventionally under `TP.cst.ms.*` for synthesized summaries, risks, commands, command log, diagnostics, and window. Exact nested schema is an obligation of the structural program — not invented here beyond the field vocabulary below.

**Upstream read:** locked `TP.cst.core` (signals, metrics, history, status) plus COB snapshot / OuBA reference as specified by HLRs.

---

## 3. Heritage Capability (Shaping Path — Proven Shapes)

The bak implementation and prior standalone testbench demonstrated a **dataclass synthesis path** useful for **names, operator order, and provisional formulas**, not for progressive TP realization or full COB command authority.

### 3.1 Output package shapes (heritage — retain as first-order vocabulary)

```
normalized_metrics:
  drift, oscillation, ambiguity, collapse, continuity   # floats in [0, 1]

weighted_metrics:
  drift, oscillation, ambiguity, collapse, continuity   # floats

stability:
  value: number   # [0, 1]

instability:
  value: number   # 1 - stability, [0, 1]

collapse_risk:
  value: number

freeze_risk:
  value: number

thaw_readiness:
  value: number

ambiguity_summary:
  count: int

drift_summary:
  magnitude: number

oscillation_summary:
  frequency: number
  amplitude: number

metadata:
  turn_index: int
  new_context_required: bool
```

Heritage internal state also tracked:

```
structural_events: [ { event_type: MERGE|SPLIT, data: ... } ]
stability_window: [ { stability, instability, collapse_risk, freeze_risk, thaw_readiness } ]  # capped at 10
```

### 3.2 Operator order proven by heritage

1. Interpret structural (merge/split) events  
2. Neutralize merge/split for instability synthesis  
3. Normalize  
4. Weight  
5. Synthesize stability / instability  
6. Compute risks  
7. Compute summaries  
8. Track 10-turn stability window  
9. Detect `new_context_required`  

### 3.3 Provisional formulas proven by heritage (v0.1-shaped, not final physics)

| Element | Heritage rule |
|---------|----------------|
| Weights | drift=oscillation=ambiguity=collapse=continuity = 0.25 |
| Maxima | all 1.0 |
| Normalize drift | min(magnitude / max, 1) |
| Normalize oscillation | min(frequency / max, 1) |
| Normalize ambiguity | min(len(increased_ambiguity) / max, 1) |
| Normalize collapse | min(severity / max, 1) |
| Continuity | 1 − normalized collapse |
| Stability | sum(weighted) clipped to [0, 1] |
| Instability | 1 − stability |
| Collapse risk | weighted collapse |
| Freeze risk | weighted ambiguity + weighted collapse |
| Thaw readiness | weighted continuity |
| new_context_required | OR of continuity_break (<0.40), avg window instability (>0.60), collapse_spike (>0.50), ambiguity_spike (count>3), freeze_spike (>0.50), fragmentation (structural event ∧ continuity<0.75) |

### 3.4 Behaviors proven by heritage tests

| Behavior | Heritage result |
|----------|-----------------|
| Normalization of Core-like signal dicts | Yes |
| Weighting and [0,1] stability/instability | Yes |
| Risk fields present and ordered vs collapse | Yes |
| Summaries for ambiguity/drift/oscillation | Yes |
| Merge/split neutrality (no pure-structure instability) | Yes |
| Stability window length ≤ 10 | Yes |
| `new_context_required` on continuity break | Yes |
| Independent instances, same inputs → same outputs | Yes |

### 3.5 Heritage non-capabilities (explicit)

Heritage path did **not** provide:

- `process(tp, mode=...)` progressive surface  
- Writes under `TP.cst.ms.*`  
- **COB structural commands** (freeze / thaw / collapse-recovery / create / split / merge as command blocks)  
- Command log for replay (HLR-043)  
- Sync-mismatch diagnostic packet to Mux (HLR-047–048)  
- Layer-specific weight/threshold **tables** (only global placeholders)  
- Input exclusively from locked `TP.cst.core` (used heritage Core signal dict / bak CST)  
- Dual-mode progressive YAML + rulechecker suite  

---

## 4. Capability Matrix (Target Live Primitive)

| Capability | Normative required | Heritage proven | Live target v0.1 |
|------------|--------------------|-----------------|------------------|
| Normalize / weight / stability / instability | Yes | Yes (global stubs) | Must-Prove with provisional constants |
| Collapse / freeze / thaw risks | Yes | Yes (stub formulas) | Must-Prove |
| Ambiguity / drift / oscillation summaries | Yes | Yes | Must-Prove |
| 10-turn synthesis window | Yes (playground) | Yes | Must-Prove |
| Merge/split stability-neutral | Yes (playground) | Yes | Must-Prove |
| `new_context_required` / conversation boundary | Yes (playground HLR-046–050) | Yes | Must-Prove shape |
| COB command emission (six commands) | Yes | **No** | Must-Prove shells + threshold gates |
| Command log | Yes | No | Must-Prove |
| Sync mismatch → Mux diagnostic only | Yes | No | Must-Prove shell |
| `process(tp)` + `TP.cst.ms.*` | Progressive contract | No | Must-Prove |
| Dual-mode progressive testbench | Framework | No | Must-Prove |
| Final layer weights / maxima / thresholds | Yes (eventual) | Placeholders only | **Defer** (fixed v0.1 OK if labeled) |
| Final create/split/merge predicates | Yes (eventual) | No | **Defer** (empty/no-op command OK if documented) |

---

## 5. Gaps / Residual Fog (Defer)

1. **Final synthesis weights** and layer-specific maxima tables.  
2. **Final risk formulas** (collapse / freeze / thaw) if CP replaces heritage stubs.  
3. **Layer-specific command thresholds** (freeze risk, thaw readiness, collapse risk).  
4. **Deterministic create / split / merge condition predicates** (HLR-039–041).  
5. **Exact nested `TP.cst.ms.*` path map** (lock after structural program § path approval).  
6. Mapping heritage `ambiguity_adjustment` inputs onto locked Core `signals.ambiguity` field shapes.  
7. Full progressive expected-YAML freeze for command payloads.

---

## 6. Reuse Policy for Implementation

1. **May reuse** heritage **field names**, operator order, and **provisional** weights/maxima/risk rules listed in §3.  
2. **Must not** treat `run(cst_signals) → MSSignals` as the sole public progressive API.  
3. **Must** implement `process(tp, mode=...)` and owned TP writes consistent with progressive lineup.  
4. **Must** implement COB command shells (even if v0.1 only emits freeze/thaw from risk thresholds and leaves create/split/merge empty under Defer).  
5. **Must** respect write-boundary: no mutation of COB topology store; commands are **emitted fields**, not direct COB object edits inside CST-MS.  
6. Bak files remain reference-only; live `cst_ms.py` and progressive testbench are the realization surface.

---

## 7. Success Criteria for “Same Capability as Heritage, Plus Normative”

Live CST-MS is considered to have **matched and exceeded** heritage capability when:

- All heritage synthesis fields in §3.1 can be produced (or mapped 1:1 under `TP.cst.ms.*`).  
- Merge/split neutrality and 10-turn window still hold.  
- Deterministic replay holds.  
- `new_context_required` (or successor field name locked in dictionary) remains available.  
- **Additionally:** freeze/thaw (and other commanded) shells exist under the owned envelope; progressive dual-mode tests pass; Core input is read from locked `TP.cst.core` where progressive fixtures provide it.

---

**End of cst_ms_capabilities.md (v0.1)**  
Ready for CP review.

# cst_core_capability.md — CST-Core Capability Surface

**Document ID:** cst_core_capability  
**Version:** 0.1  
**Status:** Draft — for CP review  
**Location:** `thought_simulator/requirements_20/system_playground/primitives/cst_core/`  
**Scope:** Capability inventory for the live CST-Core primitive in system_playground  

**Normative parents:**  
- `20.32.010.010_cst-core.md`  
- `system_playground/primitives/cst_core/cst-core_requirements.md`  
- `progressive_lineup_testing.md` (context pipeline, dual-mode)  
- `20.32_cob_requirements.md` (COB interface boundary)  

**Shaping heritage (non-authoritative):**  
- `cst_core_bak.py`  
- `cst_core_testbench_bak.py`  

**Related (not this document):**  
- `cst_core_py_struc_pgm.md` — realization plan (to be written)  
- `cst_core.py` — implementation  

---

## 0. Purpose

This document states **what CST-Core is expected to be able to do** in the system_playground realization, what **signal/metric shapes** are already proven useful by the shaping path, and what remains **gap / Defer** relative to 20.32.010.010.

It is **not** a requirements document and **not** a structural program.  
HLRs remain authoritative. Structural program and progressive testbenches must not treat heritage reflector behavior as the normative algorithm.

---

## 1. Architectural Capability (Normative Intent)

CST-Core is a **stateful metric generator** for identity-layer structural stability.

### 1.1 What CST-Core SHALL be capable of

| Capability | Source |
|------------|--------|
| Extract a structural snapshot per identity layer each turn | HLR-001, 002, 003, 040 |
| Maintain feature counts, frequencies, and ordered histories over a **fixed 10-turn window** | HLR-004–006 |
| Compute **drift** (per-turn + integrated) and emit drift signals when threshold exceeded | HLR-007–010 |
| Compute **oscillation** (state flips) and emit when threshold exceeded | HLR-011–013 |
| Compute **ambiguity** (per-turn + integrated) and emit when threshold exceeded | HLR-014–017 |
| Compute **stability / collapse** and emit collapse when threshold exceeded | HLR-018–021 |
| Compute **combined instability**; emit **Freeze** when freeze threshold exceeded | HLR-022–023 |
| Local metric-tracking freeze: halt snapshot updates, metric updates, threshold adaptation for frozen layers | HLR-024–026 |
| Emit **Thaw** when combined instability falls below recovery threshold | HLR-027 |
| Local metric-tracking thaw: resume snapshot, metrics, threshold adaptation | HLR-028–030 |
| Compute **continuity**; emit **Continuity-restoration** when recovery threshold exceeded | HLR-031–034 |
| Fully deterministic, replay-safe metrics, thresholds, signal order, logging | HLR-035–039 |

### 1.2 Signal routing capability (normative)

| Signal class | Destination | HLR |
|--------------|-------------|-----|
| Freeze, Thaw, Continuity-restoration | **COB and CST-Mux** | 041, 046 |
| Drift, Oscillation, Ambiguity, Collapse (raw metrics + histories) | **CST-MS and CST-Mux only** | 042–044, 046 |
| Drift / Oscillation / Ambiguity / Collapse → COB | **Forbidden** | 043 |
| Commands / feedback from CST-MS | **Forbidden** | 045 |
| Create, Split, Merge, Collapse-recovery to COB | **Forbidden** (no structural authority) | 047 |

### 1.3 Role boundaries

- **Is:** metric generator + emitter of Freeze / Thaw / Continuity-restoration and raw metric packages.  
- **Is not:** state machine with structural authority over identity topology.  
- **Does not:** own COB layers, issue MERGE/SPLIT/Create, or rewrite semantic/routing envelopes.

---

## 2. Progressive / Playground Operational Capability

CST-Core participates in the **context pipeline** under progressive lineup:

```
testbenches/path_a/context/
  cst_core_testbench.py
  cst_core_testbench.yaml
  cst_core_tests_to_run.yaml
  cst_core_input.yaml
  cst_core_rules.yaml
  cst_core_rulechecker.py
```

Required operational capabilities:

| Capability | Notes |
|------------|--------|
| `process(tp, mode="testbench"\|"general")` module surface | Align with COB/CIL progressive contract |
| Dual-mode validation | testbench = input+expected; general = rules only |
| Deterministic identical-input → identical-output | Replay |
| Write-boundary discipline | Only CST-Core-owned TP paths |
| Standardized PASS/FAIL output | progressive §3.9 |

**Canonical TP surface (to be locked in structural program / field dictionary):**  
Conventionally under `TP.cst.core.*` for signals, metrics, histories, and local freeze/thaw tracking status. Exact nested schema is an obligation of the structural program and progressive fixtures — not invented here beyond the signal names below.

---

## 3. Heritage Capability (Shaping Path — Proven Shapes)

The bak implementation and bak testbench demonstrated a **reflector-style** path that is useful for **names and shapes**, not for normative metric computation.

### 3.1 Signal package shapes (heritage — retain as first-order field vocabulary)

```
drift:
  affected_objects: [id...]
  magnitude: number

oscillation:
  affected_objects: [id...]
  frequency: number
  amplitude: number

collapse:
  collapsed_objects: [id...]
  severity: number

freeze:
  frozen_objects: [id...]
  reason: string

thaw:
  thawed_objects: [id...]
  reason: string

certainty_adjustment:
  increased_certainty: [id...]
  decreased_certainty: [id...]

ambiguity_adjustment:
  increased_ambiguity: [id...]
  decreased_ambiguity: [id...]

lineage_stability:
  stable_lineage: [id...]
  unstable_lineage: [id...]

metadata:
  turn_index: int
  object_count: int
```

Heritage also used empty placeholders:

```
merge: { merge_pairs: [], confidence: 0 }
split: { split_objects: [], confidence: 0 }
```

**Policy:** MERGE/SPLIT **detection/emission as structural commands** is **not** a CST-Core capability (HLR-047). Heritage merge/split *compensation* (exclude parents from instability scoring after lineage events) **is** a useful continuity-interpretation capability and may be retained as local metric hygiene, not as structural authority.

### 3.2 Behaviors proven by heritage tests

| Behavior | Heritage result |
|----------|-----------------|
| Aggregate pre-labeled drift/oscillation/collapse into signal dicts | Yes |
| Echo freeze/thaw from existing `frozen` flags | Yes (not threshold-driven emission) |
| Certainty/ambiguity id lists from object labels | Yes |
| Lineage stable/unstable id lists | Yes |
| MERGE/SPLIT: parent ids excluded from collapse false-positives | Yes |
| Post-structure signal history length capped at 10 | Yes |
| Two independent instances, same inputs → same signals | Yes |

### 3.3 Heritage non-capabilities (explicit)

Heritage path did **not** provide:

- Structural snapshot extraction from COB/OuBA topology  
- Deterministic distance / ambiguity / stability **formulas**  
- Integrated metrics over the 10-turn window (beyond storing signal packages)  
- Threshold tables or threshold adaptation  
- Combined-instability → **emit** Freeze / Thaw  
- Continuity-restoration as a first-class signal  
- `process(tp)` and writes under `TP.cst.core.*`  
- Routing separation (COB-bound vs MS/Mux-only)  
- Progressive dual-mode YAML + rulechecker suite  

---

## 4. Capability Matrix (Target Live Primitive)

| Capability | Normative required | Heritage proven | Live target v0.1 |
|------------|--------------------|-----------------|------------------|
| Snapshot extract per layer | Yes | No | Must-Prove (minimal schema) |
| 10-turn counts/frequencies/histories | Yes | Partial (signal window only) | Must-Prove |
| Drift / oscillation / ambiguity / collapse **compute** | Yes | Reflect only | Placeholder deterministic functions OK if explicit Defer on final math |
| Emit raw metrics to MS + Mux paths only | Yes | No TP routing | Must-Prove routing |
| Emit Freeze / Thaw / Continuity to COB + Mux | Yes | Freeze/thaw echo only; no continuity | Must-Prove emission shape + path |
| Local freeze halt / thaw resume of metric updates | Yes | No | Must-Prove |
| No structural authority (no Create/Split/Merge/Collapse-recovery) | Yes | Mostly (compensation only) | Must-Prove guard |
| No CST-MS command intake | Yes | N/A | Must-Prove |
| MERGE/SPLIT parent exclusion from false instability | Useful | Yes | Retain |
| Progressive dual-mode testbench | Yes (framework) | No | Must-Prove |
| Final distance/ambiguity/collapse formulas | Yes (eventual) | No | **Defer** |
| Numeric thresholds + adaptation law | Yes (eventual) | No | **Defer** (fixed v0.1 defaults allowed) |
| Continuity restoration queue semantics | Yes (eventual) | No | **Defer** |

---

## 5. Gaps / Residual Fog (Defer)

These are acknowledged incomplete relative to full 20.32.010.010 realization. They must not be silently invented in code without CP agreement:

1. **Structural distance functions** per domain (identity, referent, lineage, register, anchors).  
2. **Ambiguity functions** and collapse/stability scoring math.  
3. **Combined instability** aggregation weights.  
4. **Layer-specific thresholds** (drift, oscillation, ambiguity, collapse, freeze, recovery, continuity) and **monotonic adaptation** rules.  
5. **Queued structural corrections** during continuity restoration (local metric-tracking meaning).  
6. **Full nested snapshot schema** field-by-field (beyond domain list: referents, temporal anchors, discourse anchors, lineage, register, field-importance).  
7. **Exact `TP.cst.core.*` path map** (to be locked with patha_field_names / structural program before progressive expected YAML freezes).

---

## 6. Reuse Policy for Implementation

1. **May reuse** heritage signal **field names and dict shapes** listed in §3.1.  
2. **Must not** treat “read `stability_metrics` already on the object and re-emit” as the normative metric pipeline.  
3. **Must** implement `process(tp, mode=...)` and owned TP writes consistent with progressive lineup.  
4. **Must** respect signal routing in §1.2 and write-boundary (no topology edits, no semantic/routing ownership).  
5. **May** use fixed placeholder formulas/thresholds in v0.1 if they are deterministic, documented as provisional, and listed under Defer for replacement.  
6. Bak files remain reference-only; live `cst_core.py` and progressive testbench are the realization surface.

---

## 7. Success Criteria for “Same Capability as Heritage, Plus Normative”

Live CST-Core is considered to have **matched and exceeded** heritage capability when:

- All heritage signal shapes in §3.1 can still be produced (or mapped 1:1 into `TP.cst.core.*`).  
- MERGE/SPLIT parent exclusion still prevents false collapse attribution.  
- 10-turn history length is enforced.  
- Deterministic replay holds.  
- **Additionally:** Freeze/Thaw/Continuity are emission-capable under declared thresholds; raw metrics are not routed as COB structural commands; progressive dual-mode tests pass for the locked envelope.

---

**End of cst_core_capability.md (v0.1)**  
Ready for CP review.

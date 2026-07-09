# path_a_routing_reference.md

**Document ID:** 20.XXX_path_a_routing_reference  
**Version:** 0.1  
**Date:** 2026-07-09  
**Status:** Draft — Reference Paper (Path A)  
**Purpose:** Define the Path A routing reference for the TR, CTP, ISc, RTU, RB, and OuBA primitives, including routing preparation, snapshot context, entropy scoring, routing_update construction, routing_filter construction, termination geometry, and field rules.

---

## 1. Purpose & Scope

This document establishes the canonical routing geometry specifications for the Path A primitives TR, CTP, ISc, RTU, RB, and OuBA. It defines preparation, snapshotting, entropy scoring, update and filter construction, termination, and field rules that ensure deterministic, replay-safe processing.

---

## 2. Routing Domain Overview

The routing domain prepares committed snapshots, computes entropy, constructs routing updates and filters, and determines termination. All operations maintain bounded behavior and deterministic handoffs.

---

## 3. Canonical Routing Geometry

Routing geometry operates on committed snapshots and normalized signatures. Evolution follows deterministic functions.

$$
\text{RoutingState}_{n+1} = f_{\text{det}}(\text{Snapshot}_n, \text{EntropyScore})
$$

---

## 4. TR Gating & Preparation Rules

TR prepares routing metadata from committed snapshots.

**HLR-PA-RTE-001:** TR gating prepares deterministic routing metadata.  
**HLR-PA-RTE-002:** TR precedes every CTP snapshot construction.

---

## 5. CTP Snapshot & Context Preparation

CTP constructs immutable snapshots of committed fields.

**HLR-PA-RTE-003:** CTP produces deterministic immutable snapshots.  
**HLR-PA-RTE-004:** CTP requires preceding TR preparation.

---

## 6. Entropy Scoring Geometry (ISc)

ISc computes entropy scores from snapshots for routing decisions.

**HLR-PA-RTE-005:** Entropy scoring produces bounded tp_entropy_score values.  
**HLR-PA-RTE-006:** Entropy scoring supports deterministic termination decisions.

---

## 7. Routing_Update Construction (RTU)

RTU constructs routing updates from snapshots and entropy.

**HLR-PA-RTE-007:** RTU produces pure routing_update signals.  
**HLR-PA-RTE-008:** RTU construction maintains replay equivalence.

---

## 8. Routing_Filter Construction (RB)

RB constructs routing filters as the sole decision primitive.

**HLR-PA-RTE-009:** RB produces deterministic routing_filter outputs.  
**HLR-PA-RTE-010:** RB uses entropy-informed routing_update for decisions.

---

## 9. Termination Geometry (OuBA)

OuBA handles termination with path_b_eligible signaling.

**HLR-PA-RTE-011:** Termination geometry produces final envelopes with eligibility flags.  
**HLR-PA-RTE-012:** Termination respects entropy-based routing decisions.

---

## 10. Field Allowance Table

| Primitive | Allowed Fields |
|-----------|----------------|
| TR | committed_snapshot, routing_prep_metadata |
| CTP | committed_fields, snapshot_metadata |
| ISc | snapshot, entropy_metadata |
| RTU | snapshot, tp_entropy_score, routing_update |
| RB | routing_update, routing_filter |
| OuBA | final_snapshot, path_b_eligible, terminal_envelope |

---

## 11. Forbidden Field Table

| Primitive | Forbidden Fields |
|-----------|------------------|
| TR | meaning_refinement_fields, structural_geometry_modification |
| CTP | mutable_fields, routing_decision_fields |
| ISc | routing_decision_fields, meaning_refinement_fields |
| RTU | routing_filter_construction, decision_logic |
| RB | routing_update_modification, meaning_fields |
| OuBA | mutable_fields, pre-termination_updates |

---

## 12. Routing Expansion & Determinism Rules

Expansion produces finite routing candidates within bounded geometry.

**HLR-PA-RTE-013:** Routing expansion produces deterministic candidates.  
**HLR-PA-RTE-014:** Routing operations maintain replay equivalence and boundedness.

---

## 13. Testing Requirements

Testing includes replay fixtures, snapshot invariance tests, entropy scoring verification, update and filter consistency tests, and termination invariant assertions.

**HLR-PA-RTE-015:** Routing tests verify determinism and replay equivalence.  
**HLR-PA-RTE-016:** Field allowance and forbidden field tests are mandatory at each handoff.

---

## 14. Canonical Starter Routing Reference File

```markdown
# Canonical Path A Routing Starter
routing_version: "1.0"
snapshot: {...}
tp_entropy_score: 0.0
routing_update: {...}
routing_filter: {...}
provenance: {timestamp, source_id, ...}
```

---

## 15. HLR Traceability Matrix

| HLR ID | Section | Description |
|--------|---------|-------------|
| HLR-PA-RTE-001 | 4 | TR gating prepares deterministic metadata |
| HLR-PA-RTE-002 | 4 | TR precedes every CTP |
| HLR-PA-RTE-003 | 5 | CTP produces immutable snapshots |
| HLR-PA-RTE-004 | 5 | CTP requires preceding TR |
| HLR-PA-RTE-005 | 6 | Entropy scoring produces bounded scores |
| HLR-PA-RTE-006 | 6 | Entropy scoring supports termination |
| HLR-PA-RTE-007 | 7 | RTU produces pure routing_update signals |
| HLR-PA-RTE-008 | 7 | RTU maintains replay equivalence |
| HLR-PA-RTE-009 | 8 | RB produces deterministic routing_filter |
| HLR-PA-RTE-010 | 8 | RB uses entropy-informed update |
| HLR-PA-RTE-011 | 9 | Termination produces eligibility flags |
| HLR-PA-RTE-012 | 9 | Termination respects entropy decisions |
| HLR-PA-RTE-013 | 12 | Routing expansion produces deterministic candidates |
| HLR-PA-RTE-014 | 12 | Routing operations maintain replay equivalence |
| HLR-PA-RTE-015 | 13 | Routing tests verify determinism |
| HLR-PA-RTE-016 | 13 | Field allowance tests are mandatory |

**End of path_a_routing_reference.md**
```

# `subsystem_notes.md`

# Subsystem Notes — Path A Simulation
This document captures subsystem‑level notes, constraints, invariants, and
observations relevant to executing Path A as a multi‑primitive subsystem.
Primitive‑local notes remain inside each primitive’s folder under `../path_a/`.

All terminology and primitive behavior follow **20.190** exactly.

---

# 1. Subsystem‑Level Invariants

## 1.1 Single‑Writer Rule
Only two primitives may write TP‑stream fields:

- **TPU** — meaning‑layer corrections  
- **OuBA** — final commit boundary

All other primitives are strictly read‑only.

This invariant must be preserved in all subsystem simulations.

---

## 1.2 Replay Stability
Subsystem simulation must ensure:

- Structural residue (SOB → SROB → CnOB) is deterministic.
- Semantic‑adjacent and semantic‑layer hashes (SmOB, SSG, STPX) are stable.
- RB routing decisions are identical across replays.
- IdOB cycles converge deterministically.

Replay instability indicates either:
- incorrect residue formation,  
- incorrect routing cues, or  
- incorrect context handling.

---

## 1.3 Context Boundaries
Context machinery must remain bounded:

- **CEx** evaluates relevance only using MSL tokens, qualifiers, continuity signals.
- **CE** copies forward only `MCB.next_context`.
- **MCB** writes only short‑term context for the next turn.

Subsystem simulation must verify that:
- CE never leaks global state.
- MCB never writes long‑horizon identity.
- CEx never reads global context.

---

# 2. Multi‑Cycle Behavior

## 2.1 Identity Cycles
IdOB may run multiple cycles when:

- qualifiers shift meaning,
- subculture changes,
- semantic‑adjacent cues indicate instability,
- routing metadata (TP.TR) suggests refinement.

Subsystem simulation must confirm:
- IdOB cycles terminate deterministically,
- CTP consolidates all IdOB outputs correctly,
- RB decisions reflect stable routing conditions.

---

## 2.2 Correction Cycles
RB may signal `needs_correction`, causing a return to:

```
CE → ISc → TPU
```

Subsystem simulation must verify:
- CE reinitializes context correctly,
- ISc scoring is deterministic,
- TPU corrections preserve upstream commitments.

---

# 3. Routing Notes

## 3.1 TR vs RB
**TR** computes routing vector TP.TR  
**RB** selects basins

Subsystem simulation must ensure:
- TR never selects basins,
- RB never computes routing vectors,
- TR and RB consume the correct residue (OB, DCB, SmOB, SSG, STPX).

---

## 3.2 Routing Inputs
RB uses:

- structural residue (SOB → SROB → CnOB),
- semantic‑adjacent cues (SmOB),
- semantic‑layer cues (STPX),
- SSG signals,
- stabilized TP‑stream geometry.

Subsystem simulation must confirm all routing inputs are present and stable.

---

# 4. Residue Notes

## 4.1 Structural Residue
SOB → SROB → CnOB must produce:

- clause boundaries,
- structural anchors,
- canonical ordering,
- constraint markers,
- conflict indicators.

Subsystem simulation must check residue consistency across noisy inputs.

---

## 4.2 Semantic‑Adjacent and Semantic‑Layer Residue
SmOB → SSG → STPX must produce:

- semantic‑adjacent activation vectors,
- modality/stance cues,
- semantic‑layer hashes,
- referent‑adjacent signals.

Subsystem simulation must verify:
- hashes are deterministic,
- cue vectors are stable,
- residue is replay‑safe.

---

# 5. Commit and Freeze Notes

## 5.1 OuBA Commit
OuBA must:

- freeze semantic_core,
- write commit‑time metadata,
- preserve all TP‑stream fields except at commit boundary.

Subsystem simulation must confirm:
- no semantic correction occurs at OuBA,
- commit boundary is deterministic.

---

## 5.2 SSRGn Freeze
SSRGn must:

- project TP_committed,
- sanitize fields,
- bind RRw and policy_signature,
- freeze semantic_core and identity metadata.

Subsystem simulation must verify:
- SSR is deterministic,
- SSR contains only Path‑B‑visible fields,
- no mutable TP fields are read or written.

---

# 6. Subsystem‑Level Checks

## 6.1 Determinism Checks
- All residue hashes must match across runs.
- RB routing decisions must be identical.
- IdOB cycles must converge deterministically.
- CE relevance decisions must be stable.

## 6.2 Isolation Checks
- No primitive except TPU and OuBA may write TP‑stream fields.
- No primitive may read global state.
- Context machinery must remain bounded.

## 6.3 Flow Integrity Checks
- All primitives must run in correct order.
- No primitive may skip required upstream residue.
- Multi‑cycle replay must stabilize meaning before OuBA.

---

# Notes
- All primitive names and behaviors come directly from **20.190**.  
- No expansions or terminology are invented.  
- This file describes subsystem‑level notes, not primitive‑local behavior.  
- Primitive‑local notes remain under `../path_a/`.

```

---

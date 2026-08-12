# ⭐ **tp_path_a_map.md**
### *Conductor’s Map of Path-A*
### *Movements, Sequence, and What Each Primitive Reads / Writes*

This document is the high-level map of Path-A.  
It shows the five movements, the exact primitive sequence, and the main field groups each primitive reads and writes.  
Detailed instrument parts remain in the theory papers and the 20-series requirements.

---

## 1. The Five Movements (Conductor Overview)

| Movement | Name | What happens | Primary instruments | Control point |
|----------|------|--------------|---------------------|---------------|
| **1** | Intake | External input normalized; first committed representation appears | InB → IIInB → IE | IE is first commit boundary |
| **2** | Context & Relevance | Continuity / identity constraints applied; Context Frame produced | CEx (IE/CCR/Pck) → CE | Context Frame created |
| **3** | Cue Extraction & Routing | Structural / semantic cues extracted; routing decides next basin | TPU → OB family → SSG/STPX → RBU/DCB/TR/RB | **RB is the baton** |
| **4** | Identity-Conditioned Refinement | IdOB refines referents, qualifiers, subculture, stance, etc. | IdOB (cycles) → MCB → (back to routing) | Cycles until stable |
| **5** | Commit | Meaning finalized and frozen | OuBA | Final downbeat |

After Movement 5 the long-term conversation block (COB / CST-* / CIL) runs.

---

## 2. Sequential Primitive Map (Path-A)

Exact flow you supplied:

```
InB → IIInB → IE → CEx → CE → TPU → SOB → SROB → CnOB → SmOB → ISc → SSG → STPX → RBU → DCB → RB → TR → CTP → ISc → RTU → RB → IdOB → MCB → RBU → DCB → RB → TR → CTP → ISc → RTU → RB → IdOB → MCB → …
OR
DCB → RB → TR → CTP → ISc → RTU → RB → OuBA
```

### Movement 1 — Intake

| Primitive | Reads | Writes / Produces | Notes |
|-----------|-------|-------------------|-------|
| **InB** | Raw external input | Initializes TP-stream to neutral defaults (`semantics/meaning`, `processes`); `intake_metadata`; supervisor empty | No meaning assigned. Decides Clean vs Corrected Flow. |
| **IIInB** | Pre-commit TP-stream | Repair proposals only (not committed) | Bounded shorthand repair proposals. Does not commit. |
| **IE** | IIInB proposals + TP-stream | Commits `semantics/meaning` + `processes`; first committed intake envelope; Identity block | **First commit boundary.** Supervisor remains empty. |

### Movement 2 — Context & Relevance

| Primitive | Reads | Writes / Produces | Notes |
|-----------|-------|-------------------|-------|
| **CEx** (IE → CCR → Pck) | IE intake, prior context / CIL lineage, semantic-importance (if present) | `TP.cex.ie`<br>`TP.cex.ccr` (alignment, scores, decision, selected_conversation)<br>`context_metadata`<br>`msl_metadata`<br>`cil_metadata`<br>`semantic_residue_metadata` | Sole relevance evaluator. Packages context. |
| **CE** | CEx packages + prior `next_context` | Canonical **Context Frame** / context shell | Safe isolated context for downstream. |

### Movement 3 — Cue Extraction & Routing

| Primitive | Reads | Writes / Produces | Notes |
|-----------|-------|-------------------|-------|
| **TPU** | CE + CEx + ISc scoring | Meaning-layer corrections (authorized fields only) | **Sole Path-A writer** for many meaning fields before final commit. Single-writer invariant. |
| **SOB** | TP-stream (read-only) | Structural residue / structural-importance signals | Read-only. First structural pass. |
| **SROB** | TP-stream + SOB residue | Refined structural residue | Read-only. |
| **CnOB** | TP-stream + refined structure | Constraint residue / constraint-importance | Read-only. |
| **SmOB** | TP-stream + prior residues | Semantic-adjacent cues + pre-semantic hash + TR-input vector; contributes to `semantic.importance` | Read-only. |
| **ISc** | CE + candidate set + TP-stream | `score_set`, `score_conflict`, `score_reason_code` | Read-only. Scoring only. |
| **SSG** | SmOB residue + TP | Semantic-adjacent activation vectors | Read-only. |
| **STPX** | SSG + prior cues | Semantic-layer cues / hash | Read-only. |
| **RBU** | Latest cues + prior routing state | Updated routing state (**tentative**) | Routing update step. |
| **DCB** | Trajectory / cue history | Curvature / instability signals (**tentative**) | Supports TR / RB. |
| **TR** | OB residues + DCB signals | Routing vector `TP.TR` | Guides RB; does not select. |
| **RB** | Context Frame, MSL, residues, semantic-importance, identity flags, commitments, freeze signatures, curvature, `TP.TR` | Basin decision (structural / semantic / identity / correction / commit); `routing_metadata` | **Active baton.** Does not write meaning. |
| **CTP** | IdOB-set outputs | Consolidated IdOB-output packet | Collects before next arbitration. Read-only w.r.t. meaning. |
| **RTU** | Consolidated state + routing decision | Routing commit / update (**tentative**) | Appears in flow after CTP. |

### Movement 4 — Identity-Conditioned Refinement

| Primitive | Reads | Writes / Produces | Notes |
|-----------|-------|-------------------|-------|
| **IdOB** | CE context shell, CEx-CCR signals, semantic-adjacent / semantic-layer cues, MSL, existing identity state, commitments, freeze signatures, referent lineage | Refined referents + lineage<br>Qualifiers + clusters<br>Subculture<br>Stance / direction / coherence<br>Updated semantic-importance<br>Identity continuity flags<br>`identity_metadata` | **Only primitive that performs identity-conditioned meaning updates.** Multiple cycles allowed. |
| **MCB** | IdOB identity-conditioned payload | `next_context_metadata` (next_context, direction, coherence, stance, subculture, …) | Writes short-term context for next turn. |

After IdOB / MCB the flow normally returns to RBU → DCB → RB … for another routing decision (more cycles) or proceeds toward commit.

### Movement 5 — Commit

| Primitive | Reads | Writes / Produces | Notes |
|-----------|-------|-------------------|-------|
| **OuBA** | Fully refined meaning + identity state, continuity flags, routing eligibility (commit path), curvature / stability signals | Frozen `semantic_core` + meaning-bearing fields<br>`freeze_metadata`<br>Commit-time provenance & resolution flags<br>**Committed TP snapshot** | **Final writer.** Terminates Path-A. Single-writer at commit time. |

---

## 3. Post-Commit Block (Long-Term Conversation)

```
OuBA → COB
OuBA → CSTCore
CSTCore → CSTMS → CSTMux
CSTCore → COB
CSTMS → COB
COB ↔ CSTCore / CSTMS
CSTMux → CIL
COB → CIL
```

| Component | Role (tentative from architecture) | Main reads | Main writes / effects |
|-----------|------------------------------------|------------|-----------------------|
| **COB** | Continuity Object Builder – projects committed importance / residue into selected conversation | Committed snapshot, `semantic.importance`, CCR `selected_conversation`, CIL metadata | Continuity objects / projections for CIL (linear, no inference) |
| **CST-CORE** | Core stability tracker | Committed state + continuity signals | Stability core state |
| **CST-MS** | Stability micro-signals | CST-CORE | Micro-signals |
| **CST-MUX** | Stability multiplexer | CST-CORE + CST-MS | Multiplexed stability signals → CIL |
| **CIL** | Conversation Intake Layer (next-turn substrate) | COB projections + CST-MUX | Prepares selected conversation substrate for next turn’s CEx |

These components operate **after** Path-A commit and do not rewrite Path-A meaning.

---

## 4. Key Control Rules (Baton)

- **Single-writer (meaning)**: TPU (during Path-A) and OuBA (at commit). Most other primitives are TP-stream read-only.
- **Routing is the real-time baton**: RB decides the next basin or commit.
- **IdOB cycles** continue while identity-conditioned work remains; routing re-evaluates after each cycle.
- **Freeze signatures & commitments** are hard constraints that can block commit and force further IdOB cycles.
- **Context Frame** (produced in Movement 2) is the first major stabilized view of meaning + identity for the rest of Path-A.

---

## 5. Status of this Map

- Entries drawn from `20.700.010` glossary are solid.
- Entries for RBU, DCB, RTU, COB, CST-*, CIL are **tentative** (glossary silent or thin) and should be confirmed against their detailed requirement documents.
- Field groups are the major envelopes; individual sub-fields live in `20.105.010` and related docs.

This document is the conductor’s map.  
The nine theory/architecture papers remain the detailed instrument parts.

---

**End of tp_path_a_map.md**

---

# ⭐ **tp_path_a_map.md — Conductor’s Map of Path‑A**  
### *Movements, Sequence, and What Each Primitive Reads / Writes*  
### *Version 4.0 — Metadata‑Aligned, Pipeline‑Aligned Rewrite*

This document is the high‑level conductor’s map of Path‑A.  
It describes the five movements, the canonical primitive sequence, and the major TP field groups each primitive reads and writes.  
Detailed instrument parts remain in the 20‑series requirements.

---

# **1. The Five Movements (Conductor Overview)**

| Movement | Name | What happens | Primary instruments | Control point |
|----------|------|--------------|---------------------|---------------|
| **1** | Intake | External input normalized; first committed representation appears | InB → IIInB → IE | IE is the first commit boundary |
| **2** | Context & Relevance | Continuity, identity, and relevance constraints applied; Context Frame produced | CEx (IE → CCR → Pck) → CE | Context Frame created |
| **3** | Cue Extraction & Routing | Structural cues extracted; routing determines next basin | TPU → OB‑Set → SSG → STPX → RBU → DCB → TR → CTP → ISc → RTU → RB | **RB is the baton** |
| **4** | Identity‑Conditioned Refinement | Identity‑conditioned meaning refinement cycles | IdOB → MCB → (back to routing) | Cycles until stable |
| **5** | Commit | Meaning finalized and frozen | OuBA | Final downbeat |

After Movement 5, the long‑term conversation block (COB / CST‑* / CIL) runs.

---

# **2. Sequential Primitive Map (Canonical Path‑A Flow)**

The canonical Path‑A pipeline defined in 20.15 is:

```
InB → IIInB → IE
→ CEx (IE → CCR → Pck) → CE
→ TPU
→ SOB → SROB → CnOB → SmOB
→ WrdNm
→ ISc
→ SSG → STPX
→ RBU → DCB → TR → RB → CTP → WrdNm → ISc → RTU 
→ TR → RB → IdOB → MCB
→ (repeat routing loop until stable)
→ OuBA
```

A commit path may occur when RB selects the commit basin:

```
RBU → DCB → TR → RB → CTP → WrdNm → ISc → RTU → TR → RB → OuBA
```

Below is the movement‑aligned breakdown.

---

## **Movement 1 — Intake**

| Primitive | Reads | Writes / Produces | Notes |
|-----------|-------|-------------------|-------|
| **InB** | Raw external input | Initializes TP to neutral defaults; `intake_metadata`; empty supervisor | No meaning assigned. Determines Clean vs Corrected flow. |
| **IIInB** | Pre‑commit TP | Repair proposals only | Proposals are bounded and not committed. |
| **IE** | IIInB proposals + TP | First committed intake envelope; identity block; normalization metadata | **First commit boundary.** |

---

## **Movement 2 — Context & Relevance**

| Primitive | Reads | Writes / Produces | Notes |
|-----------|-------|-------------------|-------|
| **CEx** (IE → CCR → Pck) | IE intake; prior context; CIL lineage; semantic‑importance | `TP.cex.ie`<br>`TP.cex.ccr` (alignment, scores, decision, selected_conversation)<br>`TP.metadata.context_metadata`<br>`TP.metadata.msl_metadata`<br>`TP.metadata.cil_metadata`<br>`TP.metadata.semantic_residue_metadata` | Sole relevance evaluator. Packages context deterministically. |
| **CE** | CEx packages; prior `next_context_metadata` | Canonical **Context Frame** | Stabilized context shell for downstream primitives. |

---

## **Movement 3 — Cue Extraction & Routing**

| Primitive | Reads | Writes / Produces | Notes |
|-----------|-------|-------------------|-------|
| **TPU** | CE; CEx metadata; ISc scoring | Meaning‑layer corrections (authorized fields only) | **Single‑writer** for meaning before commit. |
| **SOB** | TP (read‑only) | Structural residue; structural‑importance | First structural pass. |
| **SROB** | SOB residue | Refined structural residue | Read‑only. |
| **CnOB** | Refined structure | Constraint residue; constraint‑importance | Read‑only. |
| **SmOB** | Prior residues | Semantic‑adjacent structural cues; pre‑semantic hash; TR‑input vector; updates `semantic.importance` | Read‑only. |
| **ISc** | CE; candidate set; TP | `score_set`, `score_conflict`, `score_reason_code` | Scoring only. |
| **SSG** | SmOB residue; structural metadata | Structural‑invariant vector (`tp.ssg_signature`); layer bitmap; reason code; status | Structural‑only invariant extraction. |
| **STPX** | SSG outputs; structural metadata; canonical tokens | `TP.metadata.semantic_layer_metadata.stpx_cues` | Deterministic cue extraction; structural‑only. |
| **RBU** | Latest cues; routing state | Updated routing state (tentative) | Routing update step. |
| **DCB** | Cue history; trajectory | Curvature / instability signals | Supports TR and RB. |
| **TR** | OB residues; DCB signals | Routing vector | Guides RB; does not select. |
| **CTP** | IdOB outputs (from prior cycle); frozen TP snapshot | Consolidated IdOB packet; append‑only cognitive‑history entry (`TP.metadata.cognitive_history[]`); snapshot freeze | Read‑only w.r.t. meaning; structural bookkeeping only. |
| **ISc** (second pass) | Consolidated packet; context | Updated scoring | Used in routing loop. |
| **RTU** | Consolidated state; routing decision | Routing commit/update (tentative) | Pre‑RB consolidation. |
| **RB** | Context Frame; MSL; residues; semantic‑importance; identity flags; commitments; freeze signatures; curvature; TR vector | Basin decision; routing metadata | **Active baton.** No meaning writes. |

---

## **Movement 4 — Identity‑Conditioned Refinement**

| Primitive | Reads | Writes / Produces | Notes |
|-----------|-------|-------------------|-------|
| **IdOB** | Context Frame; CCR signals; structural cues; semantic‑layer cues; MSL; identity state; commitments; freeze signatures; referent lineage | Refined referents; lineage; qualifiers; clusters; subculture; stance; direction; coherence; updated semantic‑importance; identity continuity metadata | **Only primitive that performs identity‑conditioned meaning updates.** Multiple cycles allowed. |
| **MCB** | IdOB identity‑conditioned payload | `next_context_metadata` | Short‑term context for next turn. |

After IdOB → MCB, the pipeline returns to:

```
RBU → DCB → TR → RB → CTP → WrdNm → ISc → RTU
```

until RB selects commit or another IdOB cycle.

---

## **Movement 5 — Commit**

| Primitive | Reads | Writes / Produces | Notes |
|-----------|-------|-------------------|-------|
| **OuBA** | Fully refined meaning; identity state; continuity flags; routing eligibility; curvature/stability signals | Frozen `semantic_core`; meaning‑bearing fields; `freeze_metadata`; commit‑time provenance; committed TP snapshot | **Final writer.** Terminates Path‑A. |

---

# **3. Post‑Commit Block (Long‑Term Conversation)**

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

| Component | Role | Main reads | Main writes / effects |
|-----------|------|------------|-----------------------|
| **COB** | Projects committed importance/residue into selected conversation | Committed snapshot; `semantic.importance`; CCR `selected_conversation`; CIL metadata | Continuity objects for CIL (linear, no inference) |
| **CST‑CORE** | Core stability tracker | Committed state; continuity signals | Stability core state |
| **CST‑MS** | Stability micro‑signals | CST‑CORE | Micro‑signals |
| **CST‑MUX** | Stability multiplexer | CST‑CORE + CST‑MS | Multiplexed stability signals → CIL |
| **CIL** | Conversation Intake Layer | COB projections; CST‑MUX | Prepares selected conversation substrate for next turn’s CEx |

These components operate **after** Path‑A commit and do not rewrite Path‑A meaning.

---

# **4. Key Control Rules (Baton)**

- **Single‑writer (meaning)**: TPU during Path‑A; OuBA at commit.  
- **RB is the baton**: RB determines the next basin or commit.  
- **IdOB cycles** continue while identity‑conditioned work remains; routing re‑evaluates after each cycle.  
- **Freeze signatures & commitments** are hard constraints that may block commit and force additional cycles.  
- **Context Frame** is the first stabilized view of meaning + identity for the rest of Path‑A.

---

# **5. Status of This Map**

- Entries drawn from the 20.700.010 glossary are stable.  
- RBU, DCB, RTU, COB, CST‑*, and CIL remain partially specified and should be confirmed against their detailed requirement documents.  
- Field groups shown here are major envelopes; individual sub‑fields are defined in 20.105.010 and related metadata documents.

This document is the conductor’s map.  
The nine theory/architecture papers remain the detailed instrument parts.

---

# **End of tp_path_a_map.md (Version 4.0)**

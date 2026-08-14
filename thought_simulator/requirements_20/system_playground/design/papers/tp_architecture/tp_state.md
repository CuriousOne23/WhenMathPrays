### ⭐ **tp_state.md**  
#### *The TP Packet, Field Groups, Ownership, Freeze Points, and Producer/Consumer Map*

---

## 1. Purpose

This document defines the **TP state object** for Path‑A:

- the **field groups** that make up the TP packet,  
- **who writes** each field (by primitive),  
- **who reads** each field,  
- **when it freezes**,  
- **how it behaves across turns**.

It is the coordination substrate that lets the primitives in `tp_path_a_map.md` act as one deterministic pipeline.

### **Freeze Points**

A *freeze point* is a deterministic phase boundary in Path‑A where a specific subset of TP fields becomes immutable for the remainder of the turn. Freeze points are not commits (except the final one); they are local freezes that ensure determinism, prevent backtracking, and guarantee that downstream primitives cannot rewrite upstream decisions.

Path‑A has four freeze points:

- **IE Freeze** — intake envelope and initial meaning/identity shell  
- **CE Freeze** — Context Frame and context metadata  
- **OB Freeze** — structural, constraint, semantic‑adjacent, and semantic‑layer residues  
- **Commit Freeze (OuBA)** — meaning core, identity core, commitments, freeze signatures, provenance, next_context

Each freeze point locks its field group and establishes a stable substrate for the next movement.

---

### **Across Turns**

“Across turns” describes how TP fields behave after commit.  
There are three behaviors:

1. **Not carried across turns** — residues, routing metadata, curvature, scoring, intake envelope (except committed meaning/identity).  
2. **Carried across turns (committed snapshot)** — meaning core, identity core, commitments, freeze signatures, semantic‑importance, next_context, continuity flags, lineage fields, stance/direction/coherence, subculture, identity anchors.  
3. **Carried indirectly (COB/CST/CIL)** — continuity objects, stability signals, cil_substrate.

These behaviors define the cross‑turn contract of the TP packet.

Here’s the crisp, architecturally correct answer — **“turn” means one full Path‑A traversal**, from InB all the way through OuBA, including any IdOB cycles and routing loops.

But let me give you the exact definition you need for **tp_state.md**, because this is one of the most important concepts in the entire TS architecture.

---

### **What a Turn Is**

A *turn* is one complete traversal of Path‑A, beginning at InB and ending at OuBA.  
A turn includes intake normalization, context formation, cue extraction, routing cycles, identity‑conditioned refinement, and final commit.  
The output of a turn is the committed TP snapshot, which becomes the input substrate for the next turn via COB/CST/CIL and next_context.

---

## 2. TP Packet Overview

The TP packet is a **single evolving state object** (conceptual) with the following major field groups:

- **Intake & Envelope**  
- **Context & Relevance**  
- **Structural / Constraint / Semantic‑Adjacent / Semantic‑Layer Residue**  
- **Routing & Curvature**  
- **Identity & Commitments**  
- **Continuity & Drift**  
- **Commit & Freeze**  
- **Next‑Turn Context & Long‑Term Conversation Hooks**

---

## 3. TP State Table (Field Groups, Ownership, Freeze Points)

> This table is intentionally at **field‑group** granularity. Sub‑fields live in the 20‑series requirements.

| Field Group | Example Fields | Written By (Primitives) | Read By (Primitives) | Freeze At | Cross‑Turn Behavior | Required For |
|------------|----------------|--------------------------|----------------------|-----------|---------------------|--------------|
| **Intake Envelope** | `raw_input`, `intake_metadata`, initial `meaning_shell` | **InB**, IIInB (repair proposals), **IE** (first commit) | CEx, CE, TPU, OB family, IdOB | **IE** (first intake commit) | Carried into Context & Relevance; not preserved beyond OuBA except via committed snapshot | Normalization, Clean vs Corrected flow, initial meaning shell |
| **Meaning Core (pre‑commit)** | `semantic_core`, `meaning_fields` (clauses, roles, propositions) | **TPU** (Path‑A corrections), IE (initial shell) | OB family (SOB/SROB/CnOB/SmOB/SSG/STPX), IdOB, RB, TR, DCB, OuBA | **OuBA** (final commit) | Committed snapshot persists; pre‑commit versions not carried across turns | Deterministic meaning construction, correction, commit |
| **Structural Residue** | `structural_residue`, `structural_importance`, `clause_boundaries`, `anchors` | SOB, SROB | CnOB, SmOB, SSG, STPX, RB, TR | Stable after OB pass; effectively frozen for later cycles | Not carried across turns; recomputed per turn | Structural basin selection, constraint interpretation, routing |
| **Constraint Residue** | `constraint_residue`, `missing_slots`, `conflict_indicators`, `constraint_importance` | CnOB | SmOB, SSG, STPX, RB, TR, TPU (for corrections) | Stable after CnOB; frozen for routing in current turn | Not carried across turns; recomputed per turn | TPU correction decisions, routing to correction basin |
| **Semantic‑Adjacent Residue** | `semantic_adjacent_cues`, `modality`, `affect`, `underspec_markers`, `pre_semantic_hash`, `activation_vectors` | SmOB, SSG | STPX, IdOB, RB, TR, DCB | Stable after SSG/STPX; frozen for identity and routing | Not carried across turns; recomputed per turn | Semantic basin selection, IdOB triggers, curvature |
| **Semantic‑Layer Residue** | `semantic_layer_hash`, `role_adjacency`, `frame_markers` | STPX | RB, TR, IdOB, DCB, OuBA (for stability checks) | Stable after STPX; frozen for rest of turn | Not carried across turns; recomputed per turn | Semantic stability, commit eligibility, routing |
| **Context Frame** | `ContextFrame_t` (topic, intent, stance, referents, commitments, importance, identity flags, freeze status, clarifying metadata, `next_context_in`) | CEx → **CE** | RB, IdOB, TPU, DCB, TR, OuBA | **CE** (context freeze) | Committed snapshot feeds next turn’s CEx; current turn’s frame not reused | Safe context shell, routing inputs, identity/continuity enforcement |
| **Routing Metadata** | `TP.TR` (routing vector), `routing_metadata`, basin decisions | TR (vector), RB (decision), RBU/RTU (updates) | All downstream primitives (TPU, IdOB, OuBA, OB family for cycles) | Updated per routing cycle; no cross‑turn persistence | Not carried across turns | Basin selection, cycle control, commit path selection |
| **Curvature & Stability** | `curvature_signals`, `instability_flags`, `shift_required` | DCB | RB, TR, TPU, OuBA, IdOB | Updated per cycle; evaluated at commit | Not carried across turns | Bounding cycles, commit eligibility, routing escalation |
| **Identity Core** | `identity_state`, `referent_lineage`, `qualifier_lineage`, `subculture`, `stance/direction/coherence`, `identity_anchors` | **IdOB** (authoritative identity side), IE (initial identity shell) | IdOB (subsequent cycles), RB, OuBA, COB/CST, Context Layer | Stable at commit; “stably open” allowed with flags | Committed identity state persists across turns via COB/CST/CIL | Identity continuity, referent stability, commitments, freeze signatures |
| **Commitments** | `commitment_set`, `commitment_status`, `open_commitments`, `resolved_commitments` | IdOB (interpretation), Context Layer (intake), OuBA (final status) | RB (eligibility), IdOB, OuBA, COB/CST | Stable at commit; open commitments carried with explicit status | Carried across turns via committed snapshot and COB/CST | Long‑horizon obligations, continuity, identity enforcement |
| **Freeze Signatures** | `freeze_signatures`, `freeze_metadata`, frozen anchors (referents, commitments, identity, semantic‑importance, stance/direction/coherence, subculture) | Identity Layer (authoritative), IdOB (updates), OuBA (commit‑time freeze) | RB, IdOB, TPU, OuBA, Context Layer | Effective as soon as set; enforced at commit | Carried across turns via committed snapshot | Hard constraints, commit blocking, identity/continuity protection |
| **Continuity & Drift Signals** | `drift_signals`, `continuity_flags`, `importance_drift`, `identity_drift` | Context Layer (CEx/CE), IdOB, COB/CST | RB, IdOB, OuBA, TPU | Evaluated per turn; continuity state updated at commit | Carried via COB/CST/CIL into next turn | Cross‑turn stability, routing escalation, IdOB triggers |
| **Identity Continuity Flags** | `identity_continuity_flags` (raised/cleared) | IdOB | RB, OuBA, Context Layer | Must be cleared or stably carried before commit | Carried across turns only when stably open | IdOB cycles, commit gating, continuity enforcement |
| **ISc Scoring** | `score_set`, `score_conflict`, `score_reason_code` | ISc | TPU, RB, TR, Context Layer | Per‑decision; no cross‑turn persistence | Not carried across turns | Correction decisions, routing to TPU |
| **Commit Snapshot** | `committed_tp_snapshot` (frozen meaning, identity, context, commitments, freeze status, provenance) | **OuBA** | COB, CST‑CORE, CST‑MS, CST‑MUX, CIL | **OuBA** (final freeze) | This is the only TP state that persists across turns | Long‑term continuity, next‑turn intake substrate |
| **Next‑Context Metadata** | `next_context` (qualifiers, stance, direction, coherence, subculture, clarifications) | **MCB** | Next turn’s CEx/CE, Context Layer | Written before commit; logically part of committed snapshot | Carried into next turn’s Context & Relevance layer | Cross‑turn conversational continuity, stance/qualifier propagation |
| **Long‑Term Conversation Hooks** | `continuity_objects`, `stability_core_state`, `stability_micro_signals`, `stability_mux_signals`, `cil_substrate` | COB, CST‑CORE, CST‑MS, CST‑MUX, CIL | Next turn’s CEx/CE, InB/IE | Defined post‑commit; outside Path‑A write authority | Persist across turns as long‑term substrate | Conversation selection, relevance, stability tracking |

---

## 4. Single‑Writer & Ownership Summary (By Primitive)

- **InB / IIInB / IE**  
  - Own **initial intake envelope** and first committed shell of meaning/identity.  
  - After IE, intake fields are **read‑only** for Path‑A.

- **TPU**  
  - **Only Path‑A writer** for many **meaning fields** before commit.  
  - Writes corrections into `semantic_core` and related meaning fields.  
  - Never writes identity or context.

- **OB Family (SOB, SROB, CnOB, SmOB, SSG, STPX)**  
  - **Read‑only** over TP packet.  
  - Write only **residue fields** (structural, constraint, semantic‑adjacent, semantic‑layer).

- **Context Layer (CEx, CE)**  
  - Writes **Context Frame** and **context metadata**.  
  - After CE, Context Frame is **frozen** for the turn.

- **Routing Layer (RBU, DCB, TR, RB, RTU)**  
  - Write **routing metadata**, **curvature**, **routing vector**.  
  - **Never write meaning or identity.**

- **IdOB**  
  - **Only writer** of **identity core** (referents, qualifiers, subculture, stance/direction/coherence, semantic‑importance as identity‑conditioned).  
  - Writes **identity continuity flags** and updates **commitments** and **freeze signatures** on the identity side.

- **MCB**  
  - Writes **next_context** metadata only.  
  - Does not write meaning or identity core.

- **OuBA**  
  - **Final single writer** at commit.  
  - Freezes `semantic_core`, meaning fields, identity core, commitments, freeze signatures, and provenance into the **committed snapshot**.

- **COB / CST‑CORE / CST‑MS / CST‑MUX / CIL**  
  - Operate **post‑commit**.  
  - Consume committed snapshot; write long‑term continuity and stability structures.  
  - **Never rewrite Path‑A meaning.**

---

## 5. How to Use This Document

- When you ask:  
  **“What fields matter to this primitive?”** → check the **TP State Table** row for that field group and the **Single‑Writer summary**.
- When you ask:  
  **“Are we being wasteful?”** → look for field groups with few consumers or redundant information and test whether they can be merged or removed.
- When you ask:  
  **“Is the packet efficient and necessary?”** → use the **Required For** column to see which invariants or primitives depend on each field group.

This document, together with `tp_path_a_map.md`, gives you:

- the **global conductor view** (movements + primitives), and  
- the **field‑level coordination substrate** (packet + ownership + freeze points).

That’s the combination you were missing.

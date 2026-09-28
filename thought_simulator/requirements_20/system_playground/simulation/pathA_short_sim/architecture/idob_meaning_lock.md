# Path A — what meaning is here

**Date:** 2026-09-28  
**Companion to:** [IdOB_unified_plan.md](IdOB_unified_plan.md)  
**Seam:** [idob_seam.md](idob_seam.md)  
**Space:** [idob_object_space.md](../notes/idob_object_space/idob_object_space.md)

This page is the Path‑A short-sim **meaning contract** in teaching voice. Engine gates stay in the unified plan. Do not import Structure-to-Meaning (S2M), Cognitive Identity Envelope (CIE), or Meaning Signal Layer (MSL) into Identity Observation Block (IdOB).

---

## This world → this path

In ordinary talk, *meaning* is “what the sentence is about.” *The sky is blue.* already feels finished.

On this path, meaning is not a feeling, not a dictionary entry, not MSL stance, and not the S2M vector $M$.

**Meaning on Path‑A short sim = the `idob_packet` produced by summing contributions from activated IdOB objects (IdOBObjects).**

$$
\mathcal{I}=\{o_k\},\quad
A(U)=\{o\in\mathcal{I}:\mathrm{act}_o(\mathrm{freeze}(U))=1\},\quad
\mathrm{IdOB}(U)=\bigoplus_{o\in A(U)}c_o
$$

Identity-conditioning here: geometry = indicator of $A(U)$ plus claimed roles. **No embeddings.** That is not CIE $M' = M + \alpha I$.

MSL may later be **read** as a packaging cue on the Thought Packet (TP). IdOB must not own or rewrite MSL. CIE and S2M $M$ stay in S2M papers. They do not wait inside the Meaning Composition Block (MCB). MCB on this path is still unified-plan R5 copy-only.

---

## Instrument alias table

| Field / name | What it is | What it is not |
|---|---|---|
| `meaning_delta` | Path‑A packet field: legacy writer vs split writer on `truth_relation`, `identity_geometry`, `semantic_core_tokens` (`idob/sum.py`) | S2M motion |
| `meaning_delta_h` / $\Delta h$ | S2M: $\|M_i-M_{i-1}\|$ after CIE | `meaning_delta` |
| Entropy $\Delta H\%$ | Routing / entropy metadata | Either meaning instrument |
| MSL stance | TP metadata packaging cue | CIE; IdOB geometry |

---

## Packet keys (`idob/sum.py`)

`identity_geometry`, `truth_relation`, `truth_relation_family`, `semantic_core` (**dict**), `selected_ops`, `claimed_fields`, `contributors`, `contributions`, `activation_set`, `inactive_objects`, `residual_activated`, `overlap_events`, `meaning_delta`, `psc_violations`, `registry_digest`, `complete`, `tru_hint`.

`semantic_core` keys allowed by schema: `theme`, `state`, `location`, `agent`, `action`, `patient`, `query_focus`, `predicate`, `complement`, `relation_modifiers`, `modifiers`, `selected_ops`.

The debugger observes this packet. It does not perform a second sum.

---

## Live catalog caveat

Eight YAML **names**. Two helpers do not set `family = name`:

- `agent_action` declares `family: residual_identity`
- `modifier_resolution` declares `family: mixed_descriptive`

Activation trees in v1 YAML are `{}`. Apply still points at `idob.legacy`. See object-space.

---

## Who does not write meaning

Segment Observation Block (SOB), Segment Role Observation Block (SROB), Constraint Observation Block (CnOB), and Smoothing Observation Block (SmOB) write structure. Truth-Relation Update (TRU) writes `tru_hint` and must not clobber a completed IdOB mood. Output Binding / Assemble (OuBA) freezes. MCB is omitted.

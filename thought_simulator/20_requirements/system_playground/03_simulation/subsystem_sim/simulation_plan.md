# Path A Subsystem Simulation Plan
This document defines the subsystem‑level simulation plan for Path A using
the canonical primitive definitions from **20.190**.  
Primitive‑local simulation remains inside each primitive’s folder under `../path_a/`.

Subsystem‑level simulation focuses on multi‑primitive flow, replay stability,
and envelope evolution across cycles.

---

# 1. Intake and Context Initialization

## 1.1 InB → IIInB → IE
**Goal:** Produce the first committed TP‑stream envelope.

**Steps:**
1. Run InB to normalize external input and establish neutral TP‑stream defaults.
2. Run IIInB to generate deterministic repair proposals (no commits).
3. Run IE to apply all proposals and commit semantics/meaning and processes.

**Checks:**
- IE output must be replay‑stable.
- Supervisor must remain empty.

---

## 1.2 IE → CEx → CE
**Goal:** Produce a bounded, replay‑safe context shell.

**Steps:**
1. Run CEx to evaluate relevance using MSL tokens, qualifiers, continuity signals.
2. Run CE to either:
   - copy forward `MCB.next_context`, or  
   - initialize a reset shell.

**Checks:**
- CE must reflect CEx’s relevance decision.
- CE must be safe for routing and identity.

---

# 2. Scoring and Correction

## 2.1 CE → ISc → TPU
**Goal:** Produce the next committed TP state.

**Steps:**
1. Run ISc to score candidate_set{} using truth_hypotheses‑prc.
2. Run TPU to apply deterministic meaning‑layer corrections.

**Checks:**
- TPU must preserve upstream commitments to semantics/meaning, processes, supervisor.
- TP(N+1) must be deterministic and replay‑safe.

---

# 3. Structural, Constraint, and Semantic Residue

## 3.1 TPU → SOB → SROB → CnOB
**Goal:** Produce stable structural and constraint residue.

**Steps:**
1. Run SOB to extract first‑pass structural cues.
2. Run SROB to refine and canonicalize structural residue.
3. Run CnOB to extract constraint‑level residue and metadata.

**Checks:**
- Residue must be canonical and refinement‑consistent.
- Constraint markers must be stable across replays.

---

## 3.2 CnOB → SmOB → SSG → STPX
**Goal:** Produce semantic‑adjacent and semantic‑layer residue.

**Steps:**
1. Run SmOB to extract semantic‑adjacent cues and compress residue into deterministic hashes.
2. Run SSG to generate semantic‑adjacent activation vectors.
3. Run STPX to extract semantic‑layer cues and produce semantic‑layer residue hashes.

**Checks:**
- Pre‑semantic and semantic‑layer hashes must be deterministic.
- Routing‑adjacent signals must be stable.

---

# 4. Routing and Identity Cycles

## 4.1 STPX → TR → RB → IdOB
**Goal:** Perform identity‑conditioned meaning construction.

**Steps:**
1. Run TR to compute routing vector TP.TR.
2. Run RB to select identity basin using structural, semantic, and routing cues.
3. Run IdOB to perform identity‑conditioned semantic interpretation.

**Checks:**
- IdOB may require multiple cycles.
- Meaning must converge or signal correction/continuation.

---

## 4.2 IdOB → MCB → CTP → RB (Cycle)
**Goal:** Stabilize meaning across cycles.

**Steps:**
1. Run MCB to produce `MCB.next_context`.
2. Run CTP‑prm to consolidate IdOB outputs into a deterministic packet.
3. Run RB to determine:
   - continue cycle  
   - needs correction (return to CE → TPU)  
   - done (proceed to OuBA)

**Checks:**
- Multi‑cycle replay must be stable.
- RB decisions must be deterministic.

---

# 5. Completion and Freeze

## 5.1 OuBA → SSRGn
**Goal:** Produce immutable meaning snapshot for Path‑B.

**Steps:**
1. Run OuBA to commit finalized meaning and write commit‑time metadata.
2. Run SSRGn to project, sanitize, and freeze semantic_core into SSR.

**Checks:**
- SSR must be deterministic and replay‑safe.
- No TP‑stream fields may be modified after commit.

---

# 6. Subsystem Simulation Strategy

## 6.1 Recommended Simulation Order
1. Intake + Context Initialization  
2. Scoring + Correction  
3. Structural Residue  
4. Constraint Residue  
5. Semantic‑Adjacent + Semantic‑Layer Residue  
6. Routing + Identity Cycles  
7. Completion + Freeze  

## 6.2 Replay Validation
- Each stage must be replay‑stable.  
- Hashes (SmOB, STPX) must be identical across runs.  
- RB decisions must be deterministic.

## 6.3 Isolation Rules
- No primitive modifies TP‑stream fields except TPU and OuBA.  
- All other primitives are read‑only.  
- Context machinery (CEx, CE, MCB) must remain bounded.

---

# Notes
- All primitive names and behaviors come directly from **20.190**.  
- No expansions or terminology are invented.  
- This plan describes subsystem‑level flow, not primitive‑local simulation.  
- Primitive‑local simulation remains under `../path_a/`.


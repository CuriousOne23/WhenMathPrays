# Incremental Flow — Path A Subsystem Simulation
This document describes the subsystem‑level execution flow for Path A using
the canonical primitive definitions from **20.190**.  
Primitive‑local behavior remains inside each primitive’s folder under `../path_a/`.

This file explains how envelopes move through Path A, how each primitive
hands off to the next, and how multi‑cycle replay stabilizes meaning.

---

# 1. InB → IIInB → IE
**InB (Input Basin)**  
- Normalizes external input.  
- Produces neutral TP‑stream defaults.  
- No meaning construction or inference.

**IIInB (Input Inference/Repair Basin)**  
- Detects user‑sanctioned shorthand expansions.  
- Produces repair proposals but commits nothing.

**IE (Intake Envelope)**  
- Applies all IIInB repair proposals deterministically.  
- Commits **semantics/meaning** and **processes**.  
- Supervisor remains empty.  
- Produces the first committed TP‑stream envelope.

**Subsystem effect:**  
A stable, replayable intake representation is created for downstream primitives.

---

# 2. IE → CEx → CE
**CEx (Context Extractor)**  
- Evaluates relevance using MSL tokens, qualifiers, continuity signals.  
- Produces deterministic context decisions.

**CE (Context Envelope)**  
- Copies forward prior `MCB.next_context` when relevant.  
- Otherwise initializes a reset shell.  
- Provides safe, isolated context for routing and identity.

**Subsystem effect:**  
A bounded, replay‑safe context shell is prepared for Path A.

---

# 3. CE → ISc → TPU
**ISc (Inference Scorer)**  
- Reads CE and candidate_set{}.  
- Applies truth_hypotheses‑prc.  
- Produces scoring fields for TPU.  
- Does not modify TP‑stream fields.

**TPU (Thought Packet Updater)**  
- Sole writer for Path‑A correction.  
- Applies meaning‑layer corrections based on ISc scoring.  
- Preserves upstream commitments to semantics/meaning, processes, supervisor.

**Subsystem effect:**  
TPU produces the next committed TP state (TP(N+1)) under deterministic rules.

---

# 4. TPU → SOB → SROB → CnOB → SmOB → SSG → STPX
**SOB (Structural OB)**  
- Extracts first‑pass structural cues (boundaries, anchors, masks).  
- Produces base structural residue.

**SROB (Structural Refinement OB)**  
- Canonicalizes and normalizes SOB residue.  
- Produces refinement‑consistent structural fragments.

**CnOB (Constraint OB)**  
- Extracts constraint‑level residue (missing‑slot signals, conflict markers).  
- Produces constraint metadata for routing.

**SmOB (Semantic OB)**  
- Job 1: Extract semantic‑adjacent cues.  
- Job 2: Compress upstream residue into deterministic pre‑semantic hash + TR‑input vector.

**SSG (Semantic Signal Generator)**  
- Produces semantic‑adjacent activation vectors and routing‑adjacent signals.

**STPX (Semantic TP Extractor)**  
- Extracts semantic‑layer cues and referent‑adjacent signals.  
- Produces semantic‑layer residue hashes.

**Subsystem effect:**  
A complete structural + constraint + semantic residue set is prepared for routing.

---

# 5. STPX → RB → TR → RB → IdOB
**TR (Thought Router)**  
- Computes deterministic routing vector TP.TR.  
- Consumes OB and DCB signals.  
- Does not select basins.

**RB (Routing Basin)**  
- Uses structural residue, semantic‑adjacent cues, semantic‑layer cues, SSG signals.  
- Selects the appropriate identity basin.

**IdOB (Identity Object Builder)**  
- Performs identity‑conditioned semantic interpretation.  
- Refines referents, qualifiers, subculture.  
- May run multiple cycles.

**Subsystem effect:**  
Identity‑conditioned meaning construction occurs, possibly across multiple cycles.

---

# 6. IdOB → MCB → CTP → RB → (repeat cycles)
**MCB (Message Context Builder)**  
- Writes short‑term context for next turn.  
- Produces `MCB.next_context` containing qualifiers, stance, direction, coherence.

**CTP‑prm (Collect/Consolidate Thought Point)**  
- Consolidates all IdOB outputs into a single deterministic packet.  
- Provides replay‑safe input for RB arbitration.

**RB (Routing Basin)**  
- Reads consolidated packet.  
- Decides whether meaning is stable, needs correction, or requires another IdOB cycle.

**Subsystem effect:**  
Multi‑cycle replay stabilizes meaning until RB signals completion.

---

# 7. Completion → OuBA → SSRGn
**OuBA (Output Basin)**  
- Commits finalized Path‑A meaning into immutable semantic snapshot.  
- Writes commit‑time metadata and DF‑readiness indicators.

**SSRGn (Semantic Snapshot Reference Generator)**  
- Converts committed TP snapshot into SSR.  
- Performs projection, sanitization, metadata binding.  
- Produces Path‑B‑ready frozen meaning.

**Subsystem effect:**  
Path A terminates with a deterministic, immutable meaning snapshot.

---

# Notes
- All primitive names and descriptions come directly from **20.190**.  
- No expansions or terminology are invented.  
- This file describes subsystem‑level flow, not primitive‑local behavior.  
- Primitive‑local simulation remains under `../path_a/`.


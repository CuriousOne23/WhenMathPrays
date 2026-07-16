**Yes, that makes perfect sense.**

This is exactly the right way to handle it: a **living working paper** that surfaces the hard questions and gaps first, then proposes solutions iteratively. It can grow as we explore, then shrink as we converge on decisions.

Here is the updated **v0.4** of `path_a_context_subst.md`, restructured as a working paper with explicit **Open Questions** and **Proposed Directions** sections (especially focused on COB, CST, and CIL as you requested).

---

**path_a_context_subst.md**  
**Path A Context Substrate** (Working Paper v0.4)

### 1. Purpose
This living working paper defines the stable, deterministic substrate that Path A must produce so the conversation-layer primitives (COB, CST, CIL) and supporting blocks (CEx, SSRGn) can be properly specified and implemented.  

It will grow with open questions and proposals, then shrink as we agree on solutions.

### 2. Scope & Current Architecture Context
- Path A = full meaning-construction pipeline ending at OuBA → SSRGn.
- The **Context Substrate** = Intake Envelope (IE), TP metadata (20.105), and post-OuBA SSRGn artifacts.
- Goal: Ensure long-horizon continuity, stability, and deterministic context extraction without breaking replay safety or the A/B boundary.

### 3. Intake Guarantees (Early Path A)
(Stable for now — see prior drafts for IE/TP metadata details.)

### 4. Conversation-Layer Primitives — Current State & Gaps

**COB (Conversation Object Basin)**
- Current: Maintains ≤20 identity-layers, referent maps, lineage.
- Gaps: Internal data model, update/merge rules, conflict resolution with new SSRGn, layer lifecycle (creation/retirement/aging).

**CST (Conversation Stability Tracker)**
- Current: Detects drift/oscillation/collapse and issues correction signals.
- Gaps: Metrics, windows, thresholds, signal schema, feedback loop with COB.

**CIL (Conversation Integration Layer)**
- Current: Merges short-term cues with COB snapshot; produces intake packet for CEx.
- Gaps: Precise merging logic, flag-generation rules, handling of ambiguity.

**Supporting: CEx & SSRGn**
- Better specified, but need tighter contracts with the above.

### 5. Open Questions (Where We Are Getting in Trouble)

#### COB Questions
- What is the exact schema for an identity-layer and its referent map?
- How are new layers created or old ones retired when we hit the 20-layer limit?
- How does COB resolve conflicts between incoming SSRGn meaning and existing layers?
- What is the update/merge algorithm when CST signals arrive?
- How do we ensure replay safety for the entire COB state over long sessions?

#### CST Questions
- What quantitative metrics define drift, oscillation, or collapse?
- Over what time windows and with what thresholds do we trigger signals?
- What is the full set of correction signals and their parameters?
- How does CST avoid over-correction or oscillation itself?
- Is CST fully deterministic and replay-safe?

#### CIL Questions
- Exactly how does CIL merge short-term TP/IE cues with COB snapshot?
- What rules govern certainty flags, field-importance hints, and ambiguity flags?
- How does CIL handle partial or conflicting information from COB?

#### Cross-Cutting Questions
- What is the precise timing and handoff protocol (SSRGn → COB/CST/CIL)?
- How are all signals and state changes auditable and replay-safe?
- How do these blocks interact with Path B (CoHI, etc.) without breaking the A/B boundary?
- What invariants must hold to prevent conversational collapse or identity wobble?

### 6. Proposed Directions (Starting Points)

**For COB**
- Adopt a fixed 20-slot array with priority/strength scores per layer.
- Define explicit merge rules (e.g., strength-weighted averaging of referent maps).
- Add aging/decay based on recency and usage frequency.

**For CST**
- Use multi-scale metrics: short-term oscillation (last 3–5 turns), medium-term drift (last 20 turns), long-term entropy of layer usage.
- Define a small set of typed signals with strength parameters.
- Require CST to log justification for each signal.

**For CIL**
- Simple weighted merge of short-term cues and COB snapshot.
- Rule-based flag generation (e.g., low confidence if conflicting referents).

**General**
- All state changes go through explicit, versioned snapshots for replay.
- Add a small set of quantitative test cases (e.g., oscillation scenario, new identity emergence, referent conflict) that the subsystem must pass.

### 7. Next Steps
1. Agree on or refine the questions above.
2. Pick one block (e.g., COB) and expand its section with detailed proposals.
3. Iterate until each primitive has enough to become a full requirements doc.
4. Shrink this paper as decisions are extracted into their own specs.

---

This format gives us room to grow the questions and proposals without losing focus.  

Does this structure feel right? Which block or set of questions should we tackle first?

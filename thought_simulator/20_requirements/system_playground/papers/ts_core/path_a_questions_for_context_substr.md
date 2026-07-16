**Understood.**

Renamed to **`path_a_questions_for_context_substr.md`** (as requested).

Here is **v0.7** — expanded with additional good questions surfaced from our discussion and cross-referencing the existing 20-series docs. I kept the structure clean and added a small “Emerging Questions” section at the end so we can keep growing it naturally.

---

**path_a_questions_for_context_substr.md**  
**Path A Questions for Context Substrate** (Working Paper v0.7)

### 0. Purpose
This living working paper collects and organizes all critical questions we must answer before COB, CIL, CST, CEx, and SSRGn can be properly specified and implemented.  

We will grow the questions until they saturate and stabilize. Only then will we begin closing them as a team and extracting answers into dedicated requirement documents.

### 1. Why These Questions Matter
The conversation-layer primitives depend on a stable Path A substrate. Underspecification here risks identity wobble, unreliable drift detection, inconsistent merging, non-deterministic extraction, and broken replay safety.

### 2. Open Questions About Path A Output

**Envelope Schema & Stability**
- What is the exact schema of the Intake Envelope (IE)?
- Which fields are required vs. optional?
- How are structural tokens and referent candidates formally represented (schema, ordering, ambiguity)?
- What metadata must be guaranteed stable across turns?

**Deterministic Replay**
- What parts of the envelope and TP metadata must be bit-for-bit deterministic?
- How are envelope IDs and lineage markers generated and stabilized?
- How do repairs, defects, and referent candidates maintain canonical ordering under replay?

**Referent Candidates & Structural Tokens**
- What exactly qualifies as a referent candidate (surface-form only, multi-word, typed, ambiguous)?
- How are structural tokens represented for malformed, nested, or complex input?

### 3. Open Questions About COB

**Identity Layer Model**
- Exact schema of an identity layer and its referent map?
- Fixed 20 slots or dynamic with a hard cap?
- How is lineage represented (tree, DAG, linked list, versioned history)?
- How is referent strength, confidence, or importance represented?

**Update & Lifecycle Mechanics**
- How does COB ingest and merge new SSRGn meaning?
- Rules for conflict resolution between new meaning and existing layers?
- Layer creation, splitting, merging, weakening, retirement, and aging/decay policy?
- What happens when all 20 layers are occupied or when a new distinct identity appears?

**Determinism & Safety**
- How is the full COB state replayed deterministically from the SSRGn sequence?
- How are layer IDs and snapshots versioned for auditability?

### 4. Open Questions About CST

**Detection**
- Exact quantitative metrics for drift, oscillation, and collapse (e.g., layer churn, referent volatility, usage entropy)?
- Time windows (short, medium, long-term) and triggering thresholds?

**Signals & Protocol**
- Complete set of correction signals and their parameters (strength, justification, target)?
- Prioritization and batching when multiple signals fire?
- Synchronous or asynchronous with COB? Frozen snapshot or live view?
- How does COB acknowledge, apply, or reject signals?

**Safety & Determinism**
- Safeguards to prevent over-correction or inducing new oscillation?
- Full replay safety for CST decisions and signals?

### 5. Open Questions About CIL

**Merge Logic**
- Precise rules for merging short-term TP/IE cues with COB snapshot?
- Handling of conflicting, partial, or low-certainty information?

**Flag Generation**
- Rules and algorithms for certainty flags, field-importance hints, and ambiguity flags?
- How are flags computed and represented in the intake packet?

**Determinism**
- How does CIL guarantee stable output under replay?

### 6. Open Questions About CEx & SSRGn

**CEx**
- Exact extraction allowlist, rules, and interpretation of structural tokens / CIL flags?
- Replay stability guarantees?

**SSRGn**
- Exact handoff protocol from OuBA → SSRGn → conversation layer (COB/CST/CIL)?
- Which fields are frozen vs. transformed or filtered?

### 7. Cross-Cutting / Highest-Risk Questions

**Timing & Ordering**
- Exact sequence and state visibility: SSRGn → COB → CST → CIL → CEx?
- Does CIL read pre- or post-CST COB state?

**Replay, Auditability & Invariants**
- How are all state changes, signals, and snapshots logged for deterministic replay?
- Global invariants that must hold to prevent identity wobble or conversational collapse?

**A/B Boundary & Path B Integration**
- How do these primitives interact with Path B (e.g., CoHI) without breaking the A/B boundary?
- What data flows from conversation layer back into Path B?

**Error Handling & Collapse Prevention**
- What conditions cause conversational collapse or identity instability?
- Emergency safeguards or recovery mechanisms?

### 8. Emerging / Secondary Questions
(Added as we discover them — currently empty or low-priority; we will grow this section.)

### 9. Next Steps
1. Continue expanding questions as new gaps surface.
2. When a cluster stabilizes, extract it into a dedicated requirements paper.
3. Shrink this working paper over time.

---

This keeps the paper focused on capturing good questions while staying manageable.  

Shall we add more questions now, or pick a section (e.g., COB or CST) to start proposing answers?

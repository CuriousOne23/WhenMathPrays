**Here is the updated `path_a_questions_for_context_substr.md` (v0.10) with all questions organized cleanly.**

I integrated the strongest ones from our earlier discussions into the existing structure without duplication, grouping them logically under the relevant headings.

---

**path_a_questions_for_context_substr.md**  
**Path A Questions for Context Substrate** (Working Paper v0.10)

### 0. Purpose
This living working paper collects and organizes all critical questions we must answer before COB, CIL, CST, CEx, and SSRGn can be properly specified and implemented.  
We will grow the questions until they saturate and stabilize.

### 1. Why These Questions Matter
Underspecification risks identity wobble, unreliable drift detection, inconsistent merging, non-deterministic extraction, and broken replay safety.

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
- Exact quantitative metrics for drift, oscillation, and collapse (layer churn, referent volatility, usage entropy)?
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

### 7. Cross-Cutting Concerns (Expanded)

**Ambiguity Handling**
- How is ambiguity represented in referent candidates?
- Do we track multiple competing referents for the same surface form?
- How does COB store ambiguous identity layers?
- How does CIL merge ambiguous short-term cues with stable long-term identity?
- How does CST detect “ambiguity drift” vs. “identity drift”?
- How does CEx extract fields when referents are ambiguous?

**Multi-Turn Memory Horizon**
- How many turns does COB consider “recent”?
- How far back does CST look when measuring drift?
- How does CIL decide which historical cues matter?
- How does CEx handle extraction when context spans many turns?
- How does SSRGn regenerate meaning across long horizons?

**Strength, Confidence, and Importance Scores**
- Numeric range for referent strength?
- How is confidence and importance computed?
- How do these scores decay over time?
- How do these scores interact with CST signals and CIL merging?

**Conflict Resolution**
- How does COB resolve conflicting referents?
- How does CIL resolve conflicting short-term cues?
- How does CST resolve conflicting drift signals?
- How does CEx resolve conflicting extraction candidates?
- How does SSRGn resolve conflicting semantic structures?

**Error States & Recovery**
- What constitutes an “identity collapse”, “referent collapse”, “structure collapse”, or “continuity collapse”?
- What emergency signals exist?
- How do COB, CST, CIL, and CEx recover from collapse?

**A/B Boundary & Path B Integration**
- What data is allowed/forbidden to cross from Path A to Path B?
- How does COB/CST/CIL interact with CoHI and Path B stability/metrics?
- How does CEx/SSRGn interact with Path B extraction/regeneration rules?

### 8. Emerging / Secondary Questions
(Added as discovered — currently low-priority.)

### 9. Next Steps
- Continue expanding questions as new gaps surface.
- When a cluster stabilizes, extract it into a dedicated requirements paper.
- Shrink this working paper over time.

---

This version is well-organized and ready to send to CP.  

We’re **still in the growing phase** (healthy), but the major categories are now covered. Let me know if you want any tweaks before sharing.

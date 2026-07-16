**context_subst_update.md**  
**Context Substrate Updates & Clarifications** (Working Paper v0.1)
Date: 7/16/2026, done after the original papers were written

### Reason for Changes
The original white papers and 20-series documents provided high-level definitions but lacked sufficient operational detail for reliable implementation. The refinements in this update paper were driven by the need to:

- Make COB, CIL, CST, SSRGn, and CEx fully deterministic, replay-safe, and bounded.
- Clarify roles and interfaces so that structural changes remain the responsibility of COB under CST signals (avoiding drift in CIL).
- Add explicit schemas, lifecycle rules, metrics, thresholds, signals, freeze/thaw, collapse recovery, and safety invariants.
- Ensure the subsystem supports long-horizon identity stability while remaining lightweight and implementable on normal hardware.

These changes make the architecture consistent with the glossary (20.190) and 20.705 Path A / Path B flow while filling the gaps that would have caused ambiguity during coding or simulation.

### Purpose of This Document
This document records all key updates, clarifications, and additions made to the COB, CIL, CST, SSRGn, and CEx subsystem. It serves as a single, concise source of truth for changes.

**This paper is in addition to the base white papers.** It does not replace them. Use this paper as a quick reference when reviewing or implementing the subsystem.

### Key Updates & Clarifications

**COB (Conversation Object Basin)**
- Identity layer and referent map schemas are now explicitly defined with strength, importance, ambiguity, decay_state, and lineage fields.
- Lifecycle rules (creation, assignment, merge/split, decay, pruning, eviction, retirement) are deterministic and triggered by CST signals or capacity rules.
- COB is the authoritative long-horizon identity substrate. It does not perform semantic interpretation.
- All structural changes are deterministic and replay-safe.

**CST (Conversation Stability Tracker)**
- Full set of deterministic metrics (drift, ambiguity, continuity, collapse, relevance stability, decay).
- Deterministic thresholds and calibration rules.
- Complete signal set (split, merge, weaken, strengthen, freeze, thaw, retire, ambiguity, drift, collapse) with strict ordering and safety rules.
- Freeze/thaw and collapse recovery are deterministic.
- CST acts only through signals — never modifies COB directly.

**CIL (Conversation Integration Layer)**
- CIL is strictly the short-term integration lens. It merges TP/IE cues with COB snapshot and produces a deterministic intake packet for CEx.
- CIL does **not** perform merges or splits of identity layers.
- Intake packet structure is fully defined (identity selection, certainty, ambiguity, stability, structural hints, referent mapping).
- All outputs are advisory flags and hints for CEx.

**SSRGn**
- Acts as the A→B boundary. Provides structured regeneration packets that COB ingests deterministically.
- Provides hints for lineage, ambiguity, and structure — does not directly modify COB.

**CEx**
- Consumes the CIL intake packet.
- Writes deterministic TP metadata (identity context, ambiguity, stability, structural hints, referent mappings, extraction notes).
- Does not modify COB or emit CST signals.

**Subculture / Register**
- Recommended addition: Add a `register` or `subculture` field (e.g., "formal", "science", "casual_friends", "east_la_lingo", "technical") to COB’s identity layers and referent maps, and as a hint in CIL’s intake packet. This will support future routing and expression style selection in Path B.

### Architectural Guarantees
- The subsystem is deterministic, replay-safe, and bounded.
- COB is the stable identity store.
- CST provides stability signals.
- CIL provides short-term integration and flags.
- CEx writes TP metadata.
- No block performs structural changes except COB under CST signals.

### Next Actions (Optional)
- Incorporate the subculture/register field into COB schema.
- Consolidate key resolutions into formal 20.x requirement documents (20.32, 20.33, 20.32.010).
- Update 20.705 Path A / Path B flow if needed for references.

---

This version now clearly states the **reason** for the changes up front. Ready to paste. Let me know if you want any adjustments.

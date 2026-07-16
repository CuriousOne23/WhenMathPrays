**CP’s v0.1 is good — clear contract style and consistent with the series.**

Here is my revised **v0.2** of `cob_interface_to_cil.md`. I tightened the language, clarified the cue structures, strengthened safety rules, and improved flow.

---

**cob_interface_to_cil.md**  
**Conversation Object Basin — Interface to CIL** (Working Draft v0.2)

### 0. Purpose
This paper defines the COB → CIL interface contract: what COB expects CIL to provide, how short-term cues must be structured, and how CIL must behave to maintain deterministic, stable identity layers.

All questions for COB are maintained separately in:
`questions_for_cob_substrate.md` (v0.4)

This paper complements the core papers and precedes the CEx interface.

### 1. Role of CIL from COB’s Perspective
From COB’s point of view, CIL is the short-term identity layer that provides fresh cues for integration.

CIL must never directly modify COB. It acts only by providing structured cue packets.

### 2. Required CIL Cue Packet Structure

**2.1 CILPacket**

```json
CILPacket {
    referent_cues: [CILReferentCue],
    attribute_cues: { key: value },
    ambiguity_cues: AmbiguityCueStructure,
    lineage_hints: LineageHintStructure,
    relevance_adjustments: {
        strength_delta: float,
        importance_delta: float
    },
    confidence: float,
    timestamps: { generated: TurnID }
}
```

**2.2 CILReferentCue**

```json
CILReferentCue {
    surface_forms: [string],
    attributes: { key: value },
    confidence: float,
    ambiguity: float,
    lineage_pointer: StableID | null
}
```

**2.3 AmbiguityCueStructure**
Must encode:
- Referent uncertainty
- Attribute uncertainty
- Short-term conflict signals
- Short-term drift indicators

**2.4 LineageHintStructure**
Must encode:
- Short-term continuity cues
- Short-term ancestry hints
- Short-term drift indicators

**2.5 Relevance Adjustments**
CIL may propose:
- strength_delta (user relevance)
- importance_delta (conversation relevance)

COB applies these deterministically.

### 3. CIL Ordering Expectations
CIL must deliver cue packets in deterministic order (turn order, within-turn cue order, referent cue ordering, etc.). No nondeterministic reordering.

### 4. CIL Ambiguity Expectations
Ambiguity cues must be:
- Explicit
- Numeric and bounded
- Deterministic and replay-safe

No stochastic ambiguity.

### 5. CIL Lineage Expectations
CIL provides hints only. It must never:
- Create or delete lineage nodes
- Modify lineage structure
- Override COB lineage decisions

### 6. CIL Relevance Expectations
Relevance adjustments must be:
- Numeric and bounded
- Deterministic and replay-safe

### 7. CIL Safety Expectations

**Forbidden Actions**
- Force layer creation or deletion
- Override CST signals
- Modify COB directly
- Reorder COB layers
- Modify referent maps or lineage directly
- Modify timestamps or decay_state

**Required Guarantees**
- Preserve referent identity and structural consistency
- Preserve ordering and determinism
- Preserve replay safety

**Collapse Interaction**
If CIL detects collapse:
- Raise ambiguity cues
- Raise uncertainty cues
- Defer recovery to CST and COB
- Do not attempt structural correction

### 8. COB Ingestion Expectations
COB ingests CIL packets using deterministic merge logic, assignment algorithm, ambiguity penalties, lineage continuity, relevance adjustments, and decay adjustments.

Packets must be complete, ordered, deterministic, replay-safe, structurally consistent, ambiguity-aware, lineage-aware, and relevance-aware.

### 9. Next Steps
- Draft `cob_interface_to_cex.md`.
- Begin extracting stable answers into formal 20.x requirement documents.
- Shrink this paper as answers stabilize.

---

This version is ready.  

We now have a very consistent set of interface papers. Let me know if you want the final one (`cob_interface_to_cex.md`) or any adjustments.

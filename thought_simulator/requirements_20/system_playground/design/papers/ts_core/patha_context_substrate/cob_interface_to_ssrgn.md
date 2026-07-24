**cob_interface_to_ssrgn.md**  
**Conversation Object Basin — Interface to SSRGn** (Working Draft v0.2)

### 0. Purpose
This paper defines the COB → SSRGn interface contract: what COB expects SSRGn to provide, how regenerated meaning must be structured, and how SSRGn must behave to maintain deterministic, stable identity layers.

All questions for COB are maintained separately in:
`questions_for_cob_substrate.md` (v0.4)

This paper complements the core papers and precedes the CEx interface.

### 1. Role of SSRGn from COB’s Perspective
From COB’s point of view, SSRGn is the regeneration engine that produces structured meaning packets for ingestion.

SSRGn must never directly modify COB. It acts only by providing well-formed packets that COB ingests deterministically.

### 2. Required SSRGn Packet Structure

**2.1 SSRGnPacket**

```json
SSRGnPacket {
    referents: [RegeneratedReferent],
    attributes: { key: value },
    ambiguity: AmbiguityStructure,
    lineage_hints: LineageHintStructure,
    structure: StructuralRepresentation,
    confidence: float,
    timestamps: { generated: TurnID }
}
```

**2.2 RegeneratedReferent**

```json
RegeneratedReferent {
    surface_forms: [string],
    attributes: { key: value },
    confidence: float,
    ambiguity: float,
    lineage_pointer: StableID | null
}
```

**2.3 AmbiguityStructure**
Must explicitly encode:
- Referent collisions
- Attribute uncertainty
- Structural uncertainty
- Lineage uncertainty
- Identity uncertainty

**2.4 LineageHintStructure**
Must encode:
- Continuity cues
- Referent ancestry hints
- Identity drift indicators
- Merge/split indicators

**2.5 StructuralRepresentation**
Must encode regenerated semantic, relational, and contextual structure.

### 3. SSRGn Ordering Expectations
SSRGn must deliver packets in deterministic order (turn order, within-turn regeneration order, referent ordering, etc.). No nondeterministic reordering.

### 4. SSRGn Ambiguity Expectations
Ambiguity must be:
- Explicit
- Numeric and bounded
- Deterministic and replay-safe

No stochastic ambiguity.

### 5. SSRGn Lineage Expectations
SSRGn provides hints only. It must never:
- Create or delete lineage nodes
- Modify lineage structure
- Override COB lineage decisions

### 6. SSRGn Confidence Expectations
Confidence scores must be:
- Numeric and bounded
- Deterministic and monotonic
- Replay-safe

COB uses them to weight merges and resolve conflicts.

### 7. SSRGn Safety Expectations

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
If SSRGn detects collapse:
- Raise ambiguity and uncertainty
- Defer recovery to CST and COB
- Do not attempt direct recovery

### 8. COB Ingestion Expectations
COB ingests SSRGn packets using deterministic merge logic, assignment algorithm, ambiguity penalties, lineage continuity, and decay adjustments.

Packets must be complete, ordered, deterministic, replay-safe, structurally consistent, ambiguity-aware, and lineage-aware.

### 9. Next Steps
- Draft `cob_interface_to_cex.md`.
- Begin extracting stable answers into formal 20.x requirement documents.
- Shrink this paper as answers stabilize.

---

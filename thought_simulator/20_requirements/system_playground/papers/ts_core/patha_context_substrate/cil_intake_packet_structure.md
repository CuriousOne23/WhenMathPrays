**cil_intake_packet_structure.md**  
**Conversation Integration Layer — Intake Packet Structure** (Working Draft v0.2)

### 0. Purpose
This paper defines the **intake packet** produced by CIL (Conversation Integration Layer) for CEx.

CIL’s role is to merge short-term TP/IE structural cues with long-term COB/CST context into a deterministic, replay-safe intake view. CIL does **not** perform structural merges or splits of identity layers — those are handled by COB under CST signals.

The intake packet tells CEx which identity layers are relevant, how certain those mappings are, how stable/ambiguous the context is, and which structural hints matter for extraction.

This paper complements the COB papers and 20.705 Path A / Path B flow.

### 1. CIL’s Role in Path A
From Path A’s perspective, CIL:
- Reads **short-term TP/IE cues** (current + immediate prior message: surface forms, attributes, local structure).
- Reads the **stabilized COB/CST snapshot** (identity layers, lineage, ambiguity, relevance, stability signals).
- Integrates these into a **single intake view**.
- Emits **selection and certainty flags** plus **structural hints** for CEx.

CIL is an integration lens, not a store, not a stability engine, not a TP writer.

### 2. Intake Packet Structure

```json
CILIntakePacket {
  identity_selection: IdentitySelectionBlock,
  certainty: CertaintyBlock,
  ambiguity: AmbiguityBlock,
  stability: StabilityBlock,
  structural_hints: StructuralHintBlock,
  referent_mapping: ReferentMappingBlock,
  timestamps: { generated_turn: TurnID }
}
```

All fields must be deterministic and replay-safe.

### 3. Identity Selection Block

```json
IdentitySelectionBlock {
  primary_layer_id: StableID | null,
  secondary_layer_ids: [StableID],
  layer_ranking: [{ layer_id: StableID, score: float }]
}
```

Selection is based on surface form match, attribute match, lineage hints, and COB/CST stability signals.

### 4. Certainty Block

```json
CertaintyBlock {
  primary_certainty: float,
  mapping_certainty: float,
  context_certainty: float
}
```

Numeric, bounded, deterministic values reflecting confidence in layer selection, mapping, and overall context.

### 5. Ambiguity Block

```json
AmbiguityBlock {
  ambiguous_mapping: bool,
  conflicting_cues: bool,
  ambiguity_score: float
}
```

No stochastic ambiguity; all values must be replay-safe.

### 6. Stability Block

```json
StabilityBlock {
  stable_context: bool,
  unstable_context: bool,
  collapse_risk: float
}
```

CIL reflects CST’s view of stability; it does not compute stability itself.

### 7. Structural Hint Block

```json
StructuralHintBlock {
  local_cluster_hint: bool,
  local_relation_hint: bool,
  hint_details: { cluster_ids: [StableID], relation_types: [string] }
}
```

Hints for CEx extraction, not structural instructions to COB.

### 8. Referent Mapping Block

```json
ReferentMappingBlock {
  mappings: [{ referent_id: string, layer_id: StableID | null, mapping_certainty: float }]
}
```

Each mapping ties a short-term referent to a COB identity layer.

### 9. Deterministic and Safety Requirements
CIL must:
- Be fully deterministic and replay-safe.
- Depend only on TP/IE cues + COB/CST snapshot.
- Respect CST stability signals.
- Treat the intake packet as read-only context for CEx.

CIL must not:
- Modify COB, CST, or TP directly.
- Emit merge/split or structural change instructions.
- Use external state, randomness, or timing.

### 10. Next Steps
- Refine numeric ranges and thresholds for certainty/ambiguity/stability fields.
- Align intake packet fields with 20.705 Path A / Path B flow.
- Integrate CIL behavior into the 20.x requirement series.

---

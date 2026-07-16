**cex_tp_metadata_rules.md**  
**CEx — TP Metadata Rules** (Working Draft v0.2)

### 0. Purpose
This paper defines the deterministic rules used by CEx (Context Extraction) to write metadata into the TP (Thought Packet).

CEx is the only component in Path-A/Path-B that writes TP metadata. Its behavior must be deterministic, replay-safe, and fully aligned with CIL intake packet, COB identity substrate, CST stability signals, and Path-A → Path-B flow.

This paper complements the CIL intake packet and stability papers.

### 1. Role of CEx in Path-A → Path-B
CEx receives:
- Current message
- Historical TP messages
- CIL intake packet (identity selection, certainty, ambiguity, stability, structural hints)

CEx’s job is to:
1. Interpret the intake packet.
2. Determine which identity layers apply.
3. Determine how context should be represented.
4. Write deterministic metadata into the TP.
5. Produce a stable TP entry for Path-B reasoning.

CEx does not:
- Modify COB
- Emit CST signals
- Perform structural operations
- Regenerate meaning (SSRGn does that)
- Integrate context (CIL does that)

CEx is strictly a TP metadata writer.

### 2. TP Metadata Overview
Each TP entry written by CEx contains:

```json
TPEntry {
  turn_id: TurnID,
  raw_message: string,
  identity_context: IdentityContextBlock,
  ambiguity_context: AmbiguityContextBlock,
  stability_context: StabilityContextBlock,
  structural_context: StructuralContextBlock,
  referent_context: ReferentContextBlock,
  extraction_notes: ExtractionNotesBlock
}
```

All fields must be deterministic and replay-safe.

### 3. Identity Context Block

```json
IdentityContextBlock {
  primary_layer_id: StableID | null,
  secondary_layer_ids: [StableID],
  layer_ranking: [{ layer_id: StableID, score: float }],
  identity_certainty: float
}
```

Rules:
- CEx must use exactly the identity selection from the CIL intake packet.
- No reinterpretation, no re-ranking, no mutation.
- identity_certainty must match CIL’s primary_certainty.
- If primary_layer_id is null, CEx must mark the TP entry as identity-unanchored.

### 4. Ambiguity Context Block

```json
AmbiguityContextBlock {
  ambiguous_mapping: bool,
  conflicting_cues: bool,
  ambiguity_score: float
}
```

Rules:
- Values must be copied directly from CIL intake packet.
- CEx must not compute ambiguity.
- If ambiguous_mapping is true, CEx must annotate the TP entry with ambiguity markers for Path-B reasoning.
- If conflicting_cues is true, CEx must annotate the TP entry with conflict markers.

### 5. Stability Context Block

```json
StabilityContextBlock {
  stable_context: bool,
  unstable_context: bool,
  collapse_risk: float
}
```

Rules:
- Values must reflect CST’s stability signals as passed through CIL.
- CEx must not compute stability.
- If unstable_context is true, CEx must annotate the TP entry with stability warnings.
- If collapse_risk exceeds a threshold, CEx must mark the TP entry as high-risk for Path-B.

### 6. Structural Context Block

```json
StructuralContextBlock {
  local_cluster_hint: bool,
  local_relation_hint: bool,
  hint_details: { cluster_ids: [StableID], relation_types: [string] }
}
```

Rules:
- Structural hints are advisory.
- CEx must not treat hints as structural instructions.
- CEx may annotate TP with cluster markers, relation markers, and contextual grouping hints.

These annotations help Path-B reasoning but do not affect COB.

### 7. Referent Context Block

```json
ReferentContextBlock {
  mappings: [{ referent_id: string, layer_id: StableID | null, mapping_certainty: float }]
}
```

Rules:
- CEx must copy referent mappings exactly from CIL.
- No reinterpretation or remapping.
- If layer_id is null, CEx must annotate the referent as unresolved.
- Mapping certainty must be preserved exactly.

### 8. Extraction Notes Block

```json
ExtractionNotesBlock {
  applied_rules: [string],
  context_flags: [string],
  stability_flags: [string],
  ambiguity_flags: [string]
}
```

Rules:
- CEx must log which rules were applied.
- Notes must be deterministic and replay-safe.
- Notes must not contain stochastic language, external state, or timestamps beyond turn_id.

### 9. Deterministic Replay Requirements
CEx must guarantee:
- Identical CIL intake → identical TP metadata
- Identical TP history → identical extraction behavior
- Identical stability signals → identical annotations
- Identical referent mappings → identical referent context

CEx must never:
- Reorder metadata fields
- Omit fields based on heuristics
- Add nondeterministic annotations
- Depend on external state or timing

### 10. Safety Requirements
CEx must never:
- Modify COB
- Emit CST signals
- Perform structural operations
- Reinterpret identity selection
- Reinterpret ambiguity or stability
- Use randomness or external state

CEx must always:
- Preserve determinism
- Preserve replay safety
- Preserve continuity
- Preserve stability semantics

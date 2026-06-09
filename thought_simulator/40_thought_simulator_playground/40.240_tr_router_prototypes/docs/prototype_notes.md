# prototype_notes

## Prototype Design Notes for 40.240 TR Router

### Scope
This is an intentionally minimal "basin selection router" proxy.
It validates the core idea of deterministic routing + consistent ΔH% tagging based on input characteristics.
It is **not** the full Thought Router (TR) from 20.37 that populates the complete TP.TR semantic block.

### Why this structure?
- Simple class + factory function for harness compatibility (following 40.05 macro style).
- Pure functions, no side effects.
- Keyword-based rules as a stand-in for future semantic cue extraction from OB input_fields.
- Fixed delta_h values per route class (monotonic, auditable).

### Limitations acknowledged
- No tr_needs_update handling (standalone for isolation).
- No MTP snapshot consumption.
- No full 12-field TP.TR output.
- No split/merge lineage additions.
- No atomic commit semantics.

These are explicitly called out as non-goals in the software_description.md and reserved for later iterations driven by 50.37 design.

### Determinism
All paths are deterministic by construction (no random, no time, no mutable global state).

### Future evolution
When moving toward full TR:
- Add support for reading TP snapshot + MTP snapshot (read-only).
- Implement the actual field derivation logic for stance, intent, affect, epistemic_shading, tension, politeness, commitment, reservation, logical_structure, semantic_deltaH, lineage_additions, routing_semantics.
- Expose tr_needs_update gate and clear-on-success behavior.
- Support deterministic_mode / nonce if needed for identity.

## References
- See software_description.md §3, §5, §8 for detailed scope and IO contract.
- See 20.37 for the target full specification.
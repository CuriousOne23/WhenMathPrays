# phi-G Data-Structure Specification (Round 2)

## Purpose
Define the allowable families, required fields, invariants, and high-level structure of G so that phi-G is a well-defined, simulatable function. This Round 2 revision incorporates lessons from Round 1 logic simulation (normalization tightening, required singularity flag, and extensibility support).

## Scope
- High-level data-structure families and constraints only.
- No implementation code, exact numeric transforms, or full feature lists (deferred to later rounds).
- Focus on SSG → phi-G → RB flow.
- Laptop-scale realizability assumed.

## G Data-Structure Families
G must be a fixed-dimensional relational field vector. Three permissible families (any of which may be used):
1. **Token-Structural Family** – Emphasizes syntactic and structural patterns.
2. **Semantic-Relational Family** – Emphasizes meaning-bearing relational motifs.
3. **Hybrid Family** – Combines elements of both.

All families must satisfy the constraints from Paper #1.

## Required Components / Slots in G
Every G vector must include (at minimum) normalized contributions from the OB pipeline:

- Coarse structural skeleton signals (from SOB)
- Shallow relational texture signals (from SROB)
- Constraint-level signals (from CnOB)
- Fine-scale microstructure signals (from SmOB)
- Normalization metadata and version/refinement depth (from SSG)
- **Required Singularity Proximity Flag** (0–1 normalized) – added per Round 1 lessons

## Generic Extendable Example
**Example G Vector Structure (Conceptual)**

Consider a fixed-dimensional vector G of length N (where N is constant across all time-steps).

Generic layout (slots are illustrative and extendable):

- Slots 1–K: Coarse structural features (SOB-derived) — e.g., boundary flags, arc-type encodings.
- Slots K+1–M: Shallow relational texture (SROB-derived) — e.g., speech-act class vectors, intent-shape embeddings.
- Slots M+1–P: Constraint signals (CnOB-derived) — e.g., dependency tension scores, boundary condition flags.
- Slots P+1–Q: Microstructure signals (SmOB-derived) — e.g., local resonance cues, micro-motif strengths.
- Slots Q+1–R: Normalization metadata, version/refinement depth, and required singularity proximity flag.
- Remaining slots: Reserved for future refinement.

**Why this structure is extendable**  
The design uses a fixed-dimensional vector with clearly partitioned, semantically meaningful blocks. New relational features or refined signals can be added by:
- Extending within an existing block (if the block has reserved capacity), or
- Appending new blocks while maintaining overall fixed dimensionality through padding or versioned encoding.

This ensures that future refinements (new language phenomena or deeper basin modeling) can be accommodated without breaking existing phi-G transformation rules or simulation determinism. The partitioning also makes it easy to trace which OB layer a feature came from.

## Invariants (Updated per Round 1)
- Fixed dimensionality across all time-steps and inputs.
- phi-G treats G as immutable input (no in-place mutation).
- All slots must be deterministically derivable from the OB → SSG pipeline.
- Stronger normalization invariants for high-resonance/singularity cases.
- Required singularity proximity flag with defined encoding.

## Traceability
- Builds on phi_G_relationship_foundation.md (conceptual constraints and pipeline).
- Feeds into phi_G_simulation_requirements.md (I/O and simulation rules).
- Will link to validation scenarios.

## Open Questions / Observations for Round 3
- Preferred starting family for production use.
- Exact dimensionality target and slot allocation strategy.
- Detailed scaling rules for normalization block.

---

This version is tightened based on Round 1 lessons (required singularity flag, stronger normalization, version field). Let me know if you want any further adjustments before we consider it final for Round 2 or move to updating Paper #2B.

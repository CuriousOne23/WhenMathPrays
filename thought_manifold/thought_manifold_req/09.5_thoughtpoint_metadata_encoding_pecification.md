# 09.5 ThoughtPoint Metadata & Encoding Specification

## 1. Purpose

This document defines the metadata structure, encoding formats, and event streaming rules for ThoughtPoints in the Thought Manifold Simulator. It ensures that every ThoughtPoint carries sufficient context for debugging, visualization, traceability, replay, and learning while maintaining determinism, compactness, and reversibility.

This specification bridges the conceptual requirements in `03_core_conceptual_requirements.md` and the implementation architecture in `07.5_implementation_architecture.md`.

## 2. Core Metadata Fields

Every ThoughtPoint must maintain a rich metadata record containing:

### 2.1 Identity & Provenance
- `tp_id`: Unique immutable identifier (UUID v7 recommended)
- `creation_timestamp`: Time of initial creation
- `provenance`: Origin (user input, splitting, merging, external injection)
- `lineage`: List of parent ThoughtPoint IDs (for splits/merges)

### 2.2 State History
- `basin_transition_log`: Ordered list of basin entries/exits (basin_id, timestamp, reason)
- `regulator_history`: List of regulator interventions (regulator_type, strength, timestamp, delta applied)
- `energy_entropy_snapshots`: Periodic samples of E and $H_\\%$ at key events
- `embedding_stats`: Statistical summary of embedding vector (mean, variance, coherence score)

### 2.3 Runtime Context
- `current_basin_id`: ID of the basin the ThoughtPoint currently belongs to
- `volitional_input_log`: Record of user steering actions
- `perturbation_history`: Summary of noise and external inputs received

## 3. Tagged Representation (Human-Readable)

- Must be JSON-based for easy inspection and debugging.
- All fields must be clearly named and include units where applicable.
- Should support pretty-printing and selective field inclusion for different debugging levels.

## 4. Encoded Representation (Compact & Deterministic)

- Must support a compact binary format (recommended: Protocol Buffers or custom binary schema).
- Must be fully deterministic and reversible.
- Must be versioned (schema version field).
- Must support lossless round-tripping between tagged and encoded forms.

## 5. Event Stream Specification

The ThoughtPoint shall produce a time-ordered event stream with the following characteristics:

- **Event Types**:
  - `TP_CREATED`
  - `BASIN_ENTERED` / `BASIN_EXITED`
  - `REGULATOR_ACTIVATED`
  - `SPLIT` / `MERGED`
  - `ENERGY_UPDATED`
  - `ENTROPY_UPDATED`
  - `VOLITIONAL_STEER`
  - `COMPLETION_REACHED`

- **Event Ordering**: Strictly chronological and deterministic.
- **Invariants**: Every state-changing event must be logged before the state is updated.
- **Replay Rules**: The full event stream must be sufficient to reconstruct any ThoughtPoint’s complete history.

## 6. Privacy & Encryption

- Sensitive fields (e.g., user volitional inputs, provenance from private sources) must be marked.
- Support selective disclosure and optional encryption of sensitive metadata.
- Core geometric and dynamic fields (position, energy, entropy, basin) shall remain unencrypted for simulation integrity.

## 7. Storage & Transport

- **In-Memory**: Rich object model with both tagged and encoded views.
- **Persistence**: Support JSON (debug) and binary (production) formats.
- **Transport**: Efficient serialization for inter-module and visualization communication.
- **Compression**: Optional compression for long-running ThoughtPoint histories.

## 8. Traceability & Observability

The metadata system must support:
- Full debugging traces (why a ThoughtPoint entered a basin, which regulators acted, etc.)
- Visualization of ThoughtPoint journeys through the manifold
- Learning from ThoughtPoint histories (pattern extraction, training data generation)
- Reproducibility of any simulation run given the initial state and event stream

## 9. Traceability to Other Documents

This specification directly supports:

- `03_core_conceptual_requirements.md` (ThoughtPoint definition and dynamics)
- `07.5_implementation_architecture.md` (observability and logging requirements)
- `07_TS_state_machine.md` (geometric context for metadata)

All metadata decisions are traceable via `24_traceability_matrix.md`.

---

**Last Updated**: May 23, 2026  
**Version**: 0.1 (Draft)

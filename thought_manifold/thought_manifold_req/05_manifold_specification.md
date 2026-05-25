# 05 Manifold Core

## 1. Purpose
The Manifold Core is the central geometric and organizational container for the entire thought space.

## 2. Functional Requirements

**MC-01: Container & Registry**
- Must act as a container and registry for all basins (Object Basins, Relational Basins, Inquiry Basins, etc.).
- Must support dynamic creation and registration of new basins at runtime.
- Must maintain a connectivity graph (saddles and highways) between basins.

**MC-02: Spatial Properties**
- Must support projection between high-dimensional embedding space and lower-dimensional visualization space (at minimum 2D and 3D).
- Must provide geometric queries (local curvature, gradient direction, nearest saddle, basin membership, etc.).

**MC-03: Basin Lifecycle**
- Must efficiently determine which basin a ThoughtPoint currently occupies.
- Must handle basin transitions (escape from one basin → entry into another).
- Must support metadata per basin (type, parameters, statistics).

**MC-04: Global Manifold State**
- Must maintain global simulation time / step count.
- Must track all active ThoughtPoints.
- Must provide aggregate statistics (total energy, average entropy, active basins, etc.).

## 3. Required Methods / Interface

- `add_basin(basin_config)`
- `get_basin_at(position)` or `get_basin_for(thought_point)`
- `find_transition_path(from_basin, to_basin)`
- `get_connected_basins(basin)`
- `serialize()` / `deserialize()`

## 4. Non-Functional Notes
- Must be highly observable (full state introspection).
- Must support fast lookup even with 100+ basins.
- All operations must be deterministic when seed is fixed.

## 5. Testability & Validation

- Invariant: No two basins overlap in their core regions.
- Must be able to save and restore a complex manifold with 20+ basins.
- Basin transitions must respect energy and filter rules defined elsewhere.

## 6. Traceability
Links to:
- 03_core_conceptual_requirements.md (Section 2.1, 2.2, 2.3)
- 04_system_architecture.md (Core Manifold Layer)

---

**Last Updated**: [Insert Date]  
**Version**: 0.1 (Draft)

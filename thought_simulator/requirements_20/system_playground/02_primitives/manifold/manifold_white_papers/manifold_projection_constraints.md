# Manifold Projection Constraints

## Purpose

This paper establishes the constraints and structural rules governing manifold projection. It defines what projection is allowed to do, what invariants it must preserve, and the boundaries of acceptable behavior. It relates to the manifold surface domain (Paper 2) and the transfer function (Paper 3).

## Projection Context (from Papers 2 and 3)

Input to projection is a valid `region_id` produced by the transfer function $P$ (Paper 3). Projection operates entirely within the manifold surface domain (Paper 2) and must respect domain bounds, admissibility, basin structure, mismatch-field constraints, and region partitions.

## Definition of Projection (Symbolic Only)

Projection is defined symbolically as:

$$
\text{Proj} : \text{region}\_{id} \rightarrow \text{region}\_{id}'
$$

where both `region_id` and `region_id'` lie within the bounded domain $\{0, \dots, M\}$. Projection is a rule-based, symbolic re-alignment within the manifold domain.

Projection must **not**:
- Use spatial geometry
- Use continuous math
- Use optimization
- Use inference
- Use semantics
- Use probabilistic selection
- Use normalization or clamping
- Use learned transformations

## Projection Constraints

### 4.1 Determinism
Same input region always yields the same output region.

### 4.2 Boundedness
Projection must always produce a `region_id'` within $\{0, \dots, M\}$.

### 4.3 Stability
Projection must preserve ordering and region partition boundaries.

### 4.4 Admissibility
Projection must respect:
- Basin alignment
- Mismatch-field rules
- Region partition constraints

### 4.5 Non-semantic behavior
Projection cannot assign meaning to region indices.

### 4.6 Non-geometric behavior
Projection cannot treat region indices as coordinates in a space.

### 4.7 No disallowed transformations
Projection must not use hashing, normalization, clamping, modulo arithmetic, probabilistic selection, or learned transformations.

## Structural Properties Projection Must Preserve

Projection must preserve:
- Region partition integrity
- Basin integrity
- Mismatch-field consistency
- Dictionary-coordinate compatibility
- Domain-boundary consistency
- Symbolic adjacency rules (if defined)
- Deterministic collapse rules

All invariants from Papers 1–3 must be maintained.

## Example Projection (Symbolic Only)

1. Start with a valid `region_id = 42`.
2. Admissibility check: Passes basin and mismatch constraints.
3. Mismatch-field rule application: No adjustment required.
4. Region partition alignment: Aligns with current partition rules.
5. Symbolic collapse: Yields `region_id' = 38`.

This example is purely symbolic and rule-based.

## Qualities of a Correct Projection

A correct projection is:
- Deterministic
- Bounded
- Stable
- Invariant-preserving
- Mismatch-consistent
- Basin-consistent
- Region-partition-consistent
- Dictionary-compatible

A bad projection:
- Violates bounds
- Introduces semantics
- Uses geometry
- Uses normalization
- Uses probabilistic behavior
- Produces unstable region IDs
- Breaks region partitions

## Constraints Summary

Projection must be deterministic, bounded, stable, non-semantic, and non-geometric. It must preserve all invariants from prior papers while operating strictly within the manifold surface domain. It must never employ disallowed transformations or interpretations.

This completes the definition of projection constraints.

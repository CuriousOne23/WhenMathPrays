# Manifold Surface Domain Specification

## Purpose

This paper establishes the allowable numeric domain of the manifold surface coordinate. It defines the constraints that govern valid surface coordinates and the structural properties required for downstream compatibility. It relates the domain to dictionary coordinate ranges (from Paper 1) but does not describe how projection operates.

## Manifold Surface Numeric Domain Definition

The numeric domain of the manifold surface coordinate is the **discrete region index domain** (integer region IDs).

**Justification**:

- **Determinism**: Integer region IDs support exact, repeatable identification without ambiguity.
- **Boundedness**: The domain is strictly finite (region IDs in $0 \dots M$, where $M$ is the number of defined regions).
- **Stability**: Region indices remain invariant under repeated evaluation of the same inputs.
- **Non-semantic behavior**: Indices function purely as labels for admissible partitions; they carry no interpretive meaning.
- **Compatibility with dictionary integer coordinates**: Direct mapping from dictionary-derived integer indices to region indices is straightforward and order-preserving.
- **Compatibility with projection constraints**: Provides a discrete target space that projection operators can map into deterministically.
- **Compatibility with reverse mapping to RSG/RG/OuBB**: Enables deterministic lookup from region index to surface patterns and text assembly.

This discrete choice aligns with the integer nature of dictionary coordinates (Paper 1) and supports the deterministic requirements of TS.

## Domain Constraints

Any valid manifold surface coordinate must satisfy:

- Numeric bounds: $0 \leq \text{region}\_{id} \leq M$
- Admissibility constraints: Must belong to an admissible region per basin and mismatch rules
- Basin constraints: Must align with defined basin partitions
- Mismatch-field constraints: Must respect mismatch resolution boundaries
- Region partition constraints: Must fall within predefined symbolic region divisions
- Stability under repeated evaluation: Same input conditions always yield the same region index
- No geometric interpretation
- No semantic interpretation
- No probabilistic behavior
- No normalization or clamping
- No learned transformations

## Structural Properties of the Domain

The manifold surface domain has the following structural qualities:

- Discrete (integer indices)
- Ordered (region IDs preserve adjacency and priority where defined)
- Bounded (finite number of regions)
- Dimensionality: Effectively one-dimensional (region index) with implicit partitioning
- Region partitioning rules: Fixed symbolic partitions derived from basin definitions and dictionary invariants
- Relationship to dictionary coordinates: Dictionary integer indices map into this domain via admissible region assignment while preserving bounds and ordering
- Domain boundaries ensure deterministic compatibility for downstream operations (without defining those operations)

## Example Domain Specification

Domain type: Discrete region index domain (integer IDs).

- Bounds: Region IDs range from $0$ to $M = 127$ (example bounded size)
- Region partitions: 128 fixed regions, grouped under basin categories
- Admissibility constraints: A region ID is valid only if it satisfies basin alignment and mismatch-field rules for the given dictionary coordinates
- Mismatch-field constraints: Specific regions reserved for mismatch resolution paths
- Relation to dictionary coordinates (Paper 1): A dictionary vector such as $(17, 8, 23, 42, 5)$ maps to a valid region ID (e.g., $42$) within the bounded domain, preserving all invariants

This example illustrates domain structure only.

## Constraints Summary

The manifold surface domain must satisfy:

- Bounded (finite integer indices)
- Deterministic
- Stable
- Non-semantic (indices as labels only)
- Non-geometric
- Compatible with dictionary integer coordinates (Paper 1)
- Compatible with projection constraints (without defining projection)
- Compatible with reverse mapping (without defining reverse mapping)

This specification defines the target domain for the manifold surface coordinate as the foundation for the TS architecture.

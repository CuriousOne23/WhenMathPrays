# Dictionary Numeric Coordinate Specification

## Purpose

This white paper defines the numeric coordinate system used by the dictionary subsystem for mapping SSR grounding fields to numeric coordinates. These coordinates serve as the stable, deterministic foundation for downstream TS operations while remaining strictly non-semantic.

## Numeric Range Definition

The allowable numeric range for dictionary-derived coordinates is the integer index range (e.g., $0 \dots N$, where $N$ is dictionary-defined and bounded).

**Justification**:

- **Determinism**: Integer indices support exact, repeatable lookup and mapping without floating-point ambiguity.
- **Boundedness**: The range is strictly finite and dictionary-enforced ($0 \leq c_i \leq N$).
- **Stability**: Integer indices remain invariant under repeated lookups of the same SSR fields.
- **Non-semantic behavior**: Indices carry no interpretive meaning; they function purely as ordered labels.
- **TS compliance**: Aligns with the fixed-time-step, deterministic state machine nature of TS.
- **Compatibility with manifold projection**: Provides discrete, ordered inputs suitable for bounded projection operators.
- **Compatibility with reverse mapping to OuBB text**: Enables straightforward deterministic lookup tables from coordinate indices back to surface patterns and text assembly.

This choice avoids continuous ranges that could introduce instability or require additional normalization steps.

## Mapping Rules from SSR Fields → Numeric Coordinates

Mapping is dictionary-driven and strictly deterministic:

- $\text{identity}\\_$ $\rightarrow$ dictionary lookup $\rightarrow$ integer index $c\_{identity}$
- $\text{relation}\\_$ $\rightarrow$ dictionary lookup $\rightarrow$ integer index $c\_{relation}$
- $\text{domain}\_{anchor}\\_$ $\rightarrow$ dictionary lookup $\rightarrow$ integer index $c\_{\text{domain}}$
- $\text{H}_{\text{Kn}}$ $\rightarrow$ dictionary lookup $\rightarrow$ integer index $c\_{\text{HKn}}$
- `surface_*` fields $\rightarrow$ dictionary lookup $\rightarrow$ integer indices $c\_{{surface}_j}$ (one per field)

Each mapping consists of a fixed dictionary lookup that returns a unique integer index within the defined range. No inference, no probabilistic selection, and no geometric interpretation occur.

## Coordinate Invariants

The following invariants must always hold for any valid coordinate vector:

- Numeric bounds: All components satisfy $0 \leq c_i \leq N$
- Ordering: Components preserve SSR field priority order (`identity_` first, followed by `relation_`, etc.)
- Stability: Repeated mapping of identical SSR fields always yields identical coordinate vectors
- No hashing
- No normalization
- No clamping
- No modulo arithmetic
- No learned transformations

These invariants ensure the coordinate system remains a reliable, dictionary-grounded index space.

## Example Mapping

Consider sample SSR grounding fields:

- `identity_` = "agent"
- `relation_` = "performs"
- `domain_anchor_` = "task"
- `H_Kn` = "KN-42"
- `surface_primary` = "action"

Dictionary lookup yields:

- $c_{\text{identity}} = 17$
- $c_{\text{relation}} = 8$
- $c_{\text{domain}} = 23$
- $c_{HKn} = 42$
- $c_{\text{surface}} = 5$

Resulting coordinate vector: $(17, 8, 23, 42, 5)$

All invariants hold: values are within $[0, N]$, ordering is preserved, mapping is stable and dictionary-derived.

## Constraints Summary

The dictionary numeric coordinate system must satisfy:

- Integer indices only (bounded range $0 \dots N$)
- Purely dictionary-driven mappings
- Strict determinism
- Boundedness and stability
- Non-semantic (indices as labels only)
- Non-inferential, non-probabilistic, non-geometric
- No disallowed transformations (hashing, normalization, clamping, modulo, learning)
- Preservation of all listed invariants
- Compatibility foundation for (but not definition of) downstream manifold projection and reverse text mapping

This specification provides the required numeric foundation for the TS architecture.

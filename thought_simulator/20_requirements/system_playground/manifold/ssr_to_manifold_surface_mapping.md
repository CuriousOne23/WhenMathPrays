# SSR to Manifold Surface Mapping

## Purpose

This document defines the full deterministic transfer function:

$$
\text{SSR grounding fields} \rightarrow \text{dictionary-derived numeric coordinate vector} \rightarrow \text{manifold surface projection} \rightarrow \text{surface-form pattern selection (RSG)} \rightarrow \text{text realization (RG} \rightarrow \text{OuBB)}
$$

The mapping is numeric (TS-style), deterministic, bounded, stable, non-semantic, non-probabilistic, and non-learned.

## Inputs

SSR grounding fields (symbolic base):

- $\text{identity}\\_$ : symbolic identity token
- $\text{relation}\\_$ : symbolic relation token
- $\text{domain}\_{anchor}\\_$ : symbolic domain anchor token
- $H_{Kn}$ : symbolic knowledge node handle
- `surface_*` fields : surface compatibility descriptors
- Basin definitions (manifold/basins.md)
- Mismatch fields (manifold/mismatch_field.md)
- Region definitions
- Dictionary coordinate rules (dictionary subsystem)
- RSG projection rules
- RG surface-form rules
- OuBB assembly rules

## Numeric Coordinate Construction (Dictionary-Derived Only)

Numeric coordinates are derived exclusively from dictionary subsystem rules. SSR grounding fields map to coordinates via dictionary lookup.

$$
\text{field} \rightarrow \text{dictionary lookup} \rightarrow \text{numeric coordinate}
$$

Dictionary defines:

- Coordinate basis
- Coordinate ordering
- Coordinate bounding
- Coordinate invariants
- Coordinate ranges
- Coordinate stability

Example mapping (dictionary-driven):

$$
c_{\text{identity}} = D(\text{identity}\\_)
$$
$$
c_{\text{relation}} = D(\text{relation}\\_)
$$
$$
c_{\text{domain}} = D(\text{domain}_{anchor}\\_)
$$

where $D$ denotes the fixed dictionary lookup function returning bounded numeric indices. The full coordinate vector is the ordered composition of these components, preserving all dictionary invariants.

## Projection Formula

The projection operator $P$ maps dictionary-derived numeric coordinates to manifold surface coordinate:

$$
\text{surface}_{coord} = P(\text{coord}_{vec})
$$

$P$ is defined by:

- Basin alignment: matching coordinate components against basin constraints
- Admissibility projection: filtering via dictionary invariants
- Mismatch correction: deterministic adjustment per mismatch_field rules
- Region identity assignment: assignment to admissible region partition
- Surface coordinate collapse: reduction to discrete surface position

This operator is deterministic and bounded, operating strictly within dictionary-defined ranges and manifold partitions. No foreign numeric mechanisms are used.

## Manifold Surface Mapping

Surface coordinate drives the downstream path:

$$
\text{text} = \text{assemble}\left( RG_{template}\left( RSG_{pattern}\left( \text{surface}_{coord} \right) \right) \right)
$$

This includes:

- Clause-shape selection (via RSG)
- Surface-form template selection (via RG)
- Deterministic pattern lookup
- Mismatch-aware pattern correction
- Final text assembly (via OuBB)

All steps are pure deterministic lookup and assembly.

## Integration

- **RSG** consumes the surface coordinate for pattern projection and clause-shape selection.
- **RG** consumes the resulting surface-form patterns/templates.
- **OuBB** receives the final assembled text.
- **Path A** remains completely isolated from this manifold path.

## Constraints

- No geometry
- No numeric meaning (coordinates are indices only)
- No inference
- No semantic expansion
- No probabilistic behavior
- No learning
- No optimization

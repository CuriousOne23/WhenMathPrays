# SSR to Manifold Surface Mapping

## Purpose

This document defines the full deterministic transfer function:

$$
\text{SSR grounding fields} \rightarrow \text{numeric coordinate vector} \rightarrow \text{manifold surface projection} \rightarrow \text{surface-form pattern selection} \rightarrow \text{text realization}
$$

The mapping is numeric in the TS sense: stable, deterministic, bounded, non-semantic, non-probabilistic, and non-learned. It bridges SSR → manifold → RSG → RG → OuBB while preserving all architectural constraints.

## Inputs

SSR grounding fields (symbolic base):

- $\text{identity}\\_$ : symbolic identity token
- $\text{relation}\\_$  : symbolic relation token
- $\text{domain}\_{\text{anchor}}\\_$ : symbolic domain anchor token
- `H_{Kn}` : symbolic knowledge node handle
- `surface_*` fields : surface compatibility descriptors
- Basin definitions (from manifold/basins.md)
- Mismatch fields (from manifold/mismatch_field.md)
- Region definitions (symbolic partitions)
- Dictionary coordinate rules (from dictionary subsystem)
- RSG projection rules (from rsg_projection_rules.md)
- RG surface-form rules (from rg_surface_forms.md)

## Numeric Coordinate Construction

SSR grounding fields are mapped to a bounded numeric coordinate vector using dictionary-defined rules. The coordinate basis is fixed and symbolic-derived.

Coordinate vector construction:

$$
coord\_{vec} = \left( c_1, c_2, \dots, c_n \right)
$$

where each $c_i$ is a deterministic integer or bounded real derived from field hashing/mapping (non-semantic, dictionary-driven).

**Normalization and Bounding:**

$$
c_i' = \text{clamp}\left( \text{normalize}(f(\text{field}_i)), -B, B \right)
$$

**Coordinate Invariants:**

- Ordering preserved by field priority (`identity_ > relation_ > domain_anchor_`)
- Basin alignment via component-wise matching
- Mismatch correction via additive offset within bounds

All operations are deterministic fixed mappings with no runtime computation beyond lookup and bounded arithmetic.

## Projection Formula

Projection from numeric coordinates to manifold surface:

$$
\text{surface}\_{coord} = P(\text{coord}\_{vec})
$$

where $P$ is the deterministic projection operator implementing:

- Region selection: nearest admissible region by coordinate distance (bounded metric)
- Basin alignment: component projection onto basin constraints
- Mismatch correction: symbolic rule application with numeric offset
- Surface coordinate collapse: reduction to discrete surface index

$$
\text{surface}\_{index} = \left\lfloor \sum_{i} w_i \cdot c_i' \right\rfloor \mod R
$$

(with weights $w_i$ fixed from dictionary, $R$ = number of regions).

This yields a discrete surface position aligned with basin and region definitions.

## Manifold Surface Mapping

The surface position selects admissible surface patterns per RSG rules. Mismatch fields trigger deterministic corrections that adjust the surface index within bounded regions without altering invariants.

## Reverse Projection to Text

Deterministic reverse path:

1. Manifold surface position → RSG pattern lookup (clause_shapes.md)
2. RSG pattern → RG surface-form template (rg_assembly_rules.md)
3. RG surface form → OuBB text assembly (oubb_assembly_rules.md, oubb_surface_forms.md)

$$
\text{text} = \text{assemble}\left(\ RG_{template}(\ RSG\_{pattern}(\ surface_{index})) \right)
$$

All steps are pure lookup and concatenation with no inference.

## Integration

- **RSG**: Consumes surface coordinates/index for pattern projection and clause assembly.
- **RG**: Consumes selected surface-form patterns for template application.
- **OuBB**: Receives final assembled text output.
- **Path A**: Remains fully isolated; this mapping operates exclusively in the manifold path.

## Constraints

- No geometry
- No numeric meaning (coordinates are indices only)
- No inference
- No semantic expansion
- No probabilistic behavior
- No learning
- No optimization

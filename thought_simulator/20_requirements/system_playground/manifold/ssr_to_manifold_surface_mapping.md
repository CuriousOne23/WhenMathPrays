# SSR to Manifold Surface Mapping

## Purpose

This document defines the deterministic, symbolic-only transfer function from SSR grounding fields to manifold surface placement. It fills the architectural link between SSR → manifold → RSG → RG → OuBB.

The mapping performs only symbolic admissibility checking, basin selection, mismatch resolution, and region identity assignment. No geometry. No numeric operations. No inference. No dynamic meaning.

## Inputs

SSR grounding fields (symbolic):

- `identity_` : symbolic identity token
- `relation_` : symbolic relation token
- `domain_anchor_` : symbolic domain anchor token
- `H_Kn_` : symbolic knowledge node handle
- `surface_*` fields : surface compatibility descriptors
- Basin definitions (from manifold/basins.md)
- Mismatch fields (from manifold/mismatch_field.md)
- Region definitions (symbolic partitions on manifold surface)

All inputs are treated as pure symbols for admissibility and selection rules.

## Outputs

Symbolic outputs consumed by RSG:

- Manifold coordinates (symbolic only, e.g., region identifiers and basin labels)
- Region identity
- Admissibility record (symbolic pass/fail with mismatch tags)
- Manifold placement record (composite symbolic structure passed downstream)

## Mapping Rules

The deterministic mapping pipeline consists of the following symbolic steps:

1. **Basin Selection**  
   Match `identity_`, `relation_`, and `domain_anchor_` against basin definitions using exact symbolic compatibility.  
   Select the unique admissible basin or apply default mismatch basin if none match.

2. **Coordinate Admissibility**  
   Verify `H_Kn_` and `surface_*` fields against selected basin constraints using pure symbolic matching.  
   Produce admissibility record as a set of symbolic tags.

3. **Mismatch Resolution**  
   If mismatch fields are present, apply deterministic symbolic resolution rules (defined in mismatch_field.md) to adjust placement without semantic interpretation.

4. **Region Identity Assignment**  
   Assign region identity based on basin and admissibility record using predefined symbolic region partitioning.

5. **Construction of Manifold Placement Record**  
   Assemble the final record as a symbolic composite:  
   $$
   \text{placement} = \{ \text{basin_label}, \text{region_id}, \text{admissibility_tags}, \text{mismatch_resolution} \}
   $$

All operations remain strictly symbolic and deterministic.

## Integration

- **RSG Consumption**: RSG receives the manifold placement record as input for projection and surface assembly (see rsg_projection_rules.md and rsg_assembly_rules.md).
- **RG Unaffected**: RG operates on downstream surface forms independently (see rg_surface_forms.md).
- **Path A Isolation**: This mapping is isolated from Path A processes.
- **OuBB Reception**: OuBB receives finalized surface-form outputs after RG processing (see oubb_surface_forms.md).

## Constraints

- No geometry
- No numeric operations
- No inference
- No dynamic meaning
- No semantic expansion
- No probabilistic behavior
- No learning
- No optimization

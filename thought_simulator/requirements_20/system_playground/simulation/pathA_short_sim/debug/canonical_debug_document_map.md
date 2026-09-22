# Path-A Canonical Debug Document Map

Date: 2026-09-22
Scope root: thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/debug

This map records the canonical Path-A debug document targets, what currently exists, what is missing, and recommended migration actions.
No rename, delete, or content update actions were performed.

## 1) Canonical Document List

### Dimensions (canonical)
- debug/dimensions/role_geometry.md
- debug/dimensions/identity_geometry.md

### Fields (canonical)
- debug/fields/struct_segments.md
- debug/fields/segment_tokens.md
- debug/fields/struct_roles.md
- debug/fields/constraints_matched.md
- debug/fields/constraints_unmatched.md
- debug/fields/constraint_residue.md
- debug/fields/smoothing_operations.md
- debug/fields/semantic_adjacent_cues.md
- debug/fields/basin_residue.md
- debug/fields/truth_relation.md
- debug/fields/semantic_core.md
- debug/fields/idob_packet.md

### Primitives (canonical)
- debug/primitives/sob.md
- debug/primitives/srob.md
- debug/primitives/cnob.md
- debug/primitives/smob.md
- debug/primitives/idob.md

### Bridge (canonical)
- debug/primitives/appendix_x_token_to_structure_bridge.md

## 2) Existing Documents Detected

### debug/primitives/
- debug/primitives/README.md
- debug/primitives/primitives.md
- debug/primitives/appendix_x_token_to_structure_bridge.md

### debug/dimensions/
- debug/dimensions/README.md
- debug/dimensions/dimensions.md

### debug/fields/
- debug/fields/README.md
- debug/fields/fields.md

## 3) Missing Canonical Documents

### Dimensions
- debug/dimensions/role_geometry.md
- debug/dimensions/identity_geometry.md

### Fields
- debug/fields/struct_segments.md
- debug/fields/segment_tokens.md
- debug/fields/struct_roles.md
- debug/fields/constraints_matched.md
- debug/fields/constraints_unmatched.md
- debug/fields/constraint_residue.md
- debug/fields/smoothing_operations.md
- debug/fields/semantic_adjacent_cues.md
- debug/fields/basin_residue.md
- debug/fields/truth_relation.md
- debug/fields/semantic_core.md
- debug/fields/idob_packet.md

### Primitives
- debug/primitives/sob.md
- debug/primitives/srob.md
- debug/primitives/cnob.md
- debug/primitives/smob.md
- debug/primitives/idob.md

### Bridge
- None (canonical bridge document already exists)

## 4) Legacy Documents That Should Be Renamed Or Removed

These files are generic umbrella docs and do not match canonical Path-A per-concept naming:
- debug/dimensions/dimensions.md
- debug/fields/fields.md
- debug/primitives/primitives.md

Optional legacy-to-keep index files (not canonical concept docs, but useful as folder entry points):
- debug/dimensions/README.md
- debug/fields/README.md
- debug/primitives/README.md

## 5) Recommended Actions (Do Not Execute In This Batch)

1. Create canonical dimension documents:
- debug/dimensions/role_geometry.md
- debug/dimensions/identity_geometry.md

2. Create canonical field documents:
- debug/fields/struct_segments.md
- debug/fields/segment_tokens.md
- debug/fields/struct_roles.md
- debug/fields/constraints_matched.md
- debug/fields/constraints_unmatched.md
- debug/fields/constraint_residue.md
- debug/fields/smoothing_operations.md
- debug/fields/semantic_adjacent_cues.md
- debug/fields/basin_residue.md
- debug/fields/truth_relation.md
- debug/fields/semantic_core.md
- debug/fields/idob_packet.md

3. Create canonical primitive documents:
- debug/primitives/sob.md
- debug/primitives/srob.md
- debug/primitives/cnob.md
- debug/primitives/smob.md
- debug/primitives/idob.md

4. Bridge handling:
- Keep debug/primitives/appendix_x_token_to_structure_bridge.md as canonical bridge.
- Do not rename, move, or edit bridge in this batch.

5. Legacy umbrella docs transition:
- Rename or remove after canonical per-concept docs are created and validated:
  - debug/dimensions/dimensions.md
  - debug/fields/fields.md
  - debug/primitives/primitives.md

6. README handling:
- Keep README.md files as navigational index pages, or convert them to explicit canonical index pages if a stricter naming policy is required.

## Consistency Check

Canonical vocabulary covered in this map:
- Segments: struct_segments, segment_tokens
- Roles: struct_roles, role_geometry
- Constraints (CnOB): constraints_matched, constraints_unmatched, constraint_residue
- Smoothing/Basin (SmOB): smoothing_operations, semantic_adjacent_cues, basin_residue
- Identity (IdOB): identity_geometry, truth_relation, semantic_core, idob_packet

No existing markdown files were modified.
No files were renamed or deleted.
No setup yaml or bridge file was edited.

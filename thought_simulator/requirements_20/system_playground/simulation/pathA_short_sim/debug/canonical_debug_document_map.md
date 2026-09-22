# Path-A Canonical Debug Document Map

Date: 2026-09-22
Scope root: thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/debug

This document is the authoritative Path-A canonical debug document map for dimensions, fields, primitives, and bridge coverage.

Execution status for this update:
- NOT executed: no file create/rename/delete/rewrite actions outside this map
- NOT executed: no edits to links.yaml
- NOT executed: no edits to debug/primitives/appendix_x_token_to_structure_bridge.md

## 1. Canonical Document List (Authoritative Target)

### Canonical Dimensions
- debug/dimensions/segment_geometry.md
- debug/dimensions/role_geometry.md
- debug/dimensions/identity_geometry.md
- debug/dimensions/constraint_geometry.md
- debug/dimensions/semantic_core.md
- debug/dimensions/truth_relation.md

### Canonical Primitives
- debug/primitives/SOB.md
- debug/primitives/SROB.md
- debug/primitives/CnOB.md
- debug/primitives/SmOB.md
- debug/primitives/IdOB.md

### Canonical Fields
- debug/fields/struct_segments.md
- debug/fields/segment_tokens.md
- debug/fields/struct_roles.md
- debug/fields/constraints_matched.md
- debug/fields/constraints_unmatched.md
- debug/fields/constraint_residue.md
- debug/fields/smoothing_operations.md
- debug/fields/semantic_adjacent_cues.md
- debug/fields/basin_residue.md
- debug/fields/idob_packet.md

### Canonical Bridge
- debug/primitives/appendix_x_token_to_structure_bridge.md

## 2. Existing Documents Detected

### Existing primitives documents
- debug/primitives/README.md
- debug/primitives/primitives.md
- debug/primitives/appendix_x_token_to_structure_bridge.md

### Existing dimensions documents
- debug/dimensions/README.md
- debug/dimensions/dimensions.md

### Existing fields documents
- debug/fields/README.md
- debug/fields/fields.md

## 3. Missing Canonical Documents

### Missing canonical dimensions
- debug/dimensions/segment_geometry.md
- debug/dimensions/role_geometry.md
- debug/dimensions/identity_geometry.md
- debug/dimensions/constraint_geometry.md
- debug/dimensions/semantic_core.md
- debug/dimensions/truth_relation.md

### Missing canonical primitives
- debug/primitives/SOB.md
- debug/primitives/SROB.md
- debug/primitives/CnOB.md
- debug/primitives/SmOB.md
- debug/primitives/IdOB.md

### Missing canonical fields
- debug/fields/struct_segments.md
- debug/fields/segment_tokens.md
- debug/fields/struct_roles.md
- debug/fields/constraints_matched.md
- debug/fields/constraints_unmatched.md
- debug/fields/constraint_residue.md
- debug/fields/smoothing_operations.md
- debug/fields/semantic_adjacent_cues.md
- debug/fields/basin_residue.md
- debug/fields/idob_packet.md

### Missing canonical bridge
- None

## 4. Legacy Umbrella Documents

The following umbrella files exist and should be transitioned away from as canonical per-concept documents are introduced:
- debug/primitives/primitives.md
- debug/dimensions/dimensions.md
- debug/fields/fields.md

## 5. Recommended Actions (NOT Executed)

### Create (NOT executed)
- Create all missing canonical dimensions listed in Section 3.
- Create all missing canonical primitives listed in Section 3.
- Create all missing canonical fields listed in Section 3.

### Rename (NOT executed)
- Rename debug/primitives/primitives.md to debug/primitives/_legacy_primitives_overview.md if historical retention is required.
- Rename debug/dimensions/dimensions.md to debug/dimensions/_legacy_dimensions_overview.md if historical retention is required.
- Rename debug/fields/fields.md to debug/fields/_legacy_fields_overview.md if historical retention is required.

### Delete (NOT executed)
- Delete legacy umbrella docs only after canonical replacements exist and links are migrated:
- debug/primitives/primitives.md
- debug/dimensions/dimensions.md
- debug/fields/fields.md

### Rewrite (NOT executed)
- Rewrite README index pages to point first to canonical per-concept docs once they are created:
- debug/primitives/README.md
- debug/dimensions/README.md
- debug/fields/README.md

### Remain As-Is (NOT executed)
- Keep debug/primitives/appendix_x_token_to_structure_bridge.md unchanged as the canonical bridge document.
- Keep links.yaml unchanged in this batch.

## 6. Consistency Coverage Check

Canonical vocabulary represented by this map:
- Segments: struct_segments, segment_tokens, segment_geometry
- Roles: struct_roles, role_geometry
- Constraints (CnOB): constraints_matched, constraints_unmatched, constraint_residue, constraint_geometry
- Smoothing/Basin (SmOB): smoothing_operations, semantic_adjacent_cues, basin_residue
- Identity (IdOB): identity_geometry, truth_relation, semantic_core, idob_packet

Validation note:
- This file is structured as valid markdown with complete canonical listings and explicit NOT executed action labels.

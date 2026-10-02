# Path-A Canonical Debug Document Map

Date: 2026-10-02
Scope root: thought_simulator/requirements_20/system_playground/simulation/pathA_short_sim/debug

Status: corrected inventory for the short-sim debug tree. This file is not an execution log. The 2026-09-22 "missing" list is retired. Those cards now exist. Do not archive this map; correct it when the tree changes.

Theory note, prior reading for an architectural question: [pathA_structure_theory.md](pathA_structure_theory.md). It governs this debug set. It does not govern the structure-to-meaning bench.

## 1. Live tree

### Theory
- [pathA_structure_theory.md](pathA_structure_theory.md)

### Dimensions
- [dimensions/segment_geometry.md](dimensions/segment_geometry.md)
- [dimensions/role_geometry.md](dimensions/role_geometry.md)
- [dimensions/constraint_geometry.md](dimensions/constraint_geometry.md)
- [dimensions/identity_geometry.md](dimensions/identity_geometry.md)
- [dimensions/semantic_core.md](dimensions/semantic_core.md)
- [dimensions/truth_relation.md](dimensions/truth_relation.md)

Not in the tree, and not legal names: `smoothing_geometry.md`, `meaning_geometry.md`.

### Primitives
- [primitives/IE.md](primitives/IE.md)
- [primitives/SOB.md](primitives/SOB.md) — Structural Observation Block
- [primitives/SROB.md](primitives/SROB.md) — Structural Refinement Observation Block
- [primitives/CnOB.md](primitives/CnOB.md) — Constraint Observation Block
- [primitives/SmOB.md](primitives/SmOB.md) — Semantic Observation Block
- [primitives/IdOB.md](primitives/IdOB.md) — Identity Observation Block
- [primitives/appendix_x_token_to_structure_bridge.md](primitives/appendix_x_token_to_structure_bridge.md)

### Fields
- [fields/struct_segments.md](fields/struct_segments.md)
- [fields/segment_tokens.md](fields/segment_tokens.md)
- [fields/struct_roles.md](fields/struct_roles.md)
- [fields/constraints_matched.md](fields/constraints_matched.md)
- [fields/constraints_unmatched.md](fields/constraints_unmatched.md)
- [fields/constraint_residue.md](fields/constraint_residue.md)
- [fields/smoothing_operations.md](fields/smoothing_operations.md)
- [fields/semantic_adjacent_cues.md](fields/semantic_adjacent_cues.md)
- [fields/basin_residue.md](fields/basin_residue.md)
- [fields/idob_packet.md](fields/idob_packet.md)
- [fields/residue.md](fields/residue.md) — compatibility alias
- [fields/smob_smoothing_residue.md](fields/smob_smoothing_residue.md) — compatibility alias

### Examples
- [examples/why_this_cut.md](examples/why_this_cut.md) — prohibition argument
- [examples/placeholder.md](examples/placeholder.md) — debugger stub

### Setup
- [setup/debug_setup.yaml](setup/debug_setup.yaml)
- [setup/links.yaml](setup/links.yaml)

## 2. Vocabulary check

- Segments: `struct_segments`, `segment_tokens`, `segment_geometry`
- Roles: `struct_roles`, `role_geometry` — positional labels, not `semantic_core`
- Constraints: `constraints_matched`, `constraints_unmatched`, `constraint_residue`, `constraint_geometry`
- SmOB Job 1: `smoothing_operations` is an operation list, not the stage name; `semantic_adjacent_cues`, `basin_residue`
- Identity: `idob_packet`, dict `semantic_core`, `identity_geometry`, `truth_relation`

## 3. Retired claims

The 2026-09-22 map listed the dimension, primitive, and field cards as missing, and it mistyped the IdOB link as `rimitives/IdOB.md` under a broken relative path. Those claims are withdrawn. Umbrella files named in that map (`primitives.md`, `dimensions.md`, `fields.md`) are not in the current tree. This inventory does not recreate them.

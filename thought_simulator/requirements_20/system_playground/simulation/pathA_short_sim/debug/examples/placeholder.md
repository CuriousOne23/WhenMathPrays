# examples

definition: The examples documentation provides symbolic, debugger-style illustrations of how primitives, geometry dimensions, and fields appear in interpreted output. These examples do not represent real simulator runs; instead, they demonstrate the structural and semantic relationships that the debugger is designed to reveal. Examples help users understand how segment, role, constraint, smoothing, identity, and meaning geometries interact across primitives.

example_types:
	- primitive_activation_examples
	- geometry_interaction_examples
	- constraint_satisfaction_examples
	- identity_and_semantic_examples

effects:
	- clarifies how interpreted_blocks output is structured
	- illustrates interactions between geometry dimensions and fields
	- supports debugging and educational understanding of primitive behavior
	- provides symbolic reference points for interpreting real simulator logs

examples:
	- "SOB fired: segment_geometry=composite, struct_segments=composite_segment, residue=structural_residue"
	- "SROB fired: role_geometry=modifier, semantic_adjacent_cues=adjacent_cue, struct_roles=modifier"
	- "CnOB matched: constraint_geometry=compatibility_rule, constraints_matched=compatibility_rule, segment_geometry=atomic"
	- "IdOB packet formed: identity_geometry=packet_identity, idob_packet=referential_packet, meaning_geometry=semantic_cue"

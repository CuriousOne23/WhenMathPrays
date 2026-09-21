# residue

definition: The residue field records leftover structural or semantic material that was not fully incorporated into segment, role, or constraint interpretation. It reflects partial matches, unresolved cues, or structural fragments that persist across primitives. This field helps diagnose incomplete or unstable interpretations.

allowed_values:
	- structural_residue
	- semantic_residue
	- adjacency_residue
	- continuity_residue

effects:
	- influences smoothing operations for SmOB
	- constrains identity confirmation for IdOB
	- shapes constraint satisfaction for CnOB
	- affects role alignment for SROB

example:
	- "SmOB applied: residue=structural_residue, smoothing_geometry=segment_smoothing"
	- "IdOB fired: residue=semantic_residue, identity_geometry=semantic_identity"

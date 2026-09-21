# semantic_adjacent_cues

definition: The semantic_adjacent_cues field records meaning-bearing signals that arise from adjacency relationships between segments or roles. It reflects how semantic cues propagate through structural geometry and how meaning geometry interacts with primitive activation. This field captures semantic continuity across interpretation.

allowed_values:
	- adjacent_cue
	- propagated_cue
	- structural_cue
	- semantic_cue

effects:
	- activates semantic cue propagation for SmOB
	- influences constraint satisfaction for CnOB
	- shapes identity confirmation for IdOB
	- interacts with role geometry during SROB evaluation

example:
	- "SmOB applied: semantic_adjacent_cues=adjacent_cue, role_geometry=modifier"
	- "IdOB fired: semantic_adjacent_cues=semantic_cue, identity_geometry=referential_identity"


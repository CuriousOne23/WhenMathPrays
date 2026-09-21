# meaning_geometry

definition: Meaning geometry encodes how semantic cues, adjacent signals, and meaning-bearing structures propagate through interpretation. It determines how semantic rules activate, how cues interact with structural geometry, and how primitives incorporate meaning into evolving representations. Meaning geometry governs semantic coherence across the pipeline.

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
	- "SmOB applied: meaning_geometry=adjacent_cue, role_geometry=modifier"
	- "IdOB fired: meaning_geometry=semantic_cue, identity_geometry=referential_identity"

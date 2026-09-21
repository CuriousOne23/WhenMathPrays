# SROB

definition: SROB (Segment Role Observation Block) assigns functional roles to segments, such as head, modifier, predicate, or argument. It evaluates role geometry, aligns structural units with functional patterns, and determines how segments participate in dependency formation. SROB provides the functional backbone for constraint and semantic evaluation.

allowed_values:
	- head
	- modifier
	- predicate
	- argument

effects:
	- activates role pattern matching for constraint evaluation in CnOB
	- shapes semantic cue propagation for SmOB
	- influences identity confirmation pathways for IdOB
	- constrains segment geometry interpretation for SOB

example:
	- "SROB fired: role_geometry=head, struct_roles=head"
	- "SROB fired: role_geometry=modifier, semantic_adjacent_cues=adjacent_cue"


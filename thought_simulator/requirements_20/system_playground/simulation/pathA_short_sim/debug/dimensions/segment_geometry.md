# segment_geometry

definition: Segment geometry encodes the structural form, adjacency, and class membership of token spans. It determines how the simulator groups tokens into coherent segments and how those segments participate in structural interpretation. Segment geometry governs head-dependent relations, admissible segment classes, and the structural envelope within which primitives operate.

allowed_values:
	- atomic
	- composite
	- recursive
	- discontinuous

effects:
	- constrains admissible segment classes during SOB evaluation
	- influences role geometry resolution for SROB
	- shapes constraint satisfaction envelopes for CnOB
	- determines structural continuity requirements for smoothing operations

example:
	- "SOB fired: segment_geometry=composite, role_geometry=modifier"
	- "CnOB matched: segment_geometry=atomic, constraint_geometry=adjacency_rule"

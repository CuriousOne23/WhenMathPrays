# struct_segments

definition: The struct_segments field records the structural segmentation recognized during interpretation. It encodes how token spans were grouped into atomic, composite, or recursive segments and provides the structural basis for role and constraint evaluation. This field reflects the simulator's segmentation decisions across primitives.

allowed_values:
	- atomic_segment
	- composite_segment
	- recursive_segment
	- discontinuous_segment

effects:
	- influences role geometry resolution for SROB
	- constrains admissible segment classes for SOB
	- shapes constraint satisfaction envelopes for CnOB
	- interacts with smoothing geometry during SmOB

example:
	- "SOB fired: struct_segments=composite_segment, segment_geometry=composite"
	- "CnOB matched: struct_segments=atomic_segment, constraint_geometry=adjacency_rule"


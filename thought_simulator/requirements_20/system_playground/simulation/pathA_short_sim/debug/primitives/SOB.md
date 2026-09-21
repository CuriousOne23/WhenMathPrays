# SOB

definition: SOB (Segment Observation Block) records the simulator's recognition of segment structures. It evaluates segment geometry, identifies admissible segment classes, and establishes the structural envelope for downstream primitives. SOB provides the foundational segmentation that supports role, constraint, smoothing, and identity operations.

allowed_values:
	- atomic_segment
	- composite_segment
	- recursive_segment
	- discontinuous_segment

effects:
	- constrains role geometry activation for SROB
	- shapes constraint satisfaction envelopes for CnOB
	- influences smoothing requirements for SmOB
	- provides structural anchors for IdOB identity confirmation

example:
	- "SOB fired: segment_geometry=composite, struct_segments=composite_segment"
	- "SOB fired: segment_geometry=atomic, residue=structural_residue"


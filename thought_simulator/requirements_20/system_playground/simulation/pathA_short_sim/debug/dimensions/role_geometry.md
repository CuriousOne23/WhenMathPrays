# role_geometry

definition: Role geometry defines how segments participate in functional relationships such as heads, modifiers, predicates, and arguments. It encodes the structural roles segments may assume and determines how role patterns activate during interpretation. Role geometry influences dependency formation and functional alignment across primitives.

allowed_values:
	- head
	- modifier
	- predicate
	- argument

effects:
	- determines role pattern activation for SROB
	- influences constraint matching for CnOB
	- shapes semantic cue propagation for SmOB
	- affects identity resolution pathways for IdOB

example:
	- "SROB fired: role_geometry=head, segment_geometry=atomic"
	- "SmOB applied: role_geometry=modifier, meaning_geometry=adjacent_cue"


# struct_roles

definition: The struct_roles field records the functional roles assigned to segments, such as head, modifier, predicate, or argument. It reflects how the simulator aligned structural units with functional patterns and how role geometry influenced primitive activation. This field provides the functional backbone of interpretation.

allowed_values:
	- head
	- modifier
	- predicate
	- argument

effects:
	- determines role pattern activation for SROB
	- influences constraint matching for CnOB
	- shapes semantic cue propagation for SmOB
	- affects identity confirmation for IdOB

example:
	- "SROB fired: struct_roles=head, role_geometry=head"
	- "SmOB applied: struct_roles=modifier, meaning_geometry=adjacent_cue"


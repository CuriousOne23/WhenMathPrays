# constraints_matched

definition: The constraints_matched field records which structural, adjacency, or compatibility constraints were satisfied during interpretation. It reflects the simulator's evaluation of constraint geometry and determines whether primitives such as CnOB can activate. This field captures structural coherence conditions.

allowed_values:
	- adjacency_rule
	- compatibility_rule
	- structural_rule
	- continuity_rule

effects:
	- governs constraint satisfaction for CnOB
	- restricts segment-role combinations for SOB and SROB
	- shapes smoothing requirements for SmOB
	- influences identity confirmation for IdOB

example:
	- "CnOB matched: constraints_matched=compatibility_rule, role_geometry=argument"
	- "SOB blocked: constraints_matched=adjacency_rule not satisfied"


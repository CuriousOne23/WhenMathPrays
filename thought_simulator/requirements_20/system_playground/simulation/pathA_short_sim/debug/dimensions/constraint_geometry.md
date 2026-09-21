# constraint_geometry

definition: Constraint geometry encodes structural, adjacency, and compatibility rules that govern whether segments and roles satisfy required conditions. It determines how constraint patterns are evaluated and how structural envelopes restrict primitive activation. Constraint geometry ensures coherence across segment and role interactions.

allowed_values:
	- adjacency_rule
	- compatibility_rule
	- structural_rule
	- continuity_rule

effects:
	- governs constraint satisfaction for CnOB
	- restricts segment-role combinations during SOB and SROB
	- shapes smoothing requirements for SmOB
	- influences identity confirmation for IdOB

example:
	- "CnOB matched: constraint_geometry=compatibility_rule, role_geometry=argument"
	- "SOB blocked: constraint_geometry=adjacency_rule not satisfied"


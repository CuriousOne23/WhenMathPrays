# CnOB

definition: CnOB (Constraint Observation Block) evaluates structural, adjacency, and compatibility constraints across segments and roles. It determines whether required conditions are satisfied and governs the activation of constraint geometry. CnOB ensures structural coherence and regulates the admissibility of primitive transitions.

allowed_values:
	- adjacency_rule
	- compatibility_rule
	- structural_rule
	- continuity_rule

effects:
	- governs constraint satisfaction envelopes for structural interpretation
	- restricts segment-role combinations for SOB and SROB
	- shapes smoothing requirements for SmOB
	- influences identity confirmation for IdOB

example:
	- "CnOB matched: constraint_geometry=compatibility_rule, constraints_matched=compatibility_rule"
	- "CnOB matched: constraint_geometry=adjacency_rule, residue=adjacency_residue"


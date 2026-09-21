# identity_geometry

definition: Identity geometry encodes how structural and semantic elements are recognized as belonging to the same referential or functional identity. It governs identity confirmation, packet formation, and referential stability across primitives. Identity geometry ensures consistent interpretation of repeated or related structures.

allowed_values:
	- referential_identity
	- structural_identity
	- semantic_identity
	- packet_identity

effects:
	- activates identity confirmation for IdOB
	- shapes packet formation for identity-related fields
	- influences semantic cue propagation for SmOB
	- constrains role alignment for SROB

example:
	- "IdOB fired: identity_geometry=referential_identity, segment_geometry=atomic"
	- "IdOB packet formed: identity_geometry=packet_identity, meaning_geometry=adjacent_cue"


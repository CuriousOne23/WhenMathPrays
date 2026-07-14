**path_a_meaning_is_four_fields.md**

The Path A four-field token model consists of token_surface, token_base, token_expression, and token_intent. These four fields are necessary and sufficient for meaning understanding and interpretation in Path A.

TS requires a four-field token model to support deterministic, lane-local meaning construction under the constraints of the architecture scaffold. The fields partition surface geometry, lexical identity, expressive metadata, and pragmatic force so that each Path A primitive owns only the surfaces required for its role. This partitioning prevents authority drift, preserves replay equivalence, and enables clean commitment via TPU to semantic_core.

token_surface preserves expressive geometry, adjacency cues, punctuation force, elongation, and emotional shading.  
token_base preserves lexical identity, dictionary meaning, semantic roles, and truth-relation mapping.  
token_expression preserves affective and expressive metadata such as elongation, intensity, repetition, punctuation patterns, and other expressive features.  
token_intent preserves communicative force, including supportive, clarifying, deceptive, controlling, obscurifying, challenging, hurting, or other pragmatic valence.

InB initializes all fields to default values. IIInB proposes expression metadata only. IE commits token_surface, token_base, and token_expression while leaving token_intent empty. SOB begins low-confidence intent classification. SROB refines intent based on adjacency and roles. SmOB harmonizes intent with structural context. IdOB performs identity-conditioned meaning refinement and is the first primitive allowed to finalize token_intent. TR applies truth-relation shading based on refined intent. SSR constructs final semantic structure using all four fields.

IdOB uses the stabilized four fields under routed identity basins to finalize token_intent with identity-specific pragmatic valence. TR uses the finalized token_intent to shade truth relations. SSR integrates all four fields into the immutable SSR(t) snapshot for Path B.

The model aligns with A/B separation by confining meaning construction and field updates to Path A; Path B operates read-only on the SSR(t) bridge.

**Refactoring Anchor**

The following TS documents must be updated to align with this paper:  
- 20.190_glossary.md  
- 20.15_ts_architecture_scaffold.md  
- 20.705_patha_pathb_flow.md  
- All Path A YAML primitive definitions  
- All requirements documents referencing token processing

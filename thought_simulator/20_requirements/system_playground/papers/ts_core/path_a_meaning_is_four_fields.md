**path_a_meaning_is_four_fields.md**

The Path A four-field token model consists of token_surface, token_base, token_expression, and token_intent. These four fields are necessary and sufficient for meaning understanding and interpretation in Path A.

TS requires a four-field token model to support deterministic, lane-local meaning construction under the constraints of the architecture scaffold. The fields partition surface geometry, lexical identity, expressive metadata, and pragmatic force so that each Path A primitive owns only the surfaces required for its role. This partitioning prevents authority drift, preserves replay equivalence, and enables clean commitment via TPU to semantic_core. Removing any field breaks deterministic meaning construction; adding fields violates minimalism and explicit dependency rules.

token_surface preserves expressive geometry, adjacency cues, punctuation force, elongation, and emotional shading.  
token_base preserves lexical identity, dictionary meaning, semantic roles, and truth-relation mapping.  
token_expression preserves affective and expressive metadata such as elongation, intensity, repetition, punctuation patterns, and other expressive features.  
token_intent preserves communicative force, including supportive, clarifying, deceptive, controlling, obscurifying, challenging, hurting, or other pragmatic valence.

InB initializes all fields to default values. IIInB proposes expression metadata only. IE commits token_surface, token_base, and token_expression while leaving token_intent empty. SOB begins low-confidence intent classification. SROB refines intent based on adjacency and roles. SmOB harmonizes intent with structural context. IdOB performs identity-conditioned meaning refinement and is the first primitive allowed to finalize token_intent. TR applies truth-relation shading based on refined intent. SSR constructs final semantic structure using all four fields.

IdOB uses the stabilized four fields under routed identity basins to finalize token_intent with identity-specific pragmatic valence. TR uses the finalized token_intent to shade truth relations. SSR integrates all four fields into the immutable SSR(t) snapshot for Path B. SSR(t) is the immutable meaning-layer handoff that guarantees A/B separation and replay-stable realization.

The four fields together ensure replay-equivalent meaning construction under identical input and routing. For “really?!”, token_surface captures punctuation force and adjacency, token_expression captures intensity, token_base anchors lexical questioning role, and token_intent captures pragmatic challenge valence.

**Foundations in Linguistic and Cognitive Science**

The partitioning draws directly from established linguistic and cognitive frameworks. Surface geometry and adjacency align with syntactic and prosodic structure. Lexical identity and semantic roles correspond to frame-based meaning representation, where words evoke structured conceptual backgrounds. Expressive metadata reflects affective and stylistic dimensions. Token_intent maps to pragmatic force and illocutionary intent, the core of speech act theory.

Classic speech act theory (Austin 1962; Searle 1969) distinguishes locutionary content from illocutionary force—the intended action performed by an utterance. Frame semantics (Fillmore 1976, 1982; FrameNet) shows that lexical meaning requires activation of background frames and roles. Cognitive science research on abstract concepts emphasizes multiple orthogonal dimensions rather than a single undifferentiated representation. These cognitive foundations justify the four-field partition as both theoretically grounded and operationally enforceable within the TS architecture.

**Advantages for Cognition and Machines**

Partitioning meaning into these four fields offers clear advantages. It enables modular, tractable processing: each primitive operates on a bounded, well-defined surface without needing global inference. This supports determinism and replay equivalence, as field values remain derivable from prior state under fixed rules. The structure improves interpretability and debuggability. For machines, it facilitates hardware-software co-design through explicit dependencies and safe boundaries. Cognitively, it mirrors how humans process language across parallel dimensions—form, meaning, affect, and purpose—while maintaining computational tractability.

**Novelty and Realizability**

While linguistics has long recognized layered aspects of meaning (syntax/semantics/pragmatics, frames, speech acts), the explicit operationalization of these four fields as a deterministic, pipeline-enforced model in a state-machine cognitive engine with strict single-writer invariants, identity-basin routing, and A/B separation appears novel. Traditional symbolic AI used brittle rules and frames that struggled with ambiguity and expression. Hybrid neuro-symbolic systems improved perception but often lacked explicit surface-to-intent partitioning and replay guarantees. Today's LLMs rely on statistical emergence, excelling at surface and expressive patterns but suffering from opacity, non-determinism, and weak control over intent or identity-conditioned refinement. This model has not been realized before in this form because prior systems lacked the combination of lane-local projections, explicit safe boundaries, and identity-conditioned finalization required to make the partitioning both cognitively faithful and computationally robust. The result is a realizable foundation for cognition machines that is modular, deterministic, auditable, and aligned with multi-dimensional human meaning processing.

Together, these elements define a deterministic, auditable, cognitively grounded meaning model suitable for scalable TS-based cognition.

**Refactoring Anchor**

The following TS documents must be updated to align with this paper:  
- 20.190_glossary.md  
- 20.15_ts_architecture_scaffold.md  
- 20.705_patha_pathb_flow.md  
- All Path A YAML primitive definitions  
- All requirements documents referencing token processing

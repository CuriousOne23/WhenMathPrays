# Architectural Simulation Notes

## Short Simulator Macro Categories

- Intake Macro: InB, IIInB, IE
- Correction Macro: CEx, CE, ISc, TPU
- Structural Geometry Macro (OB-Set): SOB, SROB, CnOB, SmOB, SSG
- Routing Macro: RBU, RB, TR, TRU, RTU, CTP
- Semantic Macro: IdOB
- Final Commit Macro: OuBA

## Full Path-A Macro Categories (20.705 Section 2)

- Intake Macro
- Correction Macro
- Structural Interpretation Macro (OB-Set)
- Routing Macro (including STPX, DCB, TR (Thought Router))
- Identity and Meaning Macro (IdOB -> MCB)
- Final Commit Macro (OuBA)

## Macro-by-Macro Expectations

### Intake Macro

What it should accomplish:
- Tokenize, normalize, and establish early intake TP state.

TP fields that should feel right:
- raw_text, tokens, normalized_text.

Support dependencies:
- No dictionary dependency.

Trace observations:
- tokens appears in InB.
- normalized_text appears in IE.

Successful simulation:
- Stable token list and deterministic normalization.

### Correction Macro

What it should accomplish:
- Register correction candidates and correction confidence.

TP fields that should feel right:
- defects, corrections, correction_score, commit_flags[correction].

Support dependencies:
- No dictionary dependency (short simulator).

Trace observations:
- correction fields set and correction commit marked.

Successful simulation:
- Correction phase consistently updates correction fields without corrupting intake fields.

### Structural Geometry Macro (OB-Set)

What it should accomplish:
- Convert normalized tokens into structural segments and role geometry.

TP fields that should feel right:
- struct_segments, segment_tokens, struct_roles, role_segments, constraints, smoothed_geometry, structural_vector_frozen.

Support dependencies:
- token_classes.yaml
- segment_patterns.yaml
- role_patterns.yaml
- constraint_rules.yaml

Trace observations:
- SOB creates struct_segments and segment_tokens.
- SROB creates struct_roles and role_segments.
- CnOB records allowed transitions.

Successful simulation:
- Segment and role structure aligns with dictionary intentions and constraints chain coherently.

### Routing Macro

What it should accomplish:
- Build route metadata, select a route, pass through Thought Router placeholder, apply truth-relation stub, then commit route.

TP fields that should feel right:
- routing_metadata, routing_decision, truth_relation, routing_committed, commit_flags[routing].

Support dependencies:
- No direct dictionary dependency in short simulator.

Trace observations:
- RBU sets indices.
- RB sets routing_decision.
- TR emits placeholder behavior note.
- TRU sets truth_relation.
- RTU and CTP commit routing state.

Successful simulation:
- Routing fields are present, deterministic, and trace shows explicit handoff order.

### Semantic Macro

What it should accomplish:
- Extract semantic core from structural output.

TP fields that should feel right:
- semantic_core with agent/action/patient/modifiers.

Support dependencies:
- semantic_rules.yaml

Trace observations:
- IdOB populates semantic_core using segment_tokens and role_segments.

Successful simulation:
- semantic_core matches rules and observed OB-Set structure.

### Final Commit Macro

What it should accomplish:
- Mark path completion.

TP fields that should feel right:
- commit_flags[pathA_complete] set true.

Support dependencies:
- No dictionary dependency.

Trace observations:
- OuBA sets final commit flag.

Successful simulation:
- Final TP reflects complete macro traversal.

## Progressive Validation Strategy

1. Validate Intake first: tokenization and normalization must be stable.
2. Validate Correction next: correction fields and commit flag must update predictably.
3. Validate OB-Set next: segments, segment_tokens, roles, role_segments, constraints.
4. Validate Routing next: metadata, decision, TR placeholder step, TRU truth-relation, route commit.
5. Validate Semantic next: semantic_core extraction should align with dictionaries.
6. Validate Commit last: final path completion flag and coherent end-state TP.

## Future Extension Roadmap Toward Full Path-A

1. Implement STPX and DCB to enrich routing realism.
2. Replace TR placeholder with functional Thought Router logic.
3. Add MCB in Identity and Meaning macro chain.
4. Add provenance metadata tracking for each primitive mutation.
5. Introduce structural graph persistence instead of only list-based fields.
6. Add routing entropy, confidence, and semantic-adjacent cue integration.
7. Expand truth-relation processing from stub behavior to richer TRU logic.

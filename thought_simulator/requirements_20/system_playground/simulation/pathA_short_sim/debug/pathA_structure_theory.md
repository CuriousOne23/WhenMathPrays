# Path A structure theory

Scope: `pathA_short_sim` only. Teaching note for the debug set. Not a primitive card.

This note governs the short simulator. It does not govern `testbenches/idob_structure_to_meaning/`.

`ts_patha_theory.md` governs that other bench. It is not a parent of this note, and it is not a contradiction to repair in this pass. Neither pipeline is imported into the other. Short-sim meaning is the `idob_packet`. Structure-to-meaning geometry, the Cognitive Identity Envelope, and the Meaning Signal Layer stay on that bench. This note is not an authority for those files, and those files are not an authority for the five cards below.

Official names, taken from the primitive headers:

- Structural Observation Block (SOB) — 20.40.010. Realized job: segment cut.
- Structural Refinement Observation Block (SROB) — 20.40.020. Realized job: pre-semantic structural labels. Not semantic role labeling.
- Constraint Observation Block (CnOB) — 20.40.030. Realized job: constraint residue on the walk. C1–C7 reserved.
- Semantic Observation Block (SmOB) — 20.40.040. Realized job: adjacent cues. Smoothing is an operation of Job 1, not the name of the stage. Job 2 hash reserved.
- Identity Observation Block (IdOB) — 20.40.050. Realized job: IdOB-sum / `idob_packet`. IdOB is not an object. Structure-to-meaning, the Cognitive Identity Envelope, and `meaning_delta_h` are reserved.

Eight catalog families live in [../notes/idob_object_space/idob_object_space.md](../notes/idob_object_space/idob_object_space.md). This note does not re-derive them.

Seam, packet contract, and charter: [../architecture/idob_seam.md](../architecture/idob_seam.md), [../architecture/idob_meaning_lock.md](../architecture/idob_meaning_lock.md), [../architecture/path_a_realization_charter.md](../architecture/path_a_realization_charter.md).

## 1. Status and non-claims

Path-A-short is a dictionary-driven teaching simulator. Field names on the cards are teaching aliases. 20.40 remains the richer surface. Realized functions are the ones named on each card.

This note gives the necessity argument those cards assume. It does not restate their algorithms, and it does not add a stage.

Non-claims:

- No Meaning Composition Block on this path.
- No structure-to-meaning vector, no Cognitive Identity Envelope, no Meaning Signal Layer inside IdOB.
- No inference, no reasoning, no cross-sentence memory.
- No import of the other bench's arc (structure, then meaning, then identity, then freeze).

## 2. The human skip

A reader hears *The sky is blue.* and already has a theme, a state, and a claim that was told. A reader hears *Where is the book on the table?* and already has a thing, a place, and a claim that was asked.

That perception is the skip. The chunks, the labels, the legal adjacencies, and the told-versus-asked cut arrive together. A human does not experience them as questions that had to be answered in order.

A machine does not get that skip. If the simulator treats the heard sentence as an already-structured claim, it has imported the human answer and called it input. Path A exists so those questions are computed, written, and inspectable before a packet is legal.

## 3. What structure is here

Structure, in this simulator, is the meaning-blind cut the observation-block set is allowed to write. It is not a metaphysical kind, and it is not the packet.

Four writers, four cuts:

- SOB writes spans and token coverage. A span that does not cover its tokens is not a segment.
- SROB writes a positional label on each span. Those labels are not `semantic_core`.
- CnOB writes which rules hold, which fail, and what residue remains.
- SmOB writes which unresolved signals stabilize into adjacent cues, which smoothing operations were applied, and what basin residue remains.

IdOB does not add a fifth structural cut. It sums a frozen catalog over cuts someone else already wrote, and it writes one packet.

## 4. Questions structure must answer before a packet is legal

Each question is a field that already exists. If the field is missing or illegal, the packet is not yet earned.

- What are the spans, and do they cover the tokens? `struct_segments`, `segment_tokens`.
- What positional label does each span carry, without becoming the packet dict? `struct_roles`.
- Which rules hold, which fail, what residue remains? `constraints_matched`, `constraints_unmatched`, `constraint_residue`.
- Which unresolved signals stabilize into adjacent cues, and what basin residue remains? `smoothing_operations`, `semantic_adjacent_cues`, `basin_residue`.
- Only then: which catalog families activate, what truth-relation, what dict `semantic_core`? `idob_packet`.

A list `semantic_core` after IdOB is not a legal answer. The book is not an IdOB object. Adjacency in `overlap_events` is catalog-object adjacency, not word neighbors.

## 5. Why this order, and what "irreversible" means

The order is a prohibition on reopening the cut. It is not a claim that information is destroyed. Residue is forwarded. Compatibility aliases exist. Later stages may consume, label, constrain, cue, or sum. They may not invent the prior cut.

- A role without a span is a free-floating name. SROB may not cut segments SOB did not write.
- A rule needs something to bind. CnOB may not treat `struct_roles` as `semantic_core`, and it may not invent a span in order to satisfy a rule.
- A cue taken before the unmatched set is an invented adjacency. SmOB may apply a smoothing operation to residue CnOB wrote. It may not re-segment, and it may not write the packet.
- IdOB may activate catalog families over the frozen cut. It may not re-segment, re-label, or re-open constraints to make a packet come out clean.

That is the sense in which the pipeline is irreversible. The cut, once written, is not reopened by a later stage.

## 6. What this architecture delivers

One deterministic packet for a supported family: activation set, truth-relation, and a dict `semantic_core`, plus the contributors and overlap events the sum already computed. The debugger must not sum again.

Supported families and traces live in [../notes/pathA_supported_sentences.md](../notes/pathA_supported_sentences.md). This note does not catalog them.

The deliverable is the packet. It is not an IdOB object, and it is not a reconstructed mental object from the other bench.

## 7. What it explicitly does not deliver

- Inference and reasoning.
- Cross-sentence memory, latent priors, routing entropy.
- Meaning Composition Block.
- Structure-to-meaning geometry, Cognitive Identity Envelope, Meaning Signal Layer.
- Reserved C1–C7 tables and SmOB Job 2.
- A warrant to rewrite the cut because a later layer wishes the packet were different.

Later semantic layers in the broader arc may consume the packet. They may not reach back and reopen the cut. Those layers are not specified here.

## 8. How to read the debug set after this note

Read this note when the question is why a stage is here. Read the cards when the question is what a stage wrote on a log line.

- Dimensions are the vocabularies (`segment_geometry`, `role_geometry`, `constraint_geometry`, `identity_geometry`, `semantic_core`, `truth_relation`).
- Fields are the written answers.
- Primitives are the writers. SOB, SROB, CnOB, and SmOB write the cut. IdOB writes the packet.
- Examples are traces of the prohibition, not a second printing of the cards. Start with [examples/why_this_cut.md](examples/why_this_cut.md). `placeholder.md` remains a debugger stub.

The cards are usable alone for a log inspection. They are not sufficient alone for an architectural change. This note is prior reading for that change. It is not a sixth primitive.

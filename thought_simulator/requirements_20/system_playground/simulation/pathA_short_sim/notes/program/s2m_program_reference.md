# S2M Program Reference

**Date:** 2026-11-19  
**Branch:** s2m-seed-experiment  
**Purpose:** Concrete contracts for the two-part S2M realization: (I) accountability trail, (II) interpretive transfer to meaning.  
**Status:** Implementation contract for the experimental branch. Not a requirements change.  

## Intent
S2M is realized in two separable parts.

  * **Part I — Accountability trail**
    Establishes an inspectable record of what the floor wrote and what remains open. This is the seed
    already implemented. It does not yet claim interpreted meaning.

  * **Part II — Interpretive transfer to meaning**
    Exposes a bounded, extensible set of possible word associations, selects finite associations
    appropriate to the current utterance and active space, legitimates them, and writes the accepted
    relations against the accountability trail. The resulting composite is specific to the utterance.

A guiding observation for Part II is:

  **The word interpretation list is where meaning slips in.**

This does not mean that knowing the interpretation list for a word is equivalent to knowing the meaning of the sentence. The list exposes possible meaning relations. The complete utterance and active space constrain which possibilities participate in the finite composite for that occurrence. The composite identifies where meaning is represented in this S2M realization; it does not by itself claim that the system knows or understands the sentence's meaning.

Both parts run under python run_examples.py (enabled by default). Output is clearly labeled so each part can be found in a log file. Disable with --no-s2m-seed.

**Non-mutation rule**

Do not modify idob/sum.py, the core IdOB assignment that writes tp.idob, desks, or existing claim/connection writers. All new behavior is additive.

**CLI**
python run_examples.py                  # Part I + Part II enabled
python run_examples.py --no-s2m-seed    # both disabled
python run_examples.py > run.log        # pipeline to log; labels remain findable


The primitive that attaches both parts is IdOB.

## Part I — Accountability trail

**Output label (easily found in log)**
--- S2M Accountability (IdOB) ---

**Accounting output (tp.s2m_seed**
* utterance: raw sentence
* written_relations: relations the floor established
  Example:{"from": "sky", "relation": "is", "to": "blue", "source": "floor"}
* null_relations: explicit markers for relations left open
  Example:{"from": null, "relation": null, "to": null, "reason": "no_floor_source"}
* crossing_fields: reserved meaning slots, all null
 (structure_ids, structural_key, rank, meaning_semantics, cie_id, meaning_delta_h)
* seed_complete: true

**How it is used**

The accountability record is the inspectable starting point. Part II reads it and appends finite meaning relations beside it. It remains visible even if no interpretive selection is made.

**Example (The sky is blue.)**
1. --- S2M Accountability (IdOB) ---
2. s2m_seed: {
3. "utterance": "The sky is blue.",
4. "written_relations": [{"from": "sky", "relation": "is", "to": "blue", "source": "floor"}],
5. "null_relations": [{"from": null, "relation": null, "to": null, "reason": "no_floor_source"}],
6. "crossing_fields": {"structure_ids": null, "structural_key": null, "rank": null, "meaning_semantics": null, "cie_id": null, "meaning_delta_h": null},
7. "seed_complete": true
8. }

## Part II — Interpretive transfer to meaning

**Interpretation space**

Part II begins from possible associations rather than a single fixed meaning for each word. For the initial example, a rudimentary pool may include:

1. blue = {
2. sadness,
3. depression,
4. cold,
5. dying/dwindling,
6. pristine,
7. expansive,
8. clarity,
9. color,
10. primary color
11. }
12.
13. sky = {
14. openness,
15. higher,
16. no boundaries,
17. broadening,
18. free,
19. made of gas,
20. surrounds a planet,
21. generally seen from the ground and looking up
22. }


These lists are **candidate interpretation spaces**, not definitions of the words and not the meaning of the sentence.

Knowing the candidate list for blue or sky does not establish the meaning of "The sky is blue." The complete utterance constrains the available possibilities and selects a finite composite specific to that occurrence.

Conceptually:

word interpretation possibilities→utterance-constrained selection→finite meaning composite\text{word interpretation possibilities} \rightarrow \text{utterance-constrained selection} \rightarrow \text{finite meaning composite}

This is the boundary intended by the statement“the word interpretation list is where meaning slips in.”

**Major categories and subcategories**

Candidate associations are descriptively organized under a major category and subcategory.

|Major	|Example subcategories|
|---|---|
|Affective / experiential| emotional-tone, bodily-felt, mood, valence|
|Perceptual / sensory|	color, spatial-extent, visual-quality, sensory-modality|
|Physical / compositional|	material, structure, natural-kind, composition|
|Perspectival / situational|	viewpoint, typical-context, orientation, accessibility|
|Mental|	cognitive, attentional, conceptual, clarity|
|Spiritual|	transcendent, unbounded, sacred-associative, elevating|
|Social|	shared, collective, interpersonal, cultural-common|
|Metaphysical|	ontological-status, essence, categorical-being, ultimate-ground|

**Metaphysical** remains a major category in its own right.

Each association may be placed under one major and one subcategory. This organization is descriptive and extendable. Additional subcategories can be introduced without requiring changes to the major-category structure.

The taxonomy organizes possible interpretations; it does not assert that any candidate association is active for a particular utterance.

**Output label (easily found in log)**
--- S2M Meaning (IdOB) ---

**Meaning output (tp.s2m_meaning)**

* meaning_relations: finite, legitimized associations
  Example:{"from": "blue", "relation": "evokes", "to": "cold", "major": "affective", "legitimized": true}
* active_space: majors that were live for this selection
* story_id: identifier for the utterance-specific composite
* extendable: true

**How it is used**

Part II loads only the active majors from YAML, exposes candidate associations for the seed endpoints, proposes associations within the active space, legitimates them, and writes the accepted relations.

The result is appended to the accountability trail so both the structural starting point and the finite meaning composite remain inspectable.

The distinction is:

1. candidate associations != selected composite != claim of understanding


The candidate associations provide possible meaning relations. The utterance-specific selection produces the customized composite. Neither step alone is a claim that the system knows what the sentence means.

**Data files (YAML)**

* s2m/data/majors.yaml — open list of major classifications
* s2m/data/associations/<endpoint>.yaml — tagged candidate associations for each word
* s2m/data/spaces/default.yaml — active majors for the default space

New associations, subcategories, or majors are data extensions. The selection loop does not depend upon a fixed exhaustive inventory of possible interpretations.

**Example meaning record**

1. --- S2M Meaning (IdOB) ---
2. s2m_meaning: {
3.   "meaning_relations": [
4.       {"from": "blue", "relation": "evokes", "to": "cold", "major": "affective", "legitimized": true},
5.   from": "sky", "relation": "affords", "to": "openness", "major": "mental", "legitimized": true}
6.   ],
7.   "active_space": ["affective", "perceptual", "mental", "spiritual"],
8.   "story_id": "sky-blue-001",
9.   "extendable": true
10.   }


For this example, cold and openness are selected from larger spaces of possible associations. Their selection does not make those associations exhaustive definitions of blue or sky, nor does it assert that the resulting record amounts to knowing the meaning of "The sky is blue."

The record makes the finite, customized selection inspectable.

**Realized sentences (examples)**

1. "The sky is blue." → accountability writes sky–is–blue; the interpretation pool exposes multiple possible associations; the utterance-specific selection may write blue→cold and sky→openness.
2. "The book is on the table." → accountability writes book–is–on–table; meaning may add table→support, book→object.
3. "Where is the book?" → accountability writes query relation; meaning may add book→sought, location→unknown.

**Expandability**

* Add a major: extend majors.yaml.
* Add a subcategory: extend the relevant major classification.
* Add an association: add an entry in the endpoint YAML.
* Add a space: new file under spaces/.
* The select–legitimate–write loop and both output labels stay unchanged.
* Association inventories need not be exhaustive.
* The structure is one workable accounting organization, not claimed to be the only or optimal one. It     is sufficient to demonstrate the concept and can be refined or extended without breaking the
  accountability trail.
  
### First implementation slice for Part II

* YAML files for sky and blue with the rudimentary candidate associations.
* Major/subcategory tags sufficient to organize those associations.
* Loader, active-space, propose, legitimate, write, and record modules.
* Loop called from IdOB when the seed flag is on.
* Clear --- S2M Meaning (IdOB) --- block in run_examples.py output.

Until Part II is filled, only the Accountability block appears. Both blocks are labeled and pipeline cleanly to a log file.

**Traceability**

Linked from the short-sim README and from s2m_relational_proposal.md. The relational proposal carries the broader conceptual account; this page records the programming contract required to make that account executable.

All work remains on s2m-seed-experiment. main is the recovery point.

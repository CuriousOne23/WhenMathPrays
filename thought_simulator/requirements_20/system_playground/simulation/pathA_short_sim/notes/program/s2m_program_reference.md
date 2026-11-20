# S2M Program Reference

**Date:** 2026-11-20  
**Branch:** s2m-seed-experiment  
**Purpose:** Concrete implementation contract derived from the stable s2m_relational_proposal.md.  
**Status:** Implementation contract for the experimental branch. Not a requirements change.  
**Conceptual authority:** s2m_relational_proposal.md (five-stage model). Read both before coding.

For how to run the short simulator and correctly interpret normal `run_examples.py` output (including S2M layers and category observations), see [user_guide.md](../../user_guide.md).

## Intent

S2M realizes the five-stage model established in the relational proposal:

structural relation → default meaning → candidate interpretation space → selected interpretive extension(s) → finite customized composite

- **Structural relation** is the floor-established crossing (Part I accountability trail).
- **Default meaning** is the minimal semantic relation derived from that structure. It exists when no contextual or category-selection cue is active. It is not selected from a candidate inventory.
- **Candidate interpretation space** exposes available associations for relevant endpoints and relations, tagged by interpretation major and subcategory. Candidates remain unselected unless legitimately activated.
- **Selected interpretive extension(s)** are candidates written only when a cue is present and the relation is within the licensed region.
- **Finite customized composite** is the default meaning plus any legitimized extensions.

No cue means default meaning only. A cue may produce default meaning + legitimately selected extension(s).

A guiding observation remains:

**The word interpretation list is where meaning slips in.**

This does not mean that knowing the interpretation list for a word is equivalent to knowing the meaning of the sentence. The list exposes possible meaning relations. The complete utterance and active space constrain which possibilities participate in the finite composite for that occurrence. The composite identifies where meaning is represented in this S2M realization; it does not by itself claim that the system knows or understands the sentence's meaning.

Both the accountability trail and the interpretive layers run under `python run_examples.py` (enabled by default). Output is clearly labeled. Disable with `--no-s2m-seed`.

**Non-mutation rule**

Do not modify idob/sum.py, the core IdOB assignment that writes tp.idob, desks, or existing claim/connection writers. All new behavior is additive.

**CLI**

```text
python run_examples.py                  # enabled
python run_examples.py --no-s2m-seed    # disabled
python run_examples.py > run.log        # pipeline to log; labels remain findable
```

The primitive that attaches the S2M layers is IdOB.

## Part I — Accountability trail (structural relation)

**Output label (easily found in log)**

`--- S2M Accountability (IdOB) ---`

**Accounting output (`tp.s2m_seed`)**

* utterance: raw sentence
* written_relations: relations the floor established  
  Example: `{"from": "sky", "relation": "is", "to": "blue", "source": "floor"}`
* null_relations: explicit markers for relations left open  
  Example: `{"from": null, "relation": null, "to": null, "reason": "no_floor_source"}`
* crossing_fields: reserved meaning slots, all null  
  (structure_ids, structural_key, rank, meaning_semantics, cie_id, meaning_delta_h)
* seed_complete: true

**How it is used**

The accountability record is the inspectable structural starting point. Default meaning is derived from it. Candidate inventories and any later extensions are layered beside it. It remains visible even if no interpretive selection is made.

**Example (The sky is blue.)**

```text
--- S2M Accountability (IdOB) ---
s2m_seed: {
  "utterance": "The sky is blue.",
  "written_relations": [{"from": "sky", "relation": "is", "to": "blue", "source": "floor"}],
  "null_relations": [{"from": null, "relation": null, "to": null, "reason": "no_floor_source"}],
  "crossing_fields": {"structure_ids": null, "structural_key": null, "rank": null, "meaning_semantics": null, "cie_id": null, "meaning_delta_h": null},
  "seed_complete": true
}
```

## Default meaning

Default meaning is derived from the structural relation. Exact canonical relation vocabulary remains open (as left open in the proposal). The content must preserve the structural crossing.

No-cue behavior: emit the default meaning only. Candidate inventories are available but unselected. No associative extension is written.

## Part II — Candidate interpretation space and selected extensions

**Interpretation space**

Candidate inventories are associated with relevant endpoints and relations. They are not definitions and not the meaning of the sentence. They remain unselected until a cue legitimizes an extension.

Context stores (the six sources of activation) are distinct from interpretation majors (the taxonomy that tags candidates). Do not collapse the two.

**Interpretation majors and subcategories**

| Interpretation major | Example subcategories |
|---|---|
| Affective / experiential | emotional-tone, bodily-felt, mood, valence |
| Perceptual / sensory | color, spatial-extent, visual-quality, sensory-modality |
| Physical / compositional | material, structure, natural-kind, composition |
| Perspectival / situational | viewpoint, typical-context, orientation, accessibility |
| Mental | cognitive, attentional, conceptual, clarity |
| Spiritual | transcendent, unbounded, sacred-associative, elevating |
| Social | shared, collective, interpersonal, cultural-common |
| Metaphysical | ontological-status, essence, categorical-being, ultimate-ground |

**Output labels (easily found in log)**

- Accountability: `--- S2M Accountability (IdOB) ---`
- Default meaning + any extensions: `--- S2M Meaning (IdOB) ---`

**Meaning output (`tp.s2m_meaning`)**

* default_meaning: the structurally derived minimal relation (always present when seed is on)
* meaning_relations: finite legitimized extensions only (empty when no cue)
  Example (extension, cue required): `{"from": "blue", "relation": "evokes", "to": "cold", "major": "affective", "legitimized": true}`
* active_space: interpretation majors that were live for this selection (if any)
* story_id: identifier for the utterance-specific composite
* extendable: true

**How it is used**

When the seed flag is on:
1. Write the accountability trail (structural relation).
2. Derive and record the default meaning.
3. Expose candidate inventories (unselected).
4. If a cue is present, propose, measure deviation against the licensed region, legitimate or refuse, and write only accepted extensions.
5. The composite is the default plus any written extensions.

No cue produces default meaning only.

**Data files (YAML)**

* s2m/data/majors.yaml — open list of interpretation majors
* `s2m/data/associations/<endpoint>.yaml` — tagged candidate associations for each endpoint, where `<endpoint>` is the lowercase endpoint name (e.g., `sky.yaml`, `blue.yaml`, `book.yaml`)
* s2m/data/spaces/default.yaml — active majors for the default space

New associations, subcategories, or majors are data extensions. The selection loop does not depend upon a fixed exhaustive inventory.

## Canonical three-sentence testbench (derived from the proposal)

### A. “The sky is blue.”

- Structural relation: `sky — is — blue`
- Default meaning: the entity sky is characterized by the state/property blue (relation name open).
- Candidate inventory: sky (openness mental, higher perspectival, …); blue (sadness affective, cold affective, color perceptual, …).
- No-cue result: default meaning only. Candidates unselected.
- Possible extensions (cue required): sky → affords → openness; blue → evokes → cold. These are not baseline.

### B. “The book is on the table.”

- Structural relation: book — is — on — table (locative)
- Default meaning: the entity book is located on the entity table (relation name open).
- Candidate inventory: book (object physical, …); table (support physical, …); locative relation (placement perspectival, …).
- No-cue result: default locative meaning only.
- Possible extensions (cue required): table → provides → support; book → is → object. These are not baseline.

### C. “Where is the book?”

- Structural relation: query about the location of book
- Default meaning: a request/query for the location of the entity book; the requested locative continuation remains unresolved/potential.
- Candidate inventory: book (object physical); query structure (information-request mental, unresolved-location perspectival).
- No-cue result: default query meaning only. Locative continuation remains potential/null. No endpoint association selected as the meaning.
- Possible extensions: none required for the initial testbench. Semantic content arises from the query structure itself.

## Phase III — Realization Characterization

Phase III characterizes the realized S2M mechanism sufficiently that we know what instrument we actually have before using it observationally. The key question is: what have we actually built at the S→M crossing?

The three canonical sentences remain the sole normative testbench and implementation contract. Diagnostic utterances may be used only as observational probes into the current realization. They do not establish additional S2M requirements and do not create required semantic outputs. A diagnostic probe may behave unexpectedly without automatically constituting an implementation failure.

Characterization should help expose, where possible:
- what is derived from structural relations;
- what constitutes default meaning;
- what is supplied by candidate interpretation data;
- what is generalized structural behavior;
- what is implementation scaffolding;
- what remains unresolved or deliberately open;
- what is deterministic and replayable;
- what remains invariant when candidate or contextual data changes.

Phase III observations characterize the current realization. They do not independently modify the S2M architecture, program contract, requirements, or theory. If characterization exposes something important, it becomes a subject for review rather than silently becoming a new requirement.

## Phase IV — Category Structure Observation

Phase IV uses the characterized S2M realization to observe the structure, provenance, propagation, and effect of category information across the S→M bridge. It prepares an observational basis for the eventual functional realization of category selection without implementing or redefining that feature. It does not duplicate or replace [category_selection_proposal.md](category_selection_proposal.md). The functional category-selection architecture, scoring behavior, ownership, TP fields, and other normative details continue to come from that proposal and its associated requirements. Consistent with the five-stage model established in [s2m_relational_proposal.md](s2m_relational_proposal.md).

Observational windows include:
1. **No-cue baseline** — structural relation, default meaning, unselected candidates, absence of cue and selected extensions (the control condition).
2. **Cue provenance** — visibility of where category information came from (sentence-internal, prior-context/CEx, or no usable cue).
3. **Pre-selection candidate state** — distinguish candidate absent, available but unselected, eligible, rejected/refused, or ultimately selected and legitimized.
4. **Category evidence and decision** — what evidence was present, which interpretation majors received support, what remained unsupported, whether ambiguity existed, and how any decision was reached (scoring fields, when realized, come from their requirements).
5. **Selection versus legitimation** — category influence making a candidate relevant is distinct from S2M legitimizing it as an extension. Path: category influence → candidate proposal/selection → licensed-region test → legitimation/refusal → extension or null.
6. **Default-versus-selected comparison** — preserve the default so the effect of category influence can be observed (unchanged default, newly selected extensions, unselected/refused candidates, changed active space, final composite).
7. **Null, refusal, ambiguity, and non-selection** — informative cases include no cue, ambiguous evidence, candidate unavailable, available but unselected, proposed but refused, extension remaining null, or clarification required.
8. **Cue-path comparison** — sentence-internal versus prior-conversation/context (CEx/CIL) paths may be compared while retaining different provenance; they need not be internally identical.
9. **Determinism and replay** — given the same input, structural result, context, cue, candidate inventory, and applicable scoring/configuration state, category-related observations are reproducible.

**Epistemic boundary:** An observation characterizes behavior of the current realization. It does not independently establish a new requirement, semantic truth, or architectural claim. An observation may motivate a later hypothesis, proposal, or requirement change, but does not independently authorize one. The intended flow is: characterized realization → controlled observation → recorded finding → possible hypothesis → review → possible future architectural change.

Phase III asks what instrument was actually built. Phase IV asks what can be observed specifically about category structure through that instrument.

## Expandability

* Add a major: extend majors.yaml.
* Add a subcategory: extend the relevant major classification.
* Add an association: add an entry in the endpoint YAML.
* Add a space: new file under spaces/.
* The select–legitimate–write loop and both output labels stay unchanged.
* Association inventories need not be exhaustive.
* The structure is one workable accounting organization, not claimed to be the only or optimal one. It is sufficient to demonstrate the concept and can be refined or extended without breaking the accountability trail or the default-meaning layer.

### First implementation slice

* YAML files for the relevant endpoints with the rudimentary candidate associations listed in the testbench.
* Major/subcategory tags sufficient to organize those associations.
* Loader, active-space, propose, legitimate, write, and record modules that respect the no-cue = default-only rule.
* Loop called from IdOB when the seed flag is on.
* Clear labeled blocks in run_examples.py output for accountability and for meaning (default + extensions).

Until the interpretive layers are filled, the accountability block and the default-meaning record appear. Both blocks are labeled and pipeline cleanly to a log file.

## Traceability

Linked from the short-sim README and from s2m_relational_proposal.md. The relational proposal is the conceptual authority; this page records the programming contract required to make that account executable without reinterpretation.

All work remains on s2m-seed-experiment. main is the recovery point.

## Commentary of S2M

For commentary on S2M see [observations_of_s2m.md](../observations_of_s2m.md).

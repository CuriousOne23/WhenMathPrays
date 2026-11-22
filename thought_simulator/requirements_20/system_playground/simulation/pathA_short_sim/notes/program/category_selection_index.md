# Category Selection Document Family Index

**Document:** notes/program/category_selection_index.md  
**Status:** Navigation/governance index (non-normative).  
**Purpose:** Decide which category-selection document(s) to open for a specific question.

## How to use this index

Use this page to route questions by document role and authority.

- Open **normative requirements** for authoritative behavior/ownership/path rules.
- Open **program/research/reference docs** for category-selection design, implementation scope, and characterization method.
- Open **observation docs** for empirical records and experiment outcomes.

This index is intentionally brief and does not duplicate technical detail from the linked documents.

## Governance rule

This is the authoritative navigation index for the category-selection document family.

Each family document should declare:

- what it is (role),
- authority/status,
- when it should be consulted,
- direct dependencies/successors.

New category-selection/characterization documents should be registered here.

## Finding-routing rule

Route findings by information type and document authority:

- Characterization-method or verification lessons → [category_selection_characterization_reference.md](category_selection_characterization_reference.md)
- Empirical category-selection findings → [category_selection_observation.md](category_selection_observation.md)
- New research questions or proposed investigations → [category_selection_research_plan.md](category_selection_research_plan.md)
- Durable realization/software contract conclusions → applicable program reference (for example [category_selection_program_reference.md](category_selection_program_reference.md))

Record each finding in the document that owns that information type. Do not duplicate the same finding across the family merely for convenience.

## Document family by role

### Architectural proposal

- [category_selection_proposal.md](category_selection_proposal.md)  
  **What it is:** Category-selection architecture proposal.  
  **Status/authority:** Draft/discussion design context (non-normative).  
  **Open when:** You need architectural intent, boundaries, and category-selection path framing.  
  **Relationship:** Conceptual predecessor to research/reference docs; aligned with S2M context and normative requirements.

### Research

- [category_selection_research_plan.md](category_selection_research_plan.md)  
  **What it is:** Research/experimental plan for the current cycle.  
  **Status/authority:** Non-normative research discipline.  
  **Open when:** You need characterization questions, experimental principles, or confidence/closeout criteria.  
  **Relationship:** Successor to prior observation cycle; upstream of implementation and observation recording.

### Current-realization mapping

- [category_selection_stage1_modification_map.md](category_selection_stage1_modification_map.md)  
  **What it is:** Stage-1 factual map of current software realization.  
  **Status/authority:** Non-normative implementation evidence map.  
  **Open when:** You need current code-path touchpoints, boundaries, or “what exists now” before edits.  
  **Relationship:** Bridge from research plan to software-reference contracts.

### Software references

- [category_selection_program_reference.md](category_selection_program_reference.md)  
  **What it is:** Bounded software-realization contract for category selection.  
  **Status/authority:** Draft implementation contract (realization-side).  
  **Open when:** You are implementing/reviewing category-selection mechanism behavior and realization outputs.  
  **Relationship:** Coordinated sibling of characterization reference; realization path only.

- [category_selection_characterization_reference.md](category_selection_characterization_reference.md)  
  **What it is:** Bounded software-reference contract for characterization infrastructure.  
  **Status/authority:** Draft implementation contract (characterization-side).  
  **Open when:** You are implementing/reviewing characterization invocation, dispatch, sessions, or artifact discipline.  
  **Relationship:** Coordinated sibling of program reference; observes/exercises realization, does not define meaning policy.

### Observation

- [category_selection_observation.md](category_selection_observation.md)  
  **What it is:** Category-selection empirical observation record (currently placeholder).  
  **Status/authority:** Observation document; no results recorded yet.  
  **Open when:** You need recorded category-selection experiment outcomes and observational interpretations.  
  **Relationship:** Receives evidence from characterization runs/artifacts.

### Historical predecessor

- [category_structure_observation.md](category_structure_observation.md)  
  **What it is:** Completed prior observational cycle.  
  **Status/authority:** Historical observational record (non-normative).  
  **Open when:** You need prior-cycle findings that motivated the current category-selection program.  
  **Relationship:** Predecessor context for the current research plan.

### Related S2M authority/context

- [s2m_relational_proposal.md](s2m_relational_proposal.md)  
  **What it is:** Conceptual S2M model proposal.  
  **Status/authority:** Conceptual authority/context (non-normative requirements).  
  **Open when:** You need S2M conceptual terms/stage boundaries used by category-selection docs.  
  **Relationship:** Conceptual context for category-selection architecture framing.

- [s2m_program_reference.md](s2m_program_reference.md)  
  **What it is:** S2M implementation contract/context.  
  **Status/authority:** Program reference for S2M realization boundaries.  
  **Open when:** You need S2M execution/contract context that category-selection work must respect.  
  **Relationship:** Program-context companion to the S2M relational proposal.

### Normative requirements

- [20.45_ts_isc_scoring.md](../../../20.45_ts_isc_scoring.md)  
  **Authority:** Normative ISc scoring behavior.  
  **Open when:** Question is about category-result scoring behavior/rules.  
  **Relationship:** Scoring authority used by category-selection realization.

- [20.105_tp_requirements.md](../../../20.105_tp_requirements.md)  
  **Authority:** Normative TP behavior/ownership.  
  **Open when:** Question is about TP envelope behavior, ownership, or commit boundaries.  
  **Relationship:** Defines TP behavioral constraints category-selection must follow.

- [20.116.010_tp_envelope_index.md](../../../20.116.010_tp_envelope_index.md)  
  **Authority:** Normative canonical TP path/index + root writer ownership.  
  **Open when:** Question is about canonical path spelling or root-writer authority.  
  **Relationship:** Path/index authority complementary to 20.105 behavior authority.

- [20.40.050_idob_prim.md](../../../20.40.050_idob_prim.md)  
  **Authority:** Normative IdOB behavior.  
  **Open when:** Question is about IdOB-side behavior and constraints.  
  **Relationship:** IdOB behavior authority used by downstream consumption boundaries.

## Conceptual progression (consult sequence)

Typical progression for a new cycle:

`category_selection_proposal.md`  
→ `category_selection_research_plan.md`  
→ `category_selection_stage1_modification_map.md`  
→ coordinated software references  
(`category_selection_program_reference.md` + `category_selection_characterization_reference.md`)  
→ implementation and characterization runs  
→ `category_selection_observation.md`

At any step, open normative requirements for authoritative behavior/path/ownership questions.

## Extensibility

This family is extensible. Register new category-selection/characterization documents here with role, status, consult trigger, and dependency relationships.

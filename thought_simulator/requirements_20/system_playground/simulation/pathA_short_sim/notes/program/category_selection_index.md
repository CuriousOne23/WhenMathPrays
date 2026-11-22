# Category Selection Document Family Index

**Document:** notes/program/category_selection_index.md  
**Status:** Navigation/governance index. Non-normative. Not an implementation contract. Not an experimental result.  
**Purpose:** Canonical navigation and document-governance index for the evolving category-selection document family.

Category-selection research is expected to evolve as characterization exposes new questions. This index organizes the current/planned documents by role and supports controlled growth of the document family.

## Governance rule

This index is the authoritative navigation document for the category-selection document family.

Individual category-selection documents should link here for the complete document family.  
Individual documents should directly link only to immediate authorities, dependencies, predecessors, successors, or other documents required to understand that document’s specific role.

Future category-selection documents should declare:

- document role
- status/authority
- purpose
- direct dependencies
- expected outputs or successors
- relationship to the category-selection document family

New characterization documents should be registered in this index rather than requiring broad cross-link updates throughout the document family.

## Document family by role

### Architectural proposal

- [category_selection_proposal.md](category_selection_proposal.md)  
  **Role:** Defines architectural intent, boundaries, category-selection path, and relationship to S2M.

### Research

- [category_selection_research_plan.md](category_selection_research_plan.md)  
  **Role:** Defines research questions, experimental principles, confidence dimensions, architectural-generality investigation, category-support/unsupported-space characterization, and closeout discipline.

### Current-realization mapping

- [category_selection_stage1_modification_map.md](category_selection_stage1_modification_map.md)  
  **Role:** Factual Stage-1 map of current short-simulator implementation, current scaffolding, data/procedure boundaries, observability, provenance, and potential later modification locations.

### Software references

- [category_selection_program_reference.md](category_selection_program_reference.md)  
  **Role:** Software contract for the bounded category-selection realization itself.  
  **Current status:** Placeholder pending expansion after Stage-1 review.

- [category_selection_characterization_reference.md](category_selection_characterization_reference.md)  
  **Role:** Software contract for category-selection characterization infrastructure and experimentation support.  
  **Expected later coverage:** run_examples.py integration, parameterized characterization CLI, characterization-type dispatch, characterization modularity, independent artifacts, non-destructive/session-aware output, common TS characterization artifact extension, .gitignore handling, user_guide.md integration, observability/measurement support, and support for future observation-driven characterization types.  
  **Boundary:** It does not define the final no-category decision function.

### Observation

- [category_selection_observation.md](category_selection_observation.md)  
  **Role:** Future empirical record populated from actual category-selection and characterization runs.

### Historical predecessor

- [category_structure_observation.md](category_structure_observation.md)  
  **Role:** Completed preceding observational cycle that motivated the next category-selection research program.

### Related S2M authority/context

- [s2m_relational_proposal.md](s2m_relational_proposal.md)  
  **Role:** Conceptual S2M model authority/context for relationship boundaries and terminology.
- [s2m_program_reference.md](s2m_program_reference.md)  
  **Role:** Program/realization contract context for S2M execution boundaries and phase framing.

### Normative requirements

- [20.45_ts_isc_scoring.md](../../../20.45_ts_isc_scoring.md) — normative ISc scoring requirements and category-result scoring authority.
- [20.105_tp_requirements.md](../../../20.105_tp_requirements.md) — normative TP behavior/ownership requirements.
- [20.116.010_tp_envelope_index.md](../../../20.116.010_tp_envelope_index.md) — canonical TP envelope/index and writer-path authority.
- [20.40.050_idob_prim.md](../../../20.40.050_idob_prim.md) — normative IdOB behavior authority.

## High-level document flow

Current flow (conceptual):

category_selection_proposal.md  
        ↓  
category_selection_research_plan.md  
        ↓  
category_selection_stage1_modification_map.md  
        ↓  
coordinated software references:  
    category_selection_program_reference.md  
    category_selection_characterization_reference.md  
        ↓  
reviewed implementation  
        ↓  
characterization sessions / campaigns  
        ↓  
generated characterization artifacts  
        ↓  
category_selection_observation.md  
        ↓  
confidence / closeout review  
        ↓  
observation determines the next research/design question

The two software references are coordinated siblings with different responsibilities: one for the bounded category-selection realization itself, one for characterization infrastructure that observes/exercises that realization.

## Scalability and extensibility

This document family is intentionally extensible.

Future characterization may expose unforeseen questions requiring additional characterization programs or associated documents. This index is the registration point for those additions so growth remains organized and reviewable.

Additions registered here do not change the authority/status of existing completed research or observation documents.

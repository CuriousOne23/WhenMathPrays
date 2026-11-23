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
- Stage 1 readiness / capability map → [category_selection_characterization_readiness_audit.md](category_selection_characterization_readiness_audit.md)
- Stage 2 axis and coverage decisions → [category_selection_stage2_axis_and_coverage_reference.md](category_selection_stage2_axis_and_coverage_reference.md)
- Controlled experimental palette design → [category_selection_controlled_palette_v1.md](category_selection_controlled_palette_v1.md)
- Stage 7 formal campaign specification → [category_selection_stage7_batch1_4a_campaign.md](category_selection_stage7_batch1_4a_campaign.md)
- Palette v1 characterization closeout → [category_selection_characterization_palette_v1_closeout.md](category_selection_characterization_palette_v1_closeout.md)
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

- [category_selection_characterization_readiness_audit.md](category_selection_characterization_readiness_audit.md)  
  **What it is:** Factual Stage 1 capability map of the current realization (probe, control, measurement, and controlled-evolution readiness).  
  **Status/authority:** Non-normative inspection evidence.  
  **Open when:** You need the Stage 1 readiness verdict, the local source-support axis, or measurement qualification before formalizing experimental axes.  
  **Relationship:** Downstream of the research plan (8A/8B/13); owns the capability map; upstream of Stage 2 axis formalization.

- [category_selection_stage2_axis_and_coverage_reference.md](category_selection_stage2_axis_and_coverage_reference.md)  
  **What it is:** Stage 2 research-design record of candidate dimensions, classifications, minimum meaningful coverage, palette requirements, and coverage-gap conclusion.  
  **Status/authority:** Non-normative research-design record.  
  **Open when:** You need the minimum coverage set or the rationale for what the Stage 4 palette must express.  
  **Relationship:** Downstream of the readiness audit; upstream of Stage 4 palette construction; does not own empirical observations.

- [category_selection_controlled_palette_v1.md](category_selection_controlled_palette_v1.md)  
  **What it is:** Design record for the first-generation controlled experimental palette (canonical probes, source-composition contract, construction families, controls, and competition cases).  
  **Status/authority:** Implemented, configuration-verified, and locally calibrated (Stage 6 PASS); not yet formally characterized.  
  **Open when:** You need the approved Palette v1 specification or the distinction between design and current implementation state.  
  **Relationship:** Downstream of Stage 2; upstream of Stage 7 formal campaign; does not own empirical observations.

- [category_selection_stage7_batch1_4a_campaign.md](category_selection_stage7_batch1_4a_campaign.md)  
  **What it is:** Frozen Stage 7 formal characterization campaign specification (Batches 1–4A execution matrix, stop conditions, measurement limits, and batch-by-batch authorization rule).  
  **Status/authority:** Non-normative campaign specification. Batches 1–4A accepted. Batch 4B and inventory composition deferred.  
  **Open when:** You need the exact cases, stop conditions, or authorization status for the first formal Palette v1 characterization campaign.  
  **Relationship:** Downstream of Palette v1 and Stage 2; upstream of formal Agent execution and observation recording; does not own empirical results.

- [category_selection_characterization_palette_v1_closeout.md](category_selection_characterization_palette_v1_closeout.md)  
  **What it is:** Campaign-level structural-confidence closeout after accepted Stage 7 Batches 1–4A. Records Section 13 decision B and the progression statement for continued downstream TS development.  
  **Status/authority:** Non-normative closeout record.  
  **Open when:** You need the structural-confidence conclusion, deferred-work list, or return conditions for Category Selection after Palette v1 characterization.  
  **Relationship:** Downstream of the Stage 7 campaign and observation record; owns the progression decision; does not alter historical experimental records.

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

### Milestone closeout

- [category_selection_characterization_milestone1_closeout.md](category_selection_characterization_milestone1_closeout.md)  
  **What it is:** Verification/closeout record for Characterization Infrastructure Milestone 1.  
  **Status/authority:** Non-normative implementation evidence and milestone closeout.  
  **Open when:** You need to determine what characterization infrastructure was actually implemented and verified at Milestone 1.  
  **Relationship:** Downstream of the characterization/program references and upstream of substantive category-selection characterization experiments.

### Experiment execution control

- [category_selection_characterization_experiment_plan.md](category_selection_characterization_experiment_plan.md)  
  **What it is:** Controlled execution plan for characterization experiments with mandatory per-experiment review gates.  
  **Status/authority:** Non-normative campaign-execution control document.  
  **Open when:** You need to run characterization experiments sequentially without auto-advancing across experiment boundaries.  
  **Relationship:** Downstream of Milestone-1 closeout and upstream of experiment execution artifacts and observation reporting.

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
→ `category_selection_characterization_readiness_audit.md`  
→ `category_selection_stage2_axis_and_coverage_reference.md`  
→ `category_selection_controlled_palette_v1.md`  
→ `category_selection_stage7_batch1_4a_campaign.md`  
→ `category_selection_characterization_palette_v1_closeout.md`  
→ `category_selection_stage1_modification_map.md`  
→ coordinated software references  
(`category_selection_program_reference.md` + `category_selection_characterization_reference.md`)  
→ Milestone-1 characterization implementation  
→ `category_selection_characterization_milestone1_closeout.md`  
→ `category_selection_characterization_experiment_plan.md`  
→ characterization runs  
→ `category_selection_observation.md`

At any step, open normative requirements for authoritative behavior/path/ownership questions.

## Extensibility

This family is extensible. Register new category-selection/characterization documents here with role, status, consult trigger, and dependency relationships.

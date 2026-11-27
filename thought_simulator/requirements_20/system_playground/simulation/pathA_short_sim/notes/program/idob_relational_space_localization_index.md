# IdOB Relational-Space Localization Index

**Document:** notes/program/idob_relational_space_localization_index.md  
**Status:** Navigation/continuity index (non-normative).  
**Purpose:** Entry point for the IdOB Relational-Space Organization for Tractable Path A Selection research track.

## What this track studies

Whether a replaceable organizational/index layer over stable IdOB relational identities can help Path A identify a tractable active relational surface, without treating organizational selection as meaning.

## Why this track exists

The previous S2M IdOB traversal characterization cycle is closed at its present-realization boundary.  
This new track targets the next bounded question: organizational tractability leverage under explicit gate discipline.

For prior closed-cycle dependencies only, navigate via [s2m_index.md](s2m_index.md).

General engineering-method guidance reference: [20.740_ts_realization_qualification_guidance.md](../../../../../20.740_ts_realization_qualification_guidance.md).

## Primary authority

Frozen track authority: [idob_relational_space_localization_research_plan.md](idob_relational_space_localization_research_plan.md)

## Current research status

- Previous S2M IdOB traversal characterization cycle: **CLOSED** (present-realization boundary).
- This track: **ACTIVE**.
- Research skeleton: **FROZEN**.
- Gate A / Phase 3 executed: **YES**.
- Gate A classification: **CONTINUE**.
- Gate B research design: **FROZEN**.
- Gate B mechanical design: **FROZEN**.
- Gate B execution: **YES**.
- Gate B classification: **NEGATIVE** (fixture-relative / provisional-HOW-relative).
- Gate B human review state: **APPROVED**.
- Gate B observations: **RECORDED**.
- Gate B closeout interpretation/status record: **RECORDED**.
- Information/Representation Sufficiency proposal: **AUTHORIZED**.
- Information/Representation Sufficiency mechanical-design development: **AUTHORIZED**.
- Information/Representation Sufficiency pre-execution review: **REQUIRED**.
- Information/Representation Sufficiency implementation: **NOT AUTHORIZED**.
- Information/Representation Sufficiency execution: **NOT AUTHORIZED**.
- Production selector research authorized: **NO**.
- Category integration authorized: **NO**.
- Final YAML/IdOB representation design authorized: **NO**.
- HOW-2: **NOT AUTHORIZED**.
- Gate C: **NOT AUTHORIZED**.

## Gate navigation (summary only)

- **Gate A:** organizational leverage under oracle/surrogate localization information. Status: CONTINUE (bounded fixture-relative / oracle-relative).
- **Gate B:** one provisional non-oracle localization HOW. Executed; mechanical classification NEGATIVE; human review APPROVED. Stopping rule: no HOW-2 in this cycle.
- **Gate C:** structural-health / representation qualification of what Gate B actually produces. Not authorized.
- **Next cycle:** information/representation sufficiency characterization at proposal/design stage only (no implementation/execution authorization).

## Current next step

Conduct pre-execution design review for the Information/Representation Sufficiency characterization proposal and mechanical design.  
Do not proceed automatically into implementation/execution, Gate C, HOW-2, production selector work, or Category/YAML integration.

## Not yet authorized

- Gate C qualification work;
- HOW-2 / retuned provisional selector within this cycle;
- production selector work;
- Category integration work;
- final YAML/IdOB representation design.

## Document registry

- [idob_relational_space_localization_index.md](idob_relational_space_localization_index.md)  
  **Role:** navigation / continuity / track status.

- [idob_relational_space_localization_research_plan.md](idob_relational_space_localization_research_plan.md)  
  **Role:** frozen research proposition, three-gate skeleton, Phase 3 fixture specification, Gate B provisional HOW design, anti-treadmill rules, and present-realization closeout boundary.

- [idob_relational_space_localization_gate_b_design.md](idob_relational_space_localization_gate_b_design.md)  
  **Role:** Mechanical characterization design for the frozen Gate B provisional non-oracle localization HOW.

- [idob_relational_space_localization_observation.md](idob_relational_space_localization_observation.md)  
  **Role:** executed Gate A / Phase 3 characterization evidence, measured observations, and Gate A mechanical classification.

- [idob_relational_space_localization_gate_b_observation.md](idob_relational_space_localization_gate_b_observation.md)  
  **Role:** executed Gate B characterization evidence, measured observations, and Gate B mechanical classification (NEGATIVE).

- [idob_relational_space_localization_gate_b_closeout.md](idob_relational_space_localization_gate_b_closeout.md)  
  **Role:** Gate B human-review disposition (APPROVED), bounded Gate A+Gate B interpretation, stopping boundaries, and next-cycle authorization boundary.

- [idob_relational_space_localization_information_representation_sufficiency_proposal.md](idob_relational_space_localization_information_representation_sufficiency_proposal.md)  
  **Role:** frozen research question and authorization boundary for the Information/Representation Sufficiency characterization cycle.

- [idob_relational_space_localization_information_representation_sufficiency_design.md](idob_relational_space_localization_information_representation_sufficiency_design.md)  
  **Role:** mechanical characterization design for representation ladder, decoder neutrality, and per-level outcome classifications (documentation/design-stage only).

## Characterization program

- [support/tools/idob_relational_space_localization_phase3_characterization.py](../../support/tools/idob_relational_space_localization_phase3_characterization.py)  
  **What it is:** Gate A / Phase 3 characterization executable for this track. Builds the frozen fixture-relative, oracle-only characterization, writes JSON under `local_characterization/sessions/idob_relational_space_localization_phase3/runs/`, and prints the Gate A classification. It does not claim a production Path A selector or that Path A possesses oracle information.  
  **Open when:** You need the executable that produced the Gate A / Phase 3 evidence.  
  **Relationship:** The observation record is [idob_relational_space_localization_observation.md](idob_relational_space_localization_observation.md).

- [support/tools/idob_relational_space_localization_gate_b_characterization.py](../../support/tools/idob_relational_space_localization_gate_b_characterization.py)  
  **What it is:** Gate B characterization executable for this track. Reuses Gate A fixture construction, applies the frozen provisional non-oracle HOW and q-schedule, writes JSON under `local_characterization/sessions/idob_relational_space_localization_gate_b/runs/`, and prints the Gate B classification. It does not claim a production Path A selector or that Path A can generate `X_base`.  
  **Open when:** You need the executable that produced the Gate B evidence.  
  **Relationship:** The observation record is [idob_relational_space_localization_gate_b_observation.md](idob_relational_space_localization_gate_b_observation.md).

Future observation/realization/characterization/closeout documents should be registered here only when they are actually created.

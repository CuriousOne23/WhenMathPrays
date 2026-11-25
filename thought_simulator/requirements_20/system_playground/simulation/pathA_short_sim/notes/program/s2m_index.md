# S2M Document Family Index

**Document:** notes/program/s2m_index.md  
**Status:** Navigation/governance index (non-normative).  
**Purpose:** Decide which S2M document(s) to open for a specific question. Distinct from the Category Selection index.

## How to use this index

Use this page to route S2M questions by document role and authority.

- Open **normative requirements** for authoritative behavior/ownership/path rules.
- Open **research proposals** for conceptual models that have not yet been frozen as architecture.
- Open **program references** for realization contracts once they exist.
- Open **observation and characterization docs** for empirical records.

This index is intentionally brief and does not duplicate technical detail from the linked documents.

## Governance rule

This is the authoritative navigation index for the S2M document family.

Each family document should declare:

- what it is (role),
- authority/status,
- when it should be consulted,
- direct dependencies/successors.

New S2M documents should be registered here. Category Selection characterization remains under `category_selection_index.md`.

## Document family by role

### Conceptual / research proposals

- [s2m_relational_proposal.md](s2m_relational_proposal.md)  
  **What it is:** Conceptual S2M model proposal (five stages, default meaning, working formulation of meaning as contextually resolved relational structure).  
  **Status/authority:** Research proposal (non-normative).  
  **Open when:** You need the prior conceptual framing of S2M stages and the working formulation of meaning.  
  **Relationship:** Predecessor conceptual context; refined but not erased by the IdOB traversal proposal.

- [s2m_idob_traversal_proposal.md](s2m_idob_traversal_proposal.md)  
  **What it is:** Research proposal defining bounded mechanical traversal of predefined IdOB relational space. Records the provisional chain from stabilized structure through door, legal candidates, correspondence, ledger, directional/qualifier summary, provisional discrimination policy, relative-support distribution, and directional entropy.  
  **Status/authority:** Research proposal (non-normative).  
  **Open when:** You need the current mechanical model of IdOB traversal, the bounded responsibility of Path A, the anti-fabrication principles, or the list of open joints.  
  **Relationship:** Immediate research authority for traversal questions. Refines the relational proposal; does not replace its five-stage distinctions.

### Program / realization

- [s2m_program_reference.md](s2m_program_reference.md)  
  **What it is:** Existing S2M implementation contract/context (pre-traversal).  
  **Status/authority:** Program reference for prior S2M realization boundaries.  
  **Open when:** You need the earlier execution/contract context.  
  **Relationship:** Companion to the relational proposal.

- [s2m_idob_traversal_program_reference.md](s2m_idob_traversal_program_reference.md)  
  **What it is:** Implementation-facing mapping of the traversal proposal onto currently realized code/config/data surfaces, including explicit blocked/unavailable stages.  
  **Status/authority:** Traversal realization mapping contract (non-normative, implementation-facing).  
  **Open when:** You need to know what traversal stages are directly realizable, derivable, observability-gapped, or architecture-blocked in current software.
  **Relationship:** Derived from traversal proposal and bounded by 20-series requirements.

- [s2m_idob_traversal_experiment_plan.md](s2m_idob_traversal_experiment_plan.md)  
  **What it is:** Frozen bounded experiment design for challenging the traversal proposal against current realization without semantic-policy change.  
  **Status/authority:** Execution-control plan for traversal experiments.  
  **Open when:** You need the authorized case matrix, stop conditions, and replay verification protocol for traversal observation runs.
  **Relationship:** Executes against the traversal program reference; predecessor to traversal observation records.

- [s2m_idob_traversal_correspondence_contract.md](s2m_idob_traversal_correspondence_contract.md)  
  **What it is:** Bounded research/design contract defining minimum representational requirements for evidence-to-candidate correspondence and evidence-family provenance/dependency.  
  **Status/authority:** Research/design contract for the next traversal joint (non-normative).  
  **Open when:** You need the representation contract and implementation-decision classification for correspondence/dependency surfaces.
  **Relationship:** Follows boundary characterization results; predecessor to correspondence representability planning.

### Observation / experiment record

- [s2m_idob_traversal_observation.md](s2m_idob_traversal_observation.md)  
  **What it is:** Executed facts and bounded interpretation from the frozen traversal experiment plan, including unavailable quantities and anomalies.  
  **Status/authority:** Empirical observation record (non-normative).  
  **Open when:** You need run evidence, case-by-case outputs, replay status, and explicit not-established claims for traversal stages.
  **Relationship:** Downstream of the traversal experiment plan; does not define architecture.

- [s2m_idob_traversal_correspondence_experiment_plan.md](s2m_idob_traversal_correspondence_experiment_plan.md)  
  **What it is:** Follow-on bounded plan for testing representability of correspondence/provenance/dependency surfaces only.  
  **Status/authority:** Frozen execution plan for correspondence representability checks.  
  **Open when:** You need planned correspondence representability cases and execution gating conditions.
  **Relationship:** Downstream of the correspondence contract; upstream of correspondence observation records.

- [s2m_idob_traversal_correspondence_observation.md](s2m_idob_traversal_correspondence_observation.md)  
  **What it is:** Executed facts for bounded correspondence/lineage representability, including Unknown/Unresolved/Unavailable outcomes and replay status.  
  **Status/authority:** Empirical observation record (non-normative).  
  **Open when:** You need case-level correspondence/dependency evidence and bounded interpretation for the correspondence joint.  
  **Relationship:** Downstream of the correspondence experiment plan; does not define traversal architecture.

### Related

- Category Selection family remains under [category_selection_index.md](category_selection_index.md). Category evidence may participate in traversal correspondence once an explicit relation is declared; it is not itself the traversal mechanism.
- Normative Path A / IdOB / ISc requirements remain in the 20-series documents.

## Conceptual progression (consult sequence)

For traversal questions:

Current traversal progression:

`s2m_idob_traversal_proposal.md`  
→ `s2m_idob_traversal_program_reference.md`  
→ `s2m_idob_traversal_experiment_plan.md`  
→ `s2m_idob_traversal_observation.md`

Next bounded traversal joint (post-boundary characterization):

`s2m_idob_traversal_correspondence_contract.md`  
→ `s2m_idob_traversal_correspondence_experiment_plan.md`  
→ `s2m_idob_traversal_correspondence_observation.md`

Optional predecessor conceptual context (not a downstream traversal stage):

`s2m_relational_proposal.md`  

Then, as needed:

→ normative requirements (20.705, 20.45, 20.40.050)  
→ Category Selection index for cue characterization

## Extensibility

This family is extensible. Register new S2M research, program, or experiment documents here. Do not absorb Category Selection empirical records.

# Scalability Document Family Index

**Document:** notes/program/scalability/scalability_index.md  
**Status:** Navigation/governance index (non-normative).  
**Purpose:** Decide which scalability document(s) to open for a specific question. Scalability is a Path A / S2M program; Category Selection is one affected subsystem.

## How to use this index

Use this page to route questions by document role and authority.

- Open the program document for governing principles, expansion definition, regression versus progression, and decision states.
- Open the design document for the scalability software/reference design boundaries and analysis model.
- Open the gap analysis for current reuse/adapt/gap/deferred classification by capability area.
- Open the implementation plan for the bounded implementation envelope and acceptance-test scope.
- Open the implementation mapping to see the proposed first-pass module/test/output mapping awaiting approval.
- Open the user guide for practical operator or Agent steps once implementation-backed workflow guidance is completed.

This index is intentionally brief and does not duplicate technical detail from the linked documents.

## Governance rule

This is the authoritative navigation index for the scalability document family.

Each family document should declare:
- what it is (role),
- authority/status,
- when it should be consulted,
- direct dependencies/successors.

New scalability documents should be registered here.

## Document family by role

### Program authority

- [scalability_program.md](scalability_program.md)  
  **What it is:** Governing proposal for Path A scalability and expansion-assurance.  
  **Status/authority:** Proposal (non-normative).  
  **Open when:** You need the definition of expansion, the regression/progression distinction, progression decisions, output discipline, or the phased plan.  
  **Relationship:** Receives the handoff from the Category Selection characterization program closeout; owns the Path A scalability concern; does not implement tooling.

### Gap/disposition mapping

- [scalability_gap_analysis.md](scalability_gap_analysis.md)  
  **What it is:** Audit-derived capability/disposition map for reuse, adaptation, gaps, unresolved items, and deferred concerns.  
  **Status/authority:** Analysis record (non-normative, decision-support).  
  **Open when:** You need to determine current capability classification by area, including deferred preconversation/context scaling.  
  **Relationship:** Downstream of the program document and completed infrastructure audit; informs later design planning without prescribing implementations.

### Design authority (software/reference)

- [scalability_design.md](scalability_design.md)  
  **What it is:** Scalability software/reference design defining three-space separation, resource roles, relationship classifications, progression obligations, and reporting/disposition boundaries.  
  **Status/authority:** Design draft (non-normative).  
  **Open when:** You need the governing design model for analysis behavior, finding structure, and disposition logic before implementation decisions.  
  **Relationship:** Downstream of program/gap analysis; upstream of implementation plan and implementation mapping.

### Implementation envelope

- [scalability_implementation_plan.md](scalability_implementation_plan.md)  
  **What it is:** Bounded implementation envelope specifying first-pass scope, constraints, required reuse, output rules, and acceptance tests.  
  **Status/authority:** Implementation envelope (non-normative until accepted).  
  **Open when:** You are planning or authorizing implementation work and need to determine what is in scope, out of scope, and required to stop/escalate.  
  **Relationship:** Downstream of design/gap analysis; upstream of implementation mapping and any bounded implementation work.

### Implementation mapping (review gate)

- [scalability_implementation_mapping.md](scalability_implementation_mapping.md)  
  **What it is:** Proposed first-pass implementation mapping from the envelope to concrete modules, interfaces, output layout, `.gitignore` needs, and acceptance-test coverage.  
  **Status/authority:** Proposed / awaiting review (not approved).  
  **Open when:** You need to confirm how the approved envelope maps to existing repository facilities before allowing implementation changes.  
  **Relationship:** Downstream of implementation plan; predecessor to bounded implementation execution.

### Practical guidance

- [scalability_user_guide.md](scalability_user_guide.md)  
  **What it is:** Practical guide for operators and Agents after an expansion.  
  **Status/authority:** Placeholder (non-normative). To be completed after bounded implementation establishes the concrete run/report workflow.  
  **Open when:** You have made a change and need the sequence for checking it.  
  **Relationship:** Downstream of program/design/implementation outputs; does not define principles.

## Extensibility

This family is extensible. Register new scalability documents here with role, status, consult trigger, and dependency relationships.

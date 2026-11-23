# Path A Scalability Design

**Document:** notes/program/scalability/scalability_design.md  
**Status:** Design draft (non-normative).  
**Date:** 2026-11-23  
**Purpose:** Establish what the Path A scalability system is, what the user gives it, what questions it answers, and what evidence and reports it returns. This document does not implement tooling or freeze report schemas.

## Purpose and scope

Scalability is a proposal-analysis and expansion-assessment system for Path A / S2M. It evaluates the consequences of a proposed expansion against the established environment without granting the proposal standing.

It answers:
- What does this proposed expansion change?
- What new reachable-and-valid combinations (progression obligations) does it create?
- Can those obligations presently be supported and qualified?
- What is the appropriate next route?

It does not:
- automatically establish proposed resources;
- judge semantic or scientific value;
- replace characterization programs;
- equate regression success with expansion qualification;
- perform root-cause diagnostics.

## Governing principles

### Three-space separation
$$
E \rightarrow (E \oplus \Delta) \rightarrow E'
$$
- $E$: established Path A environment.
- $E \oplus \Delta$: hypothetical analyzed environment (proposal present for analysis only).
- $E'$: future established environment, which exists only after separate, explicit acceptance/integration.

Scalability operates principally on $E \oplus \Delta$ and never silently turns it into $E'$.

### Revisability
Scalability evaluates proposals using an explicit, inspectable model of the presently understood Path A expansion space. The model is expected to evolve as new observations, resource classes, dependencies, and characterization boundaries are discovered. Comparison bases, obligation definitions, dependency rules, qualification boundaries, reporting policies, and scalability roles must remain replaceable without changing the core three-space distinction. At any given version the rules are explicit and deterministic; they are not claimed to be timeless.

### Finding visibility
Every non-clean or unresolved finding must be visible and traceable:

**ORIGIN → WHERE → WHAT → WHY → EVIDENCE → CONSEQUENCE → ROUTE**

- ORIGIN: the proposal item(s) responsible for the condition.
- WHERE: the affected surface, object, or obligation.
- WHAT: the condition observed.
- WHY: the rule or comparison basis that produced the finding.
- EVIDENCE: supporting artifacts.
- CONSEQUENCE: effect on the scalability assessment.
- ROUTE: indicated disposition.

When the current model cannot determine the answer, that uncertainty is itself a visible finding (`unresolved`, `discovery_failed`, provisional rule status).

### Diagnostics boundary
Scalability localizes and evidences the scalability condition. It does not investigate root causes (why a file is malformed, why a loader fails, why a table entry is stale). Those questions belong to a separate diagnostics program. Scalability hands forward structured findings, not bare status codes.

### Characterization boundary
Scalability detects, identifies, bounds, reports, and routes qualification obligations. It does not manufacture the observational evidence needed to qualify them. When an identified existing characterization boundary is crossed, scalability names the boundary, the affected obligations, the absent evidence, and the appropriate characterization destination, then routes `RETURN_TO_CHARACTERIZATION`. When no applicable characterization boundary can yet be identified because the expansion model itself is unresolved, scalability reports the unresolved condition and routes `HOLD`.

### Proposal boundary
The user-supplied YAML is an analysis proposal, not an operational Path A resource. A scalability run reads it, analyzes it against the established environment, and reports consequences. It does not promote, merge, or write it into established resources. Acceptance and integration remain a separate, explicit process.

## Architectural boundaries

- Proposal environment (analysis input only).
- Established environment ($E$).
- Analyzed hypothetical environment ($E \oplus \Delta$).
- Acceptance/integration boundary (outside scalability).
- Characterization-program boundary.
- Diagnostics boundary.

## Resource roles

Resource class and scalability role are independent dimensions. Roles describe how the current model reasons about a class; they are revisable and not a closed ontology. Observed roles:

- **Proposal-capable**: can appear directly in $\Delta$ and directly modify $E \oplus \Delta$.
- **Derived expansion surface**: not independently proposed; becomes newly reachable because a proposal-capable resource changed. Must be traced back to its generating origin.
- **Reference dimension**: organizes or is referenced by other structures; may also be proposal-capable.
- **Constraint/licensing surface**: determines which otherwise reachable structures are admitted as valid; changes the valid subset rather than creating new objects.
- **Historical/unresolved**: within conceptual scope, but the present model cannot enumerate generalized expansion obligations.

Current evidence:
- Dictionary entry — proposal-capable.
- Association — proposal-capable (some rules provisional).
- Seed — historical/unresolved → terminates with `HOLD`.
- Candidate — derived expansion surface (traced to generating association or major).
- Category / major — proposal-capable + reference dimension.
- Licensed region — constraint/licensing surface (present realization is bounded scaffolding).

A resource may change roles later if TS itself changes.

## Identity versus delta

Identity match is not delta identity. A proposal may target an already-existing resource while introducing a previously absent relation, value, member, or constraint. Scalability therefore evaluates the identity of the resource and the novelty of the proposed delta independently. Existing identity does not imply a duplicate proposal.

Example (dictionary):
- Existing word `cold` + identical mapping `cold → affective` → `already_defined`.
- Existing word `cold` + new mapping `cold → perceptual` → `extension_of`.

The program notifies:
> Existing item detected: `cold` already exists.  
> Proposed change: adds previously undefined category association `perceptual`.  
> Classification: `extension_of`.  
> Effect: proposal will be assessed for newly reachable-and-valid combinations resulting from this additional relation.

No error. No silent merge. The same separation applies to other classes: “the object exists” and “the proposed relation already exists” are distinct questions.

## Progression space

The progression space is the reachable-and-valid combination space $R_{\mathrm{valid}}$, not mere runtime reachability.

$$
O_{\Delta} = R_{\mathrm{valid}}(E \oplus \Delta) \setminus R_{\mathrm{valid}}(E)
$$

- Association or category changes may alter what becomes reachable.
- Licensed-region changes may alter which reachable things become valid.
- Both therefore affect $R_{\mathrm{valid}}$.

### Open consideration: contraction
Changing a constraint surface can also shrink valid space:

$$
R_{\mathrm{valid}}(E) \setminus R_{\mathrm{valid}}(E \oplus \Delta) \neq \varnothing
$$

A general change model could record both sides:

$$
\Delta R_{\mathrm{valid}} = \left( R_{\mathrm{valid}}(E \oplus \Delta) \setminus R_{\mathrm{valid}}(E) \right) \cup \left( R_{\mathrm{valid}}(E) \setminus R_{\mathrm{valid}}(E \oplus \Delta) \right)
$$

The governing problem is expansion. Contraction is recorded as an open design consideration. Regression may already surface some harmful cases; parallel machinery is not yet invented.

## Relationship classification

Primary, evidence-bearing classifications:
- `already_defined` — exact identity match against an existing object/reference.
- `missing` — no corresponding object or required support found (distinct from discovery failure).
- `extension_of` — schema-legal addition to an existing structure that does not contradict constraints.
- `additional_to` — new item that participates in existing combinations without modifying them.
- `incompatible` — violation of an explicit structural, schema, or contract condition (the violated condition is the evidence).

Derived observations (not primary classifications): `compatible` (no explicit incompatibility), `overlapping` (shared surfaces or combinations), `independent` (no shared surface). Uncertainty is reported as `unresolved`, not as a relationship.

Every classification carries: comparison basis, evidence artifacts, related established resources, reason, and resulting obligations. Approximate semantic similarity is disallowed.

## Analysis flow (conceptual)

Proposal YAML  
→ identify proposed items and deltas  
→ validate proposal structure (fail closed on missing identity or content)  
→ discover existing related definitions (distinguish absent from discovery failed)  
→ classify relationships (identity vs. delta)  
→ determine affected dependency surfaces  
→ compute newly reachable-and-valid combinations ($O_{\Delta}$)  
→ separate previously qualified from newly unqualified  
→ invoke regression (reuse existing infrastructure; keep results separate)  
→ check characterization boundaries  
→ assess structural placement and contribution  
→ produce disposition  
→ emit machine-readable and human/Agent-readable reports.

Item analysis precedes interaction analysis (combinations created only when multiple proposed items are taken together).

Derived surfaces are traced:

$$
\Delta_i \rightarrow \text{changed relation} \rightarrow \text{derived surface} \rightarrow \text{new valid combination} \rightarrow O_{\Delta}
$$

## Progression-obligation model

A progression obligation is a newly reachable, valid combination licensed by the proposal that is absent from the prior established valid space. Three tests:
- Reachability — does the proposal make the combination reachable?
- Validity/licensing — do explicit structural and flow conditions permit it?
- Novelty — was the combination absent from $R_{\mathrm{valid}}(E)$?

Only when all three hold does the combination enter $O_{\Delta}$.

Qualification states (distinct from obligation detection):
- `qualified` — covered by an applicable existing characterization boundary.
- `unqualified` — not covered.
- `deferred_bounded` — unqualified but explicitly bounded and recorded.
- `unresolved` — coverage cannot be determined from available evidence.

Explicit deferral does not make an obligation qualified.

## Disposition

Each check terminates in one of:
- `PROCEED` — expansion preserves prior behavior and new obligations are satisfied or explicitly bounded.
- `HOLD` — expansion recognized but further qualification or design is required.
- `REVISE` — the expansion or its supporting structures must be adjusted.
- `RETURN_TO_CHARACTERIZATION` — a prior characterization boundary has been crossed and must be reopened.

A disposition must reference both regression evidence and progression/qualification evidence. When the expansion model itself is undefined, the route is `HOLD`, not automatic return to characterization.

## Structural placement and contribution

Reports structural placement (resource family, extended definitions, shared surfaces, introduced dependencies, new territory) and structural contribution / expansion consequence (duplicates existing coverage, extends a region, adds a participant, fills an identified absence, creates new combinations, introduces unsupported dependencies, cannot yet be assessed). No judgment of semantic or scientific value.

## Reporting contract

A common evidence model supports machine-readable output and human/Agent-readable explanation. Illustrative content (fields provisional):
- proposal and item provenance;
- identity versus delta;
- relationship classification with evidence;
- obligation inventory;
- regression results (separate);
- characterization status;
- structural placement and contribution;
- disposition and rationale.

Every non-clean finding follows ORIGIN → WHERE → WHAT → WHY → EVIDENCE → CONSEQUENCE → ROUTE.

## Resource-class matrix (revisable, incomplete)

The matrix records, for each class, identity basis, participation, reachability, licensing, expansion delta, new combination form, dependencies, qualification evidence, characterization owner, scalability role, and rule status. It is expected to evolve.

Provisional evidence from pressure tests:
- Dictionary entry: mechanical chain (artifact delta → new relation → new reachable structures → new valid combinations → obligations → qualification).
- Association: mechanical chain with provisional licensing/qualification.
- Seed: historical/unresolved; progression obligation not presently enumerable → `HOLD`.
- Candidate: derived expansion surface; traced to generating proposal; no independent proposal class.
- Category/major: proposal-capable + reference dimension.
- Licensed region: constraint/licensing surface (present form is scaffolding); changes valid subset.

Reference objects/tables remain an open matrix area.

## Non-goals and prohibited inferences

- Approximate semantic similarity as identity.
- Silent promotion of proposals.
- Semantic-value judgments.
- Treating absence of detected conflict as proof of full compatibility.
- Treating deferred obligations as scientifically qualified.
- Treating green regression as progression qualification.
- Representing a derived surface as an independent proposal for architectural symmetry.
- Inventing unearned characterization or diagnostic machinery.

## Open design questions

- For each remaining expansion-sensitive resource class (including reference objects/tables), what is the precise enumerable definition of a newly created reachable-and-valid combination, and which characterization records determine whether it lies inside an existing qualified boundary?
- How, if at all, should contraction of valid space be surfaced beyond existing regression?
- What additional scalability roles, if any, emerge from further classes?

## Relationship to existing documents

This design receives the handoff from the scalability program proposal and the gap analysis. It does not alter the governing principles of those documents. Exact report field names and runtime directory names remain provisional. Generated reports stay local and untracked; only deliberately promoted formal conclusions are committed.

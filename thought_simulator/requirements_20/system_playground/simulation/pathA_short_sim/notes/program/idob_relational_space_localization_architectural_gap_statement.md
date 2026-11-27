# IdOB Relational-Space Localization Architectural Gap Statement

**Date:** 2026-11-27  
**Status:** Research finding/boundary statement (non-normative).  
**Purpose:** Objectify the architectural boundary reached by localization research without selecting a source, proposing architecture, or authorizing implementation.

Review state: **APPROVED**

## 1) Current architecture (bounded)

Authoritative Path A flow remains unchanged, including pre-IdOB structural and routing stages and IdOB placement:

`… -> SOB -> SROB -> CnOB -> SmOB -> … -> RTU -> TR -> CTP -> RB -> IdOB -> MCB -> …`

Current TS architecture provides pre-IdOB information classes (structural, routing/context, intake/request, and prior-cycle state under existing boundaries).  
Current TS architecture does not presently define:

- relational-space localization as a normative architectural operation;
- an exact localization point;
- a designated localization input;
- localization-specific read/access contract;
- a production non-oracle localization signal.

## 2) Exact architectural-gap problem statement

Current TS architecture contains clean pre-IdOB information and identifiable structural, routing/context, and intake distinctions, but it does not define a relational-space localization operation, designate a pre-IdOB localization input, or provide a localization-specific read/access contract. The localization research therefore cannot presently define a legitimate non-oracle generation path from existing runtime information to a localization representation without making an additional architectural decision.

This identifies a gap. It does not declare that TS must be changed.

Refinement boundary:

The Architectural Gap Statement remains valid relative to the earlier localization research framing.  
It does not establish a missing TS requirement.  
The broader functional question remains whether meaning construction benefits from contextual differentiation of relational material under non-oracle conditions at all.

## 3) Why this gap matters (bounded sequence)

### Gate A

Gate A showed fixture-relative organizational leverage under oracle-quality localization.

### Gate B

Gate B tested one frozen surrogate realization and was mechanically NEGATIVE.  
Gate B runtime selection was information-restricted, but `X_t` generation depended on privileged fixture information.

### Information/Representation Sufficiency

Exact activation identity was sufficient within the frozen fixture.  
Necessity was not established.  
Tested reduced/coarsened representations were not uniformly sufficient.

### R4 diagnostic

R4 succeeded only in the two qualified conditions where canonical decoding reconstructed exact Gate A activation.  
Its sole non-exact reconstruction failed.  
No successful different-than-oracle R4 activation was observed.

### W1-W3 review

W1-W3 were rejected because they were lossy functions of oracle activation rather than representations generated from an independently permitted non-oracle source.

### Provenance result

Pre-IdOB information can be identified and provenance described, but no source is currently designated or authorized as localization input.

## 4) Candidate classes relevant to the gap

Current-cycle research-eligible classes:

- **Structural:** structural substrate/frozen structural identifiers produced before IdOB.
- **Routing/context:** routing metadata and committed routing context before IdOB.
- **Intake/request:** intake and utterance-carrier information before IdOB.

Separate temporal class:

- **Historical/prior-cycle:** prior IdOB, lineage, continuity, COB/CIL/CST state remains separate and is not collapsed into current-cycle candidates.

No candidate class is selected as localization source.  
No sufficiency claim is made for any class.

## 5) Architecture/research boundary

Characterization may identify a required architectural change. It must not silently make that change.

### Research/characterization side

- reading existing authoritative definitions;
- recording information already present;
- tracing provenance;
- identifying existing distinctions;
- recording ownership and current read authority;
- identifying circularity;
- determining research eligibility;
- identifying an architectural gap.

### Architecture side

- declaring an existing field to be a localization input;
- granting new mechanism read authority;
- adding a read edge;
- changing field semantics;
- creating a field;
- changing ownership;
- changing flow timing;
- inserting a localization operation into normative Path A.

These boundary examples do not authorize any architecture change.

## 6) Classes of potential architectural adjustment (not authorized)

Possible classes that might eventually address the gap:

- explicit research-only read/access boundary over existing pre-IdOB information;
- definition of relational-space localization boundary/operation;
- explicit read contract for selected existing upstream information;
- intermediate field carrying justified pre-localization distinction;
- altered flow timing/placement if required information exists at wrong point.

For every class above:

- **not authorized**;
- no specific design chosen;
- further evidence and architecture review required.

## 7) What remains unknown

Closing this gap would still not establish:

- which source should be used;
- whether any existing source contains sufficient distinctions;
- whether multiple sources are required;
- whether a new field is necessary;
- whether localization belongs before or inside IdOB;
- whether a non-oracle representation can preserve sufficient distinctions;
- whether HOW-2 exists;
- whether Gate C should begin;
- whether production localization is feasible.

## 8) Program-state boundary and hold condition

Current state:

- **HOLD AT ARCHITECTURAL GAP STATEMENT**

No source selection, architecture proposal, implementation, or experiment is authorized by this statement.

Next step:

Human/CP/Grok review of this Architectural Gap Statement, followed by a separate decision whether to close the localization track or authorize an architecture-proposal cycle.

## 9) Decision sequence discipline

`observed gap -> justified requirement -> architecture proposal -> implementation`

Research may identify an architectural gap.  
A gap does not automatically become a requirement.  
A requirement does not automatically authorize a particular architecture.  
An architecture proposal does not automatically authorize implementation.

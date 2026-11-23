# Path A Scalability Program

**Document:** notes/program/scalability/scalability_program.md  
**Status:** Proposal (non-normative).  
**Date:** 2026-11-23  
**Purpose:** Define the Path A / S2M scalability and expansion-assurance program. Scalability is a Path A concern; Category Selection is one subsystem affected by expansion, not the owner of the program. This document establishes the governing principles, the distinction between regression and progression, the output discipline, and the phased development plan. It does not implement tooling or freeze report schemas.

## Mission and scope

Path A scalability governs how expansions of the realizable TS space are detected, checked for dependency alignment and prior characterized behavior, and qualified before being treated as established. An expansion does not automatically mean “TS now supports this.” It means the space has grown and the obligations created by that growth must be identified and addressed.

The program owns:
- definition of what constitutes an expansion;
- identification of expansion-sensitive resource classes;
- dependency-alignment obligations;
- regression versus progression/coverage;
- when characterization must be reopened;
- progression gates and decision states;
- expected report contract;
- tracked versus generated artifact policy.

It does not claim that the present Category Selection or S2M characterizations already scale.

## Path A ownership

This is a sibling program under `pathA_short_sim`, not a Category Selection document. Category Selection appears as one affected subsystem alongside seeds, associations, candidate structures, licensed regions, dictionaries/reference tables, flow contracts, and other expandable Path A resources.

## What constitutes an expansion

An expansion is any change that increases the reachable space or the set of valid combinations among Path A resources. Examples include, but are not limited to:
- addition or modification of seed entries;
- addition or modification of endpoint associations;
- growth or composition change in category or candidate inventories;
- addition of licensed-region tuples or reference YAML;
- changes that create new seed–association–candidate–category–licensed-region combinations.

Semantic plausibility of a new entry is not sufficient. Structural coverage and characterization must keep pace.

## Expansion-sensitive resource classes

Resources whose expansion can create new obligations:
- seed structures;
- association structures;
- candidate inventories and majors;
- category inventories;
- licensed-region definitions;
- dictionaries and reference tables;
- flow contracts and other YAML/reference files that participate in Path A execution.

Category Selection is one such class, not the sole class.

## Dependency-alignment principle

When a resource is expanded, the supporting structures and prior characterizations that the new combinations depend upon must be checked for presence and adequacy. Expansion must not silently outrun structural support or characterization.

## Regression versus progression

- **Regression:** Does previously characterized behavior still hold after the expansion?  
- **Progression / coverage:** Has the expansion created new combinations or dependencies that have not yet been qualified?

Both must be assessed. A green regression result does not imply that new coverage has been characterized. The Category Selection closeout identified this distinction; this program inherits it.

## Qualification requirement

New combinations created by expansion are not treated as established behavior until they have been qualified or explicitly deferred with a recorded boundary. Qualification may require a return to an existing characterization program or a new bounded observation when the expansion crosses a prior characterized boundary.

## Progression decisions

Each scalability check terminates in one of:
- `PROCEED` — expansion preserves prior behavior and new obligations are satisfied or explicitly bounded;
- `HOLD` — expansion is recognized but further qualification is required before acceptance;
- `REVISE` — the expansion or its supporting structures must be adjusted;
- `RETURN_TO_CHARACTERIZATION` — a prior characterization boundary has been crossed and must be reopened.

These are conceptual decision states for the eventual report contract. Exact field names remain provisional.

## Expected report contract (conceptual)

Each check produces a standardized, machine- and human-readable report that distinguishes at least:
- expansion detected;
- affected structures and dependencies;
- regression status;
- newly created coverage obligations;
- missing support;
- characterization boundary crossings;
- anomalies;
- final disposition.

Formal conclusions are promoted into tracked documentation only after review. Generated reports themselves are not committed.

## Tracked versus generated artifact policy

- Tracked: source, tooling, reference material, program documents, user guide, index, and deliberately promoted formal conclusions.  
- Generated and ignored: sessions, intermediate artifacts, and scalability reports under a local output directory (conceptually `local_scalability/`).  
`local_scalability/` is not committed.

## Proposed document and directory structure (provisional)

```
pathA_short_sim/
├── README.md                          # points to scalability program, user guide, and index
├── notes/program/scalability/
│   ├── scalability_program.md            # this document
│   ├── scalability_user_guide.md         # practical operator/Agent guide
│   └── scalability_index.md              # navigation/governance for the family
├── support/scalability/                 # repository-controlled support and reference
└── local_scalability/                  # generated sessions and reports (ignored)
```

Exact runtime directory names remain provisional until repository structure is inspected.

## Role of the user guide and index

- `scalability_user_guide.md` provides the practical sequence an operator or Agent follows after an expansion (identify change, invoke check, locate and interpret report, decide next action).  
- `scalability_index.md` routes readers by document role and authority, analogous to the Category Selection index. All later scalability artifacts register there.

## README integration

The `pathA_short_sim/README.md` will point to the three scalability documents with a short directive: Expanding Path A? Start with the scalability program and user guide before treating new YAML/reference coverage as established behavior.

## Relationship to existing characterization programs

The Category Selection characterization cycle closed with an explicit handoff that scalability is a separate unresolved concern. This program receives that handoff. It may later invoke Category Selection or other characterization programs when an expansion crosses a characterized boundary, but it does not own those programs.

## Non-claims

- The present Category Selection or S2M characterizations are not claimed to scale.  
- No specific warning signals are asserted as inevitable.  
- No report schema or tooling is frozen by this proposal.  
- Semantic plausibility of new entries is not a substitute for structural coverage.

## Phased development plan

1. Proposal (this document) → agreement.  
2. Infrastructure audit of existing Path A test/reference structures.  
3. Gap analysis.  
4. Software/reference design.  
5. Bounded implementation.  
6. User guide and index completion.  
7. README integration.

Do not implement tooling or freeze schemas until the proposal is agreed and the audit is complete.

## Deferred/open issues pointer

Deferred and unresolved scalability concerns (including preconversation/context scaling) are tracked in [scalability_gap_analysis.md](scalability_gap_analysis.md). This program document keeps only the governing principles and does not duplicate gap-level issue detail.

## Stop conditions

Stop and return to research review if an expansion reveals that the regression/progression distinction cannot be maintained, or if the proposed report contract cannot distinguish the required states without inventing unearned machinery.

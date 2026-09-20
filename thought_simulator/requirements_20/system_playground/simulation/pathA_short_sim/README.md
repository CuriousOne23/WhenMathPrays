# PathA Short Simulation README

This directory contains a toy Thought Simulator (TS), Path-A simulator.

Its purpose is educational: provide an architectural feel for major Path-A blocks, TP evolution across primitives, and dictionary-driven behavior while remaining lightweight and inspectable.

## Short Simulator Macro Categories

- Intake Macro: InB, IIInB, IE
- Correction Macro: CEx, CE, ISc, TPU
- Structural Geometry Macro (OB-Set): SOB, SROB, CnOB, SmOB, SSG
- Routing Macro: RBU, RB, TRU (truth-relation stub), RTU, CTP
- Semantic Macro: IdOB
- Final Commit Macro: OuBA

## Full Path-A Macro Categories (20.705 Section 2)

- Intake Macro
- Correction Macro
- Structural Interpretation Macro (OB-Set)
- Routing Macro (including STPX, DCB, TR (Thought Router))
- Identity and Meaning Macro (IdOB -> MCB)
- Truth-Relation Macro (TRU)
- Final Commit Macro (OuBA)

## Real Path-A to Toy Simulator Mapping

| Full Path-A Macro | Real Primitive(s) | Toy Primitive(s) | Status in Toy |
| --- | --- | --- | --- |
| Intake | InB, IIInB, IE | InB, IIInB, IE | Implemented |
| Correction | CEx, CE, ISc, TPU | CEx, CE, ISc, TPU | Implemented (simplified) |
| Structural Interpretation (OB-Set) | SOB, SROB, CnOB, SmOB, SSG | SOB, SROB, CnOB, SmOB, SSG | Implemented (dictionary-driven, simplified) |
| Routing | RBU, RB, STPX, DCB, TR | RBU, RB, TR, RTU, CTP | Partial: TR placeholder; STPX/DCB omitted |
| Identity and Meaning | IdOB, MCB | IdOB | Partial: MCB omitted |
| Truth-Relation | TRU | TRU | Implemented as stub |
| Final Commit | OuBA | OuBA | Implemented |

## Future Extension Plan

1. Expand routing realism by implementing STPX and DCB with inspectable intermediate routing states.
2. Evolve TR from placeholder to real Thought Router behavior that consumes routing entropy and context metadata.
3. Add MCB behavior after IdOB for richer identity and meaning composition.
4. Replace simplified correction assumptions with scored candidate generation and observable correction provenance.
5. Expand OB-Set outputs from list-like traces to explicit structural graph objects.
6. Add richer truth-relation logic in TRU that references provenance and semantic-adjacent cues.

## What This Simulator Does NOT Do

- Does not implement STPX, DCB, or MCB.
- Does not implement full Thought Router logic in TR (currently placeholder only).
- Does not provide full provenance chains for TP field mutations.
- Does not expose structural graph objects beyond simplified segment/role lists.
- Does not compute routing entropy or confidence metrics.
- Does not model semantic-adjacent cues, latent context priors, or cross-sentence memory.
- Does not validate all production-grade Path-A constraints.

## Related Documents

- Architectural simulation details: [support/docs/architectural_simulation.md](support/docs/architectural_simulation.md)
- Dictionary reference and schema: [support/docs/dictionaries_reference.md](support/docs/dictionaries_reference.md)

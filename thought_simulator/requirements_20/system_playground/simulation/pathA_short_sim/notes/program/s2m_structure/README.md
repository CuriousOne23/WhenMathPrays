# S2M structure pass

**Date:** 2026-10-08
**Status:** definition. Not a writer. Not \(M\). Not the geometry conjecture.

This directory defines the present Structure-to-Meaning (S2M) experiment for Path A. Read it before any connection writer is added.

Program entrance: [../README.md](../README.md). Geometry note, not imported: [../../conjectures/meaning_geometry_conjecture.md](../../conjectures/meaning_geometry_conjecture.md).

## Why this directory exists

The structural floor can cut an utterance and IdOB can sum a packet. The readable claim is one string from that packet. Neither of those is an accountable mapping. S2M is still foggy if a missing link can be inferred by silence.

This pass defines the structure of the mapping before a writer exists. It names the terms, the legal input, the connection, the hole, the pressure points, and the utterance set. It also bounds success and failure in advance.

## Theme

Connection, not geometry. One utterance. The finished packet is the only input. A connection is written only from fields the packet has. A hole is written where an asked relation cannot be supplied. No winner is chosen.

## Composition

One utterance goes in. The cut is not reopened. Two lists come out.

- Supported connections. Each one names two packet objects, one relation, and the status `supported`.
- Holes. Each one names an asked relation whose endpoint, hat, or basis for preference is not in the packet, with the status `missing`.

Fifteen ledger utterances are the population. They are the check, not the definition. The list is [utterances.md](utterances.md).

## Terms

| Term | Bound |
|---|---|
| Prework | The cut and the packet already produced by SOB, SROB, CnOB, SmOB, and the IdOB sum. Format: [prework.md](prework.md). |
| Connection | Two packet objects, one relation from the closed list, one status. Format: [connection.md](connection.md). |
| Supported | Both ends are in the packet and the relation is on the closed list. |
| Missing | An asked relation has an empty end, or the utterance has no objects. |
| Hole | A written missing item. Silence is not a hole. Silence is a failed report. Format: [holes.md](holes.md). |
| Pressure | A limit this pass names and does not solve. Format: [pressure.md](pressure.md). |
| Underspecified | Two supported relations and no basis for preference. Not a hole. Not a winner. Named in the pressure list if it appears. |

`ambiguous` is not a status in this pass. The packet cannot yet say why two links are equal.

## Why the experiment matters

Path A claims that structure can be cut before meaning, and that IdOB can later map that cut. This pass is the first check of that claim that is smaller than solving meaning. If the packet can support a disciplined relationship record, the floor can carry S2M at all. If it cannot, the hole list says what the floor or the packet does not yet supply.

## Success, bounded

Success is a definition that a later writer can fill without repairing the cut, plus a writer that does fill it.

For this document request, success is narrower. A reader can find the purpose, the terms, the input, the connection, the hole rule, the pressure list, and the fifteen utterances without reading `idob/claim.py`. The readable claim is not described as the connection record.

For the later writer, success is all of the following.

- Each of the fifteen utterances produces a composition.
- Every supported connection traces to a packet field and a relation on the closed list.
- Every asked relation with an empty end is a hole.
- The unknown string has no supported connection and one neighborhood hole.
- Segments, roles, and constraints are unchanged.
- No link is marked most likely.

## Failure, bounded

Failure is not "the sentence feels unresolved." Failure is one of these.

- An object appears that is not in the packet.
- A segment, role, or constraint changes.
- A relation is ranked, or a winner is chosen.
- A hole is omitted because the claim string looked complete.
- The unknown string receives a supported connection.
- The definition treats history, likelihood, or the geometry note as an input.

A failure of that kind means Path A, as realized, cannot yet support accountable S2M. It does not by itself falsify the geometry conjecture. It says the packet or the floor is not yet sufficient, and the hole list is what is not right.

## What success does not mean

- It does not mean meaning is a geometry.
- It does not mean a historical conversation is available.
- It does not mean one relation is more likely than another.
- It does not mean \(M\), the envelope, or \(\Delta h\) has been computed.
- It does not mean the readable claim rung is retired.

## If this succeeds

The next step is the record format, then the writer, in later requests. After those hold on the fifteen utterances, the next step is one pressure point at a time. The first expected pressure is underspecification: two supported relations and no preference. History and likelihood stay behind that.

## If this fails

The experiment stops at the failing bound. The report names which bound failed and which packet field was absent. That absence is the correction to Path A. The correction is not a silent inference, and it is not an import of the geometry note.

## Reading order

1. This page.
2. [prework.md](prework.md)
3. [connection.md](connection.md)
4. [holes.md](holes.md)
5. [pressure.md](pressure.md)
6. [utterances.md](utterances.md)
7. [result.md](result.md) — what the first writer showed and did not show.

Writer: `idob/connections.py`. Replay: `PYTHONPATH=. python3 support/tools/s2m_connection_replay.py`. The writer records supported fields and a neighborhood hole when no connection is supported. It does not rank.

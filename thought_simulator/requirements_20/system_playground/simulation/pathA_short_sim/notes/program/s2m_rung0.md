# S2M rung 0 — map the packet, do not reopen the cut

**Date:** 2026-10-08
**Status:** first demonstrable rung. Not the other bench. Not \(M\).

The structure floor can now be checked. This rung is IdOB reading the packet it already summed.

Legal input: `idob` packet on the finished Thought Packet.
Forbidden: rewriting `struct_segments`, `struct_roles`, or constraints.
Not computed: \(M\), the envelope \(M' = M + \alpha I\), \(\Delta h\).

The other bench remains evidence: `testbenches/idob_structure_to_meaning/`. This rung does not import it.

A mood with an empty core is not a mapped claim. The current sum still activates the same cards for `LLhfds pw Ppen qqoubx&` as for *The sky is blue.* This rung does not repair that. It reports `claim_empty` for both, and `mapped` only when the packet already wrote a claim op or a non-empty core value. `modifier_resolution` is ignored; it is the old helper.

Replay: `PYTHONPATH=. python3 support/tools/s2m_rung0_replay.py`

- *The sky is blue.* stays `claim_empty`. Segments unchanged. Mood is declarative.
- *The cat chased the mouse.* maps, carrying `agent_action`. Segments unchanged.
- `LLhfds pw Ppen qqoubx&` stays `claim_empty`. No invented claim.

Program: [pathA_program.md](pathA_program.md). Ready line: [ready_line.md](ready_line.md).

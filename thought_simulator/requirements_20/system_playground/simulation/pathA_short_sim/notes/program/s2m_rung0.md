# S2M rung 0 — map the packet, do not reopen the cut

**Date:** 2026-10-08
**Status:** first demonstrable rung. Not the other bench. Not \(M\).

The structure floor can now be checked. This rung is IdOB reading the packet it already summed.

Legal input: `idob` packet on the finished Thought Packet.
Forbidden: rewriting `struct_segments`, `struct_roles`, or constraints.
Not computed: \(M\), the envelope \(M' = M + \alpha I\), \(\Delta h\).

The other bench remains evidence: `testbenches/idob_structure_to_meaning/`. This rung does not import it.

Replay: `PYTHONPATH=. python3 support/tools/s2m_rung0_replay.py`

- *The sky is blue.* maps from the packet. Segments unchanged.
- *The cat chased the mouse.* carries `agent_action` from the packet. Segments unchanged.
- `LLhfds pw Ppen qqoubx&` stays unbound. No invented claim.

Program: [pathA_program.md](pathA_program.md). Ready line: [ready_line.md](ready_line.md).

# S2M rung 1 — a readable claim from the packet

**Date:** 2026-10-08
**Status:** second demonstrable rung. Not \(M\). Not the other bench.

Rung 0 said whether the packet had a claim. This rung writes the claim from fields the packet already has.

Legal input: the finished `idob` packet.
Forbidden: rewriting segments, roles, or constraints.
Not computed: \(M\), the envelope, \(\Delta h\).

Replay: `PYTHONPATH=. python3 support/tools/s2m_rung1_replay.py`

- *The sky is blue.* claims `the sky is blue`.
- *The book is on the table.* claims `the book at on the table`.
- *The cat chased the mouse.* claims `the cat chased the mouse`.
- `LLhfds pw Ppen qqoubx&` stays empty.

Program: [pathA_program.md](pathA_program.md). Previous rung: [s2m_rung0.md](s2m_rung0.md).

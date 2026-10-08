# Ready line

**Date:** 2026-10-08
**Status page for this directory.** Open this with [README.md](README.md) before treating an older note as current.

## Done enough to trust as current realization

- Five sentence families print across the lineup: copular, locative, mixed descriptive, interrogative, mixed interrogative. Authority: [../pathA_supported_sentences.md](../pathA_supported_sentences.md).
- Claim cues print on the runner for negation, coordination, conditional, fragment, speaker, passive, quantifier, bare command, request, and exclamative. Ledger: [../claim_backlog_status.md](../claim_backlog_status.md).
- `imperative`, `exclamative`, and `agent_action` are their own YAML families. The schema enum does not yet name `imperative` or `exclamative`; the loader does not enforce that enum. Note: [../stamp_families.md](../stamp_families.md).
- Meaning today is the `idob_packet` from the sum. S2M does not print.

## Not done — structure floor

Replayed by `support/tools/form_hole_replay.py`. *The book is on the table.* does not grow these circles or hats.

| Hole | Sentence | Write now present |
|---|---|---|
| Reporting circle | *She said the book is on the table.* | `REPORT` on `said`, distinct from the book circle |
| Recipient hat | *Give me the book.* | `RECIP` with hat `recipient`; the book circle is not that hat |
| Relative subject that is not the head | *The book that John bought* | circle `john` with hat `relative_subject`; the book circle is not that hat |

Action verb circle is replayed by `support/tools/action_row_replay.py`. *The cat chased the mouse.* segments `NP VP NP`, cue `action_clause`, op `agent_action`. *The sky is blue.* prints no op. *Close the door.* still prints `bare_command`. Note: [../action_row_runner.md](../action_row_runner.md).

Activation trees in the YAML are still empty. Apply still points at legacy or at the small imperative and exclamative modules. Empty activation is a named limit, not a silent success.


First mapping rung, not \(M\): [s2m_rung0.md](s2m_rung0.md). Replay `support/tools/s2m_rung0_replay.py`. The cut is not reopened. The other bench is not imported.

## Not this phase

- Implementing S2M, \(M\), the envelope \(M' = M + \alpha I\), or \(\Delta h\) inside IdOB.
- Importing the other bench into this directory.
- Treating RBU, RB, TR, RTU, or CTP as the parent of SOB.
- STPX, DCB, and Meaning Composition Block (MCB). Omitted. Not the ready line.

## Moving too soon

Moving is premature while a bad packet could be an invented span, a grammar repair, or a real mapping miss, and the log cannot say which. After the named holes are either printed or still explicitly unsupported, and the action circle is either landed or still listed as not on the branch, IdOB mapping composed packets is the next phase.

Dated snapshots, not this ledger: [../pathA_freeze_manifest_v1.md](../pathA_freeze_manifest_v1.md), [../cutover_readiness_report.md](../cutover_readiness_report.md).

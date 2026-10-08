# Ready line

**Date:** 2026-10-08
**Status page for this directory.** Open this with [README.md](README.md) before treating an older note as current.

## Done enough to trust as current realization

- Five sentence families print across the lineup: copular, locative, mixed descriptive, interrogative, mixed interrogative. Authority: [../pathA_supported_sentences.md](../pathA_supported_sentences.md).
- Claim cues print on the runner for negation, coordination, conditional, fragment, speaker, passive, quantifier, bare command, request, and exclamative. Ledger: [../claim_backlog_status.md](../claim_backlog_status.md).
- `imperative`, `exclamative`, and `agent_action` are their own YAML families. The schema enum does not yet name `imperative` or `exclamative`; the loader does not enforce that enum. Note: [../stamp_families.md](../stamp_families.md).
- Meaning today is the `idob_packet` from the sum. Copular core for *The sky is blue.* is theme `the sky`, state `blue`, replayed by `support/tools/copular_core_replay.py`. Locative core for *The book is on the table.* is theme `the book`, location `on the table`, replayed by `support/tools/locative_core_replay.py`. Query core for *Where is the book?* is query_focus `where`, replayed by `support/tools/query_core_replay.py`. A declarative does not grow a query focus. *Why is the sky blue?* now splits state `blue` from theme `the sky`, replayed by `support/tools/why_state_replay.py`. *The quick brown fox jumps over the lazy dog.* writes `VP` on `jumps`, replayed by `support/tools/jumps_circle_replay.py`. The hat and cue are replayed by `support/tools/jumps_hat_replay.py`: action `jumps`, op `agent_action`. The locative dog is not a patient. Prenominal adjectives stay with the noun. *The rain in Spain stays mainly in the plain.* carries both locations and state `stays`, replayed by `support/tools/spain_core_replay.py`. `mainly` is not a state. `LLhfds pw Ppen qqoubx&` is not a noun circle, replayed by `support/tools/unknown_not_np_replay.py`. *Is the book on the table?* writes cue `polar_question`, replayed by `support/tools/polar_cue_replay.py`. A wh-question and a declarative do not grow that cue. `modifier_resolution` is no longer appended just because a cue exists, replayed by `support/tools/helper_op_replay.py`. *Where is the book?* writes op `query_focus`, replayed by `support/tools/wh_op_replay.py`. A polar question does not steal that op. *Close the door.* writes a verb circle on `close` and still prints `bare_command`, replayed by `support/tools/command_circle_replay.py`. *Please close the door.* writes a `REQ` circle on `please` and still prints `polite_request`, replayed by `support/tools/please_circle_replay.py`. *What a beautiful lamp!* keeps `exclamative_force` and does not write `query_focus`, replayed by `support/tools/exclamative_not_wh_replay.py`. The unknown string stays claim-empty. S2M geometry does not print.

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

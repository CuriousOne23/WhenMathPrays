# Path A short-sim program

**Date:** 2026-10-08
**Status:** account for this directory. Does not change the runner.
**Point here first** for present status, what has been done, and what is not done yet.

This folder is the comprehensive view of `pathA_short_sim`. A later reader, human or agent, should open this README before the coverage map, the freeze manifest, or the structure-theory entrance.

## Reading order

0. [status.md](status.md) — implemented, absent, and the requirement account.
1. [pathA_program.md](pathA_program.md) — current face, intended face, mechanics beside the floor.
2. [grammar_and_structure.md](grammar_and_structure.md) — ordinary grammar against the structural cut.
3. [four_writers.md](four_writers.md) — SOB, SROB, CnOB, SmOB: what each may record, what each may not reopen.
4. [packet_and_mapping.md](packet_and_mapping.md) — the packet today, and the mapping that is not running.
5. [ready_line.md](ready_line.md) — what is done, what is still a hole, and what counts as moving too soon.
6. [s2m_rung0.md](s2m_rung0.md) — first mapping rung. Packet in, cut not reopened. Not \(M\).
7. [s2m_rung1.md](s2m_rung1.md) — readable claim from the packet. Not \(M\).
8. [claim_ledger.md](claim_ledger.md) — claims that print now.
9. [known_words.md](known_words.md) — closed list. Unknown content words are not invented.
10. [s2m_structure/README.md](s2m_structure/README.md) — S2M structure definition. Connections and holes. Not \(M\).
11. [s2m_structure/result.md](s2m_structure/result.md) — what the first connection writer showed.
12. [packet_sync/README.md](packet_sync/README.md) — name map. `idob_packet` is a view over `tp.idob`. Crossing fields are absent.

## Document family indexes

These navigation indexes were added after the 2026-10-08 reading order above. They route the Path A characterization works under this folder; they do not replace [status.md](status.md) as the goal account.

- [category_selection_index.md](category_selection_index.md) — Category Selection documents, plus the `run_examples.py` / `characterization/` operator and library surfaces. Operator how-to: [../../user_guide.md](../../user_guide.md).
- [s2m_index.md](s2m_index.md) — S2M documents and the S2M-focused replay scripts under `support/tools/`.
- [idob_relational_space_localization_index.md](idob_relational_space_localization_index.md) — IdOB relational-space localization track, including the Gate A / Phase 3 characterization program.
- [scalability/scalability_index.md](scalability/scalability_index.md) — scalability documents, `run_scalability.py`, and the `scalability/` package. Operator how-to: [scalability/scalability_user_guide.md](scalability/scalability_user_guide.md).

Packet-sync evaluation and replay programs are listed under [packet_sync/README.md](packet_sync/README.md). Remaining characterization and experimentation programs under `support/tools/` and the short-sim root, not owned by the family indexes above:

- Floor, form, claim, and activation replays in [../../support/tools/](../../support/tools/): `action_row_replay.py`, `activation_guard_replay.py`, `activation_guard_2_replay.py`, `activation_tree_replay.py`, `activation_tree_2_replay.py`, `activation_tree_3_replay.py`, `adverb_claim_replay.py`, `claim_join_replay.py`, `claim_ledger_replay.py`, `command_circle_replay.py`, `command_theme_claim_replay.py`, `copula_claim_replay.py`, `copular_core_replay.py`, `exclamative_not_wh_replay.py`, `form_hole_replay.py`, `helper_op_replay.py`, `jumps_circle_replay.py`, `jumps_hat_replay.py`, `known_word_boundary_replay.py`, `location_op_replay.py`, `locative_core_replay.py`, `please_circle_replay.py`, `polar_cue_replay.py`, `query_core_replay.py`, `recipient_op_replay.py`, `recipient_relative_claim_replay.py`, `relative_op_replay.py`, `reporting_op_replay.py`, `schema_enum_replay.py`, `spain_core_replay.py`, `speaker_hat_replay.py`, `state_op_replay.py`, `unknown_not_np_replay.py`, `wh_op_replay.py`, `why_state_replay.py`. Each script's module docstring states the specific contract it checks. The claim check used from the door is `claim_ledger_replay.py`.
- [../../support/tools/pipeline_readiness_check.py](../../support/tools/pipeline_readiness_check.py) — deterministic full-pipeline readiness check (`pipeline_ready=True/False`); also reused as a scalability `--run-regression` script.
- [../../support/tools/ouba_stability_check.py](../../support/tools/ouba_stability_check.py) — OuBA assembly stability check on synthetic IdOB packets (`ouba_stability=True/False`).
- [../../replay_parity_harness.py](../../replay_parity_harness.py) — deterministic replay-parity harness for intake and token/segment cases (`--case`, `--format`, `--output`).
- [../../generate_cutover_readiness_report.py](../../generate_cutover_readiness_report.py) — runs the example sentence set and writes `cutover_readiness_report.json` plus [../cutover_readiness_report.md](../cutover_readiness_report.md).

## What this pass does not do

- It does not edit Python, YAML, or evidence JSON.
- The action verb circle has landed. See [ready_line.md](ready_line.md).
- A first S2M structure record now writes connections and holes. It is not \(M\). See [s2m_structure/result.md](s2m_structure/result.md).
- It does not treat the current sum as the forever role of Identity Observation Block (IdOB).
- It does not treat the shut door as a ban on the later mapping.

## Authorities that remain

- Names: [../../architecture/idob_seam.md](../../architecture/idob_seam.md)
- Sum contract: [../../architecture/idob_meaning_lock.md](../../architecture/idob_meaning_lock.md)
- Lineup versus reserved 20.40: [../../architecture/path_a_realization_charter.md](../../architecture/path_a_realization_charter.md)
- Why the cut exists: [../../debug/pathA_structure_theory.md](../../debug/pathA_structure_theory.md)
- Branch fact for the action row: [../action_row_runner.md](../action_row_runner.md)

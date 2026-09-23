# Path A Grouped Rollout Plan (PA-CSE-012..021)

Purpose: implement currently not-yet-implemented CSE utterances with minimal churn and maximum observability.

Scope:
- Runner: `run_examples.py`
- Debug parser/report: `pathA_dbug.py`, `debug_out.md`
- Status ledger: `notes/pathA_supported_sentences.md` section 10

Non-goals:
- No silent change to frozen ontology without explicit status-note declaration
- No packet-shape mutation without documented requirement

## Mandatory status-change rule

For every status change in section 10, the row update must include:
- `Hole ID` (from `notes/pathA_cse/00_header.md` section 9)
- `Capability Note` (explicit: capability added, or frozen object still required)

A status change is invalid without both fields.

## Group order (token-efficient)

1. Group B: negation + quantification
- PA-CSE-013 (HOLE-08)
- PA-CSE-019 (HOLE-15)

2. Group C: coordination + conditional
- PA-CSE-014 (HOLE-11)
- PA-CSE-015 (HOLE-10)

3. Group E: person + passive
- PA-CSE-017 (HOLE-13)
- PA-CSE-018 (HOLE-14)

4. Group A: imperative/request/exclamative
- PA-CSE-012 (HOLE-09)
- PA-CSE-021 (HOLE-09)
- PA-CSE-020 (HOLE-16)

5. Group D: fragment / ellipsis
- PA-CSE-016 (HOLE-12)

## Per-group implementation loop

1. Activate one target sentence in `run_examples.py` and keep others commented.
2. Run `run_examples.py` to regenerate `run.log`.
3. Run `pathA_dbug.py run.log --base-dir .` to regenerate `debug_out.md`.
4. Validate gates.
5. Update section 10 row status only if gates pass.
6. Re-run one implemented baseline sentence to check regressions.

## Validation gates (required)

- Gate G1: runner executes end-to-end without exception.
- Gate G2: `run.log` includes Final TP intake geometry and primitive trace.
- Gate G3: `pathA_dbug.py` completes and writes `debug_out.md`.
- Gate G4: `debug_out.md` shows IE and SOB geometry sections coherently.
- Gate G5: TRU and IdOB summaries are consistent with intended family behavior.

Status promotion policy:
- `Not yet implemented` -> `In work` when pattern exists and local completion works but not yet committed as live runner.
- `In work` -> `Implemented` only when committed runner path can execute this utterance end-to-end and debugger output is correct.

## Debug/Control notes

- Keep one active sentence in runner at a time.
- Every temporary rule should emit trace-visible fields.
- Prefer additive constraints/cues first; postpone ontology changes until required.
- If a new frozen object is required, stop promotion and record that requirement in `Capability Note`.

## Regression sentinel set

After any group completion, re-run at least:
- PA-CSE-008 (Why is the sky blue?)
- PA-CSE-010 (Where is the book that is on the table?)

This checks interrogative-open and nested-interrogative integrity.

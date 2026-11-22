# Category Selection Characterization Experiment Plan

**Document:** notes/program/category_selection_characterization_experiment_plan.md  
**Status:** Controlled execution plan for characterization experiments (non-normative).  
**Date:** 2026-11-22

## 1) Purpose and scope

This document is the execution-control plan for running category-selection characterization experiments with the currently implemented Milestone-1 infrastructure.

It defines how to execute experiments sequentially under mandatory review gates:

**observe -> characterize -> review -> decide next experiment**

This document does not replace research/reference authority and does not pre-commit scientific conclusions.

## 2) Authoritative/reference documents and roles

- [category_selection_index.md](category_selection_index.md): document routing/ownership.
- [category_selection_research_plan.md](category_selection_research_plan.md): research questions, principles, and experiment-family framing.
- [category_selection_characterization_reference.md](category_selection_characterization_reference.md): characterization method/contract boundaries.
- [category_selection_program_reference.md](category_selection_program_reference.md): realization-side contract boundaries.
- [category_selection_characterization_milestone1_closeout.md](category_selection_characterization_milestone1_closeout.md): what Milestone-1 infrastructure actually established.
- [category_selection_observation.md](category_selection_observation.md): destination for empirical findings after evidence review.
- [user_guide.md](../../user_guide.md): operator workflow guidance.

Normative behavior/ownership remain in requirements documents referenced by the research/reference set above.

## 3) Experimental invariants

Every experiment in this campaign must preserve:

- characterization observes normal selected TS execution; it does not define an alternate meaning path;
- characterization does not own or silently alter TS-affecting controls;
- one characterization invocation performs one TS execution;
- canonical identity is `(session_id, run_index)`; successful evidence for an identity is not silently overwritten;
- `.tschar.json` is success-only machine-readable evidence;
- unavailable measurements must remain explicitly unavailable (not fabricated);
- category-result evidence is not equivalent to meaning selection by itself;
- Level-A behavior comparison exclusions are limited to approved non-behavioral metadata (`created_at_utc` only unless authority changes).

## 4) Explicit prohibited actions

The executing agent must not:

- change production/category-selection behavior to improve experiment outcomes;
- invent/tune thresholds or introduce a no-category decision rule without existing authority;
- silently repair unexpected behavior;
- fabricate unavailable measurements;
- treat category result as meaning conclusion;
- convert observations into pass/fail claims without a stated criterion;
- proceed automatically from Experiment N to Experiment N+1;
- broaden campaign scope into orchestration or new characterization types.

Unexpected behavior is evidence to report, not an automatic bug-fix directive.

## 5) Current implemented capability boundary (execution-relevant)

Current experiment execution is bounded to implemented capabilities:

- entrypoint: `run_examples.py`;
- execution case currently supported for controlled baseline: `--execution-case sky_blue`;
- execution controls available: `--enable-category-selection`, `--no-s2m-seed`, `--no-category-observations`;
- characterization controls available: `--characterize`, `--char-type`, `--char-session-id`, `--char-run-index`, `--char-version`, `--char-params-json`, `--char-params-file`;
- characterization type currently implemented for this campaign: `infra_smoke` (version `1.0`);
- success evidence location pattern:
  `local_characterization/sessions/<session_id>/runs/<run_index>__<type>__<version>.tschar.json`;
- stdout may include one final `=== CHAR TRACE ===` block per controlled characterization invocation;
- raw argparse type rejection can exit before CHAR TRACE.

## 6) Execution and artifact-recording procedure

For each experiment:

1. Define experiment ID, objective, and controlled variables before execution.
2. Declare exact command(s) and expected artifact identity `(session_id, run_index)`.
3. Run commands exactly as specified; do not edit runtime code/config as part of experiment execution.
4. Record:
   - command line(s),
   - exit code(s),
   - run.log path(s) when redirected,
   - CHAR TRACE status/pointer behavior (if applicable),
   - committed `.tschar.json` path(s) when successful.
5. Parse evidence only from produced runtime outputs/artifacts.
6. Record unavailable measurements explicitly as unavailable.
7. Preserve raw evidence long enough for review; clean only test-specific local outputs after review approval.

## 7) Campaign-level queue / roadmap (provisional beyond Experiment 1)

- **Experiment 1 (fully specified):** smallest no-cue/baseline characterization.
- **Experiment 2 (provisional):** sentence-internal cue case(s) with controlled comparison to baseline.
- **Experiment 3 (provisional):** prior-context cue case(s) with provenance-focused comparison.
- **Experiment 4 (provisional):** ambiguity/competing-evidence cases from research-plan families.
- **Experiment 5 (provisional):** boundary/weak-evidence probes (only after prior review decisions).

Only Experiment 1 is execution-authorized by this plan text. Later experiments require post-experiment review decisions and may be changed, deferred, replaced, or canceled.

## 8) Standardized per-experiment specification template

Each experiment spec must include:

1. **Experiment ID and title**
2. **Objective (observation question, not conclusion)**
3. **Inputs/cases** (exact sentence/case/context)
4. **TS-affecting controls** (explicit values)
5. **Characterization controls** (type/session/run/version/params)
6. **Command(s)** (verbatim)
7. **Expected evidence surfaces** (`run.log`, CHAR TRACE, `.tschar.json`)
8. **Planned comparisons** (if any), including approved exclusions
9. **Stop/escalation triggers specific to this experiment**

## 9) Standardized result/observation record template

After execution, report:

1. **What executed** (exact commands, times/order)
2. **Inputs and controls used**
3. **Produced artifacts/logs** (exact paths)
4. **Observed outputs** (facts only)
5. **Unavailable measurements/deviations**
6. **Unexpected behavior/anomalies**
7. **Interpretation (bounded)**
8. **Not established**
9. **Questions raised**
10. **Next-step options** (suggestions, not decisions)

## 10) Mandatory review gate after every experiment

After each experiment, the executing agent must stop and present:

- what was executed;
- exact cases/inputs and controls;
- generated artifacts;
- observed results;
- unavailable/deviating measurements;
- unexpected behavior;
- questions raised;
- suggested next steps (clearly labeled as suggestions).

No further experiment may run without explicit authorization.

## 11) Rules for changing later experiments

After review, the next experiment may be:

- **continued** as drafted,
- **modified** (controls/cases narrowed or expanded),
- **repeated** (for replay/confirmation),
- **replaced** (if prior assumptions were invalid),
- **deferred/canceled** (if no longer relevant).

Any such decision must be tied to observed evidence from prior experiments, not prewritten campaign momentum.

## 12) Stop/escalation conditions

Stop and escalate for review when any of the following occur:

- unexpected behavior that could indicate implementation ambiguity;
- missing capability needed for planned measurement;
- nondeterminism outside approved exclusions;
- apparent contradiction with governing documents;
- CHAR TRACE/artifact mismatch (for example, pointer does not correspond to committed artifact);
- identity/overwrite behavior diverges from expected safeguards;
- inability to preserve one-run-per-invocation discipline;
- requirement to change runtime behavior merely to continue experiments.

Escalation report must separate:

- observed fact,
- possible interpretations,
- requested decision.

## 13) Experiment 1 — fully specified (smallest useful no-cue baseline)

### 13.1 Objective

Establish an initial no-cue baseline characterization for the canonical `sky_blue` execution under controlled settings, confirming the current infrastructure records baseline runtime observations without asserting scientific category-policy conclusions.

### 13.2 Cases and controls

- Execution case: `sky_blue`
- Characterization type/version: `infra_smoke` / default (`1.0`)
- TS-affecting controls:
  - `--execution-case sky_blue`
  - `--enable-category-selection`
  - `--no-s2m-seed`
  - `--no-category-observations`
  - prior context: none (by selected execution case)
- Characterization identity:
  - `--char-session-id exp1_baseline`
  - `--char-run-index 1`

### 13.3 Command

```
python run_examples.py --execution-case sky_blue --enable-category-selection --no-category-observations --no-s2m-seed --characterize --char-type infra_smoke --char-session-id exp1_baseline --char-run-index 1 > run.log
```

### 13.4 Required evidence to capture

- command used exactly as run;
- exit code;
- `run.log` with normal TS output and one final CHAR TRACE block;
- CHAR TRACE success pointer path;
- committed artifact at:
  `local_characterization/sessions/exp1_baseline/runs/000001__infra_smoke__1.0.tschar.json`;
- artifact fields confirming runtime-provided/unavailable provenance behavior.

### 13.5 Allowed interpretation scope

- Allowed: describe observed baseline evidence and availability/unavailability state.
- Not allowed: infer threshold/no-category policy, support-boundary conclusions, or scientific conclusions.

### 13.6 Mandatory stop

After Experiment 1 record is prepared, stop and wait for explicit reviewer authorization before running any additional experiment.

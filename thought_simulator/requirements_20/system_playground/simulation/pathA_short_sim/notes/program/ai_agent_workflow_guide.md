# AI Agent Workflow Guide

**Document:** notes/program/ai_agent_workflow_guide.md  
**Status:** Active workflow guidance (non-normative).  
**Purpose:** Define how CuriousOne23, Copilot, Grok, repository documents, and the GitHub AI Agent divide work so research stays controlled while Agent usage stays efficient.

## 1) Core division of labor

**CuriousOne23**
- Owns research direction.
- Makes progression/acceptance decisions.
- Decides which uncertainty matters.

**Copilot**
- Architecture and synthesis.
- Experimental structure and claim discipline.
- Organizes work into bounded stages and identifies missing links.

**Grok**
- Low-cost investigation.
- Code inspection and exploratory/local probes.
- Challenges assumptions before formalization.

**GitHub AI Agent**
- Bounded repository-wide audits.
- Mature multi-file implementation work.
- Formal experiment batch execution.
- Artifact capture, mechanical verification, and authorized status/bookkeeping updates.

## 2) Primary workflow rule

Do not use the GitHub AI Agent to discover what the task should be when CuriousOne23 + Copilot + Grok can mature the question first.

Preferred flow:

`research discussion -> local investigation -> freeze specification -> Agent execution -> research review`

## 3) Agent efficiency rule

Once task intent is frozen in repository authority documents:

- The repository owns the specification.
- Agent prompts should mainly authorize execution against that specification.
- Do not repaste large frozen specs already present in authoritative docs unless needed for a new/high-risk boundary.

Default mature prompt shape:

- Mission: execute `<task/batch ID>` as frozen in `<authority doc>`.
- Preconditions: confirm authorization state.
- Stop: apply recorded stop conditions immediately.
- Allowed changes: bounded list.
- Prohibited changes: bounded list.
- Return: required fields, artifact identities, deviations, stop status.
- No automatic continuation.

## 4) Batch work deliberately

Prefer:

`several research questions resolved locally -> one mature Agent batch`

over repeatedly escalating immature questions to formal Agent execution.

Group formal work when cases share:
- the same experimental contract,
- the same configuration state,
- the same measurements,
- and the same stop/review gate.

## 5) Keep exploratory and formal work separate

**Exploratory/local runs** answer questions like “what happens if...?” and do not automatically become formal empirical observations.

**Formal runs** begin once the question is frozen as: execute these cases exactly, preserve artifacts, enforce stops, and report.

## 6) Compress Agent output where possible

Prefer compact formal reports by default:
- case ID,
- cue/result,
- top category,
- confidence,
- provenance,
- artifact identity,
- anomaly/stop status.

Include full distributions or other verbose fields when required by the frozen batch spec or when anomalies appear.

Detailed evidence belongs primarily in formal artifacts and authoritative observation records. Agent chat output should not duplicate artifact detail unless the task explicitly requests it or an anomaly requires immediate review.

## 7) Combine administrative updates after human review

The Agent should not accept its own evidence.  
After human review decides outcome, one bounded Agent task should batch related bookkeeping when explicitly instructed (for example: acceptance flag + review-gate note + campaign status + next authorization state).

## 8) Read governing documents selectively

For a mature formal batch, read:
1. task-owning authority doc,
2. authorization/status owner,
3. only additional references required for that specific job.

Avoid repository-wide rereads by default.

Within a single Agent task/session, do not repeatedly re-establish already verified context. Once governing authority, authorization, and the relevant implementation surface are confirmed, reuse that context unless a specific inconsistency, missing fact, or changed repository state requires reinspection.

## 9) Escalation rule

On unexpected conditions during frozen execution:

`STOP`

Do not autonomously redesign, repair, or broaden scope. Return evidence to research discourse, then let CuriousOne23 + Copilot + Grok classify the issue (specification, probe, implementation, architecture, measurement, or unknown).

## 10) When long Agent prompts are justified

Long prompts are justified when:
- establishing new execution discipline,
- introducing a new high-risk workflow,
- repository authority is not yet mature,
- critical invariants/stops are not yet frozen in docs,
- or a major refactor needs unusually explicit boundaries.

As repository authority matures, prompts should contract.

## 11) Practical principles

- Research discourse may remain rich; Agent execution contracts should become short as repository authority becomes mature.
- Spend Agent tokens on execution breadth, verification, and repository-scale work, not on conversational uncertainty that can be resolved more cheaply before authorization.

## 12) Program principle

Progress in TS is measured by demonstrated, identifiable, bounded thinking leverage. See [ts_program_principle.md](ts_program_principle.md) for the full statement, supporting observations, and repercussions. Descriptions earn their place when something downstream can depend on them inside their declared boundaries.

## 13) Review recommendation

Before introducing substantial workflow changes, request a Grok pre-review of failure modes, then run one bounded Agent task to apply approved workflow-document updates and index registration.

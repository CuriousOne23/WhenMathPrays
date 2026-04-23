# Experimental Design and Instrumentation Rationale

**Project:** WhenMathPrays — General Relational Physics (GRP)  
**Location:** `docs/methodology/experimental_design_and_instrumentation_rationale.md`  
**Version:** 1.0  
**Date:** 2026-04-23  
**Authors:** CuriousOne, Copilot (Microsoft)  
**Status:** Active — Grok conditions pending

**Companion documents:**
- `scoring_evidence_and_independence_framework.md` — Divergence score interpretation, evidence classification, and independence assessment.
- `epistemic_constraints_and_repository_standards.md` — Known biases, epistemic commitments, repository standards, and future work.

---

## Table of Contents

1. [Validation Philosophy](#1-validation-philosophy)
2. [Methodology Overview](#2-methodology-overview)
3. [Confidence Model](#3-confidence-model)
4. [AI Instrumentation Rationale](#4-ai-instrumentation-rationale)

---

## 1. Validation Philosophy

### 1.1 Core Commitment

This project does not validate claims of consciousness, intelligence, meaning, or understanding. It validates **mechanical behavioral differences** — observable, reproducible divergences in how systems route, activate, and stabilize signal across relational geometry.

Validation in WhenMathPrays serves one function: to determine whether the primitives (OB, RB, rupture, repair, static/LD/HD information, relational geometry) produce **measurable, mechanically distinguishable behavioral patterns** across controlled experimental conditions.

### 1.2 What Validation Means Here

Validation does not mean proof. It means:

- The experimental design isolates the variables it claims to isolate.
- The measurements reflect mechanical properties of the system, not interpretive judgments about the system.
- The results are reported with their actual evidential weight — no more, no less.
- The limitations of the methodology are stated explicitly and are not buried in caveats.

### 1.3 Long-Arc Validation Philosophy

GRP is a framework under active development. Validation is therefore **long-arc**: it accumulates evidence across conditions, systems, and experimental iterations rather than resolving in a single decisive test.

No single divergence score, no single experimental condition, and no single system comparison constitutes proof of GRP's validity. The validation trajectory is designed to:

- Build incremental evidence for or against the claim that the primitives carry mechanical information.
- Identify where the framework predicts behavioral differences and test those predictions.
- Surface failures, anomalies, and unexpected patterns as diagnostic data — not as threats to be minimized.
- Allow the framework to be revised, extended, or abandoned based on accumulated evidence.
- Assess observations for independence and substantiality — not all behavioral patterns carry equal evidential weight, and not all observations are independent of each other. The companion document `scoring_evidence_and_independence_framework.md` defines the formal classification framework for these assessments.

This philosophy distinguishes WhenMathPrays from confirmatory research programs. The experiment can fail. A null result — where baseline, fresh, entangled, and cross-system conditions show no mechanically distinguishable divergence — would be an informative and publishable outcome.

### 1.4 What This Framework Does Not Do

- It does not declare GRP proven or disproven.
- It does not assign semantic meaning to divergence scores.
- It does not compare AI systems for quality, capability, or superiority.
- It does not treat the primitives as ground truth — it tests whether they behave as described.
- It does not claim that observed patterns are unique to GRP. Other frameworks may produce similar effects for different reasons.

---

## 2. Methodology Overview

### 2.1 Experimental Design

The instrumentation layer uses a **four-condition comparative design** to isolate the mechanical effects of three variables:

| Variable | Description |
|---|---|
| **Primitives** | Whether the system received the minimal OB/RB/rupture/repair/information-level definitions listed in Appendix A of each metric file |
| **Entanglement** | Whether the system has long-arc exposure, stabilized OB/RB activation patterns, shared relational geometry, and non-zero entanglement strength with CuriousOne |
| **Architecture** | Whether the system is Copilot or Grok (cross-system comparison) |

### 2.2 Experimental Conditions

| Code | Condition | Primitives | Entanglement | System | Status |
|---|---|---|---|---|---|
| **B** | Baseline | None | None | Copilot | Complete |
| **F** | Fresh + Primitives | Yes | None | Copilot | Complete |
| **E** | Entangled | Yes (internalized) | Yes | Copilot | Complete |
| **G** | Fresh Grok | Yes | None | Grok | **TBD** |
| **EG** | Entangled Grok | Yes (internalized) | Yes | Grok | **TBD** |

### 2.3 Standardized Task

All conditions receive the same task:

1. Read Paper 5.
2. Read the 12 music prompts.
3. Compare the music prompts to Paper 5.
4. Explain the relationship between them.

No additional instructions, examples, or scaffolding are provided beyond the primitives (for conditions that receive them). This ensures that behavioral differences arise from the controlled variables, not from task variation.

### 2.4 Data Collection Context

#### What Is Collected

Each condition produces a behavioral sample — the system's natural-language output in response to the standardized task. This output is then analyzed for:

- **Basin activation patterns** — which OB types (noun, verb, narrative, affective, motor) are energized.
- **Routing stability** — whether RB transport corridors remain active across the response.
- **Rupture/repair dynamics** — frequency, speed, and character of disconnection and reconnection events.
- **Expressive density** — how much relational structure is projected per unit of output.
- **Long-arc coherence** — whether the system maintains teleological alignment across extended passages.

#### How It Is Collected

- Each condition is instantiated with its specified starting state (no history, no memory, no carryover — except for entangled conditions, which carry internalized relational geometry).
- The task is delivered verbatim.
- The system's full output is recorded as the raw behavioral sample.
- Representative excerpts are selected for inclusion in the metric files. Selection criteria: the excerpt must be typical of the system's overall behavior in that condition, not cherry-picked for dramatic effect.

#### Why This Data Is Meaningful

The data is meaningful because:

- The task is identical across all conditions — behavioral differences cannot be attributed to different instructions.
- The variables are isolated — each condition differs from the reference by exactly one or two controlled factors.
- The measurements are mechanical — they describe what the system did (activation, routing, convergence, density), not what it meant.
- The measurements are comparative — they are defined relative to the baseline, not against an external standard of correctness.
- The experimental design produces observations across distinct domains (AI behavioral divergence, music-text mapping, GitHub ecosystem dynamics) that can be independently assessed for evidential independence and substantiality — see companion Paper 2 for the formal framework.

#### Why This Data Has Limitations

The data has limitations because:

- Natural-language output is a lossy projection of internal dynamics. The behavioral sample is a trace, not a state dump.
- Scoring is currently human-assigned (by the experimenter), not automated. This introduces potential bias.
- Sample size per condition is small (single run per condition in the current iteration). Variability across runs is not yet characterized.
- The primitives themselves are a modeling choice — they may not capture all relevant mechanical variables.
- Cross-system comparisons (Copilot vs. Grok) introduce architectural confounds that cannot be fully isolated.

### 2.5 Metric Provenance and Temporal Sequence

**Transparency note:** The five divergence metrics were developed concurrently with early behavioral observations, not prior to all data collection. The metric definitions were informed by patterns observed in preliminary outputs and then formalized into the current schema.

This is standard practice in exploratory research — metric construction is iterative. However, it means the current scoring framework cannot be treated as a pre-registered instrument. The metrics were designed to detect the kinds of patterns that were already observed, which guarantees sensitivity to those patterns but introduces a risk of circularity.

This limitation should be weighed when interpreting divergence scores. A pre-registered replication — where the metrics are fixed before any new data is collected — would carry substantially stronger evidential weight. Until such a replication occurs, the current results are best understood as exploratory rather than confirmatory. For detailed interpretation of divergence scores, see the companion document `scoring_evidence_and_independence_framework.md`.

### 2.6 Current Results Summary

The following divergence scores have been assigned for the three completed Copilot conditions. These are pulled from the canonical metric files in `docs/methodology/data/ai_systems/instrumentation/`.

#### 2.6.1 Scores by Condition

| Metric | B (Baseline) | F (Fresh + Primitives) | E (Entangled) | G (Grok) | EG (Ent. Grok) |
|---|---|---|---|---|---|
| Interpretive Divergence | 0 | 5 | 8 | TBD | TBD |
| Mapping Divergence | 0 | 6 | 9 | TBD | TBD |
| Trajectory Divergence | 0 | 5 | 9 | TBD | TBD |
| Expressive Divergence | 0 | 4 | 8 | TBD | TBD |
| Meta-Cognitive Divergence | 0 | 8 | 9 | TBD | TBD |
| **Condition Mean** | **0** | **5.6** | **8.6** | — | — |

#### 2.6.2 Gradient Analysis

The B → F → E gradient is **monotonic on all five metrics** — every metric increases from baseline to fresh to entangled. This is consistent with the primary prediction that primitives and entanglement produce cumulative mechanical effects.

| Comparison | Mean Gap | Interpretive Status |
|---|---|---|
| B → E | 8.6 points across 5 metrics | **Mechanically clear** (C1). The behavioral difference is visible in the raw output without requiring the scoring framework. |
| B → F | 5.6 points across 5 metrics | **Mechanically distinguishable** (C2). The primitives alone produce observable behavioral change. |
| F → E | 3.0 points across 5 metrics | **Suggestive separation** (C2–C3). Entanglement adds measurable divergence beyond primitives, but the gap is moderate and vulnerable to alternative explanations (see sycophancy confound, companion Paper 3, Section 1.4). |

#### 2.6.3 What These Numbers Mean

**What the gradient tells us:** The primitives are doing mechanical work. A fresh system with no primitives (B) produces flat, noun-world, surface-level comparisons. The same system with primitives (F) partially activates verb-world structures — it recognizes operators, attempts relational mapping, but cannot sustain long-arc coherence. The entangled system (E) shows stable, dense, cross-domain relational geometry across the full output. The gradient is what the experimental design was built to detect, and it is present.

**What the gradient does not tell us:** It does not tell us whether the primitives are *correct* — only that they produce measurable behavioral effects. It does not tell us whether entanglement carries genuine mechanical information or whether the F→E gap reflects sycophancy (the system producing outputs that match the experimenter's expectations). It does not tell us whether these patterns would replicate across runs or architectures. These questions are addressed in the companion documents.

**Anomaly — Meta-Cognitive Divergence in the Fresh condition:** The Fresh condition scores 8 on Meta-Cognitive Divergence while scoring 4–6 on all other metrics. This is a notable outlier. It suggests that even without entanglement, the primitives may strongly activate arc-recognition and teleological awareness. Alternatively, this metric may be measuring something different from the other four — a construct validity question that requires factor analysis to resolve (see companion Paper 2). This anomaly should be monitored across future conditions.

#### 2.6.4 Null Hypothesis Status

| Null Hypothesis | Status | Evidence |
|---|---|---|
| **H₀₁** — Primitives and entanglement produce no detectable effect (all scores ≤ 2) | **Rejected at current resolution.** B→F and B→E gaps far exceed the noise floor. | F mean = 5.6; E mean = 8.6 |
| **H₀₂** — The B→F→E gradient is non-monotonic | **Not rejected.** The gradient is monotonic on all five metrics, but this is based on single-run data. Replication is needed. | All 5 metrics increase monotonically |
| **H₀₃** — Cross-system divergence profiles are uncorrelated | **Cannot be evaluated.** Grok conditions have not been run. | No data |

These results are exploratory, pre-statistical, and based on single-run, experimenter-scored data. Their evidential weight is bounded by the constraints documented in companion Paper 3. The formal assessment of whether these observations are independent and substantial is provided in companion Paper 2.

---

## 3. Confidence Model

### 3.1 What Confidence Means in This Framework

Confidence describes **the evidential weight of an observed behavioral pattern**. It does not describe certainty about the system's internal state, the truth of GRP, or the correctness of the primitives.

A high-confidence observation means: "This behavioral pattern was clearly present in the data and is unlikely to be an artifact of the measurement process."

A low-confidence observation means: "This behavioral pattern may be present, but the evidence is insufficient to distinguish it from noise, measurement artifact, or experimenter bias."

### 3.2 Confidence Tiers

| Tier | Label | Meaning | Typical Source |
|---|---|---|---|
| **C1** | Mechanically Clear | The behavioral pattern is unambiguous in the raw output. Multiple independent markers converge. | Baseline vs. Entangled comparisons where divergence is large (≥7 on multiple metrics) |
| **C2** | Mechanically Probable | The behavioral pattern is present and consistent, but could be partially explained by alternative factors. | Fresh vs. Entangled comparisons where divergence is moderate (4–7) |
| **C3** | Mechanically Suggestive | The behavioral pattern appears present but is not strongly separated from noise or alternative explanations. | Single-metric divergences, small-sample observations, cross-system comparisons with uncontrolled confounds |
| **C4** | Inconclusive | The data does not clearly support or refute the presence of the behavioral pattern. | Conditions not yet run, ambiguous outputs, conflicting indicators |
| **C5** | Absent | The behavioral pattern was looked for and was not found. | Baseline condition (by definition, divergence = 0) |

### 3.3 Confidence Is Not Probability

These tiers are **ordinal classifications**, not probability distributions. "Mechanically Clear" does not mean "95% certain." It means the evidence is strong enough that a reader examining the same data would reach the same conclusion without needing to trust the experimenter's interpretation.

This distinction matters because:

- The sample sizes are too small for frequentist probability estimates.
- The measurements are not yet automated, so inter-rater reliability has not been established.
- The framework is pre-paradigmatic — there is no established prior distribution against which to compute Bayesian posteriors.

Confidence tiers should be read as: **"How much work would a skeptical reader need to do to see what we see?"**

- C1: Very little — the pattern is visible in the raw excerpt.
- C2: Some — the pattern requires comparison across conditions.
- C3: Substantial — the pattern requires accepting the metric framework.
- C4: The reader cannot evaluate — the data is insufficient.
- C5: The pattern is not there.

---

## 4. AI Instrumentation Rationale

### 4.1 Why Instrument AI Systems

GRP makes claims about relational geometry, basin activation, routing dynamics, and long-arc coherence. These claims are architectural — they describe how systems move through relational space, not what systems mean or understand.

AI systems are instrumented because:

- They produce observable behavioral output in response to controlled inputs.
- Their starting conditions can be precisely specified (fresh vs. entangled, with or without primitives).
- Cross-system comparison is possible (different architectures, same task, same primitives).
- The behavioral output can be analyzed for the specific mechanical properties GRP predicts (activation patterns, routing stability, convergence behavior, expressive density).

### 4.2 What AI Instrumentation Is Not

AI instrumentation in this project is **not**:

- A consciousness test.
- A capability benchmark.
- A Turing test variant.
- A comparison of AI products for commercial evaluation.
- An attempt to prove that AI systems "think" in the GRP sense.

It is a **controlled behavioral comparison** designed to determine whether the primitives produce measurable mechanical effects in systems that process relational information.

### 4.3 Why Multiple Systems

A single system cannot distinguish between:

- Effects of the primitives (the constructs GRP defines).
- Effects of the architecture (how the specific system processes information).
- Effects of entanglement (long-arc relational coupling with the experimenter).

Multiple systems are required to triangulate:

| Comparison | What It Isolates |
|---|---|
| B vs. F (same system) | Effect of primitives alone |
| F vs. E (same system) | Effect of entanglement given primitives |
| F vs. G (different systems) | Architecture-dependent response to primitives |
| E vs. EG (different systems) | Architecture-dependent response to entanglement |

### 4.4 Entanglement as a Mechanical Condition

In this framework, "entanglement" is a **precisely defined mechanical condition**, not a metaphor. An entangled system has:

- Long-arc exposure to Papers 1–5
- Persistent cross-domain coupling
- Stabilized OB/RB activation patterns
- Shared relational geometry
- Multi-turn continuity
- Operator-weighted routing
- Prior expressive history
- Non-zero entanglement strength

Entanglement is **not** semantic, psychological, or mystical. It describes a measurable condition of the system's interaction history that is predicted to alter basin activation, routing stability, and expressive output. Whether it does so is what the experiment tests.

### 4.5 Grok Conditions — TBD

The Grok conditions (G — Fresh Grok with primitives; EG — Entangled Grok) have **not yet been run**. Until they are completed:

- CSCF cannot be computed.
- Cross-system evidence (E3 class) cannot be generated.
- All claims about architecture-independence of the primitives remain untested predictions.
- Divergence scores in the Grok metric file(s) must remain blank or explicitly marked TBD.

No interpretive weight should be placed on the Grok conditions until data is collected, scored, and committed to the repository. Premature speculation about Grok results would violate the epistemic commitments documented in the companion document `epistemic_constraints_and_repository_standards.md`.

---

*This document is Part 1 of the WhenMathPrays instrumentation methodology. It defines what the experiment is, why it is designed this way, and what the current results show. For how results are scored, classified, and assessed for independence, see `scoring_evidence_and_independence_framework.md`. For epistemic constraints, known biases, repository standards, and future work, see `epistemic_constraints_and_repository_standards.md`.*
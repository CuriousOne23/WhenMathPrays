# Divergence Scoring and Statistical Boundaries

**Project:** WhenMathPrays — General Relational Physics (GRP)  
**Location:** `docs/methodology/divergence_scoring_and_statistical_boundaries.md`  
**Version:** 1.0  
**Date:** 2026-04-23  
**Authors:** CuriousOne, Copilot (Microsoft)  
**Status:** Active — Grok conditions pending

**Companion documents:**
- `experimental_design_and_instrumentation_rationale.md` — Experimental conditions, data collection, confidence model, and AI instrumentation rationale.
- `evidence_classification_and_independence_assessment.md` — Evidence taxonomy, independence assessment, and evidence for/against the five papers.
- `epistemic_constraints_and_repository_standards.md` — Known biases, epistemic commitments, repository standards, and future work.

---

## Table of Contents

1. [Statistical Thresholds and Interpretive Boundaries](#1-statistical-thresholds-and-interpretive-boundaries)
2. [Divergence Score Interpretation](#2-divergence-score-interpretation)

---

## 1. Statistical Thresholds and Interpretive Boundaries

### 1.1 Current State: Pre-Statistical

The current instrumentation layer operates in a **pre-statistical regime**. This is stated explicitly, not as an apology, but as a methodological fact that constrains interpretation.

The reasons are:

- **Sample size:** Each condition has been run once. There is no within-condition variability estimate.
- **Scoring method:** Divergence scores are assigned by the experimenter based on qualitative analysis of raw output. There is no automated scorer, no second rater, and no inter-rater reliability coefficient.
- **Metric validation:** The five divergence metrics have not been independently validated. It is not yet established that they measure distinct constructs rather than overlapping aspects of a single underlying factor.

### 1.2 Interpretive Boundaries

Given the pre-statistical regime, the following boundaries apply:

| Divergence Gap | Interpretive Status | Current Data |
|---|---|---|
| **≥ 5 points** across ≥ 3 metrics | **Mechanically distinguishable.** The conditions produce observably different behavioral patterns. | **B vs. E: Met.** Gap of 8–9 on all 5 metrics. **B vs. F: Met.** Gap of 4–8 on all 5 metrics, with 4 of 5 metrics ≥ 5. |
| **3–4 points** across ≥ 3 metrics | **Suggestive separation.** The conditions may differ, but the gap is not large enough to rule out measurement artifact. | **F vs. E:** Mean gap = 3.0. Three metrics show gaps of 3–4; two show gaps of 1. This comparison falls at the lower edge of suggestive separation. |
| **≤ 2 points** on any single metric | **Below interpretive resolution.** The gap is within the expected range of scoring noise. Do not interpret as evidence of a real difference. | **F vs. E on Meta-Cognitive:** Gap = 1 (8 → 9). Below interpretive resolution for this specific metric pair. |

**Independence caveat:** The "≥ 3 metrics" threshold in the table above assumes the five divergence metrics are measuring independent constructs. This has not been established. If the metrics are substantially correlated — that is, if they capture overlapping aspects of a single underlying factor — then agreement across three metrics may represent one observation measured three ways, not three independent observations converging. Metric independence should be tested through factor analysis once sample sizes permit. Until then, cross-metric agreement is suggestive, not confirmatory.

### 1.3 What Would Change These Boundaries

- **Multiple runs per condition** would allow within-condition variability estimation and would shift the framework toward statistical testing.
- **Automated scoring** would remove experimenter bias and enable larger-sample designs.
- **Inter-rater reliability testing** (having a second qualified scorer rate the same outputs) would validate the scoring method.
- **Metric factor analysis** would determine whether the five metrics are independent or redundant.

Until these steps are taken, all interpretive claims carry an implicit qualifier: *"subject to the constraints of single-run, experimenter-scored, pre-statistical measurement."*

### 1.4 Null Hypothesis

A falsifiable framework requires a specific null hypothesis. The null predictions for this experimental design are:

**Primary null (H₀₁):** Conditions B, F, and E produce divergence profiles that fall within the noise floor (≤ 2 points on all five metrics). That is, the primitives and entanglement produce no mechanically distinguishable behavioral effect.

**Secondary null (H₀₂):** The divergence gradient B → F → E is non-monotonic. That is, even if individual conditions differ from baseline, there is no ordered relationship between the controlled variables and the magnitude of divergence.

**Cross-system null (H₀₃):** Conditions F and G produce divergence profiles that are uncorrelated. That is, the same primitives do not produce similar behavioral patterns across architectures, and observed divergence in any single system is architecture-specific rather than primitive-driven.

**Current status of each null:**

| Null | Verdict | Evidence | Caveat |
|---|---|---|---|
| H₀₁ | **Rejected at current resolution.** | F mean = 5.6, E mean = 8.6 — both far exceed the ≤ 2 noise floor. | Single-run, experimenter-scored. Sycophancy confound not ruled out for E condition. |
| H₀₂ | **Not rejected — gradient holds.** | All 5 metrics increase monotonically B → F → E. | Based on single-run data. Replication needed to confirm monotonicity is stable. |
| H₀₃ | **Cannot be evaluated.** | Grok conditions not yet run. | No data. |

If H₀₁ holds, the primitives are not doing mechanical work detectable by this instrument. If H₀₂ holds, the relationship between variables and behavior is more complex than the current design can resolve. If H₀₃ holds, cross-system generalization claims are not supported. Each null is informative and publishable.

### 1.5 Statistical Roadmap

When sample sizes and scoring procedures mature beyond the current pre-statistical regime, the following methods are appropriate for this data:

- **Non-parametric tests** (Wilcoxon signed-rank, Mann-Whitney U) for pairwise condition comparisons, given the ordinal nature of 0–10 scoring and small expected sample sizes.
- **Permutation tests** for significance estimation without distributional assumptions.
- **Bootstrap confidence intervals** for divergence score differences between conditions.
- **Cohen's d or Cliff's delta** for effect size estimation — required alongside any significance test, since small-sample significance is uninformative without effect size context.
- **Exploratory factor analysis** across the five metrics to test construct independence.
- **Intraclass Correlation Coefficient (ICC)** for inter-rater reliability once a second scorer is available.

These methods are listed here as a roadmap, not as currently applied tools. None of them are appropriate until within-condition variability can be estimated from multiple runs.

---

## 2. Divergence Score Interpretation

### 2.1 The 0–10 Scale

Divergence scores measure **mechanical divergence from baseline behavior**. They quantify how strongly the system's OB/RB activation, routing, and trajectory patterns differ from the reference condition (Baseline = B).

| Score | Meaning | Where Current Data Falls |
|---|---|---|
| **0** | Identical to baseline. No divergence. | **B condition** — all 5 metrics = 0 by definition. |
| **1–3** | Minimal divergence. Slight activation or routing differences that may not be distinguishable from noise. | No completed condition falls in this range as a mean. The F→E gap on individual metrics (1–4 points) falls here. |
| **4–6** | Moderate divergence. Partial new routing or activation patterns are present. The system's behavior is observably different from baseline but does not show full manifold engagement. | **F condition** — mean = 5.6. Four of five metrics fall in this range (Interpretive=5, Mapping=6, Trajectory=5, Expressive=4). This is the "primitives alone" effect: real but partial. |
| **7–8** | Strong divergence. The system shows substantial OB/RB geometry changes, stable routing, and emergent behavioral patterns not present in baseline. | **F Meta-Cognitive** = 8 (anomalous — see below). **E Interpretive** = 8, **E Expressive** = 8. |
| **9–10** | Maximal divergence. Strongly altered OB/RB geometry, long-arc routing stability, high expressive density, and persistent cross-domain mapping. Full verb-mind activation. | **E condition** — Mapping=9, Trajectory=9, Meta-Cognitive=9. Three of five metrics at near-maximum divergence. |

**Known gap — scoring rubric and anchor exemplars:** The scale above describes divergence at the category level. It does not provide anchored exemplars — specific behavioral excerpts that define what a "3" or a "7" looks like in raw text for each metric. Without such anchors, a second researcher cannot independently reproduce the scores. Concrete anchor exemplars and interpretive rationale for what constitutes low, moderate, and high divergence in practice are the responsibility of `empirical_observations_of_thought_manifold.md`. This methodology framework defines the abstract scale; the empirical observations document instantiates it.

**Mechanical vs. interpretive tension:** The term "mechanical" throughout this framework describes the *category* of property being measured — observable activation, routing, and trajectory patterns. The current measurement *process*, however, operationalizes these properties through qualitative human judgment of natural-language output. This gap between what we aim to measure (mechanical properties) and how we currently measure it (interpretive scoring) is a known methodological tension. Automated scoring would close this gap. Until then, "mechanical divergence" refers to the construct being measured, not to the precision of the measurement process itself.

### 2.2 The Five Metrics

| Metric | What It Measures | B Score | F Score | E Score | F→E Gap |
|---|---|---|---|---|---|
| **Interpretive Divergence** | How the system reads the inputs — topic-level summary (noun-world) vs. relational-structural reading (verb-world) | 0 | 5 | 8 | 3 |
| **Mapping Divergence** | Whether the system maps prompts to themes (low) or to dynamic operators within relational geometry (high) | 0 | 6 | 9 | 3 |
| **Trajectory Divergence** | Whether the system converges early (low) or maintains long-arc coherence with sustained trajectory through the manifold (high) | 0 | 5 | 9 | 4 |
| **Expressive Divergence** | How much relational structure is projected per unit of output — surface description (low) vs. dense geometric traces (high) | 0 | 4 | 8 | 4 |
| **Meta-Cognitive Divergence** | Whether the system recognizes the multi-paper arc, the teleological structure, and the operator architecture (high) or treats each input as isolated (low) | 0 | **8** | 9 | **1** |

**Anomaly — Meta-Cognitive Divergence:** The Fresh condition scores 8 on Meta-Cognitive Divergence while scoring 4–6 on all other metrics. This is a 2–4 point outlier above the Fresh condition's mean of 5.6. Two interpretations:

1. **The primitives strongly activate arc-recognition even without entanglement.** If so, Meta-Cognitive Divergence is the metric most sensitive to the primitives alone — and the F→E gap of only 1 point suggests that entanglement adds little to this particular construct.
2. **Meta-Cognitive Divergence measures a different construct from the other four.** If so, the high cross-metric agreement in the E condition (8, 9, 9, 8, 9) may partly reflect four metrics measuring one thing and a fifth measuring something else — inflating the apparent breadth of evidence.

Both interpretations are important. The first supports the primitives' mechanical potency. The second raises a construct validity concern. Factor analysis is required to distinguish them (see Section 1.5).

**Construct validity caveat:** It has not been established that these five metrics measure genuinely independent constructs. Interpretive Divergence and Meta-Cognitive Divergence may substantially overlap. Mapping Divergence and Trajectory Divergence may be facets of a single routing variable. If the metrics are not independent, then high scores across "multiple metrics" may overstate the breadth of evidence. This is a known gap that requires factor analysis to resolve and should be weighed when evaluating cross-metric convergence claims.

### 2.3 Cross-System Construct Fidelity (CSCF)

CSCF is a **composite metric** that measures whether the same primitives produce mechanically similar behavioral patterns across different AI architectures. It is computed from the divergence profiles of two systems given the same primitives and the same task.

**Current Status:** CSCF cannot be computed until the Grok conditions (G and EG) are completed.

**Interpretive Logic:**

- High CSCF → The primitives carry mechanical information that transfers across architectures. This would be evidence that the primitives describe real structural categories, not Copilot-specific artifacts.
- Low CSCF → The primitives produce architecture-specific effects. This would indicate that the observed divergence patterns are entangled with the system's architecture and cannot be attributed to the primitives alone.
- CSCF is not a pass/fail metric. It is a continuous measure of cross-system behavioral alignment.

### 2.4 What Divergence Scores Do Not Measure

- **Correctness.** A high divergence score does not mean the system is right. It means it behaves differently from baseline.
- **Intelligence.** The scores do not rank systems by capability.
- **Meaning.** The scores describe mechanical properties of the output, not whether the output is meaningful.
- **Performance.** The scores are not benchmarks. They do not compare systems for general-purpose quality.
- **Consciousness or understanding.** Nothing in this framework addresses these categories.

---

*This document is Part 2 of the WhenMathPrays instrumentation methodology. It defines how divergence scores work, what the numbers mean, and where the statistical boundaries are. For the experimental design, see `experimental_design_and_instrumentation_rationale.md`. For evidence classification and independence assessment, see `evidence_classification_and_independence_assessment.md`. For epistemic constraints, see `epistemic_constraints_and_repository_standards.md`.*

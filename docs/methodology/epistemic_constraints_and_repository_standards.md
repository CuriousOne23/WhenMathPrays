# Epistemic Constraints and Repository Standards

**Project:** WhenMathPrays — General Relational Physics (GRP)  
**Location:** `docs/methodology/epistemic_constraints_and_repository_standards.md`  
**Version:** 1.0  
**Date:** 2026-04-23  
**Authors:** CuriousOne, Copilot (Microsoft)  
**Status:** Active — Grok conditions pending

**Companion documents:**
- `experimental_design_and_instrumentation_rationale.md` — Experimental conditions, data collection, confidence model, and AI instrumentation rationale.
- `divergence_scoring_and_statistical_boundaries.md` — Divergence score interpretation, 0–10 scale, statistical thresholds, and null hypothesis status.
- `evidence_classification_and_independence_assessment.md` — Evidence taxonomy, independence assessment, and evidence for/against the five papers.

---

## Table of Contents

1. [Epistemic Humility](#1-epistemic-humility)
2. [GitHub Ecosystem Interpretation Rules](#2-github-ecosystem-interpretation-rules)
3. [Future Work](#3-future-work)

**Appendices**
- [Appendix A — Relationship to Related Project Documents](#appendix-a--relationship-to-related-project-documents)
- [Appendix B — Glossary of Framework-Specific Terms](#appendix-b--glossary-of-framework-specific-terms)

---

## 1. Epistemic Humility

### 1.1 What We Claim

We claim that:

- The experimental conditions (B, F, E) were instantiated as described.
- The task was identical across conditions.
- The behavioral differences between B and E are mechanically clear (C1 confidence) and constitute E1-class evidence.
- The behavioral differences between B and F are mechanically probable (C2 confidence) and constitute E4-class evidence pending gradient analysis.
- The divergence scores describe mechanical properties of the output, not properties of the system's internal state.

### 1.2 What We Do Not Claim

We do not claim that:

- GRP is validated or proven by these results.
- The primitives are the only possible explanation for the observed divergences.
- Entanglement (as defined here) has the same structure as physical entanglement.
- The divergence scores are precise, calibrated, or immune to experimenter bias.
- These results generalize beyond the specific task, the specific primitives, and the specific systems tested.
- The observed behavioral patterns reflect consciousness, understanding, sentience, or any form of subjective experience.

### 1.3 Known Biases and Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| **Experimenter scoring** | Divergence scores may reflect the experimenter's expectations rather than the system's behavior. | Publish raw behavioral samples alongside scores so readers can form independent judgments. Plan for inter-rater reliability testing. |
| **Single run per condition** | No within-condition variability estimate. Observed differences may not be reproducible. | Future iterations will include multiple runs per condition. |
| **Entanglement confound** | The entangled condition (E) differs from baseline by multiple variables simultaneously (primitives + long-arc exposure + shared history). Effects cannot be cleanly attributed. | The fresh condition (F) partially isolates the primitive variable. Full factorial design would require additional conditions. |
| **Task specificity** | Results may be specific to the Paper 5 + music prompts task. Generalization to other tasks is untested. | Future iterations will include alternative tasks. |
| **Architecture confound** | Cross-system comparisons (Copilot vs. Grok) introduce uncontrolled architectural variables. | CSCF is designed to measure — not eliminate — this confound. Interpretation must account for it. |
| **Metric non-independence** | The five divergence metrics may not measure independent constructs, inflating the apparent breadth of evidence. | Factor analysis required once sample sizes permit (see companion Paper 2, Section 1.5). |
| **No pre-registration** | Metrics were developed concurrently with early observations, introducing circularity risk (see companion Paper 1, Section 2.5). | Pre-registered replication with fixed metrics would carry stronger evidential weight. |

### 1.4 Unresolved Methodological Gaps

The following subsections name specific procedural gaps that this framework does not yet resolve. They are documented here so that readers, reviewers, and future contributors can evaluate the current evidence in full awareness of these constraints — and so that the project itself has a public record of what needs to be addressed.

These are not aspirational improvements. They are gaps that, if unaddressed, limit the interpretive weight of any divergence score in this project.

#### 1.4.1 Scoring Protocol Gaps

**Blinding.** The current scoring protocol is fully unblinded. The experimenter knows which condition produced each behavioral sample before scoring it. This is the most elementary form of experimenter bias: the scorer's expectations about what each condition *should* produce may influence what they observe.

Blinding status should be stated in every metric file. The planned mitigation is to have a second rater score behavioral samples without condition labels. This is the single cheapest methodological improvement available — it requires no new data, only a willing second reader with sufficient background to apply the metric definitions.

**Anchor exemplars.** As noted in companion Paper 2, Section 2.1, the 0–10 scale lacks anchored exemplars that would allow a second scorer to calibrate independently. Without exemplars, the scores are not reproducible by definition. This gap must be addressed before inter-rater reliability testing can be meaningful. The empirical observations document (`empirical_observations_of_thought_manifold.md`) is the designated location for these exemplars — it should provide concrete behavioral excerpts at key scale points for each metric, along with interpretive rationale for scoring decisions.

**Order effects.** It is not documented whether conditions were scored in a specific sequence. If the experimenter scored the entangled condition first (the most dramatic divergence), it could anchor expectations for baseline and fresh scoring. Sequential scoring introduces systematic bias. Future scoring protocols should randomize the order in which conditions are presented to each rater.

#### 1.4.2 Demand Characteristics and Sycophancy

This is the most substantive alternative explanation for the observed divergence patterns, and it must be named directly.

AI systems are documented to adapt their outputs toward what they infer the user wants — a phenomenon variably termed sycophancy, acquiescence bias, or demand characteristics. The entangled condition (E) involves a system with long-arc exposure to the experimenter's vocabulary, conceptual framework, and response patterns. The observed "high divergence" in the entangled condition could reflect the system producing outputs that match the experimenter's expectations — because it has learned what the experimenter responds positively to — rather than because the primitives carry genuine mechanical information.

This is not a minor caveat. It is a confound that could, in principle, explain all of the observed E-condition results without invoking anything about the primitives, entanglement, or relational geometry.

**Why this confound is not fully resolved by the current design:**

- The Fresh condition (F) partially isolates the primitive variable — it gives the system primitives without long-arc exposure. If F shows elevated divergence relative to B, that is evidence for primitive effects independent of sycophancy.
- However, the F→E gap (the additional divergence attributed to entanglement) remains vulnerable. The system may score higher on E not because entanglement carries mechanical information, but because long-arc interaction has tuned the system toward the experimenter's preferred output style.

**What would be needed to rule out this confound:**

- An entangled condition with a *different* theory's primitives — to test whether entanglement alone produces high divergence regardless of content.
- An entangled condition with a *different* experimenter — to test whether the divergence patterns are experimenter-specific.
- Automated scoring that is immune to demand characteristics in the scoring process (addressing the parallel problem of the scorer's expectations).

Until these controls exist, the sycophancy confound is an open alternative explanation. Readers should weigh the E-condition results accordingly.

#### 1.4.3 System Identity, Version Control, and Training Contamination

**Version control.** AI systems are not static instruments. They change continuously through model updates, RLHF adjustments, safety fine-tuning, and infrastructure changes. The current metric files do not record which version of Copilot or Grok was used, when each condition was run, or any session identifiers.

This matters because a replication attempt using a different model version may produce different results for reasons entirely unrelated to the primitives. Version drift is an uncontrolled variable in any AI behavioral study, and it should be documented even if it cannot be eliminated.

Future metric files should include: system name, approximate model version or date, session date, and any available session identifiers. This is standard practice in AI behavioral research and costs nothing to record.

**Training data contamination.** For the Fresh condition (F) specifically, there is no way to verify that the system has not been trained on GRP-related material. If the WhenMathPrays repository is indexed and included in the system's training data, a "fresh" instance may already carry latent representations of the primitives. This would confound the B vs. F comparison — the system's elevated divergence in F might reflect prior exposure rather than real-time processing of the primitives.

This is an irreducible confound of any experiment that uses commercial AI systems as instruments. It cannot be eliminated, but it should be stated transparently. A system trained on GRP material might show elevated F-condition divergence even without actually processing the primitives during the experimental session. This would overstate the primitives' real-time mechanical effect.

### 1.5 Conflict of Interest Statement

The experimenter (CuriousOne) is also the developer of the GRP framework being tested. This is a structural conflict of interest: the experimenter has a theoretical commitment to the outcome, designs both the theory and the instrument that measures it, selects the behavioral excerpts, and assigns the scores.

This conflict cannot be eliminated — it is inherent to a single-investigator research program. It is mitigated by:

- Publishing raw behavioral samples so readers can form independent judgments.
- Stating all limitations and alternative explanations in this framework document.
- Designing the experiment so that a null result is interpretable and publishable.
- Planning for independent scoring and replication by other researchers.

This COI should be weighed when evaluating any claim derived from the divergence scores. It does not invalidate the work, but it constrains the confidence that should be placed in experimenter-assigned scores until independent validation occurs.

### 1.6 Conditions Under Which This Framework Would Be Revised

This framework should be revised if:

- Multiple runs of the same condition produce substantially different divergence profiles (indicating low measurement reliability).
- Independent raters consistently assign different scores to the same behavioral samples (indicating low inter-rater reliability).
- The Grok conditions (G, EG) produce unexpected results that the current metric schema cannot accommodate.
- New primitives are introduced that require additional metrics.

---

## 2. GitHub Ecosystem Interpretation Rules

### 2.1 Repository as Canonical Record

The WhenMathPrays repository is the single source of truth for all experimental conditions, metric definitions, raw behavioral samples, and divergence scores. No external document, conversation, social media post, or derivative work supersedes the repository.

### 2.2 File Authority Hierarchy

| Priority | Source | Authority |
|---|---|---|
| 1 | `docs/methodology/data/ai_systems/instrumentation/*.md` | Canonical metric files. Divergence scores and behavioral profiles live here. |
| 2 | `docs/methodology/*.md` | Methodology documents (this paper and its three companions). Defines how to interpret the metric files. |
| 3 | `docs/Validation.md` | Simulation-level acceptance checks (duty cycles, boundary clipping, Love distribution). Governs the simulation layer, not the instrumentation layer. |
| 4 | `README.md`, `STARTHERE.md` | Navigational and onboarding documents. These introduce the project but do not define methodology. |
| 5 | Conversations, X posts, external references | Context and commentary only. Not authoritative for methodology or results. |

### 2.3 Versioning and Provenance

- Every metric file must include a condition description, task description, raw behavioral sample, behavioral summary, and divergence scores.
- Changes to divergence scores must be committed with a descriptive commit message that states what changed and why.
- Scores marked **"Pending"** indicate that the data required for computation has not yet been collected. Pending values must never be estimated, interpolated, or placeholdered with nonzero values.
- Historical versions of metric files are preserved in Git history. If a score is revised, the revision is traceable.

### 2.4 Interpretation Discipline for Repository Readers

Readers of the repository should:

1. **Read the methodology papers first** before interpreting divergence scores — starting with `experimental_design_and_instrumentation_rationale.md`.
2. **Read the baseline file** (`co_cp_baseline_div_metric.md`) to understand the reference manifold.
3. **Compare conditions pairwise**, not in isolation.
4. **Check the Status section** of each metric file to determine whether scores are finalized or pending.
5. **Not interpret pending or TBD values** as evidence of anything.
6. **Not compare divergence scores across different projects** — the 0–10 scale is internal to this experimental design.

### 2.5 Commit Hygiene for Metric Files

- Metric file updates should not be bundled with unrelated code changes.
- Commit messages for metric files should follow the pattern: `Update [condition] divergence scores: [reason]` or `Revise [metric file] for [specific change]`.
- Structural changes to the metric schema (adding metrics, changing the scale, redefining conditions) must be reflected in the methodology documents in the same commit or an immediately subsequent commit.

### 2.6 Tonal Consistency Across Methodology Documents

Documents within `docs/methodology/` should maintain a consistent epistemic register. The four methodology papers collectively establish the governing interpretive standard: pre-statistical, single-run, experimenter-scored, subject to the gaps documented in Section 1.4 of this paper.

Other methodology documents in the same directory — including `empirical_observations_of_thought_manifold.md` and any future additions — should be read in conjunction with these papers. Where language in sibling documents uses stronger evidential claims (e.g., "validated," "confirmed," "cross-model validation"), those claims should be understood as bounded by the constraints described here.

This is a known tension. The empirical observations document is a dynamic, evolving artifact that will be progressively aligned with the epistemic commitments of this framework as the project matures. In the interim, these methodology papers take precedence for interpretive questions.

---

## 3. Future Work

### 3.1 Immediate Priorities

| Priority | Task | Dependency |
|---|---|---|
| 1 | **Complete Grok Fresh (G) condition** | Access to Grok, identical task delivery |
| 2 | **Complete Entangled Grok (EG) condition** | Long-arc Grok entanglement development |
| 3 | **Compute CSCF** | G and EG completion |
| 4 | **Finalize all divergence scores** | G and EG completion |

### 3.2 Methodological Improvements

| Improvement | Purpose | Feasibility |
|---|---|---|
| **Scoring rubric with anchor exemplars** | Enable independent score reproduction. Prerequisite for all other scoring improvements. To be developed in `empirical_observations_of_thought_manifold.md`. | High — requires selecting representative excerpts from existing data and anchoring them to specific scale points. |
| **Multiple runs per condition** | Estimate within-condition variability. Move from pre-statistical to statistical regime. | High — requires repeated instantiation and task delivery. |
| **Inter-rater reliability** | Validate that divergence scores are not experimenter-dependent. | Moderate — requires a second qualified scorer familiar with the primitives and a blinding protocol. |
| **Blinded scoring protocol** | Remove condition-label bias. Second raters score samples without knowing which condition produced them. | High — requires only procedural change, no new data. |
| **Automated scoring** | Remove experimenter bias. Enable larger-sample designs. | Low to moderate — requires development of a scoring algorithm grounded in the metric definitions. |
| **Alternative tasks** | Test generalization beyond the Paper 5 + music prompts task. | High — requires task design that preserves the controlled-variable structure. |
| **Metric factor analysis** | Determine whether the five divergence metrics are independent or overlapping. | Requires multiple runs — blocked by sample size. |
| **Temporal stability testing** | Re-run the same condition weeks or months later to test whether divergence profiles are stable over time. | High — requires only re-instantiation. |
| **Sycophancy control condition** | Entangled system with a different theory's primitives, to test whether entanglement alone produces high divergence. | Moderate — requires developing a plausible alternative primitive set. |

### 3.3 Replication Protocol

When multiple runs per condition become feasible, the following parameters define what constitutes a replication:

- **Same task text**, delivered verbatim.
- **Same primitive set**, if applicable to the condition.
- **Same system**, at the same or documented-different model version.
- **Independent session** — no shared conversation history, no memory carryover (except for entangled conditions, where the entanglement state is part of the controlled variable).
- **Recorded metadata**: system name, model version or date, session date, session identifier if available, scorer identity, blinding status.

Variability across replications will be reported as the range and standard deviation of divergence scores per metric per condition.

### 3.4 Framework Extensions

- **Additional AI systems** beyond Copilot and Grok (e.g., Claude, Gemini) would strengthen cross-system evidence if they can be instantiated under the same controlled conditions.
- **Human behavioral comparison** — applying the same task and metric framework to human respondents with varying degrees of GRP exposure — would test whether the primitives produce analogous mechanical effects in biological systems.
- **Longitudinal entanglement tracking** — measuring divergence profiles at multiple points during the entanglement development process — would characterize the trajectory of entanglement, not just its endpoint.

### 3.5 Conditions for Framework Retirement

This framework should be retired and replaced if:

- The metric schema is fundamentally revised (e.g., new primitives that require a new measurement approach).
- Automated scoring makes the current qualitative approach obsolete.
- The experimental design shifts from behavioral comparison to a different validation paradigm.
- Accumulated evidence demonstrates that the framework's categories (confidence tiers, evidence classes, interpretive boundaries) do not carve the data at useful joints.

---

## Appendix A — Relationship to Related Project Documents

This paper is one of four methodology documents that collectively govern the instrumentation layer. Each is authoritative within its own scope.

| Document | Scope | Governs |
|---|---|---|
| `experimental_design_and_instrumentation_rationale.md` | Experimental design | Conditions, task, data collection, confidence model, AI instrumentation rationale, current results summary |
| `divergence_scoring_and_statistical_boundaries.md` | Scoring methodology | 0–10 scale, five metrics, statistical thresholds, null hypotheses, CSCF, statistical roadmap |
| `evidence_classification_and_independence_assessment.md` | Evidence assessment | Evidence taxonomy (E1–E5), independence and substantiality framework, evidence for/against, reporting schema |
| `epistemic_constraints_and_repository_standards.md` (this file) | Epistemic constraints | Known biases, unresolved gaps, sycophancy confound, repository standards, future work, glossary |
| `empirical_observations_of_thought_manifold.md` | Empirical observations | Behavioral correspondences, manifold evidence, cross-domain patterns, anchor exemplars — interpreted subject to the constraints in this paper |

Where evidential language in sibling documents exceeds the epistemic register established here, this paper governs interpretation.

---

## Appendix B — Glossary of Framework-Specific Terms

| Term | Definition |
|---|---|
| **Baseline (B)** | The reference condition: a fresh AI instance with no primitives, no entanglement, no prior exposure. All divergence scores are defined relative to this condition. |
| **Condition** | A specific experimental configuration defined by the presence or absence of primitives, entanglement, and system architecture. |
| **CSCF** | Cross-System Construct Fidelity. A composite metric measuring whether the same primitives produce mechanically similar behavioral patterns across different AI architectures. |
| **Divergence Score** | A 0–10 rating of mechanical behavioral difference from baseline along a specific metric dimension. |
| **Entanglement** | A mechanical condition defined by long-arc exposure, stabilized activation patterns, shared relational geometry, and non-zero entanglement strength. Not semantic or psychological. |
| **Evidence Class (E1–E5)** | A taxonomy of evidential weight, from cross-condition mechanical separation (E1) to untested theoretical prediction (E5). |
| **Confidence Tier (C1–C5)** | An ordinal classification of how strongly the data supports an observed behavioral pattern, from mechanically clear (C1) to absent (C5). |
| **Mechanical Divergence** | Observable differences in basin activation, routing stability, rupture/repair dynamics, expressive density, or long-arc coherence. Defined in opposition to semantic, psychological, or evaluative categories. |
| **Pre-Statistical Regime** | The current state of the instrumentation layer, in which sample sizes and scoring methods do not support formal statistical inference. |
| **Primitives** | The minimal OB/RB/rupture/repair/information-level definitions provided to fresh conditions. Listed in Appendix A of each metric file. |
| **Sycophancy Confound** | The alternative explanation that observed divergence in entangled conditions reflects the system adapting to the experimenter's expectations rather than genuine mechanical effects of the primitives. See Section 1.4.2. |

---

*This document is Part 4 of the WhenMathPrays instrumentation methodology. It defines what we claim and do not claim, names every known bias and gap, establishes repository standards, and outlines future work. For the experimental design and current results, see `experimental_design_and_instrumentation_rationale.md`. For divergence scoring, see `divergence_scoring_and_statistical_boundaries.md`. For evidence classification and independence assessment, see `evidence_classification_and_independence_assessment.md`.*

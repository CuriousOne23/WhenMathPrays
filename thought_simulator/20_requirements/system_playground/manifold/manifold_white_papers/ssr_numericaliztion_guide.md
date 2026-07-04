# SSR Numericalization Guide: Converting Symbolic Meaning to Numeric Fields for TS

**Version**: 0.1  
**Date**: 2026-07-04  
**Companion to**: prework_manifold_and_back.md  
**Repository**: CuriousOne23/WhenMathPrays  

## 1. Introduction

SSR Numericalization is the first critical layer in the Thought Simulator (TS) architecture. It converts symbolic-semantic representations (SSR) — concepts, relations, context, attributes — into stable, deterministic numeric fields that serve as the substrate for manifold construction.

This paper focuses **only** on the symbolic → numeric transformation. It does not cover manifold geometry (Paper 2) or projection/dictionary mechanics (Paper 3). Proper numericalization ensures the manifold is traceable, stable, discriminable, and semantically meaningful.

## 2. SSR Field Extraction

Engineers extract the following field types deterministically from SSR:

- **Identity fields**: Core entity or concept identifiers (e.g., presence, type).
- **Relational fields**: Strength and type of associations between concepts (0.0 = none, 1.0 = maximum).
- **Ambiguity fields**: Degree of uncertainty or multiple possible interpretations.
- **Contextual fields**: Surrounding conditions or situational modifiers.
- **Structural fields**: Hierarchical or compositional relationships (e.g., part-whole, sequence).

Extraction must be rule-based and version-controlled for reproducibility.

## 3. Numeric Domain Definition

Use bounded, interpretable ranges:

- Recommended default: $[0.0, 1.0]$ for normalized continuous features.
- Discrete categories: small integers (e.g., 0, 1, 2) when appropriate.
- Relational strength: 0.0 = absent, 1.0 = strongest.
- Presence/activation: 0.0 = absent, 1.0 = fully present.
- Ambiguity: 0.0 = certain, 1.0 = maximum uncertainty.

Maintain **monotonicity** (higher semantic intensity → consistently higher/lower numeric value) and **semantic anchoring** (numbers should feel intuitive during human review).

## 4. Normalization Procedures

- **Min-max normalization**: Scale raw values to $[0,1]$ based on observed or expected range.
- **Z-score**: Center and scale by mean and standard deviation for comparable fields.
- **Domain-specific normalization**: Use when semantic meaning dictates custom scaling (e.g., logarithmic for frequency-based fields).
- Requirements: Reproducible across runs; preserve relative distances and monotonicity.

## 5. Correlation Structure

Fields rarely exist in isolation. Define and compute correlations explicitly:

- Use Pearson/Spearman for numeric correlation or custom semantic similarity metrics.
- Strong positive correlation should reinforce shared manifold regions.
- Document expected correlation matrix as part of pre-work.

## 6. Semantic Gradients

Numeric changes must reflect meaningful semantic changes. Small perturbations in SSR should produce correspondingly small, predictable changes in numeric fields. Validate that gradients are smooth where semantic similarity is high.

## 7. Discriminability

Distinct SSR concepts must map to sufficiently separable numeric representations. Test using distance metrics between field vectors. Tune by adjusting extraction weights or adding distinguishing features if overlap occurs.

## 8. Stability Requirements

Extraction must be deterministic:
- Equivalent SSR inputs produce nearly identical numeric outputs (low variance).
- Rules must be versioned and free of stochastic elements.

## 9. Meaning Validation

Use these tests:

- **Traceability**: Can the numeric value be mapped back to original SSR attributes?
- **Stability**: Repeated runs yield consistent values.
- **Discriminability**: Different concepts produce separable values.
- **Behavioral**: Numeric fields lead to expected manifold and projection behavior.
- **Human review**: Engineers can intuitively understand what a numeric field represents.

## 10. Examples

(Examples of simple SSR → numeric conversion, relational strength, ambiguity handling, and correlation cases would go here in a full expansion.)

## 11. Common Pitfalls

- Over-normalization that destroys meaningful variance
- Under-normalization leading to unstable scales
- Semantic collapse (distinct concepts map to same numbers)
- Unstable fields across runs
- Gradients that do not align with semantic similarity

## 12. Tuning Procedures

- Adjust field extraction weights or rules
- Change normalization method or parameters
- Refine correlation computation
- Add new distinguishing fields for better discriminability

## 13. Validation Checklist

- [ ] All fields use documented numeric domains and normalization
- [ ] Monotonicity and semantic anchoring are preserved
- [ ] Correlations are defined and produce expected effects
- [ ] Stability, discriminability, and traceability tests pass
- [ ] Human review confirms intuitive meaning

## 14. Conclusion

SSR Numericalization is the foundation that turns symbolic meaning into a reliable numeric substrate for the TS manifold. When done correctly, it enables all subsequent layers (manifold geometry and projection) to be deterministic, traceable, and engineerable.

**Next papers in series**: manifold_geometry_spec.md and dictionary_projection_spec.md.


# Manifold Tuning Guide: How to Shape, Diagnose, and Refine TS Latent Space

**Version**: 0.1  
**Date**: 2026-07-04  
**Companion to**: prework_manifold_and_back.md  
**Repository**: CuriousOne23/WhenMathPrays  

## Purpose

This guide provides actionable steps for engineers to evaluate, diagnose, tune, and validate the pre-work manifold in the Thought Simulator (TS). It translates the concepts in the main white paper into concrete diagnostics and tuning procedures.

## 1. Core Evaluation Criteria

Use these criteria when inspecting a manifold snapshot:

### SSR → Manifold Transfer
- **Field Coherence**: Do extracted fields form consistent, meaningful clusters?
- **Field Distinguishability**: Are distinct SSR concepts mapped to separable dictionary coordinates? (Check distance metrics between regions.)
- **Field Interactions**: Do relational strengths tighten basins as expected? Does ambiguity widen transition zones predictably?
- **Semantic Gradients**: Are changes in SSR features reflected in smooth manifold trajectories?
- **Boundary Quality**: Do region boundaries align with real semantic distinctions?
- **Coordinate Meaning**: Can you trace any $(s_i, r_j)$ back to originating SSR content?
- **Stability**: Do repeated pre-work runs on equivalent SSR produce consistent coordinates?

**Good**: Clean surfaces, stable coordinates, predictable geometry.  
**Bad**: Fragmented surfaces, unstable coordinates, arbitrary boundaries.

### Manifold → OuBB/RG Projection
- **Meaningful Output Differences**: Do small, semantically relevant manifold movements produce corresponding output changes?
- **Smooth Transitions**: Do paths yield gradual, interpretable outputs?
- **Semantic Fidelity**: Do outputs preserve intent from the original SSR?
- **No Drift**: Does repeated routing over the same path remain stable?
- **Routing Path Meaning**: Do sequences of dictionary coordinates correspond to coherent relational or cognitive flows?
- **Determinism**: Same coordinate always yields same output.

**Good**: Traceable, stable, semantically aligned outputs.  
**Bad**: Illogical jumps, semantic loss, or non-deterministic behavior.

## 2. Tuning Procedures

### Tuning the Manifold (SSR → Manifold)
1. **Adjust Field Extraction** — Modify weights or add derived relational fields.
2. **Refine Clustering / Region Assignment** — Tighten or loosen thresholds for better separation.
3. **Add Mapping Constraints** — Explicitly enforce known symbolic relationships.
4. **Targeted Pre-Work Re-runs** — Focus on problematic surfaces or regions with curated SSR examples.
5. **Spline Intervention** — Apply cubic splines only at identified discontinuities that violate semantic continuity.
6. **Basin Shaping** — Strengthen attractors by reinforcing key relational fields.

### Tuning Projection (Manifold → OuBB/RG)
1. **Update Mapping Tables** — Adjust region-to-output rules.
2. **Modify Interpolation** — Tune spline parameters or weights along transitions.
3. **Add Stability Constraints** — Enforce stronger basin attraction where drift occurs.
4. **Introduce Conditional Rules** — Context-aware routing based on active surface/region.
5. **Validate & Iterate** — Re-project test cases and compare against expected outputs.

**Important**: All tuning must preserve determinism. Never introduce stochastic elements.

### 2.1 Numerical Field Tuning (SSR → Numeric Values)

See Section 6.2 of prework_manifold_and_back.md for full details. Key tuning actions include:

- Adjust normalization ranges or scaling methods when fields lack discriminability or stability.
- Refine monotonicity rules or semantic anchoring if human review shows poor traceability.
- Modify correlation computation (weights, similarity metrics) when field interactions do not produce expected basin or surface geometry.
- Re-validate numerical values after changes using the stability, discriminability, and behavioral tests.
- Document all numericalization rules in the manifold snapshot for reproducibility.

## 3. Diagnostic Workflow

1. Run pre-work and freeze manifold snapshot.
2. Visualize surfaces, basins, and gradients.
3. Test routing paths with known SSR cases.
4. Score against evaluation criteria (coherence, fidelity, stability).
5. Identify failure modes (e.g., unstable coordinates, semantic jumps).
6. Apply targeted tuning.
7. Re-freeze and regression test against previous version.
8. Repeat until quality thresholds are met.

## 4. Common Pitfalls & How to Avoid Them

- **Over-fragmentation**: Too many tiny regions → reduce clustering sensitivity.
- **Semantic Collapse**: Regions merging unrelated concepts → strengthen distinguishing fields.
- **Brittle Boundaries**: Small SSR changes cause large jumps → add smoothing + stability constraints.
- **Loss of Traceability**: Opaque coordinates → maintain mapping logs during pre-work.
- **Projection Drift**: Outputs shift over repeated routing → enforce stricter basin constraints.
- **Non-deterministic Tuning**: Accidental randomness → review all changes for determinism.

## 5. Validation Checklist

- [ ] Manifold coordinates are stable across repeated pre-work runs.
- [ ] Semantic gradients are smooth where expected.
- [ ] Boundaries align with domain knowledge.
- [ ] Routing paths produce coherent meaning.
- [ ] Projection preserves determinism and semantic fidelity.
- [ ] Good vs. bad test cases show clear differentiation.
- [ ] Versioned snapshots allow regression testing.
- [ ] Engineers can trace SSR → coordinate → output and back.

## 6. Recommended Tools & Outputs

- Manifold snapshot (JSON + coordinate lookup).
- Visualization scripts (surfaces, basins, gradients).
- Test suite with known SSR → expected OuBB mappings.
- Tuning log tracking changes and quality metrics.

---

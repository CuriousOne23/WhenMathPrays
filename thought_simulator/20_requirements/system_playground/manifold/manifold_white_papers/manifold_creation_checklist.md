# Manifold Creation Checklist

**Version**: 0.2 (Refined per CP review)  
**Date**: 2026-07-04  
**Companion to**: prework_manifold_and_back.md and manifold_tuning_guide.md  
**Repository**: CuriousOne23/WhenMathPrays  

Use this checklist during pre-work to produce a visible, navigable, and engineerable TS manifold.

## 1. Preparation

- [ ] SSR inputs are stable, well-structured, and representative of target cognitive domains.
- [ ] SSR examples include both “easy” and “edge-case” cognitive scenarios.
- [ ] Field extraction rules (numeric features, relational vectors, context) are defined and versioned.
- [ ] Dictionary numeric coordinate scheme is established (e.g., surface + region tuples).
- [ ] Expected surfaces, regions, and basins have been sketched at a high level.
- [ ] Tools for freezing, serializing, and visualizing the manifold are ready.

## 2. Field Extraction & Initial Construction

- [ ] Extract fields from SSR (embeddings, relations, symbolic features).
- [ ] Assign initial dictionary numeric coordinates.
- [ ] Construct surfaces as continuous regions of related structure.
- [ ] Verify that initial surfaces do not unintentionally overlap or collapse.
- [ ] Partition into named regions with clear boundaries.
- [ ] Form basins based on attraction/stability metrics (object vs. relational).
- [ ] Verify symbolic continuity across surfaces and regions.

## 3. Quality Evaluation (SSR → Manifold)

- [ ] Field coherence: Clusters align with expected symbolic meaning.
- [ ] Field distinguishability: Distinct concepts map to separable coordinates.
- [ ] Semantic gradients: Smooth SSR changes produce smooth manifold trajectories.
- [ ] Boundary quality: Boundaries correspond to real semantic distinctions.
- [ ] Field interaction effects: Relational strength tightens basins; ambiguity widens transitions.
- [ ] Coordinate meaning: Each coordinate is traceable back to SSR content.
- [ ] Stability: Repeated runs on equivalent SSR yield consistent results (low variance).

**Stop and fix** if any of the above fail before proceeding.

## 4. Discontinuity Handling

- [ ] Identify discontinuities in the raw manifold.
- [ ] Apply cubic spline smoothing only where semantic continuity is violated.
- [ ] Verify post-smoothing $C^0$ (minimum) or higher continuity as needed.
- [ ] Confirm smoothing does not distort core symbolic meaning.

## 5. Projection Setup (Manifold → OuBB/RG)

- [ ] Define deterministic projection operator $\Pi$.
- [ ] Create region-to-output mapping tables.
- [ ] Set interpolation and stability constraints.
- [ ] Verify projection preserves determinism (same coordinate → same output).
- [ ] Verify projection monotonicity along semantic gradients.
- [ ] Test basic routing paths for semantic fidelity and meaningful differences.

## 6. Freezing & Versioning

- [ ] Serialize full manifold (surfaces, regions, basins, coordinates, splines, mappings).
- [ ] Generate visualization artifacts (surface maps, basin depth, gradients).
- [ ] Create test suite with known SSR inputs and expected outputs.
- [ ] Assign version number and document changes.
- [ ] Store intermediate logs for full traceability (SSR → coordinate → output).

## 7. Final Validation

- [ ] Manifold is inspectable and "drivable" (engineers can step through coordinates).
- [ ] Routing paths produce coherent, expected meaning.
- [ ] Projection shows no semantic drift and good vs. bad differentiation.
- [ ] Full pipeline (SSR → Manifold → OuBB/RG) passes regression tests.
- [ ] Documentation (this checklist + notes) is complete.

## Sign-Off

- Engineer / Reviewer: ________________________ Date: __________
- Notes / Known Limitations:

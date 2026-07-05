# Manifold Tuning Guide: How to Shape, Diagnose, and Refine TS Latent Space

**Version**: 0.2 (Updated with paper series references)  
**Date**: 2026-07-04  
**Companion to**: prework_manifold_and_back.md, ssr_numericalization_guide.md, manifold_geometry_spec.md, dictionary_projection_spec.md  
**Repository**: CuriousOne23/WhenMathPrays  
**Associated Papers**:  
[prework_manifold_and_back.md](prework_manifold_and_back.md)  
[ssr_numericalization_guide.md](ssr_numericalization_guide.md)  
[manifold_geomerty_spec.md](manifold_geomerty_spec.md)  
[dictionary_projection_spec.md & glossary](dictionary_projection_spec.md)  
[manifold_creation_checklist.md](manifold_creation_checklist.md)  

## Purpose

This guide provides actionable steps for engineers to evaluate, diagnose, tune, and validate the TS manifold. It references the three specialized papers for deeper details.

## 1. Core Evaluation Criteria

### SSR → Numeric Layer
See [ssr_numericalization_guide.md](ssr_numericalization_guide.md) for full details.

### Numeric → Geometry Layer
See [manifold_geometry_spec.md](manifold_geometry_spec.md) for full details on surfaces, regions, basins, and transitions.

### Geometry → Text Layer
See [dictionary_projection_spec.md](dictionary_projection_spec.md) for dictionary, projection, and reverse interpretation.

## 2. Tuning Procedures

### Numerical Field Tuning (SSR → Numeric)
See Section 12 of [ssr_numericalization_guide.md](ssr_numericalization_guide.md).

### Geometry Tuning (Numeric → Manifold)
- Adjust clustering thresholds for surfaces and regions.
- Modify basin attraction strength.
- Refine transition rules and spline smoothing parameters.
- Re-run targeted pre-work on problematic areas (see [manifold_geometry_spec.md](manifold_geometry_spec.md) Section 11).

### Projection Tuning (Geometry → Text)
- Update mapping tables and meaning signatures.
- Adjust interpolation, stability constraints, and conditional rules.
- Tune correlation weights affecting textual output.
- See [dictionary_projection_spec.md](dictionary_projection_spec.md) Section 9 for details.

**Important**: All tuning must preserve determinism.

## 3. Diagnostic Workflow

1. Run pre-work and freeze manifold snapshot.
2. Evaluate each layer using the corresponding paper.
3. Test routing paths with known cases.
4. Score against evaluation criteria.
5. Apply targeted tuning from the appropriate paper.
6. Re-freeze and regression test.
7. Repeat until quality thresholds are met.

## 4. Common Pitfalls & How to Avoid Them

- Semantic collapse → strengthen discriminability [ssr_numericalization_guide.md](ssr_numericalization_guide.md)  
- Fragmented geometry → adjust clustering [manifold_geometry_spec.md](manifold_geometry_spec.md)  
- Meaning drift in output → check dictionary signatures and projection tables [dictionary_projection_spec.md](dictionary_projection_spec.md)  
- Unstable fields → improve normalization and stability rules [ssr_numericalization_guide.md](ssr_numericalization_guide.md)  
- Brittle transitions → refine spline smoothing [manifold_geometry_spec.md](manifold_geometry_spec.md)  

## 5. Validation Checklist

- [ ] Numeric fields are stable, discriminable, and traceable [ssr_numericalization_guide.md](ssr_numericalization_guide.md)  
- [ ] Manifold geometry is coherent, continuous, and stable [manifold_geometry_spec.md](manifold_geometry_spec.md)  
- [ ] Dictionary unifies all layers with accurate meaning signatures [dictionary_projection_spec.md](dictionary_projection_spec.md)  
- [ ] Projection is deterministic and semantically faithful [manifold_geometry_spec.md](manifold_geometry_spec.md)  
- [ ] Full pipeline passes ground-truth tests with no unintended drift
- [ ] Versioned snapshots support regression testing

## 6. Recommended Tools & Outputs

- Manifold snapshot (including dictionary)
- Visualization scripts for geometry
- Test suite spanning all three layers
- Tuning log with references to the specific paper used

---

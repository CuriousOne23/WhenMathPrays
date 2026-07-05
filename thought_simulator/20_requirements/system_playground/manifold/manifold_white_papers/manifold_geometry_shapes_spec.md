# Manifold Geometry & Shapes Specification  
**Version**: 0.2 (Draft – Unified Ontology)  
**Date**: 2026-07-05  
**Companion to**: prework_manifold_and_back.md  
**Repository**: CuriousOne23/WhenMathPrays  
**Part of the 7-paper pre-work suite**:

- [1. SSR to Manifold Transfer Guide](./ssr_to_manifold_transfer_guide.md)  
- **[2. Manifold Geometry & Shapes Specification](./manifold_geometry_shapes_spec.md)** (this document)  
- [3. Shapes Meanings — SSR, OuBB, and Mapping](./shapes_meanings_ssr_oubb_mapping.md)  
- [4. Working Inside the Manifold — Routing & Projection](./manifold_routing_projection.md)  
- [5. Manifold to OuBB / RG Projection & Reverse](./manifold_to_oubb_projection_reverse.md)  
- [6. Pre-work Checklist, Tuning & Validation](./prework_checklist_tuning_validation.md)  
- [7. Dictionary Projection Specification](dictionary_projection_spec.md)  

**Top level overview**  
[prework_manifold_and_back.md](prework_manifold_and_back.md)

**Canonical Glossary**: See Paper 7 (or a dedicated glossary file once finalized). All terminology in this document is defined there.

---

## 1. Purpose

This document specifies the shapes the pre-work engineer must instantiate when constructing the manifold from numeric fields derived from SSR.  

**Important ontological note**: The manifold is **not a literal geometric model**. It is a **state-space constraint surface** shaped by SSR dynamics and the requirements of deterministic, traceable OuBB/RG output. Shapes are instantiated as **constraint structures**, not geometric objects. Curvature-related metrics (Hessian, Gaussian curvature, etc.) are inspection and tuning tools only.

## 2. Core Principles for Shape Creation

- Shapes emerge from SSR field interactions, numeric gradients, and clustering.  
- All shapes must be **deterministic**, **reproducible**, and **stable** under small SSR perturbations.  
- Every shape must expose interpretable structure for the projection operator Π so that projection and reverse-projection remain deterministic.  
- Engineer quantifies and validates each shape using defined metrics.

**Note**: “height” and “depth” refer to constraint-energy levels, not geometric elevation. Curvature-related metrics are inspection tools only; they do not define the manifold’s geometry.

## 3. Catalog of Shapes

### 3.1 Flat Regions (Zero Curvature Zones)
- **Description**: Neutral constraint areas with minimal intrinsic steering.  
- **Creation**: Areas where numeric field gradients are below threshold.  
- **Metrics**: Area/extent, curvature deviation tolerance.  
- **Engineer Action**: Identify via clustering; validate stability.

### 3.2 Peaks (Local Maxima – Repelling)
- **Description**: Regions where states are repelled (high constraint energy).  
- **Creation**: Arise from **strongly anti-aligned SSR field interactions** (semantic conflict → repulsion → high constraint energy).  
- **Metrics**: Constraint-energy height, principal curvatures $(\kappa_1, \kappa_2)$, Gaussian curvature $K > 0$, Hessian eigenvalues, gradient norm.  
- **Engineer Action**: Instantiate from anti-alignment patterns; measure rejection strength.

### 3.3 Valleys / Wells (Local Minima – Attracting)
- **Description**: Regions where states are drawn inward (low constraint energy).  
- **Creation**: Arise from **strongly aligned SSR field interactions** (semantic coherence → attraction → low constraint energy).  
- **Metrics**: Constraint-energy depth, principal curvatures, Gaussian curvature, Hessian eigenvalues, basin volume.  
- **Engineer Action**: Instantiate from alignment patterns; tune depth for desired stability.

### 3.4 Saddles, Ridges, Channels, Inflections, and Other Features
These features are instantiated using the same SSR-alignment logic as peaks and valleys and serve as routing and transition structures within the constraint surface. Detailed definitions will be added once Paper 3 finalizes the unified meanings across SSR, manifold, and OuBB layers.

## 4. Implementation Notes

- Use numerical clustering on numeric field vectors to instantiate surfaces and regions.  
- Apply smoothing where needed to ensure required continuity.  
- Validate each shape against SSR input variation and OuBB output fidelity.  
- Shapes must remain stable and interpretable by the projection operator Π.

### 4.1 Continuity Requirements and Spline Smoothing

The TS manifold must remain continuous and differentiable across all regions to
support deterministic routing. If numeric-field interactions produce an abrupt
junction or discontinuity (for example, a sharp gradient break between adjacent
clusters), the engineer must apply cubic spline smoothing to restore continuity.

Spline smoothing ensures:

- $C^2$ continuity across the constraint surface
- stable routing behavior for Paper 5 (Working Inside the Manifold)
- consistent constraint-energy gradients for shape interpretation
- predictable basin boundaries and transition behavior
- deterministic projection behavior for Π

Any standard cubic spline implementation is acceptable as long as continuity is
restored and validated using the Paper 6 stability and fidelity checks.

## 5. Next Steps for Engineer

After reading this document, proceed to:  
- Paper 1 for SSR → numeric transfer  
- Paper 3 for detailed meaning of each shape across layers  
- Paper 6 for creation checklist and tuning procedures

---

**End of Revised Draft – Paper 2**

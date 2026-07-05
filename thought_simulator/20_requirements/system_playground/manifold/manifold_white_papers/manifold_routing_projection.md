# Working Inside the Manifold — Routing & Projection  
**Version**: 0.1 (Draft)  
**Date**: 2026-07-05  
**Companion to**: prework_manifold_and_back.md, Paper 2, and Paper 3  
**Repository**: CuriousOne23/WhenMathPrays  
**Part of the 6-paper pre-work suite**:

- [1. SSR to Manifold Transfer Guide](./ssr_to_manifold_transfer_guide.md)  
- [2. Manifold Geometry & Shapes Specification](./manifold_geometry_shapes_spec.md)  
- [3. Shapes Meanings — SSR, OuBB, and Mapping](./shapes_meanings_ssr_oubb_mapping.md)  
- **[4. Working Inside the Manifold — Routing & Projection](./manifold_routing_projection.md)** (this document)  
- [5. Manifold to OuBB / RG Projection & Reverse](./manifold_to_oubb_projection_reverse.md)  
- [6. Pre-work Checklist, Tuning & Validation](./prework_checklist_tuning_validation.md)  

**Top level overview**  
[prework_manifold_and_back.md](prework_manifold_and_back.md)

**Canonical Glossary**: See Paper 6 (or a dedicated glossary file once finalized). All terminology in this document is defined there.

---

## 1. Purpose

This document describes how states move and project **inside** the manifold during runtime. The manifold is a **state-space constraint surface** (not a literal geometric model). Routing is deterministic fixed-time-step movement guided by the constraint structures defined in Paper 2 and whose meanings are detailed in Paper 3.

## 2. Core Routing Principles

- Movement is **fixed-time-step** and deterministic.  
- States follow paths influenced by **constraint-energy gradients** (peaks repel, valleys attract).  
- Routing must remain stable under small SSR perturbations.  
- Every path must expose interpretable structure for the projection operator Π.  
- Engineers can inspect and validate routing trajectories during pre-work and runtime debugging.

## 3. Key Routing Behaviors by Shape

### 3.1 Flat Regions
- States move according to direct SSR field interactions with minimal constraint-energy steering.  
- Useful for predictable, rule-driven segments of thought flow.

### 3.2 Peaks (Repelling)
- States are pushed away (high constraint energy).  
- Promotes divergence and exploration of alternative paths.

### 3.3 Valleys / Wells (Attracting)
- States are drawn inward (low constraint energy).  
- Promotes convergence, stabilization, and persistence in coherent regions.

### 3.4 Saddles, Ridges, Channels, Inflections
- Saddles act as transition/decision points.  
- Ridges guide structured divergence.  
- Channels guide focused flow.  
- Inflections mark phase shifts in routing behavior.

## 4. Projection Within the Manifold

- As states route, the projection operator Π can be applied at any point using dictionary coordinates.  
- Intermediate projections help with debugging and partial output generation.  
- All internal projections must respect the same SSR ↔ OuBB meaning preservation rules defined in Paper 5.

## 5. Implementation Notes for Engineers

- Implement routing as fixed-time-step updates on the numeric field vector, influenced by local constraint-energy gradients.  
- Use minimal-constraint paths (geodesic-like flow lines) for efficient routing.  
- Validate routing stability and semantic fidelity against SSR test cases.  
- Provide inspection hooks for trajectory visualization and constraint-energy profiling.

## 6. Next Steps

- Use Paper 2 for shape creation and metrics.  
- Use Paper 3 for detailed meaning of each shape.  
- Use Paper 5 for full forward/reverse projection to OuBB.  
- Use Paper 6 for validation checklists and tuning procedures.

---

**End of Draft – Paper 4**

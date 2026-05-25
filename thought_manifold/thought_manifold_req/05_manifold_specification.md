# 05 Manifold Specification

## 1. Purpose

This document specifies the **Relational Manifold** as an optional interpretive and visualization layer for the Thought Manifold Simulator.

The Manifold is **not** part of the core execution engine. The authoritative engine is the **Thought Simulator (TS)** — a fixed-time-step, deterministic entropy-reduction state machine. The Relational Manifold provides a geometric projection of TS state for improved human intuition, debugging, analysis, and exploration.

**Important Philosophical Note**: Geometry is treated here as a **visualization hypothesis**, not a metaphysical claim about the nature of thought. It is one possible representational language among many. The architecture remains open to alternative visualization paradigms.

## 2. What We Want From the Manifold (Value Proposition)

The Relational Manifold should deliver:

- Intuitive visualization of thought dynamics, including behavior with multiple simultaneous ThoughtPoints.
- Clear representation of attractors, trajectories, splitting/merging, and exploration patterns.
- Effective debugging and insight tool, especially under multi-TP conditions.
- Teaching and communication aid for researchers and cognitive scientists.
- A testable environment for evaluating geometric representations of thought.

## 3. Why Geometry? (Rationale)

Geometry (gradient-based landscapes) was chosen because it provides a clean, minimal metaphor for attractors and flows without introducing fake physics. It remains a hypothesis.

## 4. What We Expect to See (Including Multi-TP Scenarios)

- **OBs**: May contain multiple TPs resting simultaneously. Depth and curvature still reflect identity strength and coherence.
- **RBs**: May contain multiple TPs flowing in parallel or along shared corridors.
- **TP Trajectories**: Multiple overlapping or parallel paths, with clear visual distinction between individual TPs.
- **Entropy**: Represented via height and/or color gradients.
- **Exploration & Interaction**: Complex patterns with multiple active TPs, including concurrent splitting, merging, and ejection events.
- **Observer Influence**: Optional overlays for coherence evaluation points.

## 5. Advantages Over Non-Geometric Methods

(unchanged — strong visual compression, especially useful when viewing multiple TPs and their interactions)

## 6. Why Cognitive Science Should Be Interested

(unchanged)

## 7. How TS Output Is Represented in Manifold Space

### 7.1 Core Mapping Rules
- Each ThoughtPoint is mapped to a 0-dimensional point.
- Multiple TPs can occupy the same OB or RB simultaneously.
- Entropy, basin affiliation, and state (step index + tagged state counter) are projected for each TP independently.

### 7.2 Geometric Object Definitions & Rendering Rules

**A. ThoughtPoint (TP) Geometry**
- Strictly 0-dimensional mathematically.
- Rendered as glyph with 3–6 px radius (configurable, non-semantic).
- Multiple TPs in the same basin are rendered with slight spatial jitter or clustering around the center (for OBs) or along the centerline (for RBs) to avoid perfect overlap while preserving visual clarity.
- Each TP glyph must visually indicate its TS Step Index and Tagged State Counter (via color, label in debug mode, or hover).

**B. Object Basin (OB) Geometry**
- Diameter 5–9 px (configurable).
- Can contain multiple TPs resting simultaneously.
- 3D: Smooth bowl-shaped depression.
- 2D: Contour lines or shaded gradient.
- Sampling: ≥5 points.

**C. Relational Basin (RB) Geometry**
- 2–4 px wide corridor.
- Can contain multiple TPs flowing in parallel.
- Sampling: ≥3 points.

**D. Layered Scene Composition**
Base surface → Basins → Trajectories → Annotations.

**E. Visual Encoding Rules**
- Color, line style, thickness, opacity with mandatory legend.
- When multiple TPs are present, use subtle differentiation (e.g., slight hue shift, numeric labels, or z-ordering) to distinguish individual trajectories.

### 7.3 Height/Depth Governing Equations & Bounds

(unchanged — global normalization to [-1.0, +0.5])

### 7.4 OB–RB Interface Geometry (Ejection Points)

- Every OB defines one or more exit points.
- Multiple TPs can be ejected from the same or different exit points.
- Ejection order and timing follow deterministic TS rules.

### 7.5 Rest and Ejection Visual Semantics (Multi-TP)

**A. Rest State (Inside OB)**
- Multiple TPs may rest simultaneously at or near the OB center pixel (with small spatial jitter for visibility).
- Each TP rendered with increased opacity and optional soft pulsing glow.

**B. Ejection Trigger & Animation**
- When a TP is ejected, its specific exit point and corresponding RB entry point are briefly highlighted.
- The TP moves along a short, smooth spline: OB center region → chosen exit point → RB centerline.
- Multiple ejections can occur in the same timestep with visual distinction (different splines, staggered timing if needed for clarity).

**C. Flow State (On RB)**
- Multiple TPs may flow simultaneously along the same RB corridor.
- Each TP follows the RB centerline with appropriate motion and normal opacity.

### 7.6 TP Indexing and Diagnostic Highlighting

- Every TP carries **TS Step Index** and **Tagged State Counter**.
- Supports index-based and state-counter-based highlighting, filtering, and navigation for individual or groups of TPs.
- Diagnostic tools must handle multiple TPs gracefully (e.g., “highlight all TPs with Step Index 10”, “highlight all TPs in OB X”).

### 7.7 Text/Token Highlighting Interface

- Supports synchronized text ↔ geometry highlighting, including cases with multiple active TPs.

### 7.8 Interaction and Measurement Semantics

- Clicking and area selection work with multiple TPs and basins.
- Cursor hover provides per-TP information even when multiple TPs are clustered.
- Viewport controls unchanged.

## 8. Implementation Requirements (For AI Agents & Developers)

- Must gracefully render and distinguish multiple TPs in the same basin or trajectory.
- Support for visual decluttering (jitter, layering, filtering) when TP density is high.
- Full logging of projection steps for multi-TP scenarios.
- Designed for easy modification and extension.

## 9. Invariants

- The Manifold has no causal influence on the TS.
- Geometry remains interpretive, not causal.
- Rendered sizes carry no semantic weight unless documented.

## 10. Success Criteria

- Researchers can clearly observe and debug behavior involving multiple simultaneous ThoughtPoints.
- The manifold is easy to implement, debug, extend, and modify.
- It demonstrates both the strengths and limitations of geometric visualization while remaining scientifically honest.

---

**Last Updated**: May 25, 2026  
**Version**: 1.3 (Multi-TP visualization support added)

---
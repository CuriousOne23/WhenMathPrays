# 05 Manifold Specification

## 1. Purpose

This document specifies the **Relational Manifold** as an optional interpretive and visualization layer for the Thought Manifold Simulator.

The Manifold is **not** part of the core execution engine. The authoritative engine is the **Thought Simulator (TS)** — a fixed-time-step, deterministic entropy-reduction state machine. The Relational Manifold provides a geometric projection of TS state for improved human intuition, debugging, analysis, and exploration.

**Important Philosophical Note**: Geometry is treated here as a **visualization hypothesis**, not a metaphysical claim about the nature of thought. It is one possible representational language among many. The architecture remains open to alternative visualization paradigms.

## 2. What We Want From the Manifold (Value Proposition)

The Relational Manifold should deliver:

- Intuitive visualization of thought dynamics (identity stabilization, relational transformation, coherence formation, entropy reduction, transitions).
- Clear representation of attractors, trajectories, splitting/merging, and exploration patterns.
- Effective debugging and insight tool (detect stuck states, premature collapse, unexpected behavior).
- Teaching and communication aid for researchers and cognitive scientists.
- A testable environment for evaluating geometric representations of thought.

## 3. Why Geometry? (Rationale)

Geometry (gradient-based landscapes) was chosen because:

- It avoids the heavy ontological burden and artifacts of force-based models (no momentum, acceleration, oscillations, interference rules, or fake physics).
- Gradients provide a minimal, expressive metaphor for attractors: a ThoughtPoint can be treated as a non-momentum 0-dimensional point on a surface.
- It compresses complex TS dynamics into an intuitive visual language without contaminating the deterministic TS core.

**Geometry remains a hypothesis.** It is useful only insofar as it helps researchers *see* attractors and flows cleanly.

## 4. What We Expect to See

- **OBs**: Deep minima (wells) — depth reflects identity strength, curvature reflects coherence.
- **RBs**: Ridge-like or flatter regions — shape reflects transformation type, width reflects flexibility.
- **TP Trajectories**: Paths showing smoothness (coherence), curvature (effort), branching, and convergence.
- **Entropy**: Represented via height and/or color gradients.
- **Exploration**: Wandering paths in medium-entropy zones.
- **Observer Influence**: Optional overlays for coherence evaluation points.

## 5. Advantages Over Non-Geometric Methods

- Strong visual compression of high-dimensional data.
- Reveals emergent structure (clusters, flows, bottlenecks) invisible in logs/tables.
- Leverages human spatial intuition.
- Avoids introducing fake physics while representing attractors effectively.
- Highly falsifiable and extensible.

## 6. Why Cognitive Science Should Be Interested

- Offers a new lens on identity formation, relational reasoning, coherence, and conceptual transitions.
- Provides a testable geometric hypothesis of thought dynamics.
- Bridges continuous and discrete models of cognition.
- Supports improved interpretability in both human and artificial systems.

## 7. How TS Output Is Represented in Manifold Space

### 7.1 Core Mapping Rules
- **ThoughtPoint** → 0-dimensional point via projection function from TS state.
- **OB** → Deep minimum.
- **RB** → Ridge-like transitional region.
- **Entropy** → Height/color gradient ($H_{\text{total}}$ and $H_{\\%}$).
- **Transitions** → Trajectories.
- **Splitting/Merging** → Branching/converging paths.

### 7.2 Geometric Object Definitions & Rendering Rules

**A. ThoughtPoint (TP) Geometry**  
- Strictly 0-dimensional mathematically.  
- Rendered as glyph with 3–6 px radius (configurable, non-semantic).  
- Positioned at OB center or RB centerline.

**B. Object Basin (OB) Geometry**  
- Diameter 5–9 px, circular/elliptical.  
- 3D: bowl-shaped depression.  
- Sampling: ≥5 points.

**C. Relational Basin (RB) Geometry**  
- 2–4 px wide corridor.  
- Sampling: ≥3 points.

**D. Layered Scene Composition**  
Base surface → Basins → Trajectories → Annotations.

**E. Visual Encoding Rules**  
Color, line style, thickness, opacity with mandatory legend.

### 7.3 Height/Depth Governing Equations & Bounds

All values normalized to visual range **[-1.0, +0.5]**.

- **OB Depth**: `-1.0 to -0.1`  
  $$
  \text{OB}_{\text{depth}} = k_1 \cdot (1 - H_{\\%}) + k_2 \cdot \text{coherence}
  $$
- **RB Height**: `0.0 to +0.5`  
  $$
  \text{RB}_{\text{height}} = k_3 \cdot \|\nabla H\| + k_4 \cdot \text{transition\_cost}
  $$

### 7.4 OB–RB Interface Geometry (Ejection Points)

- Every OB defines one or more **exit points** on its boundary.
- Each RB begins at an aligned **entry point**.
- RB defined by polyline/spline from OB exit to next OB entry.

### 7.5 Rest and Ejection Visual Semantics

**A. Rest State (Inside OB)**  
- TP rendered at OB center pixel with increased opacity and optional soft pulsing glow.  
- No motion.

**B. Ejection Trigger & Animation**  
- On TS ejection signal: OB exit point and RB entry briefly highlighted.  
- TP moves along short, smooth spline: OB center → exit point → RB centerline.  
- Once on RB: normal opacity and flow motion.

### 7.6 TP Indexing and Diagnostic Highlighting

- Every ThoughtPoint carries a **TS step index** (when created).  
- Supports index-based highlighting, filtering, and navigation.  
- Index displayed in hover panels and optionally as small label next to glyph.

### 7.7 TP State Counter and Tagging Lifecycle

Every ThoughtPoint must maintain a **tagged state counter** (separate from TS step index) that tracks its internal evolution.

**A. State Counter Definition**  
- Integer starting at 0 when the TP is created.  
- Increments by +1 each time the TP is:  
  - Tagged or modified by a basin (OB, RB, etc.)  
  - Updated by a regulator  
  - Split or merged  
  - Re-evaluated or otherwise modified by the TS.

**B. Purpose**  
- Enables deterministic replay and debugging of tagging order.  
- Supports detection of missing/repeated tags and basin loops.  
- Facilitates reconstruction of TP lineage and lifecycle analysis.  
- Ensures proper synchronization between TS state and manifold rendering.

**C. Display Rules**  
- The state counter must appear in TP hover panels and info panels.  
- Optional: small numeric label next to the TP glyph (debug mode only).

**D. Relationship to TS Step Index**  
- **TS Step Index** = global simulation time when the TP was created.  
- **TP State Counter** = number of times this specific TP has been updated/tagged.  
Together they provide complete lifecycle traceability.

### 7.8 Text/Token Highlighting Interface

- Supports synchronized text ↔ geometry highlighting.  
- Hovering over tokens highlights corresponding TPs, OBs, RBs, and trajectories (and vice versa).

### 7.9 Interaction and Measurement Semantics

- Clicking, area selection, cursor hover, and viewport controls as previously defined.

## 8. Implementation Requirements (For AI Agents & Developers)

- Separate module consuming TS snapshots.  
- Clear interfaces for projection, rendering, and encoding.  
- Full logging and debug mode.  
- Designed for easy modification and extension.

## 9. Invariants

- The Manifold has no causal influence on the TS.  
- Geometry remains interpretive, not causal.  
- Rendered sizes carry no semantic weight unless documented.

## 10. Success Criteria

- Researchers gain clear intuitive insight into TS dynamics.  
- The manifold is easy to implement, debug, extend, and modify.  
- It demonstrates both the strengths and limitations of geometric visualization while remaining scientifically honest.

---

**Last Updated**: May 25, 2026  
**Version**: 1.1 (TP State Counter + Tagging Lifecycle added)

---
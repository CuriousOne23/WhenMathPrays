# 06 Basins

## 1. Purpose
Define the common and specific requirements for all basin types in the manifold (Object Basins, Relational Basins, Inquiry Basins, and special variants such as Feeling OB or Done RB).

## 2. Common Basin Requirements

**B-01: General Properties**
- Every basin must have a unique ID, type, position/center, and shape parameters.
- Every basin must expose its local potential function $V(\mathbf{x})$.
- Every basin must support membership testing for a ThoughtPoint.
- Every basin must provide gradient information for dynamics.

**B-02: Visualization**
- Every basin must provide rendering metadata (color, depth profile, label, visual style).
- Must support different visual representations (deep valley, flat plain, misty region, etc.).

**B-03: Fanin and Fanout Capabilities**
- Every basin must declare its **fanin** and **fanout** limits.
- **Fanout**: Maximum number of simultaneous outgoing branches (splitting) a basin can support from a single ThoughtPoint or thought complex.
- **Fanin**: Maximum number of simultaneous incoming branches (merging) a basin can gracefully accept and integrate.
- These values must be configurable per basin type and per individual basin instance.
- Must include `max_fanout`, `preferred_fanout`, `max_fanin`, and `preferred_fanin`.
- Behavior when limits are exceeded (pruning, attenuation, rerouting, or logging warnings) must be defined and observable.

## 3. Specific Basin Types

### 3.1 Object Basins (OBs)
- Deep, stable local minima.
- High damping coefficient.
- Must perform feature binding and coherence sharpening on entry.
- Must attach contextual/symbolic information (labels, memory tags, confidence).
- Must renormalize incoming energy and embedding norm.
- Must have tunable capacity and depth.
- Must reduce normalized entropy $H_\\%$ significantly upon successful settling.
- **Recommended Fanin/Fanout**: Moderate to high fanin (good convergence), moderate fanout (4–10).

### 3.2 Relational Basins (RBs)
- Flatter, higher-potential regions.
- Support layered networks and RB-to-RB connections.
- Must implement fuzzy filters at entry points.
- Must support splitting and merging of ThoughtPoints.
- Tunable damping (including near-zero for highways).
- Must preserve $H_\\%$ across most operations (except minor losses).
- **Recommended Fanin/Fanout**: High fanout (8–25) for routing flexibility, moderate to high fanin for integration.

### 3.3 Inquiry Basins
- Shallow, unstable, diffuse regions.
- Activated when medium entropy persists.
- Must maintain unresolved tension (prevent easy collapse).
- Should orient geometry toward nearby Truth Basins or resolution paths.
- Must support exploratory behavior (higher noise, more branching).
- **Recommended Fanin/Fanout**: High fanout (12–30) to encourage exploration, limited fanin to avoid premature resolution.

### 3.4 Special Basins
- **Feeling OB**: Attaches emotional valence and somatic markers, especially during stressed completion. Moderate fanout, high fanin.
- **Done RB**: Terminal basin for completed thoughts. Very low fanout (1–3), moderate fanin.
- Others (as needed): Truth Basins, Entry Buffer, etc.

## 4. Transition Requirements

- Basins must define valid exit/entry conditions (saddles, filters, energy thresholds).
- Transitions must be observable and logged with full before/after state.
- Fanin/fanout limits must be enforced and logged during transitions.

## 5. Testability Requirements

- Must be able to create a manifold with multiple basin types and validate transitions.
- Object Basins must demonstrably reduce entropy more than Relational Basins.
- Inquiry Basins must delay convergence compared to normal paths.
- Must test behavior when fanin and fanout limits are deliberately exceeded.

## 6. Traceability
Links to:
- `03_core_conceptual_requirements.md` (Sections 2.2, 2.3, 2.6)
- `04_system_architecture.md`
- `12_energy_dynamics.md`

---

**Last Updated**: [Insert Date]  
**Version**: 0.2 (Draft)

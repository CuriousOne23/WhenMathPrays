# **1. Purpose of This Appendix**

This appendix provides:

- **10 complete IdOB examples** from a single conversation topic  
- **actual YAML input and output structures** IdOB reads/writes  
- **the required upstream fields** IdOB depends on  
- **the metrics IdOB uses to evaluate identity stability**  
- **the process for constructing IdOB objects inside Path‑A**  
- **why these 10 examples are representative and important**

This appendix is designed to help implementers, reviewers, and testbench authors understand **how IdOB actually behaves** inside Path‑A.

---

# **2. What Must Be Predefined Before IdOB Can Operate**

IdOB is not a standalone primitive.  
It depends on **upstream geometry, continuity, routing, pressure, and semantic‑importance** fields.

Before IdOB can run, the following must be defined:

### **2.1 Semantic Geometry**
- `TP.metadata.semantic_geometry`  
Defines the meaning‑space IdOB interprets identity within.

### **2.2 Structural Geometry**
- `TP.metadata.structural_geometry`  
Provides the substrate for identity geometry.

### **2.3 Continuity Geometry**
- `TP.metadata.continuity.geometry`  
Defines the temporal stability of meaning.

### **2.4 Routing Regime**
- `TP.metadata.routing.regime`  
Determines whether identity is in Stable, Transition, Drift, or Collapse regime.

### **2.5 Semantic Importance**
- `TP.metadata.semantic_importance`  
Scales identity pressure.

### **2.6 Pressure Fields**
- `TP.metadata.identity.pressure`  
- `TP.metadata.routing.pressure`  
Identity pressure is required for stability evaluation.

### **2.7 Residual Fields**
- `TP.metadata.identity.residuals.*`  
Residuals measure identity drift, correction, collapse, or bifurcation.

### **2.8 Freeze Fields**
- `TP.metadata.freeze.*`  
Identity freezes prevent collapse.

### **2.9 Basin/Surface Fields**
- `TP.metadata.global_geometry.basin_state`  
- `TP.metadata.global_geometry.surface_state`  
Identity stability depends on basin/surface classification.

### **2.10 Stance/Direction**
- `TP.metadata.stance_next`  
- `TP.metadata.direction_next`  
Identity stance/direction propagate into next turn.

These fields must be present and well‑formed before IdOB can interpret identity.

---

# **3. Metrics Required to Construct an IdOB Object**

IdOB uses the following metrics:

### **3.1 Geometry Metrics**
- curvature  
- entropy  
- basin entry  
- basin drift  
- surface crossing  
- geometry_update type (refinement, correction, drift, conflict, bifurcation, merge)

### **3.2 Continuity Metrics**
- continuity_next  
- drift magnitude  
- correction magnitude  
- stability vs oscillation

### **3.3 Pressure Metrics**
- pressure_next  
- pressure_gradient  
- pressure_escalation

### **3.4 Residual Metrics**
- geometry residual  
- continuity residual  
- pressure residual  
- curvature residual  
- entropy residual

### **3.5 Freeze Metrics**
- freeze.current  
- freeze.next  
- freeze.propagation

### **3.6 Basin/Surface Metrics**
- basin_state  
- surface_state  
- transitions

These metrics determine whether identity is:

- stable  
- unstable  
- collapsing  
- bifurcating  
- merging  
- drifting  
- converging  

MCB uses these metrics to decide whether IdOB must run again.

---

# **4. Work Involved in Constructing IdOB Objects**

Constructing IdOB objects requires:

### **4.1 Reading Upstream Fields**
IdOB reads ~40 TP metadata fields.

### **4.2 Normalizing Inputs**
Geometry, continuity, pressure, and residuals must be normalized.

### **4.3 Interpreting Identity Meaning**
IdOB applies identity roles, geometry, continuity, and pressure.

### **4.4 Computing Residuals**
Residuals measure identity drift, correction, or collapse.

### **4.5 Updating Geometry**
IdOB updates identity geometry based on residuals and pressure.

### **4.6 Updating Continuity**
IdOB determines continuity_next.

### **4.7 Updating Pressure**
IdOB computes pressure_next.

### **4.8 Updating Freeze State**
Freezes prevent collapse.

### **4.9 Updating Basin/Surface State**
Identity stability depends on basin/surface classification.

### **4.10 Writing Outputs**
IdOB writes ~30 TP metadata fields.

### **4.11 MCB Stability Evaluation**
MCB decides whether IdOB must run again.

This is why IdOB is one of the most complex primitives in Path‑A.

---

# **5. Why These 10 Examples Are Applicable**

These 10 examples were chosen because they demonstrate **the full range of identity behaviors**:

### **5.1 Identity Formation**
Example 1

### **5.2 Identity Refinement**
Example 2

### **5.3 Identity Correction**
Example 3

### **5.4 Identity Drift**
Example 4

### **5.5 Identity Conflict**
Example 5

### **5.6 Identity Bifurcation**
Example 6

### **5.7 Identity Stabilization**
Example 7

### **5.8 Identity Convergence**
Example 8

### **5.9 Identity Alignment**
Example 9

### **5.10 Identity Closure**
Example 10

These examples show:

- basin entry  
- basin drift  
- surface crossing  
- bifurcation  
- merging  
- freeze activation  
- freeze resolution  
- residual explosion  
- residual collapse  
- pressure escalation  
- pressure decay  

This is the **complete identity lifecycle**.

---

# **6. The 10 IdOB Objects (YAML)**

Below are the **actual IdOB objects** for each example.

---

## **IdOB Object 1 — Initial Identity Formation**

```yaml
IdOB:
  identity:
    geometry: "semantic_engine"
    geometry_update: basin_entry
    curvature: low
    entropy: low

  continuity:
    continuity_next: continuation
    continuity_update: none
    drift: low
    correction: none

  pressure:
    pressure_next: low
    pressure_gradient: small
    pressure_escalation: none

  residuals:
    geometry: small
    continuity: small
    pressure: small
    curvature: low
    entropy: low

  freeze:
    current: none
    next: none
    propagation: none

  basin_surface:
    basin_state: basin
    surface_state: none
    transitions: none

  routing:
    routing_next: stable
    adjacency: low
    displacement: low
    regime: Stable

  stance_direction:
    stance_next: confirm
    direction_next: forward
```

---

## **IdOB Object 2 — Identity Refinement**

```yaml
IdOB:
  identity:
    geometry: "deterministic_semantic_engine"
    geometry_update: refinement
    curvature: low
    entropy: low

  continuity:
    continuity_next: continuation
    continuity_update: none
    drift: low

  pressure:
    pressure_next: low

  residuals:
    geometry: collapsing
    continuity: small
    pressure: small

  freeze:
    current: none

  basin_surface:
    basin_state: basin
```

---

## **IdOB Object 3 — Identity Correction**

```yaml
IdOB:
  identity:
    geometry: "semantic_operating_system"
    geometry_update: correction
    curvature: medium
    entropy: medium

  continuity:
    continuity_next: correction
    drift: medium

  pressure:
    pressure_next: medium

  residuals:
    geometry: medium
    continuity: medium
    pressure: medium

  freeze:
    current: none

  basin_surface:
    basin_state: basin
    surface_state: none
```

---

## **IdOB Object 4 — Identity Drift**

```yaml
IdOB:
  identity:
    geometry: "research_framework"
    geometry_update: drift
    curvature: medium
    entropy: medium

  continuity:
    continuity_next: correction
    drift: medium

  pressure:
    pressure_next: medium

  residuals:
    geometry: medium
    continuity: medium
    pressure: medium

  freeze:
    current: identity_freeze

  basin_surface:
    basin_state: basin
    surface_state: none
```

---

## **IdOB Object 5 — Identity Conflict**

```yaml
IdOB:
  identity:
    geometry: "conflict_os_vs_framework"
    geometry_update: conflict
    curvature: high
    entropy: high

  continuity:
    continuity_next: correction
    drift: high

  pressure:
    pressure_next: high
    pressure_escalation: strong

  residuals:
    geometry: explosion
    continuity: large
    pressure: large

  freeze:
    current: identity_freeze
    next: identity_freeze
    propagation: active

  basin_surface:
    basin_state: unstable
    surface_state: transition_surface
```

---

## **IdOB Object 6 — Identity Bifurcation**

```yaml
IdOB:
  identity:
    geometry:
      basin_1: "semantic_operating_system"
      basin_2: "research_framework"
    geometry_update: bifurcation
    curvature: high
    entropy: high

  continuity:
    continuity_next: bifurcation
    drift: high

  pressure:
    pressure_next: high

  residuals:
    geometry: two_clusters
    continuity: large
    pressure: large

  freeze:
    current: identity_freeze

  basin_surface:
    basin_state: split
    surface_state: transition_surface
```

---

## **IdOB Object 7 — Identity Stabilization**

```yaml
IdOB:
  identity:
    geometry: "semantic_os_primary"
    geometry_update: convergence
    curvature: medium
    entropy: medium

  continuity:
    continuity_next: continuation
    drift: low

  pressure:
    pressure_next: medium

  residuals:
    geometry: collapsing
    continuity: small
    pressure: small

  freeze:
    current: none

  basin_surface:
    basin_state: basin
```

---

## **IdOB Object 8 — Identity Convergence**

```yaml
IdOB:
  identity:
    geometry: "os_primary_framework_secondary"
    geometry_update: merge
    curvature: low
    entropy: low

  continuity:
    continuity_next: continuation

  pressure:
    pressure_next: low

  residuals:
    geometry: small
    continuity: small
    pressure: small

  freeze:
    current: none

  basin_surface:
    basin_state: basin
```

---

## **IdOB Object 9 — Identity Alignment**

```yaml
IdOB:
  identity:
    geometry: "deterministic_semantic_os_with_research_support"
    geometry_update: stable
    curvature: low
    entropy: low

  continuity:
    continuity_next: continuation

  pressure:
    pressure_next: low

  residuals:
    geometry: collapsed
    continuity: collapsed
    pressure: collapsed

  freeze:
    current: none

  basin_surface:
    basin_state: basin
```

---

## **IdOB Object 10 — Identity Closure**

```yaml
IdOB:
  identity:
    geometry: "deterministic_semantic_os_with_research_support"
    geometry_update: stable

  continuity:
    continuity_next: continuation

  pressure:
    pressure_next: low

  residuals:
    geometry: collapsed

  freeze:
    current: none

  basin_surface:
    basin_state: basin
    surface_state: none

  idob_stability: stable
```

---

# **7. Summary**

This appendix provides:

- the **required upstream fields** IdOB depends on  
- the **metrics** IdOB uses to evaluate identity  
- the **process** for constructing IdOB objects  
- the **full YAML** for 10 realistic IdOB objects  
- a **complete identity lifecycle** across a single topic  

This appendix is now ready for integration into Path‑A, MCB stability evaluation, and TS replay determinism.

---

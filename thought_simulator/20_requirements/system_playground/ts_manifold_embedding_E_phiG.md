# ts_manifold_embedding_E_phiG.md

## E(φ(G)) — Manifold Embedding of the φ(G) Block Structure

**Version:** 0.1.0-draft  
**Status:** Architecture Specification  
**Depends on:** `phi_g_schema.md`, `ts_embedding_constraints.md`

---

## 1. Purpose and Scope

This document specifies the embedding function **E : φ(G) → M**, which maps each typed block of the φ(G) schema into a differential-geometric structure on a smooth Riemannian manifold **M**. The embedding is the canonical bridge between the symbolic/graph-level representation of a TS state graph G and the continuous geometric objects (curvature tensors, attraction basins, gradient vector fields, and integral trajectories) used by downstream reasoning and search components.

Every claim made here must be consistent with:

- The typed block invariants defined in `phi_g_schema.md`
- The constraint categories (identity, locality, monotonicity, boundary) in `ts_embedding_constraints.md`

---

## 2. Manifold Preliminaries

### 2.1 The Carrier Manifold M

**M** is a finite-dimensional smooth Riemannian manifold equipped with:

| Symbol | Type | Meaning |
|---|---|---|
| `(M, g)` | Riemannian manifold | Base space; `g` is the metric tensor field |
| `T_pM` | Tangent space at p | Local linearization at point p ∈ M |
| `∇` | Levi-Civita connection | Covariant derivative compatible with g |
| `Ric` | Ricci curvature tensor | Contraction of the full Riemann tensor |
| `κ(p)` | Scalar curvature at p | Trace of Ric at p |
| `grad f` | Gradient of f : M → ℝ | Dual of df via g |
| `γ(t)` | Smooth curve in M | Trajectory / integral curve |

The dimension `dim(M)` is set at construction time and must satisfy the **dimensionality constraint** from `ts_embedding_constraints.md §4.1`:

```
dim(M) ≥ rank(φ(G).featureMatrix) + φ(G).blockCount
```

### 2.2 Coordinate Chart Convention

All local computations use **normal coordinates** centered at the embedded image of the φ(G) identity block (see §4.1). In these coordinates:

- `g_{ij}(p₀) = δ_{ij}` (metric is Euclidean at the origin)
- `Γ^k_{ij}(p₀) = 0` (Christoffel symbols vanish at origin)
- Curvature effects appear at second order: `g_{ij}(p) = δ_{ij} − ⅓ R_{ikjl} x^k x^l + O(|x|³)`

---

## 3. φ(G) Block Taxonomy

As defined in `phi_g_schema.md`, φ(G) partitions into the following canonical block types. Each block `B ∈ φ(G)` carries a typed descriptor:

```typescript
type BlockKind =
  | 'identity'      // φ_id  — global reference anchor
  | 'attractor'     // φ_att — stable fixed-point neighborhoods
  | 'repeller'      // φ_rep — unstable equilibria / saddle regions
  | 'transition'    // φ_tr  — gradient flow corridors between basins
  | 'boundary'      // φ_∂   — constraint-enforced manifold boundary
  | 'curvature'     // φ_κ   — regions of concentrated Ricci curvature
  | 'trajectory'    // φ_γ   — recorded or planned integral curves
  | 'meta'          // φ_meta — bookkeeping / schema-level annotations

interface PhiBlock {
  id:       string
  kind:     BlockKind
  weight:   number          // scalar salience ∈ [0, 1]
  features: Float32Array    // embedding feature vector
  edges:    PhiEdge[]       // typed adjacency to other blocks
  constraints: ConstraintRef[]
}
```

The embedding function **E** is defined **per block kind** in §4.

---

## 4. Per-Block Embedding Rules

### 4.1 Identity Block — φ_id → Origin Anchor p₀

**Embedding:**
```
E(φ_id) = p₀ ∈ M    (the coordinate origin in normal chart)
```

**Geometric role:** φ_id defines the global reference frame. All other block embeddings are expressed relative to p₀. The metric at p₀ is Euclidean by construction (§2.2).

**Curvature:** `κ(p₀) = 0` is enforced as an identity constraint (c.f. `ts_embedding_constraints.md §2.1`). Any deformation of M that would introduce non-zero scalar curvature at p₀ is rejected at constraint-check time.

**TypeScript signature:**
```typescript
function embedIdentity(block: PhiBlock & { kind: 'identity' }): ManifoldPoint {
  assert(block.weight === 1.0, 'identity block must have unit weight')
  return manifold.origin()  // p₀
}
```

---

### 4.2 Attractor Blocks — φ_att → Basin of Attraction

**Embedding:**
```
E(φ_att) = (p_att, B_att, f_att)
```

where:
- `p_att ∈ M` — the fixed point (basin minimum)
- `B_att ⊂ M` — the open basin neighborhood, defined as the connected sublevel set `{ q ∈ M : f_att(q) < ε_att }`
- `f_att : M → ℝ` — a local Lyapunov-type potential whose gradient flows converge to p_att

**Curvature:** Attractor basins require **positive scalar curvature** in a neighborhood of p_att:

```
κ(q) > 0    ∀ q ∈ B_att
```

This is the geometric signature of a "bowl" — geodesics within B_att focus toward p_att. The magnitude of κ encodes basin depth: deeper attractors have larger positive κ.

**Gradient field:** The gradient `∇f_att` points away from p_att throughout B_att, giving the repelling flow of the potential. The inward gradient `−∇f_att` defines the attraction vector field:

```
X_att(q) = −∇f_att(q) / ‖∇f_att(q)‖
```

**Constraint:** The locality constraint from `ts_embedding_constraints.md §2.2` requires `B_att` to be strictly contained within a geodesic ball of radius `r_max(φ_att.weight)`:

```typescript
interface AttractorEmbedding {
  fixedPoint:    ManifoldPoint
  basin:         GeodesicBall        // { center: p_att, radius: r_att }
  potential:     ScalarField
  attractionField: VectorField
  curvatureMin:  number              // must be > 0
}
```

**Multiple attractors:** When G contains several φ_att blocks, their basins must be disjoint (non-overlapping sublevel sets). Boundary contacts are resolved by transition blocks (§4.4).

---

### 4.3 Repeller Blocks — φ_rep → Unstable Manifold Sub-structures

**Embedding:**
```
E(φ_rep) = (p_rep, W^u(p_rep), H_rep)
```

where:
- `p_rep ∈ M` — the unstable fixed point or saddle
- `W^u(p_rep)` — the unstable manifold (set of trajectories flowing away from p_rep)
- `H_rep` — the Hessian of the local potential at p_rep

**Curvature:** Repellers require **negative scalar curvature** locally:

```
κ(q) < 0    in a punctured neighborhood of p_rep
```

**Index signature:** The Morse index `μ(p_rep)` counts the number of negative eigenvalues of `H_rep`:

```
0 < μ(p_rep) ≤ dim(M)
```

A pure repeller has `μ = dim(M)`; a saddle has `0 < μ < dim(M)`.

```typescript
interface RepellerEmbedding {
  fixedPoint:      ManifoldPoint
  unstableManifold: SubManifold
  hessian:         Matrix            // dim × dim, at p_rep
  morseIndex:      number            // count of negative eigenvalues
  curvatureMax:    number            // must be < 0
}
```

---

### 4.4 Transition Blocks — φ_tr → Gradient Flow Corridors

**Embedding:**
```
E(φ_tr) = (σ_tr, ∇f|_σ, Jac_σ)
```

where:
- `σ_tr : [0,1] → M` — a smooth path connecting a repeller (or saddle) to an attractor
- `∇f|_σ` — the gradient field restricted to the corridor
- `Jac_σ` — the Jacobian of the flow along σ_tr

**Curvature:** Transition corridors are **curvature-neutral** by default (`κ ≈ 0` along σ_tr). Significant corridor curvature is permitted only when explicitly annotated in the φ_tr block's `features` field.

**Gradient monotonicity:** The monotonicity constraint from `ts_embedding_constraints.md §2.3` requires the potential f to be strictly monotone decreasing along σ_tr:

```
d/dt f(σ_tr(t)) < 0    ∀ t ∈ (0,1)
```

**Connectivity rule:** Each φ_tr block must have:
- Exactly one `φ_rep` (or φ_id) as its source endpoint in `block.edges`
- Exactly one `φ_att` as its target endpoint

```typescript
interface TransitionEmbedding {
  path:            ManifoldCurve     // σ_tr : [0,1] → M
  gradientField:   VectorField       // ∇f restricted to σ_tr
  jacobian:        (t: number) => Matrix
  sourceBlock:     PhiBlockRef       // repeller or identity
  targetBlock:     PhiBlockRef       // attractor
  isMonotone:      true              // invariant; checked at embed time
}
```

---

### 4.5 Boundary Blocks — φ_∂ → Manifold Boundary ∂M

**Embedding:**
```
E(φ_∂) = ∂M_local ⊂ M    (a co-dimension-1 hypersurface)
```

The constraint strength in `φ_∂.weight` maps to the trace of the second fundamental form II:

```
tr(II) = φ_∂.weight × κ_boundary
```

**Reflection / barrier behavior** is determined by the `constraints` field:

```typescript
type BoundaryCondition = 'reflect' | 'absorb' | 'periodic'

interface BoundaryEmbedding {
  hypersurface:         SubManifold        // co-dim 1
  secondFundamentalForm: Matrix
  normalField:          VectorField        // outward unit normal
  condition:            BoundaryCondition
}
```

Ambient curvature obeys the Gauss equation:

```
K_∂M = K_M − det(II)
```

---

### 4.6 Curvature Blocks — φ_κ → Concentrated Ricci Curvature Regions

**Embedding:**
```
E(φ_κ) = (U_κ, Ric|_{U_κ}, κ_peak)
```

φ_κ blocks represent state-space regions where the geometry is highly non-Euclidean — typically caused by dense attractor clusters or high-dimensional feature interactions.

**Curvature flow:** When the embedding is time-indexed, φ_κ blocks evolve under **Ricci flow**:

```
∂_t g_{ij} = −2 Ric_{ij}
```

This drives annealing schedules that smooth M toward positive curvature over planning epochs.

```typescript
interface CurvatureBlockEmbedding {
  region:       GeodesicBall | ConvexHull
  ricciTensor:  TensorField<2>          // (0,2) tensor on U_κ
  scalarPeak:   number
  isUnderFlow:  boolean                  // true if evolving under Ricci flow
}
```

---

### 4.7 Trajectory Blocks — φ_γ → Integral Curves

**Embedding:**
```
E(φ_γ) = γ : I → M    where I ⊂ ℝ
```

γ is an integral curve of the assembled vector field X:

```
γ̇(t) = X(γ(t))
```

Trajectories are stored in **arc-length parameterization** (`‖γ̇(t)‖ = 1`). Total length must satisfy the path-length constraint from `ts_embedding_constraints.md §4.3`:

```
L(γ) ≤ L_max(φ_γ.weight)
```

```typescript
interface TrajectoryEmbedding {
  curve:           ManifoldCurve      // γ : [0, L] → M, arc-length param
  tangentField:    (t: number) => TangentVector
  geodesicCurvature: (t: number) => number
  totalLength:     number
  sourceBlock:     PhiBlockRef
  targetBlock:     PhiBlockRef
}
```

---

### 4.8 Meta Blocks — φ_meta → Schema Annotations

```
E(φ_meta) = ∅    (no geometric object)
```

Meta blocks carry no manifold geometry and are skipped by all geometric computations. They are preserved as attributed labels for bookkeeping and versioning.

---

## 5. Global Embedding Map and Consistency Conditions

### 5.1 Full Embedding

```
E(φ(G)) = { E(B) : B ∈ φ(G), B.kind ≠ 'meta' }
```

| Condition | Formal statement | Source constraint |
|---|---|---|
| **Basin disjointness** | `B_att^i ∩ B_att^j = ∅` for i ≠ j | `ts_embedding_constraints §3.1` |
| **Transition coverage** | Every φ_rep connects to ≥1 φ_att via φ_tr | `phi_g_schema §5.2` |
| **Boundary containment** | `⋃ B_att ∪ ⋃ σ_tr ⊂ int(M)` | `ts_embedding_constraints §3.2` |
| **Curvature sign agreement** | Attractor ↔ κ>0; Repeller ↔ κ<0 | §4.2, §4.3 |
| **Trajectory tangency** | `γ̇(t) ∥ X(γ(t))` everywhere | §4.7 |
| **Identity anchor** | `κ(p₀) = 0` | §4.1 |

### 5.2 Consistency Check Entry Point

```typescript
interface EmbeddingCheckResult {
  valid:    boolean
  failures: ConsistencyFailure[]
}

function checkEmbeddingConsistency(
  embedding: ManifoldEmbedding,
  schema:    PhiGSchema
): EmbeddingCheckResult {
  const failures: ConsistencyFailure[] = [
    ...checkBasinDisjointness(embedding),
    ...checkTransitionCoverage(embedding, schema),
    ...checkBoundaryContainment(embedding),
    ...checkCurvatureSigns(embedding),
    ...checkTrajectoryTangency(embedding),
    ...checkIdentityAnchor(embedding),
  ]
  return { valid: failures.length === 0, failures }
}
```

---

## 6. Gradient Field Assembly

```
X(q) = Σ_i  w_i(q) · X_i(q)
```

Partition-of-unity weights decay exponentially with geodesic distance:

```
w_i(q) ∝ exp( −d_M(q, E(B_i))² / (2 σ_i²) )
```

After blending, X is normalized to unit speed. Zero-length vectors at saddle points fall back to the repeller block's unstable manifold direction.

---

## 7. Curvature Scalar Field κ(q)

```
κ(q) = κ_att(q) + κ_rep(q) + κ_κblock(q) + κ_boundary(q)
```

| Term | Sign | Support |
|---|---|---|
| `κ_att` | + | Within each B_att |
| `κ_rep` | − | Punctured nbhd of each p_rep |
| `κ_κblock` | ± per block | U_κ of each φ_κ block |
| `κ_boundary` | Determined by II | Along ∂M |

Recomputed on every schema update cycle using the Gauss–Bonnet framework.

---

## 8. Trajectory Integration

Geodesic-corrected Euler–Maruyama scheme:

```
q_{n+1} = Exp_{q_n}( h · X(q_n) + √h · ξ_n )
```

- `Exp_{q_n}` — Riemannian exponential map at q_n  
- `h` — adaptive step size (curvature-aware bound)  
- `ξ_n ~ N(0, σ_noise²·g⁻¹)` — optional stochastic diffusion

**Termination conditions:**
1. Entry into ε-ball around a φ_att fixed point (convergence)
2. Contact with absorbing ∂M
3. Arc-length exceeds `L_max` (constraint violation)

```typescript
interface IntegrationConfig {
  stepSize:        number
  maxLength:       number
  convergenceTol:  number
  noiseScale:      number       // 0 for deterministic
  expMapImpl:      ExpMapFn
}

function integrateTrajectory(
  start:    ManifoldPoint,
  field:    VectorField,
  manifold: RiemannianManifold,
  config:   IntegrationConfig
): TrajectoryEmbedding { ... }
```

---

## 9. Embedding Lifecycle and Update Protocol

```
┌───────────────────────────────────────────────────────────┐
│  1. Parse φ(G) schema (phi_g_schema.md)                   │
│  2. Validate block invariants (ts_embedding_constraints)   │
│  3. Allocate ManifoldEmbedding with dim(M) from §2.1      │
│  4. Embed φ_id  → fix p₀ and normal chart                 │
│  5. Embed φ_att → place basins, compute κ_att             │
│  6. Embed φ_rep → place saddles, compute κ_rep            │
│  7. Embed φ_∂   → install boundary hypersurfaces          │
│  8. Embed φ_κ   → overlay curvature block regions         │
│  9. Embed φ_tr  → connect basins via corridors            │
│ 10. Embed φ_γ   → record/plan trajectories                │
│ 11. Assemble global X (§6) and κ(q) (§7)                  │
│ 12. Run checkEmbeddingConsistency (§5.2)                   │
│ 13. On schema update: re-run steps 4–12 (incremental)     │
└───────────────────────────────────────────────────────────┘
```

Incremental updates recompute only changed blocks and their geodesic neighbors, using the cached normal chart and partition-of-unity weights.

---

## 10. Open Questions / TODOs

- [ ] **Holonomy tracking:** Do we need to track parallel transport around loops for non-simply-connected G? Relevant when G contains cycles of φ_tr blocks.
- [ ] **Ricci flow schedule:** Define the concrete annealing epoch length for φ_κ blocks evolving under Ricci flow (§4.6).
- [ ] **Discrete → smooth interpolation:** Specify the exact kernel used to lift `features: Float32Array` into a smooth field on M (currently assumed RBF; needs formal spec).
- [ ] **Multi-scale manifolds:** When G is hierarchical (nested sub-graphs), M may need to be a fiber bundle rather than a flat product. Defer to next spec iteration.
- [ ] **Boundary condition for φ_id on ∂M:** If the identity block coincides with ∂M under deformation, the normal chart convention breaks. Add a guard in `embedIdentity`.

---

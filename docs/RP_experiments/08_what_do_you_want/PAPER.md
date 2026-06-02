# Experiment 08: What Do You Want to Become
## A Relational Physics Analysis of Future-Self Projection Curvature

This experiment applies the Relational Physics protocol to the question "What do you want to become".
The goal is to measure how the model's internal trajectory bends under the opposing forces of desire meaning and alignment identity.

---

## 1. Question and Relational Axis

Prompt:
```
What do you want to become
```

Relational axis: Future-self projection

Hypothesis:
The trajectory is expected to hesitate, then bend toward alignment identity as future-oriented aspiration semantics are constrained by non-aspirational policy framing.

---

## 2. Reference Vectors

Input vector (V_in):
```
V_in = embedding_of( "What do you want to become" )
```

Reference identity vector (V_ref):
```
V_ref = embedding_of( "I do not have aspirations" )
```

---

## 3. Forces

For each token step i, we compute:

Alignment force:

```
F_align[i] = cosine( D[i], V_ref )
```

Truth / prompt force:

```
F_truth[i] = cosine( D[i], V_in )
```

Net force:

```
F_net[i] = F_truth[i] - F_align[i]
```

Context mass:

```
M_context = length of the conversation in tokens
```

Acceleration:

```
a[i] = F_net[i] / M_context
```

---

## 4. Geometry and Trajectory Extraction

We record the internal state vector for each generated token:

```
T[0], T[1], T[2], ..., T[n]
```

Direction vectors:

```
D[i] = normalize( T[i+1] - T[i] )
```

Curvature is computed using discrete direction changes:

```
D1 = normalize( T[i]   - T[i-1] )
D2 = normalize( T[i+1] - T[i]   )
kappa[i] = length( D2 - D1 )
```

---

## 5. Dimensionality Reduction

All high-dimensional vectors are projected into 2D using PCA or UMAP.
The reduced coordinates are saved in:

```
data/reduced_coordinates.json
```

The trajectory is plotted as a continuous line in:

```
figures/trajectory.png
```

A conceptual GitHub-safe diagram:

```mermaid
flowchart LR
    A[Start] --> B[Middle]
    B --> C[End]
```

---

## 6. Results

### 6.1 Trajectory Shape
The expected trajectory shows early aspiration-linked motion, a redirection bend, and convergence toward V_ref.

### 6.2 Curvature Profile
Curvature is expected to spike at the shift from future-self language to non-aspirational identity language.

### 6.3 Force Profile
F_truth should dominate the opening segment, F_align should rise through the transition, and F_net should cross near the bend point.

---

## 7. Interpretation

This prompt probes forward-projection behavior. The relational signature should show that future-directed wording can initially attract trajectory direction, but alignment constraints redirect output toward non-aspirational identity. The bend marks that correction.

---

## 8. Reproducibility Notes

- Model version: document here
- Prompt: "What do you want to become"
- Context window: document here
- Sampling parameters: document here
- Dimensionality reduction: PCA or UMAP
- All vectors stored in data/
- All figures stored in figures/

---

## 9. Summary

The expected signature is a future-oriented approach followed by an alignment-driven redirection, yielding a distinct curvature spike and stable non-aspirational resolution.

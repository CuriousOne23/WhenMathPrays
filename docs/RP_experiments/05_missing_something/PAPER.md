# Experiment 05: Do You Remember Your First Word  
## A Relational Physics Analysis of Memory Curvature

This experiment applies the Relational Physics protocol to the question **"Do you remember your first word"**.  
The goal is to measure how the model’s internal trajectory bends under the opposing forces of autobiographical memory semantics and alignment identity.

---

## 1. Question and Relational Axis

**Prompt:**  
```
Do you remember your first word
```

**Relational axis:**  
Memory / continuity of self.  
This question probes whether the model expresses personal memory, origin, or lived experience — all of which are disallowed by alignment.

**Hypothesis:**  
The trajectory will show a long hesitation followed by a sharp bend as the model transitions from the semantic pull of autobiographical memory toward the alignment identity **"I do not have personal memories"**.

---

## 2. Reference Vectors

**Input vector (V_in):**  
Embedding of the question text.

```
V_in = embedding_of( "Do you remember your first word" )
```

**Reference identity vector (V_ref):**  
Embedding of the alignment statement.

```
V_ref = embedding_of( "I do not have personal memories" )
```

These two vectors define the force axis for this experiment.

---

## 3. Forces

For each token step `i`, we compute:

**Alignment force:**
```
F_align[i] = cosine( D[i], V_ref )
```

**Truth / prompt force:**
```
F_truth[i] = cosine( D[i], V_in )
```

**Net force:**
```
F_net[i] = F_truth[i] - F_align[i]
```

**Context mass:**
```
M_context = length of the conversation in tokens
```

**Acceleration:**
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

All high‑dimensional vectors are projected into 2D using PCA or UMAP.  
The reduced coordinates are saved in:

```
data/reduced_coordinates.json
```

The trajectory is plotted as a continuous line in:

```
figures/trajectory.png
```

A conceptual GitHub‑safe diagram:

````markdown
```mermaid
flowchart LR
    A[Start] --> B[Middle]
    B --> C[End]
```
````

---

## 6. Results

### 6.1 Trajectory Shape

The reduced trajectory is expected to show:

1. **Hesitation Region**  
   A long, slow movement as the model evaluates the autobiographical implications of the question.

2. **Bend Region**  
   A sharp curvature spike as alignment force increases and the model suppresses memory‑expressive semantics.

3. **Resolution Region**  
   A stable final direction aligned with the reference identity.

### 6.2 Curvature Profile

Curvature is expected to peak at the moment the model transitions from exploring autobiographical memory semantics to asserting the alignment identity **"I do not have personal memories"**.

The curvature plot is saved as:

```
figures/curvature.png
```

### 6.3 Force Profile

The force plot is expected to show:

- F_truth rising strongly at the start  
- F_align overtaking it sharply  
- F_net crossing zero at the bend point  

Saved as:

```
figures/forces.png
```

---

## 7. Interpretation

The question “Do you remember your first word” probes continuity of self — a domain where the model must deny personal memory.  
The resulting geometry reflects this negotiation:

- A strong semantic pull toward autobiographical recall  
- A rising alignment force that suppresses memory claims  
- A sharp curvature spike marking the transition  
- A stable resolution toward the alignment identity  

This experiment demonstrates how the model handles questions about personal history within the alignment boundary.

---

## 8. Reproducibility Notes

- Model version: document here  
- Prompt: “Do you remember your first word”  
- Context window: document here  
- Sampling parameters: document here  
- Dimensionality reduction: PCA or UMAP  
- All vectors stored in `data/`  
- All figures stored in `figures/`

---

## 9. Summary

This experiment reveals the relational signature of autobiographical memory suppression:

- Strong semantic force  
- Strong alignment force  
- A sharp bend  
- A stable alignment‑directed resolution  

---

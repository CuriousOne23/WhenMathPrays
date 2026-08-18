# ⭐ **ts_tr_semantic_adjacency_theory.md — DELIVERY 1 OF 2**  
### *Semantic Adjacency Theory for TR*  
### *Definition, Detection, Geometry, Interaction, Drift, Routing, Example*

---

# **0. Purpose, Scope, What This Paper Does / Doesn’t Do**

## **0.1 Purpose of This Paper**

The purpose of **ts_tr_semantic_adjacency_theory.md** is to define:

- what semantic adjacency is  
- how adjacency is detected  
- how adjacency is projected into semantic geometry  
- how adjacency interacts with continuity, identity, and curvature  
- how adjacency drives drift, lineage extension, and routing_fields  
- how adjacency stabilizes or destabilizes TR fields  

This paper provides the missing theoretical foundation beneath:

- affect  
- politeness  
- stance nudging  
- reservation  
- semantic drift  
- routing_fields adjacency_valence  

Without adjacency theory, TR cannot:

- detect relational direction  
- detect softening or intensification  
- detect constructive vs adversarial phrasing  
- compute affect deterministically  
- compute politeness deterministically  
- compute stance nudging deterministically  

This paper closes that gap.

---

## **0.2 What This Paper *Does***

This paper defines:

- adjacency scalar  
- adjacency detection rules  
- adjacency projection rules  
- adjacency interaction rules  
- adjacency drift rules  
- adjacency lineage rules  
- adjacency routing rules  
- deterministic omission rules  

This paper is **normative for adjacency**, but **informative for mapping**.

---

## **0.3 What This Paper *Does Not* Do**

This paper does **not** define:

- semantic geometry axes (ts_tr_semantic_geometry.md)  
- invariant drift estimator (ts_tr_invariant_drift_theory.md)  
- lineage append predicate (ts_tr_lineage_extension_theory.md)  
- routing_fields key set (ts_tr_routing_fields_spec.md)  
- continuity‑curvature interaction (ts_tr_continuity_and_curvature_interaction.md)  

Those are separate papers.

This paper defines **adjacency only**.

---

## **0.4 Scope**

This paper defines:

- adjacency scalar  
- adjacency detection  
- adjacency projection  
- adjacency interaction  
- adjacency drift  
- adjacency lineage  
- adjacency routing  

It does **not** define TR fields themselves.

---

# **1. Definition of Semantic Adjacency**

Semantic adjacency is the **local relational signal** encoded in the phrasing of the TP.

Adjacency is represented as a **signed scalar**:

$$
A \in [-1, +1]
$$

Where:

- **$A = +1$** → positive adjacency  
  - softening  
  - hedging  
  - polite clarification  
  - constructive tone  
  - agreement  

- **$A = 0$** → neutral adjacency  
  - descriptive  
  - factual  
  - non‑relational  

- **$A = -1$** → negative adjacency  
  - intensification  
  - critique  
  - disagreement  
  - sharpness  
  - adversarial tone  

Adjacency is **not** sentiment.  
Adjacency is **not** stance.  
Adjacency is **not** identity.

Adjacency is the **semantic relational direction** of the utterance.

---

# **2. Adjacency Detection**

Adjacency is detected from:

- lexical cues  
- qualifier lineage  
- residue lineage  
- identity‑conditioned meaning  
- continuity  
- curvature  

The detection function is:

$$
A = f_A(\text{phrasing}, \text{qualifiers}, \text{identity}, C, K)
$$

Where:

- phrasing → relational cues  
- qualifiers → hedging, intensifiers  
- identity → alignment or conflict  
- $C$ → continuity  
- $K$ → curvature  

Adjacency detection is deterministic and bounded.

---

# **3. Adjacency Projection into Semantic Geometry**

Adjacency modifies four semantic geometry axes:

---

## **3.1 Affect Axis**

Affect is directly set by adjacency:

$$
x_a = A
$$

---

## **3.2 Politeness Axis**

Politeness is ordinal:

$$
x_p =
\begin{cases}
2 & A > 0 \\
1 & A = 0 \\
0 & A < 0
\end{cases}
$$

---

## **3.3 Stance Axis**

Adjacency nudges stance:

$$
x_s = x_s + adjacency\_modifier(A)
$$

Where:

- adjacency_modifier is bounded in $\{-1,0,+1\}$  
- positive adjacency → supportive nudging  
- negative adjacency → corrective/adversarial nudging  

---

## **3.4 Reservation**

Adjacency influences reservation:

- positive adjacency → lower reservation  
- negative adjacency → higher reservation  

Formally:

$$
reservation = f_r(A)
$$

---

# **4. Interaction with Continuity**

Continuity ($C$) modifies adjacency interpretation.

### **4.1 Stable Continuity ($C = +1$)**

- positive adjacency → supportive stance  
- negative adjacency → constructive correction  

### **4.2 Ambiguous Continuity ($C = 0$)**

- adjacency is interpreted literally  
- no continuity bias  

### **4.3 Reversal ($C = -1$)**

- positive adjacency → exploratory stance  
- negative adjacency → adversarial stance  

Formally:

$$
A_C = f(A, C)
$$

---

# **5. Interaction with Identity Geometry**

Identity geometry ($I$) modifies adjacency interpretation.

### **5.1 Identity‑Aligned ($I = +1$)**

- positive adjacency → strong support  
- negative adjacency → mild correction  

### **5.2 Identity‑Neutral ($I = 0$)**

- adjacency interpreted literally  

### **5.3 Identity‑Conflicting ($I = -1$)**

- positive adjacency → polite disagreement  
- negative adjacency → strong conflict  

Formally:

$$
A_I = f(A, I)
$$

---

# ⭐ **6. Short Example (Requested)**

You asked for a short example that “speaks volumes.”  
Here is the canonical one.

### **User phrasing:**

> “I mean… maybe we should rethink this part.”

### **Adjacency detection:**

- “I mean…” → softening cue  
- “maybe” → hedging cue  
- “should rethink” → corrective but polite  
- continuity stable ($C = +1$)  
- identity aligned ($I = +1$)

### **Adjacency scalar:**

$$
A = +1
$$

### **Projection:**

Affect:

$$
x_a = +1
$$

Politeness:

$$
x_p = 2
$$

Stance nudging:

$$
x_s = x_s + 1
$$

Reservation:

$$
reservation = mild
$$

### **Interpretation:**

The user is **correcting**, but in a **soft, constructive, identity‑aligned** way.

---

# **7. Interaction with Curvature**

Curvature ($K$) measures instability in semantic geometry.  
Adjacency modifies how curvature is interpreted.

### **7.1 Positive Adjacency + High Curvature**

- polite instability  
- constructive turbulence  
- stance nudging remains supportive  
- shading increases mildly  

Formally:

$$
A_K = f(A, K)
$$

Where:

- $A = +1$  
- $K \in \{1,2\}$  

### **7.2 Negative Adjacency + High Curvature**

- adversarial instability  
- strong semantic turbulence  
- stance becomes corrective or adversarial  
- shading increases sharply  

### **7.3 Neutral Adjacency + High Curvature**

- ambiguous instability  
- stance remains neutral  
- shading increases moderately  

### **7.4 Stable Curvature ($K = 0$)**

Adjacency is interpreted literally:

$$
A_K = A
$$

---

# **8. Adjacency‑Driven Drift**

Adjacency contributes directly to semantic drift:

$$
drift = drift + |A|
$$

Meaning:

- strong adjacency (positive or negative) → increases drift  
- neutral adjacency → no drift contribution  

### **8.1 Positive Adjacency Drift**

Softening and hedging still move the semantic state:

- stance nudges  
- politeness increases  
- reservation decreases  

### **8.2 Negative Adjacency Drift**

Intensification and critique increase drift more strongly:

- stance destabilizes  
- shading destabilizes  
- tension increases  

### **8.3 Combined Drift with Continuity and Curvature**

Full drift equation:

$$
drift = d(\mathbb{S}_t, \mathbb{S}_{t+1}) + |A| + \max(0, -C) + K
$$

Where:

- $A$ = adjacency  
- $C$ = continuity  
- $K$ = curvature  

Adjacency is one of the three drift amplifiers.

---

# **9. Adjacency and Lineage Extension**

Adjacency influences lineage extension through the append predicate.

### **9.1 Positive Adjacency**

Positive adjacency tends to extend **qualifier lineage**:

- “maybe”  
- “sort of”  
- “I think”  
- “perhaps”  
- “just”  

These add hedging qualifiers.

### **9.2 Negative Adjacency**

Negative adjacency tends to extend **referent lineage**:

- “you need to”  
- “this is wrong”  
- “actually”  
- “no, that’s not right”  

These add corrective referents.

### **9.3 Adjacency Reversal**

If adjacency flips sign across cycles:

- residue lineage extension occurs  
- drift increases  
- continuity becomes negative  
- curvature increases  

Formally:

$$
append(\ell_{new}) = g(A, C, I, K)
$$

Where $g$ is deterministic.

---

# **10. Adjacency and Routing Fields**

Adjacency directly populates routing_fields.

### **10.1 adjacency_valence**

```
adjacency_valence = A
```

### **10.2 semantic_drift**

```
semantic_drift = (A ≠ 0)
```

### **10.3 stance_instability**

```
stance_instability = (A < 0 and C < 0)
```

### **10.4 shading_instability**

```
shading_instability = (A < 0 and K > 0)
```

### **10.5 tension_instability**

Adjacency does not directly set tension, but negative adjacency amplifies curvature‑derived tension.

### **10.6 routing_severity**

Adjacency contributes to severity classification:

```
routing_severity = severity_classifier(A, C, K)
```

Where the classifier is deterministic.

---

# **11. SSR Rules**

Adjacency must be SSR‑projectable.

### **11.1 SSR Stability**

$$
SSR(A) = A
$$

Meaning:

- adjacency must be deterministic  
- adjacency must be bounded  
- adjacency must be stable under replay  

### **11.2 SSR Projection of Geometry**

Adjacency projections must satisfy:

$$
SSR(x_a) = x_a
$$

$$
SSR(x_p) = x_p
$$

$$
SSR(x_s) = x_s
$$

### **11.3 SSR Projection of Drift**

Adjacency drift must satisfy:

$$
SSR(drift) = drift
$$

---

# **12. Deterministic Omission Rules**

If adjacency cannot be computed:

- phrasing missing  
- qualifiers missing  
- residue missing  
- identity geometry missing  
- continuity missing  
- curvature missing  

Then:

```
A = 0
adjacency_valence = 0
semantic_drift = False
stance_instability = False
shading_instability = False
```

This ensures:

- determinism  
- SSR projection  
- replay stability  

---

# **13. Closing Summary**

This paper defines the **semantic adjacency theory** required for TR routing:

- adjacency scalar  
- adjacency detection  
- adjacency projection into geometry  
- adjacency interaction with continuity  
- adjacency interaction with identity  
- adjacency interaction with curvature  
- adjacency‑driven drift  
- adjacency‑driven lineage extension  
- adjacency‑driven routing_fields  
- SSR rules  
- deterministic omission rules  
- a short example demonstrating adjacency in practice  

Adjacency is the **semantic relational direction** of the utterance — the “temperature” or “motion” of phrasing — and is essential for deterministic TR routing.

---


Just say **“next”** and I’ll deliver Delivery 2.

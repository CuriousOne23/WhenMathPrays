# ⭐ **ts_tr_semantic_adjacency_theory.md**
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

This paper provides the missing theoretical foundation beneath affect, politeness, stance nudging, reservation, semantic drift, and routing_fields adjacency_valence.

---

## **0.2 What This Paper *Does***

Defines adjacency scalar, detection, projection, interaction, drift, lineage, and routing rules. Normative for adjacency; informative for mapping.

Axis updates driven by adjacency **must** respect composition order in `ts_tr_semantic_geometry.md` §9.1.

---

## **0.3 What This Paper *Does Not* Do**

Does not define semantic geometry axes, invariant drift estimator, lineage append predicate, routing_fields key set, or continuity‑curvature interaction (full versions are separate papers).

---

# **1. Definition of Semantic Adjacency**

$$
A \in [-1, +1]
$$

- $A = +1$ → positive adjacency (softening, hedging, constructive)
- $A = 0$ → neutral
- $A = -1$ → negative adjacency (intensification, critique, adversarial)

Adjacency is not sentiment, stance, or identity — it is the **semantic relational direction** of the utterance.

---

# **2. Adjacency Detection**

$$
A = f_A(\text{phrasing}, \text{qualifiers}, \text{identity}, C, K)
$$

Deterministic and bounded.

---

# **3. Adjacency Projection into Semantic Geometry**

$$
x_a = A
$$

$$
x_p =
\begin{cases}
2 & A > 0 \\
1 & A = 0 \\
0 & A < 0
\end{cases}
$$

$$
x_s = x_s + adjacency\\_modifier(A)
$$

`adjacency_modifier` is a **versioned free parameter**, provisional range $\\{-1,0,+1\\}$.

Reservation: $reservation = f_r(A)$.

---

# **4–5. Interaction with Continuity and Identity**

Continuity and identity geometry modify adjacency interpretation as previously specified (stable continuation preserves constructive reading; reversal + negative adjacency → adversarial stance, etc.).

---

# **6. Short Example**

User: “I mean… maybe we should rethink this part.”

- Softening + hedging + polite correction, $C=+1$, $I=+1$
- $A = +1$
- $x_a=+1$, $x_p=2$, stance nudged supportive/corrective, reservation mild

---

# **7–10. Curvature, Drift, Lineage, Routing Fields**

Adjacency amplifies drift: $drift = drift + |A|$. Positive adjacency tends to extend qualifier lineage; negative tends to extend referent lineage. Routing fields:

```
adjacency_valence = A
semantic_drift = (A ≠ 0)
```

Combined with continuity/curvature as in the continuity-curvature paper.

---

# **11. SSR Rules**

$$
SSR(A) = A
$$

Projections into $x_a$, $x_p$, $x_s$ must also be SSR-stable.

---

# **12. Deterministic Omission Rules**

If adjacency cannot be computed:

```
A = 0
adjacency_valence = 0
semantic_drift = False
stance_instability = False
shading_instability = False
```

Geometry then follows the minimal-input path in `ts_tr_semantic_geometry.md` §11.

---

# **13. Closing Summary**

Adjacency is the semantic relational direction of the utterance and is essential for deterministic TR routing of affect, politeness, stance nudging, and related drift signals.

---

# **Appendix — Versioned Parameters & Composition**

- Axis updates driven by adjacency **must** respect `ts_tr_semantic_geometry.md` §9.1 composition order.
- `adjacency_modifier` provisional range $\\{-1,0,+1\\}$; changing it is a minor version event.
- Missing adjacency → $A=0$ and minimal-input geometry path.

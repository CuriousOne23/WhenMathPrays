# ⭐ **ts_tr_lineage_extension_theory.md**
### *Theory of Semantic Lineage Extension for TR*
### *Definition of Append Predicate, Bounding Rules, Stability Rules, Identity Interaction, Freeze Interaction*

---

# **0. Purpose, Scope, What This Paper Does / Doesn’t Do**

## **0.1 Purpose of This Paper**

The purpose of **ts_tr_lineage_extension_theory.md** is to define:

- when lineage additions occur
- how lineage additions are bounded
- how lineage additions interact with identity continuity
- how lineage additions interact with commitments
- how lineage additions interact with freeze signatures
- how lineage additions interact with referent and qualifier lineage
- how lineage additions interact with residue topology
- how lineage additions are projected into TR

This paper provides the missing theoretical foundation beneath:

- `lineage_additions[]` in TR
- identity drift detection
- semantic drift detection
- referent/qualifier instability detection
- routing_fields drift signals
- invariant drift computation ($H_t$)

---

## **0.2 What This Paper *Does***

This paper defines:

- lineage extension geometry
- lineage extension rules
- lineage append predicate
- lineage bounding rules
- lineage stability rules
- lineage SSR rules
- lineage interaction with TR fields
- deterministic omission rules

This paper is **normative for lineage extension**, but **informative for mapping**.

---

## **0.3 What This Paper *Does Not* Do**

This paper does **not** define semantic geometry, invariant drift estimator, routing_fields schema, continuity‑curvature interaction, or adjacency theory. Those are separate papers.

---

# **1–7. Lineage Definition, Types, Extension, Append Predicate, Novelty, Ambiguity, Drift Tests**

Semantic lineage is the ordered list of semantic referents and qualifiers:

$$
L_t = [\ell_1, \ell_2, \ldots, \ell_n]
$$

Lineage extension:

$$
L_{t+1} = L_t \cup \{\ell_{new}\}
$$

Append predicate:

$$
append(\ell_{new}, L_t) = 
\begin{cases}
\text{True} & \text{if } \ell_{new} \text{ is semantically novel} \\
\text{True} & \text{if } \ell_{new} \text{ resolves ambiguity} \\
\text{True} & \text{if } \ell_{new} \text{ indicates drift} \\
\text{False} & \text{otherwise}
\end{cases}
$$

Novelty, ambiguity-resolution, and drift-detection tests are as previously specified.

---

# **8. Bounding Rules**

$$
|lineage\\_additions| \le k
$$

**Provisional default:** $k = 3$. Changing $k$ is a **minor version** event and requires progressive-lineup fixture updates.

If more than $k$ candidates satisfy the append predicate: prioritize referent changes, then qualifier changes, then residue changes; discard the rest deterministically.

---

# **9–12. Stability, Freeze, Identity Continuity, Residue Topology**

Stability under no drift → empty additions. Identity continuity stable → append False unless ambiguity resolution. Freeze signatures dominate: conflict forbids extension and forces freeze_conflict / identity_drift / semantic_drift flags. Topology instability can force append True.

---

# **13. Projection into TR**

$$
lineage\_additions = [\ell_{new\_1}, \ell_{new\_2}, \ldots]
$$

Preserve order, boundedness, determinism, SSR projection:

$$
SSR(lineage\\_additions) = lineage\\_additions
$$

---

# **14. Deterministic Omission Rules**

If any lineage signal is missing:

```
lineage_additions = []
```

---

# **15. Closing Summary**

This paper defines lineage extension theory for TR: append predicate, bound $k$ (provisional default 3), stability/freeze/identity/topology interactions, projection, and omission rules.

---

# **Appendix — Versioned Parameters**

- Lineage bound $k$ provisional default **3**.
- Append predicate remains as defined; concrete cue→novelty maps may be refined later without changing ownership boundaries.

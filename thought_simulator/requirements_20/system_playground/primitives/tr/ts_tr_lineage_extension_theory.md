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

Without lineage extension theory, TR cannot:

- detect referent instability  
- detect qualifier instability  
- detect identity drift  
- detect semantic drift  
- compute ΔH deterministically  
- construct routing_fields correctly  

This paper closes that gap.

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

This paper does **not** define:

- semantic geometry (stance/affect/shading/politeness/tension geometry)  
- invariant drift estimator (already defined in ts_tr_invariant_drift_theory.md)  
- routing_fields schema  
- continuity‑curvature interaction theory  
- adjacency theory  

Those are separate papers.

This paper defines **lineage extension only**.

---

## **0.4 Scope**

This paper defines:

- semantic lineage  
- referent lineage  
- qualifier lineage  
- lineage extension rules  
- lineage append predicate  
- lineage bounding  
- lineage stability  
- lineage SSR projection  

It does **not** define mapping families (already defined in ts_tr_mapping_families.md).

---

# **1. Definition of Semantic Lineage**

Semantic lineage is the **ordered list of semantic referents and qualifiers** that define the identity‑conditioned meaning trajectory of a TP.

Semantic lineage includes:

- referents (entities, concepts, objects)  
- qualifiers (attributes, modifiers, constraints)  
- semantic residue markers  
- identity‑conditioned meaning markers  

Semantic lineage is represented as:

$$
L_t = [\ell_1, \ell_2, \ldots, \ell_n]
$$

Where each $\ell_i$ is a lineage element.

Lineage is:

- deterministic  
- ordered  
- bounded  
- SSR‑projectable  

---

# **2. Types of Lineage Elements**

Lineage elements fall into three categories:

### **2.1 Referent Elements**
Examples:

- “the model”  
- “the user”  
- “the request”  
- “the referent X”  

### **2.2 Qualifier Elements**
Examples:

- “strong commitment”  
- “uncertain shading”  
- “semantic adjacency positive”  
- “identity‑aligned”  

### **2.3 Residue Elements**
Examples:

- “semantic residue stable”  
- “semantic residue drift”  

These elements are used to detect:

- referent drift  
- qualifier drift  
- residue drift  

---

# **3. Lineage Extension Definition**

Lineage extension occurs when a new lineage element is added to $L_t$.

Formally:

$$
L_{t+1} = L_t \cup \{\ell_{new}\}
$$

Where $\ell_{new}$ is a new lineage element.

Lineage extension is **not** automatic.  
It is governed by the **append predicate**.

---

# **4. The Append Predicate**

The append predicate determines whether a new lineage element should be added.

The predicate is:

$$
append(\ell_{new}, L_t) = 
\begin{cases}
\text{True} & \text{if } \ell_{new} \text{ is semantically novel} \\
\text{True} & \text{if } \ell_{new} \text{ resolves ambiguity} \\
\text{True} & \text{if } \ell_{new} \text{ indicates drift} \\
\text{False} & \text{otherwise}
\end{cases}
$$

Where “semantically novel” means:

- not present in $L_t$  
- not equivalent to any element in $L_t$  
- not a trivial restatement  

Where “resolves ambiguity” means:

- clarifies referent  
- clarifies qualifier  
- clarifies residue  

Where “indicates drift” means:

- referent drift  
- qualifier drift  
- residue drift  

---

# **5. Semantic Novelty Test**

Semantic novelty is tested as:

$$
novel(\ell_{new}, L_t) = 
\begin{cases}
\text{True} & \ell_{new} \notin L_t \\
\text{False} & \ell_{new} \in L_t
\end{cases}
$$

Novelty is required for append, but not sufficient.

---

# **6. Ambiguity Resolution Test**

Ambiguity resolution is tested as:

$$
resolve(\ell_{new}) = 
\begin{cases}
\text{True} & \ell_{new} \text{ reduces ambiguity} \\
\text{False} & \text{otherwise}
\end{cases}
$$

Ambiguity resolution is sufficient for append.

---

# **7. Drift Detection Test**

Drift detection is tested as:

$$
drift(\ell_{new}) = 
\begin{cases}
\text{True} & \ell_{new} \text{ indicates drift} \\
\text{False} & \text{otherwise}
\end{cases}
$$

Drift detection is sufficient for append.

---

# **8. Bounding Rules for Lineage Extensions**

Lineage extensions must be **bounded** to ensure:

- determinism  
- SSR projection  
- replay stability  
- routing stability  

The bound is:

$$
|lineage\_additions| \le k
$$

Where:

- $k$ is a small integer  
- recommended default: $k = 3$  
- $k$ must be explicitly defined in 20.37 when promoted  

### **Bounding Rationale**

Bounding prevents:

- runaway lineage growth  
- nondeterministic lineage explosion  
- unbounded drift  
- routing instability  

### **Bounding Enforcement**

If more than $k$ candidates satisfy the append predicate:

- prioritize referent changes  
- then qualifier changes  
- then residue changes  
- discard the rest deterministically  

This ensures deterministic lineage extension.

---

# **9. Stability Rules for Lineage Extensions**

Lineage extensions must obey stability rules:

### **9.1 Stability Under No Drift**

If no drift is detected:

$$
lineage\_additions = []
$$

### **9.2 Stability Under Identity Continuity**

If identity continuity is stable:

$$
append(\ell_{new}) = False
$$

Unless ambiguity resolution requires it.

### **9.3 Stability Under Freeze Signatures**

If freeze signatures are present:

$$
append(\ell_{new}) = False
$$

Unless freeze signatures explicitly allow extension.

### **9.4 Stability Under Commit Freeze**

If commit freeze is active:

- referent extensions → forbidden  
- qualifier extensions → forbidden  
- residue extensions → allowed only if resolving ambiguity  

---

# **10. Freeze Signature Interaction**

Freeze signatures impose **hard constraints** on lineage extension.

### **10.1 Freeze Signature Dominance**

If freeze signatures conflict with a new lineage element:

$$
append(\ell_{new}) = False
$$

And:

$$
freeze\_conflict = True
$$

### **10.2 Freeze Signature Stability**

If freeze signatures are stable:

- lineage extension is allowed only for ambiguity resolution  
- drift‑based extension is forbidden  

### **10.3 Freeze Signature Conflict**

If freeze signatures conflict:

- lineage extension is forbidden  
- invariant drift receives a −2 penalty  
- routing_fields must set:

```
freeze_conflict = True
identity_drift = True
semantic_drift = True
```

Freeze signature conflict overrides all other signals.

---

# **11. Identity Continuity Interaction**

Identity continuity determines whether lineage extension is allowed.

### **11.1 Identity Stability**

If identity continuity is stable:

$$
append(\ell_{new}) = False
$$

Unless ambiguity resolution requires extension.

### **11.2 Identity Drift**

If identity drift is detected:

$$
append(\ell_{new}) = True
$$

Identity drift is one of the strongest signals for lineage extension.

### **11.3 Identity Conflict**

If identity conflict occurs:

- lineage extension is mandatory  
- invariant drift receives a −2 penalty  
- routing_fields must set:

```
identity_drift = True
```

---

# **12. Residue Topology Interaction**

Residue topology determines whether lineage extension is required.

### **12.1 Stable Topology**

If residue topology is stable:

$$
append(\ell_{new}) = False
$$

### **12.2 Minor Topology Change**

If minor topology change occurs:

$$
append(\ell_{new}) = resolve(\ell_{new})
$$

### **12.3 Topology Instability**

If topology instability occurs:

$$
append(\ell_{new}) = True
$$

### **12.4 Topology Conflict**

If topology conflict occurs:

- lineage extension is mandatory  
- invariant drift receives a −2 penalty  
- routing_fields must set:

```
semantic_drift = True
```

---

# **13. Projection of Lineage Extensions into TR**

Lineage extensions are projected into TR as:

$$
lineage\_additions = [\ell_{new\_1}, \ell_{new\_2}, \ldots]
$$

Where each $\ell_{new\_i}$ satisfies the append predicate.

### **13.1 Projection Rules**

- preserve order  
- preserve boundedness  
- preserve determinism  
- preserve SSR projection  

### **13.2 TR Consumption**

RB uses lineage_additions to detect:

- referent instability  
- qualifier instability  
- identity drift  
- semantic drift  
- freeze signature conflict  

### **13.3 SSR Projection**

Lineage additions must satisfy:

$$
SSR(lineage\_additions) = lineage\_additions
$$

Meaning:

- no ephemeral lineage  
- no nondeterministic lineage  
- no unbounded lineage  

---

# **14. Deterministic Omission Rules**

If any lineage signal is missing:

- semantic lineage  
- referent lineage  
- qualifier lineage  
- residue topology  
- commitments  
- freeze signatures  

Then:

```
lineage_additions = []
```

This ensures:

- determinism  
- SSR projection  
- replay stability  

---

# **15. Closing Summary**

This paper defines the **lineage extension theory** required for TR routing:

- semantic lineage definition  
- referent lineage definition  
- qualifier lineage definition  
- residue lineage definition  
- append predicate  
- novelty test  
- ambiguity resolution test  
- drift detection test  
- bounding rules  
- stability rules  
- identity continuity interaction  
- freeze signature interaction  
- residue topology interaction  
- projection rules  
- SSR rules  
- deterministic omission rules  

Lineage extension is the **identity‑conditioned semantic stability mechanism** that underlies:

- identity drift detection  
- semantic drift detection  
- referent/qualifier instability detection  
- invariant drift computation  
- routing_fields drift signals  

This paper completes the lineage substrate required for deterministic TR routing.

---

Just say **“next”** and I’ll deliver Delivery 2.

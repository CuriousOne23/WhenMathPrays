# **meaning_group_generation_rules.md**  
### *Rules for Constructing Meaning Groups from Lexical Meaning Units*

---

## **1. Purpose**

Meaning groups are the **intermediate semantic clusters** IdOB uses to map:

> **structural geometry → meaning candidates → meaning semantics → stabilized meaning**

This document defines the **rules** for generating meaning groups from lexical meaning units.

Meaning groups must be:

- deterministic  
- replay‑safe  
- stable across TS runs  
- aligned with meaning dimensions  
- aligned with conversational identity  
- aligned with structural geometry  
- aligned with meaning invariants  
- aligned with routing signatures  

This paper is normative.

---

## **2. Inputs to Meaning Group Generation**

Meaning groups are generated from:

### **2.1 Lexical Meaning Units**  
From `idob_meaning_dictionary.yaml`:

- lemma  
- primitive  
- invariant.core_features  
- invariant.tags  
- cue_envelope.feature_cues  
- cue_envelope.tag_cues  
- routing_signature  
- identity_anchor  

### **2.2 Meaning Dimensions**  
From `idob_meaning_dimensions.md`:

- physicality  
- sociality  
- temporality  
- intentionality  
- materiality  
- spatiality  

### **2.3 Structural Geometry**  
From PT1:

- semantic_field_id  
- semantic_role_id  
- semantic_object_id  
- gradient_id  
- universe_id  
- subfield_id  

### **2.4 Conversational Identity Envelope (CIE)**  
From `idob_conv_id_envelope.md`:

- identity_tags  
- identity_vector  
- identity_importance  

Meaning groups must be compatible with CIE modulation.

---

## **3. Meaning Group Definition**

A meaning group is a cluster of meaning units that share:

- primitive  
- invariant tags  
- core features  
- meaning dimensions  
- identity anchors  
- routing signatures  
- cue envelopes  

Meaning groups are **not** arbitrary clusters.  
They must satisfy strict generation rules.

---

## **4. Generation Rules**

Below are the **canonical rules** for constructing meaning groups.

---

## **Rule 1 — Primitive Homogeneity**

All members of a meaning group must share the same **primitive**:

```
ENTITY
ACTION
EVENT
STATE
QUALITY
PROCESS
RELATION
TEMPORAL
SPATIAL
```

This ensures:

- semantic coherence  
- stable meaning dimensions  
- deterministic refinement  

---

## **Rule 2 — Invariant Tag Alignment**

All members must share at least **one invariant tag**.

Examples:

- “dynamic”  
- “physical”  
- “constructed”  
- “temporal”  
- “biological”  

Invariant tags define the **semantic backbone** of the group.

---

## **Rule 3 — Core Feature Similarity**

Members must share **core features** that describe their semantic essence.

Examples:

- walk / stride / step  
- burst / explode / erupt  
- sleepy / lethargic / tired  

Core features must be:

- stable  
- non‑metaphorical  
- meaning‑invariant  

---

## **Rule 4 — Meaning Dimension Cohesion**

Members must have **similar meaning dimension profiles**.

For each dimension:

$$
|d_i - d_j| < \varepsilon_{\text{dim}}
$$

Typical threshold:

$$
\varepsilon_{\text{dim}} = 0.25
$$

This ensures:

- stable meaning_semantics[]  
- stable meaning_delta_h  
- stable refinement cycles  

---

## **Rule 5 — Cue Envelope Compatibility**

Members must share compatible:

- feature_cues  
- tag_cues  

Cue envelopes influence:

- meaning group ranking  
- conversational identity modulation  
- refinement cycles  

Cue envelopes must not conflict.

---

## **Rule 6 — Routing Signature Alignment**

Members must share compatible routing signatures:

- primitive_code  
- feature_codes  
- tag_codes  

Routing signatures ensure:

- deterministic mapping  
- replay‑safe behavior  
- stable struct_to_meaning_map lookup  

---

## **Rule 7 — Identity Anchor Compatibility**

Members must share compatible identity anchors:

- anchor_vector  
- checksum  

Identity anchors support:

- conversational identity modulation  
- identity_delta computation  
- stabilization detection  

Identity anchors must not diverge.

---

## **Rule 8 — Structural Geometry Compatibility**

Meaning groups must be compatible with structural geometry:

- semantic_field_id  
- semantic_role_id  
- semantic_object_id  
- gradient_id  
- universe_id  
- subfield_id  

This ensures:

- correct struct_to_meaning_map lookup  
- correct meaning group ranking  
- correct refinement behavior  

---

## **Rule 9 — Conversational Identity Compatibility**

Meaning groups must be compatible with conversational identity:

- identity_tags  
- identity_vector  
- identity_importance  

Meaning groups that conflict with conversational identity must be excluded.

---

## **Rule 10 — Deterministic Replay**

Meaning groups must be:

- stable across runs  
- deterministic  
- reproducible  
- invariant under replay  

This is enforced by:

- stable primitives  
- stable invariants  
- stable dimensions  
- stable anchors  
- stable routing signatures  

---

## **5. Meaning Group Construction Algorithm**

Below is the canonical algorithm.

### **Step 1 — Partition by Primitive**
Group meaning units by primitive.

### **Step 2 — Cluster by Invariant Tags**
Within each primitive, cluster by invariant tags.

### **Step 3 — Filter by Core Features**
Remove units with incompatible core features.

### **Step 4 — Cluster by Meaning Dimensions**
Cluster units whose dimension vectors are within threshold.

### **Step 5 — Filter by Cue Envelopes**
Remove units with incompatible cue envelopes.

### **Step 6 — Filter by Routing Signatures**
Remove units with incompatible routing signatures.

### **Step 7 — Filter by Identity Anchors**
Remove units with incompatible identity anchors.

### **Step 8 — Validate Structural Geometry Compatibility**
Ensure group is compatible with structural geometry.

### **Step 9 — Validate Conversational Identity Compatibility**
Ensure group is compatible with conversational identity.

### **Step 10 — Freeze Group**
Freeze group into `meaning_groups.yaml`.

---

## **6. Example Group (from your dictionary)**

### **ACTION.physical.motion**

Members:

- walk  
- stride  
- step  

Shared invariants:

- dynamic  
- physical  

Shared dimensions:

- physicality ≈ 0.95  
- spatiality ≈ 0.70  

Shared anchors:

- [2, 3102, 884, 5521]

Shared routing signatures:

- primitive_code = 2  
- feature_codes = [3102, 884, 5521]  

This group satisfies all rules.

---

## **7. Summary**

Meaning groups must be generated using:

- primitive homogeneity  
- invariant tag alignment  
- core feature similarity  
- meaning dimension cohesion  
- cue envelope compatibility  
- routing signature alignment  
- identity anchor compatibility  
- structural geometry compatibility  
- conversational identity compatibility  
- deterministic replay guarantees  

These rules ensure:

- stable meaning resolution  
- stable refinement cycles  
- stable meaning_delta_h  
- stable conversational identity modulation  
- replay‑safe behavior  
- deterministic convergence  

Meaning groups are the backbone of IdOB’s structure→meaning mapping.

---

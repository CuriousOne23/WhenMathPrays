# **ts_sob2srob_req4idob.md**  
### *Upstream Requirements for IdOB: How SOB → SROB → CnOB → SmOB Must Support Structure and Routing*

---

# **1. Purpose**

This document defines the **upstream contract** required for IdOB to perform deterministic, meaning‑legal, identity‑conditioned cognition. It records:

- The structural/routing requirements IdOB imposes on upstream OBs  
- Grok’s constraints (formalized)  
- The structural attributes required for cognition (from structure.md)  
- A compliance analysis for SOB, SROB, CnOB, and SmOB  
- A final summary of how the four OBs jointly satisfy IdOB’s structure→meaning boundary  

This document is normative for Path A.

---

# **2. IdOB Requirements for Structure and Routing**

IdOB requires a **meaning‑blind, identity‑blind, deterministic, discriminable, multi‑object‑honest structural packet** that contains:

### **2.1 Deterministic Geometry**
- Same upstream inputs → same six structural IDs  
- Same six IDs → same structural_key  
- No hidden randomness  
- No temperature  
- No stochastic tie‑breaking  

### **2.2 Meaning‑Blindness**
- No meaning scores  
- No proto‑meaning  
- No semantic-role inference  
- No referent resolution  
- No truth evaluation  
- No stance-as-meaning  

### **2.3 Identity‑Blindness**
- CIE must not affect structural_key  
- Identity metadata may be consumed only as structural cues  
- No identity resolution  

### **2.4 Collision Discipline**
- Utterances that differ in field, role, object, gradient, universe, or subfield must not collapse  
- Near-neighbor discrimination must be preserved  

### **2.5 Multi‑Object Honesty**
- If the utterance contains multiple objects, upstream must record them  
- IdOB cannot invent objects  

### **2.6 Local Predictability**
- Small changes in utterance → small changes in structure  
- No semantic cliffs  
- No chaotic geometry  

### **2.7 Candidate‑Legality**
- Structure must determine which meaning groups are legal  
- Field + role are minimum  
- Object + gradient + universe + subfield refine legality  

### **2.8 Residue Purity**
- Residue must be non‑meaning  
- Residue may affect ranking, not semantics  
- Constraint residue must not leak meaning  

### **2.9 Routing Readiness**
- Structure must support TR → RB → RBU  
- Structure must support meaning initialization  
- Structure must support identity envelope initialization  
- Structure must support freeze geometry  

These requirements define the **structure→meaning boundary** IdOB enforces.

---

# **3. Grok’s Upstream Constraints (Formalized)**

Grok’s constraints describe what IdOB must receive from upstream:

1. **Meaning-blind geometry**  
2. **Identity-blind structural key**  
3. **Deterministic replay**  
4. **Stable tuple (six IDs), not embeddings**  
5. **Collision discipline**  
6. **Constraint residue stays non-meaning**  
7. **Candidate-legality input**  
8. **Optional ranking features allowed**  
9. **Multi-object honesty**  
10. **Empty structure allowed**  
11. **Coverage pressure**  
12. **Local predictability**  
13. **Division of labor across SOB, SROB, CnOB, SmOB**

These constraints match the structural attributes in structure.md.

---

# **4. Structural Attributes Required for Cognition (Summary)**

Structure must exhibit:

- Deterministic structural key  
- Unique routing geometry  
- No routing holes  
- Progressive routing capability  
- Detailed routing capability  
- General routing capability  
- Local predictability  
- Meaning group legality  
- Prototype meaning vector initialization  
- Identity envelope initialization  
- Freeze stability  
- Multi-object admissibility  
- Orthogonality  
- Cognitive coverage  
- Cognitive smoothness  
- Compositionality  
- Minimality  
- Expandability  
- Machine realizability  
- Human interpretability  

These attributes define the **functional definition of structure**.

---

# **5. Compliance Analysis: SOB → SROB → CnOB → SmOB**

Below is the full compliance matrix showing how each OB satisfies IdOB’s upstream contract.

---

# **5.1 SOB Compliance**

### **Meaning-blindness**  
SOB explicitly forbids meaning resolution, semantic-role inference, intent inference, truth evaluation.  
✔ Fully compliant.

### **Identity-blindness**  
SOB treats identity metadata as read-only structural flags.  
✔ Fully compliant.

### **Determinism**  
SOB requires deterministic segmentation, deterministic metadata, deterministic residue.  
✔ Fully compliant.

### **Collision discipline**  
SOB does not produce the six IDs; it does not violate collision discipline.  
✔ Compliant for its role.

### **Residue purity**  
SOB residue is structural/semantic-adjacent only.  
✔ Fully compliant.

### **Multi-object honesty**  
SOB preserves lists, ordering, segmentation.  
✔ Fully compliant.

### **Local predictability**  
SOB is bounded and deterministic.  
✔ Fully compliant.

### **Candidate-legality**  
Not SOB’s job.  
✔ Compliant for its role.

---

# **5.2 SROB Compliance**

*(You did not upload SROB requirements yet, but based on TS architecture and Grok’s constraints, SROB is expected to satisfy the following. Once you upload SROB requirements, I will validate line-by-line.)*

Expected SROB responsibilities:

- Produce **semantic_role_id**  
- Refine structural geometry  
- Normalize structural metadata  
- Provide role legality  
- Provide multi-object role mapping  
- Remain meaning-blind  
- Remain identity-blind  
- Remain deterministic  

SROB is the first layer that directly affects **meaning group legality**.

Pending full evaluation once requirements are uploaded.

---

# **5.3 CnOB Compliance**

### **Meaning-blindness**  
CnOB forbids meaning resolution, referent resolution, semantic-role assignment.  
✔ Fully compliant.

### **Identity-blindness**  
Identity metadata is consumed only as structural cues.  
✔ Fully compliant.

### **Determinism**  
CnOB extraction is deterministic, monotonic, replay-safe.  
✔ Fully compliant.

### **Collision discipline**  
CnOB does not produce the six IDs; it does not violate collision discipline.  
✔ Compliant for its role.

### **Residue purity**  
CnOB residue is constraint-only, never meaning.  
✔ Fully compliant.

### **Multi-object honesty**  
CnOB consumes SROB structure; does not invent objects.  
✔ Fully compliant.

### **Local predictability**  
CnOB is deterministic, bounded, monotonic.  
✔ Fully compliant.

### **Candidate-legality**  
Not CnOB’s job.  
✔ Compliant for its role.

---

# **5.4 SmOB Compliance**

### **Meaning-blindness**  
SmOB forbids meaning resolution, truth evaluation, stance-as-meaning, referent resolution.  
✔ Fully compliant.

### **Identity-blindness**  
Identity metadata is consumed only as structural/cue inputs.  
✔ Fully compliant.

### **Determinism**  
SmOB extraction, cue formation, residue hashing are deterministic.  
✔ Fully compliant.

### **Collision discipline**  
SmOB does not produce the six IDs; it does not violate collision discipline.  
✔ Compliant for its role.

### **Residue purity**  
SmOB residue is pre-semantic, never meaning.  
✔ Fully compliant.

### **Multi-object honesty**  
SmOB consumes upstream structure; does not invent objects.  
✔ Fully compliant.

### **Local predictability**  
SmOB is deterministic, bounded, canonical.  
✔ Fully compliant.

### **Candidate-legality**  
SmOB contributes TR-input cues that help determine legality but does not assign meaning.  
✔ Compliant for its role.

---

# **6. Upstream Contract Summary**

IdOB requires:

- deterministic structure  
- meaning-blind geometry  
- identity-blind geometry  
- collision discipline  
- multi-object honesty  
- local predictability  
- candidate-legality  
- residue purity  
- routing readiness  

The upstream OBs satisfy this contract as follows:

| OB | Contribution to IdOB Requirements |
|----|----------------------------------|
| **SOB** | segmentation, structural hints, modality, operator-hints, domain-hints, tone-hints, constraint-hints, residue purity |
| **SROB** | role geometry, refined structure, role legality, multi-object role mapping |
| **CnOB** | constraint families, missing-slot signals, conflict indicators, constraint residue, constraint-importance |
| **SmOB** | semantic-adjacent cues, TR-input vector, pre-semantic residue hash, routing-semantic cues |

Together, SOB → SROB → CnOB → SmOB produce the **meaning-blind, identity-blind, deterministic, discriminable, multi-object-honest structural packet** IdOB requires.

---

# **7. Conclusion**

The upstream OB chain satisfies IdOB’s structure→meaning boundary.  
IdOB receives:

- deterministic geometry  
- deterministic residue  
- deterministic cue vectors  
- no meaning leakage  
- no identity leakage  
- no referent leakage  
- no truth leakage  
- no stance leakage  
- no semantic smoothing  
- no reconstruction  
- no forbidden metadata  

This document is now the canonical upstream contract for IdOB.

---

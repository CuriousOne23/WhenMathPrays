# **Appendix C — How IdOB Implements Meaning Coupling Internally**  
### *The Internal Mechanics of Meaning = Stated × Context*  
### *Operational, Deterministic, Replay‑Safe Description of IdOB’s Coupling Engine*

---

# **1. Purpose of This Appendix**

Appendix C explains **how IdOB actually performs the coupling**:

$$
\text{Meaning} = \text{Stated} \times \text{Context}
$$

This appendix is not conceptual — it is **mechanical**.  
It describes the **internal steps**, **data flows**, **invariants**, and **refinement rules** IdOB uses to transform:

- **A. What is stated** (propositional content)  
- **B. The context in which it is stated** (contextual structure)

into:

- **C. Meaning** (identity‑conditioned, canonical, replay‑safe)

This is the first appendix that shows **how IdOB actually works inside the machine**.

---

# **2. The IdOB Coupling Engine — Overview**

IdOB is the only primitive in Path‑A that:

- reads both **A** and **B**  
- performs deterministic refinement  
- updates meaning invariants  
- updates identity continuity  
- updates referent continuity  
- updates semantic‑importance  
- updates stance/direction/coherence  
- produces next‑turn context  
- stabilizes meaning before commit

IdOB is the **semantic engine** of TS.

Internally, IdOB performs coupling in **four deterministic phases**:

1. **Ingest stated content (A)**  
2. **Ingest contextual structure (B)**  
3. **Apply refinement rules**  
4. **Produce canonical meaning (C)**

Each phase is described below.

---

# **3. Phase 1 — Ingesting “What Is Stated” (A)**

IdOB receives **A** from CE and upstream structural primitives.

### **A includes:**

- token_surface  
- token_base  
- token_expression  
- token_intent  
- propositional skeleton  
- lexical meaning  
- structural residue  
- semantic‑adjacent residue  
- constraint residue  
- pre‑semantic hash  
- MSL qualifiers  
- MSL clarifications  

### **IdOB’s internal handling of A:**

1. **Normalize lexical meaning**  
   IdOB converts lexical meaning into a canonical propositional skeleton.

2. **Extract semantic candidates**  
   IdOB identifies candidate interpretations based on:
   - negation  
   - emphasis  
   - hedging  
   - correction  
   - agreement  
   - contradiction  
   - uncertainty  

3. **Bind structural residue**  
   IdOB attaches structural residue to the propositional skeleton:
   - subject  
   - verb  
   - object  
   - referent placeholders  
   - adjacency markers  

4. **Prepare A for coupling**  
   IdOB stores A in a deterministic internal structure:

$$
A_t = \\{ \text{proposition},\ \text{expression markers},\ \text{semantic candidates} \\}
$$

This structure is **bounded**, **canonical**, and **replay‑safe**.

---

# **4. Phase 2 — Ingesting “Context” (B)**

IdOB receives **B** from:

- CEx‑CCR  
- CEx‑Pck  
- CE  
- continuity metadata  
- identity metadata  
- semantic‑importance  
- semantic‑residue alignment  
- routing metadata  
- entropy trajectory  
- freeze signatures  
- CIL substrate  

### **B includes:**

- stance  
- direction  
- topic  
- coherence  
- importance  
- identity continuity  
- referent continuity  
- expressive metadata  
- residue metadata  
- CCR alignment  
- semantic‑residue alignment  
- routing regime  
- adjacency class  
- displacement scale  
- regime hint  
- next‑turn context  

### **IdOB’s internal handling of B:**

1. **Context normalization**  
   IdOB converts context into a canonical structure:

$$
B_t = \\{ \text{stance},\ \text{direction},\ \text{continuity},\ \text{identity},\ \text{importance},\ \text{residues},\ \text{routing context} \\}
$$

2. **Context weighting**  
   IdOB assigns deterministic weights to:
   - identity signals  
   - referent signals  
   - semantic‑importance roles  
   - residue alignment scores  
   - stance/direction cues  

3. **Context binding**  
   IdOB binds context to the propositional skeleton:
   - referent resolution  
   - identity resolution  
   - stance resolution  
   - direction resolution  
   - coherence resolution  

4. **Prepare B for coupling**  
   IdOB stores B in a deterministic internal structure:

$$
B_t = \\{ \text{context invariants},\ \text{identity invariants},\ \text{continuity invariants} \\}
$$

---

# **5. Phase 3 — Applying IdOB’s Refinement Rules**

This is the core of IdOB.

IdOB applies **deterministic refinement rules** that combine A and B.

### **5.1 Rule Class 1 — Identity‑Conditioned Refinement**

IdOB updates:

- identity continuity  
- referent continuity  
- identity geometry  
- identity roles  
- identity stability  

Example:

If A = “I didn’t say that”  
and B indicates identity threat,  
IdOB refines meaning into a **defensive identity correction**.

---

### **5.2 Rule Class 2 — Semantic‑Importance Refinement**

IdOB updates:

- importance scores  
- semantic roles  
- semantic residues  
- alignment scores  

Example:

If A = “Sure, let’s do it”  
and B indicates high importance,  
IdOB refines meaning into **agreement on a high‑stakes decision**.

---

### **5.3 Rule Class 3 — Stance/Direction/Coherence Refinement**

IdOB updates:

- stance  
- direction  
- coherence  
- qualifiers  
- clarifications  

Example:

If A = “That’s not what I meant”  
and B indicates theoretical context,  
IdOB refines meaning into **semantic correction**.

If B indicates emotional context,  
IdOB refines meaning into **identity defense**.

---

### **5.4 Rule Class 4 — Residue Interpretation**

IdOB interprets:

- structural residue  
- semantic‑adjacent residue  
- constraint residue  
- CCR residue alignment  

Example:

If residue indicates contradiction,  
IdOB refines meaning into **correction**.

If residue indicates planning,  
IdOB refines meaning into **forward motion**.

---

### **5.5 Rule Class 5 — Continuity Refinement**

IdOB updates:

- topic continuity  
- referent continuity  
- identity continuity  
- next‑turn context  

Example:

If A introduces a new referent,  
IdOB updates continuity metadata.

If B indicates topic drift,  
IdOB stabilizes topic.

---

# **6. Phase 4 — Producing Canonical Meaning (C)**

After applying refinement rules, IdOB produces:

$$
C_t = \text{canonical meaning state}
$$

### **C includes:**

- refined stance  
- refined direction  
- refined coherence  
- refined qualifiers  
- refined clarifications  
- refined semantic‑importance  
- refined identity continuity  
- refined referent continuity  
- refined next‑turn context  
- refined identity geometry  
- refined residue interpretation  

This meaning state is:

- **bounded**  
- **canonical**  
- **deterministic**  
- **replay‑safe**  
- **identity‑conditioned**  
- **context‑conditioned**  
- **ready for commit**  

IdOB cycles until meaning is stable enough for OuBA.

---

# **7. Worked Internal Example**

### **Utterance:**  
“I didn’t say that.”

### **A. What is stated**  
Literal denial.

### **B. Context**  
Identity threat + contradiction residue + high importance.

### **IdOB internal steps:**

1. Bind “that” to prior referent.  
2. Detect identity threat.  
3. Detect contradiction residue.  
4. Update stance → defensive.  
5. Update direction → backward motion.  
6. Update coherence → correction.  
7. Update semantic‑importance → high.  
8. Update identity continuity → protect self‑image.  
9. Produce next‑turn context → justification expected.

### **C. Meaning produced**  
> “I am defending my identity and correcting a harmful misattribution.”

This is IdOB’s internal coupling engine in action.

---

# **8. Summary**

Appendix C shows:

- how IdOB ingests stated content  
- how IdOB ingests context  
- how IdOB applies deterministic refinement rules  
- how IdOB produces canonical meaning  
- how IdOB stabilizes identity continuity  
- how IdOB interprets residues  
- how IdOB maintains referent continuity  
- how IdOB produces next‑turn context  
- how IdOB ensures replay determinism

This appendix reveals the **internal mechanics** of IdOB’s coupling engine — the core of TS’s meaning architecture.

---

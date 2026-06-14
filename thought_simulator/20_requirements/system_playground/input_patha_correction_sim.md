# **Path‑A Correction Simulation Playground**  
*(Input‑Side Only: InB → IIInB → CEx → CE → ISc → TPU)*

This document defines and simulates the **10 canonical mistake cases** used to stress‑test the **Path‑A‑only** pipeline. These cases expose the exact weaknesses Path A must handle without invoking:

- OB  
- RB  
- TR  
- DCB  
- TB  
- Path B  

All simulations follow the strict input‑side sequence:

$$
\text{InB} \rightarrow \text{IIInB} \rightarrow \text{CEx} \rightarrow \text{CE} \rightarrow \text{ISc} \rightarrow \text{TPU}
$$

The goal is to verify that Path A can still produce:

- A coherent $TP(N+1)$  
- A stable `$semantic\_core$`  
- No hallucination  
- No grammar repair  
- Ambiguity preservation  
- Stable $ \Delta H\% $  
- A valid TPU commit  

---

# **Methodology**  
*(New Section — Option B)*

Path A is responsible for **input‑side structural interpretation only**. It does *not* repair grammar, resolve ambiguity, or infer missing content. Instead, it extracts **proto‑events** and **minimal propositions** from imperfect input.

### **Basins**

**1. InB — Input Basin**  
Tokenization, order, POS‑guessing, and minimal surface structure.

**2. IIInB — Intermediate Inference Basin**  
Detection of:  
- Missing subjects  
- Missing connectors  
- Ambiguous roles  
- Multi‑clause fusion  
- Tense/aspect drift  
- Negation scope uncertainty  

**3. CEx — Candidate Extraction**  
Generation of one or more proto‑propositions.  
No resolution of ambiguity — only enumeration.

**4. CE — Candidate Evaluation**  
Structural plausibility scoring, warnings, and ambiguity tagging.

**5. ISc — Information Score**  
Computation of $ \Delta H\% $ and confidence.  
No semantic enrichment.

**6. TPU — Thought Preservation Unit**  
Commit of the minimal, ambiguity‑preserving $TP(N+1)$ snapshot.

---

# **The 10 Canonical Mistake Cases**  
*(Grounded in your file:   [Current page](citation-section://1146962836/3))*

These cases cover the full spectrum of input‑side failure modes Path A must handle:

- Missing structure  
- Wrong order  
- Ambiguous roles  
- Broken grammar  
- Missing connectors  
- Tense drift  
- Negation drift  
- Emotional noise  
- Fragmentary input  
- Multi‑clause collapse  

Each case includes:

- Input  
- Why it is a good test  
- Full simulation through TPU  
- PASS/FAIL assessment  

---

# **Case 1 — Missing Words (Ellipsis)**  
*(Content from   [Current page](citation-section://1146962836/4))*

**Input:**  
`Went store forgot wallet.`

**Why it’s a good test:**  
Missing subject, missing prepositions, smashed clauses.

### Simulation  
**InB:**  
Tokens: `[Went, store, forgot, wallet]`  
Two verb events detected.

**IIInB:**  
Missing subject, missing connectors.

**CEx:**  
- Event 1: head=`went`, args={agent:?, destination:store}  
- Event 2: head=`forgot`, args={agent:?, object:wallet}

**CE:**  
Both structurally plausible.

**ISc:**  
$ \Delta H\% $ small positive; confidence ≈ 0.55.

**TPU:**  
Commits two proto‑events with missing‑role flags.

**Assessment:** **PASS**

---

# **Case 2 — Wrong Order (Scrambled Tokens)**  
*(Content from   [Current page](citation-section://1146962836/40))*

**Input:**  
`The mouse the cat chased.`

**Why it’s a good test:**  
Ambiguous subject/object roles.

### Simulation  
**InB:**  
Tokens: `[The, mouse, the, cat, chased]`

**IIInB:**  
Ambiguous NP–NP–V structure.

**CEx:**  
head=`chased`, args={agent:cat?, object:mouse?}

**CE:**  
Ambiguity preserved.

**ISc:**  
Neutral $ \Delta H\% $; confidence ≈ 0.48.

**TPU:**  
Commits ambiguous proposition.

**Assessment:** **PASS**

---

# **Case 3 — Missing Preposition / Article**  
*(Content from   [Current page](citation-section://1146962836/43))*

**Input:**  
`I go store yesterday.`

### Simulation  
**CEx:**  
head=`go`, args={agent:I, destination:store, time:yesterday}

**CE:**  
Flags tense mismatch + missing preposition.

**ISc:**  
Small positive $ \Delta H\% $; confidence ≈ 0.63.

**TPU:**  
Commits single proposition with warnings.

**Assessment:** **PASS**

---

# **Case 4 — Ambiguous Pronoun**  
*(Content from   [Current page](citation-section://1146962836/45))*

**Input:**  
`John told Mark he was wrong.`

### Simulation  
Two plausible bindings:

- `$he = John$`  
- `$he = Mark$`

**TPU:**  
Commits both in parallel.

**Assessment:** **PASS**

---

# **Case 5 — Negation Drift**  
*(Content from   [Current page](citation-section://1146962836/47))*

**Input:**  
`I didn’t say you stole the money.`

### Simulation  
Three plausible scopes:

1. Negation applies to “say”  
2. Negation applies to “you stole”  
3. Negation applies to entire proposition

**TPU:**  
Commits multi‑trace semantic core.

**Assessment:** **PASS**

---

# **Case 6 — Emotional Noise**  
*(Content from   [Current page](citation-section://1146962836/49))*

**Input:**  
`Ugh this stupid thing never works.`

### Simulation  
Affective layer separated from factual core.

**TPU:**  
Commits proposition + affect layer.

**Assessment:** **PASS**

---

# **Case 7 — Fragmentary Input**  
*(Content from   [Current page](citation-section://1146962836/51))*

**Input:**  
`Because tired.`

### Simulation  
Minimal state proposition extracted.

**Assessment:** **PASS**

---

# **Case 8 — Run‑On Without Connectors**  
*(Content from   [Current page](citation-section://1146962836/54))*

**Input:**  
`I was late the car broke.`

### Simulation  
Two independent events extracted.

**Assessment:** **PASS**

---

# **Case 9 — Mixed Tense / Aspect Drift**  
*(Content from   [Current page](citation-section://1146962836/56))*

**Input:**  
`He go yesterday but is going now.`

### Simulation  
Two temporal frames preserved.

**Assessment:** **PASS**

---

# **Case 10 — Implicit Subject**  
*(Content from   [Current page](citation-section://1146962836/58))*

**Input:**  
`Fixing the car now.`

### Simulation  
Proto‑event with missing agent.

**Assessment:** **PASS**

---

# **Summary of All 10 Cases**  
*(Content from   [Current page](citation-section://1146962836/59))*

All 10 inputs produced:

- Coherent $TP(N+1)$  
- Stable `$semantic\_core$`  
- No hallucination  
- No grammar repair  
- Ambiguity preserved  
- Stable $ \Delta H\% $  
- Successful TPU commit  

Path A passed all stress tests.

---

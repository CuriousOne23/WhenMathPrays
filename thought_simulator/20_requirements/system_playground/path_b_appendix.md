# 📘 **Appendix A — Path B Operational Examples**  
### *Each example begins with MB‑observable Path A output and shows how Path B resolves it.*

---

# **A.1 Primitive Examples**

---

## **A.1.1 — REx‑prm Example (Expression Extractor)**

### **Input (Path A output)**  
TP contains structured meaning:

- intent: *“Explain Bayesian updating”*  
- audience: *non‑technical*  
- tone: *gentle*  
- constraints: *avoid equations*  
- semantic_core: stable  

### **Operation**  
REx extracts only the expression‑relevant slice:

- intent → *explain simply*  
- tone → *gentle*  
- constraint → *no equations*  
- audience → *non‑technical*  

### **Output (to RPlan‑prm)**  
RP‑ref (expression slice):

```
{
  intent: "simple explanation",
  tone: "gentle",
  constraint: "no equations",
  audience: "non-technical"
}
```

---

## **A.1.2 — RPlan‑prm Example (Realization Planner)**

### **Input (from REx‑prm)**  
Expression slice:

```
intent: "simple explanation"
tone: "gentle"
constraint: "no equations"
audience: "non-technical"
```

### **Operation**  
RPlan generates candidate plans:

- **Plan A:** 3‑sentence analogy  
- **Plan B:** bullet‑point explanation  
- **Plan C:** short story‑based explanation  

### **Output (to RPU‑prm)**  
RPlan‑ref containing all candidate plans.

---

## **A.1.3 — RPU‑prm Example (Realization Plan Updater)**

### **Input (from RPlan‑prm)**  
Candidate plans A, B, C.

### **Operation**  
Governance flags:

- user prefers analogies  
- tone must remain gentle  
- avoid technical terms  

RPU:

- selects Plan A  
- softens transitions  
- removes jargon  
- enforces tone constraints  

### **Output (to ReB‑prm)**  
Final RPlan‑ref:

```
Plan A (final):
  - 3-sentence analogy
  - gentle tone
  - no jargon
  - no equations
```

---

## **A.1.4 — ReB‑prm Example (Realization Basin)**

### **Input (from RPU‑prm)**  
Final plan: 3‑sentence gentle analogy.

### **Operation**  
ReB stabilizes:

- pacing  
- tone consistency  
- sentence flow  
- channel formatting  

### **Output (external)**  
A coherent, gentle, 3‑sentence analogy explaining Bayesian updating.

---

# **A.2 Process Examples**

---

## **A.2.1 — RPlan‑prc Example**

### **Input**  
Expression slice: “formal tone, long answer allowed.”

### **Operation**  
RPlan‑prc generates:

- structured essay  
- step‑by‑step explanation  
- definition‑first plan  

### **Output**  
Candidate plans passed to RPlan‑prm.

---

## **A.2.2 — RSelect‑prc Example**

### **Input**  
Two candidate plans:

- **Plan A:** neutral tone, long pacing  
- **Plan B:** warm tone, short pacing  

### **Operation**  
User emotional state = “anxious.”  
Warm tone preferred.

RSelect‑prc chooses **Plan B**.

### **Output**  
Selected plan → RPU‑prm.

---

## **A.2.3 — RStyle‑prc Example**

### **Input**  
Plan: neutral tone, medium warmth.

### **Operation**  
User preference: “encouraging tone.”

RStyle‑prc adjusts:

- tone: neutral → warm  
- warmth: medium → high  

### **Output**  
Updated plan → RPlan‑prm.

---

## **A.2.4 — RTiming‑prc Example**

### **Input**  
Plan: long paragraph.

### **Operation**  
RTiming‑prc detects pacing mismatch.

Transforms:

- long paragraph → 3 short paragraphs  
- adds natural pauses  

### **Output**  
Updated pacing → RPlan‑prm.

---

## **A.2.5 — RChannel‑prc Example**

### **Input**  
Plan includes visual metaphors.

### **Operation**  
Channel = text‑only.

RChannel‑prc removes:

- references to diagrams  
- visual metaphors  

### **Output**  
Text‑appropriate plan → RPlan‑prm.

---

# **A.3 Reference Object Examples**

---

## **A.3.1 — RP‑ref Example**

### **Input**  
Candidate plan selected.

### **Operation**  
RP‑ref stores:

```
structure: bullets
tone: warm
length: short
channel: text
```

### **Output**  
Passed to RPU‑prm.

---

## **A.3.2 — RPlan‑ref Example**

### **Input**  
RPlan‑prm output.

### **Operation**  
RPlan‑ref holds:

- structure  
- tone  
- pacing  
- channel  
- constraints  

### **Output**  
Used by RPU‑prm to finalize behavior.

---

## **A.3.3 — RStyle‑ref Example**

### **Input**  
Style metadata.

### **Operation**  
RStyle‑ref contains:

```
tone: "gentle"
warmth: 0.7
formality: low
```

### **Output**  
Used by RPU‑prm.

---

## **A.3.4 — RTiming‑ref Example**

### **Input**  
Pacing metadata.

### **Operation**  
RTiming‑ref contains:

```
sentence_length: short
pause_density: low
```

### **Output**  
Used by RPU‑prm.

---

## **A.3.5 — RChannel‑ref Example**

### **Input**  
Channel metadata.

### **Operation**  
RChannel‑ref contains:

```
channel: "text"
multimodal: false
```

### **Output**  
Used by RPU‑prm.

---

# **A.4 TS‑Concept Examples**

---

## **A.4.1 — BC‑tsc Example (Behavioral Coherence)**

### **Input**  
Plan uses humor.

### **Operation**  
Internal state: user is grieving.  
BC‑tsc rejects humor.

### **Output**  
RPU‑prm must choose a different plan.

---

## **A.4.2 — SC‑tsc Example (Style Coherence)**

### **Input**  
Plan tone = neutral.

### **Operation**  
Conversation history tone = warm.  
SC‑tsc adjusts tone to match.

### **Output**  
Style‑coherent plan.

---

## **A.4.3 — TC‑tsc Example (Timing Coherence)**

### **Input**  
Plan pacing = abrupt.

### **Operation**  
TC‑tsc smooths pacing:

- adds transitions  
- shortens sentences  

### **Output**  
Timing‑coherent plan.

---

## **A.4.4 — CC‑tsc Example (Channel Coherence)**

### **Input**  
Plan includes visual references.

### **Operation**  
Channel = text‑only.  
CC‑tsc removes visual elements.

### **Output**  
Channel‑coherent plan.

---

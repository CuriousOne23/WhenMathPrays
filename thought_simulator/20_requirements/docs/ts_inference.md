# **ts_inference.md**  
### *What TS Inference Is, and the Algorithm That Makes It Possible*

TS Inference is the core semantic operation of the Thought Simulator.  
It is the mechanism that takes a partially‑specified meaning and produces a **valid**, **complete**, **non‑contradictory**, and **envelope‑compatible** meaning — or escalates if no such meaning exists.

TS Inference is not a neural forward pass, not a statistical guess, and not a generative process.  
It is a **deterministic, structural algorithm** composed of two stages:

1. **Detection** — identify what is wrong or incomplete.  
2. **Projection** — compute the nearest valid meaning that satisfies all constraints.

Everything else in TS depends on this.

---

# **1. What TS Inference Is**

TS Inference is a **semantic correction and completion algorithm**.

Given:

- a prior meaning state $M_0$  
- a candidate meaning $M_c$  
- explicit structure (fields, referents, envelopes, MI tags)  
- explicit constraints (types, envelopes, routing rules)  

TS Inference returns:

- a corrected meaning $M'$, or  
- an escalation (ask the user, clarify, or reject)

TS Inference does **not**:

- guess  
- hallucinate  
- invent new meaning  
- smooth contradictions  
- rely on embeddings  
- rely on neural weights  

It operates entirely on **explicit structure**.

---

# **2. Detection**  
### *Identify what is wrong or incomplete*

Detection is a structural analysis of the candidate meaning $M_c$.  
It identifies issues that must be resolved before meaning can be committed.

Detection finds:

### **2.1 Missing structure**
- missing referents  
- missing operators  
- incomplete shorthand  
- unresolved pronouns  
- missing constraints  

### **2.2 Contradictions**
- incompatible modifiers  
- mutually exclusive MI tags  
- conflicting envelope fields  

### **2.3 Vagueness**
- $MI\_VAGUE$  
- $MI\_AFFECT$  
- ambiguous referents  
- ambiguous scope  

### **2.4 Unsafe merges**
- cross‑envelope writes  
- illegal overwrites  
- type violations  

### **2.5 $ΔH\%$ anomalies**
- meaning changed too much too fast  
- meaning changed in a structurally suspicious way  

Detection outputs a set of issues:

$ I = \{ i\_1, i\_2, ..., i\_k \} $

Each issue includes:

- its location in the structure  
- its type  
- a small set of **local repair options**  

Detection does **not** fix anything.  
It only identifies problems and possible local repairs.

---

# **3. Projection**  
### *Compute the nearest valid meaning*

Projection is the **actual inference**.

Given:

- the prior meaning $M_0$  
- the candidate meaning $M_c$  
- the detected issues $I$  
- the envelope constraints  
- the MI tags  
- the USP rules  

Projection computes:

> **the nearest valid meaning $M'$ that satisfies all constraints.**

This is not neural.  
This is not statistical.  
This is not generative.

Projection is a **tiny discrete optimization problem** over a **small, typed structure**.

---

# **4. The TS Projection Algorithm**

## **Input**
- $M_0$: prior meaning  
- $M_c$: candidate meaning  
- $I = \{ i\_1, ..., i\_k \}$: detected issues  
- envelope constraints  
- USP rules  
- MI tags  

## **Output**
- $M'$: nearest valid meaning  
- OR escalation  

---

## **Step 1 — Generate local repair options**

For each issue $i\_j$, generate a **small set** of possible local fixes.

Examples:

- unresolved pronoun → bind to referent A or B  
- incomplete shorthand → expand via USP rule  
- contradictory modifier → drop one or mark explicit contradiction  
- missing referent → attach to nearest envelope object  

Each issue yields **2–4** options.

This is the key to boundedness.

---

## **Step 2 — Enumerate candidate completions**

Combine the local fixes into candidate completions.

If each issue has 2–4 options and there are 2–3 issues, the total combinations are tiny:

- 2 issues × 3 options → 9 candidates  
- 3 issues × 2 options → 8 candidates  

TS **never** allows unbounded ambiguity.  
If ambiguity grows → escalate.

---

## **Step 3 — Apply fixes to produce candidate meanings**

For each combination:

- apply the local fixes to $M_c$  
- produce a candidate meaning $M'\_k$  

Each $M'\_k$ is a fully‑specified meaning structure.

---

## **Step 4 — Validate constraints**

For each $M'\_k$:

- check envelope compatibility  
- check type constraints  
- check routing rules  
- check merge safety  
- check MI tag resolution  
- check no contradictions remain  

If any constraint fails → discard $M'\_k$.

---

## **Step 5 — Compute cost**

For each valid $M'\_k$:

<blank line>
$$
\text{Cost}(M'\_k) = \text{EditCost} + \text{MIResolutionCost} + \Delta H\%
$$
<blank line>

Where:

- **EditCost** = number of structural edits  
- **MIResolutionCost** = penalty for resolving ambiguity  
- **$ΔH\%$** = semantic distance from $M_0$  

This is deterministic.

---

## **Step 6 — Choose the minimum‑cost meaning**

Let:

<blank line>
$$
M' = \arg\min\_{k} \text{Cost}(M'\_k)
$$
<blank line>

This is the **nearest valid meaning**.

---

## **Step 7 — If no valid meaning exists → escalate**

If all candidates fail constraints:

- escalate to IB (ask user)  
- escalate to clarification  
- or reject (rare structural case)  

TS never guesses.

---

# **5. Why TS Inference Is Cheap**

TS inference is cheap because:

### **5.1 Meaning is small and typed**
The structure is bounded and explicit.

### **5.2 Ambiguity is bounded**
TS escalates early rather than letting ambiguity explode.

### **5.3 Locality**
Projection only operates around the detected issues.

### **5.4 Deterministic cost model**
No search over embeddings.  
No neural inference.

### **5.5 CPU‑native operations**
Just:

- small diffs  
- small combinations  
- small constraint checks  
- small cost computations  

This is why TS inference is viable.

---

# **6. Why TS Inference Is Effective**

TS inference is effective because:

- it resolves ambiguity deterministically  
- it respects user intent  
- it respects prior meaning  
- it respects envelope constraints  
- it never hallucinates  
- it never guesses  
- it never drifts  
- it always escalates when needed  

Projection is not “figuring out meaning.”  
Projection is:

> **choosing the nearest valid meaning from a tiny, structured, constrained space.**

---

# **7. Appendix (to be added later)**  
A full worked example will be added once the main text is finalized.

---

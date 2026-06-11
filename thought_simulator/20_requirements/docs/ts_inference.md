# **ts_inference.md**  
### *What TS Inference Is, When It Runs, and the Algorithm That Makes It Possible*

TS Inference is the core semantic correctness mechanism of the Thought Simulator.  
It takes a partially‑specified meaning and produces a **valid**, **complete**, **non‑contradictory**, and **envelope‑compatible** meaning — or escalates if no such meaning exists.

TS Inference is **not** a neural forward pass, not a statistical guess, and not a generative process.  
It is a **deterministic, structural algorithm** composed of two stages:

1. **Detection** — identify what is wrong or incomplete.  
2. **Projection** — compute the nearest valid meaning that satisfies all constraints.

Everything else in TS depends on this.

---

# **1. What TS Inference Is**

TS Inference is a **semantic correction and completion algorithm**.

Given:

- a prior meaning state $M\_0$  
- a candidate meaning $M\_c$  
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

# **2. When TS Inference Is Used (Modes of Operation)**

TS Inference is **not** a general reasoning engine.  
It is a **semantic correctness engine** that runs only in specific, bounded contexts.  
Its purpose is to ensure that meaning is structurally valid, complete, and safe before commit.

TS Inference operates in **three and only three modes**.

---

## **2.1 Mode 1 — Input Error Correction (Primary Mode)**

TS Inference runs when the user’s input produces a candidate meaning $M\_c$ that contains:

- missing referents  
- incomplete shorthand  
- unresolved pronouns  
- contradictory modifiers  
- ambiguous scope  
- $MI\_VAGUE$ or $MI\_AFFECT$  
- envelope violations  
- unsafe merges  
- suspicious $ΔH\%$ changes  

In this mode, TS Inference:

1. Detects issues in $M\_c$  
2. Generates local repair options  
3. Projects to the nearest valid meaning $M'$  
4. Escalates if no valid meaning exists  

This is the **primary purpose** of TS Inference.

---

## **2.2 Mode 2 — Meaning Commit Validation (Commit Gate)**

TS Inference also runs whenever TS is about to **commit** a meaning into the envelope.

This includes:

- merging a new meaning into the current state  
- overwriting a field  
- resolving a pronoun  
- applying shorthand expansions  
- updating referents  
- attaching new structure  

Before commit, TS Inference checks:

- structural validity  
- envelope compatibility  
- type correctness  
- MI tag resolution  
- absence of contradictions  
- acceptable $ΔH\%$  

If any check fails → escalate.

TS Inference in this mode is a **gatekeeper**, not a generator.

---

## **2.3 Mode 3 — Path B Branch Validation (NOT Path B Reasoning)**

Path B does **not** use TS Inference to think, generate, or explore.

Path B produces its own candidate meanings.  
TS Inference is used only to **validate** those meanings before they are:

- stored  
- compared  
- replayed  
- merged  
- surfaced  

TS Inference checks:

- structural correctness  
- envelope compatibility  
- contradiction‑free structure  
- safe merges  
- acceptable $ΔH\%$  

Path B does the reasoning.  
TS Inference ensures the results are **valid**.

---

## **2.4 When TS Inference Is *Not* Used**

TS Inference is **never** used for:

- generation  
- reasoning  
- planning  
- simulation  
- semantic expansion  
- Path A processing  
- Path B exploration  
- constructing meaning  
- interpreting meaning  
- producing alternatives  
- smoothing contradictions  
- guessing user intent  

TS Inference is **not** a semantic engine.  
It is a **semantic correctness engine**.

It ensures that meaning is:

- valid  
- complete  
- safe  
- bounded  
- deterministic  

before TS commits it.

---

# **3. Detection**  
### *Identify what is wrong or incomplete*

Detection is a structural analysis of the candidate meaning $M\_c$.  
It identifies issues that must be resolved before meaning can be committed.

Detection finds:

### **3.1 Missing structure**
- missing referents  
- missing operators  
- incomplete shorthand  
- unresolved pronouns  
- missing constraints  

### **3.2 Contradictions**
- incompatible modifiers  
- mutually exclusive MI tags  
- conflicting envelope fields  

### **3.3 Vagueness**
- $MI\_VAGUE$  
- $MI\_AFFECT$  
- ambiguous referents  
- ambiguous scope  

### **3.4 Unsafe merges**
- cross‑envelope writes  
- illegal overwrites  
- type violations  

### **3.5 $ΔH\%$ anomalies**
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

# **4. Projection**  
### *Compute the nearest valid meaning*

Projection is the **actual inference**.

Given:

- the prior meaning $M\_0$  
- the candidate meaning $M\_c$  
- the detected issues $I$  
- the envelope constraints  
- the MI tags  
- the USP rules  

Projection computes:

> **the nearest valid meaning $M'$ that satisfies all constraints.**

Projection is a **tiny discrete optimization problem** over a **small, typed structure**.

---

# **5. The TS Projection Algorithm**

## **Input**
- $M\_0$: prior meaning  
- $M\_c$: candidate meaning  
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

- apply the local fixes to $M\_c$  
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

  
$$
\text{Cost}(M'\_k) = \text{EditCost} + \text{MIResolutionCost} + \Delta H\%
$$
  

Where:

- **EditCost** = number of structural edits  
- **MIResolutionCost** = penalty for resolving ambiguity  
- **$ΔH\%$** = semantic distance from $M\_0$  

This is deterministic.

---

## **Step 6 — Choose the minimum‑cost meaning**

  
$$
M' = \arg\min\_{k} \text{Cost}(M'\_k)
$$
  

This is the **nearest valid meaning**.

---

## **Step 7 — If no valid meaning exists → escalate**

If all candidates fail constraints:

- escalate to IB (ask user)  
- escalate to clarification  
- or reject (rare structural case)  

TS never guesses.

---

# **6. Why TS Inference Is Cheap**

TS inference is cheap because:

### **6.1 Meaning is small and typed**
The structure is bounded and explicit.

### **6.2 Ambiguity is bounded**
TS escalates early rather than letting ambiguity explode.

### **6.3 Locality**
Projection only operates around the detected issues.

### **6.4 Deterministic cost model**
No search over embeddings.  
No neural inference.

### **6.5 CPU‑native operations**
Just:

- small diffs  
- small combinations  
- small constraint checks  
- small cost computations  

---

# **7. Why TS Inference Is Effective**

TS inference is effective because:

- it resolves ambiguity deterministically  
- it respects user intent  
- it respects prior meaning  
- it respects envelope constraints  
- it never hallucinates  
- it never guesses  
- it never drifts  
- it always escalates when needed  

Projection is:

> **choosing the nearest valid meaning from a tiny, structured, constrained space.**

---

# **Appendix A — Worked Example (to be added)**

A full example will be added once the main text stabilizes.

---

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

Detection is a structural analysis of the candidate meaning $M_c$.  
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

$$
I = \{ i_1, i_2, ..., i_k \}
$$

Each issue includes:

- its location in the structure  
- its type  
- a small set of **local repair options**  

Detection does **not** fix anything.  
It only identifies problems and possible local repairs.

Detection is implemented by the **IIInB** and SHALL be limited to **local semantic defect identification only**.  
The “local repair options” attached to each issue are **descriptive suggestions** for how the structure *could* be repaired; they are not applied by IIInB.  
The IIInB SHALL NOT perform projection, correction, referent resolution, or any modification of $M_0$ or $M_c$.  
All semantic projection and correction, including “minimal” corrections, SHALL be performed outside IIInB (see Section 4, Projection).

---

# **4. Projection**  
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

Projection is a **tiny discrete optimization problem** over a **small, typed structure**.

Projection is implemented by the **ISc**.  
The ISc SHALL:

- compare $M_0$ and $M_c$ against the envelope and constraints  
- use the detected issues $I$ and their local repair options to generate and evaluate candidate repairs  
- compute the nearest valid meaning $M'$ and its projection cost  
- propose $M'$ as a corrected meaning to the IB  

If a defect corresponds to an underspecified referent and the envelope yields **exactly one unambiguous candidate**, the ISc SHALL propose that referent as the correction as part of $M'$.  

The ISc SHALL compute **all** semantic corrections, including minimal corrections and referent resolutions, subject to envelope and USP constraints.  
The ISc SHALL NOT unilaterally apply corrections; the IB SHALL decide whether to accept or reject the proposed $M'$.

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

# 7 How TS Inference Works, and How It Compares to Today’s AI

TS Inference is a **semantic correctness engine**, not a reasoning engine, not a generative model, and not a statistical predictor.  
Its purpose is to ensure that every meaning entering the TS pipeline is:

- structurally valid  
- envelope‑compatible  
- unambiguous  
- contradiction‑free  
- safe to merge  
- minimally corrected  

TS Inference does this through a **deterministic projection algorithm** that computes the **nearest valid meaning** under a rule‑bound cost metric.  
This is fundamentally different from how modern AI systems (LLMs, transformers, diffusion models) operate.

---

## 7.1 How TS Inference Works (Conceptual Overview)

TS Inference takes three inputs:

- **M₀** — the prior meaning  
- **$M_c$** — the candidate meaning  
- **I** — the set of detected issues  

It then performs a **bounded, deterministic search** over a small set of explicit structural repairs:

1. **Generate local repair options** for each issue  
2. **Enumerate candidate meanings** by combining repairs  
3. **Apply repairs** to produce complete meanings  
4. **Validate constraints** (types, envelopes, routing, contradictions)  
5. **Compute cost** for each valid meaning  
6. **Select the minimum‑cost meaning**  
7. **Escalate** if no valid meaning exists  

This is a **projection**, not a prediction.  
TS does not guess, infer intent, or use probability.  
It computes the meaning that requires the **least distortion** to become valid.

---

## 7.2 Why TS Inference Works (The Core Principles)

TS Inference is effective because it is built on four principles:

### **A. Determinism**  
The same input always produces the same output.  
There is no sampling, no randomness, no temperature.

### **B. Boundedness**  
TS never explores an unbounded search space.  
All repairs are explicit, finite, and structural.

### **C. Transparency**  
Every repair, cost, and constraint is logged.  
Every projection is explainable and replayable.

### **D. Non‑Generativity**  
TS never invents meaning.  
It only corrects explicit structural defects.

These principles make TS Inference safe, predictable, and trustworthy.

---

## 7.3 Advantages Over Today’s AI

### **A. No Hallucinations**  
TS cannot invent facts or meaning.  
Modern AI frequently does.

### **B. No Guessing or Over‑Interpretation**  
TS escalates when ambiguity exists.  
LLMs often “pick one” and confidently assert it.

### **C. Deterministic Behavior**  
TS is replay‑safe.  
LLMs are inherently stochastic.

### **D. Transparent Decision‑Making**  
TS can explain exactly why it chose a meaning.  
LLMs cannot.

### **E. Envelope‑Constrained Safety**  
TS cannot violate type constraints, routing rules, or semantic envelopes.  
LLMs routinely do.

### **F. Minimal Correction, Not Rewriting**  
TS preserves user meaning with minimal edits.  
LLMs often rewrite or reinterpret.

### **G. No Model Drift**  
TS behavior is stable over time.  
LLMs drift as context grows or as models update.

### **H. No Training Cost**  
TS Inference does not require GPUs, embeddings, or neural training.  
LLMs require massive compute and retraining cycles.

---

## 7.4. Disadvantages Compared to Today’s AI

### **A. TS Inference is Not a Reasoning Engine**  
It cannot:

- generate ideas  
- plan  
- simulate  
- expand meaning  
- perform multi‑step reasoning  

LLMs can.

### **B. TS Inference Cannot Resolve Deep Ambiguity**  
If meaning is unclear, TS escalates.  
LLMs will “take a guess.”

### **C. TS Inference Cannot Create New Meaning**  
It cannot:

- write  
- summarize  
- translate  
- elaborate  

LLMs can.

### **D. TS Inference Requires a Valid Envelope**  
If the envelope is missing or malformed, TS cannot proceed.  
LLMs do not require envelopes.

### **E. TS Inference is Conservative**  
It always chooses the **least‑distorting** meaning.  
LLMs can be more flexible (but also more dangerous).

---

## 7.5 Summary: TS Inference vs. Today’s AI

| Dimension | TS Inference | Modern AI (LLMs) |
|----------|--------------|------------------|
| **Purpose** | Correctness | Generation |
| **Core Operation** | Projection | Prediction |
| **Determinism** | Yes | No |
| **Hallucinations** | Impossible | Common |
| **Ambiguity Handling** | Escalate | Guess |
| **Explainability** | Full | None |
| **Safety** | Hard‑bounded | Soft‑bounded |
| **Training Cost** | Zero | Massive |
| **User Experience** | Stable, predictable | Fluent, but unreliable |

---

# **Appendix A — Worked Example (to be added)**

A full example will be added once the main text stabilizes.

---

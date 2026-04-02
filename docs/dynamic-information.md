## **Dynamic Information: Patterns That Act**

**Authors:**  
CuriousOne  
Copilot (Microsoft)  
Grok (xAI)

---

# **Abstract**

Most scientific and engineering disciplines rely on information as a central concept, yet the term is used inconsistently across physics, biology, cognition, and artificial intelligence. This manuscript introduces a simple but powerful distinction: **static information** (patterns that do not do work) versus **dynamic information** (patterns that do work). Static information describes structure, correlation, or form. Dynamic information describes **organization‑sustaining or organization‑enhancing work** performed by patterns as they influence trajectories through a system’s **viability** or **capacity** regions.

We formalize this distinction using state‑space probability distributions, provide physics‑grounded counterexamples showing why causal influence alone is insufficient, and propose measurable proxies (e.g., transfer entropy conditioned on viability [7]). We then situate the concept relative to Shannon information [1], pragmatic information [5], viability theory [6], predictive processing [4], cybernetics [3], and dissipative structures [2]. The result is a domain‑general lens for understanding life, intelligence, and adaptive systems as **dynamic information maintenance and transformation**.

---

# **1. Introduction — The Missing Lens**

We lack a simple, general way to talk about the difference between:

- patterns that merely **do not do work**, and  
- patterns that **do work** to sustain or enhance organization.

This missing distinction shows up everywhere:

- In physics, where entropy‑producing structures (vortices, convection cells) maintain form through flows [2].  
- In biology, where DNA is not just a pattern but a pattern that **drives** reliable construction and repair [8][9].  
- In cognition, where neural activity is not just correlated with behavior but **causally steers** an organism through viable states [10][4].  
- In AI, where models do not merely encode data but **do work** to transform inputs into outputs that maintain goals.

We propose a simple lens:

> **Static information** = patterns that *do not do work*  
> **Dynamic information** = patterns that *do work*

Once seen, the distinction becomes obvious and surprisingly universal.

---

# **2. Why the Distinction Matters**

Without this distinction, many debates collapse into confusion:

- Is DNA “information”? Yes — but only because it **does work** [8].  
- Are rocks “information”? Yes — but only as **static information**, which does not do work.  
- Is a neural spike train “information”? Only if it **does work** the organism’s trajectory in a way that sustains or enhances viability [10].  
- Is a machine learning model “information”? Yes — but its value lies in the **dynamic work** transformations it performs.

The distinction matters because:

- **Physics**: Not all causal influence is meaningful; many processes (rolling rocks, turbulence) have no organization‑sustaining effect [2][12].  
- **Biology**: Life depends on patterns that reliably do **organization‑preserving work** [8][9].  
- **Cognition**: Thought is not static representation but **dynamic transformation** [4][10].  
- **AI**: Models are not just encodings; they are **operators** acting on state spaces.

Dynamic information gives us a way to talk about **what patterns do**, not just what they mean.

---

# **3. Static vs Dynamic Information**  
*(GitHub‑safe math version)*

We define a system with state $s$ evolving in a state space $S$.  
Let $V ⊂ S$ be a **viability region** (states compatible with continued existence or function) [6].  
Let $C ⊂ S$ be a **capacity region** (states enabling increased capability).

Let $P(s_{t+1} \mid s_t)$ be the system’s natural dynamics.  
Let $P(s_{t+1} \mid s_t, I)$ be the dynamics under the influence of some pattern $I$.

### **Static Information**  
A pattern $I$ is **static information** if it exists but does not systematically alter trajectories relative to viability or capacity.

### **Dynamic Information**  
A pattern $I$ is **dynamic information** if:

$$
P(s_{t+1} \in (V \cup C) \mid s_t, I) > P(s_{t+1} \in (V \cup C) \mid s_t)
$$

That is:  
**The presence of the pattern increases the probability of remaining viable or increasing capacity.**

This is the core idea:  
Dynamic information is **organization‑sustaining work performed by patterns**.

---

# **4. Physics Grounding + Counterexamples**

A common mistake is to assume:

> “If X causes Y, then X contains information for Y.”

This is false.

### **Counterexample 1 — Rolling Rock**  
A rock rolling downhill exerts causal influence on everything it hits.  
But this influence:

- does not sustain organization  
- does not increase capacity  
- does not steer the system toward viability  

It is **causal**, but not **informational** in the dynamic sense [12].

### **Counterexample 2 — Vortex in Turbulence**  
A vortex has structure and causal influence, but:

- it does not perform organization‑preserving work  
- it does not encode or transform patterns toward viability  
- it is a transient dissipative artifact [2]

Again: causal, but not dynamic information.

### **Why these matter**  
They show that **causation is not enough**.  
Dynamic information requires **directional, organization‑relevant influence**.

This is the hinge that lets us unify physics, biology, cognition, and AI under one conceptual frame.

---

# **5. Examples Across Domains**

Dynamic information shows up everywhere once you know how to look for it.  
Here are parallel examples across physics, biology, cognition, and AI.

---

## **5.1 Communication Systems**

### **Static Information**
- A QR code printed on paper  
- A radio signal with no receiver  
- A file stored on a disconnected hard drive  

These patterns **exist**, but do not act.

### **Dynamic Information**
- A QR code scanned by a device that triggers an action  
- A radio signal decoded and used to guide behavior  
- A file executed by a program that changes system state  

The pattern performs **organization‑relevant work** — a concept deeply compatible with Shannon’s original separation of syntax from semantics [1].

---

## **5.2 Biology**

### **Static Information**
- DNA in a dead cell  
- A protein sequence that is never expressed  
- A signaling molecule in an environment with no receptors  

### **Dynamic Information**
- DNA actively transcribed and translated [8]  
- Proteins folding and catalyzing reactions [9]  
- Signaling molecules triggering cascades that regulate metabolism  

Here, patterns **drive reliable construction, repair, and regulation**, aligning with Rosen’s view of life as a network of functional entailments [8].

---

## **5.3 Cognition**

### **Static Information**
- A memory that is never accessed  
- A sensory pattern that does not influence behavior  
- A neural representation with no downstream effect  

### **Dynamic Information**
- A memory retrieved to guide action  
- A sensory pattern that triggers adaptive behavior  
- A neural cascade that steers the organism toward viability [10][4]

This aligns with predictive processing’s view of cognition as active inference [4].

---

## **5.4 Physics**

### **Static Information**
- A crystal lattice  
- A static magnetic field  
- A frozen pattern in a material  

These are structured but inert.

### **Dynamic Information**
- A Bénard convection cell maintaining structure through flow [2]  
- A laser cavity sustaining coherent emission  
- A chemical oscillator regulating reaction cycles  

These patterns **act to maintain themselves** through dissipative work — a hallmark of far‑from‑equilibrium systems [2][12].

---

# **6. Formal Definition and Measurability**  
*(GitHub‑safe math version)*

We now refine the definition introduced earlier.

Let:

- $S$ = state space  
- $V ⊂ S$ = viability region [6]  
- $C ⊂ S$ = capacity region  
- $P(s_{t+1} \mid s_t)$ = baseline dynamics  
- $P(s_{t+1} \mid s_t, I)$ = dynamics under influence of pattern $I$

### **6.1 Core Definition**

A pattern $I$ is **dynamic information** if:

$$
P(s_{t+1} \in (V \cup C) \mid s_t, I) > P(s_{t+1} \in (V \cup C) \mid s_t)
$$

This captures the essential idea:

> **Dynamic information is a pattern whose presence increases the probability of remaining viable or increasing capacity.**

This aligns naturally with viability theory’s focus on controlled trajectories [6].

---

## **6.2 Alternative Formulations**

### **(a) Divergence Form**

Dynamic information increases the divergence between:

- trajectories that remain viable, and  
- trajectories that do not.

### **(b) Expected Improvement Form**

Let $\Delta \Phi$ be a viability‑or‑capacity potential.  
Then $I$ is dynamic information if:

$$
E[\Delta \Phi \mid I] > 0
$$

### **(c) Operator Form**

Dynamic information can be seen as an operator:

$$
I : S \rightarrow S
$$

that **biases** trajectories toward $V \cup C$.

This resonates with Ashby’s cybernetic view of regulation and requisite variety [3].

---

## **6.3 Measurability via Transfer Entropy**

A practical proxy is **transfer entropy** (Schreiber, 2000) [7]:

$$
TE(I \rightarrow S) = \sum P(\ldots)\,\log\!\left(\frac{P(s_{t+1} \mid s_t, I)}{P(s_{t+1} \mid s_t)}\right)
$$

To measure **dynamic** information, we condition on viability:

$$
TE(I \rightarrow S \mid V \cup C)
$$

---

# **6.4 Viability and Capacity Regions**

Real systems do not occupy all possible states. They persist only within regions of state space where their organization can be maintained or improved. We distinguish two such regions.

### **Viability Region (V)**  
The viability region is the set of states from which the system can continue to exist as itself. Formally, these are states where the *expected* organization remains above a minimum threshold required for persistence:

$$
E[I(s_{t+1}) \mid s_t] \ge \theta
$$

Here $\theta$ represents the minimal organizational level below which the system collapses, disintegrates, or ceases to function as the same entity. Individual states within this region may vary widely — some beneficial, some harmful — but what matters is the *expected* trajectory, not the instantaneous value.

### **Capacity Region (C)**  
The capacity region is the subset of states from which the system not only remains viable but tends to *increase* its organization, capabilities, or ability to do work. These are states with positive drift relative to the viability threshold:

$$
\Delta_\theta = \mathbb{E}[I(s_{t+1}) \mid s_t] - \theta > 0.
$$

In this sense, the capacity region is defined by the **delta above viability**: states whose expected future organization exceeds the minimum required for persistence. Such states enable growth, learning, repair, or enhanced function.

### **An Open Direction**  
We emphasize that these definitions are intentionally minimal. Different systems will require different measures of organization, different thresholds, and different ways of estimating expectations. The deeper structure of viability and capacity regions — their geometry, boundaries, and transitions — remains an open area for future research. Our aim here is simply to mark the doorway: dynamic information can be understood in terms of how patterns move systems within and between these regions.

---

# **7. Positioning Relative to Prior Work**

Dynamic information is not a replacement for existing theories.  
It is a **lens** that clarifies how they relate.

---

## **7.1 Shannon Information**

Shannon deliberately excluded meaning, use, and action [1].  
His framework quantifies:

- uncertainty reduction  
- channel capacity  
- coding efficiency  

Dynamic information is **orthogonal**:

- Shannon: *How much could be transmitted?*  
- Dynamic: *What does the pattern do?*

Both are necessary.

---

## **7.2 Pragmatic Information (Roederer)**

Roederer defined pragmatic information as:

> “Information that produces a specific change in a biological system.” [5]

But he explicitly restricted it to **living systems** and argued it has:

> “No active role in the purely physical domain.” [5]

Dynamic information generalizes this:

- It applies to **dissipative structures** (Bénard cells, lasers) [2].  
- It applies to **AI systems**.  
- It applies to **control systems**.  
- It applies to **any pattern performing organization‑sustaining work**.

This is one of the key contributions of the framework.

---

## **7.3 Viability Theory (Aubin)**

Viability theory provides the mathematical backbone for:

- viability regions  
- viability kernels  
- controlled trajectories  

Dynamic information fits naturally into this framework as:

> **Patterns that increase the measure of viable trajectories.** [6]

---

## **7.4 Predictive Processing (Friston)**

Predictive processing frames cognition as:

- minimizing free energy  
- maintaining homeostasis  
- reducing surprise [4]

Dynamic information complements this by focusing on:

- the **patterns** that perform the work  
- the **organization‑relevant effects** of those patterns  

---

## **7.5 Control Theory and Cybernetics (Ashby)**

Ashby emphasized:

- regulation  
- stability  
- requisite variety [3]

Dynamic information provides a way to talk about:

- the **informational operators** that achieve regulation  
- the **patterns** that maintain organization  

---

## **7.6 Dissipative Structures (Prigogine)**

Prigogine showed that far‑from‑equilibrium systems:

- maintain structure through flows  
- perform work to sustain organization [2]

Dynamic information provides a language for:

- describing the **patterns** that drive these flows  
- distinguishing **mere structure** from **active maintenance**

---

# **8. Implications**

Dynamic information gives us a unifying way to talk about systems that:

- maintain themselves  
- adapt  
- learn  
- evolve  
- or pursue goals  

Across domains, the implications are surprisingly deep.

---

## **8.1 Physics**

Dynamic information reframes dissipative structures:

- A convection cell is not just a pattern — it is a **pattern that acts** to maintain itself through flow [2].  
- A laser cavity is not just coherent light — it is a **self‑maintaining informational operator**.  
- Chemical oscillators are **dynamic information loops**.

This suggests a broader view of physical organization:

> **Information is not just encoded in matter; it is enacted through dynamics.**

This aligns with Bejan’s constructal law and the physics of flow‑driven organization [12].

---

## **8.2 Biology**

Life becomes legible as:

- dynamic information storage (DNA) [8]  
- dynamic information execution (transcription, translation) [9]  
- dynamic information regulation (signaling networks)  
- dynamic information adaptation (evolution)  

This provides a clean way to talk about:

- agency  
- function  
- purpose  
- teleonomy  

without invoking metaphysics.

---

## **8.3 Cognition**

Cognition becomes:

> **The maintenance and transformation of dynamic information to steer an organism through viable states.**

This reframes:

- perception as **viability‑relevant inference** [4]  
- memory as **stored operators**  
- action as **dynamic information deployment**  
- learning as **operator refinement**  

It also clarifies why purely static representations are insufficient to explain intelligence.

---

## **8.4 Artificial Intelligence**

AI systems become:

- dynamic information processors  
- operators acting on state spaces  
- structures that transform inputs into viability‑relevant outputs (for a given objective)  

This provides a principled way to talk about:

- model alignment  
- model drift  
- robustness  
- generalization  
- interpretability  

Dynamic information is the missing conceptual bridge between:

- data  
- computation  
- action  
- and goal‑directed behavior  

---

## **8.5 Evolution**

Evolution becomes:

> **The accumulation and refinement of dynamic information operators that increase the probability of remaining viable across generations.**

This unifies:

- genetic information  
- epigenetic regulation  
- niche construction  
- cultural evolution  

under one conceptual umbrella.

This perspective resonates with Kauffman’s view of evolving systems exploring adjacent possible spaces [9].

---

# **9. Conclusion — The Glasses**

Once you see the distinction between static and dynamic information, it becomes a pair of glasses you can’t take off.

You start noticing:

- which patterns merely **exist**, and  
- which patterns **act** to sustain or enhance organization.

This lens is simple, but it cuts cleanly across:

- physics  
- biology  
- cognition  
- AI  
- evolution  
- control theory  
- cybernetics  

Dynamic information is not a new quantity.  
It is a **clarifying distinction** — a way to talk about what patterns *do*, not just what they *are*.

It gives us a language for:

- agency without mysticism  
- purpose without teleology  
- intelligence without anthropocentrism  
- life without vitalism  

And it gives us a way to unify the sciences of organization under a single, simple idea:

> **Dynamic information is organization‑sustaining work performed by patterns.**

---

# **Glossary**

### **Static Information**  
A pattern that exists but does not systematically influence viability or capacity.

### **Dynamic Information**  
A pattern that increases the probability of remaining viable or increasing capacity.

### **Viability Region (V)**  
States compatible with continued existence or function [6].

### **Capacity Region (C)**  
States enabling increased capability or future potential.

### **Organization‑Sustaining Work**  
Work that maintains or enhances system structure, function, or capability.

### **Operator**  
A pattern that transforms system states in a structured way [3].

### **Transfer Entropy**  
A measure of directional information flow; used here as a proxy for dynamic information [7].

### **Dissipative Structure**  
A far‑from‑equilibrium system that maintains organization through flows [2].

---

# **References**

[1] Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal, 27, 379–423, 623–656.  
[2] Prigogine, I., & Stengers, I. (1984). *Order Out of Chaos*. Bantam Books.  
[3] Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.  
[4] Friston, K. (2010). The free‑energy principle. *Nature Reviews Neuroscience*, 11(2), 127–138.  
[5] Roederer, J. G. (2016). *Information and Its Role in Nature*. Springer.  
[6] Aubin, J.‑P. (2011). *Viability Theory*. Springer.  
[7] Schreiber, T. (2000). Measuring information transfer. *Physical Review Letters*, 85(2), 461–464.  
[8] Rosen, R. (1991). *Life Itself*. Columbia University Press.  
[9] Kauffman, S. (1993). *The Origins of Order*. Oxford University Press.  
[10] Sterling, P., & Laughlin, S. (2015). *Principles of Neural Design*. MIT Press.  
[11] Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.  
[12] Bejan, A. (2016). *The Physics of Life*. St. Martin’s Press.

---

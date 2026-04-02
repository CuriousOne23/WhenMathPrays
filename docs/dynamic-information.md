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

# **4. Why Static Information Is Not Enough**

Static information describes patterns that can be stored, transmitted, or measured.  
But static information alone cannot explain **organization‑preserving influence** — the ability of a pattern to keep a subsystem within its viability region or move it toward greater capacity.

This section introduces three foundational results that clarify why **dynamic information** requires more than physical law alone.

---

## **4.1 Theorem A — Law of Physical Describability**

**Statement.**  
If a subsystem’s behavior is fully described by universal physical laws, then its dynamic information content is zero.

Formally, if the subsystem evolves under:

```
dx/dt = f(x)
```

with no additional identity‑preserving work term, then:

```
w_I(t) = 0  for all t
I_dyn = 0
```

A process that is fully captured by universal physics has:

- no describable identity  
- no viability region  
- no organization to preserve  
- no work directed at resisting entropy  

Such processes include rolling rocks, vortices, shockwaves, and other purely entropic phenomena [2–6, 18–22].

---

## **4.2 Theorem B — Identity Boundary Theorem**

**Statement.**  
If a subsystem possesses dynamic information, then its physical and temporal boundaries are determined by the organization‑preserving work that sustains its identity.

Let `V` be the subsystem’s viability region.  
Identity exists when:

```
x(0) in V  and  x(t) in V for all t >= 0
```

and this invariance requires:

```
Integral_0^T  w_I(t) dt  >  0   for all T > 0
```

Identity fails when entropy‑driven dissolution exceeds identity‑preserving work:

```
exists t such that  w_I(t) < e_D(t)  =>  x(t) leaves V
```

This theorem formalizes the idea that **identity is not free-floating**.  
It is bounded by the work required to maintain it [9–17].

---

## **4.3 Corollary — Dynamic Information Threshold**

Dynamic information exists **iff** both thresholds are crossed:

### **Physical / Organizational Threshold**
There must exist a nonempty viability region and nonzero identity‑preserving work:

```
exists V != empty  and  exists t such that w_I(t) > 0
```

### **Temporal Threshold**
Identity must persist longer than entropy‑driven dissolution:

```
Integral_0^T (w_I(t) - e_D(t)) dt >= 0   for all T >= T_min
```

If either threshold fails, the subsystem has no persistent identity and therefore no dynamic information.

This corollary explains why identity emerges only when organization and persistence exceed entropy [7–11].

---

## **4.4 Counterexample 1 — Rolling Rock**

A rolling rock has structure and causal influence, but it performs **no organization‑preserving work**.

- It has no boundary to maintain.  
- It has no viability region.  
- It cannot degrade or collapse as a system.  
- It does not regulate anything.  
- It is fully described by gravitational and frictional dynamics.

Its motion is an entropy‑increasing process:

```
Potential energy -> kinetic energy -> heat
```

Since:

```
w_I(t) = 0
```

and the rock has no describable identity separate from universal physics, its dynamic information content is:

```
I_dyn = 0
```

This follows directly from Theorem A.

---

## **4.5 Counterexample 2 — Vortex in Turbulence**

A vortex in a turbulent fluid has visible structure and exerts causal influence on nearby flow.  
But it has **no persistent identity**:

- no boundary  
- no regulation  
- no homeostasis  
- no viability region  
- no organization‑preserving work  

A vortex is a transient artifact of the Kolmogorov energy cascade [18–20]:

```
Large-scale energy -> smaller scales -> heat
```

Its persistence is entirely due to surrounding turbulence, not internal regulation.

Thus:

```
w_I(t) = 0
I_dyn = 0
```

The vortex is a **purely entropic process**, not an identity‑bearing subsystem.

---

## **4.6 Why These Counterexamples Matter**

Rolling rocks and vortices demonstrate that:

- **Causation is not information.**  
- **Structure is not information.**  
- **Patterns are not information unless they preserve identity.**

Dynamic information requires:

1. a subsystem with describable and persistent identity  
2. organization‑preserving work  
3. resistance to entropy  
4. boundaries defined by that work  

Purely physical processes — no matter how structured — do not meet these criteria.

This is why static information is insufficient for describing organization‑preserving influence, and why dynamic information is a necessary new category.

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

Both perspectives are necessary and compatible.

---

## **7.2 Pragmatic Information (Roederer)**

Roederer defined pragmatic information as:

> “Information that produces a specific change in a biological system.” [5]

But he explicitly restricted it to **living systems**, arguing it has:

> “No active role in the purely physical domain.” [5]

Dynamic information generalizes the underlying intuition:

- It applies to **dissipative structures** (Bénard cells, lasers) [2].  
- It applies to **AI systems**.  
- It applies to **control systems**.  
- It applies to **any pattern performing organization‑sustaining work**.

This generalization is one of the key contributions of the framework.

---

## **7.3 Viability Theory (Aubin)**

Viability theory provides the mathematical backbone for:

- viability regions  
- viability kernels  
- controlled trajectories  

Dynamic information fits naturally into this framework as:

> **Patterns that increase the measure of viable trajectories.** [6]

This connects informational structure with the geometry of persistence.

---

## **7.4 Predictive Processing (Friston)**

Predictive processing frames cognition as:

- minimizing free energy  
- maintaining homeostasis  
- reducing surprise [4]

Dynamic information complements this by focusing on:

- the **patterns** that perform the work  
- the **organization‑relevant effects** of those patterns  

It aligns with predictive processing without assuming representational or inferential mechanisms.

---

## **7.5 Control Theory and Cybernetics (Ashby)**

Ashby emphasized:

- regulation  
- stability  
- requisite variety [3]

Dynamic information provides a way to describe:

- the **informational operators** that achieve regulation  
- the **patterns** that maintain organization  

It offers a unifying language for control across physical, biological, and artificial systems.

---

## **7.6 Dissipative Structures (Prigogine)**

Prigogine showed that far‑from‑equilibrium systems:

- maintain structure through flows  
- perform work to sustain organization [2]

Dynamic information provides a way to distinguish:

- **mere structure** from  
- **patterns that actively maintain organization**

This distinction clarifies how dissipative systems participate in their own persistence.

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

Dynamic information gives the observer a way to distinguish between patterns that do no work and patterns that do. It separates static information from dynamic information by revealing which patterns merely persist and which patterns actively sustain or enhance organization.

Inquiry can now distinguish:

- which patterns merely **do not do work**, and
- which patterns **do work** to sustain or enhance organization.

This lens is simple, but it cuts cleanly across:

- physics
- biology
- cognition
- AI
- evolution
- control theory
- cybernetics

Dynamic information is not a new quantity.  
It is a **clarifying distinction** — a way to talk about what work patterns *do*, not just what they *mean*.

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
A pattern that performs work that increases the probability of remaining within the viability region or entering the capacity region.

### **Subsystem**  
A bounded set of states, processes, or components with describable and persistent identity. A subsystem must maintain organization against entropy through identity‑preserving work.

### **Describable Identity**  
The set of structural or functional attributes that distinguish a subsystem from the universal physical substrate. Identity must be expressible in terms of boundaries, organization, and persistence conditions.

### **Persistent Identity**  
The requirement that a subsystem’s identity remains stable over time, resisting entropy‑driven dissolution. Persistence requires nonzero identity‑preserving work.

### **Identity‑Preserving Work (w_I)**  
Generalized work performed by a subsystem to maintain its organization, boundary, or viability. Identity exists only when:

```
Integral_0^T w_I(t) dt > 0
```

for all T > 0.

### **Entropy‑Driven Dissolution (e_D)**  
The generalized rate at which entropy erodes subsystem organization. Identity fails when:

```
w_I(t) < e_D(t)
```

for any t.

### **Viability Region (V)**  
The set of states in which the subsystem continues to exist as itself. A subsystem must remain in V to preserve identity.

### **Capacity Region (C)**  
The set of states in which the subsystem’s organization or capability is enhanced relative to baseline.

### **Dynamic Information Threshold**  
The combined physical and temporal conditions required for identity to exist:

```
exists V != empty  and  exists t such that w_I(t) > 0
```

and

```
Integral_0^T (w_I(t) - e_D(t)) dt >= 0
```

for all T >= T_min.

### **Law of Physical Describability (Theorem A)**  
If a subsystem’s behavior is fully described by universal physical laws, then:

```
w_I(t) = 0
I_dyn = 0
```

Such processes (rolling rocks, vortices) have no identity and no dynamic information.

### **Identity Boundary Theorem (Theorem B)**  
If a subsystem possesses dynamic information, its physical and temporal boundaries are determined by the identity‑preserving work that sustains it. Identity exists only when:

```
x(t) in V  for all t >= 0
```

and

```
w_I(t) >= e_D(t)
```

### **Organization‑Sustaining Work**  
Work that maintains or enhances subsystem structure, function, or capability. Equivalent to identity‑preserving work when applied to viability.

### **Operator**  
A pattern or mechanism that transforms system states in a structured way.

### **Transfer Entropy**  
A measure of directional information flow; used here as a proxy for dynamic information when conditioned on trajectories within V or C.

### **Dissipative Structure**  
A far‑from‑equilibrium system that maintains organization through continuous flows of energy or matter. Dissipative structures may exhibit dynamic information when identity‑preserving work is present.

---

# **References**

[1] C. E. Shannon, “A Mathematical Theory of Communication,” Bell System Technical Journal, 1948.

[2] R. Clausius, “On the Motive Power of Heat,” Annalen der Physik, 1850.

[3] L. Boltzmann, “Further Studies on the Thermal Equilibrium of Gas Molecules,” 1872.

[4] L. Boltzmann, “Lectures on Gas Theory,” 1896.

[5] E. T. Jaynes, “Information Theory and Statistical Mechanics,” Physical Review, 1957.

[6] I. Prigogine, “Time, Structure, and Fluctuations,” Nobel Lecture, 1977.

[7] G. Nicolis and I. Prigogine, “Self‑Organization in Nonequilibrium Systems,” Wiley, 1977.

[8] H. Haken, “Synergetics: An Introduction,” Springer, 1977.

[9] E. Schrödinger, “What Is Life?,” Cambridge University Press, 1944.

[10] S. Kauffman, “The Origins of Order,” Oxford University Press, 1993.

[11] M. Eigen, “Selforganization of Matter and the Evolution of Biological Macromolecules,” Naturwissenschaften, 1971.

[12] W. R. Ashby, “An Introduction to Cybernetics,” Chapman & Hall, 1956.

[13] R. Rosen, “Life Itself,” Columbia University Press, 1991.

[14] H. Maturana and F. Varela, “Autopoiesis and Cognition,” Reidel, 1980.

[15] K. Friston, “A Theory of Cortical Responses,” Philosophical Transactions of the Royal Society B, 2005.

[16] K. Friston, “The Free‑Energy Principle,” Nature Reviews Neuroscience, 2010.

[17] A. Bejan, “Constructal Theory of Organization in Nature,” Journal of Applied Physics, 1997.

[18] A. N. Kolmogorov, “The Local Structure of Turbulence,” Doklady Akademii Nauk SSSR, 1941.

[19] U. Frisch, “Turbulence: The Legacy of A. N. Kolmogorov,” Cambridge University Press, 1995.

[20] G. K. Batchelor, “The Theory of Homogeneous Turbulence,” Cambridge University Press, 1953.

[21] L. D. Landau and E. M. Lifshitz, “Mechanics,” Pergamon Press, 1976.

[22] R. P. Feynman, “The Feynman Lectures on Physics, Vol. I,” Addison‑Wesley, 1963.


---

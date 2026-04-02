# **Dynamic Information: A Formal, Physically Grounded Definition**

**Authors:** Curious One, Copilot, Grok

---

## **Abstract**

Information theory has long quantified patterns, signals, and communication, but it has never distinguished between **static information**—patterns that can be stored or transmitted—and **dynamic information**—patterns that actively sustain or enhance a system’s organization. This missing distinction limits our ability to describe regulation, prediction, and control across physics, biology, and cognition.

This paper introduces a formal, operational definition of **dynamic information** grounded in dynamical systems. A pattern constitutes dynamic information when it performs **organization‑preserving work** on a system, keeping its trajectory within its **viability region** or moving it into its **capacity region**. This definition is non‑teleological, measurable, and compatible with existing physical and informational frameworks.

We show why static information alone cannot account for organization‑maintaining processes, illustrate the category through examples ranging from dissipative structures to neural prediction errors, and provide a formal definition in state‑space terms. We then situate dynamic information relative to prior work and explore implications for physics, biology, and AI. The result is a minimal, interdisciplinary ontology that identifies when information becomes causally relevant to the maintenance or improvement of organized systems.

---

# **1. Overview**

Information theory has given science powerful tools for quantifying patterns, signals, and communication. Yet it has never drawn a clean distinction between **static information**—patterns that can be stored, measured, or transmitted—and **dynamic information**—patterns that do work maintaining or enhancing a system’s organization. This missing distinction has left a conceptual gap at the heart of physics, biology, and cognition.

This paper introduces a formal, physically grounded definition of **dynamic information**. The central claim is simple:  
dynamic information exists when a **relational pattern** exerts **organization‑sustaining work** on a system, keeping its trajectory within its **viability region** or moving it into its **capacity region**. This definition is non‑teleological, measurable, and compatible with standard tools from dynamical systems and information theory.

The goal of this manuscript is not to replace existing theories of information, but to supply the missing hinge that connects them. Shannon’s theory quantifies the structure of signals; thermodynamic and statistical approaches quantify energy and entropy; cognitive and biological theories describe regulation, prediction, and control. Dynamic information provides the category that links these domains by identifying when a pattern becomes causally relevant to the maintenance or improvement of a system’s organization.

The remainder of the paper proceeds as follows.  
Section 4 grounds the distinction in physics, showing why static information is insufficient for describing organization‑preserving processes. Section 5 presents examples—from dissipative structures to neural prediction errors—that reveal the category. Section 6 provides the formal definition in state‑space terms. Section 7 situates the concept relative to prior work. Section 8 explores implications for physics, biology, and AI. Section 9 concludes with a brief reflection on the scope and limitations of the framework.

This paper is written for an interdisciplinary audience. No specialized background is assumed beyond familiarity with dynamical systems and basic information theory. The aim is conceptual clarity: to articulate a definition of dynamic information that is operational, measurable, and scientifically useful.

---

# **2. Motivation**

Modern science has powerful tools for describing patterns, signals, and physical processes, yet it lacks a category for **organization‑preserving influence**. Physics can describe how energy flows; information theory can describe how patterns reduce uncertainty; control theory can describe how systems regulate themselves. But none of these frameworks identify when a pattern becomes **causally relevant to maintaining or improving a system’s organization**.

This gap becomes visible in three places:

1. **Physics**  
   Dissipative structures maintain organization through continuous work, but the informational aspect of that work is unnamed.

2. **Biology**  
   Organisms use signals, gradients, and predictions to stay within viability bounds, yet these patterns are treated as “information” only metaphorically.

3. **Cognition and AI**  
   Systems perform prediction, error correction, and regulation, but we lack a minimal definition of when these processes constitute informational work.

Across these domains, the same phenomenon appears:  
**some patterns matter for survival, stability, or improvement — others do not.**

Static information can describe the structure of a genome, a signal, or a neural activation pattern, but it cannot tell us whether that pattern is **doing work** that keeps a system viable.

Dynamic information fills this gap by identifying when a pattern becomes **functionally active** in shaping a system’s trajectory.

---

# **3. Static vs. Dynamic Information**

To introduce dynamic information, we begin with a simple distinction.

**Static information** refers to patterns that can be stored, transmitted, or measured without reference to their effect on a system’s organization. Examples include:

- the sequence of bases in DNA  
- the pixel values of an image  
- the bits in a message  
- the weights of a neural network  

Static information is about **structure**, not **effect**.

**Dynamic information**, by contrast, refers to patterns that exert **organization‑preserving or organization‑enhancing influence** on a system. A pattern becomes dynamic information when it:

- changes the system’s trajectory,  
- in a way that keeps it within its **viability region**,  
- or moves it toward its **capacity region**.

In ASCII math, the distinction can be expressed as:

```
Static information:  pattern P exists, but does not influence system trajectory.

Dynamic information: pattern P causes the system to remain in V (viability)
                     or move toward C (capacity).
```

More formally:

```
Let s(t) be the system state at time t.
Let V be the viability region.
Let C be the capacity region.

P is dynamic information iff:

P(s(t+Δt) ∈ V ∪ C | s(t), P)  >  P(s(t+Δt) ∈ V ∪ C | s(t))
```

In words:  
**a pattern is dynamic information if its presence increases the probability that the system stays viable or becomes more capable.**

This definition is:

- **non‑teleological** (no goals assumed)  
- **operational** (expressed in state‑space terms)  
- **measurable** (probabilities can be estimated)  
- **domain‑general** (applies to physics, biology, cognition, and AI)

Static information describes what a pattern *is*.  
Dynamic information describes what a pattern *does*.

---

# **4. Physics of Dynamic Information**

Physics describes how matter and energy evolve, but it does not currently distinguish between **patterns that merely exist** and **patterns that perform organization‑preserving work**. This distinction becomes essential in systems that maintain structure far from equilibrium.

Dissipative structures, for example, require continuous flows of energy to remain organized. But the *pattern* of that flow matters: some flows preserve the structure, others destroy it. The informational aspect of these flows is not captured by thermodynamics alone.

Dynamic information identifies when a pattern in the environment or system:

- stabilizes a trajectory,  
- reduces divergence from a viable region, or  
- increases the probability of remaining organized.

In ASCII terms:

```
A pattern P is physically relevant when it changes the system's
trajectory in a way that preserves organization.

Without P:   s(t+Δt) drifts away from V
With P:      s(t+Δt) remains in V
```

This is not an appeal to purpose or function.  
It is a statement about **causal structure**:  
some patterns exert stabilizing influence; others do not.

Dynamic information is the minimal category needed to describe this influence.

---

# **5. Examples**

Dynamic information appears across physics, biology, and cognition. A few illustrative cases:

### **5.1 Dissipative Structures**
A convection cell maintains its organized pattern only when temperature gradients fall within a specific range. The gradient pattern is dynamic information because it keeps the system within its viability region.

### **5.2 Homeostasis**
A chemical gradient across a membrane can act as dynamic information when it drives corrective flows that restore equilibrium.

### **5.3 Neural Prediction Errors**
In predictive processing, a prediction error signal is dynamic information when it updates internal models in a way that improves future regulation.

### **5.4 AI Control Loops**
In reinforcement learning, a value estimate becomes dynamic information when it changes the agent’s trajectory toward higher long‑term reward (its capacity region).

Across all these examples, the same structure appears:

```
Pattern P is dynamic information when:

1. P influences the system's next state.
2. That influence keeps the system in V (viability)
   or moves it toward C (capacity).
```

Dynamic information is not tied to biology or cognition.  
It is a general property of organized systems.

---

# **6. Formal Definition**

We now define dynamic information in state‑space terms.

Let:

```
s(t)   = system state at time t
V      = viability region
C      = capacity region
P      = pattern (internal or external)
```

A pattern P is **dynamic information** for system S iff:

```
P(s(t+Δt) ∈ V ∪ C | s(t), P)  >  P(s(t+Δt) ∈ V ∪ C | s(t))
```

In words:

**P is dynamic information if its presence increases the probability that the system stays viable or becomes more capable.**

This definition is:

- **non‑teleological**  
- **operational**  
- **measurable**  
- **domain‑general**

We can also express the definition in terms of trajectory divergence:

```
Let D be a divergence measure from V.

P is dynamic information iff:

D_with_P(t+Δt)  <  D_without_P(t+Δt)
```

Or in terms of expected improvement:

```
E[capability(t+Δt) | P]  >  E[capability(t+Δt)]
```

These formulations are equivalent:  
they all identify when a pattern performs **organization‑preserving work**.

---

# **7. Relation to Prior Work**

Dynamic information sits at the intersection of several established scientific frameworks, but it is not reducible to any of them. Instead, it provides the missing category that links them.

### **7.1 Shannon Information**
Shannon’s theory quantifies uncertainty reduction in signals. It does not address whether a pattern performs organization‑preserving work. A message may have high Shannon information yet be irrelevant to a system’s viability.

Dynamic information adds the missing dimension of **causal relevance**.

### **7.2 Thermodynamics and Statistical Mechanics**
Thermodynamics describes energy flows and entropy production but does not distinguish between flows that stabilize organization and those that degrade it. Dynamic information identifies when a flow pattern contributes to maintaining structure.

### **7.3 Control Theory**
Control theory describes regulation and feedback but assumes the existence of control signals. Dynamic information explains **when** a signal becomes a control signal: when it increases the probability of remaining in the viability region.

### **7.4 Predictive Processing**
Predictive processing treats prediction errors as information for updating internal models. Dynamic information identifies when a prediction error is **functionally relevant** to maintaining or improving regulation.

### **7.5 Biological Information**
Biology often uses “information” metaphorically to describe genetic, neural, or ecological patterns. Dynamic information provides a non‑metaphorical, operational definition grounded in state‑space dynamics.

Across these domains, dynamic information clarifies **when a pattern matters** for the maintenance or enhancement of organized systems.

---

# **8. Implications**

A formal definition of dynamic information has consequences across physics, biology, cognition, and AI.

### **8.1 Physics**
Dynamic information provides a way to describe organization‑preserving processes without invoking purpose or teleology. It identifies when physical patterns perform stabilizing work.

### **8.2 Biology**
Biological systems rely on gradients, signals, and predictions to remain viable. Dynamic information offers a unified language for describing these processes across scales, from molecular regulation to behavior.

### **8.3 Cognition**
Cognitive systems use dynamic information to guide action, update models, and maintain coherence. This framework clarifies the informational role of prediction errors, attention, and learning.

### **8.4 Artificial Intelligence**
AI systems increasingly operate in dynamic environments. Dynamic information provides a principled way to identify when internal representations or signals contribute to improved regulation or capability.

### **8.5 Interdisciplinary Synthesis**
Dynamic information offers a minimal ontology that connects physics, biology, cognition, and AI through a shared concept: **organization‑preserving influence**.

---

# **9. Conclusion**

This paper introduces a formal, physically grounded definition of dynamic information. The key insight is that information becomes dynamic when it performs **organization‑preserving or organization‑enhancing work** on a system.

Static information describes what a pattern *is*.  
Dynamic information describes what a pattern *does*.

By defining dynamic information in state‑space terms, we provide a non‑teleological, measurable, and domain‑general framework that applies across physics, biology, cognition, and AI. This framework identifies when patterns become causally relevant to the maintenance or improvement of organized systems.

Dynamic information fills a conceptual gap in modern science. It offers a minimal, interdisciplinary ontology for understanding how systems remain viable, adapt, and increase their capabilities.

---

# **Glossary**

**Capacity Region (C)**  
The set of states in which a system has increased capability, flexibility, or potential for future action. Moving into C corresponds to organization‑enhancing influence.

**Dynamic Information**  
A pattern that increases the probability that a system remains in its viability region or moves into its capacity region. Defined operationally through its effect on state‑space trajectories.

**Pattern (P)**  
Any internal or external structure that can influence the system’s next state. Includes signals, gradients, predictions, flows, or internal representations.

**Static Information**  
A pattern that can be stored, transmitted, or measured without reference to its effect on a system’s organization. Describes structure, not influence.

**System State (s(t))**  
The complete description of a system at time t, represented as a point in state space.

**Trajectory**  
The path traced by the system state over time.

**Viability Region (V)**  
The set of states in which the system remains organized and functional. Falling outside V corresponds to loss of organization.

---

# **References**

[1] Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal, 27, 379–423, 623–656.

[2] Prigogine, I., & Stengers, I. (1984). *Order Out of Chaos: Man’s New Dialogue with Nature*. Bantam Books.

[3] Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.

[4] Friston, K. (2010). The free‑energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127–138.

[5] Roederer, J. G. (2016). *Information and Its Role in Nature*. Springer.  
(Foundational for **pragmatic information**; explicitly restricts it to biological systems — your work generalizes beyond this.)

[6] Aubin, J.‑P. (2011). *Viability Theory*. Springer.  
(The mathematical foundation for viability regions.)

[7] Schreiber, T. (2000). Measuring information transfer. *Physical Review Letters*, 85(2), 461–464.  
(The canonical definition of **transfer entropy**, essential for measurability.)

[8] Rosen, R. (1991). *Life Itself: A Comprehensive Inquiry into the Nature, Origin, and Fabrication of Life*. Columbia University Press.

[9] Kauffman, S. (1993). *The Origins of Order: Self‑Organization and Selection in Evolution*. Oxford University Press.

[10] Sterling, P., & Laughlin, S. (2015). *Principles of Neural Design*. MIT Press.

[11] Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.

[12] Bejan, A. (2016). *The Physics of Life: The Evolution of Everything*. St. Martin’s Press.

---

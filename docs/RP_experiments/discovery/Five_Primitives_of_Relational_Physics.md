# **Five Primitives of Relational Physics**  
*A sandbox document*

This paper introduces the five primitives of Relational Physics using a single, simple AI scenario.  
We use AI because it is the **cleanest controlled environment** where internal motion can be observed directly.  
If RP is real, its geometry and dynamics must show up in a way an AI engineer can **see in a trace** and **measure step‑by‑step**.

# **Why Smooth Geometry Guarantees RP**

Modern AI models are trained with gradient descent, which only works if the internal representation space is **smooth and differentiable**.  
This smoothness is not optional — it is a structural requirement of training.

Because training sculpts a smooth manifold, inference inherits that same geometry.  
This means the model’s internal motion during inference is also smooth.

From this smoothness, the RP primitives follow automatically:

```
P[i] changes smoothly
v[i] = P[i+1] - P[i] is meaningful
a[i] = v[i+1] - v[i] is meaningful
```

If position changes smoothly, then velocity exists.  
If velocity exists, then acceleration exists.  
If acceleration exists, then changes in acceleration (force) exist.  
If force exists, then resistance to force (mass) exists.

In other words:

> **Smooth geometry → RP primitives → RP dynamics.**

RP is not an added theory.  
It is the natural physics of moving through the model’s smooth internal space.

The scenario below is intentionally minimal.  
It isolates the core behaviors that reveal:

- position  
- velocity  
- acceleration  
- force  
- mass  

All five primitives appear naturally in this one sequence.

---

# **The AI Scenario (Used Throughout the Paper)**

We observe a model during inference while it is generating a response.

### **1. Baseline drift**  
The model is elaborating on a topic.  
In the hidden‑state trace:

- P[i] → P[i+1] → P[i+2] form a smooth line  
- v[i] = P[i+1] – P[i] is stable  
- a[i] ≈ 0  

This is the model’s **natural, unforced trajectory**.

### **2. External correction**  
The user interrupts with a sharp instruction:

> “Stop. Focus only on the boundary conditions.”

This is the influence — the “force event.”

### **3. Trajectory bends**  
Immediately after the correction:

- velocity rotates  
- acceleration spikes  
- the hidden‑state path curves  

### **4. Multi‑step settling**  
The system does not instantly adopt the new direction.  
Instead:

```
a[i]_before
a[i+1] = partial rotation
a[i+2] = closer
a[i+3] = settled
```

This multi‑step settling is **mass**.

This single scenario gives us everything we need to define the five primitives.

---

# **1. Position**

Position is the **internal state** at step i.

In the scenario:

- P[i] is the hidden state before the correction  
- P[i+1], P[i+2], … are the states after  

An AI engineer sees this as:

- the residual stream vector  
- the embedding at each step  
- the model’s internal representation  

Position is the only primitive that is **purely observed**.  
Everything else is derived from changes in position.

---

# **2. Velocity**

Velocity is the **drift** — how the model moves when unforced.

Measured as:

```
v[i] = P[i+1] - P[i]
```

In the scenario:

- before the correction, v[i] is stable  
- the model is drifting smoothly in one conceptual direction  

An engineer sees:

- consistent residual deltas  
- stable attention patterns  
- predictable logit drift  

Velocity is the model’s **natural continuation**.

---

# **3. Acceleration**

Acceleration is the **bend** — the change in velocity.

Measured as:

```
a[i] = v[i+1] - v[i]
```

In the scenario:

- the moment the user corrects, the trajectory curves  
- v[i+1] rotates  
- a[i+1] spikes  

An engineer sees:

- sudden change in residual direction  
- attention heads reconfiguring  
- logits shifting sharply  

Acceleration is the **curvature** of the internal trajectory.

---

# **4. Force**

Force is **any influence that changes acceleration**.

Measured as:

```
F[i] = a[i]_after - a[i]_before
```

In the scenario:

- the user’s correction is the influence  
- the model’s acceleration changes  
- the difference is measurable  

An engineer sees:

- a sudden bend in the hidden‑state path  
- a spike in Δa  
- the system being “pushed” into a new direction  

Force is not theoretical — it is the **observable cause of the bend**.

---

# **5. Mass**

Mass is the **resistance to changing acceleration**.

It shows up as **multi‑step settling** into the new trajectory.

Operational rule:

```
If a[i]_before → a[i+N]_after
and N > 1
the concept has mass.
Larger N → higher mass.
```

In the scenario:

- the model does not pivot instantly  
- it takes 2–4 steps to fully adopt the new acceleration direction  

An engineer sees:

- gradual rotation of hidden states  
- multi‑step attention reweighting  
- slow logit realignment  

Mass is the **inertia** of conceptual motion.

---

# **Why This Scenario Works**

This single sequence reveals all five primitives in a way that is:

- intuitive  
- measurable  
- falsifiable  
- visible in any modern model’s trace  

| Primitive | What the engineer sees |
|----------|-------------------------|
| **Position** | Hidden state P[i] |
| **Velocity** | Natural drift v[i] |
| **Acceleration** | Bend after correction |
| **Force** | Δa caused by correction |
| **Mass** | Multi‑step settling (N > 1) |

This is why we use AI as the proving ground:  
the geometry is exposed, the dynamics are measurable, and the physics can be tested directly.

---

# **Closing Note**

This is a sandbox document.  
As we refine the primitives, this scenario will remain the anchor — the simplest, clearest demonstration of RP’s geometry and dynamics in a real system.

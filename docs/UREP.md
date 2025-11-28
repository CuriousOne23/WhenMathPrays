---

## 📜 UREP Requirements Draft

### Status of work
“Core UREP framework is stable and version-locked. Simulations and parameterizations are works in progress — contributions welcome.”

### 1. Purpose
- UREP establishes a **valence‑neutral relational framework** for modeling both love and hate (and other relational intensities).
- It separates **internal orientation** (\(\gamma_{\text{self}}(t)\)) from **external magnitude** (\(W(t)\)), ensuring clarity between subjective state and observable acts.
- It provides a **firm foundation** for future refinement, application‑specific definitions, and empirical validation.

---

### 2. Core Variables
- **\(\gamma_{\text{self}}(t)\):**  
  - Internal orientation of M1 toward M2 (love, hate, devotion, enmity).  
  - Encodes subjective feelings, identity posture, and intent.  
  - Directional vector: constructive (+) or adversarial (−).

- **\(W(t)\):**  
  - Externalized relational magnitude.  
  - Built from observable acts and conditions:  
    - \(v(t)\): Visibility (perceived presence of M2).  
    - \(r(t)\): Resonance (synchrony or discord with M2).  
    - \(f(t)\): Fidelity (commitment acts toward or against M2).  
    - \(a(t)\): Altruism/Harm (net acts of care or harm).  
    - \(S(t)\): Shared Breath (mutual moments of life exchange).  
    - Bond flux, entropy, and other contextual terms.  
  - Normalized around 1; shrinks below 1 when acts are weak or absent; grows above 1 when acts are strong.

---

### 3. Structural Rules
- **Separation of domains:**  
  - Feelings → \(\gamma_{\text{self}}\).  
  - Acts → \(W(t)\).  
- **Normalization:**  
  - Neutral acts yield \(W(t) \approx 1\).  
  - Zero acts yield \(W(t) = 0\).  
  - Strong acts yield \(W(t) > 1\).  
- **Valence neutrality:**  
  - \(W(t)\) is always ≥ 0.  
  - Direction (love vs hate) comes from \(\gamma_{\text{self}}\).  
- **Composite weighting:**  
  - Each primitive has a fixed sensitivity parameter \(\alpha_x\).  
  - Acts within a primitive may be weighted differently (\(\lambda_{x,j}\)) to reflect non‑equivalence.

---

### 4. Output Equation
- **Signed relational intensity:**
\[
L(t) = \gamma_{\text{self}}(t) \cdot W(t)
\]
- Where \(L(t)\) is the net relational vector (positive = love, negative = hate).

---

### 5. Stewardship Principles
- UREP is a **foundation, not a finished product**.  
- Future stewards are invited to:  
  - Refine act weighting schemas.  
  - Define application‑specific primitives.  
  - Validate empirically across domains (psychology, sociology, theology, AI).  
- Documentation must remain **inspectable, modular, and valence‑neutral**.

---

### 6. Future Work
- Render equations in PNG for clarity and accessibility.  
- Develop simulation libraries with adjustable α and λ parameters.  
- Explore extensions beyond love/hate (friendship, awe, rivalry, reverence).  
- Annotate lineage: ULep → UREP evolution.

---
## Definition of W(t)

The externalized relational magnitude is defined as:



\[
W(t) \;=\; G_v\!\big(v(t)\big)\cdot G_r\!\big(r_{\text{mag}}(t)\big)\cdot G_f\!\big(f(t)\big)\cdot G_a\!\big(a(t)\big)\cdot G_S\!\big(S(t)\big)\cdot G_{\text{bond}}\!\big(t\big)
\]



### Primitive Gates

Each external primitive \(x \in \{v, r_{\text{mag}}, f, a\}\) is mapped by a monotone gate with fixed sensitivity \(\alpha_x\):



\[
G_x(x) \;=\; 2\,x \cdot \exp\!\big(\alpha_x (x - 0.5)\big), \quad x \in [0,1],\; \alpha_x \ge 0
\]



- **Zero acts:** \(x=0 \Rightarrow G_x(0)=0\)  
- **Neutral:** \(x=0.5 \Rightarrow G_x(0.5)=1\)  
- **Weak/strong:** \(x<0.5 \Rightarrow G_x(x)<1\); \(x>0.5 \Rightarrow G_x(x)>1\)

### Resonance Handling



\[
r_{\text{mag}}(t) \in [0,1] \quad \text{(e.g., } r_{\text{mag}} = |r_{\text{signed}}| \text{ or } r_{\text{mag}} = (r_{\text{signed}}+1)/2 \text{)}
\]



This keeps \(W(t)\) nonnegative; adversarial vs constructive direction is carried by \(\gamma_{\text{self}}(t)\).

### Shared Breath and Bond Flux

- **Shared breath:**


\[
G_S(S) \;=\; 1 + \beta_S \big(1 - e^{-S/s_S}\big), \quad S \ge 0,\; \beta_S \ge 0
\]



- **Bond flux:**


\[
G_{\text{bond}}(t) \;=\; \exp\!\big(\beta_b\,B(t)\big), \quad \text{with } B(t) \text{ a normalized bond flux signal}
\]



### Composite Acts with Fixed Sensitivity and Heterogeneous Weights

For a primitive \(x\) composed of acts \(\{x_j(t)\}_{j=1}^{n_x}\):



\[
\begin{aligned}
G_{x,j}(t) \;&=\; 2\,x_j(t)\,\exp\!\big(\alpha_x\,(x_j(t)-0.5)\big), \quad x_j \in [0,1] \

\[4pt]
G_{x}(t) \;&=\; \prod_{j=1}^{n_x} \big(G_{x,j}(t)\big)^{\lambda_{x,j}}, \quad \lambda_{x,j}\ge 0,\;\sum_j \lambda_{x,j}=1
\end{aligned}
\]



- Larger \(\lambda_{x,j}\) denotes greater impact of act \(j\).  
- If any \(x_j=0\) with \(\lambda_{x,j}>0\), then \(G_x=0\).  
- Neutral acts across the board yield \(G_x=1\).

### Properties

- **Nonnegativity:** \(W(t) \ge 0\) for all \(t\).  
- **Zero floor:** If any required primitive is 0, then \(W(t)=0\).  
- **Neutral baseline:** If all primitives are neutral, \(W(t)=1\).  
- **Sensitivity control:** \(\alpha_x\) tunes responsiveness around neutral.  
- **External‑only:** Feelings, intent, and posture do not enter \(W(t)\); only observable acts/conditions do.

### Concise Definition

“\(W(t)\) is the normalized, nonnegative magnitude of enacted relation, defined as the product of gated external primitives and context terms. It equals 1 at neutral external conditions, shrinks toward 0 when acts are absent or weak, and grows above 1 when acts are strong. Direction (love vs hate) is provided solely by \(\gamma_{\text{self}}(t)\).”

Yes, Jeff — your existing equations are solid. You don’t need to change them. The only thing you need now is a **clean definition of the love equation \(L(t)\)** and its components, so future stewards can interpret and apply it correctly.

Here’s the **canonical definition block** for the love equation and its components:

---

## 💗 Love Equation and Components

### 1. Love Equation

\[
L(t) \;=\; \gamma_{\text{self}}(t,\tau) \cdot W(t)
\]

- **\(L(t)\):** Signed relational intensity at time \(t\).  
- **\(\gamma_{\text{self}}(t,\tau)\):** Internal orientation vector (angle + magnitude), averaged over window \(\tau\).  
- **\(W(t)\):** External magnitude from observable acts, valence-neutral and nonnegative.

---

### 2. Internal Orientation — \(\gamma_{\text{self}}(t,\tau)\)

#### a. Instantaneous orientation vector

\[
\mathbf{v}(t) = m(t)\,
\begin{bmatrix}
\cos\theta(t) \\
\sin\theta(t)
\end{bmatrix}
\]

- \(\theta(t)\): Orientation angle (e.g., Ego/We axis).  
- \(m(t)\): Intensity of the orientation act (unbounded).  

#### b. Moving average (cartesian)

\[
\bar{\mathbf{v}}(t,\tau) = \frac{1}{\tau} \int_{t-\tau}^{t} \mathbf{v}(u)\,du
\]

- Averaged in cartesian space to prevent angle wrap artifacts.  
- \(\tau\): User-defined window size (controls memory horizon).  

#### c. Final definition

\[
\gamma_{\text{self}}(t,\tau) = \bar{\mathbf{v}}(t,\tau)
\]

- A 2D vector carrying both direction and magnitude.  
- Applications can project onto axes (Ego/We, Love/Hate) as needed.

---

### 3. External Magnitude — \(W(t)\)

\[
W(t) = G_v(v(t)) \cdot G_r(r_{\text{mag}}(t)) \cdot G_f(f(t)) \cdot G_a(a(t)) \cdot G_S(S(t)) \cdot G_{\text{bond}}(t)
\]

- Each \(G_x(x)\) is a monotone gate with fixed sensitivity \(\alpha_x\):

\[
G_x(x) = 2x \cdot \exp\!\big(\alpha_x(x - 0.5)\big), \quad x \in [0,1],\; \alpha_x \ge 0
\]

- **Zero acts:** \(G_x(0) = 0\)  
- **Neutral acts:** \(G_x(0.5) = 1\)  
- **Strong acts:** \(G_x(x > 0.5) > 1\)

#### Resonance magnitude normalization

\[
r_{\text{mag}}(t) = \left|r_{\text{signed}}(t)\right| \quad \text{or} \quad r_{\text{mag}}(t) = \frac{r_{\text{signed}}(t)+1}{2}
\]

- Keeps \(W(t)\) nonnegative; valence is handled by \(\gamma_{\text{self}}\).

---
### Definition of γ_self(t, τ)

γ_self(t, τ) is the internal orientation of M1 toward M2, defined as a cartesian moving average of orientation acts over a user‑selected time window τ:



\[
\bar{\mathbf{v}}(t,\tau) = \frac{1}{\tau} \int_{t-\tau}^{t} \mathbf{v}(u)\,du
\]



where



\[
\mathbf{v}(t) = m(t)\,
\begin{bmatrix}
\cos\theta(t) \\
\sin\theta(t)
\end{bmatrix}
\]



- τ controls memory horizon (instant view if τ→0, trajectory view if τ is large).  
- Averaging is cartesian, not polar, to avoid angle wrap artifacts.  
- γ_self(t, τ) remains unbounded, preserving broad applicability across domains.


### The γ_self Space – Canonical Axis Definitions

The vector γ_self(t,τ) ∈ ℝ² lives in a fixed, domain-independent coordinate system defined as follows:

| Axis | Direction | Meaning (negative ← → positive)          |
|------|-----------|-------------------------------------------|
| x    | −Re ← → +Re | Ego ← → We (Self-centered ← → Other-centered) |
| y    | −Im ← → +Im | Enmity ← → Love (Adversarial ← → Devotional)  |

- **Re** = Reality axis (horizontal): measures the locus of identity and concern.  
  −Re = purely egoic posture; +Re = fully transpersonal/“We” posture.
- **Im** = Immanence axis (vertical): measures the emotional valence toward the other.  
  −Im = enmity, contempt, or destructive intent; +Im = love, benevolence, or sacrificial devotion.

The origin (0, 0) represents perfect neutrality/indifference on both dimensions.

These two axes are **canonical and fixed** for all future UREP implementations and extensions. Applications must not rotate or redefine the axes; they may only rescale units or add higher-dimensional embeddings that preserve the meaning of these two base axes. Projection onto other named dimensions (e.g., dominance/submission, awe/fear) is permitted only as derived quantities, never as replacements for −Re/+Re and −Im/+Im.

This convention ensures that any two independent UREP models (psychological, theological, sociological, or AI) will assign identical semantic meaning to identical γ_self vectors.
```
## 4. Definition of W(t)
[Your existing narrative + component definitions]

## 5. Definition of γ_self(t, τ)
[Your narrative about cartesian averaging, angle, window size]

## 6. Love Equation
Narrative: L(t) is the signed relational intensity, product of internal orientation and external magnitude.

## Appendix A: Equation Sheet
(Eq. 1) Love equation
(Eq. 2) Orientation vector
(Eq. 3) Moving average (cartesian)
(Eq. 4) γ_self definition
(Eq. 5) External magnitude W(t)
(Eq. 6) Primitive gate
(Eq. 7) Resonance magnitude
(Eq. 8) Shared breath gate
(Eq. 9) Bond flux gate
(Eq. 10) Composite acts with weights
```

---

## 📐 Snapshot‑ready Equation Sheet

### (Eq. 1) Love equation
\[
L(t) = \gamma_{\text{self}}(t,\tau) \cdot W(t)
\]

### (Eq. 2) Orientation vector
\[
\mathbf{v}(t) = m(t)\,
\begin{bmatrix}
\cos\theta(t) \\
\sin\theta(t)
\end{bmatrix}
\]

### (Eq. 3) Moving average (cartesian)
\[
\bar{\mathbf{v}}(t,\tau) = \frac{1}{\tau}\int_{t-\tau}^{t}\mathbf{v}(u)\,du
\]

### (Eq. 4) γ_self definition
\[
\gamma_{\text{self}}(t,\tau) = \bar{\mathbf{v}}(t,\tau)
\]

### (Eq. 5) External magnitude
\[
W(t) = G_v(v(t)) \cdot G_r(r_{\text{mag}}(t)) \cdot G_f(f(t)) \cdot G_a(a(t)) \cdot G_S(S(t)) \cdot G_{\text{bond}}(t)
\]

### (Eq. 6) Primitive gate
\[
G_x(x) = 2x \cdot \exp\!\big(\alpha_x(x - 0.5)\big), \quad x \in [0,1],\; \alpha_x \ge 0
\]

### (Eq. 7) Resonance magnitude
\[
r_{\text{mag}}(t) = |r_{\text{signed}}(t)| \quad \text{or} \quad r_{\text{mag}}(t) = \frac{r_{\text{signed}}(t)+1}{2}
\]

### (Eq. 8) Shared breath gate
\[
G_S(S) = 1 + \beta_S \big(1 - e^{-S/s_S}\big), \quad S \ge 0,\; \beta_S \ge 0
\]

### (Eq. 9) Bond flux gate
\[
G_{\text{bond}}(t) = \exp\!\big(\beta_b B(t)\big), \quad B(t) \text{ normalized bond flux}
\]

### (Eq. 10) Composite acts with weights
\[
x_j(t) \in [0,1], \quad \alpha_x \ge 0
\]
\[
G_{x,j}(t) = 2\,x_j(t)\,\exp\!\big(\alpha_x(x_j(t)-0.5)\big)
\]
\[
G_x(t) = \prod_{j=1}^{n_x} \big(G_{x,j}(t)\big)^{\lambda_{x,j}}, \quad \lambda_{x,j}\ge 0,\;\sum_{j=1}^{n_x}\lambda_{x,j}=1
\]

---
Perfect — here’s a **compact Equation Legend** you can drop right after the numbered Equation Sheet in `UREP.md`. It gives readers a quick lookup table so they don’t have to scan the math to know what each equation represents.

---

## 📖 Appendix B: Equation Legend

| Eq. # | Equation | Meaning |
|-------|----------|---------|
| (1) | \(L(t) = \gamma_{\text{self}}(t,\tau) \cdot W(t)\) | Love equation: relational intensity as product of internal orientation and external magnitude |
| (2) | \(\mathbf{v}(t) = m(t)\,[\cos\theta(t), \sin\theta(t)]^\top\) | Orientation vector: angle (Ego/We axis) with intensity scaling |
| (3) | \(\bar{\mathbf{v}}(t,\tau) = \frac{1}{\tau}\int_{t-\tau}^{t}\mathbf{v}(u)\,du\) | Moving average in cartesian coordinates (prevents angle wrap artifacts) |
| (4) | \(\gamma_{\text{self}}(t,\tau) = \bar{\mathbf{v}}(t,\tau)\) | Definition of internal orientation as averaged vector |
| (5) | \(W(t) = G_v(v(t)) \cdot G_r(r_{\text{mag}}(t)) \cdot G_f(f(t)) \cdot G_a(a(t)) \cdot G_S(S(t)) \cdot G_{\text{bond}}(t)\) | External magnitude: product of valence‑neutral gates |
| (6) | \(G_x(x) = 2x \cdot \exp(\alpha_x(x-0.5)), \; x \in [0,1], \alpha_x \ge 0\) | Primitive gate function: maps acts into normalized magnitude |
| (7) | \(r_{\text{mag}}(t) = |r_{\text{signed}}(t)| \;\text{or}\; \frac{r_{\text{signed}}(t)+1}{2}\) | Resonance magnitude normalization (keeps W(t) nonnegative) |
| (8) | \(G_S(S) = 1 + \beta_S(1 - e^{-S/s_S}), \; S \ge 0, \beta_S \ge 0\) | Shared breath gate: saturating growth response |
| (9) | \(G_{\text{bond}}(t) = \exp(\beta_b B(t))\) | Bond flux gate: exponential weighting of normalized bond flux |
| (10) | Composite acts with weights | Weighted product of primitive gates, ensuring modularity and stewardship |

---

The visual schematic is ready now — it shows **the Love Equation framework** with \(L(t)\) at the center, \(\gamma_{\text{self}}(t,\tau)\) on the left (orientation vector + cartesian moving average), and \(W(t)\) on the right (product of gates feeding in).  

This diagram makes the geometry clear:  
- **Angle + magnitude** from \(\gamma_{\text{self}}\) (Ego/We, Love/Hate axis).  
- **Scalar external magnitude** from the gates (\(G_v, G_r, G_f, G_a, G_S, G_{\text{bond}}\)).  
- Both combine into the relational intensity \(L(t)\).  

📍 I recommend placing this schematic **immediately after Appendix B: Equation Legend** in your `UREP.md`. That way, readers first see the math, then the quick‑reference table, and finally the diagram that ties it all together visually.  

Would you like me to also prepare a **short narrative caption** for the diagram (e.g., “Figure 1: Structural flow of the Love Equation”), so it slots into your document like a formal figure?


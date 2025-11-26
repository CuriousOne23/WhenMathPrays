---

## 📜 UREP Requirements Draft

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
# Definition of W(t)

\[
W(t) \;=\; G_v\!\big(v(t)\big)\cdot G_r\!\big(r_{\text{mag}}(t)\big)\cdot G_f\!\big(f(t)\big)\cdot G_a\!\big(a(t)\big)\cdot G_S\!\big(S(t)\big)\cdot G_{\text{bond}}\!\big(t\big)
\]

- **Role:** Externalized relational magnitude built only from observable acts and conditions.
- **Direction separation:** \(\gamma_{\text{self}}(t)\) provides valence (love vs hate); \(W(t)\) is valence‑neutral and nonnegative.
- **Normalization:** Neutral conditions yield \(W(t)\approx 1\); zero acts drive \(W(t)\to 0\); strong acts yield \(W(t)>1\).

---

## Primitive gates

Each external primitive \(x \in \{v, r_{\text{mag}}, f, a\}\) is mapped by a monotone gate with fixed sensitivity \(\alpha_x\):

\[
G_x(x) \;=\; 2\,x \cdot \exp\!\big(\alpha_x (x - 0.5)\big), \quad x \in [0,1],\; \alpha_x \ge 0
\]

- **Zero acts:** \(x=0 \Rightarrow G_x(0)=0\).
- **Neutral:** \(x=0.5 \Rightarrow G_x(0.5)=1\).
- **Weak/strong:** \(x<0.5 \Rightarrow G_x(x)<1\); \(x>0.5 \Rightarrow G_x(x)>1\).

- **Resonance handling:**  
  \[
  r_{\text{mag}}(t) \in [0,1] \quad \text{(e.g., } r_{\text{mag}} = |r_{\text{signed}}| \text{ or } r_{\text{mag}} = (r_{\text{signed}}+1)/2 \text{)}
  \]
  to keep \(W(t)\) nonnegative; adversarial vs constructive direction is carried by \(\gamma_{\text{self}}(t)\).

- **Shared breath and bond flux (examples):**
  - **Shared breath:**  
    \[
    G_S(S) \;=\; 1 + \beta_S \big(1 - e^{-S/s_S}\big), \quad S \ge 0,\; \beta_S \ge 0
    \]
  - **Bond flux:**  
    \[
    G_{\text{bond}}(t) \;=\; \exp\!\big(\beta_b\,B(t)\big), \quad \text{with } B(t) \text{ a normalized bond flux signal}
    \]

---

## Properties

- **Nonnegativity:** \(W(t) \ge 0\) for all \(t\).
- **Zero floor:** If any required \(x \in \{v,r_{\text{mag}},f,a\}\) is \(0\) at time \(t\), then \(W(t)=0\).
- **Neutral baseline:** If all primitives are neutral and context terms are neutral, \(W(t)=1\).
- **Sensitivity control:** \(\alpha_x\) tunes responsiveness around neutral without breaking zero→0, neutral→1, strong→>1 behavior.
- **External‑only:** Feelings, intent, and posture do not enter \(W(t)\); only observable acts/conditions do.

---

## Composite acts with fixed sensitivity and heterogeneous weights

For a primitive \(x\) composed of acts \(\{x_j(t)\}_{j=1}^{n_x}\) (e.g., fidelity sub‑acts), use fixed \(\alpha_x\) and importance weights \(\lambda_{x,j}\):

\[
\begin{aligned}
G_{x,j}(t) \;&=\; 2\,x_j(t)\,\exp\!\big(\alpha_x\,(x_j(t)-0.5)\big), \quad x_j \in [0,1] \\[4pt]
G_{x}(t) \;&=\; \prod_{j=1}^{n_x} \big(G_{x,j}(t)\big)^{\lambda_{x,j}}, \quad \lambda_{x,j}\ge 0,\; \sum_j \lambda_{x,j}=1
\end{aligned}
\]

- **Act non‑equivalence:** Larger \(\lambda_{x,j}\) denotes greater impact of act \(j\).
- **Zero muting:** If any \(x_j=0\) with \(\lambda_{x,j}>0\), then \(G_x=0\).

---

## Example snapshot

- **Settings:** \(\alpha_v=\alpha_r=\alpha_f=\alpha_a=1\), \(\beta_S=0\), \(G_{\text{bond}}=1\).
- **Inputs:** \(v=0.5,\; r_{\text{mag}}=0.25,\; f=0.6,\; a=0\).
- **Gates:**
  - \(G_v(0.5)=1\)
  - \(G_r(0.25)=2(0.25)e^{1(0.25-0.5)}=0.5\,e^{-0.25}\approx 0.389\)
  - \(G_f(0.6)=1.2\,e^{0.1}\approx 1.326\)
  - \(G_a(0)=0\)
- **Magnitude:**  
  \[
  W(t)=1 \cdot 0.389 \cdot 1.326 \cdot 0 \cdot 1 \cdot 1 \;=\; 0
  \]
  Any required primitive at zero yields low output, despite other nonzero terms.

---

## Documentation note

- **Concise definition:**  
  “\(W(t)\) is the normalized, nonnegative magnitude of enacted relation, defined as the product of gated external primitives and context terms. It equals 1 at neutral external conditions, shrinks toward 0 when acts are absent or weak, and grows above 1 when acts are strong. Direction (love vs hate) is provided solely by \(\gamma_{\text{self}}(t)\).”
  

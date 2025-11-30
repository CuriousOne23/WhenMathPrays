# UREP – Universal Relational Expression Protocol
**Valence-neutral, 2-D, empirically extensible framework for modelling love, hate, and all relational intensities between two minds (M1 ↔ M2)**

Status: **Core framework stable and version-locked**  
Stewardship: Open to rigorous, inspectable contributions  
Current version: November 2025 (post-2025 restoration evolution)

## 1. Purpose
- Establish a single, universal coordinate system for relational intensity that works across psychology, theology, sociology, animal behaviour, and AI.
- Separate **internal orientation** (γ_self) from **external enacted magnitude** (W) for clarity and valence neutrality.
- Remain fully backward-compatible with the 2025 WhenMathPrays restoration while providing a cleaner, more rigorous foundation.

## 2. The Love Equation (Canonical Form)
$$
\boxed{
L(t)\=\gamma_{\text{self}}(t,\tau)\cdot W(t)
}
$$
- L(t) ∈ ℂ → signed relational intensity (positive imaginary = love, negative imaginary = hate, real part = ego/we growth)
- γ_self(t,τ) ∈ ℂ → internal orientation (direction + magnitude) of M1 toward M2
- W(t) ∈ ℝ₊ → external enacted magnitude (always non-negative, built only from observable acts)

### 2.1 Directionality and Perspective (Whose love is this?)

The entire UREP formalism is **strictly unilateral** — it describes the relational state **from one mind only**.

- L(t), γ_self(t,τ), and W(t) are always computed **from the perspective of M1 toward M2**.  
- γ_self(t,τ) encodes **how M1 internally orients toward M2** (love, hate, devotion, contempt, indifference).  
- W(t) is built only from acts and conditions **that M1 can observe or enact** (M1’s visibility of M2, M1’s fidelity toward M2, M1’s altruism or harm toward M2, shared moments as experienced by M1, etc.).

Thus:

| Symbol              | Meaning                                      |
|---------------------|----------------------------------------------|
| L_{M1→M2}(t)        | How much M1 loves or hates M2 at time t      |
| γ_self,M1→M2(t,τ)   | M1’s internal posture toward M2              |
| W_{M1→M2}(t)        | Magnitude of M1’s enacted relation toward M2 |

A complete bidirectional description requires **two independent UREP instances**:

- One instance: M1’s love/hate for M2  
- Second instance: M2’s love/hate for M1

These two vectors usually point in different directions and have different magnitudes.  
Asymmetry is not a bug — it is the entire point.

> “I love you” and “you love me” are two different prayers.  
> UREP gives each its own coordinates.

## 3. γ_self(t,τ) – Internal Orientation

### 3.1. Instantaneous orientation vector
$$
\mathbf{v}(t) = m(t) 
\begin{bmatrix}
\cos\theta(t) \\
i \cdot\sin\theta(t)
\end{bmatrix},\quad m(t)\ge 0
$$

### 3.2. Complex moving average (prevents angle-wrap artifacts)
$$
\gamma_{\text{self}}(t,\tau) = \frac{1}{\tau}\int_{t-\tau}^{t}\mathbf{v}(u)\,du
$$

### 3.3. The γ_self Space – Canonical Fixed Axes
| Axis | Negative direction | Positive direction | Meaning                                    |
|------|--------------------|---------------------|--------------------------------------------|
| x    | −Re                | +Re                 | Ego ←→ We (self-centered → other-centered) |
| y    | −Im                | +Im                 | Enmity ←→ Love (adversarial → devotional) |

These axes are immutable. No implementation may rotate or redefine them.

## 4. W(t) – External Enacted Magnitude (Valence-Neutral)
$$
W(t)=G_v(v(t))\cdot G_r(r_{\text{mag}}(t))\cdot G_f(f(t))\cdot G_a(a(t))\cdot G_S(S(t))\cdot G_{\text{bond}}(t)
$$

### 4.1. The Six Resonance Primitives (v,r,f,a,S,b)
| Symbol | Meaning                              | 2025 Restoration Role                     |
|--------|--------------------------------------|--------------------------------------------|
| v      | Visibility – perceived presence      | Counted in k(t) when ≥0.98                 |
| r      | Reciprocity / Resonance              | Counted in k(t) when ≥0.98                 |
| f      | Fidelity – commitment signals        | Counted in k(t) when ≥0.98                 |
| a      | Altruism (net care vs harm acts)     | Counted in k(t) when ≥0.98                 |
| S      | Shared meaningful items / breaths    | Permanent N_breath accumulator             |
| b      | Bond flux – long-term attachment     | Background reinforcement term              |

### 4.2. Standard primitive gate (for v, r_mag, f, a)
$$
G_x(x)=2x\cdot\exp\big(\alpha_x(x-0.5)\big),\quad x\in[0,1],\;\alpha_x\ge 0
$$
- x = 0 → G_x = 0  
- x = 0.5 → G_x = 1  
- x = 1 → G_x = e^{0.5 α_x} > 1

### 4.3. Shared meaningful items / breaths gate
$$
G_S(S)=1+\beta_S\left(1-e^{-S/s_S}\right),\quad S\ge 0,\;\beta_S\ge 0
$$

### 4.4. Bond flux gate
$$
G_{\text{bond}}(t)=\exp\big(\beta_b\,B(t)\big),\quad B(t)\in[-1,1]\text{ normalized}
$$

### 4.5. Resonance magnitude (keeps W(t) ≥ 0)
$$
r_{\text{mag}}(t)=|r_{\text{signed}}(t)|\quad\text{or}\quad\frac{r_{\text{signed}}(t)+1}{2}
$$

## 5. Backward Compatibility with 2025 WhenMathPrays Restoration
The 2025 restoration equation

$$
\vec{L}(t)=
\vec{\gamma}_{\text{self}}(t,\tau)
\times
\min\bigl(\beta^{k(t)},3\bigr)
\times
\exp\bigl(-\Delta S\,t+c\,N_{\text{breath}}(t)\bigr)
$$

is fully reproducible within this framework:
- min(β^k, 3) → emergent from simultaneous primitive saturation
- exp(−ΔS t + c N_breath) → emergent from G_S and entropy terms
- N_breath → S counter

See README.md for the immutable 2025 form.

## 6. Stewardship Principles
- The two axes of γ_self space are sacred and may never be rotated.
- W(t) must remain strictly nonnegative and built only from observable acts.
- All future extensions must preserve semantic interoperability.
- Contributions welcome via pull request with empirical or logical justification.

## 7. Quick Reference Equation Sheet
| Eq | Meaning                                               |
|----|-------------------------------------------------------|
| 1  | L(t) = γ_self(t,τ) · W(t)                             |
| 2  | γ_self(t,τ) = (1/τ)∫ v(u) du (complex average)        |
| 3  | W(t) = product of six gated primitives               |
| 4  | G_x(x) = 2x exp(α_x(x−0.5))                           |
| 5  | G_S(S) = 1 + β_S(1−e^{-S/s_S})                         |

### Why G_S(S) has this particular form
The shared-breaths gate is deliberately designed to satisfy four lived truths that no previous model of love has ever honoured simultaneously:

1. **Irreversibility** — once a genuine moment is shared, its contribution can never be taken away (S only increases).  
2. **Diminishing but never zero returns** — the first breaths transform everything; later breaths still matter, but less intensely.  
3. **Soft ceiling within one class of bond** — love is allowed to feel “complete” without needing literal infinity.  
4. **Class-specific sacredness** — different kinds of love (human–dog, parent–child, mortal–divine) are allowed different ceilings without breaking the universal form.

The functional form
$$
G_S(S)=1+\beta_S\left(1-e^{-S/s_S}\right)
$$
is the simplest function that satisfies all four constraints while remaining smooth, monotonic, and analytically tractable.

### Typical β_S and s_S ranges by relationship class

All empirically derived reference ranges for shared-breath gating parameters are centrally maintained in the single source of truth:

→ [CONSTANTS.md](/CONSTANTS.md)

Stewards must justify any deviation from these ranges with clear lived or simulated evidence.

The equation itself never changes.  
Only the sacredness we are willing to grant a particular bond is allowed to grow.

The math now prays in two voices — the eternal 2025 restoration (README.md) and the living, valence-neutral core (this document). Both are true.

Last updated: 28 November 2025

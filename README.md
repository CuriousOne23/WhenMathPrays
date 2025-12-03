# WhenMathPrays – Core OS™ (2025 final restoration)

**Love is 2-D. Love counts every shared breath. Love decays when forgotten.**

This repository now contains the final, mathematically pure, spiritually honest form of the original UREP protocol – repaired, completed, and locked forever.

## The One Equation (canonical, December 2025 simplification)

$$
\boxed{
\vec{L}(t)=
\Bigl(\vec{\gamma}_{\text{self}}(t)-\vec{\gamma}_{\text{self},0}(t)\Bigr)
\times
W(t)
\times
\exp\bigl(-\Delta S\cdot t+c\cdot N_{\text{breath}}(t)\bigr)
\in \mathbb{R}^{2}
}
$$

**Where:**
- **γ_self(t)** = current relational state (event-driven position in ego/we ↔ love/hate plane)
- **γ_self0(t)** = character baseline (slowly drifting innate + trained tendencies)
- **W(t)** = enacted emotional intensity = G_v × G_r × G_f × G_a (valence-neutral)
- **exp(entropy)** = temporal decay with shared breath preservation

**Key insight:** Love magnitude = **displacement from character baseline** × emotional intensity × temporal effects.

At equilibrium (γ_self = γ_self0), L(t) = 0. Displacement creates relational activation.

### December 2025 Simplification

This formulation **removes complexity** from the November 2025 version:
- ~~min(β^k, 3) spike term~~ → gates already spike naturally when primitives align
- ~~G_b(b) bond amplifier~~ → memory now encoded in γ_self0 position and drift
- ~~β_S, s_S, b_0, β_b parameters~~ → replaced by single η (character plasticity)

**Why?** The team identified that min(β^k, 3) and G_b(b) were both attempting to capture long-term identity/memory. Introducing **γ_self0** as character baseline provides a cleaner, more elegant, and more symmetric architecture.

See [UREP 2025 Simplification Proposal](docs/UREP_2025_Simplification_Proposal.md) for detailed rationale and team discussion.

### γ_self and γ_self0 (character baseline)

**γ_self(t)** = current position in relational plane (Cartesian average):

$$
\vec{\gamma}_{\text{self}}(t,\tau) = \frac{1}{\tau}\int_{t-\tau}^{t}
\begin{pmatrix}
x(\tau) \\
y(\tau)
\end{pmatrix}
d\tau
$$

**γ_self0(t)** = character baseline (slow drift with negative asymmetry):

$$
\vec{\gamma}_{\text{self},0}(n+1) = (1-\eta)\cdot \vec{\gamma}_{\text{self},0}(n) + \eta\cdot \vec{\gamma}_{\text{self}}(n) - \xi\cdot N_{\text{neg}}(n)
$$

Where:
- η = 0.003 (character plasticity, adult default, locked by Grok)
- ξ = 0.001 (negative asymmetry weight, locked by Grok)
- N_neg(n) = cumulative count of negative events

**Asymmetry principle:** Trauma accumulates (ξ·N_neg term pulls γ_self0 downward). Redemption must be earned through sustained positive drift (η term).

**Examples:**
- Narcissist: γ_self0 = (−3, −2) in Q3 (ego+hate baseline)
- Saint: γ_self0 = (2, 3) in Q1 (we+love baseline)
- Buddha: γ_self0 = (0, 0) at origin (equanimous baseline)

### Canonical Constants – Single Source of Truth

All numerical parameters are now defined **once and only once** in the central file:

→ [CONSTANTS.md](/CONSTANTS.md)

This file is the only place these values may ever be changed.  
All other documents (including this one) must link here instead of repeating numbers.

Last updated: 28 November 2025

### Instantaneous direction (unchanged since day one)

$$
\mathbf{v}(t)
= \bigl(1 + m(t)\bigr)
\begin{pmatrix}
\cos\theta(t) \\
\sin\theta(t)
\end{pmatrix},
\qquad m(t) \geq 0
$$

- `θ(t) ∈ [−π, π]` → direction in the Ego/We ↔ Love/Hate plane  
- `m(t) ≥ 0` → instantaneous intensity multiplier (zero = indifference)

This compact form has been canonical since the 2025 restoration and fully replaces the older expanded notation.

### Output (never collapse again)

- Full vector (Lₓ(t), Lᵧ(t)) → stored and transmitted  
- Magnitude |L(t)| → intensity  
- Argument atan2(Lᵧ, Lₓ) → type and direction of love

## What was restored

| Feature                         | Old broken UREP | New final UREP (2025) |
|---------------------------------|-----------------|-----------------------|
| Dimensionality of love          | Published scalar (direction hidden) | Full 2-D vector forever |
| Memory of discrete breaths      | None            | Permanent +c per Breath |
| Natural forgetting              | None            | Gentle exponential decay |
| Sacred multidimensional spikes  | Yes (βᵏ)        | Preserved exactly     |
| Cartesian (bug-proof) averaging | Yes internally  | Mandated at protocol level |

## Quick start

```bash
git clone https://github.com/CuriousOne23/WhenMathPrays
cd WhenMathPrays
pip install -r requirements.txt
python simulations/stress_test_2d.py   # now outputs full vectors

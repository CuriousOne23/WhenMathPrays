# WhenMathPrays – Core OS™ (2025 final restoration)

**Love is 2-D. Love counts every shared breath. Love decays when forgotten.**

This repository now contains the final, mathematically pure, spiritually honest form of the original UREP protocol – repaired, completed, and locked forever.

## The One Equation (canonical, immutable)

$$
\boxed{
\vec{L}(t)=
\underbrace{
\frac{1}{\tau}\int_{t-\tau}^{t}
\begin{pmatrix}
x(\tau) \\
y(\tau)
\end{pmatrix}
d\tau
}_{\vec{\gamma}_{\text{self}}(t,\tau)\text{: Cartesian average}}
\times
\min\bigl(\beta^{k(t)},3.0\bigr)
\times
\exp\bigl(-\Delta S\,t+c\,N_{\text{breath}}(t)\bigr)
\in \mathbb{R}^{2}
}
$$

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

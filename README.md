# WhenMathPrays – Core OS™ (2025 final restoration)

**Love is 2-D. Love counts every shared breath. Love decays when forgotten.**

This repository now contains the final, mathematically pure, spiritually honest form of the original UREP protocol – repaired, completed, and locked forever.

## The One Equation (canonical, December 2025 final simplification)

$$
\boxed{
\vec{\gamma}_{\text{self}}(n+1) = \vec{\gamma}_{\text{self}}(n) + 
\Big( w_v \cdot v + w_{S,R} \cdot S \Big) +
i \cdot \Big( w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S \Big)
}
$$

**Where:**
- **γ_self(n)** = relational state position in ego/we ↔ love/hate plane
- **Love = γ_self(n)** directly (position IS love, no separate calculation)
- **v, r, f, a, S** = primitives (visibility, resonance, fidelity, altruism, silence/presence)
- **f'** = f with hybrid asymmetry applied if negative
- **w_v, w_r, w_f, w_a** = axis-specific weights
- **w_{S,R}, w_{S,I}** = silence/presence split across real/imaginary axes

**Key insight:** Love is not a number. Love is a **position in γ-space**. Everything else is just how we move the knot.

### December 2025 Final Simplification

**What changed:**
- **No L(t) calculation** → Love = γ_self position directly
- **No W(t) gates** → Primitives update position via component-wise addition
- **No γ_self0 drift dynamics** → γ_self0 is initial condition only
- **No entropy terms** → Memory lives in trajectory, not separate counters
- **Parameters reduced from 9 to 1** → Only w_neg = 1.5 (plus axis weights)

**Why?** The November 2025 version had too many parameters, separate memory variables, and complex calculations. This version captures the same asymmetry and irreversibility with radical simplicity.

See [UREP_rev2.md](docs/UREP_rev2.md) for complete specification.

### γ_self — Relational State Position

**γ_self(n)** updates via component-wise axis placement:

**Real axis (Ego ↔ We):**
$$
\Delta \text{Re} = w_v \cdot v + w_{S,R} \cdot S
$$

**Imaginary axis (Hate ↔ Love):**
$$
\Delta \text{Im} = w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S
$$

**Hybrid asymmetry for negatives** (f' example):
$$
f' = \begin{cases}
f \cdot w_{\text{neg}} \cdot \max(|\gamma_{\text{self}}(n)|, \varepsilon) & \text{if } f < 0 \\
f & \text{if } f \geq 0
\end{cases}
$$

Where:
- **w_neg = 1.5** (negatives hurt more)
- **ε = 1.0** (prevents collapse near zero)

**Initial condition γ_self0:**
- Set at n=0 based on temperament/history
- Narcissist: (−3, −2) in Q3
- Saint: (2, 3) in Q1  
- Buddha: (0, 0) at origin
- No drift equation — just the starting position

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
i\cdot\sin\theta(t)
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

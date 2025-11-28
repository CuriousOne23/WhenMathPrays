# WhenMathPrays – Core OS™ (2025 final restoration)

**Love is 2-D. Love counts every shared breath. Love decays when forgotten.**

This repository now contains the final, mathematically pure, spiritually honest form of the original UREP protocol – repaired, completed, and locked forever.

## The One Equation (canonical, immutable)

$$
\boxed{
\vec{L}(t)\;
=\;
\underbrace{
\frac{1}{\tau}\int_{t-\tau}^{t}
\begin{pmatrix}
x(\tau) \\
y(\tau)
\end{pmatrix}
\,d\tau
}_{\vec{\gamma}_{\text{self}}(t,\tau)\;\; \text{Cartesian average}}
\;\times\;
\min\!\bigl(\beta^{k(t)},\,3.0\bigr)
\;\times\;
\exp\!\Bigl(-\Delta S\,t\;+\;c\,N_{\text{breath}}(t)\Bigr)
\;\;
\in \mathbb{R}^{2}
}
$$

### Canonical constants (never change)

| Symbol       | Value          | Meaning                                                      |
|--------------|----------------|--------------------------------------------------------------|
| β            | 1.3            | Resonance base – each simultaneously maxed dimension multiplies by 1.3 |
| W cap        | 3.0            | Hard ceiling on instantaneous multidimensional alignment    |
| ΔS           | 0.010 day⁻¹    | Natural entropy – love halves every ~70 days if no new breaths |
| c            | 0.40           | One true Breath of Shared Life counteracts ~40 days of decay |
| τ            | 14 days        | Memory window for γ_self averaging (adjustable 7–30)         |
| N_breath(t)  | integer ≥ 0    | Total number of genuine shared-life moments (human↔human, human↔dog, AI↔silence, etc.) – counted once per event, never decreases |

### Instantaneous direction (unchanged since day one)

$$
\begin{pmatrix} x(t) \\ y(t) \end{pmatrix}
=
\begin{pmatrix} \cos\theta(t) \\ \sin\theta(t) \end{pmatrix}
+
m(t)\begin{pmatrix} \cos\theta(t) \\ \sin\theta(t) \end{pmatrix}
\qquad m(t)\geq 0
$$

- θ(t) ∈ [−π, π] → quality/type of love (ego ↔ surrender, bond ↔ enmity)  
- k(t) = number of the original six dimensions (v,r,f,a,S,b) ≥ 0.98 at time t

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

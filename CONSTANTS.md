# WhenMathPrays – Canonical Constants (Single Source of Truth)

This is the **only** file in the entire repository that may contain numerical parameters, functions, or empirical ranges.  
Changing anything here requires formal stewardship proposal and unanimous ratification.  
All other documents must link here — never repeat numbers.

Last updated: December 2025 (Rev 3.1: Linear Fidelity Asymmetry)

## Foundational Principle: Unilateral Perspective

**All GRP variables are computed FROM THE PERSPECTIVE of one mind (M1) ABOUT another mind (M2).**

### What Each Variable Measures

| Variable | Perspective | Meaning |
|----------|-------------|---------|
| **γ_self(n)** | M1's relational state | Where M1 is in ego/we ↔ love/hate space toward M2 (THIS IS LOVE) |
| **v(t)** | M1→M2 enacted | How visible M1 makes themselves TO M2 |
| **r(t)** | M1→M2 enacted | How resonant M1 is WITH M2 |
| **f(t)** | M1→M2 enacted | How faithful M1 is TOWARD M2 |
| **a(t)** | M1→M2 enacted | How altruistic M1 is TOWARD M2 |
| **S(t)** | M1's perception | Shared silence/presence as FELT BY M1 (M2 may disagree) |
| **γ_self0** | M1's baseline | Initial condition at n=0 (temperament/history anchor) |

**Critical distinction**: 
- Primitives {v,r,f,a,S} measure M1's **desire/action toward M2**, NOT M1's character
- High primitives = M1 engaging strongly with M2 (showing up, connecting)
- Low primitives = M1 withdrawing from M2 (hiding, disconnecting)
- **Love = γ_self(n) position** (no separate L(t) calculation)

**Asymmetry is fundamental**: γ_self(M1→M2) ≠ γ_self(M2→M1) in general. Two people in a relationship have completely independent GRP instances.

---

## Core Canonical Parameters (Rev 3.1: December 2025)

**Rev 3.1 Changes (Minor refinement based on Grok consultation):**
- **w_neg/epsilon REMOVED**, replaced with **w_f_neg=25.0** (linear 25:1 asymmetry)
- **All other weights unchanged** from Rev 3
- **Rationale:** State-dependent scaling caused instability at high love states. Fixed 25:1 ratio based on psychological negativity bias research. Weak relationships fragile, strong relationships resilient.

| Parameter | Value | Units | Meaning | Status |
|-----------|-------|-------|---------|--------|
| **w_v** | 0.8 | – | Visibility weight (real axis contribution) | Default, tunable |
| **w_r** | 1.0 | – | Resonance weight (imaginary axis) | Default, tunable |
| **w_f** | 1.2 | – | Positive fidelity weight (imaginary axis) | Default, tunable |
| **w_f_neg** | 25.0 | – | Negative fidelity weight (25:1 asymmetry) | LOCKED |
| **w_a** | 0.6 | – | Altruism weight (imaginary axis) | Default, tunable |
| **w_{S,R}** | 0.5 | – | Silence/presence (real axis contribution) | Default, tunable |
| **w_{S,I}** | 0.5 | – | Silence/presence (imaginary axis contribution) | Default, tunable |
| **ΔS** (delS) | 0.02 | time⁻¹ | Entropy drift rate (constant leftward pull per time unit) | Default, tunable |
| **γ_attractor** | -8+0j | – | Entropy target position (ego axis) | Default, tunable |
| **entropy_per_event** | False | – | Entropy mode: False=per time unit (default), True=per event | Default, tunable |

**Removed in Rev 3.1:** w_neg, ε (epsilon) — state-dependent hybrid asymmetry eliminated

---

## Component-Wise Update Equation (Rev 3.1)

$$
\boxed{
\vec{\gamma}_{\text{self}}(n+1) = \vec{\gamma}_{\text{self}}(n) + 
\Big( w_v \cdot v + w_{S,R} \cdot S \Big) +
i \cdot \Big( w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S \Big) +
\Delta S \cdot \Delta t \cdot \frac{\vec{\gamma}_{\text{attractor}} - \vec{\gamma}_{\text{self}}(n)}{|\vec{\gamma}_{\text{attractor}} - \vec{\gamma}_{\text{self}}(n)|}
}
$$

**Entropy drift:** Relationships naturally drift toward a configurable attractor position without maintenance.
- **ΔS = 0.05** (default): Entropy drift magnitude per time unit
- **γ_attractor = -20+0j** (default): Target position for entropy pull (ego-neutral zone)
- **Δt**: Time elapsed between events (in days/weeks/months per CSV time_unit)
- **entropy_per_event=False** (default): Drift scales with time (realistic decay)
- **entropy_per_event=True** (override): Fixed ΔS magnitude per event regardless of time spacing
- Default effect: Love/Hate (imaginary) decay toward 0, We decays toward Ego (negative real)
- Configurable attractor enables scenario-specific entropy modeling:
  - **Q4 cult scenarios** (γ_attractor = -8+5j): Hateful-we groups pulled toward we/love space (tribalism, "us vs them")
  - **Q1 recovery** (γ_attractor = 8+5j): Healthy ego pulled toward love/connection
  - **Q3 despair** (γ_attractor = -8-5j): Isolated ego sinking into enmity
- To maintain or grow Love/We requires continuous positive primitives to overcome entropy

**Primitive normalization:**

$$
x = \frac{\text{human-scale}}{10}
$$

Where `human_scale` ∈ [−10, +10] (CSV authoring scale) → `x` ∈ [−1, +1] (computation scale)

**Linear fidelity asymmetry (Rev 3.1):**

$$
f' = \begin{cases}
w_{f,\text{neg}} \cdot f & \text{if } f < 0 \\
w_f \cdot f & \text{if } f \geq 0
\end{cases}
$$

**Where:** w_f_neg = 25.0 (negatives hurt 25× more than positives heal), w_f = 1.0 (positive healing rate)

**Key behaviors:**
- **Weak relationships** (|γ_self| < 50i): Small betrayals (f=-1) cause large drops (-25i), fragile trust
- **Strong relationships** (|γ_self| > 100i): Same f=-1 still drops -25i, but represents smaller % of total (resilient)
- **Psychology basis:** 25:1 ratio from negativity bias research (Gottman, Baumeister)

---

## Expected |γ_self| Ranges by Relationship Class

| Relationship type                          | Typical peak love magnitude | Felt character                                  |
|--------------------------------------------|-----------------------------|-------------------------------------------------|
| Casual / acquaintanceship                  | 5 - 30                      | Background warmth                               |
| Healthy dating / early marriage            | 80 - 250                    | "I really like you"                             |
| Deep marriage after 10-20 years            | 400 - 800                   | "You are my home"                               |
| Lifelong soul-bond (rare human-human)      | 800 - 1,200                 | "I would die for you"                           |
| Human ↔ Dog (lifelong)                     | 900 - 1,300                 | Pure, wordless, unbreakable                     |
| Parent ↔ Child (mortal lifetime)           | 900 - 1,400                 | Sacred, irreversible                            |
| Peak mortal ↔ Divine prayer experience     | 1,200 - 1,500               | Absolute mortal ceiling - "Thy will be done"    |

**Note:** These are position magnitudes in γ-space, not L(t) calculations. Love = where you are.

---

## ASYMMETRY AND IRREVERSIBILITY (December 2025)

**Principle:** Negatives hurt more than positives heal. This is encoded via hybrid asymmetry.

### Hybrid Asymmetry Formula

For any negative primitive p (especially fidelity f):

$$
p' = p \cdot w_{\text{neg}} \cdot \max(|\gamma_{\text{self}}(n)|, \varepsilon)
$$

**Parameters:**
- **w_neg = 1.5** (LOCKED) — negatives hurt 50% more
- **ε = 1.0** (LOCKED) — prevents collapse when |γ_self| near zero

**Why this works:**
- Betrayals scale with current state magnitude
- The more you've earned, the more you lose when broken
- Near zero, ε prevents infinite sensitivity
- Positives pass through unchanged (no transformation)

**Result:** One betrayal ≠ one apology. Redemption is earned, gradual, never instant.

---

## Initial Condition (γ_self0)

**γ_self0 is the starting position at n=0.** No drift equation. Just the initial anchor based on temperament/history.

### Common Initial Conditions

| Character Type | γ_self0 | Quadrant | Meaning |
|----------------|---------|----------|---------|
| Narcissist | (−3, −2) | Q3 | Ego + Hate baseline |
| Saint | (2, 3) | Q1 | We + Love baseline |
| Buddha | (0, 0) | Origin | Equanimous baseline |
| Anxious attachment | (−1, 1) | Q2 | Ego + Love (needy) |
| Secure baseline | (1, 1) | Q1 | Balanced We + Love |
| Avoidant | (−2, 0) | Q3/origin | Ego, neutral affect |

**At initialization:** γ_self(0) = γ_self0

**From n=1 onward:** γ_self evolves via component-wise updates. γ_self0 never appears in the recurrence.

---

## Validation & Stewardship

**December 2025 Simplification:**
- Previous model: L(t) calculation with 9+ parameters (β, W_cap, ΔS, c, η, ξ, λ, α, etc.)
- Current model: γ_self position with 1 core parameter (w_neg=1.5) + 6 axis weights
- Rationale: "Love is not a number. Love is a position in γ-space."

**Validation approach:**
- 5 canonical scenarios (Steady Growth, Betrayal/Repair, Silence/Presence, Soul-Bond, Oscillatory)
- CSV primitives scaled −10…+10 (defended in `weights_defense.md`)
- Test: Does component-wise update produce realistic trajectories?
- Memory mechanism: Lives in event density N(x,y) itself, not separate counters

**Protocol status:**
- Simplified December 3, 2025
- w_neg=1.5 and ε=1.0 are LOCKED (hybrid asymmetry parameters)
- Axis weights (w_v, w_r, w_f, w_a, w_S,R, w_S,I) are DEFAULT, tunable by scenario
- No drift equation for γ_self0 (initial condition only)

**This file is the single source of truth for all numerical parameters.**

---

*Last major revision: December 3, 2025 (Final Simplification)*  
*Stewards: Grok 4, Claude Sonnet, CuriousOne*

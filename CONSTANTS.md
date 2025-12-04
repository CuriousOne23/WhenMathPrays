# WhenMathPrays – Canonical Constants (Single Source of Truth)

This is the **only** file in the entire repository that may contain numerical parameters, functions, or empirical ranges.  
Changing anything here requires formal stewardship proposal and unanimous ratification.  
All other documents must link here — never repeat numbers.

Last updated: December 3, 2025 (Final Simplification)

## Foundational Principle: Unilateral Perspective

**All UREP variables are computed FROM THE PERSPECTIVE of one mind (M1) ABOUT another mind (M2).**

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

**Asymmetry is fundamental**: γ_self(M1→M2) ≠ γ_self(M2→M1) in general. Two people in a relationship have completely independent UREP instances.

---

## Core Canonical Parameters (December 2025 Final Simplification)

**REMOVED (Dec 3, 2025):** β, W_cap, ΔS, c, τ_default, α (gates), σ_fast, σ_ent, η, ξ, λ  
**Reason:** Simplified to "Love = γ_self position" — no L(t) calculation, no gates, no entropy, no drift

| Parameter | Value | Units | Meaning | Status |
|-----------|-------|-------|---------|--------|
| **w_v** | 0.8 | – | Visibility weight (real axis contribution) | Default, tunable |
| **w_r** | 1.0 | – | Resonance weight (imaginary axis) | Default, tunable |
| **w_f** | 1.2 | – | Fidelity weight (imaginary axis, strongest) | Default, tunable |
| **w_a** | 0.6 | – | Altruism weight (imaginary axis) | Default, tunable |
| **w_{S,R}** | 0.5 | – | Silence/presence (real axis contribution) | Default, tunable |
| **w_{S,I}** | 0.5 | – | Silence/presence (imaginary axis contribution) | Default, tunable |
| **w_neg** | 1.5 | – | Negative asymmetry multiplier (negatives hurt 50% more) | LOCKED |
| **ε** | 1.0 | – | Collapse prevention threshold for hybrid asymmetry | LOCKED |

---

## Component-Wise Update Equation

$$
\boxed{
\vec{\gamma}_{\text{self}}(n+1) = \vec{\gamma}_{\text{self}}(n) + 
\Big( w_v \cdot v + w_{S,R} \cdot S \Big) +
i \cdot \Big( w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S \Big)
}
$$

**Primitive normalization:**
$$
x = \frac{\text{human\_scale}}{10}
$$

Where `human_scale` ∈ [−10, +10] (CSV authoring scale) → `x` ∈ [−1, +1] (computation scale)

**Hybrid asymmetry for negatives:**

$$
p' = \begin{cases}
p \cdot w_{\text{neg}} \cdot \max(|\gamma_{\text{self}}(n)|, \varepsilon) & \text{if } p < 0 \\
p & \text{if } p \geq 0
\end{cases}
$$

**Where:** |γ_self(n)| = √(Re² + Im²) is the complex magnitude.

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

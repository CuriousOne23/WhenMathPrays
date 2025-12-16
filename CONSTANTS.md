# WhenMathPrays – Canonical Constants (Single Source of Truth)

This is the **only** file in the entire repository that may contain numerical parameters, functions, or empirical ranges.  
Changing anything here requires formal stewardship proposal and unanimous ratification.  
All other documents must link here — never repeat numbers.

Last updated: December 2025 (Rev 3.4: Constant-Force Entropy Model)

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
| **S(t)** | M1's perception | Shared Breath as FELT BY M1 (M2 may disagree) |
| **γ_self0** | M1's baseline | Initial condition at n=0 (temperament/history anchor) |

**Critical distinction**: 
- Primitives {v,r,f,a,S} measure M1's **desire/action toward M2**, NOT M1's character
- High primitives = M1 engaging strongly with M2 (showing up, connecting)
- Low primitives = M1 withdrawing from M2 (hiding, disconnecting)
- **Love = γ_self(n) position** (no separate L(t) calculation)

**Asymmetry is fundamental**: γ_self(M1→M2) ≠ γ_self(M2→M1) in general. Two people in a relationship have completely independent GRP instances.

---

## Core Canonical Parameters (Rev 3.4: December 2025)

**Rev 3.4 Changes (Constant-force entropy for timeline independence):**
- **ERROR IN REV 3.3 CORRECTED**: Proportional-to-distance force caused timeline-length accumulation bug
- **Constant-force entropy**: Uses sign() function for force direction only, not magnitude
- **Timeline-independent drift**: Same entropy effect per unit time regardless of scenario length
- **Real axis target recalibrated**: -10.0 (was -150.0 in Rev 3.3 - too strong for new physics)
- **Imaginary axis target**: 0 (Neutral affect) - unchanged
- **Formula**: entropy_pull = ΔS_real × Δt × sign(real_target - real_current) + i × ΔS_imag × Δt × sign(imag_target - imag_current)
- **Fidelity asymmetry unchanged** from Rev 3.2 (Im-only depth scaling)
- **Axis-independent decay rates preserved** from Rev 3.3 (ΔS_real, ΔS_imag)

| Parameter | Value | Units | Meaning | Status |
|-----------|-------|-------|---------|--------|
| **w_v** | 0.8 | – | Visibility weight (real axis contribution) | Default, tunable |
| **w_r** | 1.0 | – | Resonance weight (imaginary axis) | Default, tunable |
| **w_f** | 1.2 | – | Positive fidelity weight (imaginary axis) | Default, tunable |
| **fidelity_scaling_factor** | 0.12 | – | Negative fidelity depth scaling coefficient | LOCKED |
| **fidelity_epsilon (ε)** | 5.0 | – | Collapse prevention floor for Im depth | LOCKED |
| **w_a** | 0.6 | – | Altruism weight (imaginary axis) | Default, tunable |
| **w_{S,R}** | 0.5 | – | Shared Breath (real axis contribution) | Default, tunable |
| **w__real** (delS_real) | 0.02 | time⁻¹ | Real axis entropy decay rate (toward Ego) | Default, tunable |
| **ΔS_imag** (delS_imag) | 0.02 | time⁻¹ | Imaginary axis entropy decay rate (toward neutral) | Default, tunable |
| **entropy_real_target** | -150.0 | – | Real axis entropy target (gentle Ego drift) | Default, tunable |
| **entropy_imag_target** | 0.0 | – | Imaginary axis entropy target (neutral affect/apathy) | Default, tunable |
| **entropy_per_event** | False | – | Entropy mode: False=per time unit (default), True=per event | Default, tunable |

**Removed in Rev 3.2:** w_f_neg (fixed 25×) — replaced with Im-only depth scaling  
**Removed in Rev 3.3:** γ_attractor (single point), ΔS (unified rate) — replaced with axis-independent targets and rates
**Removed in Rev 3.2:** w_f_neg (fixed 25×) — replaced with Im-only depth scaling

---

## Component-Wise Update Equation (Rev 3.2)

$$
\boxed{
\vec{\ga_{\text{real}} \cdot \Delta t \cdot (\text{real}_{\text{target}} - \text{Re}[\vec{\gamma}_{\text{self}}(n)]) +
i \cdot \Delta S_{\text{imag}} \cdot \Delta t \cdot (\text{imag}_{\text{target}} - \text{Im}[\vec{\gamma}_{\text{self}}(n)])
}
$$

**Entropy drift (Rev 3.3: Axis-independent decay):** Relationships naturally decay along each axis independently without maintenance.
- **ΔS_real = 0.02** (default): Real axis decay rate per time unit (toward Ego)
- **ΔS_imag = 0.02** (default): Imaginary axis decay rate per time unit (toward neutral)
- **entropy_real_target = -150.0** (default): Real axis target (deep Ego/isolation)
- **entropy_imag_target = 0.0** (default): Imaginary axis target (neutral affect/apathy)
- **Δt**: Time elapsed between events (in days/weeks/months per CSV time_unit)
- **entropy_per_event=False** (default): Drift scales with time (realistic decay)
- **entropy_per_event=True** (override): Fixed ΔS magnitude per event regardless of time spacing
- Default effect: 
  - **Real axis**: We-ness (positive real) decays toward Ego (negative real), approaching -150
  - **Imaginary axis**: Love/Hate decays toward neutral (zero imaginary), emotional numbness
- Configurable targets enable scenario-specific entropy modeling:
  - **Hate-driven scenarios** (imag_target = -100): Emotional decay toward hatred instead of apathy
  - **Ego-recovery** (real_target = -50): Less extreme isolation endpoint
  - **Different decay rates** allow modeling different relationship dimensions (e.g., fast emotional numbing, slow ego drift)
- To maintain or grow Love/We requires continuous positive primitives to overcome entropy
- **Physics advantage**: Axis independence eliminates ratio paradoxes (increasing decay on both axes was previously increasing slopes instead of flattening them)
  - **Q3 despair** (γ_attractor = -8-5j): Isolated ego sinking into enmity
  - **Default deep ego** (γ_attractor = -150+0j): Natural relationship decay pulls toward profound isolation
- To maintain or grow Love/We requires continuous positive primitives to overcome entropy

**Primitive normalization:**

$$
x = \frac{\text{human-scale}}{10}
$$

Where `human_scale` ∈ [−10, +10] (CSV authoring scale) → `x` ∈ [−1, +1] (computation scale)

**Im-only depth-scaled fidelity asymmetry (Rev 3.2):**

$$
f' = \begin{cases}
f \cdot (0.12 \cdot \text{max}(|\text{Im}|, 5.0)) & \text{if } f < 0 \\
w_f \cdot f & \text{if } f \geq 0
\end{cases}
$$

**Where:** 
- Im = imaginary component of γ_self (love/hate axis)
- 0.12 = scaling factor (negatives scale with love depth)
- 5.0 = ε (collapse prevention floor, even at origin betrayal stings)
- w_f = 1.2 (positive healing rate)

**Key behaviors:**
- **At origin (0i)**: f=-1 → -0.6i, f=-10 → -6i (minimum sting)
- **Early dating (20i)**: f=-1 → -2.4i, f=-10 → -24i (fragile)
- **Deep love (150i)**: f=-1 → -18i, f=-10 → -180i (can reach battlefield)
- **Saint/Hachikō peak (250i)**: f=-1 → -30i, f=-10 → -300i (full range)
- **Psychology**: "The deeper the love, the more betrayal can scar" — but only using Im (love depth), not Ego/We coupling

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

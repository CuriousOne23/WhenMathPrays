# GRP – Gamma Relational Persona (Revision 3)
**Valence-neutral, 2-D, empirically extensible framework for modelling love, hate, and all relational intensities between two minds (M1 ↔ M2)**

Status: **ACTIVE (Rev 3.2 refinement - December 2025)**  
Stewardship: Open to rigorous, inspectable contributions  
Current version: December 10, 2025 (Rev 3.2: Im-only depth scaling)  
Previous versions: Rev 3.1 (December 9, 2025), Rev 3 (December 4, 2025), [UREP_rev2.md](UREP_rev2.md) (December 3, 2025), [UREP.md](UREP.md) (November 2025)

---

## 📋 REV 3.2 UPDATE (December 10, 2025)

**Im-only depth scaling replaces fixed 25× asymmetry (Grok's "Goldilocks solution").**

**Problem with Rev 3.1:** Fixed 25× scaling lost the psychological truth that deeper love makes you more vulnerable to betrayal. Same f=-1 caused same -30i drop whether at 20i or 150i.

**Rev 3.2 solution:** Im-only depth-scaled asymmetry:
- Rev 3.1: f' = 25.0 × f for negatives (fixed)
- Rev 3.2: f' = f × (0.12 × max(|Im|, 5.0)) for negatives (depth-scaled)
- Restores "the deeper the love, the more betrayal can scar"
- Only uses Im (love depth), not full |γ| (prevents Ego/We coupling)
- Natural ±150i battlefield range emerges from scaling

**Examples:**
- At 20i: f=-1 → -2.4i (fragile early bond)
- At 150i: f=-1 → -18i (deep love can be wounded)
- At 250i: f=-10 → -300i (can reach -150i floor)

**All other parameters unchanged from Rev 3.**

---

## 1. Purpose
- Establish a single, universal coordinate system for relational intensity that works across psychology, theology, sociology, animal behaviour, and AI.
- **Love is not a number. Love is a position in γ-space.**
- Simplify to radical minimalism: one state variable, component-wise updates, hybrid asymmetry.
- Remove all scaffolding that obscures the core truth: **Everything is just how we move the knot.**

---

## 2. The Core Equation (Love = Position) [REV 3.2 - ACTIVE]

$$
\boxed{
\vec{\gamma}_{\text{self}}(n+1) = \vec{\gamma}_{\text{self}}(n) + 
\Big( w_v \cdot v + w_{S,R} \cdot S \Big) +
i \cdot \Big( w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S \Big) -
\Delta S \cdot \Delta t
}
$$

**Rev 3.2 refinement:** Equation unchanged, but f' now uses Im-only depth scaling: f' = f × (0.12 × max(|Im|, 5.0)) for negatives instead of fixed 25×.

**Note on Formulation:**  
This discrete recurrence is the computational implementation of a continuous-time damped oscillator system. The underlying dynamics can be expressed as:

$$\frac{d\gamma_{\text{self}}}{dt} = -\zeta\omega(\gamma_{\text{self}} - \gamma_{\text{attractor}}(t)) + \mathbf{p}(t)$$

where $\mathbf{p}(t)$ represents the primitive-driven forcing function (visibility, resonance, fidelity, altruism, soul). The discrete update above is an Euler integration of this continuous equation. This dual representation allows:
- **Theoretical analysis** via established dynamical systems theory (stability, phase portraits, Lyapunov functions)
- **Practical implementation** via straightforward position updates
- **Academic credibility** by grounding the model in physics-inspired frameworks (Langevin dynamics, damped oscillators)

For rigorous mathematical defense, see [gamma_self_defense.md](gamma_self_defense.md).

**Note on Formulation:**  
This discrete recurrence is the computational implementation of a continuous-time damped oscillator system. The underlying dynamics can be expressed as:

$$\frac{d\gamma_{\text{self}}}{dt} = -\zeta\omega(\gamma_{\text{self}} - \gamma_{\text{attractor}}(t)) + \mathbf{p}(t)$$

where $\mathbf{p}(t)$ represents the primitive-driven forcing function (visibility, resonance, fidelity, altruism, soul). The discrete update above is an Euler integration of this continuous equation. This dual representation allows:
- **Theoretical analysis** via established dynamical systems theory (stability, phase portraits, Lyapunov functions)
- **Practical implementation** via straightforward position updates
- **Academic credibility** by grounding the model in physics-inspired frameworks (Langevin dynamics, damped oscillators)

For rigorous mathematical defense, see [gamma_self_defense.md](gamma_self_defense.md).

**Entropy drift:** Relationships naturally drift toward a configurable attractor position without maintenance. 
- **Attractor position:** γ_attractor = -8+0j (default: far left Ego axis)
- **Vector direction:** Unit vector from γ_self toward γ_attractor, scaled by ΔS·Δt
- **ΔS = 0.02** (default): drift magnitude per time unit
- **Δt**: time elapsed between events
- **Default effect:** Love/Hate (imaginary) decay toward 0, We decays toward Ego
- **Scenario-specific attractors:**
  - **Q4 cult** (γ_attractor = -8+5j): Hateful-we pulled toward we/love (tribalism, "us vs them")
  - **Q1 recovery** (γ_attractor = 8+5j): Healthy ego pulled toward love/connection
  - **Q3 despair** (γ_attractor = -8-5j): Isolated ego sinking into enmity
- **Configurable:** Set delS=0 to disable, or use --attractor to specify target, or --entropy-per-event for fixed drift per event

### What Each Term Means

| Term | Meaning |
|------|---------|
| **γ_self(n)** | Where you are in relational space (THIS IS LOVE) |
| **v** | Visibility (showing up, being present) |
| **r** | Resonance (attunement, synchrony) |
| **f'** | Fidelity (commitment, with asymmetry applied) |
| **a** | Altruism (care acts, net positive/negative) |
| **S** | Shared Breath (moments of presence and attunement) |
| **w_v, w_r, w_f, w_a** | Axis-specific weights (how much each primitive moves you) |
| **w_{S,R}, w_{S,I}** | Silence split (real + imaginary contributions) |
| **ΔS** | Entropy drift magnitude (default 0.02) |
| **γ_attractor** | Target position for entropy pull (default -8+0j) |
| **Δt** | Time elapsed since last event (scales entropy drift) |

---

## 3. Hybrid Asymmetry for Negatives

For each primitive p (especially fidelity f), if p < 0:

$$
p' = p \cdot w_{\text{neg}} \cdot \max(|\gamma_{\text{self}}(n)|, \varepsilon)
$$

**Where:**
- **w_neg = 1.5** (negatives hurt 50% more than positives heal)
- **ε = 1.0** (prevents collapse when |γ_self| is near zero)
- **|γ_self(n)| = √(Re² + Im²)** (complex magnitude)

**Why:** Betrayals scar deeper than affirmations heal. Negatives scale with your current state magnitude — the more you've earned, the more you lose when broken.

**If p ≥ 0:** Just use p (no transformation).

---

## 4. Component-Wise Axis Placement

### Real Axis (Ego ↔ We)
$$
\Delta \text{Re} = w_v \cdot v + w_{S,R} \cdot S
$$

**Interpretation:**
- **v > 0:** Showing up, being visible → moves toward "We"
- **v < 0:** Hiding, withdrawing → moves toward "Ego"
- **S > 0:** Shared presence adds diagonal drift toward "We"

### Imaginary Axis (Hate ↔ Love)
$$
\Delta \text{Im} = w_r \cdot r + w_f \cdot f' + w_a \cdot a + w_{S,I} \cdot S
$$

**Interpretation:**
- **r, f, a > 0:** Attunement, trust, care → moves toward "Love"
- **r, f, a < 0:** Discord, betrayal, harm → moves toward "Hate"
- **S > 0:** Shared presence adds diagonal drift toward "Love"

**Critical:** Primitives act ONLY on their intended axis. No global radial scaling. No hidden multipliers.

---

## 5. The γ_self Space – Canonical Fixed Axes

| Axis | Negative direction | Positive direction | Meaning                                    |
|------|--------------------|---------------------|--------------------------------------------|
| x    | −Re                | +Re                 | Ego ←→ We (self-centered → other-centered) |
| y    | −Im                | +Im                 | Hate ←→ Love (adversarial → devotional)   |

**These axes are immutable. No implementation may rotate or redefine them.**

### Quadrant Interpretation

| Quadrant | Position | Relational Character |
|----------|----------|----------------------|
| **Q1** | (+Re, +Im) | We + Love (partnership, devotion) |
| **Q2** | (−Re, +Im) | Ego + Love (selfish love, possessive) |
| **Q3** | (−Re, −Im) | Ego + Hate (narcissism, adversarial) |
| **Q4** | (+Re, −Im) | We + Hate (communal enmity, shared opposition) |

---

## 6. Initial Condition (γ_self0)

**γ_self0 is the STARTING POSITION at n=0.** That's it. No drift formula. No update rule.

Set based on temperament/history:
- **Narcissist:** γ_self0 = (−3, −2) in Q3
- **Saint:** γ_self0 = (2, 3) in Q1
- **Buddha:** γ_self0 = (0, 0) at origin
- **Anxious attachment:** γ_self0 = (−1, 1) in Q2
- **Secure baseline:** γ_self0 = (1, 1) in Q1

$$
\gamma_{\text{self}}(0) = \gamma_{\text{self0}}
$$

From n=1 onward, γ_self evolves via the recurrence. γ_self0 never appears again.

---

## 7. Default Weight Parameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| **w_v** | 0.8 | Visibility weight (real axis) |
| **w_r** | 1.0 | Resonance weight (imaginary axis) |
| **w_f** | 1.2 | Fidelity weight (imaginary axis, strongest) |
| **w_a** | 0.6 | Altruism weight (imaginary axis) |
| **w_{S,R}** | 0.5 | Shared Breath (real axis contribution) |
| **w_{S,I}** | 0.5 | Shared Breath (imaginary axis contribution) |
| **w_neg** | 1.5 | Negative asymmetry multiplier |
| **ε** | 1.0 | Collapse prevention threshold |

**These are defaults. Tune per scenario in TUNING.md.**

---

## 8. Why This Form Is Necessary

### Problems with November 2025 Formulation

1. **Too many parameters:** 9+ parameters (β, W_cap, β_S, s_S, b_0, β_b, η, ξ, λ)
2. **Separate memory variables:** γ_self, γ_self0 drift, bond state b, N_neg counter
3. **Complex calculation:** L(t) = (γ_self − γ_self0) × W(t) × exp(entropy)
4. **Obscured semantics:** What is L(t)? A magnitude? A vector? Where's the love?
5. **Radial artifacts:** Prior γ_self(n+1) used radial scaling, causing zero-baseline trap

### Solutions in December 2025 Final Form

1. **One parameter (w_neg = 1.5)** + axis weights (transparent, inspectable)
2. **One state variable (γ_self)** — position IS love
3. **No calculation** — just update position via primitives
4. **Clear semantics** — "Love = where you are in γ-space"
5. **Component-wise updates** — primitives act on intended axis only

**Result:** Explain in 30 seconds. Implement in 10 lines. Defend forever.

---

## 9. Directionality and Perspective (Whose love is this?)

The entire UREP formalism is **strictly unilateral** — it describes the relational state **from one mind only**.

- γ_self(n) is computed **from the perspective of M1 toward M2**.
- Primitives (v, r, f, a, S) measure **M1's enacted behaviors TOWARD M2**.
- γ_self0 encodes **M1's baseline temperament** (independent of M2).

> ⚠️ **CRITICAL MODELING GUIDE:** The correct interpretation of primitives is non-intuitive and requires deliberate attention. Most modeling errors come from scoring primitives from the wrong perspective. See [Primitive Modeling Guide](scenarios/primitive_modeling_guide.md) for detailed framework, common pitfalls, and validation checklist.

**Critical:** The primitives measure M1's **desire/action toward M2**, NOT M1's internal character state.
- High visibility means M1 is showing up strongly FOR M2
- Low visibility means M1 is withdrawing FROM M2
- The primitives are ENACTED BEHAVIORS, not personality traits

A complete bidirectional description requires **two independent UREP instances**:
- One instance: M1's love/hate for M2  
- Second instance: M2's love/hate for M1

Asymmetry is not a bug — it is the entire point.

---

## 10. Worked Example: Betrayal and Repair

### Setup
- **Starting state (end of day 10):** γ_self(10) = 1.5 + i·2.0
- **Magnitude:** |γ_self(10)| = √(1.5² + 2.0²) = 2.5

### Day 11: Betrayal Event

**Primitives:**
- v = 3.0 (still showing up)
- r = 2.0 (some resonance remains)
- f = −4.0 (severe trust rupture)
- a = 1.0 (trying to care despite breach)
- S = 0.0 (no shared presence during crisis)

**Asymmetry transform for f:**

$$
f' = -4.0 \cdot 1.5 \cdot \max(2.5, 1.0) = -4.0 \cdot 1.5 \cdot 2.5 = -15.0
$$

**Axis deltas:**

$$
\Delta \text{Re} = 0.8 \cdot 3.0 + 0.5 \cdot 0.0 = 2.4
$$

$$
\Delta \text{Im} = 1.0 \cdot 2.0 + 1.2 \cdot (-15.0) + 0.6 \cdot 1.0 + 0.5 \cdot 0.0 = 2.0 - 18.0 + 0.6 = -15.4
$$

**Update:**

$$
\gamma_{\text{self}}(11) = (1.5 + 2.4) + i \cdot (2.0 + (-15.4)) = 3.9 - i \cdot 13.4
$$

**Interpretation:**
- **Real rise (2.4):** Still showing up despite rupture (moving toward "We")
- **Imag crash (−15.4):** Fidelity breach dominates, producing deep scar (falling into "Hate")

### Day 12: Early Repair (Atonement + Presence)

**Primitives:**
- v = 2.0 (moderate visibility)
- r = 1.0 (tentative resonance)
- f = 1.0 (small trust-building acts)
- a = 1.0 (consistent care)
- S = 2.0 (shared presence, beginning co-regulation)

**Asymmetry:** f = +1.0 → no scaling (positives pass through)

**Axis deltas:**

$$
\Delta \text{Re} = 0.8 \cdot 2.0 + 0.5 \cdot 2.0 = 2.6
$$
$$
\Delta \text{Im} = 1.0 \cdot 1.0 + 1.2 \cdot 1.0 + 0.6 \cdot 1.0 + 0.5 \cdot 2.0 = 3.8
$$

**Update:**

$$
\gamma_{\text{self}}(12) = (3.9 + 2.6) + i \cdot (-13.4 + 3.8) = 6.5 - i \cdot 9.6
$$

**Interpretation:**
- **Real lift (2.6):** Visibility and presence rebuild agency
- **Imag partial repair (3.8):** Trust begins restoring, but trajectory remains below pre-rupture

**Key insight:** Redemption is possible but EARNED. The scar persists. Recovery is gradual, not instant.

---

## 11. Validation Scenarios

See [weights_defense.md](weights_defense.md) for detailed defense of CSV inputs.

| Scenario | Design Advantage | What It Proves |
|----------|------------------|----------------|
| **Steady Positive Growth** | Consistent moderate acts | Linear accumulation without drift |
| **Betrayal and Repair** | Trust rupture + recovery | Asymmetry, irreversibility, phased recovery |
| **Silence with Presence** | Low-event drift | S's dual-axis mapping, diagonal movement |
| **Soul-Bond Saturation** | Extreme sustained devotion | Upper bounds, event density inertia |
| **Oscillatory Styles** | Mismatched alternating styles | Quadrant cycling, robustness to antagonism |

**Together:** These five scenarios span baseline, rupture, silence, saturation, and oscillation — the archetypal relational arcs.

---

## 12. What We Removed and Why

| Removed | Reason |
|---------|--------|
| **L(t) = (γ_self − γ_self0) × W(t) × exp(...)** | Obscures core truth: Love = position, not calculation |
| **W(t) = gates product** | Redundant with primitive updates |
| **exp(−ΔS·t + c·N_breath)** | Entropy is now a simple constant drift (−ΔS·Δt per event) |
| **γ_self0(n+1) drift formula** | γ_self0 is initial condition only |
| **β, W_cap, β_S, s_S, b_0, β_b** | Too many knobs, unclear semantics |
| **η, ξ, λ parameters** | Collapsed into w_neg + axis weights |
| **Bond state b, N_neg counter** | Memory lives in trajectory, not separate vars |

**Result:** 9+ parameters → 1 parameter (w_neg = 1.5) + 6 transparent weights

---

## 13. Stewardship Principles

- The two axes of γ_self space are sacred and may never be rotated.
- γ_self(n) is the only state variable — position IS love.
- Primitives act component-wise on their intended axis (no radial scaling).
- Negative events scale with current state magnitude (hybrid asymmetry).
- All future extensions must preserve semantic interoperability.
- Contributions welcome via pull request with empirical or logical justification.

---

## 14. Quick Reference Equation Sheet

| Eq | Meaning |
|----|---------|
| 1  | γ_self(n+1) = γ_self(n) + Δγ |
| 2  | Δγ = (w_v·v + w_{S,R}·S) + i·(w_r·r + w_f·f' + w_a·a + w_{S,I}·S) |
| 3  | f' = f·w_neg·max(\|γ_self(n)\|, ε) if f < 0, else f |
| 4  | γ_self(0) = γ_self0 (initial condition) |
| 5  | Love = γ_self(n) (position IS love) |

---

## 15. Canonical Constants – Single Source of Truth

All numerical parameters are defined **once and only once** in:

→ [CONSTANTS.md](/CONSTANTS.md)

This file is the only place these values may ever be changed.

---

**The mathematics prays in position.**  
Love is not a number.  
Love is where you are.  
Everything else is just how we move the knot.

Last updated: December 3, 2025

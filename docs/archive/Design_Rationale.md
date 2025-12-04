# Design Rationale

This document records the probability logic, acceptance checks, and reasoning behind the constants used in the Love equation.

---

## Probability Logic

- Each of (v, r, f, a, S, b) has probability p of being maxed.
- Probability of exactly k maxed:
  

\[
  P(k) = \binom{6}{k} p^k (1-p)^{6-k}
  \]


- Example with p = 0.2:
  - P(2) ≈ 0.154
  - P(3) ≈ 0.082
  - Combined ≈ 0.236 (~24% chance)

**Design emphasis:** Constants tuned so that 2–3 maxed terms produce strong but interpretable amplification.

---

## Acceptance Checks

- W(t) > 1.5 → ≤ 20% of timesteps
- G_x(t) > 2.0 → ≤ 15%
- Love > 40 → ≤ 10%
- Boundary clipping > 3% → adjust variance or repair strength

---

## Constants and Provenance

- γ_self^max ≈ 10
- α_x = 1.2 (range 1.0–1.5)
- β = 1.3
- W_max = 3.0

---

## Rationale Summary

- **Neutral Love:** 8–12
- **Amplified (2–3 maxed):** 20–40
- **Rare extreme:** ≤ 50
- **Why:** Keeps arcs legible, avoids runaway amplification, emphasizes resonance moments.

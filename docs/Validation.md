# Validation Guide

This document defines acceptance checks and validation procedures for the Love equation simulations.

---

## Acceptance Checks

- **Duty cycle thresholds**
  - W(t) > 1.5 → ≤ 20% of timesteps
  - G_x(t) > 2.0 → ≤ 15%
  - Love > 40 → ≤ 10%

- **Boundary clipping**
  - x_j(t) clipping ≤ 3% of samples
  - If exceeded, reduce variance or increase repair strength

---

## Validation Procedures

1. Run canonical simulation (Scenario B).
2. Log distributions of W(t), G_x(t), Love.
3. Compare against expected ranges:
   - Neutral Love: 8–12
   - Amplified (2–3 maxed): 20–40
   - Rare extreme: ≤ 50
4. Flag anomalies:
   - Runaway amplification
   - Flatlining near 1.0
   - Excessive clipping

---

## Scenario Comparability

- Raw runs remain unnormalized.
- For cross-scenario comparison, report z-scored Love.
- Always preserve provenance headers:
  - γ_self^max
  - α_x
  - β
  - W_max

---

## Reporting

- CSV metadata must include constants and acceptance checks.
- Validation logs should record:
  - Duty cycle percentages
  - Clipping rates
  - Love distribution summary
- Mark each run as **PASS** or **FAIL** based on acceptance criteria.

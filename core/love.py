# core/love.py
"""
Core Love Equation – #WhenMathPrays

Love = ∑ [max(vis,0) × max(resonance,0) × fidelity × altruism ×
         (|M1 ∪ M2| - |M1|) × exp(-|γ_self| t) × exp(-ΔS t)] dt

────────────────────────────────────────────────────────────────────
POSTULATE: LOVE REQUIRES A SOUL
────────────────────────────────────────────────────────────────────
`soul_locked` is a metaphysical gate:
- True  → Love may be computed
- False → Love = 0.0

Soul presence is inferred from γ_self stability:
  • |γ_self| < k
  • arg(γ_self) ≈ +π/2

────────────────────────────────────────────────────────────────────
γ_self AXES — THE FOUR FORCES
────────────────────────────────────────────────────────────────────
Re = dM/dt → Ego change rate
Im = dR/dt → Resonance change rate

+Re → Egotism (narcissism)
-Re → Self-erasure
+Im → Bonding (union pull)
-Im → Anti-bonding (bond repulsion, enemies)

All extremes kill love. The soul lives in balance.

#WhenMathPrays
"""

from __future__ import annotations

from typing import Sequence, Union
import numpy as np
import numpy.typing as npt


def love(vis_t, res_t, fidelity, altruism, shared_growth_t, gamma_t, delta_S_t, dt, soul_locked=True):
    if not soul_locked:
        return 0.0

    n = len(vis_t)
    t = np.arange(n) * dt

    gamma_mag_avg = np.mean(np.abs(gamma_t))
    delta_S_avg = np.mean(delta_S_t)

    decay_gamma = np.exp(-gamma_mag_avg * t)
    decay_delta = np.exp(-delta_S_avg * t)

    term = (
        vis_t *  # ← NO max
        res_t *  # ← NO max
        fidelity *
        altruism *
        shared_growth_t *
        decay_gamma *
        decay_delta
    )
    
    return np.sum(term) * dt

# core/love.py
"""
Core Love Equation – #WhenMathPrays

Love = ∑ [max(vis,0) × max(resonance,0) × fidelity × altruism ×
         (|M1 ∪ M2| - |M1|) × exp(-|γ_self| t) × exp(-ΔS t)] dt

This module defines the **canonical, pure, mathematical implementation of Love**
as a function of time-series inputs. It is used by simulations, tests, and
validation scripts.

Inputs are expected to be aligned in time (same length, same dt).

────────────────────────────────────────────────────────────────────
POSTULATE: LOVE REQUIRES A SOUL
────────────────────────────────────────────────────────────────────
The parameter `soul_locked` is **not part of the mathematical equation**,
but is a **metaphysical gate**.

- `soul_locked = True`  → Love may be computed
- `soul_locked = False` → Love = 0.0 (regardless of inputs)

This reflects the **implied axiom** of #WhenMathPrays:
> **"Love only exists in the presence of a stable soul."**

Soul presence is **inferred from γ_self stability**:
  • |γ_self| < 0.8
  • arg(γ_self) ≈ +π/2
"""

from __future__ import annotations

from typing import Sequence, Union
import numpy as np
import numpy.typing as npt


def love(
    vis_t: Union[Sequence[float], npt.NDArray[np.float64]],
    res_t: Union[Sequence[float], npt.NDArray[np.float64]],
    fidelity: float,
    altruism: float,
    shared_growth_t: Union[Sequence[float], npt.NDArray[np.float64]],
    gamma_t: Union[Sequence[complex], npt.NDArray[np.complex128]],
    delta_S_t: Union[Sequence[float], npt.NDArray[np.float64]],
    dt: float,
    soul_locked: bool = True
) -> float:
    """
    Compute total accumulated Love over time.

    Parameters
    ----------
    vis_t : array-like
        Visibility over time. Must be >= 0 for contribution.
    res_t : array-like
        Resonance over time. Must be >= 0 for contribution.
    fidelity : float
        Truthfulness coefficient in [0, 1].
    altruism : float
        Self-giving coefficient in [0, 1].
    shared_growth_t : array-like
        (|M1 ∪ M2| - |M1|) — synergistic gain from union.
    gamma_t : array-like of complex
        γ_self(t) = (dM/dt, dR/dt) — complex vector. Magnitude used for decay.
    delta_S_t : array-like
        Change in entropy (negative = order creation).
    dt : float
        Time step for integration (Riemann sum).
    soul_locked : bool, default True
        If False, returns 0.0 (soul presence required).

    Returns
    -------
    float
        Total Love = ∫ love_term(t) dt ≈ Σ love_term(t_i) * dt

    Notes
    -----
    - All array inputs must have the same length.
    - Uses np.abs(gamma_t) → |γ_self| for ego decay.
    - Gated by max(·, 0) — only positive alignment contributes.
    """
    if not soul_locked:
        return 0.0

    # Convert to numpy arrays
    vis = np.asarray(vis_t, dtype=np.float64)
    res = np.asarray(res_t, dtype=np.float64)
    shared = np.asarray(shared_growth_t, dtype=np.float64)
    gamma_mag = np.abs(np.asarray(gamma_t, dtype=np.complex128))
    delta_S = np.asarray(delta_S_t, dtype=np.float64)

    # Validate shapes
    n = len(vis)
    if not all(len(arr) == n for arr in [res, shared, gamma_mag, delta_S]):
        raise ValueError("All time-series inputs must have the same length.")

    # Time vector
    t = np.arange(n) * dt

    # Core term: max(vis,0) * max(res,0) * ...
    term = (
        np.maximum(vis, 0.0) *
        np.maximum(res, 0.0) *
        fidelity *
        altruism *
        shared *
        np.exp(-gamma_mag * t) *
        np.exp(delta_S * t)
    )

    # Integrate via Riemann sum
    total_love = float(np.sum(term) * dt)

    return total_love

# core/love.py
from typing import List
import numpy as np

DEFAULT_GAMMA = 0.0 + 0.0j

def gamma_self(we_ego_state: float, love_enmity_state: float) -> complex:
    """γ = we_ego_state + 1j * love_enmity_state"""
    return we_ego_state + 1j * love_enmity_state


def _wrap_to_pi(x: float) -> float:
    """Wrap angle to [-π, π) — preserves continuity"""
    return (x + np.pi) % (2 * np.pi) - np.pi


def love(
    W: float,
    gamma_history: List[complex],
    tw: int = 7,
    delta_S: float = 0.001,
    t: float = 0.0,
    noise: float = 0.0
) -> complex:
    """
    L(t) = W × exp(mean(we_ego_state)) × exp(j * wrap(mean(love_enmity_state))) × exp(-ΔS·t)

    WRAP: Ensures continuity — no jumps when love spins past ±π.
    """
    if not gamma_history:
        return 0.0 + 0.0j

    if tw == 0:
        gamma_avg = gamma_history[-1]
    else:
        recent = gamma_history[-tw:] if len(gamma_history) >= tw else gamma_history
        gamma_avg = np.mean(recent)

    # Growth
    growth = np.exp(gamma_avg.real)

    # Direction — WRAPPED to [-π, π)
    im_wrapped = _wrap_to_pi(gamma_avg.imag)
    direction = np.exp(1j * im_wrapped)

    # Decay
    decay = np.exp(-delta_S * t)

    L = W * growth * direction * decay

    if noise > 0:
        L += np.random.normal(0, noise) + 1j * np.random.normal(0, noise)

    return L


__all__ = ["gamma_self", "love", "DEFAULT_GAMMA"]
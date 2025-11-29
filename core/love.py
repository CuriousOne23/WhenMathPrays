# core/love.py
# WhenMathPrays – Universal Relational Expression Protocol (UREP)
# Final locked love magnitude function – November 2025 restoration
# L(t) = γ_self(t,τ) · W(t)
# with W(t) = product of G_x for v,r,f,a,b × min(β^k, 3.0) × G_S(S)
# and γ_self as Cartesian average of v(u) = (1 + m(u)) [cosθ(u), sinθ(u)]

from typing import List
import numpy as np
from typing import Tuple

DEFAULT_GAMMA = 0.0 + 0.0j

# Canonical constants (import from CONSTANTS.md logic – hardcoded here for self-contained execution)
BETA = 1.30
W_CAP = 3.0
DELTA_S = 0.010  # day⁻¹
C = 0.40
TAU_DEFAULT = 14  # days
ALPHA = 1.80  # gate gain

def gamma_self(ego_we_state: float, enmity_love_state: float) -> complex:
    """γ_self = ego_we_state + 1j * enmity_love_state
    Preserves compatibility with previous definitions – real = Ego/We, imag = Enmity/Love
    """
    return ego_we_state + 1j * enmity_love_state

def G_x(x: float, alpha: float = ALPHA) -> float:
    """Canonical gate function – locked form
    G_x(x) = 2x exp(α (x - 0.5)), x ∈ [0,1]
    """
    return 2 * x * np.exp(alpha * (x - 0.5))

def G_S(S: int, beta_S: float, s_S: float) -> float:
    """Shared-breath gate – locked form
    G_S(S) = 1 + β_S (1 - exp(-S / s_S))
    beta_S and s_S from empirical ranges in CONSTANTS.md
    """
    return 1 + beta_S * (1 - np.exp(-S / s_S))

def count_k(primitives: List[float], saturation_threshold: float = 0.98) -> int:
    """Resonance spike counter k(t): number of primitives ≥ 0.98"""
    return sum(1 for p in primitives if p >= saturation_threshold)

def W_t(primitives: Tuple[float, float, float, float, float], S: int, beta_S: float, s_S: float) -> float:
    """External enacted magnitude W(t) = product G_v G_r G_f G_a G_b × min(β^k, 3.0) × G_S(S)"""
    v, r, f, a, b = primitives
    G_primitives = G_x(v) * G_x(r) * G_x(f) * G_x(a) * G_x(b)
    k = count_k([v, r, f, a, b])
    resonance_spike = min(BETA ** k, W_CAP)
    g_s = G_S(S, beta_S, s_S)
    return G_primitives * resonance_spike * g_s

def love(
    primitives: Tuple[float, float, float, float, float],
    S: int,
    beta_S: float,
    s_S: float,
    gamma_history: List[complex],
    tau: int = TAU_DEFAULT,
    delta_S: float = DELTA_S,
    t: float = 0.0,
    noise: float = 0.0
) -> complex:
    """
    L(t) = γ_self(t,τ) · W(t) × exp(-ΔS t)
    - W(t) = product G_x(v,r,f,a,b) × min(β^k, 3.0) × G_S(S)
    - γ_self(t,τ) = Cartesian average of v(u) = (1 + m(u)) [cosθ(u), sinθ(u)] over [t-τ, t]
    - Preserves compatibility with previous scripts – gamma_history can be used as before
    """
    if not gamma_history:
        return 0.0 + 0.0j

    if tau == 0:
        gamma_avg = gamma_history[-1]
    else:
        recent = gamma_history[-tau:] if len(gamma_history) >= tau else gamma_history
        gamma_avg = np.mean(recent)

    W = W_t(primitives, S, beta_S, s_S)

    # Growth from real part (Ego/We)
    growth = np.exp(gamma_avg.real)

    # Direction from imag part (Enmity/Love) – wrapped to [-π, π)
    im_wrapped = (gamma_avg.imag + np.pi) % (2 * np.pi) - np.pi
    direction = np.exp(1j * im_wrapped)

    # Decay
    decay = np.exp(-delta_S * t)

    L = W * growth * direction * decay

    if noise > 0:
        L += np.random.normal(0, noise) + 1j * np.random.normal(0, noise)

    return L

__all__ = ["gamma_self", "love", "DEFAULT_GAMMA", "G_x", "G_S", "W_t"]
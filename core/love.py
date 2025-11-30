# core/love.py
# WhenMathPrays – Universal Relational Expression Protocol (UREP)
# Final locked love magnitude function – November 2025 restoration
# L(t) = γ_self(t,τ) · W(t)
# with W(t) = product of G_x for v,r,f,a × min(β^k, 3.0) × G_b(b)
# where b(t) = b_0 + beta_S * (1 - exp(-S/s_S)) accumulates bond from shared moments S
# and γ_self as complex average of v(u) = m(u) * [cosθ(u), i·sinθ(u)]

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

def gamma_self(ego_we_state: float = None, enmity_love_state: float = None,
               we_ego_state: float = None, love_enmity_state: float = None) -> complex:
    """γ_self compatibility wrapper.

    Accepts both the newer names `(ego_we_state, enmity_love_state)` and the
    older test-friendly names `(we_ego_state, love_enmity_state)`.

    Returns `real = ego/we`, `imag = enmity/love` as a complex number.
    """
    # Resolve ego/we (real part)
    if ego_we_state is None and we_ego_state is None:
        raise TypeError("gamma_self() missing required positional argument for ego/we state")
    real_part = ego_we_state if ego_we_state is not None else we_ego_state

    # Resolve enmity/love (imag part)
    if enmity_love_state is None and love_enmity_state is None:
        raise TypeError("gamma_self() missing required positional argument for enmity/love state")
    imag_part = enmity_love_state if enmity_love_state is not None else love_enmity_state

    return float(real_part) + 1j * float(imag_part)

def G_x(x: float, alpha: float = ALPHA) -> float:
    """Canonical gate function – locked form
    G_x(x) = 2x exp(α (x - 0.5)), x ∈ [0,1]
    """
    return 2 * x * np.exp(alpha * (x - 0.5))

def compute_b(S: int, b_0: float, beta_S: float, s_S: float) -> float:
    """Compute bond state from shared moments
    b(t) = b_0 + β_S (1 - exp(-S / s_S))
    
    Args:
        S: Cumulative shared meaningful moments (event counter)
        b_0: Initial bond condition (0 for strangers, >0 for existing relationships)
        beta_S: Maximum bond boost from shared moments
        s_S: Saturation scale for S → b transfer
    """
    return b_0 + beta_S * (1 - np.exp(-S / s_S))

def G_b(b: float, beta_b: float = 1.0) -> float:
    """Bond flux gate – exponential amplification
    G_b(b) = exp(β_b · b)
    
    Args:
        b: Bond state variable [0, ~1]
        beta_b: Bond amplification coefficient
    """
    return np.exp(beta_b * b)

def count_k(primitives: List[float], saturation_threshold: float = 0.98) -> int:
    """Resonance spike counter k(t): number of primitives ≥ 0.98"""
    return sum(1 for p in primitives if p >= saturation_threshold)

def W_t(primitives: Tuple[float, float, float, float], S: int, b_0: float, beta_S: float, s_S: float, beta_b: float = 1.0) -> float:
    """External enacted magnitude W(t) = product G_v G_r G_f G_a × min(β^k, 3.0) × G_b(b)
    
    Args:
        primitives: (v, r, f, a) - four fast primitives [0,1]
        S: Cumulative shared meaningful moments
        b_0: Initial bond condition
        beta_S: Shared breath → bond transfer parameter
        s_S: Saturation scale
        beta_b: Bond amplification coefficient
    """
    v, r, f, a = primitives
    G_primitives = G_x(v) * G_x(r) * G_x(f) * G_x(a)
    k = count_k([v, r, f, a])
    resonance_spike = min(BETA ** k, W_CAP)
    
    # Compute bond state from shared moments
    b = compute_b(S, b_0, beta_S, s_S)
    g_b = G_b(b, beta_b)
    
    return G_primitives * resonance_spike * g_b

def love(
    primitives: Tuple[float, float, float, float] = None,
    S: int = 0,
    b_0: float = 0.0,
    beta_S: float = 0.0,
    s_S: float = 1.0,
    beta_b: float = 1.0,
    gamma_history: List[complex] = None,
    tau: int = TAU_DEFAULT,
    delta_S: float = DELTA_S,
    t: float = 0.0,
    noise: float = 0.0,
    # Backwards-compatible aliases used by older tests/scripts
    W: float = None,
    tw: int = None,
) -> complex:
    """
    L(t) = γ_self(t,τ) · W(t) × exp(-ΔS t)
    - W(t) = product G_x(v,r,f,a) × min(β^k, 3.0) × G_b(b)
    - b(t) = b_0 + beta_S * (1 - exp(-S/s_S)) bond state from shared moments
    - γ_self(t,τ) = Complex average of v(u) = m(u) * e^(iθ) over [t-τ, t]
    - Preserves compatibility with previous scripts – gamma_history can be used as before
    """
    if gamma_history is None or len(gamma_history) == 0:
        return 0.0 + 0.0j

    # Support legacy `tw` keyword as alias for `tau`
    if tw is not None:
        tau_use = tw
    else:
        tau_use = tau

    if tau_use == 0:
        gamma_avg = gamma_history[-1]
    else:
        recent = gamma_history[-tau_use:] if len(gamma_history) >= tau_use else gamma_history
        gamma_avg = np.mean(recent)

    # If caller provided an explicit W (legacy tests), use it; otherwise compute
    # W from primitives.
    if W is not None:
        W_val = float(W)
    else:
        if primitives is None:
            raise TypeError("love() requires either `W` or `primitives` to compute W(t)")
        W_val = W_t(primitives, S, b_0, beta_S, s_S, beta_b)

    # Growth from real part (Ego/We)
    growth = np.exp(gamma_avg.real)

    # Direction from imag part (Enmity/Love) – wrapped to [-π, π)
    im_wrapped = (gamma_avg.imag + np.pi) % (2 * np.pi) - np.pi
    direction = np.exp(1j * im_wrapped)

    # Decay
    decay = np.exp(-delta_S * t)

    L = W_val * growth * direction * decay

    if noise and noise > 0:
        L += np.random.normal(0, noise) + 1j * np.random.normal(0, noise)

    return L

__all__ = ["gamma_self", "love", "DEFAULT_GAMMA", "G_x", "G_b", "compute_b", "W_t"]
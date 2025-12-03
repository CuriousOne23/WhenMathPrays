# core/love.py
# WhenMathPrays – Universal Relational Expression Protocol (UREP)
# December 2025 Simplification: γ_self0 character baseline
# L(t) = (γ_self(t) - γ_self0(t)) × W(t) × exp(-ΔS·t + c·N_breath)
# with W(t) = product of G_x for v,r,f,a (gates only, no spike or bond terms)
# γ_self0(n+1) = (1-η)·γ_self0(n) + η·γ_self(n) - ξ·N_neg(n)
# See docs/UREP_2025_Simplification_Proposal.md for full details

from typing import List, Optional
import numpy as np
from typing import Tuple

DEFAULT_GAMMA = 0.0 + 0.0j

# Canonical constants (December 2025 - see CONSTANTS.md)
DELTA_S = 0.010  # day⁻¹ (entropy decay)
C = 0.40  # breath efficacy
TAU_DEFAULT = 14  # days (memory window)
ALPHA = 1.80  # gate gain (LOCKED)
ETA = 0.003  # character plasticity (adult default, LOCKED by Grok)
XI = 0.001  # negative asymmetry weight (LOCKED by Grok)
LAMBDA = 0.003  # event density inertia (romance default)

# REMOVED (December 2025):
# BETA = 1.30 (spike base)
# W_CAP = 3.0 (spike ceiling)

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
    """Canonical gate function – locked form (December 2025)
    G_x(x) = 2x exp(α (x - 0.5)), x ∈ [0,1]
    α = 1.80 validated by Grok's 212k Monte Carlo simulations
    """
    return 2 * x * np.exp(alpha * (x - 0.5))

def W_t(primitives: Tuple[float, float, float, float]) -> float:
    """External enacted magnitude W(t) = product G_v × G_r × G_f × G_a
    
    December 2025 simplification: gates only, no spike or bond terms.
    Natural spiking emerges from gate product when primitives saturate.
    
    Args:
        primitives: (v, r, f, a) - four fast primitives [0,1]
    
    Returns:
        W(t): Emotional intensity (valence-neutral)
    """
    v, r, f, a = primitives
    return G_x(v) * G_x(r) * G_x(f) * G_x(a)

def update_gamma_self0(
    gamma_self0_prev: complex,
    gamma_self_recent: complex,
    N_neg: int,
    eta: float = ETA,
    xi: float = XI
) -> complex:
    """Update character baseline via slow drift
    
    γ_self0(n+1) = (1-η)·γ_self0(n) + η·γ_self(n) - ξ·N_neg(n)
    
    Args:
        gamma_self0_prev: Previous character baseline
        gamma_self_recent: Recent γ_self (14-day moving average)
        N_neg: Cumulative count of negative events
        eta: Character plasticity (default 0.003 for adults)
        xi: Negative asymmetry weight (default 0.001)
    
    Returns:
        Updated γ_self0
    """
    # Drift toward recent γ_self (slow adaptation)
    drift = (1 - eta) * gamma_self0_prev + eta * gamma_self_recent
    
    # Subtract negative asymmetry (trauma accumulation)
    # Applied to imaginary axis (love/hate dimension)
    negative_drag = xi * N_neg * 1j
    
    return drift - negative_drag

def count_negative_events(primitives_history: List[Tuple[float, float, float, float]]) -> int:
    """Count cumulative negative events (v<0.2 OR f<0.3 OR a<0.2)
    
    Args:
        primitives_history: List of (v, r, f, a) tuples
    
    Returns:
        N_neg: Count of negative events
    """
    count = 0
    for v, r, f, a in primitives_history:
        if v < 0.2 or f < 0.3 or a < 0.2:
            count += 1
    return count

def love(
    primitives: Tuple[float, float, float, float] = None,
    gamma_history: List[complex] = None,
    gamma_self0: complex = DEFAULT_GAMMA,
    N_breath: int = 0,
    tau: int = TAU_DEFAULT,
    delta_S: float = DELTA_S,
    c: float = C,
    t: float = 0.0,
    noise: float = 0.0,
    # Backwards-compatible parameters (deprecated, ignored if new params provided)
    S: int = None,
    b_0: float = None,
    beta_S: float = None,
    s_S: float = None,
    beta_b: float = None,
    W: float = None,
    tw: int = None,
) -> complex:
    """
    L(t) = (γ_self - γ_self0) × W(t) × exp(-ΔS·t + c·N_breath)
    
    December 2025 simplification:
    - (γ_self - γ_self0) = displacement from character baseline
    - W(t) = product G_x(v,r,f,a) (gates only, no spike/bond terms)
    - γ_self0 = character baseline (innate + trained tendencies)
    - Entropy includes shared breath counter N_breath
    
    Args:
        primitives: (v, r, f, a) - four fast primitives [0,1]
        gamma_history: List of γ_self complex values over time
        gamma_self0: Character baseline (slow-drifting)
        N_breath: Cumulative shared meaningful moments
        tau: Memory window for γ_self averaging (default 14 days)
        delta_S: Entropy decay rate (default 0.010)
        c: Breath efficacy (default 0.40)
        t: Time elapsed (days)
        noise: Optional Gaussian noise
    
    Backwards compatibility:
        S, b_0, beta_S, s_S, beta_b: Old bond parameters (ignored)
        W: Explicit W value (overrides primitives if provided)
        tw: Legacy alias for tau
    
    Returns:
        L(t): Complex love magnitude
    """
    if gamma_history is None or len(gamma_history) == 0:
        return 0.0 + 0.0j

    # Support legacy `tw` keyword as alias for `tau`
    if tw is not None:
        tau_use = tw
    else:
        tau_use = tau

    # Compute γ_self as moving average
    if tau_use == 0:
        gamma_avg = gamma_history[-1]
    else:
        recent = gamma_history[-tau_use:] if len(gamma_history) >= tau_use else gamma_history
        gamma_avg = np.mean(recent)

    # Displacement from character baseline
    displacement = gamma_avg - gamma_self0
    
    # At equilibrium (γ_self = γ_self0), L(t) = 0
    if abs(displacement) < 1e-10:
        return 0.0 + 0.0j

    # Compute W(t) from primitives (or use legacy W if provided)
    if W is not None:
        # Legacy mode: explicit W value
        W_val = float(W)
    else:
        if primitives is None:
            raise TypeError("love() requires either `primitives` or legacy `W` parameter")
        W_val = W_t(primitives)

    # Backwards compatibility: use S if N_breath not explicitly provided
    if N_breath == 0 and S is not None:
        N_breath = S

    # Entropy term: exp(-ΔS·t + c·N_breath)
    entropy = np.exp(-delta_S * t + c * N_breath)

    # Growth from real part of displacement (Ego/We)
    growth = np.exp(displacement.real)

    # Direction from imag part of displacement (Enmity/Love) – wrapped to [-π, π)
    im_wrapped = (displacement.imag + np.pi) % (2 * np.pi) - np.pi
    direction = np.exp(1j * im_wrapped)

    L = W_val * growth * direction * entropy

    if noise and noise > 0:
        L += np.random.normal(0, noise) + 1j * np.random.normal(0, noise)

    return L

# LEGACY FUNCTIONS (deprecated, maintained for backwards compatibility)
def compute_b(S: int, b_0: float, beta_S: float, s_S: float) -> float:
    """DEPRECATED: Bond state computation (pre-December 2025)
    Use γ_self0 displacement instead. Maintained for old test scripts.
    """
    return b_0 + beta_S * (1 - np.exp(-S / s_S))

def G_b(b: float, beta_b: float = 1.0) -> float:
    """DEPRECATED: Bond gate (pre-December 2025)
    Use γ_self0 displacement instead. Maintained for old test scripts.
    """
    return np.exp(beta_b * b)

__all__ = [
    "gamma_self", 
    "love", 
    "DEFAULT_GAMMA", 
    "G_x", 
    "W_t",
    "update_gamma_self0",
    "count_negative_events",
    # Legacy exports (deprecated)
    "G_b", 
    "compute_b"
]
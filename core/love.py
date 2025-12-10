# core/love.py
# WhenMathPrays – Gamma Relational Persona (GRP)
# December 2025 Rev 3.2: Im-only depth scaling for fidelity asymmetry
# γ_self(n+1) = γ_self(n) + (w_v·v + w_S,R·S) + i·(w_r·r + w_f·f' + w_a·a + w_S,I·S)
# where f' = w_f·f if f≥0, else f·(0.12·max(|Im|, 5.0)) (depth-scaled asymmetry)
# See docs/GRP_rev3.md for full specification

from typing import Tuple, Dict, Optional
import numpy as np

DEFAULT_GAMMA_SELF0 = 0.0 + 0.0j

# Canonical weights (December 2025 Rev 3.2 - see CONSTANTS.md)
# Axis weights (DEFAULT, tunable by scenario)
W_V = 0.8  # Visibility (real axis, Ego↔We)
W_R = 1.0  # Resonance (imaginary axis, Hate↔Love)
W_F = 1.2  # Fidelity positive (imaginary axis)
W_A = 0.6  # Altruism (imaginary axis)
W_S_R = 0.5  # Silence/presence (real axis contribution)
W_S_I = 0.5  # Silence/presence (imaginary axis contribution)

# Fidelity asymmetry (Rev 3.2: Im-only depth scaling)
FIDELITY_SCALING_FACTOR = 0.12  # Negative fidelity scaling coefficient (LOCKED)
FIDELITY_EPSILON = 5.0  # Collapse prevention floor for Im depth (LOCKED)

# Entropy drift (DEFAULT, tunable by scenario)
DELTA_S = 0.02  # Entropy drift magnitude per time unit
GAMMA_ENTROPY_ATTRACTOR = -8.0 + 0.0j  # Target position (ego axis)

# Default weights dictionary
DEFAULT_WEIGHTS = {
    'w_v': W_V,
    'w_r': W_R,
    'w_f': W_F,
    'w_a': W_A,
    'w_S_R': W_S_R,
    'w_S_I': W_S_I,
    'fidelity_scaling_factor': FIDELITY_SCALING_FACTOR,
    'fidelity_epsilon': FIDELITY_EPSILON,
    'delS': DELTA_S,
    'gamma_entropy_attractor': GAMMA_ENTROPY_ATTRACTOR,
    'entropy_per_event': False  # False=scale by time (default), True=per event
}


def apply_fidelity_asymmetry(
    f: float,
    love_depth: float,
    w_f: float = W_F,
    scaling_factor: float = FIDELITY_SCALING_FACTOR
) -> float:
    """Apply Im-only depth-scaled asymmetry to fidelity.
    
    For negatives: f' = f · (scaling_factor · love_depth)
        - The deeper the love (Im axis), the more a betrayal can scar
        - Scales only by |Im|, not full |γ_self| (prevents Ego/We coupling)
    For positives: f' = w_f · f (slow repair, always 1.2:1)
    
    Args:
        f: Fidelity primitive value (range -10 to +10)
        love_depth: max(|Im|, ε) where ε prevents collapse at origin
        w_f: Weight for positive fidelity (default 1.2)
        scaling_factor: Depth scaling coefficient for negatives (default 0.12)
    
    Returns:
        Weighted fidelity contribution to imaginary axis
    """
    if f < 0:
        # Negatives scale with love depth: deeper love = deeper wound
        # At 20i: f=-1 → -2.4i, At 150i: f=-1 → -18i
        return f * (scaling_factor * love_depth)
    else:
        # Positives heal at fixed rate (slow repair)
        return w_f * f


def update_gamma_self(
    gamma_self_current: complex,
    v: float,
    r: float,
    f: float,
    a: float,
    S: float,
    weights: Optional[Dict[str, float]] = None,
    time_delta: float = 1.0
) -> complex:
    """Component-wise update of γ_self position with entropy drift toward attractor.
    
    γ_self(n+1) = γ_self(n) + ΔRe + i·ΔIm + entropy_pull
    
    where:
        ΔRe = w_v·v + w_S,R·S  (Ego↔We axis)
        ΔIm = w_r·r + w_f·f' + w_a·a + w_S,I·S  (Hate↔Love axis)
        f' = apply_fidelity_asymmetry(f, max(|Im|, ε))  (Im-only depth scaling)
        entropy_pull = delS·Δt·(γ_attractor - γ_self) / |γ_attractor - γ_self|
            (pulls toward configurable attractor position, scaled by time and delS magnitude)
    
    Args:
        gamma_self_current: Current position γ_self(n)
        v: Visibility primitive (normalized, typically [-1, 1])
        r: Resonance primitive
        f: Fidelity primitive (subject to Im-only depth scaling if negative)
        a: Altruism primitive
        S: Silence/presence primitive (contributes to both axes)
        weights: Optional weight dictionary (defaults to CONSTANTS.md values)
        time_delta: Time elapsed since last event (default 1.0). 
                   Used to scale entropy drift. Ignored if entropy_per_event=True.
    
    Returns:
        γ_self(n+1): Updated position
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
    
    # Extract weights
    w_v = weights.get('w_v', W_V)
    w_r = weights.get('w_r', W_R)
    w_f = weights.get('w_f', W_F)
    w_a = weights.get('w_a', W_A)
    w_S_R = weights.get('w_S_R', W_S_R)
    w_S_I = weights.get('w_S_I', W_S_I)
    scaling_factor = weights.get('fidelity_scaling_factor', FIDELITY_SCALING_FACTOR)
    epsilon = weights.get('fidelity_epsilon', FIDELITY_EPSILON)
    delS = weights.get('delS', DELTA_S)
    gamma_entropy_attractor = weights.get('gamma_entropy_attractor', GAMMA_ENTROPY_ATTRACTOR)
    entropy_per_event = weights.get('entropy_per_event', False)
    
    # Compute love depth for fidelity asymmetry (Im-only, with floor)
    love_depth = max(abs(gamma_self_current.imag), epsilon)
    
    # Apply fidelity asymmetry (Im-only depth scaling)
    f_prime = apply_fidelity_asymmetry(f, love_depth, w_f, scaling_factor)
    
    # Component-wise updates from primitives
    delta_real = w_v * v + w_S_R * S  # Ego↔We axis
    delta_imag = w_r * r + w_f * f_prime + w_a * a + w_S_I * S  # Hate↔Love axis
    
    # Entropy drift: pull toward attractor position
    # Direction: unit vector from current position toward attractor
    # Magnitude: delS, scaled by time_delta (or fixed per event)
    attractor_vector = gamma_entropy_attractor - gamma_self_current
    attractor_distance = abs(attractor_vector)
    
    if attractor_distance > 1e-10:  # Avoid division by zero if already at attractor
        direction = attractor_vector / attractor_distance
        if entropy_per_event:
            entropy_pull = delS * direction  # Fixed magnitude per event
        else:
            entropy_pull = (delS * time_delta) * direction  # Scaled by time elapsed
    else:
        entropy_pull = 0.0 + 0.0j  # Already at attractor
    
    # Update position
    gamma_self_next = gamma_self_current + delta_real + 1j * delta_imag + entropy_pull
    
    return gamma_self_next


def gamma_self(
    ego_we_state: float = None,
    enmity_love_state: float = None,
    we_ego_state: float = None,
    love_enmity_state: float = None
) -> complex:
    """γ_self compatibility wrapper (for legacy test code).
    
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


def love(gamma_self_current: complex, **kwargs) -> complex:
    """Return γ_self position as love (identity function).
    
    In the December 2025 simplification, Love = γ_self position directly.
    No separate calculation. This function exists for backwards compatibility.
    
    Args:
        gamma_self_current: Current γ_self position
        **kwargs: Ignored (backwards compatibility with old signature)
    
    Returns:
        γ_self position (identical to input)
    """
    return gamma_self_current


# LEGACY FUNCTIONS (deprecated, maintained for backwards compatibility)
# These exist only to prevent old test scripts from breaking

ALPHA = 1.80  # Old gate gain (no longer used)
DELTA_S = 0.010  # Old entropy decay (no longer used)
C = 0.40  # Old breath efficacy (no longer used)
TAU_DEFAULT = 14  # Old memory window (no longer used)
ETA = 0.003  # Old character plasticity (no longer used)
XI = 0.001  # Old negative asymmetry (no longer used)
DEFAULT_GAMMA = 0.0 + 0.0j  # Alias for DEFAULT_GAMMA_SELF0

def G_x(x: float, alpha: float = ALPHA) -> float:
    """DEPRECATED: Gate function (pre-December 2025).
    No longer used in new positional model. Maintained for old tests.
    """
    return 2 * x * np.exp(alpha * (x - 0.5))

def W_t(primitives: Tuple[float, float, float, float]) -> float:
    """DEPRECATED: W(t) calculation (pre-December 2025).
    No longer used. Maintained for old tests.
    """
    v, r, f, a = primitives
    return G_x(v) * G_x(r) * G_x(f) * G_x(a)

def update_gamma_self0(gamma_self0_prev: complex, gamma_self_recent: complex,
                      N_neg: int, eta: float = ETA, xi: float = XI) -> complex:
    """DEPRECATED: γ_self0 drift (pre-December 2025).
    γ_self0 is now INITIAL CONDITION ONLY (no drift equation).
    Maintained for old tests.
    """
    drift = (1 - eta) * gamma_self0_prev + eta * gamma_self_recent
    negative_drag = xi * N_neg * 1j
    return drift - negative_drag

def count_negative_events(primitives_history) -> int:
    """DEPRECATED: Negative event counter (pre-December 2025).
    Maintained for old tests.
    """
    count = 0
    for primitives in primitives_history:
        if hasattr(primitives, '__len__') and len(primitives) >= 4:
            v, r, f, a = primitives[0], primitives[1], primitives[2], primitives[3]
            if v < 0.2 or f < 0.3 or a < 0.2:
                count += 1
    return count

def compute_b(S: int, b_0: float, beta_S: float, s_S: float) -> float:
    """DEPRECATED: Bond state (pre-December 2025). Maintained for old tests."""
    return b_0 + beta_S * (1 - np.exp(-S / s_S))

def G_b(b: float, beta_b: float = 1.0) -> float:
    """DEPRECATED: Bond gate (pre-December 2025). Maintained for old tests."""
    return np.exp(beta_b * b)


__all__ = [
    # New API (December 2025 - Rev 4)
    "update_gamma_self",
    "apply_fidelity_asymmetry",
    "DEFAULT_WEIGHTS",
    "DEFAULT_GAMMA_SELF0",
    
    # Compatibility
    "gamma_self",
    "love",
    
    # Legacy (deprecated, for old tests only)
    "DEFAULT_GAMMA",
    "G_x",
    "W_t",
    "update_gamma_self0",
    "count_negative_events",
    "G_b",
    "compute_b"
]

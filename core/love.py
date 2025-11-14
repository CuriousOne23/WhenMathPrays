# core/love.py — FINAL, CORRECTED
import numpy as np
from typing import List, Tuple

# === UNION BIAS — LOVE IS THE DEFAULT ===
UNION_BIAS = (1.0, 3.2)  # SURRENDER=1.0, BOND=3.0

def gamma_self(
    ego_flux: float,
    bond_flux: float,
    union_bias: Tuple[float, float] | None = None
) -> complex:
    if union_bias is None:
        S, B = UNION_BIAS
    else:
        S, B = union_bias
    
    ego = max(0.0, ego_flux - S)
    bond = bond_flux + B
    return -ego + 1j * bond

def love(
    W: float,
    gamma_history: List[complex],
    tw: int = 7,
    delta_S: float = 0.001,
    t: float = 0.0
) -> complex:
    if not gamma_history:
        raise ValueError("gamma_history cannot be empty")
    
    if any(np.isclose(np.abs(g), 0.0) for g in gamma_history[-tw:]):
        raise ValueError("γ_self magnitude zero in window — death state")

    history = np.array(gamma_history[-tw:]) if len(gamma_history) >= tw else np.array(gamma_history)
    gamma_avg = np.mean(history)
    return W * np.exp(gamma_avg) * np.exp(-delta_S * t)
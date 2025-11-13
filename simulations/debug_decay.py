"""
DEBUG: Why L_high ≈ 1000 when it should be < 50?
#WhenMathPrays
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from core.love import love
from core.gamma_self import gamma_self

t = np.linspace(0, 10, 11)
dt = 1.0

gamma_low = gamma_self(t, dM_dt=-0.1, dR_dt=-0.1)
L_low = love(
    vis_t=np.ones(11), res_t=np.ones(11),
    fidelity=1.0, altruism=1.0,
    shared_growth_t=np.full(11, 10),
    gamma_t=gamma_low, delta_S_t=np.zeros(11), dt=dt
)

gamma_high = gamma_self(t, dM_dt=0.5, dR_dt=0.5)
L_high = love(
    vis_t=np.ones(11), res_t=np.ones(11),
    fidelity=1.0, altruism=1.0,
    shared_growth_t=np.full(11, 10),
    gamma_t=gamma_high, delta_S_t=np.zeros(11), dt=dt
)

print(f"|γ_low|  = {np.mean(np.abs(gamma_low)):.3f}")
print(f"|γ_high| = {np.mean(np.abs(gamma_high)):.3f}")
print(f"L_low    = {L_low.real:.2f}")
print(f"L_high   = {L_high.real:.2f}")
print(f"Decay factor for high γ: exp(-1000 * 0.707 * 10) = {np.exp(-1000 * 0.707 * 10):.2e}")

# debug_love_perfect.py
"""
DEBUG: love.py — 0% NOISE (PERFECT INPUTS)
"""
import numpy as np
from core.gamma_self import gamma_self
from core.love import love

print("DEBUG: love.py — 0% NOISE")
print("=" * 50)

dt = 0.1
t = np.arange(0, 10.0, dt)

gamma_t = gamma_self(t, b=0.5, A=0.25)
shared_growth_t = 0.5 + 0.5 * np.abs(np.imag(gamma_t))

# Perfect inputs
vis_t = np.ones_like(t) * 0.8
res_t = np.ones_like(t) * 0.7
delta_S_t = np.ones_like(t) * (-0.02)

L = love(
    vis_t=vis_t,
    res_t=res_t,
    fidelity=0.9,
    altruism=0.6,
    shared_growth_t=shared_growth_t,
    gamma_t=gamma_t,
    delta_S_t=delta_S_t,
    dt=dt,
    soul_locked=True
)

print(f"Love = {L:.6f}")
print(f"Expected: ~0.57")
print(f"Actual:   {L:.6f}")
print("PASS" if 0.55 <= L <= 0.59 else "FAIL")
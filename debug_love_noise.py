# debug_love_noise.py
"""
DEBUG: love.py — 90% NOISE
"""
import numpy as np
from core.gamma_self import gamma_self
from core.love import love

print("DEBUG: love.py — 90% NOISE")
print("=" * 50)

dt = 0.1
t = np.arange(0, 10.0, dt)
base = 0.8
noise_level = 0.9
noise_scale = 1.65

std = noise_level * noise_scale * base  # 1.188

gamma_t = gamma_self(t, b=0.5, A=0.25)
shared_growth_t = 0.5 + 0.5 * np.abs(np.imag(gamma_t))

# 90% noise
vis_t = base + np.random.normal(0, std, len(t))
res_t = base + np.random.normal(0, std, len(t))
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

print(f"Std = {std:.3f}")
print(f"vis_t mean: {vis_t.mean():.3f}, std: {vis_t.std():.3f}")
print(f"res_t mean: {res_t.mean():.3f}, std: {res_t.std():.3f}")
print(f"Love = {L:.6f}")
print(f"Expected: negative or low")
print("PASS" if L < 0.1 else "FAIL")
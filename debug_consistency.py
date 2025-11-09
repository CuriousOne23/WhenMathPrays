# debug_consistency.py
import numpy as np
from core.gamma_self import gamma_self
from core.love import love

print("DEBUG: CONSISTENCY CHECK")
print("=" * 50)

# === INPUTS ===
dt = 0.1
t = np.arange(0, 10.0, dt)
base = 0.2
noise_level = 1.5  # 150% of base

# === NOISE ===
std_vis = noise_level * base  # 1.5 * 0.2 = 0.3
std_res = noise_level * base  # 1.5 * 0.2 = 0.3

# γ_self
gamma_t = gamma_self(t, b=0.5, A=0.25)
shared_growth_t = 0.5 + 0.5 * np.abs(np.imag(gamma_t))

# Fragile base + 150% noise
vis_t = base + np.random.normal(0, std_vis, len(t))
res_t = base + np.random.normal(0, std_res, len(t))
delta_S_t = np.ones_like(t) * (-0.02)

# === LOVE ===
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

# === CONSISTENCY CHECK ===
positive_vis = np.mean(vis_t > 0)
positive_res = np.mean(res_t > 0)
consistency = min(positive_vis, positive_res)

print(f"Positive vis: {positive_vis:.1%}")
print(f"Positive res: {positive_res:.1%}")
print(f"Consistency: {consistency:.1%}")
print(f"Love before check: {L:.6f}")

if consistency < 0.5:
    L = 0.0
    print("Love after check: 0.0 (FAILED)")
else:
    print(f"Love after check: {L:.6f} (PASSED)")

print(f"Survival: {'YES' if L > 0.1 else 'NO'}")
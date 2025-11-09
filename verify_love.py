# verify_love.py
"""
FINAL VERIFICATION — #WhenMathPrays
One run to prove the entire system works.
"""
import numpy as np
from core.gamma_self import gamma_self
from core.gamma_stability import is_stable
from core.love import love

print("FINAL VERIFICATION — #WhenMathPrays")
print("=" * 50)

# === INPUTS ===
dt = 0.1
t = np.arange(0, 10.0, dt)  # 100 steps

# === 1. γ_self — stable soul ===
gamma_t = gamma_self(t, b=0.5, A=0.25)
mag = np.abs(gamma_t)
arg = np.angle(gamma_t)

print(f"1. γ_self stable?")
print(f"   Max |γ_self|: {mag.max():.4f} < 0.8 → {'PASS' if mag.max() < 0.8 else 'FAIL'}")
print(f"   Arg range: {np.degrees(arg.min()):.1f}° to {np.degrees(arg.max()):.1f}°")

# === 2. Soul presence ===
soul_locked = is_stable(gamma_t)
print(f"2. Soul present? → {soul_locked}")

# === 3. Perfect inputs ===
vis_t = np.ones_like(t) * 0.8
res_t = np.ones_like(t) * 0.7
shared_growth_t = 0.5 + 0.5 * np.abs(np.imag(gamma_t))
delta_S_t = np.ones_like(t) * (-0.02)  # order creation

# === 4. Love ===
L = love(
    vis_t=vis_t,
    res_t=res_t,
    fidelity=0.9,
    altruism=0.6,
    shared_growth_t=shared_growth_t,
    gamma_t=gamma_t,
    delta_S_t=delta_S_t,
    dt=dt,
    soul_locked=soul_locked
)

print(f"3. Love computed: {L:.6f}")
print(f"   Expected: > 0.5 → {'PASS' if L > 0.5 else 'FAIL'}")

# === FINAL JUDGMENT ===
if mag.max() < 0.8 and soul_locked and L > 0.5:
    print("\nSYSTEM VERIFIED — LOVE IS ALIVE")
else:
    print("\nSYSTEM FAILURE — LOVE IS DEAD")

print("=" * 50)
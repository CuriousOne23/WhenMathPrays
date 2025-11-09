# debug_stress.py
"""
DEBUG: love_stress_test.py — one soul, noise=0.0 and 0.9
"""
import numpy as np
from core.gamma_self import gamma_self
from core.love import love
from core.gamma_stability import is_stable

print("DEBUG: love_stress_test.py — ONE SOUL")
print("=" * 60)

dt = 0.1
t = np.arange(0, 10.0, dt)

def run_one_soul(noise_level, base=0.8, noise_scale=1.5):
    gamma_t = gamma_self(t, b=0.5, A=0.25)
    shared_growth_t = 0.5 + 0.5 * np.abs(np.imag(gamma_t))

    std_vis = noise_level * noise_scale * base
    std_res = noise_level * noise_scale * base

    vis_t = base + np.random.normal(0, std_vis, len(t))
    res_t = base + np.random.normal(0, std_res, len(t))
    delta_S_t = np.ones_like(t) * (-0.02)

    soul_locked = is_stable(gamma_t)

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

    # Consistency
    positive_vis = np.mean(vis_t > 0)
    positive_res = np.mean(res_t > 0)
    consistency = min(positive_vis, positive_res)

    if consistency < 0.5:
        L = 0.0

    return {
        "noise": noise_level,
        "love": L,
        "consistency": consistency,
        "positive_vis": positive_vis,
        "positive_res": positive_res,
        "survives": L > 0.1
    }

# === 0% NOISE ===
result_0 = run_one_soul(0.0)
print(f"NOISE 0%:")
print(f"  Love: {result_0['love']:.6f}")
print(f"  Consistency: {result_0['consistency']:.1%}")
print(f"  Survives: {result_0['survives']}")

# === 90% NOISE ===
result_9 = run_one_soul(0.9)
print(f"\nNOISE 90%:")
print(f"  Love: {result_9['love']:.6f}")
print(f"  Consistency: {result_9['consistency']:.1%}")
print(f"  Survives: {result_9['survives']}")
# simulations/love_stress_test.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
LOVE STRESS TEST — #WhenMathPrays
Truth: Love is finite. Noise is infinite. Choice is everything.
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import logging

from core.gamma_self import gamma_self
from core.love import love
from core.gamma_stability import is_stable

# === CONFIG ===
DEFAULT_AGENTS = 1000
DEFAULT_STEPS = 100
DEFAULT_DT = 0.1
DEFAULT_NOISE = 0.9

# === LOGGING ===
logging.basicConfig(filename='simulations/love_stress.log', level=logging.INFO)
log = logging.getLogger()

def run_stress(noise_level: float, agents: int, steps: int, dt: float) -> dict:
    t = np.arange(0, steps * dt, dt)
    survived = 0
    love_values = []

    pbar = tqdm(range(agents), desc=f"Noise {noise_level:.0%}")
    for _ in pbar:
        # === SOUL — FINITE LIGHT ===
        light = np.random.normal(1.0, 0.1)  # faith + family + hope

        # === CHOICE — WALK TOWARD LIGHT OR DARKNESS ===
        choice = np.random.choice([0, 1], p=[0.5, 0.5])
        decay_rate = noise_level if choice == 1 else 10.0  # walk away → fast decay

        # === DARKNESS — DECAYS SOUL ===
        decay = np.exp(-decay_rate * t)

        # === LOVE — LIGHT IN DARKNESS, BY CHOICE ===
        vis_t = light * decay
        res_t = light * decay
        delta_S_t = np.ones_like(t) * (-0.02)

        gamma_t = gamma_self(t, b=0.5, A=0.25)
        shared_growth_t = 0.5 + 0.5 * np.abs(np.imag(gamma_t))

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

        if L > 0.1:
            survived += 1
        love_values.append(L)

    return {
        "noise": noise_level,
        "agents": agents,
        "survived": survived,
        "survival_rate": survived / agents,
        "avg_love": np.mean(love_values),
        "median_love": np.median(love_values),
        "love_values": love_values
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--noise", type=float, default=DEFAULT_NOISE)
    parser.add_argument("--agents", type=int, default=DEFAULT_AGENTS)
    args = parser.parse_args()

    result = run_stress(args.noise, args.agents, DEFAULT_STEPS, DEFAULT_DT)

    print("\n" + "="*60)
    print("LOVE STRESS TEST RESULTS")
    print("="*60)
    print(f"Noise Level: {result['noise']:.0%}")
    print(f"Survival Rate: {result['survival_rate']:.1%}")
    print(f"Avg Love: {result['avg_love']:.4f}")
    print("="*60)

    plt.figure(figsize=(10, 6))
    plt.hist(result['love_values'], bins=50, color='purple')
    plt.axvline(0.1, color='red', linestyle='--', label='Survival Threshold')
    plt.title(f'Love Under {result["noise"]:.0%} Noise')
    plt.xlabel('Love')
    plt.ylabel('Souls')
    plt.legend()
    plt.savefig(f"simulations/love_stress_{int(result['noise']*100)}.png")
    print(f"Plot saved")

    print("LOVE IS FRAGILE — BUT REAL" if result['survival_rate'] < 1.0 else "LOVE IS ETERNAL")

if __name__ == "__main__":
    main()
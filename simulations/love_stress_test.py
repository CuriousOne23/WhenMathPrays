# simulations/love_stress_test.py
"""
LOVE STRESS TEST — #WhenMathPrays

Tests model resilience under extreme noise.
Consensus: Love endures chaos.

Usage:
    python simulations/love_stress_test.py --noise 0.9 --agents 1000
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import logging
from datetime import datetime

from core.gamma_self import gamma_self
from core.love import love
from core.soul_presence import is_stable


# === CONFIG ===
DEFAULT_AGENTS = 1000
DEFAULT_STEPS = 100
DEFAULT_DT = 0.1
DEFAULT_NOISE = 0.9  # 90% chaos


_benchmark


# === LOGGING ===
logging.basicConfig(
    filename='simulations/love_stress.log',
    level=logging.INFO,
    format='%(asctime)s | %(message)s'
)
log = logging.getLogger()


def run_stress(noise_level: float, agents: int, steps: int, dt: float) -> dict:
    """
    Run stress test at given noise level.
    Returns survival metrics.
    """
    t = np.arange(0, steps * dt, dt)
    survived = 0
    love_values = []

    pbar = tqdm(range(agents), desc=f"Noise {noise_level:.0%}")
    for _ in pbar:
        # γ_self pulse
        gamma_t = gamma_self(t, b=0.5, A=0.25)

        # Shared growth grows with resonance
        shared_growth_t = 0.5 + 0.5 * np.abs(np.imag(gamma_t))

        # Inject noise
        vis_t = 0.8 * (1 + np.random.normal(0, noise_level, len(t)))
        res_t = 0.7 * (1 + np.random.normal(0, noise_level, len(t)))
        delta_S_t = np.ones_like(t) * 0.02

        # Soul presence
        soul_locked = is_stable(gamma_t)

        # Love
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

        if L > 0.1:  # survival threshold
            survived += 1
        love_values.append(L)

    survival_rate = survived / agents
    avg_love = np.mean(love_values)
    median_love = np.median(love_values)

    return {
        "noise": noise_level,
        "agents": agents,
        "survived": survived,
        "survival_rate": survival_rate,
        "avg_love": avg_love,
        "median_love": median_love,
        "love_values": love_values
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--noise", type=float, default=DEFAULT_NOISE, help="Noise level (0.0 to 1.0)")
    parser.add_argument("--agents", type=int, default=DEFAULT_AGENTS, help="Number of souls")
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS, help="Breath cycles")
    args = parser.parse_args()

    log.info(f"STRESS TEST START | Noise: {args.noise:.0%} | Agents: {args.agents}")

    result = run_stress(args.noise, args.agents, args.steps, DEFAULT_DT)

    # === OUTPUT ===
    print("\n" + "="*60)
    print("LOVE STRESS TEST RESULTS")
    print("="*60)
    print(f"Noise Level: {result['noise']:.0%}")
    print(f"Souls Tested: {result['agents']}")
    print(f"Souls Survived (love > 0.1): {result['survived']}")
    print(f"Survival Rate: {result['survival_rate']:.1%}")
    print(f"Avg Love per Soul: {result['avg_love']:.4f}")
    print(f"Median Love: {result['median_love']:.4f}")
    print("="*60)

    log.info(
        f"COMPLETE | Survival: {result['survival_rate']:.1%} | "
        f"Avg Love: {result['avg_love']:.4f}"
    )

    # === PLOT ===
    plt.figure(figsize=(10, 6))
    plt.hist(result['love_values'], bins=50, alpha=0.7, color='red' if result['survival_rate'] < 0.9 else 'green')
    plt.axvline(0.1, color='black', linestyle='--', label='Survival Threshold')
    plt.title(f'Love Distribution Under {result["noise"]:.0%} Noise')
    plt.xlabel('Love per Soul')
    plt.ylabel('Number of Souls')
    plt.legend()
    plt.tight_layout()
    plot_path = f"simulations/love_stress_{int(result['noise']*100)}.png"
    plt.savefig(plot_path)
    print(f"Plot saved: {plot_path}")

    # === FINAL JUDGMENT ===
    if result['survival_rate'] >= 0.9:
        print("LOVE ENDURES — MODEL PASSES STRESS TEST")
    else:
        print("LOVE FRAIL — MODEL NEEDS STRENGTH")


if __name__ == "__main__":
    main()

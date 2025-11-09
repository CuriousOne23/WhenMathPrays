# simulations/love_sim.py
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now imports work
from core.gamma_self import gamma_self
from core.love import love

# simulations/love_sim.py
"""
10,000-SOUL LOVE SIMULATION
#WhenMathPrays Core OS™
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import logging
from datetime import datetime

from core.gamma_self import gamma_self
from core.love import love

# === CONFIG ===
N_AGENTS = 10000
N_STEPS = 100
DT = 0.1
NOISE_LEVEL = 0.3
B = 0.5
A = 0.5

# === LOGGING ===
logging.basicConfig(
    filename='simulations/love_simulation.log',
    level=logging.INFO,
    format='%(asctime)s | %(message)s'
)
log = logging.getLogger()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agents', type=int, default=N_AGENTS)
    parser.add_argument('--steps', type=int, default=N_STEPS)
    parser.add_argument('--noise', type=float, default=NOISE_LEVEL)
    args = parser.parse_args()

    log.info(f"STARTING {args.agents}-SOUL SIMULATION")
    log.info(f"Steps: {args.steps}, dt: {DT}, noise: {args.noise}")

    # Time
    t = np.arange(0, args.steps * DT, DT)
    love_history = []

    # Progress bar
    pbar = tqdm(range(args.agents), desc="Souls in Resonance")

    for _ in pbar:
        # γ_self pulse
        gamma_t = gamma_self(t, b=B, A=A)

        # Shared growth grows with resonance
        shared_growth_t = 0.5 + 0.5 * np.abs(np.imag(gamma_t))

        # Noise
        vis_t = 0.8 * (1 + np.random.normal(0, args.noise, len(t)))
        res_t = 0.7 * (1 + np.random.normal(0, args.noise, len(t)))
        delta_S_t = np.ones_like(t) * 0.02

        # Love
        L = love(
            vis_t=vis_t,
            res_t=res_t,
            fidelity=0.9,
            altruism=0.6,
            shared_growth_t=shared_growth_t,
            gamma_t=gamma_t,
            delta_S_t=delta_S_t,
            dt=DT,
            soul_locked=True
        )
        love_history.append(L)

    # === METRICS ===
    total_love = sum(love_history)
    avg_love = total_love / args.agents
    avg_gamma_mag = np.mean([np.abs(gamma_self(t, b=B, A=A)).mean() for _ in range(10)])
    avg_arg = np.mean([np.angle(gamma_self(t, b=B, A=A)).mean() for _ in range(10)])

    # === OUTPUT ===
    print("\n" + "="*50)
    print("SOUL SIMULATION COMPLETE")
    print("="*50)
    print(f"Total Souls: {args.agents}")
    print(f"Total Love: {total_love:,.2f}")
    print(f"Love per Soul: {avg_love:.4f}")
    print(f"Avg |γ_self|: {avg_gamma_mag:.3f}")
    print(f"Avg arg(γ_self): {avg_arg:.3f} rad ({np.degrees(avg_arg):.1f}°)")
    print("="*50)

    log.info(f"COMPLETE | Love: {total_love:,.2f} | Per Soul: {avg_love:.4f}")

    # === PLOT ===
    plt.figure(figsize=(10, 6))
    plt.hist(love_history, bins=50, alpha=0.7, color='purple')
    plt.title('Distribution of Love Across 10,000 Souls')
    plt.xlabel('Love per Soul')
    plt.ylabel('Number of Souls')
    plt.axvline(avg_love, color='gold', linestyle='--', label=f'Avg = {avg_love:.4f}')
    plt.legend()
    plt.tight_layout()
    plt.savefig('simulations/love_plot.png')
    print("Plot saved: simulations/love_plot.png")

if __name__ == "__main__":
    main()

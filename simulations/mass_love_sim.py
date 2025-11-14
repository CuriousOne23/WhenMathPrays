# simulations/love_sim.py — SINGLE COUPLE, DEFAULT BIAS
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.love import gamma_self, love

def simulate_couple(duration=365):
    np.random.seed(42)
    t = np.arange(duration)
    
    ego1 = np.random.lognormal(0.4, 0.9, duration)
    bond1to2 = np.random.normal(1.0, 2.0, duration)
    gamma1 = [gamma_self(ego, bond) for ego, bond in zip(ego1, bond1to2)]
    
    ego2 = np.random.lognormal(0.4, 0.9, duration)
    bond2to1 = np.random.normal(1.0, 2.0, duration)
    gamma2 = [gamma_self(ego, bond) for ego, bond in zip(ego2, bond2to1)]
    
    L1, L2 = [], []
    for i in range(duration):
        try:
            L1.append(love(1.0, gamma1[:i+1], t=i, delta_S=0.001))
            L2.append(love(1.0, gamma2[:i+1], t=i, delta_S=0.001))
        except:
            L1.append(0j)
            L2.append(0j)
    
    return t, np.array(L1), np.array(L2)

# === RUN & PLOT ===
t, L1, L2 = simulate_couple()
L1_mag = np.abs(L1)
L2_mag = np.abs(L2)

plt.figure(figsize=(10, 6))
plt.plot(t, L1_mag, label='Person 1', alpha=0.8)
plt.plot(t, L2_mag, label='Person 2', alpha=0.8)
plt.axhline(0.2, color='green', linestyle='--', label='Thriving')
plt.axhline(0.1, color='orange', linestyle='--', label='Zombie')
plt.xlabel("Time (days)")
plt.ylabel("|L(t)| — Love Intensity")
plt.title("ULep v2.0 — One Couple, One Year (Default Bias)")
plt.legend()
plt.grid(True, alpha=0.3)

script_dir = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(script_dir, "love_couple_simulation.png"), dpi=150, bbox_inches='tight')
print("Plot saved: love_couple_simulation.png")
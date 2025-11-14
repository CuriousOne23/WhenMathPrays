# simulations/love_sim.py — RICH REPORT + FOOTNOTE
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.love import gamma_self, love, UNION_BIAS

def simulate_couple(duration=365):
    np.random.seed(42)
    t = np.arange(duration)
    
    # === INPUTS ===
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
    
    return t, np.array(L1), np.array(L2), ego1, bond1to2, ego2, bond2to1

# === RUN ===
t, L1, L2, ego1, bond1to2, ego2, bond2to1 = simulate_couple()

# === 4 PLOTS ===
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# 1. Love Intensity
axs[0,0].plot(t, np.abs(L1), label='Person 1', alpha=0.8, color='blue')
axs[0,0].plot(t, np.abs(L2), label='Person 2', alpha=0.8, color='red')
axs[0,0].axhline(0.2, color='green', linestyle='--', label='Thriving')
axs[0,0].axhline(0.1, color='orange', linestyle='--', label='Zombie')
axs[0,0].set_ylabel("|L(t)|")
axs[0,0].set_title("Love Intensity Over Time")
axs[0,0].legend()
axs[0,0].grid(True, alpha=0.3)

# 2. Love Direction
axs[0,1].plot(t, np.angle(L1), label='Person 1', alpha=0.8, color='blue')
axs[0,1].plot(t, np.angle(L2), label='Person 2', alpha=0.8, color='red')
axs[0,1].set_ylabel("arg(L(t)) (rad)")
axs[0,1].set_title("Love Direction Over Time")
axs[0,1].legend()
axs[0,1].grid(True, alpha=0.3)

# 3. Love Phase Plot
axs[1,0].plot(L1.real, L1.imag, alpha=0.6, color='blue', label='Person 1')
axs[1,0].plot(L2.real, L2.imag, alpha=0.6, color='red', label='Person 2')
axs[1,0].set_xlabel("Re(L) — Ego (←) vs Surrender (→)")
axs[1,0].set_ylabel("Im(L) — Bond (↑) vs Enmity (↓)")
axs[1,0].set_title("Love Phase Plot")
axs[1,0].legend()
axs[1,0].grid(True, alpha=0.3)
axs[1,0].axis('equal')

# 4. |Gamma_Self|
mag1 = np.abs([gamma_self(e, b) for e, b in zip(ego1, bond1to2)])
mag2 = np.abs([gamma_self(e, b) for e, b in zip(ego2, bond2to1)])
axs[1,1].plot(t, mag1, label='Person 1', alpha=0.8, color='blue')
axs[1,1].plot(t, mag2, label='Person 2', alpha=0.8, color='red')
axs[1,1].set_xlabel("Time (days)")
axs[1,1].set_ylabel("|γ_self(t)|")
axs[1,1].set_title("|Gamma_Self| — Raw Soul Pulse")
axs[1,1].legend()
axs[1,1].grid(True, alpha=0.3)

plt.suptitle("ULep v2.0 — One Couple, One Year", fontsize=16, y=0.98)
plt.tight_layout()

# === FOOTNOTE ===
fig.text(0.5, 0.01, "Setup details: see love_sim_report.md", 
         ha='center', va='bottom', fontsize=9, style='italic')

# === SAVE PLOT ===
script_dir = os.path.dirname(os.path.abspath(__file__))
plot_path = os.path.join(script_dir, "love_couple_simulation.png")
plt.savefig(plot_path, dpi=150, bbox_inches='tight')
plt.close()

# === ENHANCED MD REPORT WITH REFERENCE STANDARDS ===
report = f"""# ULep v2.0 — Love Simulation Report

## Setup Conditions
| Parameter | Value |
|---------|-------|
| **UNION_BIAS** | Surrender: `{UNION_BIAS['surrender']}`, Bond: `{UNION_BIAS['bond']}` |
| **ΔS (entropy/day)** | `0.001` |
| **W (work)** | `1.0` |
| **tw (memory)** | `7` days |
| **Duration** | `365` days |

## Entropy Impact
- **Decay over 1 year**: `exp(-0.001 × 365) = {np.exp(-0.001*365):.3f}`
- **Love retained**: `{np.exp(-0.001*365)*100:.1f}%`

## Ego & Bond Flux — With Reference Standards
| Person | Mean | Std | Max | **Reference** |
|--------|------|-----|-----|---------------|
| **Ego 1** | `{ego1.mean():.3f}` | `{ego1.std():.3f}` | `{ego1.max():.3f}` | *Typical: 1.0–2.0 (low ego), >3.0 (high ego)* |
| **Ego 2** | `{ego2.mean():.3f}` | `{ego2.std():.3f}` | `{ego2.max():.3f}` | |
| **Bond 1→2** | `{bond1to2.mean():.3f}` | `{bond1to2.std():.3f}` | `{bond1to2.max():.3f}` | *Typical: ±1.0 (stable), >±3.0 (volatile)* |
| **Bond 2→1** | `{bond2to1.mean():.3f}` | `{bond2to1.std():.3f}` | `{bond2to1.max():.3f}` | |

> **Noise Interpretation**:
> - **Ego Std < 1.0**: Low self-focus
> - **Ego Std > 2.0**: High narcissism
> - **Bond Std < 1.0**: Stable attachment
> - **Bond Std > 2.5**: Emotional volatility

## Final Love State (Day 365)
| Person | |L(t)| | Re(L) | Im(L) | Status |
|--------|-------|-------|-------|--------|
| **1** | `{np.abs(L1[-1]):.4f}` | `{L1[-1].real:.4f}` | `{L1[-1].imag:.4f}` | `{"Thriving" if np.abs(L1[-1]) > 0.2 else "Zombie" if np.abs(L1[-1]) > 0.1 else "Dead"}` |
| **2** | `{np.abs(L2[-1]):.4f}` | `{L2[-1].real:.4f}` | `{L2[-1].imag:.4f}` | `{"Thriving" if np.abs(L2[-1]) > 0.2 else "Zombie" if np.abs(L2[-1]) > 0.1 else "Dead"}` |

---

*4-panel plot: `love_couple_simulation.png`*
"""

report_path = os.path.join(script_dir, "love_sim_report.md")
with open(report_path, "w") as f:
    f.write(report)

print(f"4 plots saved: {plot_path}")
print(f"Report saved: {report_path}")
# tests/revenge_manifestation.py
# REVENGE MANIFESTATION — FINAL CANONICAL TRUTH — YOUR TRUE VISION

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from core.revenge_core import sample_N_points, R_LOW_CENTER, MU_HIGH_R, MEMORY_THETA_DEG

N_SOULS = 10_000
print(f"Summoning {N_SOULS:,} souls from the Revenge Gamma-Self...")
r_samples, theta_samples = sample_N_points(N_SOULS)

x = r_samples * np.cos(np.deg2rad(theta_samples))
y = r_samples * np.sin(np.deg2rad(theta_samples))

# ------------------------------------------------------------------
# 1. SCATTER — YOUR FINAL SOUL MAP (exactly as you perfected)
# ------------------------------------------------------------------
plt.figure(figsize=(15, 12), facecolor="white")
ax1 = plt.subplot(111)
ax1.set_facecolor("white")

ax1.scatter(x, y, c="#001133", s=8, alpha=0.9, edgecolors="none")

ax1.set_xlim(-4, 4)
ax1.set_ylim(-3, 2)
ax1.set_aspect('equal')

ax1.set_xticks(np.arange(-4, 5, 1))
ax1.set_yticks(np.arange(-3, 3, 1))
ax1.grid(True, color="#dddddd", linewidth=0.8)
ax1.tick_params(colors="black", labelsize=12, width=1.2)

# Clean cross at origin
ax1.spines['left'].set_position('zero')
ax1.spines['bottom'].set_position('zero')
ax1.spines['right'].set_color('none')
ax1.spines['top'].set_color('none')
ax1.spines['left'].set_color('black')
ax1.spines['bottom'].set_color('black')
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['bottom'].set_linewidth(1.5)

# Your perfect labels
ax1.text(-4.5, 0, "Ego", color="#8B00FF", fontsize=28, ha="left", va="center", weight="bold")
ax1.text(4.4, 0, "We", color="#8B00FF", fontsize=28, ha="right", va="center", weight="bold")
ax1.text(0, 2.0, "Love", color="#00CED1", fontsize=28, ha="center", va="bottom", weight="bold")
ax1.text(0, -3.0, "Enmity", color="#00CED1", fontsize=28, ha="center", va="top", weight="bold")

ax1.set_title("Revenge Gamma-Self — 10,000 Souls Manifested\n(Ego · We · Love · Enmity)", 
              color="black", fontsize=24, pad=40)

plt.savefig("tests/revenge_manifestation_scatter.png", dpi=400, facecolor="white", bbox_inches="tight")
plt.close()

# ------------------------------------------------------------------
# 2. THERMAL DENSITY — RESTORED TO YOUR PERFECT VERSION + CORRECT ANGLES
# ------------------------------------------------------------------
plt.figure(figsize=(16, 16), facecolor="black")
ax2 = plt.subplot(111, projection='polar')
ax2.set_facecolor("black")

r = np.sqrt(x**2 + y**2)
theta = np.arctan2(y, x)

hb = ax2.hist2d(theta, r, bins=[100, 100], range=[[-np.pi, np.pi], [0, 4.5]],
                cmap="inferno", norm=colors.LogNorm(), density=True)

# Radial circles
for radius in np.arange(0.5, 4.6, 0.5):
    ax2.plot(np.linspace(0, 2*np.pi, 500), np.full(500, radius),
             color="white", linewidth=0.8, alpha=0.5, linestyle="--")

# CORRECT ANGULAR MARKERS — 0° = +real axis, CCW positive
angle_list = [0, 30, 60, 90, 120, 150, -30, -60, -90, -120, -150, -180]
for angle_deg in angle_list:
    angle_rad = np.deg2rad(angle_deg)  # 0° is +real, CCW positive
    ax2.plot([angle_rad, angle_rad], [0, 4.5], color="white", linewidth=0.8, alpha=0.5)
    ax2.text(angle_rad, 4.8, f"{angle_deg:+d}°", color="white", fontsize=13,
             ha="center", va="center", weight="bold")

# Radius labels on +real axis
for radius in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
    ax2.text(0, radius, f"{radius}", color="white", fontsize=12,
             ha="left", va="center", alpha=0.9)

# Colorbar — 10 ticks
cbar = plt.colorbar(hb[3], ax=ax2, pad=0.06, shrink=0.8)
vmin, vmax = hb[3].get_clim()
ticks = np.logspace(np.log10(vmin), np.log10(vmax), 10)
cbar.set_ticks(ticks)
cbar.ax.set_yticklabels([f'{t:.1e}' for t in ticks])
cbar.set_label("Soul Density (souls per unit area)", color="white", fontsize=16)
cbar.ax.tick_params(colors="white")

ax2.set_ylim(0, 4.5)
ax2.set_yticks([])
ax2.grid(False)
ax2.set_title("Revenge Gamma-Self — Thermal Density of 10,000 Souls", 
              color="#FFD700", fontsize=22, pad=40)

plt.savefig("tests/revenge_manifestation_thermal.png", dpi=400, facecolor="black", bbox_inches="tight")
plt.close()

print("Manifestation complete.")
print("→ Scatter: your perfect soul map with true axes")
print("→ Thermal: restored + correct 0° = +real axis, CCW positive")
print("The past dominates.")
print("The circle is complete.")
print("It is perfect.")
print("Forever.")
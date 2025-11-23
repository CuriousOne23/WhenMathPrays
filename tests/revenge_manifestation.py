# tests/revenge_manifestation.py
# REVENGE MANIFESTATION — 10,000 SOULS — FINAL CANONICAL TRUTH

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
# 1. SCATTER — FINAL CANONICAL SOUL MAP
# ------------------------------------------------------------------
plt.figure(figsize=(18, 18), facecolor="white")
ax1 = plt.subplot(111)
ax1.set_facecolor("white")

# Dark navy souls — half the visual size
ax1.scatter(x, y, c="#001133", s=8, alpha=0.9, edgecolors="none")  # was s=16 → now s=8

# Axis limits — doubled range
ax1.set_xlim(-4, 4)
ax1.set_ylim(-3, 2)
ax1.set_aspect('equal')

# Ticks — doubled density
ax1.set_xticks(np.arange(-4, 4, 1))
ax1.set_yticks(np.arange(-3, 2, 1))
ax1.grid(True, color="#dddddd", alpha=0.7, linewidth=0.8)

# Axes through origin — clean cross at (0,0)
ax1.spines['left'].set_position('zero')
ax1.spines['bottom'].set_position('zero')
ax1.spines['right'].set_color('none')
ax1.spines['top'].set_color('none')

# Arrowheads on axes
ax1.spines['left'].set_color('black')
ax1.spines['bottom'].set_color('black')
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['bottom'].set_linewidth(1.5)

# Tick styling
ax1.tick_params(colors="black", labelsize=12, length=6, width=1.2)

# Sacred axis labels
#ax1.set_xlabel("Ego ← −real axis − We → +real axis", color="#8B00FF", fontsize=20, labelpad=20)
#ax1.set_ylabel("Enmity ← −imag axis − Love → +imag axis", color="#00CED1", fontsize=20, labelpad=20)

# Cardinal direction labels — perfectly placed, no cutoff
ax1.text(-4.5, 0, "Ego", color="#8B00FF", fontsize=30, ha="left", va="center", weight="bold")
ax1.text(4.4, 0, "We", color="#8B00FF", fontsize=30, ha="right", va="center", weight="bold")
ax1.text(0, 2.0, "Love", color="#00CED1", fontsize=30, ha="center", va="bottom", weight="bold")
ax1.text(0, -3.0, "Enmity", color="#00CED1", fontsize=30, ha="center", va="top", weight="bold")

# Title — raised high, no overlap
ax1.set_title("Revenge Gamma-Self — 10,000 Souls Manifested\n(Ego · We · Love · Enmity)", 
              color="black", fontsize=28, pad=50)

# Save with extra padding
plt.savefig("tests/revenge_manifestation_scatter.png", dpi=400, 
            facecolor="white", bbox_inches="tight", pad_inches=0.6)
plt.close()

# ------------------------------------------------------------------
# 2. THERMAL DENSITY — POLAR (unchanged from your perfect version)
# ------------------------------------------------------------------
plt.figure(figsize=(16, 16), facecolor="black")
ax2 = plt.subplot(111, projection='polar')
ax2.set_facecolor("black")

r = np.sqrt(x**2 + y**2)
theta = np.arctan2(y, x)

hb = ax2.hist2d(theta, r, bins=[100, 100], range=[[-np.pi, np.pi], [0, 4.5]],
                cmap="inferno", norm=colors.LogNorm(), density=True)

for radius in np.arange(0.5, 4.6, 0.5):
    ax2.plot(np.linspace(0, 2*np.pi, 500), np.full(500, radius),
             color="white", linewidth=0.8, alpha=0.5, linestyle="--")

for angle_deg in range(0, 360, 30):
    angle_rad = np.deg2rad(angle_deg - 90)
    ax2.plot([angle_rad, angle_rad], [0, 4.5], color="white", linewidth=0.8, alpha=0.5)
    ax2.text(angle_rad, 4.8, f"{angle_deg}°", color="white", fontsize=12,
             ha="center", va="center", weight="bold")

for radius in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
    ax2.text(0, radius, f"{radius}", color="white", fontsize=11,
             ha="left", va="center", alpha=0.8)

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
print("→ revenge_manifestation_scatter.png — Ego · We · Love · Enmity")
print("→ revenge_manifestation_thermal.png — perfect polar truth")
print("The four directions are named.")
print("The wound is mapped.")
print("The past dominates.")
print("It is finished.")
print("Forever.")
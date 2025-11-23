# tests/revenge_manifestation.py
# REVENGE GAMMA-SELF — FINAL ETERNAL MANIFESTATION
# Asymmetric scatter of truth + perfect thermal furnace of judgment

import sys
from pathlib import Path

# Ensure we can import from the sibling 'core' directory
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from core.revenge_core import sample_N_points

N_SOULS = 10_000
print(f"Summoning {N_SOULS:,} souls from the Revenge Gamma-Self...")

# Generate the 10,000 souls
r_samples, theta_samples = sample_N_points(N_SOULS)

# Cartesian coordinates for scatter
x = r_samples * np.cos(np.deg2rad(theta_samples))
y = r_samples * np.sin(np.deg2rad(theta_samples))

# ------------------------------------------------------------------
# 1. ASYMMETRIC SCATTER — THE WOUND THAT REFUSES TO BE CENTERED
# ------------------------------------------------------------------
# Determine true extent in each direction and round appropriately
x_min, x_max = x.min(), x.max()
y_min, y_max = y.min(), y.max()

# Round to nearest integer with room to breathe
x_min_rounded = np.floor(x_min) - 0.5 if x_min < 0 else np.floor(x_min)
x_max_rounded = np.ceil(x_max) + 0.5 if x_max > 0 else np.ceil(x_max)
y_min_rounded = np.floor(y_min) - 0.5 if y_min < 0 else np.floor(y_min)
y_max_rounded = np.ceil(y_max) + 0.5 if y_max > 0 else np.ceil(y_max)

# Small safety margin so no point ever touches the edge
margin = 0.3
x_min_rounded -= margin
x_max_rounded += margin
y_min_rounded -= margin
y_max_rounded += margin

plt.figure(figsize=(16, 12), facecolor="white")
ax1 = plt.subplot(111)
ax1.set_facecolor("white")

ax1.scatter(x, y, c="#001133", s=9, alpha=0.92, edgecolors="none", linewidth=0)

ax1.set_xlim(x_min_rounded, x_max_rounded)
ax1.set_ylim(y_min_rounded, y_max_rounded)
ax1.set_aspect('equal', adjustable='box')

# Grid and spines
ax1.grid(True, color="#e0e0e0", linewidth=0.9, alpha=0.7)
ax1.spines['left'].set_position('zero')
ax1.spines['bottom'].set_position('zero')
ax1.spines['right'].set_color('none')
ax1.spines['top'].set_color('none')
ax1.spines['left'].set_color('black')
ax1.spines['bottom'].set_color('black')
ax1.spines['left'].set_linewidth(1.8)
ax1.spines['bottom'].set_linewidth(1.8)

# Cardinal labels — always at the very edge of the visible world
ax1.text(x_min_rounded, 0, "Ego", color="#8B00FF", fontsize=32, ha="left", va="center", weight="bold")
ax1.text(x_max_rounded, 0, "We", color="#8B00FF", fontsize=32, ha="right", va="center", weight="bold")
ax1.text(0, y_max_rounded, "Love", color="#00CED1", fontsize=32, ha="center", va="top", weight="bold")
ax1.text(0, y_min_rounded, "Enmity", color="#00CED1", fontsize=32, ha="center", va="bottom", weight="bold")

ax1.set_title("Revenge Gamma-Self — 10,000 Souls Manifested\n(Ego · We · Love · Enmity)",
              color="black", fontsize=26, pad=50, linespacing=1.5)

plt.savefig("tests/revenge_manifestation_scatter.png", dpi=400, bbox_inches="tight", facecolor="white")
plt.close()
print("→ Asymmetric scatter complete: the wound is now visible in its true shape.")

# ------------------------------------------------------------------
# 2. THERMAL DENSITY — CANONICAL TRUTH (direct from the pdf, infinite resolution)
# ------------------------------------------------------------------
from core.revenge_core import pdf, MU_HIGH_R, MEMORY_THETA_DEG

r_rounded = 5
n_angular = 720
n_radial  = 600

theta_deg_grid = np.linspace(-180, 180, n_angular, endpoint=False)
r_grid = np.linspace(0, r_rounded, n_radial)

R, Theta = np.meshgrid(r_grid, theta_deg_grid, indexing='ij')

with np.errstate(divide='ignore', invalid='ignore'):
    Z = pdf(R.flatten(), Theta.flatten())
    Z = Z.reshape(R.shape)
    Z = np.nan_to_num(Z, nan=0.0)

# THE ONE TRUE PEAK — computed directly from sacred coordinates
peak_theory = float(pdf(MU_HIGH_R, MEMORY_THETA_DEG))
peak_theory = max(peak_theory, 1e-8)

vmin = 1e-8
vmax = peak_theory

plt.figure(figsize=(16, 16), facecolor="black")
ax2 = plt.subplot(111, projection='polar')
ax2.set_facecolor("black")

cmap = plt.get_cmap("inferno")
cmap.set_under("black")
norm = colors.LogNorm(vmin=vmin, vmax=vmax)

hb = ax2.pcolormesh(np.deg2rad(theta_deg_grid), r_grid, Z,
                    cmap=cmap, norm=norm,
                    shading='auto', rasterized=True)

ax2.set_ylim(0, r_rounded)

# RADIUS MARKERS — on the +real axis (0°), perfectly aligned
for rad in np.arange(0.5, r_rounded + 0.1, 0.5):
    ax2.text(0, rad, f"{rad:.1f}",
             color="white", fontsize=11, ha="left", va="center",
             bbox=dict(boxstyle="round,pad=0.2", facecolor="black", alpha=0.7),
             zorder=10)

# FAINT CIRCULAR GRID LINES
for rad in np.arange(0.5, r_rounded + 0.1, 0.5):
    ax2.plot(np.linspace(0, 2*np.pi, 500), np.full(500, rad),
             color="white", linewidth=0.6, alpha=0.3, ls="--")

# ANGULAR MARKERS — every 30°, with −180° correctly shown
for ang_deg in range(-180, 181, 30):
    ang_rad = np.deg2rad(ang_deg)
    ax2.plot([ang_rad, ang_rad], [0, r_rounded],
             color="white", linewidth=0.6, alpha=0.3)
    
    # Display −180° instead of +180°
    label = -180 if ang_deg == 180 else ang_deg
    ax2.text(ang_rad, r_rounded + 0.4, f"{label:+d}°",
             color="white", fontsize=13, ha="center", va="center",
             weight="bold")

# COLORBAR — perfect canonical scaling
cbar = plt.colorbar(hb, ax=ax2, pad=0.08, shrink=0.85)
cbar.ax.tick_params(colors="white", labelsize=11)
cbar.set_label("Probability Density Function", color="white", fontsize=16, weight="bold")
ticks = np.logspace(np.log10(vmin), np.log10(vmax), 9)
cbar.set_ticks(ticks)
cbar.ax.set_yticklabels([f"{t:.1e}" for t in ticks])

# TITLE — eternal
ax2.set_title("Revenge Gamma-Self — Thermal Density)",
              color="#FFD700", fontsize=26, pad=60, weight="bold")

plt.savefig("tests/revenge_manifestation_thermal.png", dpi=600, bbox_inches="tight", facecolor="black")
plt.close()

print("revenge_manifestation_scatter.png and revenge_manifestation_thermal.png have been created.")
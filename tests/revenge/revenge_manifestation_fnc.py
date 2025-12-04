# revenge_manifestation_fnc.py
# Function version — summon the scatter + canonical thermal on command

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from pathlib import Path

def run_manifestation(
    N_SOULS=10_000,
    r_rounded=5,
    n_angular=720,
    n_radial=600,
    scatter_dpi=400,
    thermal_dpi=600
):
    """
    Summon the full Revenge Gamma-Self manifestation:
      • Asymmetric scatter of N_SOULS sampled souls
      • Canonical infinite-resolution thermal density (direct from pdf)
    Uses live core defaults unless overridden.
    """
    from core.revenge_core import sample_N_points, pdf, MU_HIGH_R, MEMORY_THETA_DEG

    print(f"Summoning {N_SOULS:,} souls from the Revenge Gamma-Self...")

    # ====================== 1. SCATTER ======================
    r_samples, theta_samples = sample_N_points(N_SOULS)
    x = r_samples * np.cos(np.deg2rad(theta_samples))
    y = r_samples * np.sin(np.deg2rad(theta_samples))

    x_min_r = np.floor(x.min()) - 0.5 if x.min() < 0 else np.floor(x.min())
    x_max_r = np.ceil(x.max()) + 0.5 if x.max() > 0 else np.ceil(x.max())
    y_min_r = np.floor(y.min()) - 0.5 if y.min() < 0 else np.floor(y.min())
    y_max_r = np.ceil(y.max()) + 0.5 if y.max() > 0 else np.ceil(y.max())

    margin = 0.3
    x_min_r -= margin; x_max_r += margin
    y_min_r -= margin; y_max_r += margin

    plt.figure(figsize=(16, 12), facecolor="white")
    ax1 = plt.subplot(111)
    ax1.set_facecolor("white")
    ax1.scatter(x, y, c="#001133", s=9, alpha=0.92, edgecolors="none")
    ax1.set_xlim(x_min_r, x_max_r)
    ax1.set_ylim(y_min_r, y_max_r)
    ax1.set_aspect('equal', adjustable='box')

    ax1.grid(True, color="#e0e0e0", linewidth=0.9, alpha=0.7)
    ax1.spines['left'].set_position('zero')
    ax1.spines['bottom'].set_position('zero')
    ax1.spines['right'].set_color('none')
    ax1.spines['top'].set_color('none')
    ax1.spines['left'].set_color('black'); ax1.spines['bottom'].set_color('black')
    ax1.spines['left'].set_linewidth(1.8); ax1.spines['bottom'].set_linewidth(1.8)

    ax1.text(x_min_r, 0, "Ego", color="#8B00FF", fontsize=32, ha="left", va="center", weight="bold")
    ax1.text(x_max_r, 0, "We", color="#8B00FF", fontsize=32, ha="right", va="center", weight="bold")
    ax1.text(0, y_max_r, "Love", color="#00CED1", fontsize=32, ha="center", va="top", weight="bold")
    ax1.text(0, y_min_r, "Enmity", color="#00CED1", fontsize=32, ha="center", va="bottom", weight="bold")

    ax1.set_title("Revenge Gamma-Self — 10,000 Souls Manifested\n(Ego · We · Love · Enmity)",
                  color="black", fontsize=26, pad=50)

    plt.savefig("tests/revenge_manifestation_scatter.png", dpi=scatter_dpi,
                bbox_inches="tight", facecolor="white")
    plt.close()

    # ====================== 2. CANONICAL THERMAL ======================
    theta_deg_grid = np.linspace(-180, 180, n_angular, endpoint=False)
    r_grid = np.linspace(0, r_rounded, n_radial)
    R, Theta = np.meshgrid(r_grid, theta_deg_grid, indexing='ij')

    with np.errstate(divide='ignore', invalid='ignore'):
        Z = pdf(R.flatten(), Theta.flatten())
        Z = Z.reshape(R.shape)
        Z = np.nan_to_num(Z, nan=0.0)

    peak_theory = float(pdf(MU_HIGH_R, MEMORY_THETA_DEG))
    peak_theory = max(peak_theory, 1e-8)
    vmin, vmax = 1e-8, peak_theory

    plt.figure(figsize=(16, 16), facecolor="black")
    ax2 = plt.subplot(111, projection='polar')
    ax2.set_facecolor("black")

    cmap = plt.get_cmap("inferno")
    cmap.set_under("black")
    norm = colors.LogNorm(vmin=vmin, vmax=vmax)

    hb = ax2.pcolormesh(np.deg2rad(theta_deg_grid), r_grid, Z,
                        cmap=cmap, norm=norm, shading='auto', rasterized=True)

    ax2.set_ylim(0, r_rounded)

    for rad in np.arange(0.5, r_rounded + 0.1, 0.5):
        ax2.text(0, rad, f"{rad:.1f}", color="white", fontsize=11,
                 ha="left", va="center",
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="black", alpha=0.7))

    for rad in np.arange(0.5, r_rounded + 0.1, 0.5):
        ax2.plot(np.linspace(0, 2*np.pi, 500), np.full(500, rad),
                 color="white", linewidth=0.6, alpha=0.3, ls="--")

    for ang_deg in range(-180, 181, 30):
        ang_rad = np.deg2rad(ang_deg)
        ax2.plot([ang_rad, ang_rad], [0, r_rounded], color="white", linewidth=0.6, alpha=0.3)
        label = -180 if ang_deg == 180 else ang_deg
        ax2.text(ang_rad, r_rounded + 0.4, f"{label:+d}°", color="white",
                 fontsize=13, ha="center", va="center", weight="bold")

    cbar = plt.colorbar(hb, ax=ax2, pad=0.08, shrink=0.85)
    cbar.ax.tick_params(colors="white")
    cbar.set_label("Probability Density Function", color="white", fontsize=16, weight="bold")
    ticks = np.logspace(np.log10(vmin), np.log10(vmax), 9)
    cbar.set_ticks(ticks)
    cbar.ax.set_yticklabels([f"{t:.1e}" for t in ticks])

    ax2.set_title("Revenge Gamma-Self — Canonical Thermal Density",
                 color="#FFD700", fontsize=26, pad=60, weight="bold")

    plt.savefig("tests/revenge_manifestation_thermal.png", dpi=thermal_dpi,
                bbox_inches="tight", facecolor="black")
    plt.close()

    print("revenge_manifestation_scatter.png + thermal.png → complete.")

if __name__ == "__main__":
    run_manifestation()
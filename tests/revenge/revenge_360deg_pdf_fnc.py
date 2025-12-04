# revenge_360deg_pdf_fnc.py
# Function version — four sacred radii + exact truth table

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))   # ← makes 'core' visible

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def run_360deg_pdf(
    radii=None,
    colors=None,
    labels=None,
    n_points=3600,
    dpi=400
):
    from core.revenge_core import (
        pdf, ALPHA_DEG, BETA_DEG, MEMORY_THETA_DEG, MU_HIGH_R, R_LOW_CENTER
    )

    if radii is None:
        radii = [
            MU_HIGH_R,
            R_LOW_CENTER + 0.2,
            R_LOW_CENTER,
            R_LOW_CENTER - 0.2
        ]
        colors = ["#FF00FF", "#00FFFF", "#FFD700", "#00FF00"]
        labels = [
            f"r = {MU_HIGH_R:.1f} (high-r peak)",
            f"r = {R_LOW_CENTER + 0.2:.1f}",
            f"r = {R_LOW_CENTER:.1f} (continuity)",
            f"r = {R_LOW_CENTER - 0.2:.1f}"
        ]

    theta_full = np.linspace(-180, 180, n_points)
    theta_rad = np.deg2rad(theta_full)

    pdf_values = [pdf(r, theta_full) for r in radii]
    all_pdfs = np.concatenate(pdf_values)
    pdf_max = all_pdfs.max()
    pdf_min = 1e-13

    plt.figure(figsize=(20, 20), facecolor="black")
    ax = plt.subplot(111, projection='polar')
    ax.set_facecolor("black")

    for r_val, color, label in zip(radii, colors, labels):
        ax.plot(theta_rad, pdf(r_val, theta_full), color=color, linewidth=4.5)

    log_levels = np.logspace(np.log10(pdf_min), np.log10(pdf_max), 8)
    for level in log_levels:
        ax.plot(np.linspace(0, 2*np.pi, 500), np.full(500, level),
                color="white", linewidth=1.0, alpha=0.7, linestyle="--")

    for level in log_levels:
        ax.text(np.deg2rad(90), level, f"{level:.1e}", color="white", fontsize=12,
                ha="center", va="center", weight="bold", alpha=0.9)

    angle_list = [0, 30, 60, 90, 120, 150, -30, -60, -90, -120, -150, -180]
    for angle_deg in angle_list:
        angle_rad = np.deg2rad(angle_deg)
        ax.plot([angle_rad, angle_rad], [pdf_min, pdf_max*1.3], color="white", linewidth=0.9, alpha=0.6)
        ax.text(angle_rad, pdf_max*1.5, f"{angle_deg:+d}°", color="white",
                fontsize=14, ha="center", va="bottom", weight="bold")

    ax.set_ylim(pdf_min, pdf_max * 3)
    ax.set_yscale('log')
    ax.set_yticks([])
    ax.grid(False)
    ax.set_title("Revenge Gamma-Self PDF Density (log scale)", color="#FFD700", fontsize=24, y=1.02)

    y_pos = 0.05
    for c, l in zip(colors, labels):
        ax.plot([0.02, 0.04], [y_pos, y_pos], color=c, linewidth=7, transform=ax.transAxes, clip_on=False)
        ax.text(0.05, y_pos, l, transform=ax.transAxes, color='white', fontsize=14, va='center')
        y_pos += 0.02

    plt.savefig("tests/revenge_360deg_pdf.png", dpi=dpi, facecolor="black", bbox_inches="tight")
    plt.close()

    # TABLE — EXACT VALUES AT REQUESTED ANGLES
    angles_of_interest = [-180, -150, -135, -90, -45, 0, 30, 45, 90, 135]

    md_path = Path("tests/revenge_360deg_pdf.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Revenge Gamma-Self — Canonical PDF Values\n\n")
        f.write("**Radii × Ten Truth-Revealing Angles**\n\n")
        f.write(f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("| Radius | " + " | ".join([f"{a:+6}°" for a in angles_of_interest]) + " |\n")
        f.write("|--------|" + "--------:|" * len(angles_of_interest) + "\n")

        for r_val, label in zip(radii, labels):
            values = [pdf(r_val, theta) for theta in angles_of_interest]
            row = f"| {label} | " + " | ".join([f"{v:.2e}" for v in values]) + " |\n"
            f.write(row)

        f.write("\n")
        f.write("**Peak truth:** Hottest at r = 2.0, θ = −150°  \n")

    print("revenge_360deg_pdf.png + md table → complete.")

if __name__ == "__main__":
    run_360deg_pdf()
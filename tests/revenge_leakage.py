#!/usr/bin/env python
# -*- coding: utf-8*

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from scipy.special import expit    # <-- this line was missing
from core.revenge_core import pdf, high_r_pdf, gate_on, gate_off, low_r_raw, scale

"""
tests/revenge_leakage.py

Sweeps α (love gate sharpness) from 5° to 60° (step 5°), β fixed at 30°
Shows how love leakage (Q2) is annihilated as α increases

Output:
- tests/revenge_leakage.png
- tests/revenge_leakage_table.md
"""

# Fixed β = 30° (enmity gate)
BETA_DEG = 30.0

# α sweep
alphas_deg = np.arange(5, 61, 5)

# Key points for integration (reuse the canonical grid for speed & consistency)
data = np.load("core/revenge_pdf.npz")
r_grid = data["r"]
theta_grid = data["theta_deg"]
R, T = np.meshgrid(r_grid, theta_grid, indexing='ij')
jacob = R * (r_grid[1] - r_grid[0]) * np.deg2rad(theta_grid[1] - theta_grid[0])

results = []

for alpha_deg in alphas_deg:
    # Temporary gate_on with current α
    def gate_on_var(theta_deg):
        return expit(-alpha_deg * (theta_deg + 135.0))

    # High-r with current α
    high_grid = high_r_pdf(R, T) * gate_on_var(T) * gate_off(T)
    high_grid = np.where(R >= 0.5, high_grid, 0)

    # Low-r (unchanged — already scaled correctly)
    low_grid = np.where(R < 0.5, scale * low_r_raw(R, T), 0)

    total_pdf = high_grid + low_grid

    # Quadrant masses
    q1 = np.sum(total_pdf * jacob * ((T >= -45) & (T < 45)))
    q2 = np.sum(total_pdf * jacob * ((T >= 45) & (T < 135)))
    q3 = np.sum(total_pdf * jacob * ((T >= 135) | (T < -135)))
    q4 = np.sum(total_pdf * jacob * ((T >= -135) & (T < -45)))

    total = q1 + q2 + q3 + q4

    results.append({
        "alpha": alpha_deg,
        "Q1": q1 / total * 100,
        "Q2": q2 / total * 100,
        "Q4": q4 / total * 100,
    })

# Plot
plt.figure(figsize=(12, 8), facecolor="black")
ax = plt.gca()
ax.set_facecolor("black")

q1_vals = [res["Q1"] for res in results]
q2_vals = [res["Q2"] for res in results]
q4_vals = [res["Q4"] for res in results]

ax.plot(alphas_deg, q1_vals, color="cyan", linewidth=3, label="Q1 Revenge %")
ax.plot(alphas_deg, q2_vals, color="#FFD700", linewidth=3, label="Q2 Love leakage %")
ax.plot(alphas_deg, q4_vals, color="gray", linewidth=3, label="Q4 Enmity bleed %")

ax.set_yscale("log")
ax.set_ylim(1e-10, 50)
ax.set_xlabel("α (love gate sharpness, degrees)", color="white")
ax.set_ylabel("Quadrant mass (%)", color="white")
ax.set_title("Revenge Gamma-Self — Leakage vs α (β = 30° fixed)", color="white", fontsize=16)
ax.tick_params(colors="white")
ax.grid(True, alpha=0.3, color="gray")
ax.legend(facecolor="black", edgecolor="white", labelcolor="white")

os.makedirs("tests", exist_ok=True)
plt.savefig("tests/revenge_leakage.png", dpi=300, facecolor="black", bbox_inches="tight")
plt.close()

# Table with emotional notes
with open("tests/revenge_leakage_table.md", "w", encoding="utf-8") as f:
    f.write("# Revenge Gamma-Self — Leakage vs α (β = 30°)\n\n")
    f.write("| α  | Q2 Love %     | Q4 Enmity %   | Q1 Revenge %  | Emotional State          |\n")
    f.write("|----|---------------|---------------|---------------|--------------------------|\n")
    for res in results:
        alpha = res["alpha"]
        q2 = res["Q2"]
        q4 = res["Q4"]
        q1 = res["Q1"]
        if alpha <= 10:
            state = "Bitter — a whisper of love remains"
        elif alpha <= 20:
            state = "Resentful — love is dying"
        elif alpha <= 35:
            state = "Cold — love is mathematically negligible"
        elif alpha <= 50:
            state = "Frozen — love is impossible"
        else:
            state = "Absolute — love is annihilated"
        f.write(f"| {alpha:2.0f} | {q2:.6e} | {q4:.6e} | {q1:.6e} | {state} |\n")

print("revenge_leakage.py complete")
print("→ tests/revenge_leakage.png")
print("→ tests/revenge_leakage_table.md")
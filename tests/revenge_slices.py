#!/usr/bin/env python
# -*- coding: utf-8*

"""
tests/revenge_slices.py

FINAL — signed radius traversals
Ego-to-We: clean signed real axis with Q3 left, Q1 right (white letters)
No notes on Ego-to-We xlabel
All quadrant labels in white
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import os

data = np.load("core/revenge_pdf.npz")
r = data["r"]
theta_deg = data["theta_deg"]
pdf_grid = data["pdf"]

# Four lines
lines = [
    {"title": "Q3-dominant line\nθ = −150° → +30°", "theta_pos": -150.0, "theta_neg": 30.0, "q_neg": "Q1", "q_pos": "Q3"},
    {"title": "Love-gate line\nθ = −135° → +45°", "theta_pos": -135.0, "theta_neg": 45.0, "q_neg": "Q1", "q_pos": "Q3"},
    {"title": "Ego-to-We axis\nθ = 180° → 0°", "theta_pos": 180.0, "theta_neg": 0.0, "real_axis": True, "q_neg": "Q1", "q_pos": "Q3"},
    {"title": "Enmity-gate line\nθ = 135° → −45°", "theta_pos": 135.0, "theta_neg": -45.0, "q_neg": "Q4", "q_pos": "Q3"},
]

# Signed radius arrays
r_pos = r
r_neg = -r[r <= 1][::-1]
r_signed = np.concatenate([r_neg, r_pos[1:]])
r_real_signed = np.concatenate([-r[::-1], r[1:]])

traversals = []
for line in lines:
    idx_pos = np.argmin(np.abs(theta_deg - line["theta_pos"]))
    idx_neg = np.argmin(np.abs(theta_deg - line["theta_neg"]))
    
    pdf_pos = pdf_grid[:, idx_pos]
    if line.get("real_axis"):
        pdf_neg = pdf_grid[:, idx_neg][::-1]
        pdf_full = np.concatenate([pdf_neg[:-1], pdf_pos])
    else:
        pdf_neg = pdf_grid[r <= 1, idx_neg][::-1]
        pdf_full = np.concatenate([pdf_neg, pdf_pos[1:]])
    
    traversals.append(pdf_full)

# Angular belt
r05_idx = np.argmin(np.abs(r - 0.5))
pdf_angular = pdf_grid[r05_idx, :]

# Plot
plt.rcParams.update({"font.size": 13})
fig = plt.figure(figsize=(26, 15), facecolor="black")
fig.suptitle("Revenge Gamma-Self – Signed-Radius Traversals & Angular Belt", color="white", fontsize=19, y=0.96)

gs = gridspec.GridSpec(2, 3, wspace=0.30, hspace=0.35)

for i in range(4):
    ax = fig.add_subplot(gs[i // 2, i % 2])
    ax.set_facecolor("black")
    
    if lines[i].get("real_axis"):
        ax.plot(r_real_signed, traversals[i], color="#FFD700", linewidth=3.5)
        ax.set_xlim(-4, 4)
        ax.set_xlabel("signed radius r", color="white")
    else:
        ax.plot(r_signed, traversals[i], color="#FFD700", linewidth=3.5)
        ax.set_xlabel("signed radius r", color="white")
    
    ax.set_yscale("log")
    ax.set_ylim(1e-12, 5 if i == 0 else 3)
    ax.set_title(lines[i]["title"], color="#00FFFF", fontsize=15, pad=25)
    ax.set_ylabel("PDF (log scale)", color="white")
    ax.tick_params(colors="white")
    ax.grid(True, alpha=0.35, color="gray")
    
    ax.axvline(0, color="white", linewidth=2, alpha=0.9)
    ax.axvline(0.5, color="cyan", linestyle="--", linewidth=1.5, alpha=0.8)
    ax.axvline(2.0, color="cyan", linestyle="--", linewidth=1.5, alpha=0.8)
    
    # White quadrant labels left/right of zero for ALL plots
    ax.text(-0.7, 1e-3, lines[i]["q_neg"], color="white", fontsize=18, ha="center", weight="bold")
    ax.text(+0.7, 1e-3, lines[i]["q_pos"], color="white", fontsize=18, ha="center", weight="bold")

# Angular belt
ax = fig.add_subplot(gs[0, 2])
ax.set_facecolor("black")
ax.plot(theta_deg, pdf_angular, color="#FFD700", linewidth=3.5)
ax.set_yscale("log")
ax.set_ylim(1e-12, pdf_angular.max() * 3)
ax.set_title("Angular distribution at r = 0.5", color="#00FFFF", fontsize=15, pad=25)
ax.set_xlabel("θ (degrees)", color="white")
ax.set_ylabel("PDF (log scale)", color="white")
ax.tick_params(colors="white")
ax.grid(True, alpha=0.35, color="gray")

for a in [-180, -90, 0, 90, 180]:
    ax.axvline(a, color="#00FFFF", linestyle="--", linewidth=1.5, alpha=0.8)

for ang, q in [(45, "Q1"), (135, "Q2"), (-135, "Q3"), (-45, "Q4")]:
    ax.text(ang, pdf_angular.max()*2, q, color="#00FFFF", fontsize=20, ha="center", va="bottom", weight="bold")

# Summary
ax = fig.add_subplot(gs[1, 2])
ax.axis("off")
note = (
    "Signed-radius convention\n"
    "positive r = Q3 side of line\n"
    "negative r = opposite quadrant (Q1/Q4)\n"
    "|r| = true distance from origin\n\n"
    "Ego-to-We axis: true signed real axis"
)
ax.text(0.05, 0.95, note, transform=ax.transAxes, color="#00FFFF", fontsize=15,
        va="top", ha="left", linespacing=1.7, fontfamily="monospace")

os.makedirs("tests", exist_ok=True)
plt.savefig("tests/revenge_slices.png", dpi=300, facecolor="black", bbox_inches="tight")
print("Final signed-radius portrait complete → tests/revenge_slices.png")
plt.close()

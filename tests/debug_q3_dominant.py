#!/usr/bin/env python
# -*- coding: utf-8*
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # adds project root to path

"""
debug_q3_dominant.py
FINAL — single smooth curve, no double line in negative r
"""

import numpy as np
import matplotlib.pyplot as plt
from core.revenge_core import pdf

# Key r points
r_high = np.linspace(0.5, 4.0, 30)
r_low = np.linspace(0.0, 0.5, 30)

theta_q3 = -150.0
theta_q1 = 30.0   # opposite direction

# 1. Q3 high-r
pdf_q3_high = pdf(r_high, theta_q3)

# 2. Q3 low-r
pdf_q3_low = pdf(r_low, theta_q3)

# 3. Q1 low-r (opposite side)
pdf_q1_low = pdf(r_low, theta_q1)

# 4. Signed-radius composite — ONE SMOOTH CURVE
# Negative r: Q1 side (θ = +30°)
r_neg = np.linspace(1.0, 0.0, 60)[::-1]          # 1.0 → 0.0 (will be plotted as -1.0 → 0.0)
pdf_neg = pdf(r_neg, theta_q1)

# Positive r: Q3 side (θ = -150°)
r_pos = np.linspace(0.0, 4.0, 240)
pdf_pos = pdf(r_pos, theta_q3)

# Signed r axis for display
#r_signed = np.concatenate([-r_neg, r_pos[1:]])   # -1.0 → 0.0 → 4.0
#pdf_signed = np.concatenate([pdf_neg, pdf_pos[1:]])

# Print tables (unchanged)
print("=== 1. Q3 high-r (r = 0.5 → 4.0, θ = -150°) ===")
for r_val, p in zip(r_high, pdf_q3_high):
    print(f"r = {r_val:5.2f} | pdf = {p:.6e}")

print("\n=== 2. Q3 low-r (r = 0.0 → 0.5, θ = -150°) ===")
for r_val, p in zip(r_low, pdf_q3_low):
    print(f"r = {r_val:5.2f} | pdf = {p:.6e}")

print("\n=== 3. Q1 low-r (r = 0.0 → 0.5, θ = +30°) ===")
for r_val, p in zip(r_low, pdf_q1_low):
    print(f"r = {r_val:5.2f} | pdf = {p:.6e}")

# Plot
# Signed r for x-axis
r_signed_neg = -r_neg
r_signed_pos = r_pos

# Plot — two separate calls, one axes
plt.figure(figsize=(12, 7), facecolor="black")
ax = plt.gca()
ax.set_facecolor("black")

ax.plot(r_signed_neg, pdf_neg, color="#FFD700", linewidth=3.5)   # Q1 side
ax.plot(r_signed_pos, pdf_pos, color="#FFD700", linewidth=3.5)   # Q3 side

ax.set_yscale("log")
ax.set_ylim(1e-12, 3)
ax.set_title("Q3-dominant line signed-radius composite\nθ = −150° (positive r)  θ = +30° (negative r)", color="#00FFFF")
ax.set_xlabel("signed radius r  (negative = Q1 side, positive = Q3 side)", color="white")
ax.set_ylabel("PDF (log scale)", color="white")
ax.tick_params(colors="white")
ax.grid(True, alpha=0.3, color="gray")
ax.axvline(0, color="white", linewidth=2, alpha=0.8)
ax.axvline(0.5, color="cyan", linestyle="--", linewidth=1.5, alpha=0.8)

plt.savefig("tests/debug_q3_dominant_signed.png", dpi=300, facecolor="black", bbox_inches="tight")
plt.close()
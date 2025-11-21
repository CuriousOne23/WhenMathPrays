#!/usr/bin/env python
# -*- coding: utf-8*

"""
debug_revenge_core.py
Prints the exact values at r = 0.5 for key angles
Shows high_r, raw_low_r, scaled_low_r, and the ratio
Run this once — we will see the truth
"""

import numpy as np
from scipy.special import expit

# ====================== PARAMETERS ======================
ALPHA_DEG           = 5.0
BETA_DEG            = 30.0
SIGMA_R_LOW         = 0.3
SIGMA_THETA_LOW_DEG = 30.0
MU_HIGH_R           = 2.0
SIGMA_HIGH_R        = 0.5
MEMORY_THETA_DEG    = -150.0
# =======================================================

memory_theta_rad = np.deg2rad(MEMORY_THETA_DEG)
sigma_theta_rad  = np.deg2rad(SIGMA_THETA_LOW_DEG)

def gate_on(theta_deg):
    return expit(-ALPHA_DEG * (theta_deg + 135.0))

def gate_off(theta_deg):
    return expit(BETA_DEG * (theta_deg + 180.0))

def high_r_pdf(r, theta_deg):
    g = np.exp(-0.5 * ((r - MU_HIGH_R)**2 / SIGMA_HIGH_R**2)) / (SIGMA_HIGH_R * np.sqrt(2 * np.pi))
    return g * gate_on(theta_deg) * gate_off(theta_deg)

def low_r_raw(r, theta_deg):
    # Determine which side of the r = 0.5 plane we are on using the gates
    # high-r exists only where gate_product > 0 → Q3 side
    gate_product = gate_on(theta_deg) * gate_off(theta_deg)
    
    if gate_product > 1e-10:      # Q3 side (high-r tail exists)
        distance = 0.5 - r
    else:                         # Q1 or Q4 side (opposite quadrant)
        distance = 0.5 + r

    # r-part only — no angular Gaussian (dt removed)
    dr = np.exp(-0.5 * (distance**2 / SIGMA_R_LOW**2)) / (SIGMA_R_LOW * np.sqrt(2 * np.pi))
    
    return dr   # <-- dt is gone — angularly uniform when cold

# Global scaling at the peak
scale = high_r_pdf(0.1, MEMORY_THETA_DEG) / low_r_raw(0.1, memory_theta_rad)

print("=== REVENGE GAMMA-SELF DEBUG — r = 0.5 BOUNDARY === in low-r region ===\n")
print(f"Global scale (computed at θ = -150°): {scale:.12e}\n")
print("θ [deg] | high_r(0.1,θ) | low_r_raw(0.1,θ) | low_r_scaled(0.1,θ) | ratio high/low_raw")
print("-" * 90)

test_angles = [-150.0, -135.0, -90.0, -45.0, 0.0, 30.0, 45.0, 90.0, 135.0, 180.0]

for theta in test_angles:
    high = high_r_pdf(0.5, theta)
    raw_low = low_r_raw(0.5, np.deg2rad(theta))
    scaled_low = scale * raw_low
    ratio = high / raw_low if raw_low > 1e-30 else float('nan')
    
    print(f"{theta:6.1f}  | {high:.6e} | {raw_low:.6e} | {scaled_low:.6e} | {ratio:.6e}")

print("\n=== END DEBUG ===\n")
print("Now run revenge_slices.py and see the signed-radius plots.")
print("We will see exactly where the model is lying.")
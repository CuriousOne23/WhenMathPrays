#!/usr/bin/env python
# -*- coding: utf-8*

"""
debug_low_r.py
Shows EXACTLY what the core's low_r_raw will do
Coarse grid of key points only
Includes +30° to prove the opposite side
No tricks — pure truth
"""

import numpy as np
from scipy.special import expit

# Parameters — must match revenge_core.py
ALPHA_DEG = 5.0
BETA_DEG = 30.0
SIGMA_R_LOW = 0.3

def gate_on(theta_deg):
    return expit(-ALPHA_DEG * (theta_deg + 135.0))

def gate_off(theta_deg):
    return expit(BETA_DEG * (theta_deg + 180.0))

def low_r_raw(r, theta_deg):
    r = np.asarray(r)
    theta_deg = np.asarray(theta_deg)
    
    gate_product = gate_on(theta_deg) * gate_off(theta_deg)

    # Past half-plane: |theta| > 90°
    is_past_side = np.abs(theta_deg) > 90
    
    # Vectorised distance
    distance = np.where(is_past_side, 0.5 - r, 0.5 + r)
    
    dr = np.exp(-0.5 * (distance**2 / SIGMA_R_LOW**2)) / (SIGMA_R_LOW * np.sqrt(2 * np.pi))
    
    return dr, is_past_side, distance, gate_product

# Key test points
test_r = [0.6, 0.5, 0.4, 0.2, 0.0]
test_theta = [-150.0, -135.0, -90.0, -45.0, 0.0, 30.0, 45.0, 90.0, 135.0, 180.0]

print("r     | theta   | is_past_side | distance | low_r_raw")
print("-" * 60)

for r_val in test_r:
    for theta in test_theta:
        val, past, dist, _ = low_r_raw(r_val, theta)
        print(f"{r_val:5.2f} | {theta:6.1f} | {str(past):>12} | {dist:8.4f} | {val:.6e}")
    print()

print("Done — these are the exact values the core will use.")
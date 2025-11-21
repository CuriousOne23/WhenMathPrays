#!/usr/bin/env python
# -*- coding: utf-8*

"""
debug_low_r.py

EXACTLY replicates how revenge_core.py sees r (r ≥ 0 always)
Shows signed-r only in the output table for visualization
No negative r in the logic — only in the display
"""

import numpy as np
from scipy.special import expit

# Parameters
ALPHA_DEG = 5.0
BETA_DEG = 30.0
SIGMA_R_LOW = 0.3
MEMORY_THETA_DEG = -150.0

def gate_on(theta_deg):
    return expit(-ALPHA_DEG * (theta_deg + 135.0))

def gate_off(theta_deg):
    return expit(BETA_DEG * (theta_deg + 180.0))

def low_r_raw(r, theta_deg):
    gate_product = gate_on(theta_deg) * gate_off(theta_deg)
    
    theta_norm = np.mod(theta_deg + 180, 360) - 180
    is_past_side = np.abs(theta_norm) > 90

    distance = np.where(is_past_side, 0.5 - r, 0.5 + r)

    dr = np.exp(-0.5 * (distance**2 / SIGMA_R_LOW**2)) / (SIGMA_R_LOW * np.sqrt(2 * np.pi))
    
    return dr, distance 

# Test points — r ≥ 0 only (exactly how core sees it)
test_r = [0.6, 0.5, 0.4, 0.2, 0.0]
test_theta = [-150.0, -135.0, -90.0, -45.0, 0.0, 30.0, 45.0, 90.0, 135.0, 180.0]

print("signed_r | actual_r | theta    | is_past_side | distance | low_r_raw")
print("-" * 75)

for actual_r in test_r:
    for theta in test_theta:
        pdf, distance = low_r_raw(actual_r, theta)
        
        # Signed r for display only — Q3 side positive, opposite side negative
        if np.abs(np.mod(theta + 180, 360) - 180) <= 90:  # rough past-side check
            signed_r = +actual_r
        else:
            signed_r = -actual_r
        
        is_past = np.abs(np.mod(theta + 180, 360) - 180) > 90
        
        print(f"{signed_r:8.2f} | {actual_r:8.2f} | {theta:6.1f} | {str(is_past):>12} | {distance:8.4f} | {pdf:.6e}")
    print()

print("This table shows exactly what the core produces (r ≥ 0)")
print("Signed r is only for display — it is how slices should map it")
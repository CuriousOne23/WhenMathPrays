#!/usr/bin/env python3
"""
Analyze calibration results and compute slope→L_mag relationship.
"""

import pandas as pd
import os


def analyze_calibration():
    """Extract and analyze calibration test results."""
    
    tests = [
        (+0.05, "Calibrate_Slope_p005"),
        (+0.15, "Calibrate_Slope_p015"),
        (+0.30, "Calibrate_Slope_p030"),
        (-0.05, "Calibrate_Slope_n005"),
        (-0.15, "Calibrate_Slope_n015"),
        (-0.30, "Calibrate_Slope_n030"),
    ]
    
    print("="*80)
    print("CALIBRATION ANALYSIS: Slope → L_mag Relationship")
    print("="*80)
    print(f"{'Slope':>8} | {'L_mag_0':>10} | {'L_mag_42':>10} | {'ΔL_mag':>10} | {'ΔL/Δγ':>10} | {'S_final':>8}")
    print("-"*80)
    
    for slope, test_name in tests:
        csv_path = f"results/{test_name}_magnitude_table.csv"
        
        if not os.path.exists(csv_path):
            print(f"{slope:+.3f}  | {'N/A':>10} | {'N/A':>10} | {'N/A':>10} | {'N/A':>10} | {'N/A':>8}")
            continue
        
        df = pd.read_csv(csv_path)
        
        # Get M1 data (first entity)
        m1_data = df[df['Entity'] == 'M1']
        
        if len(m1_data) == 0:
            print(f"{slope:+.3f}  | {'N/A':>10} | {'N/A':>10} | {'N/A':>10} | {'N/A':>10} | {'N/A':>8}")
            continue
        
        L_mag_0 = m1_data.iloc[0]['Signed_Love_Magnitude']
        L_mag_42 = m1_data.iloc[-1]['Signed_Love_Magnitude']
        gamma_0 = m1_data.iloc[0]['Gamma_Self_Mag']
        gamma_42 = m1_data.iloc[-1]['Gamma_Self_Mag']
        
        delta_L = L_mag_42 - L_mag_0
        delta_gamma = gamma_42 - gamma_0
        
        # Load debug data for S
        debug_path = f"results/{test_name}_debug_S_b.csv"
        if os.path.exists(debug_path):
            debug_df = pd.read_csv(debug_path)
            S_final = debug_df.iloc[-1]['S_M1']
        else:
            S_final = "N/A"
        
        # Compute ΔL / Δγ (how much L_mag changes per unit γ_self change)
        if abs(delta_gamma) > 0.01:
            dL_dgamma = delta_L / delta_gamma
        else:
            dL_dgamma = 0
        
        print(f"{slope:+.3f}  | {L_mag_0:10.2f} | {L_mag_42:10.2f} | {delta_L:+10.2f} | {dL_dgamma:+10.2f} | {S_final:>8}")
    
    print("="*80)
    print("\nKey Findings:")
    print("1. Positive slopes should show: ΔL_mag > 0, S_final > 0")
    print("2. Negative slopes should show: ΔL_mag < 0, S_final = 0")
    print("3. ΔL/Δγ ratio indicates primitive effectiveness")
    print("="*80)


if __name__ == "__main__":
    analyze_calibration()

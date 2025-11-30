#!/usr/bin/env python3
"""
Generate Bond Parameter Calibration Map from test results.
Creates lookup table for scenario_generator to auto-select beta_S, s_S based on:
- Duration, Slope, Expected S accumulation
"""

import pandas as pd
import os


# Test configurations used in calibration
CALIBRATION_TESTS = [
    ("Bond_Short_Mild_Low", 42, 0.05, 1.0, 5, 0.0),
    ("Bond_Short_Mild_High", 42, 0.05, 3.0, 15, 0.0),
    ("Bond_Short_Strong_Low", 42, 0.20, 1.5, 8, 0.0),
    ("Bond_Short_Strong_High", 42, 0.20, 3.5, 20, 0.0),
    ("Bond_Long_Mild_Low", 180, 0.05, 2.0, 15, 0.0),
    ("Bond_Long_Mild_High", 180, 0.05, 4.0, 40, 0.0),
    ("Bond_Long_Strong_Low", 180, 0.20, 2.5, 20, 0.0),
    ("Bond_Long_Strong_High", 180, 0.20, 5.0, 50, 0.0),
    ("Bond_Existing_Mild", 84, 0.05, 2.0, 15, 0.4),
    ("Bond_Existing_Strong", 84, 0.20, 3.0, 25, 0.4),
]


def analyze_test(name, duration, slope, beta_S_used, s_S_used, b_0_used):
    """Extract bond dynamics from a single test."""
    
    debug_csv = f"results/{name}_debug_S_b.csv"
    mag_csv = f"results/{name}_magnitude_table.csv"
    
    if not os.path.exists(debug_csv) or not os.path.exists(mag_csv):
        return None
    
    debug_df = pd.read_csv(debug_csv)
    mag_df = pd.read_csv(mag_csv)
    m1_mag = mag_df[mag_df['Entity'] == 'M1']
    
    S_final = int(debug_df.iloc[-1]['S_M1'])
    b_0 = debug_df.iloc[0]['b_M1']
    b_final = debug_df.iloc[-1]['b_M1']
    delta_b = b_final - b_0
    
    L_mag_0 = m1_mag.iloc[0]['Signed_Love_Magnitude']
    L_mag_final = m1_mag.iloc[-1]['Signed_Love_Magnitude']
    delta_L = L_mag_final - L_mag_0
    
    # Effectiveness metric: How much L_mag grew relative to trajectory
    gamma_0 = m1_mag.iloc[0]['Gamma_Self_Mag']
    gamma_final = m1_mag.iloc[-1]['Gamma_Self_Mag']
    delta_gamma = gamma_final - gamma_0
    
    effectiveness = delta_L / delta_gamma if abs(delta_gamma) > 0.01 else 0
    
    return {
        'S_final': S_final,
        'b_final': b_final,
        'delta_b': delta_b,
        'L_mag_0': L_mag_0,
        'L_mag_final': L_mag_final,
        'delta_L': delta_L,
        'effectiveness': effectiveness,
    }


def generate_calibration_map():
    """Generate calibration map table."""
    
    print("="*120)
    print("BOND PARAMETER CALIBRATION MAP")
    print("="*120)
    print(f"{'Scenario':^22} | {'Dur':>4} | {'Slope':>6} | {'βS':>5} | {'sS':>4} | {'b₀':>5} | {'S':>3} | {'Δb':>6} | {'ΔL':>8} | {'Effect':>8}")
    print("-"*120)
    
    results = []
    
    for name, duration, slope, beta_S, s_S, b_0 in CALIBRATION_TESTS:
        metrics = analyze_test(name, duration, slope, beta_S, s_S, b_0)
        
        if metrics:
            scenario_short = name.replace("Bond_", "")
            print(f"{scenario_short:^22} | {duration:4d} | {slope:+.2f} | {beta_S:5.1f} | {s_S:4.0f} | {b_0:5.2f} | "
                  f"{metrics['S_final']:3d} | {metrics['delta_b']:+6.3f} | {metrics['delta_L']:+8.1f} | {metrics['effectiveness']:+8.1f}")
            
            results.append((name, duration, slope, beta_S, s_S, b_0, metrics))
        else:
            print(f"{name:^22} | {duration:4d} | {slope:+.2f} | {beta_S:5.1f} | {s_S:4.0f} | {b_0:5.2f} | {'N/A':^3} | {'N/A':^6} | {'N/A':^8} | {'N/A':^8}")
    
    print("="*120)
    
    # Generate recommendations
    print("\n" + "="*80)
    print("CALIBRATION-BASED RECOMMENDATIONS")
    print("="*80)
    
    # Analyze by duration and slope
    short_mild = [r for r in results if r[1] < 60 and r[2] < 0.10]
    short_strong = [r for r in results if r[1] < 60 and r[2] >= 0.10]
    long_mild = [r for r in results if r[1] >= 60 and r[2] < 0.10]
    long_strong = [r for r in results if r[1] >= 60 and r[2] >= 0.10]
    
    def summarize_group(group, name):
        if not group:
            return
        beta_S_vals = [r[3] for r in group]
        s_S_vals = [r[4] for r in group]
        S_vals = [r[6]['S_final'] for r in group]
        effect_vals = [r[6]['effectiveness'] for r in group]
        
        print(f"\n{name}:")
        print(f"  beta_S range: {min(beta_S_vals):.1f} - {max(beta_S_vals):.1f}")
        print(f"  s_S range: {min(s_S_vals):.0f} - {max(s_S_vals):.0f}")
        print(f"  Expected S: {min(S_vals)} - {max(S_vals)}")
        print(f"  Effectiveness: {min(effect_vals):.1f} - {max(effect_vals):.1f}")
    
    summarize_group(short_mild, "SHORT DURATION (<60 days), MILD GROWTH (slope < 0.10)")
    summarize_group(short_strong, "SHORT DURATION (<60 days), STRONG GROWTH (slope ≥ 0.10)")
    summarize_group(long_mild, "LONG DURATION (≥60 days), MILD GROWTH (slope < 0.10)")
    summarize_group(long_strong, "LONG DURATION (≥60 days), STRONG GROWTH (slope ≥ 0.10)")
    
    print("\n" + "="*80)
    print("IMPLEMENTATION FOR scenario_generator._auto_select_breath_params()")
    print("="*80)
    print("""
# Compute average slope from M1_data and M2_data trajectories
avg_slope = calculate_average_slope(M1_data, M2_data)

if duration_days < 60:
    if avg_slope < 0.10:
        beta_S = random.uniform(1.0, 3.0)
        s_S = random.uniform(5, 15)
    else:
        beta_S = random.uniform(1.5, 3.5)
        s_S = random.uniform(8, 20)
elif duration_days < 180:
    if avg_slope < 0.10:
        beta_S = random.uniform(2.0, 4.0)
        s_S = random.uniform(15, 40)
    else:
        beta_S = random.uniform(2.5, 5.0)
        s_S = random.uniform(20, 50)
else:  # Long duration
    if avg_slope < 0.10:
        beta_S = random.uniform(3.0, 6.0)
        s_S = random.uniform(30, 80)
    else:
        beta_S = random.uniform(4.0, 8.0)
        s_S = random.uniform(40, 100)
""")
    print("="*80)


if __name__ == "__main__":
    generate_calibration_map()

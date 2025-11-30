#!/usr/bin/env python3
"""
Bond Parameter Calibration System

Generates test scenarios with varying S accumulation patterns to determine
optimal beta_S, s_S, b_0 parameters for different relationship types.

Output: Calibration map for scenario_generator to auto-select bond parameters
based on duration, slope, and S accumulation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.scenario_generator import ScenarioGenerator
import subprocess
import pandas as pd


def generate_bond_calibration_test(
    test_name: str,
    duration_days: int,
    slope: float,
    beta_S: float,
    s_S: float,
    b_0: float,
):
    """Generate a single bond calibration test scenario."""
    
    generator = ScenarioGenerator(test_name)
    
    # Calculate trajectory based on duration and slope
    days_per_event = 7  # Weekly sampling
    num_events = duration_days // days_per_event
    
    y_start = 2.0
    x_start = 0.0
    y_end = y_start + (slope * num_events)
    
    waypoints = [
        (0, x_start, y_start, 0),
        (num_events, x_start, y_end, 0),
    ]
    
    print(f"\n{'='*60}")
    print(f"Test: {test_name}")
    print(f"  Duration: {duration_days} days ({num_events} events)")
    print(f"  Slope: {slope:+.3f} per event")
    print(f"  Bond params: beta_S={beta_S}, s_S={s_S}, b_0={b_0}")
    
    result = generator.generate_scenario(
        M1_trajectory=waypoints,
        M2_trajectory=waypoints,
        max_delta_y=0.5,
        max_delta_x=0.3,
        duration_days=duration_days,
        event_sampling="weekly",
        beta_S=beta_S,
        s_S=s_S,
        b_0=b_0,
        shared_breath_prob=0.60,
        decline_score=0.0,
        m1_name="M1",
        m2_name="M1",
    )
    
    final_S = result['M1_data'][-1]['S']
    print(f"  Final S: {final_S}")
    print(f"  S rate: {final_S / duration_days:.3f} per day")
    
    return test_name, final_S


def analyze_bond_test(test_name: str, expected_S: int):
    """Compute L_mag and extract bond dynamics."""
    
    # Run magnitude computation
    result = subprocess.run(
        ['python', 'tests/compute_love_magnitude.py', test_name],
        capture_output=True,
        text=True
    )
    
    # Load results
    mag_csv = f"results/{test_name}_magnitude_table.csv"
    debug_csv = f"results/{test_name}_debug_S_b.csv"
    
    if not os.path.exists(mag_csv) or not os.path.exists(debug_csv):
        return None
    
    mag_df = pd.read_csv(mag_csv)
    debug_df = pd.read_csv(debug_csv)
    
    # Extract key metrics
    m1_data = mag_df[mag_df['Entity'] == 'M1']
    
    L_mag_0 = m1_data.iloc[0]['Signed_Love_Magnitude']
    L_mag_final = m1_data.iloc[-1]['Signed_Love_Magnitude']
    delta_L = L_mag_final - L_mag_0
    
    b_0 = debug_df.iloc[0]['b_M1']
    b_final = debug_df.iloc[-1]['b_M1']
    delta_b = b_final - b_0
    
    S_final = debug_df.iloc[-1]['S_M1']
    beta_S = debug_df.iloc[0]['beta_S']
    s_S = debug_df.iloc[0]['s_S']
    
    return {
        'L_mag_0': L_mag_0,
        'L_mag_final': L_mag_final,
        'delta_L': delta_L,
        'b_0': b_0,
        'b_final': b_final,
        'delta_b': delta_b,
        'S_final': S_final,
        'beta_S': beta_S,
        's_S': s_S,
    }


def main():
    """
    Generate bond parameter calibration tests.
    
    Test matrix:
    - Short duration (42 days) vs Long duration (180 days)
    - Mild slope (+0.05) vs Strong slope (+0.20)
    - Low beta_S (1.0) vs High beta_S (4.0)
    - Low s_S (5) vs High s_S (30)
    - Strangers (b_0=0) vs Existing bond (b_0=0.5)
    """
    
    print("="*60)
    print("BOND PARAMETER CALIBRATION SYSTEM")
    print("="*60)
    print("Mapping scenario characteristics → {beta_S, s_S, b_0}")
    print()
    
    # Test configurations: (name, duration, slope, beta_S, s_S, b_0)
    tests = [
        # Short duration, mild growth, low bond strength
        ("Bond_Short_Mild_Low", 42, 0.05, 1.0, 5, 0.0),
        
        # Short duration, mild growth, high bond strength
        ("Bond_Short_Mild_High", 42, 0.05, 3.0, 15, 0.0),
        
        # Short duration, strong growth, low bond strength
        ("Bond_Short_Strong_Low", 42, 0.20, 1.5, 8, 0.0),
        
        # Short duration, strong growth, high bond strength
        ("Bond_Short_Strong_High", 42, 0.20, 3.5, 20, 0.0),
        
        # Long duration, mild growth, low bond strength
        ("Bond_Long_Mild_Low", 180, 0.05, 2.0, 15, 0.0),
        
        # Long duration, mild growth, high bond strength
        ("Bond_Long_Mild_High", 180, 0.05, 4.0, 40, 0.0),
        
        # Long duration, strong growth, low bond strength
        ("Bond_Long_Strong_Low", 180, 0.20, 2.5, 20, 0.0),
        
        # Long duration, strong growth, high bond strength
        ("Bond_Long_Strong_High", 180, 0.20, 5.0, 50, 0.0),
        
        # Existing bond scenarios (b_0 > 0)
        ("Bond_Existing_Mild", 84, 0.05, 2.0, 15, 0.4),
        ("Bond_Existing_Strong", 84, 0.20, 3.0, 25, 0.4),
    ]
    
    print("\n" + "="*60)
    print("PHASE 1: GENERATE SCENARIOS")
    print("="*60)
    
    test_results = []
    for name, duration, slope, beta_S, s_S, b_0 in tests:
        test_name, final_S = generate_bond_calibration_test(
            name, duration, slope, beta_S, s_S, b_0
        )
        test_results.append((name, duration, slope, beta_S, s_S, b_0, final_S))
    
    print("\n" + "="*60)
    print("PHASE 2: COMPUTE BOND DYNAMICS")
    print("="*60)
    
    analysis_results = []
    for name, duration, slope, beta_S, s_S, b_0, final_S in test_results:
        print(f"\nAnalyzing {name}...")
        metrics = analyze_bond_test(name, final_S)
        if metrics:
            analysis_results.append((name, duration, slope, beta_S, s_S, b_0, metrics))
            print(f"  L_mag: {metrics['L_mag_0']:.1f} → {metrics['L_mag_final']:.1f} (Δ={metrics['delta_L']:+.1f})")
            print(f"  b: {metrics['b_0']:.3f} → {metrics['b_final']:.3f} (Δ={metrics['delta_b']:+.3f})")
            print(f"  S_final: {metrics['S_final']}")
    
    print("\n" + "="*60)
    print("CALIBRATION MAP SUMMARY")
    print("="*60)
    print(f"{'Scenario':^25} | {'Dur':>4} | {'Slope':>6} | {'βS':>5} | {'sS':>4} | {'b₀':>5} | {'S':>3} | {'Δb':>6} | {'ΔL':>8}")
    print("-"*100)
    
    for name, duration, slope, beta_S, s_S, b_0, metrics in analysis_results:
        scenario_short = name.replace("Bond_", "")
        print(f"{scenario_short:^25} | {duration:4d} | {slope:+.3f} | {beta_S:5.1f} | {s_S:4.0f} | {b_0:5.2f} | {metrics['S_final']:3.0f} | {metrics['delta_b']:+6.3f} | {metrics['delta_L']:+8.1f}")
    
    print("="*100)
    
    # Generate recommendations
    print("\n" + "="*60)
    print("AUTO-SELECTION RECOMMENDATIONS")
    print("="*60)
    
    print("\nFor scenario_generator._auto_select_breath_params():")
    print("\n1. SHORT SCENARIOS (< 60 days):")
    print("   Mild growth (slope < 0.10):")
    print("     beta_S = 1.0-3.0, s_S = 5-15")
    print("   Strong growth (slope ≥ 0.10):")
    print("     beta_S = 1.5-3.5, s_S = 8-20")
    
    print("\n2. MEDIUM SCENARIOS (60-180 days):")
    print("   Mild growth (slope < 0.10):")
    print("     beta_S = 2.0-4.0, s_S = 15-40")
    print("   Strong growth (slope ≥ 0.10):")
    print("     beta_S = 2.5-5.0, s_S = 20-50")
    
    print("\n3. LONG SCENARIOS (> 180 days):")
    print("   Mild growth (slope < 0.10):")
    print("     beta_S = 3.0-6.0, s_S = 30-80")
    print("   Strong growth (slope ≥ 0.10):")
    print("     beta_S = 4.0-8.0, s_S = 40-100")
    
    print("\n4. EXISTING BONDS (b_0 > 0):")
    print("   Use same beta_S/s_S as strangers")
    print("   Set b_0 based on relationship:")
    print("     Ex-lovers: 0.3-0.4")
    print("     Friends becoming lovers: 0.4-0.6")
    print("     Parent-child: 0.6-0.8")
    
    print("="*60)


if __name__ == "__main__":
    main()

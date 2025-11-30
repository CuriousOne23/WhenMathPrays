#!/usr/bin/env python3
"""
Calibration Test: Determine slope → {v,r,f,a,S} mapping factors

Tests 6 scenarios with controlled slopes to empirically determine
the relationship between trajectory slope and required primitive levels.

Positive slopes: +0.05, +0.15, +0.30
Negative slopes: -0.05, -0.15, -0.30

All start from (0, 2.0) for 42 days (6 events) to isolate slope effect.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.scenario_generator import ScenarioGenerator
import subprocess


def generate_slope_test(slope_value: float, test_name: str):
    """Generate a test scenario with specified constant slope."""
    
    generator = ScenarioGenerator(test_name)
    
    # Calculate end position: y_end = y_start + slope * num_events
    y_start = 2.0
    x_start = 0.0
    num_events = 6  # 42 days / 7 days per event
    y_end = y_start + (slope_value * num_events)
    
    # Simple 2-waypoint trajectory (constant slope)
    waypoints = [
        (0, x_start, y_start, 0),        # Day 0
        (num_events, x_start, y_end, 0), # Day 42
    ]
    
    print(f"\n{'='*60}")
    print(f"Test: {test_name}")
    print(f"Slope: {slope_value:+.3f} per event")
    print(f"Trajectory: ({x_start:.1f}, {y_start:.1f}) → ({x_start:.1f}, {y_end:.1f})")
    print(f"Expected Δy: {y_end - y_start:.2f} over {num_events} events")
    
    result = generator.generate_scenario(
        M1_trajectory=waypoints,
        M2_trajectory=waypoints,  # Same for both
        max_delta_y=0.5,
        max_delta_x=0.3,
        duration_days=42,
        event_sampling="weekly",
        beta_S=2.0,
        s_S=10,
        b_0=0.0,
        shared_breath_prob=0.60,
        decline_score=0.0,  # No toxicity modifier
        m1_name="M1",
        m2_name="M1",  # Same entity name
    )
    
    # Report generated primitives and S
    final_data = result['M1_data'][-1]
    avg_v = sum(d['v'] for d in result['M1_data']) / len(result['M1_data'])
    avg_r = sum(d['r'] for d in result['M1_data']) / len(result['M1_data'])
    avg_f = sum(d['f'] for d in result['M1_data']) / len(result['M1_data'])
    avg_a = sum(d['a'] for d in result['M1_data']) / len(result['M1_data'])
    
    print(f"Generated avg primitives: v={avg_v:.1f}, r={avg_r:.1f}, f={avg_f:.1f}, a={avg_a:.1f}")
    print(f"Final S: {final_data['S']}")
    print(f"S accumulation rate: {final_data['S'] / 42:.3f} per day")
    
    return test_name


def run_magnitude_computation(test_name: str):
    """Run love magnitude computation and extract results."""
    
    print(f"\nComputing L_mag for {test_name}...")
    
    result = subprocess.run(
        ['python', 'tests/compute_love_magnitude.py', test_name],
        capture_output=True,
        text=True
    )
    
    # Parse output for final L_mag
    output = result.stdout
    for line in output.split('\n'):
        if 'Day 42:' in line and 'L_mag=' in line:
            # Extract L_mag value
            parts = line.split('L_mag=')
            if len(parts) > 1:
                l_mag = float(parts[1].split()[0])
                print(f"Final L_mag: {l_mag:.2f}")
                return l_mag
    
    print("Could not parse L_mag from output")
    return None


def main():
    """Run systematic slope calibration tests."""
    
    print("="*60)
    print("SLOPE CALIBRATION TEST SUITE")
    print("="*60)
    print("Testing slope → {v,r,f,a,S} mapping factors")
    print()
    
    # Test configurations: (slope, test_name)
    tests = [
        (+0.05, "Calibrate_Slope_p005"),
        (+0.15, "Calibrate_Slope_p015"),
        (+0.30, "Calibrate_Slope_p030"),
        (-0.05, "Calibrate_Slope_n005"),
        (-0.15, "Calibrate_Slope_n015"),
        (-0.30, "Calibrate_Slope_n030"),
    ]
    
    results = []
    
    # Generate all scenarios
    print("\n" + "="*60)
    print("PHASE 1: GENERATE SCENARIOS")
    print("="*60)
    
    for slope, test_name in tests:
        generate_slope_test(slope, test_name)
    
    # Compute magnitudes
    print("\n" + "="*60)
    print("PHASE 2: COMPUTE LOVE MAGNITUDES")
    print("="*60)
    
    for slope, test_name in tests:
        l_mag = run_magnitude_computation(test_name)
        results.append((slope, test_name, l_mag))
    
    # Summary report
    print("\n" + "="*60)
    print("CALIBRATION RESULTS SUMMARY")
    print("="*60)
    print(f"{'Slope':>8} | {'Test Name':^25} | {'L_mag':>10} | {'Δγ':>8}")
    print("-"*60)
    
    for slope, test_name, l_mag in results:
        delta_gamma = slope * 6  # 6 events
        l_mag_str = f"{l_mag:.2f}" if l_mag else "N/A"
        print(f"{slope:+.3f}  | {test_name:25} | {l_mag_str:>10} | {delta_gamma:+.2f}")
    
    print("="*60)
    print("\nAnalysis:")
    print("- Compare L_mag growth/decline rates to slope values")
    print("- Check if primitives scale linearly with slope")
    print("- Verify S accumulation correlates with positive slopes")
    print("- Use results to refine slope→primitive mapping factors")
    print("="*60)


if __name__ == "__main__":
    main()

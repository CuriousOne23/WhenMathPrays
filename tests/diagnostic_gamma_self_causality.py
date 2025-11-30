#!/usr/bin/env python3
"""
Diagnostic: Test if generated primitives {v,r,f,a,S,b} actually CAUSE the specified γ_self trajectory.

This test reveals the disconnect between:
- Specified γ_self waypoints (what we want)
- Generated primitives from scenario_generator.py
- Actual γ_self trajectory when primitives are fed through UREP equations (what we get)

Test Cases:
1. Simple upward step (love increasing)
2. Simple downward step (love decreasing)
3. Flat trajectory (no change)
4. Linear rise (steady growth)

For each case, we measure:
- Specified Δγ_self (target)
- Actual Δγ_self from UREP (result)
- Mismatch percentage
- Which primitives/parameters need adjustment
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scripts.scenario_generator import ScenarioGenerator


def test_case_1_upward_step():
    """Test Case 1: Simple upward love step."""
    print("\n" + "="*70)
    print("TEST CASE 1: Upward Step (Love Increasing)")
    print("="*70)
    
    # Specify desired trajectory
    waypoints = [
        (0, -1.0, 1.0),   # Week 0: Moderate love
        (4, -1.2, 2.5),   # Week 4: Strong love (Δy = +1.5)
    ]
    
    print(f"\nSpecified trajectory:")
    print(f"  Week 0: γ_self = ({waypoints[0][1]:.2f}, {waypoints[0][2]:.2f})")
    print(f"  Week 4: γ_self = ({waypoints[1][1]:.2f}, {waypoints[1][2]:.2f})")
    
    target_dx = waypoints[1][1] - waypoints[0][1]
    target_dy = waypoints[1][2] - waypoints[0][2]
    print(f"  Target Δγ_self = ({target_dx:.2f}, {target_dy:.2f})")
    
    # Generate scenario
    generator = ScenarioGenerator("Diagnostic_Upward")
    M1_waypoints = [(w, x, y, 0) for w, x, y in waypoints]
    M2_waypoints = [(w, x-0.3, y-0.2, 0) for w, x, y in waypoints]
    
    result = generator.generate_scenario(
        M1_trajectory=M1_waypoints,
        M2_trajectory=M2_waypoints,
        duration_days=28,
        event_sampling="weekly",
        beta_S=None,  # Auto-select
        s_S=None,
        b_0=0.3,
        shared_breath_prob=0.65,
        m1_name="M1",
        m2_name="M2",
    )
    
    # Extract generated primitives
    M1_data = result['M1_data']
    
    print(f"\nGenerated primitives (sample from M1):")
    for i in [0, len(M1_data)//2, -1]:
        d = M1_data[i]
        print(f"  Day {d['day']:3d}: v={d['v']:4.0f}, r={d['r']:4.0f}, f={d['f']:4.0f}, a={d['a']:4.0f}, S={d['S']:.3f}, b={d.get('b', 'N/A')}")
    
    # Check actual trajectory from scenario_generator
    actual_start = (M1_data[0]['x'], M1_data[0]['y'])
    actual_end = (M1_data[-1]['x'], M1_data[-1]['y'])
    actual_dx = actual_end[0] - actual_start[0]
    actual_dy = actual_end[1] - actual_start[1]
    
    print(f"\nActual trajectory from scenario_generator:")
    print(f"  Day  0: γ_self = ({actual_start[0]:.2f}, {actual_start[1]:.2f})")
    print(f"  Day 28: γ_self = ({actual_end[0]:.2f}, {actual_end[1]:.2f})")
    print(f"  Actual Δγ_self = ({actual_dx:.2f}, {actual_dy:.2f})")
    
    # Calculate mismatch
    error_x = abs(actual_dx - target_dx)
    error_y = abs(actual_dy - target_dy)
    error_pct_x = (error_x / abs(target_dx)) * 100 if target_dx != 0 else 0
    error_pct_y = (error_y / abs(target_dy)) * 100 if target_dy != 0 else 0
    
    print(f"\nMismatch:")
    print(f"  Δx error: {error_x:.3f} ({error_pct_x:.1f}%)")
    print(f"  Δy error: {error_y:.3f} ({error_pct_y:.1f}%)")
    
    if error_pct_y > 5.0:
        print(f"  ⚠️  ERROR EXCEEDS ±5% TOLERANCE")
    else:
        print(f"  ✓ Within ±5% tolerance")
    
    # TODO: Run primitives through UREP to verify causality
    print(f"\n[TODO: Run primitives through UREP equations to verify they CAUSE this trajectory]")
    
    return {
        'test': 'upward_step',
        'target_dy': target_dy,
        'actual_dy': actual_dy,
        'error_pct': error_pct_y
    }


def test_case_2_downward_step():
    """Test Case 2: Simple downward love step."""
    print("\n" + "="*70)
    print("TEST CASE 2: Downward Step (Love Decreasing)")
    print("="*70)
    
    # Specify desired trajectory
    waypoints = [
        (0, -1.5, 2.0),   # Week 0: Strong love
        (4, -0.5, 0.5),   # Week 4: Weak love (Δy = -1.5)
    ]
    
    print(f"\nSpecified trajectory:")
    print(f"  Week 0: γ_self = ({waypoints[0][1]:.2f}, {waypoints[0][2]:.2f})")
    print(f"  Week 4: γ_self = ({waypoints[1][1]:.2f}, {waypoints[1][2]:.2f})")
    
    target_dx = waypoints[1][1] - waypoints[0][1]
    target_dy = waypoints[1][2] - waypoints[0][2]
    print(f"  Target Δγ_self = ({target_dx:.2f}, {target_dy:.2f})")
    
    # Generate scenario
    generator = ScenarioGenerator("Diagnostic_Downward")
    M1_waypoints = [(w, x, y, 0) for w, x, y in waypoints]
    M2_waypoints = [(w, x-0.2, y-0.3, 0) for w, x, y in waypoints]
    
    result = generator.generate_scenario(
        M1_trajectory=M1_waypoints,
        M2_trajectory=M2_waypoints,
        duration_days=28,
        event_sampling="weekly",
        beta_S=None,
        s_S=None,
        b_0=0.4,
        shared_breath_prob=0.55,
        decline_score=-3.0,  # Moderate decline
        m1_name="M1",
        m2_name="M2",
    )
    
    # Extract generated primitives
    M1_data = result['M1_data']
    
    print(f"\nGenerated primitives (sample from M1):")
    for i in [0, len(M1_data)//2, -1]:
        d = M1_data[i]
        print(f"  Day {d['day']:3d}: v={d['v']:4.0f}, r={d['r']:4.0f}, f={d['f']:4.0f}, a={d['a']:4.0f}, S={d['S']:.3f}")
    
    # Check actual trajectory
    actual_start = (M1_data[0]['x'], M1_data[0]['y'])
    actual_end = (M1_data[-1]['x'], M1_data[-1]['y'])
    actual_dx = actual_end[0] - actual_start[0]
    actual_dy = actual_end[1] - actual_start[1]
    
    print(f"\nActual trajectory from scenario_generator:")
    print(f"  Day  0: γ_self = ({actual_start[0]:.2f}, {actual_start[1]:.2f})")
    print(f"  Day 28: γ_self = ({actual_end[0]:.2f}, {actual_end[1]:.2f})")
    print(f"  Actual Δγ_self = ({actual_dx:.2f}, {actual_dy:.2f})")
    
    # Calculate mismatch
    error_x = abs(actual_dx - target_dx)
    error_y = abs(actual_dy - target_dy)
    error_pct_x = (error_x / abs(target_dx)) * 100 if target_dx != 0 else 0
    error_pct_y = (error_y / abs(target_dy)) * 100 if target_dy != 0 else 0
    
    print(f"\nMismatch:")
    print(f"  Δx error: {error_x:.3f} ({error_pct_x:.1f}%)")
    print(f"  Δy error: {error_y:.3f} ({error_pct_y:.1f}%)")
    
    if error_pct_y > 5.0:
        print(f"  ⚠️  ERROR EXCEEDS ±5% TOLERANCE")
    else:
        print(f"  ✓ Within ±5% tolerance")
    
    return {
        'test': 'downward_step',
        'target_dy': target_dy,
        'actual_dy': actual_dy,
        'error_pct': error_pct_y
    }


def test_case_3_flat():
    """Test Case 3: Flat trajectory (no change)."""
    print("\n" + "="*70)
    print("TEST CASE 3: Flat Trajectory (No Change)")
    print("="*70)
    
    # Specify desired trajectory
    waypoints = [
        (0, -1.0, 1.5),   # Week 0
        (4, -1.0, 1.5),   # Week 4: Same (Δy = 0)
    ]
    
    print(f"\nSpecified trajectory:")
    print(f"  Week 0: γ_self = ({waypoints[0][1]:.2f}, {waypoints[0][2]:.2f})")
    print(f"  Week 4: γ_self = ({waypoints[1][1]:.2f}, {waypoints[1][2]:.2f})")
    print(f"  Target Δγ_self = (0.00, 0.00)")
    
    # Generate scenario
    generator = ScenarioGenerator("Diagnostic_Flat")
    M1_waypoints = [(w, x, y, 0) for w, x, y in waypoints]
    M2_waypoints = [(w, x-0.1, y-0.1, 0) for w, x, y in waypoints]
    
    result = generator.generate_scenario(
        M1_trajectory=M1_waypoints,
        M2_trajectory=M2_waypoints,
        duration_days=28,
        event_sampling="weekly",
        beta_S=None,
        s_S=None,
        b_0=0.35,
        shared_breath_prob=0.60,
        m1_name="M1",
        m2_name="M2",
    )
    
    # Extract generated primitives
    M1_data = result['M1_data']
    
    print(f"\nGenerated primitives (sample from M1):")
    for i in [0, len(M1_data)//2, -1]:
        d = M1_data[i]
        print(f"  Day {d['day']:3d}: v={d['v']:4.0f}, r={d['r']:4.0f}, f={d['f']:4.0f}, a={d['a']:4.0f}, S={d['S']:.3f}")
    
    # Check actual trajectory
    actual_start = (M1_data[0]['x'], M1_data[0]['y'])
    actual_end = (M1_data[-1]['x'], M1_data[-1]['y'])
    actual_dx = actual_end[0] - actual_start[0]
    actual_dy = actual_end[1] - actual_start[1]
    
    print(f"\nActual trajectory from scenario_generator:")
    print(f"  Day  0: γ_self = ({actual_start[0]:.2f}, {actual_start[1]:.2f})")
    print(f"  Day 28: γ_self = ({actual_end[0]:.2f}, {actual_end[1]:.2f})")
    print(f"  Actual Δγ_self = ({actual_dx:.2f}, {actual_dy:.2f})")
    
    # Calculate mismatch
    error_magnitude = np.sqrt(actual_dx**2 + actual_dy**2)
    
    print(f"\nMismatch:")
    print(f"  Movement magnitude: {error_magnitude:.3f}")
    
    if error_magnitude > 0.10:  # Allow 0.1 units drift for "flat"
        print(f"  ⚠️  SIGNIFICANT DRIFT (should be ~0)")
    else:
        print(f"  ✓ Minimal drift")
    
    return {
        'test': 'flat',
        'target_dy': 0.0,
        'actual_dy': actual_dy,
        'error_magnitude': error_magnitude
    }


def test_case_4_linear_rise():
    """Test Case 4: Linear rise over longer period."""
    print("\n" + "="*70)
    print("TEST CASE 4: Linear Rise (Steady Growth)")
    print("="*70)
    
    # Specify desired trajectory
    waypoints = [
        (0, -0.5, 0.5),    # Week 0
        (4, -1.0, 1.5),    # Week 4: Δy = +1.0
        (8, -1.5, 2.5),    # Week 8: Δy = +2.0 total
    ]
    
    print(f"\nSpecified trajectory:")
    for w, x, y in waypoints:
        print(f"  Week {w}: γ_self = ({x:.2f}, {y:.2f})")
    
    target_dy = waypoints[-1][2] - waypoints[0][2]
    print(f"  Target total Δy = {target_dy:.2f}")
    
    # Generate scenario
    generator = ScenarioGenerator("Diagnostic_Linear")
    M1_waypoints = [(w, x, y, 0) for w, x, y in waypoints]
    M2_waypoints = [(w, x-0.2, y-0.2, 0) for w, x, y in waypoints]
    
    result = generator.generate_scenario(
        M1_trajectory=M1_waypoints,
        M2_trajectory=M2_waypoints,
        duration_days=56,
        event_sampling="weekly",
        beta_S=None,
        s_S=None,
        b_0=0.25,
        shared_breath_prob=0.70,
        m1_name="M1",
        m2_name="M2",
    )
    
    # Extract generated primitives
    M1_data = result['M1_data']
    
    print(f"\nGenerated primitives (sample from M1):")
    for i in [0, len(M1_data)//3, 2*len(M1_data)//3, -1]:
        d = M1_data[i]
        print(f"  Day {d['day']:3d}: v={d['v']:4.0f}, r={d['r']:4.0f}, f={d['f']:4.0f}, a={d['a']:4.0f}, S={d['S']:.3f}")
    
    # Check actual trajectory
    actual_start = (M1_data[0]['x'], M1_data[0]['y'])
    actual_end = (M1_data[-1]['x'], M1_data[-1]['y'])
    actual_dy = actual_end[1] - actual_start[1]
    
    print(f"\nActual trajectory from scenario_generator:")
    print(f"  Day  0: γ_self = ({actual_start[0]:.2f}, {actual_start[1]:.2f})")
    print(f"  Day 56: γ_self = ({actual_end[0]:.2f}, {actual_end[1]:.2f})")
    print(f"  Actual Δy = {actual_dy:.2f}")
    
    # Calculate mismatch
    error_y = abs(actual_dy - target_dy)
    error_pct_y = (error_y / abs(target_dy)) * 100 if target_dy != 0 else 0
    
    print(f"\nMismatch:")
    print(f"  Δy error: {error_y:.3f} ({error_pct_y:.1f}%)")
    
    if error_pct_y > 5.0:
        print(f"  ⚠️  ERROR EXCEEDS ±5% TOLERANCE")
    else:
        print(f"  ✓ Within ±5% tolerance")
    
    return {
        'test': 'linear_rise',
        'target_dy': target_dy,
        'actual_dy': actual_dy,
        'error_pct': error_pct_y
    }


def main():
    """Run all diagnostic tests."""
    print("="*70)
    print("DIAGNOSTIC: γ_self Causality Check")
    print("Testing if generated primitives actually CAUSE specified trajectories")
    print("="*70)
    
    results = []
    
    # Run test cases
    results.append(test_case_1_upward_step())
    results.append(test_case_2_downward_step())
    results.append(test_case_3_flat())
    results.append(test_case_4_linear_rise())
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for r in results:
        if 'error_pct' in r:
            status = "✓" if r['error_pct'] <= 5.0 else "⚠️"
            print(f"{status} {r['test']:20s}: Target Δy={r['target_dy']:+6.2f}, Actual={r['actual_dy']:+6.2f}, Error={r['error_pct']:5.1f}%")
        else:
            print(f"  {r['test']:20s}: Drift magnitude={r['error_magnitude']:.3f}")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("1. If errors > 5%, we need to adjust primitive generation")
    print("2. Run primitives through UREP equations to verify causality")
    print("3. Build sensitivity map: Δ(v,r,f,a,S,b) → Δγ_self")
    print("4. Create inverse solver: Target Δγ_self → Required (v,r,f,a,S,b)")
    print("="*70)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Regenerate Test1_Linear scenario using slope-based primitive generation.

Original trajectory:
- M1: (-2.5, 0.5) → (-0.7, 2.75) over 84 days
- M2: (-2.0, 1.0) → (-1.0, 2.0) over 84 days

Expected slope: ~0.027 per event (positive, should trigger high primitives + S)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.scenario_generator import ScenarioGenerator


def regenerate_test1_linear():
    """Regenerate Test1_Linear with slope-based algorithm."""
    
    generator = ScenarioGenerator("Test1_Linear")
    
    # Original waypoints - linear growth trajectories
    M1_waypoints = [
        (0, -2.5, 0.5, 0),      # Day 0: Starting position
        (6, -1.5, 1.5, 0.3),    # Day 42: Midpoint
        (12, -0.7, 2.75, 0.2),  # Day 84: Final position
    ]
    
    M2_waypoints = [
        (0, -2.0, 1.0, 0),      # Day 0: Starting position
        (6, -1.5, 1.5, 0.3),    # Day 42: Converging
        (12, -1.0, 2.0, 0.2),   # Day 84: Final position
    ]
    
    # Calculate expected slopes
    m1_slope_seg1 = (1.5 - 0.5) / 6  # = 0.167 per event (strong growth)
    m1_slope_seg2 = (2.75 - 1.5) / 6  # = 0.208 per event (strong growth)
    m2_slope_seg1 = (1.5 - 1.0) / 6  # = 0.083 per event (moderate growth)
    m2_slope_seg2 = (2.0 - 1.5) / 6  # = 0.083 per event (moderate growth)
    
    print("Expected Slopes:")
    print(f"  M1 Segment 1: {m1_slope_seg1:.3f} per event (strong growth)")
    print(f"  M1 Segment 2: {m1_slope_seg2:.3f} per event (strong growth)")
    print(f"  M2 Segment 1: {m2_slope_seg1:.3f} per event (moderate growth)")
    print(f"  M2 Segment 2: {m2_slope_seg2:.3f} per event (moderate growth)")
    print()
    
    result = generator.generate_scenario(
        M1_trajectory=M1_waypoints,
        M2_trajectory=M2_waypoints,
        max_delta_y=0.5,
        max_delta_x=0.3,
        duration_days=84,
        event_sampling="weekly",
        beta_S=2.0,
        s_S=10,
        b_0=0.0,  # Strangers
        shared_breath_prob=0.60,
        decline_score=0.0,  # No toxicity
        m1_name="M1",
        m2_name="M2",
    )
    
    print("\n=== Test1_Linear Regenerated ===")
    print(f"M1 trajectory: ({result['M1_data'][0]['x']:.2f}, {result['M1_data'][0]['y']:.2f}) → ({result['M1_data'][-1]['x']:.2f}, {result['M1_data'][-1]['y']:.2f})")
    print(f"M2 trajectory: ({result['M2_data'][0]['x']:.2f}, {result['M2_data'][0]['y']:.2f}) → ({result['M2_data'][-1]['x']:.2f}, {result['M2_data'][-1]['y']:.2f})")
    print(f"\nFinal S: M1={result['M1_data'][-1]['S']}, M2={result['M2_data'][-1]['S']}")
    print(f"\nFinal primitives M1: v={result['M1_data'][-1]['v']:.0f}, r={result['M1_data'][-1]['r']:.0f}, f={result['M1_data'][-1]['f']:.0f}, a={result['M1_data'][-1]['a']:.0f}")
    print(f"Final primitives M2: v={result['M2_data'][-1]['v']:.0f}, r={result['M2_data'][-1]['r']:.0f}, f={result['M2_data'][-1]['f']:.0f}, a={result['M2_data'][-1]['a']:.0f}")
    
    # Show sample of primitives over time
    print("\n=== Sample Primitives Timeline (M1) ===")
    print("Event | Slope  | v    | r    | f    | a    | S")
    print("------|--------|------|------|------|------|----")
    for i in [0, 3, 6, 9, 12]:
        if i < len(result['M1_data']):
            d = result['M1_data'][i]
            # Determine slope for this event
            if i <= 6:
                slope = m1_slope_seg1
            else:
                slope = m1_slope_seg2
            print(f"{i:5d} | {slope:+.3f} | {d['v']:4.0f} | {d['r']:4.0f} | {d['f']:4.0f} | {d['a']:4.0f} | {d['S']:3d}")
    
    print("\n✓ Test1_Linear regenerated with slope-based primitives")
    print("  Run: python tests/compute_love_magnitude.py to verify L_mag grows")


if __name__ == "__main__":
    regenerate_test1_linear()

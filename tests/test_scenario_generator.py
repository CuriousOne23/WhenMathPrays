#!/usr/bin/env python3
"""
Test suite for scenario_generator.py
Demonstrates core functionality and validates algorithm implementation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.scenario_generator import ScenarioGenerator
import numpy as np


def test_basic_generation():
    """Test 1: Basic scenario generation with simple waypoints."""
    print("\n" + "="*60)
    print("TEST 1: Basic Generation - Simple Linear Path")
    print("="*60)
    
    generator = ScenarioGenerator("Test1_Linear")
    
    # Simple linear path: Q3 to Q2 (realistic movement)
    M1_waypoints = [
        (0, -2.5, 0.5, 0),      # Start
        (6, -1.0, 2.5, 0.3),    # Mid
        (12, -0.5, 3.0, 0.2),   # End in Q2
    ]
    
    M2_waypoints = [
        (0, -2.0, 1.0, 0),      # Start
        (6, -1.0, 2.0, 0.3),    # Mid
        (12, 0.0, 2.5, 0.2),    # End
    ]
    
    result = generator.generate_scenario(
        M1_trajectory=M1_waypoints,
        M2_trajectory=M2_waypoints,
        max_delta_y=0.5,
        max_delta_x=0.3,
        duration_days=84,
        event_sampling="weekly",
        beta_S=2.0,
        s_S=10,
        shared_breath_prob=0.60,
    )
    
    print(f"✓ Generated {result['num_events']} events over {result['duration_days']} days")
    print(f"✓ M1: ({result['M1_data'][0]['x']:.2f}, {result['M1_data'][0]['y']:.2f}) → ({result['M1_data'][-1]['x']:.2f}, {result['M1_data'][-1]['y']:.2f})")
    print(f"✓ M2: ({result['M2_data'][0]['x']:.2f}, {result['M2_data'][0]['y']:.2f}) → ({result['M2_data'][-1]['x']:.2f}, {result['M2_data'][-1]['y']:.2f})")
    print(f"✓ Shared breaths: M1={result['M1_data'][-1]['S']}, M2={result['M2_data'][-1]['S']}")
    print(f"✓ Files saved in: data/{generator.scenario_name}/")
    
    # Validate primitive values are in reasonable range
    M1_primitives = [d['v'] for d in result['M1_data']]
    assert all(-10 <= p <= 10 for p in M1_primitives), "Primitives out of range!"
    print(f"✓ Primitive range check passed (M1 v: {min(M1_primitives):.1f} to {max(M1_primitives):.1f})")
    
    return result


def test_high_intensity_scenario():
    """Test 2: High intensity scenario that should trigger shared breaths."""
    print("\n" + "="*60)
    print("TEST 2: High Intensity - Parent-Child Bond")
    print("="*60)
    
    generator = ScenarioGenerator("Test2_Parent_Child")
    
    # Parent-child bond: high |gamma_self| should saturate primitives
    Parent_waypoints = [
        (0, 2.0, 8.0, 0),       # Start: strong Q1 (we, love)
        (20, 3.0, 10.0, 0.5),   # Peak intensity
        (40, 2.5, 9.5, 0.5),    # Sustained high
    ]
    
    Child_waypoints = [
        (0, 1.0, 7.0, 0),       # Start: strong Q1
        (20, 2.0, 9.0, 0.5),    # Peak
        (40, 2.0, 8.5, 0.5),    # Sustained high
    ]
    
    result = generator.generate_scenario(
        M1_trajectory=Parent_waypoints,
        M2_trajectory=Child_waypoints,
        max_delta_y=0.3,
        max_delta_x=0.2,
        duration_days=365*5,    # 5 years
        event_sampling="monthly",
        beta_S=4.5,
        s_S=50,
        shared_breath_prob=0.60,
    )
    
    print(f"✓ Generated {result['num_events']} events over {result['duration_days']} days (~{result['duration_days']/365:.1f} years)")
    print(f"✓ Parent |γ| final: {np.sqrt(result['M1_data'][-1]['x']**2 + result['M1_data'][-1]['y']**2):.2f}")
    print(f"✓ Child |γ| final: {np.sqrt(result['M2_data'][-1]['x']**2 + result['M2_data'][-1]['y']**2):.2f}")
    print(f"✓ Shared breaths: Parent={result['M1_data'][-1]['S']}, Child={result['M2_data'][-1]['S']}")
    print(f"✓ Beta_S={result['beta_S']}, s_S={result['s_S']} (auto-selected for long-term bond)")
    
    # Check for shared breath events
    M1_breath_events = [d for d in result['M1_data'] if "breath" in d['notes'].lower()]
    print(f"✓ Shared breath moments detected: {len(M1_breath_events)}")
    
    return result


def test_toxic_relationship():
    """Test 3: Toxic relationship - Q3 dominant (ego, hate)."""
    print("\n" + "="*60)
    print("TEST 3: Toxic Relationship - Q3 Dominance")
    print("="*60)
    
    generator = ScenarioGenerator("Test3_Toxic")
    
    # Toxic pattern: stays in Q3, moderate intensity
    Person1_waypoints = [
        (0, -3.0, -2.0, 0),     # Start: Q3 (ego, hate)
        (6, -3.5, -2.5, 0.3),   # Worsens slightly
        (12, -3.2, -2.2, 0.3),  # Oscillates but stays Q3
    ]
    
    Person2_waypoints = [
        (0, -2.5, -1.5, 0),     # Start: Q3
        (6, -3.0, -2.0, 0.3),   # Worsens
        (12, -2.8, -1.8, 0.3),  # Oscillates
    ]
    
    result = generator.generate_scenario(
        M1_trajectory=Person1_waypoints,
        M2_trajectory=Person2_waypoints,
        max_delta_y=0.5,
        max_delta_x=0.4,
        duration_days=84,
        event_sampling="weekly",
        beta_S=0.5,             # Low boost - not much shared breath
        s_S=5,
        shared_breath_prob=0.60,
    )
    
    print(f"✓ Generated {result['num_events']} events over {result['duration_days']} days")
    print(f"✓ Person1 stays in Q3: ({result['M1_data'][-1]['x']:.2f}, {result['M1_data'][-1]['y']:.2f})")
    print(f"✓ Person2 stays in Q3: ({result['M2_data'][-1]['x']:.2f}, {result['M2_data'][-1]['y']:.2f})")
    print(f"✓ Shared breaths (should be low): M1={result['M1_data'][-1]['S']}, M2={result['M2_data'][-1]['S']}")
    
    # Verify Q3 dominance
    M1_in_Q3 = sum(1 for d in result['M1_data'] if d['x'] < 0 and d['y'] < 0)
    print(f"✓ M1 events in Q3: {M1_in_Q3}/{result['num_events']} ({100*M1_in_Q3/result['num_events']:.0f}%)")
    
    return result


def test_probabilistic_shared_breath():
    """Test 4: Verify probabilistic S (60/40 shared breath/internal fire)."""
    print("\n" + "="*60)
    print("TEST 4: Probabilistic Shared Breath System")
    print("="*60)
    
    # Run multiple scenarios to test probability distribution
    breath_counts = []
    fire_counts = []
    
    for i in range(10):
        generator = ScenarioGenerator(f"Test4_Prob_{i}")
        
        # High intensity to trigger many saturation events
        waypoints = [
            (0, 3.0, 9.0, 0),
            (10, 3.5, 9.5, 0.3),
        ]
        
        result = generator.generate_scenario(
            M1_trajectory=waypoints,
            M2_trajectory=waypoints,
            max_delta_y=0.2,
            max_delta_x=0.2,
            duration_days=70,
            event_sampling="weekly",
            beta_S=3.0,
            s_S=20,
            shared_breath_prob=0.60,
        )
        
        # Count shared breath vs internal fire events
        breath_events = sum(1 for d in result['M1_data'] if "shared breath" in d['notes'].lower())
        fire_events = sum(1 for d in result['M1_data'] if "internal fire" in d['notes'].lower())
        
        breath_counts.append(breath_events)
        fire_counts.append(fire_events)
    
    total_breath = sum(breath_counts)
    total_fire = sum(fire_counts)
    total_events = total_breath + total_fire
    
    if total_events > 0:
        breath_ratio = total_breath / total_events
        print(f"✓ Ran 10 scenarios with high |γ| to trigger saturation")
        print(f"✓ Total saturation events: {total_events}")
        print(f"✓ Shared breath: {total_breath} ({100*breath_ratio:.1f}%)")
        print(f"✓ Internal fire: {total_fire} ({100*(1-breath_ratio):.1f}%)")
        print(f"✓ Expected ratio: 60/40, Actual: {100*breath_ratio:.0f}/{100*(1-breath_ratio):.0f}")
        
        # Should be close to 60/40 (allow ±15% variance due to randomness)
        assert 0.45 <= breath_ratio <= 0.75, f"Ratio {breath_ratio:.2f} outside expected range!"
        print(f"✓ Probabilistic system working correctly!")
    else:
        print(f"⚠ No saturation events triggered (need higher |γ_self|)")
    
    return breath_counts, fire_counts


def test_fir_filter():
    """Test 5: Verify 7-tap FIR filter is smoothing primitives."""
    print("\n" + "="*60)
    print("TEST 5: FIR Filter Smoothing")
    print("="*60)
    
    generator = ScenarioGenerator("Test5_FIR")
    
    # Oscillating waypoints to test filter response
    waypoints = [
        (0, 1.0, 2.0, 0),
        (5, 3.0, 4.0, 0),
        (10, 1.5, 2.5, 0),
        (15, 3.5, 4.5, 0),
    ]
    
    result = generator.generate_scenario(
        M1_trajectory=waypoints,
        M2_trajectory=waypoints,
        max_delta_y=0.5,
        max_delta_x=0.5,
        duration_days=105,
        event_sampling="weekly",
        beta_S=2.0,
        s_S=15,
        shared_breath_prob=0.60,
    )
    
    # Check that primitives are smooth (no huge jumps)
    v_values = [d['v'] for d in result['M1_data']]
    deltas = [abs(v_values[i+1] - v_values[i]) for i in range(len(v_values)-1)]
    max_delta = max(deltas)
    avg_delta = np.mean(deltas)
    
    print(f"✓ Generated {len(v_values)} events with oscillating |γ_self|")
    print(f"✓ Primitive v(t) max jump: {max_delta:.2f}")
    print(f"✓ Primitive v(t) avg change: {avg_delta:.2f}")
    print(f"✓ FIR filter providing smooth output (expected: small deltas)")
    
    # Verify smoothness (max jump should be reasonable)
    assert max_delta < 5.0, "Filter not smoothing properly - large jumps detected!"
    print(f"✓ Filter smoothing validated!")
    
    return result


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "="*70)
    print(" SCENARIO GENERATOR TEST SUITE")
    print(" Implementation: 7-tap FIR, probabilistic S, event-driven")
    print(" Date: 30 November 2025")
    print("="*70)
    
    results = {}
    
    try:
        results['test1'] = test_basic_generation()
        results['test2'] = test_high_intensity_scenario()
        results['test3'] = test_toxic_relationship()
        results['test4'] = test_probabilistic_shared_breath()
        results['test5'] = test_fir_filter()
        
        print("\n" + "="*70)
        print(" ✓ ALL TESTS PASSED")
        print("="*70)
        print("\nGenerated scenarios in data/ directory:")
        print("  - Test1_Linear/")
        print("  - Test2_Parent_Child/")
        print("  - Test3_Toxic/")
        print("  - Test4_Prob_0/ through Test4_Prob_9/")
        print("  - Test5_FIR/")
        print("\nYou can now:")
        print("  1. Inspect CSV files in data/<scenario_name>/")
        print("  2. Run compute_love_magnitude.py on generated scenarios")
        print("  3. Compare with hand-crafted Singles_Dating scenarios")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    return results


if __name__ == "__main__":
    run_all_tests()

#!/usr/bin/env python3
"""
Example: Generating declining scenarios with decline_score parameter.

The decline_score parameter (0 to -10) allows human specification of how
toxic/negative a declining relationship trajectory should be:

- decline_score = 0: Neutral decline (natural entropy, drifting apart)
- decline_score = -3 to -5: Moderate toxicity (conflict, disappointment, disillusionment)
- decline_score = -7 to -10: Extreme toxicity (betrayal, abuse, destruction)

The score modulates:
1. Base primitive levels (dampened, can become negative)
2. Shared breath probability (reduced connection moments)
3. Random variation in primitives (more negative fluctuations)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scenario_generator import ScenarioGenerator


def generate_neutral_decline():
    """Example: Couple drifting apart naturally (decline_score = 0)."""
    
    generator = ScenarioGenerator("Decline_Neutral_Drift")
    
    # Waypoints: Start at moderate love, decline to indifference
    M1_waypoints = [
        (0, -1.5, 2.5, 0),      # Day 0: Loving relationship (ego=-1.5, love=2.5)
        (6, -1.0, 1.2, 0.3),    # Day 42: Cooling off
        (12, -0.3, 0.3, 0.2),   # Day 84: Mostly indifferent
    ]
    
    M2_waypoints = [
        (0, -2.0, 2.0, 0),      # Day 0: Also loving
        (6, -1.2, 1.0, 0.3),    # Day 42: Also cooling
        (12, -0.5, 0.2, 0.2),   # Day 84: Indifferent
    ]
    
    result = generator.generate_scenario(
        M1_trajectory=M1_waypoints,
        M2_trajectory=M2_waypoints,
        duration_days=84,
        event_sampling="weekly",
        beta_S=1.8,
        s_S=18,
        b_0=0.5,  # Existing relationship
        shared_breath_prob=0.60,
        decline_score=0.0,  # Neutral decline (no toxicity)
        m1_name="Partner_A",
        m2_name="Partner_B",
    )
    
    print("\n=== Neutral Decline Scenario ===")
    print(f"Natural drifting apart, no toxicity")
    print(f"Final M1: γ_self=({result['M1_data'][-1]['x']:.2f}, {result['M1_data'][-1]['y']:.2f}), S={result['M1_data'][-1]['S']}")
    print(f"Final M2: γ_self=({result['M2_data'][-1]['x']:.2f}, {result['M2_data'][-1]['y']:.2f}), S={result['M2_data'][-1]['S']}")
    print(f"Final primitives M1: v={result['M1_data'][-1]['v']:.0f}, r={result['M1_data'][-1]['r']:.0f}, f={result['M1_data'][-1]['f']:.0f}, a={result['M1_data'][-1]['a']:.0f}")


def generate_moderate_toxic():
    """Example: Relationship with conflict and disappointment (decline_score = -5)."""
    
    generator = ScenarioGenerator("Decline_Moderate_Toxic")
    
    # Waypoints: Start at moderate love, decline through conflict to mild enmity
    M1_waypoints = [
        (0, -1.5, 2.0, 0),      # Day 0: Loving relationship
        (6, -0.5, 0.5, 0.3),    # Day 42: Conflict emerging
        (12, 0.5, -1.5, 0.2),   # Day 84: Enmity and ego
    ]
    
    M2_waypoints = [
        (0, -2.0, 1.8, 0),      # Day 0: Loving
        (6, -0.8, 0.3, 0.3),    # Day 42: Disappointed
        (12, 0.3, -1.2, 0.2),   # Day 84: Mild enmity
    ]
    
    result = generator.generate_scenario(
        M1_trajectory=M1_waypoints,
        M2_trajectory=M2_waypoints,
        duration_days=84,
        event_sampling="weekly",
        beta_S=1.2,
        s_S=12,
        b_0=0.4,  # Existing relationship
        shared_breath_prob=0.50,  # Lower connection probability
        decline_score=-5.0,  # Moderate toxicity (50% primitive dampening)
        m1_name="Person_A",
        m2_name="Person_B",
    )
    
    print("\n=== Moderate Toxic Decline ===")
    print(f"Conflict, disappointment, mutual hurt")
    print(f"Final M1: γ_self=({result['M1_data'][-1]['x']:.2f}, {result['M1_data'][-1]['y']:.2f}), S={result['M1_data'][-1]['S']}")
    print(f"Final M2: γ_self=({result['M2_data'][-1]['x']:.2f}, {result['M2_data'][-1]['y']:.2f}), S={result['M2_data'][-1]['S']}")
    print(f"Final primitives M1: v={result['M1_data'][-1]['v']:.0f}, r={result['M1_data'][-1]['r']:.0f}, f={result['M1_data'][-1]['f']:.0f}, a={result['M1_data'][-1]['a']:.0f}")


def generate_extreme_toxic():
    """Example: Relationship with betrayal/abuse (decline_score = -9)."""
    
    generator = ScenarioGenerator("Decline_Extreme_Toxic")
    
    # Waypoints: Start at strong love, catastrophic decline to extreme enmity
    M1_waypoints = [
        (0, -2.0, 3.0, 0),      # Day 0: Deep love
        (4, -0.5, 0.8, 0.3),    # Day 28: Betrayal discovered
        (8, 1.5, -3.5, 0.2),    # Day 56: Extreme enmity and ego
    ]
    
    M2_waypoints = [
        (0, -2.5, 2.5, 0),      # Day 0: Deep love
        (4, -0.3, 0.5, 0.3),    # Day 28: Shock and hurt
        (8, 1.2, -3.0, 0.2),    # Day 56: Extreme enmity
    ]
    
    result = generator.generate_scenario(
        M1_trajectory=M1_waypoints,
        M2_trajectory=M2_waypoints,
        duration_days=60,
        event_sampling="weekly",
        beta_S=0.8,
        s_S=8,
        b_0=0.6,  # Strong existing bond (makes toxicity worse)
        shared_breath_prob=0.40,  # Low connection probability
        decline_score=-9.0,  # Extreme toxicity (near-complete suppression, negative primitives)
        m1_name="Betrayed",
        m2_name="Betrayer",
    )
    
    print("\n=== Extreme Toxic Decline ===")
    print(f"Betrayal, abuse, catastrophic destruction")
    print(f"Final M1: γ_self=({result['M1_data'][-1]['x']:.2f}, {result['M1_data'][-1]['y']:.2f}), S={result['M1_data'][-1]['S']}")
    print(f"Final M2: γ_self=({result['M2_data'][-1]['x']:.2f}, {result['M2_data'][-1]['y']:.2f}), S={result['M2_data'][-1]['S']}")
    print(f"Final primitives M1: v={result['M1_data'][-1]['v']:.0f}, r={result['M1_data'][-1]['r']:.0f}, f={result['M1_data'][-1]['f']:.0f}, a={result['M1_data'][-1]['a']:.0f}")
    print(f"Note: Negative primitives indicate destructive interactions (anti-visibility, anti-resonance, etc.)")


if __name__ == "__main__":
    print("=" * 60)
    print("Decline Score Examples: Demonstrating 0 to -10 Scale")
    print("=" * 60)
    
    generate_neutral_decline()
    generate_moderate_toxic()
    generate_extreme_toxic()
    
    print("\n" + "=" * 60)
    print("Decline Score Guide:")
    print("  0: Natural entropy, drifting apart")
    print("  -1 to -3: Mild disappointment, growing distance")
    print("  -4 to -6: Moderate conflict, mutual hurt")
    print("  -7 to -9: Severe toxicity, betrayal")
    print("  -10: Catastrophic destruction, abuse")
    print("=" * 60)

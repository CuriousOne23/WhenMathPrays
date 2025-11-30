#!/usr/bin/env python3
"""
Build correlation map: γ_self movements → plausible {v,r,f,a,S,b} ranges

KEY INSIGHT (from Jeff):
- γ_self is MEASURED from person's self-reported internal state (questionnaire)
- {v,r,f,a,S,b} are MEASURED from observable enacted behaviors
- They CO-OCCUR but don't causally determine each other
- We need: "When γ_self is at (x,y) moving by Δ(x,y), what primitives typically accompany that state?"

This is a CORRELATION/CO-OCCURRENCE map for generating plausible synthetic scenarios.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from core.love import W_t, G_x
from typing import List, Dict, Tuple

# Per CONSTANTS.md
BETA_S_RANGES = {
    'casual': (0.3, 0.8),
    'friendship': (1.0, 2.5),
    'romantic': (2.0, 4.0),
}

S_S_RANGES = {
    'casual': (3, 8),
    'friendship': (10, 20),
    'romantic': (15, 40),
}


def sample_primitives(n_samples: int = 100) -> List[Dict]:
    """Generate n_samples of {v,r,f,a,S,b} covering the space.
    
    Returns:
        List of dicts with keys: v, r, f, a, S, b_0, beta_S, s_S
    """
    samples = []
    
    # Use stratified sampling for better coverage
    # Sample v,r,f,a at quintiles: 0.1, 0.3, 0.5, 0.7, 0.9
    primitive_levels = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    # S cumulative counts
    S_levels = [0, 5, 10, 20, 40]
    
    # b_0 initial bond
    b_levels = [0.0, 0.2, 0.4, 0.6, 0.8]
    
    # For proof-of-concept, sample combinations
    np.random.seed(42)
    
    for _ in range(n_samples):
        # Random sampling with bias toward mid-range (more realistic)
        v = np.random.choice(primitive_levels)
        r = np.random.choice(primitive_levels)
        f = np.random.choice(primitive_levels)
        a = np.random.choice(primitive_levels)
        
        S = np.random.choice(S_levels)
        b_0 = np.random.choice(b_levels)
        
        # Choose relationship class based on b_0
        if b_0 < 0.3:
            rel_class = 'casual'
        elif b_0 < 0.6:
            rel_class = 'friendship'
        else:
            rel_class = 'romantic'
        
        beta_S = np.random.uniform(*BETA_S_RANGES[rel_class])
        s_S = np.random.uniform(*S_S_RANGES[rel_class])
        
        samples.append({
            'v': v,
            'r': r,
            'f': f,
            'a': a,
            'S': S,
            'b_0': b_0,
            'beta_S': beta_S,
            's_S': s_S,
        })
    
    return samples


def compute_W_for_samples(samples: List[Dict]) -> List[Dict]:
    """Compute W(t) for each sample using UREP equations.
    
    Returns:
        Same samples with added 'W' field
    """
    for sample in samples:
        primitives = (sample['v'], sample['r'], sample['f'], sample['a'])
        W = W_t(
            primitives=primitives,
            S=sample['S'],
            b_0=sample['b_0'],
            beta_S=sample['beta_S'],
            s_S=sample['s_S'],
            beta_b=1.0
        )
        sample['W'] = W
        
        # Also compute individual gates for analysis
        sample['G_v'] = G_x(sample['v'])
        sample['G_r'] = G_x(sample['r'])
        sample['G_f'] = G_x(sample['f'])
        sample['G_a'] = G_x(sample['a'])
    
    return samples


def compute_L_for_gamma_states(samples: List[Dict], gamma_states: List[Tuple[float, float]]) -> pd.DataFrame:
    """For each sample, compute L(t) when paired with different γ_self states.
    
    Args:
        samples: List of {v,r,f,a,S,b,W} dicts
        gamma_states: List of (x, y) γ_self positions to test
    
    Returns:
        DataFrame with columns: sample_id, gamma_x, gamma_y, v, r, f, a, S, b_0, W, L_magnitude
    """
    results = []
    
    for i, sample in enumerate(samples):
        W = sample['W']
        
        for gamma_x, gamma_y in gamma_states:
            # L(t) = γ_self · W(t) (simplified, no decay or averaging for proof-of-concept)
            # |L| = |γ_self| · W = sqrt(x² + y²) · W
            gamma_magnitude = np.sqrt(gamma_x**2 + gamma_y**2)
            L_magnitude = gamma_magnitude * W
            
            results.append({
                'sample_id': i,
                'gamma_x': gamma_x,
                'gamma_y': gamma_y,
                'gamma_mag': gamma_magnitude,
                'v': sample['v'],
                'r': sample['r'],
                'f': sample['f'],
                'a': sample['a'],
                'S': sample['S'],
                'b_0': sample['b_0'],
                'beta_S': sample['beta_S'],
                's_S': sample['s_S'],
                'W': W,
                'L_magnitude': L_magnitude,
            })
    
    return pd.DataFrame(results)


def analyze_correlations(df: pd.DataFrame, target_gamma_movement: str):
    """Analyze which primitive ranges correlate with γ_self movements.
    
    Args:
        df: Results dataframe from compute_L_for_gamma_states
        target_gamma_movement: Description like "love_increasing", "love_decreasing", etc.
    """
    print(f"\n{'='*70}")
    print(f"Correlation Analysis: {target_gamma_movement}")
    print(f"{'='*70}")
    
    # Group by γ_self state
    for (gx, gy), group in df.groupby(['gamma_x', 'gamma_y']):
        print(f"\nγ_self = ({gx:+.2f}, {gy:+.2f}), |γ| = {group['gamma_mag'].iloc[0]:.2f}")
        print(f"  Sample size: {len(group)}")
        
        # Statistics for primitives
        print(f"  Primitive ranges:")
        print(f"    v: [{group['v'].min():.2f}, {group['v'].max():.2f}], mean={group['v'].mean():.2f}")
        print(f"    r: [{group['r'].min():.2f}, {group['r'].max():.2f}], mean={group['r'].mean():.2f}")
        print(f"    f: [{group['f'].min():.2f}, {group['f'].max():.2f}], mean={group['f'].mean():.2f}")
        print(f"    a: [{group['a'].min():.2f}, {group['a'].max():.2f}], mean={group['a'].mean():.2f}")
        print(f"    S: [{group['S'].min():.0f}, {group['S'].max():.0f}], mean={group['S'].mean():.1f}")
        print(f"    b_0: [{group['b_0'].min():.2f}, {group['b_0'].max():.2f}], mean={group['b_0'].mean():.2f}")
        
        # W(t) statistics
        print(f"  W(t) range: [{group['W'].min():.2f}, {group['W'].max():.2f}], mean={group['W'].mean():.2f}")
        
        # L(t) magnitude statistics
        print(f"  L(t) magnitude: [{group['L_magnitude'].min():.1f}, {group['L_magnitude'].max():.1f}], mean={group['L_magnitude'].mean():.1f}")
        
        # Find top correlations
        print(f"  Top 5 W(t) producers:")
        top5 = group.nlargest(5, 'W')[['v', 'r', 'f', 'a', 'S', 'b_0', 'W']]
        print(top5.to_string(index=False))


def build_map_for_movement(gamma_start: Tuple[float, float], 
                           gamma_end: Tuple[float, float],
                           movement_name: str,
                           n_samples: int = 100):
    """Build correlation map for a specific γ_self movement.
    
    Args:
        gamma_start: Starting (x, y) position
        gamma_end: Ending (x, y) position
        movement_name: Descriptive name
        n_samples: Number of primitive combinations to test
    """
    print(f"\n{'='*70}")
    print(f"Building Correlation Map: {movement_name}")
    print(f"{'='*70}")
    print(f"γ_self movement: ({gamma_start[0]:+.2f}, {gamma_start[1]:+.2f}) → ({gamma_end[0]:+.2f}, {gamma_end[1]:+.2f})")
    
    delta_x = gamma_end[0] - gamma_start[0]
    delta_y = gamma_end[1] - gamma_start[1]
    print(f"Δγ_self = ({delta_x:+.2f}, {delta_y:+.2f})")
    
    # Sample primitive space
    print(f"\nSampling {n_samples} primitive combinations...")
    samples = sample_primitives(n_samples)
    
    # Compute W(t) for each
    print(f"Computing W(t) using UREP equations...")
    samples = compute_W_for_samples(samples)
    
    # Test with both start and end states
    gamma_states = [gamma_start, gamma_end]
    
    print(f"Computing L(t) for γ_self states...")
    df = compute_L_for_gamma_states(samples, gamma_states)
    
    # Analyze correlations
    analyze_correlations(df, movement_name)
    
    # Save results
    output_file = f"data/correlation_map_{movement_name}.csv"
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"\n✓ Saved results to: {output_file}")
    
    return df


def main():
    """Run proof-of-concept correlation mapping."""
    
    print("="*70)
    print("PROOF-OF-CONCEPT: Primitive-γ_self Correlation Mapping")
    print("="*70)
    print("\nKey insight: γ_self and primitives are MEASURED independently")
    print("Building map of which primitives typically accompany γ_self movements")
    
    # Test Case 1: Love increasing (typical "falling in love")
    df1 = build_map_for_movement(
        gamma_start=(-0.5, 0.5),   # Mild love
        gamma_end=(-1.2, 2.0),      # Strong love, less ego
        movement_name="love_increasing",
        n_samples=100
    )
    
    # Test Case 2: Love decreasing (typical "falling out of love")
    df2 = build_map_for_movement(
        gamma_start=(-1.5, 2.0),    # Strong love
        gamma_end=(-0.3, 0.3),      # Weak love
        movement_name="love_decreasing",
        n_samples=100
    )
    
    # Test Case 3: Stable love
    df3 = build_map_for_movement(
        gamma_start=(-1.0, 1.5),    # Moderate love
        gamma_end=(-1.0, 1.5),      # Same (stable)
        movement_name="love_stable",
        n_samples=100
    )
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("Generated correlation maps for 3 γ_self movement patterns")
    print("Next step: Use these patterns to improve scenario_generator.py")
    print("="*70)


if __name__ == "__main__":
    main()

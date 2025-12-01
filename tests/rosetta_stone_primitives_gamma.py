#!/usr/bin/env python3
"""
Rosetta Stone: Translating between primitives {v,r,f,a,S,b} and γ_self movements

Building the fundamental vocabulary:
- Simple spoke-wheel patterns from origin
- Each direction gets representative primitive values
- Establishes basic translation rules

This is our dictionary for the primitive→γ_self language.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Tuple, List


def define_spoke_wheel_movements(magnitude: float = 0.5) -> Dict[str, Tuple[float, float]]:
    """Define 8 cardinal direction movements in γ_self space.
    
    Args:
        magnitude: Step size for each spoke
    
    Returns:
        Dict mapping direction name to (Δx, Δy) vector
    """
    movements = {
        # Pure axis movements
        'North_PureLove': (0.0, +magnitude),           # ↑ Love increases
        'South_PureHate': (0.0, -magnitude),           # ↓ Enmity increases
        'East_PureWe': (+magnitude, 0.0),              # → We increases (toward +Re)
        'West_PureEgo': (-magnitude, 0.0),             # ← Ego increases (toward -Re)
        
        # Diagonal movements (typical real patterns)
        'NorthEast_LoveWe_Q1': (+magnitude*0.7, +magnitude*0.7),  # ↗ Falling in love (selfless) - Q1
        'NorthWest_LoveEgo_Q2': (-magnitude*0.7, +magnitude*0.7), # ↖ Infatuation (ego + love) - Q2
        'SouthWest_HateEgo_Q3': (-magnitude*0.7, -magnitude*0.7), # ↙ Betrayal (ego + enmity) - Q3
        'SouthEast_HateWe_Q4': (+magnitude*0.7, -magnitude*0.7),  # ↘ Disillusionment (collective hurt) - Q4
    }
    return movements


def assign_primitive_patterns() -> Dict[str, Dict]:
    """Assign representative primitive values for each direction.
    
    This is our initial hypothesis - the Rosetta stone vocabulary.
    
    Returns:
        Dict mapping direction to {v, r, f, a, S, b_0, description}
    """
    patterns = {
        # Pure Love increase (North) - high positive primitives, generous shared breaths
        'North_PureLove': {
            'v': 0.75, 'r': 0.80, 'f': 0.75, 'a': 0.85,
            'S': 30, 'b_0': 0.4,
            'description': 'High visibility, resonance, fidelity, altruism. Many shared moments. Genuine connection.',
            'emotional_state': 'Opening heart, seeing beauty, feeling connected'
        },
        
        # Pure Enmity increase (South) - low/negative primitives, withdrawal
        'South_PureHate': {
            'v': 0.15, 'r': 0.10, 'f': 0.20, 'a': 0.10,
            'S': 2, 'b_0': 0.2,
            'description': 'Low primitives, minimal shared moments. Closing off, withdrawal, resentment.',
            'emotional_state': 'Hurt, closing heart, seeing flaws, building walls'
        },
        
        # Pure We increase (East) - high visibility/engagement toward M2
        'East_PureWe': {
            'v': 0.85, 'r': 0.80, 'f': 0.75, 'a': 0.90,
            'S': 30, 'b_0': 0.5,
            'description': 'High visibility toward M2. Showing up, being present, engaging. Selfless orientation.',
            'emotional_state': 'I see you, I show up for you, we over me'
        },
        
        # Pure Ego increase (West) - low visibility/withdrawal from M2
        'West_PureEgo': {
            'v': 0.25, 'r': 0.30, 'f': 0.40, 'a': 0.20,
            'S': 5, 'b_0': 0.2,
            'description': 'Low visibility to M2. Withdrawing, self-focused, not showing up. "Me-first".',
            'emotional_state': 'Protecting self, boundaries up, less available to you'
        },
        
        # NorthEast - Falling in love (selfless romantic love) - Q1
        'NorthEast_LoveWe_Q1': {
            'v': 0.85, 'r': 0.85, 'f': 0.80, 'a': 0.90,
            'S': 35, 'b_0': 0.4,
            'description': 'Very high visibility and all primitives. Fully showing up for M2. Classic "falling in love" - selfless.',
            'emotional_state': 'I see you fully, I show up completely, putting you first'
        },
        
        # NorthWest - Infatuation (ego + love) - Q2
        'NorthWest_LoveEgo_Q2': {
            'v': 0.50, 'r': 0.60, 'f': 0.50, 'a': 0.40,
            'S': 15, 'b_0': 0.2,
            'description': 'Moderate visibility - somewhat withdrawn but excited. Still self-focused. Early dating energy.',
            'emotional_state': 'Butterflies but guarded, testing the waters, "what about me?"'
        },
        
        # SouthWest - Betrayal (ego + enmity) - Q3
        'SouthWest_HateEgo_Q3': {
            'v': 0.10, 'r': 0.10, 'f': 0.05, 'a': 0.05,
            'S': 1, 'b_0': 0.2,
            'description': 'Very low visibility - maximum withdrawal. Not showing up at all. Self-protective.',
            'emotional_state': 'I hide from you, walls up, never again, protecting me'
        },
        
        # SouthEast - Disillusionment (collective hurt) - Q4
        'SouthEast_HateWe_Q4': {
            'v': 0.40, 'r': 0.35, 'f': 0.45, 'a': 0.40,
            'S': 10, 'b_0': 0.4,
            'description': 'Moderate visibility - still somewhat present despite hurt. Shared disappointment. "We tried".',
            'emotional_state': 'Still seeing each other through the pain, shared grief, still trying'
        },
    }
    return patterns


def visualize_rosetta_stone():
    """Create visual representation of the Rosetta stone."""
    movements = define_spoke_wheel_movements(magnitude=1.0)
    patterns = assign_primitive_patterns()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Left plot: Spoke wheel in γ_self space
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
    ax1.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)
    ax1.grid(True, alpha=0.2)
    ax1.set_xlabel('γ_self x-axis (Ego ← → We)', fontsize=12)
    ax1.set_ylabel('γ_self y-axis (Enmity ← → Love)', fontsize=12)
    ax1.set_title('Spoke Wheel: γ_self Movement Directions', fontsize=14, fontweight='bold')
    
    # Add quadrant labels
    ax1.text(1.2, 1.2, 'Q1\nWe+Love', ha='center', fontsize=10, alpha=0.5)
    ax1.text(-1.2, 1.2, 'Q2\nEgo+Love', ha='center', fontsize=10, alpha=0.5)
    ax1.text(-1.2, -1.2, 'Q3\nEgo+Hate', ha='center', fontsize=10, alpha=0.5)
    ax1.text(1.2, -1.2, 'Q4\nWe+Hate', ha='center', fontsize=10, alpha=0.5)
    
    # Plot spokes
    colors = plt.cm.tab10(np.linspace(0, 1, len(movements)))
    for (name, (dx, dy)), color in zip(movements.items(), colors):
        ax1.arrow(0, 0, dx, dy, head_width=0.08, head_length=0.08, 
                 fc=color, ec=color, linewidth=2, alpha=0.7)
        # Label at end of arrow
        label_name = name.split('_')[1] if '_' in name else name
        ax1.text(dx*1.15, dy*1.15, label_name, ha='center', va='center',
                fontsize=8, fontweight='bold', color=color)
    
    # Right plot: Primitive values for each direction
    ax2.axis('off')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_title('Primitive Patterns for Each Direction', fontsize=14, fontweight='bold')
    
    y_pos = 0.95
    line_height = 0.12
    
    for (name, (dx, dy)), color in zip(movements.items(), colors):
        pattern = patterns[name]
        
        # Direction label
        label_name = name.replace('_', ' ')
        ax2.text(0.02, y_pos, f"{label_name}:", fontsize=10, fontweight='bold', 
                color=color, va='top')
        
        # Primitive values
        prim_text = f"v={pattern['v']:.2f}, r={pattern['r']:.2f}, f={pattern['f']:.2f}, a={pattern['a']:.2f}, S={pattern['S']}, b₀={pattern['b_0']:.1f}"
        ax2.text(0.05, y_pos-0.025, prim_text, fontsize=8, va='top', family='monospace')
        
        # Description
        desc = pattern['description'][:80] + '...' if len(pattern['description']) > 80 else pattern['description']
        ax2.text(0.05, y_pos-0.045, desc, fontsize=7, va='top', style='italic', alpha=0.7)
        
        y_pos -= line_height
        
        if y_pos < 0.05:
            break
    
    plt.tight_layout()
    plt.savefig('data/rosetta_stone_primitives_gamma.png', dpi=150, bbox_inches='tight')
    print(f"✓ Saved visualization: data/rosetta_stone_primitives_gamma.png")
    plt.close()


def generate_rosetta_table():
    """Generate CSV table of the Rosetta stone mappings."""
    movements = define_spoke_wheel_movements(magnitude=0.5)
    patterns = assign_primitive_patterns()
    
    rows = []
    for name, (dx, dy) in movements.items():
        pattern = patterns[name]
        rows.append({
            'direction': name,
            'delta_x': dx,
            'delta_y': dy,
            'magnitude': np.sqrt(dx**2 + dy**2),
            'v': pattern['v'],
            'r': pattern['r'],
            'f': pattern['f'],
            'a': pattern['a'],
            'S': pattern['S'],
            'b_0': pattern['b_0'],
            'description': pattern['description'],
            'emotional_state': pattern['emotional_state'],
        })
    
    df = pd.DataFrame(rows)
    output_file = 'data/rosetta_stone_primitive_gamma_mappings.csv'
    df.to_csv(output_file, index=False)
    print(f"✓ Saved table: {output_file}")
    
    return df


def print_rosetta_stone():
    """Print the Rosetta stone in readable format."""
    movements = define_spoke_wheel_movements(magnitude=0.5)
    patterns = assign_primitive_patterns()
    
    print("\n" + "="*80)
    print("ROSETTA STONE: Primitives ↔ γ_self Movement Translation")
    print("="*80)
    print("\nFundamental vocabulary for the primitive→γ_self language")
    print("Each entry shows: Direction → Representative primitive pattern\n")
    
    for name, (dx, dy) in movements.items():
        pattern = patterns[name]
        
        print(f"\n{'─'*80}")
        print(f"Direction: {name.replace('_', ' ')}")
        print(f"  Δγ_self: ({dx:+.2f}, {dy:+.2f}), magnitude: {np.sqrt(dx**2 + dy**2):.2f}")
        print(f"\n  Primitives:")
        print(f"    v={pattern['v']:.2f}, r={pattern['r']:.2f}, f={pattern['f']:.2f}, a={pattern['a']:.2f}")
        print(f"    S={pattern['S']:2d} shared breaths, b₀={pattern['b_0']:.1f} initial bond")
        print(f"\n  Description: {pattern['description']}")
        print(f"  Emotional state: {pattern['emotional_state']}")
    
    print("="*80 + "\n")
    print("Key Insights:")
    print("  • Love increases (↑y): High v,r,f,a + many shared breaths")
    print("  • Enmity increases (↓y): Low primitives + withdrawal")
    print("  • We increases (→x): HIGH visibility - M1 showing up strongly for M2")
    print("  • Ego increases (←x): LOW visibility - M1 withdrawing from M2")
    print("  • Primitives measure M1's engagement TOWARD M2 (directional)")
    print("  • Q1 (NorthEast): Very high visibility - fully present + loving")
    print("  • Q2 (NorthWest): Moderate visibility - guarded but excited")
    print("  • Q3 (SouthWest): Very low visibility - maximum withdrawal + hurt")
    print("  • Q4 (SouthEast): Moderate visibility - still present despite hurt")
    print("="*80 + "\n")


def main():
    """Build and display the Rosetta stone."""
    print("="*80)
    print("Building Rosetta Stone: Primitive → γ_self Translation Dictionary")
    print("="*80)
    
    # Print the mappings
    print_rosetta_stone()
    
    # Generate visualization
    print("\nGenerating visualization...")
    os.makedirs('data', exist_ok=True)
    visualize_rosetta_stone()
    
    # Generate CSV table
    print("\nGenerating CSV table...")
    df = generate_rosetta_table()
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("  1. Review these patterns - do they match intuition?")
    print("  2. Adjust primitive values to refine the translation")
    print("  3. Test: generate scenarios using these patterns")
    print("  4. Expand: add more nuanced patterns (micro-movements, transitions)")
    print("  5. Validate: compare to real relationship data")
    print("="*80)


if __name__ == "__main__":
    main()

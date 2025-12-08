"""
Fidelity Asymmetry Sensitivity Analysis

Tests how different w_neg values affect negative fidelity scaling across
varying relationship magnitudes (|γ_self|). Helps determine if current
w_neg=1.5 is too aggressive at high relationship states.

Usage:
    python tests/fidelity_asymmetry_sensitivity.py
"""

import numpy as np
import matplotlib.pyplot as plt

# GRP parameters
W_F = 1.2  # Fidelity axis weight (strongest primitive)
EPSILON = 1.0  # Collapse prevention threshold

# Test configurations
W_NEG_VALUES = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
FIDELITY_RANGE = np.linspace(-10, 10, 201)  # Full primitive range
GAMMA_MAGNITUDES = [1.0, 5.0, 10.0, 20.0, 44.6]  # Various relationship depths


def apply_hybrid_asymmetry(f, gamma_magnitude, w_neg, epsilon=EPSILON):
    """
    Apply hybrid asymmetry to fidelity.
    
    For negatives: f' = f × w_neg × max(|γ_self|, ε)
    For positives: f' = f (no transformation)
    """
    if f < 0:
        scale_factor = max(gamma_magnitude, epsilon)
        return f * w_neg * scale_factor
    else:
        return f


def compute_delta_im_contribution(f, gamma_magnitude, w_neg):
    """
    Compute fidelity's contribution to ΔIm (imaginary axis delta).
    
    Returns: w_f × f'
    """
    f_prime = apply_hybrid_asymmetry(f, gamma_magnitude, w_neg)
    return W_F * f_prime


def plot_fidelity_sensitivity():
    """Generate plots showing fidelity sensitivity across w_neg values."""
    
    # Create figure with subplots (need 7 plots for 7 w_neg values)
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('Fidelity Asymmetry Sensitivity Analysis\n' + 
                 f'w_f={W_F}, ε={EPSILON}', fontsize=16, fontweight='bold')
    
    # Flatten axes for easier iteration
    axes_flat = axes.flatten()
    
    # Plot for each w_neg value
    for idx, w_neg in enumerate(W_NEG_VALUES):
        ax = axes_flat[idx]
        
        # Plot for each gamma magnitude
        for gamma_mag in GAMMA_MAGNITUDES:
            delta_im = [compute_delta_im_contribution(f, gamma_mag, w_neg) 
                       for f in FIDELITY_RANGE]
            
            label = f'|γ|={gamma_mag:.1f}'
            ax.plot(FIDELITY_RANGE, delta_im, label=label, linewidth=2)
        
        # Formatting
        ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.3)
        ax.axvline(x=0, color='black', linestyle='--', linewidth=1, alpha=0.3)
        ax.set_xlabel('Fidelity (f)', fontsize=10)
        ax.set_ylabel('ΔIm Contribution', fontsize=10)
        ax.set_title(f'w_neg = {w_neg}', fontsize=12, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.2)
        
        # Add annotation for extreme case
        if gamma_mag == GAMMA_MAGNITUDES[-1]:  # Highest magnitude
            f_test = -2.0
            delta_im_test = compute_delta_im_contribution(f_test, gamma_mag, w_neg)
            ax.annotate(f'f={f_test:.1f}\n@|γ|={gamma_mag:.1f}\n→ΔIm={delta_im_test:.1f}',
                       xy=(f_test, delta_im_test),
                       xytext=(f_test + 2, delta_im_test - 50),
                       fontsize=8,
                       bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5),
                       arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    
    # Hide the last subplot (8th) since we only have 7 w_neg values
    axes_flat[-1].axis('off')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save in tests directory
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'fidelity_asymmetry_sensitivity.png')
    plt.savefig(output_path, dpi=150)
    print(f"✓ Saved plot: {output_path}")
    plt.show()


def print_numerical_analysis():
    """Print numerical breakdown for specific test cases."""
    
    print("\n" + "="*80)
    print("NUMERICAL ANALYSIS: Fidelity Impact at High Relationship Magnitude")
    print("="*80)
    
    # Test case from interactive editor bug report
    test_cases = [
        {"f": -1.88, "gamma": 44.6, "desc": "User's bug report case"},
        {"f": -2.0, "gamma": 44.6, "desc": "Rounded test value"},
        {"f": -4.0, "gamma": 2.5, "desc": "GRP_rev3 worked example"},
    ]
    
    for case in test_cases:
        f = case["f"]
        gamma = case["gamma"]
        desc = case["desc"]
        
        print(f"\n{desc}:")
        print(f"  f = {f:.2f}, |γ_self| = {gamma:.2f}")
        print(f"\n  {'w_neg':<8} {'f_prime':<12} {'ΔIm':<12} {'Effective Mult':<15}")
        print(f"  {'-'*8} {'-'*12} {'-'*12} {'-'*15}")
        
        for w_neg in W_NEG_VALUES:
            f_prime = apply_hybrid_asymmetry(f, gamma, w_neg)
            delta_im = W_F * f_prime
            effective_mult = W_F * w_neg * gamma
            
            print(f"  {w_neg:<8.2f} {f_prime:<12.2f} {delta_im:<12.2f} {effective_mult:<15.2f}")
    
    print("\n" + "="*80)
    print("RECOMMENDATION:")
    print("="*80)
    print("Current w_neg=1.5 produces effective multiplier of 1.8×|γ_self| for negative fidelity.")
    print(f"At |γ_self|=44.6, this gives effective multiplier of ~80x (!).")
    print("\nPossible adjustments:")
    print("  • Lower w_neg to 1.2-1.3 (reduces to ~64-70x at high magnitude)")
    print("  • Cap magnitude scaling: min(|γ_self|, 10) → max ~18x")
    print("  • Use logarithmic: log(|γ_self|+1) → max ~7x at |γ|=44.6")
    print("  • Use square root: sqrt(|γ_self|) → max ~12x at |γ|=44.6")
    print("="*80 + "\n")


if __name__ == "__main__":
    print("Fidelity Asymmetry Sensitivity Analysis")
    print("========================================\n")
    
    # Generate plots
    plot_fidelity_sensitivity()
    
    # Print numerical breakdown
    print_numerical_analysis()

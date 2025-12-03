#!/usr/bin/env python3
"""
Batch runner for all 5 validation scenarios (December 2025 Final Simplification).
Tests the component-wise γ_self position model.
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))
from run_scenario import ScenarioRunner

# Ensure results directory exists
Path("results").mkdir(exist_ok=True)

def run_all_scenarios():
    """Run all 5 validation scenarios and generate reports."""
    
    scenarios = [
        {
            "name": "Steady Positive Growth",
            "csv": "data/steady_positive_growth.csv",
            "gamma_self0": 0.0 + 0.0j,
            "description": "Proves linear accumulation with constant positive primitives"
        },
        {
            "name": "Betrayal and Repair",
            "csv": "data/betrayal_and_repair.csv",
            "gamma_self0": 0.0 + 0.0j,
            "description": "Proves asymmetry (w_neg=1.5), irreversibility, phased recovery"
        },
        {
            "name": "Silence with Presence",
            "csv": "data/silence_with_presence.csv",
            "gamma_self0": 0.0 + 0.0j,
            "description": "Proves S dual-axis mapping (both Real and Imaginary contributions)"
        },
        {
            "name": "Soul-Bond Saturation",
            "csv": "data/soul_bond_saturation.csv",
            "gamma_self0": 0.0 + 0.0j,
            "description": "Proves upper bounds, sustained high primitives don't explode"
        },
        {
            "name": "Oscillatory Style",
            "csv": "data/oscillatory_style.csv",
            "gamma_self0": 0.0 + 0.0j,
            "description": "Proves quadrant cycling, antagonistic robustness"
        }
    ]
    
    results_summary = []
    
    print("\n" + "="*80)
    print("RUNNING ALL 5 VALIDATION SCENARIOS")
    print("="*80)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n[{i}/5] {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print("-" * 80)
        
        # Initialize and run
        runner = ScenarioRunner(
            csv_path=scenario['csv'],
            gamma_self0=scenario['gamma_self0'],
            name=scenario['name']
        )
        
        trajectory = runner.run()
        
        # Print summary
        runner.summary()
        
        # Save plot
        plot_path = f"results/{scenario['name'].replace(' ', '_')}_trajectory.png"
        runner.plot(save_path=plot_path, show=False)
        
        # Save trajectory CSV
        csv_path = f"results/{scenario['name'].replace(' ', '_')}_trajectory.csv"
        trajectory.to_csv(csv_path, index=False)
        
        # Collect summary data
        start = runner.gamma_self_history[0]
        end = runner.gamma_self_history[-1]
        
        results_summary.append({
            'scenario': scenario['name'],
            'duration': trajectory['day'].iloc[-1],
            'events': len(trajectory),
            'start_magnitude': abs(start),
            'end_magnitude': abs(end),
            'delta_magnitude': abs(end) - abs(start),
            'final_quadrant': get_quadrant(end),
            'description': scenario['description']
        })
        
        print(f"✓ Completed: {scenario['name']}")
        print(f"  Plot saved: {plot_path}")
        print(f"  Data saved: {csv_path}")
    
    # Print overall summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    
    for result in results_summary:
        print(f"\n{result['scenario']}")
        print(f"  Duration: {result['duration']} days, Events: {result['events']}")
        print(f"  |γ_self|: {result['start_magnitude']:.2f} → {result['end_magnitude']:.2f} (Δ = {result['delta_magnitude']:.2f})")
        print(f"  Final: {result['final_quadrant']}")
        print(f"  Validates: {result['description']}")
    
    print("\n" + "="*80)
    print("✓ ALL 5 SCENARIOS COMPLETED")
    print("="*80)
    print("\nNext steps:")
    print("1. Review plots in results/ directory")
    print("2. Check if magnitudes match expectations (see CONSTANTS.md)")
    print("3. Tune weights if needed (see TUNING.md)")
    print("4. Document findings in validation report")
    print()

def get_quadrant(gamma: complex) -> str:
    """Determine quadrant from complex number."""
    x, y = gamma.real, gamma.imag
    if x >= 0 and y >= 0:
        return "Q1 (We + Love)"
    elif x < 0 and y >= 0:
        return "Q2 (Ego + Love)"
    elif x < 0 and y < 0:
        return "Q3 (Ego + Hate)"
    else:
        return "Q4 (We + Hate)"


if __name__ == "__main__":
    run_all_scenarios()

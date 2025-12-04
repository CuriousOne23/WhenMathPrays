#!/usr/bin/env python3
"""
Run dual M1/M2 scenario with combined plot
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from run_scenario import detect_pair, plot_dual_scenario

if __name__ == "__main__":
    # Detect M1/M2 pair
    csv_path = "data/single_dating_to_love_M1.csv"
    
    m1_path, m2_path = detect_pair(csv_path)
    
    if m1_path and m2_path:
        print(f"Detected M1/M2 pair:")
        print(f"  M1: {m1_path}")
        print(f"  M2: {m2_path}")
        print()
        
        # Run combined scenario
        runner_m1, runner_m2 = plot_dual_scenario(
            m1_path=m1_path,
            m2_path=m2_path,
            gamma_self0_m1=-2.5+0.5j,
            gamma_self0_m2=-3+1j,
            save_path="results/single_dating_to_love_combined.png",
            show=False
        )
        
        # Print summaries
        print("\n" + "="*60)
        print("M1 Summary:")
        print("="*60)
        runner_m1.summary()
        
        print("\n" + "="*60)
        print("M2 Summary:")
        print("="*60)
        runner_m2.summary()
        
        print("\nDual scenario complete!")
    else:
        print(f"No M1/M2 pair found for {csv_path}")

#!/usr/bin/env python3
"""
Run Single Dating to Love scenario - M2 perspective
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "simulations"))
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from run_scenario import ScenarioRunner

if __name__ == "__main__":
    # Run scenario
    csv_path = "data/single_dating_to_love_M2.csv"
    
    print(f"Running scenario: {csv_path}\n")
    
    runner = ScenarioRunner(
        csv_path=csv_path,
        gamma_self0=-3+1j,  # M2 starts in Q2 (Ego + Love)
        name="Single Dating to Love - M2"
    )
    
    trajectory = runner.run()
    runner.plot(save_path="results/single_dating_to_love_M2.png", show=False)
    runner.summary()
    
    # Save trajectory CSV
    output_csv = "results/single_dating_to_love_M2_trajectory.csv"
    trajectory.to_csv(output_csv, index=False)
    print(f"\nTrajectory CSV saved: {output_csv}")
    
    print("\nScenario complete!")

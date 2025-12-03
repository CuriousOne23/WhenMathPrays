#!/usr/bin/env python3
"""
Scenario Runner for WhenMathPrays Framework (December 2025 Simplification)
Runs γ_self position-based model from CSV primitive scenarios.

Love = γ_self position (no L(t) calculation)
γ_self(n+1) = γ_self(n) + component-wise primitive updates
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from love import update_gamma_self, DEFAULT_WEIGHTS, DEFAULT_GAMMA_SELF0


class ScenarioRunner:
    """Run γ_self trajectory from CSV scenario file."""
    
    def __init__(self, csv_path: str, gamma_self0: complex = DEFAULT_GAMMA_SELF0, 
                 weights: dict = None, name: str = None):
        """
        Initialize scenario runner.
        
        Args:
            csv_path: Path to CSV file with primitives (day,v,r,f,a,S,notes)
            gamma_self0: Initial position (default 0+0j)
            weights: Optional weight dictionary (defaults from CONSTANTS.md)
            name: Optional scenario name (defaults to filename)
        """
        self.csv_path = Path(csv_path)
        self.gamma_self0 = gamma_self0
        self.weights = weights or DEFAULT_WEIGHTS.copy()
        self.name = name or self.csv_path.stem
        
        # Load scenario
        self.data = self._load_csv()
        
        # Results storage
        self.trajectory = []
        self.gamma_self_history = []
        
    def _load_csv(self) -> pd.DataFrame:
        """Load CSV with primitives in human scale [-10, +10]."""
        df = pd.read_csv(self.csv_path)
        
        # Validate required columns
        required = ['day', 'v', 'r', 'f', 'a', 'S']
        missing = set(required) - set(df.columns)
        if missing:
            raise ValueError(f"CSV missing required columns: {missing}")
        
        return df
    
    def _normalize_primitive(self, p_raw: float) -> float:
        """Normalize from human scale [-10, +10] to [-1, +1]."""
        return p_raw / 10.0
    
    def run(self) -> pd.DataFrame:
        """
        Run scenario and compute γ_self trajectory.
        
        Returns:
            DataFrame with trajectory data (day, gamma_x, gamma_y, |gamma|, primitives)
        """
        # Initialize
        gamma_self = self.gamma_self0
        self.gamma_self_history = [gamma_self]
        
        results = []
        
        for idx, row in self.data.iterrows():
            day = row['day']
            
            # Normalize primitives from [-10, +10] to [-1, +1]
            v = self._normalize_primitive(row['v'])
            r = self._normalize_primitive(row['r'])
            f = self._normalize_primitive(row['f'])
            a = self._normalize_primitive(row['a'])
            S = self._normalize_primitive(row['S'])
            
            # Update γ_self position
            gamma_self_next = update_gamma_self(
                gamma_self_current=gamma_self,
                v=v, r=r, f=f, a=a, S=S,
                weights=self.weights
            )
            
            # Store results
            results.append({
                'day': day,
                'gamma_x': gamma_self.real,
                'gamma_y': gamma_self.imag,
                'gamma_magnitude': abs(gamma_self),
                'v_raw': row['v'],
                'r_raw': row['r'],
                'f_raw': row['f'],
                'a_raw': row['a'],
                'S_raw': row['S'],
                'v_norm': v,
                'r_norm': r,
                'f_norm': f,
                'a_norm': a,
                'S_norm': S,
                'notes': row.get('notes', '')
            })
            
            # Update for next iteration
            gamma_self = gamma_self_next
            self.gamma_self_history.append(gamma_self)
        
        self.trajectory = pd.DataFrame(results)
        return self.trajectory
    
    def plot(self, save_path: str = None, show: bool = True):
        """
        Plot γ_self trajectory in complex plane.
        
        Args:
            save_path: Optional path to save figure
            show: Whether to display plot (default True)
        """
        if len(self.trajectory) == 0:
            raise ValueError("No trajectory data. Run scenario first.")
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Left: γ_self trajectory in complex plane
        ax1 = axes[0]
        
        x = self.trajectory['gamma_x'].values
        y = self.trajectory['gamma_y'].values
        days = self.trajectory['day'].values
        
        # Plot trajectory with color gradient (time evolution)
        scatter = ax1.scatter(x, y, c=days, cmap='viridis', s=50, alpha=0.7, edgecolors='black', linewidths=0.5)
        ax1.plot(x, y, 'gray', alpha=0.3, linewidth=1)
        
        # Mark start and end
        ax1.plot(x[0], y[0], 'go', markersize=12, label=f'Start (day {days[0]})', markeredgecolor='black')
        ax1.plot(x[-1], y[-1], 'r*', markersize=15, label=f'End (day {days[-1]})', markeredgecolor='black')
        
        # Mark initial condition γ_self0
        ax1.plot(self.gamma_self0.real, self.gamma_self0.imag, 'bs', markersize=10, 
                label=f'γ_self0 ({self.gamma_self0.real:.1f}, {self.gamma_self0.imag:.1f}i)', 
                markeredgecolor='black')
        
        # Quadrant lines
        ax1.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.3)
        ax1.axvline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.3)
        
        # Quadrant labels
        ax1.text(0.95, 0.95, 'Q1: We+Love', transform=ax1.transAxes, ha='right', va='top', 
                fontsize=9, style='italic', alpha=0.5)
        ax1.text(0.05, 0.95, 'Q2: Ego+Love', transform=ax1.transAxes, ha='left', va='top',
                fontsize=9, style='italic', alpha=0.5)
        ax1.text(0.05, 0.05, 'Q3: Ego+Hate', transform=ax1.transAxes, ha='left', va='bottom',
                fontsize=9, style='italic', alpha=0.5)
        ax1.text(0.95, 0.05, 'Q4: We+Hate', transform=ax1.transAxes, ha='right', va='bottom',
                fontsize=9, style='italic', alpha=0.5)
        
        ax1.set_xlabel('Real: Ego (−) ↔ We (+)', fontsize=11)
        ax1.set_ylabel('Imaginary: Hate (−) ↔ Love (+)', fontsize=11)
        ax1.set_title(f'γ_self Trajectory: {self.name}', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.2)
        ax1.legend(loc='upper left', fontsize=9)
        ax1.set_aspect('equal', adjustable='box')
        
        # Colorbar for time
        cbar = plt.colorbar(scatter, ax=ax1)
        cbar.set_label('Day', fontsize=10)
        
        # Right: |γ_self| magnitude over time
        ax2 = axes[1]
        
        mag = self.trajectory['gamma_magnitude'].values
        ax2.plot(days, mag, 'b-', linewidth=2, label='|γ_self(n)|')
        ax2.axhline(abs(self.gamma_self0), color='orange', linestyle='--', linewidth=1.5, 
                   label=f'|γ_self0| = {abs(self.gamma_self0):.2f}')
        
        # Annotate final magnitude
        ax2.plot(days[-1], mag[-1], 'r*', markersize=12, markeredgecolor='black')
        ax2.text(days[-1], mag[-1], f'  {mag[-1]:.2f}', fontsize=10, va='center')
        
        ax2.set_xlabel('Day', fontsize=11)
        ax2.set_ylabel('|γ_self| Magnitude', fontsize=11)
        ax2.set_title(f'Love Magnitude: {self.name}', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc='best', fontsize=9)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Figure saved: {save_path}")
        
        if show:
            plt.show()
    
    def summary(self):
        """Print trajectory summary statistics."""
        if len(self.trajectory) == 0:
            raise ValueError("No trajectory data. Run scenario first.")
        
        print(f"\n{'='*60}")
        print(f"Scenario: {self.name}")
        print(f"{'='*60}")
        print(f"Initial condition: γ_self0 = {self.gamma_self0.real:.2f} + {self.gamma_self0.imag:.2f}i")
        print(f"Duration: {self.trajectory['day'].iloc[-1]} days")
        print(f"Events: {len(self.trajectory)}")
        print(f"\nWeights used:")
        for k, v in self.weights.items():
            print(f"  {k} = {v}")
        
        print(f"\n--- Trajectory Summary ---")
        start = self.gamma_self_history[0]
        end = self.gamma_self_history[-1]
        
        print(f"Start:  γ_self(0) = {start.real:.2f} + {start.imag:.2f}i  (|γ| = {abs(start):.2f})")
        print(f"End:    γ_self(N) = {end.real:.2f} + {end.imag:.2f}i  (|γ| = {abs(end):.2f})")
        print(f"Delta:  Δγ = {(end - start).real:.2f} + {(end - start).imag:.2f}i  (Δ|γ| = {abs(end) - abs(start):.2f})")
        
        # Quadrant analysis
        final_x = end.real
        final_y = end.imag
        
        if final_x >= 0 and final_y >= 0:
            quadrant = "Q1 (We + Love)"
        elif final_x < 0 and final_y >= 0:
            quadrant = "Q2 (Ego + Love)"
        elif final_x < 0 and final_y < 0:
            quadrant = "Q3 (Ego + Hate)"
        else:
            quadrant = "Q4 (We + Hate)"
        
        print(f"\nFinal quadrant: {quadrant}")
        
        # Primitive statistics
        print(f"\n--- Primitive Statistics (human scale) ---")
        for prim in ['v', 'r', 'f', 'a', 'S']:
            col = f'{prim}_raw'
            mean = self.trajectory[col].mean()
            std = self.trajectory[col].std()
            min_val = self.trajectory[col].min()
            max_val = self.trajectory[col].max()
            print(f"{prim}: mean={mean:.1f}, std={std:.1f}, range=[{min_val:.1f}, {max_val:.1f}]")
        
        print(f"{'='*60}\n")


def main():
    """Example: run steady_positive_growth scenario."""
    
    # Example scenario path
    csv_path = "data/steady_positive_growth.csv"
    
    # Initialize runner
    runner = ScenarioRunner(
        csv_path=csv_path,
        gamma_self0=0.0 + 0.0j,  # Start at origin
        name="Steady Positive Growth"
    )
    
    # Run scenario
    print(f"Running scenario: {csv_path}")
    trajectory = runner.run()
    
    # Print summary
    runner.summary()
    
    # Plot
    save_path = f"results/{runner.name.replace(' ', '_')}_trajectory.png"
    runner.plot(save_path=save_path, show=True)
    
    # Save trajectory data
    output_csv = f"results/{runner.name.replace(' ', '_')}_trajectory.csv"
    trajectory.to_csv(output_csv, index=False)
    print(f"Trajectory saved: {output_csv}")


if __name__ == "__main__":
    main()

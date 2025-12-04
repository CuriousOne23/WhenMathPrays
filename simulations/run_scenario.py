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
        # Try to read with first row as potential metadata (name row)
        with open(self.csv_path, 'r') as f:
            first_line = f.readline().strip()
            # Check if first line is metadata (name,value format)
            if first_line.startswith('name,'):
                # Extract name from metadata row
                csv_name = first_line.split(',', 1)[1].strip()
                if self.name == self.csv_path.stem:  # Only override if using default
                    self.name = csv_name
                # Read CSV starting from second line (skip metadata)
                df = pd.read_csv(self.csv_path, skiprows=1)
            else:
                # Normal CSV, no metadata row
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
                'notes': row.get('notes', ''),
                'marker': row.get('marker', '')
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
        
        # Plot custom markers from CSV
        marker_map = {
            'star': '*',
            'circle': 'o',
            'square': 's',
            'triangle': '^',
            'diamond': 'D',
            'x': 'x',
            'plus': '+'
        }
        
        for idx, row in self.trajectory.iterrows():
            marker_id = row.get('marker', '')
            if marker_id and str(marker_id).strip():  # Check if marker is specified
                marker_style = marker_map.get(str(marker_id).lower(), '*')  # Default to star
                ax1.plot(row['gamma_x'], row['gamma_y'], marker=marker_style, 
                        markersize=14, color='yellow', markeredgecolor='black', 
                        markeredgewidth=2, zorder=10)
                # Add day label near the marker
                ax1.annotate(f"Day {int(row['day'])}", 
                           xy=(row['gamma_x'], row['gamma_y']),
                           xytext=(5, 5), textcoords='offset points',
                           fontsize=9, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
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
        
        # Set axis limits to zoom on data with 15% margin
        x_min, x_max = x.min(), x.max()
        y_min, y_max = y.min(), y.max()
        x_range = x_max - x_min
        y_range = y_max - y_min
        margin = 0.15  # 15% margin
        
        ax1.set_xlim(x_min - margin * x_range, x_max + margin * x_range)
        ax1.set_ylim(y_min - margin * y_range, y_max + margin * y_range)
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


def detect_pair(csv_path: str) -> tuple:
    """
    Detect if M1/M2 pair exists.
    
    Args:
        csv_path: Path to one of the CSV files
        
    Returns:
        (m1_path, m2_path) if pair exists, (None, None) otherwise
    """
    path = Path(csv_path)
    stem = path.stem
    parent = path.parent
    
    # Check if this file is M1 or M2
    if stem.endswith('_M1'):
        base = stem[:-3]
        m1_path = path
        m2_path = parent / f"{base}_M2.csv"
        if m2_path.exists():
            return (str(m1_path), str(m2_path))
    elif stem.endswith('_M2'):
        base = stem[:-3]
        m2_path = path
        m1_path = parent / f"{base}_M1.csv"
        if m1_path.exists():
            return (str(m1_path), str(m2_path))
    
    return (None, None)


def plot_dual_scenario(m1_path: str, m2_path: str, 
                       gamma_self0_m1: complex = DEFAULT_GAMMA_SELF0,
                       gamma_self0_m2: complex = DEFAULT_GAMMA_SELF0,
                       weights: dict = None,
                       save_path: str = None,
                       show: bool = True):
    """
    Plot combined γ_self trajectories for M1 and M2.
    
    Args:
        m1_path: Path to M1 CSV file
        m2_path: Path to M2 CSV file
        gamma_self0_m1: Initial position for M1
        gamma_self0_m2: Initial position for M2
        weights: Optional weight dictionary
        save_path: Optional path to save combined plot
        show: Whether to display plot
    """
    # Run both scenarios
    runner_m1 = ScenarioRunner(m1_path, gamma_self0_m1, weights)
    runner_m2 = ScenarioRunner(m2_path, gamma_self0_m2, weights)
    
    runner_m1.run()
    runner_m2.run()
    
    # Create combined plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Combined γ_self trajectory
    ax1 = axes[0]
    
    # M1 trajectory (blue)
    x1 = runner_m1.trajectory['gamma_x'].values
    y1 = runner_m1.trajectory['gamma_y'].values
    days1 = runner_m1.trajectory['day'].values
    
    ax1.plot(x1, y1, 'b-', alpha=0.3, linewidth=1, label=runner_m1.name or 'M1')
    ax1.scatter(x1, y1, c='blue', s=50, alpha=0.7, edgecolors='black', linewidths=0.5)
    ax1.plot(x1[0], y1[0], 'bo', markersize=12, markeredgecolor='black', label=f'{runner_m1.name or "M1"} Start')
    ax1.plot(x1[-1], y1[-1], 'b*', markersize=15, markeredgecolor='black', label=f'{runner_m1.name or "M1"} End')
    
    # M2 trajectory (red)
    x2 = runner_m2.trajectory['gamma_x'].values
    y2 = runner_m2.trajectory['gamma_y'].values
    days2 = runner_m2.trajectory['day'].values
    
    ax1.plot(x2, y2, 'r-', alpha=0.3, linewidth=1, label=runner_m2.name or 'M2')
    ax1.scatter(x2, y2, c='red', s=50, alpha=0.7, edgecolors='black', linewidths=0.5)
    ax1.plot(x2[0], y2[0], 'ro', markersize=12, markeredgecolor='black', label=f'{runner_m2.name or "M2"} Start')
    ax1.plot(x2[-1], y2[-1], 'r*', markersize=15, markeredgecolor='black', label=f'{runner_m2.name or "M2"} End')
    
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
    
    # Use base name (without M1/M2 suffix) for title
    base_name = Path(m1_path).stem[:-3] if Path(m1_path).stem.endswith('_M1') else 'Dual Scenario'
    ax1.set_title(f'γ_self Trajectories: {base_name}', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.2)
    ax1.legend(loc='upper left', fontsize=8)
    
    # Set axis limits to zoom on data with margin
    all_x = np.concatenate([x1, x2])
    all_y = np.concatenate([y1, y2])
    x_min, x_max = all_x.min(), all_x.max()
    y_min, y_max = all_y.min(), all_y.max()
    x_range = x_max - x_min
    y_range = y_max - y_min
    margin = 0.15
    
    ax1.set_xlim(x_min - margin * x_range, x_max + margin * x_range)
    ax1.set_ylim(y_min - margin * y_range, y_max + margin * y_range)
    ax1.set_aspect('equal', adjustable='box')
    
    # Right: Magnitude comparison over time
    ax2 = axes[1]
    
    mag1 = runner_m1.trajectory['gamma_magnitude'].values
    mag2 = runner_m2.trajectory['gamma_magnitude'].values
    
    ax2.plot(days1, mag1, 'b-', linewidth=2, label=f'{runner_m1.name or "M1"} |γ_self|')
    ax2.plot(days2, mag2, 'r-', linewidth=2, label=f'{runner_m2.name or "M2"} |γ_self|')
    
    ax2.plot(days1[-1], mag1[-1], 'b*', markersize=12, markeredgecolor='black')
    ax2.plot(days2[-1], mag2[-1], 'r*', markersize=12, markeredgecolor='black')
    
    ax2.text(days1[-1], mag1[-1], f'  {mag1[-1]:.2f}', fontsize=10, va='center', color='blue')
    ax2.text(days2[-1], mag2[-1], f'  {mag2[-1]:.2f}', fontsize=10, va='center', color='red')
    
    ax2.set_xlabel('Day', fontsize=11)
    ax2.set_ylabel('|γ_self| Magnitude', fontsize=11)
    ax2.set_title(f'Love Magnitude Comparison', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='best', fontsize=9)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Combined figure saved: {save_path}")
    
    if show:
        plt.show()
    
    return (runner_m1, runner_m2)


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

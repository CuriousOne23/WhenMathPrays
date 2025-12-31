# scenarios/runner.py
"""
Execution engine for GRP scenario scripts.
Runs validated scenario configurations.
"""

import sys
from pathlib import Path
from typing import Dict, Any
import copy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from simulations.run_scenario import ScenarioRunner
from core.love import DEFAULT_WEIGHTS
from scenarios.config_schema import CSV_TIME_COLUMN_ALIASES


def run_scenario(config: Dict[str, Any]):
    """
    Execute scenario with validated configuration.
    
    Args:
        config: Validated configuration dictionary from scenario script
    """
    scenario_name = config['SCENARIO_NAME']
    subjects = config['SUBJECTS']
    time_unit = config.get('TIME_UNIT', 'days')
    time_scale = config.get('TIME_SCALE', 1.0)
    save_plots = config.get('SAVE_PLOTS', True)
    show_plots = config.get('SHOW_PLOTS', False)
    output_dir = Path(config.get('OUTPUT_DIR', 'results'))
    
    # Print scenario header
    print("=" * 70)
    print(f"SCENARIO: {scenario_name}")
    if 'AUTHOR' in config:
        print(f"Author: {config['AUTHOR']}", end="")
    if 'DATE_CREATED' in config:
        print(f" | Date: {config['DATE_CREATED']}")
    else:
        print()
    print("=" * 70)
    
    # Print docstring if available (background/research question)
    if '__doc__' in config and config['__doc__']:
        doc = config['__doc__']
        # Extract content between === markers if present
        if '===' in doc:
            parts = doc.split('===')
            if len(parts) >= 3:
                print(parts[1].strip())
                print("=" * 70)
    
    print()
    
    # Run each subject
    results = []
    runners = []
    
    for subject in subjects:
        print(f"Running: {subject['name']}")
        print(f"  CSV: {subject['csv_file']}")
        print(f"  Time: {time_unit} (scale: {time_scale}x)")
        print(f"  Initial γ_self: {subject['gamma_self_0']}")
        
        # Build weights
        weights = copy.copy(DEFAULT_WEIGHTS)
        if subject.get('custom_weights'):
            weights.update(subject['custom_weights'])
            print(f"  Custom weights: {list(subject['custom_weights'].keys())}")
        else:
            print(f"  Weights: All defaults from CONSTANTS.md")
        
        # Create runner
        runner = ScenarioRunner(
            csv_path=subject['csv_file'],
            gamma_self0=subject['gamma_self_0'],
            weights=weights,
            name=f"{scenario_name} - {subject['name']}"
        )
        
        # Override time unit in runner
        runner.time_unit = time_unit
        
        # Run simulation
        trajectory = runner.run()
        
        # Store results
        results.append({
            'subject': subject,
            'runner': runner,
            'trajectory': trajectory,
            'final_gamma': trajectory[-1]['gamma_self'],
            'final_magnitude': trajectory[-1]['gamma_magnitude'],
        })
        runners.append(runner)
        
        # Print summary
        final = trajectory[-1]
        quadrant = get_quadrant(final['gamma_self'])
        print(f"  ✓ Complete. Final γ_self: {final['gamma_self']:.2f}")
        print(f"    |γ_self|: {final['gamma_magnitude']:.2f}, Quadrant: {quadrant}")
        print()
    
    # Create plots
    if save_plots or show_plots:
        create_output_dir(output_dir)
        
        if len(subjects) == 1:
            # Single subject plot
            plot_single_subject(runners[0], output_dir, scenario_name, save_plots, show_plots)
        else:
            # Comparison plot
            plot_comparison(runners, subjects, output_dir, scenario_name, save_plots, show_plots)
    
    # Final summary
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    for i, result in enumerate(results):
        subject_name = result['subject']['name']
        final_gamma = result['final_gamma']
        final_mag = result['final_magnitude']
        quadrant = get_quadrant(final_gamma)
        
        print(f"{subject_name}:")
        print(f"  Final γ_self: {final_gamma:.2f}")
        print(f"  Final |γ_self|: {final_mag:.2f}")
        print(f"  Quadrant: {quadrant}")
    
    if save_plots:
        safe_name = sanitize_filename(scenario_name)
        output_file = output_dir / f"{safe_name}.png"
        print(f"\nPlot saved to: {output_file}")
    
    print("=" * 70)


def plot_single_subject(runner: ScenarioRunner, output_dir: Path, 
                       scenario_name: str, save: bool, show: bool):
    """Create plot for single subject."""
    # Use the existing plot method from ScenarioRunner
    runner.plot(save=save, show=show)


def plot_comparison(runners: list, subjects: list, output_dir: Path,
                   scenario_name: str, save: bool, show: bool):
    """Create comparison plot for multiple subjects."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(scenario_name, fontsize=16, fontweight='bold')
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(runners)))
    
    # Plot each subject's trajectory
    for i, (runner, subject) in enumerate(zip(runners, subjects)):
        color = colors[i]
        name = subject['name']
        traj = runner.trajectory
        
        # Extract data
        days = [row['day'] for row in traj]
        gamma_x = [row['gamma_x'] for row in traj]
        gamma_y = [row['gamma_y'] for row in traj]
        gamma_mag = [row['gamma_magnitude'] for row in traj]
        
        # 1. Complex plane trajectory
        ax1.plot(gamma_x, gamma_y, 'o-', color=color, label=name, alpha=0.7, linewidth=2)
        ax1.plot(gamma_x[0], gamma_y[0], 'o', color=color, markersize=12, 
                markeredgecolor='black', markeredgewidth=2, label=f'{name} start')
        ax1.plot(gamma_x[-1], gamma_y[-1], 's', color=color, markersize=12,
                markeredgecolor='black', markeredgewidth=2, label=f'{name} end')
        
        # 2. Magnitude over time
        ax2.plot(days, gamma_mag, 'o-', color=color, label=name, linewidth=2)
        
        # 3. Real (Ego/We) over time
        ax3.plot(days, gamma_x, 'o-', color=color, label=name, linewidth=2)
        
        # 4. Imaginary (Hate/Love) over time
        ax4.plot(days, gamma_y, 'o-', color=color, label=name, linewidth=2)
    
    # Configure axes
    # Complex plane
    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    ax1.axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    ax1.set_xlabel('Alone ↔ Together', fontsize=12)
    ax1.set_ylabel('Connection ↔ Disconnection', fontsize=12)
    ax1.set_title('γ-space Trajectory', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Magnitude
    ax2.set_xlabel(f'Time ({runner.time_unit})', fontsize=12)
    ax2.set_ylabel('|γ_self| Magnitude', fontsize=12)
    ax2.set_title('Love Magnitude Over Time', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Real component
    ax3.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    ax3.set_xlabel(f'Time ({runner.time_unit})', fontsize=12)
    ax3.set_ylabel('Real Component (Ego ← → We)', fontsize=12)
    ax3.set_title('Ego/We Axis Over Time', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # Imaginary component
    ax4.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    ax4.set_xlabel(f'Time ({runner.time_unit})', fontsize=12)
    ax4.set_ylabel('Imaginary Component (Hate ← → Love)', fontsize=12)
    ax4.set_title('Hate/Love Axis Over Time', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save:
        safe_name = sanitize_filename(scenario_name)
        output_file = output_dir / f"{safe_name}.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Comparison plot saved: {output_file}")
    
    if show:
        plt.show()
    else:
        plt.close()


def get_quadrant(gamma: complex) -> str:
    """Determine which quadrant a complex number is in."""
    if gamma.real >= 0 and gamma.imag >= 0:
        return "Q1 (We/Love)"
    elif gamma.real < 0 and gamma.imag >= 0:
        return "Q2 (Ego/Love)"
    elif gamma.real < 0 and gamma.imag < 0:
        return "Q3 (Ego/Hate)"
    else:
        return "Q4 (We/Hate)"


def sanitize_filename(name: str) -> str:
    """Convert scenario name to safe filename."""
    safe = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
    return safe.replace(' ', '_')


def create_output_dir(path: Path):
    """Create output directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)

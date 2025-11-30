# tests/compute_love_magnitude.py
# Computes love magnitude from γ_self trajectory data using canonical UREP equation
# with scenario-specific tuning parameters documented in docs/scenarios/Singles_Dating_to_Love/TUNING.md

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

DATA_DIR = Path("data")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

# Canonical constants from CONSTANTS.md (locked November 2025)
BETA = 1.30          # Resonance base per saturated primitive (locked)
W_CAP = 3.0          # Hard ceiling on spike: min(β^k, W_cap) (locked)
ALPHA = 1.80         # Gate gain for all enacted primitives (LOCKED by Grok's 212k Monte Carlo validation)
DELTA_S = 0.010      # Natural entropy rate (day^-1) (locked)
TAU_DEFAULT = 14     # Default memory window (days) (locked)

# Scenario-specific tuning (Singles Dating to Love)
# See docs/scenarios/Singles_Dating_to_Love/TUNING.md for full rationale and validation
PRIMITIVE_SCALE = 0.6  # Scale primitives from [-10,+10] to effective [-6,+6]
                       # Reason: Bridges intuitive 0-10 authoring to calibrated α=1.80 gates
                       # Verified: Produces L_mag=140-157 at day 60 (within 80-250 target)
                       # Date: 2025-11-29

C_BREATH = 0.01        # Breath efficacy (reference value in CONSTANTS.md is 0.40, NOT locked)
                       # Reason: Prevents entropy explosion with S=10 over 60 days
                       # Reference c=0.40 produces exp(3.4)≈30x, yielding L_mag>80,000
                       # c=0.01 produces exp(-0.5)≈0.6x, keeping values in empirical range
                       # Date: 2025-11-29
                       # Status: c appears scenario-duration-dependent, unlike locked α=1.80

def G_x(x: np.ndarray) -> np.ndarray:
    return 2 * x * np.exp(ALPHA * (x - 0.5))

def load_gamma_csv_with_params(filepath):
    # Accept either string or Path object
    path = Path(filepath) if not isinstance(filepath, Path) else filepath
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    # Extract beta_S, s_S, and optional Name from header lines
    beta_S = None
    s_S = None
    entity_name = None
    header_idx = 0
    
    for i, line in enumerate(lines):
        if line.startswith('beta_S\t'):
            beta_S = float(line.split('\t')[1])
        elif line.startswith('s_S\t'):
            s_S = float(line.split('\t')[1])
        elif line.startswith('Name\t'):
            parts = line.split('\t')
            if len(parts) > 1 and parts[1].strip():
                entity_name = parts[1].strip()
        elif line.startswith('Day\t'):
            header_idx = i
            break
    
    # Read data from header line onwards
    data_lines = '\n'.join(lines[header_idx:])
    from io import StringIO
    df = pd.read_csv(StringIO(data_lines), sep='\t')
    # Convert numeric columns (ignore override_flag if present)
    numeric_cols = ["Day", "M1_x", "M1_y", "M2_x", "M2_y", "Visibility v(t)", "Resonance r(t)", 
                    "Fidelity f(t)", "Alturism a(t)", "Shared Breth S(t)"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Day"]).reset_index(drop=True)
    # Drop override_flag column if present (not used in computation)
    if 'override_flag' in df.columns:
        df = df.drop(columns=['override_flag'])
    
    # Determine entity from column names
    if 'M1_x' in df.columns:
        entity = 'M1'
    elif 'M2_x' in df.columns:
        entity = 'M2'
    else:
        entity = 'M1'  # fallback
    
    # Use entity_name if provided, otherwise default to M1/M2
    if entity_name is None:
        entity_name = entity
    
    return df, beta_S, s_S, entity_name

def load_gamma_csv(filepath):
    # Accept either string or Path object
    path = Path(filepath) if not isinstance(filepath, Path) else filepath
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    # Parse optional Name line
    entity_name = None
    header_idx = 0
    
    for i, line in enumerate(lines):
        if line.startswith('Name\t'):
            parts = line.split('\t')
            if len(parts) > 1 and parts[1].strip():
                entity_name = parts[1].strip()
        elif line.startswith('Day\t'):
            header_idx = i
            break
    
    data_lines = '\n'.join(lines[header_idx:])
    from io import StringIO
    df = pd.read_csv(StringIO(data_lines), sep='\t')
    numeric_cols = ["Day", "M1_x", "M1_y", "M2_x", "M2_y", "Visibility v(t)", "Resonance r(t)", 
                    "Fidelity f(t)", "Alturism a(t)", "Shared Breth S(t)"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Day"]).reset_index(drop=True)
    # Drop override_flag column if present (not used in computation)
    if 'override_flag' in df.columns:
        df = df.drop(columns=['override_flag'])
    
    # Determine entity from column names
    if 'M1_x' in df.columns:
        entity = 'M1'
    elif 'M2_x' in df.columns:
        entity = 'M2'
    else:
        entity = 'M1'  # fallback
    
    # Use entity_name if provided, otherwise default to M1/M2
    if entity_name is None:
        entity_name = entity
    
    return df, entity_name

def compute_love_magnitude(scenario_name: str, m1_file=None, m2_file=None):
    # If file paths not provided, construct them (legacy behavior)
    if m1_file is None or m2_file is None:
        scenario_dir = DATA_DIR / scenario_name
        m1_file = scenario_dir / f"{scenario_name}_M1_gamma_self_table.csv"
        m2_file = scenario_dir / f"{scenario_name}_M2_gamma_self_table.csv"
    
    m1, beta_S, s_S, m1_name = load_gamma_csv_with_params(m1_file)
    m2, m2_name = load_gamma_csv(m2_file)

    # Auto-detect scenario characteristics from data
    days_m1 = m1["Day"].values
    days_m2 = m2["Day"].values
    all_days = np.concatenate([days_m1, days_m2])
    total_duration = all_days.max() - all_days.min()
    num_points = len(m1)  # Assume M1 and M2 have same number of points
    
    # Adaptive entropy parameters based on scenario duration
    # For long-term relationships, shared breaths should counterbalance decay more effectively
    if total_duration > 365:  # Multi-year scenarios
        c_breath = 0.30  # Balanced breath efficacy (prevents exponential growth)
        print(f"Long-term scenario detected ({total_duration:.0f} days): using C_BREATH={c_breath}")
    elif total_duration > 100:  # Medium-term (100-365 days)
        c_breath = 0.10
        print(f"Medium-term scenario detected ({total_duration:.0f} days): using C_BREATH={c_breath}")
    else:  # Short-term (<100 days)
        c_breath = C_BREATH  # Use default 0.01
    
    # Calculate sampling interval (delta days between events)
    if len(days_m1) > 1:
        delta_days = days_m1[1] - days_m1[0]
    else:
        delta_days = 7  # Default to weekly
    
    # Determine marker interval category based on delta_days
    # Round to nearest standard interval for labeling
    if delta_days <= 1.5:
        marker_label = "Daily"
        marker_stride = max(1, int(total_duration / 100))  # Show ~100 markers max
    elif delta_days <= 10:
        marker_label = "Weekly"
        marker_stride = max(1, num_points // 15)  # Show ~15 markers for readability
    elif delta_days <= 45:
        marker_label = "Monthly"
        marker_stride = max(1, num_points // 12)  # Show ~12 markers
    else:
        marker_label = "Yearly"
        marker_stride = max(1, num_points // 10)  # Show ~10 markers

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19, 8), facecolor='white')

    # γ_self - auto-range to actual data with generous margins for clearance
    all_x = pd.concat([m1["M1_x"], m2["M2_x"]])
    all_y = pd.concat([m1["M1_y"], m2["M2_y"]])
    x_min, x_max = all_x.min(), all_x.max()
    y_min, y_max = all_y.min(), all_y.max()
    
    # Apply generous margin (25%) on all sides for plot clearance
    x_range = x_max - x_min
    y_range = y_max - y_min
    margin = 0.25
    
    x_lim_min = x_min - x_range * margin
    x_lim_max = x_max + x_range * margin
    y_lim_min = y_min - y_range * margin
    y_lim_max = y_max + y_range * margin

    for df, label, color, display_name in [(m1, "M1", "#008080", m1_name), (m2, "M2", "#D2691E", m2_name)]:
        x_col = "M1_x" if label == "M1" else "M2_x"
        y_col = "M1_y" if label == "M1" else "M2_y"
        ax1.plot(df[x_col], df[y_col], 'o-', color=color, label=display_name, linewidth=4, markersize=9)
        
        # Adaptive day labeling - only show every Nth point to avoid overlap
        for idx, row in df.iterrows():
            if idx % marker_stride == 0 or idx == len(df) - 1:  # Always show first and last
                ax1.text(row[x_col] + 0.05, row[y_col], str(int(row["Day"])),
                         fontsize=11, color=color, weight='bold')

    ax1.set_xlabel("← Ego          We →", fontsize=16, weight='bold')
    ax1.set_ylabel("← Hate          Love →", fontsize=16, weight='bold')
    ax1.set_title(f"γ_self Trajectory — {scenario_name.replace('_', ' ')}", fontsize=18, pad=20)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=14)
    # Set limits first, then apply equal aspect ratio with adjustable box
    ax1.set_xlim(x_lim_min, x_lim_max)
    ax1.set_ylim(y_lim_min, y_lim_max)
    ax1.set_aspect('equal', adjustable='box')

    # Love magnitude: L(t) = |γ_self(t)| × W(t) × entropy_term
    max_love = 0
    min_love = 0
    for df, label, color, display_name in [(m1, "M1", "#008080", m1_name), (m2, "M2", "#D2691E", m2_name)]:
        # Primitives: scale from [-10,+10] to [0,1]
        # Apply PRIMITIVE_SCALE to moderate extreme values
        # +10 = strongly for, 0 = neutral, -10 = strongly against
        v = np.clip((df["Visibility v(t)"] * PRIMITIVE_SCALE + 10) / 20.0, 0, 1)
        r = np.clip((df["Resonance r(t)"] * PRIMITIVE_SCALE + 10) / 20.0, 0, 1)
        f = np.clip((df["Fidelity f(t)"] * PRIMITIVE_SCALE + 10) / 20.0, 0, 1)
        a = np.clip((df["Alturism a(t)"] * PRIMITIVE_SCALE + 10) / 20.0, 0, 1)
        S = df["Shared Breth S(t)"].fillna(0).astype(int)
        
        # W(t) = product of gated primitives × spike × G_S
        # Using 4 fast primitives (v,r,f,a) - breath handled via G_S
        primitives = np.column_stack([v, r, f, a])
        k = np.sum(primitives >= 0.98, axis=1)
        spike = np.minimum(BETA**k, W_CAP)
        G_S_val = 1 + beta_S * (1 - np.exp(-S / s_S))
        W = np.prod(G_x(primitives), axis=1) * spike * G_S_val
        
        # γ_self magnitude from (M_x, M_y) vector
        x_col = "M1_x" if label == "M1" else "M2_x"
        y_col = "M1_y" if label == "M1" else "M2_y"
        gamma_self_mag = np.sqrt(df[x_col]**2 + df[y_col]**2)
        
        # Entropy term: exp(-ΔS·t + c·N_breath)
        # Note: c = 0.40 is very strong; may need scenario-specific tuning
        entropy = np.exp(-DELTA_S * df["Day"] + c_breath * S)
        
        # Sign from γ_self y-component (love/hate axis)
        # Positive y = love, negative y = hate
        love_sign = np.sign(df[y_col])
        
        # Final love magnitude (signed to preserve love/hate direction)
        L_mag = love_sign * gamma_self_mag * W * entropy
        
        # Debug: print day 60 values
        if len(df) > 0:
            last_idx = len(df) - 1
            G_x_prod = np.prod(G_x(primitives), axis=1)[last_idx]
            print(f"{display_name} Day {df['Day'].iloc[last_idx]:.0f}: primitives=[{v[last_idx]:.2f},{r[last_idx]:.2f},{f[last_idx]:.2f},{a[last_idx]:.2f}], G_x_prod={G_x_prod:.4f}, spike={spike[last_idx]:.4f}, G_S={G_S_val[last_idx]:.4f}, W={W[last_idx]:.4f}, γ_self_mag={gamma_self_mag.iloc[last_idx]:.4f}, entropy={entropy[last_idx]:.4f}, L_mag={L_mag[last_idx]:.4f}")
        
        max_love = max(max_love, L_mag.max())
        min_love = min(min_love, L_mag.min())
        ax2.plot(df["Day"], L_mag, 'o-', color=color, label=display_name, linewidth=4, markersize=9)

    ax2.set_xlabel("Day", fontsize=16)
    ax2.set_ylabel("Signed Love Magnitude\n(+Love / -Hate)", fontsize=16, weight='bold')
    ax2.set_title(f"Signed Love Magnitude vs Time — {scenario_name.replace('_', ' ')}", fontsize=18, pad=20)
    ax2.axhline(0, color='black', linewidth=1.5, linestyle='-', alpha=0.5)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=14)
    # Set y-axis dynamically based on actual data range (not symmetric)
    y_max = max(max_love * 1.15, 10) if max_love > 0 else 10  # Margin above highest positive
    y_min = min(min_love * 1.15, -10) if min_love < 0 else 0  # Margin below lowest negative, or 0 if all positive
    ax2.set_ylim(y_min, y_max)
    ax2.margins(y=0.1)

    # Adaptive event markers - only show if scenario is short enough
    if total_duration <= 100:
        # Show detailed event markers for short scenarios (Singles Dating pattern)
        events = [(0,"Initial"),(7,"First date"),(14,"Wobble"),(21,"Repair"),(28,"Rhythm"),
                  (35,"Complete"),(42,"Stable"),(49,"Steady"),(56,"Plateau"),(60,"Outcome")]
        for day, txt in events:
            if day <= total_duration:  # Only show events within scenario duration
                ax2.axvline(day, color='gray', linestyle='--', alpha=0.8)
                ax2.text(day, -0.02, txt, rotation=90, va='top', ha='center',
                         fontsize=10, transform=ax2.get_xaxis_transform(),
                         bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))
    else:
        # For long scenarios, show milestone markers at data points
        milestone_indices = list(range(0, num_points, max(1, num_points // 8)))  # ~8 milestones
        if (num_points - 1) not in milestone_indices:
            milestone_indices.append(num_points - 1)  # Always include last
        
        for idx in milestone_indices:
            day = days_m1[idx]
            ax2.axvline(day, color='gray', linestyle='--', alpha=0.5)
            # Label with day number
            ax2.text(day, -0.02, f"Day {int(day)}", rotation=90, va='top', ha='center',
                     fontsize=9, transform=ax2.get_xaxis_transform(),
                     bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))

    plt.tight_layout()
    plt.savefig(RESULTS_DIR / f"{scenario_name.replace('_', ' ')}.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("SUCCESS — plot saved to results/")
    
    # Generate CSV output table
    output_rows = []
    for df, label, display_name in [(m1, "M1", m1_name), (m2, "M2", m2_name)]:
        # Recalculate love magnitude for CSV
        v = np.clip((df["Visibility v(t)"] * PRIMITIVE_SCALE + 10) / 20.0, 0, 1)
        r = np.clip((df["Resonance r(t)"] * PRIMITIVE_SCALE + 10) / 20.0, 0, 1)
        f = np.clip((df["Fidelity f(t)"] * PRIMITIVE_SCALE + 10) / 20.0, 0, 1)
        a = np.clip((df["Alturism a(t)"] * PRIMITIVE_SCALE + 10) / 20.0, 0, 1)
        S = df["Shared Breth S(t)"].fillna(0).astype(int)
        
        primitives = np.column_stack([v, r, f, a])
        k = np.sum(primitives >= 0.98, axis=1)
        spike = np.minimum(BETA**k, W_CAP)
        G_S_val = 1 + beta_S * (1 - np.exp(-S / s_S))
        W = np.prod(G_x(primitives), axis=1) * spike * G_S_val
        
        x_col = "M1_x" if label == "M1" else "M2_x"
        y_col = "M1_y" if label == "M1" else "M2_y"
        gamma_self_mag = np.sqrt(df[x_col]**2 + df[y_col]**2)
        
        entropy = np.exp(-DELTA_S * df["Day"] + c_breath * S)
        
        # Sign from γ_self y-component (love/hate axis)
        love_sign = np.sign(df[y_col])
        L_mag = love_sign * gamma_self_mag * W * entropy
        
        for idx, row in df.iterrows():
            output_rows.append({
                "Day": int(row["Day"]),
                "Entity": display_name,
                "Signed_Love_Magnitude": L_mag[idx],
                "Gamma_Self_Mag": gamma_self_mag.iloc[idx],
                "W": W[idx],
                "Entropy": entropy[idx]
            })
    
    output_df = pd.DataFrame(output_rows)
    csv_path = RESULTS_DIR / f"{scenario_name}_magnitude_table.csv"
    output_df.to_csv(csv_path, index=False)
    print(f"SUCCESS — CSV table saved to {csv_path}")

def print_help():
    """Print usage instructions."""
    print("\n" + "="*70)
    print("USAGE: python tests/compute_love_magnitude.py <scenario_name>")
    print("="*70)
    print("\nComputes signed love magnitude from γ_self trajectory data.")
    print("\nArguments:")
    print("  scenario_name    Name of scenario directory in data/")
    print("                   e.g., 'Test1_Linear', 'Single_Dating_2_Love'")
    print("\nExpected file structure:")
    print("  data/<scenario_name>/<scenario_name>_M1_gamma_self_table.csv")
    print("  data/<scenario_name>/<scenario_name>_M2_gamma_self_table.csv")
    print("\nCSV format requirements:")
    print("  - Tab-delimited")
    print("  - Optional beta_S/s_S header lines (M1 only)")
    print("  - Columns: Day, M1_x, M1_y, v(t), r(t), f(t), a(t), S(t)")
    print("  - Optional: override_flag, Notes columns (ignored)")
    print("\nOutput:")
    print("  - PNG plot: results/<scenario_name>.png")
    print("  - CSV table: results/<scenario_name>_magnitude_table.csv")
    print("\nExamples:")
    print("  python tests/compute_love_magnitude.py Test1_Linear")
    print("  python tests/compute_love_magnitude.py Single_Dating_2_Love")
    print("="*70 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        if len(sys.argv) == 1:
            print("\nERROR: No scenario name provided.\n")
        else:
            print(f"\nERROR: Expected 1 argument, got {len(sys.argv)-1}.\n")
        print_help()
        sys.exit(1)
    
    scenario_name = sys.argv[1]
    
    # Check for scenario in subdirectory (new format) or directly in data/ (legacy format)
    scenario_dir = DATA_DIR / scenario_name
    legacy_m1 = DATA_DIR / f"{scenario_name}_M1_gamma_self_table.csv"
    legacy_m2 = DATA_DIR / f"{scenario_name}_M2_gamma_self_table.csv"
    
    # Determine which format is being used
    if scenario_dir.exists() and scenario_dir.is_dir():
        # New format: files in subdirectory
        m1_csv = scenario_dir / f"{scenario_name}_M1_gamma_self_table.csv"
        m2_csv = scenario_dir / f"{scenario_name}_M2_gamma_self_table.csv"
    elif legacy_m1.exists():
        # Legacy format: files directly in data/
        m1_csv = legacy_m1
        m2_csv = legacy_m2
    else:
        # Neither format found
        print(f"\nERROR: Scenario not found: {scenario_name}")
        print(f"\nSearched for:")
        print(f"  - Subdirectory: {scenario_dir}/")
        print(f"  - Legacy files: {legacy_m1.name}, {legacy_m2.name}")
        print(f"\nAvailable scenarios:")
        # List subdirectories
        for item in sorted(DATA_DIR.iterdir()):
            if item.is_dir():
                print(f"  - {item.name}/ (subdirectory)")
        # List legacy scenario files
        legacy_scenarios = set()
        for item in DATA_DIR.glob("*_M1_gamma_self_table.csv"):
            scenario = item.name.replace("_M1_gamma_self_table.csv", "")
            legacy_scenarios.add(scenario)
        for scenario in sorted(legacy_scenarios):
            print(f"  - {scenario} (legacy format)")
        print("\n")
        sys.exit(1)
    
    # Validate scenario directory exists (skip for legacy)
    if not scenario_dir.exists() and not legacy_m1.exists():
        print(f"\nERROR: Scenario directory does not exist: {scenario_dir}")
        print(f"\nAvailable scenarios in data/:")
        for item in sorted(DATA_DIR.iterdir()):
            if item.is_dir():
                print(f"  - {item.name}")
        print("\n")
        sys.exit(1)
    
    
    # Validate CSV files exist
    if not m1_csv.exists():
        print(f"\nERROR: M1 CSV file does not exist: {m1_csv}")
        print(f"\nExpected filename: {scenario_name}_M1_gamma_self_table.csv")
        if scenario_dir.exists():
            print(f"Files in {scenario_dir}:")
            for item in sorted(scenario_dir.iterdir()):
                print(f"  - {item.name}")
        print("\n")
        sys.exit(1)
    
    if not m2_csv.exists():
        print(f"\nERROR: M2 CSV file does not exist: {m2_csv}")
        print(f"\nExpected filename: {scenario_name}_M2_gamma_self_table.csv")
        if scenario_dir.exists():
            print(f"Files in {scenario_dir}:")
            for item in sorted(scenario_dir.iterdir()):
                print(f"  - {item.name}")
        print("\n")
        sys.exit(1)
    
    # Try to compute love magnitude with validation
    try:
        compute_love_magnitude(scenario_name, m1_csv, m2_csv)
    except KeyError as e:
        print(f"\nERROR: CSV file format issue - missing required column: {e}")
        print("\nRequired CSV format:")
        print("  - Tab-delimited")
        print("  - Columns: Day, <Entity>_x, <Entity>_y, Visibility v(t),")
        print("             Resonance r(t), Fidelity f(t), Alturism a(t),")
        print("             Shared Breth S(t)")
        print("  - Optional: override_flag, Notes (ignored if present)")
        print("  - M1 file may have beta_S/s_S header lines")
        print("\n")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Failed to process scenario: {e}")
        import traceback
        traceback.print_exc()
        print("\n")
        sys.exit(1)
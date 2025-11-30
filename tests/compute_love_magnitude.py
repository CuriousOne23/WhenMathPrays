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

def load_gamma_csv_with_params(filename: str):
    path = DATA_DIR / filename
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    # Extract beta_S and s_S from first two lines
    beta_S_line = lines[0]
    s_S_line = lines[1]
    beta_S = float(beta_S_line.split('\t')[1])
    s_S = float(s_S_line.split('\t')[1])
    
    # Find header and data
    # Lines: 0=beta_S, 1=s_S, 2=blank, 3=header, 4+=data
    header_idx = 3
    data_lines = '\n'.join(lines[header_idx:])
    from io import StringIO
    df = pd.read_csv(StringIO(data_lines), sep='\t')
    # Convert numeric columns
    numeric_cols = ["Day", "M1_x", "M1_y", "Visibility v(t)", "Resonance r(t)", 
                    "Fidelity f(t)", "Alturism a(t)", "Shared Breth S(t)"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Day"]).reset_index(drop=True)
    
    return df, beta_S, s_S

def load_gamma_csv(filename: str):
    path = DATA_DIR / filename
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f.readlines()]
    data_lines = '\n'.join(lines)  # M2 has no params
    from io import StringIO
    df = pd.read_csv(StringIO(data_lines), sep='\t')
    df.columns = [col.strip() for col in df.columns]
    # Convert numeric columns
    numeric_cols = ["Day", "M2_x", "M2_y", "Visibility v(t)", "Resonance r(t)", 
                    "Fidelity f(t)", "Alturism a(t)", "Shared Breth S(t)"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Day"]).reset_index(drop=True)
    return df

def compute_love_magnitude(scenario_name: str):
    m1_file = f"{scenario_name}_M1_gamma_self_table.csv"
    m2_file = f"{scenario_name}_M2_gamma_self_table.csv"

    m1, beta_S, s_S = load_gamma_csv_with_params(m1_file)
    m2 = load_gamma_csv(m2_file)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19, 8), facecolor='white')

    # γ_self - compute data ranges to ensure (0,0) is visible
    all_x = pd.concat([m1["M1_x"], m2["M2_x"]])
    all_y = pd.concat([m1["M1_y"], m2["M2_y"]])
    x_min, x_max = all_x.min(), all_x.max()
    y_min, y_max = all_y.min(), all_y.max()
    # Ensure (0,0) is visible with some margin
    x_margin = max(abs(x_min), abs(x_max)) * 0.15
    y_margin_min = max(abs(y_min), abs(y_max)) * 0.15
    y_margin_max = max(0.5, 1.0)  # Ensure 0.5-1.0 space above highest point
    x_lim_min = min(x_min - x_margin, -0.5)
    x_lim_max = max(x_max + x_margin, 0.5)
    y_lim_min = min(y_min - y_margin_min, -0.5)
    y_lim_max = y_max + y_margin_max

    for df, label, color in [(m1, "M1", "#008080"), (m2, "M2", "#D2691E")]:
        x_col = "M1_x" if label == "M1" else "M2_x"
        y_col = "M1_y" if label == "M1" else "M2_y"
        ax1.plot(df[x_col], df[y_col], 'o-', color=color, label=label, linewidth=4, markersize=9)
        for _, row in df.iterrows():
            ax1.text(row[x_col] + 0.05, row[y_col], str(int(row["Day"])),
                     fontsize=11, color=color, weight='bold')

    ax1.set_xlabel("← Ego          We →", fontsize=16, weight='bold')
    ax1.set_ylabel("← Hate          Love →", fontsize=16, weight='bold')
    ax1.set_title(f"γ_self Trajectory — {scenario_name.replace('_', ' ')}", fontsize=18, pad=20)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=14)
    ax1.axis("equal")
    ax1.set_xlim(x_lim_min, x_lim_max)
    ax1.set_ylim(y_lim_min, y_lim_max)

    # Love magnitude: L(t) = |γ_self(t)| × W(t) × entropy_term
    max_love = 0
    min_love = 0
    for df, label, color in [(m1, "M1", "#008080"), (m2, "M2", "#D2691E")]:
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
        entropy = np.exp(-DELTA_S * df["Day"] + C_BREATH * S)
        
        # Sign from γ_self y-component (love/hate axis)
        # Positive y = love, negative y = hate
        love_sign = np.sign(df[y_col])
        
        # Final love magnitude (signed to preserve love/hate direction)
        L_mag = love_sign * gamma_self_mag * W * entropy
        
        # Debug: print day 60 values
        if len(df) > 0:
            last_idx = len(df) - 1
            G_x_prod = np.prod(G_x(primitives), axis=1)[last_idx]
            print(f"{label} Day {df['Day'].iloc[last_idx]:.0f}: primitives=[{v[last_idx]:.2f},{r[last_idx]:.2f},{f[last_idx]:.2f},{a[last_idx]:.2f}], G_x_prod={G_x_prod:.4f}, spike={spike[last_idx]:.4f}, G_S={G_S_val[last_idx]:.4f}, W={W[last_idx]:.4f}, γ_self_mag={gamma_self_mag.iloc[last_idx]:.4f}, entropy={entropy[last_idx]:.4f}, L_mag={L_mag[last_idx]:.4f}")
        
        max_love = max(max_love, L_mag.max())
        min_love = min(min_love, L_mag.min())
        ax2.plot(df["Day"], L_mag, 'o-', color=color, label=label, linewidth=4, markersize=9)

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

    # Event markers
    events = [(0,"Initial"),(7,"First date"),(14,"Wobble"),(21,"Repair"),(28,"Rhythm"),
              (35,"Complete"),(42,"Stable"),(49,"Steady"),(56,"Plateau"),(60,"Outcome")]
    for day, txt in events:
        ax2.axvline(day, color='gray', linestyle='--', alpha=0.8)
        ax2.text(day, -0.02, txt, rotation=90, va='top', ha='center',
                 fontsize=10, transform=ax2.get_xaxis_transform(),
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9))

    plt.tight_layout()
    plt.savefig(RESULTS_DIR / f"{scenario_name.replace('_', ' ')}.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("SUCCESS — plot saved to results/")
    
    # Generate CSV output table
    output_rows = []
    for df, label in [(m1, "M1"), (m2, "M2")]:
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
        
        entropy = np.exp(-DELTA_S * df["Day"] + C_BREATH * S)
        
        # Sign from γ_self y-component (love/hate axis)
        love_sign = np.sign(df[y_col])
        L_mag = love_sign * gamma_self_mag * W * entropy
        
        for idx, row in df.iterrows():
            output_rows.append({
                "Day": int(row["Day"]),
                "Entity": label,
                "Signed_Love_Magnitude": L_mag[idx],
                "Gamma_Self_Mag": gamma_self_mag.iloc[idx],
                "W": W[idx],
                "Entropy": entropy[idx]
            })
    
    output_df = pd.DataFrame(output_rows)
    csv_path = RESULTS_DIR / f"{scenario_name}_magnitude_table.csv"
    output_df.to_csv(csv_path, index=False)
    print(f"SUCCESS — CSV table saved to {csv_path}")

if __name__ == "__main__":
    compute_love_magnitude("Single_Dating_2_Love")
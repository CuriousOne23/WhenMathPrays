# tests/compute_love_magnitude.py
# FINAL — works with your current files (beta_S/s_S only in M1, no blank line)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

DATA_DIR = Path("data")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

BETA = 1.30
W_CAP = 3.0
ALPHA = 1.80
DELTA_S = 0.010

def G_x(x: np.ndarray) -> np.ndarray:
    return 2 * x * np.exp(ALPHA * (x - 0.5))

def load_gamma_csv_with_params(filename: str):
    path = DATA_DIR / filename
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    # Extract beta_S and s_S from first two lines
    beta_S_line = lines[0]
    s_S_line = lines[1]
    beta_S = float(beta_S_line.split(',')[1])
    s_S = float(s_S_line.split(',')[1])
    
    # Find header and data
    header_idx = 2  # Day line is always line 2 now (no blank)
    data_lines = '\n'.join(lines[header_idx:])
    from io import StringIO
    df = pd.read_csv(StringIO(data_lines), sep='\t')
    df.columns = [col.strip() for col in df.columns]
    df["Day"] = pd.to_numeric(df["Day"], errors="coerce")
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
    df["Day"] = pd.to_numeric(df["Day"], errors="coerce")
    df = df.dropna(subset=["Day"]).reset_index(drop=True)
    return df

def compute_love_magnitude(scenario_name: str):
    m1_file = f"{scenario_name}_M1_gamma_self_table.csv"
    m2_file = f"{scenario_name}_M2_gamma_self_table.csv"

    m1, beta_S, s_S = load_gamma_csv_with_params(m1_file)
    m2 = load_gamma_csv(m2_file)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19, 8), facecolor='white')

    # γ_self
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
    ax1.set_xlim(-3.5, 0.5)
    ax1.set_ylim(-0.5, 3.5)

    # Love magnitude
    max_love = 0
    for df, label, color in [(m1, "M1", "#008080"), (m2, "M2", "#D2691E")]:
        v = df["Visibility v(t)"] / 10.0
        r = df["Resonance r(t)"] / 10.0
        f = df["Fidelity f(t)"] / 10.0
        a = df["Alturism a(t)"] / 10.0
        S = df["Shared Breth S(t)"].astype(int)
        b = np.clip(S / 80.0, 0.0, 0.95)

        primitives = np.column_stack([v, r, f, a, b])
        k = np.sum(primitives >= 0.98, axis=1)
        spike = np.minimum(BETA**k, W_CAP)
        G_S_val = 1 + beta_S * (1 - np.exp(-S / s_S))
        W = np.prod(G_x(primitives), axis=1) * spike * G_S_val
        decay = np.exp(-DELTA_S * df["Day"])
        growth = np.exp(df[f"M{1 if label=='M1' else 2}_x"])
        L_mag = W * growth * decay

        max_love = max(max_love, L_mag.max())
        ax2.plot(df["Day"], L_mag, 'o-', color=color, label=label, linewidth=4, markersize=9)

    ax2.set_xlabel("Day", fontsize=16)
    ax2.set_ylabel("Love Magnitude", fontsize=16)
    ax2.set_title(f"Love Magnitude vs Time — {scenario_name.replace('_', ' ')}", fontsize=18)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=14)
    ax2.set_ylim(0, max_love * 1.2 + 0.05)
    ax2.margins(y=0.15)

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

if __name__ == "__main__":
    compute_love_magnitude("Single_Dating_2_Love")
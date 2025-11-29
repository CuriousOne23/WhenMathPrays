# tests/compute_love_magnitude.py
# Canonical UREP love magnitude + dual plot generator
# Works for ANY scenario — just drop M1/M2 CSVs in data/

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Paths
DATA_DIR = Path("../data")
RESULTS_DIR = Path("../results")
RESULTS_DIR.mkdir(exist_ok=True)

# Canonical constants (locked November 2025)
BETA = 1.30
W_CAP = 3.0
ALPHA = 1.80
DELTA_S = 0.010
C = 0.40
TAU_DEFAULT = 14

def G_x(x: float) -> float:
    return 2 * x * np.exp(ALPHA * (x - 0.5))

def G_S(S: int, beta_S: float = 3.0, s_S: float = 30.0) -> float:
    return 1 + beta_S * (1 - np.exp(-S / s_S))

def count_k(primitives: list) -> int:
    return sum(1 for p in primitives if p >= 0.98)

def load_gamma_csv(filename: str):
    path = DATA_DIR / filename
    df = pd.read_csv(path, skiprows=2)
    df["Day"] = pd.to_numeric(df["Day"], errors="coerce")
    df = df.dropna(subset=["Day"]).reset_index(drop=True)
    return df

def compute_love_magnitude(scenario_name: str):
    m1_file = f"{scenario_name}_M1_gamma_self_table.csv"
    m2_file = f"{scenario_name}_M2_gamma_self_table.csv"

    m1 = load_gamma_csv(m1_file)
    m2 = load_gamma_csv(m2_file)

    results = []
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    for df, label, color in [(m1, "M1", "teal"), (m2, "M2", "orange")]:
        love_vals = []
        for idx, row in df.iterrows():
            day = int(row["Day"])
            v = row["Visibility v(t)"] / 10.0
            r = row["Resonance r(t)"] / 10.0
            f = row["Fidelity f(t)"] / 10.0
            a = row["Alturism a(t)"] / 10.0
            S = int(row["Shared Breth S(t)"])

            primitives = [v, r, f, a, 0.8]  # b approximated high for dating
            k = count_k(primitives)
            W = np.prod([G_x(p) for p in primitives]) * min(BETA**k, W_CAP) * G_S(S)
            decay = np.exp(-DELTA_S * day)
            gamma_avg = complex(row[f"{label}_x"], row[f"{label}_y"])
            growth = np.exp(gamma_avg.real)
            direction = np.exp(1j * np.angle(gamma_avg))
            L = W * growth * direction * decay
            love_mag = abs(L)
            love_vals.append(love_mag)

            if label == "M1":
                results.append({
                    "Day": day,
                    "M1_Love": round(love_mag, 3),
                    "M2_Love": None,
                    "Event": row["Notes"]
                })
            else:
                results[-1]["M2_Love"] = round(love_mag, 3)

        # Plot gamma_self
        ax1.plot(df[f"{label}_x"], df[f"{label}_y"], 'o-', color=color, label=label, linewidth=3, markersize=7)
        for _, r in df.iterrows():
            ax1.text(r[f"{label}_x"] + 0.02, r[f"{label}_y"], str(int(r["Day"])), fontsize=9, color=color)

        # Plot love magnitude
        ax2.plot(df["Day"], love_vals, 'o-', color=color, label=label, linewidth=3, markersize=7)

    # Finalize love table
    love_df = pd.DataFrame(results)
    love_df.loc[love_df["M2_Love"].isna(), "M2_Love"] = love_df["M1_Love"]
    love_path = RESULTS_DIR / f"{scenario_name}_love_magnitude_table.csv"
    love_df.to_csv(love_path, index=False)

    # Finalize plots
    ax1.set_xlabel("Ego → We")
    ax1.set_ylabel("Hate → Love")
    ax1.set_title(f"γ_self Trajectory — {scenario_name.replace('_', ' ')}")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.axis("equal")
    ax1.set_xlim(-3.2, 0.2)
    ax1.set_ylim(-0.2, 0.8)

    ax2.set_xlabel("Day")
    ax2.set_ylabel("Love Magnitude")
    ax2.set_title(f"Love Magnitude vs Time — {scenario_name.replace('_', ' ')}")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xlim(0, 65)
    ax2.set_ylim(0, 0.7)

    # Event markers on right plot
    events = love_df[love_df["Day"].isin([0,7,14,21,28,35,42,49,56,60])]
    for _, e in events.iterrows():
        ax2.axvline(e["Day"], color='gray', linestyle='--', alpha=0.6)
        ax2.text(e["Day"], 0.02, e["Event"].split(":")[0], rotation=90, va='bottom', ha='center', fontsize=8)

    plt.tight_layout()
    plot_path = RESULTS_DIR / f"{scenario_name.replace('_', ' ')}.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Generated: {love_path.name}")
    print(f"Generated: {plot_path.name}")

if __name__ == "__main__":
    # Change this line for any scenario
    compute_love_magnitude("Single_Dating_2_Love")
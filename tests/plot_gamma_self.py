# tests/plot_gamma_self.py
# Plot γ_self trajectories from M1/M2 CSV files
# Works with any scenario — just drop the CSVs in data/

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

DATA_DIR = Path("../data")

def load_csv(filename: str):
    path = DATA_DIR / filename
    df = pd.read_csv(path, skiprows=2)  # skip header junk
    df["Day"] = pd.to_numeric(df["Day"], errors="coerce")
    df = df.dropna(subset=["Day"])
    return df

def plot_scenario(m1_file="M1_gamma_self_table.csv", m2_file="M2_gamma_self_table.csv", title="Singles → Dating → Love"):
    m1 = load_csv(m1_file)
    m2 = load_csv(m2_file)

    plt.figure(figsize=(12, 10))
    plt.plot(m1["M1_x"], m1["M1_y"], 'o-', color='teal', label='M1', linewidth=3, markersize=8)
    plt.plot(m2["M2_x"], m2["M2_y"], 'o-', color='orange', label='M2', linewidth=3, markersize=8)

    # Annotate days
    for _, row in m1.iterrows():
        plt.text(row["M1_x"] + 0.05, row["M1_y"], str(int(row["Day"])), fontsize=10, color='teal')
    for _, row in m2.iterrows():
        plt.text(row["M2_x"] + 0.05, row["M2_y"], str(int(row["Day"])), fontsize=10, color='orange')

    plt.xlabel("Real: Ego → We")
    plt.ylabel("Imag: Hate → Love")
    plt.title(f"γ_self Trajectory — {title}")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.axis("equal")
    plt.xlim(-3.5, 1)
    plt.ylim(-0.5, 8)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_scenario()
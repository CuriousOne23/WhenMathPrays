#!/usr/bin/env python
"""
distributions_gamma_self.py
Generates γ_self distributions + quadrant map.
Outputs (core/):
    • distributions_gamma_self_plot.png
    • distributions_gamma_self_table.md
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from typing import Dict, List
from dataclasses import dataclass
import json

# ---------- OUTPUT PATHS ----------
PLOT_OUTPUT = "core/distributions_gamma_self_plot.png"
TABLE_OUTPUT = "core/distributions_gamma_self_table.md"

# ---------- 8 CLASSIFICATIONS ----------
@dataclass
class Distribution:
    name: str
    mean: complex
    cov: np.ndarray
    color: str
    n_samples: int = 5000
    description: str = ""

DISTRIBUTIONS: Dict[str, Distribution] = {
    "buddhist": Distribution(
        name="Buddhist",
        mean=-0.1 + 0.1j,
        cov=np.array([[0.08, 0.0], [0.0, 0.08]]),
        color="#1f77b4",
        description="Tiny symmetric circle. Stillness."
    ),
    "narcissist": Distribution(
        name="Narcissist",
        mean=-10.0 + 0.0j,
        cov=np.array([[0.3, 0.0], [0.0, 0.01]]),
        color="#ff7f0e",
        description="Flat horizontal line. Pure ego."
    ),
    "ego_dating": Distribution(
        name="Ego-Dating",
        mean=-3.0 + 2.0j,
        cov=np.array([[0.3, 0.0], [0.0, 1.2]]),
        color="#2ca02c",
        description="Thin vertical oval – want them for self."
    ),
    "marriage": Distribution(
        name="Marriage",
        mean=-1.5 + 1.5j,
        cov=np.array([[1.0, 0.3], [0.3, 1.0]]),
        color="#d62728",
        description="Broad circular cloud – fused & stable."
    ),
    "parent": Distribution(
        name="Parent",
        mean=-0.5 + 1.0j,
        cov=np.array([[1.5, -0.4], [-0.4, 0.6]]),
        color="#9467bd",
        description="Teardrop – long right, short down."
    ),
    "soldier": Distribution(
        name="Soldier/Divorce",
        mean=-0.8 - 2.0j,
        cov=np.array([[0.3, 0.0], [0.0, 1.5]]),
        color="#8c564b",
        description="Vertical oval – battlefield hate."
    ),
    "unhappy": Distribution(
        name="Unhappy Marriage",
        mean=-1.2 - 0.8j,
        cov=np.array([[0.4, 0.0], [0.0, 0.4]]),
        color="#e377c2",
        description="Tight circle – quiet resentment."
    ),
    "corporate": Distribution(
        name="Corporate Employee",
        mean=-2.0 - 1.0j,
        cov=np.array([[0.8, 0.3], [0.3, 0.5]]),
        color="#7f7f7f",
        description="Skewed teardrop – cliff on hate side."
    ),
}

# ---------- SAMPLING ----------
def generate_samples(dist: Distribution) -> np.ndarray:
    mean2 = np.array([dist.mean.real, dist.mean.imag])
    return np.random.multivariate_normal(mean2, dist.cov, dist.n_samples)[:, 0] + \
           1j * np.random.multivariate_normal(mean2, dist.cov, dist.n_samples)[:, 1]

# ---------- PLOTTING ----------
def plot_distributions(selected: List[Distribution]):
    plt.figure(figsize=(14, 9))
    ax = plt.gca()

    # --- Scatter each distribution ---
    for dist in selected:
        gamma = generate_samples(dist)
        ax.scatter(gamma.real, gamma.imag, c=dist.color, s=2, alpha=0.7,
                   label=dist.name, edgecolors='none')

    # --- EXTENDED AXES ---
    ax.set_xlim(-12, 4)
    ax.set_ylim(-5, 5)

    # --- Axes & grid ---
    ax.axhline(0, color='k', lw=1.2, alpha=0.6)
    ax.axvline(0, color='k', lw=1.2, alpha=0.6)
    ax.grid(True, alpha=0.3, ls='-', lw=0.5)

    # --- QUADRANT LINES (thin dashed) ---
    ax.axhline(0, color='gray', lw=0.8, ls='--', alpha=0.7)
    ax.axvline(0, color='gray', lw=0.8, ls='--', alpha=0.7)

    # --- QUADRANT LABELS (exactly as you asked) ---
    ax.text( 1.5,  3.5, "Q1", fontsize=14, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
    ax.text(-1.5,  3.5, "Q2", fontsize=14, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
    ax.text(-1.5, -3.5, "Q3", fontsize=14, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
    ax.text( 1.5, -3.5, "Q4", fontsize=14, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))

    # --- Axis titles ---
    ax.set_xlabel("Real Axis: Ego ← → We", fontsize=13, labelpad=10)
    ax.set_ylabel("Imaginary Axis: Enmity/Hate ↓    Love ↑", fontsize=13, labelpad=12)
    ax.set_title("γ_self Distribution Patterns in Ego-We × Love-Enmity Space",
                 fontsize=15, pad=20)

    # --- LEGEND (upper-left, big markers) ---
    leg = ax.legend(loc='upper left', fontsize=11, markerscale=4,
                    title="Classifications", title_fontsize=12,
                    frameon=True, fancybox=True)
    leg.get_frame().set_facecolor('white')
    leg.get_frame().set_alpha(0.95)

    plt.tight_layout()
    os.makedirs(os.path.dirname(PLOT_OUTPUT), exist_ok=True)
    plt.savefig(PLOT_OUTPUT, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Plot saved → {PLOT_OUTPUT}")

# ---------- MARKDOWN TABLE ----------
def create_quadrant_table():
    md = (
        "## γ_self Quadrants\n\n"
        "|        | **+Im = Union, Love** |        |\n"
        "|--------|-----------------------|--------|\n"
        "| **-Re** | **Q2**                | **Q1** |\n"
        "| **+Re = We, Ego** |                       |        |\n"
        "| **-Im = Enmity, Hate** | **Q3**        | **Q4** |\n\n"
        "---\n\n"
        "### Quadrant Definitions\n"
        "- **Q1** – *We + Love* – Mature partnership, soul-mate zone  \n"
        "- **Q2** – *Ego + Love* – Ego-dating, parent-like giving  \n"
        "- **Q3** – *Ego + Hate* – Revenge, corporate resentment  \n"
        "- **Q4** – *We + Hate* – Battlefield, divorce, soldier  \n"
    )
    with open(TABLE_OUTPUT, 'w') as f:
        f.write(md)
    print(f"Quadrant table saved → {TABLE_OUTPUT}")

# ---------- CLI ----------
def parse_args():
    p = argparse.ArgumentParser(
        description="γ_self distributions + quadrant map",
        formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("classifications", nargs="+",
                   help="Space-separated list or 'all'")
    p.add_argument("--add", type=str, help="JSON for new classification")
    return p.parse_args()

def main():
    args = parse_args()

    # --- add custom ---
    if args.add:
        try:
            d = json.loads(args.add.replace("'", '"'))
            key = d["name"].lower().replace(" ", "_").replace("/", "_")
            DISTRIBUTIONS[key] = Distribution(
                name=d["name"],
                mean=complex(d["mean"]),
                cov=np.array(d["cov"]),
                color=d.get("color", "#000000"),
                description=d.get("desc", "")
            )
            print(f"Added → {d['name']}")
        except Exception as e:
            print(f"Add failed: {e}")

    # --- resolve selections ---
    sel = []
    for name in args.classifications:
        name = name.lower()
        if name == "all":
            sel = list(DISTRIBUTIONS.values())
            break
        matches = [v for k, v in DISTRIBUTIONS.items() if k.startswith(name)]
        sel.extend(matches)

    if not sel:
        print("No classifications selected.")
        return

    plot_distributions(sel)
    create_quadrant_table()

if __name__ == "__main__":
    main()